# Permessi per la cartella del progetto
$projectPath = "C:\inetpub\wwwroot\pratiche_pareri"
$poolIdentity = "IIS AppPool\$poolName"

Write-Host "🔧 Configurazione permessi..." -ForegroundColor Yellow

# Permessi base di lettura ed esecuzione
$acl = Get-Acl $projectPath
$readAccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule($poolIdentity,"ReadAndExecute","ContainerInherit,ObjectInherit","None","Allow")
$acl.SetAccessRule($readAccessRule)

# Permessi di scrittura per cartelle specifiche
$writeAccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule($poolIdentity,"FullControl","ContainerInherit,ObjectInherit","None","Allow")

# Media folder (se esiste e necessita scrittura)
$mediaPath = Join-Path $projectPath "media"
if (Test-Path $mediaPath) {
    $mediaAcl = Get-Acl $mediaPath
    $mediaAcl.SetAccessRule($writeAccessRule)
    Set-Acl $mediaPath $mediaAcl
    Write-Host "✅ Permessi di scrittura assegnati a media/" -ForegroundColor Green
}

# Applica permessi base
Set-Acl $projectPath $acl
Write-Host "✅ Permessi base assegnati al progetto" -ForegroundColor Green

# Testa nuovamente i permessi per i log
try {
    $testFile = Join-Path "E:\prod\logs\pratiche_pareri" "test_final.tmp"
    "Test finale $(Get-Date)" | Out-File $testFile
    Remove-Item $testFile
    Write-Host "✅ Permessi log funzionanti" -ForegroundColor Green
} catch {
    Write-Host "❌ Problema permessi log: $($_.Exception.Message)" -ForegroundColor Red
}
