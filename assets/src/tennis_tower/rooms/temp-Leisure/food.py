"""F1-FOOD (X 44..102, Z 64..79). Rev 3.2 s3 room-local vendors (spec X30..54 stalls land in R1-NW; relocated inside F1-FOOD).
Stall = 6 x 5 m incl. kitchen, local front +Z (place yaw 180 on the N facade).
Facade inner line (tt_facade_bay fins) is Z78.38, so N stalls take Z73.3..78.3."""
from lz_lib import *
ml._m('lz_moss_dk', 'TT_MossDark', (.14, .32, .16), 0, .85, a=1.0)
ml._m('lz_moss_md', 'TT_MossMid', (.20, .42, .18), 0, .85, a=1.0)
MDK, MMD = 'lz_moss_dk', 'lz_moss_md'

def seated_mound(c, r, seed=0):
    """moss_mound with bottom exactly at c[1]."""
    raw = moss_mound((0, 0, 0), r, seed)
    lift = -float(raw.bounds[0][1]) + c[1]
    return moss_mound((c[0], lift, c[2]), r, seed)

def seated_clump(c, r, seed=0, sub=0):
    raw = clump((0, 0, 0), r, seed, sub)
    lift = -float(raw.bounds[0][1]) + c[1]
    return clump((c[0], lift, c[2]), r, seed, sub)

def finish_moss_scissor(path):
    """MASK 0.5, baseColor alpha 1.0, lancet-leaf alpha texture for TT_MossDark / TT_MossMid."""
    import io as _io
    import pygltflib as pg
    from PIL import Image, ImageDraw
    n = 64
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    poly = [(0.5*n, 0.02*n), (0.96*n, 0.35*n), (0.5*n, 0.98*n), (0.04*n, 0.35*n)]
    dr.polygon(poly, fill=(40, 90, 45, 255))
    b = _io.BytesIO(); im.save(b, 'PNG'); data = b.getvalue()
    g = pg.GLTF2().load(path); blob = bytearray(g.binary_blob()); hit = False
    if not g.samplers:
        g.samplers.append(pg.Sampler(magFilter=9729, minFilter=9987, wrapS=33071, wrapT=33071))
    for m in g.materials:
        if m.name not in ('TT_MossDark', 'TT_MossMid'):
            continue
        hit = True
        while len(blob) % 4: blob.append(0)
        g.bufferViews.append(pg.BufferView(buffer=0, byteOffset=len(blob), byteLength=len(data)))
        blob.extend(data)
        g.images.append(pg.Image(bufferView=len(g.bufferViews)-1, mimeType='image/png'))
        g.textures.append(pg.Texture(source=len(g.images)-1, sampler=0))
        m.alphaMode = 'MASK'
        m.alphaCutoff = .5
        m.doubleSided = True
        if m.pbrMetallicRoughness is None:
            m.pbrMetallicRoughness = pg.MaterialPBRMetallicRoughness()
        bc = m.pbrMetallicRoughness.baseColorFactor or [1, 1, 1, 1]
        m.pbrMetallicRoughness.baseColorFactor = [bc[0], bc[1], bc[2], 1.0]
        m.pbrMetallicRoughness.baseColorTexture = pg.TextureInfo(index=len(g.textures)-1)
    if hit:
        while len(blob) % 4: blob.append(0)
        g.buffers[0].byteLength = len(blob)
        g.set_binary_blob(bytes(blob))
        g.save_binary(path)

def paint_menu(it, x0, x1, y0, y1, z0, z1, variant=0):
    """Opaque menu board art: slate plate + cyan rows + amber price ticks + ball/leaf accent."""
    it.b('Menu_Plate', SL, x0, x1, y0, y1, z0, z1)
    zf = max(z0, z1) + 0.005
    rows = 4
    for i in range(rows):
        yy = y0 + 0.1 + i * (abs(y1 - y0) - 0.28) / (rows - 0.5)
        it.b('Menu_Row', CY if i % 2 == 0 else WH, x0 + 0.1, x1 - 0.28, yy, yy + 0.04, zf, zf + 0.003)
        it.b('Menu_Price', AM, x1 - 0.24, x1 - 0.1, yy, yy + 0.04, zf, zf + 0.003)
    it.b('Menu_Header', BA, x0 + 0.1, x1 - 0.1, y1 - 0.1, y1 - 0.06, zf + 0.002, zf + 0.005)
    cx = (x0 + x1) / 2
    if variant % 2 == 0:
        it.a('Menu_Ball', BA, cap((cx, y0 + 0.08, zf + 0.014), 0.035, 0.01, 10, 'z'))
    else:
        it.a('Menu_Leaf', LF2, zwall_leaf((cx, y0 + 0.1, zf + 0.01), 0.15, 0.22, 0.08))

