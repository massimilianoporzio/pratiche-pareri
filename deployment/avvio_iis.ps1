# Riavvia IIS per applicare tutte le configurazioni
Write-Host "🔄 Riavvio IIS..." -ForegroundColor Yellow
iisreset

# Attendi qualche secondo per l'avvio
Start-Sleep -Seconds 5

# Verifica stato Application Pool
$pool = Get-IISAppPool -Name $poolName
Write-Host "✅ Application Pool stato: $($pool.State)" -ForegroundColor Green

Write-Host "=== DEPLOYMENT COMPLETATO ===" -ForegroundColor Green
Write-Host "Il sito dovrebbe essere disponibile su:" -ForegroundColor Cyan
Write-Host "http://10.69.86.123/pratiche-pareri/" -ForegroundColor White
