extends Node
## Floor and room portal for the tower props. Compatibility occlusion does not
## split a MultiMesh, so a 32 m batch stays drawn if any corner is in frame.
## Structural shells stay visible (ceilings, facade, roof). Props on floors and
## in rooms the camera is not in are hidden. Colliders are not touched.
## From the drum the interior props drop out past a short bubble, leaving the shell.


const BUBBLE_M := 20.0
const OUTSIDE_M := 26.0
const CIRC_M := 36.0
const NEIGHBOR_M := 28.0
const OUTSIDE_SDF := 1.5
const SLAB_BAND := 1.7
const LOOK_UP := 0.2
const SHELL_M := 38.0

# floor, x0, x1, z0, z1. Smallest containing rect wins so a corridor beats a hall.
const _RECTS: Array = [
	[1, -14.0, 2.0, 8.0, 71.0],
	[1, -2.0, 32.0, 32.5, 46.5],
	[1, 0.0, 32.0, 0.0, 35.5],
	[1, 0.0, 32.0, 43.5, 79.0],
	[1, 30.0, 58.0, 0.0, 16.0],
	[1, 75.0, 104.0, 0.0, 16.0],
	[1, 38.0, 106.0, 20.0, 58.0],
	[1, 42.0, 104.0, 62.0, 79.0],
	[1, 108.0, 142.0, 0.0, 79.0],
	[1, 96.0, 114.0, 0.0, 16.0],
	[1, 28.0, 46.0, 63.0, 79.0],
	[1, 100.0, 114.0, 63.0, 79.0],
	[2, -14.0, 2.0, 8.0, 71.0],
	[2, 38.0, 106.0, 20.0, 58.0],
	[2, 42.0, 104.0, 62.0, 79.0],
	[2, 28.0, 114.0, 0.0, 16.0],
	[2, 108.0, 142.0, 0.0, 79.0],
	[2, 0.0, 22.0, 48.0, 64.0],
	[3, 38.0, 106.0, 20.0, 58.0],
	[3, 0.0, 128.0, 0.0, 6.0],
	[3, 0.0, 128.0, 73.0, 79.0],
	[3, 0.0, 6.0, 0.0, 79.0],
	[3, 122.0, 130.0, 0.0, 79.0],
	[3, 0.0, 26.0, 4.0, 76.0],
	[3, -14.0, 2.0, 16.0, 64.0],
	[3, 126.0, 142.0, 18.0, 60.0],
]

# Stair and lift shafts. Both neighbouring floors stay active inside them.
const _STAIRS: Array = [
	[-8.0, 4.0, 8.0, 22.0],
	[-8.0, 4.0, 56.0, 72.0],
	[30.0, 42.0, 12.0, 24.0],
	[30.0, 42.0, 54.0, 68.0],
	[22.0, 34.0, 30.0, 44.0],
]

var _ppa: Node = null
var _props: Array[GeometryInstance3D] = []
var _floor: PackedInt32Array = PackedInt32Array()
var _room: PackedInt32Array = PackedInt32Array()
var _kind: PackedInt32Array = PackedInt32Array()
var _x: PackedFloat32Array = PackedFloat32Array()
var _z: PackedFloat32Array = PackedFloat32Array()
var _neighbors: Array = []
var _key: int = -999999
var _sun_far: float = -1.0
var _logs: int = 0


func setup(ppa: Node, tower: Node3D) -> void:
	_ppa = ppa
	_build_neighbors()
	_props.clear()
	_floor = PackedInt32Array()
	_room = PackedInt32Array()
	_kind = PackedInt32Array()
	_x = PackedFloat32Array()
	_z = PackedFloat32Array()
	_gather(tower)
	print("[TT] vis props=%d" % _props.size())
	_key = -999999
	_apply()


func _process(_delta: float) -> void:
	if _ppa == null or _props.is_empty():
		return
	_apply()


func _build_neighbors() -> void:
	_neighbors.clear()
	for i: int in range(_RECTS.size()):
		var row: Array = []
		var a: Array = _RECTS[i]
		for j: int in range(_RECTS.size()):
			if i == j:
				continue
			var b: Array = _RECTS[j]
			if int(a[0]) != int(b[0]):
				continue
			if _expanded_hit(a, b, 4.0):
				row.append(j)
		_neighbors.append(row)


func _expanded_hit(a: Array, b: Array, pad: float) -> bool:
	return not (float(a[2]) + pad < float(b[1]) - pad or float(b[2]) + pad < float(a[1]) - pad or float(a[4]) + pad < float(b[3]) - pad or float(b[4]) + pad < float(a[3]) - pad)


func _gather(n: Node) -> void:
	if n is GeometryInstance3D and n.has_meta("tt_vis_floor") and not n.has_meta("tt_vis_mover"):
		var fl := int(n.get_meta("tt_vis_floor"))
		var keep := bool(n.get_meta("tt_vis_keep"))
		var tag := String(n.get_meta("tt_vis_tag", ""))
		var roof := bool(n.get_meta("tt_vis_roof", false))
		var slab := bool(n.get_meta("tt_vis_slab", false))
		# 0 interior prop, 1 roof, 2 site, 3 far shell, 4 upper slab.
		var kind := -1
		if fl >= 1 and fl <= 3 and not keep:
			kind = 0
		elif roof:
			kind = 1
		elif tag == "site":
			kind = 2
		elif tag == "f3" and slab:
			kind = 4
		elif tag == "facade" or tag == "env" or tag == "cols" or tag == "plant" or tag == "struct":
			kind = 3
		if kind >= 0:
			var px := float(n.get_meta("tt_vis_x"))
			var pz := float(n.get_meta("tt_vis_z"))
			_props.append(n as GeometryInstance3D)
			_floor.append(fl)
			_x.append(px)
			_z.append(pz)
			_kind.append(kind)
			_room.append(_room_at(fl, px, pz) if kind == 0 else -1)
	for c: Node in n.get_children():
		_gather(c)


