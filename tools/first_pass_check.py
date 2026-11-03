#!/usr/bin/env python3
"""First-pass checker for Cylinder Hab-7 / Aegis-7 (docs/FIRST_PASS_CHECKLIST.md).

Usage:
    python tools/first_pass_check.py <scene or path> [--no-godot] [--strict]

Read-only: never writes into the repo. The optional headless Godot probe is
written to a system temp dir and deleted afterwards. Python stdlib only.
Prints PASS / WARN / FAIL per check plus a summary. Exit code 1 on any FAIL
(with --strict, WARN also fails). Exit code 2 on usage errors.
"""
import argparse, hashlib, json, os, re, shutil, struct, subprocess, sys, tempfile, textwrap

# ============================== CONFIG ======================================
CONFIG = {
    # Jared-confirmed values
    "wall_mount_gap_max_m": 0.010,        # wall-mounted items <= 10 mm from wall
    "prop_back_gap_min_m": 0.000,         # prop backs 0..50 mm
    "prop_back_gap_max_m": 0.050,
    "stair_collider_max_deg": 35.0,       # stair colliders <= 35 deg
    "walkable_max_deg": 45.0,             # any walkable surface < 45 deg
    "ramp_max_ratio": 1.0 / 12.0,         # accessible ramps <= 1:12
    "accent_colors": ["#FF9500", "#282E38"],  # OLED amber, gunmetal
    "forbid_wood_albedo": True,
    # Patch brief / checklist defaults
    "floor_contact_tol_m": 0.005,
    "subpart_overlap_max_m": 0.010,
    "portal_intrusion_max_m": 0.010,
    "capsule_radius_m": 0.35,
    "capsule_height_m": 1.75,
    "capsule_escape_dist_m": 0.6,
    "capsule_escape_min_dirs": 2,
    "cast_start_back_m": 0.4,
    "prop_tri_max": 6000,
    "albedo_bright_max": 0.9,
    "emission_energy_max": 1.5,
    "texture_max_px": 4096,
    "oversized_file_mb": 50.0,
    "accent_hue_tol_deg": 8.0,            # colours this close to amber hue must be exact
    "godot_timeout_s": 120,
    "godot_bin_candidates": ["godot", "godot4", "Godot_v4.7-stable_win64_console.exe"],
    # names
    "debug_name_words": ["debug", "test", "temp", "tmp", "placeholder"],  # matched as whole name tokens
    "glass_hardware_re": r"(?i)(clamp|bracket|bolt|screw|mount|hinge|fixing|fitting|frame|holder|spigot|standoff)",
    "nonmetal_name_re": r"(?i)(concrete|paint|slate|composite|plastic|fabric|rubber|ceramic|stone|tile|plaster|foam|cloth|glass|leather|vinyl)",
    "metal_name_re": r"(?i)(metal|steel|alloy|gunmetal|chrome|alumin|brass|copper|iron|titan)",
    "wood_name_re": r"(?i)(wood|oak|walnut|timber|plywood|birch|maple|teak|pine)",
    # paths excluded from the keycode scan (QA helpers / debug tools)
    "qa_func_re": r"(?i)(^|_)(qa|test|tests|probe|debug)(_|$)",   # funcs treated as QA helpers
    "keycode_exclude_re": r"(?i)(/tools/qa/|/qa/|_probe|_test|test_|/tests?/|debug)",
    # repo hygiene
    "junk_tracked_re": r"(?i)(^|/)(\.godot/|renders?/|qa_shots[^/]*/|screenshots?/)|\.(log|bak|orig|swp|rej|tmp|blend1|pyc)$|(^|/)(Thumbs\.db|\.DS_Store)$",
    "required_gitignore": [".godot/", "godot/renders/", "*.log", "*.bak", "*.tmp", "__pycache__/"],
}
# ============================================================================

RESULTS = []  # (status, check, message)
TEXT_EXT = (".tscn", ".tres", ".gd", ".godot", ".import", ".gdshader", ".cfg")


def rec(status, check, msg="", details=None, limit=8):
    RESULTS.append((status, check, msg))
    line = f"[{status}] {check}" + (f": {msg}" if msg else "")
    print(line)
    if details:
        for d in details[:limit]:
            print(f"        - {d}")
        if len(details) > limit:
            print(f"        ... and {len(details) - limit} more")


def name_tokens(n):
    n = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", n)
    n = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", n)
    return [t.lower() for t in re.split(r"[^A-Za-z]+|\s+", n) if t]


def is_debug_name(n):
    return any(t in CONFIG["debug_name_words"] for t in name_tokens(n))


def read_text(p):
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def find_up(start, marker):
    d = os.path.abspath(start if os.path.isdir(start) else os.path.dirname(start))
    while True:
        if os.path.exists(os.path.join(d, marker)):
            return d
        nd = os.path.dirname(d)
        if nd == d:
            return None
        d = nd


def git(root, *args):
    try:
        return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""


def rel(p, base):
    try:
        return os.path.relpath(p, base).replace(os.sep, "/")
    except ValueError:
        return p


def res_to_path(res, proj):
    return os.path.join(proj, res[len("res://"):]) if res.startswith("res://") else None


