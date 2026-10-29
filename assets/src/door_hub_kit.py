#!/usr/bin/env python3
"""
Force-Field Door Hub family (Vance v2 spec, design/forcefield_rfid_access_device_concepts.md).
Shared kit (bezel, unit-number inlay, pictogram display, scan pad, intercom, override, coupler/dock,
pressure columns, hub conduit) + per-concept builders. Quick blockouts.

Hub-local frame: origin = floor, at the hub column centre, on the +Z wall face (z=0).
-Z goes into the 0.30 m wall. Nothing may exceed z=+0.005. Pockets stay above z=-0.30.
Mount in Godot at (hub_x, 0, 0.15) beside rfid_forcefield_door.glb (frame outer edge x=0.91).

Usage: python3 door_hub_kit.py N   (N = 1 Halo Panel, 2 Threshold Spine, 3 Bulkhead Hub, 4 Service Niche)
Writes godot/assets/models/door_hub_cand_0N.glb and a render spec json to godot/_tmp_hub/.
"""
import os, sys, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_builder import SubMesh, PBRMaterialDef, make_beveled_box, make_cylinder, export_glb

MODELS = "/workspace/game-project/godot/assets/models"
TMP = "/workspace/game-project/godot/_tmp_hub"
AMBER = (1.0, 0.584, 0.0)
GREEN = (0.247, 0.686, 0.416)
CYAN = (0.0, 0.898, 1.0)

M = {
    "pearl": PBRMaterialDef("Mat_Hub_Pearl", (0.847, 0.871, 0.902, 1.0), 0.2, 0.40),
    "graph": PBRMaterialDef("Mat_Hub_Graphite", (0.157, 0.180, 0.220, 1.0), 0.5, 0.50),
    "screen": PBRMaterialDef("Mat_Hub_MatteScreen", (0.045, 0.055, 0.065, 1.0), 0.0, 0.85),
    "steel": PBRMaterialDef("Mat_Hub_BrushedSteel", (0.62, 0.64, 0.67, 1.0), 0.9, 0.30),
    "orange": PBRMaterialDef("Mat_Hub_OverrideOrange", (0.851, 0.357, 0.149, 1.0), 0.1, 0.45),
    "glass": PBRMaterialDef("Mat_Hub_Glass", (0.60, 0.70, 0.76, 0.22), 0.1, 0.05, double_sided=True, alpha_mode="BLEND"),
    "fluid": PBRMaterialDef("Mat_Hub_Fluid", (0.20, 0.36, 0.52, 1.0), 0.0, 0.2),
    "glow": PBRMaterialDef("Mat_Hub_StateGlow", AMBER + (1.0,), 0.0, 0.3, emissive=AMBER),
    "cyan": PBRMaterialDef("Mat_Hub_IntercomRing", CYAN + (1.0,), 0.0, 0.3, emissive=tuple(c * 0.4 for c in CYAN)),
}


