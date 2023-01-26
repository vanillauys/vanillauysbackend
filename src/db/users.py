# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import os
from deta import Deta
from dotenv import load_dotenv
from schemas import Schemas
from auth.auth_manager import Auth
from typing import Dict, Tuple


# ---------------------------------------------------------------------------- #
# --- User Database ---------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


load_dotenv()

class UserDB():

    auth = Auth()
    schemas = Schemas()
    PROJECT_KEY = os.getenv('DETA_PROJECT_KEY')
    deta = Deta(PROJECT_KEY)
    users = deta.Base('users')

    def create_user(self, user: schemas.UserSchema) -> Tuple[int, str]:
        code, _, _ = self.get_user_by_email(user.email)
        if code == 200:
            return 409, f"email '{user.email}' already exists in the db."
        if code == 500:
            return 500, f"an error occured while checking if email '{user.email}' exists in the db."

        code, _, _ = self.get_user_by_username(user.username)
        if code == 200:
            return 409, f"username '{user.username}' already exists in the db."
        if code == 500:
            return 500, f"an error occured while checking if username '{user.username}' exists in the db."


        data = {
            'username': user.username,
            'email': user.email,
            'password': self.auth.hash_password(user.password)
        }

        try:
            self.users.put(data)
            return 200, f"successfully added user '{user.email}' to the db."
        except Exception:
            return 500, 'an error occured while adding user to the db.'            


    def login_user(self, user: schemas.UserLoginSchema) -> Tuple[int, str]:
        code, response, result = self.get_user_by_email(user.email)

        if code != 200:
            return code, response

        if not self.auth.verify_password(user.password, result['password']):
            return 401, f"invalid password for '{user.email}'."

        return 200, f"'{user.email}' logged in successfully."


    def get_user_by_email(self, email: str) -> Tuple[int, str, Dict]:
        try:
            results = self.users.fetch({'email': email})
            user = results.items

            if not user:
                return 404, f"email '{email}' not found in db.", None

            return 200, f"email '{email}' found in db.", user[0]

        except Exception:
            return 500, f"an error occurred while fetching '{email}'", None


    def get_user_by_username(self, username: str) -> Tuple[int, str, Dict]:
        try:
            results = self.users.fetch({'username': username})
            user = results.items

            if not user:
                return 404, f"username '{username}' not found in db.", None
            
            return 200, f"username '{username}' found in db.", user[0]

        except Exception:
            return 500, f"an error occurred while fetching '{username}'", None
