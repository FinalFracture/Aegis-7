#!/usr/bin/env python3
"""
Generates the Mid-Key Balanced & Forensic Environmental Storytelling PBR Texture Suite (1024x1024)
for the Preface 2-Story Residential Sector (`preface_playable_area.tscn` / `preface_residential_sector.glb`)
per Jared's [t4u] & [t6u] directives:
  1. Readable Mid-Tone Architectural Base Surfaces (Clean World-Space Tiling, ZERO Repeating Text/Clutter):
     - `UV_WALL_APT` (`u:0.02..0.48, v:0.02..0.25`): Warm titanium-putty / light slate grey (`RGB ~ 142, 148, 156` / `#8E949C`)
       with subtle panel seams, lower kickplate scuffing, and micro-grain.
     - `UV_WALL_ATRIUM` (`u:0.52..0.98, v:0.02..0.24`): Mid-tone slate-putty bulkhead panels (`RGB ~ 136, 142, 150` / `#888E96`)
       with clean expansion joints and subtle condensation streaks near the base.
     - `UV_FLOOR_SLATE` (`u:0.52..0.98, v:0.26..0.48`): Mid-tone slate terrazzo / composite decking (`RGB ~ 98, 104, 112` / `#626870`)
       with warm aggregate, clean expansion joints, and foot-traffic polishing down the center (`roughness ~0.32`)
       vs. dustier matte oxidation along the edges (`roughness ~0.78`).
     - `UV_WOOD_WALNUT` (`u:0.02..0.23, v:0.28..0.48`): Warm natural honey-teak / weathered birch-walnut wood grain (`RGB ~ 138, 106, 78` / `#8A6A4E`).
     - `UV_FABRIC_SLATE` (`u:0.26..0.48, v:0.28..0.48`): Mid-tone woven slate upholstery (`RGB ~ 86, 98, 112` / `#566270`).
     - `UV_STEEL_TRIM` (`u:0.02..0.48, v:0.52..0.70`): Brushed structural dark steel (`RGB ~ 84, 92, 102` / `#545C66`).
  2. Cohesive Forensic Conspiracy Trail ("The 03:14 UTC Sub-Bus Load Spike & Unit #0204 Re-Designation")
     baked strictly into non-tiled, dedicated UV regions:
     - Clue 1A (`UV_WORKBENCH_TOP = (0.76, 0.99, 0.51, 0.64)`): Rostov's workbench top with wear-polished forearm rest,
       plasma-arc & solder-flux scorch mark from the blown 3rd neural capacitor coil (`COIL C3`), coffee mug ring,
       scratched serial `A7-0204-MEM` + tally marks `III`, and taped oscilloscope calibration note showing the
       `03:14 UTC` 13.56 MHz / 412 Hz spike on `BUS B-14` & `UNIT #0204: PUDDLE -> KELVIN`.
     - Clue 1B (`UV_WORKBENCH_PEGBOARD = (0.52, 0.75, 0.64, 0.75)`): Workbench tool pegboard with rectangular ghost mark
       where an older D-03 frame hung + pinned schematic (`13.56 MHz RFID TAP // PIN_RESET -> B-14`).
     - Clue 2 (`UV_FLOOR_SKID_TRAIL = (0.76, 0.99, 0.64, 0.75)`): Asymmetric single-locked-tread rubber skid mark +
       glossy violet/cyan cryo-coolant drip trail (`roughness ~0.18`) + `BUS B-14 // HATCH 04` stencil leading into Room 1B.
     - Clue 3 (`UV_PLACARD_201..1B`):
       * `APT 201`: Pried-bezel screwdriver nicks on the left edge + scratched-out `CLR-4 [REVOKED] -> TECH-2`.
       * `RM 1B`: Ghost stenciling bleeding through underneath as `SEC-04 // TELEMETRY RELAY [RESTRICTED]` + broken
         security seal stamped `2026-10-19 // 03:14`.
"""
import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TEX_DIRS = [
    "/workspace/game-project/assets/textures",
    "/workspace/game-project/assets/textures/preface",
    "/workspace/game-project/assets/textures/residential",
    "/workspace/game-project/godot/assets/textures",
    "/workspace/game-project/godot/assets/textures/preface",
    "/workspace/game-project/godot/assets/textures/residential",
]
for d in TEX_DIRS:
    os.makedirs(d, exist_ok=True)


def hex_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def load_font(size: int, bold: bool = True):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def add_ultra_clean_micro_grain(arr: np.ndarray, sigma: float = 0.55, seed: int = 42) -> np.ndarray:
    """Adds subtle <0.25% micro-grain so flat patches have natural tactile variation well under the 1.0% threshold."""
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, sigma, size=arr.shape)
    return np.clip(np.round(arr.astype(np.float32) + noise), 0, 255).astype(np.uint8)


def compute_micro_noise_pct(arr: np.ndarray) -> float:
    """Computes high-frequency micro-noise percentage relative to 3x3 smoothed baseline."""
    im = Image.fromarray(arr)
    blur = np.asarray(im.filter(ImageFilter.BoxBlur(1)), dtype=np.float32)
    diff = np.abs(arr.astype(np.float32) - blur)
    return float(np.mean(diff) / 255.0 * 100.0)


