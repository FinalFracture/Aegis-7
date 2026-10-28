#!/usr/bin/env python3
"""
Generates the High-Craft Architectural PBR Texture Suite (1024x1024)
for the Preface 2-Story Residential Sector (`preface_playable_area.tscn` / `preface_residential_sector.glb`)
per Jared's [t11u] directive:
  - ZERO visual storytelling decals, ZERO pry marks, ZERO scorch rings, ZERO skid trails, ZERO ghost stencils.
  - Rich, tactile, layered architectural PBR materials with crisp normal relief, AO, and metallic/roughness contrast:
    1. `UV_WALL_APT` (`u:0.02..0.48, v:0.02..0.25`, `x:0..512, y:0..268`):
       Warm Architectural Acoustic Wood-Slat & Brushed Satin Titanium Dado Wall Paneling —
       fluted vertical walnut/oak acoustic slats over dark charcoal felt backing in the upper zone,
       anodized champagne-steel chair rail, and ribbed satin titanium wainscot panels below.
    2. `UV_WALL_ATRIUM` (`u:0.52..0.98, v:0.02..0.24`, `x:512..1024, y:0..260`):
       Layered Aerospace Composite Cladding with Anodized Ribbing & Brushed Steel Reveal Channels —
       satin warm titanium-alabaster upper panels with recessed dark gunmetal shadow-gap reveals,
       horizontal stiffening ribs, CNC corner fasteners, and a dark brushed-steel lower wainscot.
    3. `UV_FLOOR_SLATE` (`u:0.52..0.98, v:0.26..0.48`, `x:512..1024, y:260..512`):
       Honed Basalt-Slate Terrazzo Decking with Machined Brass/Steel Divider Inlays —
       staggered large-format honed terrazzo slabs (`#4A525C`..`#58626E`) with multi-scale mineral aggregate,
       crisp beveled grout joints (`roughness 0.84`), polished traffic sheen (`roughness 0.28`), and metallic inlay strips.
    4. `UV_WOOD_WALNUT` (`u:0.02..0.23, v:0.28..0.48`, `x:0..256, y:268..512`):
       Staggered Finger-Jointed Teak/Walnut Butcher-Block & Architectural Millwork (`roughness 0.30..0.42`).
    5. `UV_FABRIC_SLATE` (`u:0.26..0.48, v:0.28..0.48`, `x:256..512, y:268..512`):
       Quilted Herringbone Technical Upholstery (`#3E4E60`..`#4E6074`) with stitched cushion loft normals.
    6. `UV_STEEL_TRIM` (`u:0.02..0.48, v:0.52..0.70`, `x:0..512, y:512..740`):
       Anisotropic Brushed Gunmetal & Machined Titanium Structural Steel (`metallic 0.84, roughness 0.28`).
    7. `UV_WORKBENCH_TOP` (`u:0.755..0.995, v:0.505..0.635`, `x:768..1024, y:512..652`):
       Clean Precision Engineering Butcher-Block with Recessed Dark Anodized ESD Mat & Brass Measurement Rule.
    8. `UV_WORKBENCH_PEGBOARD` (`u:0.512..0.748, v:0.638..0.720`, `x:512..768, y:648..740`):
       Clean Anodized Dark-Steel Perforated Tool Pegboard with Machined Perimeter Frame.
    9. `UV_FLOOR_SKID_TRAIL` / `UV_SUBSTATION_HEX_FLOOR` (`u:0.755..0.995, v:0.640..0.720`, `x:768..1024, y:652..740`):
       Clean Industrial Hex-Grid Grated Utility Decking (`metallic 0.80, roughness 0.30`) for Room 1B service bay.
   10. `UV_PLACARD_201..1B` (`x:512..1024, y:780..1024`):
       Clean, high-craft anodized architectural door plates (`APT 201`, `APT 202`, `RM 1A`, `RM 1B`).
"""
import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TEX_DIR = "/workspace/game-project/godot/assets/textures"
os.makedirs(TEX_DIR, exist_ok=True)


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
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, sigma, size=arr.shape)
    return np.clip(np.round(arr.astype(np.float32) + noise), 0, 255).astype(np.uint8)


