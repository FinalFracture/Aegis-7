extends SceneTree
## Exterior placement checks for the preface playable area.
##   xvfb-run -a godot --path godot --rendering-driver opengl3 -s res://tools/placement_assert_exterior.gd -- --qa-placement
## Windows (windowed): Godot_v4.7.2-stable_win64_console.exe --path godot -s res://tools/placement_assert_exterior.gd -- --qa-placement
## --qa-placement loads the scene without the hand QA, keeps the player inside, and disables interior streaming.
## Exit 0 all pass, 1 any failed check, a missing scene, or a timeout.

const SCENE_PATH := "res://scenes/preface/preface_playable_area.tscn"
const TIMEOUT_FRAMES := 600
const FLOOR_BAND := 0.02
const DECAL_ABOVE := 0.03
const PEN_MAX := 0.010
const SNAP_ABOVE := 0.3
# Match the spawn snap: a corner on the east guardrail (top y 1.245) is not support.
const SUPPORT_LIFT := 0.40
const SNAP_DEPTH := 12.0
const CORNER_INSET := 0.05
const KIND_GROUND := 0
const KIND_SOLID := 1
const KIND_CAR := 2
const KIND_DECAL := 3

var _scene: Node = null
var _frames: int = 0
var _done: bool = false
var _spawn_signal: bool = false
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
	if inst.has_signal("exterior_spawned"):
		inst.connect("exterior_spawned", Callable(self, "_on_exterior_spawned"))
	root.add_child(inst)
	# Headless boot sets this and quits the tree at frame 4, before the checks run.
	if "_validate_only" in inst:
		inst.set("_validate_only", false)
	_scene = inst


func _on_exterior_spawned() -> void:
	_spawn_signal = true


func _exterior_ready() -> bool:
	if _spawn_signal:
		return true
	if _scene == null:
		return false
	return bool(_scene.get_meta("exterior_spawned", false))


func _process(_delta: float) -> bool:
	if _done:
		return true
	_frames += 1
	if not _exterior_ready():
		if _frames >= TIMEOUT_FRAMES:
			_done = true
			print("EXT_ASSERT FAIL - - timeout frames=%d" % _frames)
			print("EXT_ASSERT: 0 pass, 1 fail")
			quit(1)
			return true
		return false
	_done = true
	_run_checks()
	return true


func _run_checks() -> void:
	var nodes: Array[Node] = get_nodes_in_group("exterior_placement")
	_check_ts4_row()
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


## #49 is the middle slot of the west id-25 row, not a hidden scene TS-4.
func _check_ts4_row() -> void:
	var neighbours: Array[Node3D] = []
	var dead: Node3D = null
	var wear: Node3D = null
	for node: Node in get_nodes_in_group("exterior_placement"):
		if not (node is Node3D):
			continue
		var prop := node as Node3D
		var id := _id_of(prop)
		var base := _base(_asset_of(prop))
		if id == "25" and base == "hydro_planter_tiered_exterior":
			neighbours.append(prop)
		elif id == "49" and base == "ext_ts4_dead_foliage":
			dead = prop
		elif id == "49" and base == "ext_ts4_wear_decal":
			wear = prop
	if neighbours.size() != 2 or dead == null or wear == null:
		_bad("49", "ts4", "row neighbours=%d dead=%s wear=%s" % [neighbours.size(), str(dead != null), str(wear != null)])
		return
	var z_mid := (neighbours[0].global_position.z + neighbours[1].global_position.z) * 0.5
	var pieces: Array[Node3D] = [dead, wear]
	var aligned := true
	for piece: Node3D in pieces:
		var x_ok := true
		var rot_ok := true
		for nb: Node3D in neighbours:
			if absf(piece.global_position.x - nb.global_position.x) > 0.01:
				x_ok = false
			if _yaw_delta(piece.rotation_degrees.y, nb.rotation_degrees.y) > 0.1:
				rot_ok = false
		var z_ok := absf(piece.global_position.z - z_mid) <= 0.01
		if x_ok and rot_ok and z_ok:
			continue
		aligned = false
		_bad("49", _asset_of(piece), "ts4 slot x=%s z=%s rot=%s mid_z=%s nb_x=%s,%s nb_z=%s,%s nb_rot=%s,%s" % [
			_fmt(piece.global_position.x), _fmt(piece.global_position.z), _fmt(piece.rotation_degrees.y), _fmt(z_mid),
			_fmt(neighbours[0].global_position.x), _fmt(neighbours[1].global_position.x),
			_fmt(neighbours[0].global_position.z), _fmt(neighbours[1].global_position.z),
			_fmt(neighbours[0].rotation_degrees.y), _fmt(neighbours[1].rotation_degrees.y),
		])
	if aligned:
		_pass_n += 1


