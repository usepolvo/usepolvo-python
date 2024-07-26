import base64

from cryptography.fernet import Fernet


class EncryptionManager:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def encrypt(self, data: str) -> str:
        encrypted_data = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()

    def decrypt(self, token: str) -> str:
        # Fix padding issues
        token += "=" * (-len(token) % 4)
        encrypted_data = base64.urlsafe_b64decode(token)
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return decrypted_data.decode()


def generate_key() -> str:
    return Fernet.generate_key().decode()