class Hub:
    def __init__(self):
        self.parts = {}      # node name -> (material key, [geoms])
        self.order = []
        self.cutouts = []    # [w, h, d, cx, cy] hub-local
        self.states = {"standby": {}, "scanning": {}, "granted": {}, "closeup": {}}

    def add(self, node, mat, geom):
        if node not in self.parts:
            self.parts[node] = (mat, []); self.order.append(node)
        self.parts[node][1].append(geom)

    def box(self, node, mat, size, center, bevel=0.0, rz=0.0):
        p, n, u, i = make_beveled_box(size, (0, 0, 0), bevel=bevel)
        if rz:
            a = math.radians(rz)
            R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]], np.float32)
            p = p @ R.T; n = n @ R.T
        self.add(node, mat, (p + np.array(center, np.float32), n, u, i))

    def cyl(self, node, mat, r0, r1, h, center, axis="z", seg=16):
        self.add(node, mat, make_cylinder(r0, r1, h, center, segments=seg, axis=axis))

    def prism(self, node, mat, poly, z0, z1):
        poly = np.array(poly, np.float32); k = len(poly)
        P, N, U, I = [], [], [], []
        mn, mx = poly.min(0), poly.max(0); span = np.maximum(mx - mn, 1e-6)
        for z, nz in ((z1, 1), (z0, -1)):
            b = len(P)
            for q in poly:
                P.append([q[0], q[1], z]); N.append([0, 0, nz]); U.append(list((q - mn) / span))
            for t in range(1, k - 1):
                I.append([b, b + t, b + t + 1] if nz > 0 else [b, b + t + 1, b + t])
        for e in range(k):
            a, c = poly[e], poly[(e + 1) % k]
            d = c - a; nn = np.array([d[1], -d[0], 0]); nn /= max(np.linalg.norm(nn), 1e-9)
            b = len(P)
            for q, z in ((a, z0), (c, z0), (c, z1), (a, z1)):
                P.append([q[0], q[1], z]); N.append(list(nn)); U.append([0, 0])
            I += [[b, b + 1, b + 2], [b, b + 2, b + 3]]
        self.add(node, mat, (np.array(P, np.float32), np.array(N, np.float32), np.array(U, np.float32), np.array(I, np.uint32)))

    def state(self, st, node, **op):
        for s in (st if isinstance(st, (list, tuple)) else [st]):
            self.states[s].setdefault(node, {}).update(op)

    # ---------------- shared kit ----------------
    def pocket(self, w, h, d, cx, cy, bottom_open=False, band=0.014):
        """Stepped pearl/graphite bezel + graphite liner for a flush pocket (cy = centre)."""
        self.cutouts.append([w, h, d, cx, cy])
        hw, hh = w / 2, h / 2
        for sx in (-1, 1):   # outer pearl ring (3 mm proud) and graphite step (recessed)
            self.box("Bezel", "pearl", (band, h, 0.02), (cx + sx * (hw - band / 2), cy, -0.007), 0.003)
            self.box("BezelStep", "graph", (0.010, h - 2 * band, 0.03), (cx + sx * (hw - band - 0.005), cy, -0.021))
            self.box("Liner", "graph", (0.004, h, d), (cx + sx * (hw - 0.002), cy, -d / 2))
        self.box("Bezel", "pearl", (w, band, 0.02), (cx, cy + hh - band / 2, -0.007), 0.003)
        self.box("BezelStep", "graph", (w - 2 * band, 0.010, 0.03), (cx, cy + hh - band - 0.005, -0.021))
        self.box("Liner", "graph", (w, 0.004, d), (cx, cy + hh - 0.002, -d / 2))
        if not bottom_open:
            self.box("Bezel", "pearl", (w, band, 0.02), (cx, cy - hh + band / 2, -0.007), 0.003)
            self.box("BezelStep", "graph", (w - 2 * band, 0.010, 0.03), (cx, cy - hh + band + 0.005, -0.021))
            self.box("Liner", "graph", (w, 0.004, d), (cx, cy - hh + 0.002, -d / 2))
        self.box("Liner", "graph", (w, h, 0.004), (cx, cy, -d + 0.002))

    def face(self, w, h, cx, cy, z=-0.012, mat="graph", node="FacePlate"):
        self.box(node, mat, (w, h, 0.006), (cx, cy, z - 0.003))

    SEG = {"C": "adef", "-": "g", "2": "abged", "1": "bc", "4": "fgbc", "S": "afgcd", "0": "abcdef",
           "E": "adefg", "7": "abc", "A": "abcefg"}

    def unit_number(self, text, cx, cy, ch=0.03, plate=True, z=-0.004):
        """Etched/inlaid unit number as crisp 7-segment geometry on a stepped pearl tab."""
        cw, t = ch * 0.55, ch * 0.12
        total = len(text) * cw * 1.35
        if plate:
            self.box("UnitTab", "pearl", (total + 0.03, ch + 0.024, 0.008), (cx, cy, z - 0.004), 0.002)
        x0 = cx - total / 2 + cw * 0.675
        zz = z + 0.0005
        for k, chh in enumerate(text):
            x = x0 + k * cw * 1.35
            for s in self.SEG.get(chh, ""):
                hx, hy = cw / 2, ch / 2
                seg = {"a": ((cw, t), (0, hy)), "d": ((cw, t), (0, -hy)), "g": ((cw, t), (0, 0)),
                       "b": ((t, hy), (hx, hy / 2)), "c": ((t, hy), (hx, -hy / 2)),
                       "f": ((t, hy), (-hx, hy / 2)), "e": ((t, hy), (-hx, -hy / 2))}[s]
                self.box("UnitDigits", "graph", (seg[0][0], seg[0][1], 0.0015), (x + seg[1][0], cy + seg[1][1], zz))

    def display(self, w, h, cx, cy, z=-0.006):
        """Matte low-glare screen with wordless pictograms (occupant dot, field, P/O2 bars, envelope, spin)."""
        self.box("Display", "screen", (w, h, 0.004), (cx, cy, z - 0.002))
        g, gz = "DisplayGlyphs", z + 0.0005
        u = min(w, h)
        self.cyl(g, "glow", u * 0.06, u * 0.06, 0.001, (cx - w * 0.36, cy + h * 0.36, gz), seg=10)          # occupant dot
        self.box(g, "glow", (w * 0.30, u * 0.035, 0.001), (cx + w * 0.12, cy + h * 0.36, gz))              # field state bar
        for k in range(2):                                                                                 # P / O2 bars
            self.box(g, "glow", (u * 0.06, h * (0.22 + 0.10 * k), 0.001), (cx - w * 0.30 + k * u * 0.11, cy - h * 0.18 + h * 0.05 * k, gz))
        ex, ey, ew, eh = cx + w * 0.18, cy - h * 0.20, w * 0.22, h * 0.16                                  # envelope
        for (sw, sh, ox, oy) in ((ew, 0.002, 0, eh / 2), (ew, 0.002, 0, -eh / 2), (0.002, eh, ew / 2, 0), (0.002, eh, -ew / 2, 0)):
            self.box(g, "glow", (sw, sh, 0.001), (ex + ox, ey + oy, gz))
        for k in range(8):                                                                                 # spin glyph (dotted ring)
            a = k * math.pi / 4
            self.box(g, "glow", (u * 0.03, u * 0.03, 0.001), (cx + w * 0.02 + math.cos(a) * u * 0.09, cy + math.sin(a) * u * 0.09, gz))

    def scan_pad(self, cx, cy, r=0.035, z=-0.004):
        self.cyl("ScanPad", "graph", r, r, 0.006, (cx, cy, z - 0.003), seg=20)
        for k in range(12):
            a = k * math.pi / 6
            self.box("ScanRing", "glow", (0.006, 0.010, 0.002), (cx + math.cos(a) * r * 0.8, cy + math.sin(a) * r * 0.8, z + 0.0015), rz=math.degrees(a))

    def intercom(self, cx, cy, w=0.07, z=-0.004):
        self.box("IntercomPlate", "pearl", (w, 0.05, 0.006), (cx, cy, z - 0.003), 0.002)
        for k in range(5):
            self.box("IntercomGrille", "graph", (w * 0.75, 0.0035, 0.002), (cx - 0.008, cy + 0.016 - k * 0.008, z + 0.0005))
        px = cx + w / 2 - 0.009
        self.box("TalkPad", "graph", (0.010, 0.030, 0.002), (px, cy, z + 0.0005))
        for (sw, sh, ox, oy) in ((0.014, 0.002, 0, 0.017), (0.014, 0.002, 0, -0.017), (0.002, 0.034, 0.007, 0), (0.002, 0.034, -0.007, 0)):
            self.box("IntercomRing", "cyan", (sw, sh, 0.001), (px + ox, cy + oy, z + 0.001))

    def override(self, cx, cy, scale=1.0, z=-0.004):
        """#D95B26 manual field-drop lever behind a hinged smoked cover (hinge at top)."""
        w, h = 0.04 * scale, 0.07 * scale
        self.box("OverrideWell", "graph", (w, h, 0.02), (cx, cy, z - 0.013))
        self.box("OverrideLever", "orange", (0.012 * scale, h * 0.65, 0.010), (cx, cy - h * 0.05, z - 0.007), 0.002)
        self.box("OverrideCover", "glass", (w + 0.006, h + 0.006, 0.004), (cx, cy, z + 0.005))   # front face z=+0.003
        self.box("OverrideHinge", "graph", (w + 0.006, 0.006, 0.006), (cx, cy + h / 2 + 0.003, z + 0.004))
        return (cx, cy + h / 2 + 0.003, z + 0.004)

    def dock(self, w, h, d, cx, coupler_y, coupler="slot", cy=None, bottom=0.0):
        """Floor-level Sprocket dock: liner, induction plate, coupler with occupied ring."""
        cy = bottom + h / 2 if cy is None else cy
        self.pocket(w, h, d, cx, cy, bottom_open=True)
        self.box("InductionPlate", "glow", (w - 0.04, 0.004, d - 0.04), (cx, bottom + 0.002, -d / 2))
        self.box("InductionPlateBase", "graph", (w - 0.02, 0.003, d - 0.02), (cx, bottom + 0.0005, -d / 2))
        cz = -d + 0.006
        if coupler == "slot":
            self.box("Coupler", "graph", (w * 0.6, 0.03, 0.012), (cx, coupler_y, cz))
            for (sw, sh, ox, oy) in ((w * 0.6 + 0.012, 0.004, 0, 0.019), (w * 0.6 + 0.012, 0.004, 0, -0.019),
                                     (0.004, 0.04, w * 0.3 + 0.006, 0), (0.004, 0.04, -w * 0.3 - 0.006, 0)):
                self.box("CouplerRing", "glow", (sw, sh, 0.004), (cx + ox, coupler_y + oy, cz + 0.006))
        else:
            self.cyl("Coupler", "steel", 0.010, 0.010, 0.05, (cx, coupler_y, cz + 0.025), seg=10)
            self.cyl("CouplerRing", "glow", 0.022, 0.022, 0.004, (cx, coupler_y, cz + 0.002), seg=16)

    def hub_conduit(self, x, y0, y1, door_x_local, link_y):
        """Routed light-pipe channel on the wall face: dock -> hub -> door frame conduit."""
        self.box("ConduitChannel", "graph", (0.016, y1 - y0, 0.004), (x, (y0 + y1) / 2, -0.002))
        self.box("HubConduit", "glow", (0.008, y1 - y0, 0.003), (x, (y0 + y1) / 2, -0.0005))
        L = abs(x - door_x_local)
        self.box("ConduitChannel", "graph", (L, 0.016, 0.004), ((x + door_x_local) / 2, link_y, -0.002))
        self.box("HubConduit", "glow", (L, 0.008, 0.003), ((x + door_x_local) / 2, link_y, -0.0005))

    def columns(self, xs, y0, y1, z=-0.012, r=0.009, names=("L", "R")):
        h = y1 - y0
        for x, nm in zip(xs, names):
            self.cyl("ColumnGlass", "glass", r, r, h, (x, (y0 + y1) / 2, z), axis="y", seg=12)
            self.cyl("Fluid_" + nm, "fluid", r * 0.65, r * 0.65, h - 0.01, (x, (y0 + y1) / 2, z), axis="y", seg=8)
            self.cyl("Meniscus_" + nm, "glow", r * 0.68, r * 0.68, 0.004, (x, y1 - 0.007, z), axis="y", seg=8)
            for k in range(7):
                self.box("ColumnTicks", "graph", (0.006, 0.0015, 0.0015), (x + r + 0.005, y0 + 0.01 + k * (h - 0.02) / 6, -0.004))
        return h - 0.01

    def level(self, st, nm, frac, x_unused, y0, y1):
        """Fluid fill fraction (0..1) via scale about column base + meniscus move."""
        h = y1 - y0 - 0.01
        base = y0 + 0.005
        self.state(st, "Fluid_" + nm, scale=[1, frac, 1, 0, base, 0])
        self.state(st, "Meniscus_" + nm, move=[0, (base + h * frac) - (y1 - 0.007), 0])

    def petals(self, cx, cy, R=0.045, z0=-0.010, z1=-0.005):
        names = []
        for k in range(6):
            a0, a1 = math.radians(60 * k + 30), math.radians(60 * k + 90)
            pts = [(0, 0), (R * math.cos(a0), R * math.sin(a0)), (R * math.cos(a1), R * math.sin(a1))]
            c = np.mean(pts, 0)
            pts = [(cx + c[0] + (p[0] - c[0]) * 0.93, cy + c[1] + (p[1] - c[1]) * 0.93) for p in pts]
            nm = "Petal_%d" % k
            self.prism(nm, "pearl", pts, z0, z1)
            self.prism(nm, "graph", [(cx + c[0] * 0.2 + (p[0] - cx) * 0.25, cy + c[1] * 0.2 + (p[1] - cy) * 0.25) for p in pts], z1, z1 + 0.0008) if False else None
            names.append((nm, cx + c[0], cy + c[1], c[0], c[1]))
        hexpts = [(cx + R * math.cos(math.radians(60 * k + 30)), cy + R * math.sin(math.radians(60 * k + 30))) for k in range(6)]
        self.prism("SeamGlow", "glow", hexpts, z0 - 0.003, z0 - 0.001)
        for k in range(6):
            a, b = hexpts[k], hexpts[(k + 1) % 6]
            L = math.dist(a, b); ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
            self.box("HexRim", "glow", (L, 0.003, 0.002), ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, z1 + 0.002), rz=ang)
        return names

    def gyro(self, cx, cy, r=0.035, z=-0.004):
        self.cyl("GyroWell", "graph", r + 0.006, r + 0.006, 0.02, (cx, cy, z - 0.012), seg=20)
        self.cyl("GyroDisc", "steel", r * 0.85, r * 0.85, 0.003, (cx, cy, z - 0.006), seg=20)
        self.box("GyroTick", "glow", (0.003, r * 0.35, 0.002), (cx, cy + r * 0.62, z - 0.004))
        for k in range(16):
            if k == 4: continue   # gap at 12 o'clock = fixed notch
            a = k * math.pi / 8
            self.box("NotchRing", "glow", (0.004, 0.0025, 0.001), (cx + math.cos(a) * (r + 0.003), cy + math.sin(a) * (r + 0.003), z + 0.0005), rz=math.degrees(a))
        self.box("GyroNotch", "graph", (0.004, 0.006, 0.002), (cx, cy + r + 0.003, z + 0.0005))
        self.box("GyroGlass", "glass", (2 * r + 0.006, 2 * r + 0.006, 0.002), (cx, cy, z - 0.001))

    def reeds(self, cx, cy, w=0.12, h=0.16, z=-0.004, n=9):
        self.box("ReedWindowBack", "graph", (w, h, 0.004), (cx, cy, z - 0.034))
        base = cy - h / 2 + 0.012
        for k in range(n):
            x = cx - w * 0.4 + k * (w * 0.8 / (n - 1))
            L = h - 0.035
            self.box("Reed_%d" % k, "graph", (0.003, L, 0.003), (x, base + L / 2, z - 0.022))
            self.box("ReedTip_%d" % k, "glow", (0.0034, 0.010, 0.0034), (x, base + L - 0.005, z - 0.022))
        self.box("ReedHairline", "glow", (w * 0.9, 0.002, 0.002), (cx, base - 0.004, z - 0.022))
        self.box("ReedGlass", "glass", (w, h, 0.003), (cx, cy, z - 0.006))
        return base, z - 0.022

    def rename(self, mapping):
        self.order = [mapping.get(n, n) for n in self.order]
        self.parts = {mapping.get(k, k): v for k, v in self.parts.items()}

    def export(self, n, title, mount_x, extra=None, path=None, check_skip=()):
        subs = []
        for node in self.order:
            mat, gs = self.parts[node]
            P, N, U, I = [], [], [], []; off = 0
            for p, nn, u, i in gs:
                P.append(p); N.append(nn); U.append(u); I.append(i + off); off += len(p)
            subs.append(SubMesh(node, np.vstack(P).astype(np.float32), np.vstack(N).astype(np.float32),
                                np.vstack(U).astype(np.float32), np.vstack(I).astype(np.uint32), M[mat]))
        allp = np.vstack([s.positions for s in subs if s.name not in check_skip])
        tris = sum(len(s.indices) for s in subs)
        zmax, zmin = float(allp[:, 2].max()), float(allp[:, 2].min())
        assert zmax <= 0.005 + 1e-6, f"protrudes {zmax*1000:.1f} mm"
        assert zmin > -0.30, "pocket exceeds wall depth"
        assert allp[:, 0].min() + mount_x >= 0.91 - 1e-4, "overlaps door frame"
        path = path or f"{MODELS}/door_hub_cand_{n:02d}.glb"
        export_glb(path, subs, root_name=f"DoorHubCand{n:02d}" if isinstance(n, int) else "DoorHubBulkhead")
        os.makedirs(TMP, exist_ok=True)
        spec = {"n": n, "title": title, "glb": path, "mount": [mount_x, 0.0, 0.15], "cutouts": self.cutouts,
                "states": self.states, "tris": tris, "zmax": zmax, "zmin": zmin}
        spec.update(extra or {})
        json.dump(spec, open(f"{TMP}/cand_{n}.json", "w"), indent=1)
        print(f"cand {n} tris={tris} zmax={zmax*1000:.1f}mm zmin={zmin:.3f} "
              f"x=[{allp[:,0].min()+mount_x:.3f},{allp[:,0].max()+mount_x:.3f}] cutouts={self.cutouts}")


