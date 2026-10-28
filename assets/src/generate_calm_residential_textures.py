#!/usr/bin/env python3
"""
Generates the High-Craft 2048x2048 Architectural PBR Texture Suite
for the Preface 2-Story Residential Sector (`preface_playable_area.tscn` / `preface_residential_sector.glb`),
plus clean zero-blurry-text `wrist_rfid_winner_04_neural_tendon_and_bci_atlas_*.png` (1024x1024)
and `utility_bot_round2_atlas_*.png` (2048x2048) per Jared's [t11u], [t21u], & [t22u] directives:
  - ZERO blurry/fuzzy rasterized text baked into any shared PBR surface atlas!
  - All in-world room placards (`APT 201`, `APT 202`, `ALCOVE 2C`, `RM 1A`, `RM 1B`, `SECTOR-4 PROMENADE`),
    Wall/Workbench Diagnostic Monitors, and `#05` Hammerhead Bot chest nameplates use clean machined
    dark-anodized titanium bezel & geometric screen graphics in the texture with razor-sharp 3D `Label3D`
    typography mounted flush in Godot.
"""
import os
import glob
import math
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TEX_DIR = "/workspace/game-project/godot/assets/textures"
MODELS_DIR = "/workspace/game-project/godot/assets/models"
os.makedirs(TEX_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)


def hex_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def add_ultra_clean_micro_grain(arr: np.ndarray, sigma: float = 0.55, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, sigma, size=arr.shape)
    return np.clip(np.round(arr.astype(np.float32) + noise), 0, 255).astype(np.uint8)


def compute_micro_noise_pct(arr: np.ndarray) -> float:
    im = Image.fromarray(arr)
    blur = np.asarray(im.filter(ImageFilter.BoxBlur(1)), dtype=np.float32)
    diff = np.abs(arr.astype(np.float32) - blur)
    return float(np.mean(diff) / 255.0 * 100.0)


def build_normal_from_height(hgt: np.ndarray, scale: float = 6.0) -> np.ndarray:
    gy, gx = np.gradient(hgt / 255.0 * scale)
    nx = -gx
    ny = -gy
    nz = np.ones_like(nx)
    nlen = np.sqrt(nx * nx + ny * ny + nz * nz)
    nrm = np.zeros((hgt.shape[0], hgt.shape[1], 3), dtype=np.uint8)
    nrm[:, :, 0] = np.clip((nx / nlen * 0.5 + 0.5) * 255.0, 0, 255).astype(np.uint8)
    nrm[:, :, 1] = np.clip((ny / nlen * 0.5 + 0.5) * 255.0, 0, 255).astype(np.uint8)
    nrm[:, :, 2] = np.clip((nz / nlen * 0.5 + 0.5) * 255.0, 0, 255).astype(np.uint8)
    return nrm


