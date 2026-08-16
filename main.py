import getpass
import sys

from cryptography.fernet import InvalidToken

from soulcrypt import encrypt_text, decrypt_text


def encrypt_file(input_path):
    print("Remember to write your passphrase somewhere safe!")
    passphrase = getpass.getpass("Enter Your Passphrase\n> ")

    print("Enter your secrets: ")
    print("Type END on a new line when finished.")
    lines = []

    while True:
        line = input()  
        if line == "END":
            break
        lines.append(line)

    poem = "\n".join(lines)



    encrypted = encrypt_text(poem, passphrase)

    with open(input_path, "wb") as secret_file:
        secret_file.write(encrypted)

    print("Your soul has been sealed.")


def decrypt_file(input_path):
    passphrase = getpass.getpass("Enter Your Passphrase\n> ")

    try:
        with open(input_path, "rb") as secret_file:
            encrypted = secret_file.read()

        poem = decrypt_text(encrypted, passphrase)

        print("\nYour soul has been restored:")
        print(poem)

    except FileNotFoundError:
        print("Error: Soul file does not exist.")

    except InvalidToken:
        print("Error: Incorrect passphrase or corrupted Soul file.")

    except ValueError as error:
        print(f"Error: {error}")


def main():
    arguments = sys.argv[1:]

    if len(arguments) != 2:
        print("Usage:")
        print("  python main.py encrypt <file>")
        print("  python main.py decrypt <file>")
        sys.exit(1)

    command = arguments[0]
    file_path = arguments[1]

    if command == "encrypt":
        encrypt_file(file_path)

    elif command == "decrypt":
        decrypt_file(file_path)

    else:
        print(f"Error: Unknown command '{command}'")
        print("Use 'encrypt' or 'decrypt'.")
        sys.exit(1)


if __name__ == "__main__":
    main()