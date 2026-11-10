"""Rook: Tennis Tower STRUCTURAL BLOCKOUT (spec Rev 2.9). Coarse but complete: slabs/concourses F1-F3, partitions + openings,
columns (PT, aquatic X 0 / X 30, F1 runoff, E-band X 126.5) with impact pads, 9 aquatic transfer trusses (one instanced asset),
diving-well coffer, climbing-void guard + W-CL frame, 4 plant stacks, roof edges / closures / corner returns / 4 m infill bays,
F3 Glass Box corner closures, F3 ball net. Run: python3 build_structure.py  ->  godot/assets/models/tt_struct_*.glb +
tt_struct_layout.json (world offsets for chunked level pieces; instanced kit pieces are placed by assemble_preview.py)."""
from struct_lib import *
from tower_plan import *
REP, LAY = [], {}
R = lambda r, pad=0: (r[0] - pad, r[1] + pad, r[2] - pad, r[3] + pad)
TREE_HOLES = [(x - .7, x + .7, z - .7, z + .7) for x, z in TREES]
CORE_HOLES = [c[2] for c in CORES]; LIFT_HOLES = [l[1] for l in LIFTS]; PLANT_HOLES = [p[1] for p in PLANT]
POOL_CUT = [(1, 10, 26, 32), (8.5, 10, 32, 34.2)]           # r4 Rev 3.6 pool switchback cut + passage (deck to the lobby wall face Z 34.2)
LEIS_CUT = [(0, 15.3, 44.8, 46.3), (0, 1.8, 46.3, 47.0)]         # r4 Rev 3.5 leisure S-strip ramp + bottom landing
SKIP_X0 = {12.5, 66.5}; SKIP_X30 = {39.5}        # columns that land inside a stair-core wall (ST-AQS / ST-AQN / LW): bearing taken by the core

def f1_slab():
    it = []
    DV = R(WATER["diving"][:4], .3); holes = [(0, 30, 0, 34.5), (0, 30, 44.5, 79), DV]
    it += [("Slab_F1", CON, m) for m in slab(FOOT, holes, F1, SLAB[F1])]
    it += [("Slab_F1", CON, m) for m in slab((0, 30, 0, 34.5), [DV], F1, SLAB[F1])]
    it += [("Slab_F1", CON, m) for m in slab((0, 30, 44.5, 79), [], F1, SLAB[F1])]
    x0, x1, z0, z1, d = WATER["diving"]; pit = F1 + 2.0 - d          # pit floor -2.5
    it += [("Slab_F1", CON, box(x0, x1, pit - .4, pit, z0, z1))]
    it += [("Slab_F1", CON, m) for m in (box(x0 - .3, x0 + E, pit - .4, F1, z0 - .3, z1 + .3), box(x1 - E, x1 + .3, pit - .4, F1, z0 - .3, z1 + .3),
                                            box(x0 + E, x1 - E, pit - .4, F1, z0 - .3, z0 + E), box(x0 + E, x1 - E, pit - .4, F1, z1 - E, z1 + .3))]
    # S deck +2.0 (lap / diving). r4 Rev 3.5: the X 4..7 deck stair is replaced by the switchback cut (tt_struct_pool_ramp, Rev 3.6)
    it += [("Deck_S_+2.0", SSL, m) for m in slab((0, 30, 0, 34.2), [WATER["lap"][:4], WATER["diving"][:4]] + POOL_CUT, 2.0, 2.0 + E)]
    # N deck +1.0 (river channel, splash -0.6, runout -1.0), N-deck access steps from the foyer door Z 45..47
    holes = RIVER + [WATER["splash"][:4], WATER["runout"][:4]]
    it += [("Deck_N_+1.0", SSL, m) for m in slab((0, 30, 44.8, 79), holes + LEIS_CUT, 1.0, 1.0 + E)]   # r4: S-strip ramp cut
    sx0, sx1, sz0, sz1, sd = WATER["splash"]; it += [("Deck_N_+1.0", SSL, box(sx0, sx1, -E, 1.0 - sd, sz0, sz1))]
    return it

