"""Reusable PCB-art validator (Sloane). Geometry JSON schema:
{ "pads":[{"id","net","x","y","r"}], "vias":[{"net","x","y","r"}],
  "traces":[{"net","layer":"top|bot","w","pts":[[x,y],...]}],
  "pours":[{"net","layer","cell":1.0,"cells":[[cx,cy],...]}],   # cell centers
  "expected_open":[{"net","gap":[[x,y],[x,y]],"groups":[[padid..],[padid..]]}],
  "clearance":0.25 }
Checks: per-net connectivity (union-find over pads/vias/traces/pours), shorts,
unconnected pads, dangling trace ends (stubs), same-layer clearance between
different nets, bend angles (45-degree multiples, never acute)."""
import json, math, sys, itertools
def _pseg(p,a,b):
    ax,ay=a;bx,by=b;px,py=p;dx,dy=bx-ax,by-ay;L=dx*dx+dy*dy
    t=0 if L==0 else max(0,min(1,((px-ax)*dx+(py-ay)*dy)/L))
    return math.hypot(px-ax-t*dx,py-ay-t*dy)
def _ss(a,b,c,d):
    def ccw(p,q,r): return (r[1]-p[1])*(q[0]-p[0])-(q[1]-p[1])*(r[0]-p[0])
    if ccw(a,b,c)*ccw(a,b,d)<0 and ccw(c,d,a)*ccw(c,d,b)<0: return 0.0
    return min(_pseg(a,c,d),_pseg(b,c,d),_pseg(c,a,b),_pseg(d,a,b))
class UF:
    def __init__(s): s.p={}
    def f(s,x):
        s.p.setdefault(x,x)
        while s.p[x]!=x: s.p[x]=s.p[s.p[x]]; x=s.p[x]
        return x
    def u(s,a,b): s.p[s.f(a)]=s.f(b)
