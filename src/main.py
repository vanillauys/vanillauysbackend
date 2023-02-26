# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from routers import calculators, crypto, users, budgets, notes, blogs
from schemas import Schemas
from dotenv import load_dotenv


# ---------------------------------------------------------------------------- #
# --- App Configuration ------------------------------------------------------ #
# ---------------------------------------------------------------------------- #

load_dotenv()
schemas = Schemas()
favicon_path = 'icon.jpg'

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
        "name": "Users",
        "description": "User sign up and authentication."
    },
    {
        "name": "Budgets",
        "description": "Keeping track of income and expenses."
    },
    {
        "name": "Notes",
        "description": "For taking simple notes."
    },
    {
        "name": "Blogs",
        "description": "AI Generated blogs from YouTube videos."
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


# Configure the API with detailed description
app = FastAPI(
    title="Vanillauys Backend Documentation",
    description="A collection of simple APIs for my front end.",
    version="0.5.1",
    terms_of_service="https://vanillauys.vercel.app/about",
    contact={
        "name": "Wihan Uys",
        "url": "https://vanillauys.vercel.app/about",
        "email": "wihan@duck.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://spdx.org/licenses/MIT.html",
    },
    openapi_tags=TAGS_METADATA,
    openapi_url="/openapi.json",
)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers from different files here, to keep things tidy.
app.include_router(calculators.router)
app.include_router(crypto.router)
app.include_router(users.router)
app.include_router(budgets.router)
app.include_router(notes.router)
app.include_router(blogs.router)


# ---------------------------------------------------------------------------- #
# --- Basic API Route -------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


@app.get('/', tags=['Testing'],
    response_model=schemas.Detail,
    responses={
        500: {"model": schemas.Detail}
    }
)
def info():
    """
    ### Basic route to test functionality.
    """
    response = {
        'detail': "https://vanillauys-1-t9282601.deta.app/"
    }
    return JSONResponse(status_code=200, content=response)


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def main():
    load_dotenv()
    # Nothing to do here...


if __name__ == "__main__":
    main()
