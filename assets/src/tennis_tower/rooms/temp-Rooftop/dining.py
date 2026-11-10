"""F3-DINE W dining terraces + bar (X -0.7..24.1, Z 4..75). Rev 3.0. Reuse tt_bar, stools, tables; emit the accessible counter."""
from rt_lib import *

BAR_P = (14.0, F3_Y, 39.5)
BAR_YAW = -90
# bar-local (lx, lz); already include the +0.20 recenter shift (bar.py STOOLS)
STOOL_LOCAL = [(-3.575, 1.88), (-2.925, 1.88), (-2.275, 1.88), (-1.625, 1.88), (-0.975, 1.88),
               (-0.325, 1.88), (0.325, 1.88), (0.975, 1.88), (1.625, 1.88), (2.275, 1.88),
               (2.925, 1.88), (3.575, 1.88), (-4.65, -1.25), (-4.65, -0.6), (-4.65, 0.05),
               (-4.65, 0.7), (4.65, -1.25), (4.65, -0.6), (4.65, 0.05), (4.65, 0.7)]
COLS = [4.5, 7.4, 10.3, 16.1, 19.0, 21.9]   # X 13.2 omitted: 4 m aisle to the bar
KEEP = [('trackW', 0.7, 2.5, 0.0, 79.0), ('TC-W1', 22.8, 24.2, 29.8, 31.2), ('TC-W2', 22.8, 24.2, 47.8, 49.2),
        ('lift', 16.0, 30.0, 34.5, 39.0), ('WCshell', 24.1, 30.0, 21.0, 34.0)]
GAP = 0.02

def _acc():
    """1.5 m counter, top 0.86 m, knee space on local +Z, back on local -Z. Pivot bottom-centre."""
    it = It()
    it.b('AccTop', SL, -0.74, 0.74, 0.82, 0.856, -0.30, 0.27)
    it.a('AccTop', SL, tube((-0.73, 0.84, 0.28), (0.73, 0.84, 0.28), 0.02, 10))
    it.a('AccTop', SL, node((-0.73, 0.84, 0.28), 0.02))
    it.a('AccTop', SL, node((0.73, 0.84, 0.28), 0.02))
    it.b('CourtLine', WH, -0.70, 0.70, 0.854, 0.858, 0.192, 0.208)
    it.b('CourtLine', WH, -0.70, 0.70, 0.854, 0.858, -0.208, -0.192)
    it.b('EdgeReveal', G, -0.694, 0.694, 0.80, 0.824, -0.266, 0.24)
    it.b('AccLeg', KP, 0.698, 0.748, 0.030, 0.824, -0.27, 0.27, col=True)
    it.b('AccLeg', KP, -0.748, -0.698, 0.030, 0.824, -0.27, 0.27, col=True)
    it.b('LegFoot', ALY, 0.692, 0.75, 0.0, 0.034, -0.29, 0.29)
    it.b('LegFoot', ALY, -0.75, -0.692, 0.0, 0.034, -0.29, 0.29)
    for s in (-1, 1):
        cx = s * (0.698 - 0.003)
        for y in (0.15, 0.70):
            for z in (-0.2, 0.2):
                it.a('Fastener', ALY, node((cx, y, z), 0.007))
    it.b('AccessMarker', VIO, 0.708, 0.738, 0.10, 0.70, 0.268, 0.274)
    it.b('AccessMarker', VIO, -0.738, -0.708, 0.10, 0.70, 0.268, 0.274)
    it.b('AccModesty', KP, -0.694, 0.694, 0.30, 0.824, -0.298, -0.268)
    for y0, y1 in ((0.41, 0.43), (0.53, 0.55), (0.65, 0.67)):
        it.b('ModestyRib', G, -0.68, 0.68, y0, y1, -0.270, -0.256)
    it.col(-0.75, 0.75, 0.82, 0.86, -0.30, 0.30)
    return it

def _put(PL, asset, x, z, yaw):
    place(PL, [(asset, (0.0, 0.0, 0.0))], x, F3_Y, z, yaw)

def _wxz(px, pz, yaw, lx, lz):
    """Same yaw map as rt_lib.place(): world_x = px + lx*cos + lz*sin; world_z = pz - lx*sin + lz*cos."""
    a = math.radians(yaw); c, s = math.cos(a), math.sin(a)
    return px + lx * c + lz * s, pz - lx * s + lz * c

def _aabb(p, b):
    (x0, y0, z0), (x1, y1, z1) = b
    px, py, pz = p['p']; xs = []; zs = []
    for lx in (float(x0), float(x1)):
        for lz in (float(z0), float(z1)):
            wx, wz = _wxz(px, pz, p.get('yaw', 0), lx, lz)
            xs.append(wx); zs.append(wz)
    return (min(xs), max(xs), min(zs), max(zs), py + float(y0))

def _sep(a0, a1, b0, b1):
    if a1 < b0: return b0 - a1
    if b1 < a0: return a0 - b1
    return 0.0

def _gap(a, b):
    dx, dz = _sep(a[0], a[1], b[0], b[1]), _sep(a[2], a[3], b[2], b[3])
    if dx == 0.0 and dz == 0.0:
        ox = min(a[1], b[1]) - max(a[0], b[0]); oz = min(a[3], b[3]) - max(a[2], b[2])
        return -min(ox, oz)
    return math.hypot(dx, dz)

