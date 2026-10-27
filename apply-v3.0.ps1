# AGKIT2 3.0.0 apply script
$ErrorActionPreference = 'Stop'
$kit = [IO.Path]::GetFullPath($PSScriptRoot)
$update = Join-Path $kit '_v3.0-update'
if (!(Test-Path -LiteralPath $update)) { throw "Update folder not found: $update" }
$backup = Join-Path (Split-Path -Parent $kit) 'agkit2-backup-v2.9.0'
if (Test-Path -LiteralPath $backup) { $backup = $backup + '-' + (Get-Date -Format 'yyyyMMdd-HHmmss') }

Write-Output "1/5 Backing up $kit -> $backup"
robocopy $kit $backup /E /XD $update /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "Backup failed (robocopy exit $LASTEXITCODE)" }

Write-Output '2/5 Copying updated files'
robocopy $update $kit /E /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "Update copy failed (robocopy exit $LASTEXITCODE)" }

Write-Output '3/5 Removing old agents and v2.9 helpers'
$remove = @('agents\seo-specialist.md','agents\mobile-developer.md','agents\solution-architect.md','agents\frontend-specialist.md','agents\ux-architect.md','agents\database-architect.md','agents\security-auditor.md','agents\documentation-writer.md','agents\performance-optimizer.md','agents\plan-reviewer.md','agents\code-archaeologist.md','agents\project-planner.md','agents\penetration-tester.md','agents\backend-specialist.md','agents\explorer-agent.md','agents\product-manager.md','agents\orchestrator.md','agents\test-engineer.md','apply-v2.9.ps1','RUN-apply-v2.9.cmd')
foreach ($rel in $remove) {
    $p = Join-Path $kit $rel
    if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p -Recurse -Force; Write-Output "   removed $rel" }
}
Get-ChildItem -LiteralPath $kit -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force
Remove-Item -LiteralPath $update -Recurse -Force

Write-Output '4/5 Validating source'
& (Join-Path $kit 'install.ps1') -Check

Write-Output '5/5 Installing into Antigravity (~/.gemini/config)'
& (Join-Path $kit 'install.ps1')
Write-Output "Done. Backup of the v2.9 kit: $backup"
