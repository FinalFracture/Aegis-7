"""Aquatic finish kit, spec Rev 3.2 (aquatic coordinates Rev 3.0). Run with Python 3; uses shared modlib.
Y-up and +Z-front, bottom-centre pivots; placements restore building coordinates.
No changes to the structural kit; finishes are separate additions to its cut-outs.
"""
import sys,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent; TT=HERE.parent.parent
sys.path[:0]=[str(TT),str(TT/'structure')]
from struct_lib import *
import modlib as ml
import corridor_access as ca
import slides as sl
import bridges_finish as bf
OUT=Path('/workspace/renders/tennis_tower/rooms/temp-Aquatics'); OUT.mkdir(parents=True,exist_ok=True)
ml._m('aq_tile','TT_PoolCeramic',(.64,.75,.78),0,.45)
ml._m('aq_water','TT_OpaquePoolWater',(.025,.31,.37),0,.19)
ml._m('aq_rubber','TT_PoolRubber',(.16,.37,.38),0,.85)
# Local palette correction only, no changes to shared modlib.
ml._m(WH,'TT_WhiteComposite',(.84,.87,.90),0,.5)
ml._m(SL,'TT_CarbonSlate',(.157,.18,.22),0,.75)
TI,WA,RU='aq_tile','aq_water','aq_rubber'
ml.TEXMAP['TT_PoolCeramic']='facade_aerospace_white_cladding.png'
REP=[]; LAY={}; ITEMS={}; ALL=[]
def add(it,n,m,mesh): it.append((n,m,mesh)); return mesh
def B(it,n,m,a,b,c,d,e,f): return add(it,n,m,box(a,b,c,d,e,f))
def subtract(host,cuts):
    for m in [host,*cuts]: m.fix_normals()
    return trimesh.boolean.difference([host,*cuts],engine='manifold')

def emit(n,it,note=''):
    if n.startswith('tt_gallery_') and n!='tt_gallery_floor':
        for _,_,m in it:
            uv=m.metadata['uv']; m.apply_translation((0,.008,0)); m.metadata['uv']=uv
    if n=='tt_pool_start_blocks' or n.startswith('tt_pool_board_') or n in ('tt_leisure_nature_mounds',):
        for _,_,m in it:
            uv=m.metadata['uv']; m.apply_translation((0,-.004,0)); m.metadata['uv']=uv
    for _,_,m in it: m.fix_normals()
    ITEMS[n]=it
    # Pack includes actual ceramic/rubber solid colliders, but excludes water/foliage.
    chunks=[[]]; count=0; solid=(SL,G,ST,CON,SSL,WH,TI,RU,SCR,LF)
    for item in sorted(it,key=lambda a:a[2].bounds.mean(0)[0]):
        cost=len(item[2].faces)*(2 if item[1] in solid else 1)
        if count+cost>5600 and chunks[-1]: chunks.append([]); count=0
        chunks[-1].append(item); count+=cost
    for i,ch in enumerate(chunks):
        name=n if len(chunks)==1 else n+'_'+chr(97+i)
        groups={}
        for pn,mk,m in ch: groups.setdefault((pn,mk),[]).append(m)
        cols=[m.copy() for pn,mk,m in ch if mk in solid]
        out=export_chunk(name,[(pn,mk,ms) for (pn,mk),ms in groups.items()],[("Solid-colonly",cols)],REP,layout=LAY,note=note)
        ALL.append(out)
def finish(it,rect,holes,y):
    for a,b,c,d in rect_minus(rect,holes): B(it,'Deck_Terrazzo',SL,a,b,y-E,y+.012,c,d)
def rim(it,r,y):
    a,b,c,d=r
    for z in (c-.09,d+.09):
        B(it,'Gutter_DarkSlot',G,a-.18,b+.18,y-E,y+.008,z-.06,z+.06)
        for x in np.arange(a,b,.27): B(it,'Gutter_Grate',ST,x,x+.11,y+.004,y+.016,z-.064,z+.064)
    for x in (a-.09,b+.09):
        B(it,'Gutter_DarkSlot',G,x-.06,x+.06,y-E,y+.008,c,d)
        for z in np.arange(c+.1,d-.1,.27): B(it,'Gutter_Grate',ST,x-.064,x+.064,y+.004,y+.016,z,min(z+.11,d-.004))  # last grate stops short of the slot end
    B(it,'Coping',WH,a,a+.06,y-.08,y+.016,c,d)
    B(it,'Coping',WH,b-.06,b,y-.08,y+.016,c,d)
    B(it,'Coping',WH,a+.064,b-.064,y-.08,y+.016,c,c+.06)
    B(it,'Coping',WH,a+.064,b-.064,y-.08,y+.016,d-.06,d)
