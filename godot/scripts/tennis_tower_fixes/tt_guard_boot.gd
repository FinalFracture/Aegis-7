extends SceneTree
## Headless: standalone tower, walk grid, collider fallback, guard JSON.
##   godot --headless --path godot -s res://scripts/tennis_tower_fixes/tt_guard_boot.gd


func _initialize() -> void:
	var n: Node = Node.new()
	n.set_script(load("res://scripts/tennis_tower_fixes/tt_guard_gen.gd"))
	root.add_child(n)