def f2_slab():
    it = []; y = F2; d = SLAB[F2]
    aq = [(0, 30, 0, 34.5), (0, 30, 44.5, 56), (2, 30, 56, 58), (20, 30, 58, 60.4), (0, 30, 60.4, 79)]
    holes = aq + CORE_HOLES + LIFT_HOLES + TREE_HOLES + PLANT_HOLES
    it += [("Slab_F2", CON, m) for m in slab(FOOT, holes, y, d)]
    for x in (45.5, 71.5, 97.5): it.append(("Beams_F2", CON, box(x - .3, x + .3, y - 1.1, y - d + E, 24.5, 54.5)))
    it.append(("Beams_F2", CON, box(39.5, 103.5, y - 1.1, y - d + E, 39.2, 39.8)))
    for z in PT_Z: it.append(("Beams_F2", CON, box(39.05, 103.95, y - 1.1, y - d + E, z - .45, z + .45)))
    for z in AQ_Z[1:-1]:
        if 20 < z < 60: it.append(("Beams_F2", CON, box(126.2, 126.8, y - 1.0, y - d + E, z - 4, z + 4)))
    return it

def f3_slab():
    it = []; y = F3; d = SLAB[F3]
    holes = CORE_HOLES + LIFT_HOLES + TREE_HOLES + PLANT_HOLES + [(35, 57, 3, 9.1), (0, 30, 21.8, 30.2)]
    it += [("Slab_F3", CON, m) for m in slab(FOOT, holes, y, d)]
    for x in PT_X: it.append(("Beams_F3", CON, box(x - .6, x + .6, y - 1.5, y - d + E, 24.95, 54.05)))
    for z in PT_Z: it.append(("Beams_F3", CON, box(39.05, 103.95, y - 1.5, y - d + E, z - .45, z + .45)))
    for z in (3.0, 8.0): it.append(("Trimmer_F3", G, box(35, 57, y - 1.2, y - d + E, z - .25 if z == 8 else z - .25, z + .25)))
    for z in AQ_Z: it.append(("Beams_F3", CON, box(126.2, 126.8, y - 1.0, y - d + E, max(z - 4.5, 0), min(z + 4.5, 79))) if 5 < z < 75 else None)
    return [i for i in it if i]

def walls_f1():
    y0, y1 = F1 - E, F2 - SLAB[F2] + E; W = []
    aqp30 = [(z - .3, z + .3) for z in AQ_Z if z not in SKIP_X30]; aqp0 = [(z - .3, z + .3) for z in AQ_Z if z not in SKIP_X0]
    W += wall(30, 113, y0, y1, axis="x", line=15, side=-1, openings=[(66.5, 76.5, y1), (50, 53, 3.0), (90, 93, 3.0)])
    W += wall(30, 113, y0, y1, axis="x", line=64, side=1, openings=[(66.5, 76.5, y1), (50, 53, 3.0), (90, 93, 3.0)])
    W += wall(0.3, 78.7, y0, y1, axis="z", line=30, side=-1, openings=[(34.5, 44.5, y1)], piers=aqp30)
    W += wall(0.3, 78.7, y0, y1, axis="z", line=113, side=1, openings=[(34.5, 44.5, y1), (24, 27, 3.0), (52, 55, 3.0), (70, 73, 3.0), (5, 8, 3.0)])
    W += wall(20.6, 58.4, y0, y1, axis="z", line=0, openings=[(34.5, 42.5, 4.5), (45, 47, 3.0)], piers=aqp0)
    W += wall(0.3, 26, y0, y1, axis="x", line=34.5, side=-1, openings=[(8.5, 10, 3.0)], piers=[(-.3, .3)])   # r4 Rev 3.6: 1.5 m ramp passage opening
    W += wall(0.3, 24.5, y0, y1, axis="x", line=44.5, side=1)
    W += [box(0.3, 1.0, y0, y1, 42.5, 44.5 + E), box(23, 24.5, y0, y1, 42.5, 44.5 + E)]          # tank end closures
    W += wall(0.3, 2.6, y0, y1, axis="z", line=57.5, t=1.0) + wall(13.2, 14.7, y0, y1, axis="z", line=57.5, t=1.0)   # bowling acoustic wall stubs
    W += wall(0.3, 14.7, y0, y1, axis="z", line=77, t=.3, openings=[(2, 4.5, 3.0)])
    W += wall(0.3, 14.7, y0, y1, axis="z", line=84.5, t=1.0, piers=[(7.8, 9.2)])                 # AXE 1 target wall (TC-S3 inside)
    W += wall(0.3, 14.7, y0, y1, axis="z", line=93.85, t=.3, openings=[(0.6, 2.5, 3.0)])
    W += wall(0.3, 14.7, y0, y1, axis="z", line=101.5, t=1.0, piers=[(7.8, 9.2)])                # AXE 2 target wall (TC-S4 inside)
    W += wall(64.3, 78.7, y0, y1, axis="z", line=44, openings=[(70, 72.5, 3.0)])
    W += wall(64.3, 78.7, y0, y1, axis="z", line=102, openings=[(70, 72.5, 3.0)])
    return [("Walls_F1", SL, m) for m in W]

