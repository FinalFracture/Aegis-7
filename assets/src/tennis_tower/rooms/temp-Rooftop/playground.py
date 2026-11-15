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
    # TTQA-042: the moss mounds reached 0.1355 m below the pad, so the bottom-centre pivot sat on the mound and the whole
    # soft-play floated 0.1355 m over the roof slab; cut them 4 mm into the pad top (pad bottom = pivot y 0 again)
    for c_, r_, sd in (((1.1, .03, 1.0), .45, 4), ((-1.2, .03, .6), .35, 5)):
        h = moss_mound(c_, r_, sd).slice_plane([0, .03 - E, 0], [0, 1, 0], cap=True); h.metadata["uv"] = h.vertices[:, [0, 2]] / 2.0
        it.a('Hill', RU, h)
    it.b('Wedge', WH, -1.4, -.4, .03 - E, .28, 1.2, 1.7)
    return it

def _fence_panel(L=2.0):
    """L m panel (default 2.0): kick plate 0.35 m + pickets to 1.2 m. Local X -L/2..L/2 (post at -X end), +Z outside."""
    it = It(); H = 1.2; pw = .04; h = L / 2
    it.b('Post', ALY, -h, -h + 2 * pw, 0, H + .02, -pw, pw, col=True)
    it.b('Kick', KP, -h + 2 * pw + D, h, 0, .35, -.025, .025, col=True)
    it.b('RailTop', ALY, -h + 2 * pw + D, h, H - .06, H - .02, -.018, .018)
    it.b('RailLow', ALY, -h + 2 * pw + D, h, .35 - E, .41, -.018, .018)
    n = max(2, int(round(12 * L / 2.0))); xs = [(-h + 2 * pw + .05) + i * ((L - 2 * pw - .1) / (n - 1)) for i in range(n)]
    for x in xs:
        it.b('Picket', WH, x - .015, x + .015, .41 - E, H - .06 + E, -.012, .012)
    it.a('Cap', ALY, cap((-h + pw, H + .02 + .015 - E, 0), .038, .03, 8, 'y'))
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
    # TTQA-044: S/N runs are laid out between the W/E fence faces (X 128.34..139.41) around the 1.6 m gate (X 133.35..134.95),
    # so no panel overlaps the gate or the corner fences; 1.01 m and 0.46 m fillers close the runs
    # the gate latch sticks 45 mm past its post, so the run on the latch side stops 50 mm short of the gate (S: W side, N: E side)
    A_fl = {L: emit(f'tt_play_fence_kick_{int(round(L * 100)):03d}', _fence_panel(L), f'{L:.2f}m filler pickets over kick plate') for L in (1.01, .96, .46, .41)}
    Y = F3_Y
    # TTQA-042 rooftop safety pads: every 30 mm pad sat on the roof slab top (y 12.200) and the overlapping pads shared one top plane
    # (z-fight). Each pad asset is lifted off the slab and the overlapping ones are staggered >= 1.2 mm apart (floor gap <= 4.4 mm,
    # inside the +-5 mm contact rule): see-saw +1.2, surface/soft-play +2.0, swing/dome +3.2, balance trail/toddler +4.4 mm
    # (toddler vs see-saw 3.2 mm apart: the see-saw Court_Line top sits 2 mm over its own pad top).
    PAD = dict(tt_play_surface=.0020, tt_see_saw=.0012, tt_play_soft4=.0020, tt_swing_set=.0032, tt_dome_climber=.0032, tt_toddler_zone=.0044, tt_balance_trail=.0044)
    PY = {k: round(Y + v, 4) for k, v in PAD.items()}
    PL.append(dict(glb=str(GM / 'tt_play_surface.glb'), asset='tt_play_surface', p=[134.15, PY['tt_play_surface'], 39.5], yaw=0, tag='f3'))
    PL.append(dict(glb=str(GM / 'tt_play_tower.glb'), asset='tt_play_tower', p=[136.14, Y, 28.0], yaw=0, tag='f3'))
    PL.append(dict(glb=str(GM / 'tt_swing_set.glb'), asset='tt_swing_set', p=[136.0, PY['tt_swing_set'], 35.0], yaw=0, tag='f3'))  # TTQA-042: pad trimmed to X 139.39 by dome_pad_trim.py
    PL.append(dict(glb=str(GM / 'tt_dome_climber.glb'), asset='tt_dome_climber', p=[136.5, PY['tt_dome_climber'], 42.0], yaw=0, tag='f3'))  # r7e: back to 136.50 (clears balance-trail stones); pad trimmed by dome_pad_trim.py
    PL.append(dict(glb=str(GM / 'tt_see_saw.glb'), asset='tt_see_saw', p=[136.0, PY['tt_see_saw'], 48.0], yaw=90, tag='f3'))
    PL.append(dict(glb=str(GM / 'tt_toddler_zone.glb'), asset='tt_toddler_zone', p=[134.5, PY['tt_toddler_zone'], 54.0], yaw=0, tag='f3'))
    PL.append(dict(glb=str(GM / 'tt_balance_trail.glb'), asset='tt_balance_trail', p=[132.5, PY['tt_balance_trail'], 38.0], yaw=90, tag='f3'))
    place(PL, A_s, 136.5, PY['tt_play_soft4'], 24.5, 0, local=False)
    place(PL, A_g, 128.3, Y, 51.0, -90)
    for z in [21.6 + 2.0 * i for i in range(18)]:
        if 49.5 < z < 52.5: continue
        place(PL, A_f, 128.3, Y, z, -90)
    place(PL, A_g, 134.15, Y, 20.6, 180)
    place(PL, A_g, 134.15, Y, 58.4, 0)
    for z in [21.6 + 2.0 * i for i in range(18)]:
        place(PL, A_f, 139.45, Y, z, 90)
    for zr, yw, run in ((20.6, 180, ((A_f, 128.34, 130.34), (A_f, 130.34, 132.34), (A_fl[.96], 132.34, 133.30), (A_f, 134.95, 136.95), (A_f, 136.95, 138.95), (A_fl[.46], 138.95, 139.41))),
                        (58.4, 0, ((A_f, 128.34, 130.34), (A_f, 130.34, 132.34), (A_fl[1.01], 132.34, 133.35), (A_f, 135.0, 137.0), (A_f, 137.0, 139.0), (A_fl[.41], 139.0, 139.41)))):
        for a_, x0, x1 in run:
            place(PL, a_, (x0 + x1) / 2, Y, zr, yw)
    # TTQA-044: perches centred between the W-run posts (posts at Z 20.6 + 2k) and 6 mm off the kick plate face
    for z in (25.6, 33.6, 41.6, 45.6):
        place(PL, A_p, 128.484, Y, z, 90, local=False)
    return dict(soft4=1, fences='kick+picket', perches=4, seesaw_yaw=90)
