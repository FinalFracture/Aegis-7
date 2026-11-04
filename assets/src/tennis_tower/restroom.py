"""Rook: Tennis Tower restroom stall row (spec §3.10, §3.11.7 Rev 2.5, block positions Rev 2.7). Instanced half row unit
7.2 x 2.4 m = 8 WC stalls 0.9 x 1.5 m + half of the 1.8 m aisle; place two face to face (180 deg) for the 7.2 x 4.8 m row unit,
repeat along X every 7.2 m. Partitions 1.8 m tall, 0.15 m off the floor. Back wet wall (+0.1 m) at -Z, aisle centre at +Z.
REUSE: WC and status light are bath_pod_generator.wc() (residential bath pod fixture, white composite / gunmetal vac unit),
partitions/pilasters/doors use the Rev C stair PBR texture sets (white cladding, qa03 gunmetal), door-frame language of bath_pod door_frame().
Run: python3 restroom.py"""
from modlib import *
import bath_pod_generator as bp
bp.FL = 0.0  # host floor = 0 (bath pod has a raised 0.06 floor)
NS, SW, SD, WW = 8, .9, 1.5, .1
Z0 = -2.4; ZW = Z0 + WW; ZF = ZW + SD - WW + .1   # wall back, wall face, stall front line (1.5 m stall incl. wall)

def wc(p, x, z):  # bath_pod_generator.wc() recipe (same bowl/seat lofts, materials, status light); vac tank wall-hung + slimmed so it clears the bowl
    blk, place = bp.blk, bp.place
    base = blk(-0.19, 0.19, 0, 0.38, 0.05, 0.62, 0.15, 4)
    seat = xf(loft(rrect(0.36, 0.5, 0.17, 4), [(0.38 - E, 1, 1), (0.42, 1, 1), (0.43, .9, .9)]), t=(0, 0, 0.36))
    p.add("WC", "white", place(base, x, z, "+z"), place(seat, x, z, "+z"))
    p.add("WC_VacUnit", "gunmetal", place(blk(-0.2, 0.2, .45, 1.0, 0.0, 0.05 + E, 0.02), x, z, "+z"))
    p.add("StatusLight", "green", place(blk(-0.05, 0.05, .9, .92, 0.05, 0.064, 0.004, 1), x, z, "+z"))

def build(q):
    p = Part(); X0 = -NS*SW/2
    p.add("Wet_Wall", WH, box(X0 + .001, -X0 - .001, 0, 2.4, Z0, ZW)); p.add("Aisle_Centre_Strip", SSL, box(X0 + .001, -X0 - .001, 0, .003, -.03, -.001))  # fixes the bbox to the 2.4 m half unit
    bounds = [X0 + k*SW for k in range(NS + 1)]
    for b in bounds[1:-1]: p.add("Partitions", WH, box(b - .0125, b + .0125, .15, 1.95, ZW - E, ZF - .02 + E))
    pil = [box(max(b - .075, X0 + .001), min(b + .075, -X0 - .001), 0, 1.95, ZF - .02, ZF + .02) for b in bounds]
    p.add("Pilasters", SGM, *pil)
    doors, pulls = [], []
    for k in range(NS):
        cx = X0 + (k + .5)*SW; a, b = X0 + k*SW + .075 + .005, X0 + (k+1)*SW - .075 - .005
        doors.append(box(a, b, .15, 1.95, ZF - .012, ZF + .008)); pulls.append(box(b - .08, b - .05, .95, 1.1, ZF + .008 - E, ZF + .03))
        wc(p, cx, ZW - E)
    p.add("Stall_Doors", q.get("door_mat", WH), *doors); p.add("Door_Pulls", ALY, *pulls)
    d = q["dress"]
    if d == "garden":  # aisle-side planter ledge on the pilaster line + green wall band above the stalls
        p.add("Green_Wall_Band", LF, green_wall(X0 + .1, -X0 - .1, 1.98, 2.38, ZW, r=.12, seed=2))
        tr, so, sy = planter(X0 + .2, X0 + 1.4, 0, ZF + .05, ZF + .45, h=.5); p.add("Planter_Trough", G, tr); p.add("Planter_Soil", SO, so); p.add("Foliage", LF2, shrubs(X0 + .25, X0 + 1.35, sy, ZF + .25, r=.16, seed=4))
    elif d == "leaf":  # leaf crests on the partition tops (Leaf Capital echo), leaf-green doors
        p.add("Leaf_Crests", LF, *[leaf_dir((b, 1.95 - .003, (ZW + ZF)/2), (0, 1, 0), .35, .25, t=.0125) for b in bounds[1:-1]])
    elif d == "fin":  # Branch Fin pilaster caps: Y-forks rising from every pilaster
        for b in bounds[1:-1]:
            c = np.array([b, 1.95 + .25, ZF]); p.add("Branch_Fins", ST, tube((b, 1.95 - E, ZF), c, .015, 5), tube(c, (b - .12, 2.35, ZF), .01, 4), tube(c, (b + .12, 2.35, ZF), .01, 4))
    elif d == "canopy":  # Branch Diagonals rail over the aisle with hanging leaf pots
        p.add("Canopy_Rail", ST, box(X0 + .001, -X0 - .001, 2.34, 2.38, ZW - E, ZW + .3 + E), *[tube((x, 2.36, ZW + .3), (x + .45, 2.36, ZW + .9), .015, 4) for x in np.arange(X0 + .2, -X0 - .6, .9)])
        p.add("Hanging_Foliage", LF2, *[clump((x + .45, 2.36 - .16 + E - .01, ZW + .9), .15, i) for i, x in enumerate(np.arange(X0 + .2, -X0 - .6, .9))])
    elif d == "court":  # sports wayfinding: court-line floor stripe, green/amber occupancy lamps, tennis-ball coat hooks
        p.add("Court_Line_Floor", AM, box(X0 + .05, -X0 - .05, 0, .003, ZF + .6, ZF + .66))
        p.add("Occupancy_Lamps", GRN, *[box(X0 + (k + .5)*SW - .04, X0 + (k + .5)*SW + .04, 1.97, 2.0, ZF - .015, ZF + .015) for k in range(NS)]) if False else \
        p.add("Occupancy_Lamps", GRN, *[box(X0 + k*SW + .075 + .01, X0 + k*SW + .075 + .07, 1.8, 1.86, ZF + .008 - E, ZF + .02) for k in range(NS)])
        p.add("Ball_Hooks", BA, *[node((X0 + (k + .5)*SW, 1.6, ZW + .035 - E), .035, 0) for k in range(NS)])
    return p

VARIANTS = [
    dict(label="Garden Aisle: green wall band over the stalls, aisle planter", dress="garden"),
    dict(label="Leaf Crest: leaf tops on partitions, leaf-green doors", dress="leaf", door_mat=LF),
    dict(label="Branch Fin: Y-fork caps on every pilaster", dress="fin"),
    dict(label="Canopy: Branch Diagonals rail with hanging foliage", dress="canopy"),
    dict(label="Court Line: floor stripe, occupancy lamps, ball hooks", dress="court"),
]
if __name__ == "__main__": run("restroom", build, VARIANTS, title="half row unit 7.2 x 2.4 m, 8 WC stalls (place 2 face to face) | nature + sports")
