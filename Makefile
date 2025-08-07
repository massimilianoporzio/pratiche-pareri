install:
	uv sync
migrate:
	uv run manage.py migrate
migrations:
	uv run manage.py makemigrations
run-server:
	uv run manage.py runserver
superuser:
	uv run manage.py createsuperuser
update: install migrate ;