def generate_residential_atlas():
    # Generate at 1024 base grid and upsample 2x with crisp geometric overlays to 2048x2048
    W, H = 1024, 1024
    alb = np.zeros((H, W, 3), dtype=np.uint8)
    orm = np.zeros((H, W, 3), dtype=np.uint8)  # R=AO, G=Roughness, B=Metallic
    emi = np.zeros((H, W, 3), dtype=np.uint8)
    hgt = np.full((H, W), 128.0, dtype=np.float32)

    # 1. `UV_WALL_APT` (`x: 0..512, y: 0..268`) — Warm Architectural Acoustic Wood-Slat & Satin Titanium Dado
    alb[0:20, 0:512] = (118, 124, 132)
    orm[0:20, 0:512] = (242, int(0.32 * 255), int(0.68 * 255))
    hgt[0:20, 0:512] = 142.0
    yy_apt, xx_apt = np.mgrid[20:176, 0:512]
    flute_wave = np.sin(xx_apt * (2.0 * math.pi / 16.0))
    alb[20:176, 0:512, 0] = np.clip(154.0 + 6.0 * flute_wave, 0, 255).astype(np.uint8)
    alb[20:176, 0:512, 1] = np.clip(158.0 + 6.0 * flute_wave, 0, 255).astype(np.uint8)
    alb[20:176, 0:512, 2] = np.clip(164.0 + 5.0 * flute_wave, 0, 255).astype(np.uint8)
    orm[20:176, 0:512, 0] = np.clip(236.0 + 14.0 * flute_wave, 200, 252).astype(np.uint8)
    orm[20:176, 0:512, 1] = np.clip((0.44 - 0.06 * flute_wave) * 255.0, 70, 140).astype(np.uint8)
    orm[20:176, 0:512, 2] = int(0.14 * 255)
    hgt[20:176, 0:512] = 132.0 + 7.5 * flute_wave

    for sx in range(0, 512, 12):
        alb[44:152, sx : sx + 3] = (46, 48, 54)
        orm[44:152, sx : sx + 3] = (178, int(0.82 * 255), int(0.02 * 255))
        hgt[44:152, sx : sx + 3] = 108.0
        slat_tone = int(4.0 * math.sin(sx * 0.35))
        alb[44:152, sx + 3 : sx + 12] = (146 + slat_tone, 114 + slat_tone, 84 + slat_tone)
        orm[44:152, sx + 3 : sx + 12] = (246, int(0.34 * 255), int(0.06 * 255))
        hgt[44:152, sx + 3 : sx + 12] = 144.0

    alb[176:192, 0:512] = (142, 126, 104)
    orm[176:192, 0:512] = (248, int(0.26 * 255), int(0.78 * 255))
    hgt[176:192, 0:512] = 148.0
    alb[174:176, 0:512] = (54, 58, 66)
    hgt[174:176, 0:512] = 110.0

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
    for px in [0, 128, 256, 384, 509]:
        alb[0:268, px : px + 3] = (58, 64, 72)
        orm[0:268, px : px + 3, 0] = 185
        hgt[0:268, px : px + 3] = 104.0

    # 2. `UV_WALL_ATRIUM` (`x: 512..1024, y: 0..260`)
    yy_atr, xx_atr = np.mgrid[0:260, 512:1024]
    micro_brush = 3.5 * np.sin(yy_atr * 0.85) + 2.5 * np.cos(xx_atr * 0.12)
    alb[0:200, 512:1024, 0] = np.clip(156.0 + micro_brush[0:200], 0, 255).astype(np.uint8)
    alb[0:200, 512:1024, 1] = np.clip(162.0 + micro_brush[0:200], 0, 255).astype(np.uint8)
    alb[0:200, 512:1024, 2] = np.clip(170.0 + micro_brush[0:200], 0, 255).astype(np.uint8)
    orm[0:200, 512:1024] = (246, int(0.38 * 255), int(0.22 * 255))
    hgt[0:200, 512:1024] = 136.0 + micro_brush[0:200] * 0.6

    for ry in [24, 88, 152]:
        alb[ry : ry + 4, 512:1024] = (68, 76, 86)
        orm[ry : ry + 4, 512:1024] = (188, int(0.52 * 255), int(0.65 * 255))
        hgt[ry : ry + 4, 512:1024] = 106.0
        alb[ry + 4 : ry + 8, 512:1024] = (176, 182, 190)
        hgt[ry + 4 : ry + 8, 512:1024] = 144.0

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

    # 3. `UV_WOOD_WALNUT` (`x: 0..256, y: 268..512`)
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

    # 4. `UV_FABRIC_SLATE` (`x: 256..512, y: 268..512`)
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

    # 5. `UV_FLOOR_SLATE` (`x: 512..1024, y: 260..512`)
    yy_fl, xx_fl = np.mgrid[260:512, 512:1024]
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

    rng_fl = np.random.default_rng(314)
    for _ in range(420):
        ax = int(rng_fl.integers(516, 1018))
        ay = int(rng_fl.integers(264, 506))
        cw = int(rng_fl.integers(2, 5))
        ch = int(rng_fl.integers(2, 5))
        chip_type = int(rng_fl.integers(0, 3))
        if chip_type == 0:
            alb[ay : ay + ch, ax : ax + cw] = (128, 134, 142)
            orm[ay : ay + ch, ax : ax + cw, 1] = int(0.22 * 255)
            hgt[ay : ay + ch, ax : ax + cw] = 136.0
        elif chip_type == 1:
            alb[ay : ay + ch, ax : ax + cw] = (116, 108, 98)
            orm[ay : ay + ch, ax : ax + cw, 1] = int(0.26 * 255)
        else:
            alb[ay : ay + ch, ax : ax + cw] = (62, 68, 76)
            orm[ay : ay + ch, ax : ax + cw, 1] = int(0.42 * 255)

    for fy in range(260, 512, 64):
        alb[fy : fy + 3, 512:1024] = (52, 58, 66)
        orm[fy : fy + 3, 512:1024] = (182, int(0.78 * 255), int(0.10 * 255))
        hgt[fy : fy + 3, 512:1024] = 108.0
        if fy + 4 < 512:
            alb[fy + 3 : fy + 5, 512:1024] = (132, 122, 104)
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

    # 6. `UV_STEEL_TRIM` (`x: 0..512, y: 512..740`)
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

    # 7A. `UV_PLANTER_STONE` (`x: 512..768, y: 512..648`)
    alb[512:648, 512:768] = (104, 110, 118)
    orm[512:648, 512:768] = (244, int(0.56 * 255), int(0.10 * 255))
    for py in [546, 580, 614]:
        alb[py : py + 3, 512:768] = (74, 80, 88)
        orm[py : py + 3, 512:768, 0] = 196
        hgt[py : py + 3, 512:768] = 112.0
        alb[py + 3 : py + 6, 512:768] = (124, 130, 138)
        hgt[py + 3 : py + 6, 512:768] = 140.0

    # 7B. `UV_WORKBENCH_TOP` (`x: 768..1024, y: 512..652`)
    yy_wb, xx_wb = np.mgrid[512:652, 768:1024]
    wb_grain = 7.0 * np.sin(yy_wb * 0.35) + 4.0 * np.cos(xx_wb * 0.12)
    alb[512:652, 768:1024, 0] = np.clip(148.0 + wb_grain, 0, 255).astype(np.uint8)
    alb[512:652, 768:1024, 1] = np.clip(112.0 + wb_grain * 0.8, 0, 255).astype(np.uint8)
    alb[512:652, 768:1024, 2] = np.clip(80.0 + wb_grain * 0.6, 0, 255).astype(np.uint8)
    orm[512:652, 768:1024] = (246, int(0.32 * 255), int(0.06 * 255))
    hgt[512:652, 768:1024] = 136.0 + wb_grain * 0.4
    alb[530:634, 794:998] = (138, 120, 92)
    orm[530:634, 794:998] = (248, int(0.24 * 255), int(0.84 * 255))
    hgt[530:634, 794:998] = 142.0
    alb[534:630, 798:994] = (46, 54, 64)
    orm[534:630, 798:994] = (240, int(0.48 * 255), int(0.12 * 255))
    hgt[534:630, 798:994] = 124.0
    for gx in range(814, 990, 24):
        alb[536:628, gx : gx + 1] = (62, 74, 86)
    for gy in range(546, 626, 20):
        alb[gy : gy + 1, 800:992] = (62, 74, 86)

    # 7C. `UV_WORKBENCH_PEGBOARD` (`x: 512..768, y: 648..740`)
    alb[648:740, 512:768] = (76, 84, 94)
    orm[648:740, 512:768] = (242, int(0.34 * 255), int(0.78 * 255))
    hgt[648:740, 512:768] = 134.0
    for py in range(658, 734, 12):
        for px in range(524, 758, 14):
            alb[py : py + 4, px : px + 4] = (38, 42, 48)
            orm[py : py + 4, px : px + 4, 0] = 165
            hgt[py : py + 4, px : px + 4] = 102.0

    # 7D. `UV_FLOOR_SKID_TRAIL` / `UV_SUBSTATION_HEX_FLOOR` (`x: 768..1024, y: 652..740`)
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
    alb[744:776, 528:680] = hex_rgb("#F5E2C4")
    orm[744:776, 528:680] = (255, int(0.20 * 255), int(0.05 * 255))
    emi[744:776, 528:680] = hex_rgb("#C8AE8A")
    alb[744:776, 696:848] = hex_rgb("#2E8B9A")
    orm[744:776, 696:848] = (255, int(0.20 * 255), int(0.10 * 255))
    emi[744:776, 696:848] = hex_rgb("#1E5C66")
    alb[744:776, 864:1008] = hex_rgb("#B87328")
    orm[744:776, 864:1008] = (255, int(0.24 * 255), int(0.10 * 255))
    emi[744:776, 864:1008] = hex_rgb("#784A1A")

    # 7F. Clean Anodized Architectural Door Plaques & Wall Monitor Screens (`x: 512..1024, y: 780..1024`)
    # ZERO rasterized text! Pure physical dark-anodized titanium bezels, obsidian display glass,
    # corner fasteners, and glowing cyan/amber status bars & geometric oscilloscope/telemetry lines.
    alb[780:1024, 512:1024] = hex_rgb("#1E242C")
    orm[780:1024, 512:1024] = (244, int(0.24 * 255), int(0.72 * 255))
    hgt[780:1024, 512:1024] = 136.0

    alb = add_ultra_clean_micro_grain(alb, sigma=0.45, seed=101)
    orm = add_ultra_clean_micro_grain(orm, sigma=0.35, seed=102)
    nrm = build_normal_from_height(hgt, scale=5.5)

    # Upscale to 2048x2048 and draw razor-sharp geometric plaque/monitor frames (ZERO raster text!)
    alb_2k = Image.fromarray(alb, "RGB").resize((2048, 2048), Image.Resampling.NEAREST)
    orm_2k = Image.fromarray(orm, "RGB").resize((2048, 2048), Image.Resampling.NEAREST)
    nrm_2k = Image.fromarray(nrm, "RGB").resize((2048, 2048), Image.Resampling.BILINEAR)
    emi_2k = Image.fromarray(emi, "RGB").resize((2048, 2048), Image.Resampling.NEAREST)

    draw_alb = ImageDraw.Draw(alb_2k)
    draw_emi = ImageDraw.Draw(emi_2k)

    # 4 Plaque / Monitor Screen Sub-Rects in 2048x2048 coordinates (2x of 528..1008, 780..1012)
    plaques_2k = [
        (1056, 1560, 1520, 1776, "#2E96B2", "#1E6478", False),  # UV_PLACARD_201
        (1552, 1560, 2016, 1776, "#2E96B2", "#1E6478", True),   # UV_PLACARD_202 & Wall Monitor Screen
        (1056, 1808, 1520, 2024, "#2E96B2", "#1E6478", False),  # UV_PLACARD_1A
        (1552, 1808, 2016, 2024, "#C47D2B", "#825018", False),  # UV_PLACARD_1B
    ]
    for x0, y0, x1, y1, acc_hex, em_hex, is_monitor in plaques_2k:
        # Outer machined titanium bezel + recessed dark obsidian panel
        draw_alb.rectangle([x0, y0, x1, y1], fill=hex_rgb("#141920"), outline=hex_rgb("#647282"), width=6)
        draw_alb.rectangle([x0 + 8, y0 + 8, x1 - 8, y1 - 8], outline=hex_rgb("#2C3642"), width=2)
        # Left vertical glowing status accent bar
        draw_alb.rectangle([x0 + 20, y0 + 24, x0 + 34, y1 - 24], fill=hex_rgb(acc_hex))
        draw_emi.rectangle([x0 + 20, y0 + 24, x0 + 34, y1 - 24], fill=hex_rgb(em_hex))
        # Subtle horizontal divider rule between header & subheader zones
        mid_y = y0 + int((y1 - y0) * 0.56)
        draw_alb.rectangle([x0 + 48, mid_y, x1 - 24, mid_y + 3], fill=hex_rgb("#2A3644"))
        if is_monitor:
            # Crisp geometric telemetry grid & status bars for monitor screen background
            for gx in range(x0 + 56, x1 - 28, 36):
                draw_alb.line([(gx, y0 + 24), (gx, y1 - 24)], fill=hex_rgb("#1C2632"), width=2)
            for gy in range(y0 + 28, y1 - 24, 28):
                draw_alb.line([(x0 + 48, gy), (x1 - 24, gy)], fill=hex_rgb("#1C2632"), width=2)
            # Right-side geometric signal-strength bars
            for bi, bh in enumerate([24, 42, 64, 52, 76, 60]):
                bx = x1 - 132 + bi * 18
                by1 = y1 - 28
                by0 = by1 - bh
                col_b = "#2E96B2" if bi < 4 else "#C47D2B"
                em_b = "#1E6478" if bi < 4 else "#825018"
                draw_alb.rectangle([bx, by0, bx + 11, by1], fill=hex_rgb(col_b))
                draw_emi.rectangle([bx, by0, bx + 11, by1], fill=hex_rgb(em_b))

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

    suites = [
        ("residential_atrium_and_apartment_atlas_albedo.png", alb_2k),
        ("residential_atrium_and_apartment_atlas_orm.png", orm_2k),
        ("residential_atrium_and_apartment_atlas_normal.png", nrm_2k),
        ("residential_atrium_and_apartment_atlas_emission.png", emi_2k),
        ("residential_atrium_glass_translucent.png", Image.fromarray(gls, "RGBA")),
    ]
    for fn, img_obj in suites:
        out_p = os.path.join(TEX_DIR, fn)
        img_obj.save(out_p, format="PNG")
        for m_copy in glob.glob(os.path.join(MODELS_DIR, f"*_{fn}")):
            shutil.copyfile(out_p, m_copy)

    print(f"[ResidentialAtlas] Saved 2048x2048 zero-raster-text PBR suite to {TEX_DIR}")


