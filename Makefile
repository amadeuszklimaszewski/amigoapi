postgres-user = postgres
postgres-database = postgres


build-dev:
	-cp -n ./config/.env.template ./.env
	docker-compose build backend

up-dev:
	docker-compose run --rm backend bash -c "alembic upgrade head"
	docker-compose start backend

bash:
	docker-compose exec backend bash

db-bash:
	docker-compose exec db bash

db-shell:
	docker-compose exec db psql -U $(postgres-user)

test:
	docker-compose exec backend bash -c "pytest -s $(location)"