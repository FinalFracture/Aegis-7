"""F1-AXE (X 77..102, Z 0..15). Rev 3.2 s2: bays 3.4 m (BAY_W param) across Z 0.3..13.9 incl. 0.1 m partitions,
0.3 m frame zone Z0..0.3, aisle Z13.9..15 (wall face 14.7 -> aisle clear 0.8 m, three aisle-swing gates). Throw +X axially.
Row 1 X77.15..84 (target wall face X84), row 2 = same assets +17 m (X94.15..101, face X101).
Targets stand on frames at X83.3 / 100.3 to clear the TC-S3 / TC-S4 trunk flare (r 1.0 at grade) in bay 3."""
from lz_lib import *
BAY_W = 3.4; X0, XF, XT = 77.2, 83.95, 83.3
def bay(w=BAY_W, south_trim=False, tree_notch=False):
    it = It(); a, b = .3 + .05 + D, .3 + w - .05 - D; zc = (a + b)/2
    # S facade inner ledge Z 0.621; k=0 bay origin at Z 0 so local z >= 0.631
    za = 0.631 if south_trim else a
    it.b('Floor_Mat', RU, X0, XF, 0, .025, za, b, col=True)
    for x in (XT - 3.66, XT - 4.88): it.b('Throw_Lines', AM, x, x + .05, .021, .03, max(a + .1, za), b - .1)
    z_in_s = max(a + .06, za)
    for z in (z_in_s, b - .09): it.b('Court_Inlay', BA, X0 + .1, XF - .1, .021, .029, z, z + .03)
    # optional notch around TC-S3/S4 Trunk_Clad (r=0.6 + 12 mm) in bay k=2 (origin Z 6.8 -> local 1.088..2.312)
    spans = [(za, b)]
    if tree_notch:
        t0, t1 = 1.088, 2.312
        spans = []
        if za < t0: spans.append((za, t0))
        if b > t1: spans.append((t1, b))
    for u, v in spans:
        if v - u <= 0.04: continue
        it.b('Wall_Lining', FA, 83.95 + D, 84.002, .1, 5.6, u, v)
        # keep reveal 12 mm shy of a notch cut so the z-end faces are not coplanar with the lining
        ru, rv = max(u, a + .1), min(v, b - .1)
        if tree_notch:
            if v == 1.088: rv = min(rv, v - .012)
            if u == 2.312: ru = max(ru, u + .012)
        if rv - ru > 0.04:
            for y in (1.0, 2.2, 3.4, 4.6): it.b('Lining_Reveal', CY, 83.947, 83.958, y, y + .03, ru, rv)
    for z in (zc - 1.05, zc + 1.05):
        it.a('Target_Posts', ST, tube((XT + .06, .056, z), (XT + .06, 2.75, z), .045, 8)); it.col(XT, XT + .12, 0, 2.75, z - .06, z + .06)
        it.a('Target_Feet', G, box(XT - .2, XT + .32, .021, .06, z - .12, z + .12))
    for k in range(5):
        z0 = zc - 1.0 + k*.4; it.b('Target_Boards', WH, XT - .1, XT + .002, .6, 2.6, z0 + .002, z0 + .398, col=k == 2)
    yc = 1.52
    for k, (r, mk) in enumerate(((.62, SL), (.46, CY), (.3, WH), (.12, BA))):
        xx = XT - .1 - .006 - k*.008; it.a('Target_Rings', mk, cap((xx + .004, yc, zc), r, .012, 24, 'x'))
    # crosshair floated 20 mm west of boards/rings to avoid coplanar faces
    xf = XT - .1 - .05
    it.b('Target_Cross_H', BA, xf, xf + .008, yc - .015, yc + .015, zc - .5, zc - .14)
    it.b('Target_Cross_H', BA, xf, xf + .008, yc - .015, yc + .015, zc + .14, zc + .5)
    it.b('Target_Cross_V', BA, xf, xf + .008, yc - .5, yc - .14, zc - .015, zc + .015)
    it.b('Target_Cross_V', BA, xf, xf + .008, yc + .14, yc + .5, zc - .015, zc + .015)
    it.b('Target_Cross_Mid', CY, xf - .002, xf + .006, yc - .04, yc + .04, zc - .04, zc + .04)
    for dz, dy, mk in ((.58, 0, AM), (-.58, 0, AM), (0, .58, VIO), (0, -.58, VIO)):
        it.b('Target_Ticks', mk, xf - .002, xf + .01, yc + dy - .03, yc + dy + .03, zc + dz - .03, zc + dz + .03)
    for dz in (-.75, .75): it.a('Kill_Shots', VIO, cap((XT - .1 - .002, 2.32, zc + dz), .055, .012, 12, 'x'))
    for k in range(7): it.a('Target_LeafCrown', LF2, wall_leaf((XT - .1, 2.55, zc - .9 + .3*k), (k - 3)*.3, .4, .15, face=-1))
    it.a('Target_Ball', BA, node((XT - .05, 3.1, zc), .09, 1))
    it.a('Target_Ball_Stem', ST, tube((XT - .05, 2.596, zc), (XT - .05, 3.016, zc), .018, 6))
    rp0 = max(a + .25, za); it.b('Rack_Post', G, 77.35, 77.45, .021, 1.5, rp0, rp0 + .10, col=True)
    it.b('Rack_Bar', G, 77.45, 77.6, 1.25, 1.35, a + .1, a + .9)
    for k in range(3):
        z = a + .3 + k*.25; it.a('Axe_Handles', ALY, tube((77.62, .796, z), (77.62, 1.34, z), .018, 6))
        it.b('Axe_Heads', ALY, 77.6, 77.82, .7, .8, z - .012, z + .012)
    it.b('Tablet_Post', G, 77.35, 77.45, .021, 1.25, b - .35, b - .25, col=True)
    it.b('Tablet', SL, 77.452, 77.5, 1.05, 1.45, b - .55, b - .05)
    # legible tablet score art (face +X)
    it.b('Tablet_Plate', SL, 77.498, 77.504, 1.09, 1.41, b - .51, b - .09)
    for i in range(4):
        yy = 1.14 + i * 0.06
        it.b('Tablet_Rows', CY if i % 2 == 0 else AM, 77.508, 77.514, yy, yy + 0.035, b - .46, b - .14)
    it.b('Tablet_Ticker', AM, 77.508, 77.514, 1.38, 1.395, b - .46, b - .14)
    nm = 'tt_axe_bay_s' if south_trim else 'tt_axe_bay_tree' if tree_notch else 'tt_axe_bay'
    return emit(nm, it, f'one axe bay {w} m wide, throw +X, target face X{XT}; place at Z offsets 3.4k, row 2 +17 m in X')