# ---------------------------------------------------------------- scope -----
def collect_scope(target, proj):
    """Return the set of files to check. A scene expands to its dependency closure."""
    files = set()
    if os.path.isdir(target):
        for dp, dns, fns in os.walk(target):
            dns[:] = [d for d in dns if d not in (".godot", ".git", "renders", "__pycache__")]
            for fn in fns:
                files.add(os.path.join(dp, fn))
        return files
    todo = [os.path.abspath(target)]
    while todo:
        f = todo.pop()
        if f in files or not os.path.exists(f):
            continue
        files.add(f)
        if f.endswith((".tscn", ".tres", ".gd")) and proj:
            for m in re.finditer(r'res://[^"\'\s)]+', read_text(f)):
                p = res_to_path(m.group(0), proj)
                if p and os.path.exists(p):
                    if p.endswith((".tscn", ".tres", ".gd")):
                        todo.append(p)
                    else:
                        files.add(p)
    return files


# --------------------------------------------------------- repo hygiene -----
def check_repo(root, strict_scope_files):
    if not root:
        rec("WARN", "repo.git", "not inside a git repo; hygiene checks skipped")
        return
    st = git(root, "status", "--porcelain")
    rec("PASS" if not st.strip() else "WARN", "repo.status_clean",
        "git status clean" if not st.strip() else f"{len(st.splitlines())} uncommitted/untracked entries",
        st.splitlines())
    tracked = [l for l in git(root, "ls-files", "-z").split("\0") if l]
    jre = re.compile(CONFIG["junk_tracked_re"])
    junk = [t for t in tracked if jre.search(t)]
    rec("FAIL" if junk else "PASS", "repo.no_tracked_junk",
        f"{len(junk)} tracked render/log/.godot/bak files" if junk else f"{len(tracked)} tracked files, no junk", junk)
    # orphan .import sidecars (source deleted)
    orphan = [t for t in tracked if t.endswith(".import") and t[:-7] not in set(tracked)]
    rec("WARN" if orphan else "PASS", "repo.orphan_import_sidecars",
        f"{len(orphan)} .import files whose source is not tracked" if orphan else "every .import has its source", orphan)
    # tracked but ignored
    ign = git(root, "ls-files", "-ci", "--exclude-standard").split("\n")
    ign = [i for i in ign if i]
    rec("FAIL" if ign else "PASS", "repo.tracked_but_ignored",
        f"{len(ign)} tracked files match .gitignore" if ign else "none", ign)
    gi = read_text(os.path.join(root, ".gitignore"))
    gi_lines = {l.strip() for l in gi.splitlines()}
    missing = [e for e in CONFIG["required_gitignore"] if e not in gi_lines]
    rec("WARN" if missing else "PASS", "repo.gitignore_entries",
        f"missing: {', '.join(missing)}" if missing else "required entries present")
    # untracked output dirs not ignored
    unt = [l[3:] for l in st.splitlines() if l.startswith("??")]
    out_like = [u for u in unt if re.search(r"(?i)(render|shot|log|cache|tmp|temp|out)", u)]
    rec("WARN" if out_like else "PASS", "repo.untracked_outputs_ignored",
        f"{len(out_like)} untracked output-like paths not in .gitignore" if out_like else "none", out_like)
    big, sizes = [], {}
    for t in tracked:
        p = os.path.join(root, t)
        try:
            s = os.path.getsize(p)
        except OSError:
            continue
        sizes[t] = s
        if s > CONFIG["oversized_file_mb"] * 1e6:
            big.append(f"{t} ({s/1e6:.1f} MB)")
    rec("WARN" if big else "PASS", "repo.oversized_files",
        f"{len(big)} files > {CONFIG['oversized_file_mb']} MB" if big else "none", big)
    # duplicates by git blob hash (no file reads needed)
    by_hash = {}
    for line in git(root, "ls-files", "-s").splitlines():
        parts = line.split(None, 3)
        if len(parts) == 4 and not parts[3].endswith((".import", ".uid")) and sizes.get(parts[3], 0) > 1024:
            by_hash.setdefault(parts[1], []).append(parts[3])
    dups = [" == ".join(v) for v in by_hash.values() if len(v) > 1]
    rec("WARN" if dups else "PASS", "repo.duplicate_files",
        f"{len(dups)} groups of identical tracked files" if dups else "none", dups)


# ------------------------------------------------------- tscn parsing -------
SECTION_RE = re.compile(r"^\[(\w+)([^\]]*)\]\s*$", re.M)
ATTR_RE = re.compile(r'(\w+)=("([^"]*)"|[^\s\]]+)')


def parse_tscn(text):
    """Yield (kind, attrs, props) for each [section]."""
    out = []
    ms = list(SECTION_RE.finditer(text))
    for i, m in enumerate(ms):
        attrs = {a.group(1): (a.group(3) if a.group(3) is not None else a.group(2)) for a in ATTR_RE.finditer(m.group(2))}
        body = text[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(text)]
        props = {}
        for line in body.splitlines():
            if " = " in line and not line.startswith((" ", "\t")):
                k, v = line.split(" = ", 1)
                props[k.strip()] = v.strip()
        out.append((m.group(1), attrs, props))
    return out


def parse_color(v):
    m = re.match(r"Color\(([^)]*)\)", v or "")
    if not m:
        return None
    try:
        c = [float(x) for x in m.group(1).split(",")]
    except ValueError:
        return None
    return (c + [1.0] * 4)[:4]


def hue(rgb):
    import colorsys
    h, s, v = colorsys.rgb_to_hsv(*rgb[:3])
    return h * 360, s, v


