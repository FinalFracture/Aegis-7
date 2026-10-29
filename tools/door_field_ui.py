#!/usr/bin/env python3
r"""Cylinder Hab-7 // RFID force-field door field UI ([t45u]).

File format: {"DOOR_RM1B": {"opacity": 0.4, "color": [r, g, b, a]}, "ALL": {...}, ...}
The running game polls the file every 0.5 s, re-applies it when its modified time changes and calls
set_door_field(door_id, opacity, color) on each door ("ALL" = every door, applied first).

Where the game reads it:
  * editor / dev run (`godot --path godot`):  res://config/door_fields.json  = godot/config/door_fields.json
    (default target of this tool; godot/config/ is gitignored)
  * exported build:                          user://door_fields.json
    user:// is Godot's app_userdata/<project name>/ folder:
      Linux   ~/.local/share/godot/app_userdata/<name>/
      Windows %APPDATA%\Godot\app_userdata\<name>\
      macOS   ~/Library/Application Support/Godot/app_userdata/<name>/
    The game prints the exact folder at boot ("[FORCEFIELD] door field overrides: ... (user dir: ...)").
    Target it with --user (guessed folder) or --user-dir <that folder>; --print-paths shows both.

Run:  python3 tools/door_field_ui.py                       GUI (needs python3-tk)
      python3 tools/door_field_ui.py --set DOOR_RM1B --opacity 0.4 --color 0,1,1,1
      python3 tools/door_field_ui.py --set ALL --opacity 0.45 --color 0.72,0.35,1,1 --user
      python3 tools/door_field_ui.py --print-paths
"""
import argparse
import json
import os
import re
import sys

DOOR_IDS = ["DOOR_APT201", "DOOR_ALCOVE2C", "DOOR_APT202", "DOOR_RM1A", "DOOR_RM1B", "DOOR_SECTOR4_EXIT"]
DEFAULT = {"opacity": 0.45, "color": [0.72, 0.35, 1.0, 1.0]}  # in-game violet default
HERE = os.path.dirname(os.path.abspath(__file__))
GODOT_DIR = os.path.normpath(os.path.join(HERE, "..", "godot"))
DEFAULT_PATH = os.path.join(GODOT_DIR, "config", "door_fields.json")


def project_name():
    try:
        with open(os.path.join(GODOT_DIR, "project.godot")) as f:
            m = re.search(r'^config/name="(.*)"', f.read(), re.M)
        return m.group(1) if m else "Godot Project"
    except OSError:
        return "Godot Project"


def guess_user_dir():
    """Best guess at Godot's user:// folder (the game prints the authoritative one at boot)."""
    name = re.sub(r'[\\/:*?"<>|]', "-", project_name())  # chars invalid in folder names
    if sys.platform.startswith("win"):
        base = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "Godot")
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support/Godot")
    else:
        base = os.path.join(os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share")), "godot")
    return os.path.join(base, "app_userdata", name)


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


def parse_color(text):
    parts = [float(p) for p in text.split(",")]
    if len(parts) not in (3, 4):
        raise argparse.ArgumentTypeError("color must be r,g,b or r,g,b,a (0..1)")
    return [max(0.0, min(1.0, p)) for p in parts] + ([1.0] if len(parts) == 3 else [])


def set_entry(path, door, opacity, color):
    data = load(path)
    entry = {"opacity": round(max(0.0, min(1.0, opacity)), 3), "color": [round(c, 4) for c in color]}
    if door == "ALL":
        data = {"ALL": entry}  # ALL resets every per-door override
    else:
        data[door] = entry
    save(path, data)
    return data


class DoorFieldUI:
    def __init__(self, root, path):
        from tkinter import ttk

        self.path, self.data, self._pending = path, load(path), None
        root.title("Force-Field Door Fields")
        import tkinter as tk
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
        from tkinter import colorchooser
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
        self.data = set_entry(self.path, self.door.get(), float(self.opacity.get()), self.color)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--path", help="explicit JSON file (overrides --user / --user-dir)")
    ap.add_argument("--user", action="store_true", help="write user://door_fields.json (exported build) in the guessed user dir")
    ap.add_argument("--user-dir", help="Godot user:// folder printed by the game at boot")
    ap.add_argument("--set", metavar="DOOR_ID", choices=["ALL"] + DOOR_IDS, help="write one entry and exit (no GUI)")
    ap.add_argument("--opacity", type=float, default=DEFAULT["opacity"])
    ap.add_argument("--color", type=parse_color, default=DEFAULT["color"], help="r,g,b[,a] in 0..1")
    ap.add_argument("--print-paths", action="store_true", help="print the dev and user:// JSON paths and exit")
    args = ap.parse_args()
    user_path = os.path.join(args.user_dir or guess_user_dir(), "door_fields.json")
    path = args.path or (user_path if (args.user or args.user_dir) else DEFAULT_PATH)
    if args.print_paths:
        print("dev   (res://config/door_fields.json):", DEFAULT_PATH)
        print("user  (user://door_fields.json):      ", user_path)
        return
    if args.set:
        data = set_entry(path, args.set, args.opacity, args.color)
        print("wrote %s: %s" % (path, json.dumps(data)))
        return
    try:
        import tkinter as tk
    except ImportError:
        sys.exit("tkinter is not installed (apt install python3-tk); use --set DOOR_ID --opacity X --color r,g,b,a instead")
    root = tk.Tk()
    DoorFieldUI(root, path)
    root.mainloop()


if __name__ == "__main__":
    main()
