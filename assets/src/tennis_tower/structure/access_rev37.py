"""Rook r8 (2026-11-15): spec Rev 3.7 (Vance 059db69) access pieces, building coords (X axial, Z across, Y up, F1 = 0).
#1 SW / NW switchback ramps + W grand stair, #2 E ramp + E stair (V1 Court Line: stair slate legs/treads, white/amber court
lines, alloy rails + ball finials, scissor-glass guards; solid cast fill to the drum). Terrace edge opening variants (V1 kit,
guard/kerb removed over the opening, deck flush). Every piece carries '*-colonly' colliders. Exports via struct_lib.export_chunk
and records world offsets in tt_struct_layout.json (assemble_preview.structure() places every layout entry); the edge variants
are swapped in assemble_preview.site().  Run: python3 access_rev37.py"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from struct_lib import *
from ridge_crown import huv
import ramps as RP
from ramps import Kit, RH, RR, RO, GT, strip
import terrace as T
from terrace import DK

def drum(z):          # walkable drum floor in the building frame (spec Rev 3.7 #1; true circle, facets add <= 8 mm)
    return 195.9592 - math.sqrt(40000.0 - (z - 40.0)**2)

def prism(x0, x1, z0, z1, top, ybot):
    """closed hull from ybot up to a top surface given at the 4 corners top(x, z) (planar or gently warped)."""
    return huv([(x, y, z) for x in (x0, x1) for z in (z0, z1) for y in (ybot, top(x, z))])

def pw(xs, ys):       # piecewise-linear profile along X
    return lambda x, z=0.0: float(np.interp(x, xs, ys))

# ------------------------------------------------------------------ #1 / #2 switchback ramps
def U(ms):
    """boolean union (manifold) of overlapping closed solids -> one closed mesh, huv-style projected UVs (no internal / coplanar faces)."""
    def vol(x):
        y = trimesh.Trimesh(np.asarray(x.vertices), np.asarray(x.faces), process=True); y.merge_vertices(); trimesh.repair.fix_normals(y); return y
    m = trimesh.boolean.union([vol(x) for x in ms], engine="manifold") if len(ms) > 1 else ms[0].copy()
    m.metadata["uv"] = m.vertices[:, [0, 2]] / 2.0 + m.vertices[:, [1, 1]] * [0, .5]; return m

L1, L2, L3 = -.559, -1.118, -1.678     # 3 runs x 0.559 over 6.71 m (1:12)
# r8b Rev 3.7.1 #5: lane B run 3 (1:12) ends on a LEVEL 1.5 m foot landing; the drum cross-falls 0.30 m (1:6.4) across the 1.95 m lane
# at Z 8.3..10.25, so a level landing at the mean drum height would leave the drum 0.15 m proud of its S half (flagged to Vance);
# the landing is set to the highest drum point under it (Z 8.3 edge, circle + 3 mm, facets <= 7.6 mm lower) and a 1:20 terrain fillet
# (part of the deck, colonly) runs off its open E end down onto the drum. S side meets the drum flush; N side is the median.
LF = drum(8.3) + .003                  # foot landing level
XE = -41.92 + (L2 - LF) * 12.0         # run 3 end / landing start (1:12)
XF = XE + 1.5                          # landing end, fillet start
def fillet(x0, z0, z1, ytop, ybot, dz=.1):
    """<= 1:20 apron from a level edge (x = x0, height ytop) down +X onto the drum, in Z strips (each strip runs until the plane meets
    the drum + 3 mm at its lower-drum side; strips overlap 1 cm and are unioned by the caller)."""
    out = []; zs = list(np.arange(z0, z1 - 1e-6, dz)) + [z1]
    for za, zb in zip(zs[:-1], zs[1:]):
        zl = za if drum(za) < drum(zb) else zb                # lower drum side -> longest run
        l = max((ytop - drum(zl) - .003) * 20.0, .02)
        top = lambda x, z: max(ytop - (x - x0) / 20.0, drum(z) + .003)
        out.append(prism(x0 - .01, x0 + l, max(z0, za - .005), min(z1, zb + .005), top, ybot))
    return out
def ramp_sw():
    """SW ramp in its own frame (= building coords of the SW ramp). NW = mirror Z about 40, E = mirror X about 64."""
    k = Kit()
    YB = drum(13.5) - .12                                    # common fill bottom (lowest drum point under the footprint - 0.12)
    xA = [-43.42, -41.92, -35.21, -33.71, -27.0, -25.0]; yA = [L2, L2, L1, L1, 0.0, 0.0]
    fA = pw(xA, yA)                                          # lane A walk line (turn -> run 2 -> landing -> run 1 -> top landing)
    fBn = pw([-43.42, -41.92, XE, XF], [L2, L2, LF, LF])
    def fB(x, z):
        return fBn(x) if x <= XF else max(LF - (x - XF) / 20.0, drum(z) + .003)
    D = []
    for a, b in zip(xA[:-1], xA[1:]):                        # lane A Z 10.5..12.3 (segments overlap 2 cm, unioned)
        D.append(prism(a - .02 if a > -43 else a, b, 10.5, 12.3, lambda x, z: fA(x), YB))
    # Top landing: solid fill only under lane A (Z 10.5..12.30). The 1.15 m alley between
    # lane A's N face (Z 12.30) and the terrace-skirt south face (Z 13.45, Skirt-colonly) is
    # the --qa-ring S-face drum lane (player pinned at bldg (155.4, -2.3, 12.9) when the fill
    # ran to Z 13.37). A 0.08 m deck bridges the alley (headroom 2.03 m at Z 12.30, 2.12 m at
    # 12.90; capsule 1.75) so the landing still meets the terrace; the cantilever over the
    # skirt cap is unchanged. SW/NW mirrors keep the same undercroft on the N/S edges.
    D.append(prism(-27.0, -25.0, 10.5, 12.30, lambda x, z: 0.0, YB))        # solid fill under lane A
    D.append(prism(-27.0, -25.0, 12.30 - .01, 13.37, lambda x, z: 0.0, -.08))  # thin deck over the ring lane
    D.append(box(-27.0, -25.0, -.29, 0.0, 13.3, 13.5))                       # cantilever slab over the skirt cap (top -0.30)
    D.append(prism(-43.42, -41.9, 8.3, 12.3, lambda x, z: L2, YB))           # turn landing spans both lanes
    D.append(prism(-41.92, XE, 8.3, 10.25, fB, YB))                          # lane B run 3
    D.append(prism(XE - .01, XF, 8.3, 10.25, lambda x, z: LF, YB))           # level 1.5 m foot landing
    D += fillet(XF, 8.3, 10.25, LF, YB)                                      # 1:20 terrain fillet off the open E end
    deck = U(D); k.add("Ramp_Deck", SSL, deck); k.col(deck.copy())
    # cast walls 1.07 over lane A: N cheek Z 12.3..12.5 (X -43.42..-27); median Z 10.25..10.5 stops at the turn landing X -41.92
    # (Rev 3.7 lists the median as X -43.42..-25.0, which would cut the turn landing: flagged to Vance)
    def wall(xs, z0, z1):
        return [huv([(x, y, z) for x in (a, b) for z in (z0, z1) for y in (YB + E, fA(x) + GT)]) for a, b in zip(xs[:-1], xs[1:])]
    W = wall([-43.43, -41.92, -35.21, -33.71, -27.0 + E], 12.3 - 2 * E, 12.5) + wall([-41.9 + E, -35.21, -33.71, -27.0, -25.0 - E], 10.25 - 2 * E, 10.5 + 2 * E)
    w = U(W); k.add("Ramp_Walls", SL, w); k.col(w.copy())
    CAP = [huv([(x, y, z) for x in (m.bounds[0][0], m.bounds[1][0]) for z in (m.bounds[0][2] - .01, m.bounds[1][2] + .01)
                for y in (fA(x) + GT - E, fA(x) + GT + .03)]) for m in W]
    k.add("Wall_Caps", ALY, U(CAP))
    # glass guards: S edge (turn landing / run 3 / warped tail), turn landing W end, top landing E edge + its W return
    bS = lambda t: fB(t, 8.3) if t > -41.92 else L2
    k.guard(-43.42, -41.92, 8.375, "x", bS, lambda t: bS(t) + GT, (True, True), kerb=False)
    k.guard(-41.92, XE, 8.375, "x", bS, lambda t: bS(t) + GT, (False, True), kerb=False)
    k.guard(XE, XE + .35, 8.375, "x", bS, lambda t: bS(t) + GT, (False, True), kerb=False)
    k.guard(8.45, 12.3 - 2 * E, -43.37, "z", lambda t: L2, lambda t: L2 + GT, (False, False))
    k.guard(10.5 + 2 * E, 13.44, -25.05, "z", lambda t: 0.0, lambda t: GT, (False, True))
    k.guard(12.5, 13.44, -26.95, "z", lambda t: 0.0, lambda t: GT, (False, False))
    # court lines (V1): white centre line per run, amber run-end bands
    CL = [strip(-33.61, -27.1, 11.375, 11.425, fA, "x"), strip(-41.82, -35.31, 11.375, 11.425, fA, "x"), strip(-41.82, XE - .1, 9.325, 9.375, fBn, "x")]
    AL = [strip(a, a + .05, z0 + .05, z1 - .05, f, "x") for a, f, z0, z1 in ((-27.06, fA, 10.5, 12.3), (-33.70, fA, 10.5, 12.3), (-35.26, fA, 10.5, 12.3),
                                                                             (-41.91, fA, 10.5, 12.3), (-41.91, fBn, 8.45, 10.25), (XE, fBn, 8.45, 10.2))]
    k.add("Court_Lines", WH, *CL); k.add("Court_Line_Amber", AM, *AL)
    # handrails both sides of each lane (0.865 m), 0.3 m extensions
    pa = [(-26.7, RH), (-27.0, RH), (-33.71, L1 + RH), (-35.21, L1 + RH), (-41.92, L2 + RH), (-42.22, L2 + RH)]
    k.rail(pa, 12.3 - RO, "x", 12.3 - 2 * E); k.rail(pa, 10.5 + RO, "x", 10.5 + 2 * E)
    pb = [(-42.22, L2 + RH), (-41.92, L2 + RH), (XE, LF + RH), (XE + .3, LF + RH)]
    k.rail(pb, 10.25 - RO, "x", 10.25 - 2 * E); k.rail(pb, 8.45 + RO, "x", 8.375 + .035)
    return k, fB

def mirror(k, M):
    for _, _, m in k.I: uv = m.metadata.get("uv"); m.apply_transform(M); m.metadata["uv"] = uv
    for m in k.C: m.apply_transform(M)
    return k
MZ = np.diag([1, 1, -1, 1.0]); MZ[2, 3] = 80.0          # Z' = 80 - Z  (NW)
MX = np.diag([-1, 1, 1, 1.0]); MX[0, 3] = 128.0          # X' = 128 - X (E: -27 -> 155, -43.42 -> 171.42)

# ------------------------------------------------------------------ grand stairs
def stair(x_top, sgn, z0, z1, n1, n2, land, centre_rail):
    """x_top: flight-1 start (outer end of the 1.0 m top landing), descending along sgn*X. 23 risers x 0.1752, 0.30 treads,
    flight 1 = n1 risers, landing `land`, flight 2 = n2 risers onto a 2 m foot pad warped to the drum."""
    k = Kit(); R, TR = 4.0296 / 23, .30; YB = min(drum(z0), drum(z1)) - .12
    xs = lambda a, b: (min(a, b), max(a, b))
    land_top = x_top - sgn * 1.0; sk = land_top + sgn * .12  # skirt climbing face / holds reach 0.11 m past the edge face
    D = [box(*xs(sk, x_top), YB, 0.0, z0, z1), box(*xs(land_top, sk + sgn * .02), -.29, 0.0, z0, z1)]
    NOS = []; x = x_top; y = 0.0
    for i in range(n1 + n2 - 1):
        y -= R; w = land if i == n1 - 1 else TR
        D.append(box(*xs(x - sgn * .02, x + sgn * w), YB, y, z0, z1))
        if i != n1 - 1: NOS.append(box(*xs(x + sgn * .008, x + sgn * .05), y - E, y + .004, z0 + .05, z1 - .05))
        x += sgn * w
    foot0, foot1 = x, x + sgn * 2.0; yl = y - R               # last riser lands on the pad (-4.0296), pad warps to the drum by its far end
    D.append(huv([(xx, yy, zz) for xx in (foot0 - sgn * .02, foot1) for zz in (z0, z1) for yy in (YB, (yl if xx != foot1 else drum(zz) + .003))]))
    body = U(D); k.add("Stair_Body", SSL, body); k.add("Nosing_Court_Line", WH, *NOS)
    f1 = (n1 - 1) * TR; d2 = f1 + land; d3 = d2 + (n2 - 1) * TR
    # TTQA-052: smooth Flight_Ramp-style collider along the nosing line (cores never snag) instead of the stepped tread body:
    # top landing flat, flight 1 nosing line 0 -> -n1*R reached one tread onto the landing, landing flat, flight 2 the same onto the pad.
    RP = [(0.0, 0.0), (f1 + TR, -n1 * R), (d2, -n1 * R), (d3 + TR, -(n1 + n2) * R)]
    ramp = [huv([(x_top + sgn * dd, yy, zz) for dd, yt in (RP[j], RP[j + 1]) for zz in (z0, z1) for yy in (YB, yt)]) for j in range(3)]
    k.col(D[0].copy(), D[1].copy(), *ramp, D[-1].copy())
    PD = [0, f1, f1 + .001, d2, d3, d3 + .001, d3 + 2.0]; PY = [0, -(n1 - 1) * R, -n1 * R, -n1 * R, -(n1 + n2 - 1) * R, -(n1 + n2) * R, -(n1 + n2) * R]
    nose = lambda xx: float(np.interp(sgn * (xx - x_top), PD, PY))
    bp = [x_top + sgn * d for d in (0, f1, d2, d3, d3 + 2.0)]
    W, CAP = [], []
    for zi0, zi1 in ((z0 - .2, z0 + E), (z1 - E, z1 + .2)):   # cheek walls overlap the body 4 mm
        W.append(box(*xs(land_top, sk + sgn * .02), -.29, GT, zi0, zi1)); CAP.append(box(*xs(land_top, sk), GT - E, GT + .03, zi0 - .01, zi1 + .01))
        for a, b in zip([sk] + bp[:-1], bp):
            W.append(huv([(xx, yy, zz) for xx in (a, b) for zz in (zi0, zi1) for yy in (YB, (nose(xx) if xx != sk else 0.0) + GT)]))
            CAP.append(huv([(xx, yy, zz) for xx in (a, b) for zz in (zi0 - .01, zi1 + .01) for yy in ((nose(xx) if xx != sk else 0.0) + GT - E, (nose(xx) if xx != sk else 0.0) + GT + .03)]))
    w = U(W); k.add("Cheek_Walls", SL, w); k.col(w.copy()); k.add("Cheek_Caps", ALY, U(CAP))
    rail = [(x_top - sgn * .3, RH)] + [(b, nose(b) + RH) for b in bp[:-1]] + [(bp[-2] + sgn * .3, nose(bp[-2]) + RH)]
    k.rail(rail, z0 + E + RO, "x", z0 + E); k.rail(rail, z1 - E - RO, "x", z1 - E)
    if centre_rail:   # centre handrail on posts (Rev 3.7: W stair 6 m clear -> centre rail at Z 39.5)
        zc = (z0 + z1) / 2; k.rail(rail, zc, "x")
        P = [(xx, nose(xx)) for xx in np.linspace(bp[0] + sgn * .15, bp[-2] - sgn * .15, 9)]
        k.add("Centre_Rail_Posts", ALY, *[tube((xx, yy - E, zc), (xx, yy + RH - RR - .02, zc), .025, 8) for xx, yy in P])
        k.col(*[box(xx - .03, xx + .03, yy, yy + RH, zc - .03, zc + .03) for xx, yy in P])
    return k

# ------------------------------------------------------------------ terrace edge opening variants
def edge_open(a, b, name):
    """tt_terrace_edge with the kerb + guard removed over local X a..b (deck paved flush to the outer face). Same AABB / pivot as tt_terrace_edge."""
    import terrace_final as TF
    p = Part(name); rng = np.random.default_rng(5); h = 2.0; X0, X1 = -h + .001, h - .001; zc0, zc1 = .25, .9
    p.add("Deck_Slab", G, box(X0, X1, 0, .2 + .002, -1.6, zc0 - .002)); TF.deck(p, X0, X1, -1.6, zc0 - .004, rng, medal=False)
    segs = [(u, v) for u, v in ((X0, a - .002), (b + .002, X1)) if v - u > .05]
    K = []; KL = []; KC = []; NR = []; GF = []
    for u, v in segs:
        if v - u < .9: continue
        K += [box(u, v, 0, .36, zc0, zc1 - .06), box(u, v, .36 - E, .4, zc0 + .04, zc1 - .14), box(u, v, .06, .33, zc1 - .06 - E, zc1)]
        KL.append(box(u, v, .2, .24, zc1 - E, zc1 + .007)); KC.append(box(u, v, .4 - E, .404, zc0 + .07, zc0 + .12))
    if K: p.add("Coping_Kerb", SL, *K); p.add("Coping_Line", AM, *KL); p.add("Coping_Court_Line", WH, *KC)
    # opening: flush paved threshold over the coping zone (slab + pavers to DK), amber edge band at the outer face
    a, b = max(a, X0), min(b, X1)
    p.add("Threshold_Slab", G, box(a, b, 0, .2 + .002, zc0 - .002 + E, zc1)); TF.paver_field(p, a, b, zc0 + .002, zc1 - .06, 4, 1, lambda x, z: .2, lambda x, z: DK, rng, tag="_T")
    p.add("Threshold_Amber", AM, box(a + .01, b - .01, DK - .004, DK + .004, zc1 - .055, zc1 - .005))
    q = dict(theme="court"); stubs = []
    for i, (u, v) in enumerate(segs):
        if v - u < .9: stubs.append(box(u, v, 0, 1.47, zc0, zc1 + .007)); continue   # short return: solid kerb pier to guard height
        sub = Part("g"); T.guard(sub, q, u, v, .62, .4)
        for kk, (mk, m) in sub.P.items():
            nm = kk.replace("Guard-convcolonly", f"Guard{i}-convcolonly"); p.add(nm, mk, m)
    if stubs: p.add("Kerb_Pier", SL, *stubs); p.add("Pier-colonly", SL, *[s.copy() for s in stubs])
    p.add("Edge-colonly", SL, *[box(u, v, 0, .36, -1.6, zc1) for u, v in segs] + [box(a, b, 0, DK, -1.6, zc1)])
    return p

def export_part(name, p, REP, LAY=None, note=""):
    parts = [(k, mk, [m]) for k, (mk, m) in p.P.items() if "colonly" not in k]
    cols = [(k, [m]) for k, (mk, m) in p.P.items() if "colonly" in k]
    return export_chunk(name, parts, cols, REP, layout=LAY, note=note)

def export_kit(name, k, REP, LAY, note):
    groups = {}
    for pn, mk, m in k.I: groups.setdefault((pn, mk), []).append(m)
    return export_chunk(name, [(pn, mk, ms) for (pn, mk), ms in groups.items()], [("Access-colonly", k.C)], REP, layout=LAY, note=note)


# ------------------------------------------------------------------ #6 / #7 / #8 guards (1.07 m Court Line glass, kerb -> < 100 mm openings)
F3 = 12.2
def gd(k, a, b, line, axis, y, pe=(True, True)):
    k.guard(a, b, line, axis, lambda t: y, lambda t: y + GT, pe, kerb=True)
def guards_holes():
    """#6 F3 track side of the ST+S1 (X 57..64) and ST+S2 (X 86..92) core holes. Corners: the abutting run starts 0.04 m clear of
    the through run's rail and its kerb 0.09 m clear (no clip). The F3 stand back (Z 9.07) is open under the rake between its
    aisle walls (probed), so the N side gets a guard on Z 9.0 as Rev 3.7 asks."""
    k = Kit(); y = F3
    # TTQA-042 (Rook 2026-11-15): kerb faces kept 3 mm off the slab-hole edges / core outer wall faces (X 64.0, 86.0, 92.0) and the
    # track-bed edge (Z 2.50) instead of flush on them (coplanar contacts); the S runs sit on Z 2.548 so the kerb laps the track bed
    # 2 mm (was 10 mm); the ST+S1 cross guard starts 52 mm off the stand 1696 aisle-wall face (X 59.596; end post r .035, finial r .05)
    # (it ran 0.236 m into it); both cross guards on Z 10.303 so the kerb's S face is 3 mm inside the Top_Landing_Slate edge (Z 10.25), not flush.
    # ST+S1: connector X 57.03 Z 2.503..2.93 closes the 0.36 m gap to the existing void guard kerb (Z 2.94) - not in Rev 3.7
    gd(k, 2.503, 2.93, 57.03, "z", y, (True, False))
    gd(k, 57.07, 64.05, 2.548, "x", y, (False, True)); gd(k, 2.60, 8.92, 64.053, "z", y, (False, False))
    gd(k, 57.06, 64.10, 9.0, "x", y)      # stand-back rail: bears on the TC-S1 trunk clad (X 56.9..58.1), core 988 W/E wall heads and the slab E of X 64
    gd(k, 59.648, 61.0, 10.303, "x", y)   # cross over flight 1 at the top landing; W of it the F3 stand 1696 aisle wall (X 59.015..59.596) closes it
    # ST+S2
    gd(k, 85.9, 92.1, 2.548, "x", y); gd(k, 2.60, 8.92, 85.947, "z", y, (False, False)); gd(k, 2.60, 8.92, 92.053, "z", y, (False, False))
    gd(k, 85.9, 92.1, 9.0, "x", y); gd(k, 86.2, 88.9, 10.303, "x", y)
    return k
def guards_cores():
    """#7 F3 core-top guard rings on the wall heads (y 12.2) + cross guards over flight 1, open at the flight-2 arrival."""
    k = Kit(); y = F3
    for z0, zc in ((9.6, 17.0), (59.4, 66.82)):          # LS a_956 / LN a_958 (X 71..76.5)
        gd(k, 71.0, 76.5, z0, "x", y); gd(k, z0 + .09, zc + .05, 71.1, "z", y, (False, True)); gd(k, z0 + .09, zc - .03, 76.4, "z", y, (False, True))
        gd(k, 71.19, 73.7, zc, "x", y, (False, True))
    # LW a_960 (yaw 90): W X 24.6, S Z 39.1 / N Z 44.4 to X 31.97, cross along X 32.02 over Z 41.8..44.31
    gd(k, 39.0, 44.5, 24.6, "z", y); gd(k, 24.69, 31.97, 39.1, "x", y, (False, True)); gd(k, 24.69, 32.07, 44.4, "x", y, (False, True))
    gd(k, 41.8, 44.31, 32.02, "z", y, (True, False))
    # ST-ARN b_m_980: cross Z 61.30 over X 134.0..136.9, W guard X 134.1 over Z 61.39..69.0 (E side = facade, N side = NE plant stack)
    gd(k, 134.0, 136.9, 61.30, "x", y); gd(k, 61.39, 69.0, 134.1, "z", y, (False, True))
    return k
