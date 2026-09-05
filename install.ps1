# AG Kit v2 Windows Installer for Antigravity
# Maintained by Keith Torda

$ErrorActionPreference = "Stop"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "        AG Kit v2 Installer for Antigravity          " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

$UserProfileForward = ($env:USERPROFILE -replace '\\', '/')
$AntigravityConfig = "$env:USERPROFILE\.gemini\config"
$PluginsDir = Join-Path $AntigravityConfig "plugins\ag-kit-v2"
$RulesDir = Join-Path $AntigravityConfig "rules"

Write-Host "[1/4] Setting up directories..." -ForegroundColor Yellow
if (-not (Test-Path $PluginsDir)) {
    New-Item -ItemType Directory -Path $PluginsDir -Force | Out-Null
}
if (-not (Test-Path $RulesDir)) {
    New-Item -ItemType Directory -Path $RulesDir -Force | Out-Null
}

Write-Host "[2/4] Installing AG Kit v2 plugin and rules..." -ForegroundColor Yellow
$CurrentDir = $PSScriptRoot
Get-ChildItem -Path $CurrentDir -Exclude "rules", ".git", "install.ps1", "README.md" | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $PluginsDir -Recurse -Force
}

if (Test-Path (Join-Path $CurrentDir "rules")) {
    Copy-Item -Path (Join-Path $CurrentDir "rules\*") -Destination $RulesDir -Recurse -Force
}

Write-Host "[3/4] Adapting user paths for current machine ($env:USERNAME)..." -ForegroundColor Yellow
$DefaultUserPath = "C:/Users/Keith"
if ($UserProfileForward -ne $DefaultUserPath) {
    Write-Host "Updating user directory paths from '$DefaultUserPath' to '$UserProfileForward'..." -ForegroundColor Cyan
    $FilesToPatch = Get-ChildItem -Path $PluginsDir, $RulesDir -Include *.md, *.py, *.json -Recurse
    foreach ($file in $FilesToPatch) {
        $content = [System.IO.File]::ReadAllText($file.FullName)
        if ($content -match "C:/Users/Keith") {
            $updated = $content.Replace("C:/Users/Keith", $UserProfileForward)
            [System.IO.File]::WriteAllText($file.FullName, $updated)
        }
    }
}

Write-Host "[4/4] Validating installation..." -ForegroundColor Yellow
$ValidateScript = Join-Path $PluginsDir "scripts\validate_kit.py"
if (Test-Path $ValidateScript) {
    python $ValidateScript
}

Write-Host "`n[SUCCESS] AG Kit v2 successfully installed to Antigravity!" -ForegroundColor Green
Write-Host "Plugin Path: $PluginsDir" -ForegroundColor Gray
Write-Host "Rules Path:  $RulesDir`n" -ForegroundColor Gray
