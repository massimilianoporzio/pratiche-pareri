# Deploy su Windows Server IIS

## Prerequisiti

- Windows Server con IIS
- HTTPPlatformHandler installato
- Python e uv

## Deploy (apri terminale powershell)

1. Clona il repository in `E:\prod\pratiche-pareri`
2. Crea virtual environment: `uv venv`
3. Installa dipendenze: `uv sync`
4. Configura Application Pool "pratiche_pareri"
5. Crea applicazione IIS "pratiche_pareri" sotto un sito (es: Default Site) che ascolta sulla porta 80
6. Configura cartella log: `E:\prod\logs\pratiche_pareri` (puoi usare lo script 'setup_log.ps1')
7. Raccogli file statici: `uv run manage.prod.py collectstatic`

## URL

Il sito sarà disponibile su: `http://server-ip/pratiche_pareri/`

## Log

- Django: `E:\prod\logs\pratiche_pareri\pratiche_pareri.log`
- IIS: `C:\inetpub\wwwroot\mio-sito\python.log`
