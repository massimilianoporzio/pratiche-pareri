.PHONY: install
install:
	uv sync

.PHONY: migrate
migrate:
	uv run manage.py migrate

.PHONY: migrate-stage
migrate-stage:
	uv run manage.stage.py migrate

.PHONY: migrations
migrations:
	uv run manage.py makemigrations

.PHONY: migrations-stage
migrations-stage:
	uv run manage.stage.py makemigrations

.PHONY: run-server-docker-prod
run-server-docker-prod: rundb-if-needed
	uv run manage.prod.py runserver

.PHONY: run-server
run-server: rundb-if-needed
	uv run manage.py runserver

.PHONY: run-server-stage
run-server-stage:
	uv run manage.stage.py runserver

.PHONY: superuser
superuser:
	uv run manage.py createsuperuser

.PHONY: update
update: install migrate

.PHONY: dumpdata
dumpdata:
	python -Xutf8  manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > initial_data.json

.PHONY: dump_incrementale
dump_incrementale:
	python -Xutf8  manage.py dump_incrementale

.PHONY: loaddata_incr
loaddata_incr:
ifndef FILE_NAME
	$(error Devi specificare il nome del file. Esempio: make loaddata_incr FILE_NAME=incremental_dump_2025-08-18_171306.json)
endif
	uv run manage.py loaddata $(FILE_NAME)


.PHONY: dump_full
dump_full:
	@echo "Eseguo il dump di tutte le tabelle..."
	@python -Xutf8  manage.py dumpdata --exclude contenttypes --exclude auth.Permission auth.Group users.customuser cities_light.country cities_light.region cities_light.subregion cities_light.city pareri datoriLavoro --indent 2 --output fixtures/full_dump.json

.PHONY: loaddata_full-stage
loaddata_full-stage:
	@echo "Carico i dati da un dump completo..."
	@python -Xutf8  manage.stage.py  loaddata --traceback fixtures/full_dump.json

.PHONY: loaddata_full-prod
loaddata_full-prod:
	@echo "Carico i dati da un dump completo..."
	@python -Xutf8  manage.prod.py  loaddata --traceback fixtures/full_dump.json

.PHONY: loaddata_full-dev
loaddata_full-dev:
	@echo "Carico i dati da un dump completo..."
	@python -Xutf8  manage.py  loaddata --traceback fixtures/full_dump.json


.PHONY: loaddata-stage
loaddata-stage:
ifndef TIMESTAMP
	$(error Devi specificare un timestamp. Esempio: make loaddata_stage TIMESTAMP=2025-08-18_174749)
endif
	@echo "Carico i dati statici..."
	@for %%m in (country region subregion city) do @if exist "fixtures\$(TIMESTAMP)\dump_%%m_$(TIMESTAMP).json" ( python -Xutf8  manage.stage.py loaddata --traceback "fixtures\$(TIMESTAMP)\dump_%%m_$(TIMESTAMP).json" ) else ( echo "Nessun file di dump statico trovato per %%m, saltando..." )

	@echo "Carico i dati dinamici..."
	@for %%m in (customuser datorelavoro sede datorelavorosede) do @if exist "fixtures\$(TIMESTAMP)\incremental_dump_%%m_$(TIMESTAMP).json" ( python -Xutf8  manage.stage.py loaddata --traceback "fixtures\$(TIMESTAMP)\incremental_dump_%%m_$(TIMESTAMP).json" ) else ( echo "Nessun file di dump incrementale trovato per %%m, saltando..." )

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

.PHONY: dump_all
dump_all:
	@powershell -command " \
		$$TIMESTAMP = Get-Date -Format 'yyyy-MM-dd_HHmmss'; \
		Write-Host \"Creating dump with timestamp: $$TIMESTAMP\"; \
		python -Xutf8 manage.py dump_static $$TIMESTAMP; \
		python -Xutf8 manage.py dump_incrementale $$TIMESTAMP; \
	"
