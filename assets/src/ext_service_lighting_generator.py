"""Rook (Oct 30, box pipeline): list v1 #35 junction cabinet, #36 service hand cart, #21 amber street light pole, #22 low bollard light.
Same rules/pattern as ext_street_furniture_generator.py (Aegis-7 palette, BLEND glass, Y-up bottom-centre pivot, +Z front,
0.004 m joint embeds, ext_clip_check before export). Run: python3 ext_service_lighting_generator.py [cabinet|cart|light|blight|all]"""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import G, S, T, A, GL, E, ring, box, blk, Pod, loft
from cycler_route_generator import cyl_z

# ---------------- #35 utility junction cabinet 0.8 W x 0.4 D x 1.4 H, <=400 ----------------
def cabinet(v):
    p = Pod(f"ext_junction_cabinet_0{v}"); F = .19  # body front face z
    zb = -.15 if v == 5 else -.19  # v5: shallower body leaves room for the rear conduit inside the 0.4 m depth
    p.add("Plinth", G, box(-.38, .38, 0, .08, zb + .01, .18))
    if v == 4:  # body split by an amber hazard band
        p.add("Body", S, blk(-.39, .39, .08 - E, .9, -.19, .19, .02, 1), blk(-.39, .39, .96 - E, 1.34, -.19, .19, .02, 1))
        p.add("Hazard_Band", A, blk(-.395, .395, .9 - E, .96, -.195, .195, .02, 1))
    else: p.add("Body", S if v != 5 else G, blk(-.39, .39, .08 - E, 1.34, zb, .19, .02, 1))
    if v == 2: p.add("Roof", T, loft(np.array([(.4, .2), (-.4, .2), (-.4, -.2), (.4, -.2)]), [(1.34 - E, 1, 1), (1.37, 1, 1), (1.4, .96, .7)]))
    else: p.add("Roof", T, blk(-.4, .4, 1.34 - E, 1.4, zb - .01, .2, .02, 1))
    if v == 1:  # Twin Door: two gunmetal doors, titanium pulls, amber status pip
        p.add("Doors", G, box(-.36, -.006, .14, 1.28, F - E, .197), box(.006, .36, .14, 1.28, F - E, .197))
        p.add("Pulls_Hardware", T, box(-.05, -.03, .6, .8, .195, .205), box(.03, .05, .6, .8, .195, .205))
        p.add("Status_Pip", A, box(.28, .32, 1.2, 1.23, .195, .203))
    elif v == 2:  # Louvred: single door, side louvre fins, sloped roof
        p.add("Door", G, box(-.34, .34, .14, 1.28, F - E, .197))
        p.add("Louvres", T, *[box(sx * .39 - .006, sx * .39 + .006, y, y + .02, -.12, .12) if False else box(s0, s1, y, y + .02, -.12, .12)
                               for sx in (-1, 1) for (s0, s1) in [((-.398, -.386) if sx < 0 else (.386, .398))] for y in np.linspace(.9, 1.2, 4)])
        p.add("Status_Pip", A, box(-.02, .02, 1.22, 1.25, .195, .203))
    elif v == 3:  # Meter Window: door with a BLEND glass meter viewport framed in amber
        p.add("Door", G, box(-.34, .34, .14, 1.28, F - E, .197))
        p.add("Meter_Window", GL, box(-.15, .15, .9, 1.15, .195, .205))
        p.add("Window_Frame", A, box(-.17, .17, .88, .9 + E, .193, .207), box(-.17, .17, 1.15 - E, 1.17, .193, .207))
        p.add("Pulls_Hardware", T, box(.24, .28, .5, .7, .195, .205))
    elif v == 4:  # Hazard Band: twin doors above and below the band, titanium hinges
        p.add("Doors", G, box(-.34, .34, .14, .86, F - E, .197), box(-.34, .34, 1.0, 1.28, F - E, .197))
        p.add("Pulls_Hardware", T, box(.24, .28, .45, .6, .195, .205), box(.24, .28, 1.1, 1.18, .195, .205))
    elif v == 5:  # Conduit Tower: gunmetal body, rear cable conduit to grade, slate door, amber pip strip
        p.add("Door", S, box(-.34, .34, .14, 1.28, F - E, .197))
        p.add("Pip_Strip", A, box(-.2, .2, 1.22, 1.24, .195, .203))
        p.add("Conduit", T, ring(.025, .012, 1.0, 8, z=zb - .021))  # rear conduit, 0.004 into the body back
        p.add("Conduit_Clamp", G, box(-.04, .04, 0, .016, zb - .05, zb - .002))
    return p
