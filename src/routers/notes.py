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
    response_model=schemas.Detail,
    responses={
        401: {"model": schemas.Detail},
        409: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def create(
    note: schemas.CreateNote,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    decoded_token = auth.decode_token(token)
    note.email = str(note.email)
    if decoded_token != note.email:
        return JSONResponse(
            status_code=401,
            content={'detail': 'you may not create a note for this user.'}
            )

    code, response = db.create_note(note)
    return JSONResponse(status_code=code, content={'detail': response})


@router.post('/notes/update', tags=['Notes'],
    response_model=schemas.Detail,
    responses={
        401: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def update(
    note: schemas.UpdateNote,
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
    response_model=list[schemas.Notes],
    responses={
        401: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
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
    response_model=schemas.Notes,
    responses={
        401: {"model": schemas.Detail},
        404: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
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
    response_model=schemas.Detail,
    responses={
        401: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def delete(
    delete: schemas.DeleteNote,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    decoded_token = auth.decode_token(token)
    delete.email = str(delete.email)
    if decoded_token != delete.email:
        return JSONResponse(
            status_code=401,
            content={'detail': 'you may not delete a note for this user.'}
            )

    code, response = db.delete_note(delete.key)
    return JSONResponse(status_code=code, content={'detail': response})