def _zgap(a, b):
    if a[3] < b[2]: return b[2] - a[3]
    if b[3] < a[2]: return a[2] - b[3]
    return -(min(a[3], b[3]) - max(a[2], b[2]))

def _bar_zone(asset):
    return asset == 'tt_bar_stool' or str(asset).startswith('tt_dine_bar_acc')

def _attached(a, b):
    s = {a, b}
    return 'tt_bar' in s and any(str(x).startswith('tt_dine_bar_acc') for x in s)

def _bounds(asset, cache):
    if asset not in cache:
        sc = trimesh.load(str(GM / (asset + '.glb')), force='scene')
        if sc.bounds is None: raise AssertionError('no bounds ' + asset)
        cache[asset] = sc.bounds
    return cache[asset]

def check_placements(PL_all, new):
    """Headless section-C assert. Returns the smallest pairwise clearance (attached acc/bar joint excluded)."""
    cache, bad, boxes = {}, [], []
    for p in new:
        box = _aabb(p, _bounds(p['asset'], cache)); boxes.append(box)
        x0, x1, z0, z1, y0 = box
        if x0 < -0.7 - 1e-6 or x1 > 24.1 + 1e-6:
            bad.append('roomX %s %s %.3f..%.3f' % (p['asset'], p['p'], x0, x1))
        zlo, zhi = (34.5, 44.5) if _bar_zone(p['asset']) else (4.0, 75.0)
        if z0 < zlo - 1e-6 or z1 > zhi + 1e-6:
            bad.append('roomZ %s %s %.3f..%.3f want %.1f..%.1f' % (p['asset'], p['p'], z0, z1, zlo, zhi))
        if abs(y0 - F3_Y) > 0.005 + 1e-9:
            bad.append('miny %s %s %.4f' % (p['asset'], p['p'], y0))
        for name, a, b, c, d in KEEP:
            g = _gap(box, (a, b, c, d))
            if g < GAP - 1e-9: bad.append('keep %s %s %s gap %.4f' % (name, p['asset'], p['p'], g))
    min_clear = None
    for i in range(len(new)):
        for j in range(i + 1, len(new)):
            if _attached(new[i]['asset'], new[j]['asset']):
                zg = _zgap(boxes[i], boxes[j])
                if zg < -1e-9 or zg > 0.015 + 1e-9:
                    bad.append('acc-bar Zgap %.4f %s %s' % (zg, new[i]['p'], new[j]['p']))
                continue
            g = _gap(boxes[i], boxes[j])
            min_clear = g if min_clear is None else min(min_clear, g)
            if g < GAP - 1e-9:
                bad.append('pair %s %s / %s %s gap %.4f' % (new[i]['asset'], new[i]['p'], new[j]['asset'], new[j]['p'], g))
    for i, p in enumerate(new):
        for q in PL_all:
            a = q.get('asset', '')
            if q is p or not (str(a).startswith('tt_cab') or a == 'tt_cabana'): continue
            g = _gap(boxes[i], _aabb(q, _bounds(a, cache)))
            min_clear = g if min_clear is None else min(min_clear, g)
            if g < GAP - 1e-9: bad.append('cab %s %s / %s %s gap %.4f' % (p['asset'], p['p'], a, q.get('p'), g))
    if bad: raise AssertionError('placement breaches (%d):\n%s' % (len(bad), '\n'.join(bad)))
    return 0.0 if min_clear is None else min_clear

def build(PL):
    n0 = len(PL)
    _put(PL, 'tt_bar', BAR_P[0], BAR_P[2], BAR_YAW)
    for lx, lz in STOOL_LOCAL:
        x, z = _wxz(BAR_P[0], BAR_P[2], BAR_YAW, lx, lz)
        _put(PL, 'tt_bar_stool', x, z, BAR_YAW)
    # yaw 180: back (local -Z) lands at Z 35.248, 2 mm off the bar S face (Z 35.25). Footprint X 11.55..13.05.
    A_acc = emit('tt_dine_bar_acc', _acc(), '1.5 m accessible bar section 0.86 m, knee space')
    place(PL, A_acc, BAR_P[0] - 1.70, F3_Y, BAR_P[2] - 4.552, 180)
    ss = sa = ns = na = 0
    for side, z0, sgn in (('S', 5.0, 1.0), ('N', 74.0, -1.0)):
        for j in range(10):
            z = z0 + sgn * 2.9 * j
            for ci, x in enumerate(COLS):
                if ci == 5 and j >= 8: continue          # col 21.9, two rows nearest each tree
                acc = j == 9 and ci in (1, 2, 3, 4)      # plaza row, cols 7.4 10.3 16.1 19.0
                _put(PL, 'tt_food_table4_acc' if acc else 'tt_food_table4', x, z, 0)
                if side == 'S':
                    if acc: sa += 1
                    else: ss += 1
                else:
                    if acc: na += 1
                    else: ns += 1
    mc = check_placements(PL, PL[n0:])
    return dict(bar=1, bar_yaw=BAR_YAW, bar_p=list(BAR_P), stools=len(STOOL_LOCAL), acc_counter=1,
                tables_S_std=ss, tables_S_acc=sa, tables_N_std=ns, tables_N_acc=na,
                seats_tables=(ss + sa + ns + na) * 4, min_clear=round(mc, 4))