def tank(it,r,y,depth,lanes=False):
    a,b,c,d=r; bot=y-depth
    B(it,'Tank_Floor',TI,a+.064,b-.064,bot,bot+.035,c+.064,d-.064)
    for x in (a+.03,b-.03): B(it,'Tank_Ends',TI,x-.026,x+.026,bot,bot+depth-.09,c+.064,d-.064)
    for z in (c+.03,d-.03): B(it,'Tank_Sides',TI,a+.004,b-.004,bot,bot+depth-.09,z-.026,z+.026)
    B(it,'Water_Opaque',WA,a+.064,b-.064,y-.085,y-.08,c+.064,d-.064)
    if lanes:
        for k in range(8):
            z=c+.5+1.25+2.5*k
            B(it,'Lane_FloorMarks',G,a+.655,b-.655,bot+.031,bot+.043,z-.07,z+.07)
            for x in (a+.6,b-.6): B(it,'Lane_EndT',G,x-.05,x+.05,bot+.031,bot+.043,z-.45,z+.45)
        for k in range(9):
            z=c+.5+2.5*k
            for j,x in enumerate(np.arange(a+.35,b-.3,.51)):
                add(it,'Lane_Floats',BA if j<9 or j>38 else WH,tube((x,y-.040,z),(x+.27,y-.040,z),.044,6))
    for x in np.arange(a+1,b-1,2.8):
        for z in np.arange(c+1,d-1,3):
            if not lanes or min(abs(z-(c+.5+2.5*k)) for k in range(9))>.10:
                B(it,'Water_Ripple',CY,x,x+.32,y-.077,y-.072,z,z+.014)