def partition():
    it = It(); z0, z1 = -.05, .05
    it.b('Part_Sill', G, X0, XF, 0, .08, z0, z1, col=True)
    xs = np.linspace(X0 + .03, XF - .03, 5)
    for x in xs: it.b('Part_Posts', G, x - .03, x + .03, .076, 3.4, z0, z1)
    for xa, xb in zip(xs[:-1], xs[1:]):
        it.b('Part_Acoustic', FA, xa + .032, xb - .032, .084, 2.4, z0 + .01, z1 - .01, col=True)
        it.b('Part_Net_Scissor', NET, xa + .032, xb - .032, 2.44, 3.36, -.008, .008)
        for za, zb in ((z0 + .006, z0 + .014), (z1 - .014, z1 - .006)): it.b('Part_Reveal', CY, xa + .05, xb - .05, 1.2, 1.23, za, zb)
        it.b('Part_MidRail', ST, xa + .034, xb - .034, 2.396, 2.444, z0 - .005, z1 + .005)
    it.b('Part_TopRail', ST, X0, XF, 3.396, 3.46, z0 - .01, z1 + .01)
    for x in xs[1:-1]:
        st, lv = vine([(x, .1, z1 + .06), (x + .02, 1.2, z1 + .06), (x - .02, 2.3, z1 + .06)], seed=int(x*10), outward=True)
        it.a('Vine_Stems', LF, st); it.a('Vine_Leaves', LF2, lv)
    return emit('tt_axe_partition', it, 'bay partition 0.1 m (acoustic lined, net above 2.4); place at Z 3.7/7.1/10.5')

