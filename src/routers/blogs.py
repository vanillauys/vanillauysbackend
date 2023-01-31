# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schemas import Schemas
from db.blogs import BlogsDB


# ---------------------------------------------------------------------------- #
# --- Route Configuration ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


router = APIRouter()
db = BlogsDB()
schemas = Schemas()


# ---------------------------------------------------------------------------- #
# --- App Routes : Blogs Application ----------------------------------------- #
# ---------------------------------------------------------------------------- #


@router.get('/blogs/all', tags=['Blogs'],
    response_model=list[schemas.BlogInfo],
    responses={
        500: {"model": schemas.Detail}
}
)
def get_all():
    code, response, blogs = db.get_all_blogs()
    if code != 200:
        return JSONResponse(status_code=code, content={'detail': response})
    
    return JSONResponse(status_code=code, content=blogs)


@router.get('/blogs/{key}', tags=['Blogs'],
    response_model=list[schemas.Blog],
    responses={
        404: {"model": schemas.Detail},
        500: {"model": schemas.Detail}
    }
)
def get_one(key: str):
    code, response, blog = db.get_blog_by_key(key)
    if code != 200:
        return JSONResponse(status_code=code, content={'detail': response})
    
    return JSONResponse(status_code=200, content=blog)
