"""F3-CAB cabanas + lounge (X -12..-0.7, Z 18..62). Rev 3.0. Reuse tt_cabana; emit dressing + seating + rail."""
from rt_lib import *

def _mound():
    it = It()
    it.a('Moss', LF, moss_mound((0, 0, 0), .28, 1))
    it.a('Moss', LF2, moss_mound((.42, 0, .18), .16, 2))
    it.a('Moss', LF, moss_mound((-.4, 0, -.18), .16, 3))
    it.a('Tuft', LF2, clump((.15, .06, -.32), .06, 10))
    it.a('Tuft', LF2, clump((-.18, .06, .34), .06, 11))
    it.a('Balls', BA, node((.28, .08, -.28), .03, 0))
    it.a('Balls', BA, node((-.3, .08, .28), .03, 0))
    return it

def _vine():
    """Green-wall post. Envelope x -0.12..0.12, z -0.14..0.14, y 0..2.80. Back strand is the front yawed 180 about Y."""
    it = It()
    it.b('Plate', KP, -0.04, 0.04, 0.03, 2.776, -0.02, 0.02, col=True)
    it.b('PlateShoe', SSL, -0.07, 0.07, 0, 0.034, -0.05, 0.05)
    it.b('PlateCap', KP, -0.05, 0.05, 2.772, 2.8, -0.03, 0.03)
    for y in (0.6, 1.4, 2.2):
        for s in (1.0, -1.0):
            it.a('Bolt', ALY, node((0.0, y, s * (0.02 + 0.004)), 0.008))
    # |z| >= 0.035 so an r=0.012 stem stays outside the plate (|z|<=0.02) by >= 3 mm.
    front = [(0.03, 0.08, 0.035), (0.06, 0.6, 0.05), (0.02, 1.2, 0.04),
             (0.06, 1.8, 0.05), (0.02, 2.4, 0.04), (0.04, 2.72, 0.045)]

    def yaw180(m):
        out = trimesh.Trimesh(np.array(m.vertices, float, copy=True), np.array(m.faces, copy=True), process=False)
        out.metadata['uv'] = np.array(m.metadata['uv'], float, copy=True)
        R = np.eye(4)
        R[0, 0] = -1.0
        R[2, 2] = -1.0
        return xf(out, R=R)

    stem = merge([tube(a, b, 0.012, 6) for a, b in zip(front[:-1], front[1:])] + [node(p, 0.012) for p in front])
    it.a('VineStem', LF, merge([stem, yaw180(stem)]))

    def samples(pts, step):
        pts = [np.asarray(p, float) for p in pts]
        out, dist, target = [], 0.0, step
        for a, b in zip(pts[:-1], pts[1:]):
            seg = b - a
            L = float(np.linalg.norm(seg))
            while target <= dist + L + 1e-9:
                u = (target - dist) / L
                if u > 1.0:
                    break
                out.append(a + seg * u)
                target += step
            dist += L
        return out

    def fits(m):
        lo, hi = m.bounds
        return (lo[0] >= -0.12 and hi[0] <= 0.12 and lo[1] >= 0.0 and hi[1] <= 2.8
                and lo[2] >= -0.14 and hi[2] <= 0.14)

    def fit_leaf(c, d, length, width):
        # Shorten length only. The stem point stays put.
        m = leaf_dir(c, d, length, width, 0.02)
        if fits(m):
            return m
        lo_l, hi_l, best = 1e-3, float(length), None
        for _ in range(20):
            mid = 0.5 * (lo_l + hi_l)
            trial = leaf_dir(c, d, mid, width, 0.02)
            if fits(trial):
                best, lo_l = trial, mid
            else:
                hi_l = mid
        return best if best is not None else leaf_dir(c, d, lo_l, width, 0.02)

    def cuts_plate(m):
        v = np.asarray(m.vertices)
        return bool(np.any((np.abs(v[:, 0]) < 0.038) & (np.abs(v[:, 2]) < 0.018)
                           & (v[:, 1] >= 0.03) & (v[:, 1] <= 2.776)))

    rng = np.random.default_rng(7)
    specs = []
    for i, p in enumerate(samples(front, 0.09)):
        length = float(rng.uniform(0.15, 0.20))
        width = float(rng.uniform(0.06, 0.08))
        x = (1.0 if i % 2 == 0 else -1.0) * float(rng.uniform(0.3, 0.5))
        y = float(rng.uniform(0.6, 0.8))
        z = float(rng.uniform(0.35, 0.55))
        specs.append((p, np.array([x, y, z], float), length, width))
    tip = np.asarray(front[-1], float)
    for x, w in zip((-0.50, -0.25, 0.0, 0.25, 0.50), (0.066, 0.072, 0.078, 0.072, 0.066)):
        specs.append((tip, np.array([x, 0.80, 0.45], float), 0.16, w))
    lf, lf2 = [], []
    for i, (c, d, length, width) in enumerate(specs):
        c = c + 0.003 * d / np.linalg.norm(d)
        m = fit_leaf(c, d, length, width)
        if cuts_plate(m):
            continue
        (lf if i % 3 == 2 else lf2).append(m)
    if lf2:
        it.a('VineLeaves', LF2, merge(lf2 + [yaw180(m) for m in lf2]))
    if lf:
        it.a('VineLeaves', LF, merge(lf + [yaw180(m) for m in lf]))

    def clip_moss(m):
        v = np.array(m.vertices, float, copy=True)
        v[:, 0] = np.clip(v[:, 0], -0.10, 0.10)
        v[:, 1] = np.clip(v[:, 1], 0.0, 2.8)
        v[:, 2] = np.clip(v[:, 2], -0.12, 0.12)
        m.vertices = v
        return m

    for c, seed in (((0.04, 0.05, 0.07), 31), ((-0.04, 0.05, -0.07), 32)):
        it.a('MossTuft', LF, clip_moss(clump(c, 0.045, seed)))
    return it

