# Voron KlipperScreen Neon Dashboard

A touch-friendly neon dashboard concept for KlipperScreen, designed around a Voron printer and an 800×480 touchscreen.

> **Status: experimental / community customization.** This is a custom KlipperScreen panel, not an official KlipperScreen feature. Test on a non-critical session first and keep a backup of your working installation.

## Features

- Dark navy interface with cyan / blue neon styling
- Consistent symbolic GTK icons for navigation, temperature cards, telemetry and print actions
- Semantic icon accents: amber nozzle, cyan bed/fans, purple chamber, green system health, magenta flow
- Print filename, progress percentage, layer information and elapsed time
- Nozzle, bed and chamber temperature cards
- Fan, speed, flow and filament-use indicators
- Navigation shortcuts for common KlipperScreen panels
- Pause, resume and confirmed stop controls
- Installer with timestamped backup and rollback script

## Compatibility

- KlipperScreen 0.4.x panel architecture (verify against your installed revision)
- GTK 3 / PyGObject
- Intended layout: 800×480 landscape
- Printer telemetry is read from KlipperScreen's printer status object

Some fields depend on your printer configuration. Chamber and MCU temperatures require matching temperature sensor names. CPU load is not yet integrated and is shown as a placeholder.

## 800×480 layout and icon system

The dashboard uses a compact 800×480 landscape layout, GTK symbolic icons (no emoji dependency), and semantic neon accents. The custom Home dashboard is updated; other KlipperScreen pages retain their native controls and receive the shared GTK icon styling from the appended theme.

See [the implementation specification](docs/800x480-implementation-spec.md) for page inventory, sizing, icon mapping and verification requirements.

## Install

1. Copy this repository to your printer or download it as a ZIP.
2. Extract it.
3. Run the installer with the path to your KlipperScreen source directory:

```bash
cd voron-klipperscreen-neon-dashboard
bash install.sh ~/KlipperScreen
sudo systemctl restart KlipperScreen
```

If KlipperScreen is installed elsewhere, pass its actual directory instead of `~/KlipperScreen`.

The installer backs up the current `panels/main_menu.py` and `styles/base.css` in a timestamped folder inside the KlipperScreen directory before replacing/appending anything.

## Roll back

```bash
cd voron-klipperscreen-neon-dashboard
bash uninstall.sh ~/KlipperScreen
sudo systemctl restart KlipperScreen
```

The rollback script uses the backup path saved by the installer. If you have multiple backups, inspect `~/KlipperScreen/.voron-dashboard-backup-path` before rolling back.

## Custom panel shortcuts

The left navigation includes Bed Mesh, PA Fine and Spoolman shortcuts. The PA Fine and Spoolman panel IDs are installation-specific; edit the list in `panels/voron_dashboard.py` to match the panel IDs used by your KlipperScreen configuration.

## Important notes

- This project does not modify `printer.cfg`, Moonraker configuration, macros, or MCU firmware.
- The dashboard is not a pixel-perfect port of the supplied 1650×930 concept image; it rearranges the same information for an 800×480 display.
- Verify pause, resume, and stop behavior before starting a long print.
- If KlipperScreen fails to start, restore the backup as described above and inspect the service journal.

## License

MIT. See [LICENSE](LICENSE).
