@echo off
cd /d "%~dp0"
set "GIT=git"
where git >nul 2>nul || set "GIT=%USERPROFILE%\PortableGit\cmd\git.exe"
echo Using: %GIT%
"%GIT%" status --short
"%GIT%" add -A
"%GIT%" commit -m "AGKIT2 3.0.0: own rules (01-06) and 14 rebuilt agents" -m "- Removed old v2.8 rules, /motionv and mandatory browser checks (2.9.0)" -m "- Added Rule 02 Work Style, 03 Code Standards, 04 System Integration (Option B), 05 Planning and Docs, 06 Security Baseline" -m "- Rebuilt agents 20 -> 14 on one template; updated skills, validator, tests and installer" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -m "Claude-Session: https://claude.ai/code/session_011h5x3m7EwfbiC8Th2hzGCG"
"%GIT%" push origin main
echo.
echo ===== Result =====
"%GIT%" log --oneline -3
"%GIT%" status -sb
echo.
pause
