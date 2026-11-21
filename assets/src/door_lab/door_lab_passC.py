"""Rook door_lab pass C runner (Vance REALISM_SPEC section 9 re-check, 2026-11-20): builds the 5 variants of each door-lab asset,
exports them, runs the clip / motion-sweep / flush / clear-opening / tri-budget QA and renders the closed + open views and a variant
contact sheet.
  Exports: assets/glb/door_lab/<asset>/v1..v5.glb; V1 (placed) also to godot/assets/models/door_lab/door_lab_<asset>.glb.
  QA json: assets/src/door_lab/passC_qa.json     Renders: /workspace/renders/doorlab_passC/
Variants:
  bulkhead_hatch   V1 RH 150 mm coaming (placed) | V2 LH coaming (X-mirror) | V3 RH 300 mm marine coaming | V4 LH 300 mm coaming | V5 RH coaming, 6 back ribs + kick plate
  biparting_slide  V1 access panel shown swung up (placed) | V2 panel closed (20 mm slot) | V3 no panel (service area) | V4 = V1 handed | V5 = V2 handed
  floor_hatch      V1 RH stay, 0.45 well (placed) | V2 LH stay (X-mirror) | V3 RH 0.75 step-down well | V4 LH 0.75 well | V5 RH 0.30 shallow well
Run: python3 assets/src/door_lab/door_lab_passC.py [--no-render] [--only bulkhead_hatch,biparting_slide,floor_hatch]"""
import os, sys, json, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from door_lab_lib import *
import bulkhead_hatch as bh, biparting_slide as bs, floor_hatch as fh

GLB_DIR = os.path.join(ROOT, "assets/glb/door_lab"); RENDER = "/workspace/renders/doorlab_passC"
QA_JSON = os.path.join(HERE, "passC_qa.json"); BUDGET = 6000

def V(a, b):
    a, b = np.radians(a), np.radians(b)
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]); Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
    return Rx @ Ry
APPROACH = V(180 + 32, 14); BACK = V(32, 18); DOWN = V(28, 38); DOWN_OPEN = V(150, 30)

# ---------------------------------------------------------------- variant builders (each returns a finalized rig + the deltas mirror flag)
def _bh(prm, mir):
    r = bh.build(prm); r.recenter()
    if mir: r = mirror_rig(r)
    return r, mir
def _bs(panel, hand):
    r = bs.build(panel); bs.finalize(r)
    return (bs.swap_lr(r) if hand else r), False
def _fh(prm, mir):
    r = fh.build(prm); fh.finalize(r)
    if mir: m = mirror_rig(r); m.meta = dict(r.meta); r = m
    return r, mir

VARIANTS = {
    "bulkhead_hatch": [("v1", "RH 150 mm coaming (placed)", lambda: _bh({}, False)), ("v2", "LH 150 mm coaming", lambda: _bh({}, True)),
                       ("v3", "RH 300 mm marine coaming", lambda: _bh(dict(sill=.30), False)), ("v4", "LH 300 mm marine coaming", lambda: _bh(dict(sill=.30), True)),
                       ("v5", "RH coaming, 6 back ribs + kick plate", lambda: _bh(dict(ribs=6, kick=True), False))],
    "biparting_slide": [("v1", "access panel shown swung up (placed)", lambda: _bs(2, False)), ("v2", "access panel closed (20 mm carriage slot)", lambda: _bs(1, False)),
                        ("v3", "no panel - service area, track exposed", lambda: _bs(0, False)), ("v4", "V1 handed (release + solenoid on the right)", lambda: _bs(2, True)),
                        ("v5", "V2 handed", lambda: _bs(1, True))],
    "floor_hatch": [("v1", "RH stay, 0.45 m well (placed)", lambda: _fh({}, False)), ("v2", "LH stay, 0.45 m well", lambda: _fh({}, True)),
                    ("v3", "RH stay, 0.75 m step-down well", lambda: _fh(dict(well=.75), False)), ("v4", "LH stay, 0.75 m well", lambda: _fh(dict(well=.75), True)),
                    ("v5", "RH stay, 0.30 m shallow well", lambda: _fh(dict(well=.30), False))],
}

def poses(asset, r, mir):
    if asset == "bulkhead_hatch":
        D = lambda **k: bh.deltas(r, mirror=mir, **k)
        return {"closed_dogged": D(f_open=0, f_dog=1), "closed_seal_inflated": D(f_open=0, f_dog=1, f_seal=1), "undogged_rams_out": D(f_open=0, f_dog=0, f_ram=1),
                "equalize_open_110kPa": D(f_open=0, f_dog=1, f_eq=1, kpa=110), "open_100deg": D(f_open=1, f_dog=0)}
    if asset == "biparting_slide":
        D = lambda **k: bs.deltas(r, **k)
        out = {"closed_locked": D(f=0, f_lock=1), "closed": D(f=0), "half": D(f=.5), "open_hex_released": D(f=1, f_hex=1)}
        if "slide_AccessPanel" in r.N: out["closed_panel_shut"] = D(f=0, f_panel=0); out["closed_panel_open"] = D(f=0, f_panel=1)
        return out
    D = lambda **k: fh.deltas(r, mirror=mir, **k)
    return {"closed_dogged": D(f_open=0, f_dog=1), "closed_seal_inflated": D(f_open=0, f_dog=1, f_seal=1), "undogged_lever_up": D(f_open=0, f_dog=0, f_lever=1),
            "open_52deg": D(f_open=.5, f_dog=0), "open_104deg": D(f_open=104/105, f_dog=0), "open_105deg": D(f_open=1, f_dog=0)}

