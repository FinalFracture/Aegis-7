"""Rook: Tennis Tower E-terrace playground piece 2, 2-bay swing set (spec §3.11.6: 4 seats, swinging along X, 7 x 3 m).
Beam along Z (3.1 m) at +2.45 on three splayed A-frames (z -1.5 / 0 / +1.5, feet at x +-1.0), 4 belt seats at z -1.1, -0.4, +0.4, +1.1,
seat +0.45, chain 1.94 m; poured-rubber pad 7.0 x 3.0 under the swing arc. Seats + chains are separate animatable parts
(Swing1..4_*, hinge axis = Z line at y 2.39 through x 0). No wood. Court Line playground language (#63) as baseline.
REUSE: play_tower materials (EPDM rubber, HDPE), #63 ball finials + court-line, restroom Leaf Crest crest(), tree-column Y-fork,
curtain-wall fin(), stand planter()/shrubs(), cabana_lounger pillow()/boxuv. Run: python3 swing_set.py"""
from modlib import *
import play_tower as pt
from cabana_lounger import boxuv, pillow, fit, T
from restroom_extras import crest
YB, HY, PAD = 2.45, 2.39, .03; ZS = (-1.1, -.4, .4, 1.1); ZA = (-1.5, 0, 1.5); FX = 1.0
U = pt.U
def build(q):
    p = Part(); d = q["dress"]; fm = q.get("frame", SGM); sm = q.get("seat", BA)
    p.add("Safety_Pad", pt.RU, boxuv(box(-3.5, 3.5, 0, PAD, -1.5, 1.5), .5))
    F = [tube((0, YB, -1.55), (0, YB, 1.55), .06, 10)]
    for z in ZA:
        if d != "fin": F += [tube((0, YB, z), (sx*FX, PAD + .02, z), .05, 8) for sx in (-1, 1)]
        F += [box(sx*FX - .12, sx*FX + .12, PAD - E, PAD + .03, z - .08, z + .08) for sx in (-1, 1)]
    if d == "fin":   # Branch Fin legs: fish-belly fin plates in the A-frame plane
        for z in ZA:
            for sx in (-1, 1):
                L = np.linalg.norm([sx*FX, PAD + .02 - YB]); m = fin(0, 0, L, .1, .04, 0, belly=.4); m.apply_translation((0, 0, .05))
                F.append(xf(m, R=trimesh.geometry.align_vectors([0, 1, 0], np.array([sx*FX, PAD + .02 - YB, 0]) / L), t=(0, YB, z)))
    F += [box(-.04, .04, HY - .03, YB - .04, z + s*.18 - .02, z + s*.18 + .02) for z in ZS for s in (-1, 1)]   # hangers
    p.add("Swing_Frame", fm, *[boxuv(m, .5) for m in F])
    for i, z in enumerate(ZS, 1):
        seat = fit(T(pillow(.2, .04, .45, r=.015), trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])), (-.1, .43, z - .225))
        p.add(f"Swing{i}_Seat", sm, boxuv(seat, .4))
        p.add(f"Swing{i}_Chains", ALY, *[boxuv(tube((0, .47 - E, z + s*.18), (0, HY - .03 + E, z + s*.18), .008, 4), .3) for s in (-1, 1)])
    p.add("Frame-convcolonly", G, *[U(trimesh.convex.convex_hull(np.array([(0, YB + .06, z - .06), (0, YB + .06, z + .06), (sx*FX, 0, z - .08), (sx*FX, 0, z + .08), (0, YB - .1, z)]))) for z in ZA for sx in (-1, 1)])
    p.add("Beam-convcolonly", G, U(trimesh.creation.box(bounds=[[-.06, YB - .06, -1.55], [.06, YB + .06, 1.55]])))
    if d == "court":   # Court Line: ball finials on the beam ends, amber court lines on the pad marking the swing zone
        p.add("Ball_Finials", BA, *[node((0, YB, s*(1.55 + .045 - E)), .045, 0) for s in (-1, 1)])
        p.add("Court_Line", AM, *[boxuv(box(-3.4, 3.4, PAD - .002, PAD + .002, z - .025, z + .025), .5) for z in (-.75, .75)], *[boxuv(box(s*2.2 - .025, s*2.2 + .025, PAD - .002, PAD + .002, -1.4, 1.4), .5) for s in (-1, 1)])
    elif d == "leaf":  # Leaf Crest: leaf crests on every A-frame apex, leaf-green seats
        p.add("Leaf_Crests", LF, *[crest((0, YB + .06 + .17 - .003, z)) for z in ZA])
    elif d == "tree":  # Tree Swing: Y-fork branches off the end A-frames + foliage crowns over the beam ends
        p.add("Tree_Forks", ST, *[boxuv(tube((sx*.45, (YB + PAD)/2 + .45, s*1.5), (sx*.85, YB + .5, s*1.5), .03, 6), .5) for sx in (-1, 1) for s in (-1, 1)])
        p.add("Foliage_Crowns", LF2, *[clump((sx*.85, YB + .5 + .15 - E, s*1.5), .2, i) for i, (sx, s) in enumerate([(a, b) for a in (-1, 1) for b in (-1, 1)])])
    elif d == "garden":  # Garden Swing: planter troughs inside each end A-frame + shrubs
        for s in (-1, 1):
            tr, so, sy = planter(-.55, .55, PAD - E, s*1.5 - .12, s*1.5 + .12, h=.3); p.add("Planters", G, boxuv(tr, .5)); p.add("Planter_Soil", SO, so)
            p.add("Foliage", LF2, shrubs(-.5, .5, sy, s*1.5, r=.1, seed=5 + s))
    return p