func _room_at(floor_n: int, x: float, z: float) -> int:
	var best := -1
	var best_a := 1.0e12
	for i: int in range(_RECTS.size()):
		var r: Array = _RECTS[i]
		if int(r[0]) != floor_n:
			continue
		if x < float(r[1]) or x > float(r[2]) or z < float(r[3]) or z > float(r[4]):
			continue
		var area := (float(r[2]) - float(r[1])) * (float(r[4]) - float(r[3]))
		if area < best_a:
			best_a = area
			best = i
	return best


func _fi(y: float) -> int:
	if y < 4.8:
		return 1
	if y < 10.6:
		return 2
	return 3


func _in_stair(x: float, z: float) -> bool:
	for s: Variant in _STAIRS:
		var r: Array = s
		if x >= float(r[0]) and x <= float(r[1]) and z >= float(r[2]) and z <= float(r[3]):
			return true
	return false


func _mask(eye_y: float, ahead_y: float, stair: bool) -> int:
	var m := 0
	m |= 1 << _fi(eye_y)
	m |= 1 << _fi(ahead_y)
	if absf(eye_y - 6.1) < SLAB_BAND:
		m |= (1 << 1) | (1 << 2)
	if absf(eye_y - 12.2) < SLAB_BAND:
		m |= (1 << 2) | (1 << 3)
	if stair:
		var f := _fi(eye_y)
		m |= 1 << f
		if f > 1:
			m |= 1 << (f - 1)
		if f < 3:
			m |= 1 << (f + 1)
	return m


func _apply() -> void:
	var cam: Camera3D = _ppa.get("_camera") as Camera3D
	if cam == null:
		return
	var inv: Transform3D = _ppa.get("_tower_inv")
	var q: Vector3 = inv * cam.global_position
	var ahead: Vector3 = inv * (cam.global_position + (-cam.global_basis.z) * 10.0)
	var outside := false
	if _ppa.has_method("_tt_sdf_local"):
		outside = float(_ppa.call("_tt_sdf_local", q)) > OUTSIDE_SDF
	var stair := _in_stair(q.x, q.z)
	var mask := 0 if outside else _mask(q.y, ahead.y, stair)
	var look := ahead - q
	var look_len := look.length()
	var looking_up := look_len > 0.001 and look.y / look_len > LOOK_UP
	var cell := Vector2i(floori(q.x / 4.0), floori(q.z / 4.0))
	var key := cell.x + cell.y * 128 + mask * 8192 + (100000 if outside else 0) + (400000 if looking_up else 0)
	if key == _key:
		return
	_key = key
	var cam_room: Array = [-1, -1, -1, -1]
	if not outside:
		for fl: int in [1, 2, 3]:
			if (mask & (1 << fl)) != 0:
				cam_room[fl] = _room_at(fl, q.x, q.z)
	var shown := 0
	var shown_roof := 0
	var shown_site := 0
	var on_f2 := (mask & (1 << 2)) != 0
	var on_f3 := (mask & (1 << 3)) != 0
	var bubble := OUTSIDE_M if outside else BUBBLE_M
	var bubble2 := bubble * bubble
	var site2 := OUTSIDE_M * OUTSIDE_M
	var shell2 := SHELL_M * SHELL_M
	var circ2 := CIRC_M * CIRC_M
	var near2 := NEIGHBOR_M * NEIGHBOR_M
	for i: int in range(_props.size()):
		var dx := _x[i] - q.x
		var dz := _z[i] - q.z
		var d2 := dx * dx + dz * dz
		var show := false
		var kind := _kind[i]
		if kind == 1:
			# F3 slab is the ceiling below the roof. On F3 the roof is the lid.
			show = outside or on_f3 or looking_up
		elif kind == 2:
			show = d2 < site2
		elif kind == 3:
			show = outside or looking_up or d2 < shell2
		elif kind == 4:
			show = outside or looking_up or on_f2 or on_f3
		elif outside:
			show = d2 < bubble2
		else:
			var fl2 := _floor[i]
			if (mask & (1 << fl2)) != 0:
				if d2 < bubble2:
					show = true
				else:
					var cr: int = cam_room[fl2]
					var pr := _room[i]
					if cr < 0:
						show = d2 < circ2
					elif pr == cr:
						show = true
					elif pr >= 0 and _neighbors[cr].has(pr) and d2 < near2:
						show = true
		var gi := _props[i]
		if gi.visible != show:
			gi.visible = show
		if show:
			shown += 1
			if kind == 1:
				shown_roof += 1
			elif kind == 2:
				shown_site += 1
	_set_sun(not outside)
	if _logs < 8:
		_logs += 1
		print("[TT] vis shown=%d roof=%d site=%d outside=%s up=%s mask=%d eye=(%.1f,%.1f,%.1f)" % [shown, shown_roof, shown_site, str(outside), str(looking_up), mask, q.x, q.y, q.z])


func _set_sun(inside: bool) -> void:
	var sun: DirectionalLight3D = _ppa.get("_sun") as DirectionalLight3D
	if sun == null:
		return
	if _sun_far < 0.0:
		_sun_far = sun.directional_shadow_max_distance
	var want := 45.0 if inside else _sun_far
	if absf(sun.directional_shadow_max_distance - want) > 0.5:
		sun.directional_shadow_max_distance = want