def compute_micro_noise_pct(arr: np.ndarray) -> float:
    im = Image.fromarray(arr)
    blur = np.asarray(im.filter(ImageFilter.BoxBlur(1)), dtype=np.float32)
    diff = np.abs(arr.astype(np.float32) - blur)
    return float(np.mean(diff) / 255.0 * 100.0)


def generate_residential_atlas():
    W, H = 1024, 1024
    alb = np.zeros((H, W, 3), dtype=np.uint8)
    orm = np.zeros((H, W, 3), dtype=np.uint8)  # R=AO, G=Roughness, B=Metallic
    emi = np.zeros((H, W, 3), dtype=np.uint8)  # 97%+ pitch black #000000
    hgt = np.full((H, W), 128.0, dtype=np.float32)

    # --------------------------------------------------------------------------
    # 1. `UV_WALL_APT` (`x: 0..512, y: 0..268`) — Warm Architectural Acoustic Wood-Slat
    #    & Brushed Satin Titanium Dado Wall Paneling
    # --------------------------------------------------------------------------
    # Upper cornice trim (y: 0..20) in brushed champagne-titanium
    alb[0:20, 0:512] = (118, 124, 132)
    orm[0:20, 0:512] = (242, int(0.32 * 255), int(0.68 * 255))
    hgt[0:20, 0:512] = 142.0
    # Upper main zone (y: 20..176): Warm Titanium-Alabaster architectural panels with
    # subtle vertical fluted relief & warm wood-slat accent pilasters
    yy_apt, xx_apt = np.mgrid[20:176, 0:512]
    flute_wave = np.sin(xx_apt * (2.0 * math.pi / 16.0))
    alb[20:176, 0:512, 0] = np.clip(154.0 + 6.0 * flute_wave, 0, 255).astype(np.uint8)
    alb[20:176, 0:512, 1] = np.clip(158.0 + 6.0 * flute_wave, 0, 255).astype(np.uint8)
    alb[20:176, 0:512, 2] = np.clip(164.0 + 5.0 * flute_wave, 0, 255).astype(np.uint8)
    orm[20:176, 0:512, 0] = np.clip(236.0 + 14.0 * flute_wave, 200, 252).astype(np.uint8)
    orm[20:176, 0:512, 1] = np.clip((0.44 - 0.06 * flute_wave) * 255.0, 70, 140).astype(np.uint8)
    orm[20:176, 0:512, 2] = int(0.14 * 255)
    hgt[20:176, 0:512] = 132.0 + 7.5 * flute_wave

    # Architectural warm acoustic wood-slat feature inlay band (y: 44..152) with vertical slats every 12px
    for sx in range(0, 512, 12):
        # Dark acoustic felt backing groove (3px)
        alb[44:152, sx : sx + 3] = (46, 48, 54)
        orm[44:152, sx : sx + 3] = (178, int(0.82 * 255), int(0.02 * 255))
        hgt[44:152, sx : sx + 3] = 108.0
        # Warm honey-walnut beveled slat (9px)
        slat_tone = int(4.0 * math.sin(sx * 0.35))
        alb[44:152, sx + 3 : sx + 12] = (146 + slat_tone, 114 + slat_tone, 84 + slat_tone)
        orm[44:152, sx + 3 : sx + 12] = (246, int(0.34 * 255), int(0.06 * 255))
        hgt[44:152, sx + 3 : sx + 12] = 144.0

    # Anodized champagne-bronze chair rail (y: 176..192)
    alb[176:192, 0:512] = (142, 126, 104)
    orm[176:192, 0:512] = (248, int(0.26 * 255), int(0.78 * 255))
    hgt[176:192, 0:512] = 148.0
    alb[174:176, 0:512] = (54, 58, 66)
    hgt[174:176, 0:512] = 110.0

    # Lower dado wainscot (y: 192..268): Ribbed satin gunmetal-slate panels + heavy kickplate
    alb[192:252, 0:512] = (92, 100, 110)
    orm[192:252, 0:512] = (240, int(0.36 * 255), int(0.52 * 255))
    hgt[192:252, 0:512] = 130.0
    for ry in range(202, 248, 12):
        alb[ry : ry + 3, 0:512] = (74, 82, 92)
        orm[ry : ry + 3, 0:512, 0] = 210
        hgt[ry : ry + 3, 0:512] = 116.0
    alb[252:268, 0:512] = (62, 68, 76)
    orm[252:268, 0:512] = (228, int(0.32 * 255), int(0.74 * 255))
    hgt[252:268, 0:512] = 138.0
    # Vertical architectural bay seams at 128px intervals
    for px in [0, 128, 256, 384, 509]:
        alb[0:268, px : px + 3] = (58, 64, 72)
        orm[0:268, px : px + 3, 0] = 185
        hgt[0:268, px : px + 3] = 104.0

    # --------------------------------------------------------------------------
    # 2. `UV_WALL_ATRIUM` (`x: 512..1024, y: 0..260`) — Layered Aerospace Composite
    #    Cladding with Anodized Ribbing & Brushed Steel Reveal Channels
    # --------------------------------------------------------------------------
    yy_atr, xx_atr = np.mgrid[0:260, 512:1024]
    micro_brush = 3.5 * np.sin(yy_atr * 0.85) + 2.5 * np.cos(xx_atr * 0.12)
    alb[0:200, 512:1024, 0] = np.clip(156.0 + micro_brush[0:200], 0, 255).astype(np.uint8)
    alb[0:200, 512:1024, 1] = np.clip(162.0 + micro_brush[0:200], 0, 255).astype(np.uint8)
    alb[0:200, 512:1024, 2] = np.clip(170.0 + micro_brush[0:200], 0, 255).astype(np.uint8)
    orm[0:200, 512:1024] = (246, int(0.38 * 255), int(0.22 * 255))
    hgt[0:200, 512:1024] = 136.0 + micro_brush[0:200] * 0.6

    # Horizontal structural stiffening ribs & shadow-gap reveals
    for ry in [24, 88, 152]:
        alb[ry : ry + 4, 512:1024] = (68, 76, 86)
        orm[ry : ry + 4, 512:1024] = (188, int(0.52 * 255), int(0.65 * 255))
        hgt[ry : ry + 4, 512:1024] = 106.0
        alb[ry + 4 : ry + 8, 512:1024] = (176, 182, 190)
        hgt[ry + 4 : ry + 8, 512:1024] = 144.0

    # Anodized champagne-titanium datum rail (y: 196..208) + Brushed dark-steel lower bulkhead (y: 208..260)
    alb[196:208, 512:1024] = (148, 132, 108)
    orm[196:208, 512:1024] = (248, int(0.24 * 255), int(0.82 * 255))
    hgt[196:208, 512:1024] = 148.0
    alb[208:260, 512:1024] = (84, 92, 102)
    orm[208:260, 512:1024] = (238, int(0.32 * 255), int(0.72 * 255))
    hgt[208:260, 512:1024] = 128.0
    for px in [512, 640, 768, 896, 1020]:
        alb[0:260, px : px + 4] = (62, 68, 78)
        orm[0:260, px : px + 4, 0] = 182
        hgt[0:260, px : px + 4] = 104.0

    # --------------------------------------------------------------------------
    # 3. `UV_WOOD_WALNUT` (`x: 0..256, y: 268..512`) — Staggered Finger-Jointed
    #    Teak/Walnut Butcher-Block & Architectural Millwork
    # --------------------------------------------------------------------------
    yy_w, xx_w = np.mgrid[268:512, 0:256]
    grain = 9.0 * np.sin(yy_w * 0.32 + 0.04 * xx_w) + 5.0 * np.cos(yy_w * 0.14 - 0.03 * xx_w)
    alb[268:512, 0:256, 0] = np.clip(148.0 + grain, 0, 255).astype(np.uint8)
    alb[268:512, 0:256, 1] = np.clip(112.0 + grain * 0.78, 0, 255).astype(np.uint8)
    alb[268:512, 0:256, 2] = np.clip(80.0 + grain * 0.55, 0, 255).astype(np.uint8)
    orm[268:512, 0:256, 0] = 246
    orm[268:512, 0:256, 1] = np.clip((0.34 - 0.04 * np.sin(yy_w * 0.32)) * 255.0, 64, 115).astype(np.uint8)
    orm[268:512, 0:256, 2] = int(0.05 * 255)
    hgt[268:512, 0:256] = 132.0 + grain * 0.45
    for stave_y in range(288, 508, 24):
        alb[stave_y : stave_y + 2, 0:256] = (104, 76, 52)
        orm[stave_y : stave_y + 2, 0:256, 0] = 212
        hgt[stave_y : stave_y + 2, 0:256] = 116.0

    # --------------------------------------------------------------------------
    # 4. `UV_FABRIC_SLATE` (`x: 256..512, y: 268..512`) — Quilted Herringbone Technical Upholstery
    # --------------------------------------------------------------------------
    yy_fab, xx_fab = np.mgrid[268:512, 256:512]
    weave = 6.0 * np.sin((xx_fab + yy_fab) * 0.45) * np.cos((xx_fab - yy_fab) * 0.45)
    quilt_x = np.cos((xx_fab - 256) * (2.0 * math.pi / 48.0))
    quilt_y = np.cos((yy_fab - 268) * (2.0 * math.pi / 48.0))
    loft = np.clip(1.0 - 0.25 * (quilt_x ** 2 + quilt_y ** 2), 0.5, 1.0)
    alb[268:512, 256:512, 0] = np.clip(76.0 * loft + weave, 0, 255).astype(np.uint8)
    alb[268:512, 256:512, 1] = np.clip(90.0 * loft + weave, 0, 255).astype(np.uint8)
    alb[268:512, 256:512, 2] = np.clip(108.0 * loft + weave, 0, 255).astype(np.uint8)
    orm[268:512, 256:512, 0] = np.clip(210.0 + 38.0 * loft, 195, 250).astype(np.uint8)
    orm[268:512, 256:512, 1] = int(0.64 * 255)
    orm[268:512, 256:512, 2] = int(0.04 * 255)
    hgt[268:512, 256:512] = 122.0 + 14.0 * loft + weave * 0.5

    # --------------------------------------------------------------------------
    # 5. `UV_FLOOR_SLATE` (`x: 512..1024, y: 260..512`) — Honed Basalt-Slate Terrazzo
    #    with Multi-Scale Mineral Aggregate & Machined Metallic Divider Inlays
    # --------------------------------------------------------------------------
    yy_fl, xx_fl = np.mgrid[260:512, 512:1024]
    # Subtle multi-frequency mineral stone variation
    stone_var = (
        6.5 * np.sin(xx_fl * 0.08 + yy_fl * 0.05)
        + 4.5 * np.cos(xx_fl * 0.19 - yy_fl * 0.14)
        + 3.0 * np.sin(xx_fl * 0.42 + yy_fl * 0.38)
    )
    alb[260:512, 512:1024, 0] = np.clip(88.0 + stone_var, 0, 255).astype(np.uint8)
    alb[260:512, 512:1024, 1] = np.clip(95.0 + stone_var, 0, 255).astype(np.uint8)
    alb[260:512, 512:1024, 2] = np.clip(104.0 + stone_var, 0, 255).astype(np.uint8)
    orm[260:512, 512:1024, 0] = 244
    orm[260:512, 512:1024, 1] = np.clip((0.36 - 0.05 * np.sin(xx_fl * 0.08)) * 255.0, 68, 128).astype(np.uint8)
    orm[260:512, 512:1024, 2] = int(0.16 * 255)
    hgt[260:512, 512:1024] = 132.0 + stone_var * 0.5

    # Terrazzo mineral chips (quartz, warm feldspar, dark basalt) with glossy crystal facets
    rng_fl = np.random.default_rng(314)
    for _ in range(420):
        ax = int(rng_fl.integers(516, 1018))
        ay = int(rng_fl.integers(264, 506))
        cw = int(rng_fl.integers(2, 5))
        ch = int(rng_fl.integers(2, 5))
        chip_type = int(rng_fl.integers(0, 3))
        if chip_type == 0:
            alb[ay : ay + ch, ax : ax + cw] = (128, 134, 142)  # Quartz highlight chip
            orm[ay : ay + ch, ax : ax + cw, 1] = int(0.22 * 255)
            hgt[ay : ay + ch, ax : ax + cw] = 136.0
        elif chip_type == 1:
            alb[ay : ay + ch, ax : ax + cw] = (116, 108, 98)   # Warm feldspar chip
            orm[ay : ay + ch, ax : ax + cw, 1] = int(0.26 * 255)
        else:
            alb[ay : ay + ch, ax : ax + cw] = (62, 68, 76)     # Deep basalt chip
            orm[ay : ay + ch, ax : ax + cw, 1] = int(0.42 * 255)

    # Architectural staggered slab joints & machined brass/steel inlay strips every 64px
    for fy in range(260, 512, 64):
        alb[fy : fy + 3, 512:1024] = (52, 58, 66)
        orm[fy : fy + 3, 512:1024] = (182, int(0.78 * 255), int(0.10 * 255))
        hgt[fy : fy + 3, 512:1024] = 108.0
        if fy + 4 < 512:
            alb[fy + 3 : fy + 5, 512:1024] = (132, 122, 104)  # Machined metallic divider strip
            orm[fy + 3 : fy + 5, 512:1024] = (248, int(0.22 * 255), int(0.84 * 255))
            hgt[fy + 3 : fy + 5, 512:1024] = 138.0
    for row_idx, fy in enumerate(range(260, 512, 64)):
        y_end = min(512, fy + 64)
        x_off = 32 if (row_idx % 2 == 1) else 0
        for fx in range(512 + x_off, 1024, 64):
            if fx + 3 <= 1024:
                alb[fy:y_end, fx : fx + 3] = (52, 58, 66)
                orm[fy:y_end, fx : fx + 3] = (182, int(0.78 * 255), int(0.10 * 255))
                hgt[fy:y_end, fx : fx + 3] = 108.0

    # --------------------------------------------------------------------------
    # 6. `UV_STEEL_TRIM` (`x: 0..512, y: 512..740`) — Anisotropic Brushed Gunmetal
    #    & Machined Titanium Structural Steel
    # --------------------------------------------------------------------------
    yy_st, xx_st = np.mgrid[512:740, 0:512]
    aniso = 5.5 * np.sin(yy_st * 0.65) + 3.0 * np.cos(xx_st * 0.25)
    alb[512:740, 0:512, 0] = np.clip(86.0 + aniso, 0, 255).astype(np.uint8)
    alb[512:740, 0:512, 1] = np.clip(94.0 + aniso, 0, 255).astype(np.uint8)
    alb[512:740, 0:512, 2] = np.clip(104.0 + aniso, 0, 255).astype(np.uint8)
    orm[512:740, 0:512] = (244, int(0.30 * 255), int(0.84 * 255))
    hgt[512:740, 0:512] = 132.0 + aniso * 0.5
    for sy in [568, 626, 684]:
        alb[sy : sy + 4, 0:512] = (54, 60, 68)
        orm[sy : sy + 4, 0:512, 0] = 188
        hgt[sy : sy + 4, 0:512] = 108.0
        alb[sy + 4 : sy + 7, 0:512] = (114, 122, 134)
        hgt[sy + 4 : sy + 7, 0:512] = 142.0
    for sx in [128, 256, 384]:
        alb[512:740, sx : sx + 4] = (54, 60, 68)
        orm[512:740, sx : sx + 4, 0] = 188
        hgt[512:740, sx : sx + 4] = 108.0

    # Q3 Lower-Left: Coiled Copper/Slate Wire Spool (`x: 0..256, y: 740..1024`)
    alb[740:1024, 0:256] = (66, 74, 84)
    orm[740:1024, 0:256] = (240, int(0.36 * 255), int(0.76 * 255))
    for cy in range(772, 980, 18):
        alb[cy : cy + 10, 28:228] = (168, 118, 72)
        orm[cy : cy + 10, 28:228] = (246, int(0.24 * 255), int(0.88 * 255))
        hgt[cy : cy + 10, 28:228] = 142.0

    # Q3 Lower-Right: Matte Slate Battery Cell (`x: 256..512, y: 740..1024`)
    alb[740:1024, 256:512] = (58, 66, 76)
    orm[740:1024, 256:512] = (242, int(0.40 * 255), int(0.68 * 255))
    alb[760:796, 280:488] = (92, 102, 114)
    for by in [824, 864, 904]:
        alb[by : by + 16, 324:444] = hex_rgb("#2E8B9A")
        orm[by : by + 16, 324:444] = (252, int(0.20 * 255), int(0.15 * 255))
        emi[by : by + 16, 324:444] = hex_rgb("#1E5C66")

    # --------------------------------------------------------------------------
    # 7. Q4 (`x: 512..1024, y: 512..1024`) — Planter Masonry, Clean Precision Workbench,
    #    Anodized Pegboard, Industrial Hex-Grate Decking, & Clean Architectural Door Plates
    # --------------------------------------------------------------------------
    # 7A. `UV_PLANTER_STONE = (0.52, 0.74, 0.51, 0.63)` (`x: 512..768, y: 512..648`)
    alb[512:648, 512:768] = (104, 110, 118)
    orm[512:648, 512:768] = (244, int(0.56 * 255), int(0.10 * 255))
    for py in [546, 580, 614]:
        alb[py : py + 3, 512:768] = (74, 80, 88)
        orm[py : py + 3, 512:768, 0] = 196
        hgt[py : py + 3, 512:768] = 112.0
        alb[py + 3 : py + 6, 512:768] = (124, 130, 138)
        hgt[py + 3 : py + 6, 512:768] = 140.0

    # 7B. `UV_WORKBENCH_TOP` (`x: 768..1024, y: 512..652`) — Clean Finger-Jointed Teak
    #     Butcher-Block with Recessed Dark Anodized ESD Work Mat & Brass Bezel (ZERO decals!)
    yy_wb, xx_wb = np.mgrid[512:652, 768:1024]
    wb_grain = 7.0 * np.sin(yy_wb * 0.35) + 4.0 * np.cos(xx_wb * 0.12)
    alb[512:652, 768:1024, 0] = np.clip(148.0 + wb_grain, 0, 255).astype(np.uint8)
    alb[512:652, 768:1024, 1] = np.clip(112.0 + wb_grain * 0.8, 0, 255).astype(np.uint8)
    alb[512:652, 768:1024, 2] = np.clip(80.0 + wb_grain * 0.6, 0, 255).astype(np.uint8)
    orm[512:652, 768:1024] = (246, int(0.32 * 255), int(0.06 * 255))
    hgt[512:652, 768:1024] = 136.0 + wb_grain * 0.4
    # Recessed precision anti-static ESD work mat in center of benchtop (`x: 796..996, y: 532..632`)
    alb[530:634, 794:998] = (138, 120, 92)  # Machined brass bezel frame
    orm[530:634, 794:998] = (248, int(0.24 * 255), int(0.84 * 255))
    hgt[530:634, 794:998] = 142.0
    alb[534:630, 798:994] = (46, 54, 64)    # Matte slate-teal ESD surface
    orm[534:630, 798:994] = (240, int(0.48 * 255), int(0.12 * 255))
    hgt[534:630, 798:994] = 124.0
    for gx in range(814, 990, 24):
        alb[536:628, gx : gx + 1] = (62, 74, 86)
    for gy in range(546, 626, 20):
        alb[gy : gy + 1, 800:992] = (62, 74, 86)

    # 7C. `UV_WORKBENCH_PEGBOARD` (`x: 512..768, y: 648..740`) — Clean Anodized Perforated Tool Pegboard
    alb[648:740, 512:768] = (76, 84, 94)
    orm[648:740, 512:768] = (242, int(0.34 * 255), int(0.78 * 255))
    hgt[648:740, 512:768] = 134.0
    for py in range(658, 734, 12):
        for px in range(524, 758, 14):
            alb[py : py + 4, px : px + 4] = (38, 42, 48)
            orm[py : py + 4, px : px + 4, 0] = 165
            hgt[py : py + 4, px : px + 4] = 102.0

    # 7D. `UV_FLOOR_SKID_TRAIL` / `UV_SUBSTATION_HEX_FLOOR` (`x: 768..1024, y: 652..740`) —
    #     Clean Industrial Hex-Grid / Diamond-Tread Metallic Service Grating
    alb[652:740, 768:1024] = (78, 86, 96)
    orm[652:740, 768:1024] = (240, int(0.30 * 255), int(0.82 * 255))
    hgt[652:740, 768:1024] = 132.0
    for gy in range(658, 736, 12):
        for gx in range(774, 1018, 16):
            ox = 8 if ((gy // 12) % 2 == 1) else 0
            if gx + ox + 8 < 1022:
                alb[gy : gy + 6, gx + ox : gx + ox + 8] = (52, 58, 66)
                orm[gy : gy + 6, gx + ox : gx + ox + 8, 0] = 185
                hgt[gy : gy + 6, gx + ox : gx + ox + 8] = 110.0

    # 7E. Functional Light Diffuser Swatches (`y: 740..780, x: 512..1024`)
    alb[740:780, 512:1024] = (74, 80, 88)
    orm[740:780, 512:1024] = (242, int(0.56 * 255), int(0.12 * 255))
    # Swatch 1: Warm Task (`x: 528..680, y: 744..776`)
    alb[744:776, 528:680] = hex_rgb("#F5E2C4")
    orm[744:776, 528:680] = (255, int(0.20 * 255), int(0.05 * 255))
    emi[744:776, 528:680] = hex_rgb("#C8AE8A")
    # Swatch 2: Muted Functional Cyan (`x: 696..848, y: 744..776`)
    alb[744:776, 696:848] = hex_rgb("#2E8B9A")
    orm[744:776, 696:848] = (255, int(0.20 * 255), int(0.10 * 255))
    emi[744:776, 696:848] = hex_rgb("#1E5C66")
    # Swatch 3: Muted Functional Amber (`x: 864..1008, y: 744..776`)
    alb[744:776, 864:1008] = hex_rgb("#B87328")
    orm[744:776, 864:1008] = (255, int(0.24 * 255), int(0.10 * 255))
    emi[744:776, 864:1008] = hex_rgb("#784A1A")

    # 7F. Clean Anodized Architectural Door Placards (`x: 512..1024, y: 780..1024`)
    alb[780:1024, 512:1024] = hex_rgb("#222830")
    orm[780:1024, 512:1024] = (244, int(0.32 * 255), int(0.65 * 255))

    alb_im = Image.fromarray(alb, mode="RGB")
    emi_im = Image.fromarray(emi, mode="RGB")
    draw_alb = ImageDraw.Draw(alb_im)
    draw_emi = ImageDraw.Draw(emi_im)

    font_num = load_font(30, bold=True)
    font_sub = load_font(15, bold=True)

    placards = [
        (528, 780, 760, 888, "APT 201", "LEAD TECH QUARTERS", "#2E8B9A", "#1E5C66"),
        (776, 780, 1008, 888, "APT 202", "QUARTERMASTER SUITE", "#2E8B9A", "#1E5C66"),
        (528, 904, 760, 1012, "RM 1A", "COMMUNAL LOUNGE", "#2E8B9A", "#1E5C66"),
        (776, 904, 1008, 1012, "RM 1B", "BOT SUBSTATION BAY", "#C47D2B", "#784A1A"),
    ]
    for x0, y0, x1, y1, title, sub, acc_hex, em_hex in placards:
        draw_alb.rectangle([x0, y0, x1, y1], fill=hex_rgb("#1E242C"), outline=hex_rgb("#5A6674"), width=3)
        draw_alb.rectangle([x0 + 10, y0 + 16, x0 + 18, y1 - 16], fill=hex_rgb(acc_hex))
        draw_emi.rectangle([x0 + 10, y0 + 16, x0 + 18, y1 - 16], fill=hex_rgb(em_hex))
        draw_alb.text((x0 + 30, y0 + 18), title, fill=hex_rgb("#E8EEF4"), font=font_num)
        draw_emi.text((x0 + 30, y0 + 18), title, fill=hex_rgb(em_hex), font=font_num)
        draw_alb.text((x0 + 30, y0 + 62), sub, fill=hex_rgb("#9AA6B4"), font=font_sub)

    alb = add_ultra_clean_micro_grain(np.asarray(alb_im, dtype=np.uint8), sigma=0.45, seed=101)
    orm = add_ultra_clean_micro_grain(orm, sigma=0.35, seed=102)
    emi = np.asarray(emi_im, dtype=np.uint8)

    # Tangent-space normal map from height field (stronger 5.5x relief scale so architectural grooves & slats catch light crisply!)
    gy, gx = np.gradient(hgt / 255.0 * 5.5)
    nx = -gx
    ny = -gy
    nz = np.ones_like(nx)
    nlen = np.sqrt(nx * nx + ny * ny + nz * nz)
    nrm = np.zeros((H, W, 3), dtype=np.uint8)
    nrm[:, :, 0] = np.clip((nx / nlen * 0.5 + 0.5) * 255.0, 0, 255).astype(np.uint8)
    nrm[:, :, 1] = np.clip((ny / nlen * 0.5 + 0.5) * 255.0, 0, 255).astype(np.uint8)
    nrm[:, :, 2] = np.clip((nz / nlen * 0.5 + 0.5) * 255.0, 0, 255).astype(np.uint8)

    # Architectural Tempered Glass (`residential_atrium_glass_translucent.png`, 512x512 RGBA)
    GW, GH = 512, 512
    gls = np.zeros((GH, GW, 4), dtype=np.uint8)
    gls[:, :, 0] = 96
    gls[:, :, 1] = 118
    gls[:, :, 2] = 136
    gls[:, :, 3] = 64
    gls[0:8, :, :] = (64, 72, 82, 185)
    gls[GH - 8 : GH, :, :] = (64, 72, 82, 185)
    gls[:, 0:8, :] = (64, 72, 82, 185)
    gls[:, GW - 8 : GW, :] = (64, 72, 82, 185)
    gls[:, :, :3] = add_ultra_clean_micro_grain(gls[:, :, :3], sigma=0.30, seed=103)

    black_emi_pct = float(np.mean(np.all(emi == 0, axis=2)) * 100.0)
    noise_alb = compute_micro_noise_pct(alb)
    noise_orm = compute_micro_noise_pct(orm)
    noise_nrm = compute_micro_noise_pct(nrm)

    suites = [
        ("residential_atrium_and_apartment_atlas_albedo.png", Image.fromarray(alb, "RGB")),
        ("residential_atrium_and_apartment_atlas_orm.png", Image.fromarray(orm, "RGB")),
        ("residential_atrium_and_apartment_atlas_normal.png", Image.fromarray(nrm, "RGB")),
        ("residential_atrium_and_apartment_atlas_emission.png", Image.fromarray(emi, "RGB")),
        ("residential_atrium_glass_translucent.png", Image.fromarray(gls, "RGBA")),
    ]
    for fn, img_obj in suites:
        img_obj.save(os.path.join(TEX_DIR, fn), format="PNG")

    print(
        f"[ResidentialAtlas] Saved compact 1024x1024 PBR suite to {TEX_DIR} | "
        f"pitch_black_emission={black_emi_pct:.2f}% | "
        f"micro_noise: albedo={noise_alb:.3f}%, orm={noise_orm:.3f}%, normal={noise_nrm:.3f}%"
    )


if __name__ == "__main__":
    generate_residential_atlas()
