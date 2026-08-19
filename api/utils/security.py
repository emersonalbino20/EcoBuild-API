from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

password_hash = PasswordHash((BcryptHasher(),))

def generate_pass_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_pass_hash(pure_pass: str, hash_pass: str) -> bool:
    return password_hash.verify(pure_pass, hash_pass)
