"""F1-ARC / F2-ARC (X 113..140, Z 0..79), Rev 3.2 s4. Cabinets are instanced GLBs (local front +Z, bottom-centre),
yaw 90 = facing +X. Mix per floor: ~40 video, 20 redemption, 10 claw, 10 sit-down racers, 6 air hockey, 4 pinball (row), 4 VR pods.
Prize counter on L1 north of ST+E. Feature stair X126..139, Z38..40.5 (decorative, mid landing). No slab cuts are made here."""
from lz_lib import *
def _buttons(it, y, z, xs, mk=BA): [it.a('Buttons', mk, cap((x, y, z), .022, .012, 8, 'y')) for x in xs]
def paint_screen(it, x0, x1, y0, y1, z0, z1, kind='court'):
    """Readable opaque-emissive screen art (sports/nature). Art offset clear of plate; ball clear of bars."""
    dx, dy, dz = abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)
    it.b('Screen_Plate', SL, x0, x1, y0, y1, z0, z1)
    if dz <= dx and dz <= dy:  # face in Z
        zf = max(z0, z1) + 0.004
        def hbar(ya, yb, mk=CY): it.b('Scr_Art', mk, x0 + .06, x1 - .06, ya, yb, zf, zf + .003)
        def vbar(xa, xb, mk=CY): it.b('Scr_Art', mk, xa, xb, y0 + .08, y1 - .08, zf, zf + .003)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if kind == 'court':
            hbar(y0 + .08, y0 + .1); hbar(y1 - .1, y1 - .08)
            vbar(x0 + .08, x0 + .1); vbar(x1 - .1, x1 - .08)
            it.a('Scr_Ball', BA, cap((cx, cy, zf + .014), min(.05, dy * .18), .012, 12, 'z'))
            it.a('Scr_Leaf', LF2, zwall_leaf((cx + dy * .22, y1 - .14, zf + .01), .2, .26, .1))
        elif kind == 'track':
            for i, mk in enumerate((AM, BA, AM)):
                yy = y0 + .12 + i * (dy - .28) / 2.5; hbar(yy, yy + .025, mk)
            hbar(y1 - .12, y1 - .08, CY)
            it.a('Scr_Ball', BA, cap((cx, y0 + dy * .55, zf + .014), .04, .012, 10, 'z'))
        elif kind == 'score':
            for i in range(4):
                yy = y0 + .1 + i * (dy - .28) / 3.5; hbar(yy, yy + .035, CY if i % 2 == 0 else AM)
            for i in range(3): it.b('Scr_Dot', VIO, x0 + .1 + i * .12, x0 + .14 + i * .12, y1 - .12, y1 - .08, zf + .002, zf + .005)
        else:
            hbar(y0 + .12, y0 + .14, CY)
            for i in range(3): it.a('Scr_Leaf', LF2, zwall_leaf((x0 + .18 + i * .18, cy, zf + .01), (i - 1) * .3, .3, .11))
            it.a('Scr_Ball', BA, cap((cx, y1 - .14, zf + .014), .04, .012, 10, 'z'))
    elif dy <= dx:
        yf = max(y0, y1) + 0.004
        it.b('Scr_Art', CY, x0 + .08, x1 - .08, yf, yf + .003, z0 + .08, z1 - .08)
        it.a('Scr_Ball', BA, cap(((x0 + x1) / 2, yf + .014, (z0 + z1) / 2), .05, .012, 10, 'y'))
    else:
        xf = max(x0, x1) + 0.004
        def hbar(ya, yb, mk=CY): it.b('Scr_Art', mk, xf, xf + .003, ya, yb, z0 + .06, z1 - .06)
        def vbar(za, zb, mk=CY): it.b('Scr_Art', mk, xf, xf + .003, y0 + .08, y1 - .08, za, zb)
        cz, cy = (z0 + z1) / 2, (y0 + y1) / 2
        hbar(y0 + .08, y0 + .1); hbar(y1 - .1, y1 - .08, AM if kind == 'track' else CY)
        vbar(z0 + .08, z0 + .1); vbar(z1 - .1, z1 - .08)
        it.a('Scr_Ball', BA, cap((xf + .014, cy, cz), min(.05, dy * .18), .012, 12, 'x'))
