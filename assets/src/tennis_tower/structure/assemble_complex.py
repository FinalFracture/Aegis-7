"""Rook: Tennis Tower integrated PREVIEW (box-side only, not a game scene).

Merges assemble_preview's structure / envelope / site / hull with every committed
temp-*_placements.json on main. Owner files win for their room contents; Courts is
canonical for stands and court doors. temp-Services_placements.json is untracked /
unverified and is excluded. Writes a placement report + optional Godot tour under
/workspace/renders/tennis_tower/complex_tour/.

Usage: python3 assemble_complex.py [--no-render] [--sanity-only] [--shots name,name]
"""
from __future__ import annotations

import json, math, os, shutil, subprocess, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import assemble_preview as AP
import numpy as np
import trimesh

ROOT = AP.ROOT
MD = AP.MD
OUT = "/workspace/renders/tennis_tower/complex_tour"
ROOMS = os.path.join(MD, "rooms")

# Committed placement files only (Services is untracked — do not load it).
OWNER_FILES = {
    "Arrival": "temp-Arrival_placements.json",
    "Aquatics": "temp-Aquatics_placements.json",
    "Leisure": "temp-Leisure_placements.json",
    "Courts": "temp-Courts_placements.json",
    "Active": "temp-Active_placements.json",
    "Rooftop": "temp-Rooftop_placements.json",
}

# Categories assemble_preview still emits that owners now own. Dropped from the
# Rook side so the owner record is the only copy (positions may differ).
OWNER_ASSETS = (
    "tt_stand_module",
    "tt_court_partition",
    "tt_court_net",
    "tt_aquarium_",
    "tt_foyer_",
    "tt_climbing_",
    "tt_cabana",
    "tt_bar",
    "tt_bar_stool",
    "tt_play_",
    "tt_toddler_zone",
    "tt_soft_play",
    "tt_see_saw",
    "tt_swing_set",
    "tt_balance_trail",
    "tt_dome_climber",
    "tt_fence_",
    "tt_roof_plant_cutout",
)

SKIP_STATUS = {"withheld", "held", "held_unplaced", "unplaced", "skipped", "proposed_unplaced"}

# Whole-floor container meshes: rooms sit inside these AABBs by design.
MEGA_STRUCTURE = {
    "preview_hull",
    "tt_struct_f1_slab", "tt_struct_f1_walls",
    "tt_struct_f2_slab", "tt_struct_f2_walls",
    "tt_struct_f3_slab", "tt_struct_f3_walls",
    "tt_struct_columns",
}


# Leisure asked for these two entrances; assemble_preview.envelope already places them.
LEISURE_ENTRANCES = (
    ("tt_secondary_entrance_n", (72.0, 0.0, 79.98), 0.0),
    ("tt_secondary_entrance_e", (140.98, 0.0, 37.5), 90.0),
)

HIDE_UPPER = ["f2", "f3", "roof", "env", "facade", "plant"]
HIDE_F3_ROOF = ["f3", "roof", "env", "facade", "plant"]
HIDE_ROOF = ["roof", "env"]

