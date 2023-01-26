# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import APIRouter
from fastapi.responses import JSONResponse
from crypto.valr import Valr
from schemas import Schemas


# ---------------------------------------------------------------------------- #
# --- Route Configuration ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


router = APIRouter()
valr = Valr()
schemas = Schemas()


# ---------------------------------------------------------------------------- #
# --- App Routes : Calculators ------------------------------------------------ #
# ---------------------------------------------------------------------------- #


@router.get('/crypto/rates', tags=["Crypto"],
    response_model=list[schemas.Crypto],
    responses={
        500: {"model": schemas.Detail}
    }
)
async def get_rates():
    """
    ### Gets all ZAR trading pair info from Valr
    """
    code, response, result = await valr.get_exchange_rates()
    if code != 200:
        return JSONResponse(status_code=code, content={'detail': response})
    
    return JSONResponse(status_code=code, content=result)
