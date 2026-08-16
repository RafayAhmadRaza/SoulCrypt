import os
import unittest

from cryptography.fernet import InvalidToken

from soulcrypt import (
    SALT_SIZE,
    ITERATIONS,
    derive_key,
    encrypt_text,
    decrypt_text,
)


class TestSoulCrypt(unittest.TestCase):

    def test_constants(self):
        """Make sure our crypto parameters haven't accidentally changed."""
        self.assertEqual(SALT_SIZE, 16)
        self.assertEqual(ITERATIONS, 600_000)

    def test_key_derivation(self):
        """Same password + same salt must produce the same key."""
        password = "correct horse battery staple"
        salt = b"0123456789abcdef"

        key1 = derive_key(password, salt)
        key2 = derive_key(password, salt)

        self.assertEqual(key1, key2)

    def test_different_password_produces_different_key(self):
        """Different passwords must produce different keys."""
        salt = b"0123456789abcdef"

        key1 = derive_key("password-one", salt)
        key2 = derive_key("password-two", salt)

        self.assertNotEqual(key1, key2)

    def test_different_salt_produces_different_key(self):
        """Different salts must produce different keys."""
        password = "same-password"

        key1 = derive_key(password, b"0123456789abcdef")
        key2 = derive_key(password, b"fedcba9876543210")

        self.assertNotEqual(key1, key2)

    def test_encrypt_returns_bytes(self):
        """Encryption should produce bytes."""
        encrypted = encrypt_text(
            "Hello World",
            "password"
        )

        self.assertIsInstance(encrypted, bytes)

    def test_salt_is_16_bytes(self):
        """The encrypted file should begin with our 16-byte salt."""
        encrypted = encrypt_text(
            "Hello World",
            "password"
        )

        salt = encrypted[:SALT_SIZE]

        self.assertEqual(len(salt), SALT_SIZE)

    def test_encrypt_and_decrypt(self):
        """The basic encryption/decryption cycle."""
        original = "Hello World"
        password = "my secret password"

        encrypted = encrypt_text(original, password)
        decrypted = decrypt_text(encrypted, password)

        self.assertEqual(decrypted, original)

    def test_empty_string(self):
        """Even an empty string should round-trip correctly."""
        original = ""
        password = "password"

        encrypted = encrypt_text(original, password)
        decrypted = decrypt_text(encrypted, password)

        self.assertEqual(decrypted, original)

    def test_unicode(self):
        """Unicode text should survive encryption."""
        original = "Hello 🌳🔐 — 你好 — مرحبا"
        password = "secret"

        encrypted = encrypt_text(original, password)
        decrypted = decrypt_text(encrypted, password)

        self.assertEqual(decrypted, original)

    def test_long_text(self):
        """Large text should survive encryption."""
        original = "The Garden of Knowledge.\n" * 10_000
        password = "very-secret-password"

        encrypted = encrypt_text(original, password)
        decrypted = decrypt_text(encrypted, password)

        self.assertEqual(decrypted, original)

    def test_wrong_password(self):
        """A wrong password must not decrypt the message."""
        encrypted = encrypt_text(
            "This is secret.",
            "correct password"
        )

        with self.assertRaises(InvalidToken):
            decrypt_text(encrypted, "wrong password")

    def test_modified_ciphertext(self):
        """Tampering with the ciphertext must be detected."""
        encrypted = bytearray(
            encrypt_text(
                "Do not touch this.",
                "password"
            )
        )

        # Modify one byte of the ciphertext.
        encrypted[-1] ^= 1

        with self.assertRaises(InvalidToken):
            decrypt_text(bytes(encrypted), "password")

    def test_modified_salt(self):
        """Changing the salt should result in the wrong encryption key."""
        encrypted = bytearray(
            encrypt_text(
                "Secret text",
                "password"
            )
        )

        encrypted[0] ^= 1

        with self.assertRaises(InvalidToken):
            decrypt_text(bytes(encrypted), "password")

    def test_truncated_file(self):
        """A file containing only a salt should be rejected."""
        salt_only = os.urandom(SALT_SIZE)

        with self.assertRaises(ValueError):
            decrypt_text(salt_only, "password")

    def test_random_encryptions_are_different(self):
        """
        Encrypting the same plaintext twice should produce
        different ciphertext because each encryption gets a new salt.
        """
        plaintext = "Same message"
        password = "same password"

        encrypted1 = encrypt_text(plaintext, password)
        encrypted2 = encrypt_text(plaintext, password)

        self.assertNotEqual(encrypted1, encrypted2)

    def test_multiple_messages(self):
        """Test several different messages."""
        messages = [
            "Hello",
            "Helloworld",
            "The Garden awaits.",
            "Oh How Cruel Be Thee.",
            "1234567890",
            "🔥",
            "",
        ]

        password = "garden-password"

        for message in messages:
            with self.subTest(message=message):
                encrypted = encrypt_text(message, password)
                decrypted = decrypt_text(encrypted, password)

                self.assertEqual(decrypted, message)


if __name__ == "__main__":
    unittest.main()