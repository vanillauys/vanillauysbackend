# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import APIRouter
from fastapi.responses import JSONResponse
from calculators.interest import InterestCalculator
from calculators.datecalculator import DateCalculator
from schemas import Schemas


# ---------------------------------------------------------------------------- #
# --- Route Configuration ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


router = APIRouter()
interest_calc = InterestCalculator()
age_calc = DateCalculator()
schemas = Schemas()


# ---------------------------------------------------------------------------- #
# --- App Routes : Calculators ----------------------------------------------- #
# ---------------------------------------------------------------------------- #


# Interest Rate Calculator
@router.post('/calculators/interest', tags=["Calculators"],
    response_model=schemas.Interest,
    responses={
        400: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def interest_calculator(interest_body: schemas.InterestBody):
    """
    ### Calculates compound interest.
    """
    code, response, result = interest_calc.interest(
        interest_body.initial,
        interest_body.rate,
        interest_body.n,
        interest_body.t
    )
    if code != 200:
        return JSONResponse(status_code=code, content={'detail': response})
    
    return JSONResponse(status_code=code, content=result)


# Age Calculator
@router.post('/calculators/age', tags=["Calculators"],
    response_model=schemas.Age,
    responses={
        400: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def age_calculator(start_date: str, end_date: str):
    """
    ### Calculates the age in various time units between two dates.
    """
    code, response, result = age_calc.calculate_time(start_date, end_date)
    if code != 200:
        return JSONResponse(status_code=code, content={'detail': response})

    return JSONResponse(status_code=code, content=result)