# name, camera pos, look-at, fov, hidden tags, amb, exposure, omni mul
SHOTS = [
    ("01_exterior_hero_sw",           (-62, 42, -32), (70, 10, 42), 48, [], 1.35, 1.15, 0.7),
    ("02_exterior_hero_ne",           (198, 40, 128), (70, 10, 40), 48, [], 1.35, 1.15, 0.7),
    ("03_aerial_overview",            (40, 95, -48), (64, 4, 40), 50, [], 1.25, 1.1, 0.6),
    ("04_west_entrance_run",          (-42, 5.5, 14), (-10, 5.5, 44), 58, [], 1.4, 1.15, 0.8),
    ("05_foyer_desks_kiosks",         (-8.2, 1.85, 21.5), (-1.2, 1.35, 33.5), 68, [], 2.0, 1.25, 1.3),
    ("06_aquarium_corridor",          (1.6, 1.75, 36.4), (21.5, 1.55, 40.6), 70, [], 2.0, 1.25, 1.3),
    ("07_pool_diving_hall",           (2.2, 4.2, 3.5), (20, 2.4, 24), 72, [], 2.05, 1.3, 1.35),
    ("08_leisure_slides_link",        (4.0, 8.2, 74.5), (22, 5.2, 56.5), 68, [], 2.0, 1.25, 1.3),
    ("09_spin_court_hall",            (71.5, 16, 8), (71.5, 0.5, 40), 58, HIDE_UPPER, 1.7, 1.2, 1.1),
    ("10_concourse_stands",           (51.0, 12.5, 23.5), (60.0, 3.5, 18.2), 58, HIDE_F3_ROOF, 1.75, 1.2, 1.15),
    ("11_bowling",                    (36.5, 1.85, 7.4), (64, 1.2, 7.4), 68, [], 2.05, 1.3, 1.35),
    ("12_arcade",                     (146, 14, 42), (128, 2.2, 42), 58, HIDE_F3_ROOF, 1.7, 1.2, 1.1),
    ("13_food_court",                 (80.0, 1.8, 67.8), (81.0, 1.25, 76.0), 65, HIDE_UPPER, 2.0, 1.3, 1.3),
    ("14_rink",                       (52, 10.5, 16), (72, 7.0, 40), 62, HIDE_F3_ROOF, 1.85, 1.25, 1.2),
    ("15_climbing_gym",               (46, 10.0, -5.0), (46, 10.5, 8.0), 58, HIDE_F3_ROOF, 1.85, 1.25, 1.2),
    ("16_gym",                        (70, 15.5, 91.0), (72, 6.4, 71.5), 58, HIDE_F3_ROOF, 1.75, 1.2, 1.15),
    ("17_rooftop_dining_bar",         (5.5, 15.0, 22), (14.0, 13.4, 39.5), 62, HIDE_ROOF, 1.8, 1.25, 1.2),
    ("18_cabanas",                    (-24, 18, 12), (-6, 13.4, 40), 58, HIDE_ROOF, 1.7, 1.2, 1.1),
    ("19_playground",                 (128.5, 16.5, 16), (134.5, 13.0, 42), 60, HIDE_ROOF, 1.7, 1.2, 1.1),
    ("20_basketball_track",           (20, 26, -6), (72, 13.5, 42), 58, HIDE_ROOF, 1.65, 1.2, 1.05),
]
SHOTS += [   # r2 tour (2026-11-10): Rev 3.5/3.6 ramps, flush footbridge, lead wall, feature stair, foyer end wall, T2 gate, tree crowns
    ("21_pool_switchback_ramp",       (13.5, 7.5, 20.5), (5.5, 1.0, 29.5), 64, HIDE_UPPER, 2.0, 1.25, 1.3),
    ("22_leisure_s_strip_ramp",       (-4.0, 1.7, 46.0), (6.0, 0.8, 45.6), 66, HIDE_UPPER, 2.0, 1.25, 1.3),
    ("23_flush_footbridge_s",         (14.5, 2.7, 54.5), (19.0, 0.9, 48.5), 64, HIDE_UPPER, 2.0, 1.25, 1.3),
    ("24_lead_climbing_wall",         (35.6, 13.9, 3.5), (50.0, 11.0, 7.8), 76, [], 2.0, 1.25, 1.3),
    ("25_arcade_feature_stair",       (128.0, 9.2, 34.0), (135.5, 4.5, 39.25), 64, HIDE_F3_ROOF, 2.0, 1.25, 1.3),
    ("26_foyer_end_wall_st_aqn",      (-2.6, 1.7, 52.0), (-3.0, 2.4, 58.4), 70, [], 2.0, 1.25, 1.3),
    ("27_t2_bridge_gate",             (14.5, 8.0, 63.5), (20.0, 7.0, 58.7), 62, [], 2.0, 1.25, 1.3),
    ("28_tree_crowns_over_f3_stands", (49.0, 15.0, 22.0), (57.5, 19.5, 9.0), 66, [], 1.6, 1.1, 1.1),
]


def asset_name(glb, asset=None):
    if asset:
        return asset
    return os.path.basename(glb or "").replace(".glb", "")


def is_owner_asset(asset):
    for prefix in OWNER_ASSETS:
        if asset == prefix or asset.startswith(prefix):
            return True
    return False


def resolve_glb(rec):
    glb = rec.get("glb") or ""
    asset = rec.get("asset")
    if glb.startswith("res://assets/models/"):
        return os.path.join(MD, glb[len("res://assets/models/"):])
    if glb.startswith(MD) or (glb.startswith("/") and glb.endswith(".glb")):
        return glb
    if glb.startswith("godot/"):
        return os.path.join(ROOT, glb)
    if asset:
        return os.path.join(MD, asset + ".glb")
    if glb:
        return os.path.join(MD, os.path.basename(glb))
    return None


