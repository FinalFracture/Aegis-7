extends RefCounted
## Bends flat preface geometry onto the Hab-7 drum.
## Flat z is arc length: s = z - z0, th = s / R.
## bend(p) = (p.x, axis_y - (R - h) cos th, z0 + (R - h) sin th), h = p.y - deck_top.
## Local up after the bend is Basis(Vector3.RIGHT, -th) * UP = (0, cos th, -sin th),
## which points at the axis. A +th rotation about +X would lean the other way.

const META_TREE := "deck_bent_tree"
const META_SELF := "deck_bent_self"
const RIGID_Z := 2.0
const EDGE_Z := 1.5
# Wall props carry one AABB box and an AnimationPlayer. Vertex-warping that box
# fills the chord under the feet and the placement rays sample a flat min-y plane.
# 2.6 m on R=200 sags ~4 mm at the ends, inside the 5 mm floor epsilon.
const PROP_RIGID_Z := 2.6

const SKIP_NAMES := {
	"CylinderHab7_DrumAxisPivot": true,
	"CylinderHab7_FullScale_Mesh": true,
	"HabDrumSpinGravityRing": true,
	"StarfieldOuterCylinder": true,
	"CylinderSpinGravityTestRing": true,
}

var axis_y: float = 0.0
var axis_z: float = 0.0
var radius: float = 200.0
var deck_top: float = 0.12
var meshes: int = 0
var verts: int = 0
var shapes: int = 0
var _spans: Dictionary = {}
var _excluded: Dictionary = {}


func setup(p_axis_y: float, p_axis_z: float, p_radius: float, p_deck_top: float) -> void:
	axis_y = p_axis_y
	axis_z = p_axis_z
	radius = p_radius
	deck_top = p_deck_top


func bend_basis(th: float) -> Basis:
	return Basis(Vector3.RIGHT, -th)


func bend_point(p: Vector3) -> Vector3:
	var s: float = p.z - axis_z
	var h: float = p.y - deck_top
	var th: float = s / radius
	var radial: float = radius - h
	return Vector3(p.x, axis_y - radial * cos(th), axis_z + radial * sin(th))


func self_check() -> bool:
	var nadir: Vector3 = bend_point(Vector3(0.0, deck_top, axis_z))
	var nadir_err: float = nadir.distance_to(Vector3(0.0, deck_top, axis_z))
	var th: float = 0.5
	var up: Vector3 = bend_basis(th) * Vector3.UP
	var up_err: float = up.distance_to(Vector3(0.0, cos(th), -sin(th)))
	var q: Vector3 = bend_point(Vector3(2.0, deck_top, axis_z + 10.0))
	var rho: float = Vector2(q.y - axis_y, q.z - axis_z).length()
	var rho_err: float = absf(rho - radius)
	var x_err: float = absf(q.x - 2.0)
	var ok: bool = nadir_err < 0.0001 and up_err < 0.00001 and rho_err < 0.001 and x_err < 0.0001
	print("[BEND] self_check %s nadir=%.6f up=%.6f rho=%.6f x=%.6f" % ["PASS" if ok else "FAIL", nadir_err, up_err, rho_err, x_err])
	return ok


func run(root: Node) -> Dictionary:
	meshes = 0
	verts = 0
	shapes = 0
	_spans.clear()
	_excluded.clear()
	var t0: int = Time.get_ticks_msec()
	self_check()
	_measure(root)
	_walk(root)
	var ms: int = Time.get_ticks_msec() - t0
	return {"ms": ms, "meshes": meshes, "verts": verts, "shapes": shapes}


func _skip_name(n: Node) -> bool:
	return SKIP_NAMES.has(String(n.name))


func _merge_z(a: Vector2, b: Vector2) -> Vector2:
	return Vector2(minf(a.x, b.x), maxf(a.y, b.y))


