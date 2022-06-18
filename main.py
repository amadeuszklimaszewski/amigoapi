from fastapi import FastAPI, status, Request
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from src.apps.users.routers import user_router
from src.apps.recipes.routers import recipe_router
from src.apps.reviews.routers import review_router

from src.core.exceptions import APIException

app = FastAPI()

router = APIRouter()

router.include_router(user_router)
router.include_router(recipe_router)
router.include_router(review_router)

app.include_router(router)


@app.get("/")
def root():
    return {"Amigo": "A culinary recipes website."}


@app.exception_handler(APIException)
def api_error_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
