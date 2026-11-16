extends RefCounted
## TTQA-025. Per-room lights past the foyer, which tennis_tower_lighting.gd
## already covers. No shadows. Every light distance-fades. A light whose
## range reaches the lobby eye or the lobby floor samples is dropped so the
## foyer mean stays on the shipped lights. Emissive panels are one MultiMesh
## per floor and skip the lobby view column.


const COL := Color(0.98, 0.91, 0.78)
const FADE_BEGIN := 28.0
const FADE_LEN := 8.0

static var omni_n: int = 0
static var spot_n: int = 0
static var shadowed_n: int = 0
static var panel_n: int = 0
static var dropped_n: int = 0
static var max_overlap: int = 0
static var _pts: Array[Vector3] = []
static var _rngs: Array[float] = []


static func run(tower: Node3D) -> void:
	omni_n = 0
	spot_n = 0
	shadowed_n = 0
	panel_n = 0
	dropped_n = 0
	max_overlap = 0
	_pts.clear()
	_rngs.clear()
	var root := Node3D.new()
	root.name = "TT_RoomLights"
	tower.add_child(root)
	var panels: Dictionary = {"f1": [], "f2": [], "f3": []}
	var gallery_panels: Array = []
	var arcade_panels: Array = []
	var room_list: Array[Dictionary] = rooms()
	for fitted: Dictionary in room_list:
		_fit_room(fitted)
	for room: Dictionary in room_list:
		var rects: Array = room["rects"]
		var y_base := float(room["y_base"])
		var space := float(room["space"])
		var rng := float(room["rng"])
		var energy := float(room["energy"])
		var yoff := float(room["yoff"])
		var ceil_y := float(room["ceil"])
		var bucket: String = "f1" if y_base < 3.0 else ("f2" if y_base < 9.0 else "f3")
		for rect: Array in rects:
			var x0 := float(rect[0])
			var x1 := float(rect[1])
			var z0 := float(rect[2])
			var z1 := float(rect[3])
			var cols := maxi(1, int(ceil((x1 - x0) / space)))
			var rows := maxi(1, int(ceil((z1 - z0) / space)))
			for ix: int in range(cols):
				for iz: int in range(rows):
					var px := lerpf(x0, x1, (float(ix) + 0.5) / float(cols))
					var pz := lerpf(z0, z1, (float(iz) + 0.5) / float(rows))
					var pos := Vector3(px, y_base + yoff, pz)
					if _hits_lobby(pos, rng):
						dropped_n += 1
					else:
						_omni(root, "TT_Room_%s_%d" % [String(room["id"]), omni_n], pos, energy, rng)
						_pts.append(pos)
						_rngs.append(rng)
						omni_n += 1
						# Foyer column stays dark on F1. The gallery ceiling is its own
						# mesh of wide panels, above the lobby camera.
						if String(room["id"]) == "f2_gallery":
							gallery_panels.append(Vector3(px, ceil_y - 0.22, pz))
						elif String(room["id"]).ends_with("arcade"):
							arcade_panels.append(Vector3(px, ceil_y - 0.22, pz))
						elif not _in_lobby_column(px, pz):
							(panels[bucket] as Array).append(Vector3(px, ceil_y - 0.22, pz))
	for key: String in ["f1", "f2", "f3"]:
		panel_n += _panels(root, key, panels[key] as Array)
	panel_n += _panels(root, "gallery", gallery_panels, Vector3(5.4, 0.04, 5.4))
	panel_n += _panels(root, "arcade", arcade_panels, Vector3(2.6, 0.05, 2.6), 1.35)
	max_overlap = _overlap()
	print("[TT] room lights omni=%d spot=%d shadowed=%d panels=%d max_overlap=%d dropped_lobby=%d" % [
		omni_n, spot_n, shadowed_n, panel_n, max_overlap, dropped_n])