def pool():
    lap=(2.5,27.5,.5,21.5); dive=(15,28,22,34)
    it=[]; tank(it,lap,2,2,True); emit('tt_pool_lap_tank',it,'8 axial 25m lanes; opaque water; floor y=0, deck y=2')
    it=[]; tank(it,dive,2,4.5); emit('tt_pool_diving_tank',it,'4.5m depth; floor y=-2.5, water y=1.92')
    # Rev 3.5 switchback: L cut X4..10.5 @ Z22..31 + passage X4..6.25 @ Z31..34.5 (replaces the X4..7 stair hole);
    # the X10.5..15 top-landing exit band stays finished.
    it=[]; holes=[(2.32,27.68,.32,21.68),(14.82,28.18,21.82,34.18),(4,10.5,22,31),(4,6.25,31,34.5)]
    finish(it,(.32,29.68,.32,34.2),holes,2); rim(it,lap,2); rim(it,dive,2)
    emit('tt_pool_deck_finish',it,'finish on existing +2 deck; Rev 3.5 switchback L cut X4..10.5/Z22..31 + X4..6.25/Z31..34.5 left open')
    it=[]
    for k in range(8):
        z=2.25+2.5*k
        B(it,'Start_Foot',G,1.03,1.79,2.012,2.092,z-.37,z+.37)
        B(it,'Start_Pedestal',WH,1.12,1.70,2.088,2.48,z-.25,z+.25)
        add(it,'Start_Cap',ST,xf(loft(rrect(.82,.76,.08,3),[(2.476,1,1),(2.53,.95,.95)]),t=(1.41,0,z)))
        add(it,'Start_Nonslip',RU,xf(loft(rrect(.70,.62,.06,3),[(2.526,1,1),(2.55,1,1)]),t=(1.41,0,z)))
        for x in (1.13,1.42,1.65): B(it,'Start_TreadInlay',BA,x,x+.018,2.546,2.558,z-.29,z+.29)
        for j in range(k+1): B(it,'Start_LaneIndex',CY,1.705,1.717,2.17,2.23,z-.2+j*.05,z-.18+j*.05)
    emit('tt_pool_start_blocks',it,'8 blocks face +X; mount on deck finish at +2.012')
    for height,z in ((3,25),(1,28.5),(1,31.5)):
        it=[]; y=2.012; top=y+height; n=height*6; end=12.6; start=end-n*.28
        for i in range(n): B(it,'Board_StairTreads',WH,start+i*.28,start+(i+1)*.28+E,y,y+(i+1)*height/n,z-.5,z+.5)
        for i in range(n):
            yt=y+(i+1)*height/n
            B(it,'Board_TreadPad',RU,start+i*.28+.025,start+(i+1)*.28-.025,yt-E,yt+.009,z-.44,z+.44)
            B(it,'Board_TreadNosing',CY,start+(i+1)*.28-.018,start+(i+1)*.28-.006,yt-E,yt+.011,z-.43,z+.43)
        B(it,'Board_Platform',WH,end-E,14,top-.14,top+.003,z-.496,z+.496)
        for x in (12.8,13.8): B(it,'Board_Supports',G,x-.08,x+.08,y,top-.136,z-.43,z+.43)
        B(it,'Board_FlexibleBlade',WH,13.996,17.5,top-.08,top,z-.25,z+.25)
        B(it,'Board_Nonslip',RU,14.05,17.44,top-E,top+.018,z-.22,z+.22)
        for dz in (-.48,.48):
            a=np.array((start+.07,y+1.02,z+dz)); b=np.array((end-.07,top+1.02,z+dz))
            segments=[tube(a,b,.028,8),tube((end-.074,top+1.02,z+dz),(14,top+1.02,z+dz),.028,8)]
            for segment in segments: segment.fix_normals()
            handrail=trimesh.boolean.union(segments,engine='manifold')
            handrail.metadata['uv']=np.c_[handrail.vertices[:,0],handrail.vertices[:,1]]
            add(it,'Board_Handrail',ST,handrail)
            for x,base in ((start+.09,y+1/6),(end-.1,top),(13.85,top)):
                rail_y=float(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])) if x<end-.07 else top+1.02
                add(it,'Board_RailPosts',ST,tube((x,base-E,z+dz),(x,rail_y-.045,z+dz),.025,8))
        emit('tt_pool_board_3m' if height==3 else f'tt_pool_board_1m_{int(z*10)}',it,'Axial +X board; stairs .1667m rise x.28m; top measured above finish')
    it=[]
    for z in (23,27,28.8):
        B(it,'Wall_Panel',G,.154,.23,2.2,4.8,z-.65,z+.65)
        B(it,'Wall_Reveal',CY,.226,.24,2.28,2.33,z-.57,z+.57)
        for j in range(5): add(it,'Wall_LeafCrests',LF2,leaf_dir((.282,2.5+j*.34,z-.4),(.5,1,.4),.42,.24))
        add(it,'Wall_BallMedallion',BA,cap((.26,4.4,z),.14,.04,12,axis='x'))
    emit('tt_pool_nature_relief',it,'X0 pool wall sport/nature sculpture, no planter boxes')
    chair()
def chair():
    it=[]; y=2.012; x=28.7; z=12
    for a in (-.42,.42):
        for b in (-.4,.4):
            B(it,'Chair_Feet',G,x+a-.10,x+a+.10,y-.004,y+.055,z+b-.10,z+b+.10)   # 4 mm into the finish (no coplanar contact)
            add(it,'Chair_Legs',ST,tube((x+a,y+.050,z+b),(x+a*.72,y+1.82,z+b*.72),.04,8))
    B(it,'Chair_Seat',WH,x-.36,x+.36,y+1.816,y+1.89,z-.38,z+.38)
    B(it,'Chair_Back',RU,x+.31,x+.38,y+1.886,y+2.43,z-.38,z+.38)
    for dz in (-.34,.34): add(it,'Chair_Arm',ST,tube((x-.31,y+2.16,z+dz),(x+.314,y+2.16,z+dz),.025,8))
    for xx in (x-.30,x+.30): add(it,'Chair_Ladder',ST,tube((xx,y,z+.64),(xx,y+1.82,z+.35),.025,8))
    for j in range(6):
        h=.28*(j+1); zz=z+.64-.29*h/1.82
        add(it,'Chair_Rungs',ST,tube((x-.279,y+h,zz),(x+.279,y+h,zz),.022,8))
    emit('tt_pool_lifeguard_chair',it,'East deck +2; seat faces -X across lap pool; >.02m wall gap')
