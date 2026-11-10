"""temp-Rooftop shared helpers (spec Rev 3.0). Y-up, X axial, Z across, +Z front, bottom-centre pivots. F3_Y=12.2
Rules used everywhere: siblings of different parts keep a 2 mm gap; stacked parts embed E=4 mm and inset >= 2 mm
(no coplanar faces); same-name parts may overlap. Colliders are simple boxes in '*-colonly' nodes."""
import sys, json, math
from pathlib import Path
HERE = Path(__file__).resolve().parent; TT = HERE.parent.parent
sys.path[:0] = [str(TT), str(TT / 'structure'), str(TT.parent)]
from struct_lib import *          # noqa
import modlib as ml
import numpy as np, trimesh
ml._m('rt_rub', 'TT_PlayRubber_Slate', (.20, .24, .27), 0, .9)
ml._m('rt_fab', 'TT_Upholstery_FabricSlate', (.24, .28, .33), 0, .95)
RU, FA, KP = 'rt_rub', 'rt_fab', G
SOLID = {SL, G, ST, CON, SSL, WH, ALY, SGM, RU, FA, KP, SCR} if 'SCR' in globals() else {SL, G, ST, CON, SSL, WH, ALY, SGM, RU, FA, KP}
GM = Path(GODOT_MODELS)
REP = []; LAY = {}
D = 0.002
F3_Y = 12.2

class It(list):
    """item list [(part, mat, mesh)] + collider boxes"""
    def __init__(s): super().__init__(); s.cols = []
    def a(s, n, m, mesh): s.append((n, m, mesh)); return mesh
    def b(s, n, m, x0, x1, y0, y1, z0, z1, col=False):
        mesh = box(x0, x1, y0, y1, z0, z1); s.append((n, m, mesh))
        if col: s.cols.append(box(x0, x1, y0, y1, z0, z1))
        return mesh
    def col(s, x0, x1, y0, y1, z0, z1): s.cols.append(box(x0, x1, y0, y1, z0, z1))

def emit(name, it, note='', budget=5600):
    """export one GLB (or _a/_b chunks along X) -> list of (asset, world_offset)."""
    items = sorted(it, key=lambda a: a[2].bounds.mean(0)[0]); cols = list(it.cols)
    nc = sum(len(c.faces) for c in cols)
    chunks = [[]]; t = 0
    for i in items:
        n = len(i[2].faces)
        if t + n + nc > budget and chunks[-1]: chunks.append([]); t = 0
        chunks[-1].append(i); t += n
    out = []
    for k, ch in enumerate(chunks):
        nm = name if len(chunks) == 1 else f'{name}_{chr(97 + k)}'
        lo = min(c[2].bounds[0][0] for c in ch); hi = max(c[2].bounds[1][0] for c in ch)
        if len(chunks) > 1:
            cc_ = [c for c in cols if lo - .01 <= c.bounds.mean(0)[0] <= hi + .01]
        else: cc_ = cols
        g = {}
        for pn, mk, m in ch: g.setdefault((pn, mk), []).append(m)
        r, _ = export_chunk(nm, [(pn, mk, ms) for (pn, mk), ms in g.items()], [('Solid-colonly', [c.copy() for c in cc_])] if cc_ else None,
                            REP, layout=LAY, note=note)
        out.append((nm, r['world_offset']))
    return out

def place(PL, assets, x, y, z, yaw=0, tag='f3', local=True):
    """assets from emit(); local=True: (x,y,z) is the design origin of a locally built piece (adds rotated offset)."""
    for nm, o in assets:
        px, py, pz = x, y, z
        if local:
            a = math.radians(yaw); px += o[0]*math.cos(a) + o[2]*math.sin(a); pz += -o[0]*math.sin(a) + o[2]*math.cos(a); py += o[1]
        PL.append(dict(glb=str(GM / f'{nm}.glb'), asset=nm, p=[round(px, 4), round(py, 4), round(pz, 4)], yaw=yaw, tag=tag))

def pin(c, h=.38):
    rings = [(0, .45, .45), (.03, .75, .75), (.12, 1.0, 1.0), (.2, .82, .82), (.26, .42, .42), (.3, .5, .5), (.34, .55, .55), (.37, .3, .3)]
    m = loft(circle(.06, 8), [(y * h / .38, a, b) for y, a, b in rings]); return xf(m, t=c)

def moss_mound(c, r, seed=0):
    """moss boulder: low clump of jittered blobs (nature cue, no planter)."""
    rng = np.random.default_rng(seed); ms = [clump((c[0], c[1] + r*.45, c[2]), r, seed, 1)]
    for k in range(3):
        a = rng.uniform(0, 6.28); ms.append(clump((c[0] + .7*r*math.cos(a), c[1] + r*.3, c[2] + .7*r*math.sin(a)), r*.55, seed + k + 1))
    return merge(ms)

