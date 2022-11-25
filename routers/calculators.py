# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from calculators.interest import interest
from calculators.datecalculator import calculate_time
from schemas import Message, Interest, Age


# ---------------------------------------------------------------------------- #
# --- Route Configuration ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


router = APIRouter()


class InterestBody(BaseModel):
    initial: float
    rate: float
    n: float
    t: float


# ---------------------------------------------------------------------------- #
# --- App Routes : Calculators ------------------------------------------------ #
# ---------------------------------------------------------------------------- #


# Interest Rate Calculator
@router.post('/calculators/interest', tags=["Calculators"],
             response_model=Interest,
             responses={
    500: {"model": Message}
})
def interest_calculator(interest_body: InterestBody):
    """
    ### Calculates compound interest.
    """
    result = interest(
        interest_body.initial,
        interest_body.rate,
        interest_body.n,
        interest_body.t
    )
    if result:
        response = {
            'total': result[0],
            'interest': result[1]
        }
        return JSONResponse(status_code=200, content=response)
    else:
        return JSONResponse(status_code=500, content="An error occured on the server.")


# Age Calculator
@router.post('/calculators/age', tags=["Calculators"],
             response_model=Age,
             responses={
    500: {"model": Message}
})
def age_calculator(start_date: str, end_date: str):
    """
    ### Calculates the age in various time units between two dates.
    """
    status, result = calculate_time(start_date, end_date)
    if status:
        return JSONResponse(status_code=200, content=result)
    else:
        return JSONResponse(status_code=500, content=result)
