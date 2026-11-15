"""Rook r8b (2026-11-15): spec Rev 3.7 #5 / Rev 3.7.1 pool walk-outs (TTQA-009/010), building coords (X axial, Z across, Y up, F1 = 0).
Lap tank: recessed E-alcove stair X 27.44..29.6, Z 0.5..3.8 (11 x 0.178 / 10 x 0.28, rails both sides) + 3 ladders (N X12.5, W Z20.8,
E Z19.5). Diving well: in-tank stair X 26.6..27.94 (13 x 0.18 to Z 30.34 / y -0.16, landing to 29.14, 12 x 0.18 to Z 26.06 / +2.0, top landing
Z 26.06..24.56 exiting +X) + ladders at Z 23.0 on the E and W walls. Lazy river: 4 bank entries (6 x 0.16 / 5 x 0.28, 1.4 m projection,
1.2 m clear between rails) + the runout W-wall stair X 5.0..6.4 onto the island strip. Solids are manifold unions (no internal / coplanar
faces); every solid lands in the room kit's Solid-colonly. Gage owns water volumes and the ladder climb Area3Ds."""
import numpy as np, trimesh
from struct_lib import *
TI, WA, RU = 'aq_tile', 'aq_water', 'aq_rubber'
RAIL_R = .021
def U(ms):
    def vol(x):
        y = trimesh.Trimesh(np.asarray(x.vertices), np.asarray(x.faces), process=True); y.merge_vertices(); trimesh.repair.fix_normals(y); return y
    m = trimesh.boolean.union([vol(x) for x in ms], engine='manifold') if len(ms) > 1 else vol(ms[0])
    m.metadata['uv'] = m.vertices[:, [0, 2]] / 2.0 + m.vertices[:, [1, 1]] * [0, .5]; return m
def path(pts, r=RAIL_R, seg=8):
    """one closed rail/stringer: tubes between points + ball joints, unioned."""
    ms = [tube(a, b, r, seg) for a, b in zip(pts[:-1], pts[1:])] + [trimesh.creation.icosphere(1, r * 1.0).apply_translation(p) for p in pts[1:-1]]
    return U(ms)
def steps_z(xa, xb, y0, z_top_face, dirz, tops, tread=.28, extra=()):
    """stepped solid along Z: step k (top tops[k]) spans tread k counted from the TOP face z_top_face going dirz (down the stair); each block
    runs from y0 up to its top and back to the top face, so the union is a single stepped solid. extra: more boxes to union."""
    bs = []
    for k, yt in enumerate(tops):                         # k = 0 is the highest tread (next to the top face)
        za, zb = sorted((z_top_face, z_top_face + dirz * tread * (k + 1)))
        bs.append(box(xa, xb, y0, yt, za, zb))
    return U(bs + list(extra))
def nosings(it, xa, xb, z_top_face, dirz, tops, tread=.28):
    for k, yt in enumerate(tops):
        zf = z_top_face + dirz * tread * (k + 1)          # nosing edge of tread k
        za, zb = sorted((zf + dirz * .002, zf - dirz * .04))          # front 2 mm proud of the riser (no shared plane)
        B = box(xa + .03, xb - .03, yt - E, yt + .006, za, zb); B.metadata['uv'] = B.vertices[:, [0, 2]]; it.append(('Step_Nosing_Cyan', CY, B))
def stair_rails(it, xs, z_top_face, dirz, tops, deck_y, floor_y, tread=.28, h=.865, ext=.3):
    """handrails both sides along the nosing line (h above) with level extensions (0.3 m over the deck, one tread past the bottom nosing);
    posts stand under the two level ends (bottom one on the tank / river floor)."""
    n = len(tops); zb = z_top_face + dirz * tread * n; ybot = tops[-1]
    for x in xs:
        pts = [(x, ybot + h, zb + dirz * tread), (x, ybot + h, zb), (x, deck_y + h, z_top_face), (x, deck_y + h, z_top_face - dirz * ext)]
        it.append(('Pool_Handrail', ST, path(pts)))
        for zz, yy, yr in ((zb + dirz * (tread - .06), floor_y, ybot + h), (z_top_face - dirz * (ext - .05), deck_y, deck_y + h)):
            it.append(('Pool_RailPosts', ST, tube((x, yy - E, zz), (x, yr - RAIL_R + .006, zz), .024, 8)))
def ladder(it, x, z, n, y_floor, deck_y, face):
    """pool ladder on a tank wall: (x, z) = point on the lining inner face, n = (nx, nz) into the water; stringers +-0.25 along the wall,
    0.12 off the face; grab rails return 0.45 over the coping and land on the deck finish; rungs every 0.3 m (4 mm bite into the stringers)."""
    n = np.array([n[0], 0, n[1]], float); t = np.array([-n[2], 0, n[0]]); p0 = np.array([x, 0, z]) + n * .12; top = deck_y + .9
    for s in (-.25, .25):
        b = p0 + t * s
        pts = [b + [0, y_floor - E, 0], b + [0, top, 0], b - n * (.12 + .45) + [0, top, 0], b - n * (.12 + .45) + [0, deck_y + .012 - E, 0]]
        it.append(('Ladder_Stringers', ST, path(pts, .025)))
    for y in np.arange(y_floor + .35, deck_y - .1, .3):
        a, b = p0 + t * -.229 + [0, y, 0], p0 + t * .229 + [0, y, 0]
        it.append(('Ladder_Rungs', ST, tube(a, b, .02, 8)))
        c = trimesh.creation.box((.43, .012, .06)); R = np.eye(4); R[:3, 0] = t; R[:3, 2] = n; R[:3, 3] = p0 + [0, y + .02 + .006 - .004, 0]; c.apply_transform(R)
        c.metadata['uv'] = c.vertices[:, [0, 2]]; it.append(('Ladder_Tread_Rubber', RU, c))
