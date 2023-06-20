from cryptography.fernet import Fernet


class Cryptographer:

    def __init__(self):
        self.key = self._get_key()

    def _get_key(self):
        """
        Get a key used by the Cryptography library for en- and decryption.

        :return str: key
        """
        try:
            with open('key.bin', 'rb') as file_object:
                for line in file_object:
                    key = line
        except FileNotFoundError:
            key = Fernet.generate_key()
        return key

    def encrypt_psw(self, password):
        """
        Encrypt a password.

        :param str password: password to encrypt
        :return str: encrypted password
        """
        cipher_suite = Fernet(self.key)
        return cipher_suite.encrypt(password.encode())

    def decrypt_psw(self, password):
        """
        Decrypt a password.

        :param str password: password to decrypt
        :return str: decrypted password
        """
        cipher_suite = Fernet(self.key)
        ciphered_psw = password.encode()
        return cipher_suite.decrypt(ciphered_psw)