def glow(c, e=1.5): return {"glow": list(c) + [e]}
OFF = {"off": True}


def std_dock_states(h):
    h.state("standby", "InductionPlate", **glow(AMBER, 0.4)); h.state("standby", "CouplerRing", **glow(AMBER, 0.5))
    h.state("scanning", "InductionPlate", **glow(AMBER, 0.4)); h.state("scanning", "CouplerRing", **glow(AMBER, 0.5))
    h.state(["granted", "closeup"], "InductionPlate", **glow(GREEN, 1.2)); h.state(["granted", "closeup"], "CouplerRing", **glow(GREEN, 2.0))
    h.state("standby", "HubConduit", **glow(AMBER, 0.5)); h.state("scanning", "HubConduit", **glow(AMBER, 1.6))
    h.state(["granted", "closeup"], "HubConduit", **glow(GREEN, 2.2))
    h.state(["standby", "scanning"], "DisplayGlyphs", **glow(AMBER, 0.8)); h.state(["granted", "closeup"], "DisplayGlyphs", **glow(GREEN, 1.2))


# ---------------- concept builders ----------------
def halo():
    h = Hub(); X = 1.15; door = 0.91 - X
    pc = 1.25
    h.pocket(0.32, 0.40, 0.12, 0.0, pc)
    h.face(0.292, 0.372, 0.0, pc, z=-0.012)
    icx, icy = 0.0, pc + 0.02
    h.cyl("IrisWell", "graph", 0.06, 0.06, 0.03, (icx, icy, -0.027), seg=24)
    h.cyl("Cup", "steel", 0.038, 0.038, 0.014, (icx, icy, -0.023), seg=20)
    for k in range(12):
        a = k * math.pi / 6
        h.box("CupRing", "glow", (0.005, 0.009, 0.002), (icx + math.cos(a) * 0.031, icy + math.sin(a) * 0.031, -0.015), rz=math.degrees(a))
    pet = h.petals(icx, icy, 0.045, z0=-0.010, z1=-0.005)
    segs = 12
    for k in range(segs):   # radial ring display around the iris (clockwise from 12 o'clock)
        a = math.pi / 2 - k * 2 * math.pi / segs
        h.box("RingSeg_%02d" % k, "glow", (0.034, 0.012, 0.003), (icx + math.cos(a) * 0.08, icy + math.sin(a) * 0.08, -0.004), rz=math.degrees(a) + 90)
    h.cyl("RingBezel", "pearl", 0.098, 0.098, 0.004, (icx, icy, -0.009), seg=32)
    h.unit_number("C-214", 0.0, pc + 0.168, ch=0.022)
    cy0, cy1 = pc - 0.16, pc + 0.15
    h.columns([-0.128, 0.128], cy0, cy1, names=("L", "R"))
    h.intercom(-0.045, pc - 0.135)
    hinge = h.override(0.055, pc - 0.13, 0.8)
    h.dock(0.40, 0.25, 0.25, 0.0, 0.15)
    h.hub_conduit(door + 0.012, 0.27, pc, door, pc)   # runs in a 16 mm channel on the door side
    std_dock_states(h)
    for k in range(segs):
        nm = "RingSeg_%02d" % k
        h.state("standby", nm, **glow(AMBER, 1.6 if k in (2, 3) else (0.8 if k in (1, 4) else 0.15)))
        h.state("scanning", nm, **glow(AMBER, 1.8 if k < 7 else 0.15))
        h.state(["granted", "closeup"], nm, **glow(GREEN, 1.6))
    h.state(["standby"], "SeamGlow", **glow(AMBER, 1.4)); h.state(["scanning", "granted", "closeup"], "SeamGlow", **OFF)
    h.state(["standby"], "CupRing", **OFF); h.state("scanning", "CupRing", **glow(AMBER, 1.8)); h.state(["granted", "closeup"], "CupRing", **glow(GREEN, 1.8))
    h.state(["standby", "scanning"], "HexRim", **OFF); h.state(["granted", "closeup"], "HexRim", **glow(GREEN, 2.0))
    h.state(["scanning", "granted", "closeup"], "Cup", move=[0, 0, 0.008])
    h.state(["scanning", "granted", "closeup"], "CupRing", move=[0, 0, 0.008])
    for nm, pcx, pcy, dx, dy in pet:
        d = math.hypot(dx, dy)
        for st, r, s in (("scanning", 0.038, 0.45), ("granted", 0.016, 0.8), ("closeup", 0.016, 0.8)):
            h.state(st, nm, scale=[s, s, 1, pcx, pcy, 0], move=[dx / d * r, dy / d * r, 0])
    for st, fl, fr in (("standby", 0.62, 0.48), ("scanning", 0.57, 0.53), ("granted", 0.55, 0.55), ("closeup", 0.55, 0.55)):
        h.level(st, "L", fl, 0, cy0, cy1); h.level(st, "R", fr, 0, cy0, cy1)
    h.state(["standby", "scanning"], "Meniscus_L", **glow(AMBER, 1.2)); h.state(["standby", "scanning"], "Meniscus_R", **glow(AMBER, 1.2))
    h.state(["granted", "closeup"], "Meniscus_L", **glow(GREEN, 1.5)); h.state(["granted", "closeup"], "Meniscus_R", **glow(GREEN, 1.5))
    h.export(1, "HALO PANEL", X, {"bot": {"x": 0.0, "facing": "nose_in"},
             "closeup_cam": [[1.35, 1.50, 1.75], [-0.05, 0.70, 0.15], 55]})


