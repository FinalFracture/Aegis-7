"""Task lamp (rev C item #27, blockout Apt201_Workbench_TaskLight, 0.2 x 0.2 x 0.5 m, qty 3).
Five iterations: no swinging pendants, latched arms/heads, clamp or rail mounting, in-cylinder manufacture,
Sprocket-serviceable heads. Pivot: bottom-centre at the bench-top/rail mount point, front +Z."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
import dining_chair_generator as dc
from dining_chair_generator import xf, torus_ring
from bath_pod_generator import blk, cyl, Pod
from kitchen_counter_generator import bev, box
from washer_dryer_generator import zdisc, zring
from wardrobe_generator import sheet
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT = os.path.join(dc.ROOT, "design/assets/task_lamp")

def rod(p0, p1, r, s=10):
    p0, p1 = np.array(p0, float), np.array(p1, float); L = np.linalg.norm(p1 - p0)
    m = cyl(0, 0, r, 0, L, s); M = trimesh.geometry.align_vectors([0, 1, 0], (p1 - p0) / L)
    m = xf(m, M); return xf(m, t=tuple(p0))
def ylatch(p, x, y, z, R=.022):      # amber latch collar around a vertical joint
    p.add("Latch_Lights", "amber", xf(torus_ring(R, .004, 14, 3), t=(x, y, z)))
def clamp(p, z=0.0):                 # C-clamp on a 30 mm bench edge (bench top at y=0, edge face at z=-.0)
    p.add("Clamp", "gunmetal", box(-.035, .035, -.004, .012, z - .07, z + .01), box(-.035, .035, -.05, -.034, z - .07, z + .01),
          box(-.035, .035, -.05, .012, z + .0, z + .016))
    p.add("Clamp_Screw", "alloy", cyl(0, z - .04, .008, -.08, -.05, 10), xf(zdisc(0, -.08, 0, .01, .02, 12), t=(0, 0, z - .045)))
def head_disc(p, c, r=.06, h=.035, mat="white"):
    x, y, z = c; p.add("Head_Shell", mat, cyl(x, z, r, y, y + h, 18))
    p.add("Head_Lens", "violet", cyl(x, z, r - .008, y - .003, y, 18))

def iter1():  # clamp + two latched elbow arms + disc head
    p = Pod("Clamp_Elbow"); clamp(p)
    p.add("Post", "alloy", cyl(0, -.03, .012, .012, .22, 12)); ylatch(p, 0, .22, -.03)
    p.add("Arm", "white", rod((0, .22, -.03), (0, .36, .06), .011), rod((0, .36, .06), (0, .40, .15), .011))
    p.add("Joints", "gunmetal", xf(zdisc(0, .36, -.015, .015, .02, 12), t=(0, 0, .06)))
    ylatch(p, 0, .36, .06, .024); head_disc(p, (0, .38, .16)); return p
def iter2():  # rail shuttle mount: slider on 40 mm wall rail, horizontal latched boom
    p = Pod("Rail_Slider")
    p.add("Rail_Stub", "alloy", blk(-.1, .1, .0, .04, -.1, -.08, .006, 1))
    p.add("Slider", "gunmetal", bev(.07, .05, -.01, .05, .01, .004, 1, 0, -.065)); ylatch(p, 0, .055, -.065)
    p.add("Mast", "alloy", cyl(0, -.065, .012, .05, .42, 12))
    p.add("Boom", "white", rod((0, .42, -.065), (0, .42, .11), .012)); ylatch(p, 0, .42, -.065, .02)
    head_disc(p, (0, .39, .11), .055); return p
def iter3():  # telescoping mast in clamp, tilt-latched cylinder head (all turned parts)
    p = Pod("Telescoping_Mast"); clamp(p)
    p.add("Mast_Outer", "gunmetal", cyl(0, -.03, .016, .012, .26, 14)); p.add("Mast_Inner", "alloy", cyl(0, -.03, .011, .26, .44, 12), box(-.004, .004, .40, .44, -.034, -.026))
    ylatch(p, 0, .26, -.03, .021)
    p.add("Head_Yoke", "gunmetal", box(-.04, .04, .44, .45, -.04, -.02), box(-.04, -.028, .4, .45, -.04, -.02), box(.028, .04, .4, .45, -.04, -.02))
    p.add("Head_Shell", "white", rod((0, .41, -.05), (0, .41, .14), .028, 16))
    p.add("Head_Lens", "violet", rod((0, .41, .14), (0, .41, .143), .022, 16)); p.add("Latch_Lights", "amber", box(.04, .046, .4, .42, -.035, -.025)); return p
def iter4():  # stacked latch-ring column + cantilever bar light
    p = Pod("Ring_Column"); clamp(p)
    for i in range(5): p.add("Column", "alloy" if i % 2 else "white", cyl(0, -.03, .014, .012 + i * .07, .08 + i * .07, 12))
    for i in range(1, 5): ylatch(p, 0, .012 + i * .07, -.03, .018)
    p.add("Bar_Arm", "white", blk(-.012, .012, .36, .38, -.03, .16, .006, 1))
    p.add("Bar_Light", "gunmetal", blk(-.03, .03, .34, .36, .04, .17, .006, 1)); p.add("Head_Lens", "violet", box(-.024, .024, .337, .34, .05, .16)); return p
def iter5():  # Sprocket-service cartridge head (front-pull lug), clamp + latched elbow
    p = Pod("Service_Cartridge"); clamp(p)
    p.add("Post", "alloy", cyl(0, -.03, .013, .012, .30, 12)); ylatch(p, 0, .30, -.03)
    p.add("Arm", "white", rod((0, .30, -.03), (0, .42, .07), .012))
    p.add("Head_Dock", "gunmetal", bev(.1, .08, .39, .43, .012, .004, 2, 0, .1))
    p.add("Head_Shell", "white", bev(.085, .07, .37, .395, .01, .004, 1, 0, .1)); p.add("Head_Lens", "violet", box(-.035, .035, .367, .37, .07, .13))
    p.add("Service_Lug", "amber", box(-.015, .015, .38, .39, .135, .15)); p.add("Status", "violet", box(-.01, .01, .43, .434, .08, .1)); return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (#27 task lamp)")
        isos.append((p.name, iso)); print(i, p.name, tris, lo, hi, (hi - lo).round(3), "bad:", bad)
    fig, axs = plt.subplots(2, 3, figsize=(15, 10), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=11, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
if __name__ == "__main__": main()
