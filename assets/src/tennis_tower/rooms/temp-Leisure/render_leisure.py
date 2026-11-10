"""Owner-local render runner (temp-Leisure). Reuses assemble_preview's placement functions read-only (the file is not
edited), swaps in our scissor entrance copies, adds temp-Leisure_placements.json and renders our room shots with Godot
headless into /workspace/renders/tennis_tower/rooms/temp-Leisure/. Throwaway Godot project in /tmp."""
import os, sys, json, shutil, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent; STRUCT = HERE.parent.parent / 'structure'; sys.path.insert(0, str(STRUCT))
import assemble_preview as AP
OUT = '/workspace/renders/tennis_tower/rooms/temp-Leisure'
U = AP.ALL_UPPER; U2 = ["f3", "roof", "env", "facade", "plant"]
SHOTS = [
 ("final_bowl_01_cutaway_aerial", (36, 24, -14), (45, 0, 8), 60, U), ("final_bowl_02_int_from_settees", (30.8, 1.7, 7.4), (56, 1.0, 7.4), 70, []),
 ("final_bowl_03_int_pin_deck_masking", (49, 1.9, 1.2), (56.5, 1.4, 9), 70, []), ("final_bowl_04_int_core_acoustic_panels", (50, 2.2, 14.2), (57, 2.6, 6), 70, []),
 ("final_axe_01_cutaway_aerial", (89, 28, -16), (89, 0, 8), 60, U), ("final_axe_02_int_row1_from_aisle", (77.6, 1.7, 14.4), (84, 1.4, 5), 75, []),
 ("final_axe_03_int_target_close", (79.2, 1.6, 1.4), (83.3, 1.5, 2.2), 70, []), ("final_axe_04_int_row2_from_aisle", (94.5, 1.7, 14.4), (101, 1.4, 5), 75, []),
 ("final_food_01_cutaway_aerial", (72, 32, 104), (72, 0, 71), 60, U), ("final_food_02_int_east_seating", (101, 1.7, 65.2), (78, 1.2, 73), 70, []),
 ("final_food_03_int_stalls_n_entrance", (64.5, 1.9, 66.5), (73, 1.8, 77), 75, []), ("final_food_04_int_west_stalls_waste_door", (57.5, 1.7, 66.5), (48, 1.6, 76), 75, []),
 ("final_arc_01_L1_cutaway_aerial", (168, 36, 40), (126, 0, 40), 60, U), ("final_arc_02_L1_int_south", (114.2, 1.7, 1.0), (128, 1.0, 30), 75, []),
 ("final_arc_03_L1_int_prize_counter", (121, 1.7, 69), (122.5, 1.4, 60), 70, []), ("final_arc_04_L1_feature_stair", (128, 1.8, 29), (134, 3.0, 39.2), 75, []),
 ("final_arc_05_L2_cutaway_aerial", (168, 42, 40), (126, 6.1, 40), 60, U2), ("final_arc_06_L2_int_north", (114.2, 7.8, 77.6), (128, 7.0, 45), 75, []),
]
def main():
    os.makedirs(OUT, exist_ok=True)
    AP.structure(); AP.roof(); AP.envelope(); AP.site(); AP.interiors(); AP.OUT = OUT; AP.hull_mesh()
    doc = json.load(open(HERE.parents[4] / 'godot/assets/models/rooms/temp-Leisure_placements.json'))
    PL = list(AP.PL)
    md = HERE.parents[4] / 'godot/assets/models'
    for ps in doc['rooms'].values():
        for p in ps: PL.append(dict(glb=str(md / f"{p['asset']}.glb"), p=p['p'], yaw=p['yaw'], tag=p['tag']))
    for p in PL:
        if 'secondary_entrance_s' in p['glb']: pass
    miss = {p['glb'] for p in PL if not os.path.exists(p['glb'])}; print('placements', len(PL), 'missing', miss)
    tmp = '/tmp/tt_leisure_preview'; os.makedirs(tmp, exist_ok=True)
    open(os.path.join(tmp, 'project.godot'), 'w').write('config_version=5\n[application]\nconfig/name="tt_leisure"\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n')
    shutil.copy(STRUCT / 'render_preview.gd', os.path.join(tmp, 'render_preview.gd'))
    json.dump(dict(placements=PL, shots=[dict(name=n, pos=p, look=l, fov=f, hide=h, amb=(1.8 if '_int_' in n or '_L1_f' in n or '_L2_int' in n else .7), out=os.path.join(OUT, n + '.png')) for n, p, l, f, h in SHOTS]), open(os.path.join(tmp, 'job.json'), 'w'))
    cmd = ['xvfb-run', '-a', '-s', '-screen 0 1920x1080x24', 'godot', '--rendering-driver', 'opengl3', '--resolution', '1600x900', '--path', tmp, '-s', 'render_preview.gd']
    subprocess.run(cmd, check=False, timeout=3000)
if __name__ == '__main__': main()