func _measure(n: Node) -> Vector2:
	var id: int = n.get_instance_id()
	if _skip_name(n):
		_excluded[id] = true
		return Vector2(INF, -INF)
	var acc := Vector2(INF, -INF)
	if n is Node3D:
		var z: float = (n as Node3D).global_position.z
		acc = Vector2(z, z)
	if n is MeshInstance3D:
		acc = _merge_z(acc, _mesh_z(n as MeshInstance3D))
	elif n is CollisionShape3D:
		acc = _merge_z(acc, _shape_z(n as CollisionShape3D))
	var excl: bool = false
	for c: Node in n.get_children():
		acc = _merge_z(acc, _measure(c))
		if _excluded.get(c.get_instance_id(), false):
			excl = true
	if excl:
		_excluded[id] = true
	_spans[id] = acc
	return acc


func _mesh_z(mi: MeshInstance3D) -> Vector2:
	if mi.mesh == null:
		return Vector2(INF, -INF)
	var aabb: AABB = mi.mesh.get_aabb()
	var xf: Transform3D = mi.global_transform
	var acc := Vector2(INF, -INF)
	for i: int in range(8):
		var c: Vector3 = aabb.position
		if (i & 1) != 0:
			c.x += aabb.size.x
		if (i & 2) != 0:
			c.y += aabb.size.y
		if (i & 4) != 0:
			c.z += aabb.size.z
		var z: float = (xf * c).z
		acc = Vector2(minf(acc.x, z), maxf(acc.y, z))
	return acc


func _shape_z(cs: CollisionShape3D) -> Vector2:
	var shape: Shape3D = cs.shape
	if shape == null:
		return Vector2(INF, -INF)
	var xf: Transform3D = cs.global_transform
	if shape is BoxShape3D:
		return _aabb_z(xf, AABB(-(shape as BoxShape3D).size * 0.5, (shape as BoxShape3D).size))
	if shape is SphereShape3D:
		var r: float = (shape as SphereShape3D).radius
		return _aabb_z(xf, AABB(Vector3(-r, -r, -r), Vector3(r, r, r) * 2.0))
	if shape is CapsuleShape3D:
		var cap: CapsuleShape3D = shape as CapsuleShape3D
		return _aabb_z(xf, AABB(Vector3(-cap.radius, -cap.height * 0.5, -cap.radius), Vector3(cap.radius * 2.0, cap.height, cap.radius * 2.0)))
	if shape is CylinderShape3D:
		var cyl: CylinderShape3D = shape as CylinderShape3D
		return _aabb_z(xf, AABB(Vector3(-cyl.radius, -cyl.height * 0.5, -cyl.radius), Vector3(cyl.radius * 2.0, cyl.height, cyl.radius * 2.0)))
	if shape is ConcavePolygonShape3D:
		return _points_z(xf, (shape as ConcavePolygonShape3D).get_faces())
	if shape is ConvexPolygonShape3D:
		return _points_z(xf, (shape as ConvexPolygonShape3D).points)
	var z: float = xf.origin.z
	return Vector2(z, z)


func _aabb_z(xf: Transform3D, aabb: AABB) -> Vector2:
	var acc := Vector2(INF, -INF)
	for i: int in range(8):
		var c: Vector3 = aabb.position
		if (i & 1) != 0:
			c.x += aabb.size.x
		if (i & 2) != 0:
			c.y += aabb.size.y
		if (i & 4) != 0:
			c.z += aabb.size.z
		var z: float = (xf * c).z
		acc = Vector2(minf(acc.x, z), maxf(acc.y, z))
	return acc


func _points_z(xf: Transform3D, pts: PackedVector3Array) -> Vector2:
	if pts.is_empty():
		var z: float = xf.origin.z
		return Vector2(z, z)
	var acc := Vector2(INF, -INF)
	for p: Vector3 in pts:
		var z: float = (xf * p).z
		acc = Vector2(minf(acc.x, z), maxf(acc.y, z))
	return acc


func _span_width(n: Node) -> float:
	var sp: Vector2 = _spans.get(n.get_instance_id(), Vector2(INF, -INF))
	if sp.x > sp.y:
		return 0.0
	return sp.y - sp.x


func _rigid_limit(n: Node) -> float:
	if n.get_node_or_null("PropAabbBody") != null:
		return PROP_RIGID_Z
	return RIGID_Z


