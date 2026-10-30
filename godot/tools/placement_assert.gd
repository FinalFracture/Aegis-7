extends SceneTree
## Wall-backed animated-prop placement checks for the preface playable area.
##   xvfb-run -a godot --path godot --rendering-driver opengl3 -s res://tools/placement_assert.gd
## Exit 0 all pass, 1 any failed check, 2 a prop node is missing, 3 still running after 600 frames.
## mesh_clearance and front_zone are checks in that same pass. The summary counts them.

const SCENE_PATH := "res://scenes/preface/preface_playable_area.tscn"
const SETTLE_FRAMES := 60
const TIMEOUT_FRAMES := 600
const FLOOR_EPS := 0.005
const FLOOR_UP := 0.5
const FLOOR_DOWN := 1.0
const FOOT_INSET := 0.05
const WALL_X_INSET := 0.10
const WALL_FRONT := 0.10
const WALL_RAY_LEN := 0.30
const WALL_GAP_MAX := 0.015
const WALL_FAR_GAP := 0.05
const WALL_MIN_HITS := 7
const WALL_MAX_FAR := 2
const WALL_DOT_MIN := 0.9
const CLEAR_SIDE := 0.02
const CLEAR_BACK_IN := 0.02
const CLEAR_TOP := 0.02
const CLEAR_BOTTOM := 0.01
const PAIR_GAP_MIN := 0.02
const FRONT_DEPTH := 0.60
const MESH_REPORT_MAX := 5
const SAT_AXIS_EPS := 1.0e-16

const FALLBACK_SPECS: Array[Dictionary] = [
	{"id": "Prop38_FoldingCounter", "mount": "wall"},
	{"id": "Prop39_FlipSeat", "mount": "wall"},
	{"id": "Prop42_Substation", "mount": "wall"},
	{"id": "Prop43_SparesDispenser", "mount": "wall"},
]

var _scene: Node = null
var _frames: int = 0
var _done: bool = false
var _pass_n: int = 0
var _fail_n: int = 0
var _missing_n: int = 0
# World-space triangles, keyed by gathered-mesh index. Filled only after an AABB overlap.
var _face_cache: Dictionary = {}


func _initialize() -> void:
	var packed: PackedScene = load(SCENE_PATH) as PackedScene
	if packed == null:
		print("FAIL scene load path=%s" % SCENE_PATH)
		return
	var inst: Node = packed.instantiate()
	if inst == null:
		print("FAIL scene load path=%s instantiate" % SCENE_PATH)
		return
	root.add_child(inst)
	# Headless boot sets this and quits the tree at frame 4, before the checks run.
	if "_validate_only" in inst:
		inst.set("_validate_only", false)
	_scene = inst


func _process(_delta: float) -> bool:
	if _done:
		return true
	_frames += 1
	if _frames >= TIMEOUT_FRAMES:
		_done = true
		print("FAIL timeout timeout frames=%d" % _frames)
		print("PLACEMENT_ASSERT: 0 pass, 1 fail")
		quit(3)
		return true
	if _frames < SETTLE_FRAMES:
		return false
	_done = true
	_run_checks()
	return true


