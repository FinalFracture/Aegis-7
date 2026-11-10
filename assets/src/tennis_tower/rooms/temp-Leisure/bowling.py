"""F1-BOWL (X 30..57, Z 0.25..14.65). Rev 3.2 s5: 4 lane pairs x 3.6 m, settees X30..32.4, approach X32.4..37,
head pin X54, pin deck X54..57 (masking only; pinsetter machinery is in the SE plant stack, not ours).
50 mm clear of stand face Z14.7. Rev 3.0 #4: 50 mm panels on ST+S1 W face X57 (Z2.6..13.2) + stubs."""
from lz_lib import *
LZ = [(.14, .38, 'G'), (.38, 1.446, 'L'), (1.446, 1.686, 'G'), (1.686, 1.914, 'C'), (1.914, 2.154, 'G'), (2.154, 3.22, 'L'), (3.22, 3.46, 'G')]
def lane_pair():
    it = It(); x0, x1 = 32.4, 56.9
    it.b('Lane_Bed', G, x0, x1, 0, .03, 0, 3.6, col=True)
    for a, b, k in LZ:
        if k == 'L':
            it.b('Lane_Approach', LN, x0 + D, 36.98, .026, .058, a + D, b - D)
            it.b('Lane_Surface', LN, 37.02, 56.2, .026, .06, a + D, b - D)
            it.b('Foul_Line', AM, 36.982, 37.018, .026, .05, a + .01, b - .01)
            for j in range(7):  # target arrows
                zz = a + .13 + j*(b - a - .26)/6; xa = 41.2 + abs(j - 3)*.3
                it.b('Lane_Arrows', CY, xa, xa + .22, .058, .064, zz - .012, zz + .012)
            for j in range(5): zz = a + .15 + j*(b - a - .3)/4; it.b('Approach_Dots', CY, 34.4, 34.44, .056, .061, zz - .02, zz + .02)
            for xr in (40.0, 47.0, 52.0):  # court-line style lane inlays (sport cue)
                it.b('Lane_CourtLine', BA, xr, xr + .03, .058, .063, a + .05, b - .05)
            zc = (a + b)/2; s = .3048
            for r in range(4):
                for q in range(r + 1):
                    it.a('Pins', WH, pin((54.0 + r*s*.866, .058, zc + (q - r/2)*s)))
        elif k == 'G':
            it.b('Gutters', SL, 37.02, 56.2, .026, .04, a + D, b - D)
            it.b('Gutters', SL, x0 + D, 36.98, .026, .052, a + D, b - D)
        else:
            it.b('Capping', ST, 37.3, 54.55, .026, .12, a + D, b - D)
            it.b('Capping_Reveal', CY, 37.3, 54.55, .116, .124, a + .08, b - .08)
            it.b('Approach_Divider', SL, x0 + D, 36.98, .026, .054, a + D, b - D)
    for a, b in ((0, .14), (3.46, 3.6)): it.b('Capping', ST, 37.3, 54.55, .026, .14, a + D, b - D); it.b('Approach_Edge', SL, x0 + D, 36.98, .026, .054, a + D, b - D)
    # pin deck kickbacks + pit curtain (masking side only)
    for z in (.02, 1.75, 3.5):
        it.b('Kickbacks', G, 54.6, 56.6, .026, 1.1, z, z + .08, col=True)
        it.b('Kickback_LED', AM, 54.62, 56.58, 1.096, 1.11, z + .01, z + .07)
    it.b('Pit_Curtain', FA, 56.62, 56.85, .026, 1.2, .1, 3.5)
    # masking unit: sculpted panel with leaf crests + ball medallions
    it.b('Masking_Frame', G, 54.3, 54.5, 1.35, 2.55, .02, 3.58)
    it.b('Masking_Face', SL, 54.25, 54.304, 1.4, 2.5, .07, 3.53)
    it.b('Masking_Reveal', CY, 54.246, 54.256, 1.43, 1.46, .1, 3.5)
    for zc in (.9, 2.7):
        it.a('Masking_Ball', BA, cap((54.232, 2.05, zc), .22, .03, 16, 'x'))
        it.a('Masking_Seam', WH, cap((54.214, 2.05, zc), .03, .01, 8, 'x'))
        for k in range(6): it.a('Masking_LeafCrest', LF2, wall_leaf((54.25, 1.55, zc - .5 + .2*k), (k - 2.5)*.25, .5, .16, face=-1))
    for z in (.3, 3.3): it.a('Masking_Hangers', ST, tube((54.4, 2.546, z), (54.4, 5.71, z), .025, 6))
    # ball return between the pair (on the approach)
    it.b('Return_Plinth', G, 33.0, 35.6, .05, .16, 1.62, 1.98, col=True)
    hood = rrect(.7, .36, .12, 4)
    it.a('Return_Hood', WH, xf(prism(hood, .156, .9), t=(33.5, 0, 1.8)))
    it.b('Return_Track', ST, 33.86, 35.6, .156, .3, 1.66, 1.94)
    it.a('Return_Vent', CY, box(33.15, 33.85, .7, .74, 1.618, 1.623))
    for k, mk in enumerate((BA, CY, VIO, BA, GRN)):
        it.a('Return_Balls', mk, node((34.1 + k*.24, .41, 1.8), .108, 1))
    it.col(33.15, 33.85, .05, .9, 1.62, 1.98)
    # overhead scoring screen above the approach (opaque emissive)
    it.b('Score_Housing', G, 33.6, 33.8, 3.0, 3.9, .25, 3.35)
    it.b('Score_Plate', SL, 33.55, 33.604, 3.06, 3.84, .32, 3.28)
    for i in range(5):
        yy = 3.12 + i * 0.13
        it.b('Score_Rows', CY if i % 2 == 0 else AM, 33.54, 33.546, yy, yy + 0.06, .45, 1.55)
    it.b('Score_Border', BA, 33.54, 33.546, 3.08, 3.1, .4, 3.2)
    it.b('Score_Ticker', AM, 33.54, 33.546, 3.78, 3.82, .45, 3.15)
    it.a('Score_Ball', BA, cap((33.532, 3.45, 2.6), 0.05, 0.012, 10, 'x'))
    for z in (.6, 3.0): it.a('Score_Hangers', ST, tube((33.7, 3.896, z), (33.7, 5.71, z), .025, 6))
    return emit('tt_bowl_lane_pair', it, 'one lane pair (2 lanes, 3.6 m); place at Z0.3+3.6k; pin deck masking only')

