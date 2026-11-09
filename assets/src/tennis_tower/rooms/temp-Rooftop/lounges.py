"""F3-SLNG S/N rear lounges for Tennis Tower (spec Rev 3.0)."""
from rt_lib import *

HALF = {'tt_cab_lounge_seat': (0.9, 0.35), 'tt_cab_dress_mound': (0.56, 0.38), 'tt_cab_dress_vine': (0.076, 0.099)}
KIND = {'tt_cab_lounge_seat': 'seats', 'tt_cab_dress_mound': 'mounds', 'tt_cab_dress_vine': 'vines'}
# S-band pod, pitch 4 m: rear seat, vines, rear mound, front seat, mid mound. N mirrors z and yaw.
POD = (('tt_cab_lounge_seat', 0.0, 7.85), ('tt_cab_dress_vine', -1.2, 8.75), ('tt_cab_dress_vine', 1.2, 8.75),
       ('tt_cab_dress_mound', 2.0, 7.85), ('tt_cab_lounge_seat', 2.0, 5.0), ('tt_cab_dress_mound', 2.0, 6.45))
SEGS = {'S': ((24.5, 34.92), (64.02, 85.98), (92.02, 125.0)),
        'N': ((24.5, 56.78), (64.02, 85.98), (92.02, 125.0))}
BAND = {'S': (24.5, 125.0, 2.5, 9.1), 'N': (24.5, 125.0, 69.9, 76.5)}
# XZ keep-outs (x0, x1, z0, z1). N is written out; it is not a mirror of S.
KO = {
    'S': ((34.94, 57.06, 2.5, 9.1), (57.0, 64.0, 2.6, 13.2), (86.0, 92.0, 2.6, 13.2),
          (56.8, 58.2, 7.8, 9.2), (64.8, 66.2, 7.8, 9.2), (83.8, 85.2, 7.8, 9.2), (100.8, 102.2, 7.8, 9.2),
          (-1e4, 1e4, 9.08, 9.3),
          (36.4, 39.1, 2.5, 9.1), (53.9, 56.6, 2.5, 9.1), (76.9, 79.6, 2.5, 9.1),
          (82.9, 85.6, 2.5, 9.1), (92.4, 95.1, 2.5, 9.1), (103.9, 106.6, 2.5, 9.1),
          (-1e4, 1e4, 0.0, 2.52)),
    'N': ((58.0, 64.0, 65.8, 76.4), (86.0, 92.0, 65.8, 76.4),
          (56.8, 58.2, 69.8, 71.2), (64.8, 66.2, 69.8, 71.2), (83.8, 85.2, 69.8, 71.2), (100.8, 102.2, 69.8, 71.2),
          (-1e4, 1e4, 69.7, 69.92),
          (36.4, 39.1, 69.9, 76.5), (54.9, 57.6, 69.9, 76.5), (76.9, 79.6, 69.9, 76.5),
          (82.9, 85.6, 69.9, 76.5), (92.4, 95.1, 69.9, 76.5), (103.9, 106.6, 69.9, 76.5),
          (-1e4, 1e4, 77.58, 79.0)),
}
GAP, EPS = 0.02, 1e-6


def world_aabb(px, pz, yaw, hx, hz):
    """World XZ AABB. Same yaw map as rt_lib.place: x += lx*cos + lz*sin, z += -lx*sin + lz*cos."""
    a = math.radians(yaw)
    co, si = math.cos(a), math.sin(a)
    xs, zs = [], []
    for lx in (-hx, hx):
        for lz in (-hz, hz):
            xs.append(px + lx * co + lz * si)
            zs.append(pz - lx * si + lz * co)
    return (min(xs), max(xs), min(zs), max(zs))


def grown_hits(box, kos):
    x0, x1, z0, z1 = box[0] - GAP, box[1] + GAP, box[2] - GAP, box[3] + GAP
    for a, b, c, d in kos:
        if x0 < b - EPS and x1 > a + EPS and z0 < d - EPS and z1 > c + EPS:
            return True
    return False


def leaves(box, x0, x1, z0, z1):
    return box[0] - GAP < x0 - EPS or box[1] + GAP > x1 + EPS or box[2] - GAP < z0 - EPS or box[3] + GAP > z1 + EPS


def xz_gap(a, b):
    sx = max(a[0] - b[1], b[0] - a[1])
    sz = max(a[2] - b[3], b[2] - a[3])
    if sx > 0 and sz > 0:
        return math.hypot(sx, sz)
    return max(sx, sz)


def check_placements(new):
    bad, boxes = [], []
    for p in new:
        box = world_aabb(p['p'][0], p['p'][2], p['yaw'], *HALF[p['asset']])
        side = 'S' if p['p'][2] < 40 else 'N'
        bx0, bx1, bz0, bz1 = BAND[side]
        if box[0] < bx0 - EPS or box[1] > bx1 + EPS or box[2] < bz0 - EPS or box[3] > bz1 + EPS:
            bad.append(f'band {side} {p["asset"]} {p["p"]}')
        if abs(p['p'][1] - F3_Y) > 0.005:
            bad.append(f'y {p["p"]}')
        for k in KO[side]:
            if grown_hits(box, (k,)):
                bad.append(f'keep {side} {p["asset"]} {p["p"]} {k}')
        boxes.append(box)
    mc = None
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            g = xz_gap(boxes[i], boxes[j])
            mc = g if mc is None else min(mc, g)
            if g < GAP - EPS:
                bad.append(f'pair {i},{j} gap={g:.4f}')
    if bad:
        raise AssertionError('placement breaches: ' + '; '.join(bad))
    return 0.0 if mc is None else mc


def build(PL):
    new, st = [], dict(S=dict(seats=0, mounds=0, vines=0), N=dict(seats=0, mounds=0, vines=0), skipped=0)
    for side in ('S', 'N'):
        bz0, bz1 = BAND[side][2], BAND[side][3]
        for x0, x1 in SEGS[side]:
            c = x0 + 1.3
            while c + 1.0 <= x1:
                for asset, dx, zs in POD:
                    x, z = c + dx, zs if side == 'S' else 79.0 - zs
                    yaw = 0 if side == 'S' else 180
                    box = world_aabb(x, z, yaw, *HALF[asset])
                    if leaves(box, x0, x1, bz0, bz1) or grown_hits(box, KO[side]):
                        st['skipped'] += 1
                        continue
                    new.append(dict(glb=str(GM / f'{asset}.glb'), asset=asset,
                                    p=[round(x, 4), round(F3_Y, 4), round(z, 4)], yaw=yaw, tag='f3'))
                    st[side][KIND[asset]] += 1
                c += 4.0
    st['min_clear'] = check_placements(new)
    PL.extend(new)
    return st
