extends RefCounted
## Gage: Tennis Tower render batching, distance ranges, and visibility stamps.
## Runs once after TennisTowerLoader.tower_built. Rook's loader and GLBs are untouched.
## - MeshInstance3D nodes that share one mesh (and the same overrides) inside one tag and one
##   plan cell become one MultiMeshInstance3D. Originals are hidden, never freed.
## - Colliders, movers, doors, and anything marked tt_no_batch stay individual.
## - Interior props get a short visibility range, no sun shadow, and a lower LOD bias.
##   Structural shells (slabs, walls, facade, roof) stay unlimited so ceilings and the
##   drum read do not pop. tt_visibility.gd hides the prop batches the camera cannot be in.


const CELL_M := 32.0
const SHELL_CELL_M := 64.0
const MIN_BATCH := 2
const SMALL_M := 2.5
const TINY_M := 0.7
const INTERIOR_TAGS := ["f1", "f2", "f3"]
const SHELL_END_M := 0.0
const INTERIOR_END_M := 52.0
const INTERIOR_MARGIN_M := 8.0
const SMALL_END_M := 32.0
const SMALL_MARGIN_M := 6.0
const TINY_END_M := 22.0
const TINY_MARGIN_M := 4.0
const SITE_SMALL_END_M := 45.0
const SITE_SMALL_MARGIN_M := 8.0
const ORNAMENT_END_M := 48.0
const ORNAMENT_MARGIN_M := 8.0


static func _range_for(tag: String, longest: float, keep: bool) -> Vector2:
	# Slabs, curtain and columns stay unlimited. Small shell ornaments drop out
	# from the drum (~100 m) and still read in a doorway shot.
	if keep:
		if longest < SMALL_M and tag != "struct" and tag != "env" and tag != "cols":
			return Vector2(ORNAMENT_END_M, ORNAMENT_MARGIN_M)
		return Vector2(SHELL_END_M, 0.0)
	if INTERIOR_TAGS.has(tag):
		if longest < TINY_M:
			return Vector2(TINY_END_M, TINY_MARGIN_M)
		if longest < SMALL_M:
			return Vector2(SMALL_END_M, SMALL_MARGIN_M)
		return Vector2(INTERIOR_END_M, INTERIOR_MARGIN_M)
	if tag == "site" and longest < SMALL_M:
		return Vector2(SITE_SMALL_END_M, SITE_SMALL_MARGIN_M)
	return Vector2(SHELL_END_M, 0.0)


static func _apply_range(gi: GeometryInstance3D, r: Vector2) -> void:
	if r.x <= 0.0:
		return
	gi.visibility_range_begin = 0.0
	gi.visibility_range_end = r.x
	gi.visibility_range_end_margin = r.y
	# Compatibility: the margin is hysteresis. Forward+ / Mobile fade across it.
	if r.y > 0.0 and RenderingServer.get_current_rendering_method() != "gl_compatibility":
		gi.visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_SELF
	else:
		gi.visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_DISABLED


static func _decorate(gi: GeometryInstance3D, tag: String, longest: float, keep: bool) -> void:
	_apply_range(gi, _range_for(tag, longest, keep))
	if keep or not INTERIOR_TAGS.has(tag):
		return
	# Lower bias pulls the generated LOD in sooner. Runtime GLBs often have no LOD chain;
	# the property is still set so imported meshes that do have one drop detail.
	gi.lod_bias = 0.4 if longest < SMALL_M else 0.65


static func _collect(n: Node, out: Array[MeshInstance3D]) -> void:
	for c: Node in n.get_children():
		if c is StaticBody3D:
			continue
		if c is MeshInstance3D:
			var mi: MeshInstance3D = c as MeshInstance3D
			if mi.visible and mi.mesh != null:
				out.append(mi)
		if c is Node3D and not (c as Node3D).visible:
			continue
		_collect(c, out)


static func _has_surface_override(mi: MeshInstance3D) -> bool:
	for i: int in range(mi.mesh.get_surface_count()):
		if mi.get_surface_override_material(i) != null:
			return true
	return false


static func _branch_blocks(n: Node) -> bool:
	if n is StaticBody3D:
		return false
	if n is VisualInstance3D or n is Light3D:
		return true
	for c: Node in n.get_children():
		if _branch_blocks(c):
			return true
	return false


## Movers, doors, and real sub-meshes stay out. Empty pivots do not.
static func _blocks_batch(mi: MeshInstance3D) -> bool:
	if mi.has_meta("tt_no_batch"):
		return true
	for c: Node in mi.get_children():
		if _branch_blocks(c):
			return true
	return false


