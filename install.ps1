[CmdletBinding()]
param(
    [string]$PluginsRoot = (Join-Path $env:USERPROFILE '.gemini\config\plugins'),
    [string]$ArchiveRoot = 'c:\Users\Keith\Desktop\CONTABO VPS\archives\keith-agkit-backups',
    [switch]$Check
)

$ErrorActionPreference = 'Stop'
$sourceRoot = [IO.Path]::GetFullPath($PSScriptRoot)
$targetPluginDir = Join-Path ([IO.Path]::GetFullPath($PluginsRoot)) 'keith-agkit'

& python -B (Join-Path $sourceRoot 'scripts\validate_keith_kit.py')
if ($LASTEXITCODE -ne 0) {
    throw "Validation failed with exit code $LASTEXITCODE."
}

if ($Check) {
    Write-Output 'Check completed cleanly. No global files were modified.'
    return
}

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
New-Item -ItemType Directory -Path $PluginsRoot -Force | Out-Null

if (Test-Path -LiteralPath $targetPluginDir) {
    $backupDest = Join-Path $ArchiveRoot "keith-agkit-$timestamp"
    New-Item -ItemType Directory -Path $ArchiveRoot -Force | Out-Null
    Copy-Item -LiteralPath $targetPluginDir -Destination $backupDest -Recurse -Force
    Write-Output "Backed up previous plugin install to: $backupDest"
}

New-Item -ItemType Directory -Path $targetPluginDir -Force | Out-Null
# Clean stale subdirectories before copying fresh bundle
foreach ($existing in Get-ChildItem -LiteralPath $targetPluginDir -Force -ErrorAction SilentlyContinue) {
    Remove-Item -LiteralPath $existing.FullName -Recurse -Force
}
foreach ($item in @('plugin.json', 'VERSION', 'README.md', 'rules', 'skills', 'agents', 'component-catalog', 'ui-kit', 'scripts')) {
    Copy-Item -LiteralPath (Join-Path $sourceRoot $item) -Destination $targetPluginDir -Recurse -Force
}

Write-Output "Installed keith-agkit cleanly into: $targetPluginDir"
Write-Output 'Toggle it on or off anytime as one unit in Antigravity Customizations.'