def rec_pos(rec):
    return list(rec.get("p") or rec.get("pos") or [0, 0, 0])


def rec_yaw(rec):
    if "yaw" in rec:
        return float(rec["yaw"])
    if "yaw_deg" in rec:
        return float(rec["yaw_deg"])
    return 0.0


def rec_status(rec):
    for k in ("placement_status", "status", "state"):
        if rec.get(k) is not None:
            return str(rec[k]).strip().lower()
    return ""


def floor_tag(rec, owner):
    t = rec.get("tag")
    if t in {"f1", "f2", "f3", "roof", "env", "facade", "plant", "site", "ground", "cols", "struct"}:
        # Rooftop plant collars must hide with the roof on cutaways.
        asset = rec.get("asset") or ""
        if asset.startswith("tt_roof_") or (rec.get("room") or "") == "F3-ROOF-CUT":
            return "roof"
        return t
    room = rec.get("room") or ""
    asset = rec.get("asset") or ""
    if "ROOF" in room or asset.startswith("tt_roof_"):
        return "roof"
    if room.startswith("F3") or "F3-" in room:
        return "f3"
    if room.startswith("F2") or "F2-" in room:
        return "f2"
    if room.startswith("F1") or "F1-" in room:
        return "f1"
    y = rec_pos(rec)[1]
    if y >= 20:
        return "roof"
    if y >= 11:
        return "f3"
    if y >= 5:
        return "f2"
    return "f1"


def iter_owner_records(data):
    if isinstance(data, list):
        for r in data:
            yield r
        return
    if not isinstance(data, dict):
        return
    if "rooms" in data and isinstance(data["rooms"], dict):
        for recs in data["rooms"].values():
            if isinstance(recs, list):
                for r in recs:
                    yield r
        return
    if "items" in data and isinstance(data["items"], list):
        for r in data["items"]:
            yield r
        return
    if "placements" in data and isinstance(data["placements"], list):
        for r in data["placements"]:
            yield r


def load_owner(owner, filename, log):
    path = os.path.join(ROOMS, filename)
    data = json.load(open(path))
    kept, skipped = [], Counter()
    for rec in iter_owner_records(data):
        st = rec_status(rec)
        if st in SKIP_STATUS:
            skipped[st or "blank"] += 1
            continue
        # Active: "proposed" = owner's judgement, but the records are real placed
        # geometry in the committed file (withheld lives in a separate list).
        glb = resolve_glb(rec)
        asset = asset_name(glb, rec.get("asset"))
        if not glb:
            skipped["no_glb"] += 1
            continue
        p = rec_pos(rec)
        kept.append(dict(
            glb=glb, p=[round(float(p[0]), 4), round(float(p[1]), 4), round(float(p[2]), 4)],
            yaw=rec_yaw(rec), tag=floor_tag(rec, owner), owner=owner, asset=asset,
            room=rec.get("room") or "", status=st or "placed",
        ))
    log["owners"][owner] = dict(
        file=filename, read=sum(1 for _ in iter_owner_records(data)),
        kept=len(kept), skipped=dict(skipped),
        assets=dict(Counter(r["asset"] for r in kept)),
    )
    return kept


