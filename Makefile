.PHONY: install
install:
	uv sync
.PHONY: migrate
migrate:
	uv run manage.py migrate
.PHONY: migrations
migrations:
	uv run manage.py makemigrations
.PHONY: run-server
run-server:
	uv run manage.py runserver
.PHONY: superuser
superuser:
	uv run manage.py createsuperuser
.PHONY: update
update: install migrate ;
