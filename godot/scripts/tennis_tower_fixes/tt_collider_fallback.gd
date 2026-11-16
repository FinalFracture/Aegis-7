extends RefCounted
## Runtime trimesh fallback for tower visuals that have no nearby collider.
## Callable on the tower root (standalone scene or the playable area). Run after
## door setup and before the batcher hides meshes. Samples live in mesh space;
## coverage is distance to that instance's existing shapes (hollow trimesh is
## not "inside = covered").

const LAYER := 1 | (1 << 18)
const SAMPLE_N := 24
const COVER_R := 0.12
const COVER_R2 := 0.0144
const CELL := 0.5
const MIN_H := 0.3

static var _skip: RegEx
static var _door: RegEx
static var _extra: RegEx
static var _stair_mesh: RegEx
static var _stair_body: RegEx
static var _struct: RegEx
static var _opening: RegEx
static var _dress: RegEx
static var _flag_cache: Dictionary = {}
static var _face_cache: Dictionary = {}


static func _ensure() -> void:
	if _skip != null:
		return
	_skip = RegEx.new()
	_skip.compile("(?i)(vine|foliage|leaf|plant_dress|decal|caustic|light|glow|lamp_emit|water|sign_text|text|label)")
	_door = RegEx.new()
	# Sliding leaves, plus stile/push-bar hardware that sits in the clear opening.
	# pull_handle rides on the court leaf and moves with it.
	_door.compile("(?i)(door_scissor|door_leaf|door_slide|door_stile|push_bar|pull_handle)")
	_opening = RegEx.new()
	# Only a pierced shell the player has to walk through stays a trimesh.
	# A generic "frame" / "pane" / "scissor" is a solid prop and uses a box or convex hull.
	_opening.compile("(?i)(door_frame|window|mullion|grille|grate)")
	_dress = RegEx.new()
	# Detail that does not close a walk-through: foliage, cables, hardware, handrails
	# (a handrail box fills the ramp), and gate pickets (the gate stays open).
	_dress.compile("(?i)(handrail|moss|kelp|fish|tuft|cushion|crest|plush|cable|chain|reef|backdrop|stipe|button|reflector|_tick|lining_reveal|locker_reveal|nosing|tether|wheel|pins|axe_handle|tablet|score_screen|monitor|branch_trunk|grass_|swing[0-9]+_chain|ledge_moss|fish_school|gatepicket|gate_picket|pedal|crank|flywheel|fan_cage|chair_back|tableleg|table_leg|slat_frame|(^|_)arm($|_)|pc_shel|pc_plush|pos_screen|(^|_)pos($|_))")
	_extra = RegEx.new()
	# court_line / level_disc: floor decals whose AABB spans a storey; a coplanar
	# trimesh z-fights the slab. kick_panels: 0.32 m net sills across the secondary
	# door leaves (local x -2..-0.4 and 0.4..2, top y 0.38). The S/N walk goes
	# through local x ±1.085, and 0.38 m is above the 0.32 m step, so the trimesh
	# seals the clear opening. Bollards stay (posts at the module edges).
	# mid_landing: the visual is a solid from the floor up to the landing slab.
	# The walkable top is already Mid_Landing-colonly. The solid crosses the
	# flight at the switchback (ray at z=18.9 hits it at x=32.7), so F1 cannot
	# reach F2. The slate (h < 0.3) stays skipped.
	_extra.compile("(?i)(court_line|level_disc|kick_panels|mid_landing)")
	_stair_mesh = RegEx.new()
	_stair_mesh.compile("(?i)(tread|flight|nosing|step)")
	_stair_body = RegEx.new()
	_stair_body.compile("(?i)(ramp|flight)")
	_struct = RegEx.new()
	_struct.compile("(?i)^(slab_|beams_|trimmer_|plinth_fill|deck_|fill_)")


