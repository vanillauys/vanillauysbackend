# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import calculators, crypto
from schemas import Message


# ---------------------------------------------------------------------------- #
# --- App Configuration ------------------------------------------------------ #
# ---------------------------------------------------------------------------- #


TAGS_METADATA = [
    {
        "name": "Calculators",
        "description": "Some really simple calculators."
    },
    {
        "name": "Crypto",
        "description": "Cryptocurrency info from local South African exchange.",
        "externalDocs": {
            "description": "VALR",
            "url": "https://valr.com/"
        }
    },
    {
        "name": "Testing",
        "description": "Routes to test functionality.",
        "externalDocs": {
            "description": "FastAPI Documentation",
            "url": "https://fastapi.tiangolo.com/",
        }
    }
]


#Configure the API with detailed description
app = FastAPI(
    title = "Vanillauys Backend Documentation",
    description = "A collection of simple APIs for my front end.",
    version = "0.0.0",
    terms_of_service = "https://vanillauys.com/terms",
    contact = {
        "name": "Wihan Uys",
        "url": "https://vanillauys.com/about",
        "email": "wihan@duck.com",
    },
    license_info = {
        "name": "MIT",
        "url": "https://spdx.org/licenses/MIT.html",
    },
    openapi_tags = TAGS_METADATA,
    openapi_url = "/openapi.json",
)

#Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Add routers from different files here, to keep things tidy.
app.include_router(calculators.router)
app.include_router(crypto.router)


# ---------------------------------------------------------------------------- #
# --- Basic API Route -------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


@app.get('/', tags=['Testing'],
        response_model=Message, 
        responses={
            500: {"model": Message}
        }
)
def info():
    """
    ### Basic route to test functionality.
    """
    response = {
        'message': "https://vanillauys.com:8000/docs"
    }
    return JSONResponse(status_code=200, content=response)



# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def main():
    #Nothing to do here...
    pass


if __name__ == "__main__":
    main()