def hex_rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def material_checks(label, name, albedo, has_tex, transparency, emission, metallic, tex_paths, issues):
    """Shared material rules for .tscn/.tres StandardMaterial3D and GLB materials."""
    nm = name or ""
    if albedo is not None:
        r, g, b = albedo[:3]
        if not has_tex:
            if r > 0.95 and b > 0.95 and g < 0.2:
                issues["FAIL"].append(f"{label}: magenta placeholder albedo")
            elif abs(r - g) < 0.02 and abs(g - b) < 0.02 and r in (1.0,) or (abs(r - 0.8) < 0.01 and abs(g - 0.8) < 0.01 and abs(b - 0.8) < 0.01):
                issues["WARN"].append(f"{label}: default white/grey albedo with no texture")
            if max(r, g, b) > CONFIG["albedo_bright_max"]:
                issues["WARN"].append(f"{label}: albedo {max(r,g,b):.2f} > {CONFIG['albedo_bright_max']} with no texture")
        if albedo[3] < 1.0 and not transparency:
            issues["FAIL"].append(f"{label}: opaque material with alpha {albedo[3]:.2f}")
        h, s, v = hue(albedo)
        amber_h = hue(hex_rgb(CONFIG["accent_colors"][0]))[0]
        if s > 0.6 and v > 0.6 and abs(h - amber_h) < CONFIG["accent_hue_tol_deg"]:
            exact = any(all(abs(a - b) < 0.01 for a, b in zip(albedo[:3], hex_rgb(c))) for c in CONFIG["accent_colors"])
            if not exact:
                issues["WARN"].append(f"{label}: amber-ish accent {['%.3f' % x for x in albedo[:3]]} is not {CONFIG['accent_colors'][0]}")
    if emission is not None and emission > CONFIG["emission_energy_max"]:
        issues["WARN"].append(f"{label}: emission energy {emission} > {CONFIG['emission_energy_max']}")
    if CONFIG["forbid_wood_albedo"]:
        wre = re.compile(CONFIG["wood_name_re"])
        if wre.search(nm) or any(wre.search(os.path.basename(t)) for t in tex_paths):
            issues["FAIL"].append(f"{label}: wood material/albedo (art direction forbids wood)")
    if re.search(r"(?i)glass", nm) and re.search(CONFIG["glass_hardware_re"], nm):
        issues["FAIL"].append(f"{label}: hardware name contains 'glass' (runtime glass match will make it translucent)")
    if metallic is not None and metallic > 0.5 and re.search(CONFIG["nonmetal_name_re"], nm) and not re.search(CONFIG["metal_name_re"], nm):
        issues["WARN"].append(f"{label}: non-metal name with metallic {metallic:.2f}")


def check_scenes(files, proj):
    scenes = sorted(f for f in files if f.endswith((".tscn", ".tres")))
    if not scenes:
        rec("PASS", "scene.parse", "no .tscn/.tres in scope")
        return
    missing, dup_shapes, dbg, decals = [], [], [], []
    mat_issues = {"FAIL": [], "WARN": []}
    for sc in scenes:
        r = rel(sc, proj) if proj else sc
        secs = parse_tscn(read_text(sc))
        shapes_by_parent = {}
        for kind, a, p in secs:
            if kind == "ext_resource" and "path" in a:
                path = res_to_path(a["path"], proj) if proj else None
                if path and not os.path.exists(path):
                    missing.append(f"{r}: {a['path']}")
            if kind == "node":
                nm = a.get("name", "")
                if is_debug_name(nm):
                    dbg.append(f"{r}: node '{nm}'")
                if a.get("type") == "Decal":
                    decals.append(f"{r}: Decal '{nm}' (use BLEND quads on gl_compatibility)")
                if a.get("type") == "CollisionShape3D":
                    key = (a.get("parent", "."), p.get("transform", "identity"), p.get("shape", ""))
                    shapes_by_parent.setdefault(key, []).append(nm)
            if kind == "sub_resource" and a.get("type") in ("StandardMaterial3D", "ORMMaterial3D"):
                alb = parse_color(p.get("albedo_color", "Color(1, 1, 1, 1)"))
                has_tex = "albedo_texture" in p
                tr = p.get("transparency", "0") not in ("0",)
                em = float(p["emission_energy_multiplier"]) if p.get("emission_enabled") == "true" and "emission_energy_multiplier" in p else None
                met = float(p["metallic"]) if "metallic" in p else None
                name = p.get("resource_name", "").strip('"') or a.get("id", "")
                material_checks(f"{r}:{name}", name, alb, has_tex, tr, em, met, [], mat_issues)
        for (parent, xf, _), names in shapes_by_parent.items():
            if len(names) > 1:
                dup_shapes.append(f"{r}: under '{parent}': {', '.join(names)} share a transform")
    rec("FAIL" if missing else "PASS", "refs.ext_resources", f"{len(missing)} missing" if missing else f"{len(scenes)} scene/resource files resolve", missing)
    rec("FAIL" if dup_shapes else "PASS", "colliders.duplicate_shape_transforms", f"{len(dup_shapes)}" if dup_shapes else "none", dup_shapes)
    rec("WARN" if dbg else "PASS", "names.debug_nodes", f"{len(dbg)}" if dbg else "none in .tscn", dbg)
    rec("FAIL" if decals else "PASS", "compat.no_decal_nodes", f"{len(decals)}" if decals else "none in .tscn", decals)
    for s in ("FAIL", "WARN"):
        pass
    st = "FAIL" if mat_issues["FAIL"] else ("WARN" if mat_issues["WARN"] else "PASS")
    rec(st, "materials.tscn_tres", f"{len(mat_issues['FAIL'])} fail, {len(mat_issues['WARN'])} warn" if st != "PASS" else "ok",
        mat_issues["FAIL"] + mat_issues["WARN"])


