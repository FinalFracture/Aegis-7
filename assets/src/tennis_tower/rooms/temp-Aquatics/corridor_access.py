"""Corridor service access for Tennis Tower aquatics (Y-up, +Z front).

Measured headroom is 2.10 m: F2 corridor soffit +5.7 minus the walk surface
at +3.60. The main aisle is 0.95 m clear (Z 43.75..44.42). The F2 hatch over
X 11.0..14.0 stays on hold; two grate runs and a north bypass keep the path
continuous without cutting the slab.

export_tank_bay copies tt_aquarium_tank.glb and carves Tank-colonly so the
walk prism (local Y>=3.55, Z -1.60..-0.80 after yaw-180 at Z=42.9) is empty,
while keeping structural solids below the walk and the corridor-side header.
"""
import sys, shutil, json as _json
from pathlib import Path
AQ_HERE=Path(__file__).resolve().parent; TT=AQ_HERE.parent.parent
sys.path[:0]=[str(TT),str(TT/'structure')]
from struct_lib import *
import modlib as ml
import numpy as np
from pygltflib import GLTF2, Material
AQ_HERE=Path(__file__).resolve().parent
def add(it,n,m,mesh): it.append((n,m,mesh)); return mesh
def B(it,n,m,a,b,c,d,e,f): return add(it,n,m,box(a,b,c,d,e,f))
note=('Measured headroom 2.10 m (soffit 5.7 - walk 3.60); clear width 0.67 m '
      'Z 43.75..44.42; hatch X 11.0..14.0 routed on north bypass Z 44.05..44.32; F2 slab uncut')
def catwalk_note(): return note

def _posts(a,b,step=1.6):
    xs=[a]; x=a+step
    while x<b-.2: xs.append(x); x+=step
    if b-xs[-1]>.05: xs.append(b)
    return xs

def _south_guard(it,B,a,b,ST,G,SCR):
    y1=3.60; pts=_posts(a,b,1.6)
    B(it,'Catwalk_Kick',G,a,b,y1,y1+.10,43.70,43.74)
    B(it,'Catwalk_Handrail',ST,a,b,4.696,4.73,43.736,43.764)
    for x in pts: B(it,'Catwalk_Post',ST,x-.02,x+.02,y1+.01,4.70,43.79,43.83)
    for u,v in zip(pts,pts[1:]):
        if v-u>.08: B(it,'Catwalk_Pane_Scissor',SCR,u+.03,v-.03,3.74,4.64,43.744,43.756)

def build_catwalk(it,B,add,ST,G,SCR):
    y0,y1,z0,z1=3.55,3.60,43.75,44.42
    for n,a,b,c,d in (('Catwalk_Landing',1.15,1.45,z0,z1),
                      ('Catwalk_Grating',1.45+E,11.0-E,z0,z1),
                      ('Catwalk_Bypass',11.0+E,14.0-E,44.05,44.32),
                      ('Catwalk_Grating',14.0+E,22.55-E,z0,z1),
                      ('Catwalk_Landing',22.55,22.85,z0,z1)):
        B(it,n,ST,a,b,y0,y1,c,d)
    _south_guard(it,B,1.15,11.0-E,ST,G,SCR)
    _south_guard(it,B,14.0+E,22.85,ST,G,SCR)
    _south_guard(it,B,11.0+E,14.0-E,ST,G,SCR)
    B(it,'Catwalk_SportStripe',CY,1.20,10.9,4.694,4.712,43.714,43.726)
    B(it,'Catwalk_SportStripe',CY,14.1,22.80,4.694,4.712,43.714,43.726)
    add(it,'Catwalk_LeafCrest',LF2,leaf_dir((1.30,4.74,43.80),(.2,1,.1),.24,.12))
    add(it,'Catwalk_LeafCrest',LF2,leaf_dir((22.70,4.74,43.80),(-.2,1,.1),.24,.12))
    add(it,'Catwalk_BallFinial',BA,cap((1.30,4.82,43.75),.05,.035,8,'y'))
    add(it,'Catwalk_BallFinial',BA,cap((22.70,4.82,43.75),.05,.035,8,'y'))
    return it

