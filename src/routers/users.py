# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from schemas import Message, UserLoginSchema, UserSchema, LoggedIn
from db.users import create_user, login_user
from auth.auth_manager import Auth


# ---------------------------------------------------------------------------- #
# --- Route Configuration ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


router = APIRouter()
security = HTTPBearer()
auth_handler = Auth()


# ---------------------------------------------------------------------------- #
# --- App Routes : User and authentications ---------------------------------- #
# ---------------------------------------------------------------------------- #


@router.post('/users/signup', tags=['Users'],
             response_model=Message,
             responses={
    500: {"model": Message},
    409: {"model": Message}
})
def sign_up(user: UserSchema):
    status, result = create_user(user)
    if status:
        response = {
            'message': f'successfully added {user.email} to db.'
        }
        return JSONResponse(status_code=200, content=response)
    else:
        response = {
            'message': result
        }
        return JSONResponse(status_code=409, content=response)


@router.post('/users/login', tags=['Users'],
             response_model=LoggedIn,
             responses={
    500: {"model": Message},
    401: {"model": Message}
})
def login(user: UserLoginSchema):
    status, result = login_user(user)
    response = {
        'message': result
    }
    if not status:
        return JSONResponse(status_code=401, content=response)

    access_token = auth_handler.encode_token(user.email)
    refresh_token = auth_handler.encode_refresh_token(user.email)
    response = {
        'email': user.email,
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return JSONResponse(status_code=200, content=response)


@router.get('/users/potected', tags=['Users'],
            response_model=Message,
            responses={
    401: {"model": Message},
    500: {"model": Message}
})
def test_protected(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if auth_handler.decode_token(token):
        return JSONResponse(status_code=200, content={'message': 'you are logged in.'})


@router.get('/users/refresh_token', tags=['Users'],
            response_model=Message,
            responses={
    401: {"model": Message},
    500: {"model": Message}
})
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}
