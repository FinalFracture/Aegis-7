// RFID Force-Field Door field shader (apply to FieldPlane of rfid_forcefield_door.glb).
// dissolve: 0 = solid field (closed), 1 = fully gone (open). Drive with a ~0.8 s tween in code:
//   create_tween().tween_property(mat, "shader_parameter/dissolve", 1.0, 0.8)   # open
//   create_tween().tween_property(mat, "shader_parameter/dissolve", 0.0, 0.8)   # close
// field_color / opacity are meant to be exposed to the Python settings UI.
// Texture is fully procedural (hash/value noise, TIME-driven): TV static, crawling electric
// filaments, fuzzy edge falloff toward the emitter strip, scanline shimmer/jitter.
// Never a flat fill, even at opacity = 1.
shader_type spatial;
render_mode unshaded, blend_mix, cull_disabled, depth_draw_never, shadows_disabled;

uniform vec4 field_color : source_color = vec4(0.45, 0.92, 1.0, 1.0);
uniform float opacity : hint_range(0.0, 1.0) = 0.45;
uniform float dissolve : hint_range(0.0, 1.0) = 0.0;
uniform vec2 cell_count = vec2(24.0, 39.0);        // dissolve pixel cells across (W) x up (H)
uniform float static_strength : hint_range(0.0, 1.0) = 0.35;  // fine flickering TV static
uniform float arc_strength : hint_range(0.0, 2.0) = 0.8;      // crawling electric filaments
uniform float arc_speed : hint_range(0.0, 4.0) = 0.6;
uniform float edge_fuzz : hint_range(0.0, 0.3) = 0.07;        // soft falloff width where field meets emitter
uniform float edge_glow : hint_range(0.0, 3.0) = 0.9;
uniform float scanline_density = 140.0;
uniform float scanline_strength : hint_range(0.0, 1.0) = 0.15;
uniform float jitter_strength : hint_range(0.0, 0.02) = 0.004;
uniform float glow_energy : hint_range(0.0, 6.0) = 1.2;

float hash21(vec2 p) {
	p = fract(p * vec2(123.34, 456.21));
	p += dot(p, p + 45.32);
	return fract(p.x * p.y);
}

float vnoise(vec2 p) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	f = f * f * (3.0 - 2.0 * f);
	float a = hash21(i);
	float b = hash21(i + vec2(1.0, 0.0));
	float c = hash21(i + vec2(0.0, 1.0));
	float d = hash21(i + vec2(1.0, 1.0));
	return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

float fbm2(vec2 p) {
	return vnoise(p) * 0.65 + vnoise(p * 2.13 + 7.1) * 0.35;
}

// thin bright line where a warped noise field crosses 0.5 -> wandering filament
float filament(vec2 p, float t, float width) {
	float n = fbm2(p + vec2(t * 0.7, -t));
	return 1.0 - smoothstep(0.0, width, abs(n - 0.5));
}

void fragment() {
	float t = TIME;
	vec2 uv = UV;
	vec2 aspect = vec2(1.0, 1.633);                  // 2.45 / 1.50

	// --- dissolve pixel cells (unjittered so blocks stay crisp) ---
	vec2 cell = floor(uv * cell_count);
	float h = hash21(cell);
	float alive = step(dissolve, h * 0.999);
	float near = 1.0 - smoothstep(0.0, 0.10, h - dissolve);
	float pixel_flash = near * step(0.001, dissolve) * alive * 0.8;
	vec2 cf = fract(uv * cell_count);
	float grid = step(0.88, max(cf.x, cf.y)) * clamp(dissolve * 4.0, 0.0, 1.0) * (1.0 - dissolve);

	// --- scanline shimmer + horizontal jitter (per-row, steps ~12 Hz) ---
	float row = floor(uv.y * 90.0);
	float tick = floor(t * 12.0);
	float jit = (hash21(vec2(row, tick)) - 0.5) * jitter_strength
	          * step(0.82, hash21(vec2(floor(uv.y * 9.0), tick)));
	vec2 juv = uv + vec2(jit, 0.0);
	float scan = 1.0 - scanline_strength * (0.5 + 0.5 * sin((juv.y * scanline_density - t * 5.0) * 6.2831));
	float shimmer = 0.92 + 0.08 * vnoise(vec2(juv.y * 6.0 - t * 1.3, t * 0.5));

	// --- fine TV static (re-seeded ~24x/s) ---
	vec2 sp = floor(juv * vec2(220.0, 360.0));
	float st = hash21(sp + vec2(floor(t * 24.0) * 17.0, 0.0));
	float stat = mix(1.0, 0.55 + 0.9 * st, static_strength);

	// --- crawling electric filaments (two layers) ---
	vec2 ap = juv * aspect;
	float arcs = filament(ap * 3.0, t * arc_speed, 0.018) * 0.8
	           + filament(ap * 5.5 + 3.3, t * arc_speed * 1.6, 0.012) * 0.5;
	float arc_flick = 0.6 + 0.4 * vnoise(vec2(t * 9.0, 1.7));
	arcs *= arc_strength * arc_flick;

	// --- low-frequency fuzzy body variation (cloudy, never flat) ---
	float body = 0.75 + 0.35 * fbm2(ap * 4.0 + vec2(0.0, -t * 0.4));

	// --- fuzzy edge: soft fade into emitter + noisy glow rim ---
	float e = min(min(uv.x, 1.0 - uv.x) * 1.0, min(uv.y, 1.0 - uv.y) * 1.633);
	float fuzzn = vnoise(ap * 40.0 + t * 3.0);
	float edge_fade = smoothstep(0.0, edge_fuzz, e + (fuzzn - 0.5) * edge_fuzz * 0.6);
	float rim = (1.0 - smoothstep(0.0, edge_fuzz * 1.6, e)) * edge_glow * (0.6 + 0.6 * fuzzn);

	float lum = body * stat * scan * shimmer + arcs + rim + pixel_flash;
	vec3 col = field_color.rgb * glow_energy * lum * (1.0 - 0.35 * grid);
	col += vec3(0.85, 0.95, 1.0) * arcs * 0.35;     // whitish arc cores

	float a = opacity * field_color.a * alive * edge_fade * (0.55 + 0.45 * body * stat * scan) ;
	a = max(a, alive * clamp((arcs + rim * 0.5) * opacity, 0.0, 1.0));
	ALBEDO = col;
	ALPHA = clamp(a, 0.0, 1.0);
}