def _vis(r): return [n for n in r.order if r.N[n]["mesh"] and "colonly" not in n]
def _desc(r, root):
    out, st = [], [root]
    while st:
        n = st.pop()
        for c in r.children(n): out.append(c); st.append(c)
    return out

def sweeps(asset, r, mir):
    """max penetration of moving parts into fixed parts along each motion (n steps)."""
    res = {}; vis = set(_vis(r))
    if asset == "bulkhead_hatch":
        mov = [n for n in _desc(r, "leaf") if n in vis]; fix = [n for n in vis if r.N[n]["parent"] is None and not n.startswith("bulkhead_Damper")]
        w = (0.0, None, None, None)
        for fd in np.linspace(0, 1, 6):
            P = r.world_parts(bh.deltas(r, 0, fd, mirror=mir)); d = penetration({k: P[k] for k in mov}, {k: P[k] for k in fix}, n_samp=120)
            if d[0] >= w[0]: w = (d[0], d[1], d[2], round(float(fd), 2))
        res["dogs_throw"] = w; w = (0.0, None, None, None); w2 = (0.0, None, None, None)
        for fo in np.linspace(0, 1, 21):
            P = r.world_parts(bh.deltas(r, fo, 0, mirror=mir))
            d = penetration({k: P[k] for k in mov if k != "bulkhead_DamperRod"}, {k: P[k] for k in fix}, n_samp=120)
            d2 = penetration({k: P[k] for k in ("bulkhead_Damper_body", "bulkhead_DamperRod")},
                             {k: P[k] for k in fix + [m for m in mov if m not in ("bulkhead_DamperRod", "bulkhead_leaf_damper_mount")] if k != "bulkhead_damper_mount"}, n_samp=120)
            if d[0] >= w[0]: w = (d[0], d[1], d[2], round(100*float(fo), 1))
            if d2[0] >= w2[0]: w2 = (d2[0], d2[1], d2[2], round(100*float(fo), 1))
        res["leaf_swing_0_100deg"] = w; res["damper_vs_all"] = w2
    elif asset == "biparting_slide":
        mov = [n for n in _desc(r, "leaf_L") + _desc(r, "leaf_R") if n in vis]; fix = [n for n in vis if r.N[n]["parent"] is None]
        w = (0.0, None, None, None)
        for f in np.linspace(0, 1, 11):
            P = r.world_parts(bs.deltas(r, f)); d = penetration({k: P[k] for k in mov}, {k: P[k] for k in fix}, n_samp=100)
            if d[0] >= w[0]: w = (d[0], d[1], d[2], round(float(f), 2))
        res["leaves_travel_0_1000mm"] = w
        if "slide_AccessPanel" in r.N:
            w = (0.0, None, None, None)
            for fp in np.linspace(0, 1, 6):
                P = r.world_parts(bs.deltas(r, 0, f_panel=fp)); d = penetration({"slide_AccessPanel": P["slide_AccessPanel"]}, {k: P[k] for k in vis if k != "slide_AccessPanel"}, n_samp=200)
                if d[0] >= w[0]: w = (d[0], d[1], d[2], round(float(fp), 2))
            res["access_panel_0_90deg"] = w
        P = r.world_parts(bs.deltas(r, 0, f_lock=1)); d = penetration({"slide_SolenoidBolt": P["slide_SolenoidBolt"]}, {k: P[k] for k in vis if k not in ("slide_SolenoidBolt", "slide_Solenoid")}, n_samp=200)
        res["solenoid_bolt_thrown"] = (d[0], d[1], d[2], 1.0)
    else:
        stay = ["hatch_stay_arm", "hatch_stay_slider", "hatch_stay_detent_plunger", "hatch_stay_detent_knob"]
        lf = [n for n in _desc(r, "hatch_leaf") if n in vis and n not in stay]
        fix = [n for n in vis if r.N[n]["parent"] is None and n not in stay]
        w = (0.0, None, None, None)
        for fo in np.linspace(0, 1, 22):
            P = r.world_parts(fh.deltas(r, fo, 0, mirror=mir))
            d = penetration({k: P[k] for k in lf}, {k: P[k] for k in fix}, n_samp=150)
            if d[0] >= w[0]: w = (d[0], d[1], d[2], round(105*float(fo), 1))
        res["leaf_swing_0_105deg"] = w
        w = (0.0, None, None, None); w2 = (0.0, None, None, None)
        for deg in list(np.arange(0, 105.001, 1.0)):
            P = r.world_parts(fh.deltas(r, deg/105, 0, mirror=mir))
            d = penetration({k: P[k] for k in stay}, {k: P[k] for k in vis if k not in stay}, n_samp=150)
            d2 = penetration({k: P[k] for k in ("hatch_stay_arm",)}, {k: P[k] for k in ("hatch_stay_slider", "hatch_stay_detent_plunger", "hatch_stay_detent_knob")}, n_samp=150)
            d3 = penetration({k: P[k] for k in ("hatch_stay_slider",)}, {k: P[k] for k in ("hatch_stay_detent_plunger", "hatch_stay_detent_knob")}, n_samp=150)
            for dd in (d, d2, d3):
                if dd[0] >= w[0]: w = (dd[0], dd[1], dd[2], round(float(deg), 1))
        res["stay_arm_slider_detent_1deg"] = w
        for deg in np.arange(100, 105.001, .1):     # Godot-style table interpolation through the detent pop-up
            P = r.world_parts(fh.deltas(r, deg/105, 0, mirror=mir, exact=False))
            d = penetration({k: P[k] for k in ("hatch_stay_slider",)}, {k: P[k] for k in ("hatch_stay_detent_plunger", "hatch_stay_detent_knob", "hatch_frame", "hatch_stay_detent_housing")}, n_samp=150)
            if d[0] >= w2[0]: w2 = (d[0], d[1], d[2], round(float(deg), 1))
        res["detent_table_interp_100_105_0p1deg"] = w2
        w = (0.0, None, None, None)
        for fd in np.linspace(0, 1, 6):
            P = r.world_parts(fh.deltas(r, 0, fd, mirror=mir)); d = penetration({k: P[k] for k in lf}, {k: P[k] for k in fix}, n_samp=120)
            if d[0] >= w[0]: w = (d[0], d[1], d[2], round(float(fd), 2))
        res["dogs_throw"] = w
    return {k: dict(depth_m=round(float(v[0]), 4), parts=[v[1], v[2]], at=v[3]) for k, v in res.items()}

