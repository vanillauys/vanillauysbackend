# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from schemas import Message, CreateNote, UpdateNote, DeleteNote
from db.notes import (
    create_note,
    delete_note,
    update_note,
    get_all_notes,
    get_note
)
from auth.auth_manager import Auth


# ---------------------------------------------------------------------------- #
# --- Route Configuration ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


router = APIRouter()
security = HTTPBearer()
auth_handler = Auth()


# ---------------------------------------------------------------------------- #
# --- App Routes : Notes Application ----------------------------------------- #
# ---------------------------------------------------------------------------- #


@router.post('/notes/create', tags=['Notes'],
             response_model=Message,
             responses={
    401: {"model": Message},
    500: {"model": Message}
})
def create(create: CreateNote, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    decoded_token = auth_handler.decode_token(token)
    if not decoded_token:
        return JSONResponse(status_code=401, content={'message': 'Invalid credentials'})

    if decoded_token != create.email:
        return JSONResponse(status_code=401, content={'message': 'you may not create a note for this user'})

    status, response = create_note(create.email, create.title, create.body)
    if not status:
        return JSONResponse(status_code=500, content={'message': response})

    return JSONResponse(status_code=200, content={'message': response})


@router.post('/notes/update', tags=['Notes'],
             response_model=Message,
             responses={
    401: {"model": Message},
    500: {"model": Message}
})
def update(update: UpdateNote, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    decoded_token = auth_handler.decode_token(token)
    if not decoded_token:
        return JSONResponse(status_code=401, content={'message': 'Invalid credentials'})

    if decoded_token != update.email:
        return JSONResponse(status_code=401, content={'message': 'you may not update a note for this user'})

    status, response = update_note(update.key, update.title, update.body)
    if not status:
        return JSONResponse(status_code=500, content={'message': response})

    return JSONResponse(status_code=200, content={'message': response})


@router.get('/notes/all', tags=['Notes'],
            response_model=Message,
            responses={
    401: {"model": Message},
    500: {"model": Message}
})
def get_all(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    decoded_token = auth_handler.decode_token(token)
    if not decoded_token:
        return JSONResponse(status_code=401, content={'message': 'Invalid credentials'})

    status, response = get_all_notes(decoded_token)
    if not status:
        return JSONResponse(status_code=500, content={'message': response})

    return JSONResponse(status_code=200, content=response)


@router.get('/notes/{key}', tags=['Notes'],
            response_model=Message,
            responses={
    401: {"model": Message},
    500: {"model": Message}
})
def get_one(key: str, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    decoded_token = auth_handler.decode_token(token)
    if not decoded_token:
        return JSONResponse(status_code=401, content={'message': 'Invalid credentials'})

    status, response = get_note(key)
    if not status:
        return JSONResponse(status_code=500, content={'message': response})

    return JSONResponse(status_code=200, content=response)


@router.delete('/notes/delete', tags=['Notes'],
               response_model=Message,
               responses={
    401: {"model": Message},
    500: {"model": Message}
})
def delete(delete: DeleteNote, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    decoded_token = auth_handler.decode_token(token)
    if not decoded_token:
        return JSONResponse(status_code=401, content={'message': 'Invalid credentials'})

    if decoded_token != delete.email:
        return JSONResponse(status_code=401, content={'message': 'you may not delete a note for this user'})

    status, response = delete_note(delete.key)
    if not status:
        return JSONResponse(status_code=500, content={'message': response})

    return JSONResponse(status_code=200, content=response)