def gallery():
    it=[]
    for z0 in (22,28,40,45,51):
        for k in range(4):
            z=z0+k*.66
            B(it,'Locker_Carcass',G,-11.78,-11.2,6.1,8.16,z,z+.62)
            for j in range(2):
                y=6.16+j
                face=box(-11.204,-11.17,y,y+.93,z+.035,z+.585)
                cuts=[box(-11.21,-11.16,y+.69+l*.045,y+.706+l*.045,z+.1,z+.47) for l in range(3)]
                face=subtract(face,cuts)
                face.metadata['uv']=np.c_[(face.vertices[:,2]-z-.035)/.55,(face.vertices[:,1]-y)/.93]
                add(it,'Locker_Face',WH,face)
                B(it,'Locker_Reveal',CY,-11.174,-11.162,y+.08,y+.10,z+.07,z+.55)
                B(it,'Locker_Handle',ST,-11.166,-11.14,y+.35,y+.50,z+.45,z+.48)
    emit('tt_gallery_lockers',it,'40 stacked HDPE/alloy lockers, X-12 wall, no wood')
    it=[]
    for z in (24,31,43,48,54):
        for zz in (z-.65,z+.65): B(it,'Bench_Feet',G,-9.8,-9.25,6.1,6.17,zz-.07,zz+.07)
        B(it,'Bench_Pedestal',G,-9.71,-9.34,6.166,6.5,z-.65,z+.65)
        B(it,'Bench_Seat',WH,-9.85,-9.2,6.496,6.56,z-.86,z+.86)
        for zz in (z-.45,z,z+.45): B(it,'Bench_Inlay',CY,-9.79,-9.26,6.556,6.572,zz-.012,zz+.012)
    emit('tt_gallery_benches',it,'Five composite changing benches; >1.3m locker aisle')
    it=[]
    for z in (12,14,16,18):
        for zz in (z-.9,z+.9): B(it,'Changing_SupportPosts',ST,-9.304,-9.254,6.1,8.35,zz-.05,zz+.05)
        for yy in (6.6,7.8): add(it,'Changing_HardwareHinge',ST,tube((-9.27,yy,z+.746),(-9.27,yy,z+.876),.022,8))
        for zz in (z-.9,z+.9): B(it,'Changing_Dividers',WH,-11.6,-9.3,6.25,8.35,zz-.04,zz+.04)
        B(it,'Changing_Door',RU,-9.3,-9.24,6.3,8.25,z-.75,z+.75)
        B(it,'Changing_Handle',ST,-9.244,-9.20,7.05,7.24,z+.5,z+.53)
    emit('tt_gallery_changing',it,'Four private changing cabins; door interaction remains a Gage task')
    it=[]
    for z in (60,62,64,66):
        B(it,'Shower_Back',TI,-11.78,-11.71,6.1,8.5,z-.8,z+.8)
        for zz in (z-.85,z+.85): B(it,'Shower_Screens',WH,-11.71,-9.35,6.25,8.3,zz-.03,zz+.03)
        add(it,'Shower_Pipe',ST,tube((-11.67,6.75,z),(-11.67,7.104,z),.025,8))
        add(it,'Shower_Pipe',ST,tube((-11.67,7.246,z),(-11.67,8.179,z),.025,8))
        add(it,'Shower_Arm',ST,tube((-11.67,8.2,z),(-11.32,8.2,z),.025,8))
        add(it,'Shower_Head',ST,cap((-11.32,8.16,z),.09,.04,12,'y'))
        B(it,'Shower_Control',G,-11.706,-11.62,7.1,7.25,z-.1,z+.1)
    emit('tt_gallery_showers',it,'Four shower bays; dry preview; floor drainage pending')
    it=[]
    finish(it,(-11.8,-6.2,10.2,68.8),[],6.1)
    finish(it,(-5.8,-.2,20.8,58.2),[],6.1)
    emit('tt_gallery_floor',it,'12mm terrazzo finish, lockers and benches rest on top')
    it=[]
    for z in (23,32,46,54):
        B(it,'Gallery_CrestPanel',G,-5.904,-5.82,6.7,8.65,z-.47,z+.47)
        B(it,'Gallery_SportStripe',CY,-5.824,-5.806,6.82,6.86,z-.4,z+.4)
        for j in range(4): add(it,'Gallery_LeafCrests',LF2,leaf_dir((-5.77,7+j*.32,z-.25),(.5,1,.3),.36,.20))
        add(it,'Gallery_BallCrest',BA,cap((-5.79,8.45,z+.22),.11,.025,12,axis='x'))
    emit('tt_gallery_nature_relief',it,'Sculpted leaf and sport relief on gallery partition, clear of doors')
    it=[]
    for a,b in ((22,29.5),(31,33.8),(45.2,47.8),(49.2,55.5)):
        for y0,y1 in ((7.096,7.16),(9.04,9.104)): B(it,'Window_AlloyFrame',ST,-.22,-.146,y0,y1,a-.004,b+.004)
        for z0,z1 in ((a-.004,a+.06),(b-.06,b+.004)): B(it,'Window_AlloyFrame',ST,-.22,-.146,7.164,9.036,z0,z1)
        B(it,'Window_CyanSill',CY,-.234,-.216,7.108,7.14,a+.08,b-.08)
    emit('tt_gallery_window_frames',it,'Frames reuse existing TT_GlassScissor window panes; 4mm wall embeds')
