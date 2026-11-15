# Neon Voron for HelixScreen

A HelixScreen-native theme and Home Panel layout adaptation of the Voron neon dashboard concept, intended for **800×480 HDMI landscape**.

## Included

- `neon-voron.json`: valid HelixScreen theme structure with 16 semantic color tokens in both dark and light palettes, plus global border and shadow settings.
- `home-layout.json`: Home Panel widget arrangement for HelixScreen's 6×4 small-screen grid. Widget positions and spans use half-cell tracks as required by the settings format.

## What this port can and cannot reproduce

This is a native theme + widget-layout port, not a custom replacement application UI. The theme changes semantic colors, global borders, corner radius and shadows. The Home Panel layout arranges native HelixScreen widgets.

The reference mockup's bespoke Voron header, fixed left navigation, individually colored nozzle/bed/chamber cards, circular progress gauge, and dedicated Pause/Resume/Stop footer are not created by a theme or Home Panel layout alone. Those require custom UI development in HelixScreen. Native Print Status, Temperature, Fan, and other panels remain the functional controls.

Hardware-dependent widgets only appear when the corresponding sensor or device is configured and detected. Chamber temperature, LED, MCU and CPU telemetry are not fabricated by this theme.

## Install the theme

On the printer host:

```bash
mkdir -p ~/helixscreen/config/themes
cp neon-voron.json ~/helixscreen/config/themes/neon-voron.json
```

Restart HelixScreen, then choose **Settings → Appearance → Theme Colors → Neon Voron**.

User themes are discovered from `~/helixscreen/config/themes/` at launch.

## Apply the Home Panel layout

Back up your existing settings first:

```bash
cp ~/helixscreen/config/settings.json ~/helixscreen/config/settings.json.bak
```

Merge the `panel_widgets` object from `home-layout.json` into `~/helixscreen/config/settings.json`. Do not replace the whole settings file. If you already have a customized Home Panel, merge carefully or use Home Panel Edit Mode instead.

At 800×480, HelixScreen uses a 6-column × 4-row grid. In the settings JSON, positions and spans are expressed in half-cell tracks, so the grid bounds are 12×8.

## Tune the layout on screen

Long-press the Home Panel to enter Edit Mode. Move and resize widgets to suit your actual sensor names and installed hardware. Temperature and fan widgets can be configured to display the available devices.

## References

- Home Panel guide: https://helixscreen.org/guide/home-panel/
- Theme contributor guide: https://github.com/prestonbrown/helixscreen/blob/main/docs/devel/THEME_CONTRIBUTOR_GUIDE.md
- Configuration reference: https://helixscreen.org/reference/configuration/
