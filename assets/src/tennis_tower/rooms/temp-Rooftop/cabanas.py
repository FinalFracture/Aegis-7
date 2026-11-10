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
    """Green-wall post. Envelope x±0.10, z±0.12, y 0..2.8. Leaves may break mirror symmetry."""
    it = It()
    it.b('Plate', KP, -0.04, 0.04, 0.03, 2.776, -0.02, 0.02, col=True)
    it.b('PlateShoe', SSL, -0.07, 0.07, 0, 0.034, -0.05, 0.05)
    it.b('PlateCap', KP, -0.05, 0.05, 2.772, 2.8, -0.03, 0.03)
    for y in (0.6, 1.4, 2.2):
        for s in (1.0, -1.0):
            it.a('Bolt', SGM, node((0.0, y, s * (0.02 + 0.004)), 0.008))
    front0 = [(0.03, 0.08, 0.03), (0.06, 0.9, 0.05), (0.02, 1.7, 0.03), (0.05, 2.55, 0.04)]
    back0 = [(-0.03, 0.08, -0.03), (-0.05, 0.8, -0.05), (-0.02, 1.6, -0.03), (-0.05, 2.5, -0.04)]

    def push(pts, sign, floor):
        out = []
        for x, y, z in pts:
            if abs(z) < floor:
                z = sign * floor
            out.append((x, y, z))
        return out

    def inside(m):
        lo, hi = m.bounds
        return (lo[0] >= -0.10 - 1e-6 and hi[0] <= 0.10 + 1e-6 and lo[1] >= -1e-6 and hi[1] <= 2.8 + 1e-6
                and lo[2] >= -0.12 - 1e-6 and hi[2] <= 0.12 + 1e-6)

    def clip(m):
        v = np.array(m.vertices, float, copy=True)
        v[:, 0] = np.clip(v[:, 0], -0.10, 0.10)
        v[:, 1] = np.clip(v[:, 1], 0.0, 2.8)
        v[:, 2] = np.clip(v[:, 2], -0.12, 0.12)
        m.vertices = v
        return m

    # vine() parks each leaf r*2.2 toward +Z. On the -Z strand that bias points into the
    # plate, so that strand is held out far enough for an embed of about 8 mm, never past 10.
    leaf_len, stems, leaves = 0.12, None, None
    for _ in range(10):
        flare = 0.012 + 0.16 * leaf_len
        back_floor = max(0.031, 0.011 * 2.2 + flare + 0.012)
        st1, lv1 = vine(push(front0, 1.0, 0.031), r=0.011, leaf_every=0.28, leaf_len=leaf_len, seed=7, outward=True)
        st2, lv2 = vine(push(back0, -1.0, back_floor), r=0.011, leaf_every=0.28, leaf_len=leaf_len, seed=8, outward=True)
        stems, leaves = merge([st1, st2]), merge([lv1, lv2])
        if inside(stems) and inside(leaves):
            break
        leaf_len *= 0.8
    else:
        clip(leaves)
    # Drop a leaf whose vertices sit >6 mm inside the plate (|x|<0.034, |z|<0.014, plate y).
    kept = []
    for part in leaves.split(only_watertight=False):
        v = np.asarray(part.vertices)
        if np.any((np.abs(v[:, 0]) < 0.034) & (np.abs(v[:, 2]) < 0.014) & (v[:, 1] >= 0.03) & (v[:, 1] <= 2.776)):
            continue
        uv = part.metadata.get('uv')
        if uv is None or len(uv) != len(v):
            part.metadata['uv'] = np.zeros((len(v), 2))
        kept.append(part)
    leaves = merge(kept)
    it.a('VineStem', LF, stems)
    it.a('VineLeaves', LF2, leaves)
    for c, seed in (((0.04, 0.05, 0.07), 31), ((-0.04, 0.05, -0.07), 32)):
        it.a('MossTuft', LF, clip(clump(c, 0.045, seed)))
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
            place(PL, A_m, -9.0, F3_Y, gz, 0)
            place(PL, A_v, -10.6, F3_Y, gz, 0)
    # view rails along W glass covering Z 20.6..58.4 (6 m modules, yaw=-90: local X -> world -Z? 
    # yaw=-90: local +X -> world -Z, local +Z -> world -X. Rail along local X becomes along -Z. Good.
    # place at X=-11.65 so rail faces glass (local +Z toward -X after yaw=-90)
    for i, z0 in enumerate([23.6, 29.6, 35.6, 41.6, 47.6, 53.6]):
        place(PL, A_r, -11.65, F3_Y, z0, -90)
    # lounge seats in walk, facing glass (yaw=90 -> local +Z to -X)
    for i, z in enumerate([22.5, 27.0, 31.5, 36.0, 40.5, 45.0, 49.5, 54.0]):
        place(PL, A_s, -4.2, F3_Y, z, 90)
        if i % 2 == 0:
            place(PL, A_m, -5.5, F3_Y, z + 1.8, 0)
    return dict(cabanas=8, rails=6, seats=8, mounds=7 + 4, vines=7)