def rook_core():
    """Cores, lifts, trees, slide towers, restroom shells — not owner-owned kits."""
    from tower_plan import CORES, LIFTS, TREES, TREES_W, CORE_ASSET, RESTROOMS_F3
    put = AP.put
    for cid, typ, (x0, x1, z0, z1) in CORES:
        a = CORE_ASSET.get(cid, "tt_stair_core_a" if typ == "A" else "tt_stair_core_b")
        yaw = 90 if (x1 - x0) > (z1 - z0) else 0
        cx = (x0 + x1) / 2 if cid != "ST+S1" else 61.0
        for y in (0, 6.1):
            put(a, cx, y, (z0 + z1) / 2, yaw, "f1" if y == 0 else "f2")
    for _, (x0, x1, z0, z1), face in LIFTS:
        for y, t in ((-.15, "f1"), (5.95, "f2"), (12.05, "f3")):
            put("tt_lift_core", (x0 + x1) / 2, y, (z0 + z1) / 2,
                {"+z": 0, "-z": 180, "+x": 90, "-x": -90}[face], t)
    for x, z in TREES:
        put("tt_tree_column", x, 0, z, tag="cols")
    for x, z in TREES_W:
        put("tt_tree_column_west", x, 12.2, z, tag="f3")
    put("tt_core_clad_aqn", -3.075, 0, 58.359, 180, "f1")   # r3: foyer-side S face of ST-AQN (wall plane Z 58.40), relief <= 0.08
    put("tt_slide_tower_t1", 22.5, 1.0, 53.5, 0, "f1")
    put("tt_slide_tower_t2", 22.5, 1.0, 59.5, 0, "f1")
    # Services world placements were never committed; keep Rook's restroom shells.
    for (x, z), y, t in [
        ((107.5, 4), 0, "f1"), ((107.5, 9), 0, "f1"),
        ((37, 70), 0, "f1"), ((37, 74.5), 0, "f1"),
        ((107.5, 70), 0, "f1"), ((107.5, 74.5), 0, "f1"),
        ((37, 70), 6.1, "f2"), ((37, 74.5), 6.1, "f2"),
        ((107.5, 70), 6.1, "f2"), ((107.5, 74.5), 6.1, "f2"),
    ]:
        put("tt_restroom", x, y, z, 0, t)
    for (x, z), yaw in RESTROOMS_F3:   # r1: 6-stall shells in the clear bays under the Courts F3 stands
        put("tt_restroom_6", x, 12.2, z, yaw, "f3")


def tag_rook(pl):
    out = []
    dropped = 0
    for p in pl:
        asset = asset_name(p["glb"])
        if is_owner_asset(asset):
            dropped += 1
            continue
        q = dict(p)
        q.setdefault("owner", "Rook")
        q.setdefault("asset", asset)
        q.setdefault("room", "")
        q.setdefault("status", "structure")
        out.append(q)
    return out, dropped


def already_has_entrance(pl, asset, pos, yaw, tol=0.15):
    for p in pl:
        if asset_name(p["glb"]) != asset:
            continue
        d = math.dist(p["p"], list(pos))
        if d <= tol and abs((p["yaw"] - yaw + 180) % 360 - 180) < 1:
            return True
    return False


def dedup_rook_vs_owners(rook, owners, tol=0.35):
    """If Rook and an owner place the same asset nearly on top of each other, drop Rook's."""
    idx = defaultdict(list)
    for i, p in enumerate(owners):
        idx[p["asset"]].append(i)
    keep, dropped = [], []
    for p in rook:
        hit = None
        for j in idx.get(p["asset"], ()):
            o = owners[j]
            if math.dist(p["p"], o["p"]) <= tol:
                hit = o
                break
        if hit:
            dropped.append(dict(asset=p["asset"], rook_p=p["p"], owner=hit["owner"], owner_p=hit["p"]))
        else:
            keep.append(p)
    return keep, dropped


# --- sanity -----------------------------------------------------------------

def load_local_aabb(path, cache):
    if path in cache:
        return cache[path]
    if not os.path.exists(path):
        cache[path] = None
        return None
    try:
        sc = trimesh.load(path, force="scene", process=False)
    except Exception:
        try:
            m = trimesh.load(path, force="mesh", process=False)
            if m is None or len(getattr(m, "vertices", [])) == 0:
                cache[path] = None
                return None
            cache[path] = m.bounds
            return cache[path]
        except Exception:
            cache[path] = None
            return None
    bounds = None
    geoms = sc.geometry if isinstance(sc.geometry, dict) else {str(i): g for i, g in enumerate(getattr(sc, "geometry", {}) or [])}
    # Prefer a scene-wide bounds but skip obvious collider-only meshes.
    try:
        # world bounds of visible geom
        mins, maxs = [], []
        if hasattr(sc, "graph") and hasattr(sc, "geometry"):
            for node_name in sc.graph.nodes_geometry:
                xform, geom_name = sc.graph[node_name]
                if "colonly" in str(node_name).lower() or "colonly" in str(geom_name).lower():
                    continue
                geom = sc.geometry[geom_name]
                if geom is None or len(getattr(geom, "vertices", [])) == 0:
                    continue
                v = trimesh.transform_points(geom.vertices, xform)
                mins.append(v.min(axis=0)); maxs.append(v.max(axis=0))
        if mins:
            bounds = np.vstack((np.min(mins, axis=0), np.max(maxs, axis=0)))
        else:
            b = sc.bounds
            bounds = np.asarray(b) if b is not None else None
    except Exception:
        b = getattr(sc, "bounds", None)
        bounds = np.asarray(b) if b is not None else None
    cache[path] = bounds
    return bounds