static func run(tower: Node3D) -> Dictionary:
	_ensure()
	_flag_cache.clear()
	_face_cache.clear()
	_print_zero(tower)
	var t0: int = Time.get_ticks_msec()
	var groups: Dictionary = {}
	for inst in _instances(tower):
		var asset: String = _asset_name(inst)
		if not groups.has(asset):
			groups[asset] = []
		(groups[asset] as Array).append(inst)
	var shape_cache: Dictionary = {}
	var sample_cache: Dictionary = {}
	var meshes_n: int = 0
	var tris_n: int = 0
	var boxes_n: int = 0
	var convex_n: int = 0
	var tri_n: int = 0
	var inst_ids: Dictionary = {}
	var assets: Array = groups.keys()
	assets.sort()
	for asset_v in assets:
		var asset: String = String(asset_v)
		var arr: Array = groups[asset]
		var rep: Node3D = arr[0] as Node3D
		var flags: Dictionary = _flags(rep, tower)
		var decided: Dictionary = _decide(rep, tower, sample_cache, flags)
		var names: PackedStringArray = PackedStringArray()
		var added_tris: int = 0
		var stair: bool = bool(flags["stair"])
		var cols: int = int(flags["cols"])
		for inst_v in arr:
			var inst: Node3D = inst_v as Node3D
			var added: Dictionary = _apply(inst, decided, shape_cache, tower, stair, cols)
			var n: int = int(added["n"])
			if n > 0:
				inst_ids[inst.get_instance_id()] = true
				meshes_n += n
				tris_n += int(added["tris"])
				added_tris += int(added["tris"])
				boxes_n += int(added["boxes"])
				convex_n += int(added["convex"])
				tri_n += int(added["trimesh"])
				if names.is_empty():
					names = added["names"] as PackedStringArray
		if names.size() > 0:
			var shown: String = ""
			var lim: int = mini(names.size(), 14)
			for i: int in range(lim):
				shown += names[i]
				if i + 1 < lim:
					shown += ","
			if names.size() > lim:
				shown += ",+%d" % (names.size() - lim)
			print("[TT] fallback add %s x%d tris=%d: %s" % [asset, arr.size(), int(added_tris), shown])
	var seals: Dictionary = _seal_lifts(tower)
	var ms: int = Time.get_ticks_msec() - t0
	print("[TT] collider fallback meshes=%d instances=%d tris=%d ms=%d boxes=%d convex=%d trimesh=%d" % [meshes_n, inst_ids.size(), tris_n, ms, boxes_n, convex_n, tri_n])
	print("[TT] lift seals bodies=%d skipped=%d" % [int(seals["added"]), int(seals["skipped"])])
	return {"meshes": meshes_n, "instances": inst_ids.size(), "tris": tris_n, "ms": ms, "seals": int(seals["added"]), "boxes": boxes_n, "convex": convex_n, "trimesh": tri_n}


static func leak_stats(tower: Node3D) -> Dictionary:
	_ensure()
	_flag_cache.clear()
	var t0: int = Time.get_ticks_msec()
	var groups: Dictionary = {}
	var zero: int = 0
	var zero_tall: int = 0
	var zero_tall_f: int = 0
	var inst_total: int = 0
	for inst in _instances(tower):
		inst_total += 1
		var asset: String = _asset_name(inst)
		if not groups.has(asset):
			groups[asset] = []
		(groups[asset] as Array).append(inst)
		var info: Dictionary = _flags(inst, tower)
		if int(info["cols"]) == 0:
			zero += 1
			if bool(info["tall"]):
				zero_tall += 1
			if bool(info["tall_f"]):
				zero_tall_f += 1
	var raw_u: int = 0
	var raw_n: int = 0
	var fil_u: int = 0
	var fil_n: int = 0
	var sample_cache: Dictionary = {}
	for asset_v in groups.keys():
		var arr: Array = groups[asset_v]
		var rep: Node3D = arr[0] as Node3D
		var mul: int = arr.size()
		var pack: Dictionary = _collect_shapes(rep)
		var grid: Dictionary = {}
		var bigs: Array = []
		_hash_tris(pack["tris"] as PackedVector3Array, grid, bigs)
		var boxes: Array = pack["boxes"] as Array
		for mi in _meshes(rep):
			# Batching hides the source mesh; the geometry and its colliders remain.
			if mi.mesh == null:
				continue
			if _up_extent(mi, tower) < MIN_H:
				continue
			var samples: PackedVector3Array = _samples(mi.mesh, sample_cache)
			if samples.is_empty():
				continue
			var uncovered: int = 0
			for p: Vector3 in samples:
				if not _near(mi.global_transform * p, boxes, grid, bigs):
					uncovered += 1
			var tot: int = samples.size()
			raw_u += uncovered * mul
			raw_n += tot * mul
			if not _name_excluded(String(mi.name)) and not _meta_blocked(mi):
				fil_u += uncovered * mul
				fil_n += tot * mul
	var ms: int = Time.get_ticks_msec() - t0
	var raw_pct: float = 100.0 * float(raw_u) / float(maxi(raw_n, 1))
	var fil_pct: float = 100.0 * float(fil_u) / float(maxi(fil_n, 1))
	print("[TT] leak instances=%d zero=%d zero_tall=%d zero_tall_filtered=%d" % [inst_total, zero, zero_tall, zero_tall_f])
	print("[TT] leak samples raw=%d/%d (%.2f%%) filtered=%d/%d (%.2f%%) ms=%d" % [raw_u, raw_n, raw_pct, fil_u, fil_n, fil_pct, ms])
	return {"instances": inst_total, "zero": zero, "zero_tall": zero_tall, "zero_tall_filtered": zero_tall_f,
		"raw_u": raw_u, "raw_n": raw_n, "fil_u": fil_u, "fil_n": fil_n, "ms": ms}


