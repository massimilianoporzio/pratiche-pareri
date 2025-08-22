# Definisci il percorso e l'URL del repository
$repoPath = "E:\prod\pratiche_pareri"
$repoUrl = "https://github.com/massimilianoporzio/pratiche-pareri.git"

# Verifica se la cartella esiste
if (Test-Path -Path $repoPath) {
    Write-Host "✅ La cartella '$repoPath' esiste. Eseguo git pull..." -ForegroundColor Green

    # Entra nella cartella
    Set-Location -Path $repoPath

    # Esegue il pull per aggiornare
    git pull

}
else {
    Write-Host "🔧 La cartella '$repoPath' non esiste. La creo e clono il repository..." -ForegroundColor Yellow

    # Crea la cartella
    New-Item -ItemType Directory -Path $repoPath -Force

    # Entra nella cartella
    Set-Location -Path $repoPath

    # Clona il repository
    git clone $repoUrl .
}

# Verifica che i file siano presenti
Write-Host "---"
Write-Host "File presenti:" -ForegroundColor Cyan
Get-ChildItem -Name
