import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken


def get_key(path):
    key = Fernet.generate_key()

    file = open(path, 'wb')  # Open the file as wb to write bytes
    file.write(key)  # The key is type bytes still
    file.close()


def encrypt(input_file, output_file, key_file):
    with open(key_file, 'rb') as f:
        key = f.read() 

    with open(input_file, 'rb') as f:
        data = f.read()  # Read the bytes of the input file

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)
    
    os.remove(input_file)


def decrypt(input_file, output_file, key_file):
    input_file_path = Path(input_file)
    if not input_file_path.is_file():
        get_key(key_file)
        open(output_file, 'w').close()
    else:
        with open(key_file, 'rb') as f:
            key = f.read() 
            
        with open(input_file, 'rb') as f:
            data = f.read()  # Read the bytes of the encrypted file

        fernet = Fernet(key)
        try:
            decrypted = fernet.decrypt(data)

            with open(output_file, 'wb') as f:
                f.write(decrypted)  # Write the decrypted bytes to the output file
            
            os.remove(input_file)

            # Note: You can delete input_file here if you want
        except InvalidToken as e:
            print("Invalid Key - Unsuccessfully decrypted")


if __name__ == "__main__":
    get_key("data/encryption/key.key")
    encrypt("data/Users/User.txt", "data/Users/User.encrypted", "data/encryption/key.key")
    # decrypt("data/Users/User.encrypted", "data/Users/User.txt", "data/encryption/key.key")