def wall_leaf(c, ang, L, W, t=.012, face=1):
    """leaf lying flat on a wall whose normal is +-X (face), blade in the YZ plane tilted by ang (rad) about X.
    c = point on the wall surface; the leaf embeds 4 mm."""
    m = leaf((0, 0, 0), L, W, t=t)
    m = xf(m, R=trimesh.transformations.rotation_matrix(math.pi/2, [0, 1, 0]))
    m = xf(m, R=trimesh.transformations.rotation_matrix(ang, [1, 0, 0]))
    return xf(m, t=(c[0] + face*(t - .004), c[1], c[2]))
def zwall_leaf(c, ang, L, W, t=.012, face=1):
    """same for a wall whose normal is +-Z (blade in XY plane)."""
    m = leaf((0, 0, 0), L, W, t=t); m = xf(m, R=trimesh.transformations.rotation_matrix(ang, [0, 0, 1]))
    return xf(m, t=(c[0], c[1], c[2] + face*(t - .004)))

def view_rail_parts(x0, x1, z, y0=0.0, h=1.07):
    """Sculpted gunmetal view rail: round posts every 1.2 m, top rail, mid rail, cyan LED. No glass."""
    parts = []
    c0, c1 = x0 + 0.025, x1 - 0.025
    xs = [c0]
    x = c0 + 1.2
    while x < c1 - 1e-6:
        xs.append(x); x += 1.2
    if c1 - xs[-1] > 1e-6:
        xs.append(c1)
    pr, tr, mr = 0.022, 0.024, 0.014
    yc = y0 + h - tr
    cap0, cap1 = x0 + tr, x1 - tr
    # sphere r equals the rail r, so the tube stops 18 mm short and the cap embeds 6 mm
    inset = tr - 0.006
    if cap1 - inset > cap0 + inset:
        parts.append(('TopRail', KP, tube((cap0 + inset, yc, z), (cap1 - inset, yc, z), tr, 10)))
    parts.append(('RailEndCap', KP, node((cap0, yc, z), tr)))
    parts.append(('RailEndCap', KP, node((cap1, yc, z), tr)))
    for cx in xs:
        parts.append(('Post', KP, tube((cx, y0 + 0.010, z), (cx, yc - 0.0215, z), pr, 10)))
        parts.append(('BasePlate', KP, box(max(x0, cx - 0.05), min(x1, cx + 0.05), y0, y0 + 0.014, z - 0.028, z + 0.028)))
        for s in (-1, 1):
            bx = min(max(cx + s * 0.034, x0 + 0.010), x1 - 0.010)
            parts.append(('Bolt', ALY, node((bx, y0 + 0.018, z), 0.008)))
    for a, b in zip(xs, xs[1:]):
        xa, xb = a + pr - 0.004, b - pr + 0.004
        if xb > xa:
            my = y0 + h / 2
            parts.append(('MidRail', KP, tube((xa, my, z), (xb, my, z), mr, 8)))
        la = max(a + pr + D, cap0 + tr + D)
        lb = min(b - pr - D, cap1 - tr - D)
        if lb > la:
            parts.append(('RailLED', CY, box(la, lb, yc - 0.030, yc - 0.020, z - 0.006, z + 0.006)))
    return parts

def perch_it():
    """Fence perch L=1.8 D=0.3. Pivot bottom-centre; seat top ~0.45."""
    it = It()
    it.b('Seat', RU, -.88, .88, .41, .45, -.15, .13)
    it.a('Seat', RU, tube((-.88, .43, .13), (.88, .43, .13), .02, 8))
    it.a('Seat', RU, node((-.88, .43, .13), .02))
    it.a('Seat', RU, node((.88, .43, .13), .02))
    for zc in (-.09, -.02, .05):
        it.b('CourtLine', WH, -.80, .80, .448, .452, zc - .006, zc + .006)
    it.b('FrontSkirt', RU, -.86, .86, .39, .414, .146, .176)
    for s in (-1, 1):
        cx = .75 * s
        it.b('Bracket', KP, cx - .04, cx + .04, .134, .414, -.148, -.128)
        it.b('Bracket', KP, cx - .015, cx + .015, .37, .414, -.13, .10)
        # specified line (cx,.16,-.130)->(cx,.40,.07); stop just under the arm so embed stays <= 6 mm
        y_end = .3685
        t = (y_end - .16) / (.40 - .16)
        z_end = -.130 + t * (.07 + .130)
        it.a('Brace', KP, tube((cx, .16, -.130), (cx, y_end, z_end), .011, 8))
        for bx in (cx - .025, cx + .025):
            for by in (.18, .36):
                it.a('Bolt', ALY, node((bx, by, -.128 + .006), .01))
    it.col(-.9, .9, .41, .45, -.15, .15)
    for s in (-1, 1):
        cx = .75 * s
        it.col(cx - .04, cx + .04, .134, .414, -.148, -.128)
    return it
