"""Corner roof plant-stack cutout with flashing collar. Real aperture. temp-Services owns plant shells to +28.
TTQA-042 (Rook 2026-11-15): the 12.4 x 10.4 m collar ring (and 4 inverted deck boxes: OX/OZ < collar) ran over the facade
curtain-wall heads, corner closures and roof-closure frames (collar top on the Head_Track top y 25.50, gutters 11-21 mm into
the glass / fins). The cutout is now an L on the two inboard sides only, trimmed 2 mm off every neighbour:
  facade sides  : stop at the Head_Track inner faces (local x = s*5.350, z = -4.350) + 2 mm -> no ring there (the stack meets the facade)
  inboard X side: aperture edge 5.70 (stack Roof_Line_LED at 5.672) .. 5.823 (roof bay / closure frames from 5.825)
  inboard Z side: aperture edge 4.90 (LED 4.872) .. 5.20 (0.3 m collar, as before)
s = -1: facade on local -X (SW yaw 0, NE yaw 180) -> tt_roof_plant_cutout; s = +1: facade on local +X (SE yaw 0, NW yaw 180)
-> tt_roof_plant_cutout_m. Deck 0.08 + collar 0.12 + 15 mm alloy flash, gutter under the deck, 2 mm under its bottom."""
from rt_lib import *

TH, CH = 0.08, 0.12
FX, FZ = 5.348, -4.348          # facade Head_Track inner faces (5.350 / -4.350) less 2 mm
AX, AZ = 5.70, 4.90             # inboard aperture edges (stack + 28 mm)
IX, IZ = 5.823, 5.20            # inboard outer edges (roof frames at 5.825; collar 0.3 m on Z)

def _cutout(s):
    it = It()
    xa, xb = sorted((s * FX, -s * IX))                    # N strip X span: facade head .. inboard frame
    xi0, xi1 = sorted((-s * AX, -s * IX))                 # inboard X strip
    gx0, gx1 = sorted((-s * (IX - .12), -s * IX))
    for (x0, x1, z0, z1) in ((xa, xb, AZ, IZ), (xi0, xi1, FZ, IZ)):   # same part names may overlap at the corner
        it.b('Deck', SSL, x0, x1, 0, TH, z0, z1, col=True)
        c0, c1, d0, d1 = x0 + .002, x1 - .002, z0 + .002, z1 - .002          # collar 2 mm inside the deck edges (no shared side faces)
        it.b('Collar', ST, c0, c1, TH - E, TH + CH, d0, d1, col=True)
        it.b('Collar', ALY, c0, c1, TH + CH - E, TH + CH + .015, d0, d1)
    it.b('Gutter', G, xa, xb, -.04, -D, IZ - .12, IZ)
    it.b('Gutter', G, gx0, gx1, -.04, -D, FZ, IZ - .12)
    return it

def build(PL):
    A = emit('tt_roof_plant_cutout', _cutout(-1), 'TTQA-042 corner cutout flashing L (facade on local -X): SW yaw 0 / NE yaw 180')
    Am = emit('tt_roof_plant_cutout_m', _cutout(1), 'TTQA-042 corner cutout flashing L (facade on local +X): SE yaw 0 / NW yaw 180')
    RY = 25.285
    places = [(A, -6.0, 5.0, 0), (Am, 134.0, 5.0, 0), (Am, -6.0, 74.0, 180), (A, 134.0, 74.0, 180)]
    for a_, x, z, yaw in places:
        place(PL, a_, x, RY, z, yaw)
    return dict(cutouts=4, aperture='facade sides open to the head track; inboard edges x %.2f / z %.2f' % (AX, AZ), collar='L, inboard sides', roof_y=RY,
                transforms=[{'asset': a_[0][0], 'p': [x, RY, z], 'yaw': yaw} for a_, x, z, yaw in places])
