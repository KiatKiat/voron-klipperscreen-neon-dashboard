#!/usr/bin/env bash
set -euo pipefail
KS_DIR="${1:-$HOME/KlipperScreen}"
BACKUP_FILE="$KS_DIR/.voron-dashboard-backup-path"

if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "ERROR: backup pointer not found: $BACKUP_FILE" >&2
  exit 1
fi
BACKUP="$(cat "$BACKUP_FILE")"
if [[ ! -f "$BACKUP/panels/main_menu.py" || ! -f "$BACKUP/base.css" ]]; then
  echo "ERROR: backup is incomplete: $BACKUP" >&2
  exit 1
fi

cp -a "$BACKUP/panels/main_menu.py" "$KS_DIR/panels/main_menu.py"
cp -a "$BACKUP/base.css" "$KS_DIR/styles/base.css"
if [[ -f "$BACKUP/panels/voron_dashboard.py" ]]; then
  cp -a "$BACKUP/panels/voron_dashboard.py" "$KS_DIR/panels/voron_dashboard.py"
else
  rm -f "$KS_DIR/panels/voron_dashboard.py"
fi
rm -f "$KS_DIR/.voron-dashboard-backup-path"
echo "Original KlipperScreen files restored from: $BACKUP"
echo "Restart KlipperScreen: sudo systemctl restart KlipperScreen"