def generate_residential_atlas():
    W, H = 1024, 1024
    alb = np.zeros((H, W, 3), dtype=np.uint8)
    orm = np.zeros((H, W, 3), dtype=np.uint8)  # R=AO, G=Roughness, B=Metallic
    emi = np.zeros((H, W, 3), dtype=np.uint8)  # 95%+ pitch black #000000
    hgt = np.full((H, W), 128.0, dtype=np.float32)

    # --------------------------------------------------------------------------
    # 1. Q1 (`x: 0..511, y: 0..511`):
    #    - Upper (`y: 0..276`): Warm Titanium-Putty / Light Slate Grey Apartment Walls (`RGB 142, 148, 156` / `#8E949C`)
    #    - Lower-Left (`x: 0..255, y: 276..511`): Warm Honey-Teak / Weathered Birch Wood (`RGB 138, 106, 78` / `#8A6A4E`)
    #    - Lower-Right (`x: 256..511, y: 276..511`): Mid-Tone Slate Upholstery (`RGB 86, 98, 112` / `#566270`)
    # --------------------------------------------------------------------------
    alb[0:276, 0:512] = (142, 148, 156)
    orm[0:276, 0:512] = (246, int(0.54 * 255), int(0.08 * 255))
    # Subtle warm gradient & lower kickplate scuff band (y: 244..276)
    for y in range(0, 276):
        grad = int(round((1.0 - y / 276.0) * 6.0 - 2.0))
        alb[y, 0:512] = np.clip(alb[y, 0:512].astype(np.int32) + grad, 0, 255)
    alb[246:276, 0:512] = (118, 124, 132)
    orm[246:276, 0:512, 0] = 228
    orm[246:276, 0:512, 1] = int(0.64 * 255)
    # Clean architectural panel joints (zero repeating text!)
    for py in [68, 138, 208, 246]:
        alb[py : py + 3, 0:512] = (116, 122, 130)
        orm[py : py + 3, 0:512, 0] = 214
        hgt[py : py + 3, 0:512] = 112.0
    for px in [128, 256, 384]:
        alb[0:276, px : px + 3] = (116, 122, 130)
        orm[0:276, px : px + 3, 0] = 214
        hgt[0:276, px : px + 3] = 112.0

    # Q1 Lower-Left: Warm Natural Honey-Teak / Weathered Birch Wood (`RGB 138, 106, 78` / `#8A6A4E`)
    alb[276:512, 0:256] = (138, 106, 78)
    orm[276:512, 0:256] = (244, int(0.46 * 255), int(0.04 * 255))
    for wy in range(276, 512):
        wave = int(round(7.0 * math.sin(wy * 0.22) + 4.0 * math.cos(wy * 0.09)))
        alb[wy, 0:256] = np.clip(np.array([138 + wave, 106 + int(wave * 0.8), 78 + int(wave * 0.6)]), 0, 255)
        hgt[wy, 0:256] = 128.0 + 2.5 * math.sin(wy * 0.22)
    for plank_y in [324, 372, 420, 468]:
        alb[plank_y : plank_y + 2, 0:256] = (108, 80, 56)
        orm[plank_y : plank_y + 2, 0:256, 0] = 218
        hgt[plank_y : plank_y + 2, 0:256] = 116.0

    # Q1 Lower-Right: Mid-Tone Slate Upholstery (`RGB 86, 98, 112` / `#566270`)
    alb[276:512, 256:512] = (86, 98, 112)
    orm[276:512, 256:512] = (242, int(0.72 * 255), int(0.02 * 255))
    for sy in range(304, 504, 44):
        alb[sy : sy + 3, 256:512] = (68, 78, 90)
        orm[sy : sy + 3, 256:512, 0] = 212
        hgt[sy : sy + 3, 256:512] = 114.0
    for sx in range(304, 504, 56):
        alb[276:512, sx : sx + 3] = (68, 78, 90)
        hgt[276:512, sx : sx + 3] = 114.0

    # --------------------------------------------------------------------------
    # 2. Q2 (`x: 512..1023, y: 0..511`):
    #    - Upper (`y: 0..260`): Readable Mid-Tone Slate-Putty Corridor Bulkheads (`RGB 136, 142, 150` / `#888E96`)
    #    - Lower (`y: 260..511`): Mid-Tone Slate Terrazzo / Composite Floor Deck (`RGB 98, 104, 112` / `#626870`)
    #      with Foot-Traffic Polishing down the center (`roughness ~0.32`) vs. Dustier Matte Edges (`roughness ~0.78`)!
    # --------------------------------------------------------------------------
    alb[0:260, 512:1024] = (136, 142, 150)
    orm[0:260, 512:1024] = (245, int(0.54 * 255), int(0.08 * 255))
    # Subtle lower bulkhead datum band & mineral condensation shading near bottom (y: 216..260)
    alb[216:222, 512:1024] = (112, 118, 126)
    alb[222:260, 512:1024] = (122, 128, 136)
    orm[222:260, 512:1024, 1] = int(0.66 * 255)
    for py in [64, 130, 196, 220]:
        alb[py : py + 3, 512:1024] = (108, 114, 122)
        orm[py : py + 3, 512:1024, 0] = 212
        hgt[py : py + 3, 512:1024] = 112.0
    for px in [640, 768, 896]:
        alb[0:260, px : px + 3] = (108, 114, 122)
        orm[0:260, px : px + 3, 0] = 212
        hgt[0:260, px : px + 3] = 112.0

    # Q2 Lower: Mid-Tone Slate Terrazzo / Composite Floor (`y: 260..512, x: 512..1024`)
    alb[260:512, 512:1024] = (98, 104, 112)
    orm[260:512, 512:1024] = (242, int(0.58 * 255), int(0.12 * 255))
    # Foot-traffic polishing down center vs. dusty matte oxidation near edges (ORM roughness contrast!)
    yy, xx = np.mgrid[260:512, 512:1024]
    cy_f, cx_f = 386.0, 768.0
    dist_norm = np.sqrt(((yy - cy_f) / 126.0) ** 2 + ((xx - cx_f) / 256.0) ** 2)
    wear_mask = np.clip(1.0 - dist_norm * 0.85, 0.0, 1.0)
    # Center traffic zone is slightly brighter/polished (roughness ~0.32), edges are dustier (roughness ~0.78)
    rough_map = (0.78 - wear_mask * 0.46) * 255.0
    orm[260:512, 512:1024, 1] = np.clip(rough_map, 76, 204).astype(np.uint8)
    orm[260:512, 512:1024, 0] = np.clip(226.0 + wear_mask * 22.0, 215, 250).astype(np.uint8)
    for c_idx, base_v in enumerate([98, 104, 112]):
        alb[260:512, 512:1024, c_idx] = np.clip(base_v - 6.0 + wear_mask * 12.0, 0, 255).astype(np.uint8)
    # Subtle terrazzo aggregate flecks (deterministic smooth clusters)
    rng_agg = np.random.default_rng(77)
    for _ in range(180):
        ax = int(rng_agg.integers(518, 1018))
        ay = int(rng_agg.integers(266, 506))
        delta_c = int(rng_agg.choice([-10, -7, 8, 11]))
        alb[ay : ay + 3, ax : ax + 3] = np.clip(alb[ay : ay + 3, ax : ax + 3].astype(np.int32) + delta_c, 0, 255)
    # Clean terrazzo expansion joints
    for fy in [322, 386, 450]:
        alb[fy : fy + 3, 512:1024] = (74, 80, 88)
        orm[fy : fy + 3, 512:1024, 0] = 205
        orm[fy : fy + 3, 512:1024, 1] = int(0.82 * 255)
        hgt[fy : fy + 3, 512:1024] = 112.0
    for fx in [640, 768, 896]:
        alb[260:512, fx : fx + 3] = (74, 80, 88)
        orm[260:512, fx : fx + 3, 0] = 205
        orm[260:512, fx : fx + 3, 1] = int(0.82 * 255)
        hgt[260:512, fx : fx + 3] = 112.0

    # --------------------------------------------------------------------------
    # 3. Q3 (`x: 0..511, y: 512..1023`):
    #    - Upper (`y: 512..740`): Brushed Structural Steel & Trim (`RGB 84, 92, 102` / `#545C66`, rough 0.38, met 0.78)
    #    - Lower-Left (`x: 0..255, y: 740..1023`): Coiled Copper/Slate Wire Spool (`#4A525C` / `#9E6E44`)
    #    - Lower-Right (`x: 256..511, y: 740..1023`): Matte Slate Battery Cell Housing (`#38404A` / `#2E8B9A`)
    # --------------------------------------------------------------------------
    alb[512:740, 0:512] = (84, 92, 102)
    orm[512:740, 0:512] = (244, int(0.38 * 255), int(0.78 * 255))
    for sy in [568, 626, 684]:
        alb[sy : sy + 3, 0:512] = (64, 70, 78)
        orm[sy : sy + 3, 0:512, 0] = 212
        hgt[sy : sy + 3, 0:512] = 114.0
    for sx in [128, 256, 384]:
        alb[512:740, sx : sx + 3] = (102, 110, 122)
        hgt[512:740, sx : sx + 3] = 138.0

    # Q3 Lower-Left: Coiled Copper/Slate Wire Spool (`x: 0..255, y: 740..1024`)
    alb[740:1024, 0:256] = (66, 74, 84)
    orm[740:1024, 0:256] = (240, int(0.40 * 255), int(0.72 * 255))
    for cy in range(772, 980, 18):
        alb[cy : cy + 10, 28:228] = (158, 110, 68)
        orm[cy : cy + 10, 28:228] = (244, int(0.28 * 255), int(0.86 * 255))
        hgt[cy : cy + 10, 28:228] = 140.0

    # Q3 Lower-Right: Matte Slate Battery Cell (`x: 256..511, y: 740..1024`)
    alb[740:1024, 256:512] = (58, 66, 76)
    orm[740:1024, 256:512] = (242, int(0.44 * 255), int(0.65 * 255))
    alb[760:796, 280:488] = (88, 98, 110)
    for by in [824, 864, 904]:
        alb[by : by + 16, 324:444] = hex_rgb("#2E8B9A")
        orm[by : by + 16, 324:444] = (252, int(0.22 * 255), int(0.15 * 255))
        emi[by : by + 16, 324:444] = hex_rgb("#1E5C66")

    # --------------------------------------------------------------------------
    # 4. Q4 (`x: 512..1023, y: 512..1023`) — PLANTER STONE, FUNCTIONAL LIGHTS &
    #    COHESIVE FORENSIC CONSPIRACY TRAIL SUB-REGIONS (Clues 1A, 1B, 2, 3):
    # --------------------------------------------------------------------------
    # 4A. `UV_PLANTER_STONE = (0.52, 0.74, 0.51, 0.63)` (`x: 512..768, y: 512..648`)
    alb[512:648, 512:768] = (94, 101, 110)
    orm[512:648, 512:768] = (242, int(0.66 * 255), int(0.08 * 255))
    for py in [556, 600]:
        alb[py : py + 3, 512:768] = (74, 80, 88)
        hgt[py : py + 3, 512:768] = 114.0
    # Subtle water/irrigation mineral streaks near bottom lip of planter stone
    for mx in range(524, 756, 28):
        alb[612:646, mx : mx + 8] = (82, 92, 98)
        orm[612:646, mx : mx + 8, 1] = int(0.48 * 255)

    # 4B. CLUE 1A — Dedicated Apartment 201 Workbench Top (`UV_WORKBENCH_TOP = (0.76, 0.99, 0.51, 0.64)`, `x: 768..1024, y: 512..652`)
    # Base: Warm Honey-Teak Butcher-Block (`RGB 140, 108, 80`)
    alb[512:652, 768:1024] = (140, 108, 80)
    orm[512:652, 768:1024] = (244, int(0.46 * 255), int(0.04 * 255))
    for wy in range(512, 652):
        w_delta = int(round(5.0 * math.sin(wy * 0.25)))
        alb[wy, 768:1024] = np.clip(np.array([140 + w_delta, 108 + int(w_delta * 0.8), 80 + int(w_delta * 0.6)]), 0, 255)
    # Wear-polished forearm rest along the front edge (y: 618..650) — smoother roughness (0.26) & lighter honey tone
    alb[620:650, 780:1012] = (162, 130, 98)
    orm[620:650, 780:1012, 1] = int(0.26 * 255)

    # 4C. CLUE 1B — Dedicated Workbench Pegboard & Backsplash (`UV_WORKBENCH_PEGBOARD = (0.52, 0.74, 0.64, 0.72)`, `x: 512..768, y: 648..740`)
    alb[648:740, 512:768] = (78, 86, 96)
    orm[648:740, 512:768] = (238, int(0.44 * 255), int(0.74 * 255))
    # Rectangular ghost outline where an older D-03 Hydro-Cryo service frame used to hang (x: 534..626, y: 658..728)
    alb[658:728, 534:626] = (96, 104, 114)
    orm[658:728, 534:626, 1] = int(0.32 * 255)
    # Pegboard holes grid
    for py in range(656, 734, 14):
        for px in range(524, 758, 18):
            alb[py : py + 3, px : px + 3] = (42, 46, 52)
            orm[py : py + 3, px : px + 3, 0] = 175

    # 4D. CLUE 2 — Dedicated Physical Drag / Single-Locked-Tread Skid Trail (`UV_FLOOR_SKID_TRAIL = (0.76, 0.99, 0.64, 0.72)`, `x: 768..1024, y: 652..740`)
    alb[652:740, 768:1024] = (98, 104, 112)
    orm[652:740, 768:1024] = (242, int(0.56 * 255), int(0.12 * 255))
    # Asymmetric single-locked-tread rubber skid mark along left track lane (y: 666..688)
    alb[668:686, 774:1018] = (46, 50, 56)
    orm[668:686, 774:1018, 1] = int(0.76 * 255)
    for tx in range(778, 1014, 12):
        alb[666:688, tx : tx + 6] = (34, 38, 44)
        hgt[666:688, tx : tx + 6] = 120.0
    # Metallic actuator drag score line alongside the locked tread
    alb[690:693, 776:1016] = (138, 146, 156)
    orm[690:693, 776:1016, 1] = int(0.22 * 255)
    orm[690:693, 776:1016, 2] = int(0.75 * 255)
    # Glossy violet/cyan cryogen-coolant drip trail spots (`roughness = 0.16`)
    for dx, dy, dw, dh, col_drip in [
        (796, 700, 18, 10, (92, 82, 168)),
        (838, 706, 24, 12, (74, 134, 162)),
        (888, 698, 20, 11, (96, 84, 174)),
        (936, 704, 26, 12, (72, 140, 168)),
        (982, 700, 18, 10, (92, 82, 168)),
    ]:
        alb[dy : dy + dh, dx : dx + dw] = col_drip
        orm[dy : dy + dh, dx : dx + dw, 1] = int(0.16 * 255)
        orm[dy : dy + dh, dx : dx + dw, 2] = int(0.35 * 255)
        emi[dy : dy + dh, dx : dx + dw] = (22, 34, 48)

    # 4E. Functional Light Diffuser Swatches (`y: 740..780, x: 512..1024` -> `v: 0.723..0.762`)
    # Note: `patch_residential_sector_generator.py` uses `v: 0.66..0.72` or we can update the constants in `patch_residential_sector_generator.py`!
    # Let's place the 3 light swatches at `y: 742..778` (`v: 0.725..0.758`):
    alb[740:780, 512:1024] = (74, 80, 88)
    orm[740:780, 512:1024] = (242, int(0.56 * 255), int(0.12 * 255))
    # Swatch 1: Warm Task (`x: 528..680, y: 744..776` -> `u: 0.52..0.66, v: 0.727..0.757`)
    alb[744:776, 528:680] = hex_rgb("#F2D8B3")
    orm[744:776, 528:680] = (255, int(0.22 * 255), int(0.05 * 255))
    emi[744:776, 528:680] = hex_rgb("#B89E7C")
    # Swatch 2: Muted Functional Cyan (`x: 696..848, y: 744..776` -> `u: 0.68..0.825, v: 0.727..0.757`)
    alb[744:776, 696:848] = hex_rgb("#2E8B9A")
    orm[744:776, 696:848] = (255, int(0.22 * 255), int(0.10 * 255))
    emi[744:776, 696:848] = hex_rgb("#1E5C66")
    # Swatch 3: Muted Functional Amber (`x: 864..1008, y: 744..776` -> `u: 0.845..0.984, v: 0.727..0.757`)
    alb[744:776, 864:1008] = hex_rgb("#B87328")
    orm[744:776, 864:1008] = (255, int(0.26 * 255), int(0.10 * 255))
    emi[744:776, 864:1008] = hex_rgb("#784A1A")

    # 4F. CLUE 3 — Dedicated Tampered Door & Substation Placards (`x: 512..1024, y: 780..1024`)
    alb[780:1024, 512:1024] = hex_rgb("#242B34")
    orm[780:1024, 512:1024] = (244, int(0.38 * 255), int(0.48 * 255))

    alb_im = Image.fromarray(alb, mode="RGB")
    emi_im = Image.fromarray(emi, mode="RGB")
    orm_im = Image.fromarray(orm, mode="RGB")
    draw_alb = ImageDraw.Draw(alb_im)
    draw_emi = ImageDraw.Draw(emi_im)
    draw_orm = ImageDraw.Draw(orm_im)

    font_tiny = load_font(10, bold=False)
    font_small = load_font(12, bold=True)
    font_med = load_font(15, bold=True)
    font_num = load_font(28, bold=True)
    font_sub = load_font(14, bold=True)
    font_ghost = load_font(13, bold=True)

    # --------------------------------------------------------------------------
    # Draw Clue 1A Details on `UV_WORKBENCH_TOP` (`x: 768..1024, y: 512..652`):
    # --------------------------------------------------------------------------
    # 1. Circular Plasma-Arc & Solder-Flux Scorch Mark (`cx=848, cy=582`) where 3rd capacitor coil blew
    draw_alb.ellipse([814, 548, 882, 616], fill=(78, 52, 32), outline=(104, 70, 42), width=3)
    draw_alb.ellipse([826, 560, 870, 604], fill=(34, 26, 22), outline=(168, 114, 54), width=2)
    draw_alb.ellipse([838, 572, 858, 592], fill=(20, 16, 14))
    draw_orm.ellipse([814, 548, 882, 616], fill=(210, 215, 20))
    # 3 Capacitor Pad footprints (`C1`, `C2` intact copper pads, `C3` blown inside the scorch ring!)
    draw_alb.rectangle([786, 558, 804, 572], fill=(198, 146, 74), outline=(90, 64, 36), width=1)
    draw_alb.rectangle([786, 584, 804, 598], fill=(198, 146, 74), outline=(90, 64, 36), width=1)
    draw_alb.text((782, 544), "C1 C2", fill=(216, 198, 168), font=font_tiny)
    draw_alb.text((822, 616), "C3 [BLOWN]", fill=(228, 136, 92), font=font_tiny)

    # 2. Faint Coffee Mug Ring (`cx=798, cy=620`)
    draw_alb.ellipse([778, 600, 818, 640], outline=(88, 60, 38), width=3)
    draw_alb.arc([776, 598, 820, 642], start=20, end=210, fill=(72, 48, 30), width=2)

    # 3. Scratched Serial Fragment `A7-0204-MEM` & Chalk Tally Marks `III` (`x: 780..885, y: 520..542`)
    draw_alb.text((780, 518), "A7-0204-MEM // III", fill=(198, 178, 148), font=font_small)
    draw_alb.line([(780, 533), (882, 533)], fill=(176, 148, 116), width=1)

    # 4. Taped Blueprint / Oscilloscope Calibration Note (`x: 892..1016, y: 520..636`)
    draw_alb.rectangle([892, 520, 1016, 636], fill=(212, 224, 232), outline=(142, 158, 170), width=2)
    draw_orm.rectangle([892, 520, 1016, 636], fill=(250, 168, 5))
    # Yellow/Amber Kapton Tape strips on top-left and bottom-right corners
    draw_alb.polygon([(884, 528), (912, 514), (918, 524), (890, 538)], fill=(214, 156, 56))
    draw_alb.polygon([(994, 632), (1020, 618), (1023, 628), (1000, 642)], fill=(214, 156, 56))
    # Oscilloscope grid & 13.56 MHz / 412 Hz harmonic spike waveform at 03:14 UTC
    draw_alb.rectangle([898, 548, 1010, 586], fill=(24, 38, 48), outline=(56, 88, 104), width=1)
    wf_pts = [
        (900, 572), (914, 571), (924, 573), (932, 568),
        (938, 550), (943, 583), (948, 552), (954, 580),
        (960, 566), (972, 572), (990, 571), (1008, 572),
    ]
    draw_alb.line(wf_pts, fill=(68, 218, 242), width=2)
    draw_emi.line(wf_pts, fill=(24, 88, 98), width=2)
    draw_alb.text((897, 523), "03:14 UTC B-14", fill=(26, 36, 46), font=font_small)
    draw_alb.text((897, 536), "13.56MHz / 412Hz", fill=(42, 82, 104), font=font_tiny)
    draw_alb.text((897, 589), "#0204: PUDDLE", fill=(168, 42, 34), font=font_tiny)
    draw_alb.text((897, 602), "  -> KELVIN", fill=(28, 74, 96), font=font_small)
    draw_alb.text((897, 619), "COIL C3 DUMP!", fill=(168, 42, 34), font=font_tiny)
    # Hand-drawn red/amber arrow pointing from the note directly to the blown C3 scorch ring (`x=892 -> 866, y=582`)
    draw_alb.line([(894, 582), (866, 582)], fill=(196, 56, 38), width=3)
    draw_alb.polygon([(862, 582), (874, 575), (874, 589)], fill=(196, 56, 38))

    # --------------------------------------------------------------------------
    # Draw Clue 1B Details on `UV_WORKBENCH_PEGBOARD` (`x: 512..768, y: 648..740`):
    # --------------------------------------------------------------------------
    draw_alb.rectangle([534, 658, 626, 728], outline=(124, 134, 146), width=2)
    draw_alb.text((540, 684), "D-03 HYDRO", fill=(116, 126, 138), font=font_small)
    draw_alb.text((540, 700), "[REMOVED]", fill=(116, 126, 138), font=font_tiny)
    # Pinned Forensic Schematic Card on right side of pegboard (`x: 642..756, y: 656..732`)
    draw_alb.rectangle([642, 656, 756, 732], fill=(206, 218, 226), outline=(136, 150, 162), width=2)
    draw_alb.text((648, 661), "RFID BUS TAP", fill=(28, 40, 52), font=font_small)
    draw_alb.text((648, 678), "PIN_RESET->B14", fill=(42, 92, 112), font=font_tiny)
    draw_alb.text((648, 693), "03:14 MEM LOG", fill=(164, 46, 36), font=font_tiny)
    draw_alb.text((648, 708), "UNIT #0204", fill=(28, 40, 52), font=font_small)

    # --------------------------------------------------------------------------
    # Draw Clue 2 Stencil on `UV_FLOOR_SKID_TRAIL` (`x: 768..1024, y: 652..740`):
    # --------------------------------------------------------------------------
    draw_alb.text((784, 718), "SUB-BUS B-14 // HATCH 04 [DRAG TRACE #0204]", fill=(142, 150, 160), font=font_tiny)

    # --------------------------------------------------------------------------
    # Draw Clue 3 Tampered Door Placards (`x: 512..1024, y: 780..1024`):
    #   UV_PLACARD_201 = (0.516, 0.742, 0.762, 0.867) -> x: 528..760, y: 780..888
    #   UV_PLACARD_202 = (0.758, 0.984, 0.762, 0.867) -> x: 776..1008, y: 780..888
    #   UV_PLACARD_1A  = (0.516, 0.742, 0.883, 0.988) -> x: 528..760, y: 904..1012
    #   UV_PLACARD_1B  = (0.758, 0.984, 0.883, 0.988) -> x: 776..1008, y: 904..1012
    # --------------------------------------------------------------------------
    # 1. APT 201 Placard (`x: 528..760, y: 780..888`) — Pried bezel nicks + scratched-out `CLR-4 [REVOKED] -> TECH-2`
    x0, y0, x1, y1 = 528, 780, 760, 888
    draw_alb.rectangle([x0, y0, x1, y1], fill=hex_rgb("#222830"), outline=hex_rgb("#4A5462"), width=3)
    # Pried-bezel screwdriver gouges on the left metallic frame
    for gy in [796, 818, 844, 862]:
        draw_alb.line([(x0, gy), (x0 + 11, gy - 4)], fill=(182, 192, 204), width=3)
        draw_orm.line([(x0, gy), (x0 + 11, gy - 4)], fill=(250, 48, 235), width=3)
    # Corner mounting bolts
    for bx, by in [(x0 + 10, y0 + 10), (x1 - 10, y0 + 10), (x0 + 10, y1 - 10), (x1 - 10, y1 - 10)]:
        draw_alb.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(122, 132, 144))
    draw_alb.rectangle([x0 + 10, y0 + 16, x0 + 18, y1 - 16], fill=hex_rgb("#2E8B9A"))
    draw_emi.rectangle([x0 + 10, y0 + 16, x0 + 18, y1 - 16], fill=hex_rgb("#1E5C66"))
    draw_alb.text((x0 + 28, y0 + 14), "APT 201", fill=hex_rgb("#E2E8F0"), font=font_num)
    draw_emi.text((x0 + 28, y0 + 14), "APT 201", fill=hex_rgb("#1E5C66"), font=font_num)
    # Scratched-out `CLR-4 [REVOKED]` with strike-through + `-> TECH-2`
    draw_alb.text((x0 + 28, y0 + 50), "CLR-4 [REVOKED]", fill=hex_rgb("#8E98A4"), font=font_small)
    draw_alb.line([(x0 + 26, y0 + 58), (x0 + 162, y0 + 56)], fill=hex_rgb("#D45B3E"), width=3)
    draw_alb.text((x0 + 28, y0 + 68), "-> TECH-2 // 13.56MHz", fill=hex_rgb("#88C8D8"), font=font_sub)

    # 2. APT 202 Placard (`x: 776..1008, y: 780..888`) — Quartermaster + Bus B-14 inspection tag
    x0, y0, x1, y1 = 776, 780, 1008, 888
    draw_alb.rectangle([x0, y0, x1, y1], fill=hex_rgb("#222830"), outline=hex_rgb("#4A5462"), width=3)
    for bx, by in [(x0 + 10, y0 + 10), (x1 - 10, y0 + 10), (x0 + 10, y1 - 10), (x1 - 10, y1 - 10)]:
        draw_alb.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(122, 132, 144))
    draw_alb.rectangle([x0 + 10, y0 + 16, x0 + 18, y1 - 16], fill=hex_rgb("#2E8B9A"))
    draw_emi.rectangle([x0 + 10, y0 + 16, x0 + 18, y1 - 16], fill=hex_rgb("#1E5C66"))
    draw_alb.text((x0 + 28, y0 + 14), "APT 202", fill=hex_rgb("#E2E8F0"), font=font_num)
    draw_emi.text((x0 + 28, y0 + 14), "APT 202", fill=hex_rgb("#1E5C66"), font=font_num)
    draw_alb.text((x0 + 28, y0 + 52), "QUARTERMASTER", fill=hex_rgb("#9EA8B4"), font=font_sub)
    draw_alb.text((x0 + 28, y0 + 70), "SEC-04 // BUS B-14", fill=hex_rgb("#74808E"), font=font_tiny)

    # 3. RM 1A Placard (`x: 528..760, y: 904..1012`) — Laundry Lounge
    x0, y0, x1, y1 = 528, 904, 760, 1012
    draw_alb.rectangle([x0, y0, x1, y1], fill=hex_rgb("#222830"), outline=hex_rgb("#4A5462"), width=3)
    for bx, by in [(x0 + 10, y0 + 10), (x1 - 10, y0 + 10), (x0 + 10, y1 - 10), (x1 - 10, y1 - 10)]:
        draw_alb.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(122, 132, 144))
    draw_alb.rectangle([x0 + 10, y0 + 16, x0 + 18, y1 - 16], fill=hex_rgb("#2E8B9A"))
    draw_emi.rectangle([x0 + 10, y0 + 16, x0 + 18, y1 - 16], fill=hex_rgb("#1E5C66"))
    draw_alb.text((x0 + 28, y0 + 14), "RM 1A", fill=hex_rgb("#E2E8F0"), font=font_num)
    draw_emi.text((x0 + 28, y0 + 14), "RM 1A", fill=hex_rgb("#1E5C66"), font=font_num)
    draw_alb.text((x0 + 28, y0 + 52), "LAUNDRY LOUNGE", fill=hex_rgb("#9EA8B4"), font=font_sub)
    draw_alb.text((x0 + 28, y0 + 70), "HYDRO FEED // NOMINAL", fill=hex_rgb("#74808E"), font=font_tiny)

    # 4. RM 1B Placard (`x: 776..1008, y: 904..1012`) — Over-painted Ghost Stencil `SEC-04 // TELEMETRY RELAY [RESTRICTED]` + Broken Seal `2026-10-19 // 03:14`!
    x0, y0, x1, y1 = 776, 904, 1008, 1012
    draw_alb.rectangle([x0, y0, x1, y1], fill=hex_rgb("#222830"), outline=hex_rgb("#5A4A3A"), width=3)
    # Ghost stencil bleeding through underneath the fresh dark over-paint
    draw_alb.rectangle([x0 + 22, y0 + 8, x1 - 8, y1 - 8], fill=hex_rgb("#2B3038"))
    draw_alb.text((x0 + 24, y0 + 8), "SEC-04 // TELEMETRY RELAY", fill=hex_rgb("#7E6448"), font=font_ghost)
    draw_alb.text((x0 + 24, y0 + 46), "[RESTRICTED // CLR-4 ONLY]", fill=hex_rgb("#8A543E"), font=font_small)
    # Over-painted `RM 1B` & `BOT SUBSTATION`
    draw_alb.rectangle([x0 + 10, y0 + 16, x0 + 18, y1 - 16], fill=hex_rgb("#C47D2B"))
    draw_emi.rectangle([x0 + 10, y0 + 16, x0 + 18, y1 - 16], fill=hex_rgb("#784A1A"))
    draw_alb.text((x0 + 28, y0 + 18), "RM 1B", fill=hex_rgb("#E6ECF2"), font=font_num)
    draw_emi.text((x0 + 28, y0 + 18), "RM 1B", fill=hex_rgb("#784A1A"), font=font_num)
    draw_alb.text((x0 + 28, y0 + 58), "BOT SUBSTATION", fill=hex_rgb("#C8D0D8"), font=font_sub)
    # Broken Security Seal Sticker on right edge with exact timestamp `2026-10-19 // 03:14`
    draw_alb.rectangle([x0 + 26, y0 + 78, x1 - 10, y1 - 8], fill=(154, 52, 34), outline=(218, 134, 62), width=1)
    draw_alb.line([(x0 + 118, y0 + 78), (x0 + 126, y1 - 8)], fill=(28, 32, 38), width=3)  # Torn seal gap!
    draw_alb.text((x0 + 30, y0 + 80), "SEAL: 2026-10-19 // 03:14", fill=(248, 224, 188), font=font_tiny)

    alb = add_ultra_clean_micro_grain(np.asarray(alb_im, dtype=np.uint8), sigma=0.45, seed=101)
    orm = add_ultra_clean_micro_grain(np.asarray(orm_im, dtype=np.uint8), sigma=0.35, seed=102)
    emi = np.asarray(emi_im, dtype=np.uint8)

    # Tangent-space normal map from height field
    gy, gx = np.gradient(hgt / 255.0 * 3.5)
    nx = -gx
    ny = -gy
    nz = np.ones_like(nx)
    nlen = np.sqrt(nx * nx + ny * ny + nz * nz)
    nrm = np.zeros((H, W, 3), dtype=np.uint8)
    nrm[:, :, 0] = np.clip((nx / nlen * 0.5 + 0.5) * 255.0, 0, 255).astype(np.uint8)
    nrm[:, :, 1] = np.clip((ny / nlen * 0.5 + 0.5) * 255.0, 0, 255).astype(np.uint8)
    nrm[:, :, 2] = np.clip((nz / nlen * 0.5 + 0.5) * 255.0, 0, 255).astype(np.uint8)

    # Calm Architectural Tempered Glass (`residential_atrium_glass_translucent.png`, 512x512 RGBA)
    GW, GH = 512, 512
    gls = np.zeros((GH, GW, 4), dtype=np.uint8)
    gls[:, :, 0] = 96
    gls[:, :, 1] = 116
    gls[:, :, 2] = 132
    gls[:, :, 3] = 68
    gls[0:8, :, :] = (64, 72, 82, 185)
    gls[GH - 8 : GH, :, :] = (64, 72, 82, 185)
    gls[:, 0:8, :] = (64, 72, 82, 185)
    gls[:, GW - 8 : GW, :] = (64, 72, 82, 185)
    gls[:, :, :3] = add_ultra_clean_micro_grain(gls[:, :, :3], sigma=0.30, seed=103)

    # Compute metrics
    black_emi_pct = float(np.mean(np.all(emi == 0, axis=2)) * 100.0)
    noise_alb = compute_micro_noise_pct(alb)
    noise_orm = compute_micro_noise_pct(orm)
    noise_nrm = compute_micro_noise_pct(nrm)
    noise_emi = compute_micro_noise_pct(emi)
    noise_gls = compute_micro_noise_pct(gls[:, :, :3])

    suites = [
        ("residential_atrium_and_apartment_atlas_albedo.png", Image.fromarray(alb, "RGB")),
        ("residential_atrium_and_apartment_atlas_orm.png", Image.fromarray(orm, "RGB")),
        ("residential_atrium_and_apartment_atlas_normal.png", Image.fromarray(nrm, "RGB")),
        ("residential_atrium_and_apartment_atlas_emission.png", Image.fromarray(emi, "RGB")),
        ("residential_atrium_glass_translucent.png", Image.fromarray(gls, "RGBA")),
        ("tex_residential_atlas_albedo.png", Image.fromarray(alb, "RGB")),
        ("tex_residential_atlas_orm.png", Image.fromarray(orm, "RGB")),
        ("tex_residential_atlas_normal.png", Image.fromarray(nrm, "RGB")),
        ("tex_residential_atlas_emission.png", Image.fromarray(emi, "RGB")),
        ("tex_residential_glass_translucent.png", Image.fromarray(gls, "RGBA")),
    ]
    import shutil
    base_dir = TEX_DIRS[0]
    for fn, img_obj in suites[:5]:
        p0 = os.path.join(base_dir, fn)
        img_obj.save(p0, format="PNG")
    alias_pairs = list(zip([s[0] for s in suites[:5]], [s[0] for s in suites[5:]]))
    for fn_src, fn_alias in alias_pairs:
        p0 = os.path.join(base_dir, fn_src)
        shutil.copyfile(p0, os.path.join(base_dir, fn_alias))
        for d in TEX_DIRS[1:]:
            shutil.copyfile(p0, os.path.join(d, fn_src))
            shutil.copyfile(p0, os.path.join(d, fn_alias))

    print(
        f"[ResidentialAtlas] Saved 1024x1024 Forensic PBR suite across {len(TEX_DIRS)} directories | "
        f"pitch_black_emission={black_emi_pct:.2f}% | "
        f"micro_noise: albedo={noise_alb:.3f}%, orm={noise_orm:.3f}%, normal={noise_nrm:.3f}%, emission={noise_emi:.3f}%, glass={noise_gls:.3f}%"
    )


if __name__ == "__main__":
    generate_residential_atlas()
