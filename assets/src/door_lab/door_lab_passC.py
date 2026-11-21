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
            "open_105deg": D(f_open=1, f_dog=0)}

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
        lf = [n for n in _desc(r, "hatch_leaf") if n in vis]; arms = [n for n in vis if n.startswith("hatch_strut") or n == "hatch_stay_arm"]
        fix = [n for n in vis if r.N[n]["parent"] is None and n not in arms]
        w = (0.0, None, None, None); w2 = (0.0, None, None, None)
        for fo in np.linspace(0, 1, 22):
            P = r.world_parts(fh.deltas(r, fo, 0, mirror=mir))
            d = penetration({k: P[k] for k in lf if not k.startswith("hatch_strut")}, {k: P[k] for k in fix}, n_samp=150)
            d2 = penetration({k: P[k] for k in arms}, {k: P[k] for k in fix + [m for m in lf if not m.startswith("hatch_strut") and "clevis" not in m and "track" not in m]}, n_samp=150)
            if d[0] >= w[0]: w = (d[0], d[1], d[2], round(105*float(fo), 1))
            if d2[0] >= w2[0]: w2 = (d2[0], d2[1], d2[2], round(105*float(fo), 1))
        res["leaf_swing_0_105deg"] = w; res["struts_stay_vs_all"] = w2
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
    fixed = [P0[n][1] for n in P0 if r.N[n]["parent"] is None and not n.startswith("hatch_strut") and n != "hatch_stay_arm"]
    liner = {}
    for lab, dy in (("throat_-0.15", -.15), ("well_-0.30", -.30)):
        if fy + dy < .02: continue
        o = np.array([0, fy + dy, 0.0]); d = _rays(fixed, o, [(1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)])
        liner[lab] = dict(x=round(d[0] + d[1], 4), z=round(d[2] + d[3], 4))
    out["liner_clear_xz"] = liner
    out["liner_ok"] = all(v["x"] >= .8995 and v["z"] >= .8995 for v in liner.values())
    prism = {}
    for lab, kw in (("closed", dict(f_open=0, f_dog=1)), ("open", dict(f_open=1, f_dog=0))):
        P = r.world_parts(fh.deltas(r, mirror=mir, **kw)); hits = {}
        for n, (_, m) in P.items():
            if lab == "closed" and r.N[n]["parent"] is not None: continue          # the closed leaf and its underside hardware cover the opening by design
            if lab == "closed" and (n.startswith("hatch_strut") or n == "hatch_stay_arm"): continue
            S = np.vstack([m.vertices, trimesh.sample.sample_surface(m, 3000, seed=2)[0]])
            ins = (np.abs(S[:, 0]) < .449) & (np.abs(S[:, 2]) < .449) & (S[:, 1] > float(P["hatch_frame"][1].vertices[:, 1].min()) + .017) & (S[:, 1] < fy + 2.0)
            if lab == "closed": ins &= S[:, 1] < fy - LT_MIN
            if ins.any():
                q = S[ins]; hits[n] = dict(n=int(ins.sum()), x=[round(float(q[:, 0].min()), 3), round(float(q[:, 0].max()), 3)],
                                           z=[round(float(q[:, 2].min()), 3), round(float(q[:, 2].max()), 3)], y_above_floor=[round(float(q[:, 1].min() - fy), 3), round(float(q[:, 1].max() - fy), 3)],
                                           depth_from_hinge_liner_mm=round(1000*(float(q[:, 2].max()) + .45), 1))
        prism[lab] = hits
    out["hardware_inside_clear_prism"] = prism
    return out
LT_MIN = fh.LT + .07   # closed check starts below the leaf's underside hardware zone (0.17 m under the floor)

def main(only=None, do_render=True):
    rep = json.load(open(QA_JSON)) if os.path.exists(QA_JSON) and only else {}
    for asset, vars_ in VARIANTS.items():
        if only and asset not in only: continue
        rep[asset] = {}; thumbs = []
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
            if asset == "floor_hatch": e["hatch"] = hatch_checks(r, mir)
            e["pass"] = (e["under_budget"] and all(not c["bad_overlaps"] and not c["coplanar"] and not c["open"] for c in e["clip"].values())
                         and all(sw["depth_m"] <= .010 for sw in e["sweeps"].values()) and (asset != "floor_hatch" or (e["hatch"]["flush_ok"] and e["hatch"]["liner_ok"])))
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
                thumbs.append((vid, label, tp))
        if do_render: contact(asset, thumbs)
    json.dump(rep, open(QA_JSON, "w"), indent=1, default=str)
    return rep

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