def walls_f2():
    y0, y1 = F2 - E, F3 - SLAB[F3] + E; W = []; P = []
    aqp30 = [(z - .3, z + .3) for z in AQ_Z if z not in SKIP_X30]; aqp0 = [(z - .3, z + .3) for z in AQ_Z if z not in SKIP_X0]
    W += wall(30, 113, y0, y1, axis="x", line=15, side=-1, openings=[(66.5, 76.5, y1), (44, 46, F2 + 2.4), (86.3, 89, F2 + 2.4)])
    W += wall(30, 113, y0, y1, axis="x", line=64, side=1, openings=[(66.5, 76.5, y1), (50, 53, F2 + 3.0), (90, 93, F2 + 3.0)])
    W += wall(0.3, 78.7, y0, y1, axis="z", line=30, side=-1, openings=[(34.5, 44.5, y1)], piers=aqp30)
    W += wall(0.3, 78.7, y0, y1, axis="z", line=113, side=1, openings=[(34.5, 44.5, y1), (24, 27, F2 + 3.0), (52, 55, F2 + 3.0), (70, 73, F2 + 3.0)])
    win = [(22, 29.5), (31, 33.8), (45.2, 47.8), (49.2, 55.5)]                                     # gallery viewing windows (scissor)
    W += wall(20.6, 58.4, y0, y1, axis="z", line=0, openings=[(a, b, F2 + 3.0, F2 + 1.0) for a, b in win] + [(35, 44, F2 + 3.0), (56, 58.4, F2 + 3.0)], piers=aqp0)
    P += [box(-.011, .011, F2 + 1.0 - E, F2 + 3.0 + E, a - E, b + E) for a, b in win]
    W += wall(20.6, 58.4, y0, y1, axis="z", line=-6, t=.2, openings=[(26, 28, F2 + 2.2), (38, 40, F2 + 2.2), (50, 52, F2 + 2.2)])
    W += wall(30, 57, y0, y1, axis="x", line=10.5, side=1, t=.2, openings=[(40, 42, F2 + 2.2)])    # climbing changing wall
    W += wall(0.3, 14.7, y0, F2 + 5.0, axis="z", line=84.5, t=.3, side=1, piers=[(7.8, 9.2)])     # kids' wall backing (TC-S3 pillar)
    W += wall(0.3, 14.7, y0, F2 + 4.5, axis="z", line=94, t=.3, side=-1, openings=[(13.4, 14.7, F2 + 2.2)])  # training wall backing
    W += wall(64.3, 78.7, y0, y1, axis="z", line=44, openings=[(70, 72.5, F2 + 2.4)])
    W += wall(64.3, 78.7, y0, y1, axis="z", line=102, openings=[(70, 72.5, F2 + 2.4)])
    return [("Walls_F2", SL, m) for m in W] + [("Gallery_Window_Scissor", SCR, m) for m in P]

