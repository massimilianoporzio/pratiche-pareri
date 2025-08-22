# Script per creare e configurare la cartella log
$poolName = "pratiche_pareri"
$logPath = "E:\prod\logs\pratiche_pareri"

Write-Host "🔧 Configurazione cartella log..." -ForegroundColor Yellow

# Crea la cartella
New-Item -ItemType Directory -Path $logPath -Force
Write-Host "✅ Cartella creata: $logPath" -ForegroundColor Green

# Assegna permessi all'Application Pool (che creeremo dopo)
$acl = Get-Acl $logPath
$identity = "IIS AppPool\$poolName"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule($identity,"FullControl","ContainerInherit,ObjectInherit","None","Allow")
$acl.SetAccessRule($accessRule)
Set-Acl $logPath $acl

Write-Host "✅ Permessi assegnati a: $identity" -ForegroundColor Green

# Test di scrittura (fallirà ora ma confermerà la struttura)
try {
    $testFile = Join-Path $logPath "test_setup.tmp"
    "Test setup $(Get-Date)" | Out-File $testFile
    Remove-Item $testFile
    Write-Host "✅ Test scrittura riuscito" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Test scrittura fallito (normale prima di creare l'Application Pool)" -ForegroundColor Yellow
}
