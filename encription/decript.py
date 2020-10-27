from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken


def main(input_file, output_file):
    input_file_path = Path(input_file)
    if not input_file_path.is_file():
        open(output_file, 'w').close()
    else:
        with open('encription/key.key', 'rb') as f:
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

# main('encription/user.encrypted', 'data/User.txt')
