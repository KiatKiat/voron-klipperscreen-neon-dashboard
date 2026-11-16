#!/usr/bin/env bash
set -euo pipefail
KS_DIR="${1:-$HOME/KlipperScreen}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -f "$KS_DIR/screen.py" || ! -d "$KS_DIR/panels" || ! -f "$KS_DIR/styles/base.css" ]]; then
  echo "ERROR: KlipperScreen source not found or incomplete: $KS_DIR" >&2
  echo "Usage: bash install.sh /path/to/KlipperScreen" >&2
  exit 1
fi

STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$KS_DIR/.voron-dashboard-backup-$STAMP"
mkdir -p "$BACKUP/panels"
cp -a "$KS_DIR/panels/main_menu.py" "$BACKUP/panels/main_menu.py"
cp -a "$KS_DIR/styles/base.css" "$BACKUP/base.css"
if [[ -f "$KS_DIR/panels/voron_dashboard.py" ]]; then
  cp -a "$KS_DIR/panels/voron_dashboard.py" "$BACKUP/panels/voron_dashboard.py"
fi

install -m 0644 "$SCRIPT_DIR/panels/voron_dashboard.py" "$KS_DIR/panels/voron_dashboard.py"
install -m 0644 "$SCRIPT_DIR/main_menu.py" "$KS_DIR/panels/main_menu.py"
cat "$SCRIPT_DIR/styles/voron-dashboard.css" >> "$KS_DIR/styles/base.css"
bash "$SCRIPT_DIR/install-icons.sh"
printf '%s\n' "$BACKUP" > "$KS_DIR/.voron-dashboard-backup-path"

echo "Dashboard and Neon-Voron icon theme installed."
echo "Backup saved to: $BACKUP"
echo "Restart KlipperScreen: sudo systemctl restart KlipperScreen"