def _rays(meshes, o, dirs):
    M = trimesh.util.concatenate(meshes); out = []
    for d in dirs:
        loc, _, _ = M.ray.intersects_location([o], [d]); dist = np.linalg.norm(loc - o, axis=1) if len(loc) else np.array([np.inf])
        out.append(float(dist.min()))
    return out

def hatch_checks(r, mir):
    """flush (leaf top vs floor plane), liner clear opening, hardware inside the 0.90 x 0.90 clear prism (closed + open)."""
    fy = r.meta["floor_y"]; P0 = r.world_parts(fh.deltas(r, 0, 1, mirror=mir))
    frame_top = float(P0["hatch_frame"][1].vertices[:, 1].max()); leaf_top = float(P0["hatch_leaf_shell"][1].vertices[:, 1].max())
    out = dict(floor_y=round(fy, 4), frame_flange_top=round(frame_top, 4), leaf_top=round(leaf_top, 4), flush_mm=round(1000*(leaf_top - frame_top), 2),
               flush_ok=abs(leaf_top - frame_top) <= .002)
    fixed = [P0[n][1] for n in P0 if r.N[n]["parent"] is None and not n.startswith("hatch_stay")]
    liner = {}
    for lab, dy in (("throat_-0.15", -.15), ("well_-0.30", -.30)):
        if fy + dy < .02: continue
        o = np.array([0, fy + dy, 0.0]); d = _rays(fixed, o, [(1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)])
        liner[lab] = dict(x=round(d[0] + d[1], 4), z=round(d[2] + d[3], 4))
    out["liner_clear_xz"] = liner
    out["liner_ok"] = all(v["x"] >= .8995 and v["z"] >= .8995 for v in liner.values())
    out["column_sweep"] = column_sweep(r, mir)
    out["lock_gear_gaps"] = _LG_CACHE.get(r.meta.get("_vid")) or lock_gear_gaps(r, mir)
    out["dog_retraction"] = dog_phase_check()
    return out

STAY_MECH = ("hatch_stay_arm", "hatch_stay_leaf_lug", "hatch_stay_slider", "hatch_stay_detent_plunger", "hatch_stay_detent_knob", "hatch_HingeTube", "hatch_TorsionAnchor_leaf")
def _col_clear(S, fy, ylo):
    """signed horizontal clearance (m) of points to the 0.90 x 0.90 clear column (|x|, |z| < 0.45, ylo < y < floor + 2 m); < 0 = inside."""
    ax, az = np.abs(S[:, 0]), np.abs(S[:, 2]); dx, dz = np.maximum(ax - .45, 0), np.maximum(az - .45, 0)
    c = np.where((dx > 0) | (dz > 0), np.hypot(dx, dz), -np.minimum(.45 - ax, .45 - az))
    vert = (S[:, 1] > ylo) & (S[:, 1] < fy + 2.0)
    return np.where(vert, c, np.inf)
