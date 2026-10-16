[CmdletBinding()]
param(
    [string]$ConfigRoot = (Join-Path $env:USERPROFILE '.gemini\config'),
    [string]$BackupRoot = '',
    [string]$PythonCommand = 'python',
    [switch]$Check
)
$ErrorActionPreference = 'Stop'
$sourceRoot = [IO.Path]::GetFullPath($PSScriptRoot)
$configPath = [IO.Path]::GetFullPath($ConfigRoot)
$pluginParent = Join-Path $configPath 'plugins'
$pluginPath = [IO.Path]::GetFullPath((Join-Path $pluginParent 'ag-kit-v2'))
$rulesPath = Join-Path $configPath 'rules'
$globalPath = Join-Path (Split-Path -Parent $configPath) 'GEMINI.md'
$ruleNames = @('core-protocol.md','code-rules.md','design-rules.md','engineering-excellence.md','request-routing.md','universal-rules.md','quick-reference.md')
$obsoleteNames = @('copy.md','design.md','core.md','code.md','routing.md','anti-ai.md')

function Write-Utf8([string]$Path, [string]$Content) {
    [IO.File]::WriteAllText($Path, $Content, (New-Object Text.UTF8Encoding($false)))
}
function Assert-ChildPath([string]$Path, [string]$Parent) {
    $resolved = [IO.Path]::GetFullPath($Path)
    $prefix = [IO.Path]::GetFullPath($Parent).TrimEnd('\','/') + [IO.Path]::DirectorySeparatorChar
    if (!$resolved.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) { throw "Path escapes intended directory: $resolved" }
}
function Invoke-Validation([string]$Kit, [string]$Rules) {
    & $PythonCommand -B (Join-Path $Kit 'scripts\validate_kit.py') $Kit --rules $Rules --strict --quiet
    if ($LASTEXITCODE -ne 0) { throw "Kit validation failed (exit $LASTEXITCODE)." }
}
function Test-ObsoleteKitRule([string]$Path) {
    if (!(Test-Path -LiteralPath $Path -PathType Leaf)) { return $false }
    $content = [IO.File]::ReadAllText($Path)
    $kitSignature = $content -match '(?i)\bAG\s?Kit\b|plugins[/\\]+agkit3|no automatic gates|Ten code rules that apply|Which agent handles which request'
    return ($kitSignature -and $content -match '(?im)^version:\s*3\.' -and $content -match '(?im)^name:\s*(core|code|routing|design|anti-ai)\s*$') -or
           ($kitSignature -and $content -match '(?im)^name:\s*(copy|design)\s*$')
}

if ($pluginPath -eq $sourceRoot -or $sourceRoot.StartsWith($pluginPath + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Run install.ps1 from the source repository, not from the installed plugin.'
}
Assert-ChildPath $pluginPath $pluginParent
Invoke-Validation $sourceRoot (Join-Path $sourceRoot 'rules')
if ($Check) { Write-Output 'Source validation passed. No installation changes made.'; return }

$operationId = (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0,8)
if (!$BackupRoot) { $BackupRoot = Join-Path $configPath 'agkit-backups' }
$backupPath = Join-Path ([IO.Path]::GetFullPath($BackupRoot)) $operationId
$stagePath = [IO.Path]::GetFullPath((Join-Path $configPath ('.agkit2-stage-' + $operationId)))
Assert-ChildPath $stagePath $configPath
if (Test-Path -LiteralPath $stagePath) { throw 'Staging path already exists.' }
New-Item -ItemType Directory -Path (Join-Path $stagePath 'plugin') -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $stagePath 'rules') -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $backupPath 'rules') -Force | Out-Null