def validate(g):
    E=1e-6; cl=g.get("clearance",0.25); errs=[]; uf=UF()
    pads,vias,trs,pours=g["pads"],g.get("vias",[]),g["traces"],g.get("pours",[])
    exp={e["net"]:e for e in g.get("expected_open",[])}
    gaps=[tuple(p) for e in exp.values() for p in e["gap"]]
    nodes=[("P",i,p["net"],None,(p["x"],p["y"]),p["r"]) for i,p in enumerate(pads)]+[("V",i,v["net"],None,(v["x"],v["y"]),v["r"]) for i,v in enumerate(vias)]
    segs=[]
    for ti,t in enumerate(trs):
        uf.f(("T",ti))
        for a,b in zip(t["pts"],t["pts"][1:]): segs.append((ti,t["net"],t["layer"],t["w"],tuple(a),tuple(b)))
    # trace-to-node connectivity + stubs
    touched=set(); stubs=[]
    for ti,t in enumerate(trs):
        for end in (t["pts"][0],t["pts"][-1]):
            hit=False
            for k,i,net,_,c,r in nodes:
                if math.hypot(end[0]-c[0],end[1]-c[1])<=r+E:
                    if net!=t["net"]: errs.append(f"SHORT: trace {t['net']} ends on {net} {k}{i}")
                    uf.u(("T",ti),(k,i)); touched.add((k,i)); hit=True
            if not hit:
                if any(math.hypot(end[0]-q[0],end[1]-q[1])<E for q in gaps): continue
                stubs.append((t["net"],end))
    for net,end in stubs: errs.append(f"STUB/DEAD END: {net} at {end}")
    # same-layer trace-trace contact of same net (joins), other nets clearance
    for s1,s2 in itertools.combinations(segs,2):
        if s1[2]!=s2[2] or s1[0]==s2[0]: continue
        d=_ss(s1[4],s1[5],s2[4],s2[5])-s1[3]/2-s2[3]/2
        if s1[1]==s2[1]:
            if d<=0: uf.u(("T",s1[0]),("T",s2[0]))
        elif d<cl: errs.append(f"CLEARANCE: {s1[1]} vs {s2[1]} on {s1[2]} gap {d:.2f}")
    # trace vs foreign pad/via clearance (pads & vias are through-hole: both layers)
    for s in segs:
        for k,i,net,_,c,r in nodes:
            if net!=s[1] and _pseg(c,s[4],s[5])-r-s[3]/2<cl: errs.append(f"CLEARANCE: trace {s[1]} vs {k}{i} {net}")
    for (k1,i1,n1,_,c1,r1),(k2,i2,n2,_,c2,r2) in itertools.combinations(nodes,2):
        d=math.hypot(c1[0]-c2[0],c1[1]-c2[1])-r1-r2
        if n1!=n2 and d<cl: errs.append(f"CLEARANCE: {k1}{i1} {n1} vs {k2}{i2} {n2}")
        if n1==n2 and d<=0: uf.u((k1,i1),(k2,i2))
    # pours
    for pi,po in enumerate(pours):
        cs=set(map(tuple,po["cells"])); h=po.get("cell",1.0)/2; seen=set()
        for c in cs:
            if c in seen: continue
            comp=[c]; seen.add(c); st=[c]
            while st:
                x,y=st.pop()
                for n in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                    if n in cs and n not in seen: seen.add(n); comp.append(n); st.append(n)
            key=("O",pi,comp[0]); uf.f(key); attached=False
            cset=set(comp)
            for k,i,net,_,cc,r in nodes:
                if net==po["net"] and (round(cc[0]),round(cc[1])) in cset: uf.u(key,(k,i)); touched.add((k,i)); attached=True
            for s in segs:
                if s[1]==po["net"] and s[2]==po["layer"] and ((round(s[4][0]),round(s[4][1])) in cset): uf.u(key,("T",s[0])); attached=True
            if not attached: errs.append(f"FLOATING POUR island {po['net']} {po['layer']} at {comp[0]}")
        for c in cs:
            for s in segs:
                if s[2]==po["layer"] and s[1]!=po["net"] and _pseg(c,s[4],s[5])-h*math.sqrt(2)-s[3]/2<cl: errs.append(f"CLEARANCE: pour vs {s[1]}"); break
            for k,i,net,_,cc,r in nodes:
                if net!=po["net"] and math.hypot(c[0]-cc[0],c[1]-cc[1])-h*math.sqrt(2)-r<cl: errs.append(f"CLEARANCE: pour vs pad {net}"); break
    # angles
    bends=0
    for t in trs:
        p=t["pts"]
        for a,b,c in zip(p,p[1:],p[2:]):
            v1=(b[0]-a[0],b[1]-a[1]); v2=(c[0]-b[0],c[1]-b[1])
            ang=math.degrees(math.atan2(v1[0]*v2[1]-v1[1]*v2[0],v1[0]*v2[0]+v1[1]*v2[1]))
            if abs(ang)<E: continue
            bends+=1
            if abs(ang)>90+E: errs.append(f"ACUTE ANGLE: {t['net']} at {b} turn {ang:.0f}")
            elif abs(round(ang/45)*45-ang)>0.5: errs.append(f"NON-45 BEND: {t['net']} at {b} {ang:.1f}")
    for t in trs:
        for a,b in zip(t["pts"],t["pts"][1:]):
            ang=math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]))
            if abs(round(ang/45)*45-ang)>0.5: errs.append(f"OFF-AXIS SEGMENT: {t['net']} {a}->{b}")
    # unconnected pads
    for k,i,net,_,c,r in nodes:
        if k=="P" and (k,i) not in touched: errs.append(f"UNCONNECTED PAD: {pads[i]['id']} ({net})")
    # per-net connectivity
    nets={}
    for i,p in enumerate(pads): nets.setdefault(p["net"],[]).append(i)
    opens=[]
    for net,ids in nets.items():
        comps={}
        for i in ids: comps.setdefault(uf.f(("P",i)),[]).append(pads[i]["id"])
        groups=sorted(sorted(v) for v in comps.values())
        if net in exp:
            want=sorted(sorted(gq) for gq in exp[net]["groups"])
            if groups==want: opens.append(f"{net}: expected open between {groups[0]} and {groups[1]}")
            else: errs.append(f"EXPECTED-OPEN MISMATCH {net}: {groups}")
        elif len(groups)>1: errs.append(f"OPEN NET {net}: {groups}")
    # shorts via union-find
    roots={}
    for k,i,net,_,c,r in nodes: roots.setdefault(uf.f((k,i)),set()).add(net)
    for r,ns in roots.items():
        if len(ns)>1: errs.append(f"SHORT between {sorted(ns)}")
    errs=list(dict.fromkeys(errs))
    return {"ok":not errs,"errors":errs,"expected_opens":opens,"stats":{"nets":len(nets),"pads":len(pads),"vias":len(vias),"traces":len(trs),"segments":len(segs),"bends":bends,"pour_cells":sum(len(p["cells"]) for p in pours)}}
if __name__=="__main__":
    for fn in sys.argv[1:]:
        r=validate(json.load(open(fn))); print(fn,"PASS" if r["ok"] else "FAIL",r["stats"]); [print("  ",e) for e in r["errors"][:40]+r["expected_opens"]]