func _run_checks() -> void:
	var specs: Array[Dictionary] = _specs_from_scene(_scene)
	if specs.is_empty():
		specs = FALLBACK_SPECS
	var space: PhysicsDirectSpaceState3D = _direct_space()
	_face_cache.clear()
	var meshes: Array[Dictionary] = _gather_scene_meshes(_animated_prop_roots(specs))
	var placed: Array[Dictionary] = []
	for spec: Dictionary in specs:
		var id: String = String(spec.get("id", ""))
		if id == "":
			_missing_n += 1
			_report(false, "?", "missing", "id=empty")
			continue
		var node: Node = null
		if _scene != null:
			node = _scene.find_child(id, true, false)
		if node == null or not (node is Node3D):
			_missing_n += 1
			_report(false, id, "missing", "node=null")
			placed.append({"id": id, "ok": false})
			continue
		var prop: Node3D = node as Node3D
		var wall_mount: bool = String(spec.get("mount", "")) == "wall"
		var merged: Dictionary = _local_aabb(prop)
		if not bool(merged["ok"]):
			_report(false, id, "floor", "aabb=empty")
			if wall_mount:
				_report(false, id, "wall", "aabb=empty")
			_report(false, id, "clearance", "aabb=empty")
			_report(false, id, "mesh_clearance", "aabb=empty")
			if wall_mount:
				_report(false, id, "front_zone", "aabb=empty")
			placed.append({"id": id, "ok": false})
			continue
		var aabb: AABB = merged["aabb"] as AABB
		var exclude: Array[RID] = _collision_rids(prop)
		var world_bb: AABB = _world_aabb(prop, aabb)
		if space == null:
			_report(false, id, "floor", "space=null")
			if wall_mount:
				_report(false, id, "wall", "space=null")
			_report(false, id, "clearance", "space=null")
			_check_mesh_clearance(prop, aabb, meshes)
			if wall_mount:
				_check_front_zone(prop, aabb, meshes, null, exclude)
		else:
			_check_floor(prop, aabb, world_bb, space, exclude)
			if wall_mount:
				_check_wall(prop, aabb, space, exclude)
			_check_clearance(prop, aabb, space, exclude)
			_check_mesh_clearance(prop, aabb, meshes)
			if wall_mount:
				_check_front_zone(prop, aabb, meshes, space, exclude)
		placed.append({"id": id, "ok": true, "world": world_bb})
	_check_pairs(placed)
	var code: int = 0
	if _missing_n > 0:
		code = 2
	elif _fail_n > 0:
		code = 1
	print("PLACEMENT_ASSERT: %d pass, %d fail" % [_pass_n, _fail_n])
	quit(code)


func _specs_from_scene(scene_root: Node) -> Array[Dictionary]:
	if scene_root == null:
		return []
	# Const lives on the scene script. Instance property first, then the constant map.
	if "ANIMATED_PROP_SPECS" in scene_root:
		var via_inst: Array[Dictionary] = _coerce_specs(scene_root.get("ANIMATED_PROP_SPECS"))
		if not via_inst.is_empty():
			return via_inst
	var scr: Script = scene_root.get_script() as Script
	if scr != null:
		var cmap: Dictionary = scr.get_script_constant_map()
		if cmap.has("ANIMATED_PROP_SPECS"):
			return _coerce_specs(cmap["ANIMATED_PROP_SPECS"])
	return []


func _coerce_specs(raw: Variant) -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	if raw is Array:
		for item: Variant in raw as Array:
			if item is Dictionary:
				out.append(item as Dictionary)
	return out


func _direct_space() -> PhysicsDirectSpaceState3D:
	if _scene is Node3D and (_scene as Node3D).is_inside_tree():
		var world: World3D = (_scene as Node3D).get_world_3d()
		if world != null:
			return world.direct_space_state
	var vp: Viewport = root as Viewport
	if vp != null:
		var world2: World3D = vp.find_world_3d()
		if world2 != null:
			return world2.direct_space_state
	return null


func _local_aabb(prop: Node3D) -> Dictionary:
	var merged: AABB = AABB()
	var any: bool = false
	var stack: Array[Node] = [prop]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if mi.mesh != null:
				var to_local: Transform3D = prop.global_transform.affine_inverse() * mi.global_transform
				var bb: AABB = to_local * mi.get_aabb()
				if any:
					merged = merged.merge(bb)
				else:
					merged = bb
					any = true
		for child: Node in curr.get_children():
			stack.append(child)
	return {"ok": any, "aabb": merged}


func _world_aabb(prop: Node3D, local_bb: AABB) -> AABB:
	var xf: Transform3D = prop.global_transform
	var world_bb: AABB = AABB(xf * local_bb.get_endpoint(0), Vector3.ZERO)
	for i: int in range(1, 8):
		world_bb = world_bb.expand(xf * local_bb.get_endpoint(i))
	return world_bb


