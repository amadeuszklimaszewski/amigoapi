from fastapi.routing import APIRouter

user_router = APIRouter(prefix="/users")


@user_router.get("/")
def root():
    return {"Users": "users"}
