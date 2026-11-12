"""Rook r7e (2026-11-12): trim tt_dome_climber.glb Fall_Zone_Pad on its +X (east) side so the F3 playground
dome pad stops inside the E kick fence (X 139.45) instead of running under it into the curtain-wall Fin_Branch feet.
In place, same vertex/index counts: pad vertices with local x > PAD_X_MAX are clamped onto the chord, the new
chord side faces get +X normals, UVs are kept (box UVs, <=0.6 m stretch on the 3 cm edge). Every other byte of the GLB is untouched.
Idempotent. Re-run after assets/src/tennis_tower/dome_climber.py rebuilds the GLB (that script emits the full
Ø7 m pad). Placement pairs with playground.py: dome at X 136.50 -> pad edge at X 139.39 (post face 139.41)."""
import os, struct, numpy as np, pygltflib
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
GLB = os.path.join(ROOT, "godot/assets/models/tt_dome_climber.glb")
PAD_X_MAX = 2.89
def main():
    g = pygltflib.GLTF2().load(GLB); blob = bytearray(g.binary_blob())
    n = next(n for n in g.nodes if n.name == "Fall_Zone_Pad"); pr = g.meshes[n.mesh].primitives[0]
    def view(acc_i, k):
        a = g.accessors[acc_i]; bv = g.bufferViews[a.bufferView]; off = (bv.byteOffset or 0) + (a.byteOffset or 0)
        return a, off, np.frombuffer(bytes(blob[off:off + a.count * k * 4]), "<f4").reshape(a.count, k).copy()
    ap, op, P = view(pr.attributes.POSITION, 3); an, on, N = view(pr.attributes.NORMAL, 3)
    cut = P[:, 0] > PAD_X_MAX + 1e-6
    side = cut & (np.abs(N[:, 1]) < 0.5)
    if cut.any():
        P[cut, 0] = PAD_X_MAX; N[side] = (1.0, 0.0, 0.0)
    blob[op:op + P.nbytes] = P.astype("<f4").tobytes(); blob[on:on + N.nbytes] = N.astype("<f4").tobytes()
    ap.min = [float(v) for v in P.min(0)]; ap.max = [float(v) for v in P.max(0)]
    an.min = [float(v) for v in N.min(0)]; an.max = [float(v) for v in N.max(0)]
    g.set_binary_blob(bytes(blob)); g.save_binary(GLB)
    print("pad clamped", int(cut.sum()), "verts, side normals", int(side.sum()), "x range", ap.min[0], ap.max[0])
if __name__ == "__main__": main()
