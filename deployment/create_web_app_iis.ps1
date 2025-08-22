Import-Module WebAdministration
# Crea l'applicazione sotto Default Web Site
$siteName = "Default Web Site"
$appName = "pratiche_pareri"
$physicalPath = "C:\inetpub\wwwroot\pratiche-pareri"

# Rimuovi applicazione esistente se presente
$existingApp = Get-WebApplication -Name $appName -Site $siteName -ErrorAction SilentlyContinue
if ($existingApp) {
    Remove-WebApplication -Name $appName -Site $siteName
    Write-Host "⚠️ Applicazione esistente rimossa" -ForegroundColor Yellow
}

# Crea nuova applicazione
New-WebApplication -Name $appName -Site $siteName -PhysicalPath $physicalPath -ApplicationPool $poolName
Write-Host "✅ Applicazione web '$appName' creata" -ForegroundColor Green

# Verifica
$app = Get-WebApplication -Name $appName -Site $siteName
Write-Host "✅ Applicazione configurata:" -ForegroundColor Green
Write-Host "  - Nome: $($app.Path)"
Write-Host "  - Percorso fisico: $($app.PhysicalPath)"
Write-Host "  - Application Pool: $($app.ApplicationPool)"
