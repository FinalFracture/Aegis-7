"""Rook (Oct 30, box pipeline): residential exterior street furniture, list v1 #32 bench, #33 bin/recycler, #34 bollard.
Five candidates each -> design/assets/<name>/<name>_01..05.glb + <name>_contact_sheet.png.
Aegis-7: zero wood; gunmetal #1A1E24, carbon-slate #282E38, amber #FF9500 (emissive), titanium; flat PBR (0% micro-noise);
BLEND glass. Y-up, bottom-centre (0,0,0) pivot, +Z = street/front face. Parts embed 0.004 m (no coplanar contact faces),
only one part per footprint touches the floor. Every candidate passes ext_clip_check before export.
Run: python3 ext_street_furniture_generator.py [bench|bin|bollard|all]"""
import os, sys, json, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, blk, Pod, dc, plt
from dining_chair_generator import export_final, FMAT, loft, circle, rrect, xf, render_view, _PBR
from bath_pod_generator import set_glass_blend, views
from kitchen_counter_generator import crop
import ext_clip_check as cc

FMAT.update({
 "a7_gun":   _PBR(name="A7_Gunmetal", baseColorFactor=(0x1A/255, 0x1E/255, 0x24/255, 1), metallicFactor=0.8, roughnessFactor=0.5),
 "a7_slate": _PBR(name="A7_CarbonSlate", baseColorFactor=(0x28/255, 0x2E/255, 0x38/255, 1), metallicFactor=0.25, roughnessFactor=0.7),
 "a7_ti":    _PBR(name="A7_Titanium", baseColorFactor=(0.72, 0.74, 0.76, 1), metallicFactor=0.9, roughnessFactor=0.4),
 "a7_amber": _PBR(name="A7_Amber", baseColorFactor=(1.0, 0x95/255, 0.0, 1), metallicFactor=0.0, roughnessFactor=0.4, emissiveFactor=(1.0, 0x95/255, 0.0)),
})
if "glass" not in FMAT: FMAT["glass"] = _PBR(name="Glass", baseColorFactor=(0.70, 0.82, 0.90, 0.25), metallicFactor=0.0, roughnessFactor=0.05)
G, S, T, A, GL = "a7_gun", "a7_slate", "a7_ti", "a7_amber", "glass"
E = .004  # embed depth for structural joints
ROOT = dc.ROOT

def ring(r, y0, y1, n, s0=1, s1=1, x=0, z=0, top=None, flat=False):  # n-gon prism / taper (optional 3rd ring = chamfered top; flat = flat face to +Z)
    R = [(y0, s0, s0), (y1, s1, s1)] + ([top] if top else []); o = circle(r, n)
    if flat: a = np.pi / n; o = o @ np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])
    m = loft(o, R); return xf(m, t=(x, 0, z))

