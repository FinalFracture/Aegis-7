"""Owner-local render runner (temp-Rooftop). Read-only reuse of assemble_preview; do not edit it.
Renders into /workspace/renders/tennis_tower/rooms/temp-Rooftop/."""
import os, sys, json, shutil, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent; STRUCT = HERE.parent.parent / 'structure'; sys.path.insert(0, str(STRUCT))
import assemble_preview as AP
OUT = '/workspace/renders/tennis_tower/rooms/temp-Rooftop'
U = AP.ALL_UPPER if hasattr(AP, 'ALL_UPPER') else ['f3', 'roof', 'env', 'facade', 'plant']
SHOTS = [
 ('cab_01_aerial', (-30, 40, 40), (-6, 12.2, 40), 55, U),
 ('cab_02_lounge_walk', (-1.5, 13.9, 40), (-11, 13.5, 40), 70, []),
 ('cab_03_cabana_row', (-9, 14.5, 18), (-9, 13.5, 45), 65, []),
 ('cab_04_glass_rail', (-11.2, 13.8, 30), (-11.5, 13.5, 50), 70, []),
 ('play_01_aerial', (160, 42, 40), (134, 12.2, 40), 55, U),
 ('play_02_from_path', (129.2, 13.8, 39), (136, 13.2, 39), 70, []),
 ('play_03_perches', (127.5, 13.7, 33), (130, 13.3, 33), 65, []),
 ('play_04_soft4_seesaw', (138, 14.0, 26), (136, 13.0, 40), 70, []),
 ('roof_01_SW_cutout', (-20, 36, -10), (-6, 22.3, 5), 50, ['env','facade']),
 ('roof_02_SE_cutout', (160, 36, -10), (134, 22.3, 5), 50, ['env','facade']),
 ('roof_03_NW_cutout', (-20, 36, 90), (-6, 22.3, 74), 50, ['env','facade']),
 ('roof_04_NE_cutout', (160, 36, 90), (134, 22.3, 74), 50, ['env','facade']),
 ('dine_01_aerial', (-28, 46, 39.5), (12, 12.2, 39.5), 60, ['roof','env','facade','plant']),
 ('dine_02_bar_from_west', (5.5, 13.9, 39.5), (14, 13.0, 39.5), 70, []),
 ('dine_03_S_terrace', (5.0, 15.0, 6.0), (13, 12.6, 34), 70, []),
 ('dine_04_N_terrace_acc', (5.0, 15.0, 73.0), (13, 12.6, 45), 70, []),
 ('slng_01_S_aerial', (80, 40, -28), (80, 12.2, 6), 60, ['roof','env','facade','plant']),
 ('slng_02_S_west_void', (25.5, 13.9, 3.3), (36, 13.0, 7.5), 70, []),
 ('slng_03_S_east', (93.5, 13.9, 3.3), (112, 13.0, 7.5), 70, []),
 ('slng_04_N_west', (25.5, 13.9, 75.7), (46, 13.0, 71.5), 70, []),
]

def main():
    os.makedirs(OUT, exist_ok=True)
    AP.structure(); AP.roof(); AP.envelope(); AP.site(); AP.interiors(); AP.OUT = OUT
    if hasattr(AP, 'hull_mesh'): AP.hull_mesh()
    doc = json.load(open(HERE.parents[4] / 'godot/assets/models/rooms/temp-Rooftop_placements.json'))
    drop = {'tt_bar.glb', 'tt_bar_stool.glb'}
    PL = [p for p in AP.PL if not (os.path.basename(p['glb']) in drop and p.get('tag') == 'f3')]
    md = HERE.parents[4] / 'godot/assets/models'
    for ps in doc['rooms'].values():
        for p in ps:
            PL.append(dict(glb=str(md / f"{p['asset']}.glb"), p=p['p'], yaw=p['yaw'], tag=p.get('tag', 'f3')))
    miss = {p['glb'] for p in PL if not os.path.exists(p['glb'])}; print('placements', len(PL), 'missing', len(miss))
    tmp = '/tmp/tt_rooftop_preview'; os.makedirs(tmp, exist_ok=True)
    open(os.path.join(tmp, 'project.godot'), 'w').write('config_version=5\n[application]\nconfig/name="tt_rooftop"\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n')
    shutil.copy(STRUCT / 'render_preview.gd', os.path.join(tmp, 'render_preview.gd'))
    names = sys.argv[1:]
    shots = [s for s in SHOTS if any(s[0].startswith(n) for n in names)] if names else SHOTS
    json.dump(dict(placements=PL, shots=[dict(name=n, pos=list(p), look=list(l), fov=f, hide=h, amb=(1.5 if '_0' not in n else .6), out=os.path.join(OUT, n + '.png')) for n, p, l, f, h in shots]), open(os.path.join(tmp, 'job.json'), 'w'))
    cmd = ['xvfb-run', '-a', '-s', '-screen 0 1920x1080x24', 'godot', '--rendering-driver', 'opengl3', '--resolution', '1600x900', '--path', tmp, '-s', 'render_preview.gd']
    subprocess.run(cmd, check=False, timeout=3000)

if __name__ == '__main__':
    main()
