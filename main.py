from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse
from src.apps.users.routers import user_router
from src.core.exceptions import APIError

app = FastAPI()

app.include_router(user_router)


@app.exception_handler(APIError)
def api_error_handler(request, exc):
    return PlainTextResponse(content=str(exc), status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/")
def root():
    return {"Amigo": "A culinary recipes website."}
