from cryptography.fernet import Fernet
import sys
import getpass
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64



arguments = sys.argv[1:]

if len(arguments) !=2:
    print("Error Number of Arguments is wrong")
    sys.exit()

argument = arguments[0]
poem_path = arguments[1]

print("Remember to write your passphrase somewhere so you can unencrypt your files!")
print("Enter Your Passphrase")
passphrase = getpass.getpass(">")

salt = os.urandom(16)

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=600_000,
)

key = base64.urlsafe_b64encode(
    kdf.derive(passphrase.encode())
)

if argument == 'encrypt':
    fernet = Fernet(key)
    poem = input("Enter you secrets")

    with open(poem_path,'wb') as secret_file:
        poem_encypted = fernet.encrypt(poem.encode())
        secret_file.write(salt)
        secret_file.write(poem_encypted)
        print(poem_encypted)
        secret_file.close()


elif argument == 'decrypt':

    fernet = Fernet(key)
    with open(poem_path,'r') as f:
        
        decrypted_file = fernet.decrypt(f)
        print(decrypted_file)

