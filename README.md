# SoulCrypt

> Do you write things you want to keep hidden?
> Look no further than **SoulCrypt**.

SoulCrypt is a small command-line tool written in Python for encrypting
and decrypting text using a passphrase.

Originally created as a side project for securely storing some extremely
secret poetry.

## Features

- Passphrase-based encryption
- Random 16-byte salt for every encrypted file
- PBKDF2-HMAC-SHA256 key derivation
- Fernet authenticated encryption
- .soul encrypted file format
- Tampering detection
- 16 unit tests
- Pure Python

## Requirements

Python 3.10+

Install the dependency with:

```bash
pip install cryptography
```
## Use Example
### Encryption
```bash
python main.py encrypt file_name.soul
```
### Decryption
```bash

python main.py decrypt file_name.soul
```