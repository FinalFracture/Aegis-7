extends RefCounted
## Audit walkability grid (0.5 m) in tower-local metres. Mask selects which
## bodies count (1 for the standalone tower, bit 18 inside the full hab).

const STEP := 0.5
const X0 := -13.0
const X1 := 141.0
const Z0 := -1.0
const Z1 := 80.5
const CELL_M2 := 0.25


static func collect(tower: Node3D, space: PhysicsDirectSpaceState3D, mask: int) -> Array:
	var t0: int = Time.get_ticks_msec()
	var ni: int = int((X1 - X0) / STEP)
	var nj: int = int((Z1 - Z0) / STEP)
	var cap: CapsuleShape3D = CapsuleShape3D.new()
	cap.radius = 0.30
	cap.height = 1.40
	var sq: PhysicsShapeQueryParameters3D = PhysicsShapeQueryParameters3D.new()
	sq.shape = cap
	sq.collision_mask = mask
	sq.margin = 0.0
	var basis: Basis = tower.global_transform.basis
	var nodes: Array = []
	for i: int in range(ni + 1):
		var x: float = X0 + float(i) * STEP
		for j: int in range(nj + 1):
			var z: float = Z0 + float(j) * STEP
			var top: float = 24.0
			for _g: int in range(10):
				var hit: Dictionary = _ray(space, tower, Vector3(x, top, z), Vector3(x, -6.0, z), mask)
				if not hit.has("position"):
					break
				var hp: Vector3 = tower.global_transform.affine_inverse() * (hit["position"] as Vector3)
				if hp.y >= top - 0.01:
					break
				var nrm: Vector3 = (tower.global_transform.basis.inverse() * (hit["normal"] as Vector3)).normalized()
				var ang: float = rad_to_deg(acos(clampf(nrm.dot(Vector3.UP), -1.0, 1.0)))
				if ang < 50.0:
					sq.transform = Transform3D(basis, tower.global_transform * Vector3(x, hp.y + 1.06, z))
					if space.intersect_shape(sq, 1).is_empty():
						nodes.append([snappedf(x, 0.01), snappedf(z, 0.01), snappedf(hp.y, 0.001), i, j, _support(hit, tower)])
				top = hp.y - 0.05
		if i % 40 == 0:
			print("[TT] walk scan x=%.1f nodes=%d ms=%d" % [x, nodes.size(), Time.get_ticks_msec() - t0])
	print("[TT] walk scan done nodes=%d ms=%d" % [nodes.size(), Time.get_ticks_msec() - t0])
	return nodes


static func drops(tower: Node3D, space: PhysicsDirectSpaceState3D, nodes: Array, mask: int) -> Array:
	var t0: int = Time.get_ticks_msec()
	var col: Dictionary = {}
	for idx: int in range(nodes.size()):
		var nd: Array = nodes[idx]
		var key: Vector2i = Vector2i(int(nd[3]), int(nd[4]))
		if not col.has(key):
			col[key] = []
		(col[key] as Array).append(idx)
	var dirs: Array[Vector2i] = [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]
	var box: BoxShape3D = BoxShape3D.new()
	var bq: PhysicsShapeQueryParameters3D = PhysicsShapeQueryParameters3D.new()
	bq.shape = box
	bq.collision_mask = mask
	bq.margin = 0.0
	var basis: Basis = tower.global_transform.basis
	var edges: Array = []
	for idx2: int in range(nodes.size()):
		var nd2: Array = nodes[idx2]
		var y: float = float(nd2[2])
		var x: float = float(nd2[0])
		var z: float = float(nd2[1])
		for dv: Vector2i in dirs:
			var k2: Vector2i = Vector2i(int(nd2[3]) + dv.x, int(nd2[4]) + dv.y)
			var close: bool = false
			for oi: int in col.get(k2, []):
				if absf(float((nodes[oi] as Array)[2]) - y) <= 0.36:
					close = true
					break
			if close:
				continue
			var nx: float = x + float(dv.x) * STEP
			var nz: float = z + float(dv.y) * STEP
			var hd: Dictionary = _ray(space, tower, Vector3(nx, y + 0.3, nz), Vector3(nx, y - 30.0, nz), mask)
			var drop: float = 30.0
			var low: String = ""
			if hd.has("position"):
				var hy: float = (tower.global_transform.affine_inverse() * (hd["position"] as Vector3)).y
				drop = y - hy
				low = _support(hd, tower)
			if drop < 0.5:
				continue
			box.size = Vector3(0.4 if dv.x != 0 else 0.3, 0.85, 0.3 if dv.x != 0 else 0.4)
			var mid: Vector3 = Vector3(x + float(dv.x) * STEP * 0.5, y + 0.575, z + float(dv.y) * STEP * 0.5)
			bq.transform = Transform3D(basis, tower.global_transform * mid)
			var guard_h: float = 0.0
			if not space.intersect_shape(bq, 1).is_empty():
				var hb: Dictionary = _ray(space, tower, Vector3(mid.x, y + 1.6, mid.z), Vector3(mid.x, y, mid.z), mask)
				guard_h = ((tower.global_transform.affine_inverse() * (hb["position"] as Vector3)).y - y) if hb.has("position") else 1.0
				if guard_h >= 1.0:
					continue
			edges.append([x, z, y, dv.x, dv.y, snappedf(drop, 0.01), snappedf(guard_h, 0.01), String(nd2[5]), low])
		if idx2 % 8000 == 0 and idx2 > 0:
			print("[TT] walk drops scan %d/%d edges=%d" % [idx2, nodes.size(), edges.size()])
	print("[TT] walk drops=%d ms=%d" % [edges.size(), Time.get_ticks_msec() - t0])
	return edges