func _yaw_delta(a: float, b: float) -> float:
	return absf(fposmod(a - b + 180.0, 360.0) - 180.0)


func _check_floor(prop: Node3D, id: String, asset: String, aabb: AABB, space: PhysicsDirectSpaceState3D) -> void:
	var bottom_y: float = aabb.position.y
	# Same samples and exclusions as the spawn snap: centre plus four inset corners.
	# Support is the highest hit still within SUPPORT_LIFT of the centre hit.
	var hit: Dictionary = _max_surface_y(prop, aabb, _floor_exclude(prop, asset), space)
	var have_hit: bool = bool(hit["ok"])
	var hit_y: float = float(hit["y"])
	# Car body bottom is the magnet top, even when the centre ray lands on the guideway.
	if _base(asset) == "ext_maglev_car_body":
		var mag: Dictionary = _magnet_top_for_car(aabb)
		if bool(mag["ok"]):
			hit_y = float(mag["y"])
			have_hit = true
	if not have_hit:
		var centre: Vector3 = aabb.get_center()
		_bad(id, asset, "floor no_ground node=%s from=%s" % [String(prop.name), _v(Vector3(centre.x, aabb.position.y + aabb.size.y + SNAP_ABOVE, centre.z))])
		return
	var gap: float = bottom_y - hit_y
	# Decals and litter sit on the surface: 0..0.03 m above, never buried.
	var decal: bool = _is_decal_or_litter(asset)
	var ok: bool = (gap >= 0.0 and gap <= DECAL_ABOVE) if decal else absf(gap) <= FLOOR_BAND
	if ok:
		_pass_n += 1
		return
	if decal:
		_bad(id, asset, "floor bottom=%s hit=%s gap=%s above_limit=%s node=%s" % [_fmt(bottom_y), _fmt(hit_y), _fmt(gap), _fmt(DECAL_ABOVE), String(prop.name)])
	else:
		_bad(id, asset, "floor bottom=%s hit=%s gap=%s band=%s node=%s" % [_fmt(bottom_y), _fmt(hit_y), _fmt(gap), _fmt(FLOOR_BAND), String(prop.name)])


func _spawn_kind(asset: String) -> int:
	if _is_surface_sticker(asset):
		return KIND_DECAL
	var base: String = _base(asset)
	if base == "ext_maglev_car_body":
		return KIND_CAR
	if base.begins_with("ext_paving_") or base == "ext_platform_infill" or base == "ext_kerb_ramp" or base == "ext_canal_edge" or base == "ext_maglev_guideway":
		return KIND_GROUND
	return KIND_SOLID


func _floor_exclude(prop: Node, asset: String) -> Array[RID]:
	# Mirror the spawn snap: ground-like props see only the sector ground; solids see ground and paving,
	# not other solids; cars keep their magnet; scuffs ignore the car and magnet stacked on the guideway.
	# The prop's own bodies are always excluded.
	var exclude: Array[RID] = _collision_rids(prop)
	var kind: int = _spawn_kind(asset)
	if kind == KIND_GROUND:
		for node: Node in get_nodes_in_group("exterior_placement"):
			exclude.append_array(_collision_rids(node))
		return exclude
	if _base(asset) == "ext_track_scuff_guideway":
		exclude.append_array(_rids_for_bases(["ext_maglev_car_body", "ext_maglev_magnet_module"]))
	if kind == KIND_DECAL:
		return exclude
	for node: Node in get_nodes_in_group("exterior_placement"):
		if node == prop:
			continue
		var other: String = _asset_of(node)
		var other_kind: int = _spawn_kind(other)
		if other_kind == KIND_GROUND or other_kind == KIND_DECAL:
			continue
		if kind == KIND_CAR and _base(other) == "ext_maglev_magnet_module":
			continue
		exclude.append_array(_collision_rids(node))
	return exclude