CAB = [(1, "Twin_Door"), (2, "Louvred"), (3, "Meter_Window"), (4, "Hazard_Band"), (5, "Conduit_Tower")]

# ---------------- #36 service hand cart 1.4 L x 0.7 W x 1.0 H, <=900 ----------------
def wheels(p, xs=(-.45, .45), r=.09):
    for x in xs:
        for zs in (-1, 1):
            z0, z1 = (.29, .33) if zs > 0 else (-.33, -.29)
            p.add("Wheels", G, cyl_z(x, r, r, z0, z1, 12))
            p.add("Axle_Hardware", T, cyl_z(x, r, .012, min(z0, z1) - .02 if zs > 0 else z0 - .0, (z1 + .0) if zs < 0 else z1, 6) if False else cyl_z(x, r, .012, (.27 if zs > 0 else -.335), (.335 if zs > 0 else -.27), 6))
            p.add("Wheel_Brackets", G, box(x - .025, x + .025, r - .02, .18 + E, *((.255, .275) if zs > 0 else (-.275, -.255))))
def handle(p, x=-.66, top=1.0):
    p.add("Handle", T, *[box(x - .02, x + .02, .24 - E, top, z - .02, z + .02) for z in (-.28, .28)],
          box(x - .015, x + .015, top - .06, top - .02, -.26 - E, -.12 + E), box(x - .015, x + .015, top - .06, top - .02, .12 - E, .26 + E))  # crossbar split at the grip
    p.add("Grip", A, box(x - .018, x + .018, top - .065, top - .015, -.12, .12))
def cart(v):
    p = Pod(f"ext_service_hand_cart_0{v}"); wheels(p)
    p.add("Deck", G if v != 4 else S, box(-.64, .7, .18, .24, -.3, .3)); handle(p)
    if v == 1:  # Flatbed: amber deck edge rails
        p.add("Deck_Rails", A, box(-.6, .6, .24 - E, .27, .26, .28), box(-.6, .6, .24 - E, .27, -.28, -.26))
        p.add("Deck_Pad", S, box(-.58, .58, .24 - E, .25, -.24, .24))
    elif v == 2:  # Tub: slate tub with titanium rim
        p.add("Tub", S, blk(-.55, .55, .24 - E, .6, -.28, .28, .04, 2)); p.add("Tub_Rim", T, blk(-.565, .565, .6 - E, .63, -.295, .295, .045, 2))
    elif v == 3:  # Two-Tier: titanium corner posts, second shelf, amber shelf lip
        p.add("Posts", T, *[box(x - .02, x + .02, .24 - E, .62, z - .02, z + .02) for x in (-.5, .55) for z in (-.26, .26)])
        p.add("Upper_Shelf", G, box(-.6, .6, .62 - E, .66, -.3, .3)); p.add("Shelf_Lip", A, box(-.6, .6, .66 - E, .69, .27, .29))
    elif v == 4:  # Tool Crate: slate deck carrying a gunmetal tool crate with amber latches and titanium lid
        p.add("Crate", G, blk(-.45, .35, .24 - E, .6, -.24, .24, .02, 1)); p.add("Crate_Lid", T, blk(-.46, .36, .6 - E, .66, -.25, .25, .02, 1))
        p.add("Latches", A, *[box(x - .03, x + .03, .5, .58, .236, .25) for x in (-.25, .15)])
    elif v == 5:  # Tank Hauler: cradle with two titanium tanks, BLEND glass gauge, amber valve caps
        for z in (-.13, .13):
            p.add("Cradle", G, *[box(x - .03, x + .03, .24 - E, .3, z - .12, z + .12) for x in (-.4, .4)])
            p.add("Tanks", T, sf.xf(sf.loft(sf.circle(.11, 12), [(-.55, 1, 1), (.5, 1, 1)]), R=np.array([[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) if False else None, t=(0, 0, 0)) if False else _xtank(z))
            p.add("Valve_Caps", A, _xcap(z))
        p.add("Gauge_Glass", GL, box(-.62, -.58, .3, .4, -.03, .03))
    return p
def _xtank(z, x0=-.5, x1=.5, r=.11, y=.39):  # tank along X resting in the cradles (cradle top y=.3 -> tank bottom .3-E)
    m = sf.loft(sf.circle(r, 12), [(x0, 1, 1), (x1, 1, 1)]); m.apply_transform(np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]], float)); uv = m.metadata["uv"]
    m.apply_translation((0, .3 - E + r, z)); m.metadata["uv"] = uv; return m
