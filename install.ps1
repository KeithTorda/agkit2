# AG Kit v2.5 installer for Google Antigravity (Windows, PowerShell 7 or 5.1)
# Maintained by Keith Torda
$ErrorActionPreference = "Stop"

$Src       = $PSScriptRoot
$Config    = Join-Path $env:USERPROFILE ".gemini\config"
$PluginDir = Join-Path $Config "plugins\ag-kit-v2"
$RulesDir  = Join-Path $Config "rules"
$UserPath  = ($env:USERPROFILE -replace '\\', '/')

$Rules = @(
    "core-protocol.md", "engineering-excellence.md", "code-rules.md", "design-rules.md",
    "request-routing.md", "universal-rules.md", "quick-reference.md"
)
# Kit rule files from older versions that must not stay installed
$StaleRules = @("copy.md", "design.md")

Write-Host "AG Kit v2.5 -> $PluginDir"

# 1. Clean plugin install so removed files never linger
if (Test-Path $PluginDir) { Remove-Item $PluginDir -Recurse -Force }
New-Item -ItemType Directory -Path $PluginDir -Force | Out-Null
New-Item -ItemType Directory -Path $RulesDir  -Force | Out-Null

foreach ($d in @("agents", "skills", "scripts")) {
    Copy-Item -Path (Join-Path $Src $d) -Destination $PluginDir -Recurse -Force
}
foreach ($f in @("plugin.json", "VERSION", "LICENSE")) {
    $p = Join-Path $Src $f
    if (Test-Path $p) { Copy-Item -Path $p -Destination $PluginDir -Force }
}
Get-ChildItem $PluginDir -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# 2. Rules: remove stale kit rules, then copy the current set
foreach ($r in $StaleRules) {
    $p = Join-Path $RulesDir $r
    if ((Test-Path $p) -and ((Get-Content $p -Raw) -match "(?m)^name:\s*(copy|design)\s*$")) {
        Remove-Item $p -Force
        Write-Host "  removed stale rule $r"
    }
}
foreach ($r in $Rules) {
    Copy-Item -Path (Join-Path $Src "rules\$r") -Destination $RulesDir -Force
}

# 3. Point KIT at this user's profile (paths are quoted in the kit, so spaces are safe)
if ($UserPath -ne "C:/Users/Keith") {
    $targets = @(Get-ChildItem -Path $PluginDir -Recurse -File -Include *.md, *.json) +
               @($Rules | ForEach-Object { Get-Item (Join-Path $RulesDir $_) })
    foreach ($f in $targets) {
        $c = [System.IO.File]::ReadAllText($f.FullName)
        if ($c.Contains("C:/Users/Keith")) {
            [System.IO.File]::WriteAllText($f.FullName, $c.Replace("C:/Users/Keith", $UserPath))
        }
    }
}

# 4. Validate
python (Join-Path $PluginDir "scripts\validate_kit.py") "$PluginDir" --rules "$RulesDir" --quiet
$n = (Get-ChildItem $PluginDir -Recurse -File).Count
Write-Host "Installed $n files and $($Rules.Count) rules. Restart Antigravity, then try /status in a project."