def bridges():
    it=[]
    for z in (34.65,44.35):
        B(it,'Bridge_Kick',G,.32,24.15,6.1,6.2,z-.05,z+.05)
        for x in np.arange(.5,24,1.85): B(it,'Bridge_Post',ST,x-.025,x+.025,6.196,7.19,z-.025,z+.025)
        B(it,'Bridge_CapRail',ST,.32,24.15,7.186,7.22,z-.045,z+.045)
        xs=[.35]+list(np.arange(.5,24,1.85))+[24.12]
        for a,b in zip(xs,xs[1:]): B(it,'Bridge_Pane_Scissor',SCR,a+.021,b-.021,6.23,7.15,z-.008,z+.008)
    emit('tt_bridges_view_guards',it,'Existing view deck +6.1, 1.12m scissor guards; corridor soffit +5.7 untouched')
    # Rev3.0 gallery doorway is Z56..58.4; existing slab dogleg is kept, not replaced.
    it=[]
    for z in (58.10,60.30):
        B(it,'Bridge_Kick',G,2.1,19.8,6.1,6.2,z-.04,z+.04)
        B(it,'Bridge_CapRail',ST,2.1,19.8,7.186,7.22,z-.04,z+.04)
        for x in np.arange(2.2,19.9,1.5): B(it,'Bridge_Post',ST,x-.025,x+.025,6.196,7.19,z-.025,z+.025)
        xs=[2.15]+list(np.arange(2.2,19.9,1.5))+[19.8]
        for a,b in zip(xs,xs[1:]):
            if b-a>.05: B(it,'Bridge_Pane_Scissor',SCR,a+.021,b-.021,6.23,7.15,z-.008,z+.008)
    emit('tt_bridges_slide_guards',it,'Blockout dogleg span guards; gallery landing Z56..58.4 kept; gate/canopy/landing guards in separate assets')
    it=bf.landing_guard_items(); emit('tt_bridges_landing_guards',it,bf.landing_note())
    it=bf.t2_gate_items(); emit('tt_bridges_t2_gate',it,bf.gate_note())
    it=bf.canopy_items(); emit('tt_bridges_canopy',it,bf.canopy_note())
def text_z(it,label,cx,y,z,scale=.045):
    # Vectorize the bundled Pillow font into short raised, opaque LCD strokes.
    from PIL import Image,ImageFont,ImageDraw
    image=Image.new('L',(180,18)); draw=ImageDraw.Draw(image)
    draw.text((0,-2),label,font=ImageFont.load_default(size=10),fill=255)
    image=image.crop(image.getbbox()); a=np.asarray(image)>100
    h,w=a.shape; x0=cx-w*scale/2
    for row in range(h):
        xs=np.flatnonzero(a[row]); runs=np.split(xs,np.flatnonzero(np.diff(xs)>1)+1)
        for run in runs:
            if len(run): B(it,'Wayfinding_Letters',CY,x0+run[0]*scale,x0+(run[-1]+1)*scale,y+(h-row-1)*scale,y+(h-row-.06)*scale,z-E,z+.008)