# TTQA-004 r2: core-top guards for the remaining 11 F2 cores whose F3 top is open to the sky (#7 covered 970/972/974/994, cap_b 978/980).
# Same layout as #7 in each core's local frame (stair_core.stair_full): S wall-head guard, W/E wall-head guards to the top landing,
# cross guard on the top-landing edge over flight 1; open at the flight-2 arrival. (manifest index, cx, cz, yaw, type, z-mirror)
CORES_R2 = [(962, 35.1, 17.75, 90, "A", 1), (964, 107.9, 17.75, 90, "A", 1), (966, 35.1, 61.25, 90, "A", 1), (968, 107.9, 61.25, 90, "A", 1),
            (976, 113.4, 41.75, 90, "A", 1), (982, 61.0, 71.1, 0, "B", 1), (984, 89.0, 71.1, 0, "B", 1), (986, 122.5, 55.3, 0, "B", 1),
            (988, -3.0, 15.3, 0, "B", 1), (990, -3.0, 63.7, 0, "B", -1), (992, 137.0, 15.3, 0, "B", 1)]
def guards_cores_r2(sel):
    CD = {"A": (5.5, 10.2, 2.5), "B": (6.0, 10.6, 2.7)}; k = Kit(); y = F3
    for idx, cx, cz, yaw, ty, mz in CORES_R2:
        if idx not in sel: continue
        W, L, FW = CD[ty]; xi, zi = W/2 - .2, L/2 - .2; zs = -zi; z2t = zs + FW + 17 * .28; zw = zs - .1
        segs = [((-xi - .2, zw), (xi + .2, zw), (True, True)),                    # S wall head
                ((-xi - .1, zw + .09), (-xi - .1, z2t + .09), (False, True)),     # W wall head (flight-1 side) to the landing
                ((xi + .1, zw + .09), (xi + .1, z2t + .01), (False, True)),       # E wall head (flight-2 side)
                ((-xi + .09, z2t + .04), (-W/2 + .2 + FW, z2t + .04), (False, True))]   # cross on the top-landing edge over flight 1
        # S of 982/984 = the F3 stand back (tiers solid to +15.8 at Z 65.95, probed); E of 992 = facade curtain wall (as 994 in #7)
        drop = {982: {0}, 984: {0}, 992: {2}}.get(idx, set()); segs = [sg for j, sg in enumerate(segs) if j not in drop]
        if idx in (982, 984):   # the F3 stand modules overhang the core S end to Z 67.05 (probed; flagged to Vance): side runs start past the stand front
            segs = [((p0[0], zs + 1.1), p1, pe) if p0[1] == zw + .09 else (p0, p1, pe) for p0, p1, pe in segs]
        if idx == 984:          # stand 1704's aisle plate laps over the E wall head and into the core to X ~91.75 for Z 67.05..69.9 (flagged): E run starts past it
            segs = [((p0[0], 69.95 - cz), p1, pe) if p0[0] == xi + .1 else (p0, p1, pe) for p0, p1, pe in segs]
        if idx == 992:          # S run stops 0.1 m short of the curtain wall line
            segs = [((p0[0], p0[1]), (xi + .1, p1[1]), pe) if j == 0 else (p0, p1, pe) for j, (p0, p1, pe) in enumerate(segs)]
        a = np.radians(yaw); c, s_ = np.cos(a), np.sin(a)
        T = lambda lx, lz: (cx + lx * c + lz * mz * s_, cz - lx * s_ + lz * mz * c)
        for p0, p1, pe in segs:
            (x0, z0), (x1, z1) = T(*p0), T(*p1)
            if abs(z1 - z0) < 1e-6:   # world X run
                if x1 < x0: x0, x1, pe = x1, x0, pe[::-1]
                gd(k, round(x0, 4), round(x1, 4), round(z0, 4), "x", y, pe)
            else:
                if z1 < z0: z0, z1, pe = z1, z0, pe[::-1]
                gd(k, round(z0, 4), round(z1, 4), round(x0, 4), "z", y, pe)
    return k