def stall():
    it = It(); w, d = 6.0, 5.0; x0, x1, z0, z1 = -3, 3, -2.5, 2.5
    it.b('Kitchen_Floor', RU, x0 + .14, x1 - .14, 0, .02, z0 + .16, 1.3, col=False)
    it.b('Back_Wall', G, x0, x1, 0, 3.4, z0, z0 + .15, col=True)
    for xa, xb in ((x0, x0 + .14), (x1 - .14, x1)): it.b('Side_Walls', SL, xa, xb, 0, 3.4, z0 + .152, 1.3, col=True)
    for y in (.9, 1.8, 2.7): it.b('Back_Reveal', CY, x0 + .2, x1 - .2, y, y + .03, z0 + .146, z0 + .156)
    # cook line + hood
    it.b('Cook_Line', ST, x0 + .2, x1 - .2, .016, .9, z0 + .2, z0 + .85, col=True)
    for k in range(4): it.b('Cook_Hobs', G, -2.3 + 1.2*k, -1.5 + 1.2*k, .896, .93, z0 + .3, z0 + .75)
    _hv = np.array([(2.64, 2.1, 0), (-2.64, 2.1, 0), (-2.64, 2.1, -.72), (2.64, 2.1, -.72), (2.75, 2.6, 0), (-2.75, 2.6, 0), (-2.75, 2.6, -.9), (2.75, 2.6, -.9)], float)
    _hf = np.array([[0,4,5],[0,5,1],[1,5,6],[1,6,2],[2,6,7],[2,7,3],[3,7,4],[3,4,0],[0,1,2],[0,2,3],[4,7,6],[4,6,5]], int)
    _hood = trimesh.Trimesh(_hv, _hf, process=False)
    _hood.metadata['uv'] = np.c_[(_hv[:, 0] / 5.5) + .5, np.clip(_hv[:, 2] / -0.9, 0, 1)]
    it.a('Hood', ST, xf(_hood, t=(0, 0, z0 + .152 + .9)))
    it.b('Hood_LED', AM, -2.6, 2.6, 2.06, 2.104, z0 + .3, z0 + .34)
    # service counter (front) + 0.9 m accessible section at 0.86 m (left end)
    it.bv('Counter_Body', WH, -1.55, 2.86, .016, 1.0, 1.32, 1.9, col=True)
    it.bv('Counter_Top', ST, -1.56, 2.9, .996, 1.05, 1.3, 1.98)
    it.bv('Counter_Acc_Body', WH, -2.62, -1.6, .016, .81, 1.32, 1.9, col=True)
    it.bv('Counter_Acc_Top', ST, -2.66, -1.58, .806, .86, 1.3, 1.98)
    it.b('Acc_Marker', VIO, -2.3, -2.0, .4, .5, 1.896, 1.904)
    it.b('Counter_Kick', SL, -2.6, 2.84, .016, .16, 1.904, 1.92)
    for x in np.arange(-1.3, 2.7, .55): it.b('Counter_Flutes', G, x, x + .06, .2, .95, 1.896, 1.912)
    it.b('Counter_CourtLine', BA, -1.5, 2.84, .6, .63, 1.908, 1.918)
    it.b('Sneeze_Scissor', SCR, -1.4, 1.6, 1.046, 1.5, 1.5, 1.516)
    for x in (-1.42, 1.62): it.a('Sneeze_Posts', ST, tube((x, 1.046, 1.508), (x, 1.52, 1.508), .012, 6))
    for x in (-2.2, 1.9):
        it.b('POS', SL, x - .15, x + .15, 1.046 if x > 0 else .856, 1.3 if x > 0 else 1.1, 1.4, 1.6)
        ys0, ys1 = (1.12, 1.27) if x > 0 else (.93, 1.07)
        it.b('POS_Screen', SL, x - .12, x + .12, ys0, ys1, 1.598, 1.606)
        it.b('POS_Bar', CY, x - .09, x + .03, ys0 + .03, ys0 + .055, 1.608, 1.612)
        it.b('POS_Bar', CY, x - .09, x + .09, ys0 + .07, ys0 + .095, 1.608, 1.612)
    it.b('Tray_Rail', ALY, -1.5, 2.86, .8, .84, 1.98, 2.2)
    for x in (-1.0, .5, 2.0): it.b('Tray_Brackets', ST, x, x + .04, .7, .804, 1.92, 2.18)
    # canopy + menu boards (opaque emissive) + leaf crest + ball finials
    it.b('Canopy', SL, x0, x1, 3.0, 3.4, 1.3, 2.5, col=True)
    it.b('Canopy_Soffit_LED', CY, x0 + .2, x1 - .2, 2.996, 3.004, 1.5, 2.3)
    for k in range(3):
        xc = -2 + 2*k; it.b('Menu_Frames', G, xc - .9, xc + .9, 3.45, 4.25, 2.0, 2.1)
        paint_menu(it, xc - .84, xc + .84, 3.5, 4.2, 2.096, 2.104, k)
    for x in (-2.0, 0, 2.0): it.a('Menu_Hangers', ST, tube((x, 3.396, 2.05), (x, 3.454, 2.05), .02, 6))
    for k in range(9): it.a('Canopy_Leaves', LF2, zwall_leaf((-2.8 + .7*k, 3.05, 2.5), (k - 4)*.12, .55, .2, face=1))
    for x in (x0 + .15, x1 - .15): it.a('Canopy_Balls', BA, node((x, 3.5, 2.3), .09, 1))
    # moss at front corners, inset so the SW stall at (54.0, 67.2) clears the 2x2 TC-N
    # Pedestal_Concrete at (57.5, 70.5) by >= 50 mm; keep stall X/Z placement
    for i, x in enumerate((x0 + .72, x1 - .72)):
        it.a('Moss_Base', MDK if i == 0 else MMD, seated_mound((x, 0, 2.05), .10, int(abs(x)*7)))
        for k in range(3):
            lx = x + (-.05 + .05 * k); lz = 2.11
            it.a('Moss_Leaves', MMD if k % 2 == 0 else MDK,
                 leaf((lx, .22, lz), .16 + .02 * k, .07, yaw=(-.12 + .12 * k), pitch=.28, t=.01))
    it.col(x0, x1, 0, 3.4, z0, z0 + .15)
    out = emit('tt_food_stall', it, '6x5 m stall incl. kitchen; front +Z; accessible 0.9 m counter at 0.86 m')
    for nm, _ in out:
        finish_moss_scissor(str(GM / f'{nm}.glb'))
    return out

