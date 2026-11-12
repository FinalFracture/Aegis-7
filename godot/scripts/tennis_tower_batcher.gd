extends RefCounted
## Gage: Tennis Tower (Strip 5) render batching + per-floor draw distances.
## Runs once after TennisTowerLoader.tower_built. Rook's loader and GLBs are untouched.
## - Visual MeshInstance3D nodes that share one mesh (and material override / shadow mode) inside one
##   tag group and one CELL_M x CELL_M building-plan cell become one MultiMeshInstance3D.
##   The originals are hidden (visible = false), never freed, so cutaways and the loader's tag roots still work.
## - Colliders are untouched (StaticBody3D nodes from *-colonly stay as built).
## - visibility_range_end (+ margin) per tag: interiors (Tag_f1/f2/f3) and small dressing fade out with distance;
##   the exterior shell (env/facade/roof/site/struct/cols/plant) has no range limit, so it reads across the drum.

const CELL_M := 32.0
const MIN_BATCH := 2
## Longest scaled AABB side under this counts as small dressing.
const SMALL_M := 2.5
const INTERIOR_TAGS := ["f1", "f2", "f3"]
## 0 = no limit: the shell reads from anywhere in the drum (400 m across, 720 m along the axis).
const SHELL_END_M := 0.0
const INTERIOR_END_M := 80.0
const INTERIOR_MARGIN_M := 10.0
const SMALL_END_M := 40.0
const SMALL_MARGIN_M := 5.0
const SITE_SMALL_END_M := 120.0
const SITE_SMALL_MARGIN_M := 10.0


static func _range_for(tag: String, small: bool) -> Vector2:
	if INTERIOR_TAGS.has(tag):
		if small:
			return Vector2(SMALL_END_M, SMALL_MARGIN_M)
		return Vector2(INTERIOR_END_M, INTERIOR_MARGIN_M)
	if tag == "site" and small:
		return Vector2(SITE_SMALL_END_M, SITE_SMALL_MARGIN_M)
	return Vector2(SHELL_END_M, 0.0)


static func _apply_range(gi: GeometryInstance3D, r: Vector2) -> void:
	if r.x <= 0.0:
		return
	gi.visibility_range_begin = 0.0
	gi.visibility_range_end = r.x
	gi.visibility_range_end_margin = r.y
	# Compatibility renderer: margin acts as hysteresis. Forward+ / Mobile: alpha fade over the margin.
	if r.y > 0.0 and RenderingServer.get_current_rendering_method() != "gl_compatibility":
		gi.visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_SELF
	else:
		gi.visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_DISABLED


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


static func _has_visual_child(mi: MeshInstance3D) -> bool:
	for c: Node in mi.get_children():
		if c is VisualInstance3D or (c is Node3D and not (c is StaticBody3D)):
			return true
	return false


static func _surfaces(mi: MeshInstance3D) -> int:
	return mi.mesh.get_surface_count() if mi.mesh != null else 0


## tower: the TennisTower_Strip5 root (already built, in the tree).
static func run(tower: Node3D) -> Dictionary:
	var t0: int = Time.get_ticks_usec()
	var st: Dictionary = {"mi_before": 0, "surfaces_before": 0, "mmi": 0, "batched_mi": 0, "mi_after": 0,
		"surfaces_after": 0, "instances_in_mmi": 0, "ranged": 0, "ms": 0.0}
	var inv_tower: Transform3D = tower.global_transform.affine_inverse()
	for tag_node: Node in tower.get_children():
		if not (tag_node is Node3D) or not String(tag_node.name).begins_with("Tag_"):
			continue
		var tag_root: Node3D = tag_node as Node3D
		var tag: String = String(tag_root.name).substr(4)
		var inv_tag: Transform3D = tag_root.global_transform.affine_inverse()
		var mis: Array[MeshInstance3D] = []
		_collect(tag_root, mis)
		var groups: Dictionary = {}
		for mi: MeshInstance3D in mis:
			st["mi_before"] = int(st["mi_before"]) + 1
			st["surfaces_before"] = int(st["surfaces_before"]) + _surfaces(mi)
			var gx: Transform3D = mi.global_transform
			var aabb: AABB = gx * mi.mesh.get_aabb()
			var small: bool = aabb.size[aabb.get_longest_axis_index()] < SMALL_M
			if _has_surface_override(mi) or _has_visual_child(mi) or mi.has_meta("tt_no_batch"):
				_apply_range(mi, _range_for(tag, small))
				st["ranged"] = int(st["ranged"]) + 1
				continue
			var c_local: Vector3 = inv_tower * aabb.get_center()
			var cell: Vector2i = Vector2i(floori(c_local.x / CELL_M), floori(c_local.z / CELL_M))
			var mo_id: int = mi.material_override.get_instance_id() if mi.material_override != null else 0
			var key: String = "%d|%d|%d|%d|%d|%d" % [mi.mesh.get_instance_id(), mo_id, int(mi.cast_shadow), cell.x, cell.y, 1 if small else 0]
			if not groups.has(key):
				groups[key] = []
			(groups[key] as Array).append(mi)
		for key: String in groups.keys():
			var arr: Array = groups[key]
			var first: MeshInstance3D = arr[0] as MeshInstance3D
			var aabb0: AABB = first.global_transform * first.mesh.get_aabb()
			var small0: bool = aabb0.size[aabb0.get_longest_axis_index()] < SMALL_M
			var rng: Vector2 = _range_for(tag, small0)
			if arr.size() < MIN_BATCH:
				_apply_range(first, rng)
				st["ranged"] = int(st["ranged"]) + 1
				continue
			var mm: MultiMesh = MultiMesh.new()
			mm.transform_format = MultiMesh.TRANSFORM_3D
			mm.mesh = first.mesh
			mm.instance_count = arr.size()
			for i: int in range(arr.size()):
				var m: MeshInstance3D = arr[i] as MeshInstance3D
				mm.set_instance_transform(i, inv_tag * m.global_transform)
				m.visible = false
			var mmi: MultiMeshInstance3D = MultiMeshInstance3D.new()
			mmi.name = "MM_%s_%d" % [String(first.mesh.resource_name if first.mesh.resource_name != "" else first.name), int(st["mmi"])]
			mmi.multimesh = mm
			mmi.material_override = first.material_override
			mmi.cast_shadow = first.cast_shadow
			_apply_range(mmi, rng)
			tag_root.add_child(mmi)
			st["mmi"] = int(st["mmi"]) + 1
			st["batched_mi"] = int(st["batched_mi"]) + arr.size()
			st["instances_in_mmi"] = int(st["instances_in_mmi"]) + arr.size()
			st["surfaces_after"] = int(st["surfaces_after"]) + first.mesh.get_surface_count()
	# Remaining visible single MeshInstance3D nodes.
	var left: Array[MeshInstance3D] = []
	_collect(tower, left)
	st["mi_after"] = left.size()
	for mi2: MeshInstance3D in left:
		st["surfaces_after"] = int(st["surfaces_after"]) + _surfaces(mi2)
	st["ms"] = float(Time.get_ticks_usec() - t0) / 1000.0
	return st