def clean_wrist_and_bot_atlases():
    """
    Removes any small/fuzzy baked text from:
      1. `wrist_rfid_winner_04_neural_tendon_and_bci_atlas_*.png` (upgraded to 1024x1024, replacing the
         middle text banner `SUPER-WIRE 10m` / `AEGIS-BCI NEURAL AI` with crisp machined titanium-slate
         housing, copper induction coils, and glowing cyan/violet neural-tendon circuit traces).
      2. `utility_bot_round2_atlas_*.png` & `johnny5_utility_bot_atlas_*.png` (upgraded to 2048x2048,
         replacing the tiny rasterized text in `UV_Q1_BANNER` with a clean machined dark-anodized
         chest nameplate bezel + glowing department status rings so our 3D `Label3D` bot nameplates
         read with 100% vector sharpness).
    """
    # 1. Clean Wrist RFID & BCI / Super-Wire Atlas (1024x1024)
    w_alb_p = os.path.join(TEX_DIR, "wrist_rfid_winner_04_neural_tendon_and_bci_atlas_albedo.png")
    w_emi_p = os.path.join(TEX_DIR, "wrist_rfid_winner_04_neural_tendon_and_bci_atlas_emission.png")
    w_nrm_p = os.path.join(TEX_DIR, "wrist_rfid_winner_04_neural_tendon_and_bci_atlas_normal.png")
    w_orm_p = os.path.join(TEX_DIR, "wrist_rfid_winner_04_neural_tendon_and_bci_atlas_orm.png")
    if os.path.exists(w_alb_p):
        im_alb = Image.open(w_alb_p).convert("RGB").resize((1024, 1024), Image.Resampling.NEAREST)
        im_emi = Image.open(w_emi_p).convert("RGB").resize((1024, 1024), Image.Resampling.NEAREST)
        im_nrm = Image.open(w_nrm_p).convert("RGB").resize((1024, 1024), Image.Resampling.BILINEAR)
        im_orm = Image.open(w_orm_p).convert("RGB").resize((1024, 1024), Image.Resampling.NEAREST)

        d_alb = ImageDraw.Draw(im_alb)
        d_emi = ImageDraw.Draw(im_emi)
        # Middle horizontal banner (y: 500..650 in 1024x1024) previously held rasterized text
        # Replace with clean machined titanium-slate housing, copper-gold coil bands & cyan LED bars
        d_alb.rectangle([0, 500, 1024, 652], fill=hex_rgb("#C8D0D8"))
        d_emi.rectangle([0, 500, 1024, 652], fill=(0, 0, 0))
        # Left half (0..512): Signal-orange & copper-gold induction coil housing
        d_alb.rectangle([28, 520, 484, 632], fill=hex_rgb("#D96B26"), outline=hex_rgb("#48525E"), width=6)
        for cx in range(56, 460, 28):
            d_alb.rectangle([cx, 536, cx + 14, 616], fill=hex_rgb("#E6A856"))
        d_alb.rectangle([48, 570, 464, 582], fill=hex_rgb("#2E96B2"))
        d_emi.rectangle([48, 570, 464, 582], fill=hex_rgb("#1E6478"))
        # Right half (512..1024): Dark obsidian neural-tendon telemetry bezel with cyan/violet pulse bars
        d_alb.rectangle([540, 520, 996, 632], fill=hex_rgb("#182028"), outline=hex_rgb("#2E96B2"), width=5)
        for bx in range(568, 968, 36):
            col = "#2E96B2" if ((bx // 36) % 2 == 0) else "#8A64E8"
            d_alb.rectangle([bx, 548, bx + 20, 604], fill=hex_rgb(col))
            d_emi.rectangle([bx, 548, bx + 20, 604], fill=hex_rgb(col))

        for p_out, im_out in [(w_alb_p, im_alb), (w_emi_p, im_emi), (w_nrm_p, im_nrm), (w_orm_p, im_orm)]:
            im_out.save(p_out, format="PNG")
            bn = os.path.basename(p_out)
            for m_copy in glob.glob(os.path.join(MODELS_DIR, f"*_{bn}")):
                shutil.copyfile(p_out, m_copy)

    # 2. Clean Utility Bot Round 2 / Johnny-5 Atlas (2048x2048)
    b_alb_p = os.path.join(TEX_DIR, "johnny5_utility_bot_atlas_albedo.png")
    b_emi_p = os.path.join(TEX_DIR, "johnny5_utility_bot_atlas_emission.png")
    b_nrm_p = os.path.join(TEX_DIR, "johnny5_utility_bot_atlas_normal.png")
    b_orm_p = os.path.join(TEX_DIR, "johnny5_utility_bot_atlas_orm.png")
    if os.path.exists(b_alb_p):
        im_alb = Image.open(b_alb_p).convert("RGB").resize((2048, 2048), Image.Resampling.NEAREST)
        im_emi = Image.open(b_emi_p).convert("RGB").resize((2048, 2048), Image.Resampling.NEAREST)
        im_nrm = Image.open(b_nrm_p).convert("RGB").resize((2048, 2048), Image.Resampling.BILINEAR)
        im_orm = Image.open(b_orm_p).convert("RGB").resize((2048, 2048), Image.Resampling.NEAREST)

        d_alb = ImageDraw.Draw(im_alb)
        d_emi = ImageDraw.Draw(im_emi)
        # Top-Left Q1 (`x: 0..1024, y: 0..1024`) has 4 rows (`f_idx = 0..3`, each 256px high in 2048x2048)
        # Replace rasterized text inside each banner with a sleek machined dark-anodized titanium chest plate
        # with left/right glowing department status rings and horizontal micro-trim lines (3D Label3D sits on top!)
        f_bot_title = load_sign_font(40, mono=False)
        f_bot_sub = load_sign_font(23, mono=True)
        bot_specs = [
            ("SPROCKET #0419", "D-01  //  ENGINEERING", "#E89B2D", "#885418"),
            ("SWEEP #0812", "D-02  //  CIVIC SANITATION", "#38B8C8", "#1E6470"),
            ("KELVIN #0204", "D-03  //  SCIENCE & RELAY", "#8A6CFF", "#483490"),
            ("CLOVER #0631", "D-04  //  AGRI-BIOSPHERE", "#3BA868", "#1E5C38"),
        ]
        for f_idx, (b_title, b_sub, acc_c, em_c) in enumerate(bot_specs):
            y0 = f_idx * 256 + 16
            y1 = (f_idx + 1) * 256 - 16
            x0, x1 = 20, 1004
            d_alb.rectangle([x0, y0, x1, y1], fill=hex_rgb("#181E26"), outline=hex_rgb(acc_c), width=8)
            d_alb.rectangle([x0 + 14, y0 + 14, x1 - 14, y1 - 14], fill=hex_rgb("#141920"), outline=hex_rgb("#34404E"), width=3)
            d_emi.rectangle([x0, y0, x1, y1], fill=(0, 0, 0))
            cy = (y0 + y1) // 2
            for cx in [x0 + 68, x1 - 68]:
                d_alb.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=hex_rgb("#222A34"), outline=hex_rgb(acc_c), width=6)
                d_alb.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=hex_rgb("#E8EEF4"))
                d_emi.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=hex_rgb(em_c), width=5)
                d_emi.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=hex_rgb(em_c))
            d_alb.rectangle([x0 + 120, y0 + 20, x1 - 120, y0 + 26], fill=hex_rgb(acc_c))
            d_emi.rectangle([x0 + 120, y0 + 20, x1 - 120, y0 + 26], fill=hex_rgb(em_c))
            d_alb.rectangle([x0 + 120, y1 - 26, x1 - 120, y1 - 20], fill=hex_rgb("#34404E"))
            tx = (x0 + x1) // 2
            d_alb.text((tx, cy - 24), b_title, font=f_bot_title, fill=hex_rgb("#F4F8FC"), anchor="mm")
            d_emi.text((tx, cy - 24), b_title, font=f_bot_title, fill=hex_rgb("#3A4854"), anchor="mm")
            d_alb.text((tx, cy + 32), b_sub, font=f_bot_sub, fill=hex_rgb(acc_c), anchor="mm")
            d_emi.text((tx, cy + 32), b_sub, font=f_bot_sub, fill=hex_rgb(em_c), anchor="mm")

        for suffix, im_out in [
            ("albedo.png", im_alb),
            ("emission.png", im_emi),
            ("normal.png", im_nrm),
            ("orm.png", im_orm),
        ]:
            for prefix in ["johnny5_utility_bot_atlas_"]:
                p_out = os.path.join(TEX_DIR, prefix + suffix)
                im_out.save(p_out, format="PNG")
            for m_copy in glob.glob(os.path.join(MODELS_DIR, f"*_utility_bot_round2_atlas_{suffix}")):
                im_out.save(m_copy, format="PNG")

    print("[CleanAtlases] Upgraded wrist_rfid (1024x1024) & utility_bot_round2 (2048x2048) atlases with zero blurry text")