def table4(acc=False):
    it = It()
    it.b('Base', SL, -.3, .3, 0, .04, -.3, .3)
    it.a('Pedestal', G, tube((0, .036, 0), (0, .72, 0), .05, 10)); it.col(-.06, .06, 0, .72, -.06, .06)
    it.b('Top', WH, -.4, .4, .716, .75, -.4, .4, col=True)
    it.a('Top_Ball', BA, cap((0, .751, 0), .1, .006, 16, 'y'))
    for k in range(4):
        m = xf(leaf((0, 0, 0), .26, .1, t=.01), R=trimesh.transformations.rotation_matrix(-math.pi/2, [1, 0, 0])); m.apply_translation((0, 0, -.12))
        it.a('Top_Leaf', LF2, xf(xf(m, R=trimesh.transformations.rotation_matrix(k*math.pi/2 + .4, [0, 1, 0])), t=(0, .751, 0)))
    for k, (dx, dz) in enumerate(((0, .62), (0, -.62), (.62, 0), (-.62, 0))):
        if acc and k == 0: continue
        R = trimesh.transformations.rotation_matrix(math.atan2(dx, dz), [0, 1, 0])
        c = It()
        for sx in (-.19, .19):
            for sz in (-.19, .19): c.a('Chair_Legs', ALY, tube((sx, 0, sz), (sx*.9, .44, sz*.9), .014, 6))
        c.b('Chair_Seat', FA, -.22, .22, .436, .48, -.22, .22)
        c.b('Chair_Back', WH, -.21, .21, .5, .86, .22, .25)
        c.a('Chair_BackPost', ALY, tube((0, .476, .235), (0, .504, .235), .012, 6))
        for n, m, mesh in c: it.a(n, m, xf(mesh, R=R, t=(dx, 0, dz)))
        cb = xf(box(-.22, .22, 0, .48, -.22, .22), R=R, t=(dx, 0, dz)); it.cols.append(cb)
    if acc: it.a('Acc_Floor_Marker', VIO, box(-.35, .35, 0, .008, .5, 1.2))
    return emit('tt_food_table4' + ('_acc' if acc else ''), it, '4-top (accessible: 3 chairs + wheelchair place, +Z side)')