func _rigid_ok(n: Node) -> bool:
	if n is MultiMeshInstance3D or n is NavigationRegion3D or n is Camera3D:
		return false
	if _excluded.get(n.get_instance_id(), false):
		return false
	if _span_width(n) > _rigid_limit(n):
		return false
	return true


func _walk(n: Node) -> void:
	if n.get_meta(META_TREE, false):
		return
	if _skip_name(n):
		return
	if n is CanvasLayer or n is DirectionalLight3D:
		return
	if n is Camera3D:
		return
	if n is MultiMeshInstance3D:
		if not n.get_meta(META_SELF, false):
			_bend_multimesh(n as MultiMeshInstance3D)
			n.set_meta(META_SELF, true)
		return
	if n is NavigationRegion3D:
		if not n.get_meta(META_SELF, false):
			_bend_nav(n as NavigationRegion3D)
			n.set_meta(META_SELF, true)
		for c_nav: Node in n.get_children():
			_walk(c_nav)
		return
	if n is Node3D and n.get_parent() != null and _rigid_ok(n):
		_apply_rigid(n as Node3D)
		_mark_tree(n)
		return
	if n is MeshInstance3D and not n.get_meta(META_SELF, false):
		var mi: MeshInstance3D = n as MeshInstance3D
		if mi.visible:
			_warp_mesh(mi)
		mi.set_meta(META_SELF, true)
	elif n is CollisionShape3D and not n.get_meta(META_SELF, false):
		_warp_shape(n as CollisionShape3D)
		n.set_meta(META_SELF, true)
	for c: Node in n.get_children():
		_walk(c)


func _mark_tree(n: Node) -> void:
	n.set_meta(META_TREE, true)
	for c: Node in n.get_children():
		_mark_tree(c)


func _apply_rigid(n: Node3D) -> void:
	var xf: Transform3D = n.global_transform
	var th: float = (xf.origin.z - axis_z) / radius
	n.global_transform = Transform3D(bend_basis(th) * xf.basis, bend_point(xf.origin))


func _warp_mesh(mi: MeshInstance3D) -> void:
	var src: Mesh = mi.mesh
	if src == null or src.get_surface_count() <= 0:
		return
	var xf: Transform3D = mi.global_transform
	var inv: Transform3D = xf.affine_inverse()
	var rot: Basis = xf.basis.orthonormalized()
	var inv_rot: Basis = rot.inverse()
	var dst := ArrayMesh.new()
	var wrote: bool = false
	for si: int in range(src.get_surface_count()):
		var arrays: Array = src.surface_get_arrays(si)
		if arrays.is_empty() or not (arrays[Mesh.ARRAY_VERTEX] is PackedVector3Array):
			continue
		# PrimitiveMesh (BoxMesh, QuadMesh) has no surface_get_primitive_type. Its
		# generated surface is triangles. Only ArrayMesh records another type.
		var prim: Mesh.PrimitiveType = Mesh.PRIMITIVE_TRIANGLES
		if src is ArrayMesh:
			prim = (src as ArrayMesh).surface_get_primitive_type(si)
		var bones: Variant = arrays[Mesh.ARRAY_BONES] if arrays.size() > Mesh.ARRAY_BONES else null
		if bones is PackedInt32Array and (bones as PackedInt32Array).size() > 0:
			_apply_rigid(mi)
			_mark_tree(mi)
			return
		var mat: Material = mi.get_active_material(si)
		if mat == null:
			mat = src.surface_get_material(si)
		if prim != Mesh.PRIMITIVE_TRIANGLES:
			_bend_vertex_arrays(arrays, xf, inv, rot, inv_rot)
			var pi: int = dst.get_surface_count()
			dst.add_surface_from_arrays(prim, arrays)
			if mat != null:
				dst.surface_set_material(pi, mat)
			wrote = true
			continue
		if _surface_needs_split(arrays, xf):
			arrays = _split_surface(arrays, xf)
		_bend_vertex_arrays(arrays, xf, inv, rot, inv_rot)
		var ni: int = dst.get_surface_count()
		dst.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
		if mat != null:
			dst.surface_set_material(ni, mat)
		wrote = true
		verts += (arrays[Mesh.ARRAY_VERTEX] as PackedVector3Array).size()
	if not wrote:
		return
	for oi: int in range(src.get_surface_count()):
		mi.set_surface_override_material(oi, null)
	mi.mesh = dst
	meshes += 1