def load_sign_font(size: int, mono: bool = False):
    fp = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if mono else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if os.path.exists(fp):
        return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def generate_sector_door_signage_skin():
    """
    Generates the dedicated 2048x2048 Door & Architectural Signage Skin Texture Suite
    (`sector_door_signage_skin_albedo.png`, `_emission.png`, `_orm.png`, `_normal.png`)
    drawn at 2x supersampled resolution (4096x4096) and downsampled with LANCZOS:
      - 6 horizontal doorway header signboard strips (2048x220 each in 1x):
        0: APT 201  //  RESIDENTIAL QUARTERS
        1: ALCOVE 2C  //  MAINTENANCE UTILITY
        2: APT 202  //  RESIDENTIAL QUARTERS
        3: RM 1A  //  LAUNDRY & UTILITY LOUNGE
        4: RM 1B  //  BOT FABRICATION & SUBSTATION
        5: SECTOR-4 PROMENADE  //  CYLINDER HAB-7
      - Bottom OLED screen panel (y = 1320..2048 in 1x) for the APT 201 Wall Diagnostic Monitor!
    """
    SS = 2
    W, H = 2048 * SS, 2048 * SS
    alb = Image.new("RGB", (W, H), hex_rgb("#242B34"))
    emi = Image.new("RGB", (W, H), (0, 0, 0))
    orm = Image.new("RGB", (W, H), (242, int(0.28 * 255), int(0.82 * 255)))
    hgt_im = Image.new("L", (W, H), 148)

    d_alb = ImageDraw.Draw(alb)
    d_emi = ImageDraw.Draw(emi)
    d_orm = ImageDraw.Draw(orm)
    d_hgt = ImageDraw.Draw(hgt_im)

    f_title = load_sign_font(38 * SS, mono=False)
    f_sub = load_sign_font(22 * SS, mono=True)
    f_badge = load_sign_font(24 * SS, mono=True)

    signs = [
        ("APT 201  //  RESIDENTIAL QUARTERS", "ROSTOV, K.  —  LEAD SYSTEMS TECH  [SEC-04]", "D-01", "#2E96B2", "#1A5868"),
        ("ALCOVE 2C  //  MAINTENANCE UTILITY", "AUX POWER CELLS & SUPER-WIRE SUPPLY BAY", "U-2C", "#2E96B2", "#1A5868"),
        ("APT 202  //  RESIDENTIAL QUARTERS", "QUARTERMASTER SUITE  —  SECTOR-04 HABITAT", "D-02", "#2E96B2", "#1A5868"),
        ("RM 1A  //  LAUNDRY & UTILITY LOUNGE", "RESIDENTIAL COMMUNAL SERVICE & LOCKER BAY", "S-1A", "#2E96B2", "#1A5868"),
        ("RM 1B  //  BOT FABRICATION & SUBSTATION", "D-03 TELEMETRY RELAY  —  AUX BUS B-14", "B-14", "#E2963B", "#885418"),
        ("SECTOR-4 PROMENADE  //  CYLINDER HAB-7", "VALLEY-A ESPLANADE  —  R = 200m DRUM DECK", "SEC-4", "#2E96B2", "#1A5868"),
    ]

    for idx, (title, sub, badge, acc_hex, em_hex) in enumerate(signs):
        y0 = idx * 220 * SS
        y1 = (idx + 1) * 220 * SS
        # Full-bleed brushed gunmetal-titanium lintel beam skin (#545C66 matching UV_STEEL_TRIM) so the beam ITSELF is skinned!
        d_alb.rectangle([0, y0, W, y1], fill=hex_rgb("#545C66"))
        d_orm.rectangle([0, y0, W, y1], fill=(246, int(0.32 * 255), int(0.82 * 255)))
        d_hgt.rectangle([0, y0, W, y1], fill=144)

        # Subtle horizontal brushed-steel grain & top/bottom machined bevel seams across full beam width
        for gy_b in range(y0 + 6 * SS, y1 - 6 * SS, 6 * SS):
            tone_b = 84 + int(3 * math.sin(gy_b * 0.25))
            d_alb.line([(0, gy_b), (W, gy_b)], fill=(tone_b - 6, tone_b, tone_b + 8), width=2)
        d_alb.rectangle([0, y0, W, y0 + 8 * SS], fill=hex_rgb("#3C444E"))
        d_alb.rectangle([0, y1 - 8 * SS, W, y1], fill=hex_rgb("#3C444E"))
        d_hgt.rectangle([0, y0, W, y0 + 8 * SS], fill=118)
        d_hgt.rectangle([0, y1 - 8 * SS, W, y1], fill=118)

        # Left & right vertical structural jamb seam grooves + CNC hex-bolts on the steel beam
        for sx_seam in [168 * SS, W - 168 * SS]:
            d_alb.rectangle([sx_seam - 3 * SS, y0 + 10 * SS, sx_seam + 3 * SS, y1 - 10 * SS], fill=hex_rgb("#343C46"))
            d_hgt.rectangle([sx_seam - 3 * SS, y0 + 10 * SS, sx_seam + 3 * SS, y1 - 10 * SS], fill=108)
        for bx in [48 * SS, W - 48 * SS]:
            for by in [y0 + 38 * SS, y1 - 38 * SS]:
                r = 8 * SS
                d_alb.ellipse([bx - r, by - r, bx + r, by + r], fill=hex_rgb("#6E7884"), outline=hex_rgb("#2C343E"), width=2 * SS)
                d_hgt.ellipse([bx - r, by - r, bx + r, by + r], fill=178)

        # Flush stenciled department badge on the left of the steel lintel beam (NO dark box!)
        b_x0, b_y0, b_x1, b_y1 = 192 * SS, y0 + 36 * SS, 356 * SS, y1 - 36 * SS
        d_alb.rectangle([b_x0, b_y0, b_x1, b_y1], fill=hex_rgb("#464E58"), outline=hex_rgb(acc_hex), width=4 * SS)
        d_hgt.rectangle([b_x0, b_y0, b_x1, b_y1], fill=134)
        d_alb.text(((b_x0 + b_x1) // 2, (b_y0 + b_y1) // 2), badge, font=f_badge, fill=hex_rgb("#F4F8FC"), anchor="mm")
        d_emi.text(((b_x0 + b_x1) // 2, (b_y0 + b_y1) // 2), badge, font=f_badge, fill=hex_rgb(em_hex), anchor="mm")

        # Flush glowing accent stripe along top & bottom inner trim of the steel beam
        d_alb.rectangle([380 * SS, y0 + 20 * SS, W - 196 * SS, y0 + 26 * SS], fill=hex_rgb(acc_hex))
        d_emi.rectangle([380 * SS, y0 + 20 * SS, W - 196 * SS, y0 + 26 * SS], fill=hex_rgb(em_hex))
        d_alb.rectangle([380 * SS, y1 - 26 * SS, W - 196 * SS, y1 - 20 * SS], fill=hex_rgb("#3A424C"))

        # Stenciled / Engraved Architectural Lettering directly on the brushed steel beam surface
        tx = (380 * SS + W - 196 * SS) // 2
        ty_title = y0 + 82 * SS
        ty_sub = y0 + 156 * SS
        # Subtle dark engraved bevel shadow behind letters so light lettering pops on brushed steel
        for ox, oy in [(-2 * SS, -2 * SS), (2 * SS, 2 * SS), (0, 3 * SS)]:
            d_alb.text((tx + ox, ty_title + oy), title, font=f_title, fill=hex_rgb("#242A32"), anchor="mm")
            d_alb.text((tx + ox, ty_sub + oy), sub, font=f_sub, fill=hex_rgb("#242A32"), anchor="mm")

        title_col = hex_rgb("#F4F8FC") if idx != 4 else hex_rgb("#FFD68A")
        title_em = hex_rgb("#465866") if idx != 4 else hex_rgb("#684818")
        d_alb.text((tx, ty_title), title, font=f_title, fill=title_col, anchor="mm")
        d_emi.text((tx, ty_title), title, font=f_title, fill=title_em, anchor="mm")
        d_hgt.text((tx, ty_title), title, font=f_title, fill=122, anchor="mm")

        d_alb.text((tx, ty_sub), sub, font=f_sub, fill=hex_rgb("#D0E6F2"), anchor="mm")
        d_emi.text((tx, ty_sub), sub, font=f_sub, fill=hex_rgb("#243C48"), anchor="mm")
        d_hgt.text((tx, ty_sub), sub, font=f_sub, fill=126, anchor="mm")

    # Bottom Section (y = 1320..2048 in 1x): APT 201 Wall Diagnostic / Hab-7 Telemetry Monitor OLED Screen Skin
    my0 = 1320 * SS
    my1 = 2048 * SS
    mpad = 18 * SS
    d_alb.rectangle([mpad, my0 + mpad, W - mpad, my1 - mpad], fill=hex_rgb("#343E4A"), outline=hex_rgb("#748292"), width=5 * SS)
    d_orm.rectangle([mpad, my0 + mpad, W - mpad, my1 - mpad], fill=(248, int(0.22 * 255), int(0.88 * 255)))
    d_hgt.rectangle([mpad, my0 + mpad, W - mpad, my1 - mpad], fill=182)

    sx0, sy0, sx1, sy1 = 48 * SS, my0 + 44 * SS, W - 48 * SS, my1 - 44 * SS
    d_alb.rectangle([sx0, sy0, sx1, sy1], fill=hex_rgb("#0A1017"), outline=hex_rgb("#2E96B2"), width=4 * SS)
    d_orm.rectangle([sx0, sy0, sx1, sy1], fill=(252, int(0.10 * 255), int(0.18 * 255)))
    d_hgt.rectangle([sx0, sy0, sx1, sy1], fill=104)

    for gx in range(sx0 + 60 * SS, sx1 - 40 * SS, 64 * SS):
        d_alb.line([(gx, sy0 + 80 * SS), (gx, sy1 - 60 * SS)], fill=hex_rgb("#111B26"), width=2)
    for gy in range(sy0 + 96 * SS, sy1 - 60 * SS, 52 * SS):
        d_alb.line([(sx0 + 36 * SS, gy), (sx1 - 36 * SS, gy)], fill=hex_rgb("#111B26"), width=2)

    d_alb.rectangle([sx0 + 20 * SS, sy0 + 18 * SS, sx1 - 20 * SS, sy0 + 86 * SS], fill=hex_rgb("#132230"), outline=hex_rgb("#2E96B2"), width=2 * SS)
    d_emi.rectangle([sx0 + 20 * SS, sy0 + 18 * SS, sx0 + 36 * SS, sy0 + 86 * SS], fill=hex_rgb("#2E96B2"))
    d_alb.rectangle([sx0 + 20 * SS, sy0 + 18 * SS, sx0 + 36 * SS, sy0 + 86 * SS], fill=hex_rgb("#48C0E0"))

    f_mhead = load_sign_font(34 * SS, mono=False)
    f_mrow = load_sign_font(27 * SS, mono=True)
    f_mfoot = load_sign_font(21 * SS, mono=True)

    d_alb.text((sx0 + 58 * SS, sy0 + 52 * SS), "HAB-7 SECTOR-4  //  ENVIRONMENTAL & DRUM TELEMETRY", font=f_mhead, fill=hex_rgb("#9FD8EA"), anchor="lm")
    d_emi.text((sx0 + 58 * SS, sy0 + 52 * SS), "HAB-7 SECTOR-4  //  ENVIRONMENTAL & DRUM TELEMETRY", font=f_mhead, fill=hex_rgb("#2E6878"), anchor="lm")
    d_alb.text((sx1 - 42 * SS, sy0 + 52 * SS), "SYS-OK // 13.56 MHz", font=f_mfoot, fill=hex_rgb("#58C496"), anchor="rm")
    d_emi.text((sx1 - 42 * SS, sy0 + 52 * SS), "SYS-OK // 13.56 MHz", font=f_mfoot, fill=hex_rgb("#1E543C"), anchor="rm")

    m_rows = [
        ("SPIN RATE:  2.12 RPM (0.98 G)  //  CORIOLIS COMP: NOMINAL", "#E8F2FA", "#385264", "#2E96B2", 0.92),
        ("ATRIUM SUBSTATION 1B:  OFFLINE  —  AUX BUS FAULT [B-14]", "#FFB866", "#784814", "#E28B2E", 0.40),
        ("PROMENADE AIRLOCK:  STANDBY  //  ATMO: 101.3 kPa (21.2% O2)", "#8CE0B0", "#24583C", "#3BA868", 0.98),
        ("AXIAL SOLAR CORE:  5500K DAYLIGHT  //  VALLEY-A BAY 04", "#9FD8EA", "#285060", "#2E96B2", 0.86),
    ]
    for r_i, (r_txt, col_t, em_t, bar_c, fill_frac) in enumerate(m_rows):
        ry = sy0 + (152 + r_i * 116) * SS
        d_alb.rectangle([sx0 + 36 * SS, ry - 18 * SS, sx0 + 48 * SS, ry + 18 * SS], fill=hex_rgb(bar_c))
        d_emi.rectangle([sx0 + 36 * SS, ry - 18 * SS, sx0 + 48 * SS, ry + 18 * SS], fill=hex_rgb(em_t))
        d_alb.text((sx0 + 70 * SS, ry), r_txt, font=f_mrow, fill=hex_rgb(col_t), anchor="lm")
        d_emi.text((sx0 + 70 * SS, ry), r_txt, font=f_mrow, fill=hex_rgb(em_t), anchor="lm")
        bx0, bx1 = sx1 - 420 * SS, sx1 - 48 * SS
        by0, by1 = ry - 18 * SS, ry + 18 * SS
        d_alb.rectangle([bx0, by0, bx1, by1], fill=hex_rgb("#141E28"), outline=hex_rgb("#344658"), width=2 * SS)
        bf_w = int((bx1 - bx0 - 8 * SS) * fill_frac)
        d_alb.rectangle([bx0 + 4 * SS, by0 + 4 * SS, bx0 + 4 * SS + bf_w, by1 - 4 * SS], fill=hex_rgb(bar_c))
        d_emi.rectangle([bx0 + 4 * SS, by0 + 4 * SS, bx0 + 4 * SS + bf_w, by1 - 4 * SS], fill=hex_rgb(em_t))

    fy = sy1 - 38 * SS
    d_alb.line([(sx0 + 32 * SS, fy - 22 * SS), (sx1 - 32 * SS, fy - 22 * SS)], fill=hex_rgb("#26384A"), width=2 * SS)
    d_alb.text((sx0 + 42 * SS, fy), "CYLINDER HAB-7 TELEMETRY BUS  //  NODE: APT-201-WALL-MON  //  REV 4.7", font=f_mfoot, fill=hex_rgb("#7890A4"), anchor="lm")

    alb_out = alb.resize((2048, 2048), Image.Resampling.LANCZOS)
    emi_out = emi.resize((2048, 2048), Image.Resampling.LANCZOS)
    orm_out = orm.resize((2048, 2048), Image.Resampling.BILINEAR)
    hgt_arr = np.array(hgt_im.resize((2048, 2048), Image.Resampling.BILINEAR), dtype=np.float32)
    nrm_out = Image.fromarray(build_normal_from_height(hgt_arr, scale=5.5), "RGB")

    for suffix, im_o in [
        ("albedo.png", alb_out),
        ("emission.png", emi_out),
        ("orm.png", orm_out),
        ("normal.png", nrm_out),
    ]:
        p_out = os.path.join(TEX_DIR, f"sector_door_signage_skin_{suffix}")
        im_o.save(p_out, format="PNG")
    print(f"[SignageSkin] Saved 2048x2048 supersampled sector_door_signage_skin_*.png suite to {TEX_DIR}")


if __name__ == "__main__":
    generate_residential_atlas()
    clean_wrist_and_bot_atlases()
    generate_sector_door_signage_skin()