def video():
    it = It(); w = .72
    it.bv('Cab_Plinth', G, -w/2, w/2, 0, .1, -.42, .4, col=True)
    it.bv('Cab_Body', SL, -w/2 + .02, w/2 - .02, .1 + D, 1.9, -.42, .1, col=True)
    it.b('Cab_Deck', G, -w/2 + .02, w/2 - .02, .1 + D, .92, .1 + D, .4, col=True)
    it.b('Cab_Panel', WH, -w/2 + .06, w/2 - .06, .916, .96, .12, .38)
    _buttons(it, .962, .25, (-.18, -.1, .1, .18, .26))
    it.a('Joystick', ST, tube((-.2, .956, .3), (-.2, 1.072, .3), .01, 6)); it.a('Joystick_Ball', BA, node((-.2, 1.095, .3), .025, 1))
    it.b('Screen_Bezel', G, -w/2 + .05, w/2 - .05, 1.05, 1.62, .098, .14)
    paint_screen(it, -w/2 + .09, w/2 - .09, 1.09, 1.58, .136, .146, 'court')
    it.b('Marquee', AM, -w/2 + .05, w/2 - .05, 1.68, 1.86, .096, .108)
    for s in (-1, 1): it.b('Side_LED', VIO, min(s*(w/2 - .024), s*(w/2 - .014)), max(s*(w/2 - .024), s*(w/2 - .014)), .2, 1.85, -.05, .08)
    for k in range(3): it.a('Side_Leaf', LF2, wall_leaf((w/2 - .02, .5 + .35*k, -.2), .3*(k - 1), .3, .12))
    it.b('Coin_Plate', ST, -.1, .1, .3, .5, .396, .404)
    return emit('tt_arc_video', it, 'upright video cabinet 0.72 x 0.82 m')
def redemption():
    it = It(); w = 1.0
    it.b('Red_Plinth', G, -w/2, w/2, 0, .12, -.55, .55, col=True)
    it.b('Red_Body', WH, -w/2 + .02, w/2 - .02, .116, 2.2, -.55, .1, col=True)
    it.b('Red_Ramp', SL, -w/2 + .02, w/2 - .02, .116, .95, .1 - D, .55, col=True)
    it.a('Red_Wheel', CY, cap((0, 1.55, .118), .38, .04, 24, 'z')); it.a('Red_Hub', BA, cap((0, 1.55, .148), .08, .03, 12, 'z'))
    for k in range(8): a = k*math.pi/4; it.b('Red_Spokes', AM, -.012, .012, 1.55 + .14, 1.55 + .34, .136, .15).apply_transform(trimesh.transformations.rotation_matrix(a, [0, 0, 1], [0, 1.55, 0]))
    it.b('Ticket_Slot', AM, -.2, .2, .5, .54, .547, .556)
    it.b('Red_Crest', G, -w/2 + .02, w/2 - .02, 2.196, 2.3, -.5, .12)
    for k in range(5): it.a('Crest_Leaves', LF2, zwall_leaf((-.4 + .2*k, 2.24, .12), (k - 2)*.25, .3, .12))
    it.b('Red_Button', BA, -.08, .08, .95, .99, .3, .4)
    return emit('tt_arc_redemption', it, 'redemption (ticket) game 1.0 x 1.1 m')