def walls_f3():
    y = F3 - E; W = []
    for a, b in ((36, 57), (76.5, 86), (92, 107)):            # WC under the S stand: rear face Z 9.1 (doors), front Z 15, ends
        W += wall(a, b, y, F3 + 4.4, axis="x", line=9.1, side=1, t=.2, openings=[(a + 1, a + 2.5, F3 + 2.2), (b - 2.5, b - 1, F3 + 2.2)])
        W += wall(a, b, y, F3 + 2.5, axis="x", line=15, side=-1, t=.2)
        W += [box(a, a + .2, y, F3 + 3.4, 9.3 + E, 14.8 - E), box(b - .2, b, y, F3 + 3.4, 9.3 + E, 14.8 - E)]
    for a, b in ((36, 58), (76.5, 86), (92, 107)):            # N
        W += wall(a, b, y, F3 + 4.4, axis="x", line=69.9, side=-1, t=.2, openings=[(a + 1, a + 2.5, F3 + 2.2), (b - 2.5, b - 1, F3 + 2.2)])
        W += wall(a, b, y, F3 + 2.5, axis="x", line=64, side=1, t=.2)
        W += [box(a, a + .2, y, F3 + 3.4, 64.2 + E, 69.7 - E), box(b - .2, b, y, F3 + 3.4, 64.2 + E, 69.7 - E)]
    W += wall(21, 34, y, F3 + 4.4, axis="z", line=24.1, side=1, t=.2, openings=[(22, 23.5, F3 + 2.2), (31.5, 33, F3 + 2.2)])
    W += wall(21, 34, y, F3 + 2.5, axis="z", line=30, side=-1, t=.2)
    W += [box(24.3 + E, 29.8 - E, y, F3 + 3.4, 21, 21.2), box(24.3 + E, 29.8 - E, y, F3 + 3.4, 33.8, 34)]
    W += wall(21, 34, y, F3 + 4.4, axis="z", line=118.9, side=-1, t=.2, openings=[(22, 23.5, F3 + 2.2), (31.5, 33, F3 + 2.2)])
    W += wall(21, 34, y, F3 + 2.5, axis="z", line=113, side=1, t=.2)
    W += [box(113.2 + E, 118.7 - E, y, F3 + 3.4, 21, 21.2), box(113.2 + E, 118.7 - E, y, F3 + 3.4, 33.8, 34)]
    return [("WC_Shells_F3", SL, m) for m in W]

def columns():
    it = []
    for x in PT_X:
        for z in PT_Z:
            it.append(("PT_Columns", G, column(x, z, -E, F3 - 1.5 + E, .9)))
            for y0 in (F1 + .05, F2 + .05): it += [("Column_Pads", PAD, m) for m in pads(x, z, y0, 1.95, .9)]
    it.append(("PT_Columns", G, column(71.5, 39.5, -E, F2 - 1.1 + E, .6))); it += [("Column_Pads", PAD, m) for m in pads(71.5, 39.5, .05, 1.95, .6)]
    for z in AQ_Z:
        if z not in SKIP_X0: it.append(("Aquatic_Columns", G, column(0, z, -E, 9.7 + E, .6)))
        if z not in SKIP_X30: it.append(("Aquatic_Columns", G, column(30, z, -E, 9.7 + E, .6)))
    for z in [9.5 + 8*k for k in range(8)]: it.append(("E_Band_Columns", G, column(126.5, z, -E, F3 - 1.0 + E, .6)))
    return it

def truss():   # 30 m Warren transfer truss, local X 0..30 -> centred; soffit y 0 (= +9.7), top chord to +2.0 (under the F3 slab)
    L = 30.0; P = []; h0, h1 = .2, 1.8
    P += [box(-L/2, L/2, 0, .4, -.3, .3), box(-L/2, L/2, 1.6, 2.0, -.3, .3)]
    xs = np.linspace(-L/2, L/2, 11)
    for i, x in enumerate(xs):
        P.append(box(x - .15, x + .15, .4 - E, 1.6 + E, -.2, .2))
        if i < 10: P.append(beam((x, h0 + .1, 0), (xs[i + 1], h1 - .1, 0) if i % 2 == 0 else (xs[i + 1], h0 + .1, 0), .26, .26) if False else beam((x, h0 + .1, 0) if i % 2 == 0 else (x, h1 - .1, 0), (xs[i + 1], h1 - .1, 0) if i % 2 == 0 else (xs[i + 1], h0 + .1, 0), .26, .26))
    P += [box(-L/2, -L/2 + .6, -E, 2.0, -.35, .35), box(L/2 - .6, L/2, -E, 2.0, -.35, .35)]          # bearing ends over the X 0 / X 30 columns
    led = [box(-L/2 + .7, L/2 - .7, -.02, E, -.06, .06)]
    return [("Truss_Steel", G, P), ("Truss_Soffit_LED", CY, led)]

