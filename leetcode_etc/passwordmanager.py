import random
import getpass
import base64
import os
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


masterpwd = getpass.getpass("Master password: ").encode()
print(masterpwd)
# key = Fernet.generate_key()
# fer = Fernet(key)
# fer = Fernet(masterpwd)
# tok = fer.encrypt(masterpwd)
# print(key)
# print(fer)
# print(tok)
# print(fer.decrypt(tok))
# PBKDF2HMAC()

salt = os.urandom(16)
print(salt)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)
key = base64.urlsafe_b64encode(kdf.derive(masterpwd))
f = Fernet(key)
Plain_text = input("Enter the text to be encrypted: ").encode()
token = f.encrypt(Plain_text)
print("Encrypted data: ",token)
print("Decrypted data: ",f.decrypt(token).decode())

mode = input("1. Add a new password\
            \n2. View existing passwords\
            \n3. Quit\n")

def addpwd():
    user = input('Account name: ')
    upwd = getpass.getpass('Acc. password')
    
    with open('passwords.txt', 'a') as f:
        f.write(user + "," + cryptography.hexdigest(upwd))

while True:
    if mode == 1:
        addpwd()
    elif mode == 2:
        pass
    elif mode == 3:
        pass
        
    ### Work in progress ###