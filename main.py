from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"Amigo": "A culinary recipes website."}
