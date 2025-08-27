from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def derive_key(encryption_key, salt=None):
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(encryption_key.encode()))
    return key, salt

def encrypt_data(data, encryption_key):
    if isinstance(data, str):
        data = data.encode()
    
    key, salt = derive_key(encryption_key)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    return salt + encrypted

def decrypt_data(encrypted_data, encryption_key):
    salt = encrypted_data[:16]
    encrypted = encrypted_data[16:]
    
    key, _ = derive_key(encryption_key, salt)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)
    return decrypted.decode()