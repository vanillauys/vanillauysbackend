# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import APIRouter
from fastapi.responses import JSONResponse
from crypto.valr import get_exchange_rates
from schemas import Message, Crypto


# ---------------------------------------------------------------------------- #
# --- Route Configuration ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


router = APIRouter()


# ---------------------------------------------------------------------------- #
# --- App Routes : Calculators ------------------------------------------------ #
# ---------------------------------------------------------------------------- #


# Interest Rate Calculator
@router.get('/crypto/rates', tags=["Crypto"],
             response_model=list[Crypto],
             responses={
    500: {"model": Message}
})
async def get_rates():
    """
    ### Gets all ZAR trading pair info from Valr
    """
    status, response = await get_exchange_rates()
    if status:
        return JSONResponse(status_code=200, content=response)
    else:
        return JSONResponse(status_code=500, content="An error occured on the server.")