def guards_gallery():
    """#8 gallery N edge guard (Z 68.70..68.80) with the staff-door gap X -8.7..-7.5 and its floor infill to the plant-stack face,
    plus the wall collider for the 0.2 m slot at X -6.1..-5.9 (Z 58.4..69.0) north of the F2 wall end."""
    k = Kit(); y = 6.106
    gd(k, -11.36, -8.7, 68.75, "x", y); gd(k, -7.5, -6.1, 68.75, "x", y)   # W end stops at facade bay 577 (X <= -11.38), not -11.80
    inf = box(-8.7, -7.5, 5.7, y, 68.80 - E, 69.02 - E); k.add("Door_Infill", SL, inf); k.add("Door_Infill_Line", AM, box(-8.65, -7.55, y - E, y + .003, 68.95, 69.0)); k.col(inf.copy())
    return k
def slot_wall():
    """#8 'also found': wall collider for the 0.2 m slot at X -6.1..-5.9, Z 58.4..69.0 (F2), with a slate base trim as its visual."""
    k = Kit(); k.add("Slot_Base_Trim", SL, box(-6.1 + E, -5.9 - E, 6.1, 6.2, 58.4 + E, 69.0 - E)); k.col(box(-6.1, -5.9, 6.1, 8.4, 58.4 + E, 69.0 - E))
    return k

