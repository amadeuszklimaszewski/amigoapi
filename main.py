from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from src.apps.users.routers import user_router

from src.apps.recipes.routers import recipe_router
from src.core.exceptions import APIError

app = FastAPI()

app.include_router(user_router)
app.include_router(recipe_router)


@app.get("/")
def root():
    return {"Amigo": "A culinary recipes website."}


@app.exception_handler(APIError)
def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
    )


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
