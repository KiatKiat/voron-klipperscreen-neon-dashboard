# Neon Voron dashboard for KlipperScreen 0.4.x
# GTK3 presentation layer; KlipperScreen retains printer communications and controls.
import logging
from datetime import datetime

from gi.repository import GLib, Gtk, Pango
from ks_includes.screen_panel import ScreenPanel

LOG = logging.getLogger("NeonDashboard")


class Panel(ScreenPanel):
    REFRESH_SECONDS = 2

    def __init__(self, screen, title=None):
        super().__init__(screen, title or "NEON VORON")
        self._timer = None
        self._labels = {}
        self._last_values = {}
        self._progress = 0.0
        self._build()
        self.update()
        self._timer = GLib.timeout_add_seconds(self.REFRESH_SECONDS, self._tick)

    def _label(self, text="", css="nv-value", align=0.5):
        w = Gtk.Label(label=str(text), xalign=align, yalign=0.5, hexpand=True)
        w.set_ellipsize(Pango.EllipsizeMode.END)
        w.get_style_context().add_class(css)
        return w

    def _icon(self, name, size=Gtk.IconSize.BUTTON, accent=None):
        image = Gtk.Image.new_from_icon_name(name, size)
        image.get_style_context().add_class("nv-icon")
        if accent:
            image.get_style_context().add_class(accent)
        return image

    def _button(self, text, css, callback, icon=None):
        w = Gtk.Button(hexpand=True, vexpand=True)
        w.get_style_context().add_class(css)
        content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        if icon:
            content.pack_start(self._icon(icon), False, False, 0)
        content.pack_start(self._label(text, "nv-button-label"), True, True, 0)
        w.add(content)
        w.connect("clicked", callback)
        return w

    def _nav(self, caption, panel, title=None, icon="applications-system-symbolic"):
        def navigate(_button):
            try:
                self._screen.show_panel(panel, title=title or caption)
            except Exception:
                LOG.exception("Unable to open KlipperScreen panel %s", panel)
                try:
                    self._screen.show_popup_message(_("Panel unavailable: ") + panel)
                except Exception:
                    pass
        w = Gtk.Button(hexpand=True, vexpand=True)
        w.get_style_context().add_class("nv-nav")
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        content.pack_start(self._icon(icon, Gtk.IconSize.DIALOG), True, True, 0)
        content.pack_start(self._label(caption.upper(), "nv-nav-label"), False, False, 0)
        w.add(content)
        w.connect("clicked", navigate)
        return w

    def _card(self, caption, key, value="--", sub=None, compact=False):
        icons = {
            "nozzle": ("weather-clear-symbolic", "#ffad19"),
            "bed": ("view-grid-symbolic", "#00d9ff"),
            "chamber": ("weather-fog-symbolic", "#d783ff"),
            "fan": ("view-refresh-symbolic", "#00d9ff"),
            "partfan": ("view-refresh-symbolic", "#00d9ff"),
            "speed": ("media-playback-start-symbolic", "#36ff8c"),
            "flow": ("emblem-synchronizing-symbolic", "#ed35d2"),
            "filament": ("text-x-generic-symbolic", "#00d9ff"),
            "mcu": ("computer-symbolic", "#36ff8c"),
            "cpu": ("utilities-system-monitor-symbolic", "#36ff8c"),
        }
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1, hexpand=True, vexpand=True)
        card.get_style_context().add_class("nv-card")
        card.get_style_context().add_class("nv-compact" if compact else "nv-standard")
        heading = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        icon_info = icons.get(key)
        if icon_info:
            heading.pack_start(self._icon(icon_info[0], Gtk.IconSize.BUTTON, "nv-icon-" + key), False, False, 0)
        heading.pack_start(self._label(caption.upper(), "nv-caption", 0), True, True, 0)
        card.pack_start(heading, False, False, 0)
        self._labels[key] = self._label(value, "nv-number" if not compact else "nv-small-number")
        card.pack_start(self._labels[key], True, True, 0)
        if sub is not None:
            self._labels[key + "_sub"] = self._label(sub, "nv-sub")
            card.pack_start(self._labels[key + "_sub"], False, False, 0)
        return card

    def _build(self):
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4, hexpand=True, vexpand=True)
        root.get_style_context().add_class("nv-root")

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header.get_style_context().add_class("nv-header")
        header.pack_start(self._label("VORON", "nv-brand", 0), False, True, 4)
        header.pack_start(self._label("│  KLIPPERSCREEN", "nv-header-sub", 0), True, True, 0)
        self._labels["state"] = self._label("● READY", "nv-state")
        header.pack_end(self._labels["state"], False, True, 4)
        self._labels["clock"] = self._label("--:--", "nv-clock")
        header.pack_end(self._labels["clock"], False, True, 4)
        root.pack_start(header, False, False, 0)

        main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4, hexpand=True, vexpand=True)
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        sidebar.set_size_request(76, -1)
        for caption, panel, title, icon in (
            ("HOME", "main_menu", "Home", "go-home-symbolic"),
            ("TUNE", "fine_tune", "Tune", "preferences-system-symbolic"),
            ("CONTROL", "move", "Move", "input-mouse-symbolic"),
            ("FILES", "gcodes", "Files", "folder-symbolic"),
            ("TEMP", "temperature", "Temperature", "weather-clear-symbolic"),
            ("FANS", "fan", "Fans", "view-refresh-symbolic"),
            ("MESH", "bed_mesh", "Bed Mesh", "view-grid-symbolic"),
            ("SETTINGS", "settings", "Settings", "emblem-system-symbolic"),
        ):
            sidebar.pack_start(self._nav(caption, panel, title, icon), True, True, 0)
        main.pack_start(sidebar, False, False, 0)

        preview = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4, hexpand=True, vexpand=True)
        preview.get_style_context().add_class("nv-card")
        preview_head = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self._labels["filename"] = self._label("No active print", "nv-filename", 0)
        preview_head.pack_start(self._labels["filename"], True, True, 0)
        preview.pack_start(preview_head, False, False, 2)

        # Lightweight schematic preview area; no browser or external renderer required.
        self._preview_art = Gtk.DrawingArea()
        self._preview_art.set_size_request(-1, 130)
        self._preview_art.connect("draw", self._draw_preview)
        preview.pack_start(self._preview_art, True, True, 0)
        self._labels["layer"] = self._label("LAYER -- / --   •   0.20 mm", "nv-sub")
        preview.pack_start(self._labels["layer"], False, False, 0)
        main.pack_start(preview, True, True, 0)

        progress_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        progress_card.set_size_request(178, -1)
        progress_card.get_style_context().add_class("nv-card")
        progress_card.pack_start(self._label("PRINT PROGRESS", "nv-caption"), False, False, 0)
        self._ring = Gtk.DrawingArea()
        self._ring.set_size_request(150, 150)
        self._ring.connect("draw", self._draw_ring)
        progress_card.pack_start(self._ring, True, True, 0)
        self._labels["progress_sub"] = self._label("READY FOR PRINT", "nv-progress-sub")
        progress_card.pack_start(self._labels["progress_sub"], False, False, 0)
        times = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        elapsed_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        elapsed_box.pack_start(self._label("ELAPSED", "nv-caption"), False, False, 0)
        self._labels["elapsed"] = self._label("00:00:00", "nv-time")
        elapsed_box.pack_start(self._labels["elapsed"], False, False, 0)
        remain_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        remain_box.pack_start(self._label("REMAIN", "nv-caption"), False, False, 0)
        self._labels["remain"] = self._label("--:--", "nv-time")
        remain_box.pack_start(self._labels["remain"], False, False, 0)
        times.pack_start(elapsed_box, True, True, 0)
        times.pack_start(remain_box, True, True, 0)
        progress_card.pack_start(times, False, False, 0)
        main.pack_start(progress_card, False, False, 0)

        temps = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        temps.set_size_request(166, -1)
        temps.pack_start(self._card("Nozzle", "nozzle", "--°C", "Target --°C"), True, True, 0)
        temps.pack_start(self._card("Bed", "bed", "--°C", "Target --°C"), True, True, 0)
        temps.pack_start(self._card("Chamber", "chamber", "--°C", "Target --°C"), True, True, 0)
        main.pack_start(temps, False, False, 0)
        root.pack_start(main, True, True, 0)

        telemetry = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3, homogeneous=True)
        telemetry.pack_start(self._card("Fan", "fan", "--%", compact=True), True, True, 0)
        telemetry.pack_start(self._card("Part fan", "partfan", "--%", compact=True), True, True, 0)
        telemetry.pack_start(self._card("Speed", "speed", "--%", compact=True), True, True, 0)
        telemetry.pack_start(self._card("Flow", "flow", "--%", compact=True), True, True, 0)
        telemetry.pack_start(self._card("Filament", "filament", "-- m", compact=True), True, True, 0)
        telemetry.pack_start(self._card("MCU", "mcu", "--°C", compact=True), True, True, 0)
        telemetry.pack_start(self._card("CPU", "cpu", "--%", compact=True), True, True, 0)
        root.pack_start(telemetry, False, False, 0)

        actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        actions.set_size_request(-1, 48)
        actions.pack_start(self._button("PAUSE", "nv-action nv-blue", self._pause, "media-playback-pause-symbolic"), True, True, 0)
        actions.pack_start(self._button("RESUME", "nv-action nv-blue", self._resume, "media-playback-start-symbolic"), True, True, 0)
        actions.pack_start(self._button("STOP", "nv-action nv-red", self._stop, "media-playback-stop-symbolic"), True, True, 0)
        actions.pack_start(self._nav("Z ADJUST", "zcalibrate", "Z Calibrate", "go-up-symbolic"), True, True, 0)
        actions.pack_start(self._nav("MACROS", "gcode_macros", "Macros", "applications-system-symbolic"), True, True, 0)
        actions.pack_start(self._nav("CONSOLE", "console", "Console", "utilities-terminal-symbolic"), True, True, 0)
        root.pack_start(actions, False, False, 0)

        self.content.pack_start(root, True, True, 0)
        self.content.show_all()

    def _draw_preview(self, _widget, cr):
        allocation = _widget.get_allocation()
        w, h = allocation.width, allocation.height
        cr.set_source_rgb(0.015, 0.045, 0.085)
        cr.paint()
        cr.set_line_width(0.6)
        cr.set_source_rgba(0.0, 0.55, 0.95, 0.28)
        step = 18
        for x in range(0, w + h, step):
            cr.move_to(x, 0); cr.line_to(x - h, h)
            cr.move_to(x, 0); cr.line_to(x + h, h)
        cr.stroke()
        # Stylized Voron-like build-volume wireframe as a visual placeholder.
        cx, cy = w * 0.5, h * 0.57
        cr.set_line_width(2.0)
        cr.set_source_rgba(0.0, 0.75, 1.0, 0.9)
        cr.move_to(cx - 48, cy - 38); cr.line_to(cx + 36, cy - 38)
        cr.line_to(cx + 58, cy - 20); cr.line_to(cx - 28, cy - 20); cr.close_path()
        cr.move_to(cx - 48, cy - 38); cr.line_to(cx - 48, cy + 35)
        cr.line_to(cx - 28, cy + 53); cr.line_to(cx - 28, cy - 20)
        cr.move_to(cx - 28, cy + 53); cr.line_to(cx + 58, cy + 53)
        cr.line_to(cx + 58, cy - 20)
        cr.stroke()
        cr.set_source_rgba(0.0, 0.8, 1.0, 0.12)
        cr.rectangle(cx - 40, cy - 30, 80, 75); cr.fill()
        return False

    def _draw_ring(self, widget, cr):
        a = widget.get_allocation()
        cx, cy = a.width / 2.0, a.height / 2.0
        radius = min(a.width, a.height) * 0.39
        cr.set_line_width(13)
        cr.set_line_cap(1)
        cr.set_source_rgba(0.16, 0.27, 0.39, 1)
        cr.arc(cx, cy, radius, 0, 6.28318)
        cr.stroke()
        cr.set_source_rgba(0.0, 0.85, 1.0, 1)
        cr.arc(cx, cy, radius, -1.5708, -1.5708 + 6.28318 * self._progress)
        cr.stroke()
        cr.set_source_rgb(0.95, 0.98, 1.0)
        cr.select_font_face("Sans", 0, 1)
        cr.set_font_size(35)
        text = "%d%%" % round(self._progress * 100)
        ext = cr.text_extents(text)
        cr.move_to(cx - ext.width / 2, cy + ext.height / 3)
        cr.show_text(text)
        return False

    def _stat(self, obj, field, default=None):
        try:
            value = self._printer.get_stat(obj, field)
            return default if value is None else value
        except Exception:
            return default

    def _set(self, key, value):
        value = str(value)
        if self._last_values.get(key) == value:
            return
        self._last_values[key] = value
        label = self._labels.get(key)
        if label is not None:
            label.set_text(value)

    @staticmethod
    def _fmt_time(seconds):
        try:
            n = max(0, int(float(seconds or 0)))
            h, rem = divmod(n, 3600)
            m, s = divmod(rem, 60)
            return "%02d:%02d:%02d" % (h, m, s)
        except (TypeError, ValueError):
            return "--:--:--"

    def update(self):
        try:
            self._set("clock", datetime.now().strftime("%a, %b %d  %H:%M"))
            state = str(getattr(self._printer, "state", "disconnected")).upper()
            self._set("state", "● " + state)
            filename = self._stat("print_stats", "filename", "") or "No active print"
            self._set("filename", filename.split("/")[-1])
            self._progress = max(0.0, min(1.0, float(self._stat("display_status", "progress", 0) or 0)))
            self._ring.queue_draw()
            elapsed = self._stat("print_stats", "print_duration", 0) or 0
            self._set("elapsed", self._fmt_time(elapsed))
            self._set("progress_sub", "PRINTING" if state == "PRINTING" else state)
            remaining = (float(elapsed) * (1.0 - self._progress) / self._progress) if self._progress > 0.01 else 0
            self._set("remain", self._fmt_time(remaining) if self._progress > 0.01 else "--:--:--")
            layer = self._stat("print_stats", "current_layer", "--")
            total = self._stat("print_stats", "total_layer", "--")
            self._set("layer", "LAYER %s / %s   •   0.20 mm" % (layer, total))

            for key, obj in (("nozzle", "extruder"), ("bed", "heater_bed"),
                             ("chamber", "temperature_sensor chamber")):
                current = self._stat(obj, "temperature")
                target = self._stat(obj, "target", 0) or 0
                self._set(key, "%.0f°C" % float(current) if current is not None else "--°C")
                self._set(key + "_sub", "Target %.0f°C" % float(target))

            fan = float(self._stat("fan", "speed", 0) or 0) * 100
            self._set("fan", "%.0f%%" % fan)
            self._set("partfan", "%.0f%%" % (float(self._stat("heater_fan hotend_fan", "speed", 0) or 0) * 100))
            self._set("speed", "%.0f%%" % (float(self._stat("gcode_move", "speed_factor", 1) or 1) * 100))
            self._set("flow", "%.0f%%" % (float(self._stat("gcode_move", "extrude_factor", 1) or 1) * 100))
            filament = float(self._stat("print_stats", "filament_used", 0) or 0)
            self._set("filament", "%.2f m" % (filament / 1000))
            mcu = self._stat("temperature_sensor mcu", "temperature")
            self._set("mcu", "%.0f°C" % float(mcu) if mcu is not None else "--°C")
            self._set("cpu", "N/A")
        except Exception:
            LOG.exception("Dashboard refresh failed")

    def _tick(self):
        self.update()
        return True

    def _pause(self, widget):
        try:
            self._screen._send_action(widget, "printer.print.pause", {})
        except Exception:
            LOG.exception("Pause command failed")

    def _resume(self, widget):
        try:
            self._screen._send_action(widget, "printer.print.resume", {})
        except Exception:
            LOG.exception("Resume command failed")

    def _stop(self, _widget):
        dialog = Gtk.MessageDialog(transient_for=self._screen, modal=True,
            message_type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.CANCEL,
            text=_("Stop the current print?"))
        dialog.add_button(_("Stop"), Gtk.ResponseType.ACCEPT)
        dialog.format_secondary_text(_("The print will be cancelled."))
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.ACCEPT:
            try:
                self._screen._ws.api.print_cancel()
            except Exception:
                LOG.exception("Print cancellation failed")

    def activate(self):
        self.update()
        if self._timer is None:
            self._timer = GLib.timeout_add_seconds(self.REFRESH_SECONDS, self._tick)

    def deactivate(self):
        if self._timer is not None:
            GLib.source_remove(self._timer)
            self._timer = None
