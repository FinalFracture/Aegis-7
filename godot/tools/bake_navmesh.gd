extends SceneTree
## Bake the preface playable-area navmesh (D670-05).
## Covers interior + exterior walk: ramp, platform, hatch, walkways.
##   xvfb-run -a godot --path godot --rendering-driver opengl3 -s res://tools/bake_navmesh.gd -- --qa-placement
## --qa-placement is a user arg so preface_playable_area keeps interior streaming off.
## The scene skips PlayableNavRegion while this script is on the command line.
## Exit 0 when the baked mesh has at least one polygon, else 1.

const SCENE_PATH := "res://scenes/preface/preface_playable_area.tscn"
const NAV_PATH := "res://assets/nav/preface_navmesh.tres"
const SETTLE_FRAMES := 30

var _scene: Node = null
var _frames: int = 0
var _done: bool = false


func _initialize() -> void:
	var packed: PackedScene = load(SCENE_PATH) as PackedScene
	if packed == null:
		print("NAVMESH_BAKE polygons=0")
		quit(1)
		return
	var inst: Node = packed.instantiate()
	if inst == null:
		print("NAVMESH_BAKE polygons=0")
		quit(1)
		return
	# Before add_child so _ready sees it even when --qa-placement is omitted.
	# Headless boot otherwise sets _validate_only and quits the tree at frame 4.
	inst.set("_qa_placement", true)
	if "_validate_only" in inst:
		inst.set("_validate_only", false)
	root.add_child(inst)
	_scene = inst


func _process(_delta: float) -> bool:
	if _done:
		return true
	_frames += 1
	if _frames < SETTLE_FRAMES:
		return false
	_done = true
	_bake()
	return true


func _bake() -> void:
	var navmesh := NavigationMesh.new()
	navmesh.agent_radius = 0.35
	navmesh.agent_height = 1.75
	navmesh.agent_max_climb = 0.3
	navmesh.cell_size = 0.1
	navmesh.cell_height = 0.05
	navmesh.geometry_parsed_geometry_type = NavigationMesh.PARSED_GEOMETRY_STATIC_COLLIDERS
	var source := NavigationMeshSourceGeometryData3D.new()
	NavigationServer3D.parse_source_geometry_data(navmesh, source, _scene)
	NavigationServer3D.bake_from_source_geometry_data(navmesh, source)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://assets/nav"))
	var err := ResourceSaver.save(navmesh, NAV_PATH)
	var n := navmesh.get_polygon_count()
	print("NAVMESH_BAKE polygons=%d" % n)
	quit(0 if err == OK and n > 0 else 1)
