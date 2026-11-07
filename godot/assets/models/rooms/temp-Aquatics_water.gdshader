shader_type spatial;
render_mode diffuse_burley, specular_schlick_ggx, cull_back;
// Opaque animated normal, never ALPHA/BLEND; shares one material across all pools.
void fragment() {
    vec2 q = UV * 18.0;
    float u = sin(q.x * 1.8 + q.y * 0.8 + TIME * 0.65);
    float v = cos(q.y * 2.1 - q.x * 0.6 - TIME * 0.48);
    NORMAL_MAP = normalize(vec3(u * 0.11, v * 0.11, 1.0)) * 0.5 + 0.5;
    NORMAL_MAP_DEPTH = 0.65;
    ALBEDO = vec3(0.025, 0.31, 0.37) + vec3(0.005, 0.022, 0.024) * (u * v);
    ROUGHNESS = 0.24;
    METALLIC = 0.0;
}