func _surface_needs_split(arrays: Array, xf: Transform3D) -> bool:
	var pv: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	var index_v: Variant = arrays[Mesh.ARRAY_INDEX]
	var indices := PackedInt32Array()
	if index_v is PackedInt32Array and (index_v as PackedInt32Array).size() >= 3:
		indices = index_v
	else:
		indices.resize(pv.size())
		for i: int in range(pv.size()):
			indices[i] = i
	var count: int = indices.size() / 3
	for t: int in range(count):
		var i0: int = indices[t * 3]
		var i1: int = indices[t * 3 + 1]
		var i2: int = indices[t * 3 + 2]
		if i0 < 0 or i1 < 0 or i2 < 0 or i0 >= pv.size() or i1 >= pv.size() or i2 >= pv.size():
			continue
		var z0: float = (xf * pv[i0]).z
		var z1: float = (xf * pv[i1]).z
		var z2: float = (xf * pv[i2]).z
		if absf(z0 - z1) > EDGE_Z or absf(z1 - z2) > EDGE_Z or absf(z2 - z0) > EDGE_Z:
			return true
	return false


func _split_surface(arrays: Array, xf: Transform3D) -> Array:
	var src_v: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	var src_n: PackedVector3Array = arrays[Mesh.ARRAY_NORMAL] if arrays[Mesh.ARRAY_NORMAL] is PackedVector3Array else PackedVector3Array()
	var src_uv: PackedVector2Array = arrays[Mesh.ARRAY_TEX_UV] if arrays[Mesh.ARRAY_TEX_UV] is PackedVector2Array else PackedVector2Array()
	var src_uv2: PackedVector2Array = arrays[Mesh.ARRAY_TEX_UV2] if arrays[Mesh.ARRAY_TEX_UV2] is PackedVector2Array else PackedVector2Array()
	var src_c: PackedColorArray = arrays[Mesh.ARRAY_COLOR] if arrays[Mesh.ARRAY_COLOR] is PackedColorArray else PackedColorArray()
	var src_t: PackedFloat32Array = arrays[Mesh.ARRAY_TANGENT] if arrays[Mesh.ARRAY_TANGENT] is PackedFloat32Array else PackedFloat32Array()
	var has_n: bool = src_n.size() == src_v.size()
	var has_uv: bool = src_uv.size() == src_v.size()
	var has_uv2: bool = src_uv2.size() == src_v.size()
	var has_c: bool = src_c.size() == src_v.size()
	var has_t: bool = src_t.size() == src_v.size() * 4
	var wp := PackedVector3Array()
	var wn := PackedVector3Array()
	var uv := PackedVector2Array()
	var uv2 := PackedVector2Array()
	var col := PackedColorArray()
	var tg := PackedFloat32Array()
	wp.resize(src_v.size())
	for i: int in range(src_v.size()):
		wp[i] = xf * src_v[i]
	if has_n:
		wn = src_n.duplicate()
	if has_uv:
		uv = src_uv.duplicate()
	if has_uv2:
		uv2 = src_uv2.duplicate()
	if has_c:
		col = src_c.duplicate()
	if has_t:
		tg = src_t.duplicate()
	var index_v: Variant = arrays[Mesh.ARRAY_INDEX]
	var indices := PackedInt32Array()
	if index_v is PackedInt32Array and (index_v as PackedInt32Array).size() >= 3:
		indices = index_v
	else:
		indices.resize(src_v.size())
		for ii: int in range(src_v.size()):
			indices[ii] = ii
	var out_i := PackedInt32Array()
	var tri_n: int = indices.size() / 3
	for t: int in range(tri_n):
		_split_tri(indices[t * 3], indices[t * 3 + 1], indices[t * 3 + 2], 0, wp, wn, uv, uv2, col, tg, has_n, has_uv, has_uv2, has_c, has_t, out_i)
	# Positions were split in world space. The bend step expects mesh-local vertices.
	var inv_xf: Transform3D = xf.affine_inverse()
	for vi: int in range(wp.size()):
		wp[vi] = inv_xf * wp[vi]
	var out := []
	out.resize(Mesh.ARRAY_MAX)
	out[Mesh.ARRAY_VERTEX] = wp
	if has_n:
		out[Mesh.ARRAY_NORMAL] = wn
	if has_t:
		out[Mesh.ARRAY_TANGENT] = tg
	if has_c:
		out[Mesh.ARRAY_COLOR] = col
	if has_uv:
		out[Mesh.ARRAY_TEX_UV] = uv
	if has_uv2:
		out[Mesh.ARRAY_TEX_UV2] = uv2
	out[Mesh.ARRAY_INDEX] = out_i
	return out


