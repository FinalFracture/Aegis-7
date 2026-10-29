"""Rev C #16 armchair / reading chair (102, 203; qty 2; 1.0 x 1.0 x 1.0). Five iterations, family language.
Bottom-centre pivot, front +Z. Spin-down: cushions clipped (amber), base bolted / latched; no loose contents."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import dining_chair_generator as dc
from bath_pod_generator import blk, cyl, Pod
from kitchen_counter_generator import bev, box
from double_bed_generator import soft
from sofa_generator import cushions, clips, floor_clamps, tilt
from task_lamp_generator import rod
import wardrobe_generator as wg
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT = os.path.join(dc.ROOT, "design/assets/armchair")
W = D = H = 1.0; ZB, ZF = -.5, .5; SEAT = .43

def iter1():  # moulded white tub, slate cushions, recessed plinth with floor clamps
    p = Pod("Moulded_Tub")
    p.add("Plinth", "gunmetal", bev(.7, .7, 0, .1, .05, .01, 2, 0, 0))
    p.add("Shell_Seat", "white", bev(.78, .9, .1, SEAT - .14, .06, .02, 2, 0, .03))
    p.add("Shell_Back", "white", bev(W, .16, .1, H - .1, .08, .025, 3, 0, ZB + .08))
    for s in (-1, 1): p.add("Shell_Arms", "white", bev(.12, .9, .1, .64, .06, .02, 3, s * .44, .03))
    cushions(p, -.38, .38, 1, SEAT - .14, SEAT, ZB + .16, ZF - .04, "slatefab", by1=H - .14, bz=ZB + .16)
    clips(p, [-.2, .2], SEAT - .14, ZF - .03); floor_clamps(p, (-.25, .25), (-.2, .2), top=.06); return p
def iter2():  # alloy sled frame, clip-in cushion cassettes
    p = Pod("Alloy_Sled")
    for s in (-1, 1):
        x = s * .45
        p.add("Sled_Frame", "alloy", rod((x, .02, ZB + .05), (x, .02, ZF - .05), .018, 10), rod((x, .02, ZF - .05), (x, .62, ZF - .1), .018, 10),
              rod((x, .62, ZF - .1), (x, .62, ZB + .1), .018, 10), rod((x, .02, ZB + .05), (x, H - .05, ZB + .02), .018, 10))
        p.add("Arm_Pads", "slate", bev(.08, .6, .62, .66, .02, .006, 1, x, 0))
    p.add("Cross_Tubes", "alloy", rod((-.45, .3, ZF - .12), (.45, .3, ZF - .12), .016, 10), rod((-.45, .3, ZB + .1), (.45, .3, ZB + .1), .016, 10),
          rod((-.45, H - .08, ZB + .03), (.45, H - .08, ZB + .03), .016, 10))
    p.add("Seat_Cassette", "gunmetal", bev(.86, .8, .26, .3, .02, .006, 1, 0, .03)); p.add("Back_Cassette", "gunmetal", tilt(bev(.86, .04, .3, H - .1, .02, .006, 1, 0, ZB + .08), -10, [0, .3, ZB + .08]))
    cushions(p, -.42, .42, 1, .3, SEAT, ZB + .14, ZF - .05, "warmgrey", by1=H - .12, bz=ZB + .12)
    clips(p, [-.25, .25], .3, ZF - .07)
    p.add("Floor_Latches", "amber", *[box(s * .45 - .02, s * .45 + .02, 0, .015, z - .03, z + .03) for s in (-1, 1) for z in (ZB + .1, ZF - .1)]); return p
def iter3():  # wingback reading chair with integrated violet reading light + empty side slot
    p = Pod("Wingback_Reader")
    p.add("Base", "gunmetal", bev(.8, .8, 0, .12, .04, .01, 2, 0, 0))
    p.add("Shell_Seat", "white", bev(.84, .9, .12, SEAT - .13, .05, .02, 2, 0, .03))
    p.add("Shell_Back", "white", bev(W, .14, .12, H, .08, .02, 3, 0, ZB + .07))
    for s in (-1, 1):
        p.add("Wings", "white", bev(.1, .3, .62, H - .03, .04, .015, 2, s * .45, ZB + .2))
        p.add("Shell_Arms", "white", bev(.1, .85, .12, .62, .05, .015, 2, s * .45, .05))
    p.add("Reading_Light", "violet", box(-.4, -.32, H - .08, H - .06, ZB + .14, ZB + .2))
    p.add("Side_Slot", "gunmetal", box(.5, .52, .2, .55, -.25, .25))
    cushions(p, -.39, .39, 1, SEAT - .13, SEAT, ZB + .15, ZF - .04, "slatefab", by1=H - .06, bz=ZB + .15)
    p.add("Head_Pillow", "slatefab", soft(.5, .1, H - .3, H - .12, .04, 0, ZB + .2)); clips(p, [-.2, .2], SEAT - .13, ZF - .03)
    floor_clamps(p, (-.3, .3), (-.25, .25), top=.08); return p
def iter4():  # swivel on a latched pedestal (spin-down: amber swivel lock), bolted floor disc
    p = Pod("Swivel_Pedestal")
    p.add("Floor_Disc", "gunmetal", cyl(0, 0, .3, 0, .03, 24)); p.add("Pedestal", "alloy", cyl(0, 0, .06, .03, .25, 16))
    p.add("Swivel_Lock", "amber", cyl(0, 0, .075, .2, .23, 16)); p.add("Bolts", "alloy", *[cyl(.22 * np.cos(a), .22 * np.sin(a), .015, .03, .04, 8) for a in np.linspace(0, 2 * np.pi, 6, endpoint=False)])
    p.add("Shell", "white", bev(.92, .88, .25, SEAT - .12, .1, .03, 3, 0, .02), bev(.96, .12, .3, H - .05, .1, .03, 3, 0, ZB + .08),
          *[bev(.1, .75, .3, .64, .05, .015, 2, s * .43, .05) for s in (-1, 1)])
    cushions(p, -.38, .38, 1, SEAT - .12, SEAT, ZB + .15, ZF - .05, "slatefab", by1=H - .1, bz=ZB + .15); clips(p, [-.2, .2], SEAT - .12, ZF - .05); return p
def iter5():  # Sprocket-side: chair with attached side table, charge/coupler port at 0.45 on the table side
    p = Pod("Sprocket_Side")
    p.add("Base", "gunmetal", bev(.95, .8, 0, .1, .04, .01, 2, .0, 0))
    p.add("Shell", "white", bev(.7, .88, .1, SEAT - .14, .05, .02, 2, -.13, .03), bev(.78, .14, .1, H - .08, .08, .02, 3, -.11, ZB + .07),
          bev(.08, .85, .1, .62, .05, .015, 2, -.46, .05))
    p.add("Side_Table", "white", bev(.2, .8, .1, .62, .04, .012, 2, .38, 0)); p.add("Table_Top", "slate", bev(.22, .82, .62, .65, .02, .006, 1, .38, 0))
    p.add("Sprocket_Port", "gunmetal", bev(.14, .02, .38, .52, .01, .004, 1, .38, ZF + .0)); p.add("Port_Ring", "amber", box(.35, .41, .43, .47, ZF + .01, ZF + .014))
    p.add("Status", "green", box(.33, .43, .56, .58, ZF + .0, ZF + .004))
    cushions(p, -.47, .21, 1, SEAT - .14, SEAT, ZB + .15, ZF - .04, "warmgrey", by1=H - .12, bz=ZB + .15); clips(p, [-.3, .05], SEAT - .14, ZF - .03)
    floor_clamps(p, (-.3, .35), (-.25, .25), top=.06); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#16 armchair)")
        isos.append((p.name, iso)); print(i, p.name, tris, (hi - lo).round(3), "bad", bad)
    fig, axs = plt.subplots(2, 3, figsize=(15, 10), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__": main()
