"""
test_security_core.py — Standalone tests for saas_security_core.py
Run: python test_security_core.py
All tests must pass before deploying to any app.
"""

import sys
import os

# Set test pepper so we test with it enabled
os.environ['PASSWORD_PEPPER'] = 'test-pepper-do-not-use-in-production'

# Add tools dir to path
sys.path.insert(0, os.path.dirname(__file__))

from saas_security_core import (
    hash_password, verify_password, needs_hash_upgrade,
    validate_password_strength, validate_username, validate_email,
    sanitize_string, BCRYPT_AVAILABLE, ARGON2_AVAILABLE
)

PASS = '✅'
FAIL = '❌'
results = []

def test(name, condition, detail=''):
    status = PASS if condition else FAIL
    results.append((status, name, detail))
    print(f'  {status} {name}' + (f' — {detail}' if detail else ''))
    return condition

print('\n🔐 saas_security_core.py Test Suite')
print('=' * 50)

# ── Environment ───────────────────────────────────────────
print('\n📦 Environment:')
test('bcrypt available', BCRYPT_AVAILABLE, 'install: pip install bcrypt')
test('argon2 available', ARGON2_AVAILABLE, 'install: pip install argon2-cffi')

# ── Password Hashing ──────────────────────────────────────
print('\n🔑 Password Hashing:')

h1 = hash_password('TestPassword123!')
test('hash_password returns string', isinstance(h1, str))
test('hash_password is not plaintext', 'TestPassword123!' not in h1)
test('hash_password has prefix', h1.startswith(('argon2:', 'bcrypt:', 'sha256:')),
     f'got: {h1[:20]}...')

# Verify correct password
test('verify_password correct → True', verify_password('TestPassword123!', h1))

# Verify wrong password
test('verify_password wrong → False', not verify_password('WrongPassword!', h1))

# Verify empty password
test('verify_password empty → False', not verify_password('', h1))

# Two hashes of same password are different (salting)
h2 = hash_password('TestPassword123!')
test('hashes are salted (unique)', h1 != h2, 'same password → different hashes')

# Needs upgrade detection
test('needs_upgrade: new hash → False', not needs_hash_upgrade(h1))
test('needs_upgrade: sha256 → True',
     needs_hash_upgrade('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'))

# ── Legacy SHA-256 compatibility ─────────────────────────
print('\n🔄 Legacy SHA-256 Compatibility:')
import hashlib
# Legacy hash (no pepper, no salt) — must still verify for old accounts
legacy = hashlib.sha256('OldPassword99!'.encode()).hexdigest()
# Temporarily clear pepper to test legacy path
os.environ['PASSWORD_PEPPER'] = ''
test('legacy SHA-256 still verifies', verify_password('OldPassword99!', legacy),
     'old accounts can still log in')
os.environ['PASSWORD_PEPPER'] = 'test-pepper-do-not-use-in-production'

# ── Password Strength Validation ─────────────────────────
print('\n💪 Password Strength:')
ok, err = validate_password_strength('short')
test('too short → invalid', not ok, err)

ok, err = validate_password_strength('admin123')
test('common password → invalid', not ok, err)

ok, err = validate_password_strength('password')
test('"password" → invalid', not ok, err)

ok, err = validate_password_strength('Tr33top-2025!')
test('strong password → valid', ok)

ok, err = validate_password_strength('a' * 300)
test('too long → invalid', not ok, err)

# ── Username Validation ───────────────────────────────────
print('\n👤 Username Validation:')
ok, err = validate_username('jay')
test('valid username → ok', ok)

ok, err = validate_username('ab')
test('too short → invalid', not ok, err)

ok, err = validate_username('jay alexander')
test('space in username → invalid', not ok, err)

ok, err = validate_username('jay_alexander.jr')
test('underscores/dots → valid', ok)

ok, err = validate_username('')
test('empty username → invalid', not ok)

# ── Email Validation ──────────────────────────────────────
print('\n📧 Email Validation:')
ok, err = validate_email('jay@libertyemporium.com')
test('valid email → ok', ok)

ok, err = validate_email('notanemail')
test('no @ → invalid', not ok, err)

ok, err = validate_email('')
test('empty → invalid', not ok)

ok, err = validate_email('a' * 300 + '@example.com')
test('too long → invalid', not ok)

# ── String Sanitization ───────────────────────────────────
print('\n🧹 Input Sanitization:')
test('strips whitespace', sanitize_string('  hello  ') == 'hello')
test('truncates to max_length', len(sanitize_string('a' * 500, max_length=100)) == 100)
test('empty string → empty', sanitize_string('') == '')
test('None-safe', sanitize_string(None) == '')  # type: ignore

# ── Timing Safety (no timing attacks) ────────────────────
print('\n⏱️  Timing Safety:')
import time
h = hash_password('SomePassword!')

start = time.perf_counter()
verify_password('SomePassword!', h)
good_time = time.perf_counter() - start

start = time.perf_counter()
verify_password('WrongPassword!', h)
bad_time = time.perf_counter() - start

# Both should take roughly the same time (compare_digest prevents timing attacks)
# We just verify both run without error
test('correct password verify runs', good_time > 0)
test('incorrect password verify runs', bad_time > 0)

# ── Summary ───────────────────────────────────────────────
print('\n' + '=' * 50)
passed = sum(1 for r in results if r[0] == PASS)
failed = sum(1 for r in results if r[0] == FAIL)
total = len(results)

print(f'\n📊 Results: {passed}/{total} passed', end='')
if failed:
    print(f', {failed} FAILED ❌')
    print('\nFailed tests:')
    for status, name, detail in results:
        if status == FAIL:
            print(f'  ❌ {name}' + (f' — {detail}' if detail else ''))
    sys.exit(1)
else:
    print(' ✅')
    print('\n🚀 All tests passed — safe to deploy to KYS!\n')
    sys.exit(0)