def column_sweep(r, mir, step=0.5):
    """Vance: no fixed hardware in the column; no counterbalance / stay / damper part in it at any angle 0-105 deg (0.5 deg steps)."""
    fy = r.meta["floor_y"]; P0 = r.world_parts(fh.deltas(r, 0, 1, mirror=mir)); ylo = float(P0["hatch_frame"][1].vertices[:, 1].min()) + .012 + E + .001   # well-floor top
    lfd = set(_desc(r, "hatch_leaf"))
    cls = {}
    for n in P0:
        cls[n] = "boundary" if n == "hatch_frame" else ("mechanism" if n in STAY_MECH else ("leaf_body" if n in lfd else "fixed"))
    samp = {n: np.vstack([m.vertices, trimesh.sample.sample_surface(m, 4000, seed=3)[0]]) for n, (_, m) in r.world_parts().items()}
    Wc = r.pose(); loc = {n: (np.linalg.inv(Wc[n]) @ np.c_[samp[n], np.ones(len(samp[n]))].T).T[:, :3] for n in samp}
    best = {k: (np.inf, None, None) for k in ("fixed", "mechanism", "boundary")}; leaf_in = []; per5 = []; leaf105 = (np.inf, None)
    for deg in np.arange(0, OPEN + 1e-9, step):
        Wp = r.pose(fh.deltas(r, deg/OPEN, 0 if deg > 0 else 1, mirror=mir)); row = {}
        for n, L in loc.items():
            S = (Wp[n] @ np.c_[L, np.ones(len(L))].T).T[:, :3]; c = float(_col_clear(S, fy, ylo).min()); k = cls[n]
            if k == "leaf_body":
                if c < 0: leaf_in.append(deg)
                if abs(deg - OPEN) < 1e-9 and c < leaf105[0]: leaf105 = (c, n)
                continue
            if c < best[k][0]: best[k] = (c, n, float(deg))
            row[k] = min(row.get(k, np.inf), c)
        if abs(deg/5 - round(deg/5)) < 1e-9: per5.append(dict(deg=float(deg), **{k: round(1000*v, 2) for k, v in row.items()}))
    rnd = lambda t: dict(min_clearance_mm=round(1000*t[0], 2), part=t[1], at_deg=t[2])
    return dict(step_deg=step, column="|x|,|z| < 0.450 m, well floor top .. floor + 2.0 m", fixed=rnd(best["fixed"]), mechanism=rnd(best["mechanism"]),
                liner_boundary=rnd(best["boundary"]), leaf_body_at_105=dict(min_clearance_mm=round(1000*leaf105[0], 2), part=leaf105[1]),
                leaf_body_inside_deg=[float(min(leaf_in)), float(max(leaf_in))] if leaf_in else None, per_5deg=per5,
                ok=bool(best["fixed"][0] > 0 and best["mechanism"][0] > 0 and best["boundary"][0] > -5e-4 and leaf105[0] > 0))
OPEN = fh.OPEN_DEG
LOCK_GEAR = ["hatch_LockWheel"] + [f"hatch_Dog_{i:02d}" for i in range(1, 5)] + [f"hatch_Linkage_{i:02d}" for i in range(1, 5)] + ["hatch_Handle", "hatch_OverrideOrange_Handwheel", "hatch_OverrideOrange_Lever"]
LG_TARGETS = ("liner", "frame flange", "keeper")
_LG = {}
def _lg_measure(S, near=.02):
    """-> {target: (gap_m, )} for one posed sample cloud. Exact point-triangle distance on KD-prefiltered candidates, negative when inside."""
    c0 = _LG; d0, _ = c0["tree"].query(S, distance_upper_bound=near)
    cand = S[d0 < near]; full = not len(cand)
    if full: dc, _ = c0["coarse"].query(S); cand = S[np.argsort(dc)[:64]]   # nothing within 20 mm: exact distance for the 64 nearest samples
    out = {}; lo, hi = cand.min(0) - near, cand.max(0) + near
    for ci, (cn, c) in enumerate(c0["comps"]):
        fm = np.ones(len(c.faces), bool) if full else np.all((c.vertices[c.faces] >= lo).any(1) & (c.vertices[c.faces] <= hi).any(1), axis=1)
        if not fm.any(): continue
        sub = trimesh.Trimesh(c.vertices, c.faces[fm], process=False)
        cp, dist, _ = trimesh.proximity.closest_point(sub, cand)
        g = np.where(c0["ins"][ci](cand), -dist, dist)
        if cn == "hatch_Keeper": lab = np.full(len(g), "keeper", object)
        else: lab = np.where(cp[:, 1] > c0["fy"] - fh.FLT - .001, "frame flange", "liner")
        for t in LG_TARGETS:
            m = lab == t
            if m.any():
                k = int(np.argmin(np.where(m, g, np.inf)))
                if t not in out or g[k] < out[t]: out[t] = float(g[k])
    return out
def _lg_step(deg):
    c0 = _LG; f_dog = 1.0 if deg < 0 else 0.0
    Wp = c0["r"].pose(fh.deltas(c0["r"], max(deg, 0)/OPEN, f_dog, mirror=c0["mir"]))
    return deg, {n: _lg_measure((Wp[n] @ np.c_[c0["loc"][n], np.ones(len(c0["loc"][n]))].T).T[:, :3]) for n in c0["parts"]}
