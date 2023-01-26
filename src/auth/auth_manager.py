# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import os
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext


# ---------------------------------------------------------------------------- #
# --- Password hashing and verification -------------------------------------- #
# ---------------------------------------------------------------------------- #


class Auth():
    load_dotenv()
    hasher = CryptContext(schemes=['bcrypt'])
    secret = os.getenv("JWT_SECRET_KEY")

    def hash_password(self, password) -> str:
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password) -> bool:
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, email) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1, minutes=0),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': email
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if (payload['scope'] == 'access_token'):
                return payload['sub']
            raise HTTPException(
                status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def encode_refresh_token(self, email) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=14, hours=0),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': email
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def refresh_token(self, refresh_token) -> str:
        try:
            payload = jwt.decode(
                refresh_token, self.secret, algorithms=['HS256'])
            if (payload['scope'] == 'refresh_token'):
                email = payload['sub']
                new_token = self.encode_token(email)
                return new_token
            raise HTTPException(
                status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401, detail='Invalid refresh token')
