import os
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request
from fastapi import HTTPException

admin_email = os.getenv('ADMIN_EMAIL')
admin_password = os.getenv('ADMIN_PASSWORD')

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != admin_email and data['password'] != admin_password:
            raise HTTPException(status_code=403, detail="Las credenciales son invalidas")