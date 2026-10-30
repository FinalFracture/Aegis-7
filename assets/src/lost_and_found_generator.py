"""Rev C #55 Lost-and-found (Laundry N wall, X -4.3..-3.0; qty 1; 1.3 W x 1.4 H x 0.3 D). Final only, no iterations.
Kitbash: the #35 rail bins (toy_bin_generator.final_combo: alloy wall rail, gunmetal wall plates and hooks, white bins with slate lids and amber latches)
re-hung low on the wall, plus a small new wordless notice board (the exterior #52 board was dropped, so no mesh existed).
Board: slate pin panel in an alloy frame with blank cards (white/amber/green/violet) on gunmetal pins, no text. Pivot bottom-centre, +Z front, wall at -Z."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from hydro_planter_generator import cyl, box, bev, blk, Pod, dc, wg
from dining_chair_generator import export_final
OUT = os.path.join(dc.ROOT, "design/assets/lost_and_found")
W, H, D = 1.3, 1.4, .3; Z0 = -D / 2
def rail_bins(p, RY=.55, BD=.255):  # #35 rail-bin kit, same parts and materials as toy_chest_rail_bins.glb
    zb0 = Z0 + .035; zb1 = zb0 + BD
    p.add("Wall_Rail", "alloy", blk(-W / 2 + .03, W / 2 - .03, RY - .02, RY + .02, zb0 - .03, zb0, .006, 1))
    p.add("Wall_Plates", "gunmetal", *[box(x - .05, x + .05, RY - .08, RY + .08, Z0, Z0 + .005) for x in (-.58, .58)])
    p.add("Rail_Bolts", "alloy", *[cyl(x, Z0 + .005, .008, RY + dy - .005, RY + dy + .005, 6) for x in (-.58, .58) for dy in (-.06, .06)])
    for x in (-.42, 0, .42):
        p.add("Bins", "white", bev(.38, BD - .02, RY - .16, RY + .3, .03, .01, 2, x, zb0 + BD / 2 + .01))
        p.add("Bin_Hooks", "gunmetal", box(x - .1, x + .1, RY - .02, RY + .05, zb0, zb0 + .02))
        p.add("Bin_Lids", "slate", bev(.38, BD - .02, RY + .3, RY + .312, .03, .004, 1, x, zb0 + BD / 2 + .01))
        p.add("Bin_Latches", "amber", box(x - .025, x + .025, RY + .26, RY + .29, zb1, zb1 + .008))
def notice_board(p, y0=.95, y1=H):  # small wordless pin board
    z = Z0; t = .03; p.add("Board_Panel", "slate", box(-W / 2 + .04, W / 2 - .04, y0 + .03, y1 - .03, z, z + .025))
    p.add("Board_Frame", "alloy", box(-W / 2, W / 2, y0, y0 + t, z, z + .04), box(-W / 2, W / 2, y1 - t, y1, z, z + .04), box(-W / 2, -W / 2 + .04, y0 + t, y1 - t, z, z + .04), box(W / 2 - .04, W / 2, y0 + t, y1 - t, z, z + .04))
    cards = [(-.45, 1.2, .16, .12, "white"), (-.22, 1.25, .12, .16, "amber"), (.0, 1.17, .18, .12, "white"), (.25, 1.24, .14, .14, "green"), (.47, 1.15, .14, .1, "violet"), (-.35, 1.06, .14, .08, "white"), (.2, 1.05, .2, .07, "white")]
    for x, y, w, h, c in cards: p.add("Cards_" + c, c, box(x - w / 2, x + w / 2, y - h / 2, y + h / 2, z + .025, z + .028))
    pins = []
    for x, y, w, h, c in cards: pins.append(box(x - .008, x + .008, y + h / 2 - .025, y + h / 2 - .009, z + .028, z + .04))
    p.add("Pins", "gunmetal", *pins)
    p.add("Board_Lamp", "green", box(W / 2 - .12, W / 2 - .06, y0 + .006, y0 + .024, z + .04, z + .045))  # wordless 'items waiting' lamp
    p.add("Board_Brackets", "gunmetal", *[box(x - .03, x + .03, y0 - .06, y0, Z0, Z0 + .03) for x in (-.5, .5)])
def final():
    p = Pod("Lost_And_Found_Rail_Bins"); rail_bins(p); notice_board(p); return p
def final_main():
    p = final(); gp = os.path.join(dc.ROOT, "godot/assets/models/lost_and_found_rail_bins.glb"); tris, geo = export_final(p.P, [gp])
    V = np.vstack([g[1] for g in geo.values()]); bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("tris", tris, "size", (V.max(0) - V.min(0)).round(3), "lo", V.min(0).round(3), "hi", V.max(0).round(3), "bad", bad)
    os.makedirs(OUT, exist_ok=True); sp = os.path.join(OUT, "final_lost_and_found_sheet.png"); wg.sheet(p, sp, "Final  #55 lost-and-found: #35 rail bins + wordless notice board"); os.remove(sp.replace("_sheet.png", ".glb"))
if __name__ == "__main__": final_main()
