---
name: vps-safe-deploy
description: Use this skill when deploying applications, editing Nginx/PHP-FPM/PM2/systemd configurations, or running database migrations on live Ubuntu / Contabo VPS servers (such as 147.93.158.118).
---

# Contabo VPS Safe Deployment & Operations Skill

## 1. Mandatory Pre-Change Backups

1. **Configuration Files:** Before editing any live config (`/etc/nginx/sites-available/*`, `.env`, `/etc/systemd/system/*`), create a timestamped backup:
   ```bash
   cp /etc/nginx/sites-available/app.conf "/etc/nginx/sites-available/app.conf.bak.$(date +%Y%m%d-%H%M)"
   ```
2. **Databases:** Before running schema migrations or data updates on MariaDB/MySQL or SQLite:
   - MariaDB: `mysqldump --single-transaction <db_name> > "/root/backups/<db_name>_$(date +%Y%m%d-%H%M).sql"`
   - SQLite: `sqlite3 database.sqlite ".backup 'database.sqlite.bak.$(date +%Y%m%d-%H%M)'"`
   - Verify the backup file is non-empty (`ls -lh`) before proceeding.
   - Never run `migrate:fresh`, `db:wipe`, `DROP TABLE`, or `TRUNCATE` on production without explicit user approval.

## 2. Verification Before & After Service Reloads

1. **Nginx:** Always run `nginx -t` first. Reload (`systemctl reload nginx`) only when syntax test reports `syntax is ok` and `test is successful`.
2. **PHP-FPM:** Run `php-fpm8.3 -t` before restarting `php8.3-fpm`.
3. **Node / PM2:** Verify the target port is free (`ss -tulpn`), start/reload the named process (`pm2 reload <app-name>`), and run `pm2 save`.
4. **Laravel Production Cache & Permissions:**
   - Ensure `storage/` and `bootstrap/cache/` are writable by `www-data`.
   - Run `php artisan migrate --force` (only after DB backup) and `php artisan optimize`.
5. **Static Asset Cache Busting:** Bump `?v=X.Y.Z` or content hashes on updated CSS/JS files so client browsers load fresh styles immediately.
6. **Post-Deploy Smoke Check:** Check `curl -I` HTTP status (`200` / `302`) and inspect bounded recent error logs (`journalctl -u nginx -n 20 --no-pager` or app log tail) without printing secret `.env` values.
