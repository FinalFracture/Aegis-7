"""Place owned room finishes into Rook's blockout without changing his files.
Writes the requested placement JSON and renders selected rooms in a throwaway
Godot project. No source-side Godot import files are generated.
"""
import json,os,sys,math,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[4]
MD=ROOT/'godot/assets/models'; OUT=Path('/workspace/renders/tennis_tower/rooms/temp-Aquatics')
TT=HERE.parent.parent
sys.path[:0]=[str(TT),str(TT/'structure')]
import numpy as np
import assemble_preview as block
PL=[]
HELD_UNPLACED=()  # nothing held from placement
def put(asset,pos,yaw=0,tag='finish',room='',**extra):
    PL.append(dict(glb=str(MD/(asset+'.glb')),p=pos,yaw=yaw,tag=tag,room=room,**extra))
def placements():
    layout=json.load(open(OUT/'layout.json'))
    for asset,d in layout.items():
        if asset.startswith(HELD_UNPLACED): continue
        if asset in ('tt_corridor_tank_bay','tt_aquarium_tank'): continue  # placed explicitly below (four bays, yaw 180); never at the layout origin
        room={'pool':'F1-POOL','gallery':'F2-GAL','bridges':'F2-BRG','corridor':'F1-AQC','leisure':'F1-LEIS'}[asset.split('_')[1]]
        put(asset,d['world_offset'],room=room,note=d['note'])
    # Existing aquarium assets, not remodelled. Recentered tank acrylic line = local z+.4.
    for x in (3.75,9.25,14.75,20.25): put('tt_corridor_tank_bay',[x,0,42.9],180,room='F1-AQC')
    for x in (2.75,8.25,13.75,19.25): put('tt_aquarium_floor',[x,0,37.9],room='F1-AQC')
    for x in (5,10.5,16,21.5): put('tt_aquarium_bench',[x,.02,40.9],room='F1-AQC')
    for x in (2.5,23.5): put('tt_aquarium_plinth',[x,.02,36],room='F1-AQC')
    for x in (6,12,18): put('tt_aquarium_caustic',[x,5.22,40],room='F1-AQC')
    if '--placements-only' not in sys.argv: write_scene()
    json.dump(dict(spec_revision='3.2',axis='Y-up; +Z front; building coordinates',
        water_shader='res://assets/models/rooms/temp-Aquatics_water.gdshader',
        water_material_name='TT_OpaquePoolWater',placements=PL),open(MD/'rooms/temp-Aquatics_placements.json','w'),indent=2)
def write_scene():
    # This is a room-additions scene: instantiate once alongside the structural kit.
    lines=['[gd_scene load_steps='+str(len(PL)+2)+' format=3]', '']
    lines.append('[ext_resource type="Script" path="res://assets/models/rooms/temp-Aquatics_water_bind.gd" id="1"]')
    for i,p in enumerate(PL,2):
        rel=Path(p['glb']).relative_to(ROOT/'godot')
        lines.append('[ext_resource type="PackedScene" path="res://'+str(rel)+'" id="'+str(i)+'"]')
    lines+=['','[node name="AquaticRooms" type="Node3D"]','script = ExtResource("1")']
    for i,p in enumerate(PL,2):
        name=Path(p['glb']).stem+'_'+str(i)
        lines+=['','[node name="'+name+'" parent="." instance=ExtResource("'+str(i)+'")]']
        lines.append('position = Vector3('+', '.join(str(v) for v in p['p'])+')')
        if p['yaw']: lines.append('rotation = Vector3(0, '+str(math.radians(p['yaw']))+', 0)')
    (MD/'rooms/temp-Aquatics_rooms.tscn').write_text('\n'.join(lines)+'\n')