# ------------------------------------------------------------------ #10 plant-stack staff doors (locked, static) in the existing 2.0 x 2.4 openings
def stack_doors(d):
    """one 2.0 m stack opening (local X -1..1, wall Z -0.15..0.15) closed on all three floors: slate infill panel with a 1.0 m locked
    staff leaf centred at X d (white composite, amber band, gunmetal lock plates), alloy frame. Collider: the full opening per floor."""
    k = Kit()
    for y0 in (0.0, 6.1, 12.2):
        pan = U([box(-1 + E, d - .55, y0, y0 + 2.4 - E, -.1, .1), box(d + .55, 1 - E, y0, y0 + 2.4 - E, -.1, .1), box(d - .56, d + .56, y0 + 2.15 - E, y0 + 2.4 - E, -.1, .1)])
        fr = U([box(d - .554, d - .5, y0, y0 + 2.1 + E, -.06, .06), box(d + .5, d + .554, y0, y0 + 2.1 + E, -.06, .06), box(d - .554, d + .554, y0 + 2.1, y0 + 2.15, -.06, .06)])
        k.add("Infill_Panel", SL, pan); k.add("Door_Frame", ALY, fr)
        k.add("Staff_Leaf", WH, box(d - .495, d + .495, y0 + .01, y0 + 2.095, -.03, .03))
        for sz in (-1, 1):
            k.add("Leaf_Amber_Band", AM, box(d - .45, d + .45, y0 + 1.4, y0 + 1.45, *sorted((sz * (.03 - E), sz * .034))))
            k.add("Lock_Plate", G, box(d + .3, d + .38, y0 + .95, y0 + 1.15, *sorted((sz * (.03 - E), sz * .042))))
        k.col(box(-1, 1, y0, y0 + 2.4, -.15, .15))
    return k
