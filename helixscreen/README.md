# Neon Voron for HelixScreen

A HelixScreen-native adaptation of the Voron neon dashboard concept for **800x480 HDMI landscape**.

## What this port includes

- A native HelixScreen theme JSON with a near-black navy base, cyan primary accent, purple secondary accent, mint-green tertiary/success accent, and high-contrast text.
- A 6x4 Home Panel layout profile for 800x480.
- A setup guide for adding the theme and arranging the native widgets.

## Important: native HelixScreen limits

This is a theme + widget-layout port, not a replacement of HelixScreen's application UI. HelixScreen themes expose 16 semantic color tokens and global border/shadow styling. They do **not** currently let a theme draw the mockup's custom Voron header, custom left-side navigation, per-card orange/cyan/purple outlines, circular percentage gauge, or bespoke Pause/Resume/Stop footer. The app's native Print Status and control panels provide the corresponding printer functions, but their exact appearance differs from the concept image.

The theme does not add hardware telemetry. Chamber temperature, LED, and other hardware-gated widgets appear only when the corresponding sensors/devices are configured and detected.

## Install the theme

On the printer host:

```bash
mkdir -p ~/helixscreen/config/themes
cp neon-voron.json ~/helixscreen/config/themes/neon-voron.json
```

Restart HelixScreen, then select:

**Settings → Appearance → Theme Colors → Neon Voron**

The user theme directory is `~/helixscreen/config/themes/`; user themes are discovered at launch and take precedence over built-in themes.

## Set the 800x480 layout

HelixScreen auto-detects 800x480 as the standard small landscape layout (6 columns x 4 rows). Leave layout on `auto` unless you have a reason to override it.

The file `home-layout.json` contains a `panel_widgets.home` fragment. Merge that object into your existing `~/helixscreen/config/settings.json`; do not replace the entire settings file. Back up settings.json first. The layout is a starting point and can be refined with Home Panel Edit Mode.

## Hardware mapping notes

- `temperature`: nozzle temperature.
- `temp_stack`: nozzle / bed / chamber temperatures where available.
- `fan_stack`: part / hotend / auxiliary fans exposed by Klipper.
- `temp_graph`: temperature history.
- `network`: network state.
- `led`: LED quick control, only when a supported LED device is detected.
- `notifications`: pending alerts.

If chamber temperature or LED widgets are absent, configure the corresponding sensor or LED in Klipper/Moonraker and HelixScreen Hardware & Devices settings.

## Source documentation

- https://helixscreen.org/dev/contributing/themes/
- https://helixscreen.org/reference/configuration/
- https://helixscreen.org/guide/home-panel/