func _collision_rids(prop: Node) -> Array[RID]:
	# Prop collider only. Every other body, including the wall and the floor, stays in the query.
	var rids: Array[RID] = []
	var stack: Array[Node] = [prop]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is CollisionObject3D:
			rids.append((curr as CollisionObject3D).get_rid())
		for child: Node in curr.get_children():
			stack.append(child)
	return rids


func _ray(space: PhysicsDirectSpaceState3D, from: Vector3, to: Vector3, exclude: Array[RID]) -> Dictionary:
	var rq: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(from, to)
	rq.exclude = exclude
	rq.collide_with_bodies = true
	rq.collide_with_areas = false
	rq.hit_from_inside = false
	return space.intersect_ray(rq)


func _check_floor(prop: Node3D, aabb: AABB, world_bb: AABB, space: PhysicsDirectSpaceState3D, exclude: Array[RID]) -> void:
	var id: String = String(prop.name)
	var prop_min_y: float = world_bb.position.y
	var bmin: Vector3 = aabb.position
	var bmax: Vector3 = aabb.position + aabb.size
	var yb: float = bmin.y
	var pts: Array[Vector3] = []
	pts.append(Vector3(bmin.x + FOOT_INSET, yb, bmin.z + FOOT_INSET))
	pts.append(Vector3(bmax.x - FOOT_INSET, yb, bmin.z + FOOT_INSET))
	pts.append(Vector3(bmin.x + FOOT_INSET, yb, bmax.z - FOOT_INSET))
	pts.append(Vector3(bmax.x - FOOT_INSET, yb, bmax.z - FOOT_INSET))
	pts.append(Vector3((bmin.x + bmax.x) * 0.5, yb, (bmin.z + bmax.z) * 0.5))
	var hit_n: int = 0
	var floor_y: float = -INF
	var max_abs: float = 0.0
	var dev_ok: bool = true
	for lp: Vector3 in pts:
		var wp: Vector3 = prop.global_transform * lp
		var hit: Dictionary = _ray(space, wp + Vector3(0.0, FLOOR_UP, 0.0), wp + Vector3(0.0, -FLOOR_DOWN, 0.0), exclude)
		if hit.is_empty():
			continue
		hit_n += 1
		var hy: float = (hit["position"] as Vector3).y
		floor_y = maxf(floor_y, hy)
		var dev: float = absf(prop_min_y - hy)
		max_abs = maxf(max_abs, dev)
		if dev > FLOOR_EPS:
			dev_ok = false
	var sunk: bool = hit_n > 0 and prop_min_y < floor_y - FLOOR_EPS
	var ok: bool = hit_n >= 3 and dev_ok and not sunk
	var fy_txt: String = "none"
	if hit_n > 0:
		fy_txt = _fmt(floor_y)
	_report(ok, id, "floor", "prop_min_y=%s floor_y=%s hits=%d/5 max_abs=%s sunk=%d local_min=%s local_max=%s" % [
		_fmt(prop_min_y), fy_txt, hit_n, _fmt(max_abs), 1 if sunk else 0, _v(bmin), _v(bmax)
	])


