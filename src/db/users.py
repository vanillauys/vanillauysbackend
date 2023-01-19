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
    status, email = check_email(user.email)
    if not status:
        return False, 'an error occured when trying to check if the email address is in use.'
    if email:
        return False, f'{user.email} already exists in the db.'

    status, username = check_username(user.username)
    if not status:
        return False, 'an error occured when trying to check if the username is in use.'
    if username:
        return False, f'{user.username} already exists in the db.'

    data = {
        'username': user.username,
        'email': user.email,
        'password': ah.hash_password(user.password)
    }
    result = users.put(data)
    return True, result


def login_user(user: UserLoginSchema):
    status, data = check_email(user.email)

    if not status:
        return False, f'an error occured while trying to log in {user.email}.'

    if not data:
        return False, f'{user.email} does not exist in db.'

    if not ah.verify_password(user.password, data[0]['password']):
        return False, f'invalid password for {user.email}.'
    
    return True, f'{user.email} logged in successfully.'


def check_email(email: str):
    try:
        results = users.fetch({'email': email})
        user = results.items
        return True, user
    except Exception:
        return False, None


def check_username(username: str):
    try:
        results = users.fetch({'username': username})
        user = results.items
        return True, user
    except Exception:
        return False, None
