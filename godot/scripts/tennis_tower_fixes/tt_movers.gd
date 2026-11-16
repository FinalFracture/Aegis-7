extends RefCounted
## Runtime openers for Rook's leaf-grouped doors. Meshes stay visible.
## Each leaf's colonly shapes move onto an AnimatableBody3D under that leaf
## so the collider follows. Frame colliders are not touched.

const LAYER := 1
const COURT_Z := 0.12
const COURT_X := 0.50
const COURT_Z_DONE := 0.30
const PAIR_DEG := 90.0
const BAY_YAW := [90.0, 90.0, -90.0]

var moving_meshes: int = 0
var _court: Array[Dictionary] = []
var _pair: Array[Dictionary] = []
var _bay: Array[Dictionary] = []


func setup(tower: Node3D) -> void:
	moving_meshes = 0
	_court.clear()
	_pair.clear()
	_bay.clear()
	var courts: int = 0
	var pairs: int = 0
	var gates: int = 0
	var bays: int = 0
	var slides: int = 0
	for inst in _instances(tower):
		var asset: String = _asset_name(inst)
		if asset == "tt_court_partition_door_closed":
			if _add_court(inst):
				courts += 1
		elif asset == "tt_door_pair_18":
			if _add_pair(inst):
				pairs += 1
		elif asset == "tt_rink_board_gate_open" or asset == "tt_rink_board_zamboni":
			if _park_gate(inst):
				gates += 1
		elif asset == "tt_entrance_bay_3l":
			if _add_bay3(inst):
				bays += 1
		elif asset.begins_with("tt_leisure_slide_tubes"):
			slides += _tag_slide(inst)
	print("[TT] court doors=%d open=+Z %.2f then X -%.2f/+%.2f" % [courts, COURT_Z, COURT_X, COURT_X])
	print("[TT] pair doors=%d swing_deg=%.0f" % [pairs, PAIR_DEG])
	print("[TT] rink gates=%d parked_open=1" % gates)
	print("[TT] bay3 doors=%d" % bays)
	print("[TT] slide chutes nonwalkable=%d" % slides)


func update(delta: float, player: Vector3) -> void:
	_update_court(delta, player)
	_update_pair(delta, player)
	_update_bay(delta, player)


## Standalone bay test uses this on one imported root (asset not placed in the tower).
func rig_bay3(root: Node3D) -> bool:
	return _add_bay3(root)


func set_bay3_open(root: Node3D, open: bool) -> void:
	for i: int in range(3):
		var leaf: Node3D = _child_named(root, "Leaf_%d" % i)
		if leaf == null:
			continue
		var yaw: float = BAY_YAW[i] if open else 0.0
		leaf.rotation = Vector3(0.0, deg_to_rad(yaw), 0.0)
		_sync_leaf(leaf)


func _add_court(inst: Node3D) -> bool:
	var leaf_l: Node3D = _child_named(inst, "Leaf_L")
	var leaf_r: Node3D = _child_named(inst, "Leaf_R")
	if leaf_l == null or leaf_r == null:
		print("[TT] court door %s separable=0" % String(inst.name))
		return false
	_rig(leaf_l)
	_rig(leaf_r)
	_court.append({
		"root": inst, "l": leaf_l, "r": leaf_r,
		"lb": leaf_l.position, "rb": leaf_r.position, "t": 0.0,
	})
	return true


func _add_pair(inst: Node3D) -> bool:
	var leaf_l: Node3D = _child_named(inst, "Leaf_L")
	var leaf_r: Node3D = _child_named(inst, "Leaf_R")
	if leaf_l == null or leaf_r == null:
		print("[TT] pair door %s separable=0" % String(inst.name))
		return false
	_rig(leaf_l)
	_rig(leaf_r)
	_pair.append({
		"root": inst, "l": leaf_l, "r": leaf_r,
		"t": 0.0, "away": 1.0,
	})
	return true