def spine():
    h = Hub(); X = 1.03; door = 0.91 - X
    h.pocket(0.20, 2.10 - 0.35, 0.18, 0.0, 0.35 + (2.10 - 0.35) / 2)
    h.face(0.172, 2.10 - 0.35 - 0.028, 0.0, 0.35 + (2.10 - 0.35) / 2, z=-0.012, mat="pearl")
    h.unit_number("C-214", 0.0, 1.85, ch=0.026)
    h.gyro(0.0, 1.65)
    h.box("DisplayBezel", "graph", (0.152, 0.212, 0.006), (0.0, 1.45, -0.007))
    h.display(0.14, 0.20, 0.0, 1.45)
    base, rz = h.reeds(0.0, 1.15)
    h.intercom(-0.03, 0.95, w=0.08)
    hinge = h.override(0.06, 0.95, 0.75)
    h.dock(0.20, 0.35, 0.25, 0.0, 0.22, coupler="pin")
    n_line = 8
    y0, y1 = 0.38, 2.06
    for k in range(n_line):   # pilaster edge light, door side, segmented so it can climb
        L = (y1 - y0) / n_line
        h.box("PilasterLine_%d" % k, "glow", (0.005, L * 0.92, 0.003), (-0.081, y0 + L * (k + 0.5), -0.0105))
    L = -0.10 - door   # short link from pilaster bezel to door frame edge
    h.box("ConduitChannel", "graph", (L, 0.016, 0.004), (door + L / 2, 2.06, -0.002))
    h.box("HubConduit", "glow", (L, 0.008, 0.003), (door + L / 2, 2.06, -0.0005))
    std_dock_states(h)
    for k in range(n_line):
        nm = "PilasterLine_%d" % k
        h.state("standby", nm, **glow(AMBER, 0.7))
        h.state("scanning", nm, **glow(AMBER, 1.8 if k < 5 else 0.2))
        h.state(["granted", "closeup"], nm, **glow(GREEN, 2.0))
    h.state("standby", "GyroDisc", rot=[0, 0, 1, 40, 0, 1.65, 0]); h.state("standby", "GyroTick", rot=[0, 0, 1, 40, 0, 1.65, 0])
    h.state("scanning", "GyroDisc", rot=[0, 0, 1, -25, 0, 1.65, 0]); h.state("scanning", "GyroTick", rot=[0, 0, 1, -25, 0, 1.65, 0])
    h.state(["standby", "scanning"], "GyroTick", **glow(AMBER, 1.5)); h.state(["standby", "scanning"], "NotchRing", **OFF)
    h.state(["granted", "closeup"], "GyroTick", **glow(GREEN, 1.5)); h.state(["granted", "closeup"], "NotchRing", **glow(GREEN, 1.8))
    for k in range(9):
        a = 6.0 * math.sin(k * 0.9)
        for nm in ("Reed_%d" % k, "ReedTip_%d" % k):
            h.state("scanning", nm, rot=[0, 0, 1, a, 0, base, rz])
        h.state("standby", "ReedTip_%d" % k, **OFF)
        h.state("scanning", "ReedTip_%d" % k, **glow(AMBER, 1.6))
        h.state(["granted", "closeup"], "ReedTip_%d" % k, **glow(GREEN, 1.8))
    h.state(["standby", "scanning"], "ReedHairline", **glow(AMBER, 1.2)); h.state(["granted", "closeup"], "ReedHairline", **glow(GREEN, 1.2))
    h.export(2, "THRESHOLD SPINE", X, {"bot": {"x": 0.0, "facing": "tail_in"},
             "closeup_cam": [[1.35, 1.50, 1.75], [-0.05, 0.70, 0.15], 55]})