static func analyze(nodes: Array) -> Dictionary:
	var n: int = nodes.size()
	var parent: PackedInt32Array = PackedInt32Array()
	var rank: PackedInt32Array = PackedInt32Array()
	parent.resize(n)
	rank.resize(n)
	for i: int in range(n):
		parent[i] = i
	var cell: Dictionary = {}
	for i2: int in range(n):
		var nd: Array = nodes[i2]
		var key: Vector2i = Vector2i(int(nd[3]), int(nd[4]))
		if not cell.has(key):
			cell[key] = []
		(cell[key] as Array).append(i2)
	var dirs: Array[Vector2i] = [Vector2i(1, 0), Vector2i(0, 1)]
	for i3: int in range(n):
		var nd3: Array = nodes[i3]
		var y: float = float(nd3[2])
		var ij: Vector2i = Vector2i(int(nd3[3]), int(nd3[4]))
		for dv: Vector2i in dirs:
			var lst: Variant = cell.get(ij + dv, null)
			if lst == null:
				continue
			for j: int in lst as Array:
				if absf(float((nodes[j] as Array)[2]) - y) <= 0.36:
					_union(parent, rank, i3, j)
	for i4: int in range(n):
		parent[i4] = _find(parent, i4)
	var counts: Dictionary = {}
	var per: Dictionary = {}
	for i5: int in range(n):
		var r: int = parent[i5]
		counts[r] = int(counts.get(r, 0)) + 1
		var b: int = _band(float((nodes[i5] as Array)[2]))
		if not per.has(r):
			per[r] = [0, 0, 0]
		var row: Array = per[r]
		row[b] = int(row[b]) + 1
		per[r] = row
	var main: int = -1
	var main_n: int = 0
	for r2 in counts.keys():
		if int(counts[r2]) > main_n:
			main_n = int(counts[r2])
			main = int(r2)
	var band_main: Array = [0, 0, 0]
	var band_largest: Array = [0, 0, 0]
	var band_root: Array = [-1, -1, -1]
	for r3 in per.keys():
		var row3: Array = per[r3]
		if int(r3) == main:
			band_main = [int(row3[0]), int(row3[1]), int(row3[2])]
		for b2: int in range(3):
			if int(row3[b2]) > int(band_largest[b2]):
				band_largest[b2] = int(row3[b2])
				band_root[b2] = int(r3)
	return {"nodes": nodes, "parent": parent, "main": main, "main_n": main_n,
		"band_main": band_main, "band_largest": band_largest, "band_root": band_root}