func _check_wall(prop: Node3D, aabb: AABB, space: PhysicsDirectSpaceState3D, exclude: Array[RID]) -> void:
	var id: String = String(prop.name)
	var z_back: float = aabb.position.z
	var x_min: float = aabb.position.x
	var x_max: float = x_min + aabb.size.x
	var y_min: float = aabb.position.y
	var height: float = aabb.size.y
	var xs: Array[float] = []
	xs.append(x_min + WALL_X_INSET)
	xs.append((x_min + x_max) * 0.5)
	xs.append(x_max - WALL_X_INSET)
	var ys: Array[float] = []
	ys.append(y_min + height * 0.20)
	ys.append(y_min + height * 0.50)
	ys.append(y_min + height * 0.80)
	var plus_z: Vector3 = prop.global_basis.z
	if plus_z.length_squared() < 0.0000001:
		_report(false, id, "wall", "basis_z=0")
		return
	plus_z = plus_z.normalized()
	var hits: int = 0
	var far_or_miss: int = 0
	var gap_min: float = INF
	var gap_max: float = -INF
	var min_dot: float = INF
	var gap_ok: bool = true
	var normal_ok: bool = true
	for x: float in xs:
		for y: float in ys:
			var on_plane: Vector3 = prop.global_transform * Vector3(x, y, z_back)
			# 0.10 m in front of the back plane (+local Z), then 0.30 m along local -Z.
			var start: Vector3 = on_plane + plus_z * WALL_FRONT
			var end: Vector3 = start - plus_z * WALL_RAY_LEN
			var hit: Dictionary = _ray(space, start, end, exclude)
			if hit.is_empty():
				far_or_miss += 1
				continue
			hits += 1
			var dist: float = start.distance_to(hit["position"] as Vector3)
			var gap: float = dist - WALL_FRONT
			gap_min = minf(gap_min, gap)
			gap_max = maxf(gap_max, gap)
			if gap < 0.0 or gap > WALL_GAP_MAX:
				gap_ok = false
			if gap > WALL_FAR_GAP:
				far_or_miss += 1
			var nrm: Vector3 = hit["normal"] as Vector3
			if nrm.length_squared() > 0.0000001:
				nrm = nrm.normalized()
			var dot_n: float = nrm.dot(plus_z)
			min_dot = minf(min_dot, dot_n)
			if dot_n <= WALL_DOT_MIN:
				normal_ok = false
	var ok: bool = hits >= WALL_MIN_HITS and far_or_miss <= WALL_MAX_FAR and gap_ok and normal_ok
	var gap_txt: String = "none"
	var dot_txt: String = "none"
	if hits > 0:
		gap_txt = "[%s,%s]" % [_fmt(gap_min), _fmt(gap_max)]
		dot_txt = _fmt(min_dot)
	_report(ok, id, "wall", "hits=%d/9 gap=%s min_dot=%s far_or_miss=%d" % [hits, gap_txt, dot_txt, far_or_miss])


func _check_clearance(prop: Node3D, aabb: AABB, space: PhysicsDirectSpaceState3D, exclude: Array[RID]) -> void:
	var id: String = String(prop.name)
	var box: AABB = _clearance_box(aabb)
	if _fail_if_degenerate(id, "clearance", box):
		return
	var names: PackedStringArray = _query_box(prop, box, space, exclude)
	if names.is_empty():
		_report(true, id, "clearance", "overlaps=0")
	else:
		_report(false, id, "clearance", "overlaps=%d name=%s" % [names.size(), ",".join(names)])


func _check_mesh_clearance(prop: Node3D, aabb: AABB, meshes: Array[Dictionary]) -> void:
	var id: String = String(prop.name)
	var box: AABB = _clearance_box(aabb)
	if _fail_if_degenerate(id, "mesh_clearance", box):
		return
	var hit_info: Dictionary = _mesh_offenders(prop, box, meshes)
	var total: int = int(hit_info["total"])
	if total <= 0:
		_report(true, id, "mesh_clearance", "overlaps=0")
	else:
		_report(false, id, "mesh_clearance", _mesh_hit_text(hit_info))


func _check_front_zone(prop: Node3D, aabb: AABB, meshes: Array[Dictionary], space: PhysicsDirectSpaceState3D, exclude: Array[RID]) -> void:
	var id: String = String(prop.name)
	var box: AABB = _front_box(aabb)
	if _fail_if_degenerate(id, "front_zone", box):
		return
	var hit_info: Dictionary = _mesh_offenders(prop, box, meshes)
	var mesh_n: int = int(hit_info["total"])
	if space == null:
		var missing: String = "space=null"
		if mesh_n > 0:
			missing = "%s %s" % [missing, _mesh_hit_text(hit_info)]
		_report(false, id, "front_zone", missing)
		return
	var names: PackedStringArray = _query_box(prop, box, space, exclude)
	if mesh_n <= 0 and names.is_empty():
		_report(true, id, "front_zone", "overlaps=0")
		return
	var parts: PackedStringArray = PackedStringArray()
	if mesh_n > 0:
		parts.append(_mesh_hit_text(hit_info))
	if not names.is_empty():
		parts.append("colliders=%d name=%s" % [names.size(), ",".join(names)])
	_report(false, id, "front_zone", " ".join(parts))