def bulkhead():
    h = Hub(); X = 1.14; door = 0.91 - X
    pc = 1.40
    h.pocket(0.40, 0.80, 0.20, 0.0, pc, band=0.02)
    h.face(0.36, 0.76, 0.0, pc, z=-0.014)
    for sx in (-1, 1):   # armour ribs in the bezel step (inside the pocket)
        for k in range(4):
            h.box("ArmorRib", "graph", (0.012, 0.03, 0.008), (sx * 0.17, pc - 0.30 + k * 0.2, -0.008))
    h.unit_number("S-04", 0.0, pc + 0.33, ch=0.05, plate=True)
    h.box("DisplayBezel", "graph", (0.256, 0.316, 0.006), (-0.04, pc + 0.09, -0.009))
    h.display(0.24, 0.30, -0.04, pc + 0.09)
    h.cyl("MembraneWell", "graph", 0.05, 0.05, 0.02, (0.13, pc + 0.20, -0.018), seg=20)
    h.cyl("Membrane", "pearl", 0.044, 0.024, 0.012, (0.13, pc + 0.20, -0.008), seg=20)
    cy0, cy1 = pc - 0.05, pc + 0.12
    h.columns([0.11, 0.15], cy0, cy1, r=0.010)
    h.box("EqualBand", "glow", (0.07, 0.004, 0.002), (0.13, (cy0 + cy1) / 2, -0.010))
    h.scan_pad(-0.10, pc - 0.20)
    h.intercom(0.02, pc - 0.20)
    h.override(0.13, pc - 0.22, 1.3)
    h.dock(0.35, 0.30, 0.25, 0.0, 0.20)
    h.box("DockFlap", "graph", (0.32, 0.27, 0.006), (0.0, 0.135 + 0.01, -0.006), 0.002)
    for k in range(5):   # stencil-style chevrons on the flap
        h.box("FlapChevron", "orange", (0.03, 0.006, 0.001), (-0.10 + k * 0.05, 0.05, -0.0025), rz=35)
    h.hub_conduit(door + 0.012, 0.31, pc, door, pc)
    std_dock_states(h)
    h.state("closeup", "DockFlap", rot=[1, 0, 0, 80, 0, 0.28, -0.006]); h.state("closeup", "FlapChevron", rot=[1, 0, 0, 80, 0, 0.28, -0.006])
    h.state("standby", "Membrane", scale=[1, 1, 1.0, 0, 0, -0.014])
    h.state(["scanning", "granted", "closeup"], "Membrane", scale=[1, 1, 0.35, 0, 0, -0.014])
    for st, fl, fr in (("standby", 0.75, 0.40), ("scanning", 0.62, 0.52), ("granted", 0.57, 0.57), ("closeup", 0.57, 0.57)):
        h.level(st, "L", fl, 0, cy0, cy1); h.level(st, "R", fr, 0, cy0, cy1)
    for nm in ("Meniscus_L", "Meniscus_R"):
        h.state(["standby", "scanning"], nm, **glow(AMBER, 1.2)); h.state(["granted", "closeup"], nm, **glow(GREEN, 1.5))
    h.state(["standby", "scanning"], "EqualBand", **OFF); h.state(["granted", "closeup"], "EqualBand", **glow(GREEN, 2.0))
    h.state(["standby"], "ScanRing", **glow(AMBER, 0.6)); h.state("scanning", "ScanRing", **glow(AMBER, 1.8)); h.state(["granted", "closeup"], "ScanRing", **glow(GREEN, 1.8))
    h.export(3, "BULKHEAD HUB", X, {"bot": {"x": 0.0, "facing": "nose_in"},
             "closeup_cam": [[1.35, 1.50, 1.75], [-0.05, 0.70, 0.15], 55]})


