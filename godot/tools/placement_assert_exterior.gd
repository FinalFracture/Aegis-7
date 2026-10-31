extends SceneTree
## Exterior placement checks for the preface playable area.
##   xvfb-run -a godot --path godot --rendering-driver opengl3 -s res://tools/placement_assert_exterior.gd -- --qa-placement
## Windows (windowed): Godot_v4.7.2-stable_win64_console.exe --path godot -s res://tools/placement_assert_exterior.gd -- --qa-placement
## --qa-placement loads the scene without the hand QA, keeps the player inside, and disables interior streaming.
## Exit 0 all pass, 1 any failed check, a missing scene, or a timeout.

const SCENE_PATH := "res://scenes/preface/preface_playable_area.tscn"
const SETTLE_FRAMES := 60
const TIMEOUT_FRAMES := 600
const FLOOR_BAND := 0.02
const DECAL_ABOVE := 0.03
const RAY_ABOVE := 0.5
const RAY_BELOW := 4.0
const PEN_MAX := 0.02

var _scene: Node = null
var _frames: int = 0
var _done: bool = false
var _pass_n: int = 0
var _fail_n: int = 0


func _initialize() -> void:
	var packed: PackedScene = load(SCENE_PATH) as PackedScene
	if packed == null:
		_done = true
		print("EXT_ASSERT FAIL scene %s load" % SCENE_PATH)
		print("EXT_ASSERT: 0 pass, 1 fail")
		quit(1)
		return
	var inst: Node = packed.instantiate()
	if inst == null:
		_done = true
		print("EXT_ASSERT FAIL scene %s instantiate" % SCENE_PATH)
		print("EXT_ASSERT: 0 pass, 1 fail")
		quit(1)
		return
	# Before add_child so _ready sees it even when --qa-placement is omitted.
	inst.set("_qa_placement", true)
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
		print("EXT_ASSERT FAIL - - timeout frames=%d" % _frames)
		print("EXT_ASSERT: 0 pass, 1 fail")
		quit(1)
		return true
	if _frames < SETTLE_FRAMES:
		return false
	_done = true
	_run_checks()
	return true


func _run_checks() -> void:
	var nodes: Array[Node] = get_nodes_in_group("exterior_placement")
	if nodes.is_empty():
		_bad("-", "-", "no exterior_placement nodes")
		print("EXT_ASSERT: %d pass, %d fail" % [_pass_n, _fail_n])
		quit(1)
		return
	var space: PhysicsDirectSpaceState3D = _direct_space()
	var solids: Array[Dictionary] = []
	for node: Node in nodes:
		if not (node is Node3D):
			_bad(_id_of(node), _asset_of(node), "not Node3D")
			continue
		var prop: Node3D = node as Node3D
		var id: String = _id_of(prop)
		var asset: String = _asset_of(prop)
		var merged: Dictionary = _world_aabb_of(prop)
		if not bool(merged["ok"]):
			_bad(id, asset, "floor aabb=empty node=%s" % String(prop.name))
			continue
		var aabb: AABB = merged["aabb"] as AABB
		if space == null:
			_bad(id, asset, "floor space=null node=%s" % String(prop.name))
		else:
			_check_floor(prop, id, asset, aabb, space)
		# Paving is left out: paving vs paving, curb vs paving, and paving under props are ignored.
		# Surface stickers are not solid props.
		if _is_surface_sticker(asset) or _is_paving(_base(asset)):
			continue
		solids.append({
			"id": id,
			"asset": asset,
			"base": _base(asset),
			"node": String(prop.name),
			"aabb": aabb,
		})
	_check_overlaps(solids)
	print("EXT_ASSERT: %d pass, %d fail" % [_pass_n, _fail_n])
	quit(1 if _fail_n > 0 else 0)


func _check_floor(prop: Node3D, id: String, asset: String, aabb: AABB, space: PhysicsDirectSpaceState3D) -> void:
	var centre: Vector3 = aabb.get_center()
	var top_y: float = aabb.position.y + aabb.size.y
	var bottom_y: float = aabb.position.y
	var origin: Vector3 = Vector3(centre.x, top_y + RAY_ABOVE, centre.z)
	var dest: Vector3 = Vector3(centre.x, bottom_y - RAY_BELOW, centre.z)
	var hit: Dictionary = _ray(space, origin, dest, _collision_rids(prop))
	if hit.is_empty():
		_bad(id, asset, "floor no_ground node=%s from=%s" % [String(prop.name), _v(origin)])
		return
	var hit_y: float = (hit["position"] as Vector3).y
	var gap: float = bottom_y - hit_y
	# Decals and litter sit on the surface: up to 0.03 m above, not buried. 1 mm under is hit noise.
	var decal: bool = _is_decal_or_litter(asset)
	var ok: bool = (gap >= -0.001 and gap <= DECAL_ABOVE) if decal else absf(gap) <= FLOOR_BAND
	if ok:
		_pass_n += 1
		return
	if decal:
		_bad(id, asset, "floor bottom=%s hit=%s gap=%s above_limit=%s node=%s" % [_fmt(bottom_y), _fmt(hit_y), _fmt(gap), _fmt(DECAL_ABOVE), String(prop.name)])
	else:
		_bad(id, asset, "floor bottom=%s hit=%s gap=%s band=%s node=%s" % [_fmt(bottom_y), _fmt(hit_y), _fmt(gap), _fmt(FLOOR_BAND), String(prop.name)])