func _max_surface_y(prop: Node3D, aabb: AABB, exclude: Array[RID], space: PhysicsDirectSpaceState3D) -> Dictionary:
	var start_y: float = aabb.position.y + aabb.size.y + SNAP_ABOVE
	var end_y: float = prop.global_position.y - SNAP_DEPTH
	var pts: Array[Vector2] = []
	var centre: Vector3 = aabb.get_center()
	pts.append(Vector2(centre.x, centre.z))
	var inset_x: float = minf(CORNER_INSET, maxf(aabb.size.x * 0.49, 0.0))
	var inset_z: float = minf(CORNER_INSET, maxf(aabb.size.z * 0.49, 0.0))
	var x0: float = aabb.position.x + inset_x
	var x1: float = aabb.position.x + aabb.size.x - inset_x
	var z0: float = aabb.position.z + inset_z
	var z1: float = aabb.position.z + aabb.size.z - inset_z
	pts.append(Vector2(x0, z0))
	pts.append(Vector2(x1, z0))
	pts.append(Vector2(x0, z1))
	pts.append(Vector2(x1, z1))
	var hits: Array[float] = []
	var center_y: float = 0.0
	var have_center: bool = false
	for i: int in range(pts.size()):
		var p: Vector2 = pts[i]
		var hit: Dictionary = _ray(space, Vector3(p.x, start_y, p.y), Vector3(p.x, end_y, p.y), exclude)
		if hit.is_empty() or _collider_is_under(prop, hit.get("collider")):
			continue
		var hy: float = (hit["position"] as Vector3).y
		if i == 0:
			center_y = hy
			have_center = true
		hits.append(hy)
	return _support_from_hits(hits, center_y, have_center)


func _support_from_hits(hits: Array[float], center_y: float, have_center: bool) -> Dictionary:
	if hits.is_empty():
		return {"ok": false, "y": 0.0}
	var anchor: float = center_y if have_center else hits[0]
	if not have_center:
		for h: float in hits:
			anchor = minf(anchor, h)
	var best: float = -INF
	var any: bool = false
	for h2: float in hits:
		if h2 > anchor + SUPPORT_LIFT:
			continue
		if not any or h2 > best:
			best = h2
			any = true
	if not any:
		return {"ok": true, "y": anchor}
	return {"ok": true, "y": best}


func _collider_is_under(root_n: Node, collider: Object) -> bool:
	if not (collider is Node):
		return false
	var n: Node = collider as Node
	while n != null:
		if n == root_n:
			return true
		n = n.get_parent()
	return false


func _magnet_top_for_car(car_aabb: AABB) -> Dictionary:
	var c: Vector3 = car_aabb.get_center()
	var best_d: float = INF
	var best_y: float = 0.0
	var any: bool = false
	for node: Node in get_nodes_in_group("exterior_placement"):
		if not (node is Node3D):
			continue
		if _base(_asset_of(node)) != "ext_maglev_magnet_module":
			continue
		var merged: Dictionary = _world_aabb_of(node as Node3D)
		if not bool(merged["ok"]):
			continue
		var bb: AABB = merged["aabb"] as AABB
		var mc: Vector3 = bb.get_center()
		var d: float = Vector2(c.x, c.z).distance_to(Vector2(mc.x, mc.z))
		if d < best_d:
			best_d = d
			best_y = bb.position.y + bb.size.y
			any = true
	if not any or best_d > 2.0:
		return {"ok": false, "y": 0.0}
	return {"ok": true, "y": best_y}


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
			var deep: bool = pen.x > PEN_MAX and pen.y > PEN_MAX and pen.z > PEN_MAX
			# Curb vs curb is a known plan overlap (Rook de-dupe). Count it, do not fail.
			if _is_curb(String(a["base"])) and _is_curb(String(b["base"])):
				if deep:
					print("EXT_ASSERT WARN curb_overlap %s %s other=%s id=%s asset=%s pen=%s,%s,%s" % [
						String(a["id"]), String(a["asset"]), String(b["node"]), String(b["id"]), String(b["asset"]),
						_fmt(pen.x), _fmt(pen.y), _fmt(pen.z),
					])
				else:
					_pass_n += 1
				continue
			# Fail only when the overlap is deeper than 0.010 m on every axis.
			if deep:
				_bad(String(a["id"]), String(a["asset"]), "overlap other=%s id=%s asset=%s pen=%s,%s,%s" % [
					String(b["node"]), String(b["id"]), String(b["asset"]), _fmt(pen.x), _fmt(pen.y), _fmt(pen.z),
				])
			else:
				_pass_n += 1