func _split_tri(i0: int, i1: int, i2: int, depth: int, wp: PackedVector3Array, wn: PackedVector3Array, uv: PackedVector2Array, uv2: PackedVector2Array, col: PackedColorArray, tg: PackedFloat32Array, has_n: bool, has_uv: bool, has_uv2: bool, has_c: bool, has_t: bool, out_i: PackedInt32Array) -> void:
	if i0 < 0 or i1 < 0 or i2 < 0 or i0 >= wp.size() or i1 >= wp.size() or i2 >= wp.size():
		return
	var d01: float = absf(wp[i0].z - wp[i1].z)
	var d12: float = absf(wp[i1].z - wp[i2].z)
	var d20: float = absf(wp[i2].z - wp[i0].z)
	if depth >= 8 or (d01 <= EDGE_Z and d12 <= EDGE_Z and d20 <= EDGE_Z):
		out_i.append(i0)
		out_i.append(i1)
		out_i.append(i2)
		return
	var a: int = i0
	var b: int = i1
	var c: int = i2
	if d12 >= d01 and d12 >= d20:
		a = i1
		b = i2
		c = i0
	elif d20 >= d01 and d20 >= d12:
		a = i2
		b = i0
		c = i1
	var mid: int = wp.size()
	wp.append((wp[a] + wp[b]) * 0.5)
	if has_n:
		wn.append((wn[a] + wn[b]).normalized())
	if has_uv:
		uv.append((uv[a] + uv[b]) * 0.5)
	if has_uv2:
		uv2.append((uv2[a] + uv2[b]) * 0.5)
	if has_c:
		col.append(Color(
			(col[a].r + col[b].r) * 0.5,
			(col[a].g + col[b].g) * 0.5,
			(col[a].b + col[b].b) * 0.5,
			(col[a].a + col[b].a) * 0.5
		))
	if has_t:
		tg.append((tg[a * 4] + tg[b * 4]) * 0.5)
		tg.append((tg[a * 4 + 1] + tg[b * 4 + 1]) * 0.5)
		tg.append((tg[a * 4 + 2] + tg[b * 4 + 2]) * 0.5)
		tg.append(tg[a * 4 + 3])
	# a-b was the long edge. The third vertex stays c. Recurse on (a, mid, c) and (mid, b, c).
	_split_tri(a, mid, c, depth + 1, wp, wn, uv, uv2, col, tg, has_n, has_uv, has_uv2, has_c, has_t, out_i)
	_split_tri(mid, b, c, depth + 1, wp, wn, uv, uv2, col, tg, has_n, has_uv, has_uv2, has_c, has_t, out_i)


