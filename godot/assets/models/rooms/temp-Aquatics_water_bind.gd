extends Node3D
# One shared opaque material; no alpha sorting and no duplicate water surface.
func _ready() -> void:
    var material := ShaderMaterial.new()
    material.shader = preload("res://assets/models/rooms/temp-Aquatics_water.gdshader")
    _apply_water(self, material)

func _apply_water(node: Node, material: ShaderMaterial) -> void:
    if node is MeshInstance3D and node.mesh:
        for surface in node.mesh.get_surface_count():
            var old = node.mesh.surface_get_material(surface)
            if old and old.resource_name == "TT_OpaquePoolWater":
                node.set_surface_override_material(surface, material)
    for child in node.get_children():
        _apply_water(child, material)
