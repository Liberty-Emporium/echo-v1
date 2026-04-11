# Secret Encrypt Skill

Encrypt and decrypt secrets using a password. Use this to safely store API keys and secrets on GitHub.

## Usage

### Encrypt a secret
```
encrypt "<your secret>" with password "<password>"
```

### Decrypt a secret
```
decrypt "<encrypted secret>" with password "<password>"
```

## Examples

**Encrypt:**
- Input: `encrypt "sk-mr-310042639dbd01385cd8ec096c401ca95d6c7c9ce3df0a6b0a5a046c8cdc4127" with password "MySecretPass123"`
- Output: Shows encrypted string to copy

**Decrypt:**
- Input: `decrypt "U2FsdGVkX1..." with password "MySecretPass123"`
- Output: Shows original secret

## How it works
- Uses AES-256 encryption via Python's cryptography library
- Password is used to derive the encryption key
- Encrypted strings start with "U2FsdGVkX1" (OpenSSL compatible)
- Safe to share on GitHub - only someone with the password can decrypt

## Files
- `scripts/encrypt.py` - Python script for encrypt/decrypt
