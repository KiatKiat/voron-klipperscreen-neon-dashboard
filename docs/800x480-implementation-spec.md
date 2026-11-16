# Neon KlipperScreen — 800×480 implementation specification

Target: Voron Trident 300, KlipperScreen 0.4.7-206, GTK3/PyGObject, Python 3.13, Debian 13, Raspberry Pi, 800×480 landscape.

## Visual tokens

| Token | Value | Use |
|---|---|---|
| Canvas | #020711 | Main background |
| Surface | #071626 | Cards and panels |
| Surface raised | #0A2036 | Buttons and selected rows |
| Primary cyan | #00D9FF | Active navigation, primary action, live values |
| Blue | #0878DB | Navigation and primary buttons |
| Purple | #8B70FF | Secondary controls |
| Magenta | #ED35D2 | Accent / chamber |
| Green | #36FF8C | Ready / healthy |
| Amber | #FFAD19 | Heater / caution |
| Red | #FF3157 | Stop / fault |
| Main text | #EFF9FF | Primary labels |
| Muted text | #8FC9EB | Secondary labels |
| Divider | #14618E | Separators / card outlines |

## Typography

Use DejaVu Sans. On the 800×480 display, use these CSS pixel sizes:
- Page title / printer state: 18–20 px, bold.
- Main temperature / progress value: 22–26 px, bold.
- Primary action labels: 14–16 px, bold.
- Section headings: 12–14 px, bold, uppercase.
- Body / file names / settings rows: 12–14 px.
- Secondary labels / units / hints: 10–11 px.
- Compact telemetry: 10–12 px.

## Geometry and alignment

- Canvas: exactly 800×480; landscape, no scrolling on dashboard.
- Outer padding: 6 px; standard gap: 5 px.
- Header/status strip: 34 px high; align brand left, printer state center, clock/connectivity right.
- Navigation rail: 72 px wide; full available height; 5 px vertical gap.
- Card radius: 9–11 px; border: 1 px; inner padding: 6 px.
- Touch controls: minimum 42 px high and 44 px wide; destructive action red.
- Values right-aligned when paired with labels; card titles left-aligned.
- Keep all text inside its card; ellipsize long filenames instead of shrinking the whole UI.
- No continuous glow animation, blur loops, web views, or extra renderer.

## Icon system

Use GTK theme icons where available; prefer symbolic icons at 20–24 px. Keep a consistent semantic mapping:
- Home: go-home / home
- Files: folder / document-open
- Print: media-playback-start
- Pause / Resume / Stop: media-playback-pause / media-playback-start / media-playback-stop
- Temperature: thermometer
- Move: input-mouse / directional arrows
- Fan: fan
- Bed mesh: view-grid
- Settings: preferences-system
- Console: utilities-terminal
- About: help-about
- Ready: emblem-ok-symbolic
Use text glyphs only as fallback; do not rely on emoji fonts for core navigation.

## Page inventory — one full-screen page per item

1. HOME — status header, printer/job card, progress, nozzle/bed/chamber temperatures, fan/speed/flow telemetry, pause/resume/stop, quick navigation.
2. TUNE — speed factor, extrusion factor, Z offset, pressure advance; show current value and reset action.
3. CONTROL / MOVE — XY jog pad, Z up/down, selectable 0.1/1/10 mm step, Home X/Y/Z/All, motors off.
4. FILES — breadcrumb, folder/file list, filename, file size, scroll, print action and thumbnail when available.
5. PRINT STATUS — filename, progress, elapsed/remaining, layer if available, pause/resume/cancel with confirmation.
6. TEMPERATURE — extruder, bed and configured chamber sensors; current/target values, target entry and presets; graph only when native panel supports it.
7. FANS — configured fan controls, percentage and RPM when reported; do not invent missing sensors.
8. BED MESH — native mesh visualization, profile selection/load/save and calibration actions where supported by firmware.
9. MACROS — native macro list and execution; retain confirmation for potentially destructive macros.
10. CONSOLE — native G-code input, send, response history and scroll.
11. SETTINGS — native settings categories and controls; preserve upstream behavior.
12. ABOUT — Klipper, Moonraker and KlipperScreen versions, host information and network address when available.

## Functional rules

- Native KlipperScreen owns Moonraker, printer state and G-code command dispatch.
- No duplicate Moonraker connection.
- Do not replace native panels with decorative controls.
- Missing optional sensors show “N/A”; never show fabricated live readings.
- Stop/cancel must require confirmation.
- Refresh live dashboard values on a single 2-second GLib timer; update labels only when values change.
- Respect native panel navigation and upstream settings.

## Verification and screenshot procedure

Static Python/shell/SVG checks are not proof of GTK rendering. Run the project's test script, install on the target Pi with a backup, restart KlipperScreen, then capture the real HDMI framebuffer at 800×480. Verify every page, touch target, scrolling, live sensor mapping and printer actions before using during a print. The repository's gallery SVG is a design reference, not a screenshot of the running GTK application.
