"""Corner roof plant-stack cutout with 0.3 m flashing collar. Real aperture. temp-Services owns plant shells to +28."""
from rt_lib import *

OX, OZ = 6.0, 5.0
HX, HZ = 5.9, 4.9
COLLAR = 0.30
TH = 0.08
CH = 0.12

def _cutout():
    it = It()
    ax0, ax1, az0, az1 = -HX, HX, -HZ, HZ
    co0, co1, cz0, cz1 = -(HX + COLLAR), HX + COLLAR, -(HZ + COLLAR), HZ + COLLAR
    # same part name Deck so corner abutments allowed
    it.b('Deck', SSL, -OX, OX, 0, TH, -OZ, cz0 - D, col=True)
    it.b('Deck', SSL, -OX, OX, 0, TH, cz1 + D, OZ, col=True)
    it.b('Deck', SSL, -OX, co0 - D, 0, TH, cz0, cz1, col=True)
    it.b('Deck', SSL, co1 + D, OX, 0, TH, cz0, cz1, col=True)
    # collar ring as one part name; sits on deck with E embed
    it.b('Collar', ST, co0, co1, TH - E, TH + CH, az0 - COLLAR, az0, col=True)
    it.b('Collar', ST, co0, co1, TH - E, TH + CH, az1, az1 + COLLAR, col=True)
    it.b('Collar', ST, ax0 - COLLAR, ax0, TH - E, TH + CH, az0, az1, col=True)
    it.b('Collar', ST, ax1, ax1 + COLLAR, TH - E, TH + CH, az0, az1, col=True)
    # flash same stack family name Collar (cap)
    it.b('Collar', ALY, co0, co1, TH + CH - E, TH + CH + .015, az0 - COLLAR, az0)
    it.b('Collar', ALY, co0, co1, TH + CH - E, TH + CH + .015, az1, az1 + COLLAR)
    it.b('Collar', ALY, ax0 - COLLAR, ax0, TH + CH - E, TH + CH + .015, az0, az1)
    it.b('Collar', ALY, ax1, ax1 + COLLAR, TH + CH - E, TH + CH + .015, az0, az1)
    # gutters below deck, 2 mm below deck bottom so not coplanar; same name
    it.b('Gutter', G, -OX, OX, -.04, -D, -OZ, -OZ + .12)
    it.b('Gutter', G, -OX, OX, -.04, -D, OZ - .12, OZ)
    it.b('Gutter', G, -OX, -OX + .12, -.04, -D, -OZ + .12, OZ - .12)
    it.b('Gutter', G, OX - .12, OX, -.04, -D, -OZ + .12, OZ - .12)
    return it

def build(PL):
    A = emit('tt_roof_plant_cutout', _cutout(), '12x10 corner cutout +0.3m flashing collar; open aperture')
    RY = 25.285
    places = [(-6.0, 5.0, 0), (134.0, 5.0, 0), (-6.0, 74.0, 180), (134.0, 74.0, 180)]
    for x, z, yaw in places:
        place(PL, A, x, RY, z, yaw)
    return dict(cutouts=4, aperture=[2 * HX, 2 * HZ], collar=COLLAR, roof_y=RY,
                transforms=[{'p': [x, RY, z], 'yaw': yaw} for x, z, yaw in places])
