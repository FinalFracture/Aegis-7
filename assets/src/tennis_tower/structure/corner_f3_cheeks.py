"""Rook (2026-11-20): Rev 3.10 #3 corner stairs (Jared 1:50 PM CT card answer; Vance: F1/F2 Type A cores C-SW/SE/NW/NE exist, scope = F3
tie-ins). At F3 the corner cores end at their guarded wall heads (+12.2) and the F3 stand modules that abut them (12 rows, riser 0.45,
tread 0.95, rake to +17.6) stop with an open end face: up to 5.4 m unguarded drop onto the core-top landing / F3 floor. Each core gets
two stand-end cheeks (Rev 3.8 #3 cheek language: solid slate wall, 1.07 m over every tier, alloy cap):
  long S/N 3.8 m cut bay end (X 40.215 W): 0.10 m cheek on the C-SW/NW front-wall head, 10 mm off the stand end;
  long end at X 102.785 (E): 0.055 m cheek between the stand end and the C-SE/NE core-top guard on that wall head (X 102.85..102.95);
  short W/E bay end (Z 20.515 / 58.485): 0.048 m cheek between the core-top guard ring (Z 20.35..20.45 / 58.55..58.65) and the stand.
The cheek foot follows whatever it stands on (probed: core wall head +12.198, F3 slab +12.2, the under-stand WC shell wall head +14.70,
the stand back wall head +16.6), 2 mm up. Colliders: 'Guard-colonly' = the cheek solid cut into <= 0.40 m bands (TTQA-004 language).
One GLB per corner (tt_struct_f3_corner_cheeks_sw/se/nw/ne), building orientation, layout offsets via struct_lib.export_chunk.
Run: python3 corner_f3_cheeks.py [--layout-out path]   (does NOT write tt_struct_layout.json unless --layout-out points at it)"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from struct_lib import *
from access_rev37 import U
import trimesh

NT, RISE, TREAD, GT = 12, .45, .95, 1.07
MANIFEST = os.path.join(GODOT_MODELS, "tt_tower_manifest.json")

def _bands(m, h=.40):
    """closed solid -> stacked closed slabs of <= h m (stair_core._bands)."""
    lo, hi = m.bounds[0][1], m.bounds[1][1]; nb = max(1, int(np.ceil((hi - lo) / h - 1e-6))); out = []
    for i in range(nb):
        y0, y1 = lo + (hi - lo) * i / nb, lo + (hi - lo) * (i + 1) / nb; b = m
        if i > 0: b = b.slice_plane([0, y0, 0], [0, 1, 0], cap=True)
        if i < nb - 1: b = b.slice_plane([0, y1, 0], [0, -1, 0], cap=True)
        out.append(b)
    o = trimesh.util.concatenate(out); o.metadata["uv"] = np.zeros((len(o.vertices), 2)); return o

# (corner, axis of the cheek run, across lo..hi, run front, run back)  run = coordinate along the stand depth, front = concourse edge
# long ends: run along Z at X; short ends: run along X at Z.  F3 = 12.2, tier k top = 12.2 + 0.45 k over [front -/+ 0.95 (k-1) .. k]
ENDS = {
    "sw": [("z", (40.105, 40.205), 20.522, 9.122), ("x", (20.462, 20.510), 35.522, 24.122)],
    "se": [("z", (102.790, 102.845), 20.522, 9.122), ("x", (20.462, 20.510), 107.478, 118.878)],
    "nw": [("z", (40.105, 40.205), 58.478, 69.878), ("x", (58.490, 58.538), 35.522, 24.122)],
    "ne": [("z", (102.790, 102.845), 58.478, 69.878), ("x", (58.490, 58.538), 107.478, 118.878)],
}

_scene = None
def scene_hit(x0, x1, z0, z1):
    """probed support under a cheek footprint: placed colliders + visuals from the manifest (Rook's corner scan)."""
    global _scene
    if _scene is None:
        sys.path.insert(0, "/workspace/rook_ttqa/corner_stairs"); import scene as S
        ms = []
        for vis in (False, True):
            for bx in ((24, 41.5, 8.5, 21.5), (101.5, 119, 8.5, 21.5), (24, 41.5, 57.5, 70.5), (101.5, 119, 57.5, 70.5)):
                m = S.load(*bx, vis=vis)
                if m is not None: ms.append(m)
        _scene = trimesh.ray.ray_triangle.RayMeshIntersector(trimesh.util.concatenate(ms))
    return _scene

def support(axis, lo, hi, s, ytop):
    """highest surface under the cheek at run coordinate s (3 probes across the thickness), started just under ytop."""
    I = scene_hit(0, 0, 0, 0); best = 12.2
    for a in (lo + .004, (lo + hi) / 2, hi - .004):
        o = [s, ytop - .02, a] if axis == "x" else [a, ytop - .02, s]
        l, _, _ = I.intersects_location([o], [[0, -1, 0]], multiple_hits=False)
        if len(l): best = max(best, float(l[0][1]))
    return best

def cheek(axis, lohi, front, back):
    lo, hi = lohi; sg = 1 if back > front else -1; W = []; CAP = []; supports = []
    for k in range(1, NT + 1):
        a, b = front + sg * TREAD * (k - 1), front + sg * TREAD * k
        if k == 1: a = front                          # flush with the stand front
        if k == NT: b = back
        top = F3 + RISE * k + GT
        ss = np.linspace(min(a, b), max(a, b), max(3, int(abs(b - a) / .01) + 1))
        bs = [round(support(axis, lo, hi, s, F3 + RISE * k), 3) for s in ss]
        # a raised support crossed in one short group (a guard post + its ball finial) -> one run at that group's crown
        i = 0
        while i < len(bs):
            if bs[i] > F3 + .001:
                j = i
                while j + 1 < len(bs) and bs[j + 1] > F3 + .001 and abs(bs[j + 1] - bs[i]) < .3: j += 1
                crown = max(bs[i:j + 1]); bs[i:j + 1] = [crown] * (j + 1 - i); i = j + 1
            else: i += 1
        # runs of equal support -> boxes. A run only reaches past its end samples (by one 10 mm step) toward a LOWER neighbour run,
        # so no box ever pokes into the thing a neighbouring run is stacked on. Foot 2 mm over the floor / wall heads, 5 mm over
        # rail and finial tops 8 mm (sampled crowns).
        i = 0
        while i < len(ss):
            j = i
            while j + 1 < len(ss) and bs[j + 1] == bs[i]: j += 1
            u0 = ss[i] - (.01 if i > 0 and bs[i - 1] < bs[i] else 0); u1 = ss[j] + (.01 if j < len(ss) - 1 and bs[j + 1] < bs[i] else 0)
            y0 = bs[i] + (.002 if bs[i] <= F3 + .001 or abs(bs[i] - 14.7) < .002 or abs(bs[i] - 16.6) < .002 else .008)
            supports.append((round(u0, 3), round(u1, 3), bs[i]))
            W.append(box(u0, u1, y0, top, lo, hi) if axis == "x" else box(lo, hi, y0, top, u0, u1))
            i = j + 1
        u0, u1 = min(a, b), max(a, b)
        CAP.append(box(u0 + .002, u1 - .002, top - E, top + .03, lo + .002, hi - .002) if axis == "x" else box(lo + .002, hi - .002, top - E, top + .03, u0 + .002, u1 - .002))   # 2 mm inset all round: no overhang into the stand / guard, no face on the next tier wall
    return U(W), U(CAP), supports, W

def band_boxes(W, h=.40):
    """collider: every cheek box cut on a global 0.40 m grid from +12.2 -> closed boxes <= 0.40 m high (TTQA-004 bands)."""
    out = []
    for m in W:
        (x0, y0, z0), (x1, y1, z1) = m.bounds
        ys = [y0] + [F3 + h * i for i in range(1, 40) if y0 + .02 < F3 + h * i < y1 - .02] + [y1]
        out += [box(x0, x1, a, b, z0, z1) for a, b in zip(ys[:-1], ys[1:])]
    o = trimesh.util.concatenate(out); o.metadata["uv"] = np.zeros((len(o.vertices), 2)); return o

def build(corner):
    parts = {"Cheek_Wall": [], "Cheek_Cap": []}; cols = []; info = []
    for axis, lohi, front, back in ENDS[corner]:
        w, c, sup, boxes = cheek(axis, lohi, front, back)
        parts["Cheek_Wall"].append(w); parts["Cheek_Cap"].append(c); cols.append(band_boxes(boxes))
        info.append(dict(axis=axis, across=lohi, front=front, back=back, supports=sup))
    return [("Cheek_Wall", SL, parts["Cheek_Wall"]), ("Cheek_Cap", ALY, parts["Cheek_Cap"])], [("Guard-colonly", cols)], info

if __name__ == "__main__":
    REP = []; LAY = {}; INFO = {}
    for c in ("sw", "se", "nw", "ne"):
        P, C, info = build(c); INFO[c] = info
        export_chunk(f"tt_struct_f3_corner_cheeks_{c}", P, C, REP, layout=LAY,
                     note=f"Rev 3.10 #3 corner stairs: F3 stand-end cheeks at C-{c.upper()} (long-bay end + short-bay end), 1.07 m over every tier, Guard-colonly <= 0.40 m bands")
    out = sys.argv[sys.argv.index("--layout-out") + 1] if "--layout-out" in sys.argv else "/workspace/rook_ttqa/corner_stairs/layout_entries.json"
    json.dump(LAY, open(out, "w"), indent=1)
    rd = "/workspace/rook_ttqa/corner_stairs"; json.dump(dict(report=REP, info=INFO), open(os.path.join(rd, "report.json"), "w"), indent=1, default=str)
    print("ASSETS", len(REP), "FAILED", [r["asset"] for r in REP if not r["passed"]])
