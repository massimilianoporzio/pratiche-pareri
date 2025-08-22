$env:DJANGO_SETTINGS_MODULE = "pratiche.conf.prod"

$pythonCode = @"
import django
django.setup()
print('✅ Django configurato correttamente')
from django.conf import settings
print(f'✅ FORCE_SCRIPT_NAME: {settings.FORCE_SCRIPT_NAME}')
print(f'✅ STATIC_URL: {settings.STATIC_URL}')
print(f'✅ LOG_DIR: {getattr(settings, "LOG_DIR", "Non configurato")}')
"@

python -c "$pythonCode"
