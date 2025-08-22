# Imposta esplicitamente le variabili d'ambiente
$env:DATABASE_PASSWORD = "la_tua_password_di_produzione"
$env:DEBUG = "0"
$env:USE_DOCKER_FOR_DB = "0"
$env:PRODUCTION = "1"
$env:SECRET_KEY = "your-secret-key"
$env:DJANGO_ALLOWED_HOSTS = "* localhost 127.0.0.1 [::1]"

# Esegui il comando di migrazione
.\.venv\Scripts\uv.exe run manage.prod.py migrate