static func _surface_sig(mi: MeshInstance3D) -> String:
	var s := ""
	for i: int in range(mi.mesh.get_surface_count()):
		var mat: Material = mi.get_surface_override_material(i)
		s += str(mat.get_instance_id() if mat != null else 0) + ","
	return s


static func _placement_name(mi: Node) -> String:
	var n: Node = mi
	while n != null:
		var p: Node = n.get_parent()
		if p != null and String(p.name).begins_with("Tag_"):
			return String(n.name)
		n = p
	return String(mi.name)


static func _keep_visual(mi: MeshInstance3D) -> bool:
	var nm := _placement_name(mi).to_lower()
	return nm.contains("tt_struct") or nm.contains("facade") or nm.contains("entrance") or nm.contains("curtain") or nm.contains("roof") or nm.contains("column")


static func _floor_of(tag: String) -> int:
	if tag == "f1":
		return 1
	if tag == "f2":
		return 2
	if tag == "f3":
		return 3
	return 0


static func _roofish(tag: String, nm: String) -> bool:
	return tag == "roof" or nm.to_lower().contains("roof")


static func _slabish(nm: String) -> bool:
	return nm.to_lower().contains("slab")


static func _stamp(gi: GeometryInstance3D, tag: String, keep: bool, c: Vector3, roof: bool, slab: bool) -> void:
	gi.set_meta("tt_vis_floor", _floor_of(tag))
	gi.set_meta("tt_vis_keep", keep)
	gi.set_meta("tt_vis_tag", tag)
	gi.set_meta("tt_vis_roof", roof)
	gi.set_meta("tt_vis_slab", slab)
	gi.set_meta("tt_vis_x", c.x)
	gi.set_meta("tt_vis_z", c.z)


static func _mesh_for(first: MeshInstance3D) -> Mesh:
	if not _has_surface_override(first):
		return first.mesh
	var dup: Resource = first.mesh.duplicate(true)
	if not (dup is ArrayMesh):
		return null
	var baked: ArrayMesh = dup as ArrayMesh
	for i: int in range(baked.get_surface_count()):
		var ov: Material = first.get_surface_override_material(i)
		if ov != null:
			baked.surface_set_material(i, ov)
	return baked


static func _surfaces(mi: MeshInstance3D) -> int:
	return mi.mesh.get_surface_count() if mi.mesh != null else 0


static func _longest(mi: MeshInstance3D) -> float:
	var aabb: AABB = mi.global_transform * mi.mesh.get_aabb()
	return aabb.size[aabb.get_longest_axis_index()]