# ----------------------------------------------------------- gd scripts -----
def check_scripts(files, proj):
    gds = sorted(f for f in files if f.endswith(".gd"))
    if not gds:
        rec("PASS", "gd.scripts", "no .gd in scope")
        return
    exc = re.compile(CONFIG["keycode_exclude_re"])
    key_hits, frame_hits, missing_refs, dbg_names, decal_new = [], [], [], [], []
    key_re = re.compile(r"\b(KEY_[A-Z0-9_]+|physical_keycode|keycode)\b")
    frame_re = re.compile(r"(?i)\b(frame[s_]*(count|counter|_n|_left|_wait|s_waited)?\b.*(>=|>|==|<|<=)\s*\d+|for\s+\w+\s+in\s+range\(\s*\d{2,}\s*\)\s*:\s*\n?\s*await\s+get_tree\(\)\.(process|physics)_frame|get_frames_drawn\(\)|Engine\.get_(physics|process)_frames\(\))")
    test_ctx = re.compile(r"(?i)(qa|test|probe|assert|_check|verify)")
    for g in gds:
        r = rel(g, proj) if proj else g
        txt = read_text(g)
        lines = txt.splitlines()
        live = not exc.search("/" + r)
        consts = set(re.findall(r"^\s*(?:const|var)\s+(KEY_[A-Z0-9_]+)", txt, re.M))
        func = ""
        qa_func = re.compile(CONFIG["qa_func_re"])
        for i, ln in enumerate(lines, 1):
            code = ln.split("#", 1)[0]
            fm = re.match(r"\s*(?:static\s+)?func\s+(\w+)", code)
            if fm:
                func = fm.group(1)
            hits = [h for h in key_re.findall(code) if h not in consts]
            if live and hits and not qa_func.search(func) and not re.search(r"\b(is_action|InputMap|action_)", code):
                key_hits.append(f"{r}:{i} ({func or 'top'}): {code.strip()[:90]}")
            if frame_re.search(code):
                ctx = " ".join(lines[max(0, i - 15):i + 5])
                if test_ctx.search(ctx):
                    frame_hits.append(f"{r}:{i}: {code.strip()[:100]}")
            for m in re.finditer(r'"(res://[^"]+)"', code):
                p = res_to_path(m.group(1), proj) if proj else None
                if p and "%" not in m.group(1) and "{" not in m.group(1) and not p.endswith("/") and not os.path.exists(p):
                    missing_refs.append(f"{r}:{i}: {m.group(1)}")
            m = re.search(r'\.name\s*=\s*"([^"]+)"', code)
            if m and is_debug_name(m.group(1)) and live:
                dbg_names.append(f"{r}:{i}: '{m.group(1)}'")
            if re.search(r"\bDecal\.new\(\)", code):
                decal_new.append(f"{r}:{i}")
            if re.search(r"(?i)glass", code) and re.search(r"(?i)(findn?|contains|begins_with|matchn?)\s*\(\s*\"glass\"", code):
                # name-based glass match: must exclude hardware names
                window = " ".join(lines[max(0, i - 6):i + 6])
                if i < len(lines) and lines[i].strip() == "continue":
                    continue
                if not re.search(CONFIG["glass_hardware_re"], window):
                    dbg_names.append(f"{r}:{i}: name-based 'glass' match without a hardware exclusion")
    rec("FAIL" if key_hits else "PASS", "input.no_hardcoded_keys",
        f"{len(key_hits)} KEY_*/keycode uses outside the InputMap in live code" if key_hits else f"{len(gds)} scripts clean", key_hits)
    rec("WARN" if frame_hits else "PASS", "tests.no_frame_count_timing",
        f"{len(frame_hits)} frame-count timings in test/QA code (use elapsed time)" if frame_hits else "none", frame_hits)
    rec("WARN" if missing_refs else "PASS", "refs.gd_res_paths", f"{len(missing_refs)} res:// literals not on disk (FAIL if not guarded by ResourceLoader.exists)" if missing_refs else "all literal res:// paths resolve", missing_refs)
    rec("WARN" if dbg_names else "PASS", "names.debug_or_glass_match_in_gd", f"{len(dbg_names)}" if dbg_names else "none", dbg_names)
    rec("FAIL" if decal_new else "PASS", "compat.no_decal_new", f"{len(decal_new)} Decal.new() calls" if decal_new else "none", decal_new)