func _skip_pair(base_a: String, base_b: String) -> bool:
	# Guideway crosses the magnet, the car, and the track scuff. The car sits on its magnet.
	if _pair(base_a, base_b, "ext_maglev_guideway", "ext_maglev_magnet_module"):
		return true
	if _pair(base_a, base_b, "ext_maglev_guideway", "ext_maglev_car_body"):
		return true
	if _pair(base_a, base_b, "ext_maglev_guideway", "ext_track_scuff_guideway"):
		return true
	if _pair(base_a, base_b, "ext_maglev_magnet_module", "ext_maglev_car_body"):
		return true
	if (_is_curb(base_a) and _is_curb_ground_partner(base_b)) or (_is_curb(base_b) and _is_curb_ground_partner(base_a)):
		return true
	# Decals, litter, and paving are already left out of the solids list.
	if _is_paving(base_a) or _is_paving(base_b):
		return true
	if _is_decal_or_litter(base_a) or _is_decal_or_litter(base_b):
		return true
	return false


func _pair(a: String, b: String, x: String, y: String) -> bool:
	return (a == x and b == y) or (a == y and b == x)


func _is_curb(base: String) -> bool:
	return base.begins_with("ext_curb_")


func _is_curb_ground_partner(base: String) -> bool:
	return _is_paving(base) or base == "ext_platform_infill" or base == "ext_kerb_ramp" or base == "ext_canal_edge"


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


func _name_is_helper(nm: String) -> bool:
	var n: String = nm.to_lower()
	if n.contains("collision") or n.contains("collider") or n.contains("helper") or n.contains("proxy") or n.contains("colonly") or n.contains("ucx"):
		return true
	return n.ends_with("_col") or n.ends_with("-col") or n.contains("_col_") or n.contains("-col-")


func _mesh_is_visual(mi: MeshInstance3D, root_n: Node) -> bool:
	if mi.mesh == null or not mi.visible:
		return false
	var n: Node = mi
	while n != null:
		if _name_is_helper(String(n.name)):
			return false
		if n != root_n and (n is CollisionObject3D or n is CollisionShape3D):
			return false
		if n == root_n:
			break
		n = n.get_parent()
	return true


func _union_mesh_aabb(root_n: Node3D, visual_only: bool) -> Dictionary:
	var merged: AABB = AABB()
	var any: bool = false
	var stack: Array[Node] = [root_n]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			if mi.mesh != null and (not visual_only or _mesh_is_visual(mi, root_n)):
				var bb: AABB = mi.global_transform * mi.get_aabb()
				if any:
					merged = merged.merge(bb)
				else:
					merged = bb
					any = true
		for ch: Node in curr.get_children():
			stack.append(ch)
	return {"ok": any, "aabb": merged}


func _world_aabb_of(root_n: Node3D) -> Dictionary:
	var visual: Dictionary = _union_mesh_aabb(root_n, true)
	if bool(visual["ok"]):
		return visual
	return _union_mesh_aabb(root_n, false)


func _rids_for_bases(bases: Array) -> Array[RID]:
	var rids: Array[RID] = []
	for node: Node in get_nodes_in_group("exterior_placement"):
		if _base(_asset_of(node)) in bases:
			rids.append_array(_collision_rids(node))
	return rids


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
