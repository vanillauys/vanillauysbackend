# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from schemas import Schemas
from db.users import UserDB
from auth.auth_manager import Auth


# ---------------------------------------------------------------------------- #
# --- Route Configuration ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


router = APIRouter()
security = HTTPBearer()
auth = Auth()
schemas = Schemas()
db = UserDB()


# ---------------------------------------------------------------------------- #
# --- App Routes : User and authentications ---------------------------------- #
# ---------------------------------------------------------------------------- #


@router.post('/users/signup', tags=['Users'],
    response_model=schemas.Detail,
    responses={
        409: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def sign_up(user: schemas.UserSchema):
    code, response = db.create_user(user)
    return JSONResponse(status_code=code, content={'detail': response})


@router.post('/users/login', tags=['Users'],
    response_model=schemas.LoggedIn,
    responses={
        401: {"model": schemas.Detail},
        404: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def login(user: schemas.UserLoginSchema):
    code, response = db.login_user(user)
    if code != 200:
        return JSONResponse(status_code=code, content={'detail': response})

    access_token = auth.encode_token(user.email)
    refresh_token = auth.encode_refresh_token(user.email)
    response = {
        'email': user.email,
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return JSONResponse(status_code=200, content=response)


@router.get('/users/potected', tags=['Users'],
    response_model=schemas.Detail,
    responses={
        401: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def test_protected(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if auth.decode_token(token):
        return JSONResponse(status_code=200, content={'detail': 'you are logged in.'})


@router.get('/users/refresh_token', tags=['Users'],
    response_model=schemas.Detail,
    responses={
        401: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth.refresh_token(refresh_token)
    return JSONResponse(status_code=200, content={'detail': new_token})
