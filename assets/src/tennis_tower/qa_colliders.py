"""Rook TTQA r1: add collision-only '<src>-colonly' mesh nodes to existing Tennis Tower GLBs without touching any
existing mesh / accessor / material / UV / normal. Tool-made nodes carry extras {"qa_collider": true} and are replaced
on re-run (idempotent). Godot loader (tennis_tower_loader.gd) turns '*-colonly' into hidden trimesh colliders."""
import numpy as np, pygltflib, trimesh
from pygltflib import GLTF2, Node, Mesh, Primitive, Accessor, BufferView
CT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}

def _acc(g, blob, i):
    a = g.accessors[i]; bv = g.bufferViews[a.bufferView]; n = NC[a.type]; dt = np.dtype(CT[a.componentType])
    off = (bv.byteOffset or 0) + (a.byteOffset or 0); stride = bv.byteStride or dt.itemsize * n
    if stride == dt.itemsize * n:
        arr = np.frombuffer(blob, dt, a.count * n, off).reshape(a.count, n)
    else:
        arr = np.stack([np.frombuffer(blob, dt, n, off + k * stride) for k in range(a.count)])
    return arr.copy()

def _local(nd):
    if nd.matrix: return np.array(nd.matrix, float).reshape(4, 4).T
    M = np.eye(4)
    if nd.scale: M = np.diag(list(nd.scale) + [1]) @ M
    if nd.rotation:
        x, y, z, w = nd.rotation; M = trimesh.transformations.quaternion_matrix([w, x, y, z]) @ M
    if nd.translation: M[:3, 3] += nd.translation
    return M

def _world(g, idx):
    par = {c: i for i, n in enumerate(g.nodes) for c in (n.children or [])}
    M = np.eye(4); i = idx
    while i is not None: M = _local(g.nodes[i]) @ M; i = par.get(i)
    return M

def _strip(g, blob, drop_names=()):
    """remove tool nodes (+ named nodes in drop_names) and their meshes; rebuild buffer compactly."""
    kill = {i for i, n in enumerate(g.nodes) if (n.extras or {}).get('qa_collider') or n.name in drop_names}
    if not kill: return blob
    kmesh = {g.nodes[i].mesh for i in kill if g.nodes[i].mesh is not None}
    used_m = {n.mesh for i, n in enumerate(g.nodes) if i not in kill and n.mesh is not None}
    kmesh -= used_m
    kacc = set()
    for mi in kmesh:
        for p in g.meshes[mi].primitives:
            kacc |= set(v for v in p.attributes.__dict__.values() if isinstance(v, int))
            if p.indices is not None: kacc.add(p.indices)
    # node remap
    nmap = {}; nodes = []
    for i, n in enumerate(g.nodes):
        if i in kill: continue
        nmap[i] = len(nodes); nodes.append(n)
    for n in nodes:
        if n.children: n.children = [nmap[c] for c in n.children if c in nmap]
    for s in g.scenes: s.nodes = [nmap[c] for c in s.nodes if c in nmap]
    g.nodes = nodes
    mmap = {}; meshes = []
    for i, m in enumerate(g.meshes):
        if i in kmesh: continue
        mmap[i] = len(meshes); meshes.append(m)
    g.meshes = meshes
    for n in g.nodes:
        if n.mesh is not None: n.mesh = mmap[n.mesh]
    amap = {}; accs = []
    for i, a in enumerate(g.accessors):
        if i in kacc: continue
        amap[i] = len(accs); accs.append(a)
    g.accessors = accs
    for m in g.meshes:
        for p in m.primitives:
            for k, v in list(p.attributes.__dict__.items()):
                if isinstance(v, int): setattr(p.attributes, k, amap[v])
            if p.indices is not None: p.indices = amap[p.indices]
    usedbv = {a.bufferView for a in g.accessors if a.bufferView is not None}
    for im in (g.images or []):
        if im.bufferView is not None: usedbv.add(im.bufferView)
    out = bytearray(); bmap = {}; bvs = []
    for i, bv in enumerate(g.bufferViews):
        if i not in usedbv: continue
        data = blob[(bv.byteOffset or 0):(bv.byteOffset or 0) + bv.byteLength]
        while len(out) % 4: out += b'\0'
        bv.byteOffset = len(out); out += data; bmap[i] = len(bvs); bvs.append(bv)
    g.bufferViews = bvs
    for a in g.accessors:
        if a.bufferView is not None: a.bufferView = bmap[a.bufferView]
    for im in (g.images or []):
        if im.bufferView is not None: im.bufferView = bmap[im.bufferView]
    while len(out) % 4: out += b'\0'
    g.buffers[0].byteLength = len(out)
    return bytes(out)