def lock_gear_gaps(r, mir, step=0.5):
    """Vance: lock gear (lock wheel, 4 dogs, 4 linkages, handle, OverrideOrange handwheel + lever) vs liner / frame flange / keepers over the
    swing 0-105 deg in 0.5 deg steps with the dogs retracted (the phases retract them before the lurch). Gap = exact point-triangle
    distance from every vertex + 6000 surface samples of the moving part to the watertight fixed meshes, negative when inside; candidates
    within 20 mm prefiltered by a KD tree over ~400k samples/m2 of the fixed surfaces. Targets with no sample within 20 mm read as >= 20.
    Also reports the closed, dogs-THROWN state (dogs in the keeper pockets) separately."""
    from scipy.spatial import cKDTree
    fy = r.meta["floor_y"]; P0 = r.world_parts(fh.deltas(r, 0, 0, mirror=mir)); comps = []
    for n in ("hatch_frame", "hatch_Keeper"):
        for c in P0[n][1].split(only_watertight=False): comps.append((n, c))
    def inside_fn(c):            # convex pieces (liner plates, keepers): half-space test on the hull; the boolean frame body: ray containment
        h = c.convex_hull
        if abs(h.volume - abs(c.volume)) <= 1e-3*h.volume:
            A = h.face_normals; b = np.einsum("ij,ij->i", A, h.triangles[:, 0]); return lambda P: np.all(P @ A.T - b <= 1e-7, axis=1)
        return c.contains
    FS = np.vstack([np.vstack([c.vertices, trimesh.sample.sample_surface(c, max(2000, int(c.area*400000)), seed=5)[0]]) for _, c in comps])
    Wc = r.pose(); Pc = r.world_parts(); loc = {}
    for n in LOCK_GEAR:
        m = Pc[n][1]; S = np.vstack([m.vertices, trimesh.sample.sample_surface(m, 6000, seed=6)[0]])
        loc[n] = (np.linalg.inv(Wc[n]) @ np.c_[S, np.ones(len(S))].T).T[:, :3]
    _LG.clear(); _LG.update(r=r, mir=mir, fy=fy, comps=comps, ins=[inside_fn(c) for _, c in comps], tree=cKDTree(FS), coarse=cKDTree(FS[::50]), loc=loc, parts=LOCK_GEAR)
    angs = [float(a) for a in np.arange(0, OPEN + 1e-9, step)]
    rows = [_lg_step(a) for a in angs + [-1.0]]
    def agg(rows_, parts):
        res = {}
        for n in parts:
            e = dict(min_gap_mm=np.inf, at_deg=None, against=None, by_target={})
            for t in LG_TARGETS:
                best = min(((m[n][t], d) for d, m in rows_ if t in m[n]), default=None)
                e["by_target"][t] = dict(min_gap_mm=round(1000*best[0], 2), at_deg=max(best[1], 0.0)) if best and best[0] < .02 else dict(min_gap_mm=">=20", at_deg=None)
                if best and 1000*best[0] < e["min_gap_mm"]: e.update(min_gap_mm=round(1000*best[0], 2), at_deg=max(best[1], 0.0), against=t)
            res[n] = e
        return res
    res = agg([x for x in rows if x[0] >= 0], LOCK_GEAR)
    thrown = agg([x for x in rows if x[0] < 0], [n for n in LOCK_GEAR if n.startswith(("hatch_Dog", "hatch_Linkage", "hatch_LockWheel"))])
    worst = min(res, key=lambda n: res[n]["min_gap_mm"])
    dk = [res[n]["by_target"]["keeper"] for n in res if n.startswith("hatch_Dog")]
    dk_min = min((e["min_gap_mm"] for e in dk if e["min_gap_mm"] != ">=20"), default=">=20")
    return dict(step_deg=step, n_steps=len(angs), swing_dogs_retracted=res, closed_dogs_thrown=thrown,
                min_gap_mm=res[worst]["min_gap_mm"], min_part=worst, min_at_deg=res[worst]["at_deg"], min_against=res[worst]["against"],
                retracted_dogs_vs_keepers_min_mm=dk_min,
                ok=bool(all(e["min_gap_mm"] >= 0 for e in res.values())), all_ge_3mm=bool(all(e["min_gap_mm"] >= 3 for e in res.values())))

_LG_CACHE = {}
def _lg_variant(vid):   # fresh-interpreter worker (spawn): one floor-hatch variant's lock-gear sweep
    r, mir = dict((v, fn) for v, _, fn in VARIANTS["floor_hatch"])[vid](); return vid, lock_gear_gaps(r, mir)
def precompute_lock_gear():
    import multiprocessing as mp
    vids = [v for v, _, _ in VARIANTS["floor_hatch"]]
    with mp.get_context("spawn").Pool(len(vids)) as pool: _LG_CACHE.update(dict(pool.map(_lg_variant, vids)))

def dog_phase_check():
    """Vance: dogs fully retracted before the leaf lifts. Reads the door profile (godot/resources/door_lab/floorhatch.json) and
    mech_door.gd: open = dogs phase must END at or before the first phase that moves q off 0; close = dogs phase must START at or
    after q is back at 0 (phase scaling in mech_door is monotonic, so the order holds after mech_phase_scale / travel_time_scale)."""
    import re
    root = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    prof = json.load(open(os.path.join(root, "godot/resources/door_lab/floorhatch.json")))
    md = open(os.path.join(root, "godot/scripts/door_lab/mech_door.gd")).read()
    op, cl = prof["open_phases"], prof["close_phases"]
    dog_o = next(p for p in op if p["name"] == "dogs"); move_o = next(p for p in op if p.get("p1", p["p0"]) != p["p0"])
    dog_c = next(p for p in cl if p["name"] == "dogs"); seat_c = max((p for p in cl if p.get("p1", p["p0"]) != p["p0"]), key=lambda p: p["t1"])
    pre_o = [p["name"] for p in op if dog_o["t1"] <= p["t0"] < move_o["t0"]]
    m = re.search(r"func _dog_throw_u\(.*?\n(.*?)\n\n", md, re.S); body = m.group(1) if m else ""
    src_ok = "1.0 - local_t" in body and '_phase_u(["dogs"])' in body
    forced = re.search(r"if forced:\s*\n\s*return 0.0 if travel_u > ([0-9.]+) else 1.0", body)
    return dict(open_dogs_span_s=[dog_o["t0"], dog_o["t1"]], open_first_motion_phase=move_o["name"], open_first_motion_t0_s=move_o["t0"],
                open_between=pre_o, open_margin_s=round(move_o["t0"] - dog_o["t1"], 4),
                close_seated_phase=seat_c["name"], close_seated_t1_s=seat_c["t1"], close_dogs_span_s=[dog_c["t0"], dog_c["t1"]],
                close_margin_s=round(dog_c["t0"] - seat_c["t1"], 4), mech_phase_scale=prof.get("mech_phase_scale"),
                mech_door_dog_throw_open_is_1_minus_dogs_phase=bool(src_ok),
                forced_pose_threshold_travel_u=float(forced.group(1)) if forced else None,
                ok=bool(dog_o["t1"] <= move_o["t0"] and dog_c["t0"] >= seat_c["t1"] and src_ok))

