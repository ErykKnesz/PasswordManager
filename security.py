from cryptography.fernet import Fernet

try:
    with open('key.bin', 'rb') as file_object:
        for line in file_object:
            key = line
except FileNotFoundError:
    key = Fernet.generate_key()


def encrypt_psw(password):
    cipher_suite = Fernet(key)
    ciphered_psw = cipher_suite.encrypt(password.encode())
    return ciphered_psw


def decrypt_psw(password):
    cipher_suite = Fernet(key)
    ciphered_psw = password.encode()
    unciphered_psw = cipher_suite.decrypt(ciphered_psw)
    return unciphered_psw