static func _instances(tower: Node3D) -> Array[Node3D]:
	var out: Array[Node3D] = []
	for tag in tower.get_children():
		if not String(tag.name).begins_with("Tag_"):
			continue
		for ch in tag.get_children():
			# MultiMesh stand-ins are not placed instances.
			if ch is Node3D and not String(ch.name).begins_with("MM_"):
				out.append(ch as Node3D)
	return out


static func _asset_name(inst: Node) -> String:
	var nm: String = String(inst.name)
	var u: int = nm.rfind("_")
	if u <= 0:
		return nm
	var tail: String = nm.substr(u + 1)
	if tail.is_valid_int():
		return nm.substr(0, u)
	return nm


static func _meshes(inst: Node) -> Array[MeshInstance3D]:
	var out: Array[MeshInstance3D] = []
	var stack: Array[Node] = [inst]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for ch in n.get_children():
			if ch is StaticBody3D and bool((ch as Node).get_meta("tt_fallback_collider", false)):
				continue
			stack.append(ch)
		if n is MeshInstance3D and (n as MeshInstance3D).mesh != null:
			out.append(n as MeshInstance3D)
	return out


static func _name_excluded(nm: String) -> bool:
	if nm.to_lower().contains("colonly"):
		return true
	if _skip.search(nm) != null:
		return true
	if _door.search(nm) != null:
		return true
	if _extra.search(nm) != null:
		return true
	if _dress != null and _dress.search(nm) != null:
		return true
	return false


static func _meta_blocked(n: Node) -> bool:
	var c: Node = n
	while c != null:
		if c.has_meta("tt_no_batch"):
			return true
		c = c.get_parent()
	return false


static func _up_extent(mi: MeshInstance3D, tower: Node3D) -> float:
	var ab: AABB = mi.mesh.get_aabb()
	var xf: Transform3D = tower.global_transform.affine_inverse() * mi.global_transform
	var p: Vector3 = ab.position
	var s: Vector3 = ab.size
	var mn: float = INF
	var mx: float = -INF
	for i: int in range(8):
		var c: Vector3 = xf * Vector3(p.x + s.x * float(i & 1), p.y + s.y * float((i >> 1) & 1), p.z + s.z * float((i >> 2) & 1))
		mn = minf(mn, c.y)
		mx = maxf(mx, c.y)
	return mx - mn


static func _instance_flags(inst: Node, tower: Node3D) -> Dictionary:
	var cols: int = 0
	var tall: bool = false
	var tall_f: bool = false
	var stair: bool = false
	var stack: Array[Node] = [inst]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for ch in n.get_children():
			stack.append(ch)
		if n is CollisionShape3D:
			var cs: CollisionShape3D = n as CollisionShape3D
			if not cs.disabled and cs.shape != null:
				cols += 1
				if _stair_body.search(String(cs.get_parent().name)) != null:
					stair = true
		elif n is MeshInstance3D:
			var mi: MeshInstance3D = n as MeshInstance3D
			if mi.mesh != null and _up_extent(mi, tower) >= MIN_H:
				tall = true
				if not _name_excluded(String(mi.name)) and not _meta_blocked(mi):
					tall_f = true
	return {"cols": cols, "tall": tall, "tall_f": tall_f, "stair": stair}


static func _flags(inst: Node, tower: Node3D) -> Dictionary:
	var key: String = _xform_key(inst, tower)
	if _flag_cache.has(key):
		return _flag_cache[key] as Dictionary
	var info: Dictionary = _instance_flags(inst, tower)
	_flag_cache[key] = info
	return info


static func _xform_key(inst: Node, tower: Node3D) -> String:
	var basis: Basis = (tower.global_transform.affine_inverse() * (inst as Node3D).global_transform).basis
	var x: Vector3 = basis.x
	var z: Vector3 = basis.z
	return "%s|%.3f,%.3f,%.3f|%.3f,%.3f,%.3f" % [_asset_name(inst), x.x, x.y, x.z, z.x, z.y, z.z]


static func _faces(mesh: Mesh) -> PackedVector3Array:
	var id: int = mesh.get_rid().get_id()
	if _face_cache.has(id):
		return _face_cache[id] as PackedVector3Array
	var faces: PackedVector3Array = mesh.get_faces()
	_face_cache[id] = faces
	return faces


static func _samples(mesh: Mesh, cache: Dictionary) -> PackedVector3Array:
	var id: int = mesh.get_rid().get_id()
	if cache.has(id):
		return cache[id] as PackedVector3Array
	var faces: PackedVector3Array = _faces(mesh)
	var ntri: int = faces.size() / 3
	var out: PackedVector3Array = PackedVector3Array()
	if ntri > 0:
		var want: int = mini(SAMPLE_N, ntri)
		for k: int in range(want):
			var ti: int = int((float(k) + 0.5) * float(ntri) / float(want))
			if ti >= ntri:
				ti = ntri - 1
			var a: Vector3 = faces[ti * 3]
			var b: Vector3 = faces[ti * 3 + 1]
			var c: Vector3 = faces[ti * 3 + 2]
			out.append(a * 0.2 + b * 0.3 + c * 0.5)
	cache[id] = out
	return out