def world_aabb(local, p, yaw):
    (mn, mx) = local
    corners = np.array([
        [x, y, z] for x in (mn[0], mx[0]) for y in (mn[1], mx[1]) for z in (mn[2], mx[2])
    ])
    a = math.radians(yaw)
    c, s = math.cos(a), math.sin(a)
    # yaw about +Y (Godot)
    x = corners[:, 0] * c + corners[:, 2] * s
    z = -corners[:, 0] * s + corners[:, 2] * c
    y = corners[:, 1]
    pts = np.column_stack((x + p[0], y + p[1], z + p[2]))
    return pts.min(axis=0), pts.max(axis=0)


def overlap_metrics(a0, a1, b0, b1):
    ox = min(a1[0], b1[0]) - max(a0[0], b0[0])
    oy = min(a1[1], b1[1]) - max(a0[1], b0[1])
    oz = min(a1[2], b1[2]) - max(a0[2], b0[2])
    if ox <= 0 or oy <= 0 or oz <= 0:
        return None
    return ox, oy, oz, ox * oy * oz


def nominal_floor(p, tag):
    y = p[1]
    if tag in {"site", "ground"}:
        return None
    if tag == "roof":
        return None
    if -0.25 <= y <= 0.25:
        return 0.0
    if 5.90 <= y <= 6.35:
        return 6.1
    if 12.00 <= y <= 12.45:
        return 12.2
    return None


def sanity(pl, log):
    cache = {}
    boxes = []
    missing = []
    no_bounds = []
    for i, p in enumerate(pl):
        if not os.path.exists(p["glb"]):
            missing.append(p)
            continue
        local = load_local_aabb(p["glb"], cache)
        if local is None:
            no_bounds.append(p["asset"])
            continue
        a0, a1 = world_aabb(local, p["p"], p["yaw"])
        boxes.append((i, p, a0, a1, local))

    clashes_raw, clashes = [], []
    n = len(boxes)
    for ii in range(n):
        i, a, a0, a1, _ = boxes[ii]
        for jj in range(ii + 1, n):
            j, b, b0, b1, _ = boxes[jj]
            if a["owner"] == b["owner"]:
                continue
            m = overlap_metrics(a0, a1, b0, b1)
            if not m:
                continue
            ox, oy, oz, vol = m
            depth = min(ox, oy, oz)
            if depth <= 0.05:
                continue
            rec = dict(
                depth=round(float(depth), 4), volume=round(float(vol), 4),
                overlap_xyz=[round(float(ox), 4), round(float(oy), 4), round(float(oz), 4)],
                a=dict(owner=a["owner"], asset=a["asset"], p=a["p"], yaw=a["yaw"], room=a.get("room", "")),
                b=dict(owner=b["owner"], asset=b["asset"], p=b["p"], yaw=b["yaw"], room=b.get("room", "")),
            )
            clashes_raw.append(rec)
            if a["asset"] not in MEGA_STRUCTURE and b["asset"] not in MEGA_STRUCTURE:
                clashes.append(rec)
    clashes_raw.sort(key=lambda c: (-c["volume"], -c["depth"]))
    clashes.sort(key=lambda c: (-c["volume"], -c["depth"]))

    floaters, sunk = [], []
    for i, p, a0, a1, local in boxes:
        floor = nominal_floor(p["p"], p["tag"])
        if floor is None:
            continue
        gap = float(a0[1] - floor)
        rec = dict(
            owner=p["owner"], asset=p["asset"], p=p["p"], tag=p["tag"],
            room=p.get("room", ""), min_y=round(float(a0[1]), 4),
            floor=floor, gap=round(gap, 4),
            pivot_rel=round(float(a0[1] - p["p"][1]), 4),
        )
        if gap > 0.05:
            floaters.append(rec)
        elif gap < -0.05:
            sunk.append(rec)
    floaters.sort(key=lambda r: -r["gap"])
    sunk.sort(key=lambda r: r["gap"])

    log["sanity"] = dict(
        boxed=len(boxes), missing_glb=sorted({asset_name(p["glb"], p.get("asset")) for p in missing}),
        no_bounds=sorted(set(no_bounds)),
        clash_count_raw=len(clashes_raw),
        clash_count=len(clashes),
        clash_filter="Excluded whole-floor container meshes (slabs, walls, combined column kit, preview hull) whose AABBs enclose every room by design. Tree columns are kept: their 8.45 x 22.7 m canopy AABBs punch through every floor.",
        clashes_top20=clashes[:20],
        floating_count=len(floaters), floating_top=floaters[:40],
        sunk_count=len(sunk), sunk_top=sunk[:40],
    )
    return log["sanity"]


