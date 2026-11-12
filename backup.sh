#!/usr/bin/env bash
# Daily consistent SQLite backup, keeps 14. Cron: 0 2 * * * /path/backup.sh
set -e; mkdir -p backups
sqlite3 "${DB_PATH:-mediassist.db}" ".backup 'backups/mediassist-$(date +%F).db'"
ls -1t backups/*.db | tail -n +15 | xargs -r rm