# Same shell the collider query uses. Back (-Z) pulls in so the mounting wall stays outside.
# Bottom lifts off the floor. ±X, +Z front, and +Y top grow by the clearance margin.
func _clearance_box(aabb: AABB) -> AABB:
	var bmin: Vector3 = aabb.position
	var bmax: Vector3 = aabb.end
	var gmin: Vector3 = Vector3(bmin.x - CLEAR_SIDE, bmin.y + CLEAR_BOTTOM, bmin.z + CLEAR_BACK_IN)
	var gmax: Vector3 = Vector3(bmax.x + CLEAR_SIDE, bmax.y + CLEAR_TOP, bmax.z + CLEAR_SIDE)
	return AABB(gmin, gmax - gmin)


# Wall mounts only. Local +Z is the front. Nothing may stand in this slab.
func _front_box(aabb: AABB) -> AABB:
	var bmin: Vector3 = aabb.position
	var bmax: Vector3 = aabb.end
	var gmin: Vector3 = Vector3(bmin.x, bmin.y + CLEAR_BOTTOM, bmax.z)
	var gmax: Vector3 = Vector3(bmax.x, bmax.y, bmax.z + FRONT_DEPTH)
	return AABB(gmin, gmax - gmin)


func _fail_if_degenerate(id: String, check: String, box: AABB) -> bool:
	var sz: Vector3 = box.size
	if sz.x <= 0.0 or sz.y <= 0.0 or sz.z <= 0.0:
		_report(false, id, check, "degenerate size=%s" % _v(sz))
		return true
	return false


func _query_box(prop: Node3D, box: AABB, space: PhysicsDirectSpaceState3D, exclude: Array[RID]) -> PackedStringArray:
	var center: Vector3 = box.position + box.size * 0.5
	var shape: BoxShape3D = BoxShape3D.new()
	shape.size = box.size
	var q: PhysicsShapeQueryParameters3D = PhysicsShapeQueryParameters3D.new()
	q.shape = shape
	q.transform = prop.global_transform * Transform3D(Basis.IDENTITY, center)
	q.exclude = exclude
	q.margin = 0.0
	q.collide_with_bodies = true
	q.collide_with_areas = false
	var names: PackedStringArray = PackedStringArray()
	var seen: Array[RID] = []
	var results: Array = space.intersect_shape(q, 32)
	for hv: Variant in results:
		if not (hv is Dictionary):
			continue
		var hit: Dictionary = hv as Dictionary
		var rid: RID = _hit_rid(hit)
		if rid.is_valid() and _rid_in(exclude, rid):
			continue
		if rid.is_valid():
			if _rid_in(seen, rid):
				continue
			seen.append(rid)
		var col: Object = hit.get("collider") as Object
		names.append(_body_name(col))
	return names


func _animated_prop_roots(specs: Array[Dictionary]) -> Array[Node]:
	var roots: Array[Node] = []
	if _scene == null:
		return roots
	for spec: Dictionary in specs:
		var id: String = String(spec.get("id", ""))
		if id == "":
			continue
		var node: Node = _scene.find_child(id, true, false)
		if node != null:
			roots.append(node)
	return roots


func _gather_scene_meshes(prop_roots: Array[Node]) -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	if _scene == null:
		return out
	var stack: Array[Node] = [_scene]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if _is_prop_root(curr, prop_roots):
			continue
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if mi.mesh != null:
				var xf: Transform3D = mi.global_transform
				out.append({
					"name": _body_name(mi),
					"mesh": mi.mesh,
					"xf": xf,
					"world_aabb": xf * mi.get_aabb(),
				})
		for child: Node in curr.get_children():
			stack.append(child)
	return out


func _is_prop_root(node: Node, prop_roots: Array[Node]) -> bool:
	for root: Node in prop_roots:
		if node == root:
			return true
	return false