def claw():
    it = It(); w = .95
    it.bv('Claw_Base', SL, -w/2, w/2, 0, .95, -w/2, w/2, col=True)
    it.b('Claw_Prize_Floor', G, -w/2 + .056, w/2 - .056, .946, .98, -w/2 + .056, w/2 - .056)
    for k in range(16):
        x, z = -.27 + .18*(k % 4), -.27 + .18*(k // 4)
        it.a('Prizes_Balls' if k % 2 else 'Prizes_Leafy', BA if k % 2 else LF, node((x, 1.05 + .04*(k % 3), z), .07, 1) if k % 2 else clump((x, 1.06, z), .08, k))
    for x in (-w/2 + .03, w/2 - .03):
        for z in (-w/2 + .03, w/2 - .03): it.b('Claw_Posts', G, x - .02, x + .02, .946, 2.0, z - .02, z + .02)
    for s in (-1, 1):
        it.b('Claw_Pane_Scissor', SCR, -w/2 + .045, w/2 - .045, .99, 1.95, s*(w/2 - .03) - .006, s*(w/2 - .03) + .006)
        it.b('Claw_Pane_Scissor', SCR, s*(w/2 - .03) - .006, s*(w/2 - .03) + .006, .99, 1.95, -w/2 + .045, w/2 - .045)
    it.col(-w/2, w/2, .95, 2.0, -w/2, w/2)
    it.bv('Claw_Top', WH, -w/2, w/2, 1.996, 2.2, -w/2, w/2)
    paint_screen(it, -w/2 + .05, w/2 - .05, 2.05, 2.15, w/2 - .004, w/2 + .008, 'nature')
    it.a('Claw_Cable', ST, tube((.05, 1.5, 0), (.05, 1.996, 0), .006, 6)); it.b('Claw_Head', ALY, -.0, .1, 1.4, 1.5, -.05, .05)
    it.b('Claw_Controls', G, -w/2 + .05, w/2 - .05, .8, .9, w/2 - D, w/2 + .12)
    _buttons(it, .896, w/2 + .06, (.2, .3))
    return emit('tt_arc_claw', it, 'claw / prize machine 0.95 m square, scissor glazing')
def racer():
    it = It()
    it.bv('Racer_Base', G, -.55, .55, 0, .12, -.95, .95, col=True)
    it.b('Seat_Shell', WH, -.3, .3, .116, .55, .35, .98, col=True)
    it.b('Seat_Cushion', FA, -.26, .26, .546, .6, .4, .82)
    it.a('Seat_Back', WH, beam((0, .62, .95), (0, 1.15, 1.02), .1, .56))
    it.b('Dash', SL, -.5, .5, .116, .944, -.548, -.1, col=True)
    it.a('Wheel', ST, cap((0, 1.0, -.05), .16, .03, 16, 'z')); it.a('Wheel_Hub', BA, cap((0, 1.0, -.022), .04, .03, 8, 'z'))
    it.a('Wheel_Column', G, tube((0, .946, -.105), (0, 1.0, -.07), .03, 6))
    it.b('Screen_Housing', G, -.53, .53, .952, 1.75, -.95, -.552, col=True)
    paint_screen(it, -.48, .48, 1.05, 1.65, -.548, -.540, 'track')
    it.b('Pedals', ALY, -.15, .15, .118, .2, -.08, .1)
    for k in range(4):
        for sx in (-1, 1): it.b('Track_Stripes', AM if k % 2 else BA, min(sx*.32, sx*.5), max(sx*.32, sx*.5), .118, .124, .1 + .2*k, .2 + .2*k)
    it.b('Racer_Marquee', VIO, -.5, .5, 1.75 - D, 1.9, -.92, -.6)
    return emit('tt_arc_racer', it, 'sit-down racer 1.1 x 1.9 m, player faces -Z (front of seat is +Z)')
def airhockey():
    it = It(); L, W = 2.3, 1.3
    for x in (-.9, .9):
        it.b('AH_Legs', G, x - .12, x + .12, 0, .7, -.45, .45, col=True)
    it.b('AH_Body', SL, -L/2, L/2, .696, .82, -W/2, W/2, col=True)
    it.b('AH_Surface', WH, -L/2 + .08, L/2 - .08, .816, .826, -W/2 + .08, W/2 - .08)
    for z in (-W/2 + .03, W/2 - .03): it.b('AH_Rails', ST, -L/2 + .02, L/2 - .02, .816, .87, z - .02, z + .02)
    it.b('AH_CenterLine', CY, -.01, .01, .822, .83, -W/2 + .1, W/2 - .1)
    it.a('AH_Circle', CY, ring_band(.25, .826, .006, 16, .01))
    for x in (-L/2 + .3, L/2 - .3): it.a('Mallets', BA, cap((x, .85, 0), .05, .04, 12, 'y'))
    it.a('Puck', AM, cap((.3, .832, .1), .04, .01, 12, 'y'))
    for x in (-L/2, L/2): it.b('AH_Goals', G, x - .04 if x < 0 else x - .002, x + .002 if x < 0 else x + .04, .7, .86, -.25, .25)
    return emit('tt_arc_airhockey', it, 'air hockey 2.3 x 1.3 m (long axis X)')
def pinball():
    it = It()
    for x in (-.3, .3):
        for z in (-.6, .6): it.a('PB_Legs', ST, tube((x, 0, z), (x, .72, z), .025, 6))
    it.col(-.36, .36, 0, .9, -.7, .7)
    it.bv('PB_Body', SL, -.36, .36, .716, .86, -.62, .7)
    it.b('PB_Playfield', CY, -.32, .32, .856, .866, -.58, .66)
    it.b('PB_Backbox', G, -.36, .36, .856, 1.75, -.78, -.6, col=True)
    paint_screen(it, -.32, .32, 1.0, 1.7, -.602, -.594, 'nature')
    for k in range(3): it.a('PB_Bumpers', BA, cap((-.15 + .15*k, .882, -.2), .045, .05, 10, 'y'))
    return emit('tt_arc_pinball', it, 'pinball 0.72 x 1.45 m, player at +Z')
def vr_pod():
    it = It(); R = 1.1
    it.a('Pod_Floor', RU, cap((0, .04, 0), R, .08, 24, 'y')); it.col(-R, R, 0, .08, -R, R)
    it.a('Pod_Ring_LED', CY, ring_band(R, .05, .03, 24, .02))
    for k in range(6):
        a = k*math.pi/3 + math.pi/6; p0 = (R*.92*math.cos(a), .076, R*.92*math.sin(a)); p1 = (R*.5*math.cos(a), 2.6, R*.5*math.sin(a))
        it.a('Pod_Arcs', ST, tube(p0, p1, .03, 6))
        st, lv = vine([(p0[0]*1.01, .2, p0[2]*1.01), (p1[0]*1.01 + .04*math.cos(a), 2.3, p1[2]*1.01 + .04*math.sin(a))], seed=k, leaf_every=.5)
    it.a('Pod_Crown', G, cap((0, 2.62, 0), .62, .08, 18, 'y'))
    it.a('Pod_Crown_LED', AM, ring_band(.62, 2.62, .03, 18, .012))
    it.a('Pod_Tether', ST, tube((0, 2.58, 0), (0, 1.9, 0), .012, 6)); it.a('Pod_Headset', SL, box(-.1, .1, 1.8, 1.9, -.06, .06))
    it.a('Pod_Ball', BA, node((0, 2.78, 0), .1, 1))
    it.b('Pod_Ped', G, R*.92 - .2, R*.92 + .05, .076, 1.1, -.12, .12)
    paint_screen(it, R*.92 + .048, R*.92 + .056, .8, 1.05, -.1, .1, 'score')
    return emit('tt_arc_vr_pod', it, 'VR pod 2.2 m dia, open cage')
def prize_counter():
    it = It(); L = 6.0
    it.bv('PC_Body', WH, -L/2, L/2, 0, 1.0, .5, 1.1, col=True)
    it.bv('PC_Top', ST, -L/2 - .02, L/2 + .02, .996, 1.05, .46, 1.16)
    it.bv('PC_Acc_Body', WH, -L/2 + .1, -L/2 + 1.1, 0, .81, 1.104, 1.4, col=True)
    it.bv('PC_Acc_Top', ST, -L/2 + .08, -L/2 + 1.12, .806, .86, 1.104, 1.44)
    for x in np.arange(-L/2 + 1.3, L/2 - .2, .6): it.b('PC_Flutes', G, x, x + .06, .15, .9, 1.096, 1.11)
    it.b('PC_CourtLine', BA, -L/2 + 1.2, L/2 - .1, .5, .53, 1.108, 1.116)
    it.b('PC_Shelves_Back', G, -L/2, L/2, 0, 2.8, -.4, -.3, col=True)
    for y in (.6, 1.2, 1.8, 2.4): it.b('PC_Shelves', ST, -L/2 + .05, L/2 - .05, y, y + .03, -.298, .0)
    for k in range(18):
        x = -L/2 + .4 + .3*k
        for j, y in enumerate((.63, 1.23, 1.83)): it.a('PC_Plush', (LF, BA, LF2)[(k + j) % 3], clump((x, y + .1 - .004, -.15), .1, k*3 + j))
    paint_screen(it, -2.0, 2.0, 2.9, 3.3, -.35, -.33, 'court')
    it.b('PC_Sign_Back', G, -2.05, 2.05, 2.85, 3.35, -.4, -.354)
    for k in range(9): it.a('PC_Sign_Leaves', LF2, zwall_leaf((-2 + .5*k, 3.36, -.37), (k - 4)*.2, .35, .14))
    it.a('PC_Ball', BA, node((2.3, 3.1, -.37), .16, 1))
    return emit('tt_arc_prize_counter', it, 'L1 prize counter, 6 m, accessible 1.0 m at 0.86 m; shelves back to the ST+E N face')
def col_moss():
    it = It()
    for k in range(6): a = k*math.pi/3 + .2; it.a('Col_Moss', LF if k % 2 else LF2, moss_mound((.75*math.cos(a), 0, .75*math.sin(a)), .22, k + 40))
    for k in range(4): a = k*math.pi/2 + .7; it.a('Col_Stones', SL, clump((1.15*math.cos(a), .05, 1.15*math.sin(a)), .11, k + 50))
    return emit('tt_arc_col_moss', it, 'moss + stones ring at an X126.5 column base')
def seated_mound(c, r, seed=0):
    """moss_mound with bottom exactly at c[1]."""
    raw = moss_mound((0, 0, 0), r, seed)
    lift = -float(raw.bounds[0][1]) + c[1]
    return moss_mound((c[0], lift, c[2]), r, seed)

def feature_stair():
    """X126.6..139, Z38..40.5: two solid flights, mid landing +3.05, top +6.1. Guards both sides. y>=0."""
    it = It()
    z0, z1 = 38.0, 40.5
    n = 18
    rise = 6.1 / 36
    tr = .28
    xa = 126.6
    xl0 = xa + n * tr
    xl1 = xl0 + 1.4
    xb = xl1 + n * tr
    zw0, zw1 = z0 + .08, z1 - .08
    for xs, ys in ((xa, 0.0), (xl1, 3.05)):
        for i in range(n):
            x0s, x1s = xs + i * tr, xs + (i + 1) * tr
            y0s, y1s = ys + i * rise, ys + (i + 1) * rise
            it.b('Treads', WH, x0s + (E if i else 0), x1s + (E if i < n - 1 else 0), y1s - .05, y1s, zw0, zw1, col=True)
            it.b('Treads', WH, x0s, x0s + .04 + E, y0s - (E if i else 0), y1s, zw0, zw1, col=True)
            if i < n - 1:
                it.b('Nosing_LED', CY, x1s + .002, x1s + .006, y1s - .022, y1s - .008, zw0 + .04, zw1 - .04)
    it.b('Treads', WH, xl0 - E, xl1 + E, 3.0, 3.05, zw0, zw1, col=True)
    it.b('Landing_Beam', G, xl0 - .02, xl1 + .02, 2.75, 3.0 + E, z0 + .12, z1 - .12)
    for x in (xl0 + .2, xl1 - .2):
        it.a('Landing_Columns', ST, tube((x, 0, (z0 + z1) / 2), (x, 2.754, (z0 + z1) / 2), .09, 10))
        it.a('Column_Moss', LF, seated_mound((x, 0, (z0 + z1) / 2 + .5), .25, int(x)))
    it.b('Treads', WH, xb - E, 139.0, 6.05, 6.1, zw0, zw1, col=True)
    for zi, zside in ((z0, -1), (z1, +1)):
        z_pane = zi - zside * .02
        z_edge = zi - zside * .04
        for xs, ys in ((xa, 0.0), (xl1, 3.05)):
            p0 = (xs + .04, ys + .14, z_pane)
            p1 = (xs + n * tr - .04, ys + 3.05 + .14, z_pane)
            it.a('Guard_Scissor', SCR, beam((p0[0], p0[1] + .38, p0[2]), (p1[0], p1[1] + .38, p1[2]), .76, .014))
            it.a('Handrail', ALY, tube((xs + .052, ys + 1.05, z_edge), (xs + n * tr - .052, ys + 3.05 + 1.05, z_edge), .025, 8))
            for k in range(3, n, 3):
                x = xs + k * tr
                y = ys + k * rise
                it.a('Guard_Posts', ST, tube((x, y + .10, z_edge), (x, y + .98, z_edge), .018, 8))
        it.b('Guard_Scissor', SCR, xl0 + .06, xl1 - .06, 3.19, 3.95, z_pane - .007, z_pane + .007)
        it.a('Handrail', ALY, tube((xl0 + .052, 3.05 + 1.05, z_edge), (xl1 - .052, 3.05 + 1.05, z_edge), .025, 8))
        it.b('Guard_Scissor', SCR, xb + .06, 138.90, 6.24, 7.03, z_pane - .007, z_pane + .007)
        it.a('Handrail', ALY, tube((xb + .052, 6.1 + 1.05, z_edge), (138.92, 6.1 + 1.05, z_edge), .025, 8))
        for x, y in ((xa, 0.0), (xl0, 3.05), (xl1, 3.05), (xb, 6.1)):
            it.a('Newel', ALY, tube((x, y, z_edge), (x, y + 1.10, z_edge), .03, 8))
    return emit('tt_arc_feature_stair', it, 'decorative open L1->L2 stair (not egress); top lands at +6.1 X~138..139: needs an F2 slab opening (not cut here)')

# ---------------- layout ----------------
F1EX = [(113, 117, 34.5, 38.5), (113, 118.5, 39, 44.5), (119.5, 125.5, 50, 60.6), (134, 140, 10, 20.6), (134, 140, 58.4, 69),
        (128, 140, 0, 10), (128, 140, 69, 79), (125.6, 139.4, 37.2, 41.3)]
DOORS = [(113, 116, 23, 28), (113, 116, 51, 56), (113, 116, 69, 74)]
TREES_E = [(119.5, 30.5), (119.5, 48.5)]
COLS = [(126.5, 9.5 + 8*k) for k in range(8)]
def free(x0, x1, z0, z1, ex):
    if any(x0 < b and x1 > a and z0 < d and z1 > c for a, b, c, d in ex): return False
    if any(x0 - 1.1 < tx < x1 + 1.1 and z0 - 1.1 < tz < z1 + 1.1 for tx, tz in TREES_E): return False
    if any(x0 - .45 < cx < x1 + .45 and z0 - .45 < cz < z1 + .45 for cx, cz in COLS): return False
    return True
def layout(floor):
    y = 0 if floor == 1 else 6.1; ex = F1EX + DOORS + ([(113, 116, 4, 9), (133, 140, 32.5, 42.5)] if floor == 1 else [])
    if floor == 1: ex = ex + [(118.9, 126.1, 60.6, 63.2)]   # prize counter zone
    big = []
    for i in range(3):          # air hockey: 2 x 3 at X128.6..133.4, Z22..36
        for j in range(2): big.append(('tt_arc_airhockey', 129.85 + j*3.28, 23.6 + i*4.6, 0))
    for j, z in enumerate((44.0, 47.4, 50.8, 54.2)): big.append(('tt_arc_vr_pod', 130.82 if j % 2 else 132.4, z, 0))
    for k in range(4): big.append(('tt_arc_pinball', 128.1, 44.0 + .8*k + 8.0, -90 + 180))  # pinball row facing +X at Z52..54.4
    for k in range(10): big.append(('tt_arc_racer', 122.5, 1.2 + 1.25*k, -90))     # racers, player faces -X? screen at -Z local
    for a, x, z, yaw in big: ex.append((x - 1.3, x + 1.3, z - 1.2, z + 1.2) if a != 'tt_arc_racer' else (x - 1.0, x + 1.0, z - .6, z + .6))
    rows = [(113.90, 90), (116.625, -90), (117.475, 90), (120.325, -90), (121.175, 90), (124.025, -90), (127.6, 90),
            (130.455, -90), (131.305, 90), (134.155, -90), (135.0, 90), (138.93, -90)]
    slots = []
    for x, yaw in rows:
        z = .8
        while z < 78.4:
            if free(x - .5, x + .5, z - .55, z + .55, ex): slots.append((x, z, yaw)); z += 1.1
            else: z += .25
    # contiguous runs per row -> 5-cabinet blocks, 14 blocks spread evenly over the floor
    runs = []; prev = None
    for x, z, yaw in slots:
        if prev and prev[0] == x and abs(z - prev[1] - 1.1) < 1e-6: runs[-1].append((x, z, yaw))
        else: runs.append([(x, z, yaw)])
        prev = (x, z)
    blocks = [r[i:i + 5] for r in runs for i in range(0, len(r) - 4, 6)]
    pick = [blocks[int(round(k*(len(blocks) - 1)/13))] for k in range(14)]
    pick.sort(key=lambda bl: math.hypot(bl[0][0] - 122.5, bl[2][1] - 62.0))
    out = []
    for k, bl in enumerate(pick):
        a = 'tt_arc_redemption' if k < 4 else 'tt_arc_claw' if k < 6 else 'tt_arc_video'
        out += [(a, x, z, yaw) for x, z, yaw in bl]
    out += big
    if floor == 1:
        # ST-ARS F1 N door approach X 134.48..136.62, Z 20.61..22.1: keep 0.05 m clear
        _shift = {21.3: 26.8, 22.4: 27.9}
        out = [(a, x, _shift[z] if a == 'tt_arc_video' and abs(x - 135.0) < 0.02 and z in _shift else z, yaw) for a, x, z, yaw in out]
        # S facade inner ledge Z>=0.621: cab extends 0.36 m along yaw-X; nudge the Z0.8 video to Z1.00 (still 0.18 m clear of Z1.9)
        out = [(a, x, 1.00 if a == 'tt_arc_video' and abs(z - .8) < .02 else z, yaw) for a, x, z, yaw in out]
    if floor == 1: out.append(('tt_arc_prize_counter', 122.5, 61.15, 0))
    for cx, cz in COLS:
        if free(cx - 1.3, cx + 1.3, cz - 1.3, cz + 1.3, F1EX): out.append(('tt_arc_col_moss', cx, cz, 0))
    return [(a, x, y, z, yaw) for a, x, z, yaw in out], len(slots)
def build(PL):
    A = dict(tt_arc_video=video(), tt_arc_redemption=redemption(), tt_arc_claw=claw(), tt_arc_racer=racer(), tt_arc_airhockey=airhockey(),
             tt_arc_pinball=pinball(), tt_arc_vr_pod=vr_pod(), tt_arc_prize_counter=prize_counter(), tt_arc_col_moss=col_moss())
    fs = feature_stair(); stats = {}
    for fl in (1, 2):
        items, nslots = layout(fl)
        for a, x, y, z, yaw in items: place(PL, A[a], x, y, z, yaw, 'f1' if fl == 1 else 'f2')
        from collections import Counter; stats[f'L{fl}'] = dict(Counter(i[0] for i in items), slots=nslots)
    place(PL, fs, 0, 0, 0, local=True)
    return stats
if __name__ == '__main__':
    PL = []; print(json.dumps(build(PL)))
    for r in REP:
        if not r['passed']: print(r['asset'], r['bad'], r['coplanar'], r['open'], r['pivot'])
