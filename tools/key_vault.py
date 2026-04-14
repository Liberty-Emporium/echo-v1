"""
key_vault.py — Encrypted API Key Storage (BYOK Pattern)
Drop this into any app. Import get_api_key() wherever you call AI or external APIs.

Setup:
  1. Add KEY_VAULT_SECRET to Railway env vars (any random 32-char string)
  2. Add the key_vault DB table (auto-created on first use)
  3. Import and use get_api_key() in your AI calls

Usage:
  from key_vault import get_api_key, save_api_key, KeyVault
  
  # Get a key (falls back to env var if user has none)
  key = get_api_key(db, tenant_id, 'openrouter')
  
  # Save a key from settings form
  save_api_key(db, tenant_id, 'openrouter', request.form.get('api_key'))
"""

import os
import base64
import hashlib
import hmac
import sqlite3
from datetime import datetime

# ── Encryption (no external deps — uses stdlib only) ──────────────────────────

def _get_master_key():
    secret = os.environ.get("KEY_VAULT_SECRET", "default-change-in-production-please")
    return hashlib.sha256(secret.encode()).digest()

def _encrypt(plaintext: str) -> str:
    """XOR encrypt with key + HMAC for integrity. Returns base64 string."""
    if not plaintext:
        return ""
    key = _get_master_key()
    data = plaintext.encode()
    # XOR with repeating key
    encrypted = bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))
    # Add HMAC for integrity check
    mac = hmac.new(key, encrypted, hashlib.sha256).digest()
    combined = mac + encrypted
    return base64.b64encode(combined).decode()

def _decrypt(ciphertext: str) -> str:
    """Decrypt and verify HMAC. Returns plaintext or empty string on failure."""
    if not ciphertext:
        return ""
    try:
        key = _get_master_key()
        combined = base64.b64decode(ciphertext.encode())
        mac = combined[:32]
        encrypted = combined[32:]
        # Verify HMAC
        expected_mac = hmac.new(key, encrypted, hashlib.sha256).digest()
        if not hmac.compare_digest(mac, expected_mac):
            return ""  # Tampered or wrong key
        # Decrypt
        decrypted = bytes(encrypted[i] ^ key[i % len(key)] for i in range(len(encrypted)))
        return decrypted.decode()
    except Exception:
        return ""

# ── DB Setup ──────────────────────────────────────────────────────────────────

def init_key_vault(db):
    """Call this in your init_db() function."""
    db.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER,
            user_id INTEGER,
            service TEXT NOT NULL,
            encrypted_key TEXT NOT NULL,
            label TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            UNIQUE(tenant_id, service)
        )
    """)
    db.commit()

# ── Core Functions ────────────────────────────────────────────────────────────

def save_api_key(db, tenant_id, service, raw_key, label=None, user_id=None):
    """
    Encrypt and save an API key for a tenant.
    service: 'openrouter', 'stripe', 'square', etc.
    """
    if not raw_key or not raw_key.strip():
        # Delete if empty (user cleared it)
        db.execute("DELETE FROM api_keys WHERE tenant_id=? AND service=?", (tenant_id, service))
        db.commit()
        return False
    
    encrypted = _encrypt(raw_key.strip())
    db.execute("""
        INSERT INTO api_keys (tenant_id, user_id, service, encrypted_key, label, updated_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        ON CONFLICT(tenant_id, service) DO UPDATE SET
            encrypted_key=excluded.encrypted_key,
            label=excluded.label,
            updated_at=excluded.updated_at
    """, (tenant_id, user_id, service, encrypted, label or service))
    db.commit()
    return True

def get_api_key(db, tenant_id, service):
    """
    Get decrypted API key for a tenant.
    Falls back to env var if tenant has none.
    
    Fallback env var names:
      openrouter  → OPENROUTER_API_KEY
      stripe      → STRIPE_SECRET_KEY
      square      → SQUARE_ACCESS_TOKEN
    """
    # Try tenant's own key first
    row = db.execute(
        "SELECT encrypted_key FROM api_keys WHERE tenant_id=? AND service=?",
        (tenant_id, service)
    ).fetchone()
    
    if row and row[0]:
        decrypted = _decrypt(row[0])
        if decrypted:
            return decrypted
    
    # Fall back to app-level env var
    fallbacks = {
        "openrouter": "OPENROUTER_API_KEY",
        "stripe":     "STRIPE_SECRET_KEY",
        "square":     "SQUARE_ACCESS_TOKEN",
        "sendgrid":   "SENDGRID_API_KEY",
        "mailgun":    "MAILGUN_API_KEY",
    }
    env_var = fallbacks.get(service, service.upper() + "_API_KEY")
    return os.environ.get(env_var, "")

def has_own_key(db, tenant_id, service):
    """Check if tenant has set their own key (for showing masked value in UI)."""
    row = db.execute(
        "SELECT encrypted_key FROM api_keys WHERE tenant_id=? AND service=?",
        (tenant_id, service)
    ).fetchone()
    return bool(row and row[0] and _decrypt(row[0]))

def mask_key(db, tenant_id, service):
    """Return masked version of key for display e.g. 'sk-••••••••••••••••3f4a'"""
    key = get_api_key(db, tenant_id, service)
    if not key:
        return None
    if len(key) <= 8:
        return "••••••••"
    return key[:4] + "••••••••••••••••" + key[-4:]
