# amigoapi
A FastAPI culinary recipes website created for learning purposes.

## Functionality
* SwaggerUI docs available at `localhost:8000/docs`.
* Users can register, login and update profile.
* Users can create and update recipes and reviews.
* Implemented authentication and authorization using JWT.


## Tech stack
* FastAPI 0.78.0
* SQLAlchemy + Alembic
* Docker
* PostgreSQL

## Setup
1. Clone repository:
`$ git clone https://github.com/amadeuszklimaszewski/amigoapi/`
2. Run in root directory:
`$ make build-dev`
3. Provide `AUTHJWT_SECRET_KEY` in .env file
4. Run project: `make up-dev`

## Tests
`$ make test`

## Makefile
`Makefile` contains useful command aliases