def niche():
    h = Hub(); X = 1.21; door = 0.91 - X
    h.pocket(0.55, 1.50, 0.28, 0.0, 0.75, bottom_open=True)
    # upper wall stepped forward (front at z=-0.105), with an open cavity for the emblem stack
    for (x0, x1, y0, y1) in ((-0.26, 0.105, 0.80, 1.46), (0.235, 0.26, 0.80, 1.46), (0.105, 0.235, 0.80, 1.07), (0.105, 0.235, 1.37, 1.46)):
        h.box("NicheUpperFace", "pearl", (x1 - x0, y1 - y0, 0.10), ((x0 + x1) / 2, (y0 + y1) / 2, -0.155))
    h.box("DisplayBezel", "graph", (0.316, 0.196, 0.006), (-0.08, 1.30, -0.103))
    h.display(0.30, 0.18, -0.08, 1.30, z=-0.100)
    h.scan_pad(-0.08, 1.10, z=-0.100)
    h.intercom(-0.08, 0.95, z=-0.100)
    h.override(0.03, 0.95, 0.9, z=-0.100)
    # Lenticular emblem stack (12 glass slats + etched emblem shards) beside the display
    ex, ey = 0.17, 1.22
    h.box("EmblemWell", "graph", (0.13, 0.30, 0.004), (ex, ey, -0.20))
    for sx in (-1, 1):
        h.box("EmblemEdgeLight", "glow", (0.004, 0.30, 0.03), (ex + sx * 0.062, ey, -0.13))
    slats = []
    for k in range(12):
        y = ey - 0.135 + k * 0.0245
        h.box("Slat_%02d" % k, "glass", (0.11, 0.022, 0.004), (ex, y, -0.12))
        dy = y - ey; R = 0.10
        wv = max(0.0, R - abs(dy)) * 0.5
        if wv > 0.004:
            for sx in (-1, 1):
                h.box("Etch_%02d" % k, "pearl", (0.006, 0.018, 0.001), (ex + sx * wv, y, -0.1175))
        if abs(dy) < 0.06:
            h.box("Etch_%02d" % k, "pearl", (0.004, 0.018, 0.001), (ex, y, -0.1175))
        slats.append((k, y))
    h.unit_number("E-117", ex, 0.99, ch=0.022, z=-0.100)
    # shelf + consumables above the berth
    h.box("Shelf", "graph", (0.52, 0.012, 0.22), (0.0, 0.80, -0.16))
    for k, x in enumerate((-0.18, -0.10, -0.02)):
        h.cyl("Canister", "orange" if k == 0 else "steel", 0.025, 0.025, 0.09, (x, 0.851, -0.16), axis="y", seg=12)
    h.box("WireSpool", "graph", (0.10, 0.06, 0.08), (0.14, 0.836, -0.16), 0.01)
    # berth
    h.box("InductionPlate", "glow", (0.48, 0.004, 0.24), (0.0, 0.002, -0.14))
    h.box("InductionPlateBase", "graph", (0.52, 0.003, 0.26), (0.0, 0.0005, -0.14))
    h.box("CouplerArm", "steel", (0.04, 0.16, 0.03), (0.0, 0.70, -0.20), 0.004)
    h.cyl("CouplerRing", "glow", 0.024, 0.024, 0.004, (0.0, 0.62, -0.20), axis="y", seg=16)
    h.box("BayRim", "glow", (0.50, 0.004, 0.004), (0.0, 0.785, -0.012))
    h.hub_conduit(door + 0.012, 0.05, 1.45, door, 1.45)
    std_dock_states(h)
    for nm in ("CouplerArm", "CouplerRing"):
        h.state(["granted", "closeup"], nm, move=[0, -0.10, 0])
    for k, y in slats:
        r = [(-38, 22, -15, 33, -27, 12, 40, -20, 28, -35, 18, -10)[k]]
        for nm in ("Slat_%02d" % k, "Etch_%02d" % k):
            if nm not in h.parts: continue
            h.state("standby", nm, rot=[0, 1, 0, r[0], ex, y, -0.12])
            if k >= 6:
                h.state("scanning", nm, rot=[0, 1, 0, r[0], ex, y, -0.12])
    h.state(["standby", "scanning"], "EmblemEdgeLight", **glow(AMBER, 1.0)); h.state(["granted", "closeup"], "EmblemEdgeLight", **glow(GREEN, 1.5))
    h.state(["standby", "scanning"], "BayRim", **glow(AMBER, 0.8)); h.state(["granted", "closeup"], "BayRim", **glow(GREEN, 1.6))
    h.state("standby", "ScanRing", **glow(AMBER, 0.6)); h.state("scanning", "ScanRing", **glow(AMBER, 1.8)); h.state(["granted", "closeup"], "ScanRing", **glow(GREEN, 1.8))
    h.export(4, "SERVICE NICHE", X, {"bot": {"x": 0.0, "facing": "tail_in"},
             "closeup_cam": [[1.35, 1.50, 1.75], [-0.05, 0.70, 0.15], 55]})