def main(only=None, do_render=True):
    rep = json.load(open(QA_JSON)) if os.path.exists(QA_JSON) and only else {}
    for asset, vars_ in VARIANTS.items():
        if only and asset not in only: continue
        rep[asset] = {}; thumbs = []
        if asset == "floor_hatch" and not _LG_CACHE: precompute_lock_gear()   # 5 variants x 211 poses in parallel
        for vid, label, fn in vars_:
            t0 = time.time(); r, mir = fn()
            gp = os.path.join(GLB_DIR, asset, f"{vid}.glb"); tris = r.export(gp)
            if vid == "v1": r.export(os.path.join(OUT_GLB, f"door_lab_{asset}.glb"))
            e = dict(label=label, glb=os.path.relpath(gp, ROOT), tris_visual=tris["visual"], tris_collider=tris["collider"], under_budget=tris["visual"] < BUDGET,
                     mirror_deltas=mir, nodes=r.tree())
            if asset == "floor_hatch": e["floor_y"] = round(r.meta["floor_y"], 4)
            e["clip"] = {}
            for lab, d in poses(asset, r, mir).items():
                s = summarize(clip(r, d, n_samp=250))
                e["clip"][lab] = dict(worst_overlap=s["worst_overlap"], bad_overlaps=[list(map(str, o)) for o in s["bad_overlaps"]],
                                      coplanar=[list(map(str, o)) for o in s["coplanar"]], open=[str(o) for o in s["open"]])
            e["sweeps"] = sweeps(asset, r, mir)
            if asset == "floor_hatch": r.meta["_vid"] = vid; e["hatch"] = hatch_checks(r, mir)
            e["pass"] = (e["under_budget"] and all(not c["bad_overlaps"] and not c["coplanar"] and not c["open"] for c in e["clip"].values())
                         and all(sw["depth_m"] <= .010 for sw in e["sweeps"].values()) and (asset != "floor_hatch" or (e["hatch"]["flush_ok"] and e["hatch"]["liner_ok"] and e["hatch"]["column_sweep"]["ok"] and e["hatch"]["lock_gear_gaps"]["ok"] and e["hatch"]["dog_retraction"]["ok"])))
            rep[asset][vid] = e
            print(asset, vid, label, "tris", tris["visual"], "pass", e["pass"], "sweeps", {k: v["depth_m"] for k, v in e["sweeps"].items()},
                  f"{time.time() - t0:.0f}s", flush=True)
            if do_render:
                ps = poses(asset, r, mir)
                if asset == "bulkhead_hatch":
                    closed, opened = ps["closed_dogged"], ps["open_100deg"]
                    tp = render(r, closed, os.path.join(RENDER, f"{asset}_{vid}_closed_approach.png"), R=APPROACH, size=640)
                    if vid == "v1":
                        render(r, closed, os.path.join(RENDER, f"{asset}_v1_closed_back.png"), R=BACK, size=900)
                        render(r, closed, os.path.join(RENDER, f"{asset}_v1_closed_approach_hi.png"), R=APPROACH, size=900)
                        render(r, opened, os.path.join(RENDER, f"{asset}_v1_open.png"), R=BACK, size=900)
                        render(r, opened, os.path.join(RENDER, f"{asset}_v1_open_approach.png"), R=APPROACH, size=900)
                elif asset == "biparting_slide":
                    closed, opened = ps["closed_locked"], ps["open_hex_released"]
                    tp = render(r, closed, os.path.join(RENDER, f"{asset}_{vid}_closed_approach.png"), R=APPROACH, size=640)
                    if vid == "v1":
                        render(r, closed, os.path.join(RENDER, f"{asset}_v1_closed_approach_hi.png"), R=APPROACH, size=900)
                        render(r, opened, os.path.join(RENDER, f"{asset}_v1_open.png"), R=APPROACH, size=900)
                        render(r, closed, os.path.join(RENDER, f"{asset}_v1_closed_back.png"), R=BACK, size=900)
                else:
                    closed, opened = ps["closed_dogged"], ps["open_105deg"]
                    tp = render(r, closed, os.path.join(RENDER, f"{asset}_{vid}_closed.png"), R=DOWN, size=640)
                    if vid == "v1":
                        render(r, opened, os.path.join(RENDER, f"{asset}_v1_open.png"), R=DOWN, size=900)
                        render(r, opened, os.path.join(RENDER, f"{asset}_v1_open_side.png"), R=DOWN_OPEN, size=900)
                        render(r, closed, os.path.join(RENDER, f"{asset}_v1_closed_hi.png"), R=DOWN, size=900)
                        side_sweep(r, mir, os.path.join(RENDER, f"{asset}_v1_side_sweep.png"))
                        column_figure(r, mir, os.path.join(RENDER, f"{asset}_v1_column_sweep.png"))
                thumbs.append((vid, label, tp))
        if do_render: contact(asset, thumbs)
    json.dump(rep, open(QA_JSON, "w"), indent=1, default=str)
    if "floor_hatch" in rep: write_sweep_log(rep["floor_hatch"])
    return rep