# ---------------- #32 bench 1.8 W x 0.5 D x 0.45 H, <=800 tris ----------------
def bench(v):
    p = Pod(f"ext_bench_0{v}")
    if v == 1:  # Slab Plinth: carbon-slate slab on two gunmetal plinths, titanium front nosing, amber underglow
        p.add("Seat_Slab", S, blk(-.9, .9, .38, .45, -.244, .244, .03, 2))
        p.add("Plinths", G, *[blk(x - .1, x + .1, 0, .38 + E, -.17, .17, .02, 1) for x in (-.6, .6)])
        p.add("Front_Nosing", T, box(-.86, .86, .395, .435, .24, .25))
        p.add("Underglow", A, box(-.45, .45, .366, .38 + E, .14, .16))
    elif v == 2:  # Titanium Slats: 4 titanium slats on gunmetal frames, amber floor clamps
        for k, z in enumerate((-.18, -.06, .06, .18)): p.add("Seat_Slats", T, blk(-.9, .9, .41, .45, z - .05, z + .05, .012, 1))
        for x in (-.62, .62):
            p.add("Frame_Rails", G, box(x - .03, x + .03, .37, .41 + E, -.235, .235))
            p.add("Frame_Legs", G, *[box(x - .025, x + .025, .008, .37 + E, z - .025, z + .025) for z in (-.18, .18)])
            p.add("Floor_Clamps", A, *[box(x - .04, x + .04, 0, .012, z - .04, z + .04) for z in (-.18, .18)])
    elif v == 3:  # Spine Cantilever: slate shell + titanium top on a gunmetal spine and three round legs with base discs
        p.add("Spine", G, box(-.8, .8, .30, .344, -.04, .04))
        p.add("Legs", G, *[cyl(x, 0, .035, .012, .20 + E, 10) for x in (-.6, 0, .6)], *[cyl(x, 0, .035, .23 - E, .30 + E, 10) for x in (-.6, 0, .6)])  # split at the reflector
        p.add("Base_Discs", G, *[cyl(x, 0, .1, 0, .016, 12) for x in (-.6, 0, .6)])
        p.add("Leg_Reflectors", A, *[cyl(x, 0, .038, .20, .23, 10) for x in (-.6, 0, .6)])
        p.add("Seat_Shell", S, blk(-.9, .9, .34, .42, -.25, .25, .04, 2))
        p.add("Seat_Top", T, blk(-.88, .88, .42 - E, .45, -.23, .23, .03, 2))
    elif v == 4:  # Divided Sled: slate seat on gunmetal sled frames, two titanium arm dividers, amber edge light
        p.add("Seat", S, blk(-.9, .9, .34, .40, -.245, .245, .03, 2))
        p.add("Dividers", T, *[blk(x - .02, x + .02, .40 - E, .45, -.2, .2, .008, 1) for x in (-.3, .3)])
        for x in (-.66, .66):
            p.add("Sled_Runners", G, box(x - .03, x + .03, 0, .03, -.22, .22))
            p.add("Sled_Uprights", G, *[box(x - .025, x + .025, .03 - E, .34 + E, z - .025, z + .025) for z in (-.17, .17)])
        p.add("Edge_Light", A, box(-.8, .8, .33, .34 + E, .2, .215))
    elif v == 5:  # Glass Lightbox: titanium seat over twin BLEND glass panes and an amber light core on a gunmetal plinth
        p.add("Plinth", G, blk(-.75, .75, 0, .064, -.2, .2, .02, 1))
        p.add("Glass_Panes", GL, *[box(-.7, .7, .064 - E, .38 + E, z - .006, z + .006) for z in (-.17, .17)])
        p.add("Light_Core", A, box(-.66, .66, .064 - E, .38 + E, -.1, .1))
        p.add("End_Posts", G, *[box(x - .03, x + .03, .064 - E, .38 + E, -.15, .15) for x in (-.71, .71)])
        p.add("Seat", T, blk(-.9, .9, .38, .45, -.25, .25, .03, 2))
    return p
BENCH = [(1, "Slab_Plinth"), (2, "Titanium_Slats"), (3, "Spine_Cantilever"), (4, "Divided_Sled"), (5, "Glass_Lightbox")]

# ---------------- #33 bin / recycler 0.5 x 0.5 x 1.0, <=400 tris ----------------
def slot(p, x, y, w=.16, h=.05, zf=.24, mat=A):  # chute mouth: gunmetal throat plate proud of the face + amber hood (no buried insert)
    p.add("Chute_Throats", G, box(x - w / 2, x + w / 2, y - h / 2, y + h / 2, zf - E, zf + .008))
    p.add("Chute_Hoods", mat, box(x - w / 2 - .01, x + w / 2 + .01, y + h / 2 - E, y + h / 2 + .015, zf - .002, zf + .02))