## Nodes on a large component that actually touches a floor. Drops furniture
## tops, stand tiers and roof islands out of the rail scan.
static func player_floor_nodes(nodes: Array, analysis: Dictionary) -> Array:
	var parent: PackedInt32Array = analysis["parent"]
	var counts: Dictionary = {}
	var floorish: Dictionary = {}
	for i: int in range(nodes.size()):
		var r: int = parent[i]
		counts[r] = int(counts.get(r, 0)) + 1
		var y: float = float((nodes[i] as Array)[2])
		if absf(y) <= 0.45 or absf(y - 6.1) <= 0.45 or absf(y - 12.2) <= 0.45:
			floorish[r] = int(floorish.get(r, 0)) + 1
	var keep_root: Dictionary = {}
	keep_root[int(analysis["main"])] = true
	for r2 in counts.keys():
		if int(counts[r2]) >= 160 and int(floorish.get(r2, 0)) >= 12:
			keep_root[int(r2)] = true
	var out: Array = []
	for i2: int in range(nodes.size()):
		if keep_root.has(parent[i2]):
			out.append(nodes[i2])
	print("[TT] walk floor nodes=%d / %d components=%d" % [out.size(), nodes.size(), keep_root.size()])
	return out


static func report(tag: String, a: Dictionary) -> void:
	var bm: Array = a["band_main"]
	var bl: Array = a["band_largest"]
	print("[TT] walk %s main_m2=%.1f nodes=%d F1=%.1f F2=%.1f F3=%.1f band_largest F1=%.1f F2=%.1f F3=%.1f" % [
		tag, float(a["main_n"]) * CELL_M2, int(a["main_n"]),
		float(bm[0]) * CELL_M2, float(bm[1]) * CELL_M2, float(bm[2]) * CELL_M2,
		float(bl[0]) * CELL_M2, float(bl[1]) * CELL_M2, float(bl[2]) * CELL_M2])
	var nodes: Array = a["nodes"]
	var parent: PackedInt32Array = a["parent"]
	var main: int = int(a["main"])
	var band_root: Array = a["band_root"]
	for m: Array in _markers():
		var best: int = -1
		var best_d: float = 1.0
		var mx: float = float(m[1])
		var mz: float = float(m[2])
		var my: float = float(m[3])
		for i: int in range(nodes.size()):
			var nd: Array = nodes[i]
			var dx: float = float(nd[0]) - mx
			var dz: float = float(nd[1]) - mz
			var d: float = sqrt(dx * dx + dz * dz)
			if d <= best_d and absf(float(nd[2]) - my) <= 1.5:
				best_d = d
				best = i
		if best < 0:
			print("[TT] walk marker %s %s MISSING" % [tag, String(m[0])])
		else:
			var ndb: Array = nodes[best]
			var band: int = _band(float(ndb[2]))
			var in_main: bool = parent[best] == main
			var in_band: bool = parent[best] == int(band_root[band])
			print("[TT] walk marker %s %s q=(%.2f,%.2f,%.2f) main=%s band=%s" % [
				tag, String(m[0]), float(ndb[0]), float(ndb[2]), float(ndb[1]), str(in_main), str(in_band)])


static func diff(before: Dictionary, after: Dictionary) -> void:
	var b_all: Dictionary = _keys(before["nodes"], before["parent"], -1)
	var b_main: Dictionary = _keys(before["nodes"], before["parent"], int(before["main"]))
	var a_all: Dictionary = _keys(after["nodes"], after["parent"], -1)
	var a_main: Dictionary = _keys(after["nodes"], after["parent"], int(after["main"]))
	var sealed: Array = []
	var split: Array = []
	for k in b_main.keys():
		var parts: PackedStringArray = String(k).split("|")
		var i: int = int(parts[0])
		var j: int = int(parts[1])
		var yb: int = int(parts[2])
		if not _near_key(a_all, i, j, yb):
			sealed.append(Vector3i(i, j, _band(float(yb) * 0.5)))
		elif not _near_key(a_main, i, j, yb):
			split.append(Vector3i(i, j, _band(float(yb) * 0.5)))
	print("[TT] walk lost sealed=%d split=%d (main-component cells)" % [sealed.size(), split.size()])
	_clusters("sealed", sealed)
	_clusters("split", split)