SIDE = V(90, 0)
def side_sweep(r, mir, path, angs=(0, 30, 60, 90, 105)):
    """side elevation (from +X) of the hatch at several opening angles, one panel per angle, with the clear-column edges drawn in."""
    from PIL import Image, ImageDraw
    tmp = []
    for a in angs:
        tp = path.replace(".png", f"_{a:03d}.png"); render(r, fh.deltas(r, a/105, 0 if a else 1, mirror=mir), tp, R=SIDE, size=520); tmp.append((a, tp))
    ims = [Image.open(p).convert("RGB") for _, p in tmp]; h = max(i.height for i in ims); W = sum(i.width for i in ims) + 20*(len(ims) + 1)
    sheet = Image.new("RGB", (W, h + 60), (245, 245, 240)); d = ImageDraw.Draw(sheet); x = 20
    for (a, _), im in zip(tmp, ims):
        sheet.paste(im, (x, 45)); d.text((x, 12), f"{a} deg  (side elevation from +X)", fill=(20, 20, 20)); x += im.width + 20
    sheet.save(path)
    for _, p in tmp: os.remove(p)

def column_figure(r, mir, path, step=0.5):
    """plan (XZ) + side (YZ) of every counterbalance / stay / damper / fixed part over the whole 0-105 deg sweep, with the 0.90 column shaded."""
    fy = r.meta["floor_y"]; lfd = set(_desc(r, "hatch_leaf"))
    P0 = r.world_parts(); Wc = r.pose()
    samp = {n: np.vstack([m.vertices, trimesh.sample.sample_surface(m, 1500, seed=4)[0]]) for n, (_, m) in P0.items()}
    loc = {n: (np.linalg.inv(Wc[n]) @ np.c_[S, np.ones(len(S))].T).T[:, :3] for n, S in samp.items()}
    mech = {n for n in P0 if n in STAY_MECH}; leafb = {n for n in P0 if n in lfd and n not in mech}
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(15, 7.2))
    for ax in (a1, a2): ax.set_aspect("equal"); ax.grid(alpha=.25)
    a1.add_patch(plt.Rectangle((-.45, -.45), .9, .9, color=(.2, .7, .3), alpha=.18, label="0.90 x 0.90 clear column"))
    a2.axvspan(-.45, .45, color=(.2, .7, .3), alpha=.12)
    pts = {"mechanism": [], "fixed": []}
    for deg in np.arange(0, OPEN + 1e-9, step):
        Wp = r.pose(fh.deltas(r, deg/OPEN, 0 if deg else 1, mirror=mir))
        for n in mech | {k for k in P0 if r.N[k]["parent"] is None and k not in ("hatch_frame",)}:
            if deg > 0 and n not in mech and not n.startswith("hatch_stay"): continue
            S = (Wp[n] @ np.c_[loc[n], np.ones(len(loc[n]))].T).T[:, :3]
            pts["mechanism" if (n in mech or n.startswith("hatch_stay")) else "fixed"].append(S[::3])
        if abs(deg % 15) < 1e-9 or abs(deg - OPEN) < 1e-9:
            L = np.vstack([(Wp[n] @ np.c_[loc[n], np.ones(len(loc[n]))].T).T[:, :3] for n in leafb if n == "hatch_leaf_shell"])
            a2.scatter(L[:, 2], L[:, 1] - fy, s=.2, color=(.55, .55, .6), alpha=.25)
    F = np.vstack(pts["fixed"]); M = np.vstack(pts["mechanism"])
    a1.scatter(F[:, 0], F[:, 2], s=.3, color=(.25, .25, .3), label="fixed hardware (keepers, bearings, damper, torsion bar + frame anchor, detent housing)")
    a1.scatter(M[:, 0], M[:, 2], s=.3, color=(.85, .36, .15), label="moving mechanism, every 0.5 deg 0-105 (tube, leaf anchor, stay arm, lug, slider, detent)")
    a2.scatter(M[:, 2], M[:, 1] - fy, s=.3, color=(.85, .36, .15))
    cs = column_sweep(r, mir)
    a1.set_title(f"PLAN, 0-105 deg in 0.5 deg steps\nmin clearance to the column: mechanism {cs['mechanism']['min_clearance_mm']} mm, fixed {cs['fixed']['min_clearance_mm']} mm", fontsize=9)
    a1.set_xlabel("x (m)"); a1.set_ylabel("z (m), hinge at -z"); a1.legend(loc="center", fontsize=7)
    a2.set_title("SIDE (YZ): leaf every 15 deg (grey), mechanism envelope (orange)\nthe stay sits at x 0.4515-0.4805, outside the column in plan", fontsize=9)
    a2.set_xlabel("z (m)"); a2.set_ylabel("height above floor (m)")
    fig.tight_layout(); fig.savefig(path, dpi=110); plt.close(fig); return path

