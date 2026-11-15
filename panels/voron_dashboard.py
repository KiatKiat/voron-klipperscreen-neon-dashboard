# Voron neon dashboard for KlipperScreen 0.4.7+
# Copyright (c) 2026. Licensed under the MIT License.
import logging
from datetime import datetime

from gi.repository import GLib, Gtk, Pango
from ks_includes.screen_panel import ScreenPanel


class Panel(ScreenPanel):
    def __init__(self, screen, title=None):
        super().__init__(screen, title or "VORON  |  KlipperScreen")
        self.timer = None
        self.value_labels = {}
        self._make_ui()
        self.update()
        self.timer = GLib.timeout_add_seconds(1, self._tick)

    def _box(self, style, vertical=True, spacing=5):
        widget = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL if vertical else Gtk.Orientation.HORIZONTAL,
            spacing=spacing, hexpand=True, vexpand=True
        )
        widget.get_style_context().add_class(style)
        return widget

    def _label(self, text, style="vd-value", x=0.5):
        label = Gtk.Label(label=text, xalign=x, yalign=0.5, hexpand=True)
        label.get_style_context().add_class(style)
        label.set_ellipsize(Pango.EllipsizeMode.END)
        return label

    def _button(self, text, style, callback):
        button = Gtk.Button(label=text, hexpand=True, vexpand=True)
        button.get_style_context().add_class(style)
        button.connect("clicked", callback)
        return button

    def _card(self, title, key, value="--", sub=""):
        card = self._box("vd-card")
        card.pack_start(self._label(title.upper(), "vd-card-title"), False, False, 0)
        value_label = self._label(value, "vd-card-value")
        card.pack_start(value_label, True, True, 0)
        if sub:
            sub_label = self._label(sub, "vd-card-sub")
            card.pack_start(sub_label, False, False, 0)
            self.value_labels[key + "_sub"] = sub_label
        self.value_labels[key] = value_label
        return card

    def _nav(self, text, panel, title=None):
        def go(_button):
            try:
                self._screen.show_panel(panel, title=title or panel)
            except Exception:
                logging.exception("Dashboard navigation failed: %s", panel)
                self._screen.show_popup_message(_("Panel unavailable:") + " " + panel)
        return self._button(text, "vd-nav", go)

    def _make_ui(self):
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5, hexpand=True, vexpand=True)
        root.get_style_context().add_class("vd-root")

        top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        top.get_style_context().add_class("vd-top")
        top.pack_start(self._label("VORON", "vd-brand", 0), False, True, 8)
        top.pack_start(self._label("│  KlipperScreen", "vd-top-sub", 0), True, True, 2)
        self.value_labels["state"] = self._label("CONNECTING", "vd-state")
        top.pack_start(self.value_labels["state"], False, True, 4)
        self.value_labels["clock"] = self._label("--:--", "vd-top-sub")
        top.pack_end(self.value_labels["clock"], False, True, 8)
        root.pack_start(top, False, False, 0)

        body = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, hexpand=True, vexpand=True)

        nav = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        nav.set_size_request(90, -1)
        for label, panel_name, title in [
            ("⌂  HOME", "main_menu", "Home"),
            ("◇  TUNE", "move", "Tune"),
            ("⚙  CONTROL", "settings", "Control"),
            ("▣  FILES", "gcode_files", "Files"),
            ("▦  MESH", "bed_mesh", "Bed Mesh"),
            ("◎  PA FINE", "pa_fine", "PA Fine"),
            ("◉  SPOOL", "spoolman", "Spoolman"),
        ]:
            nav.pack_start(self._nav(label, panel_name, title), True, True, 0)
        body.pack_start(nav, False, False, 0)

        center = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5, hexpand=True, vexpand=True)
        job = self._box("vd-card")
        job_head = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        job_head.pack_start(self._label("CURRENT PRINT", "vd-card-title", 0), True, True, 2)
        self.value_labels["layer"] = self._label("Layer -- / --", "vd-card-sub")
        job_head.pack_end(self.value_labels["layer"], False, True, 2)
        job.pack_start(job_head, False, False, 0)
        self.value_labels["filename"] = self._label("No active print", "vd-file", 0)
        job.pack_start(self.value_labels["filename"], False, False, 0)
        self.value_labels["progress"] = self._label("0%", "vd-progress")
        job.pack_start(self.value_labels["progress"], True, True, 0)
        self.value_labels["progress_sub"] = self._label("Waiting for print", "vd-card-sub")
        job.pack_start(self.value_labels["progress_sub"], False, False, 0)
        center.pack_start(job, True, True, 0)

        temps = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, homogeneous=True)
        temps.pack_start(self._card("Nozzle", "nozzle", "--°C", "Target --°C"), True, True, 0)
        temps.pack_start(self._card("Bed", "bed", "--°C", "Target --°C"), True, True, 0)
        temps.pack_start(self._card("Chamber", "chamber", "--°C", "Target --°C"), True, True, 0)
        center.pack_start(temps, True, True, 0)

        stats = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, homogeneous=True)
        stats.pack_start(self._card("Part fan", "partfan", "--%"), True, True, 0)
        stats.pack_start(self._card("Print speed", "speed", "--%"), True, True, 0)
        stats.pack_start(self._card("Flow", "flow", "--%"), True, True, 0)
        stats.pack_start(self._card("Elapsed", "elapsed", "--:--"), True, True, 0)
        center.pack_start(stats, True, True, 0)
        body.pack_start(center, True, True, 0)

        right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        right.set_size_request(112, -1)
        right.pack_start(self._card("MCU", "mcu", "--°C"), True, True, 0)
        right.pack_start(self._card("CPU", "cpu", "--%"), True, True, 0)
        right.pack_start(self._card("Filament", "filament", "-- m"), True, True, 0)
        right.pack_start(self._nav("TEMPERATURE", "temperature", "Temperature"), True, True, 0)
        right.pack_start(self._nav("FANS", "fan", "Fans"), True, True, 0)
        body.pack_start(right, False, False, 0)
        root.pack_start(body, True, True, 0)

        actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        actions.set_size_request(-1, 52)
        actions.pack_start(self._button("Ⅱ  PAUSE", "vd-action vd-blue", self._pause), True, True, 0)
        actions.pack_start(self._button("▶  RESUME", "vd-action vd-blue", self._resume), True, True, 0)
        actions.pack_start(self._button("■  STOP", "vd-action vd-red", self._stop), True, True, 0)
        actions.pack_start(self._nav("Z ADJUST", "z_calibrate", "Z Adjust"), True, True, 0)
        actions.pack_start(self._nav("PREHEAT", "temperature", "Temperature"), True, True, 0)
        actions.pack_start(self._nav("MORE", "settings", "Settings"), True, True, 0)
        root.pack_start(actions, False, False, 0)

        self.content.pack_start(root, True, True, 0)
        self.content.show_all()

    def _stat(self, obj, field, default=None):
        try:
            value = self._printer.get_stat(obj, field)
            return default if value is None else value
        except Exception:
            return default

    def _set(self, key, value):
        label = self.value_labels.get(key)
        if label is not None:
            label.set_text(str(value))

    def _tick(self):
        self.update()
        return True

    def update(self):
        try:
            self._set("clock", datetime.now().strftime("%a %d %b  %H:%M"))
            state = getattr(self._printer, "state", "disconnected")
            self._set("state", str(state).upper())

            filename = self._stat("print_stats", "filename", "") or "No active print"
            self._set("filename", filename)
            progress = float(self._stat("display_status", "progress", 0) or 0)
            self._set("progress", f"{progress * 100:.0f}%")
            self._set("progress_sub", f"Elapsed {self._time(self._stat('print_stats', 'print_duration', 0))}  •  {progress * 100:.1f}% complete")

            current_layer = self._stat("print_stats", "current_layer", "--")
            total_layer = self._stat("print_stats", "total_layer", "--")
            self._set("layer", f"Layer {current_layer} / {total_layer}")

            elapsed = self._stat("print_stats", "print_duration", 0) or 0
            self._set("elapsed", self._time(elapsed))

            for key, obj in [
                ("nozzle", "extruder"),
                ("bed", "heater_bed"),
                ("chamber", "temperature_sensor chamber"),
            ]:
                temp = self._stat(obj, "temperature")
                target = self._stat(obj, "target", 0) or 0
                self._set(key, f"{float(temp):.0f}°C" if temp is not None else "--°C")
                self._set(key + "_sub", f"Target {float(target):.0f}°C")

            fan = self._stat("fan", "speed", 0) or 0
            self._set("partfan", f"{float(fan) * 100:.0f}%")
            speed = self._stat("gcode_move", "speed_factor", 1) or 1
            flow = self._stat("gcode_move", "extrude_factor", 1) or 1
            self._set("speed", f"{float(speed) * 100:.0f}%")
            self._set("flow", f"{float(flow) * 100:.0f}%")

            filament = self._stat("print_stats", "filament_used", 0) or 0
            self._set("filament", f"{float(filament) / 1000:.2f} m")
            mcu_temp = self._stat("temperature_sensor mcu", "temperature")
            self._set("mcu", f"{float(mcu_temp):.0f}°C" if mcu_temp is not None else "N/A")
            self._set("cpu", "N/A")
        except Exception:
            logging.exception("Voron dashboard refresh failed")

    @staticmethod
    def _time(seconds):
        try:
            seconds = max(0, int(float(seconds)))
            return f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"
        except (TypeError, ValueError):
            return "--:--"

    def _pause(self, widget):
        self._screen._send_action(widget, "printer.print.pause", {})

    def _resume(self, widget):
        self._screen._send_action(widget, "printer.print.resume", {})

    def _stop(self, _widget):
        dialog = Gtk.MessageDialog(
            transient_for=self._screen,
            modal=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.CANCEL,
            text=_("Stop the current print?"),
        )
        dialog.add_button(_("Stop"), Gtk.ResponseType.ACCEPT)
        dialog.format_secondary_text(_("The print will be cancelled."))
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.ACCEPT:
            self._screen._ws.api.print_cancel()

    def activate(self):
        self.update()
        if self.timer is None:
            self.timer = GLib.timeout_add_seconds(1, self._tick)

    def deactivate(self):
        if self.timer is not None:
            GLib.source_remove(self.timer)
            self.timer = None
