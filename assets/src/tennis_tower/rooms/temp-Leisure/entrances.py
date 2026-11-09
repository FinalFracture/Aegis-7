"""Room-local alpha-scissor copies of the shared N/E secondary entrances (approved by Rook; originals untouched).
BLEND 'Glass' -> TT_GlassScissor (MASK + dither), nodes Glass_* -> *_Scissor. Colliders already present in the source."""
import shutil
from lz_lib import *
import pygltflib as pg
def force_scissor_alpha(path):
    # Dither texel * baseColorFactor.a must clear MASK cutoff 0.5; source Glass alpha 0.251 discards all glazing.
    g = pg.GLTF2().load(path)
    for m in g.materials:
        if m.name != 'TT_GlassScissor' and m.alphaMode != 'MASK': continue
        pbr = m.pbrMetallicRoughness
        if not pbr: continue
        rgba = list(pbr.baseColorFactor or [1.0, 1.0, 1.0, 1.0])
        if len(rgba) < 4: rgba += [1.0] * (4 - len(rgba))
        rgba[3] = 1.0
        pbr.baseColorFactor = rgba[:4]
        m.alphaMode = 'MASK'; m.alphaCutoff = 0.5
    g.save_binary(path)
def scissor_copy(src, dst):
    s, d = GM / f'{src}.glb', GM / f'{dst}.glb'; shutil.copyfile(s, d)
    g = pg.GLTF2().load(str(d))
    for m in g.materials:
        if m.name == 'Glass': m.name = 'TT_GlassScissor'; m.alphaMode = 'OPAQUE'; m.pbrMetallicRoughness.baseColorTexture = None
    for n in g.nodes:
        if n.name and 'glass' in n.name.lower(): n.name = n.name.replace('Glass_', '') + '_Scissor'
    for me in g.meshes:
        if me.name and 'glass' in me.name.lower(): me.name = me.name.replace('Glass_', '') + '_Scissor'
    g.save_binary(str(d)); finish_scissor(str(d)); force_scissor_alpha(str(d))
    ok = vm.validate_file(str(d), check_tri_range=(1, 5999), require_textures=False, require_blend_glass=False)
    tris = int(sum(len(x.faces) for x in trimesh.load(str(d)).geometry.values()))
    REP.append(dict(asset=dst, tris=tris, passed=bool(ok), validate=bool(ok), note=f'scissor copy of {src}', world_offset=[0, 0, 0]))
    return [(dst, [0, 0, 0])]
def build(PL):
    n = scissor_copy('tt_secondary_entrance_n', 'tt_food_entrance_n_scissor')
    e = scissor_copy('tt_secondary_entrance_e', 'tt_arc_entrance_e_scissor')
    place(PL, n, 72, 0, 79 + .98, 0, 'facade'); place(PL, e, 140 + .98, 0, 37.5, 90, 'facade')
    return dict(replaces={'tt_secondary_entrance_n': 'tt_food_entrance_n_scissor', 'tt_secondary_entrance_e': 'tt_arc_entrance_e_scissor'})
if __name__ == '__main__':
    PL = []; print(build(PL), REP)