def clearance(p, n=13):
    """sweep each seat+chains about its hinge (Z axis at y HY, x 0) from -60 to +60 deg; min distance to the static frame / pad."""
    stat = trimesh.util.concatenate([m for k, (_, m) in p.P.items() if not (k.startswith("Swing") and k[5].isdigit()) and "colonly" not in k and k not in ("Safety_Pad", "Court_Line")])
    from scipy.spatial import cKDTree
    kd = cKDTree(np.vstack([stat.sample(40000), stat.vertices])); pad_top = PAD; worst = 9.0; low = 9.0
    for k, (_, m) in p.P.items():
        if not (k.startswith("Swing") and k[5].isdigit()): continue
        pts = m.sample(300) if k.endswith("Seat") else m.vertices
        for a in np.radians(np.linspace(-60, 60, n)):
            R = trimesh.transformations.rotation_matrix(a, [0, 0, 1], point=(0, HY, 0)); P = trimesh.transform_points(pts, R)
            far = P[np.hypot(P[:, 0], P[:, 1] - HY) > .15] if k.endswith("Chains") else P
            if len(far): worst = min(worst, float(kd.query(far)[0].min()))
            low = min(low, float(P[:, 1].min() - pad_top))
    return dict(min_frame_clear=round(worst, 3), min_ground_clear=round(low, 3), pass_=bool(worst >= .05 and low >= .35))

VARIANTS = [
    dict(label="Court Line: gunmetal A-frames, ball seats, court-line pad", dress="court"),
    dict(label="Leaf Crest: leaf crests on the apexes, leaf seats", dress="leaf", seat=LF),
    dict(label="Tree Swing: Y-fork branches + foliage crowns", dress="tree", seat=LF2, frame=ST),
    dict(label="Garden Swing: planters inside the end A-frames", dress="garden", seat="tt_hdpe_sand"),
    dict(label="Branch Fin: fish-belly fin A-frame legs", dress="fin", frame=ST, seat=AM),
]
if __name__ == "__main__":
    run("swing_set", build, VARIANTS, title="2 bays, 4 seats, beam +2.45, swing along X, pad 7 x 3 m | nature + sports")
    C = {f"v{i}": clearance(recenter(build(v))) for i, v in enumerate(VARIANTS, 1)}
    print("CLEAR", json.dumps(C)); json.dump(C, open(os.path.join(RENDER_OUT, "swing_set", "clearance.json"), "w"), indent=1)