func _world_faces(index: int, entry: Dictionary) -> PackedVector3Array:
	if _face_cache.has(index):
		return _face_cache[index] as PackedVector3Array
	var mesh: Mesh = entry["mesh"] as Mesh
	var xf: Transform3D = entry["xf"] as Transform3D
	var src: PackedVector3Array = mesh.get_faces()
	var world: PackedVector3Array = PackedVector3Array()
	world.resize(src.size())
	for i: int in src.size():
		world[i] = xf * src[i]
	_face_cache[index] = world
	return world


# Triangles are tested in the prop's local frame. Faces stay cached in world space.
func _mesh_offenders(prop: Node3D, box: AABB, meshes: Array[Dictionary]) -> Dictionary:
	var world_box: AABB = prop.global_transform * box
	var to_prop: Transform3D = prop.global_transform.affine_inverse()
	var shown: Array[Dictionary] = []
	var total: int = 0
	for index: int in range(meshes.size()):
		var entry: Dictionary = meshes[index]
		if not _aabb_overlaps(entry["world_aabb"] as AABB, world_box):
			continue
		var faces: PackedVector3Array = _world_faces(index, entry)
		var tri_n: int = int(faces.size() / 3)
		var hits: int = 0
		var centroid: Vector3 = Vector3.ZERO
		var capped: bool = shown.size() >= MESH_REPORT_MAX
		for t: int in range(tri_n):
			var i: int = t * 3
			var w0: Vector3 = faces[i]
			var w1: Vector3 = faces[i + 1]
			var w2: Vector3 = faces[i + 2]
			if not _tri_hits_aabb(to_prop * w0, to_prop * w1, to_prop * w2, box):
				continue
			if hits == 0:
				centroid = (w0 + w1 + w2) / 3.0
			hits += 1
			if capped:
				break
		if hits <= 0:
			continue
		total += 1
		if not capped:
			shown.append({"name": String(entry["name"]), "tris": hits, "centroid": centroid})
	return {"total": total, "shown": shown}


func _mesh_hit_text(hit_info: Dictionary) -> String:
	var shown: Array = hit_info["shown"] as Array
	var total: int = int(hit_info["total"])
	var parts: PackedStringArray = PackedStringArray()
	var n: int = shown.size()
	if n > MESH_REPORT_MAX:
		n = MESH_REPORT_MAX
	for i: int in range(n):
		var hit: Dictionary = shown[i] as Dictionary
		parts.append("%s tris=%d centroid=%s" % [String(hit["name"]), int(hit["tris"]), _v(hit["centroid"] as Vector3)])
	var text: String = "overlaps=%d mesh=%s" % [total, ";".join(parts)]
	if total > n:
		text += " more=%d" % (total - n)
	return text


func _aabb_overlaps(a: AABB, b: AABB) -> bool:
	if a.end.x < b.position.x or b.end.x < a.position.x:
		return false
	if a.end.y < b.position.y or b.end.y < a.position.y:
		return false
	if a.end.z < b.position.z or b.end.z < a.position.z:
		return false
	return true


# 13-axis SAT. A triangle-vs-AABB bounds test is not a hit: large hull triangles false-positive.
func _tri_hits_aabb(v0: Vector3, v1: Vector3, v2: Vector3, box: AABB) -> bool:
	var half: Vector3 = box.size * 0.5
	var origin: Vector3 = box.position + half
	var p0: Vector3 = v0 - origin
	var p1: Vector3 = v1 - origin
	var p2: Vector3 = v2 - origin
	if _axis_separates(p0, p1, p2, Vector3(1.0, 0.0, 0.0), half):
		return false
	if _axis_separates(p0, p1, p2, Vector3(0.0, 1.0, 0.0), half):
		return false
	if _axis_separates(p0, p1, p2, Vector3(0.0, 0.0, 1.0), half):
		return false
	var normal: Vector3 = (p1 - p0).cross(p2 - p0)
	if normal.length_squared() > SAT_AXIS_EPS and _axis_separates(p0, p1, p2, normal, half):
		return false
	var e0: Vector3 = p1 - p0
	var e1: Vector3 = p2 - p1
	var e2: Vector3 = p0 - p2
	if _edge_crosses_separate(p0, p1, p2, e0, half):
		return false
	if _edge_crosses_separate(p0, p1, p2, e1, half):
		return false
	if _edge_crosses_separate(p0, p1, p2, e2, half):
		return false
	return true


