# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from db.db_conf import users
from schemas import UserSchema
from schemas import UserLoginSchema
from auth.auth_manager import Auth


# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

ah = Auth()

def create_user(user: UserSchema):
    if check_email(user.email):
        return False, 'email'
    if check_username(user.username):
        return False, 'username'

    data = {
        'username': user.username,
        'email': user.email,
        'password': ah.hash_password(user.password)
    }
    result = users.put(data)
    return True, result


def login_user(user: UserLoginSchema):
    data = check_email(user.email)

    if not data:
        return False, f'{user.email} does not exist in db.'

    if not ah.verify_password(user.password, data[0]['password']):
        return False, f'invalid password for {user.email}.'
    
    return True, f'{user.email} logged in successfully.'


def check_email(email: str) -> bool:
    results = users.fetch({'email': email})
    user = results.items
    return user


def check_username(username: str) -> bool:
    results = users.fetch({'username': username})
    user = results.items
    return user