def settee():
    """settee + scoring console per pair, X 30..32.4 (local Z 0..3.6); green wall + leaf crests on the X30 wall face."""
    it = It()
    it.bv('Settee_Plinth', G, 30.25, 31.25, 0, .2, .414, 3.186, col=True)
    it.b('Settee_Seat', FA, 30.52, 31.23, .196, .44, .418, 3.182, col=True)
    it.b('Settee_Back', FA, 30.2, 30.5, .196, 1.0, .418, 3.182, col=True)
    for z in (.31, 3.29): it.b('Settee_Arms', WH, 30.2, 31.26, 0, .66, z - .1, z + .1)
    for k in range(5): it.b('Settee_Tufts', SL, 30.497, 30.51, .5, .9, .45 + .6*k, .55 + .6*k)
    it.b('Settee_LED', CY, 30.8, 31.2, .02, .04, .298, .302)
    it.b('Console_Pedestal', G, 31.6, 31.9, 0, .7, 1.65, 1.95, col=True)
    it.b('Console_Top', WH, 31.4, 32.1, .696, .74, 1.4, 2.2)
    it.b('Console_Plate', SL, 31.55, 31.95, .738, .748, 1.55, 2.05)
    for i in range(3):
        zz = 1.6 + i * 0.12
        it.b('Console_Rows', CY if i % 2 == 0 else AM, 31.62, 31.88, .752, .758, zz, zz + 0.05)
    it.b('Console_Tick', AM, 31.64, 31.86, .752, .758, 1.98, 2.02)
    it.a('Console_Ball', BA, node((31.75, .85, 2.12), .06, 1))
    # ball rack
    it.b('Rack_Frame', ST, 31.5, 32.2, 0, .06, .4, 1.2)
    for z in (.42, 1.18): it.a('Rack_Posts', ST, tube((31.85, .056, z), (31.85, .6, z), .02, 6))
    it.a('Rack_Rail', ST, tube((31.6, .5, .42), (31.6, .5, 1.18), .02, 6)); it.a('Rack_Rail', ST, tube((32.1, .5, .42), (32.1, .5, 1.18), .02, 6))
    for k, mk in enumerate((BA, CY, VIO)): it.a('Rack_Balls', mk, node((31.85, .62, .6 + .2*k), .095, 1))
    # moss green wall + leaf crests (nature) on the X30 wall face, above the settee
    gw = xf(green_wall(-3.2, -.4, 1.2, 3.4, 0, .2, 11), R=trimesh.transformations.rotation_matrix(math.pi/2, [0, 1, 0]), t=(30.0, 0, 0))
    it.a('Moss_Wall', LF, gw)
    it.b('Moss_Wall_Frame', G, 30.0, 30.06, 1.0, 1.08, .3, 3.3)
    for k in range(7): it.a('Leaf_Crests', LF2, wall_leaf((30.0, 3.62, .5 + .43*k), (k - 3)*.15, .45, .18))
    return emit('tt_bowl_settee', it, 'settee + scorer + ball rack + moss wall; per lane pair')

def acoustic():
    """50 mm fabric panels on the ST+S1 W face / stubs at X57 (Z0.3..14.7), X 56.95..57.002, y 0.15..5.6."""
    it = It(); zs = np.arange(.3, 14.7 - .01, 1.2)
    for z in zs:
        z1 = min(z + 1.2, 14.7)
        for y in np.arange(.15, 5.5, 1.35):
            it.b('Acoustic_Panels', FA, 56.95, 57.002, y + .01, y + 1.34, z + .01, z1 - .01)
        it.b('Panel_Reveal', CY, 56.946, 56.95 + D, 2.9, 2.94, z + .1, z1 - .1)
    for k, z in enumerate(np.arange(1.0, 14.5, 1.8)):
        for j in range(4): it.a('Panel_LeafRelief', LF2, wall_leaf((56.95, 3.4 + .35*j, z + (j % 2)*.2), .35*(j - 1.5), .5, .2, face=-1))
    it.b('Panel_Base', G, 56.9, 57.002, 0, .15, .3, 14.7, col=True)
    return emit('tt_bowl_core_acoustic', it, 'ST+S1 W face lining (Rev 3.0 #4); built in place')

def build(PL):
    lp = lane_pair(); st = settee(); ac = acoustic()
    for k in range(4):
        place(PL, lp, 0, 0, .25 + 3.6*k); place(PL, st, 0, 0, .25 + 3.6*k)
    place(PL, ac, 0, 0, 0, local=True)
if __name__ == '__main__':
    PL = []; build(PL)
    for r in REP:
        if not r["passed"]: print(r["asset"], r["bad"], r["coplanar"], r["open"], r["pivot"])