def bulkhead_final():
    """Final Bulkhead Hub (Jared's pick): cand 03 hub + floor DOCK PAD for the real Sprocket
    (char_bot_r2_05, ~0.78 W x 1.03 H x 0.77 D) + fold-out WALL COUPLER ARM.
    Arm is modelled DEPLOYED (pointing +Z). Stow = rotate CouplerArm/CouplerHead/CouplerHead_Ring
    +90 deg about +Y around ARM_PIVOT (folds flat into its wall pocket, max 5 mm proud)."""
    h = Hub(); X = 1.14; door = 0.91 - X
    pc = 1.40
    h.pocket(0.40, 0.80, 0.20, 0.0, pc, band=0.02)
    h.face(0.36, 0.76, 0.0, pc, z=-0.014)
    for sx in (-1, 1):
        for k in range(4):
            h.box("ArmorRib", "graph", (0.012, 0.03, 0.008), (sx * 0.17, pc - 0.30 + k * 0.2, -0.008))
    h.unit_number("S-04", 0.0, pc + 0.33, ch=0.05, plate=True)
    h.box("DisplayBezel", "graph", (0.256, 0.316, 0.006), (-0.04, pc + 0.09, -0.009))
    h.display(0.24, 0.30, -0.04, pc + 0.09)
    h.cyl("MembraneWell", "graph", 0.05, 0.05, 0.02, (0.13, pc + 0.20, -0.018), seg=20)
    h.cyl("Membrane", "pearl", 0.044, 0.024, 0.012, (0.13, pc + 0.20, -0.008), seg=20)
    cy0, cy1 = pc - 0.05, pc + 0.12
    h.columns([0.11, 0.15], cy0, cy1, r=0.010)
    h.box("EqualBand", "glow", (0.07, 0.004, 0.002), (0.13, (cy0 + cy1) / 2, -0.010))
    h.scan_pad(-0.10, pc - 0.20)
    h.intercom(0.02, pc - 0.20)
    h.override(0.13, pc - 0.22, 1.3)
    # light pipe: hub -> door frame conduit (x=0.91), and down to the coupler-arm pocket
    h.hub_conduit(door + 0.012, PORT_Y, pc, door, pc)
    L = 0.195 - (door + 0.012)
    h.box("ConduitChannel", "graph", (L, 0.016, 0.004), (door + 0.012 + L / 2, PORT_Y, -0.002))
    h.box("HubConduit", "glow", (L, 0.008, 0.003), (door + 0.012 + L / 2, PORT_Y, -0.0005))
    # coupler arm wall pocket (arm folds flat into it)
    h.pocket(0.26, 0.10, 0.06, 0.325, PORT_Y)
    px, py, pz = ARM_PIVOT
    h.cyl("CouplerArm_Pivot", "steel", 0.015, 0.015, 0.06, (px, py, pz), axis="y", seg=12)
    h.box("CouplerArm", "steel", (0.03, 0.03, PORT_Z - 0.025 - pz), (px, py, (pz + PORT_Z - 0.025) / 2), 0.004)
    h.box("CouplerHead", "graph", (0.06, 0.06, 0.025), (px, py, PORT_Z - 0.0125), 0.004)
    h.cyl("CouplerHead_Ring", "glow", 0.022, 0.022, 0.003, (px, py, PORT_Z + 0.0005), seg=16)
    # floor dock pad (13 mm total), centred beside the hub, clear of the door approach
    cx, cz = PAD_C
    h.box("DockPad", "graph", (0.90, 0.012, 0.90), (cx, 0.006, cz), 0.004)
    for k in range(24):
        a = k * math.pi / 12
        h.box("DockPad_InductionRing", "glow", (0.06, 0.001, 0.016), (cx + math.cos(a) * 0.28, 0.0125, cz + math.sin(a) * 0.28), rz=0)
    for k in range(3):   # guide chevrons pointing back toward the wall (reverse-in)
        for sx in (-1, 1):
            h.box("DockPad_Chevrons", "pearl", (0.012, 0.001, 0.12), (cx + sx * 0.04, 0.0125, cz + 0.36 - k * 0.07 + 0.0), rz=0)
    # rotate chevron arms (+/-40 deg about Y) in place
    geoms = h.parts["DockPad_Chevrons"][1]
    for i, (p, n, u, ix) in enumerate(geoms):
        c = p.mean(0); sx = 1 if c[0] > cx else -1
        a = math.radians(40 * sx); R = np.array([[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]], np.float32)
        geoms[i] = ((p - c) @ R.T + c, n @ R.T, u, ix)
    for nm in ("DockPad_InductionRing",):   # induction ring segments tangent
        geoms = h.parts[nm][1]
        for i, (p, n, u, ix) in enumerate(geoms):
            c = p.mean(0); a = -math.atan2(c[2] - cz, c[0] - cx) + math.pi / 2
            R = np.array([[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]], np.float32)
            geoms[i] = ((p - c) @ R.T + c, n @ R.T, u, ix)
    h.rename({"FacePlate": "HubPanel", "Bezel": "HubPanel_Bezel", "BezelStep": "HubPanel_BezelStep", "Liner": "HubPanel_Liner",
              "ScanPad": "ScanZone", "ScanRing": "ScanZone_Ring", "OverrideLever": "Override", "OverrideCover": "Override_Cover",
              "OverrideHinge": "Override_Hinge", "OverrideWell": "Override_Well", "HubConduit": "LightPipe",
              "ConduitChannel": "LightPipe_Channel", "UnitDigits": "UnitNumber_Etch", "UnitTab": "UnitNumber_Tab"})
    # stowed-pose protrusion check for the arm
    a = math.radians(90); R = np.array([[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]])
    piv = np.array(ARM_PIVOT)
    stz = max(float((((np.vstack([g[0] for g in h.parts[nm][1]]) - piv) @ R.T) + piv)[:, 2].max())
              for nm in ("CouplerArm", "CouplerHead", "CouplerHead_Ring", "CouplerArm_Pivot"))
    assert stz <= 0.005 + 1e-6, f"stowed arm proud {stz}"
    print(f"stowed arm max z = {stz*1000:.1f} mm")
    skip = ("DockPad", "DockPad_InductionRing", "DockPad_Chevrons", "CouplerArm", "CouplerHead", "CouplerHead_Ring")
    h.export("bulkhead", "BULKHEAD HUB FINAL", X, {"pad": PAD_C, "port": [px, PORT_Y, PORT_Z], "pivot": list(ARM_PIVOT)},
             path=f"{MODELS}/door_hub_bulkhead.glb", check_skip=skip)


# Sprocket (char_bot_r2_05) has no port node: coupler point = centre of the rear torso face
# (Torso_Core rear z=-0.325 in bot space, torso height 0.245-0.655 m -> port y = 0.45 m).
# Bot parks tail-to-wall with origin at PAD_C, facing +Z (its default), so port z = 0.47-0.325 = 0.145.
PAD_C = (0.25, 0.47)
PORT_Y, PORT_Z = 0.45, 0.145
ARM_PIVOT = (0.25, PORT_Y, -0.025)

if __name__ == "__main__":
    a = sys.argv[1]
    if a == "bulkhead":
        bulkhead_final()
    else:
        {1: halo, 2: spine, 3: bulkhead, 4: niche}[int(a)]()