func _bend_vertex_arrays(arrays: Array, xf: Transform3D, inv: Transform3D, rot: Basis, inv_rot: Basis) -> void:
	var pv: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	var normals: PackedVector3Array = arrays[Mesh.ARRAY_NORMAL] if arrays[Mesh.ARRAY_NORMAL] is PackedVector3Array else PackedVector3Array()
	var tangents: PackedFloat32Array = arrays[Mesh.ARRAY_TANGENT] if arrays[Mesh.ARRAY_TANGENT] is PackedFloat32Array else PackedFloat32Array()
	var has_n: bool = normals.size() == pv.size()
	var has_t: bool = tangents.size() == pv.size() * 4
	for i: int in range(pv.size()):
		var world_p: Vector3 = xf * pv[i]
		var th: float = (world_p.z - axis_z) / radius
		var bent_p: Vector3 = bend_point(world_p)
		pv[i] = inv * bent_p
		var spin: Basis = bend_basis(th)
		if has_n:
			var wn: Vector3 = (rot * normals[i]).normalized()
			normals[i] = (inv_rot * (spin * wn)).normalized()
		if has_t:
			var tx: Vector3 = Vector3(tangents[i * 4], tangents[i * 4 + 1], tangents[i * 4 + 2])
			var wt: Vector3 = (rot * tx).normalized()
			var bt: Vector3 = (inv_rot * (spin * wt)).normalized()
			tangents[i * 4] = bt.x
			tangents[i * 4 + 1] = bt.y
			tangents[i * 4 + 2] = bt.z
	arrays[Mesh.ARRAY_VERTEX] = pv
	if has_n:
		arrays[Mesh.ARRAY_NORMAL] = normals
	if has_t:
		arrays[Mesh.ARRAY_TANGENT] = tangents


func _warp_shape(cs: CollisionShape3D) -> void:
	var shape: Shape3D = cs.shape
	if shape == null:
		_apply_rigid(cs)
		shapes += 1
		return
	var width: float = _span_width(cs)
	if width <= RIGID_Z:
		_apply_rigid(cs)
		shapes += 1
		return
	if shape is BoxShape3D:
		_split_box(cs, shape as BoxShape3D)
		return
	if shape is ConcavePolygonShape3D:
		_warp_concave(cs, shape as ConcavePolygonShape3D)
		return
	if shape is ConvexPolygonShape3D:
		_warp_convex(cs, shape as ConvexPolygonShape3D)
		return
	_apply_rigid(cs)
	shapes += 1


func _split_box(cs: CollisionShape3D, box: BoxShape3D) -> void:
	var parent_n: Node = cs.get_parent()
	if parent_n == null or not (parent_n is Node3D):
		_apply_rigid(cs)
		shapes += 1
		return
	var xf: Transform3D = cs.global_transform
	var he: Vector3 = box.size * 0.5
	var corners: Array[Vector3] = []
	for ix: int in range(2):
		for iy: int in range(2):
			for iz: int in range(2):
				var lp := Vector3(-he.x if ix == 0 else he.x, -he.y if iy == 0 else he.y, -he.z if iz == 0 else he.z)
				corners.append(xf * lp)
	var zmin: float = INF
	var zmax: float = -INF
	for c: Vector3 in corners:
		zmin = minf(zmin, c.z)
		zmax = maxf(zmax, c.z)
	var parent_xf: Transform3D = (parent_n as Node3D).global_transform
	var inv_parent: Transform3D = parent_xf.affine_inverse()
	var first: bool = true
	var z0: float = zmin
	while z0 < zmax - 0.0001:
		var z1: float = minf(z0 + EDGE_Z, zmax)
		var clipped: PackedVector3Array = _clip_box_slab(corners, z0 - 0.0001, z1 + 0.0001)
		if clipped.size() >= 3:
			var bent := PackedVector3Array()
			bent.resize(clipped.size())
			for i: int in range(clipped.size()):
				bent[i] = inv_parent * bend_point(clipped[i])
			var convex := ConvexPolygonShape3D.new()
			convex.points = bent
			convex.margin = 0.0
			if first:
				cs.shape = convex
				cs.transform = Transform3D.IDENTITY
				cs.set_meta(META_SELF, true)
				first = false
			else:
				var extra := CollisionShape3D.new()
				extra.name = String(cs.name) + "_Bend%d" % shapes
				extra.shape = convex
				extra.transform = Transform3D.IDENTITY
				extra.set_meta(META_SELF, true)
				extra.set_meta(META_TREE, true)
				parent_n.add_child(extra)
			shapes += 1
			verts += bent.size()
		z0 = z1
	if first:
		_apply_rigid(cs)
		shapes += 1