def bin_(v):
    p = Pod(f"ext_bin_recycler_0{v}")
    if v == 1:  # Twin Slot: slate body, titanium lid, two amber-hooded chutes, gunmetal plinth
        p.add("Plinth", G, box(-.22, .22, 0, .064, -.22, .22))
        p.add("Body", S, blk(-.24, .24, .06, .96, -.24, .24, .03, 1))
        p.add("Lid", T, blk(-.25, .25, .96 - E, 1.0, -.25, .25, .03, 1))
        for x in (-.1, .1): slot(p, x, .8)
    elif v == 2:  # Round Drum: 10-sided slate drum, titanium bands, chamfered lid, single amber chute ring
        p.add("Base", G, ring(.2, 0, .064, 10))
        p.add("Drum", S, ring(.24, .06, .2, 10), ring(.24, .24 - E, .62, 10), ring(.24, .66 - E, .80, 10), ring(.24, .82 - E, .94, 10))  # drum split at bands
        p.add("Bands", T, ring(.246, .2 - E, .24, 10), ring(.246, .62 - E, .66, 10))
        p.add("Chute_Ring", A, ring(.25, .80 - E, .82, 10))
        p.add("Lid", T, ring(.25, .94 - E, .97, 10, top=(1.0, .6, .6)))
    elif v == 3:  # Glass Window Sorter: square slate body with a BLEND glass fill window and three chutes
        p.add("Plinth", G, box(-.22, .22, 0, .064, -.22, .22))
        p.add("Body", S, box(-.24, .24, .06, .96, -.24, .24))
        p.add("Fill_Window", GL, box(-.16, .16, .25 - E, .6 + E, .237, .248))
        p.add("Window_Frame", G, box(-.18, .18, .6 - E, .63, .24 - E, .252), box(-.18, .18, .22, .25 + E, .24 - E, .252))
        p.add("Lid", T, box(-.25, .25, .96 - E, 1.0, -.25, .25))
        for x in (-.15, 0, .15): slot(p, x, .82, w=.1)
    elif v == 4:  # Octagon Tower: octagonal gunmetal tower, amber ring, titanium sloped cap
        ap = .26 * np.cos(np.pi / 8)  # apothem: flat face toward +Z
        p.add("Tower", G, ring(.26, 0, .7, 8, flat=True), ring(.26, .73 - E, .9, 8, flat=True))
        p.add("Amber_Ring", A, ring(.266, .7 - E, .73, 8, flat=True))
        p.add("Cap", T, ring(.255, .9 - E, .95, 8, top=(1.0, .45, .45), flat=True))
        slot(p, 0, .82, w=.14, zf=ap)
    elif v == 5:  # Compactor: slate cabinet, tapered titanium hopper, glass status lens + amber light
        p.add("Cabinet", S, blk(-.24, .24, 0, .78, -.24, .24, .02, 1))
        p.add("Hopper", T, xf(loft(rrect(.48, .48, .02, 1), [(.78 - E, 1, 1), (.98, .8, .8), (1.0, .7, .7)]), t=(0, 0, 0)))
        p.add("Status_Lens", GL, box(.12, .2, .62, .7, .238, .25))
        p.add("Status_Light", A, box(.125, .195, .58, .62 + E, .236, .246))
        p.add("Kick_Plate", G, box(-.2, .2, .02, .12, .24 - E, .248))
    return p
BIN = [(1, "Twin_Slot"), (2, "Round_Drum"), (3, "Glass_Window_Sorter"), (4, "Octagon_Tower"), (5, "Compactor")]

# ---------------- #34 bollard 0.2 x 0.2 x 0.9, <=150 tris ----------------
def bollard(v):
    p = Pod(f"ext_bollard_0{v}")
    if v == 1:  # Round Band: gunmetal post, amber reflective band, titanium domed cap
        p.add("Post", G, ring(.095, 0, .71, 10)); p.add("Amber_Band", A, ring(.1, .706, .784, 10))
        p.add("Cap", T, ring(.095, .78, .88, 10, top=(.9, .7, .7)))
    elif v == 2:  # Square Chamfer: square slate post on gunmetal base plate, twin amber bands, chamfered titanium cap
        p.add("Base_Plate", G, box(-.1, .1, 0, .02, -.1, .1)); p.add("Post", S, box(-.09, .09, .02 - E, .62, -.09, .09), box(-.09, .09, .66 - E, .72, -.09, .09), box(-.09, .09, .76 - E, .86, -.09, .09))
        p.add("Amber_Bands", A, box(-.094, .094, .62 - E, .66, -.094, .094), box(-.094, .094, .72 - E, .76, -.094, .094))
        q = .092; p.add("Cap", T, loft(np.array([(q, q), (-q, q), (-q, -q), (q, -q)]), [(.86 - E, 1, 1), (.88, 1, 1), (.9, .6, .6)]))
    elif v == 3:  # Tapered Titanium: tapering titanium post, matching tapered amber band
        sc = lambda y: 1 - .25 * y / .9
        p.add("Post_Lower", T, ring(.1, 0, .6, 12, 1, sc(.6)))
        p.add("Amber_Band", A, ring(.1 * 1.05, .6 - E, .66 + E, 12, sc(.6) , sc(.66)))
        p.add("Post_Upper", T, ring(.1, .66, .9, 12, sc(.66), sc(.9)))
    elif v == 4:  # Flange Base: square gunmetal flange, slim slate post, amber band, tapered titanium cap
        p.add("Flange", G, box(-.1, .1, 0, .025, -.1, .1)); p.add("Post", S, ring(.07, .025 - E, .6, 8), ring(.07, .66 - E, .78, 8))
        p.add("Amber_Band", A, ring(.076, .6 - E, .66, 8)); p.add("Cap", T, ring(.08, .78 - E, .9, 8, 1, .8))
    elif v == 5:  # Lens Halo: octagonal gunmetal post, BLEND glass lens, amber halo ring, tapered titanium cap
        p.add("Post", G, ring(.1, 0, .78, 8)); p.add("Glass_Lens", GL, ring(.096, .78 - E, .84, 8))
        p.add("Amber_Halo", A, ring(.104, .84 - E, .86, 8)); p.add("Cap", T, ring(.1, .86 - E, .9, 8, 1, .75))
    return p
