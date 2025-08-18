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
run-server: rundb-if-needed
	uv run manage.py runserver

.PHONY: superuser
superuser:
	uv run manage.py createsuperuser

.PHONY: update
update: install migrate

.PHONY: dumpdata
dumpdata:
	uv run manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > initial_data.json
.PHONY: dump_incrementale
dump_incrementale:
	uv run manage.py dump_incrementale

.PHONY: loaddata_incr
loaddata_incr:
ifndef FILE_NAME
	$(error Devi specificare il nome del file. Esempio: make loaddata_incr FILE_NAME=incremental_dump_2025-08-18_171306.json)
endif
	uv run manage.py loaddata $(FILE_NAME)

.PHONY: loaddata
loaddata:
	uv run manage.py loaddata initial_data.json

.PHONY: compilemessages
compilemessages:
	uv run manage.py compilemessages

.PHONY: collectstatic
collectstatic:
	uv run manage.py collectstatic --noinput

.PHONY: rundb
rundb:
	docker compose up -d

.PHONY: stopdb
stopdb:
	 docker compose down

.PHONY: rundb-if-needed
.PHONY: rundb-if-needed
rundb-if-needed:
ifeq ($(USE_DOCKER_FOR_DB),1)
	@echo "USE_DOCKER_FOR_DB is set to 1. Starting Docker database..."
	$(MAKE) rundb
else
	@echo "USE_DOCKER_FOR_DB is not 1. Using an existing database."
endif
.PHONY: watch-css
watch-css:
	pnpm watch