func _clip_box_slab(corners: Array[Vector3], z_lo: float, z_hi: float) -> PackedVector3Array:
	var edges: Array[Vector2i] = [
		Vector2i(0, 1), Vector2i(2, 3), Vector2i(4, 5), Vector2i(6, 7),
		Vector2i(0, 2), Vector2i(1, 3), Vector2i(4, 6), Vector2i(5, 7),
		Vector2i(0, 4), Vector2i(1, 5), Vector2i(2, 6), Vector2i(3, 7),
	]
	var out := PackedVector3Array()
	for c: Vector3 in corners:
		if c.z >= z_lo and c.z <= z_hi:
			out.append(c)
	for e: Vector2i in edges:
		var a: Vector3 = corners[e.x]
		var b: Vector3 = corners[e.y]
		if absf(a.z - b.z) < 0.0000001:
			continue
		for lim: float in [z_lo, z_hi]:
			var t: float = (lim - a.z) / (b.z - a.z)
			if t > 0.0001 and t < 0.9999:
				var p: Vector3 = a.lerp(b, t)
				if p.z >= z_lo - 0.0001 and p.z <= z_hi + 0.0001:
					out.append(p)
	return out


func _warp_concave(cs: CollisionShape3D, src: ConcavePolygonShape3D) -> void:
	var dup: ConcavePolygonShape3D = src.duplicate(true) as ConcavePolygonShape3D
	if dup == null:
		return
	var faces: PackedVector3Array = dup.get_faces()
	var xf: Transform3D = cs.global_transform
	var inv: Transform3D = xf.affine_inverse()
	var world := PackedVector3Array()
	var i: int = 0
	while i + 2 < faces.size():
		_append_bent_tri(world, xf * faces[i], xf * faces[i + 1], xf * faces[i + 2], 0)
		i += 3
	var local := PackedVector3Array()
	local.resize(world.size())
	for j: int in range(world.size()):
		local[j] = inv * world[j]
	dup.set_faces(local)
	cs.shape = dup
	shapes += 1
	verts += local.size()


func _warp_convex(cs: CollisionShape3D, src: ConvexPolygonShape3D) -> void:
	var dup: ConvexPolygonShape3D = src.duplicate(true) as ConvexPolygonShape3D
	if dup == null:
		return
	var xf: Transform3D = cs.global_transform
	var inv: Transform3D = xf.affine_inverse()
	var pts: PackedVector3Array = dup.points
	for i: int in range(pts.size()):
		pts[i] = inv * bend_point(xf * pts[i])
	dup.points = pts
	cs.shape = dup
	shapes += 1
	verts += pts.size()


func _append_bent_tri(out: PackedVector3Array, a: Vector3, b: Vector3, c: Vector3, depth: int) -> void:
	var d01: float = absf(a.z - b.z)
	var d12: float = absf(b.z - c.z)
	var d20: float = absf(c.z - a.z)
	if depth >= 8 or (d01 <= EDGE_Z and d12 <= EDGE_Z and d20 <= EDGE_Z):
		out.append(bend_point(a))
		out.append(bend_point(b))
		out.append(bend_point(c))
		return
	if d01 >= d12 and d01 >= d20:
		var m: Vector3 = (a + b) * 0.5
		_append_bent_tri(out, a, m, c, depth + 1)
		_append_bent_tri(out, m, b, c, depth + 1)
	elif d12 >= d20:
		var m2: Vector3 = (b + c) * 0.5
		_append_bent_tri(out, a, b, m2, depth + 1)
		_append_bent_tri(out, a, m2, c, depth + 1)
	else:
		var m3: Vector3 = (c + a) * 0.5
		_append_bent_tri(out, a, b, m3, depth + 1)
		_append_bent_tri(out, m3, b, c, depth + 1)