def write_sweep_log(fhrep):
    L = [f"Rook floor hatch column sweep + lock-gear gaps + dog retraction (door_lab_passC.py, {time.strftime('%Y-%m-%d %H:%M %Z')})",
         "Column: |x|,|z| < 0.450 m from the well-floor top to floor + 2.0 m. Clearance = horizontal distance to the column (negative = inside).",
         "fixed = every non-moving node except the frame/liner (liner faces = the column boundary); mechanism = hinge tube, leaf torsion anchor, stay arm, lug, slider, detent plunger/knob;",
         "leaf_body = leaf shell + leaf-borne lock gear (the lid itself; it covers the column when closed and swings through it by definition).",
         "lock gear: exact point-triangle gap from every vertex + 6000 surface samples per part; per-target '>=20' = no sample within 20 mm of that target (the overall min is exact).", ""]
    for vid, e in fhrep.items():
        cs = e["hatch"]["column_sweep"]
        L.append(f"[{vid}] {e['label']}  step {cs['step_deg']} deg  ok={cs['ok']}")
        L.append(f"  fixed      min {cs['fixed']['min_clearance_mm']} mm ({cs['fixed']['part']})")
        L.append(f"  mechanism  min {cs['mechanism']['min_clearance_mm']} mm ({cs['mechanism']['part']} at {cs['mechanism']['at_deg']} deg)")
        L.append(f"  liner      min {cs['liner_boundary']['min_clearance_mm']} mm (frame liner faces = boundary)")
        L.append(f"  leaf body at 105 deg  min {cs['leaf_body_at_105']['min_clearance_mm']} mm ({cs['leaf_body_at_105']['part']}); leaf body crosses the column {cs['leaf_body_inside_deg']} deg")
        L.append("  per 5 deg (mm): " + "  ".join(f"{int(p['deg'])}:{p.get('mechanism')}/{p.get('fixed')}" for p in cs["per_5deg"]) + "   (mechanism/fixed)")
        lg = e["hatch"]["lock_gear_gaps"]
        L.append(f"  LOCK GEAR vs liner / frame flange / keepers, swing 0-105 deg @ {lg['step_deg']} deg ({lg['n_steps']} poses), dogs retracted: ok={lg['ok']} all>=3mm={lg['all_ge_3mm']}  "
                 f"min {lg['min_gap_mm']} mm ({lg['min_part']} vs {lg['min_against']} at {lg['min_at_deg']} deg); retracted dogs vs keepers min {lg['retracted_dogs_vs_keepers_min_mm']} mm")
        for n, g in lg["swing_dogs_retracted"].items():
            bt = "  ".join(f"{t} {v['min_gap_mm']}" + (f"@{v['at_deg']}" if v["at_deg"] is not None else "") for t, v in g["by_target"].items())
            L.append(f"    {n:32s} min {g['min_gap_mm']:>8} mm at {g['at_deg']:>5} deg vs {g['against']:12s} | {bt}")
        L.append("  closed, dogs THROWN (in the keeper pockets, 0 deg; not part of the swing): " + "  ".join(f"{n.replace('hatch_', '')} {g['min_gap_mm']} ({g['against']})" for n, g in lg["closed_dogs_thrown"].items()))
        dr = e["hatch"]["dog_retraction"]
        L.append(f"  DOG RETRACTION (floorhatch.json + mech_door.gd): ok={dr['ok']}  open: dogs {dr['open_dogs_span_s']} s end {dr['open_margin_s']} s before '{dr['open_first_motion_phase']}' "
                 f"(t0 {dr['open_first_motion_t0_s']} s; between: {dr['open_between']}); close: '{dr['close_seated_phase']}' seats at {dr['close_seated_t1_s']} s, dogs start {dr['close_dogs_span_s'][0]} s "
                 f"(+{dr['close_margin_s']} s); profile times before mech_phase_scale {dr['mech_phase_scale']}")
        L.append(f"  sweeps: " + ", ".join(f"{k} {v['depth_m']*1000:.1f} mm" for k, v in e["sweeps"].items()) + f"; flush {e['hatch']['flush_mm']} mm; liner {e['hatch']['liner_clear_xz']}")
        L.append("")
    open(os.path.join(HERE, "floor_hatch_column_sweep.txt"), "w").write("\n".join(L))

def contact(asset, thumbs):
    from PIL import Image, ImageDraw
    ims = [Image.open(p).convert("RGB") for _, _, p in thumbs]; h = max(i.height for i in ims); W = sum(int(i.width*h/i.height) for i in ims) + 20*(len(ims) + 1)
    sheet = Image.new("RGB", (W, h + 70), (245, 245, 240)); d = ImageDraw.Draw(sheet); x = 20
    for (vid, label, _), im in zip(thumbs, ims):
        im = im.resize((int(im.width*h/im.height), h)); sheet.paste(im, (x, 50)); d.text((x, 12), f"{vid.upper()}  {label}", fill=(20, 20, 20)); x += im.width + 20
    sheet.save(os.path.join(RENDER, f"{asset}_variants_contact.png"))

if __name__ == "__main__":
    only = None
    if "--only" in sys.argv: only = sys.argv[sys.argv.index("--only") + 1].split(",")
    main(only, "--no-render" not in sys.argv)
