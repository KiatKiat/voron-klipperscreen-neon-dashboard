#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
THEME_DIR="$DATA_HOME/icons/Neon-Voron"
SETTINGS="$CONFIG_HOME/gtk-3.0/settings.ini"

mkdir -p "$THEME_DIR" "$(dirname "$SETTINGS")"
cp -a "$SCRIPT_DIR/icons/Neon-Voron/." "$THEME_DIR/"

touch "$SETTINGS"
if grep -q '^gtk-icon-theme-name=' "$SETTINGS"; then
  sed -i 's/^gtk-icon-theme-name=.*/gtk-icon-theme-name=Neon-Voron/' "$SETTINGS"
elif grep -q '^\[Settings\]' "$SETTINGS"; then
  sed -i '/^\[Settings\]/a gtk-icon-theme-name=Neon-Voron' "$SETTINGS"
else
  printf '\n[Settings]\ngtk-icon-theme-name=Neon-Voron\n' >> "$SETTINGS"
fi

echo "Neon-Voron SVG icon theme installed: $THEME_DIR"
echo "GTK icon theme set in: $SETTINGS"
echo "Restart KlipperScreen to reload icons."