def spectator():
    """Z 13.9 screen; aisle clear to stand face Z14.7 = 0.8 m. Three gates swing into aisle (+Z), not into bays."""
    it = It(); z = 13.9
    gaps = [(77.5, 78.4), (79.8, 80.7), (82.1, 83.0)]
    segs = []; cursor = X0
    for g0, g1 in gaps:
        if g0 > cursor + 0.08: segs.append((cursor, g0 - 0.04))
        cursor = g1 + 0.04
    if XF > cursor + 0.08: segs.append((cursor, XF))
    it.b('Screen_Sill', G, X0, XF, 0, .06, z - .05, z + .05)
    for x0, x1 in segs:
        n = max(2, int((x1 - x0) / 1.8) + 1)
        xs = np.linspace(x0 + 0.04, x1 - 0.04, n)
        for x in xs: it.b('Screen_Posts', G, x - .025, x + .025, .056, 2.4, z - .035, z + .035, col=True)
        for xa, xb in zip(xs[:-1], xs[1:]):
            if xb - xa < 0.12: continue
            it.b('Screen_Pane_Scissor', SCR, xa + .04, xb - .04, .08, 1.104, z - .008, z + .008); it.col(xa, xb, 0, 2.4, z - .02, z + .02)
            it.b('Screen_Net_Scissor', NET, xa + .04, xb - .04, 1.18, 2.36, z - .006, z + .006)
            it.b('Screen_Rail', ST, xa + .04, xb - .04, 1.1, 1.16, z - .03, z + .03)
        it.b('Lean_Rail', ALY, x0, x1, 1.0, 1.05, z + .22, z + .32)
    for g0, g1 in gaps:
        it.b('Gate_Jamb', G, g0 - .04, g0 - .01, .056, 1.2, z - .04, z + .04, col=True)
        it.b('Gate_Jamb', G, g1 + .01, g1 + .04, .056, 1.2, z - .04, z + .04, col=True)
        # leaf parked OPEN into aisle (+Z), clear of posts (>=30 mm)
        it.b('Gate_Leaf', WH, g0 + 0.05, g1 - 0.05, .1, 1.1, z + 0.06, z + 0.85, col=True)
        it.a('Gate_Balls', BA, node(((g0 + g1) / 2, 1.18, z + 0.45), .055, 1))
    for k, x in enumerate(np.arange(78.55, 83.4, 1.15)):
        if any(g0 - 0.15 < x < g1 + 0.15 for g0, g1 in gaps): continue
        it.a('Kick_Moss', LF, moss_mound((x, 0.05, z + .62), .14, k))
    return emit('tt_axe_spectator', it, 'aisle screen Z13.9; 0.8 m clear to stand Z14.7; 3 gates swing +Z into aisle')

def build(PL):
    bb = bay(); bbs = bay(south_trim=True); bbt = bay(tree_notch=True)
    pt = partition(); sp = spectator()
    for dx in (0, 17):
        for k in range(4):
            place(PL, bbs if k == 0 else bbt if k == 2 else bb, dx, 0, BAY_W*k)
        for k in range(1, 4): place(PL, pt, dx, 0, .3 + BAY_W*k)
        place(PL, sp, dx, 0, 0)
if __name__ == '__main__':
    PL = []; build(PL)
    for r in REP:
        if not r['passed']: print(r['asset'], r['bad'], r['coplanar'], r['open'], r['pivot'])
