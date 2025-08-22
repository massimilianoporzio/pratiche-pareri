Import-Module IISAdministration

# Crea Application Pool
$poolName = "pratiche_pareri"
$appPool = Get-IISAppPool -Name $poolName -ErrorAction SilentlyContinue
if (-not $appPool) {
    $appPool = New-IISAppPool -Name $poolName
    Write-Host "✅ Application Pool '$poolName' creato" -ForegroundColor Green
} else {
    Write-Host "✅ Application Pool '$poolName' già esistente" -ForegroundColor Yellow
}

# Configurazione Application Pool
$appPool.ProcessModel.identityType = 'ApplicationPoolIdentity'
$appPool.ProcessModel.idleTimeout = [TimeSpan]::Parse("00:00:00")
$appPool.ProcessModel.loadUserProfile = $true
$appPool.Recycling.periodicRestart.time = [TimeSpan]::Parse("00:00:00")
$appPool | Out-Null # Salva le modifiche

Write-Host "✅ Application Pool configurato" -ForegroundColor Green