def bin_station():
    it = It()
    it.b('Bin_Plinth', G, -.6, .6, 0, .08, -.25, .25, col=True)
    for k, mk in enumerate((GRN, CY, AM)):
        x = -.39 + .39*k
        it.b('Bin_Bodies', WH, x - .18, x + .18, .076, 1.0, -.22, .22, col=True)
        it.b('Bin_Mouths', SL, x - .12, x + .12, .82, .9, .218, .226)
        it.b('Bin_Stream_LED', mk, x - .14, x + .14, .7, .73, .218, .224)
    it.b('Bin_Hood', SL, -.6, .6, .996, 1.06, -.25, .26)
    it.a('Bin_Leaf', LF2, zwall_leaf((-.39, .4, .22), .3, .25, .12)); it.a('Bin_Ball', BA, cap((.39, .45, .222), .08, .01, 12, 'z'))
    return emit('tt_food_bin', it, '3-stream waste station; waste route to the X54..57 service door')

def service_door():
    """inside face of the N facade at X54..57 (needs a facade door variant from the shared kit owner)."""
    it = It()
    it.b('Door_Frame', G, -1.5, 1.5, 0, 3.0, -.1, .0, col=True)
    for xa, xb in ((-1.4, -.002), (.002, 1.4)):
        it.b('Door_Leaves', SGM, xa, xb, .02, 2.7, .0 - D, .05, col=True)
        it.b('Door_Kick', ST, xa + .05, xb - .05, .08, .4, .048, .056)
        it.b('Door_Hazard', AM, xa + .05, xb - .05, 2.4, 2.45, .048, .056)
    it.b('Door_Sign', CY, -.4, .4, 2.75, 2.9, -.004, .006)
    it.b('Waste_Track', SL, -1.3, 1.3, 0, .01, .06, 1.5)
    return emit('tt_food_service_door', it, 'waste door X54..57 on the N facade inner face (Rev 3.2 s3)')

def tree_moss():
    it = It()
    # Pedestal_Concrete is a 2 x 2 m square (|x|,|z| <= 1.0, y 0..0.6), not an r=1 circle.
    # Keep a 50 mm gap (outside |x|<=1.05 and |z|<=1.05). N queues at Z 72.31 -> local z <= 1.81; cap ~1.65.
    rng = np.random.default_rng(7)
    FACE, RM = 1.22, 0.10
    for side, (sx, sz) in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1))):
        for i, t in enumerate((-0.62, 0.0, 0.62)):
            x = sx * FACE + sz * t
            z = sz * FACE + sx * t
            it.a('Moss_Mound', MDK if (side + i) % 2 == 0 else MMD, seated_mound((x, 0, z), RM, 10 + side * 3 + i))
    for i, (x, z) in enumerate(((1.18, 1.18), (1.18, -1.18), (-1.18, 1.18), (-1.18, -1.18))):
        it.a('Moss_Mound', MMD if i % 2 == 0 else MDK, seated_mound((x, 0, z), 0.09, 40 + i))

    def add_leaf(x, z, h0, L, W, pitch, yaw_off, mk):
        yaw = math.atan2(x, z) + yaw_off  # +pitch leans outward
        it.a('Moss_Leaves', mk, leaf((x, h0, z), L, W, yaw=yaw, pitch=pitch, t=.01))

    for side, (sx, sz) in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1))):
        for i in range(7):
            t = -0.85 + i * 0.283
            j = rng.uniform(-0.02, 0.02)
            x = sx * 1.36 + sz * (t + j)
            z = sz * 1.36 + sx * (t + j)
            h0 = rng.uniform(0.22, 0.28)
            L = rng.uniform(0.30, 0.46)
            W = rng.uniform(0.10, 0.15)
            pitch = rng.uniform(0.22, 0.42)
            mk = MDK if (side + i) % 2 == 0 else MMD
            add_leaf(x, z, h0, L, W, pitch, rng.uniform(-0.18, 0.18), mk)
    for side, (sx, sz) in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1))):
        for i in range(5):
            t = -0.70 + i * 0.35
            j = rng.uniform(-0.03, 0.03)
            x = sx * 1.46 + sz * (t + j)
            z = sz * 1.46 + sx * (t + j)
            h0 = rng.uniform(0.16, 0.22)
            L = rng.uniform(0.26, 0.38)
            W = rng.uniform(0.09, 0.14)
            pitch = rng.uniform(0.30, 0.55)
            mk = MMD if (side + i) % 2 == 0 else MDK
            add_leaf(x, z, h0, L, W, pitch, rng.uniform(-0.25, 0.25), mk)
    for i, (x, z) in enumerate(((1.30, 1.30), (1.30, -1.30), (-1.30, 1.30), (-1.30, -1.30))):
        for k in range(3):
            a = rng.uniform(-0.08, 0.08)
            b = rng.uniform(-0.08, 0.08)
            h0 = rng.uniform(0.20, 0.26)
            L = rng.uniform(0.28, 0.42)
            W = rng.uniform(0.10, 0.14)
            pitch = rng.uniform(0.22, 0.42)
            mk = MDK if (i + k) % 2 == 0 else MMD
            add_leaf(x + a, z + b, h0, L, W, pitch, rng.uniform(-0.20, 0.20), mk)
    for i, (x, z) in enumerate(((0.0, 1.44), (0.0, -1.44), (1.44, 0.0), (-1.44, 0.0),
                                (0.72, 1.42), (-0.72, 1.42), (0.72, -1.42), (-0.72, -1.42))):
        it.a('River_Stones', SL, seated_clump((x, 0, z), 0.055, 60 + i))
    out = emit('tt_food_tree_moss', it, 'square-ring dark/mid moss + scissor leaves around a TC-N tree; 2x2 ped +50mm clear; z<=1.65')
    for nm, _ in out:
        finish_moss_scissor(str(GM / f'{nm}.glb'))
    return out

