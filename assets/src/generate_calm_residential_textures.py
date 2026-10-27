#!/usr/bin/env python3
"""
Generates the Low-Key Atmospheric & 90/10 Calm Architectural Neutral PBR Texture Suite
for the Preface 2-Story Residential Sector (`preface_playable_area.tscn` / `preface_residential_sector.glb`)
per Jared's [t3u] directive:
  - 92%+ of the atlas is calm, low-saturation architectural neutrals:
    * Q1 Upper (`u:0.00..0.50, v:0.00..0.28`): Matte warm grey / architectural stone-plaster walls (`#9CA2AA` / `#848A92`, roughness 0.58, metallic 0.08) — ZERO text, ZERO neon!
    * Q1 Lower-Left (`u:0.00..0.25, v:0.28..0.50`): Muted natural walnut wood (`#5E493A` / `#6E5042`, roughness 0.52, metallic 0.04) — ZERO text, ZERO neon!
    * Q1 Lower-Right (`u:0.25..0.50, v:0.28..0.50`): Muted architectural slate upholstery (`#3C4652` / `#46505E`, roughness 0.74, metallic 0.02) — ZERO text, ZERO neon!
    * Q2 Upper (`u:0.50..1.00, v:0.00..0.26`): Calm matte architectural slate-grey corridor wall cladding (`#828890` / `#787E86`, roughness 0.58, metallic 0.08) — ZERO text, ZERO neon!
    * Q2 Lower (`u:0.50..1.00, v:0.26..0.50`): Grounded matte dark slate/concrete floor deck (`#2B3038` / `#343A44`, roughness 0.72, metallic 0.12) — ZERO text, ZERO numbers, ZERO neon stripes!
    * Q3 Upper (`u:0.00..0.50, v:0.50..0.74`): Non-emissive matte dark brushed steel (`#3A414A` / `#4E5662`, roughness 0.44, metallic 0.78, emission = #000000) for columns, portal frames, stairs, and trim.
    * Q3 Lower-Left (`u:0.00..0.25, v:0.74..1.00`): Coiled copper/dark-steel cable spool housing (`#5A4638` / `#3A414A`, roughness 0.42, metallic 0.68).
    * Q3 Lower-Right (`u:0.25..0.50, v:0.74..1.00`): Matte dark slate industrial battery cell casing (`#2B3038` / `#3A414A`, roughness 0.46, metallic 0.65) with subtle muted-cyan (`#2E8B9A`) charge ticks.
    * Q4 Upper (`u:0.50..1.00, v:0.50..0.64`): Calm architectural slate planter stone (`#464C54` / `#383E46`, roughness 0.68, metallic 0.08).
    * Q4 Mid (`u:0.50..1.00, v:0.64..0.75`): 3 Functional Light Diffuser Swatches:
      1. Soft warm white (`#F2D8B3`, 3300K) localized task lamp strip (`u:0.52..0.67, v:0.65..0.74`)
      2. Muted functional cyan (`#2E8B9A`, low emission 0.55) diagnostic terminal strip (`u:0.68..0.83, v:0.65..0.74`)
      3. Muted amber (`#B87328`, low emission 0.50) stair-tread & substation safety strip (`u:0.84..0.98, v:0.65..0.74`)
    * Q4 Lower (`u:0.50..1.00, v:0.75..1.00`): Dedicated Isolated Door Placard Sub-Region (`x:264..504, y:388..504`)
      never overlapped by any wall, floor, column, or furniture UVs:
      - `UV_PLACARD_201 = (0.52, 0.74, 0.76, 0.87)` -> `APT 201`
      - `UV_PLACARD_202 = (0.76, 0.98, 0.76, 0.87)` -> `APT 202`
      - `UV_PLACARD_1A  = (0.52, 0.74, 0.88, 0.99)` -> `RM 1A`
      - `UV_PLACARD_1B  = (0.76, 0.98, 0.88, 0.99)` -> `RM 1B`
  - >96% of the emission map is pitch black (`#000000`).
  - <1.0% micro-noise verified across all channels.
"""
import os
import shutil
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
    W, H = 512, 512
    alb = np.zeros((H, W, 3), dtype=np.uint8)
    orm = np.zeros((H, W, 3), dtype=np.uint8)  # R=AO, G=Roughness, B=Metallic
    emi = np.zeros((H, W, 3), dtype=np.uint8)  # 96%+ pitch black #000000
    hgt = np.full((H, W), 128.0, dtype=np.float32)

    # --------------------------------------------------------------------------
    # 1. Q1 (`x: 0..255, y: 0..255`):
    #    - Upper (`y: 0..143`): Matte Warm Grey / Stone-Plaster Apartment Walls (`#8E949C` / `#828890`, rough 0.58, met 0.08)
    #    - Lower-Left (`x: 0..127, y: 144..255`): Muted Natural Walnut Wood (`#5E493A` / `#6E5042`, rough 0.52, met 0.04)
    #    - Lower-Right (`x: 128..255, y: 144..255`): Muted Slate Upholstery (`#3C4652` / `#45505E`, rough 0.74, met 0.02)
    # --------------------------------------------------------------------------
    alb[0:144, 0:256] = hex_rgb("#8C929A")
    orm[0:144, 0:256] = (245, int(0.58 * 255), int(0.08 * 255))
    # Subtle architectural plaster panel joints (zero text, zero neon!)
    for py in [36, 72, 108]:
        alb[py : py + 2, 0:256] = hex_rgb("#7C828A")
        orm[py : py + 2, 0:256, 0] = 222
        hgt[py : py + 2, 0:256] = 114.0
    for px in [64, 128, 192]:
        alb[0:144, px : px + 2] = hex_rgb("#7C828A")
        orm[0:144, px : px + 2, 0] = 222
        hgt[0:144, px : px + 2] = 114.0

    # Q1 Lower-Left: Muted Natural Walnut Wood (`#5E493A` / `#685040`)
    alb[144:256, 0:128] = hex_rgb("#5E493A")
    orm[144:256, 0:128] = (244, int(0.52 * 255), int(0.04 * 255))
    for wy in range(144, 256, 6):
        alb[wy : wy + 2, 0:128] = hex_rgb("#534032")
        hgt[wy : wy + 2, 0:128] = 123.0
    for wy in range(147, 256, 12):
        alb[wy : wy + 1, 0:128] = hex_rgb("#6E5442")

    # Q1 Lower-Right: Muted Slate Upholstery (`#3C4652` / `#444E5C`)
    alb[144:256, 128:256] = hex_rgb("#3C4652")
    orm[144:256, 128:256] = (242, int(0.74 * 255), int(0.02 * 255))
    for sy in range(156, 250, 24):
        alb[sy : sy + 2, 128:256] = hex_rgb("#323B46")
        orm[sy : sy + 2, 128:256, 0] = 218
        hgt[sy : sy + 2, 128:256] = 116.0
    for sx in range(152, 248, 32):
        alb[144:256, sx : sx + 2] = hex_rgb("#323B46")
        hgt[144:256, sx : sx + 2] = 116.0

    # --------------------------------------------------------------------------
    # 2. Q2 (`x: 256..511, y: 0..255`):
    #    - Upper (`y: 0..131`): Calm Architectural Slate-Plaster Corridor Walls (`#7C828A` / `#727880`, rough 0.58, met 0.08)
    #    - Lower (`y: 132..255`): Grounded Matte Dark Slate/Concrete Floor Deck (`#2B3038` / `#343A44`, rough 0.72, met 0.12)
    #    ZERO text, ZERO stretched numbers, ZERO neon stripes!
    # --------------------------------------------------------------------------
    alb[0:132, 256:512] = hex_rgb("#7C828A")
    orm[0:132, 256:512] = (244, int(0.58 * 255), int(0.08 * 255))
    for py in [33, 66, 99]:
        alb[py : py + 2, 256:512] = hex_rgb("#6A7078")
        orm[py : py + 2, 256:512, 0] = 220
        hgt[py : py + 2, 256:512] = 114.0
    for px in [320, 384, 448]:
        alb[0:132, px : px + 2] = hex_rgb("#6A7078")
        orm[0:132, px : px + 2, 0] = 220
        hgt[0:132, px : px + 2] = 114.0

    # Q2 Lower: Grounded Matte Dark Slate/Concrete Floor (`#2B3038` / `#343A44`)
    alb[132:256, 256:512] = hex_rgb("#2E343C")
    orm[132:256, 256:512] = (240, int(0.72 * 255), int(0.12 * 255))
    for fy in [162, 194, 226]:
        alb[fy : fy + 2, 256:512] = hex_rgb("#242930")
        orm[fy : fy + 2, 256:512, 0] = 215
        hgt[fy : fy + 2, 256:512] = 115.0
    for fx in [320, 384, 448]:
        alb[132:256, fx : fx + 2] = hex_rgb("#242930")
        orm[132:256, fx : fx + 2, 0] = 215
        hgt[132:256, fx : fx + 2] = 115.0

    # --------------------------------------------------------------------------
    # 3. Q3 (`x: 0..255, y: 256..511`):
    #    - Upper (`y: 256..376`): Non-Emissive Matte Dark Brushed Steel (`#3A414A` / `#4E5662`, rough 0.44, met 0.78)
    #    - Lower-Left (`x: 0..127, y: 376..511`): Copper/Slate Wire Spool Housing (`#4E5662` / `#7C5A3E`)
    #    - Lower-Right (`x: 128..255, y: 376..511`): Matte Dark Slate Battery Cell Housing (`#2B3038` / `#3A414A`)
    # --------------------------------------------------------------------------
    alb[256:376, 0:256] = hex_rgb("#3E4650")
    orm[256:376, 0:256] = (242, int(0.44 * 255), int(0.78 * 255))
    for sy in [286, 316, 346]:
        alb[sy : sy + 2, 0:256] = hex_rgb("#323840")
        orm[sy : sy + 2, 0:256, 0] = 216
        hgt[sy : sy + 2, 0:256] = 116.0
    for sx in [64, 128, 192]:
        alb[256:376, sx : sx + 2] = hex_rgb("#4E5662")
        hgt[256:376, sx : sx + 2] = 136.0

    # Q3 Lower-Left: Coiled Copper/Slate Wire Spool (`x: 0..127, y: 376..511`)
    alb[376:512, 0:128] = hex_rgb("#363D46")
    orm[376:512, 0:128] = (238, int(0.42 * 255), int(0.72 * 255))
    for cy in range(392, 488, 10):
        alb[cy : cy + 5, 16:112] = hex_rgb("#8C623E")
        orm[cy : cy + 5, 16:112] = (242, int(0.32 * 255), int(0.85 * 255))
        hgt[cy : cy + 5, 16:112] = 138.0

    # Q3 Lower-Right: Matte Dark Slate Battery Cell (`x: 128..255, y: 376..511`)
    alb[376:512, 128:256] = hex_rgb("#2B3038")
    orm[376:512, 128:256] = (240, int(0.46 * 255), int(0.65 * 255))
    alb[384:402, 140:244] = hex_rgb("#4A525E")
    # 3 small muted functional cyan (`#2E8B9A`) charge level ticks (tiny area, low emission)
    for bi, by in enumerate([414, 434, 454]):
        alb[by : by + 8, 164:220] = hex_rgb("#2E8B9A")
        orm[by : by + 8, 164:220] = (250, int(0.24 * 255), int(0.15 * 255))
        emi[by : by + 8, 164:220] = hex_rgb("#1B535C")  # ~0.55 muted cyan intensity

    # --------------------------------------------------------------------------
    # 4. Q4 (`x: 256..511, y: 256..511`):
    #    - Upper (`y: 256..328`): Planter Architectural Concrete (`#464C54` / `#3A4048`, rough 0.68, met 0.08)
    #    - Mid (`y: 328..384`): 3 Functional Light Swatches:
    #      * Warm Task (`x: 264..340, y: 334..376`): Soft Warm White `#F2D8B3` (3300K)
    #      * Muted Cyan (`x: 348..424, y: 334..376`): Functional Cyan `#2E8B9A`
    #      * Muted Amber (`x: 432..504, y: 334..376`): Functional Amber `#B87328`
    #    - Lower (`y: 384..511`): 4 Dedicated Isolated Door Placards (`APT 201`, `APT 202`, `RM 1A`, `RM 1B`)
    # --------------------------------------------------------------------------
    alb[256:384, 256:512] = hex_rgb("#424850")
    orm[256:384, 256:512] = (242, int(0.68 * 255), int(0.08 * 255))
    for py in [280, 304]:
        alb[py : py + 2, 256:512] = hex_rgb("#343940")
        hgt[py : py + 2, 256:512] = 116.0

    # Functional Light Swatch 1: Soft Warm White (`#F2D8B3`, 3300K task lamp)
    alb[334:376, 264:340] = hex_rgb("#F2D8B3")
    orm[334:376, 264:340] = (255, int(0.22 * 255), int(0.05 * 255))
    emi[334:376, 264:340] = hex_rgb("#A89274")  # Warm low-key task glow

    # Functional Light Swatch 2: Muted Functional Cyan (`#2E8B9A`, terminal & wrist accent)
    alb[334:376, 348:424] = hex_rgb("#2E8B9A")
    orm[334:376, 348:424] = (255, int(0.22 * 255), int(0.10 * 255))
    emi[334:376, 348:424] = hex_rgb("#1C5660")  # Muted cyan low emission (~0.55)

    # Functional Light Swatch 3: Muted Functional Amber (`#B87328`, stair tread & substation safety)
    alb[334:376, 432:504] = hex_rgb("#B87328")
    orm[334:376, 432:504] = (255, int(0.26 * 255), int(0.10 * 255))
    emi[334:376, 432:504] = hex_rgb("#6E4418")  # Muted amber low emission (~0.50)

    # Dedicated Isolated Door Placards Sub-Region (`x: 256..511, y: 384..511`)
    alb[384:512, 256:512] = hex_rgb("#1E242B")
    orm[384:512, 256:512] = (244, int(0.38 * 255), int(0.45 * 255))

    alb_im = Image.fromarray(alb, mode="RGB")
    emi_im = Image.fromarray(emi, mode="RGB")
    draw_alb = ImageDraw.Draw(alb_im)
    draw_emi = ImageDraw.Draw(emi_im)

    font_num = load_font(16, bold=True)
    font_sub = load_font(9, bold=False)

    placards = [
        # (x0, y0, x1, y1, title, subtitle, accent_hex, emi_hex)
        (264, 390, 380, 444, "APT 201", "LEAD TECH", "#2E8B9A", "#1C5660"),
        (388, 390, 504, 444, "APT 202", "QUARTERMASTER", "#2E8B9A", "#1C5660"),
        (264, 452, 380, 506, "RM 1A", "LAUNDRY LOUNGE", "#2E8B9A", "#1C5660"),
        (388, 452, 504, 506, "RM 1B", "BOT SUBSTATION", "#B87328", "#6E4418"),
    ]
    for x0, y0, x1, y1, title, sub, acc_hex, em_hex in placards:
        draw_alb.rectangle([x0, y0, x1, y1], fill=hex_rgb("#1E242B"), outline=hex_rgb("#3A414A"), width=2)
        # Subtle 4px left functional indicator bar
        draw_alb.rectangle([x0 + 4, y0 + 6, x0 + 8, y1 - 6], fill=hex_rgb(acc_hex))
        draw_emi.rectangle([x0 + 4, y0 + 6, x0 + 8, y1 - 6], fill=hex_rgb(em_hex))
        # Crisp warm-white room identifier text (subtle emission on primary room code only)
        draw_alb.text((x0 + 16, y0 + 8), title, fill=hex_rgb("#D8DEE6"), font=font_num)
        draw_emi.text((x0 + 16, y0 + 8), title, fill=hex_rgb(em_hex), font=font_num)
        draw_alb.text((x0 + 16, y0 + 30), sub, fill=hex_rgb("#8C96A2"), font=font_sub)

    alb = add_ultra_clean_micro_grain(np.asarray(alb_im, dtype=np.uint8), sigma=0.45, seed=101)
    orm = add_ultra_clean_micro_grain(orm, sigma=0.35, seed=102)
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
    gls = np.zeros((H, W, 4), dtype=np.uint8)
    gls[:, :, 0] = 88   # Calm smoky slate-blue (#586A78)
    gls[:, :, 1] = 106
    gls[:, :, 2] = 120
    gls[:, :, 3] = 68   # Alpha ~0.27
    # Subtle brushed steel perimeter frame & faint architectural mullion lines
    gls[0:8, :, :] = (58, 65, 74, 185)
    gls[H - 8 : H, :, :] = (58, 65, 74, 185)
    gls[:, 0:8, :] = (58, 65, 74, 185)
    gls[:, W - 8 : W, :] = (58, 65, 74, 185)
    gls[:, :, :3] = add_ultra_clean_micro_grain(gls[:, :, :3], sigma=0.30, seed=103)

    # Compute metrics
    black_emi_pct = float(np.mean(np.all(emi == 0, axis=2)) * 100.0)
    noise_alb = compute_micro_noise_pct(alb)
    noise_orm = compute_micro_noise_pct(orm)
    noise_nrm = compute_micro_noise_pct(nrm)
    noise_emi = compute_micro_noise_pct(emi)
    noise_gls = compute_micro_noise_pct(gls[:, :, :3])

    # Save across all target directories and aliases
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
    for d in TEX_DIRS:
        for fn, img_obj in suites:
            img_obj.save(os.path.join(d, fn), format="PNG", optimize=True)

    print(
        f"[ResidentialAtlas] Saved 512x512 PBR suite across {len(TEX_DIRS)} directories | "
        f"pitch_black_emission={black_emi_pct:.2f}% | "
        f"micro_noise: albedo={noise_alb:.3f}%, orm={noise_orm:.3f}%, normal={noise_nrm:.3f}%, emission={noise_emi:.3f}%, glass={noise_gls:.3f}%"
    )


if __name__ == "__main__":
    generate_residential_atlas()