def print_sanity(s):
    print("sanity boxed", s["boxed"], "clashes", s["clash_count"],
          "(raw", s.get("clash_count_raw"), "before envelope filter)",
          "floating", s["floating_count"], "sunk", s["sunk_count"])
    print("missing GLBs:", s["missing_glb"] or "(none)")
    print("clash filter:", s.get("clash_filter"))
    print("--- top cross-owner clashes (depth>0.05 m, envelope meshes excluded) ---")
    for i, c in enumerate(s["clashes_top20"], 1):
        a, b = c["a"], c["b"]
        print(f"  {i:2d}. vol={c['volume']:.3f} depth={c['depth']:.3f} xyz={c['overlap_xyz']}")
        print(f"      {a['owner']}:{a['asset']} p={a['p']}  vs  {b['owner']}:{b['asset']} p={b['p']}")
    print("--- floating (mesh min_y > floor + 0.05, pivot near a floor) ---")
    for r in s["floating_top"][:20]:
        print(f"  {r['owner']}:{r['asset']} p={r['p']} min_y={r['min_y']} floor={r['floor']} gap={r['gap']}")
    print("--- sunk (mesh min_y < floor - 0.05, pivot near a floor) ---")
    for r in s["sunk_top"][:20]:
        print(f"  {r['owner']}:{r['asset']} p={r['p']} min_y={r['min_y']} floor={r['floor']} gap={r['gap']}")


# --- render -----------------------------------------------------------------

def render(pl, names=None):
    os.makedirs(OUT, exist_ok=True)
    tmp = "/tmp/tt_complex"
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp, exist_ok=True)
    open(os.path.join(tmp, "project.godot"), "w").write(
        'config_version=5\n[application]\nconfig/name="tt_complex"\n'
        "[rendering]\nrenderer/rendering_method=\"gl_compatibility\"\n"
        "anti_aliasing/quality/msaa_3d=2\n"
    )
    shutil.copy(os.path.join(HERE, "render_complex.gd"), os.path.join(tmp, "render_complex.gd"))
    want = set(names) if names else None
    shots = []
    for n, pos, look, fov, hide, amb, exp, omni in SHOTS:
        if want and n not in want and n.split("_", 1)[-1] not in want and n[:2] not in want:
            continue
        shots.append(dict(
            name=n, pos=list(pos), look=list(look), fov=fov, hide=list(hide),
            amb=amb, exposure=exp, omni=omni,
            out=os.path.join(OUT, n + ".png"),
        ))
    # Only the fields the renderer needs, to keep job.json small.
    slim = [dict(glb=p["glb"], p=p["p"], yaw=p["yaw"], tag=p["tag"]) for p in pl]
    json.dump(dict(placements=slim, shots=shots), open(os.path.join(tmp, "job.json"), "w"))
    cmd = [
        "xvfb-run", "-a", "-s", "-screen 0 1920x1080x24",
        "godot", "--rendering-driver", "opengl3", "--resolution", "1600x900",
        "--path", tmp, "-s", "render_complex.gd",
    ]
    print("render", len(shots), "shots:", " ".join(cmd))
    subprocess.run(cmd, check=False, timeout=3600)
    return [s["out"] for s in shots]


