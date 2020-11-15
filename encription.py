import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

KEY_PATH  = 'data/key.key'

def get_key():
    key = Fernet.generate_key()

    file = open(KEY_PATH, 'wb')  # Open the file as wb to write bytes
    file.write(key)  # The key is type bytes still
    file.close()


def encrypt(input_file, output_file):
    with open(KEY_PATH, 'rb') as f:
        key = f.read() 

    with open(input_file, 'rb') as f:
        data = f.read()  # Read the bytes of the input file

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)
    
    os.remove(input_file)


def decrypt(input_file, output_file):
    input_file_path = Path(input_file)
    if not input_file_path.is_file():
        open(output_file, 'w').close()
    else:
        with open(KEY_PATH, 'rb') as f:
            key = f.read() 
            
        with open(input_file, 'rb') as f:
            data = f.read()  # Read the bytes of the encrypted file

        fernet = Fernet(key)
        try:
            decrypted = fernet.decrypt(data)

            with open(output_file, 'wb') as f:
                f.write(decrypted)  # Write the decrypted bytes to the output file

            # Note: You can delete input_file here if you want
        except InvalidToken as e:
            print("Invalid Key - Unsuccessfully decrypted")

        os.remove(input_file)

if __name__ == "__main__":
    # encrypt("data/User.txt", "data/User.encrypted")
    decrypt("data/User.encrypted", "data/User.txt")