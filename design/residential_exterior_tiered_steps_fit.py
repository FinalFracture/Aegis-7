# Tiered Steps planter fit check against the approved exterior v1.2 geometry (Vance, Oct 29 2026). Design QC only; no PNG.
# Rook's glb: godot/assets/models/hydro_planter_tiered_exterior.glb = 4.0 W x 0.70 H x 0.41 D (TS-4). TS-2 = 2.0 m cut-down variant (same troughs).
# Re-runs every exterior v1.2 QC check with the masking planters + hydro beds + W sidewalk planters swapped for Tiered Steps.
import math
L=open("residential_exterior_plan_v1.py").read().split("\n")
src="\n".join(L[:89])   # geometry + QC + assert, stops before plotting
D=0.41; GAP=0.4
S_W=[(-13.8,4),(-9.4,4),(-5.0,2)]                       # S wall west run -13.8..-3.0 (same extent as v1.2)
S_E=[(3.0,2),(5.4,4),(9.8,4)]                           # S wall east run 3.0..13.8
N_W=[(-13.8,4),(-9.6,4),(-5.4,4)]                       # N wall west run -13.8..-1.4 (0.2 gaps)
N_E=[(8.0,4),(12.0,2)]                                  # N wall east run 8.0..14.0 (butted, reads as one 6 m bed)
mask="\n".join([f"for x0,w in {S_W+S_E}: O.append(('planter S TS-'+str(w),x0,x0+w,-9.1-{D},-9.1,False))",
                f"for x0,w in {N_W+N_E}: O.append(('planter N TS-'+str(w),x0,x0+w,9.1,9.1+{D},False))"])
src=src.replace(L[26],mask).replace(L[27],"")
# W sidewalk hydro planters: one TS-4 each, length along Z, back (high tier) to the Spin St W kerb at X -16.8
src=src.replace(L[30],f"for z0 in (-7,-2,3): O.append(('hydro planter W TS-4',-16.8,-16.8+{D},z0,z0+4,False))")
# hydro co-op beds: back-to-back TS pair (2 x 0.41 + 0.08 spine = 0.9) x (TS-4 + TS-4 + TS-2 = 10.0 m), same footprint as v1.2
src=src.replace("if n.startswith(\"planter\") or n==\"hydro planter W\"","if n.startswith(\"planter\") or n.startswith(\"hydro planter W\")")
exec(src)
X=[]
mk=[o for o in O if o[0].startswith("planter")]
X.append(("planter height masks 0.22 m plinth (0.70 m)",[] if 0.70>=0.22 else ["low"]))
for wall,zs in (("S",-9),("N",9)):
    runs=sorted((o[1],o[2]) for o in mk if o[0].startswith("planter "+wall))
    cov=sum(b-a for a,b in runs); X.append((f"{wall} wall plinth coverage {cov:.1f} m of 28 m",[]))
ramps=[o for o in O if o[0].startswith("ramp")]
cl=min(min(abs(p[1]-r[2]),abs(r[1]-p[2])) for p in mk for r in ramps if (p[3]<0)==(r[3]<0))
X.append((f"planter clearance to ramps {cl:.2f} m (>=0.3)",[] if cl>=0.3 else [cl]))
beds=sorted(o[3] for o in O if o[0]=="hydro bed"); ais=[round(beds[i+1]-(beds[i]+0.9),2) for i in range(len(beds)-1)]
X.append((f"hydro aisles {ais} m (>=1.1)",[a for a in ais if a<1.1-1e-9]))
X.append(("hydro bed = 2 x 0.41 + 0.08 spine fits 0.9",[] if 2*D+0.08<=0.9+1e-9 else ["deep"]))
X.append(("hydro bed length TS-4+TS-4+TS-2 = 10.0 m fits X -13..-3",[] if 4+4+2<=10 else ["long"]))
sag=4.0**2/(8*185.5); X.append((f"curvature sagitta over 4 m along Z {sag*1000:.1f} mm (feet take-up 25 mm)",[] if sag<0.025 else [sag]))
wsw=min(-14-(-16.8+D),99); X.append((f"W sidewalk clear width beside TS planters {wsw:.2f} m (>=0.9)",[] if wsw>=0.9 else [wsw]))
for q in X: print("FIT:",q)
assert not [k for k,v in X if v], "fit failed"
n4=sum(w==4 for _,w in S_W+S_E+N_W+N_E); n2=sum(w==2 for _,w in S_W+S_E+N_W+N_E)
print(f"masking: {n4} x TS-4 + {n2} x TS-2; hydro beds: 3 x (4 TS-4 + 2 TS-2) = 12 TS-4 + 6 TS-2; W sidewalk: 3 TS-4")