static func _clusters(tag: String, cells: Array) -> void:
	var have: Dictionary = {}
	for c: Vector3i in cells:
		have[c] = true
	var seen: Dictionary = {}
	var found: Array = []
	for c2: Vector3i in cells:
		if seen.has(c2):
			continue
		var stack: Array[Vector3i] = [c2]
		seen[c2] = true
		var cnt: int = 0
		var min_i: int = c2.x
		var max_i: int = c2.x
		var min_j: int = c2.y
		var max_j: int = c2.y
		var band: int = c2.z
		while not stack.is_empty():
			var k: Vector3i = stack.pop_back()
			cnt += 1
			min_i = mini(min_i, k.x)
			max_i = maxi(max_i, k.x)
			min_j = mini(min_j, k.y)
			max_j = maxi(max_j, k.y)
			for dv: Vector2i in [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]:
				var n: Vector3i = Vector3i(k.x + dv.x, k.y + dv.y, band)
				if have.has(n) and not seen.has(n):
					seen[n] = true
					stack.append(n)
		if cnt >= 16:
			found.append([cnt, min_i, max_i, min_j, max_j, band])
	found.sort_custom(func(a: Array, b: Array) -> bool: return int(a[0]) > int(b[0]))
	var lim: int = mini(found.size(), 18)
	for t: int in range(lim):
		var f: Array = found[t]
		print("[TT] walk region %s n=%d m2=%.1f F%d x=%.1f..%.1f z=%.1f..%.1f" % [
			tag, int(f[0]), float(f[0]) * CELL_M2, int(f[5]) + 1,
			X0 + float(f[1]) * STEP, X0 + float(f[2]) * STEP,
			Z0 + float(f[3]) * STEP, Z0 + float(f[4]) * STEP])


static func _keys(nodes: Array, parent: PackedInt32Array, main: int) -> Dictionary:
	var d: Dictionary = {}
	for i: int in range(nodes.size()):
		if main >= 0 and parent[i] != main:
			continue
		var nd: Array = nodes[i]
		d["%d|%d|%d" % [int(nd[3]), int(nd[4]), int(round(float(nd[2]) * 2.0))]] = true
	return d


static func _near_key(keys: Dictionary, i: int, j: int, yb: int) -> bool:
	for dy: int in range(-1, 2):
		if keys.has("%d|%d|%d" % [i, j, yb + dy]):
			return true
	return false


static func _band(y: float) -> int:
	if y < 4.0:
		return 0
	if y < 10.0:
		return 1
	return 2


static func _find(parent: PackedInt32Array, a: int) -> int:
	while parent[a] != a:
		parent[a] = parent[parent[a]]
		a = parent[a]
	return a


static func _union(parent: PackedInt32Array, rank: PackedInt32Array, a: int, b: int) -> void:
	var ra: int = _find(parent, a)
	var rb: int = _find(parent, b)
	if ra == rb:
		return
	if rank[ra] < rank[rb]:
		parent[ra] = rb
	elif rank[ra] > rank[rb]:
		parent[rb] = ra
	else:
		parent[rb] = ra
		rank[ra] += 1


static func _ray(space: PhysicsDirectSpaceState3D, tower: Node3D, a: Vector3, b: Vector3, mask: int) -> Dictionary:
	var rq: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(tower.global_transform * a, tower.global_transform * b, mask)
	rq.hit_back_faces = true
	return space.intersect_ray(rq)


static func _support(hit: Dictionary, tower: Node) -> String:
	var n: Node = hit.get("collider") as Node
	if n == null:
		return ""
	var body: String = String(n.name)
	var inst: String = ""
	var c: Node = n
	while c != null and c != tower:
		var p: Node = c.get_parent()
		if p != null and String(p.name).begins_with("Tag_"):
			inst = String(c.name)
			break
		c = p
	if inst == "":
		return body
	return inst + "|" + body


static func _markers() -> Array:
	return [
		["S_inside", 72.0, 6.0, 0.2],
		["N_inside", 72.0, 73.0, 0.2],
		["E_inside", 135.0, 37.5, 0.2],
		["W_foyer", -6.0, 39.5, 0.2],
		["stair_foot", 39.2, 18.9, 0.2],
		["stair_f2", 38.6, 18.9, 6.1],
		["court_aisle", 55.0, 27.0, 0.2],
		["food", 70.0, 72.0, 0.2],
		["arcade", 130.0, 49.0, 0.2],
		["restroom_side", 33.4, 70.0, 0.2],
		["gallery_f2", -8.0, 40.0, 6.1],
		["concourse", 50.0, 40.0, 0.2],
	]