## Move each interior MultiMesh to the centroid of its instances and rebase
## the instance transforms so the meshes stay put. Light selection then uses
## the cell, and the lobby omnis stay the closest lights on the lobby floor.
static func reseat_batches(tower: Node3D) -> void:
	var moved := 0
	var stack: Array[Node] = [tower]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for c: Node in node.get_children():
			stack.append(c)
		if node is MultiMeshInstance3D and String(node.name).begins_with("MM_"):
			if _reseat_one(node as MultiMeshInstance3D):
				moved += 1
	print("[TT] reseat batch origins=%d" % moved)


static func _reseat_one(mmi: MultiMeshInstance3D) -> bool:
	var mm: MultiMesh = mmi.multimesh
	if mm == null:
		return false
	var count := mm.instance_count
	if count < 2:
		return false
	mmi.physics_interpolation_mode = Node.PHYSICS_INTERPOLATION_MODE_OFF
	if mmi.position.length_squared() > 0.25:
		return false
	var acc := Vector3.ZERO
	for i: int in range(count):
		acc += mm.get_instance_transform(i).origin
	var center := acc / float(count)
	if center.length_squared() < 4.0:
		return false
	for i: int in range(count):
		var xf := mm.get_instance_transform(i)
		xf.origin -= center
		mm.set_instance_transform(i, xf)
	mmi.position = center
	return true


static func rooms() -> Array[Dictionary]:
	return [
		_room("f1_courts", [[39.5, 103.5, 24.5, 54.5]], 0.0, 6.05, 14.0, 13.0, 14.0, 2.4, Vector3(52, 1.62, 40), Vector3(78, 1.4, 40)),
		_room("f1_bowling", [[30, 57, 0, 15]], 0.0, 6.05, 10.0, 8.0, 9.0, 3.0, Vector3(40, 1.62, 8), Vector3(52, 1.3, 8)),
		_room("f1_axe", [[77, 102, 0, 15]], 0.0, 6.05, 10.0, 8.0, 6.5, 3.0, Vector3(86, 1.62, 7), Vector3(98, 1.3, 7)),
		_room("f1_pool", [[2, 29, 1, 33]], 2.0, 6.05, 10.0, 12.0, 10.0, 2.6, Vector3(8, 3.62, 12), Vector3(22, 2.6, 16)),
		_room("f1_leisure", [[2, 28, 46, 78]], 1.0, 6.05, 10.0, 9.0, 10.0, 2.8, Vector3(16, 2.62, 60), Vector3(16, 0.9, 54)),
		_room("f1_food", [[44, 102, 64, 79]], 0.0, 6.05, 12.0, 9.0, 6.5, 3.0, Vector3(60, 1.62, 71), Vector3(85, 1.4, 71)),
		_room("f1_arcade", [[113, 140, 2, 77]], 0.0, 6.05, 10.0, 18.0, 24.0, 1.6, Vector3(124, 1.7, 36), Vector3(132, 1.3, 48)),
		_room("f1_wc_s", [[102, 113, 1, 14]], 0.0, 6.05, 6.0, 6.0, 5.5, 2.8, Vector3(106, 1.62, 8), Vector3(110, 1.4, 8)),
		_room("f1_wc_nw", [[30, 44, 65, 78]], 0.0, 6.05, 7.0, 6.5, 5.5, 2.8, Vector3(36, 1.62, 71), Vector3(40, 1.4, 71)),
		_room("f1_wc_ne", [[102, 113, 65, 78]], 0.0, 6.05, 6.0, 6.0, 5.5, 2.8, Vector3(106, 1.62, 71), Vector3(110, 1.4, 71)),
		_room("f1_wc_corridor", [[96, 102, 4, 12]], 0.0, 6.05, 6.0, 6.0, 5.5, 2.8, Vector3(100, 1.62, 8), Vector3(108, 1.4, 6)),
		_room("f2_rink", [[39.5, 103.5, 24.5, 54.5]], 6.1, 12.15, 14.0, 13.0, 14.0, 2.4, Vector3(55, 7.72, 39.5), Vector3(80, 7.2, 39.5)),
		_room("f2_gym", [[44, 102, 65, 78]], 6.1, 12.15, 12.0, 9.0, 6.5, 3.0, Vector3(60, 7.72, 71), Vector3(85, 7.3, 71)),
		_room("f2_climbing", [[30, 113, 1, 14]], 6.1, 12.15, 12.0, 9.0, 6.5, 3.0, Vector3(50, 7.72, 8), Vector3(75, 7.3, 8)),
		# High mount, short range: vertical gap to the lobby eye is ~7.8 m, so the
		# sphere lights the gallery and stops above the foyer. Camera looks down
		# the walk so the side slabs stay out of frame.
		_room("f2_gallery", [[-11, -1, 12, 67]], 6.1, 12.15, 6.0, 5.5, 22.0, 3.4, Vector3(-6.0, 7.9, 36.0), Vector3(-6.0, 6.8, 55.0)),
		_room("f2_arcade", [[113, 140, 2, 77]], 6.1, 12.15, 10.0, 18.0, 30.0, 1.6, Vector3(124, 7.85, 36), Vector3(132, 7.3, 48)),
		_room("f2_slide", [[1, 19, 51, 61]], 6.1, 12.15, 8.0, 6.0, 7.5, 2.4, Vector3(10, 7.72, 56), Vector3(18, 7.2, 59)),
		_room("f3_basketball", [[39.5, 103.5, 24.5, 54.5]], 12.2, 18.2, 14.0, 13.0, 14.0, 2.4, Vector3(52, 13.82, 39.5), Vector3(80, 13.4, 39.5)),
		_room("f3_track", [[2, 126, 0.8, 3.4], [2, 126, 75.4, 78.2], [0.8, 3.6, 3.4, 75.4], [124.2, 127.2, 3.4, 75.4]], 12.2, 18.2, 16.0, 8.0, 8.0, 2.8, Vector3(20, 13.82, 1.8), Vector3(50, 13.4, 1.8)),
		_room("f3_dining", [[1, 23, 6, 74]], 12.2, 18.2, 12.0, 9.0, 6.5, 3.0, Vector3(12, 13.82, 40), Vector3(20, 13.4, 40)),
		_room("f3_cabanas", [[-11.2, -1.2, 20, 60]], 12.2, 18.2, 8.0, 6.0, 5.5, 2.6, Vector3(-8, 13.82, 40), Vector3(-3, 13.4, 40)),
		_room("f3_playground", [[129, 139.5, 22, 57]], 12.2, 18.2, 8.0, 7.0, 6.0, 2.8, Vector3(133, 13.82, 36), Vector3(136, 13.4, 48)),
	]


