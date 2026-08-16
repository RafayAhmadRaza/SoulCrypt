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

## Important
    **Do not forget your passphrase.**
    SoulCrypt does not have a password recovery mechanism.

    If you lose the passphrase, your encrypted data may be unrecoverable
## Tests
Run the test suite with:

```bash
python -m unittest test_soulcrypt.py -v
```
The tests covers:
- Encryption/decryption
- Key derivation
- wrong passwords
- Modified ciphertext
- Unicode Text
- Empty Text
- Large Text
- Randomized Encryption
- Invalid Files
- Multiple Messages

## Project Structure
```bash
SoulCrypt/
├── main.py
├── soulcrypt.py
├── test_soulcrypt.py
└── README.md
```

``` main.py ```
Command-line interface and file handling.

```soulcrypt.py```
Encryption,decryption, key derivation, and SoulCrypt file format.

```test_soulcrypt.py```
Unit Tests for SoulCrypt.

## Disclaimer
SoulCrypt is a learning project.

It was created to learn about:
- Password-based key derivation
- Symmetric encryption
- File formats
- Python CLI applications
- Unit Testing

Do not rely on SoulCrypt for protecting highly sensitive information without independently reviewing the implementation and its security.

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
## The Garden Of Knowleddge
Somewhere along the development of SoulCrypt, a questionable amount of pseudo-Shakespearean peotry was created and then ecnrypted.
The Garden shall remember your thoughs so you dont have too.

I got the Idea for this project at two am of all things....