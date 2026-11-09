"""temp-Rooftop: build F3 cabanas, playground, roof cutouts; write placements + check reports.
Usage: python3 build_rooftop.py"""
import subprocess, sys
from rt_lib import *
import cabanas, playground, roof_cutout
OUT = Path('/workspace/renders/tennis_tower/rooms/temp-Rooftop'); OUT.mkdir(parents=True, exist_ok=True)
ROOT = TT.parent.parent.parent

def main():
    PL = []; stats = {}
    stats['cabanas'] = cabanas.build(PL)
    stats['playground'] = playground.build(PL)
    stats['roof'] = roof_cutout.build(PL)
    for p in PL:
        if 'glb' not in p or not str(p['glb']).startswith('res://'):
            p['glb'] = 'res://assets/models/' + p['asset'] + '.glb'
    doc = dict(owner='temp-Rooftop', spec='design/strip5_tennis_tower_v1.md Rev 3.0',
               axes='Y up, X axial, Z across; yaw deg about +Y',
               note='p = building coords of GLB pivot (bottom centre). F3_Y=12.2. Rook owns slab cutback/guard/ridge12.',
               stats=stats,
               rooms={
                   'F3-CAB': [p for p in PL if p['asset'].startswith('tt_cab') or p['asset'] == 'tt_cabana'],
                   'F3-PLAY': [p for p in PL if p['asset'].startswith('tt_play') or p['asset'] in ('tt_see_saw','tt_swing_set','tt_dome_climber','tt_toddler_zone','tt_balance_trail','tt_play_tower','tt_play_surface')],
                   'F3-ROOF-CUT': [p for p in PL if p['asset'].startswith('tt_roof_plant')],
               })
    pp = GM / 'rooms' / 'temp-Rooftop_placements.json'; pp.parent.mkdir(exist_ok=True)
    json.dump(doc, open(pp, 'w'), indent=1)
    fp = {}
    for r in REP:
        g = GM / f"{r['asset']}.glb"
        r['validate_recheck'] = bool(vm.validate_file(str(g), check_tri_range=(1, 5999), require_blend_glass=False, require_textures=False))
        p = subprocess.run([sys.executable, str(ROOT / 'tools/first_pass_check.py'), str(g), '--no-godot'], capture_output=True, text=True, cwd=str(ROOT))
        s = p.stdout.strip().splitlines()
        fp[r['asset']] = dict(exit=p.returncode, summary=[l for l in s if 'FAIL' in l or 'WARN' in l or 'SUMMARY' in l.upper()][-12:])
        r['first_pass_exit'] = p.returncode
    json.dump(REP, open(OUT / 'model_report.json', 'w'), indent=1, default=str)
    json.dump(fp, open(OUT / 'first_pass.json', 'w'), indent=1)
    for r in REP:
        print(f"{r['asset']:32s} {r['tris']:5d} clip+val={r['passed']} reval={r['validate_recheck']} fp_exit={r['first_pass_exit']}")
    print(json.dumps(stats)); print('placements', len(PL), pp)

if __name__ == '__main__':
    main()
