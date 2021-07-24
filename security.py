from cryptography.fernet import Fernet
key = Fernet.generate_key()



def encrypt_psw(password):
    cipher_suite = Fernet(key)
    ciphered_psw = cipher_suite.encrypt(b'password')
    return ciphered_psw


def decrypt_psw(password):
    cipher_suite = Fernet(key)
    ciphered_psw = password
    unciphered_psw = (cipher_suite.decrypt(ciphered_psw))
    return unciphered_psw