static func _stand_asset(inst: Node) -> bool:
	return _asset_name(inst).contains("stand_module")


static func _stanchion_belt(inst: Node, nm: String) -> bool:
	return nm.to_lower() == "belt" and _asset_name(inst).contains("stanchion")


static func _decide(rep: Node3D, tower: Node3D, sample_cache: Dictionary, flags: Dictionary) -> Dictionary:
	var need: Dictionary = {}
	if _stand_asset(rep):
		return need
	var cols: int = int(flags["cols"])
	var stair: bool = bool(flags["stair"])
	var cands: Array[MeshInstance3D] = []
	for mi in _meshes(rep):
		if not mi.visible or mi.mesh == null:
			continue
		var nm: String = String(mi.name)
		if _name_excluded(nm) or _meta_blocked(mi):
			continue
		var span: Vector2 = _y_span(mi, tower)
		var belt: bool = _stanchion_belt(rep, nm)
		if span.y - span.x < MIN_H and not belt:
			continue
		# Overhead roofs, trusses and nets are not a walk-through at 0.1-2.0 m.
		if not belt and not _blocks_walker(span):
			continue
		if stair and _stair_mesh.search(nm) != null:
			continue
		if cols > 0 and _struct.search(nm) != null:
			continue
		if _already(mi):
			continue
		cands.append(mi)
	if cands.is_empty():
		return need
	var boxes: Array = []
	var grid: Dictionary = {}
	var bigs: Array = []
	if cols > 0:
		var pack: Dictionary = _collect_shapes(rep)
		boxes = pack["boxes"] as Array
		_hash_tris(pack["tris"] as PackedVector3Array, grid, bigs)
	for mi2: MeshInstance3D in cands:
		var nm2: String = String(mi2.name)
		var rid: int = mi2.mesh.get_rid().get_id()
		if cols == 0:
			need[rid] = nm2
			continue
		var samples: PackedVector3Array = _samples(mi2.mesh, sample_cache)
		if samples.is_empty():
			continue
		# Every sample already inside a box is covered. The triangle test is unchanged
		# when any sample misses the boxes.
		if not boxes.is_empty() and _all_in_boxes(mi2, samples, boxes):
			continue
		var uncovered: int = 0
		var covered: int = 0
		var n: int = samples.size()
		var stop_cover: int = int(ceil(0.70 * float(n) - 0.0001))
		var stop_open: int = int(floor(0.30 * float(n) + 0.0001))
		var add: bool = false
		var early: bool = false
		for p: Vector3 in samples:
			if _near(mi2.global_transform * p, boxes, grid, bigs):
				covered += 1
			else:
				uncovered += 1
			if covered >= stop_cover:
				add = false
				early = true
				break
			if uncovered > stop_open:
				add = true
				early = true
				break
		if not early:
			add = uncovered > stop_open
		if add:
			need[rid] = nm2
	return need


static func _all_in_boxes(mi: MeshInstance3D, samples: PackedVector3Array, boxes: Array) -> bool:
	for p: Vector3 in samples:
		var wp: Vector3 = mi.global_transform * p
		var hit: bool = false
		for b_v in boxes:
			var b: Dictionary = b_v as Dictionary
			if _box_near(wp, b["xf"] as Transform3D, b["half"] as Vector3):
				hit = true
				break
		if not hit:
			return false
	return true


static func _already(mi: MeshInstance3D) -> bool:
	for ch in mi.get_children():
		if ch is StaticBody3D and bool((ch as Node).get_meta("tt_fallback_collider", false)):
			return true
	return false


static func _apply(inst: Node3D, need: Dictionary, shape_cache: Dictionary, tower: Node3D, stair: bool, cols: int) -> Dictionary:
	var n: int = 0
	var tris: int = 0
	var boxes: int = 0
	var convex: int = 0
	var trimesh: int = 0
	var names: PackedStringArray = PackedStringArray()
	if need.is_empty() or _stand_asset(inst):
		return {"n": 0, "tris": 0, "names": names, "boxes": 0, "convex": 0, "trimesh": 0}
	for mi in _meshes(inst):
		if mi.mesh == null or not mi.visible:
			continue
		var nm: String = String(mi.name)
		if _name_excluded(nm) or _meta_blocked(mi):
			continue
		var span: Vector2 = _y_span(mi, tower)
		var belt: bool = _stanchion_belt(inst, nm)
		if span.y - span.x < MIN_H and not belt:
			continue
		if not belt and not _blocks_walker(span):
			continue
		if stair and _stair_mesh.search(nm) != null:
			continue
		if cols > 0 and _struct.search(nm) != null:
			continue
		var rid: int = mi.mesh.get_rid().get_id()
		if not need.has(rid):
			continue
		if _already(mi):
			continue
		var made: Dictionary = _shape_for(mi.mesh, nm, belt, shape_cache)
		var shape: Shape3D = made["shape"] as Shape3D
		if shape == null:
			continue
		var body: StaticBody3D = StaticBody3D.new()
		body.name = String(mi.name) + "_ttfb"
		body.collision_layer = LAYER
		body.collision_mask = 1
		body.set_meta("tt_fallback_collider", true)
		var cs: CollisionShape3D = CollisionShape3D.new()
		cs.shape = shape
		cs.position = made["pos"] as Vector3
		body.add_child(cs)
		mi.add_child(body)
		n += 1
		tris += int(made["tris"])
		var kind: String = String(made["kind"])
		if kind == "box" or kind == "belt":
			boxes += 1
		elif kind == "convex":
			convex += 1
		else:
			trimesh += 1
		if names.size() < 24:
			names.append(String(mi.name))
	return {"n": n, "tris": tris, "names": names, "boxes": boxes, "convex": convex, "trimesh": trimesh}


