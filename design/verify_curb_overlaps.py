"""Rook: verify 0 curb-curb and 0 curb-kerb XZ footprint overlaps in exterior_placements_v1_3.json (AABB, eps 1 mm; Y ignored)."""
import json, sys, math, collections
A = [a for a in sys.argv[1:] if a != "-v"]; F = A[0] if A else "design/exterior_placements_v1_3.json"
SIZE = {"ext_curb_segment.glb": (1.994, .304), "ext_curb_corner.glb": (.304, .304), "ext_tram_platform_kerb.glb": (1.994, 1.9)}
EPS = 1e-3
def box(p):
    sx, sz = SIZE[p["asset"]]; q = int(round((p["rot_deg"] % 360) / 90)) % 2
    hx, hz = (sz/2, sx/2) if q else (sx/2, sz/2); return (p["x"]-hx, p["x"]+hx, p["z"]-hz, p["z"]+hz)
def hit(a, b): return a[0] < b[1]-EPS and b[0] < a[1]-EPS and a[2] < b[3]-EPS and b[2] < a[3]-EPS
P = json.load(open(F))["placements"]
curbs = [p for p in P if p["asset"] in ("ext_curb_segment.glb", "ext_curb_corner.glb")]
kerbs = [p for p in P if p["asset"] == "ext_tram_platform_kerb.glb"]
CB = [box(p) for p in curbs]; KB = [box(p) for p in kerbs]
cc = [(i, j) for i in range(len(curbs)) for j in range(i+1, len(curbs)) if hit(CB[i], CB[j])]
ck = [(i, j) for i in range(len(curbs)) for j in range(len(kerbs)) if hit(CB[i], KB[j])]
dup = [k for k, v in collections.Counter((p["asset"], p["x"], p["z"], p["rot_deg"] % 180) for p in curbs).items() if v > 1]
print(f"{F}: segments {sum(p['asset']=='ext_curb_segment.glb' for p in curbs)}, corners {sum(p['asset']=='ext_curb_corner.glb' for p in curbs)}, kerbs {len(kerbs)}")
print(f"curb-curb overlaps {len(cc)}, curb-kerb overlaps {len(ck)}, exact duplicates {len(dup)}")
if "-v" in sys.argv:
    for i, j in cc[:400]: print("CC", curbs[i]["note"][:70], "|", curbs[j]["note"][:70], (curbs[i]["x"], curbs[i]["z"]), (curbs[j]["x"], curbs[j]["z"]))
sys.exit(1 if cc or ck else 0)
