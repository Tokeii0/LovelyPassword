from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class EncryptionManager:
    def __init__(self):
        self.key = None
        self.cipher_suite = None
    
    def generate_key_from_password(self, password: str, salt: bytes = None) -> bytes:
        """从主密码生成加密密钥"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def initialize(self, key: bytes):
        """初始化加密管理器"""
        self.key = key
        self.cipher_suite = Fernet(self.key)
    
    def encrypt(self, data: str) -> str:
        """加密数据"""
        if not self.cipher_suite:
            raise RuntimeError("Encryption manager not initialized")
        return self.cipher_suite.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """解密数据"""
        if not self.cipher_suite:
            raise RuntimeError("Encryption manager not initialized")
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
    
    def verify_password(self, password: str, stored_hash: str) -> bool:
        """验证密码"""
        key, _ = self.generate_key_from_password(password)
        return key.decode() == stored_hash 