def signs():
    it=[]
    B(it,'Portal_Blade',SL,4.05,6.95,3.08,3.66,34.496,34.55)
    B(it,'Portal_LowerReveal',ST,4.10,6.90,3.10,3.14,34.546,34.565)
    text_z(it,'AQUATICS',5.5,3.23,34.55,.055)
    emit('tt_corridor_deck_portal_sign',it,'AQUATICS above X4..7 deck door, 4mm embed in existing header')
    for name,x,yaw,label in (('courts',1,-90,'COURTS'),('foyer',24,90,'FOYER')):
        it=[]
        B(it,'Direction_Blade',SL,-1.35,1.35,2.6,3.16,-.06,.06)
        B(it,'Direction_Reveal',ST,-1.30,1.30,2.62,2.66,.056,.078)
        for xx in (-.9,.9): add(it,'Direction_Hangers',ST,tube((xx,3.156,0),(xx,5.704,0),.015,8))
        text_z(it,label,0,2.76,.06,.065)
        for pn,mk,m in it:
            uv=m.metadata['uv']; m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(yaw),[0,1,0])); m.apply_translation((x,0,38.5)); m.metadata['uv']=uv
        emit('tt_corridor_direction_'+name,it,'Directional blade replaces generic AQUATICS blade; 2.6m head clearance')
    it=[]; B(it,'Corridor_FloorClosure',SSL,22,24.5,0,.02,34.5,41.3)
    emit('tt_corridor_floor_closure',it,'Closes final 2.5m after four reused 5.5m floor bays')

def corridor():
    it=ca.catwalk_items(); emit('tt_corridor_catwalk',it,ca.catwalk_note())
    it=[]
    for x in (.65,23.65):
        skin=subtract(box(x-.25,x+.25,.02,5.62,42.34,42.47),[box(x-.2,x+.2,3.78,4.75,42.33,42.48)])
        skin.metadata['uv']=np.c_[skin.vertices[:,0]-x,skin.vertices[:,1]/5.62]
        add(it,'Service_EndCladding',G,skin)
        B(it,'Service_CyanReveal',CY,x-.18,x+.18,4.9,4.94,42.328,42.344)
        for y in np.arange(3.8,4.7,.13): B(it,'LifeSupport_Louvres',ST,x-.204,x+.204,y,y+.035,42.315,42.345)
        add(it,'Service_LeafCrest',LF2,leaf_dir((x-.1,3.35,42.312),(.3,1,0),.42,.2))
    emit('tt_corridor_services',it,'Opaque tank-end closures clad; clear public corridor maintained')