def _seat():
    """Lounge pair facing local -Z (back at +Z). Envelope x±0.9, z±0.35, y 0..0.77."""
    it = It()
    for sx in (-0.55, 0.55):
        it.b('ToeKick', G, sx - 0.33, sx + 0.33, 0, 0.024, -0.33, 0.33)
        it.b('SeatBase', SSL, sx - 0.35, sx + 0.35, 0.020, 0.08, -0.35, 0.35, col=True)
        it.a('Cushion', FA, box(sx - 0.33, sx + 0.33, 0.076, 0.36, -0.29, 0.25))
        it.a('Cushion', FA, tube((sx - 0.33, 0.32, -0.29), (sx + 0.33, 0.32, -0.29), 0.04, 10))
        for dx in (-0.15, 0.15):
            for bz in (-0.15, 0.08):
                it.a('Button', ALY, node((sx + dx, 0.36 + 0.008, bz), 0.012))
        it.b('BackShell', SSL, sx - 0.348, sx + 0.348, 0.076, 0.70, 0.330, 0.348, col=True)
        it.a('BackCushion', FA, box(sx - 0.33, sx + 0.33, 0.356, 0.73, 0.22, 0.334))
        it.a('BackCushion', FA, tube((sx - 0.33, 0.735, 0.285), (sx + 0.33, 0.735, 0.285), 0.035, 10))
        sgn = 1.0 if sx > 0.0 else -1.0
        # 0.345 lands the r=0.012 tube at x=0.907; stop the centre so the skin stays inside ±0.9
        ax = sgn * min(abs(sx) + 0.345, 0.9 - 0.012 - 1e-4)
        it.a('Arm', ALY, tube((ax, 0.078, -0.26), (ax, 0.52, -0.26), 0.012, 8))
        it.a('Arm', ALY, tube((ax, 0.52, -0.26), (ax, 0.52, 0.332), 0.012, 8))
        it.a('Arm', ALY, node((ax, 0.52, -0.26), 0.012))
    it.a('TableFoot', ALY, cap((0, 0.006, 0), 0.12, 0.012, axis='y'))
    it.a('TableLeg', ALY, tube((0, 0.008, 0), (0, 0.484, 0), 0.025, 8))
    it.a('TableTop', SSL, cap((0, 0.49, 0), 0.17, 0.02, axis='y'))
    it.col(-0.17, 0.17, 0, 0.50, -0.17, 0.17)
    it.a('TableBall', BA, node((0.06, 0.50 + 0.032 - 0.004, 0.05), 0.032))
    tuft = clump((-0.05, 0.035, 0.15), 0.05, 21)
    v = np.array(tuft.vertices, float, copy=True)
    low = float(v[:, 1].min())
    if low < 0.002:
        v[:, 1] += 0.002 - low
    tuft.vertices = v
    it.a('MossTuft', LF2, tuft)
    return it

def _rail():
    it = It()
    for n, m, mesh in view_rail_parts(-3.0, 3.0, 0.0, 0.0, 1.07):
        it.a(n, m, mesh)
    it.col(-3.0, 3.0, 0, 1.07, -.03, .03)
    return it

def build(PL):
    A_m = emit('tt_cab_dress_mound', _mound(), 'moss/tuft/ball dress, no planters')
    A_v = emit('tt_cab_dress_vine', _vine(), 'vine on thin plate')
    A_s = emit('tt_cab_lounge_seat', _seat(), 'lounge seat pair + table')
    A_r = emit('tt_cab_view_rail', _rail(), 'W glass view rail 6 m')
    # 8 cabanas facing W glass
    for k in range(8):
        cz = 20.0 + 5.5 * k
        PL.append(dict(glb=str(GM / 'tt_cabana.glb'), asset='tt_cabana', p=[-9.0, F3_Y, round(cz, 4)], yaw=90, tag='f3'))
        # dress in 1.5 m gaps between cabanas (avoid 2 m half-size)
        if k < 7:
            gz = cz + 2.75
            place(PL, A_m, -8.9897, F3_Y, round(gz + 0.0104, 4), 0, local=False)
            place(PL, A_v, -10.6, F3_Y, gz, 0)
    # view rails along W glass covering Z 20.6..58.4 (6 m modules, yaw=-90: local X -> world -Z? 
    # yaw=-90: local +X -> world -Z, local +Z -> world -X. Rail along local X becomes along -Z. Good.
    # place at X=-11.47 so rail faces glass (local +Z toward -X after yaw=-90)
    for i, z0 in enumerate([23.6, 29.6, 35.6, 41.6, 47.6, 53.6]):
        place(PL, A_r, -11.47, F3_Y, z0, -90)
    # lounge seats in walk, facing glass (yaw=90 -> local +Z to -X)
    for i, z in enumerate([22.5, 27.0, 31.5, 36.0, 40.5, 45.0, 49.5, 54.0]):
        place(PL, A_s, -4.2, F3_Y, z, 90)
        if i % 2 == 0:
            place(PL, A_m, -5.4897, F3_Y, round(z + 1.8 + 0.0104, 4), 0, local=False)
    return dict(cabanas=8, rails=6, seats=8, mounds=7 + 4, vines=7)
