# waitress_server.py - nuovo file nella root
import os
import sys

from waitress import serve

# Importa l'applicazione WSGI dal tuo file esistente
from pratiche.wsgi_prod import application

# Aggiungi il percorso del progetto Django
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Imposta la variabile d'ambiente per Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pratiche.conf.prod")

if __name__ == "__main__":
    print("Avvio Waitress server per pratiche_pareri...")
    print("Server disponibile su: http://127.0.0.1:8000/pratiche_pareri/")
    serve(application, host="127.0.0.1", port=8000, url_prefix="/pratiche_pareri")