## tower: the TennisTower_Strip5 root (already built, in the tree).
static func run(tower: Node3D) -> Dictionary:
	var t0: int = Time.get_ticks_usec()
	var st: Dictionary = {"mi_before": 0, "surfaces_before": 0, "mmi": 0, "batched_mi": 0, "mi_after": 0,
		"surfaces_after": 0, "instances_in_mmi": 0, "ranged": 0, "nobatch": 0, "ms": 0.0,
		"child_skip": 0, "keep": 0, "surf_batched": 0}
	var inv_tower: Transform3D = tower.global_transform.affine_inverse()
	for tag_node: Node in tower.get_children():
		if not (tag_node is Node3D) or not String(tag_node.name).begins_with("Tag_"):
			continue
		var tag_root: Node3D = tag_node as Node3D
		var tag: String = String(tag_root.name).substr(4)
		var inv_tag: Transform3D = tag_root.global_transform.affine_inverse()
		var cell_m: float = CELL_M if INTERIOR_TAGS.has(tag) else SHELL_CELL_M
		var mis: Array[MeshInstance3D] = []
		_collect(tag_root, mis)
		var groups: Dictionary = {}
		for mi: MeshInstance3D in mis:
			st["mi_before"] = int(st["mi_before"]) + 1
			st["surfaces_before"] = int(st["surfaces_before"]) + _surfaces(mi)
			var longest: float = _longest(mi)
			var keep: bool = _keep_visual(mi)
			if keep:
				st["keep"] = int(st["keep"]) + 1
			var gx: Transform3D = mi.global_transform
			var center: Vector3 = inv_tower * (gx * mi.mesh.get_aabb()).get_center()
			var placed: String = _placement_name(mi)
			var roof: bool = _roofish(tag, placed)
			var slab: bool = _slabish(placed)
			if INTERIOR_TAGS.has(tag) and not keep:
				mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
			if _blocks_batch(mi):
				if mi.has_meta("tt_no_batch"):
					st["nobatch"] = int(st["nobatch"]) + 1
				else:
					st["child_skip"] = int(st["child_skip"]) + 1
				# Swinging leaves stay drawn for the whole open. A range or a room
				# portal would hide the leaf the player is walking through.
				if not mi.has_meta("tt_vis_mover"):
					_decorate(mi, tag, longest, keep)
				_stamp(mi, tag, keep, center, roof, slab)
				st["ranged"] = int(st["ranged"]) + 1
				continue
			var cell: Vector2i = Vector2i(floori(center.x / cell_m), floori(center.z / cell_m))
			var mo_id: int = mi.material_override.get_instance_id() if mi.material_override != null else 0
			var key: String = "%d|%d|%d|%d|%d|%d|%d|%s" % [mi.mesh.get_instance_id(), mo_id, int(mi.cast_shadow), cell.x, cell.y, 1 if longest < SMALL_M else 0, 1 if keep else 0, _surface_sig(mi)]
			if not groups.has(key):
				groups[key] = []
			(groups[key] as Array).append(mi)
		for key: String in groups.keys():
			var arr: Array = groups[key]
			var first: MeshInstance3D = arr[0] as MeshInstance3D
			var longest0: float = _longest(first)
			var keep0: bool = _keep_visual(first)
			var placed0: String = _placement_name(first)
			var roof0: bool = _roofish(tag, placed0)
			var slab0: bool = _slabish(placed0)
			if arr.size() < MIN_BATCH:
				_decorate(first, tag, longest0, keep0)
				var alone: Vector3 = inv_tower * (first.global_transform * first.mesh.get_aabb()).get_center()
				_stamp(first, tag, keep0, alone, roof0, slab0)
				st["ranged"] = int(st["ranged"]) + 1
				continue
			var use_mesh: Mesh = _mesh_for(first)
			if use_mesh == null:
				for left_i: int in range(arr.size()):
					var left_m: MeshInstance3D = arr[left_i] as MeshInstance3D
					_decorate(left_m, tag, longest0, keep0)
					var left_c: Vector3 = inv_tower * (left_m.global_transform * left_m.mesh.get_aabb()).get_center()
					var placed_l: String = _placement_name(left_m)
					_stamp(left_m, tag, keep0, left_c, _roofish(tag, placed_l), _slabish(placed_l))
					st["ranged"] = int(st["ranged"]) + 1
				continue
			var acc := Vector3.ZERO
			var mm: MultiMesh = MultiMesh.new()
			mm.transform_format = MultiMesh.TRANSFORM_3D
			mm.mesh = use_mesh
			mm.instance_count = arr.size()
			for i: int in range(arr.size()):
				var m: MeshInstance3D = arr[i] as MeshInstance3D
				mm.set_instance_transform(i, inv_tag * m.global_transform)
				acc += inv_tower * (m.global_transform * m.mesh.get_aabb()).get_center()
				m.visible = false
			var mmi: MultiMeshInstance3D = MultiMeshInstance3D.new()
			mmi.physics_interpolation_mode = Node.PHYSICS_INTERPOLATION_MODE_OFF
			mmi.name = "MM_%s_%d" % [String(first.mesh.resource_name if first.mesh.resource_name != "" else first.name), int(st["mmi"])]
			mmi.multimesh = mm
			if not _has_surface_override(first):
				mmi.material_override = first.material_override
			else:
				st["surf_batched"] = int(st["surf_batched"]) + arr.size()
			mmi.cast_shadow = first.cast_shadow
			_decorate(mmi, tag, longest0, keep0)
			_stamp(mmi, tag, keep0, acc / float(arr.size()), roof0, slab0)
			tag_root.add_child(mmi)
			st["mmi"] = int(st["mmi"]) + 1
			st["batched_mi"] = int(st["batched_mi"]) + arr.size()
			st["instances_in_mmi"] = int(st["instances_in_mmi"]) + arr.size()
			st["surfaces_after"] = int(st["surfaces_after"]) + use_mesh.get_surface_count()
	var left: Array[MeshInstance3D] = []
	_collect(tower, left)
	st["mi_after"] = left.size()
	for mi2: MeshInstance3D in left:
		st["surfaces_after"] = int(st["surfaces_after"]) + _surfaces(mi2)
	st["ms"] = float(Time.get_ticks_usec() - t0) / 1000.0
	print("[TT] batch detail child_skip=%d keep=%d surf_batched=%d" % [int(st["child_skip"]), int(st["keep"]), int(st["surf_batched"])])
	return st
