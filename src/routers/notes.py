# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from schemas import Schemas
from db.notes import NotesDB
from auth.auth_manager import Auth


# ---------------------------------------------------------------------------- #
# --- Route Configuration ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


router = APIRouter()
security = HTTPBearer()
auth = Auth()
db = NotesDB()
schemas = Schemas()


# ---------------------------------------------------------------------------- #
# --- App Routes : Notes Application ----------------------------------------- #
# ---------------------------------------------------------------------------- #


@router.post('/notes/create', tags=['Notes'],
    response_model=schemas.detail(),
    responses={
        401: {"model": schemas.detail()},
        409: {"model": schemas.detail()},
        500: {"model": schemas.detail()}
    }
)
def create(
    note: schemas.create_note(),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    decoded_token = auth.decode_token(token)

    if decoded_token != note.email:
        return JSONResponse(
            status_code=401,
            content={'detail': 'you may not create a note for this user.'}
            )

    code, response = db.create_note(note)
    return JSONResponse(status_code=code, content={'detail': response})


@router.post('/notes/update', tags=['Notes'],
    response_model=schemas.detail(),
    responses={
        401: {"model": schemas.detail()},
        500: {"model": schemas.detail()}
    }
)
def update(
    note: schemas.update_note(),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    decoded_token = auth.decode_token(token)

    if decoded_token != note.email:
        return JSONResponse(
            status_code=401,
            content={'detail': 'you may not update a note for this user.'}
            )

    code, response = db.update_note(note)
    return JSONResponse(status_code=code, content={'detail': response})


@router.get('/notes/all', tags=['Notes'],
    response_model=list[schemas.notes()],
    responses={
        401: {"model": schemas.detail()},
        500: {"model": schemas.detail()}
}
)
def get_all(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    decoded_token = auth.decode_token(token)

    code, response, notes = db.get_all_notes_by_email(decoded_token)
    if code != 200:
        return JSONResponse(status_code=code, content={'detail': response})
    
    return JSONResponse(status_code=code, content=notes)


@router.get('/notes/{key}', tags=['Notes'],
    response_model=schemas.note(),
    responses={
        401: {"model": schemas.detail()},
        404: {"model": schemas.detail()},
        500: {"model": schemas.detail()}
    }
)
def get_one(
    key: str,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    auth.decode_token(token)

    code, response, note = db.get_note_by_key(key)
    if code != 200:
        return JSONResponse(status_code=code, content={'detail': response})
    
    return JSONResponse(status_code=200, content=note)


@router.delete('/notes/delete', tags=['Notes'],
    response_model=schemas.detail(),
    responses={
        401: {"model": schemas.detail()},
        500: {"model": schemas.detail()}
    }
)
def delete(
    delete: schemas.delete_note(),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    decoded_token = auth.decode_token(token)

    if decoded_token != delete.email:
        return JSONResponse(
            status_code=401,
            content={'detail': 'you may not delete a note for this user.'}
            )

    code, response = db.delete_note(delete.key)
    return JSONResponse(status_code=code, content={'detail': response})