func _check_overlaps(solids: Array[Dictionary]) -> void:
	for i: int in range(solids.size()):
		var a: Dictionary = solids[i]
		var aa: AABB = a["aabb"] as AABB
		for j: int in range(i + 1, solids.size()):
			var b: Dictionary = solids[j]
			if _skip_pair(String(a["base"]), String(b["base"])):
				continue
			var bb: AABB = b["aabb"] as AABB
			if not aa.intersects(bb):
				continue
			var pen: Vector3 = _penetration(aa, bb)
			if pen.x <= 0.0 or pen.y <= 0.0 or pen.z <= 0.0:
				continue
			# Fail only when the overlap is deeper than 0.02 m on every axis.
			if pen.x > PEN_MAX and pen.y > PEN_MAX and pen.z > PEN_MAX:
				_bad(String(a["id"]), String(a["asset"]), "overlap other=%s id=%s asset=%s pen=%s,%s,%s" % [
					String(b["node"]), String(b["id"]), String(b["asset"]), _fmt(pen.x), _fmt(pen.y), _fmt(pen.z),
				])
			else:
				_pass_n += 1


func _skip_pair(base_a: String, base_b: String) -> bool:
	# Curb corners meet segment ends. The car body overlaps its magnet module and the guideway.
	if (base_a == "ext_curb_corner" and base_b == "ext_curb_segment") or (base_b == "ext_curb_corner" and base_a == "ext_curb_segment"):
		return true
	if base_a == "ext_maglev_car_body" and (base_b == "ext_maglev_magnet_module" or base_b == "ext_maglev_guideway"):
		return true
	if base_b == "ext_maglev_car_body" and (base_a == "ext_maglev_magnet_module" or base_a == "ext_maglev_guideway"):
		return true
	return false


func _penetration(a: AABB, b: AABB) -> Vector3:
	var amax: Vector3 = a.position + a.size
	var bmax: Vector3 = b.position + b.size
	return Vector3(
		minf(amax.x, bmax.x) - maxf(a.position.x, b.position.x),
		minf(amax.y, bmax.y) - maxf(a.position.y, b.position.y),
		minf(amax.z, bmax.z) - maxf(a.position.z, b.position.z)
	)


func _is_surface_sticker(asset: String) -> bool:
	var n: String = asset.to_lower()
	return n.contains("decal") or n.contains("litter") or n.contains("scuff") or n.contains("wear") or n.contains("desire")


func _is_decal_or_litter(asset: String) -> bool:
	var n: String = asset.to_lower()
	return n.contains("decal") or n.contains("litter")


func _is_paving(base: String) -> bool:
	return base.begins_with("ext_paving_")


func _base(asset: String) -> String:
	return asset.get_file().get_basename()


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


func _world_aabb_of(root_n: Node3D) -> Dictionary:
	var merged: AABB = AABB()
	var any: bool = false
	var stack: Array[Node] = [root_n]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if mi.mesh != null:
				var bb: AABB = mi.global_transform * mi.get_aabb()
				if any:
					merged = merged.merge(bb)
				else:
					merged = bb
					any = true
		for ch: Node in curr.get_children():
			stack.append(ch)
	return {"ok": any, "aabb": merged}


func _collision_rids(prop: Node) -> Array[RID]:
	var rids: Array[RID] = []
	var stack: Array[Node] = [prop]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is CollisionObject3D:
			rids.append((curr as CollisionObject3D).get_rid())
		for ch: Node in curr.get_children():
			stack.append(ch)
	return rids


func _ray(space: PhysicsDirectSpaceState3D, from: Vector3, to: Vector3, exclude: Array[RID]) -> Dictionary:
	var rq: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(from, to)
	rq.exclude = exclude
	rq.collide_with_bodies = true
	rq.collide_with_areas = false
	rq.hit_from_inside = false
	return space.intersect_ray(rq)


func _id_of(node: Node) -> String:
	if not node.has_meta("ext_id"):
		return "-"
	return str(int(node.get_meta("ext_id")))


func _asset_of(node: Node) -> String:
	if not node.has_meta("ext_asset"):
		return "-"
	var asset: String = String(node.get_meta("ext_asset"))
	return asset if asset != "" else "-"


func _bad(id: String, asset: String, reason: String) -> void:
	_fail_n += 1
	print("EXT_ASSERT FAIL %s %s %s" % [id, asset, reason])


func _fmt(v: float) -> String:
	return "%.4f" % v


func _v(v: Vector3) -> String:
	return "(%s,%s,%s)" % [_fmt(v.x), _fmt(v.y), _fmt(v.z)]
