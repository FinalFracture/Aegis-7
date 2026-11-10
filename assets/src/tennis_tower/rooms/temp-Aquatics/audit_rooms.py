"""Read-only cross-chunk clipping and placement audit against untouched structure.
Model A1-A5 is the repository ext_clip_check, never altered. Placement uses the
actual GLB transforms; structural walls are the blockout's box meshes.
"""
import sys,json
from pathlib import Path
import numpy as np,trimesh
HERE=Path(__file__).resolve().parent; TT=HERE.parent.parent; ROOT=HERE.parents[4]
sys.path[:0]=[str(TT),str(TT/'structure')]
from modlib import cc,Part,recenter,merge
import build_structure as bs
from rtree import index
OUT=Path('/workspace/renders/tennis_tower/rooms/temp-Aquatics'); MD=ROOT/'godot/assets/models'
layout=json.load(open(OUT/'layout.json'))
rooms={}; solids=[]; audit={}; contacts=[]
for name,entry in layout.items():
    scene=trimesh.load(MD/(name+'.glb'),force='scene',process=True)
    room=name.split('_')[1]
    for gn,m in scene.geometry.items():
        if 'colonly' in gn: continue
        mat=m.visual.material.name
        m=m.copy(); m.apply_translation(entry['world_offset']); m.merge_vertices(merge_tex=True,merge_norm=True); m.metadata['uv']=np.zeros((len(m.vertices),2))
        rooms.setdefault(room,{}).setdefault(gn,[]).append(m)
        if mat not in ('TT_OpaquePoolWater','TT_CyanLED','TT_Leaf','TT_LeafLight','TT_BallYellow'):
            for piece in m.split(only_watertight=False):
                solids.append((name,gn,piece))
                expected=None
                if room=='pool' and gn in ('Start_Foot','Board_StairTreads','Board_Supports','Chair_Feet'): expected=2.012
                if room=='gallery' and gn in ('Locker_Carcass','Bench_Feet','Changing_SupportPosts','Shower_Back'): expected=6.112
                if room=='leisure' and gn=='RiverStone_Mound': expected=1.012
                # Rev 3.5 flush footbridges span the channel and bear on the river-lining tops (+0.904), same ±5 mm rule.
                if room=='leisure' and gn=='RiverBridge_Deck': expected=.904
                if room=='leisure' and gn=='Spray_Foot': expected=.435
                if expected is not None:
                    delta=float(piece.bounds[0,1]-expected)
                    contacts.append(dict(asset=name,part=gn,delta=round(delta,5),passed=abs(delta)<=.005+1e-6))
for room,parts in rooms.items():
    p=Part(room)
    for n,ms in parts.items(): p.P[n]=('unused',merge(ms))
    chk=cc.check(recenter(p).P,n_samp=80)
    audit[room]=chk
    json.dump(audit,open(OUT/'placement_audit.json','w'),indent=2)
    print(room,'cross-chunk clipping',chk['pass'],'worst',chk['worst_overlap'],'coplanar',len(chk['coplanar']),flush=True)
# Every fixed wall/column is tested in building coordinates, after final placement.
walls=[]
for group,mat,meshes in bs.walls_f1()+bs.walls_f2():
    if 'Scissor' not in group:
        walls.append((group,meshes.bounds))
for pn,mk,m in bs.columns():
    if 'Pad' not in pn: walls.append((pn,m.bounds))
idx=index.Index(properties=index.Property(dimension=3))
for i,(_,b) in enumerate(walls): idx.insert(i,tuple(b[0])+tuple(b[1]))
fail=[]; candidates=0
for asset,gn,m in solids:
    for wi in idx.intersection(tuple(m.bounds[0])+tuple(m.bounds[1])):
        wall,b=walls[wi]; ov=np.minimum(b[1],m.bounds[1])-np.maximum(b[0],m.bounds[0])
        if min(ov)<=.01+1e-6: continue
        candidates+=1
        pts,_=trimesh.sample.sample_surface(m,150,seed=8)
        pts=np.vstack([m.vertices,pts]); inside=np.all(pts>b[0],axis=1)&np.all(pts<b[1],axis=1)
        if inside.any():
            depth=np.minimum(pts[inside]-b[0],b[1]-pts[inside]).min(axis=1).max()
            if depth>.01+1e-6: fail.append(dict(asset=asset,part=gn,wall=wall,depth=round(float(depth),4)))
print('wall/column penetration failures',len(fail),'candidates',candidates,flush=True)
audit['placement']=dict(failures=fail,tested_components=len(solids),wall_count=len(walls))
audit['floor_contact']=dict(pass_=all(c['passed'] for c in contacts),checks=contacts)
audit['floor_contact']['pass']=audit['floor_contact'].pop('pass_')
print('floor contact',len(contacts),'checks',audit['floor_contact']['pass'],flush=True)
json.dump(audit,open(OUT/'placement_audit.json','w'),indent=2)
assert not fail and all(v['pass'] for k,v in audit.items() if k!='placement'), 'Placement/clipping failures; see placement_audit.json'
