from cryptography.fernet import Fernet
key = b'3TQWJL-6W7lEBUf9vCi3HNTEdJx-HhzVbg2MGoXJ5jU=' # Fernet.generate_key()


def encrypt_psw(password):
    cipher_suite = Fernet(key)
    ciphered_psw = cipher_suite.encrypt(password.encode())
    return ciphered_psw


def decrypt_psw(password):
    cipher_suite = Fernet(key)
    ciphered_psw = password.encode()
    unciphered_psw = cipher_suite.decrypt(ciphered_psw)
    return unciphered_psw