def coffer():
    x0, x1, z0, z1 = 0, 30, 21.8, 30.2; P = [box(x0, x1, F3 - .28, F3, z0, z1)]; R_ = []; L_ = []
    gx = np.arange(x0 + 1.5, x1 - .01, 1.5); gz = np.linspace(z0, z1, 7)[1:-1]
    R_ += [box(x - .1, x + .1, F3 - .4, F3 - .28 + E, z0 + .05, z1 - .05) for x in gx]
    R_ += [box(x0 + .05, x1 - .05, F3 - .4, F3 - .28 + E, z - .1, z + .1) for z in gz]
    R_ += [box(x0, x1, F3 - .45, F3 - .28 + E, z0, z0 + .3), box(x0, x1, F3 - .45, F3 - .28 + E, z1 - .3, z1)]
    xe = np.r_[x0, gx, x1]; ze = np.r_[z0 + .3, gz, z1 - .3]
    for a, b in zip(xe[:-1], xe[1:]):
        for c, d in zip(ze[:-1], ze[1:]):
            L_.append(box(a + .35, b - .35, F3 - .3, F3 - .28 + E, c + .35, d - .35))
    return [("Coffer_Plate", CON, P), ("Coffer_Ribs", SL, R_), ("Coffer_Lights", CY, L_)]

def void_guard():
    y = F3; K, PO, RA, PA = [], [], [], []
    runs = [((35, 3), (57, 3)), ((35, 3), (35, 8)), ((57, 3), (57, 8))]
    for (ax, az), (bx, bz) in runs:
        alongx = az == bz; L = abs(bx - ax) if alongx else abs(bz - az); n = int(np.ceil(L / 2.0)); s = np.linspace(0, L, n + 1)
        o = (az if alongx else ax)
        if alongx: K.append(box(ax - .06, bx + .06, y - E, y + .1, o - .06, o + .06)); RA.append(box(ax - .04, bx + .04, y + 1.01, y + 1.07, o - .04, o + .04))
        else: K.append(box(o - .06, o + .06, y - E, y + .1, az + .06, bz - .06)); RA.append(box(o - .04, o + .04, y + 1.01, y + 1.07, az + .04, bz - .04))
        for i, t in enumerate(s):
            if not alongx and i == 0: continue
            px, pz = (ax + t, o) if alongx else (o, az + t)
            PO.append(box(px - .03, px + .03, y + .1 - E, y + 1.01 + E, pz - .03, pz + .03))
        for a, b in zip(s[:-1], s[1:]):
            if alongx: PA.append(box(ax + a + .022, ax + b - .022, y + .098, y + .98, o - .01, o + .01))
            else: PA.append(box(o - .01, o + .01, y + .098, y + .98, az + a + (.065 if a == 0 else .022), az + b - .022))
    # r1: N-edge stubs at Z 8 over the 1 m gaps the lead wall leaves (panels X 36.0..56.0); each owns its corner and stops 0.02 m short of the panels
    for c, e, sg in ((35, 35.95, 1), (57, 56.05, -1)):
        lo, hi = sorted((c - sg*.06, e + sg*.03)); K.append(box(lo, hi, y - E, y + .1, 8 - .06, 8 + .06))
        lo, hi = sorted((c + sg*.04, e + sg*.03)); RA.append(box(lo, hi, y + 1.01, y + 1.07, 8 - .04, 8 + .04))
        PO.append(box(e - .03, e + .03, y + .1 - E, y + 1.01 + E, 8 - .03, 8 + .03))
        lo, hi = sorted((c + sg*.022, e - sg*.022)); PA.append(box(lo, hi, y + .098, y + .98, 8 - .01, 8 + .01))
    return [("Guard_Kerb", SL, K), ("Guard_Posts", G, PO), ("Guard_Rail", ST, RA), ("Guard_Pane_Scissor", SCR, PA)]