BOLL = [(1, "Round_Band"), (2, "Square_Chamfer"), (3, "Tapered_Titanium"), (4, "Flange_Base"), (5, "Lens_Halo")]

ASSETS = {"bench": ("ext_bench", bench, BENCH, 800, "#32 bench 1.8x0.5x0.45"),
          "bin": ("ext_bin_recycler", bin_, BIN, 400, "#33 bin/recycler 0.5x0.5x1.0"),
          "bollard": ("ext_bollard", bollard, BOLL, 150, "#34 bollard 0.2x0.2x0.9")}

def recenter(p):
    V = np.vstack([m.vertices for _, m in p.P.values()]); lo, hi = V.min(0), V.max(0); d = (-(lo[0] + hi[0]) / 2, -lo[1], -(lo[2] + hi[2]) / 2)
    for k, (mk, m) in p.P.items(): uv = m.metadata["uv"]; m.apply_translation(d); m.metadata["uv"] = uv
    return p

HEAD = {}  # key -> min y: adds a second contact-sheet row with a close-up of everything above that height (e.g. lamp heads)
def headgeo(geo, y):
    out = {}
    for k, (mk, V, N, F) in geo.items():
        keep = F[(V[F][:, :, 1] >= y).all(1)]
        if len(keep): u, inv = np.unique(keep, return_inverse=True); out[k] = (mk, V[u], N[u], inv.reshape(-1, 3))
    return out
def build(key):
    name, fn, iters, budget, title = ASSETS[key]; out = os.path.join(ROOT, "design/assets", name); os.makedirs(out, exist_ok=True)
    rep = []; tiles = []; heads = []; _, _, _, iso = views()
    for v, nm in iters:
        p = recenter(fn(v)); chk = cc.check(p.P)
        gp = os.path.join(out, f"{name}_0{v}.glb"); tris, geo = export_final(p.P, [gp]); set_glass_blend(gp)
        nouv = [k for k, (mk, m) in p.P.items() if "uv" not in m.metadata]
        r = dict(cand=f"{name}_0{v}", style=nm, tris=tris, budget_ok=tris <= budget, size=chk["size"], pivot=chk["pivot"], clip_pass=chk["pass"],
                 worst_overlap=chk["worst_overlap"], overlaps_over=[o for o in chk["overlap"] if not o[3]], coplanar=chk["coplanar"], open=chk["open"], nouv=nouv,
                 glb=os.path.relpath(gp, ROOT))
        rep.append(r); print(json.dumps(r))
        saved = {k: FMAT[k] for k in (A,)}; em = FMAT[A]
        FMAT[A] = _PBR(name=em.name, baseColorFactor=(0, 0, 0, 1), metallicFactor=0, roughnessFactor=1, emissiveFactor=(1.0, .58, 0.0))
        im = crop(render_view(geo, iso, size=600, shadow=True))
        if key in HEAD: heads.append(crop(render_view(headgeo(geo, HEAD[key]), iso, size=600, shadow=False)))
        FMAT.update(saved)
        tiles.append((f"{v}. {nm}\n{tris} tris | clip {'PASS' if chk['pass'] else 'FAIL'} | {chk['size'][0]:.2f}x{chk['size'][2]:.2f}x{chk['size'][1]:.2f} m", im))
    nr = 2 if heads else 1; fig, axs = plt.subplots(nr, 5, figsize=(22, 6 * nr), facecolor="#F4F2EC", squeeze=False)
    for ax, (t, im) in zip(axs[0], tiles): ax.imshow(im); ax.axis("off"); ax.set_title(t, fontsize=11, color="#333")
    for k, (ax, im) in enumerate(zip(axs[-1], heads) if heads else [], 1): ax.imshow(im); ax.axis("off"); ax.set_title(f"{k}. head close-up (y >= {HEAD[key]} m)", fontsize=11, color="#333")
    fig.suptitle(f"Rook  {title}  (budget {budget} tris)  candidates 01-05  |  Aegis-7 gunmetal/slate/titanium/amber, BLEND glass, +Z front, iso view", fontsize=13, color="#444")
    plt.tight_layout(rect=(0, 0, 1, .93 if nr == 1 else .96)); sp = os.path.join(out, f"{name}_contact_sheet.png"); fig.savefig(sp, dpi=90, facecolor="#F4F2EC"); plt.close(fig)
    json.dump(rep, open(os.path.join(out, f"{name}_report.json"), "w"), indent=1); print("sheet", sp); return rep

if __name__ == "__main__":
    keys = sys.argv[1:] or ["all"]
    for k in (ASSETS if keys == ["all"] else keys): build(k)
