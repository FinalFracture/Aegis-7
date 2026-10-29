#!/usr/bin/env python3
"""Cylinder Hab-7 // RFID force-field door field UI ([t45u]).

Writes godot/config/door_fields.json (res://config/door_fields.json in-game):
    {"DOOR_RM1B": {"opacity": 0.4, "color": [r, g, b, a]}, "ALL": {...}, ...}
The running game polls that file every 0.5 s and re-applies it when its modified time changes,
calling set_door_field(door_id, opacity, color) on each door ("ALL" = every door, applied first).

Run:  python3 tools/door_field_ui.py            (needs python3-tk)
      python3 tools/door_field_ui.py --path /custom/door_fields.json
"""
import argparse
import json
import os
import tkinter as tk
from tkinter import colorchooser, ttk

DOOR_IDS = ["DOOR_APT201", "DOOR_ALCOVE2C", "DOOR_APT202", "DOOR_RM1A", "DOOR_RM1B", "DOOR_SECTOR4_EXIT"]
DEFAULT = {"opacity": 0.45, "color": [0.72, 0.35, 1.0, 1.0]}  # in-game violet default
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.normpath(os.path.join(HERE, "..", "godot", "config", "door_fields.json"))


def load(path):
    try:
        with open(path) as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".part"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)  # atomic so the game never reads a half-written file


class DoorFieldUI:
    def __init__(self, root, path):
        self.path, self.data, self._pending = path, load(path), None
        root.title("Force-Field Door Fields")
        self.door = tk.StringVar(value="ALL")
        self.opacity = tk.DoubleVar(value=DEFAULT["opacity"])
        self.color = list(DEFAULT["color"])
        frm = ttk.Frame(root, padding=10)
        frm.grid()
        ttk.Label(frm, text="Door").grid(row=0, column=0, sticky="w")
        box = ttk.Combobox(frm, textvariable=self.door, values=["ALL"] + DOOR_IDS, state="readonly", width=22)
        box.grid(row=0, column=1, sticky="ew")
        box.bind("<<ComboboxSelected>>", lambda _e: self.load_door())
        ttk.Label(frm, text="Opacity").grid(row=1, column=0, sticky="w")
        ttk.Scale(frm, from_=0.0, to=1.0, variable=self.opacity, command=lambda _v: self.schedule()).grid(row=1, column=1, sticky="ew")
        self.swatch = tk.Label(frm, text="      ", relief="sunken")
        self.swatch.grid(row=2, column=0, sticky="w")
        ttk.Button(frm, text="Pick colour...", command=self.pick).grid(row=2, column=1, sticky="ew")
        ttk.Label(frm, text=path, foreground="gray").grid(row=3, column=0, columnspan=2, sticky="w")
        self.load_door()

    def load_door(self):
        e = self.data.get(self.door.get()) or self.data.get("ALL") or DEFAULT
        self.opacity.set(float(e.get("opacity", DEFAULT["opacity"])))
        self.color = list(e.get("color", DEFAULT["color"]))
        self.refresh_swatch()

    def refresh_swatch(self):
        r, g, b = (max(0, min(255, int(c * 255))) for c in self.color[:3])
        self.swatch.configure(background="#%02x%02x%02x" % (r, g, b))

    def pick(self):
        rgb, _hex = colorchooser.askcolor(color=self.swatch.cget("background"), title="Field colour")
        if rgb:
            self.color = [rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0, 1.0]
            self.refresh_swatch()
            self.schedule()

    def schedule(self):
        root = self.swatch.winfo_toplevel()
        if self._pending:
            root.after_cancel(self._pending)
        self._pending = root.after(150, self.write)  # debounce slider drags

    def write(self):
        self._pending = None
        entry = {"opacity": round(float(self.opacity.get()), 3), "color": [round(c, 4) for c in self.color]}
        if self.door.get() == "ALL":
            self.data = {"ALL": entry}  # ALL resets every per-door override
        else:
            self.data[self.door.get()] = entry
        save(self.path, self.data)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--path", default=DEFAULT_PATH)
    args = ap.parse_args()
    root = tk.Tk()
    DoorFieldUI(root, args.path)
    root.mainloop()


if __name__ == "__main__":
    main()