def _xcap(z, r=.11): return box(.5 - E, .54, .3 - E + r - .03, .3 - E + r + .03, z - .03, z + .03)
CART = [(1, "Flatbed"), (2, "Tub"), (3, "Two_Tier"), (4, "Tool_Crate"), (5, "Tank_Hauler")]

# ---------------- #21 amber street light pole 0.3 x 0.3 x 5.0, <=1200 ----------------
def light(v):
    p = Pod(f"ext_street_light_pole_0{v}"); n = 12
    p.add("Base", G, ring(.15, 0, .3, n, 1, .8))
    if v == 1:  # Column Lantern
        p.add("Pole", S, ring(.07, .3 - E, 4.4, n, 1, .8)); p.add("Housing", G, ring(.13, 4.4 - E, 4.5, n))
        p.add("Lamp_Ring", A, ring(.115, 4.5 - E, 4.53, n)); p.add("Diffuser", GL, ring(.12, 4.53 - E, 4.8, n))
        p.add("Cap", T, ring(.135, 4.8 - E, 5.0, n, 1, .4))
    elif v == 2:  # Halo Ring
        p.add("Pole", S, ring(.065, .3 - E, 4.7, n), ring(.065, 4.74 - E, 4.94, n)); p.add("Halo", A, ring(.15, 4.7 - E, 4.74, n))
        p.add("Cap", T, ring(.07, 4.94 - E, 5.0, n, 1, .5))
    elif v == 3:  # Light Seam: titanium pole with a vertical amber seam and glass head
        p.add("Pole", T, ring(.07, .3 - E, 4.6, n)); p.add("Seam", A, box(-.01, .01, .6, 4.5, .066, .075))
        p.add("Head_Glass", GL, ring(.1, 4.6 - E, 4.85, n)); p.add("Cap", G, ring(.11, 4.85 - E, 5.0, n, 1, .3))
    elif v == 4:  # Square Mast: square slate mast, gunmetal head box with glass underside and amber lamp
        p.add("Mast", S, box(-.06, .06, .3 - E, 4.7, -.06, .06))
        p.add("Head", G, box(-.15, .15, 4.8, 5.0, -.15, .15)); p.add("Head_Neck", G, box(-.05, .05, 4.7 - E, 4.776 + E, -.05, .05))  # neck stops in the glass diffuser
        p.add("Glass_Underside", GL, box(-.13, .13, 4.776, 4.8 + E, -.13, .13)); p.add("Lamp_Strip", A, box(-.1, .1, 4.86, 4.88, .146, .155))
    elif v == 5:  # Spin Markers: gunmetal column with three amber marker rings and a glass lantern
        ys = (.3, 1.2, 2.4, 3.6, 4.5)
        p.add("Pole", G, *[ring(.07, ys[k] - E, ys[k + 1] - .03, n) for k in range(4)])
        p.add("Marker_Rings", A, *[ring(.08, y - .03 - E, y, n) for y in ys[1:4]])
        p.add("Lantern_Glass", GL, ring(.12, 4.5 - E - .03, 4.85, n)); p.add("Cap", T, ring(.13, 4.85 - E, 5.0, n, 1, .5))
    return p