def climb_frame():
    P = [box(x - .15, x + .15, F2 - E, 17.6, 8.17, 8.67) for x in (36, 42, 46, 51, 56)]
    G2 = []
    for y in [F2 + 2.3, F2 + 4.6, F2 + 6.9, F2 + 9.2, 17.36]:
        G2 += [box(a + .15 - E, b - .15 + E, y - .12, y + .12, 8.22, 8.57) for a, b in ((36, 42), (42, 46), (46, 51), (51, 56))]
    return [("WCL_Posts", G, P), ("WCL_Girts", ST, G2)]

def plant_stack(mirror=False):  # local 12 (X) x 10 (Z), facade sides -X/-Z inset 0.4; door face +Z (towards the building)
    x0, x1, z0, z1 = -6 + .4, 6, -5 + .4, 5; t = .3; top = 25.4; W = []
    door = lambda y: (-.6, 1.4, y + 2.4, y)
    for y0, y1 in ((0, F2), (F2, F3), (F3, top)):
        W += wall(x0, x1, y0 - (E if y0 == 0 else 0), y1, axis="x", line=z1, side=-1, t=t, openings=[(-.6, 1.4, y0 + 2.4)])
    W += [box(x0, x1, -E, top, z0, z0 + t), box(x0, x0 + t, -E, top, z0 + t - E, z1 - t + E), box(x1 - t, x1, -E, top, z0 + t - E, z1 - t + E)]
    FL = [box(x0 + t - E, x1 - t + E, y - .25, y, z0 + t - E, z1 - t + E) for y in (F2, F3)]
    HZ = [box(x0 - .02, x1 + .02, top - .5, top - .2, z0 - .02, z0 + E), box(x0 - .02, x1 + .02, top - .5, top - .2, z1 - E, z1 + .02)]
    LV = []
    for y in np.linspace(top + .25, 27.45, 7):
        LV += [box(x0 + .1, x1 - .1, y - .05, y + .05, z0 + .05, z0 + .2), box(x0 + .1, x1 - .1, y - .05, y + .05, z1 - .2, z1 - .05)]
        LV += [box(x0 + .05, x0 + .2, y - .05, y + .05, z0 + .25, z1 - .25), box(x1 - .2, x1 - .05, y - .05, y + .05, z0 + .25, z1 - .25)]
    PO = [box(x - .15, x + .15, top - E, 27.6 + E, z - .15, z + .15) for x in (x0 + .15, x1 - .15) for z in (z0 + .15, z1 - .15)]
    CAP = [box(x0 - .1, x1 + .1, 27.6, 28.0, z0 - .1, z1 + .1)]
    parts = [("Stack_Walls", SL, W), ("Stack_Gratings", ST, FL), ("Hazard_Band", AM, HZ), ("Louvre_Blades", G, LV), ("Louvre_Blades", G, PO), ("Cap_Slab", WH, CAP)]
    if mirror:
        for _, _, ms in parts:
            for m in ms: m.vertices[:, 0] *= -1; m.invert()
    return parts

def roof_edge(L=4.0, chord=True):   # local: length along X, +Z outward; y 0 = bottom chord centre level (tile datum)
    P = [box(-L/2, L/2, 2.95, 3.35, .25, .55), box(-L/2, L/2, 3.35 - E, 3.45, .51, .55)]            # gutter box + lip
    F = [box(-L/2, L/2, 2.4, 3.0 + E, .55 - E, .62)]                                                   # fascia
    C = [box(-L/2, L/2, 2.7, 2.76, .62 - E, .64)]                                                      # cyan edge line
    parts = [("Gutter", G, P), ("Fascia", WH, F), ("Edge_LED", CY, C)]
    if chord: parts.append(("Edge_Chord", G, [tube((-L/2, 3.175, 0), (L/2, 3.175, 0), .11, 8)]))
    return parts