static func _room(id: String, rects: Array, y_base: float, ceil_y: float, space: float, rng: float, energy: float, yoff: float, eye: Vector3, look: Vector3) -> Dictionary:
	return {
		"id": id, "rects": rects, "y_base": y_base, "ceil": ceil_y,
		"space": space, "rng": rng, "energy": energy, "yoff": yoff,
		"eye": eye, "look": look,
	}


static func _hits_lobby(pos: Vector3, rng: float) -> bool:
	var samples: Array[Vector3] = [
		Vector3(-9.0, 1.7, 44.0), Vector3(-6.0, 1.2, 36.0), Vector3(-2.0, 1.2, 30.0),
		Vector3(2.0, 1.5, 28.0), Vector3(0.0, 2.0, 50.0), Vector3(-8.0, 0.5, 44.0),
	]
	for s: Vector3 in samples:
		var limit := rng + 1.5
		if s.distance_squared_to(Vector3(-9.0, 1.7, 44.0)) < 0.01:
			limit = rng + 2.0
		if pos.distance_to(s) < limit:
			return true
	return false


static func _in_lobby_column(x: float, z: float) -> bool:
	return x > -18.0 and x < 16.0 and z > 16.0 and z < 68.0


static func _omni(root: Node3D, nm: String, pos: Vector3, energy: float, rng: float) -> void:
	var l := OmniLight3D.new()
	l.name = nm
	l.position = pos
	l.light_color = COL
	l.light_energy = energy
	l.omni_range = rng
	l.omni_attenuation = 0.55
	l.shadow_enabled = false
	l.distance_fade_enabled = true
	l.distance_fade_begin = FADE_BEGIN
	l.distance_fade_length = FADE_LEN
	root.add_child(l)