func _add_bay3(inst: Node3D) -> bool:
	var leaves: Array[Node3D] = []
	for i: int in range(3):
		var leaf: Node3D = _child_named(inst, "Leaf_%d" % i)
		if leaf == null:
			print("[TT] bay3 %s separable=0 (missing Leaf_%d)" % [String(inst.name), i])
			return false
		_rig(leaf)
		leaves.append(leaf)
	_bay.append({"root": inst, "leaves": leaves, "t": 0.0})
	return true


## Leaves are already exported in the parked-open pose (rotation 0).
## Closed would be Leaf0 yaw +90 and Leaf1 yaw -90. Leave them open.
func _park_gate(inst: Node3D) -> bool:
	var n: int = 0
	for i: int in range(2):
		var leaf: Node3D = _child_named(inst, "Leaf%d" % i)
		if leaf == null:
			continue
		_rig(leaf)
		leaf.rotation = Vector3.ZERO
		_sync_leaf(leaf)
		n += 1
	if n == 0:
		print("[TT] rink gate %s separable=0" % String(inst.name))
		return false
	return true


func _tag_slide(inst: Node3D) -> int:
	var n: int = 0
	var stack: Array[Node] = [inst]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for ch: Node in node.get_children():
			stack.append(ch)
		if node is CollisionObject3D:
			node.set_meta("tt_slide_chute", true)
			n += 1
	return 1 if n > 0 else 0


func _update_court(delta: float, player: Vector3) -> void:
	for d: Dictionary in _court:
		var root: Node3D = d["root"] as Node3D
		var leaf_l: Node3D = d["l"] as Node3D
		var leaf_r: Node3D = d["r"] as Node3D
		if not _live(root) or not _live(leaf_l) or not _live(leaf_r):
			continue
		var centre: Vector3 = root.global_transform * Vector3(0.50, 1.10, 0.0)
		var want: float = 1.0 if player.distance_to(centre) < 4.2 else 0.0
		var t: float = move_toward(float(d["t"]), want, 3.4 * delta)
		d["t"] = t
		# +Z first, clear of the frame, then the exact ±0.50 slide. Both are done at t = 1.
		var z_e: float = 1.0 if t >= COURT_Z_DONE else t / COURT_Z_DONE
		var x_e: float = 0.0 if t <= COURT_Z_DONE else (t - COURT_Z_DONE) / (1.0 - COURT_Z_DONE)
		leaf_l.position = (d["lb"] as Vector3) + Vector3(-COURT_X * x_e, 0.0, COURT_Z * z_e)
		leaf_r.position = (d["rb"] as Vector3) + Vector3(COURT_X * x_e, 0.0, COURT_Z * z_e)
		_sync_leaf(leaf_l)
		_sync_leaf(leaf_r)


func _update_pair(delta: float, player: Vector3) -> void:
	for d: Dictionary in _pair:
		var root: Node3D = d["root"] as Node3D
		var leaf_l: Node3D = d["l"] as Node3D
		var leaf_r: Node3D = d["r"] as Node3D
		if not _live(root) or not _live(leaf_l) or not _live(leaf_r):
			continue
		var centre: Vector3 = root.global_transform * Vector3(0.0, 1.15, 0.0)
		var want: float = 1.0 if player.distance_to(centre) < 3.4 else 0.0
		var t: float = move_toward(float(d["t"]), want, 3.6 * delta)
		# Latch the swing while the leaves are off the closed pose so a
		# player walking through does not reverse them into the opening.
		# Godot +yaw takes local +X to local -Z. Leaf_L extends +X and Leaf_R
		# extends -X, so away = +1 swings both leaves toward -Z.
		if t <= 0.02:
			var local_z: float = (root.global_transform.affine_inverse() * player).z
			if absf(local_z) > 0.08:
				d["away"] = signf(local_z)
		d["t"] = t
		var e: float = smoothstep(0.0, 1.0, t)
		var away: float = float(d["away"])
		leaf_l.rotation = Vector3(0.0, deg_to_rad(away * PAIR_DEG * e), 0.0)
		leaf_r.rotation = Vector3(0.0, deg_to_rad(-away * PAIR_DEG * e), 0.0)
		_sync_leaf(leaf_l)
		_sync_leaf(leaf_r)