def assemble():
    log = dict(owners={}, excluded={}, notes=[])
    AP.PL.clear()
    AP.structure(); AP.roof(); AP.envelope(); AP.site(); rook_core(); AP.hull_mesh()
    rook, dropped_cat = tag_rook(list(AP.PL))
    log["notes"].append(
        "Rook interiors limited to cores, lifts, trees, slide towers and restroom shells; "
        "owner-owned kits (stands, court boxes, foyer, aquarium, climbing, cabanas/bar, playground) "
        "were not emitted from assemble_preview.interiors."
    )
    if dropped_cat:
        log["notes"].append(
            f"Dropped {dropped_cat} remaining Rook items in owner-owned categories "
            "(tt_roof_plant_cutout from roof(); Rooftop's copies are used)."
        )

    owner_pl, status_counts = [], Counter()
    for owner, fn in OWNER_FILES.items():
        recs = load_owner(owner, fn, log)
        for r in recs:
            status_counts[(owner, r["status"])] += 1
        owner_pl.extend(recs)
    log["active_status_choice"] = (
        "Included Active placement_status=valid (70) and proposed (468). "
        "Proposed records are committed, keepout-clear placed geometry; the status only "
        "marks them as temp-Active judgement rather than spec-dimensioned. "
        "The 4 withheld items (C1 desks, C6 benches) are in a separate list and were not placed."
    )
    log["services_excluded"] = (
        "temp-Services_placements.json is untracked/unverified (0 verified world "
        "placements, family rooms and fountains gated). Excluded. Rook still places "
        "the four committed plant-stack shells and the restroom placeholder shells."
    )

    # Leisure secondary entrances: add only if envelope didn't already place them.
    added_ent = []
    for asset, pos, yaw in LEISURE_ENTRANCES:
        if already_has_entrance(rook + owner_pl, asset, pos, yaw):
            log["notes"].append(
                f"Leisure entrance {asset} at {list(pos)} yaw {yaw} already placed by assemble_preview.envelope; not duplicated."
            )
        else:
            glb = os.path.join(MD, asset + ".glb")
            owner_pl.append(dict(glb=glb, p=list(pos), yaw=yaw, tag="facade",
                                 owner="Leisure", asset=asset, room="entrance", status="hand-added"))
            added_ent.append(asset)
    if added_ent:
        log["notes"].append("Hand-added Leisure entrances: " + ", ".join(added_ent))

    rook, prox = dedup_rook_vs_owners(rook, owner_pl)
    log["proximity_dedup_dropped"] = prox
    if prox:
        log["notes"].append(f"Proximity-dedup dropped {len(prox)} remaining Rook copies sitting on owner instances.")

    pl = rook + owner_pl
    # counts
    by_owner = Counter(p["owner"] for p in pl)
    missing = sorted({asset_name(p["glb"], p.get("asset")) for p in pl if not os.path.exists(p["glb"])})
    log["total"] = len(pl)
    log["by_owner"] = dict(by_owner)
    log["missing_glb"] = missing
    log["rook_structure"] = by_owner.get("Rook", 0)
    return pl, log


def main():
    global OUT
    if "--out" in sys.argv: OUT = sys.argv[sys.argv.index("--out") + 1]   # r2: e.g. --out /workspace/renders/tennis_tower/complex_tour_r2
    os.makedirs(OUT, exist_ok=True)
    pl, log = assemble()
    print("placements", log["total"], "by owner", log["by_owner"])
    print("missing GLBs:", log["missing_glb"] or "(none)")
    for n in log["notes"]:
        print("note:", n)
    print("Active policy:", log["active_status_choice"])
    print("Services:", log["services_excluded"])
    for owner, info in log["owners"].items():
        print(f"  {owner}: kept {info['kept']} of {info['read']} skipped={info['skipped']}")

    json.dump([dict(glb=p["glb"], p=p["p"], yaw=p["yaw"], tag=p["tag"],
                    owner=p["owner"], asset=p["asset"], room=p.get("room", "")) for p in pl],
              open(os.path.join(OUT, "placements.json"), "w"))

    if "--no-sanity" not in sys.argv:
        print("running sanity (AABB load)...")
        s = sanity(pl, log)
        print_sanity(s)
        json.dump(log, open(os.path.join(OUT, "integrate_report.json"), "w"), indent=2)
    else:
        json.dump(log, open(os.path.join(OUT, "integrate_report.json"), "w"), indent=2)

    if "--sanity-only" in sys.argv or "--no-render" in sys.argv:
        return
    names = None
    if "--shots" in sys.argv:
        i = sys.argv.index("--shots")
        names = [x.strip() for x in sys.argv[i + 1].split(",") if x.strip()]
    render(pl, names)


if __name__ == "__main__":
    main()