def roof_closure(chord=False):      # 4.0 (X) x 1.5 (Z) strip, local +Z outward (gutter side), inner edge z -0.75
    P = [tube((-2, 3.175, .75), (2, 3.175, .75), .11, 8), tube((-2, 3.175, -.75 + .11), (-2, 3.175, .75 - .11), .09, 8)]
    if chord: P.append(tube((-2, 3.175, -.75), (2, 3.175, -.75), .11, 8))
    N = [node((-2, 3.175, .75), .175, -1)]
    GLs = [box(-1.98, 0 - .01, 3.3, 3.32, -.73, .73), box(.01, 1.98, 3.3, 3.32, -.73, .73)]
    GB = [box(-.01 - E, .01 + E, 3.29, 3.33, -.74, .74)]
    E_ = roof_edge(4.0, chord=False)
    for _, _, ms in E_:
        for m in ms: m.apply_translation((0, 0, .70))
    return [("Closure_Frame", G, P + N), ("Glass_Closure_Roof", GL, GLs), ("Glazing_Bar", ST, GB)] + E_

def roof_corner():                  # 1.5 m gutter return + corner node post, local +Z / +X outward corner
    parts = roof_edge(1.5, chord=False)
    parts.append(("Corner_Node", G, [node((.75, 3.175, 0), .2, 0)]))
    parts.append(("Corner_Downpipe", ST, [tube((.75, -1.5, .4), (.75, 2.95 + E, .4), .08, 8)]))
    return parts

def roof_bay4():                    # one 4 x 4 m space-frame bay (square-on-square), owns its -X / -Z top edges like tt_roof_bay
    T = [tube((-2, 3.175, -2), (2, 3.175, -2), .11, 8), tube((-2, 3.175, -2), (-2, 3.175, 2), .11, 8)]
    B = [tube((0, .175, -2), (0, .175, 2), .11, 8), tube((-2, .175, 0), (2, .175, 0), .11, 8)]
    D = [tube((0, .175, 0), c, .084, 6) for c in ((-2, 3.175, -2), (2, 3.175, -2), (-2, 3.175, 2), (2, 3.175, 2))]
    N = [node((-2, 3.175, -2), .175, -1), node((0, .175, 0), .175, -1)]
    GLs = [box(-1.98, -.01, 3.3, 3.32, -1.98, 1.98), box(.01, 1.98, 3.3, 3.32, -1.98, 1.98)]
    LED = [box(-2, 2, 3.31, 3.35, -2.03, -1.97)]
    return [("Bay_Frame", G, T + B + D + N), ("Glass_Bay_Roof", GL, GLs), ("Bay_Grid_LED", CY, LED)]

def f3_corner_closure():            # 1.5 m Glass Box closure bay, 13.3 m, local +Z outward, glass plane z +0.285 like tt_curtain_wall_panel
    F = [box(x - .0125, x + .0125, .15 - E, 13.15 + E, -.31, .27 + E) for x in (-.7375, .7375)]
    T = [box(-.725 + E, .725 - E, y - .075, y + .075, -.05, .27 + E) for y in (3.325, 6.65, 9.975)]
    S = [box(-.75, .75, 0, .15, -.31, .32), box(-.75, .75, 13.15, 13.3, -.31, .32)]
    GLs = [box(-.72, .72, a + .08, b - .08, .27, .30) for a, b in ((.15, 3.325), (3.325, 6.65), (6.65, 9.975), (9.975, 13.15))]
    return [("Closure_Fins", G, F), ("Closure_Transoms", WH, T), ("Closure_Sill_Head", SL, S), ("Glass_Closure_Pane", GL, GLs)]

def ball_net():                     # 16 x 15 m tile, y 0 = net plane (hang at +21.5), rods to +1.0 (space-frame soffit +22.5)
    Nn = [box(-8, 8, -.005, .005, -7.5, 7.5)]; Nn[0].metadata["uv"] = np.c_[Nn[0].vertices[:, 0] / .4, Nn[0].vertices[:, 2] / .4]   # planar UV: 0.1 m mesh cells
    C = [tube((-8, 0, z), (8, 0, z), .02, 6) for z in (-7.5, 7.5)] + [tube((x, 0, -7.5), (x, 0, 7.5), .02, 6) for x in (-8, 8)]
    Rd = [tube((x, .02, z), (x, 1.0, z), .012, 5) for x in (-7.9, 0, 7.9) for z in (-7.4, 7.4)]
    return [("Net_Scissor", NET, Nn), ("Net_Cables", ST, C), ("Net_Hangers", G, Rd)]