static func _shape_for(mesh: Mesh, nm: String, belt: bool, cache: Dictionary) -> Dictionary:
	var id: int = mesh.get_rid().get_id()
	var opening: bool = _opening.search(nm) != null
	var key: String = "%d|%s|%s" % [id, "b" if belt else "n", "o" if opening else "s"]
	if cache.has(key):
		return cache[key] as Dictionary
	var ab: AABB = mesh.get_aabb()
	var pack: Dictionary
	if belt:
		var box: BoxShape3D = BoxShape3D.new()
		# The visual belt is a 4 cm ribbon at y~0.90. A short box at hip height
		# stops the capsule; the posts already have their own colliders.
		box.size = Vector3(maxf(ab.size.x, 0.08), 0.42, maxf(ab.size.z, 0.10))
		var centre: Vector3 = ab.get_center()
		pack = {"shape": box, "pos": Vector3(centre.x, 0.75, centre.z), "tris": 12, "kind": "belt"}
	else:
		var kind: String = _kind(mesh, opening)
		if kind == "box":
			var box2: BoxShape3D = BoxShape3D.new()
			box2.size = Vector3(maxf(ab.size.x, 0.02), maxf(ab.size.y, 0.02), maxf(ab.size.z, 0.02))
			pack = {"shape": box2, "pos": ab.get_center(), "tris": 12, "kind": "box"}
		elif kind == "convex":
			var cv: ConvexPolygonShape3D = mesh.create_convex_shape(true, false)
			var tri_n: int = 12
			if cv != null:
				var dm: Mesh = cv.get_debug_mesh()
				if dm != null:
					tri_n = maxi(dm.get_faces().size() / 3, 4)
			pack = {"shape": cv, "pos": Vector3.ZERO, "tris": tri_n, "kind": "convex"}
		else:
			var made: Shape3D = mesh.create_trimesh_shape()
			var cc: ConcavePolygonShape3D = made as ConcavePolygonShape3D
			if cc != null:
				cc.backface_collision = true
			pack = {"shape": cc, "pos": Vector3.ZERO, "tris": _tri_count(mesh), "kind": "tri"}
	cache[key] = pack
	return pack


static func _kind(mesh: Mesh, opening: bool) -> String:
	if _boxy(mesh):
		return "box"
	if opening:
		return "tri"
	if _convexish(mesh):
		return "convex"
	return "tri"


static func _boxy(mesh: Mesh) -> bool:
	var faces: PackedVector3Array = _faces(mesh)
	if faces.size() < 12:
		return false
	var ab: AABB = mesh.get_aabb()
	var p: Vector3 = ab.position
	var s: Vector3 = ab.size
	var eps: float = 0.045
	var step: int = maxi(1, faces.size() / 48)
	var seen: int = 0
	var i: int = 0
	while i < faces.size():
		var v: Vector3 = faces[i]
		var on: bool = absf(v.x - p.x) <= eps or absf(v.x - (p.x + s.x)) <= eps
		on = on or absf(v.y - p.y) <= eps or absf(v.y - (p.y + s.y)) <= eps
		on = on or absf(v.z - p.z) <= eps or absf(v.z - (p.z + s.z)) <= eps
		if not on:
			return false
		seen += 1
		i += step
	if seen < 6:
		return false
	# Chair backs and handrails also sit on the AABB shell. A solid box's
	# triangles cover most of that shell; a sparse assembly does not.
	var area: float = 0.0
	var ntri: int = faces.size() / 3
	for t: int in range(ntri):
		var a: Vector3 = faces[t * 3]
		var b: Vector3 = faces[t * 3 + 1]
		var c: Vector3 = faces[t * 3 + 2]
		area += (b - a).cross(c - a).length() * 0.5
	var shell: float = 2.0 * (s.x * s.y + s.y * s.z + s.z * s.x)
	return shell > 0.0 and area >= shell * 0.55