def _node_tris(g, blob, name):
    idx = [i for i, n in enumerate(g.nodes) if n.name == name]
    if not idx: raise KeyError(f'node {name!r} not found')
    V, F = [], []; off = 0
    for i in idx:
        nd = g.nodes[i]
        if nd.mesh is None: continue
        M = _world(g, i)
        for p in g.meshes[nd.mesh].primitives:
            if p.mode not in (None, 4): continue
            v = _acc(g, blob, p.attributes.POSITION).astype(float)
            f = _acc(g, blob, p.indices).reshape(-1, 3).astype(np.int64) if p.indices is not None else np.arange(len(v)).reshape(-1, 3)
            v = (np.c_[v, np.ones(len(v))] @ M.T)[:, :3]
            V.append(v); F.append(f + off); off += len(v)
    return np.vstack(V), np.vstack(F)

def _box(lo, hi):
    b = trimesh.creation.box(bounds=[lo, hi]); return b.vertices, b.faces

def _grow(lo, hi, t):
    lo, hi = np.array(lo, float), np.array(hi, float)
    if t > 0:
        c = (lo + hi) / 2; e = np.maximum(hi - lo, t); lo, hi = c - e / 2, c + e / 2
    return lo, hi

def _auto(V, F, min_thick, skip_small, mode):
    """mode: auto | box (one AABB) | tris (verbatim) | boxes (one AABB per connected part)"""
    out = []; nb = nt = 0
    if mode == 'box':
        lo, hi = _grow(V.min(0), V.max(0), min_thick); return [_box(lo, hi)], 1, 0
    if mode == 'tris': return [(V, F)], 0, 1
    m = trimesh.Trimesh(V, F, process=False); m.merge_vertices(digits_vertex=4)
    for c in m.split(only_watertight=False):
        lo, hi = c.bounds; e = hi - lo
        if e.max() < skip_small: continue
        vol = np.prod(np.maximum(e, 1e-9))
        try: hv = c.convex_hull.volume
        except Exception: hv = 0.0
        corner = np.all(np.min(np.abs(c.vertices[:, None, :] - np.stack([lo, hi])[None]), axis=1) < .002)
        if mode == 'boxes' or hv / vol >= .90 or (len(c.vertices) <= 24 and corner) or (np.min(e) < .03 and corner):
            lo2, hi2 = _grow(lo, hi, min_thick); out.append(_box(lo2, hi2)); nb += 1
        else:
            out.append((c.vertices, c.faces)); nt += 1
    return out, nb, nt

def _append_mesh(g, blob, name, parts, mat):
    V = []; F = []; off = 0
    for v, f in parts: V.append(np.asarray(v, float)); F.append(np.asarray(f) + off); off += len(v)
    V = np.vstack(V); F = np.vstack(F)
    tv = V[F].reshape(-1, 3).astype(np.float32)
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]); ln = np.linalg.norm(n, axis=1, keepdims=True)
    n = np.where(ln > 1e-12, n / np.maximum(ln, 1e-12), [0, 1, 0]); tn = np.repeat(n, 3, 0).astype(np.float32)
    uv = np.zeros((len(tv), 2), np.float32); ix = np.arange(len(tv), dtype=np.uint32)
    out = bytearray(blob)
    def add(arr, target, ctype, typ, mm=False):
        while len(out) % 4: out.extend(b'\0')
        o = len(out); out.extend(arr.tobytes())
        g.bufferViews.append(BufferView(buffer=0, byteOffset=o, byteLength=arr.nbytes, target=target))
        a = Accessor(bufferView=len(g.bufferViews) - 1, componentType=ctype, count=len(arr), type=typ)
        if mm: a.min = arr.min(0).tolist(); a.max = arr.max(0).tolist()
        g.accessors.append(a); return len(g.accessors) - 1
    ap = add(tv, 34962, 5126, 'VEC3', True); an = add(tn, 34962, 5126, 'VEC3'); au = add(uv, 34962, 5126, 'VEC2')
    ai = add(ix, 34963, 5125, 'SCALAR')
    prim = Primitive(attributes=pygltflib.Attributes(POSITION=ap, NORMAL=an, TEXCOORD_0=au), indices=ai, mode=4)
    if mat is not None: prim.material = mat
    g.meshes.append(Mesh(name=name, primitives=[prim]))
    g.nodes.append(Node(name=name, mesh=len(g.meshes) - 1, extras={'qa_collider': True}))
    g.scenes[g.scene or 0].nodes.append(len(g.nodes) - 1)
    while len(out) % 4: out.extend(b'\0')
    g.buffers[0].byteLength = len(out)
    return bytes(out), len(F)