static func _panels(root: Node3D, key: String, pts: Array, size: Vector3 = Vector3(1.5, 0.04, 1.5), emission: float = 1.15) -> int:
	if pts.is_empty():
		return 0
	var mesh := BoxMesh.new()
	mesh.size = size
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.mesh = mesh
	mm.instance_count = pts.size()
	for i: int in range(pts.size()):
		var p: Vector3 = pts[i]
		mm.set_instance_transform(i, Transform3D(Basis.IDENTITY, p))
	var mmi := MultiMeshInstance3D.new()
	mmi.physics_interpolation_mode = Node.PHYSICS_INTERPOLATION_MODE_OFF
	mmi.name = "TT_RoomPanels_%s" % key
	mmi.multimesh = mm
	mmi.material_override = _panel_material(emission)
	mmi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mmi.set_meta("tt_no_batch", true)
	root.add_child(mmi)
	return pts.size()


static func _panel_material(emission: float = 1.15) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.resource_name = "TT_RoomCeiling"
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.albedo_color = Color(1.0, 0.95, 0.86, 1.0)
	m.emission_enabled = true
	m.emission = Color(1.0, 0.94, 0.82)
	m.emission_energy_multiplier = emission
	return m


## Pull each omni onto its own floor sample and cap the range so it cannot
## reach the next floor. The old arcade range (18) and court range (13) stacked
## across the 6.1 m floor pitch and peaked at 22 overlaps. The grid tightens
## with the range so a cell corner still sits inside its light.
static func _fit_room(room: Dictionary) -> void:
	var id := String(room["id"])
	if id == "f2_gallery":
		return
	var yb := float(room["y_base"])
	var ceil_y := float(room["ceil"])
	var ly := yb + float(room["yoff"])
	var planes: Array[float] = [1.6, 7.7, 13.8]
	var own := planes[0]
	var own_d := absf(ly - own)
	for sy: float in planes:
		var d := absf(ly - sy)
		if d < own_d:
			own = sy
			own_d = d
	var desired := clampf(own, yb + 0.55, ceil_y - 0.55)
	var yoff := desired - yb
	ly = yb + yoff
	room["yoff"] = yoff
	# The east facade is one MultiMesh. Godot keeps the eight lights nearest
	# its origin, and the bay in the arcade shot sits just outside a 10 m
	# range. A 16 m grid leaves two of those lights on that bay. 13 m is the
	# longest range that still peaks at 7 overlaps.
	if id.ends_with("arcade"):
		room["rng"] = 13.0
		room["space"] = 16.0
		return
	# 10 m is the longest range that stays at 8 overlaps with this spacing.
	# The floor-to-floor cap (about 5.8 m) left the far end of a hall outside
	# every light that the 8-light limit keeps on a long mesh.
	var rng := minf(float(room["rng"]), 10.0)
	room["rng"] = rng
	room["space"] = maxf(float(room["space"]), rng * 1.15)


static func _overlap() -> int:
	var worst := 0
	var samples: Array[Vector3] = []
	for p: Vector3 in _pts:
		samples.append(p)
	var x := -12.0
	while x <= 140.0:
		var z := 0.0
		while z <= 79.0:
			samples.append(Vector3(x, 1.6, z))
			samples.append(Vector3(x, 7.7, z))
			samples.append(Vector3(x, 13.8, z))
			z += 8.0
		x += 8.0
	for s: Vector3 in samples:
		var n := 0
		for i: int in range(_pts.size()):
			if s.distance_to(_pts[i]) <= _rngs[i]:
				n += 1
		if n > worst:
			worst = n
	return worst
