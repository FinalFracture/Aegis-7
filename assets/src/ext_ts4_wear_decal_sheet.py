import sys; sys.path.insert(0,"assets/src")
import numpy as np, trimesh
from PIL import Image, ImageDraw
import ext_ts4_wear_decal_generator as G
S=260; W,H=int(4.1*S),int(.75*S)
def render(c):
    im=Image.new("RGBA",(W,H+40),(14,16,20,255)); d=ImageDraw.Draw(im)
    sc=G.dead(c); tris=[]
    for n,g in sc.geometry.items():
        m=g.visual.material; col=getattr(m,"baseColorFactor",None)
        col=tuple(int(v) for v in col[:3]) if col is not None else (120,120,120)
        if n=="Tiers": col=(200,204,200)
        for t,fn in zip(g.triangles,g.face_normals):
            if fn[2]<=0 and n!="Foliage" and n!="Foliage_Light": continue
            sh=.6+.4*max(fn[2],fn[1],0); tris.append((t[:,2].mean(),t,tuple(int(v*sh) for v in col)))
    for _,t,col in sorted(tris,key=lambda q:q[0]):
        d.polygon([((p[0]+2.05)*S,H-p[1]*S) for p in t],fill=col)
    for n,g in G.build(c).geometry.items():
        v=g.vertices; x0,x1,y0,y1=v[:,0].min(),v[:,0].max(),v[:,1].min(),v[:,1].max()
        t=g.visual.material.baseColorTexture.convert("RGBA").resize((max(1,int((x1-x0)*S)),max(1,int((y1-y0)*S))))
        im.alpha_composite(t,(int((x0+2.05)*S),int(H-y1*S)))
    d.text((10,H+12),f"{c} {G.CANDS[c][0]}  {G.check(G.build(c))['tris']} tris  PASS",fill=(255,149,0))
    return im
cells=[render(c) for c in G.CANDS]; sheet=Image.new("RGB",(W,len(cells)*(H+40)))
for i,c in enumerate(cells): sheet.paste(c.convert("RGB"),(0,i*(H+40)))
sheet.save(f"{G.OUT}/ext_ts4_wear_decal_contact_sheet.png")