def lap_access():
    it = []; y0 = .0; r = (2.012 - .04) / 11; tops = [2.012 - r * k for k in range(1, 11)]   # 11 equal risers 0.1793 floor +0.04 -> deck finish +2.012
    floor = [box(27.5, 29.6, 0.0, .04, .5, 3.8), box(27.437, 27.504, 0.0, .04, .556, 3.8)]   # clear of the S lining end (X <= 27.496, Z <= 0.556)
    s = steps_z(27.44, 29.6, y0, 3.8, -1, tops, extra=floor); it.append(('Lap_Stair_Tile', TI, s))
    nosings(it, 27.44, 29.6, 3.8, -1, tops)
    stair_rails(it, (27.56, 29.48), 3.8, -1, tops, 2.012, .04)
    w = box(27.44, 29.596, 1.915, 1.92, .56, 3.776)   # starts clear of the bay-26 facade fin (X 27.915..27.965, Z <= 0.551); w.metadata['uv'] = w.vertices[:, [0, 2]]; it.append(('Water_Opaque', WA, w))
    ladder(it, 12.5, 21.444, (0, -1), .035, 2.0, 'N'); ladder(it, 2.556, 20.8, (1, 0), .035, 2.0, 'W'); ladder(it, 27.444, 19.5, (-1, 0), .035, 2.0, 'E')
    return it
def dive_access():
    it = []; f1 = [-2.5 + .18 * k for k in range(1, 14)]                  # flight 1 tread tops -2.32 .. -0.16 (13th = landing)
    f2 = [-.16 + .18 * j for j in range(1, 12)]                           # flight 2 tread tops 0.02 .. 1.82 (12th riser to the +2.0 landing)
    xa, xb, yb = 26.6, 27.94, -2.469
    bs = [box(xa, xb, yb, 2.0, 24.56, 26.06)]                              # top landing
    for j, yt in enumerate(reversed(f2)):                                  # flight 2 treads from the top (26.06) going +Z
        bs.append(box(xa, xb, yb, yt, 26.06 - .004, 26.06 + .28 * (j + 1)))
    bs.append(box(xa, xb, yb, -.16, 29.14 - .004, 30.34))                  # mid landing
    for k, yt in enumerate(reversed(f1[:-1])):                             # flight 1 treads from the landing (30.34) going +Z to 33.7
        bs.append(box(xa, xb, yb, yt, 30.34 - .004, 30.34 + .28 * (k + 1)))
    it.append(('Dive_Stair_Tile', TI, U(bs)))
    nosings(it, xa, xb, 26.06, 1, list(reversed(f2))); nosings(it, xa, xb, 30.34, 1, list(reversed(f1[:-1])))
    for x in (26.66, 27.88):
        pts = [(x, f1[0] + .865, 33.56), (x, -.16 + .865, 30.34), (x, -.16 + .865, 29.14), (x, 2.0 + .865, 26.06), (x, 2.0 + .865, 25.0)]
        it.append(('Pool_Handrail', ST, path(pts)))
        for zz, yy, yr in ((33.56, f1[0], f1[0] + .865), (29.74, -.16, -.16 + .865), (25.1, 2.0, 2.865)):
            it.append(('Pool_RailPosts', ST, tube((x, yy - E, zz), (x, yr - RAIL_R + .006, zz), .024, 8)))
    ladder(it, 27.944, 23.0, (-1, 0), -2.465, 2.0, 'E'); ladder(it, 15.056, 23.0, (1, 0), -2.465, 2.0, 'W')
    return it
def bank_entry(it, xc, z_face, dirz):
    """6 risers x 0.16 from the river floor (tile +0.035) to the +1.0 deck: 5 treads x 0.28 from the bank lining face going dirz."""
    tops = [1.0 - .16 * k for k in range(1, 6)]                            # 0.84 .. 0.20 from the bank
    xa, xb = xc - .7, xc + .7; z_face -= dirz * .004                      # 4 mm bite into the bank lining (no shared face)
    it.append(('River_Entry_Tile', TI, steps_z(xa, xb, .031, z_face, dirz, tops)))
    nosings(it, xa, xb, z_face, dirz, tops)
    stair_rails(it, (xa + .06, xb - .06), z_face, dirz, tops, 1.012, .035)
def river_access():
    it = []
    bank_entry(it, 21.7, 47.055, 1); bank_entry(it, 16.3, 49.945, -1); bank_entry(it, 11.3, 74.945, -1); bank_entry(it, 6.7, 72.055, 1)
    bank_entry(it, 5.752, 70.944, -1)                                      # runout W-end stair X 5.052..6.452 (4 mm bite into the W lining), onto the island strip Z 71..72
    return it