LIGHT = [(1, "Column_Lantern"), (2, "Halo_Ring"), (3, "Light_Seam"), (4, "Square_Mast"), (5, "Spin_Markers")]

# ---------------- #22 low bollard light 0.2 x 0.2 x 0.9, <=200 ----------------
def blight(v):
    p = Pod(f"ext_bollard_light_0{v}")
    if v == 1:  # Glass Head
        p.add("Post", G, ring(.09, 0, .7, 10)); p.add("Lamp_Disc", A, ring(.085, .7 - E, .72, 10))
        p.add("Glass_Head", GL, ring(.095, .72 - E, .86, 10)); p.add("Cap", T, ring(.1, .86 - E, .9, 10, 1, .7))
    elif v == 2:  # Square Lantern
        p.add("Post", S, box(-.09, .09, 0, .68, -.09, .09)); p.add("Lamp_Plate", A, box(-.085, .085, .68 - E, .7, -.085, .085))
        p.add("Glass_Box", GL, box(-.094, .094, .7 - E, .86, -.094, .094)); p.add("Cap", T, box(-.1, .1, .86 - E, .9, -.1, .1))
    elif v == 3:  # Front Slot: round post, amber strip behind a glass slot on the street face
        p.add("Post", G, ring(.095, 0, .86, 10)); p.add("Light_Strip", A, box(-.02, .02, .5, .82, .088, .096))
        p.add("Slot_Glass", GL, box(-.025, .025, .49, .83, .092, .1)); p.add("Cap", T, ring(.1, .86 - E, .9, 10, 1, .6))
    elif v == 4:  # Mushroom: slim slate post, wide titanium mushroom head, amber underside downlight
        p.add("Post", S, ring(.05, 0, .8, 10)); p.add("Downlight", A, ring(.085, .8 - E, .82, 10))
        p.add("Head", T, ring(.1, .82 - E, .86, 10, top=(.9, .5, .5)))
    elif v == 5:  # Tapered Glow Band: tapered titanium post, BLEND glass band over an amber core band
        sc = lambda y: 1 - .2 * y / .9
        p.add("Post", T, ring(.1, 0, .6, 10, 1, sc(.6)), ring(.1, .78 - E, .9, 10, sc(.78), sc(.9)))
        p.add("Amber_Line", A, ring(.103, .6 - E, .624, 10, sc(.6), sc(.624)))
        p.add("Glow_Glass", GL, ring(.097, .624 - E, .78, 10, sc(.624), sc(.78)))
    return p
BL = [(1, "Glass_Head"), (2, "Square_Lantern"), (3, "Front_Slot"), (4, "Mushroom"), (5, "Tapered_Glow_Band")]

sf.ASSETS.update({"cabinet": ("ext_junction_cabinet", cabinet, CAB, 400, "#35 utility junction cabinet 0.8x0.4x1.4"),
                  "cart": ("ext_service_hand_cart", cart, CART, 900, "#36 service hand cart 1.4x0.7x1.0"),
                  "light": ("ext_street_light_pole", light, LIGHT, 1200, "#21 amber street light 0.3x0.3x5.0"),
                  "blight": ("ext_bollard_light", blight, BL, 200, "#22 low bollard light 0.2x0.2x0.9")})
sf.HEAD["light"] = 4.25
if __name__ == "__main__":
    for k in (sys.argv[1:] or ["cabinet", "cart", "light", "blight"]): sf.build(k)