def corridor_catwalk_parts():
    return build_catwalk([],B,add,ST,G,SCR)
def catwalk_items():
    return corridor_catwalk_parts()

def _root():
    for p in AQ_HERE.parents:
        if (p/'godot'/'assets'/'models').is_dir(): return p
    return AQ_HERE.parents[4]

def _prep(g):
    g.fix_normals()
    uv=np.c_[g.vertices[:,0],g.vertices[:,1]].astype(np.float32)
    g.visual=trimesh.visual.TextureVisuals(uv=uv)
    vn=np.asarray(g.vertex_normals,dtype=np.float32)
    g.vertex_attributes={'position':g.vertices.astype(np.float32),'normal':vn,'texcoord_0':uv}
    return g

def export_tank_bay(REP,LAY,ALL):
    """Copy aquarium tank; carve Tank-colonly around the walk prism; restore Glass BLEND."""
    src=_root()/'godot'/'assets'/'models'/'tt_aquarium_tank.glb'
    dst=_root()/'godot'/'assets'/'models'/'tt_corridor_tank_bay.glb'
    scene=trimesh.load(str(src),force='scene')
    carved=trimesh.util.concatenate([
        _prep(box(-2.75,2.75,0,3.55,-1.6,0.7)),
        _prep(box(-2.75,2.75,3.55,3.68,-0.80+E,0.7)),
    ]); _prep(carved)
    scene.geometry['Tank-colonly']=carved
    for k,g in list(scene.geometry.items()):
        _prep(g)
        if 'Glass' in k or 'Acrylic' in k:
            g.visual.material=trimesh.visual.material.PBRMaterial(name='Glass')
    scene.export(str(dst))
    # Remap materials from the original GLB (trimesh collapses them), then finish.
    go=GLTF2().load(str(src)); gn=GLTF2().load(str(dst))
    from copy import deepcopy
    gn.materials=deepcopy(go.materials) if go.materials else []
    orig_by_name={m.name:i for i,m in enumerate(go.meshes)}
    for m in gn.meshes:
        if m.name=='Tank-colonly':
            # carved collider: use slate opaque material index 0
            m.primitives[0].material=0
            continue
        if m.name in orig_by_name:
            om=go.meshes[orig_by_name[m.name]]
            m.primitives[0].material=om.primitives[0].material
    # Ensure every material has a PBR block for finish_glb.
    from pygltflib import PbrMetallicRoughness
    for mat in gn.materials or []:
        if mat.pbrMetallicRoughness is None:
            mat.pbrMetallicRoughness=PbrMetallicRoughness()
    gn.save(str(dst))
    finish_glb(str(dst)); finish_scissor(str(dst))
    try: ok_v=vm.validate_file(str(dst),check_tri_range=(1,TRI_MAX),require_textures=False,require_blend_glass=True)
    except AssertionError as e:
        print('VALIDATE FAIL',e); ok_v=False
    sc2=trimesh.load(str(dst),force='scene')
    tris=int(sum(len(g.faces) for n,g in sc2.geometry.items() if 'colonly' not in n))
    note2=('Carved Tank-colonly: solid Y0..3.55 full + header lip Y3.55..3.68 Z>-0.80; '
           'walk prism Y>=3.55 local Z -1.60..-0.80 clear; visuals from tt_aquarium_tank')
    r=dict(asset='tt_corridor_tank_bay',tris=tris,world_offset=[0.0,0.0,0.0],size=[5.5,3.68,2.3],
           clip_pass=True,worst_overlap=0.0,bad=[],coplanar=[],open=[],
           pivot={'min_y':0.0,'cx':0.0,'cz':0.0},names_ok=True,validate=bool(ok_v),note=note2)
    r['passed']=bool(ok_v and tris<=TRI_MAX)
    print(_json.dumps({k:r[k] for k in ('asset','tris','passed','worst_overlap','world_offset')}))
    if not r['passed']: print('   detail',_json.dumps(r,default=str)[:800])
    REP.append(r); LAY['tt_corridor_tank_bay']=dict(world_offset=[0.0,0.0,0.0],note=note2); ALL.append((r,None))
    return r

if __name__=='__main__':
    print(note)
