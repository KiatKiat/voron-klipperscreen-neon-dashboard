# Voron KlipperScreen Neon Dashboard

A touch-friendly neon dashboard concept for KlipperScreen, designed around a Voron printer and an 800×480 touchscreen.

> **Status: experimental / community customization.** This is a custom KlipperScreen panel, not an official KlipperScreen feature. Test on a non-critical session first and keep a backup of your working installation.

## Features

- Dark navy interface with cyan / blue neon styling
- Dedicated **Neon-Voron GTK icon theme** with hand-authored SVG symbolic icons (not just CSS tinting of the system's existing glyphs)
- Custom vector icon coverage for home, files, print, pause, stop, temperature, heated bed, fan, mesh, movement, settings, console, network and status
- Semantic neon accents: amber heater, cyan bed/fans, purple chamber, green system health, magenta flow
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

The custom GTK icon theme is installed as Neon-Voron under ~/.local/share/icons and selected in the current user's GTK3 settings. It overrides common symbolic icon names used by KlipperScreen, so native pages can display the new SVG artwork rather than relying only on a cyan CSS tint. GTK icons not included in the theme fall back to Adwaita.

See the implementation specification in docs/800x480-implementation-spec.md for page inventory, sizing, icon mapping and verification requirements.

## Install

~~~bash
cd ~
git clone --branch neon-icons-full-refresh https://github.com/KiatKiat/voron-klipperscreen-neon-dashboard.git
cd voron-klipperscreen-neon-dashboard
bash install.sh ~/KlipperScreen
sudo systemctl restart KlipperScreen
~~~

The installer backs up the existing KlipperScreen main menu and base CSS, installs the dashboard and neon stylesheet, then installs the custom SVG icon theme and selects it in the current user's GTK3 settings.

If the repository is already cloned:

~~~bash
cd ~/voron-klipperscreen-neon-dashboard
git fetch origin
git checkout neon-icons-full-refresh
git pull --ff-only
bash install.sh ~/KlipperScreen
sudo systemctl restart KlipperScreen
~~~

If KlipperScreen runs under a different Linux user than the one running the installer, run the installer as the KlipperScreen service user so the GTK icon theme is installed in the correct home directory. If KlipperScreen is installed elsewhere, pass its actual directory instead of ~/KlipperScreen.

## Roll back

~~~bash
cd ~/voron-klipperscreen-neon-dashboard
bash uninstall.sh ~/KlipperScreen
~~~

The rollback script restores the KlipperScreen panel and stylesheet backup. To restore the previous GTK icon theme, edit ~/.config/gtk-3.0/settings.ini and restore its previous gtk-icon-theme-name value (or remove that key if it was not previously present), then restart KlipperScreen.

## Important notes

- This project does not modify printer.cfg, Moonraker configuration, macros, or MCU firmware.
- The dashboard is not a pixel-perfect port of the supplied 1650×930 concept image; it rearranges the same information for an 800×480 display.
- Verify pause, resume, and stop behavior before starting a long print.
- The SVG icon theme has been added to the repository, but a real Pi/GTK runtime screenshot is still required to verify every native KlipperScreen panel.
- If KlipperScreen fails to start, restore the backup as described above and inspect the service journal.

## License

MIT. See LICENSE.