func _update_bay(delta: float, player: Vector3) -> void:
	for d: Dictionary in _bay:
		var root: Node3D = d["root"] as Node3D
		if not _live(root):
			continue
		var centre: Vector3 = root.global_transform * Vector3(0.0, 1.15, -0.4)
		var want: float = 1.0 if player.distance_to(centre) < 3.6 else 0.0
		var t: float = move_toward(float(d["t"]), want, 3.2 * delta)
		d["t"] = t
		var e: float = smoothstep(0.0, 1.0, t)
		var leaves: Array = d["leaves"] as Array
		for i: int in range(mini(leaves.size(), 3)):
			var leaf: Node3D = leaves[i] as Node3D
			if not _live(leaf):
				continue
			leaf.rotation = Vector3(0.0, deg_to_rad(BAY_YAW[i] * e), 0.0)
			_sync_leaf(leaf)


func _rig(leaf: Node3D) -> AnimatableBody3D:
	_tag_meshes(leaf)
	var body: AnimatableBody3D = AnimatableBody3D.new()
	body.name = "TT_LeafBody"
	body.sync_to_physics = true
	body.collision_layer = LAYER
	body.collision_mask = 1
	leaf.add_child(body)
	body.transform = Transform3D.IDENTITY
	var shapes: Array[CollisionShape3D] = []
	var holders: Array[CollisionObject3D] = []
	var stack: Array[Node] = [leaf]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for ch: Node in node.get_children():
			if ch == body:
				continue
			stack.append(ch)
		if node is CollisionShape3D:
			var holder: Node = node.get_parent()
			if holder is CollisionObject3D and String(holder.name).to_lower().contains("colonly"):
				shapes.append(node as CollisionShape3D)
				if not holders.has(holder as CollisionObject3D):
					holders.append(holder as CollisionObject3D)
	for cs: CollisionShape3D in shapes:
		var kept: Transform3D = cs.global_transform
		var parent: Node = cs.get_parent()
		parent.remove_child(cs)
		body.add_child(cs)
		cs.global_transform = kept
	for holder: CollisionObject3D in holders:
		var still: bool = false
		for ch2: Node in holder.get_children():
			if ch2 is CollisionShape3D:
				still = true
				break
		if not still:
			holder.collision_layer = 0
			holder.collision_mask = 0
	_sync_body(body)
	return body


func _tag_meshes(n: Node) -> void:
	if n is MeshInstance3D:
		n.set_meta("tt_no_batch", true)
		moving_meshes += 1
	for ch: Node in n.get_children():
		_tag_meshes(ch)


func _sync_leaf(leaf: Node3D) -> void:
	var body: Node = leaf.get_node_or_null("TT_LeafBody")
	if body is AnimatableBody3D:
		_sync_body(body as AnimatableBody3D)


func _sync_body(body: AnimatableBody3D) -> void:
	if body == null or not body.is_inside_tree():
		return
	PhysicsServer3D.body_set_state(body.get_rid(), PhysicsServer3D.BODY_STATE_TRANSFORM, body.global_transform)


func _live(n: Node) -> bool:
	return n != null and is_instance_valid(n)


func _child_named(root: Node, nm: String) -> Node3D:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n != root and String(n.name) == nm and n is Node3D:
			return n as Node3D
		for ch: Node in n.get_children():
			stack.append(ch)
	return null


func _instances(tower: Node3D) -> Array[Node3D]:
	var out: Array[Node3D] = []
	for tag in tower.get_children():
		if not String(tag.name).begins_with("Tag_"):
			continue
		for ch in tag.get_children():
			if ch is Node3D and not String(ch.name).begins_with("MM_"):
				out.append(ch as Node3D)
	return out


func _asset_name(inst: Node) -> String:
	var nm: String = String(inst.name)
	var u: int = nm.rfind("_")
	if u <= 0:
		return nm
	var tail: String = nm.substr(u + 1)
	if tail.is_valid_int():
		return nm.substr(0, u)
	return nm
