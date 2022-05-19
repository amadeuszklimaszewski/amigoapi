from fastapi import FastAPI

from src.apps.users.routers import user_router


app = FastAPI()

app.include_router(user_router)


@app.get("/")
def root():
    return {"Amigo": "A culinary recipes website."}