static func _convexish(mesh: Mesh) -> bool:
	var faces: PackedVector3Array = _faces(mesh)
	var ntri: int = faces.size() / 3
	if ntri < 4:
		return false
	var step: int = maxi(1, ntri / 36)
	var acc: Vector3 = Vector3.ZERO
	var nv: int = 0
	var i: int = 0
	while i < ntri:
		acc += faces[i * 3] + faces[i * 3 + 1] + faces[i * 3 + 2]
		nv += 3
		i += step
	if nv == 0:
		return false
	var c: Vector3 = acc / float(nv)
	var ext: float = mesh.get_aabb().size.length()
	var tol: float = maxf(0.025, ext * 0.012)
	var bad: int = 0
	var tested: int = 0
	i = 0
	while i < ntri:
		var a: Vector3 = faces[i * 3]
		var b: Vector3 = faces[i * 3 + 1]
		var d: Vector3 = faces[i * 3 + 2]
		var nrm: Vector3 = (b - a).cross(d - a)
		if nrm.length_squared() >= 1e-10:
			nrm = nrm.normalized()
			tested += 1
			if nrm.dot(c - a) > tol:
				bad += 1
		i += step
	if tested < 6:
		return false
	return float(bad) / float(tested) <= 0.08


static func _y_span(mi: MeshInstance3D, tower: Node3D) -> Vector2:
	var ab: AABB = mi.mesh.get_aabb()
	var xf: Transform3D = tower.global_transform.affine_inverse() * mi.global_transform
	var p: Vector3 = ab.position
	var s: Vector3 = ab.size
	var mn: float = INF
	var mx: float = -INF
	for i: int in range(8):
		var c: Vector3 = xf * Vector3(p.x + s.x * float(i & 1), p.y + s.y * float((i >> 1) & 1), p.z + s.z * float((i >> 2) & 1))
		mn = minf(mn, c.y)
		mx = maxf(mx, c.y)
	return Vector2(mn, mx)


static func _blocks_walker(span: Vector2) -> bool:
	var mn: float = span.x
	var mx: float = span.y
	var f: float = -100.0
	var floors: Array[float] = [0.0, 6.1, 12.2]
	for fl: float in floors:
		if fl <= mn + 0.30:
			f = fl
	if f < -50.0:
		return false
	# Entirely above head relative to the floor under the mesh: roof, truss, net.
	if mn - f > 2.05:
		return false
	return mx > f + 0.10 and mn < f + 2.00


static func _print_zero(tower: Node3D) -> void:
	var by: Dictionary = {}
	var zero_n: int = 0
	var band_n: int = 0
	for inst in _instances(tower):
		var info: Dictionary = _flags(inst, tower)
		if int(info["cols"]) != 0:
			continue
		zero_n += 1
		var asset: String = _asset_name(inst)
		if not by.has(asset):
			by[asset] = [0, 0]
		var row: Array = by[asset]
		row[0] = int(row[0]) + 1
		var band: bool = false
		for mi in _meshes(inst):
			if mi.mesh == null:
				continue
			var nm: String = String(mi.name)
			if _name_excluded(nm) or _meta_blocked(mi):
				continue
			var span: Vector2 = _y_span(mi, tower)
			if _stanchion_belt(inst, nm) or _blocks_walker(span):
				band = true
				break
		if band:
			row[1] = int(row[1]) + 1
			band_n += 1
		by[asset] = row
	var names: Array = by.keys()
	names.sort()
	for asset_v in names:
		var asset2: String = String(asset_v)
		var row2: Array = by[asset2]
		var flag: String = "REACHABLE" if int(row2[1]) > 0 else "overhead"
		print("[TT] zero-collider %s instances=%d player_band=%d %s" % [asset2, int(row2[0]), int(row2[1]), flag])
	print("[TT] zero-collider instances=%d assets=%d player_band_instances=%d" % [zero_n, names.size(), band_n])


static func _tri_count(mesh: Mesh) -> int:
	var n: int = 0
	for s: int in range(mesh.get_surface_count()):
		var il: int = mesh.surface_get_array_index_len(s)
		if il >= 3:
			n += il / 3
		else:
			var arr: Array = mesh.surface_get_arrays(s)
			var v: PackedVector3Array = arr[Mesh.ARRAY_VERTEX] as PackedVector3Array
			if v != null:
				n += v.size() / 3
	return n


