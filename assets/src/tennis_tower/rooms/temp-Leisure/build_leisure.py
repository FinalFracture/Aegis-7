"""temp-Leisure: build every F1 leisure room asset (spec Rev 3.2), write placements + check report.
Usage: python3 build_leisure.py   (then python3 render_leisure.py)"""
import subprocess
from lz_lib import *
import bowling, axe, food, arcade, entrances
OUT = Path('/workspace/renders/tennis_tower/rooms/temp-Leisure'); OUT.mkdir(parents=True, exist_ok=True)
ROOT = TT.parent.parent.parent
def main():
    PL = []; stats = {}
    bowling.build(PL); axe.build(PL); stats['food'] = food.build(PL); stats['arcade'] = arcade.build(PL); stats['entrances'] = entrances.build(PL)
    for p in PL: p['glb'] = 'res://assets/models/' + p['asset'] + '.glb'
    rooms = {'F1-BOWL': 'tt_bowl_', 'F1-AXE': 'tt_axe_', 'F1-FOOD': 'tt_food_', 'F1-ARC/F2-ARC': 'tt_arc_'}
    doc = dict(owner='temp-Leisure', spec='design/strip5_tennis_tower_v1.md Rev 3.2 (cc7fd9a)', axes='Y up, X axial, Z across; yaw deg about +Y',
               note='p = building coords of the GLB pivot (bottom centre). N/E secondary entrances use Arrival canonical tt_secondary_entrance_n/e (no room-local forks).',
               stats=stats, rooms={r: [p for p in PL if p['asset'].startswith(k)] for r, k in rooms.items()})
    pp = GM / 'rooms' / 'temp-Leisure_placements.json'; pp.parent.mkdir(exist_ok=True); json.dump(doc, open(pp, 'w'), indent=1)
    # independent re-validation + first-pass checks on every GLB we wrote
    fp = {}
    for r in REP:
        g = GM / f"{r['asset']}.glb"
        r['validate_recheck'] = bool(vm.validate_file(str(g), check_tri_range=(1, 5999), require_blend_glass=False, require_textures=False))
        p = subprocess.run([sys.executable, str(ROOT / 'tools/first_pass_check.py'), str(g), '--no-godot'], capture_output=True, text=True, cwd=ROOT)
        s = p.stdout.strip().splitlines(); fp[r['asset']] = dict(exit=p.returncode, summary=[l for l in s if 'FAIL' in l or 'WARN' in l or 'SUMMARY' in l.upper()][-12:])
        r['first_pass_exit'] = p.returncode
    json.dump(REP, open(OUT / 'model_report.json', 'w'), indent=1, default=str); json.dump(fp, open(OUT / 'first_pass.json', 'w'), indent=1)
    for r in REP: print(f"{r['asset']:32s} {r['tris']:5d} clip+val={r['passed']} reval={r['validate_recheck']} fp_exit={r['first_pass_exit']}")
    print(json.dumps(stats)); print('placements', len(PL), pp)
if __name__ == '__main__': main()
