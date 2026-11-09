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
    it = It()
    it.b('Plate', KP, -.04, .04, 0, 2.8, -.02, .02, col=True)
    pts = [(0.05, .1, 0), (0.08, .9, .02), (0.05, 1.7, -.02), (0.1, 2.5, .01)]
    st, lv = vine(pts, r=.012, leaf_every=.35, leaf_len=.14, seed=7, outward=True)
    it.a('Vine_Stem', LF, st); it.a('Vine_Leaves', LF2, lv)
    return it

def _seat():
    it = It()
    # pair of seats along X, facing +Z
    for sx in (-.55, .55):
        it.b('SeatBase', SSL, sx - .35, sx + .35, 0, .08, -.35, .35, col=True)
        it.b('Seat', FA, sx - .33, sx + .33, .08 - E, .42, -.32, .32)
        it.b('Back', FA, sx - .33, sx + .33, .42 - E, .77, .28, .35)
    it.b('TableTop', ALY, -.18, .18, .48, .5, -.1, .1, col=True)
    it.a('TableLeg', ALY, tube((0, 0, 0), (0, .48 + E, 0), .025, 6))
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