static func _collect_shapes(inst: Node) -> Dictionary:
	var boxes: Array = []
	var tris: PackedVector3Array = PackedVector3Array()
	var stack: Array[Node] = [inst]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for ch in n.get_children():
			stack.append(ch)
		if not (n is CollisionShape3D):
			continue
		var cs: CollisionShape3D = n as CollisionShape3D
		if cs.disabled or cs.shape == null:
			continue
		var xf: Transform3D = cs.global_transform
		var sh: Shape3D = cs.shape
		if sh is BoxShape3D:
			boxes.append({"xf": xf, "half": (sh as BoxShape3D).size * 0.5})
		elif sh is ConcavePolygonShape3D:
			var data: PackedVector3Array = (sh as ConcavePolygonShape3D).data
			for v: Vector3 in data:
				tris.append(xf * v)
		elif sh is ConvexPolygonShape3D:
			var dm: Mesh = sh.get_debug_mesh()
			if dm != null:
				var faces: PackedVector3Array = dm.get_faces()
				for v2: Vector3 in faces:
					tris.append(xf * v2)
	return {"boxes": boxes, "tris": tris}


static func _hash_tris(tris: PackedVector3Array, grid: Dictionary, bigs: Array) -> void:
	var n: int = tris.size() / 3
	for i: int in range(n):
		var a: Vector3 = tris[i * 3]
		var b: Vector3 = tris[i * 3 + 1]
		var c: Vector3 = tris[i * 3 + 2]
		var mn: Vector3 = a.min(b.min(c))
		var mx: Vector3 = a.max(b.max(c))
		var ext: Vector3 = mx - mn
		var c0: Vector3i = _cell(mn)
		var c1: Vector3i = _cell(mx)
		if ext.x > 2.0 or ext.y > 2.0 or ext.z > 2.0 or c1.x - c0.x > 4 or c1.y - c0.y > 4 or c1.z - c0.z > 4:
			bigs.append([a, b, c, mn, mx])
			continue
		for x: int in range(c0.x, c1.x + 1):
			for y: int in range(c0.y, c1.y + 1):
				for z: int in range(c0.z, c1.z + 1):
					var key: Vector3i = Vector3i(x, y, z)
					if not grid.has(key):
						grid[key] = []
					(grid[key] as Array).append([a, b, c, mn, mx])


static func _cell(p: Vector3) -> Vector3i:
	return Vector3i(floori(p.x / CELL), floori(p.y / CELL), floori(p.z / CELL))


static func _near(p: Vector3, boxes: Array, grid: Dictionary, bigs: Array) -> bool:
	for b_v in boxes:
		var b: Dictionary = b_v as Dictionary
		if _box_near(p, b["xf"] as Transform3D, b["half"] as Vector3):
			return true
	var c: Vector3i = _cell(p)
	for dx: int in range(-1, 2):
		for dy: int in range(-1, 2):
			for dz: int in range(-1, 2):
				var arr: Variant = grid.get(c + Vector3i(dx, dy, dz), null)
				if arr == null:
					continue
				for tri_v in arr as Array:
					if _tri_near(p, tri_v as Array):
						return true
	for tri_v2 in bigs:
		if _tri_near(p, tri_v2 as Array):
			return true
	return false


static func _box_near(p: Vector3, xf: Transform3D, half: Vector3) -> bool:
	var local: Vector3 = xf.affine_inverse() * p
	var q: Vector3 = local.abs() - half
	var ox: float = maxf(q.x, 0.0)
	var oy: float = maxf(q.y, 0.0)
	var oz: float = maxf(q.z, 0.0)
	return ox * ox + oy * oy + oz * oz <= COVER_R2


static func _tri_near(p: Vector3, tri: Array) -> bool:
	var mn: Vector3 = tri[3] as Vector3
	var mx: Vector3 = tri[4] as Vector3
	if p.x < mn.x - COVER_R or p.x > mx.x + COVER_R:
		return false
	if p.y < mn.y - COVER_R or p.y > mx.y + COVER_R:
		return false
	if p.z < mn.z - COVER_R or p.z > mx.z + COVER_R:
		return false
	return _dist2_tri(p, tri[0] as Vector3, tri[1] as Vector3, tri[2] as Vector3) <= COVER_R2


static func _dist2_tri(p: Vector3, a: Vector3, b: Vector3, c: Vector3) -> float:
	var ab: Vector3 = b - a
	var ac: Vector3 = c - a
	var ap: Vector3 = p - a
	var d1: float = ab.dot(ap)
	var d2: float = ac.dot(ap)
	if d1 <= 0.0 and d2 <= 0.0:
		return ap.length_squared()
	var bp: Vector3 = p - b
	var d3: float = ab.dot(bp)
	var d4: float = ac.dot(bp)
	if d3 >= 0.0 and d4 <= d3:
		return bp.length_squared()
	var vc: float = d1 * d4 - d3 * d2
	if vc <= 0.0 and d1 >= 0.0 and d3 <= 0.0:
		var v: float = d1 / (d1 - d3)
		var proj: Vector3 = a + ab * v
		return proj.distance_squared_to(p)
	var cp: Vector3 = p - c
	var d5: float = ab.dot(cp)
	var d6: float = ac.dot(cp)
	if d6 >= 0.0 and d5 <= d6:
		return cp.length_squared()
	var vb: float = d5 * d2 - d1 * d6
	if vb <= 0.0 and d2 >= 0.0 and d6 <= 0.0:
		var w: float = d2 / (d2 - d6)
		var proj2: Vector3 = a + ac * w
		return proj2.distance_squared_to(p)
	var va: float = d3 * d6 - d5 * d4
	if va <= 0.0 and (d4 - d3) >= 0.0 and (d5 - d6) >= 0.0:
		var w2: float = (d4 - d3) / ((d4 - d3) + (d5 - d6))
		var proj3: Vector3 = b + (c - b) * w2
		return proj3.distance_squared_to(p)
	var denom: float = va + vb + vc
	if absf(denom) < 1e-12:
		return ap.length_squared()
	var v2: float = vb / denom
	var w3: float = vc / denom
	var proj4: Vector3 = a + ab * v2 + ac * w3
	return proj4.distance_squared_to(p)