def render():
    # Use the untouched blockout's own placements, not a parallel structural layout.
    old=json.load(open('/workspace/renders/tennis_tower/structure_blockout/placements.json'))
    base=[]
    for p in old:
        asset=Path(p['glb']).stem
        if asset.startswith('tt_struct_') and not any(x in asset for x in ('roof','ball_net','plant_stack','f3_walls','climb')): base.append(p)
        elif asset=='tt_stair_core_b' and p['p'][0]<0 and p['p'][1]==6.1: base.append(p)
    tmp=Path('/tmp/tt_rooms_temp_Aquatics'); tmp.mkdir(exist_ok=True)
    (tmp/'project.godot').write_text('config_version=5\n[application]\nconfig/name="Aquatic room previews"\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n')
    shutil.copy(MD/'rooms/temp-Aquatics_water.gdshader',tmp/'water.gdshader')
    src=(TT/'structure/render_preview.gd').read_text()
    src=src.replace('var tagged := {}','var tagged := {}\nvar water_material: ShaderMaterial')
    src=src.replace('func _init() -> void:','func _init() -> void:\n\twater_material = ShaderMaterial.new()\n\twater_material.shader = load("res://water.gdshader")')
    src=src.replace('for c in n.get_children():','if n is MeshInstance3D and n.mesh:\n\t\tfor i in n.mesh.get_surface_count():\n\t\t\tvar m = n.mesh.surface_get_material(i)\n\t\t\tif m and m.resource_name == "TT_OpaquePoolWater": n.set_surface_override_material(i, water_material)\n\tfor c in n.get_children():')
    src=src.replace('print("shot ", s["name"])','print("shot ", s["name"], " draw_calls=", Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))')
    src=src.replace('\tquit()', '\tfor sc in cache.values(): sc.free()\n\tcache.clear()\n\tworld.free()\n\tcam.free()\n\tsun.free()\n\tenv.free()\n\twater_material = null\n\tawait process_frame\n\tquit()')
    (tmp/'render_preview.gd').write_text(src)
    shots=[]
    def shot(n,p,l,f=70,hide=()): shots.append(dict(name=n,pos=p,look=l,fov=f,hide=list(hide),amb=1.15,out=str(OUT/(n+'.png'))))
    # For sectional overview, hide upper slab/roof tags only. Interiors keep structure.
    for p in base:
        a=Path(p['glb']).stem
        p['tag']='upper' if any(k in a for k in ('f2_slab','f3_slab','diving_coffer')) else 'structure'
    shot('pool_00_baseline',(1.0,3.8,1.5),(21,2.4,26),75,['finish'])
    shot('pool_01_sw_overview',(-9,28,-10),(14,2,18),65,['upper'])
    shot('pool_02_west_deck',(1.0,3.8,1.5),(21,2.4,26),75)
    shot('pool_03_diving_boards',(7.6,4,33),(17.5,4,26),78)
    shot('pool_04_lane_start',(1.9,3.2,21),(20,2,6),75)
    shot('gallery_01_changing_aisle',(-7.5,7.8,21),(-10,7.4,34),75)
    shot('gallery_02_view_walk',(-3.7,7.8,22),(-2.7,7.7,48),75)
    shot('gallery_03_showers',(-7.5,7.8,58.6),(-10.8,7.6,65),75)
    shot('corridor_01_west_entry',(1.6,1.75,36),(21,1.7,41),75)
    shot('corridor_02_reef_detail',(8,1.7,39.6),(14,1.5,43.7),72)
    shot('bridges_01_view_deck',(1.1,7.8,35.8),(22,7.4,39.7),75)
    shot('leisure_01_north_overview',(-7,24,91),(15,1,61),68,['upper'])
    shot('leisure_02_splash_island',(5,3.0,76.7),(17,1.6,55),75)
    shot('leisure_03_river_bridge',(2.5,2.8,46),(10,1.7,52),72)
    shot('bridges_02_slide_dogleg',(-1.5,9.5,55.5),(16,6.7,59.2),70,['upper'])
    json.dump(dict(placements=base+PL,shots=shots),open(tmp/'job.json','w'))
    cmd=['xvfb-run','-a','-s','-screen 0 1600x900x24','godot','--rendering-driver','opengl3','--resolution','1600x900','--path',str(tmp),'-s','render_preview.gd']
    subprocess.run(cmd,check=True,timeout=180)
def main():
    placements()
    if '--placements-only' in sys.argv: return
    if '--no-render' not in sys.argv: render()
if __name__=='__main__': main()
