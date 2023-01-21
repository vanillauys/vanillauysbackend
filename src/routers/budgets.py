# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from schemas import Message, CreateBudget, UpdateBudget, DeleteBudget
from db.budgets import (
    create_budget,
    delete_budget,
    update_budget,
    get_all_budgets,
    get_budget
)
from auth.auth_manager import Auth


# ---------------------------------------------------------------------------- #
# --- Route Configuration ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


router = APIRouter()
security = HTTPBearer()
auth_handler = Auth()


# ---------------------------------------------------------------------------- #
# --- App Routes : Budget Application ---------------------------------------- #
# ---------------------------------------------------------------------------- #


@router.post('/budgets/create', tags=['Budgets'],
             response_model=Message,
             responses={
    401: {"model": Message},
    500: {"model": Message}
})
def create(create: CreateBudget, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    decoded_token = auth_handler.decode_token(token)
    if not decoded_token:
        return JSONResponse(status_code=401, content={'message': 'Invalid credentials'})

    if decoded_token != create.email:
        return JSONResponse(status_code=401, content={'message': 'you may not create a budget for this user'})

    status, response = create_budget(create.email, create.name)
    if not status:
        return JSONResponse(status_code=500, content={'message': response})

    return JSONResponse(status_code=200, content=response)


@router.post('/budgets/update', tags=['Budgets'],
             response_model=Message,
             responses={
    401: {"model": Message},
    500: {"model": Message}
})
def update(update: UpdateBudget, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    decoded_token = auth_handler.decode_token(token)
    if not decoded_token:
        return JSONResponse(status_code=401, content={'message': 'Invalid credentials'})

    if decoded_token != update.email:
        return JSONResponse(status_code=401, content={'message': 'you may not update a budget for this user'})

    status, response = update_budget(
        update.key, update.income, update.expenses)
    if not status:
        return JSONResponse(status_code=500, content={'message': response})

    return JSONResponse(status_code=200, content=response)


@router.get('/budgets/all', tags=['Budgets'],
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

    status, response = get_all_budgets(decoded_token)
    if not status:
        return JSONResponse(status_code=500, content={'message': response})

    return JSONResponse(status_code=200, content=response)


@router.get('/budgets/{key}', tags=['Budgets'],
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

    status, response = get_budget(key)
    if not status:
        return JSONResponse(status_code=500, content={'message': response})

    return JSONResponse(status_code=200, content=response)


@router.delete('/budgets/delete', tags=['Budgets'],
               response_model=Message,
               responses={
    401: {"model": Message},
    500: {"model": Message}
})
def delete(delete: DeleteBudget, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    decoded_token = auth_handler.decode_token(token)
    if not decoded_token:
        return JSONResponse(status_code=401, content={'message': 'Invalid credentials'})

    if decoded_token != delete.email:
        return JSONResponse(status_code=401, content={'message': 'you may not delete a budget for this user'})

    status, response = delete_budget(delete.key)
    if not status:
        return JSONResponse(status_code=500, content={'message': response})

    return JSONResponse(status_code=200, content=response)
