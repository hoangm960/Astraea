import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken


def get_key(path):
    key = Fernet.generate_key()

    with open(path, 'wb') as file:
        file.write(key) 


def encrypt(input_file, output_file, key_file):
    get_key(key_file)

    with open(key_file, 'rb') as f:
        key = f.read() 

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)
    
    os.remove(input_file)


def decrypt(input_file, output_file, key_file):
    input_file_path = Path(input_file)
    if not input_file_path.is_file():
        open(output_file, 'w').close()
    else:
        with open(key_file, 'rb') as f:
            key = f.read() 
            
        with open(input_file, 'rb') as f:
            data = f.read() 
        fernet = Fernet(key)
        try:
            decrypted = fernet.decrypt(data)

            with open(output_file, 'wb') as f:
                f.write(decrypted) 
            
            os.remove(input_file)
            
        except InvalidToken as e:
            print("Invalid Key - Unsuccessfully decrypted")


if __name__ == "__main__":
    KEY_PATH = "data/encryption/users.key"
    USER_PATH = "data/Users/User.txt"
    USER_PATH_ENCRYPTED = "data/Users/User.encrypted"
    encrypt(USER_PATH, USER_PATH_ENCRYPTED, KEY_PATH)
    # decrypt(USER_PATH_ENCRYPTED, USER_PATH, KEY_PATH)
