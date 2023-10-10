from jwt import encode, decode
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv('JWT_SECRET_KEY')
algorithm = os.getenv('JWT_ALGORITHM')

def create_token(data: dict) -> str:
    token: str = encode(payload=data, key=secret_key, algorithm=algorithm)
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key=secret_key, algorithms=[algorithm])
    return data
