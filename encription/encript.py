import os

from cryptography.fernet import Fernet

def main(input_file, output_file):
    with open('encription/key.key', 'rb') as f:
        key = f.read() 

    with open(input_file, 'rb') as f:
        data = f.read()  # Read the bytes of the input file

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)
    
    os.remove(input_file)
