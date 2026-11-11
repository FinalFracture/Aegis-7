"""F3-PLAY kids playground X 128.3..140, Z 20.6..58.4. Rev 3.0: soft4, kick-picket fence, perches, placements."""
from rt_lib import *

def _soft4():
    """4x4 soft-play, not sunken, 0.35 m raised rim, ball pit, foam bits. Local half-extent 2.0."""
    it = It(); H = 2.0; rim = .35
    it.b('Pad', RU, -H, H, 0, .03, -H, H, col=True)
    gap = 1.0
    for (x0, x1, z0, z1) in [(-H, H, -H, -H + .22), (-H, -H + .22, -H + .22, H - .22), (H - .22, H, -H + .22, H - .22),
                             (-H, -gap / 2, H - .22, H), (gap / 2, H, H - .22, H)]:
        it.b('Rim', RU, x0, x1, .03 - E, rim, z0, z1, col=True)
    it.b('Pit_Bed', SSL, -.7, .7, .032, .10, -.9, .5)
    balls = []
    for i in range(-3, 4):
        for j in range(-3, 4):
            px, pz = i * .16, -.2 + j * .16
            if px * px + (pz + .2) * (pz + .2) < .48 ** 2:
                balls.append(node((px, .10 + .055 + .002, pz), .055, -1))
    if balls:
        it.a('Balls', BA, merge(balls))
    it.a('Hill', RU, moss_mound((1.1, .03, 1.0), .45, 4))
    it.a('Hill', RU, moss_mound((-1.2, .03, .6), .35, 5))
    it.b('Wedge', WH, -1.4, -.4, .03 - E, .28, 1.2, 1.7)
    return it

def _fence_panel():
    """2.0 m panel: kick plate 0.35 m + pickets to 1.2 m. Local X -1..1, +Z outside."""
    it = It(); H = 1.2; pw = .04
    it.b('Post', ALY, -1.0, -1.0 + 2 * pw, 0, H + .02, -pw, pw, col=True)
    it.b('Kick', KP, -1.0 + 2 * pw + D, 1.0, 0, .35, -.025, .025, col=True)
    it.b('RailTop', ALY, -1.0 + 2 * pw + D, 1.0, H - .06, H - .02, -.018, .018)
    it.b('RailLow', ALY, -1.0 + 2 * pw + D, 1.0, .35 - E, .41, -.018, .018)
    n = 12; xs = [(-1.0 + 2 * pw + .05) + i * ((2.0 - 2 * pw - .1) / (n - 1)) for i in range(n)]
    for x in xs:
        it.b('Picket', WH, x - .015, x + .015, .41 - E, H - .06 + E, -.012, .012)
    it.a('Cap', ALY, cap((-1.0 + pw, H + .02 + .015 - E, 0), .038, .03, 8, 'y'))
    return it

def _fence_gate():
    it = It(); H = 1.2; pw = .04
    for x in (-.8, .8 - 2 * pw):
        it.b('Post', ALY, x, x + 2 * pw, 0, H + .02, -pw, pw, col=True)
        it.a('Cap', ALY, cap((x + pw, H + .02 + .015 - E, 0), .038, .03, 8, 'y'))
    x0, x1 = -.8 + 2 * pw + D, .8 - 2 * pw - D
    it.b('GateKick', KP, x0, x1, 0, .35, -.025, .025, col=True)
    it.b('GateRail', ALY, x0, x1, H - .06, H - .02, -.018, .018)
    n = 8; xs = [x0 + .04 + i * ((x1 - x0 - .08) / max(n - 1, 1)) for i in range(n)]
    for x in xs:
        it.b('GatePicket', WH, x - .015, x + .015, .35 - E, H - .06 + E, -.012, .012)
    # latch fully outside +X post (post ends at .8)
    it.b('Latch', G, .8 + D, .8 + .045, H - .12, H - .02, -.035, .035)
    return it

def build(PL):
    A_s = emit('tt_play_soft4', _soft4(), '4x4 soft-play 0.35 rim Rev3')
    A_f = emit('tt_play_fence_kick', _fence_panel(), '2m pickets over kick plate')
    A_g = emit('tt_play_fence_gate', _fence_gate(), '1.6m gate pickets+kick')
    A_p = emit('tt_play_perch', perch_it(), '1.8x0.3 fence perch')
    Y = F3_Y
    PL.append(dict(glb=str(GM / 'tt_play_surface.glb'), asset='tt_play_surface', p=[134.15, Y, 39.5], yaw=0, tag='f3'))
    PL.append(dict(glb=str(GM / 'tt_play_tower.glb'), asset='tt_play_tower', p=[136.14, Y, 28.0], yaw=0, tag='f3'))
    PL.append(dict(glb=str(GM / 'tt_swing_set.glb'), asset='tt_swing_set', p=[136.0, Y, 35.0], yaw=0, tag='f3'))
    PL.append(dict(glb=str(GM / 'tt_dome_climber.glb'), asset='tt_dome_climber', p=[136.32, Y, 42.0], yaw=0, tag='f3'))
    PL.append(dict(glb=str(GM / 'tt_see_saw.glb'), asset='tt_see_saw', p=[136.0, Y, 48.0], yaw=90, tag='f3'))
    PL.append(dict(glb=str(GM / 'tt_toddler_zone.glb'), asset='tt_toddler_zone', p=[134.5, Y, 54.0], yaw=0, tag='f3'))
    PL.append(dict(glb=str(GM / 'tt_balance_trail.glb'), asset='tt_balance_trail', p=[132.5, Y, 38.0], yaw=90, tag='f3'))
    place(PL, A_s, 136.5, Y, 24.5, 0, local=False)
    place(PL, A_g, 128.3, Y, 51.0, -90)
    for z in [21.6 + 2.0 * i for i in range(18)]:
        if 49.5 < z < 52.5: continue
        place(PL, A_f, 128.3, Y, z, -90)
    place(PL, A_g, 134.15, Y, 20.6, 180)
    place(PL, A_g, 134.15, Y, 58.4, 0)
    for z in [21.6 + 2.0 * i for i in range(18)]:
        place(PL, A_f, 139.45, Y, z, 90)
    for x in [129.3 + 2.0 * i for i in range(5)]:
        place(PL, A_f, x, Y, 20.6, 180)
        place(PL, A_f, x, Y, 58.4, 0)
    for z in (25.0, 33.0, 41.0, 46.0):
        place(PL, A_p, 128.478, Y, z, 90, local=False)
    return dict(soft4=1, fences='kick+picket', perches=4, seesaw_yaw=90)