static func _find_mesh(inst: Node, nm: String) -> MeshInstance3D:
	var stack: Array[Node] = [inst]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n is MeshInstance3D and String(n.name) == nm and (n as MeshInstance3D).mesh != null:
			return n as MeshInstance3D
		for ch in n.get_children():
			stack.append(ch)
	return null


static func _seal_lifts(tower: Node3D) -> Dictionary:
	var n: int = 0
	var skipped: int = 0
	var space: PhysicsDirectSpaceState3D = null
	var world: World3D = tower.get_world_3d()
	if world != null:
		space = world.direct_space_state
	for inst in _instances(tower):
		if _asset_name(inst) != "tt_lift_core":
			continue
		if inst.get_node_or_null("LandingSeal_ttfb") != null:
			continue
		var doors: MeshInstance3D = _find_mesh(inst, "Landing_Doors")
		var wall: MeshInstance3D = _find_mesh(inst, "Door_Wall")
		var mi: MeshInstance3D = doors if doors != null else wall
		if mi == null:
			continue
		if _lift_opening_closed(inst, space):
			skipped += 1
			continue
		var ab: AABB = inst.global_transform.affine_inverse() * mi.global_transform * mi.mesh.get_aabb()
		var x0: float = ab.position.x - 0.02
		var x1: float = ab.position.x + ab.size.x + 0.02
		var y0: float = 0.0
		var y1: float = maxf(ab.position.y + ab.size.y, 2.30)
		var zc: float = ab.position.z + ab.size.z * 0.5
		var z0: float = zc - 0.05
		var z1: float = zc + 0.05
		if wall != null and wall.mesh != null:
			var wab: AABB = inst.global_transform.affine_inverse() * wall.global_transform * wall.mesh.get_aabb()
			z0 = maxf(z0, wab.position.z + 0.02)
			z1 = minf(z1, wab.position.z + wab.size.z - 0.02)
			if z1 - z0 < 0.04:
				z0 = wab.position.z + wab.size.z * 0.5 - 0.04
				z1 = z0 + 0.08
		var body: StaticBody3D = StaticBody3D.new()
		body.name = "LandingSeal_ttfb"
		body.collision_layer = LAYER
		body.collision_mask = 1
		body.set_meta("tt_fallback_collider", true)
		var cs: CollisionShape3D = CollisionShape3D.new()
		var box: BoxShape3D = BoxShape3D.new()
		box.size = Vector3(x1 - x0, y1 - y0, maxf(z1 - z0, 0.04))
		cs.shape = box
		cs.position = Vector3((x0 + x1) * 0.5, (y0 + y1) * 0.5, (z0 + z1) * 0.5)
		body.add_child(cs)
		inst.add_child(body)
		n += 1
	return {"added": n, "skipped": skipped}


static func _lift_opening_closed(inst: Node3D, space: PhysicsDirectSpaceState3D) -> bool:
	# Landing_Doors-colonly covers the opening (local x -1.97..1.47, y 0.16..2.24).
	var named: Node = _find_node(inst, "Landing_Doors-colonly")
	if named is StaticBody3D:
		for ch: Node in named.get_children():
			if ch is CollisionShape3D and not (ch as CollisionShape3D).disabled and (ch as CollisionShape3D).shape != null:
				return true
	if space == null:
		return false
	# Same-frame fallback if the named body is missing: chest-height rays into the shaft.
	var xs: Array[float] = [-1.0, 0.0, 1.0]
	for x: float in xs:
		var a: Vector3 = inst.global_transform * Vector3(x, 1.05, 2.35)
		var b: Vector3 = inst.global_transform * Vector3(x, 1.05, 0.35)
		var rq: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(a, b, LAYER)
		rq.hit_back_faces = true
		if not space.intersect_ray(rq).has("position"):
			return false
	return true


static func _find_node(inst: Node, nm: String) -> Node:
	var stack: Array[Node] = [inst]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if String(n.name) == nm:
			return n
		for ch: Node in n.get_children():
			stack.append(ch)
	return null