def check_project(proj):
    if not proj:
        rec("WARN", "project.godot", "no project.godot found above target")
        return
    pg = read_text(os.path.join(proj, "project.godot"))
    rm = re.search(r'renderer/rendering_method="?([\w.]+)', pg)
    rec("PASS" if rm and "compat" in rm.group(1) else "WARN", "compat.renderer",
        f"rendering_method={rm.group(1) if rm else 'default(forward_plus)'}")
    # double-bound keys
    binds = {}
    sec = re.search(r"\[input\](.*?)(\n\[|\Z)", pg, re.S)
    if sec:
        for m in re.finditer(r'^(\w+)=\{(.*?)^\}', sec.group(1), re.S | re.M):
            for k in set(re.findall(r'"physical_keycode":(\d+)', m.group(2))) | set(re.findall(r'"keycode":(\d+)', m.group(2))):
                if k != "0":
                    binds.setdefault(k, set()).add(m.group(1))
    dbl = [f"keycode {k}: {', '.join(sorted(v))}" for k, v in binds.items() if len(v) > 1]
    rec("WARN" if dbl else "PASS", "input.double_bindings", f"{len(dbl)} keys bound to several actions (design check)" if dbl else f"{len(binds)} keys, none doubled", dbl)
    # compat-dead env features in scenes
    dead = []
    for dp, dns, fns in os.walk(proj):
        dns[:] = [d for d in dns if d not in (".godot", "renders")]
        for fn in fns:
            if fn.endswith((".tscn", ".tres")):
                t = read_text(os.path.join(dp, fn))
                for feat in ("ssao_enabled = true", "ssr_enabled = true", "sdfgi_enabled = true", "ssil_enabled = true", "volumetric_fog_enabled = true"):
                    if feat in t:
                        dead.append(f"{rel(os.path.join(dp, fn), proj)}: {feat}")
    if rm and "compat" in rm.group(1):
        rec("WARN" if dead else "PASS", "compat.dead_env_settings", f"{len(dead)} settings ignored by gl_compatibility" if dead else "none", dead)


# ---------------------------------------------------------- textures --------
def image_size(p):
    try:
        with open(p, "rb") as f:
            head = f.read(32)
            if head[:8] == b"\x89PNG\r\n\x1a\n":
                return struct.unpack(">II", head[16:24])
            if head[:2] == b"\xff\xd8":
                f.seek(2)
                while True:
                    b = f.read(1)
                    while b and b != b"\xff":
                        b = f.read(1)
                    while b == b"\xff":
                        b = f.read(1)
                    if not b:
                        return None
                    if b[0] in (0xC0, 0xC1, 0xC2):
                        f.read(3)
                        h, w = struct.unpack(">HH", f.read(4))
                        return w, h
                    ln = struct.unpack(">H", f.read(2))[0]
                    f.seek(ln - 2, 1)
            if head[:4] == b"RIFF" and head[8:12] == b"WEBP" and head[12:16] == b"VP8X":
                w = int.from_bytes(head[24:27], "little") + 1
                h = int.from_bytes(head[27:30], "little") + 1
                return w, h
    except Exception:
        return None
    return None


