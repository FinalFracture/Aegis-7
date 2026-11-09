shader_type spatial;
// Inward sky sphere. Stars are hashed in the mesh local frame so a spin of the
// node carries them, and so size and density stay even (no cylinder seam, no
// cube-face or pole pinch).
render_mode unshaded, cull_front, shadows_disabled, ambient_light_disabled;

uniform float cell_count = 48.0;
uniform float density_scale = 0.8;
uniform float star_radius = 0.00115;
uniform float nebula_strength = 0.16;

varying vec3 local_dir;

float hash13(vec3 p) {
	p = fract(p * vec3(0.1031, 0.1030, 0.0973));
	p += dot(p, p.yzx + 33.33);
	return fract((p.x + p.y) * p.z);
}

vec3 star_palette(float h) {
	float x = fract(h) * 6.0;
	if (x < 1.0) {
		return vec3(0.96, 0.98, 1.00);
	}
	if (x < 2.0) {
		return vec3(0.74, 0.88, 1.00);
	}
	if (x < 3.0) {
		return vec3(1.00, 0.93, 0.76);
	}
	if (x < 4.0) {
		return vec3(0.66, 0.84, 1.00);
	}
	if (x < 5.0) {
		return vec3(1.00, 0.78, 0.56);
	}
	return vec3(0.86, 0.76, 1.00);
}

// uv in [-1, 1] on the face. Matches cube_dir.
void cube_uv(vec3 dir, out float face, out vec2 uv) {
	vec3 ad = abs(dir);
	if (ad.x >= ad.y && ad.x >= ad.z) {
		if (dir.x >= 0.0) {
			face = 0.0;
			uv = vec2(-dir.z, dir.y) / ad.x;
		} else {
			face = 1.0;
			uv = vec2(dir.z, dir.y) / ad.x;
		}
	} else if (ad.y >= ad.z) {
		if (dir.y >= 0.0) {
			face = 2.0;
			uv = vec2(dir.x, -dir.z) / ad.y;
		} else {
			face = 3.0;
			uv = vec2(dir.x, dir.z) / ad.y;
		}
	} else {
		if (dir.z >= 0.0) {
			face = 4.0;
			uv = vec2(dir.x, dir.y) / ad.z;
		} else {
			face = 5.0;
			uv = vec2(-dir.x, dir.y) / ad.z;
		}
	}
}

vec3 cube_dir(float face, vec2 uv) {
	vec3 p = vec3(1.0, uv.y, -uv.x);
	if (face > 0.5 && face < 1.5) {
		p = vec3(-1.0, uv.y, uv.x);
	} else if (face < 2.5) {
		p = vec3(uv.x, 1.0, -uv.y);
	} else if (face < 3.5) {
		p = vec3(uv.x, -1.0, uv.y);
	} else if (face < 4.5) {
		p = vec3(uv.x, uv.y, 1.0);
	} else if (face >= 4.5) {
		p = vec3(-uv.x, uv.y, -1.0);
	}
	return normalize(p);
}

float cube_jac(vec2 uv) {
	float r2 = dot(uv, uv) + 1.0;
	return 1.0 / (r2 * sqrt(r2));
}

void vertex() {
	local_dir = VERTEX;
}

void fragment() {
	vec3 dir = normalize(local_dir);
	float face;
	vec2 uv;
	cube_uv(dir, face, uv);

	float n = max(cell_count, 2.0);
	vec2 cell_f = (uv * 0.5 + 0.5) * n;
	vec2 cell = clamp(floor(cell_f), vec2(0.0), vec2(n - 1.0));
	vec2 cuv = (cell + vec2(0.5)) / n * 2.0 - 1.0;
	float prob = min(density_scale * cube_jac(cuv), 1.0);

	// Near-black space. The nebula is a soft equatorial wash, much fainter than the old tiled band.
	vec3 col = vec3(0.005, 0.007, 0.012);
	float lat = abs(dir.x);
	float band = 1.0 - smoothstep(0.02, 0.70, lat);
	float az = atan(dir.z, dir.y);
	float wave = 0.5 + 0.5 * sin(az * 2.0 + sin(az * 5.0) * 0.55);
	vec3 neb = mix(vec3(0.018, 0.032, 0.055), vec3(0.030, 0.018, 0.042), wave);
	col = mix(col, neb, band * (0.35 + 0.65 * wave) * nebula_strength);

	vec3 id = vec3(cell.x, cell.y, face);
	float h = hash13(id + vec3(17.0, 0.0, 0.0));
	if (h < prob) {
		// Stay inside the cell so a star is not clipped by the neighbour boundary.
		float jx = hash13(id + vec3(3.1, 1.0, 0.0));
		float jy = hash13(id + vec3(9.7, 2.0, 0.0));
		vec2 suv = (cell + vec2(0.20 + 0.60 * jx, 0.20 + 0.60 * jy)) / n * 2.0 - 1.0;
		vec3 star_dir = cube_dir(face, suv);
		float ang = acos(clamp(dot(dir, star_dir), -1.0, 1.0));
		float hue = hash13(id + vec3(5.0, 0.0, 1.0));
		float bright_h = hash13(id + vec3(8.0, 4.0, 0.0));
		float beacon_h = hash13(id + vec3(40.0, 0.0, 2.0));
		// ~3% beacons, matching the old 95 / 3115 beacon share. Still 1-2 px.
		float beacon = step(0.97, beacon_h);
		float rad = star_radius * mix(0.55, 1.0, bright_h);
		rad *= mix(1.0, 1.12, beacon);
		float inten = mix(0.62, 1.0, bright_h);
		inten = mix(inten, 1.0, beacon);
		vec3 scol = mix(star_palette(hue), vec3(1.0), beacon * 0.85);
		float core = 1.0 - smoothstep(rad * 0.20, rad, ang);
		col = max(col, scol * inten * core);
	}

	ALBEDO = col;
}