func _edge_crosses_separate(p0: Vector3, p1: Vector3, p2: Vector3, edge: Vector3, half: Vector3) -> bool:
	# edge × (1,0,0), edge × (0,1,0), edge × (0,0,1). A near-zero axis is parallel and skipped.
	var ax: Vector3 = Vector3(0.0, edge.z, -edge.y)
	if ax.length_squared() > SAT_AXIS_EPS and _axis_separates(p0, p1, p2, ax, half):
		return true
	var ay: Vector3 = Vector3(-edge.z, 0.0, edge.x)
	if ay.length_squared() > SAT_AXIS_EPS and _axis_separates(p0, p1, p2, ay, half):
		return true
	var az: Vector3 = Vector3(edge.y, -edge.x, 0.0)
	if az.length_squared() > SAT_AXIS_EPS and _axis_separates(p0, p1, p2, az, half):
		return true
	return false


func _axis_separates(p0: Vector3, p1: Vector3, p2: Vector3, axis: Vector3, half: Vector3) -> bool:
	var radius: float = half.x * absf(axis.x) + half.y * absf(axis.y) + half.z * absf(axis.z)
	var d0: float = p0.dot(axis)
	var d1: float = p1.dot(axis)
	var d2: float = p2.dot(axis)
	var mn: float = minf(d0, minf(d1, d2))
	var mx: float = maxf(d0, maxf(d1, d2))
	return mn > radius or mx < -radius


func _check_pairs(placed: Array[Dictionary]) -> void:
	for i: int in range(placed.size()):
		for j: int in range(i + 1, placed.size()):
			var a: Dictionary = placed[i]
			var b: Dictionary = placed[j]
			var id: String = "%s+%s" % [String(a["id"]), String(b["id"])]
			if not bool(a.get("ok", false)) or not bool(b.get("ok", false)):
				_report(false, id, "pair_gap", "gap=missing")
				continue
			var gap: float = _separation(a["world"] as AABB, b["world"] as AABB)
			_report(gap >= PAIR_GAP_MIN, id, "pair_gap", "gap=%s" % _fmt(gap))


func _separation(a: AABB, b: AABB) -> float:
	var amax: Vector3 = a.position + a.size
	var bmax: Vector3 = b.position + b.size
	var dx: float = maxf(maxf(a.position.x - bmax.x, b.position.x - amax.x), 0.0)
	var dy: float = maxf(maxf(a.position.y - bmax.y, b.position.y - amax.y), 0.0)
	var dz: float = maxf(maxf(a.position.z - bmax.z, b.position.z - amax.z), 0.0)
	return Vector3(dx, dy, dz).length()


func _hit_rid(hit: Dictionary) -> RID:
	var rid_v: Variant = hit.get("rid", RID())
	if rid_v is RID:
		return rid_v as RID
	var col: Object = hit.get("collider") as Object
	if col is CollisionObject3D:
		return (col as CollisionObject3D).get_rid()
	return RID()


func _rid_in(rids: Array[RID], rid: RID) -> bool:
	for have: RID in rids:
		if have == rid:
			return true
	return false


func _body_name(col: Object) -> String:
	if col is Node:
		var n: Node = col as Node
		var parent: Node = n.get_parent()
		if parent != null:
			return "%s/%s" % [String(parent.name), String(n.name)]
		return String(n.name)
	return "Object"


func _report(ok: bool, id: String, check: String, detail: String) -> void:
	if ok:
		_pass_n += 1
		print("PASS %s %s %s" % [id, check, detail])
	else:
		_fail_n += 1
		print("FAIL %s %s %s" % [id, check, detail])


func _fmt(v: float) -> String:
	return "%.4f" % v


func _v(v: Vector3) -> String:
	return "(%s,%s,%s)" % [_fmt(v.x), _fmt(v.y), _fmt(v.z)]