$ruleSnapshots = @{}
$globalExisted = Test-Path -LiteralPath $globalPath -PathType Leaf
$pluginExisted = Test-Path -LiteralPath $pluginPath -PathType Container
$pluginMoved = $false
$newPluginActive = $false
$rulesTouched = $false
$globalTouched = $false
try {
    foreach ($folder in @('agents','skills','scripts')) {
        Copy-Item -LiteralPath (Join-Path $sourceRoot $folder) -Destination (Join-Path $stagePath 'plugin') -Recurse
    }
    foreach ($file in @('plugin.json','VERSION','LICENSE')) {
        Copy-Item -LiteralPath (Join-Path $sourceRoot $file) -Destination (Join-Path $stagePath 'plugin')
    }
    $sourceKitPath = 'C:/Users/Keith/.gemini/config/plugins/ag-kit-v2'
    foreach ($ruleName in $ruleNames) {
        $content = [IO.File]::ReadAllText((Join-Path $sourceRoot ('rules\' + $ruleName)))
        $content = $content.Replace($sourceKitPath, $pluginPath.Replace('\','/'))
        Write-Utf8 (Join-Path $stagePath ('rules\' + $ruleName)) $content
    }
    Invoke-Validation (Join-Path $stagePath 'plugin') (Join-Path $stagePath 'rules')
    foreach ($ruleName in ($ruleNames + $obsoleteNames)) {
        $activeRule = Join-Path $rulesPath $ruleName
        if (Test-Path -LiteralPath $activeRule -PathType Leaf) {
            $ruleSnapshots[$ruleName] = $true
            Copy-Item -LiteralPath $activeRule -Destination (Join-Path $backupPath 'rules')
        } else { $ruleSnapshots[$ruleName] = $false }
    }
    if ($globalExisted) { Copy-Item -LiteralPath $globalPath -Destination (Join-Path $backupPath 'GEMINI.md') }
    New-Item -ItemType Directory -Path $pluginParent,$rulesPath -Force | Out-Null
    if ($pluginExisted) {
        Move-Item -LiteralPath $pluginPath -Destination (Join-Path $backupPath 'installed-plugin')
        $pluginMoved = $true
    }
    Move-Item -LiteralPath (Join-Path $stagePath 'plugin') -Destination $pluginPath
    $newPluginActive = $true
    $rulesTouched = $true
    foreach ($ruleName in $ruleNames) {
        Copy-Item -LiteralPath (Join-Path $stagePath ('rules\' + $ruleName)) -Destination $rulesPath -Force
    }
    foreach ($oldName in $obsoleteNames) {
        $oldRule = Join-Path $rulesPath $oldName
        if (Test-ObsoleteKitRule $oldRule) {
            Move-Item -LiteralPath $oldRule -Destination (Join-Path $backupPath ('removed-' + $oldName))
        }
    }
    $version = ([IO.File]::ReadAllText((Join-Path $pluginPath 'VERSION'))).Trim()
    $managedBlock = @"
<!-- AGKIT2:START -->
# AGKIT2 $version
Kit: ``$($pluginPath.Replace('\','/'))``.
Rules: ``$($rulesPath.Replace('\','/'))``. Read core-protocol and request-routing there before acting; use code-rules for verification and design-rules before new visual design, including before UI files exist.
Before a new visual design ask briefly about style and references, and wait. Reuse an answer already supplied; an explicit 'you choose' delegates the choice. Maintenance matching an approved design needs no repeat intake.
Follow the accepted direction and project conventions. Visual styles are flexible; verification reports the evidence that actually ran.
<!-- AGKIT2:END -->
"@
    $priorGlobal = if ($globalExisted) { [IO.File]::ReadAllText($globalPath) } else { '' }
    if ($priorGlobal -match '(?s)<!-- AGKIT2:START -->.*?<!-- AGKIT2:END -->') {
        $updatedGlobal = [regex]::Replace($priorGlobal, '(?s)<!-- AGKIT2:START -->.*?<!-- AGKIT2:END -->', [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $managedBlock })
    } elseif ($priorGlobal -match '(?im)^# AG Kit v[23].*Global Agent Guidelines') {
        # Remove recognized legacy kit lines; preserve unrelated text even below that heading.
        $legacyLine = '^(# AG Kit v[23].*Global Agent Guidelines|This machine (uses|runs).*AG Kit|-\s+(Kit root:|Rules:|Workflow:|Follow.*core-protocol|Read the selected agent|The user.s explicit request|Verify changes in proportion|\*\*Nothing runs automatically|Verification and browser checks))'
        $unmanaged = @($priorGlobal -split '\r?\n' | Where-Object { $_ -notmatch $legacyLine }) -join "`n"
        $updatedGlobal = $unmanaged.Trim() + "`n`n" + $managedBlock
    } else {
        $updatedGlobal = $priorGlobal.TrimEnd() + "`n`n" + $managedBlock
    }
    $globalTouched = $true
    Write-Utf8 $globalPath ($updatedGlobal.Trim() + "`n")
    Invoke-Validation $pluginPath $rulesPath
    $manifest = @{version=$version; source=$sourceRoot; plugin=$pluginPath; rules=$ruleNames; backup=$backupPath; installedAt=[DateTimeOffset]::Now.ToString('o')}
    Write-Utf8 (Join-Path $backupPath 'installation.json') ($manifest | ConvertTo-Json -Depth 4)
    Assert-ChildPath $stagePath $configPath
    Remove-Item -LiteralPath $stagePath -Recurse -Force
    Write-Output "Installed AGKIT2 $version. Backup: $backupPath"
    Write-Output 'Restart Antigravity and open a new chat to load the updated instructions.'
} catch {
    $failure = $_
    if ($newPluginActive -and (Test-Path -LiteralPath $pluginPath)) {
        Assert-ChildPath $pluginPath $pluginParent
        Move-Item -LiteralPath $pluginPath -Destination (Join-Path $backupPath 'failed-plugin')
    }
    if ($pluginMoved) { Move-Item -LiteralPath (Join-Path $backupPath 'installed-plugin') -Destination $pluginPath }
    if ($rulesTouched) {
        foreach ($ruleName in ($ruleNames + $obsoleteNames)) {
            $activeRule = Join-Path $rulesPath $ruleName
            if ($ruleSnapshots[$ruleName]) {
                Copy-Item -LiteralPath (Join-Path $backupPath ('rules\' + $ruleName)) -Destination $activeRule -Force
            } elseif ((Test-Path -LiteralPath $activeRule) -and ($ruleNames -contains $ruleName)) {
                Remove-Item -LiteralPath $activeRule -Force
            }
        }
    }
    if ($globalTouched) {
        if ($globalExisted) { Copy-Item -LiteralPath (Join-Path $backupPath 'GEMINI.md') -Destination $globalPath -Force }
        elseif (Test-Path -LiteralPath $globalPath) { Remove-Item -LiteralPath $globalPath -Force }
    }
    throw "Installation failed; previous active files restored. Staging/backup retained at $backupPath. $failure"
}
