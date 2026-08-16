import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


SALT_SIZE = 16
ITERATIONS = 600_000


def derive_key(passphrase: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from a passphrase and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )

    return base64.urlsafe_b64encode(
        kdf.derive(passphrase.encode())
    )


def encrypt_text(text: str, passphrase: str) -> bytes:
    """Encrypt text and return salt + ciphertext."""
    salt = os.urandom(SALT_SIZE)
    key = derive_key(passphrase, salt)

    fernet = Fernet(key)
    encrypted = fernet.encrypt(text.encode())

    return salt + encrypted


def decrypt_text(data: bytes, passphrase: str) -> str:
    """Decrypt salt + ciphertext and return the original text."""
    if len(data) <= SALT_SIZE:
        raise ValueError("Invalid SoulCrypt file.")

    salt = data[:SALT_SIZE]
    encrypted = data[SALT_SIZE:]

    key = derive_key(passphrase, salt)

    fernet = Fernet(key)

    decrypted = fernet.decrypt(encrypted)

    return decrypted.decode()