TREES_N = [(57.5, 70.5), (65.5, 70.5), (84.5, 70.5), (101.5, 70.5)]
EXCL = [(58, 64, 65.8, 76.4), (86, 92, 65.8, 76.4), (66.5, 70.5, 64, 68), (71, 76.5, 64, 69.5), (50, 53, 64, 66.2), (90, 93, 64, 66.2),
        (46.5, 52.5, 72.4, 78.3), (78.0, 84.0, 72.4, 78.3), (95.5, 101.5, 72.4, 78.3),  # N-facade stalls + 0.9 m queue to -Z
        (44.8, 50.8, 64.55, 70.65), (51.0, 57.0, 64.55, 70.65), (94.0, 100.0, 64.55, 70.65)]  # interior stalls + 0.9 m queue to +Z
# OLD STALLS were [(51,75.8,180),(69,75.8,180),(75,75.8,180),(81,75.8,180),(98.8,75.8,180),(47.2,66.8,0)]
# NEW: 3 N-facade (door X54..57 + entrance X68..76 clear) + 3 interior yaw0 clear of R1-NW wall X44.15 and stand-back Z64.3
STALLS = [(49.5, 75.8, 180), (81.0, 75.8, 180), (98.5, 75.8, 180), (47.8, 67.2, 0), (54.0, 67.2, 0), (97.0, 67.2, 0)]
def seats(H=.84, RT=.9, P=2.58):
    """table sets (half-size H) on a P pitch = 0.9 m clear routes; 1.5 m queue/waste route Z71.8..73.3 kept clear."""
    ex = EXCL + [(101.85, 102.2, 64, 79), (43.85, 44.5, 64, 79), (68.0, 76.0, 73.0, 79.0), (54.0, 57.0, 73.0, 79.0)]
    out = []
    for x in np.arange(44.15 + H + .3, 101.85 - H, P):
        for z in np.arange(64.3 + H + .3, 71.8 - H + 1e-6, P):
            if any(a - H - RT < x < b + H + RT and c - H - RT < z < d + H + RT for a, b, c, d in ex): continue
            if any(math.hypot(x - tx, z - tz) < 1.0 + H + RT for tx, tz in TREES_N): continue
            out.append((float(x), float(z)))
    return out
def build(PL):
    st = stall(); t4 = table4(); ta = table4(True); bn = bin_station(); sd = service_door(); tm = tree_moss()
    for x, z, yaw in STALLS: place(PL, st, x, 0, z, yaw)
    pos = seats(); nacc = math.ceil(.05*len(pos)*4); step = len(pos)/nacc; accs = {int(k*step) for k in range(nacc)}
    for i, (x, z) in enumerate(pos): place(PL, ta if i in accs else t4, x, 0, z, 0)
    # bins stay inside F1-FOOD, clear of ST+N2 / tables / stall queues / N entrance (99cdd0c stall bounds unchanged)
    for x, z in ((53.2, 72.6), (76.2, 72.6), (93.75, 71.0), (86.6, 64.9)): place(PL, bn, x, 0, z, 0)
    place(PL, sd, 55.5, 0, 78.3, 180)
    for x, z in TREES_N[1:3]: place(PL, tm, x, 0, z, 0)
    acc = sum(1 for p in PL if p['asset'] == 'tt_food_table4_acc'); tot = sum(1 for p in PL if p['asset'].startswith('tt_food_table4'))
    return dict(tables=tot, accessible_tables=acc, places=tot*4, chairs=tot*4 - acc)
if __name__ == '__main__':
    PL = []; print(build(PL))
    for r in REP:
        if not r['passed']: print(r['asset'], r['bad'], r['coplanar'], r['open'], r['pivot'])