def leisure():
    it=[]
    # A continuous open ring: no cross-channel dams at the four corner joins.
    ring=[(1,29,47,50),(1,4,50,72),(26,29,50,72),(1,29,72,75)]
    for a,b,c,d in ring: B(it,'River_Floor',TI,a,b,0,.035,c,d)
    # Rev 3.5: river surface +0.85, now below the lining tops, so the water sits 4 mm inside the lining faces
    # (S/N full width, W/E between them with 4 mm joints).
    for a,b,c,d in ((1.059,28.941,47.059,49.941),(1.059,28.941,72.059,74.941),(1.059,3.941,49.945,72.055),(26.059,28.941,49.945,72.055)):
        B(it,'Water_Opaque',WA,a,b,.845,.85,c,d)
    for a,b,c,d in ((1,1.055,47,75),(28.945,29,47,75),(1.06,28.94,47,47.055),(1.06,28.94,74.945,75),
                       (3.945,4,50,72),(26,26.055,50,72),(4.004,25.996,49.945,50),(4.004,25.996,72,72.055)):
        B(it,'River_Lining',TI,a,b,.039,.904,c,d)   # top +0.904: the flush footbridges bear 4 mm onto the channel-wall linings
    emit('tt_leisure_river',it,'Open continuous 3m rectangular river, surface +0.85 (0.85 m deep); no corner dams')
    for name,r,dep in (('splash',(5,17,51,62),.6),('runout',(5,23,64,71),1)):
        it=[]; tank(it,r,1,dep)
        if name=='splash':
            it=[i for i in it if i[0]!='Water_Opaque']
            holes=[(x-.05,x+.05,z-.05,z+.05) for x,z in ((7,53),(15,54),(8,59),(15,60))]
            a,b,c,d=r
            for x0,x1,z0,z1 in rect_minus((a+.064,b-.064,c+.064,d-.064),holes): B(it,'Water_Opaque',WA,x0,x1,.915,.92,z0,z1)
        emit('tt_leisure_'+name,it,('Opaque water; slide runouts enter axially (-X) from the NE helices' if name=='runout' else 'Opaque water splash pool; ball-crown sprays'))
    it=[]
    holes=[(1,29,47,75)]
    # Rev 3.5 S-strip ramp (Rook): landing X0.3..1.8 @ Z44.8..47.0, legs X0.3..15.3 @ Z44.8..46.3.
    holes=[(1,29,47,75),(.3,15.3,44.8,46.3),(.3,1.8,44.8,47.0)]
    finish(it,(.32,29.68,44.8,78.68),holes,1)
    finish(it,(4.06,25.94,50.06,71.94),[(5,17,51,62),(5,23,64,71)],1)
    emit('tt_leisure_deck',it,'Finish on existing +1m deck, clear of water channels')
    it=[]
    # Rev 3.5 flush footbridges: 0.1 m deck (underside +0.9, 0.05 m over the +0.85 water), walking top +1.012 =
    # the deck finish top, so no step. Ends lap 4 mm into the deck finish. N X8..10 over Z72..75, S X18..20 over Z47..50.
    for x0,(za,zb) in ((18.0,(47.0,50.0)),(8.0,(72.0,75.0))):
        x1=x0+2.0
        B(it,'RiverBridge_Deck',WH,x0,x1,.9,1.0,za-.004,zb+.004)
        B(it,'RiverBridge_Nonslip',RU,x0+.004,x1-.004,.996,1.012,za-.002,zb+.002)
        for x in (x0+.05,x1-.05):
            B(it,'RiverBridge_Kick',G,x-.04,x+.04,1.008,1.112,za,zb)
            B(it,'RiverBridge_Rail',ST,x-.025,x+.025,2.078,2.112,za,zb)
            zp=[za+.05]+list(np.arange(za+.8,zb-.3,.8))+[zb-.05]
            for z in zp: B(it,'RiverBridge_Post',ST,x-.02,x+.02,1.108,2.082,z-.02,z+.02)
            for a,b in zip(zp,zp[1:]):
                B(it,'RiverBridge_Pane_Scissor',SCR,x-.008,x+.008,1.142,2.042,a+.016,b-.016)
    emit('tt_leisure_footbridges',it,'Rev 3.5 flush island footbridges (N X8..10, S X18..20): top +1.012 = deck finish, underside +0.9 over +0.85 water; 1.1 m scissor guards')
    it=[]
    for x,z in ((7,53),(15,54),(8,59),(15,60)):
        B(it,'Spray_Foot',G,x-.18,x+.18,.435,.48,z-.18,z+.18)
        add(it,'Spray_Stem',ST,tube((x,.476,z),(x,1.894,z),.045,8))
        add(it,'Spray_Crown',BA,node((x,2.01,z),.12,1))
        for dx,dz in ((.4,0),(-.4,0),(0,.4),(0,-.4)):
            add(it,'Spray_OpaqueStream',CY,tube((x+dx*.28,1.96,z+dz*.28),(x+dx,1.5,z+dz),.012,5))
    emit('tt_leisure_splash_sprays',it,'Sports ball spray crowns; stylized opaque streams, no alpha blending')
    it=[]
    for x,z in ((5,77),(17,77),(24,76.6)):
        m=clump((x,1.22,z),.52,int(x)); m.vertices[:,1]=1.012+(m.vertices[:,1]-m.bounds[0,1])*.42
        add(it,'RiverStone_Mound',SL,m)
        h=float(m.bounds[1,1]); add(it,'Moss_Crest',LF2,leaf_dir((x,h-E,z),(.3,1,.2),.24,.2))
    emit('tt_leisure_nature_mounds',it,'Sculpted river-stone/moss crests integrated into deck, no planter boxes')
    it=sl.tube_items(); emit('tt_leisure_slide_tubes',it,sl.tube_note())
    it=sl.link_items(); emit('tt_leisure_slide_link',it,sl.link_note())

def main():
    pool(); gallery(); bridges(); corridor(); signs(); leisure()
    ca.export_tank_bay(REP,LAY,ALL)
    json.dump(LAY,open(OUT/'layout.json','w'),indent=2)
    json.dump(REP,open(OUT/'model_report.json','w'),indent=2)
    assert all(r['passed'] for r in REP),'Clip/validator failure: see model_report.json'
if __name__=='__main__': main()
