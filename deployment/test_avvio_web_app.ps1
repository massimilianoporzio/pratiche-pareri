Write-Host "=== TEST MANUALE WAITRESS ===" -ForegroundColor Cyan
Write-Host "Esegui questo test manuale:" -ForegroundColor Yellow
Write-Host "1. cd C:\inetpub\wwwroot\pratiche_pareri"
Write-Host "2. .\.venv\Scripts\activate"
Write-Host "3. python waitress_server.py"
Write-Host "4. Vai su http://localhost:8000/pratiche_pareri/"
Write-Host "5. Se funziona, premi Ctrl+C per fermare e procedi"
Write-Host ""
Read-Host "Premi INVIO quando hai testato..."
