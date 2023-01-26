# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from schemas import Schemas
from db.budgets import BudgetsDB
from auth.auth_manager import Auth


# ---------------------------------------------------------------------------- #
# --- Route Configuration ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


router = APIRouter()
security = HTTPBearer()
auth = Auth()
schemas = Schemas()
db = BudgetsDB()


# ---------------------------------------------------------------------------- #
# --- App Routes : Budget Application ---------------------------------------- #
# ---------------------------------------------------------------------------- #


@router.post('/budgets/create', tags=['Budgets'],
    response_model=schemas.Detail,
    responses={
        401: {"model": schemas.Detail},
        409: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def create(
    budget: schemas.CreateBudget,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    decoded_token = auth.decode_token(token)

    if decoded_token != budget.email:
        return JSONResponse(status_code=401, content={'detail': 'you may not create a budget for this user.'})

    code, response = db.create_budget(budget)
    return JSONResponse(status_code=code, content={'detail', response})


@router.post('/budgets/update', tags=['Budgets'],
    response_model=schemas.Detail,
    responses={
        401: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def update(
    budget: schemas.UpdateBudget,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    decoded_token = auth.decode_token(token)

    if decoded_token != budget.email:
        return JSONResponse(
            status_code=401,
            content={'detail': 'you may not update a budget for this user.'}
            )

    code, response = db.update_budget(budget)
    return JSONResponse(status_code=code, content={'detail': response})


@router.get('/budgets/all', tags=['Budgets'],
    response_model=list[schemas.Budget],
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

    code, response, budgets = db.get_all_budgets_by_email(decoded_token)
    if code != 200:
        return JSONResponse(status_code=code, content={'detail': response})
    
    return JSONResponse(status_code=200, content=budgets)


@router.get('/budgets/{key}', tags=['Budgets'],
    response_model=schemas.Budget,
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

    code, response, budget = db.get_budget_by_key(key)
    if code != 200:
        return JSONResponse(status_code=code, content={'detail': response})

    return JSONResponse(status_code=200, content=budget)


@router.delete('/budgets/delete', tags=['Budgets'],
    response_model=schemas.Detail,
    responses={
        401: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def delete(
    delete: schemas.DeleteBudget,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    decoded_token = auth.decode_token(token)

    if decoded_token != delete.email:
        return JSONResponse(status_code=401, content={'message': 'you may not delete a budget for this user.'})

    code, response = db.delete_budget(delete.key)
    return JSONResponse(status_code=code, content={'detail': response})