def add_colliders(glb_path, spec, out_path=None, drop_nodes=()):
    g = GLTF2().load(glb_path); blob = g.binary_blob()
    blob = _strip(g, blob, tuple(drop_nodes))
    mat = 0 if g.materials else None
    st = dict(added=0, boxes=0, tri_components=0, collider_tris=0)
    for it in spec:
        mt, sk = it.get('min_thick', 0.0), it.get('skip_small', 0.0)
        if 'box' in it:
            lo, hi = _grow(*it['box'], mt); parts = [_box(lo, hi)]; nm = it['name']; nb, nt = 1, 0
        elif 'boxes' in it:
            parts = [_box(*_grow(*b, mt)) for b in it['boxes']]; nm = it['name']; nb, nt = len(parts), 0
        else:
            V, F = _node_tris(g, blob, it['src']); parts, nb, nt = _auto(V, F, mt, sk, it.get('mode', 'auto')); nm = it.get('name', it['src'])
        if not parts: continue
        blob, ntri = _append_mesh(g, blob, f'{nm}-colonly', parts, mat)
        st['added'] += 1; st['boxes'] += nb; st['tri_components'] += nt; st['collider_tris'] += ntri
    g.set_binary_blob(blob)
    g.save_binary(out_path or glb_path)
    return st

def count_colliders(glb_path):
    g = GLTF2().load(glb_path)
    c = [n.name for n in g.nodes if 'colonly' in (n.name or '').lower()]
    return dict(colonly_nodes=c, visual_nodes=[n.name for n in g.nodes if n.mesh is not None and n.name not in c])


# ---------------------------------------------------------------------------------------------------------------------
# Per-GLB spec (TTQA audit, Gage, main bfe716e). Each item turns a visible solid into a '-colonly' collider:
# auto = one AABB box per box-like part (walls, panes, partitions), exact triangles for anything else (openings stay open).
# Run after any generator re-export:  python3 assets/src/tennis_tower/qa_colliders.py [glb names...]
_SC = [{'src': 'Core_Walls'}, {'src': 'Front_Wall'}, {'src': 'Door_Jambs'}, {'src': 'Mid_Landing', 'mode': 'box'}]
_PANE = dict(mode='box', min_thick=.04)
SPEC = {
    # TTQA-003 lift: shaft walls on every side, door wall with its 2 openings, landing doors (L parked open beside the
    # opening with the car behind it, R closed), sills, car floor / walls / roof.
    'tt_lift_core': [{'src': s} for s in ('Shaft_Walls', 'Door_Wall', 'Door_Jambs', 'Landing_Doors', 'Sills', 'Lift_Car')],
    # TTQA-004 stair cores: walls, front wall with door opening, jambs, solid mid-landing block (treads/landings/
    # well guards already collide).
    'tt_stair_core_a': _SC, 'tt_stair_core_b': _SC, 'tt_stair_core_b_m': _SC, 'tt_stair_core_b_cap': _SC,
    # TTQA-005 court glass: one 40 mm box per pane (visual pane 12 mm), net = one box (replaces the 2 rail strips).
    'tt_court_partition': [dict(src='Court_Pane_Scissor', **_PANE)],
    'tt_court_net': [dict(src='Ball_Net_Scissor', **_PANE)],
    'tt_court_partition_door': [dict(src='Sidelight_Scissor', **_PANE), dict(src='Transom_Scissor', **_PANE)],
    'tt_court_partition_door_closed': [dict(src='Sidelight_Scissor', **_PANE), dict(src='Transom_Scissor', **_PANE)],
    # TTQA-006 restrooms: wet wall, partitions, pilasters, static closed stall doors, WCs.
    'tt_restroom': [{'src': s} for s in ('Wet_Wall', 'Partitions', 'Pilasters', 'Stall_Doors', 'WC_VacUnit')] + [{'src': 'WC', 'mode': 'boxes'}],
    'tt_restroom_6': [{'src': s} for s in ('Wet_Wall', 'Partitions', 'Pilasters', 'Stall_Doors', 'WC_VacUnit')] + [{'src': 'WC', 'mode': 'boxes'}],
}
DROP = {'tt_court_net': ['Net_Rails-colonly'], 'tt_restroom_6': ['Stalls-colonly']}

if __name__ == '__main__':
    import sys, os
    models = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../godot/assets/models')
    for nm in (sys.argv[1:] or SPEC):
        print(nm, add_colliders(os.path.join(models, nm + '.glb'), SPEC[nm], drop_nodes=DROP.get(nm, ())))
