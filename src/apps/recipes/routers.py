from uuid import UUID
from fastapi.routing import APIRouter
from fastapi import Depends, status
from sqlalchemy.orm import Session
from src.apps.recipes.models import Recipe
from src.apps.recipes.services import RecipeService
from src.apps.users.models import User
from src.apps.recipes.schemas import RecipeInputSchema, RecipeOutputSchema
from src.database.connection import get_db
from src.dependencies.users import authenticate_user

recipe_router = APIRouter(prefix="/recipes")


@recipe_router.get(
    "/",
    tags=["recipes"],
    status_code=status.HTTP_200_OK,
    response_model=list[RecipeOutputSchema],
)
def get_recipes(
    recipe_service: RecipeService = Depends(),
    session: Session = Depends(get_db),
) -> list[RecipeOutputSchema]:
    return [
        RecipeOutputSchema.from_orm(recipe)
        for recipe in recipe_service.get_recipe_list(session=session)
    ]


@recipe_router.get(
    "/{recipe_id}/",
    tags=["recipes"],
    status_code=status.HTTP_200_OK,
    response_model=RecipeOutputSchema,
)
def get_recipe_by_id(
    recipe_id: UUID,
    recipe_service: RecipeService = Depends(),
    session: Session = Depends(get_db),
) -> RecipeOutputSchema:
    recipe = recipe_service.get_recipe_by_id(recipe_id=recipe_id, session=session)
    return RecipeOutputSchema.from_orm(recipe)


@recipe_router.post(
    "/",
    tags=["recipes"],
    dependencies=[Depends(authenticate_user)],
    status_code=status.HTTP_201_CREATED,
    response_model=RecipeOutputSchema,
)
def create_recipe(
    recipe_input_schema: RecipeInputSchema,
    recipe_service: RecipeService = Depends(),
    request_user: User = Depends(authenticate_user),
    session: Session = Depends(get_db),
) -> RecipeOutputSchema:
    recipe = recipe_service.create_recipe(
        recipe_input_schema, user=request_user, session=session
    )
    return RecipeOutputSchema.from_orm(recipe)


@recipe_router.put(
    "/{recipe_id}/",
    tags=["recipes"],
    status_code=status.HTTP_200_OK,
    response_model=RecipeOutputSchema,
)
def update_recipe(
    recipe_id: UUID,
    update_schema: RecipeInputSchema,
    request_user: User = Depends(authenticate_user),
    recipe_service: RecipeService = Depends(),
    session: Session = Depends(get_db),
) -> RecipeOutputSchema:
    updated_recipe = recipe_service.update_recipe(
        recipe_id, user=request_user, schema=update_schema, session=session
    )
    return RecipeOutputSchema.from_orm(updated_recipe)