def check_textures(files, proj):
    imgs = sorted(f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")))
    if not imgs:
        rec("PASS", "textures", "no textures in scope")
        return
    npot, huge, uncomp, unused, mism = [], [], [], [], []
    mx = CONFIG["texture_max_px"]
    sizes = {}
    # reference corpus for "unused": every text file + glb json in the project
    corpus = []
    if proj:
        for dp, dns, fns in os.walk(proj):
            dns[:] = [d for d in dns if d not in (".godot", "renders")]
            for fn in fns:
                if fn.endswith((".tscn", ".tres", ".gd", ".gdshader", ".json", ".py")):
                    corpus.append(read_text(os.path.join(dp, fn)))
                elif fn.endswith(".gltf"):
                    corpus.append(read_text(os.path.join(dp, fn)))
    corpus = "\n".join(corpus)
    for im in imgs:
        r = rel(im, proj) if proj else im
        sz = image_size(im)
        if sz:
            sizes[im] = sz
            w, h = sz
            if w & (w - 1) or h & (h - 1):
                npot.append(f"{r} {w}x{h}")
            if max(w, h) > mx:
                huge.append(f"{r} {w}x{h}")
        imp = read_text(im + ".import")
        if imp and re.search(r"^compress/mode=0", imp, re.M) and "/ui/" not in r and "icon" not in r:
            uncomp.append(r)
        base = os.path.basename(im)
        stem = os.path.splitext(base)[0]
        if corpus and base not in corpus and stem not in corpus and not re.search(r"(?i)icon", base):
            unused.append(r)
    # ORM vs albedo size
    for im, sz in sizes.items():
        m = re.search(r"(?i)(.*?)(_orm|_arm)(\.\w+)$", im)
        if m:
            for suf in ("_albedo", "_basecolor", "_color", "_diffuse", "_alb", ""):
                for ext in (".png", ".jpg", ".jpeg", ".webp"):
                    cand = m.group(1) + suf + ext
                    if cand in sizes and sizes[cand] != sz:
                        mism.append(f"{rel(im, proj)} {sz} vs {rel(cand, proj)} {sizes[cand]}")
    rec("WARN" if npot else "PASS", "textures.power_of_two", f"{len(npot)} of {len(imgs)} not power-of-two" if npot else f"{len(imgs)} ok", npot)
    rec("FAIL" if huge else "PASS", "textures.max_size", f"{len(huge)} > {mx}px" if huge else f"all <= {mx}px", huge)
    rec("WARN" if mism else "PASS", "textures.orm_albedo_size", f"{len(mism)} mismatches" if mism else "ok", mism)
    rec("WARN" if uncomp else "PASS", "textures.vram_compressed", f"{len(uncomp)} lossless (compress/mode=0)" if uncomp else "ok", uncomp)
    rec("WARN" if unused else "PASS", "textures.unused", f"{len(unused)} not referenced by name anywhere (may be GLB-embedded or code-built paths)" if unused else "all referenced", unused)


# --------------------------------------------------------------- GLB --------
def glb_json(p):
    try:
        with open(p, "rb") as f:
            hdr = f.read(12)
            if hdr[:4] != b"glTF":
                return None
            ln, typ = struct.unpack("<II", f.read(8))
            if typ != 0x4E4F534A:
                return None
            return json.loads(f.read(ln).decode("utf-8", "replace"))
    except Exception:
        return None


def check_glbs(files, proj):
    glbs = sorted(f for f in files if f.lower().endswith((".glb", ".gltf")))
    if not glbs:
        rec("PASS", "glb.materials", "no GLB/glTF in scope")
        return
    issues = {"FAIL": [], "WARN": []}
    dbg, tris, nouv, bad = [], [], [], []
    for g in glbs:
        r = rel(g, proj) if proj else g
        j = glb_json(g) if g.endswith(".glb") else (json.loads(read_text(g) or "null") if True else None)
        if not j:
            bad.append(r)
            continue
        imgs = j.get("images", [])
        texs = j.get("textures", [])

        def tex_name(ti):
            try:
                im = imgs[texs[ti["index"]]["source"]]
                return im.get("uri") or im.get("name") or ""
            except Exception:
                return ""
        for m in j.get("materials", []):
            nm = m.get("name", "")
            pbr = m.get("pbrMetallicRoughness", {})
            bc = pbr.get("baseColorFactor", [1, 1, 1, 1])
            bct = pbr.get("baseColorTexture")
            tps = [tex_name(bct)] if bct else []
            em = None
            ext = m.get("extensions", {}).get("KHR_materials_emissive_strength")
            if ext:
                em = ext.get("emissiveStrength")
            tr = m.get("alphaMode", "OPAQUE") != "OPAQUE"
            met = pbr.get("metallicFactor", 1.0)
            material_checks(f"{r}:{nm}", nm, bc, bool(bct), tr, em, met, tps, issues)
            if is_debug_name(nm):
                dbg.append(f"{r}: material '{nm}'")
        for n in j.get("nodes", []):
            nm = n.get("name", "")
            if is_debug_name(nm):
                dbg.append(f"{r}: node '{nm}'")
            if re.search(r"(?i)glass", nm) and re.search(CONFIG["glass_hardware_re"], nm):
                issues["FAIL"].append(f"{r}: node '{nm}' is hardware named 'glass'")
        acc = j.get("accessors", [])
        total = 0
        for mesh in j.get("meshes", []):
            mn = mesh.get("name", "")
            for prim in mesh.get("primitives", []):
                if prim.get("mode", 4) != 4:
                    continue
                try:
                    cnt = acc[prim["indices"]]["count"] if "indices" in prim else acc[prim["attributes"]["POSITION"]]["count"]
                except Exception:
                    cnt = 0
                if not re.search(r"(?i)(-col|colonly|_col\b|convcolonly)", mn):
                    total += cnt // 3
                    if "material" in prim and "TEXCOORD_0" not in prim.get("attributes", {}):
                        mat = j.get("materials", [{}])[prim["material"]] if prim["material"] < len(j.get("materials", [])) else {}
                        if mat.get("pbrMetallicRoughness", {}).get("baseColorTexture"):
                            nouv.append(f"{r}: mesh '{mn}' textured but no UVs")
        if total > CONFIG["prop_tri_max"] and not re.search(r"(?i)(shell|hull|sector|building|exterior|cylinder|terrain)", r):
            tris.append(f"{r}: {total} tris")
    st = "FAIL" if issues["FAIL"] else ("WARN" if issues["WARN"] else "PASS")
    rec(st, "glb.materials", f"{len(glbs)} files; {len(issues['FAIL'])} fail, {len(issues['WARN'])} warn", issues["FAIL"] + issues["WARN"])
    rec("WARN" if dbg else "PASS", "glb.debug_names", f"{len(dbg)}" if dbg else "none", dbg)
    rec("WARN" if tris else "PASS", "glb.prop_triangles", f"{len(tris)} props > {CONFIG['prop_tri_max']} tris (static estimate)" if tris else "ok", tris)
    rec("WARN" if nouv else "PASS", "glb.textured_without_uv", f"{len(nouv)}" if nouv else "ok", nouv)
    if bad:
        rec("WARN", "glb.parse", f"{len(bad)} could not be parsed (LFS pointer or corrupt?)", bad)


# ------------------------------------------------------ Godot probe ---------
PROBE_GD = r'''
extends SceneTree
# Read-only probe written by tools/first_pass_check.py; lives in a temp dir.
var C = {}
func _init():
	var args = OS.get_cmdline_user_args()
	C = JSON.parse_string(FileAccess.get_file_as_string(args[1]))
	var ps = load(args[0])
	if ps == null:
		print("FPC|FAIL|godot.load|cannot load " + args[0]); quit(1); return
	var root = ps.instantiate()
	get_root().add_child(root)
	await process_frame
	await physics_frame
	await physics_frame
	var bodies = []; var meshes = []
	_walk(root, bodies, meshes)
	_check_trimesh(bodies)
	_check_dup_colliders(bodies)
	_check_slopes(bodies)
	_check_meshes(meshes)
	print("FPC|DONE|%d|%d" % [bodies.size(), meshes.size()])
	quit(0)
func _walk(n, bodies, meshes):
	if n is StaticBody3D: bodies.append(n)
	if n is MeshInstance3D: meshes.append(n)
	for c in n.get_children(): _walk(c, bodies, meshes)
func _emit(st, name, msg): print("FPC|%s|%s|%s" % [st, name, msg])
func _check_trimesh(bodies):
	var bad = 0; var ex = []
	for b in bodies:
		for c in b.get_children():
			if c is CollisionShape3D and c.shape is ConcavePolygonShape3D and not c.shape.backface_collision:
				bad += 1
				if ex.size() < 5: ex.append(str(b.get_path()))
	_emit("WARN" if bad else "PASS", "godot.trimesh_two_sided", "%d one-sided trimesh colliders %s" % [bad, ex])
func _check_dup_colliders(bodies):
	var seen = {}; var dup = 0; var ex = []
	for b in bodies:
		for c in b.get_children():
			if c is CollisionShape3D and c.shape and not c.disabled:
				var t = c.global_transform
				var k = "%s|%.3f,%.3f,%.3f|%s" % [c.shape.get_class(), t.origin.x, t.origin.y, t.origin.z, str(c.shape.get("size") if c.shape.get("size") != null else "")]
				if seen.has(k):
					dup += 1
					if ex.size() < 5: ex.append(str(c.get_path()) + " == " + seen[k])
				else: seen[k] = str(c.get_path())
	_emit("FAIL" if dup else "PASS", "godot.duplicate_static_colliders", "%d duplicates %s" % [dup, ex])
func _check_slopes(bodies):
	var steep = 0; var stair = 0; var ex = []
	var wmax = cos(deg_to_rad(C.walkable_max_deg)); var smax = deg_to_rad(C.stair_collider_max_deg)
	for b in bodies:
		var is_stair = str(b.name).to_lower().contains("stair") or str(b.get_parent().name).to_lower().contains("stair")
		for c in b.get_children():
			if not (c is CollisionShape3D) or c.shape == null: continue
			var faces = PackedVector3Array()
			if c.shape is ConcavePolygonShape3D: faces = c.shape.get_faces()
			elif c.shape is BoxShape3D: 
				var up = (c.global_transform.basis.y).normalized()
				var ang = acos(clamp(up.dot(Vector3.UP), -1, 1))
				if ang > deg_to_rad(1) and ang < deg_to_rad(80):
					if is_stair and ang > smax:
						stair += 1
					elif ang > acos(wmax):
						steep += 1
					if ang > smax and ex.size() < 5:
						ex.append("%s %.1fdeg" % [c.get_path(), rad_to_deg(ang)])
				continue
			var xf = c.global_transform
			for i in range(0, faces.size(), 3):
				var n = (xf * faces[i+1] - xf * faces[i]).cross(xf * faces[i+2] - xf * faces[i])
				if n.length() < 1e-6: continue
				n = n.normalized(); if n.y < 0: continue
				var ang = acos(clamp(n.y, -1, 1))
				# a sloped face between walkable and wall: 'sliding' range
				if is_stair and ang > smax and ang < deg_to_rad(70):
					stair += 1
					if ex.size() < 5: ex.append("%s %.1fdeg" % [c.get_path(), rad_to_deg(ang)])
				elif ang > acos(wmax) and ang < deg_to_rad(70):
					steep += 1
					if ex.size() < 5: ex.append("%s %.1fdeg" % [c.get_path(), rad_to_deg(ang)])
	_emit("WARN" if steep else "PASS", "godot.walkable_slope", "%d collider faces/boxes between %.0f and 70 deg" % [steep, C.walkable_max_deg])
	_emit("FAIL" if stair else "PASS", "godot.stair_slope", "%d stair collider faces/boxes steeper than %.0f deg %s" % [stair, C.stair_collider_max_deg, ex])
func _check_meshes(meshes):
	var noup = 0; var nomat = 0; var heavy = 0; var ex = []
	for m in meshes:
		if m.mesh == null or not m.is_visible_in_tree(): continue
		var tris = 0
		for s in m.mesh.get_surface_count():
			var mat = m.get_active_material(s)
			if mat == null:
				nomat += 1
				if ex.size() < 5: ex.append(str(m.get_path()))
			var arr = m.mesh.surface_get_arrays(s) if m.mesh is ArrayMesh else []
			if arr.size() > 0:
				if arr[Mesh.ARRAY_TEX_UV] == null and mat is BaseMaterial3D and mat.albedo_texture != null: noup += 1
				var idx = arr[Mesh.ARRAY_INDEX]
				tris += (idx.size() if idx != null else arr[Mesh.ARRAY_VERTEX].size()) / 3
		if tris > C.prop_tri_max and not str(m.get_path()).to_lower().contains("shell"): heavy += 1
	_emit("WARN" if nomat else "PASS", "godot.surfaces_have_material", "%d surfaces with no material %s" % [nomat, ex])
	_emit("WARN" if noup else "PASS", "godot.textured_without_uv", "%d" % noup)
	_emit("WARN" if heavy else "PASS", "godot.prop_triangles", "%d mesh instances > %d tris" % [heavy, C.prop_tri_max])
'''

GODOT_STUBS = [
    ("godot.floor_contact", "down-ray floor contact at +/-{floor_contact_tol_m} m"),
    ("godot.subpart_overlap", "assembled sub-part overlap <= {subpart_overlap_max_m} m"),
    ("godot.portal_intrusion", "colliders into door/portal openings <= {portal_intrusion_max_m} m (doors opened first)"),
    ("godot.capsule_escape", "capsule r {capsule_radius_m} h {capsule_height_m} escape grid"),
    ("godot.wall_gaps", "wall-mounted <= {wall_mount_gap_max_m} m, prop backs {prop_back_gap_min_m}-{prop_back_gap_max_m} m"),
    ("godot.ramp_ratio", "accessible ramps <= 1:12"),
    ("godot.draw_calls", "draw calls at fixed poses (needs a windowed run: use --qa-drawcalls)"),
]


def find_godot():
    for c in CONFIG["godot_bin_candidates"]:
        p = shutil.which(c)
        if p:
            return p
    return os.environ.get("GODOT_BIN") if os.environ.get("GODOT_BIN") and os.path.exists(os.environ["GODOT_BIN"]) else None


def run_godot(target, proj, no_godot):
    stub_msg = lambda: [rec("WARN", n, "not implemented (stub): " + d.format(**CONFIG)) for n, d in GODOT_STUBS]
    if no_godot:
        rec("WARN", "godot.probe", "skipped (--no-godot): collider slopes, duplicates, trimesh sides, mesh budgets not checked")
        stub_msg()
        return
    gb = find_godot()
    if not gb or not proj or not target.endswith(".tscn"):
        why = "no godot binary on PATH (set GODOT_BIN)" if not gb else "target is not a single .tscn"
        rec("WARN", "godot.probe", f"skipped: {why}")
        stub_msg()
        return
    if not os.path.isdir(os.path.join(proj, ".godot", "imported")):
        # Running Godot on an unimported project would trigger an import (writes .godot/); stay read-only.
        rec("WARN", "godot.probe", "skipped: project not imported yet (open it in the editor or run godot --headless --import once)")
        stub_msg()
        return
    tmp = tempfile.mkdtemp(prefix="fpc_probe_")
    try:
        probe = os.path.join(tmp, "fpc_probe.gd")
        cfg = os.path.join(tmp, "cfg.json")
        with open(probe, "w") as f:
            f.write(PROBE_GD)
        with open(cfg, "w") as f:
            json.dump(CONFIG, f)
        res = "res://" + rel(target, proj)
        try:
            p = subprocess.run([gb, "--headless", "--path", proj, "-s", probe, "--", res, cfg],
                               capture_output=True, text=True, timeout=CONFIG["godot_timeout_s"])
            out = p.stdout + p.stderr
        except subprocess.TimeoutExpired as e:
            out = (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
            rec("WARN", "godot.probe", f"timed out after {CONFIG['godot_timeout_s']} s")
        got = False
        for ln in out.splitlines():
            if ln.startswith("FPC|"):
                parts = ln.split("|", 3)
                if parts[1] == "DONE":
                    parts = ln.split("|")
                    rec("PASS", "godot.probe", f"ran on {res}: {parts[2]} static bodies, {parts[3]} meshes")
                    got = True
                elif len(parts) == 4:
                    rec(parts[1], parts[2], parts[3])
        if not got:
            errs = [l for l in out.splitlines() if "ERROR" in l or "error" in l][:5]
            rec("WARN", "godot.probe", "probe did not finish", errs)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    stub_msg()


# --------------------------------------------------------------- main -------
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("target", help=".tscn scene, file, or directory")
    ap.add_argument("--no-godot", action="store_true", help="static checks only")
    ap.add_argument("--strict", action="store_true", help="WARN counts as FAIL")
    a = ap.parse_args()
    target = os.path.abspath(a.target)
    if not os.path.exists(target):
        print(f"error: {a.target} does not exist", file=sys.stderr)
        return 2
    proj = find_up(target, "project.godot")
    if not proj and os.path.isdir(target) and os.path.exists(os.path.join(target, "godot", "project.godot")):
        proj = os.path.join(target, "godot")
    root = find_up(target, ".git")
    print(f"first_pass_check: target={a.target} project={proj} repo={root}")
    files = collect_scope(target, proj)
    print(f"scope: {len(files)} files\n")
    for fn in (lambda: check_repo(root, files), lambda: check_project(proj), lambda: check_scenes(files, proj),
               lambda: check_scripts(files, proj), lambda: check_textures(files, proj), lambda: check_glbs(files, proj),
               lambda: run_godot(target, proj, a.no_godot)):
        try:
            fn()
        except Exception as e:  # a crashing check must not hide the others
            rec("FAIL", "checker.internal", f"{type(e).__name__}: {e}")
    n = {s: sum(1 for r in RESULTS if r[0] == s) for s in ("PASS", "WARN", "FAIL")}
    print(f"\nSUMMARY: {n['PASS']} PASS, {n['WARN']} WARN, {n['FAIL']} FAIL" + (" (strict)" if a.strict else ""))
    print("Manual items (not automatable): see docs/FIRST_PASS_CHECKLIST.md 'How to run the checker'")
    return 1 if n["FAIL"] or (a.strict and n["WARN"]) else 0


if __name__ == "__main__":
    sys.exit(main())