def stack_sill():
    """SW stack F2 door sill: 0.23 m infill from the stack face (Z 9.98) to the gallery floor (Z 10.2), X -8.6..-7.6."""
    k = Kit(); b = box(-.5, .5, -.25, 0.0, 0.0, .23); k.add("Sill_Infill", SL, b); k.add("Sill_Amber", AM, box(-.45, .45, -E, .003, .17, .21)); k.col(b.copy())
    return k

EDGE_VARIANTS = {   # manifest index (bfe716e) -> (asset, local opening a..b)
    "tt_terrace_edge_open_c2": (-1.0, 1.0),     # 793 SW / 794 NW / 929 E ramp top landings (clear 2.0 m centred)
    "tt_terrace_edge_open_w38": (-1.5, 2.0),    # 747 W stair (Z 36..40, yaw -90: world Z = 38 + x) -> clear Z 36.5..40
    "tt_terrace_edge_open_w42": (-2.0, .5),     # 749 W stair (Z 40..44) -> clear Z 40..42.5
    "tt_terrace_edge_open_e38": (-1.5, 1.5),    # 903 E stair (Z 36..40, yaw 90: world Z = 38 - x) -> clear Z 36.5..39.5
}
if __name__ == "__main__":
    REP = []; LAY = json.load(open(LAYOUT))
    ramps_only = "--ramps-only" in sys.argv
    if "--guards-holes-only" in sys.argv:   # TTQA-042: re-export just the F3 hole guards (+ its layout entry)
        export_kit("tt_struct_guards_holes_f3", guards_holes(), REP, LAY, "Rev 3.7 #6 F3 track guards at the ST+S1/S2 core holes, 1.07 m")
        json.dump(LAY, open(LAYOUT, "w"), indent=1); print("ASSETS", len(REP), "FAILED", [r["asset"] for r in REP if not r["passed"]]); raise SystemExit(0)
    export_kit("tt_struct_ramp_sw", ramp_sw()[0], REP, LAY, "Rev 3.7.1 SW switchback ramp X -43.42..-25 Z 8.3..13.5, top landing y 0, 0.08 m deck over the Z 12.30..13.37 ring-lane undercroft, level 1.5 m foot landing + 1:20 fillet onto the drum")
    export_kit("tt_struct_ramp_nw", mirror(ramp_sw()[0], MZ), REP, LAY, "Rev 3.7 #1 NW ramp (SW mirrored about Z 40)")
    export_kit("tt_struct_ramp_e", mirror(ramp_sw()[0], MX), REP, LAY, "Rev 3.7 #2 E ramp X 153..171.42 (SW mirrored in X)")
    if ramps_only:
        json.dump(LAY, open(LAYOUT, "w"), indent=1)
        rd = os.path.join(RENDER_OUT, "access_rev37"); os.makedirs(rd, exist_ok=True); json.dump(REP, open(os.path.join(rd, "report.json"), "w"), indent=1, default=str)
        print("ASSETS", len(REP), "FAILED", [r["asset"] for r in REP if not r["passed"]])
        raise SystemExit(0)
    export_kit("tt_struct_stair_w", stair(-63.5, -1, 36.5, 42.5, 12, 11, 2.0, True), REP, LAY, "Rev 3.7 #1 W grand stair Z 36.5..42.5, 23 x 0.1752 / 0.30")
    export_kit("tt_struct_stair_e", stair(171.5, 1, 36.5, 39.5, 12, 11, 1.5, False), REP, LAY, "Rev 3.7 #2 E stair Z 36.5..39.5, 23 x 0.1752 / 0.30")
    export_kit("tt_struct_guards_holes_f3", guards_holes(), REP, LAY, "Rev 3.7 #6 F3 track guards at the ST+S1/S2 core holes, 1.07 m")
    export_kit("tt_struct_guards_cores_f3", guards_cores(), REP, LAY, "Rev 3.7 #7 F3 core-top guard rings + flight-1 cross guards, 1.07 m")
    export_kit("tt_struct_guards_cores_f3_r2a", guards_cores_r2({962, 964, 966}), REP, LAY, "TTQA-004 r2 core-top guards, F2 cores 962/964/966 (Type A)")
    export_kit("tt_struct_guards_cores_f3_r2b", guards_cores_r2({968, 976}), REP, LAY, "TTQA-004 r2 core-top guards, F2 cores 968/976 (Type A)")
    export_kit("tt_struct_guards_cores_f3_r2c", guards_cores_r2({982, 984, 986}), REP, LAY, "TTQA-004 r2 core-top guards, F2 cores 982/984/986 (Type B)")
    export_kit("tt_struct_guards_cores_f3_r2d", guards_cores_r2({988, 990, 992}), REP, LAY, "TTQA-004 r2 core-top guards, F2 cores 988/990/992 (Type B)")
    export_kit("tt_struct_guards_gallery", guards_gallery(), REP, LAY, "Rev 3.7 #8 gallery N edge guard + staff-door infill")
    export_kit("tt_struct_slot_wall_f2", slot_wall(), REP, LAY, "Rev 3.7 #8 slot wall collider X -6.1..-5.9 Z 58.4..69.0")
    export_kit("tt_plant_stack_staff_doors_l", stack_doors(-.25), REP, None, "Rev 3.7 #10 SW/SE stack openings, 1.0 m locked staff door per floor")
    export_kit("tt_plant_stack_staff_doors_r", stack_doors(.25), REP, None, "Rev 3.7 #10 NW/NE stack openings (yaw 180)")
    export_kit("tt_plant_stack_sill_sw", stack_sill(), REP, None, "Rev 3.7 #10 SW F2 sill infill Z 9.98..10.21")
    for nm, (a, b) in EDGE_VARIANTS.items():
        export_part(nm, edge_open(a, b, nm), REP, None, "Rev 3.7 terrace edge opening variant")
    json.dump(LAY, open(LAYOUT, "w"), indent=1)
    rd = os.path.join(RENDER_OUT, "access_rev37"); os.makedirs(rd, exist_ok=True); json.dump(REP, open(os.path.join(rd, "report.json"), "w"), indent=1, default=str)
    print("ASSETS", len(REP), "FAILED", [r["asset"] for r in REP if not r["passed"]])
