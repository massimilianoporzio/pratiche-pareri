# Raccogli i file statici
python manage.py collectstatic --noinput --settings=pratiche.conf.prod
Write-Host "✅ File statici raccolti" -ForegroundColor Green

# Verifica
if (Test-Path "staticfiles") {
    $count = (Get-ChildItem -Recurse staticfiles | Measure-Object).Count
    Write-Host "✅ $count file statici trovati" -ForegroundColor Green
} else {
    Write-Host "❌ Cartella staticfiles non trovata" -ForegroundColor Red
}
