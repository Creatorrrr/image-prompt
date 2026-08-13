from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "concealed_affection_v6_comparison.png"
FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
TILE_WIDTH = 720
IMAGE_HEIGHT = 1040
LABEL_HEIGHT = 62

PANELS = [
    (
        "USER-PREFERRED TSUNDERE DIRECTION: FIXED-IDENTITY V3",
        ROOT / "output/moe-response-review-v1/ko_tsundere_nekomimi_maid/render_identity_control.png",
    ),
    (
        "V6 SINGLE EXPRESSION EDIT",
        ROOT / "output/moe-response-review-v1/ko_tsundere_nekomimi_maid/render_concealed_affection_v6.png",
    ),
]


font = ImageFont.truetype(str(FONT_PATH), 24)
sheet = Image.new("RGB", (TILE_WIDTH * len(PANELS), IMAGE_HEIGHT + LABEL_HEIGHT), "black")

for index, (label, path) in enumerate(PANELS):
    with Image.open(path) as source:
        fitted = ImageOps.contain(source.convert("RGB"), (TILE_WIDTH, IMAGE_HEIGHT))
    tile = Image.new("RGB", (TILE_WIDTH, IMAGE_HEIGHT + LABEL_HEIGHT), "black")
    tile.paste(fitted, ((TILE_WIDTH - fitted.width) // 2, LABEL_HEIGHT))
    draw = ImageDraw.Draw(tile)
    bounds = draw.textbbox((0, 0), label, font=font)
    draw.text(
        ((TILE_WIDTH - (bounds[2] - bounds[0])) / 2, 15),
        label,
        font=font,
        fill="white",
    )
    sheet.paste(tile, (index * TILE_WIDTH, 0))

sheet.save(OUT, format="PNG", optimize=True)
