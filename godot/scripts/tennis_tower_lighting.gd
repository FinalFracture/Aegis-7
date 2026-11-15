extends RefCounted
## Gage: cheap F1-F3 interior lights. gl_compatibility pays an extra pass per object per light,
## and only 8 lights may hit one object, so ranges stay short and the count stays small.
## Shadows stay off. Emissive soffit panels are unshaded and marked tt_no_batch.


static func run(tower: Node3D) -> void:
	var root: Node3D = Node3D.new()
	root.name = "TT_InteriorLights"
	tower.add_child(root)
	var omni: int = 0
	var spot: int = 0
	var shadowed: int = 0
	var panels: int = 0
	# F1 west foyer / lobby. The --shot-tower / --qa-tower-draw eye sits near (-9, 1.7, 44).
	var foyer: Array[Vector3] = [
		Vector3(-8.0, 3.1, 24.0), Vector3(-8.0, 3.1, 36.0), Vector3(-8.0, 3.1, 46.0), Vector3(-8.0, 3.1, 58.0),
		Vector3(2.0, 3.1, 24.0), Vector3(2.0, 3.1, 36.0), Vector3(2.0, 3.1, 46.0), Vector3(2.0, 3.1, 58.0),
	]
	for i: int in range(foyer.size()):
		# Higher energy, same short range: the lobby shot stays inside these volumes.
		_omni(root, "TT_Omni_F1W_%d" % i, foyer[i], Color("#F6E6CC"), 8.0, 9.0, 0.5)
		omni += 1
	# Low fill along the lobby shot, eye (-9, 1.7, 44) looking toward (2, 1.4, 30).
	var near_floor: Array[Vector3] = [Vector3(-7.6, 2.0, 42.2), Vector3(-4.2, 2.0, 37.8), Vector3(-0.5, 2.0, 33.2)]
	for i: int in range(near_floor.size()):
		_omni(root, "TT_Omni_F1Near_%d" % i, near_floor[i], Color("#F8E8D0"), 9.0, 9.0, 0.4)
		omni += 1
	# South lobby around the S door (plan X 72, Z 6).
	var south: Array[Vector3] = [Vector3(66.0, 3.1, 8.0), Vector3(76.0, 3.1, 8.0), Vector3(72.0, 3.1, 16.0)]
	for i: int in range(south.size()):
		_omni(root, "TT_Omni_F1S_%d" % i, south[i], Color("#F6E6CC"), 2.0, 9.0)
		omni += 1
	# Walked stair cores and the west lift, F1 and F2. One short omni each.
	var cores: Array[Vector3] = [
		Vector3(35.1, 3.2, 17.75), Vector3(35.1, 9.3, 17.75),
		Vector3(35.1, 3.2, 61.25), Vector3(35.1, 9.3, 61.25),
		Vector3(28.0, 3.2, 36.5), Vector3(28.0, 9.3, 36.5),
	]
	for i: int in range(cores.size()):
		_omni(root, "TT_Omni_Core_%d" % i, cores[i], Color("#E4EAF2"), 1.6, 8.0)
		omni += 1
	# A few F2 / F3 fills so the upper floors are not black.
	var upper: Array[Vector3] = [
		Vector3(-4.0, 9.2, 32.0), Vector3(-4.0, 9.2, 52.0), Vector3(6.0, 9.2, 42.0),
		Vector3(-4.0, 15.3, 32.0), Vector3(-4.0, 15.3, 52.0), Vector3(6.0, 15.3, 42.0),
	]
	for i: int in range(upper.size()):
		_omni(root, "TT_Omni_Up_%d" % i, upper[i], Color("#F3E4CC"), 1.6, 9.0)
		omni += 1
	# Downward spots over the foyer view. Shadows stay off so the lobby draw does not multiply.
	var spots: Array[Vector3] = [Vector3(-8.0, 5.2, 42.0), Vector3(-1.0, 5.2, 32.0), Vector3(4.0, 5.2, 46.0)]
	for i: int in range(spots.size()):
		_spot(root, "TT_Spot_F1W_%d" % i, spots[i], Color("#FFF2DC"), 6.0, 10.0)
		spot += 1
	var mat: StandardMaterial3D = _panel_material()
	var mesh: BoxMesh = BoxMesh.new()
	mesh.size = Vector3(10.0, 0.04, 5.0)
	var panel_pts: Array[Vector3] = [
		Vector3(-2.0, 5.75, 26.0), Vector3(-2.0, 5.75, 42.0), Vector3(-2.0, 5.75, 58.0),
		Vector3(72.0, 5.75, 10.0),
		Vector3(-2.0, 11.85, 26.0), Vector3(-2.0, 11.85, 42.0), Vector3(-2.0, 11.85, 58.0),
		Vector3(72.0, 11.85, 10.0),
	]
	for i: int in range(panel_pts.size()):
		var mi: MeshInstance3D = MeshInstance3D.new()
		mi.name = "TT_Soffit_%d" % i
		mi.mesh = mesh
		mi.material_override = mat
		mi.position = panel_pts[i]
		mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		mi.set_meta("tt_no_batch", true)
		root.add_child(mi)
		panels += 1
	print("[TT] interior lights omni=%d spot=%d shadowed=%d panels=%d" % [omni, spot, shadowed, panels])


static func _omni(root: Node3D, nm: String, pos: Vector3, col: Color, energy: float, rng: float, atten: float = 1.15) -> void:
	var l: OmniLight3D = OmniLight3D.new()
	l.name = nm
	l.position = pos
	l.light_color = col
	l.light_energy = energy
	l.omni_range = rng
	l.omni_attenuation = atten
	l.shadow_enabled = false
	root.add_child(l)


static func _spot(root: Node3D, nm: String, pos: Vector3, col: Color, energy: float, rng: float) -> void:
	var l: SpotLight3D = SpotLight3D.new()
	l.name = nm
	l.position = pos
	# Same downward pitch as the preface ceiling spots.
	l.rotation_degrees = Vector3(-90.0, 0.0, 0.0)
	l.light_color = col
	l.light_energy = energy
	l.spot_range = rng
	l.spot_angle = 62.0
	l.spot_angle_attenuation = 0.45
	l.shadow_enabled = false
	root.add_child(l)


static func _panel_material() -> StandardMaterial3D:
	var m: StandardMaterial3D = StandardMaterial3D.new()
	m.resource_name = "TT_SoffitPanel"
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.albedo_color = Color(1.0, 0.94, 0.82, 1.0)
	m.emission_enabled = true
	m.emission = Color(1.0, 0.93, 0.80)
	m.emission_energy_multiplier = 1.7
	return m