if __name__ == "__main__":
    pack("tt_struct_f1_slab", f1_slab(), REP, LAY, note="F1 slab, aquatic decks +2.0/+1.0, diving pit, deck steps")
    pack("tt_struct_f2_slab", f2_slab(), REP, LAY, note="F2 slab, gallery, view/slide bridge decks, downstands")
    pack("tt_struct_f3_slab", f3_slab(), REP, LAY, note="F3 slab, PT band beams, climbing-void trimmers")
    pack("tt_struct_f1_walls", walls_f1(), REP, LAY, note="F1 partitions + openings")
    pack("tt_struct_f2_walls", walls_f2(), REP, LAY, note="F2 partitions + openings, scissor gallery windows")
    pack("tt_struct_f3_walls", walls_f3(), REP, LAY, note="F3 under-stand WC shells")
    pack("tt_struct_columns", columns(), REP, LAY, note="PT / runoff / aquatic / E-band columns + pads")
    pack("tt_struct_climb_frame", [(pn, mk, m) for pn, mk, ms in climb_frame() for m in ms], REP, LAY, note="W-CL 20 x 11.5 m wall frame")
    pack("tt_struct_void_guard", [(pn, mk, m) for pn, mk, ms in void_guard() for m in ms], REP, LAY, note="F3 climbing-void guard 1.07 m, scissor panes")
    pack("tt_struct_diving_coffer", [(pn, mk, m) for pn, mk, ms in coffer() for m in ms], REP, LAY, note="diving-well coffer plate, soffit +11.8")
    KIT = [("tt_struct_aquatic_truss", truss(), "transfer truss T-W1..9, place X 15, Z 3.5+9k, y +9.7"),
           ("tt_struct_plant_stack", plant_stack(False), "SW (yaw 0) / NE (yaw 180)"), ("tt_struct_plant_stack_m", plant_stack(True), "SE (yaw 0) / NW (yaw 180)"),
           ("tt_struct_roof_edge", roof_edge(4.0, False), "W edge (+Z out), no chord (tile owns it)"), ("tt_struct_roof_edge_chord", roof_edge(4.0, True), "E edge, closes the unowned +X chord"),
           ("tt_struct_roof_closure", roof_closure(False), "S 1.5 m closure strip"), ("tt_struct_roof_closure_chord", roof_closure(True), "N 1.5 m closure strip (closes Z 77.5 chord)"),
           ("tt_struct_roof_corner", roof_corner(), "4 corner gutter returns"), ("tt_struct_roof_bay4", roof_bay4(), "4 x 4 m infill bay for the 3-bay X strip / 4-bay Z strip"),
           ("tt_struct_f3_corner_closure", f3_corner_closure(), "W/E faces Z 0..1.5 / 77.5..79"), ("tt_struct_ball_net", ball_net(), "F3 ball net 16 x 15 tile, y +21.5")]
    for nm, parts, note in KIT:
        col = [("Struct-colonly", [m.copy() for pn, mk, ms in parts if mk in (SL, G, WH, CON) and "Stack" in pn for m in ms])] if "plant" in nm else None
        export_chunk(nm, parts, col, REP, note=note)
    import ramps
    ramps.export("tt_struct_pool_ramp", ramps.pool_ramp(), REP, LAY, "r4 Rev 3.5 pool-deck switchback F1 -> +2.0, guards + rails")
    ramps.export("tt_struct_leisure_ramp", ramps.leisure_ramp(), REP, LAY, "r4 Rev 3.5 leisure S-strip ramp F1 -> +1.0, guards + rails")
    json.dump(LAY, open(LAYOUT, "w"), indent=1)
    rd = os.path.join(RENDER_OUT, "structure_blockout"); os.makedirs(rd, exist_ok=True); json.dump(REP, open(os.path.join(rd, "struct_report.json"), "w"), indent=1, default=str)
    bad = [r["asset"] for r in REP if not r["passed"]]; print("ASSETS", len(REP), "FAILED", bad, "TRIS", sum(r["tris"] for r in REP))
