# Manual SAP BTP Cloud Foundry deployment helper.
# Assumes you are already logged in with cf8 and have mbt installed.

$ErrorActionPreference = "Stop"

Write-Host "--- 1. Cleaning old artifacts ---" -ForegroundColor Cyan
if (Test-Path "mta_archives") { Remove-Item -Recurse -Force "mta_archives" }
if (Test-Path "sapui5/dist") { Remove-Item -Recurse -Force "sapui5/dist" }
if (Test-Path "ui-deployer/resources") { Remove-Item -Recurse -Force "ui-deployer/resources" }

Write-Host "--- 2. Building MTA archive ---" -ForegroundColor Cyan
mbt build -t ./mta_archives --mtar ewa_analyzer.mtar

Write-Host "--- 3. Deploying to SAP BTP ---" -ForegroundColor Cyan
$params = @("deploy", "mta_archives/ewa_analyzer.mtar", "-f")
if (Test-Path "mtaext.yaml") {
    Write-Host "Using local mtaext.yaml for deployment..." -ForegroundColor Yellow
    $params += "-e"
    $params += "mtaext.yaml"
} else {
    Write-Host "No mtaext.yaml found. Deploying without credential extension." -ForegroundColor Yellow
}

cf8 $params

Write-Host "--- Deployment complete ---" -ForegroundColor Green
