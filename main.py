from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse
from src.apps.users.routers import user_router
from src.core.exceptions import APIError, AlreadyExists

app = FastAPI()

app.include_router(user_router)


@app.exception_handler(APIError)
def api_error_handler(request, exc):
    return PlainTextResponse(content=str(exc), status_code=400)


@app.get("/")
def root():
    return {"Amigo": "A culinary recipes website."}
