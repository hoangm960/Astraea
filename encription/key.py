from cryptography.fernet import Fernet


def main():
    key = Fernet.generate_key()

    file = open('encription/key.key', 'wb')  # Open the file as wb to write bytes
    file.write(key)  # The key is type bytes still
    file.close()