func _bend_multimesh(mmi: MultiMeshInstance3D) -> void:
	var mm: MultiMesh = mmi.multimesh
	if mm == null or mm.mesh == null or mm.transform_format != MultiMesh.TRANSFORM_3D:
		return
	mm = mm.duplicate() as MultiMesh
	if mm == null:
		return
	mmi.multimesh = mm
	var gt: Transform3D = mmi.global_transform
	var inv: Transform3D = gt.affine_inverse()
	var mesh_aabb: AABB = mm.mesh.get_aabb()
	var keep := PackedInt32Array()
	for i: int in range(mm.instance_count):
		var local_xf: Transform3D = mm.get_instance_transform(i)
		var world_xf: Transform3D = gt * local_xf
		var span: float = _aabb_z(world_xf, mesh_aabb).y - _aabb_z(world_xf, mesh_aabb).x
		if span > RIGID_Z:
			var exploded := MeshInstance3D.new()
			exploded.name = "ExtMMBend_%d" % i
			exploded.mesh = mm.mesh
			exploded.material_override = mmi.material_override
			exploded.cast_shadow = mmi.cast_shadow
			var host: Node = mmi.get_parent()
			if host == null:
				continue
			host.add_child(exploded)
			exploded.global_transform = world_xf
			_warp_mesh(exploded)
			exploded.set_meta(META_SELF, true)
			exploded.set_meta(META_TREE, true)
			mm.set_instance_transform(i, Transform3D(Basis().scaled(Vector3(0.0001, 0.0001, 0.0001)), world_xf.origin))
		else:
			var th: float = (world_xf.origin.z - axis_z) / radius
			var bent := Transform3D(bend_basis(th) * world_xf.basis, bend_point(world_xf.origin))
			mm.set_instance_transform(i, inv * bent)
			keep.append(i)
	shapes += 1


func _bend_nav(region: NavigationRegion3D) -> void:
	var src: NavigationMesh = region.navigation_mesh
	if src == null:
		return
	var nm: NavigationMesh = src.duplicate(true) as NavigationMesh
	if nm == null:
		return
	var src_v: PackedVector3Array = nm.vertices
	if src_v.is_empty() or nm.get_polygon_count() <= 0:
		return
	var wp := src_v.duplicate()
	var polys: Array[PackedInt32Array] = []
	for pi: int in range(nm.get_polygon_count()):
		var poly: PackedInt32Array = nm.get_polygon(pi)
		if poly.size() < 3:
			continue
		for t: int in range(1, poly.size() - 1):
			_nav_tri(poly[0], poly[t], poly[t + 1], 0, wp, polys)
	nm.clear_polygons()
	var bent := PackedVector3Array()
	bent.resize(wp.size())
	var xf: Transform3D = region.global_transform
	var inv: Transform3D = xf.affine_inverse()
	for i: int in range(wp.size()):
		bent[i] = inv * bend_point(xf * wp[i])
	nm.vertices = bent
	for poly_i: PackedInt32Array in polys:
		nm.add_polygon(poly_i)
	region.navigation_mesh = nm
	shapes += 1
	verts += bent.size()


func _nav_tri(i0: int, i1: int, i2: int, depth: int, wp: PackedVector3Array, polys: Array[PackedInt32Array]) -> void:
	if i0 < 0 or i1 < 0 or i2 < 0 or i0 >= wp.size() or i1 >= wp.size() or i2 >= wp.size():
		return
	var d01: float = absf(wp[i0].z - wp[i1].z)
	var d12: float = absf(wp[i1].z - wp[i2].z)
	var d20: float = absf(wp[i2].z - wp[i0].z)
	if depth >= 8 or (d01 <= EDGE_Z and d12 <= EDGE_Z and d20 <= EDGE_Z):
		polys.append(PackedInt32Array([i0, i1, i2]))
		return
	var a: int = i0
	var b: int = i1
	var c: int = i2
	if d12 >= d01 and d12 >= d20:
		a = i1
		b = i2
		c = i0
	elif d20 >= d01 and d20 >= d12:
		a = i2
		b = i0
		c = i1
	var mid: int = wp.size()
	wp.append((wp[a] + wp[b]) * 0.5)
	_nav_tri(a, mid, c, depth + 1, wp, polys)
	_nav_tri(mid, b, c, depth + 1, wp, polys)
