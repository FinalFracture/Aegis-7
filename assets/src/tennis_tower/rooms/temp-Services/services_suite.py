"""Rook TTQA-028 (Jared card answer 2026-11-20 1:50 PM CT): Tennis Tower Services suite, tt_services_suite.

Spec: design/strip5_tennis_tower_v1.md §3.10 (IBC 2021 A-4 + "2 all-gender accessible/family rooms per floor").
One suite per floor = the 2 family rooms for that floor (6 total). Placed next to the restroom wet stacks:
F1 / F2 in the R1/R2-NW blocks (X 30..44, Z 64..69, behind the stall wet wall), F3 in the W under-stand bay
(X 24.3..29.8, Z 21.2..27.4, door in the existing X 24.1 opening). Each floor also gets one existing
tt_services_fountain_station (bi-level + bottle filler) from the 19-station proposal.

Module 4.30 (X) x 3.80 (Z) x 2.45 m, Y-up, +Z front, bottom-centre pivot. Two rooms 2.00 x 3.60 clear, each with a
0.95 x 2.10 m doorway and a surface sliding leaf parked OPEN over the centre pier (rig: Leaf_A / Leaf_B parent nodes,
each with its own *-colonly; closed pose = slide -0.97 m (A) / +0.97 m (B) along local X). Per room: wall-hung WC
(bath-pod / restroom.wc recipe), side + rear grab bars, wall-hung lavatory with knee clearance, mirror, fold-up baby
change station, bin, ceiling LED panel. Colliders only as Shell-colonly / Fixtures-colonly / Leaf_*-colonly.
5 dress variants (V1 default placed):
  python3 services_suite.py          -> v1..v5 + contact sheet (assets/glb/tennis_tower/services_suite, renders)
  python3 services_suite.py promote  -> godot/assets/models/tt_services_suite.glb (V1) with Leaf_A/Leaf_B nodes
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); TT = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, TT)
from modlib import *
import restroom as RR
import pygltflib as pg

W, D, T = 4.30, 3.80, 0.10           # footprint, wall thickness
X0, Z0 = -W/2, -D/2                  # -2.15, -1.90
HW, HC = 2.40, 2.45                  # wall top, roof top
ZI0, ZI1 = Z0 + T, -Z0 - T           # interior Z -1.80 .. 1.80 (front wall face 1.90)
DOOR = {"A": (-1.95, -1.00), "B": (1.00, 1.95)}; DH = 2.10
LZ0, LZ1 = 1.912, 1.952              # parked leaf plane (6 mm off the base band)
LEAF = {"A": (-0.99, -0.01), "B": (0.01, 0.99)}; TRAVEL = 0.97

def shell(q):
    ws = [box(X0, -X0, 0, HW, Z0, ZI0),                                  # rear wet wall
          box(X0, X0 + T, 0, HW, ZI0 - E, ZI1 + E), box(-X0 - T, -X0, 0, HW, ZI0 - E, ZI1 + E),   # side walls
          box(-.05, .05, 0, HW, ZI0 - E, ZI1 + E)]                         # party wall
    a0, a1 = DOOR["A"]; b0, b1 = DOOR["B"]
    for x0, x1 in ((X0, a0), (a1, b0), (b1, -X0)): ws.append(box(x0, x1, 0, HW, ZI1, -Z0))   # front piers
    for x0, x1 in (DOOR["A"], DOOR["B"]): ws.append(box(x0 - E, x1 + E, DH, HW, ZI1, -Z0))     # headers
    if q.get("clerestory"):   # V3: cut a 1.95..2.30 band out of both side walls, glazed (BLEND)
        side = []
        for xs in ((X0, X0 + T), (-X0 - T, -X0)):
            side += [box(*xs, 0, 1.95, ZI0 - E, ZI1 + E), box(*xs, 2.30, HW, ZI0 - E, ZI1 + E),
                     box(*xs, 1.95 - E, 2.30 + E, ZI0 - E, ZI0 + .15), box(*xs, 1.95 - E, 2.30 + E, ZI1 - .15, ZI1 + E)]
        ws = [ws[0]] + side + ws[3:]
    return ws

def build(q):
    p = Part(); mat = q.get("shell", WH)
    ws = shell(q); p.add("Shell_Walls", mat, *ws)
    roof = box(X0 - .02, -X0 + .02, HW - E, HC, Z0 - .02, -Z0 + .02); p.add("Roof_Slab", SL, roof)
    if q.get("clerestory"):
        p.add("Clerestory_Glass", GL, *[box(xc - .006, xc + .006, 1.95 + .002, 2.30 - .002, ZI0 + .15 + .002, ZI1 - .15 - .002) for xc in (X0 + T/2, -X0 - T/2)])
    # base band (kick plate) on the outside of every solid face, embedded E
    bb = [box(X0 - .006, -X0 + .006, 0, .15, Z0 - .006, Z0 + E),
          box(X0 - .006, X0 + E, 0, .15, Z0 + E, -Z0 + .006), box(-X0 - E, -X0 + .006, 0, .15, Z0 + E, -Z0 + .006)]
    a0, a1 = DOOR["A"]; b0, b1 = DOOR["B"]
    for x0, x1 in ((X0 + E, a0), (a1, b0), (b1, -X0 - E)): bb.append(box(x0, x1, 0, .15, -Z0 - E, -Z0 + .006))
    p.add("Base_Band", SGM, *bb)
    # door jamb liners (gunmetal) on the opening reveals
    jl = []
    for x0, x1 in (DOOR["A"], DOOR["B"]):
        jl += [box(x0 - E, x0 + .012, 0, DH - .012 + E, ZI1 + .01, -Z0 - .01), box(x1 - .012, x1 + E, 0, DH - .012 + E, ZI1 + .01, -Z0 - .01),
               box(x0 + .012 - E, x1 - .012 + E, DH - .012, DH + E, ZI1 + .01, -Z0 - .01)]
    p.add("Door_Jambs", SGM, *jl)
    # sliding leaves (parked open over the centre pier), track + hangers
    p.add("Door_Track", ST, box(-2.0, 2.0, 2.14, 2.20, -Z0 - E, 1.975))
    for t, (x0, x1) in LEAF.items():
        p.add(f"Leaf_{t}_Panel", q.get("leaf", SGM), box(x0, x1, .01, 2.12, LZ0, LZ1))
        hx = x1 - .14 if t == "A" else x0 + .06
        p.add(f"Leaf_{t}_Pull", ALY, box(hx, hx + .08 if t == "A" else hx + .08, .85, 1.25, LZ1 - E, LZ1 + .03))
        p.add(f"Leaf_{t}_Hanger_Hardware", ST, *[box(x - .03, x + .03, 2.11, 2.145, LZ0 + .003, LZ1 - .003) for x in (x0 + .12, x1 - .12)])
        p.add(f"Leaf_{t}_Window_Strip", GRN, box(x0 + .1, x1 - .1, 1.98, 2.0, LZ1 - E, LZ1 + .003))   # occupancy strip
        p.add(f"Leaf_{t}-colonly", G, box(x0, x1, .01, 2.12, LZ0, LZ1))
    # signage over each door: all-gender family / accessible pictogram plates + amber service band
    sg = []
    for x0, x1 in (DOOR["A"], DOOR["B"]):
        c = (x0 + x1) / 2; sg += [box(c - .30, c + .30, 2.22, 2.38, -Z0 - E, -Z0 + .006)]
    p.add("Sign_Plates", SLATE_OR(q), *sg)
    picto = []
    for x0, x1 in (DOOR["A"], DOOR["B"]):
        c = (x0 + x1) / 2
        for dx in (-.16, 0, .16):   # three figures (adult / child / wheelchair) as simple bars
            picto.append(box(c + dx - .025, c + dx + .025, 2.25, 2.35, -Z0 + .006 - E, -Z0 + .009))
    p.add("Sign_Pictograms", CY, *picto)
    rooms(p)
    dress(p, q)
    colliders(p, ws, q)
    return p

def SLATE_OR(q): return q.get("sign", SSL)

def rooms(p):
    for s in (-1, 1):   # A (s=-1) and B (s=+1) are mirror images
        side = s * (-X0 - T)          # inner face of the outer side wall (+-2.05)
        party = s * .05               # party wall face
        wcx = side - s * .45
        RR.wc(p, wcx, ZI0 - E)        # restroom / bath-pod WC recipe, vac unit embedded E into the wet wall
        # grab bars (side wall 1.05 m at 0.84, rear 0.75 m at 0.86 beyond the vac unit) + standoffs
        gx = side - s * .045
        bars = [tube((gx, .84, -1.62), (gx, .84, -.52), .018, 8), tube((wcx - s * .30, .86, ZI0 + .045), (wcx - s * 1.0, .86, ZI0 + .045), .018, 8)]
        so = [box(min(side, gx) - (E if s > 0 else 0) - (0 if s > 0 else .0), max(side, gx), .82, .86, z - .02, z + .02) for z in (-1.57, -.57)]
        so = [box(min(side + s * E, gx), max(side + s * E, gx), .82, .86, z - .02, z + .02) for z in (-1.57, -.57)]
        so += [box(x - .02, x + .02, .84, .88, ZI0 - E, ZI0 + .045) for x in (wcx - s * .35, wcx - s * .95)]
        p.add("Grab_Bars_Hardware", ALY, *bars, *so)
        # lavatory on the party wall (wall-hung, knee clear), steel bowl plate, tap, mirror
        lx0, lx1 = sorted((party, party + s * .50))
        cl = [box(lx0 - (E if s < 0 else 0), lx1 + (E if s > 0 else 0), .74, .86, -.75, -.25)]
        p.add("Lavatory", WH, *[box(min(party - s * E, party + s * .50), max(party - s * E, party + s * .50), .74, .86, -.75, -.25)])
        p.add("Lavatory_Bowl", ST, box(min(party + s * .10, party + s * .44), max(party + s * .10, party + s * .44), .858, .866, -.68, -.32))
        tx = party + s * .06
        p.add("Tap_Hardware", ALY, box(min(tx, party - s * E), max(tx, party - s * E) + 0, .866 - E, .98, -.52, -.48) if False else box(min(tx, party - s * E), max(tx, party - s * E), .90, .94, -.52, -.48))
        p.add("Mirror", ALY, box(min(party + s * .006, party - s * E), max(party + s * .006, party - s * E), 1.0, 1.8, -.80, -.20))
        # fold-up baby change station (closed) + bin
        p.add("Change_Station", WH, box(min(party + s * .10, party - s * E), max(party + s * .10, party - s * E), .75, 1.35, .35, 1.25))
        p.add("Change_Station_Strap", GRN, box(min(party + s * .10 - s * .003, party + s * .10 + s * E), max(party + s * .10 - s * .003, party + s * .10 + s * E), 1.15, 1.18, .55, 1.05))
        p.add("Bin", SGM, box(min(party + s * .08, party + s * .34), max(party + s * .08, party + s * .34), 0, .60, -.10, .20))
        # ceiling LED panel (embedded E into the roof soffit)
        cx0, cx1 = sorted((party + s * .45, side - s * .45))
        p.add("Ceiling_LED", CY, box(cx0, cx1, HW - E - .016, HW - E + E, -1.0, .6))

def dress(p, q):
    d = q["dress"]
    if d == "court":      # court-line stripe wrapping sides + back at 1.10 m, amber service line on the roof edge
        st = [box(X0 - .006, -X0 + .006, 1.10, 1.15, Z0 - .010, Z0 - .006 + E),
              box(X0 - .010, X0 - .006 + E, 1.10, 1.15, Z0 - .006, -Z0 + .006), box(-X0 + .006 - E, -X0 + .010, 1.10, 1.15, Z0 - .006, -Z0 + .006)]
        p.add("Court_Line_Stripe", AM, *st)
        p.add("Roof_Edge_Line", AM, box(X0 + .02, -X0 - .02, HC - E, HC + .004, -Z0 - .08, -Z0 - .02))
    elif d == "green":    # living band: green wall clumps over the side + back faces
        gw = [xf(green_wall(-1.85, 1.85, 1.70, 2.30, 0, r=.13, seed=1), R=trimesh.transformations.rotation_matrix(np.pi, [0, 1, 0]), t=(0, 0, Z0))]
        for sx in (-1, 1):
            m = green_wall(-1.55, 1.55, 1.70, 2.30, 0, r=.13, seed=5 + sx)
            gw.append(xf(m, R=trimesh.transformations.rotation_matrix(sx * np.pi / 2, [0, 1, 0]), t=(sx * -X0, 0, 0)))
        p.add("Green_Wall_Band", LF, *gw)
    elif d == "leaf":     # leaf crests along the roof front edge
        p.add("Leaf_Crests", LF, *[leaf_dir((x, HC - .003, -Z0 - .25), (0, 1, 0), .35, .25, t=.0125) for x in np.linspace(-1.8, 1.8, 7)])
    elif d == "fin":      # Branch Fin: Y-fork steel fins on the side walls
        fs = []
        for sx in (-1, 1):
            xw = sx * (-X0) + sx * .004
            for z in (-1.2, 0.0, 1.2):
                c = np.array([xw + sx * .05, 1.6, z]); fs += [box(min(sx * (-X0) - sx * E, xw + sx * .07), max(sx * (-X0) - sx * E, xw + sx * .07), .15, 1.6, z - .02, z + .02),
                                                             tube(c, (xw + sx * .05, 2.30, z - .35), .015, 5), tube(c, (xw + sx * .05, 2.30, z + .35), .015, 5)]
        p.add("Branch_Fins", ST, *fs)
    # 'clerestory' dress = glass band only (built in shell)

def colliders(p, ws, q):
    def cm(ms):
        c = trimesh.util.concatenate(ms); c.metadata["uv"] = np.zeros((len(c.vertices), 2)); return c
    sh = list(ws) + [box(X0, -X0, HW - E, HC, Z0, -Z0)]
    if q.get("clerestory"):
        for xs in ((X0, X0 + T), (-X0 - T, -X0)): sh.append(box(*xs, 1.95, 2.30, ZI0, ZI1))
    p.P["Shell-colonly"] = (G, cm(sh))
    fx = []
    for s in (-1, 1):
        side = s * (-X0 - T); party = s * .05; wcx = side - s * .45
        fx += [box(wcx - .2, wcx + .2, 0, .43, ZI0, ZI0 + .64),
               box(min(party, party + s * .5), max(party, party + s * .5), .74, .86, -.75, -.25),
               box(min(party, party + s * .34), max(party, party + s * .34), 0, .60, -.10, .20),
               box(min(party, party + s * .10), max(party, party + s * .10), .75, 1.35, .35, 1.25)]
    p.P["Fixtures-colonly"] = (G, cm(fx))

VARIANTS = [
    dict(label="V1 Court Line: white shell, amber court-line stripe, gunmetal leaves", dress="court"),
    dict(label="V2 Living Band: green wall band on sides and back", dress="green"),
    dict(label="V3 Clerestory: frosted glass high band (BLEND)", dress="clerestory", clerestory=True),
    dict(label="V4 Leaf Crest: leaf crests on the roof edge, leaf-green leaves", dress="leaf", leaf=LF),
    dict(label="V5 Branch Fin: Y-fork steel fins, slate shell", dress="fin", shell=SL),
]

def group_leaves(gp):
    g = pg.GLTF2().load(gp); sc = g.scenes[g.scene or 0]
    for t in ("A", "B"):
        kids = [i for i, n in enumerate(g.nodes) if n.name and (n.name.startswith(f"Leaf_{t}_") or n.name == f"Leaf_{t}-colonly")]
        assert len(kids) >= 5, (t, kids)
        g.nodes.append(pg.Node(name=f"Leaf_{t}", children=kids)); sc.nodes = [i for i in sc.nodes if i not in kids] + [len(g.nodes) - 1]
    g.save_binary(gp)

def promote(vi=0, name="tt_services_suite"):
    p = recenter(build(VARIANTS[vi])); gp = os.path.join(ROOT, "godot/assets/models", f"{name}.glb")
    tris, geo = export_final(p.P, [gp]); finish_glb(gp); group_leaves(gp)
    chk = cc.check({k: v for k, v in p.P.items() if "colonly" not in k}, n_samp=400)
    try: ok_v = vm.validate_file(gp, check_tri_range=(1, TRI_MAX), require_textures=False, require_blend_glass=False)
    except AssertionError as e: print("VALIDATE FAIL", e); ok_v = False
    V = np.vstack([m.vertices for k, (_, m) in p.P.items() if "colonly" not in k])
    print(json.dumps(dict(glb=gp, tris=int(tris), clip_pass=bool(chk["pass"]), worst_overlap=chk["worst_overlap"], coplanar=chk["coplanar"], open=chk["open"],
                          pivot=chk["pivot"], validate=bool(ok_v), bbox=[V.min(0).round(4).tolist(), V.max(0).round(4).tolist()]), default=str))

if __name__ == "__main__" and sys.argv[1:2] == ["promote"]: promote(int(sys.argv[2]) - 1 if len(sys.argv) > 2 else 0)
elif __name__ == "__main__": run("services_suite", build, VARIANTS, title="TTQA-028 family/accessible suite 4.30 x 3.80 m, 2 rooms, sliding leaves parked open")
