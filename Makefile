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
update: install migrate
.PHONY: dumpdata
dumpdata:
	uv run manage.py dumpdata --indent 2 > initial_data.json
.PHONY: loaddata
loaddata:
	uv run manage.py loaddata initial_data.json
.PHONY: compilemessages
compilemessages:
	uv run manage.py compilemessages
