from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "contact_sheet.png"
FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
TILE_WIDTH = 480
IMAGE_HEIGHT = 680
LABEL_HEIGHT = 40

PANELS = [
    ("OLD BASELINE", ROOT / "output/skill-ab-test/baseline-arm/final.png"),
    ("PRIOR SKILL", ROOT / "output/skill-ab-test/skill-arm/final.png"),
    (
        "NEW: TSUNDERE CARE",
        ROOT / "output/moe-response-review-v1/ko_tsundere_nekomimi_maid/render_aesthetic_contract.png",
    ),
    (
        "NEW: GAP GUARD",
        ROOT / "output/moe-response-review-v1/ko_gap_moe_guard/render_aesthetic_contract.png",
    ),
    (
        "NEW: NEKOMIMI REFLEX",
        ROOT / "output/moe-response-review-v1/ko_nekomimi_barista/render_aesthetic_contract.png",
    ),
    (
        "NEW: PRIVATE JOY",
        ROOT / "output/moe-response-review-v1/ja_generic_private_joy/render_aesthetic_contract.png",
    ),
]


font = ImageFont.truetype(str(FONT_PATH), 26)
sheet = Image.new("RGB", (TILE_WIDTH * 3, (IMAGE_HEIGHT + LABEL_HEIGHT) * 2), "black")

for index, (label, path) in enumerate(PANELS):
    with Image.open(path) as source:
        fitted = ImageOps.contain(source.convert("RGB"), (TILE_WIDTH, IMAGE_HEIGHT))
    tile = Image.new("RGB", (TILE_WIDTH, IMAGE_HEIGHT + LABEL_HEIGHT), "black")
    tile.paste(fitted, ((TILE_WIDTH - fitted.width) // 2, LABEL_HEIGHT))
    draw = ImageDraw.Draw(tile)
    bounds = draw.textbbox((0, 0), label, font=font)
    draw.text(((TILE_WIDTH - (bounds[2] - bounds[0])) / 2, 6), label, font=font, fill="white")
    x = (index % 3) * TILE_WIDTH
    y = (index // 3) * (IMAGE_HEIGHT + LABEL_HEIGHT)
    sheet.paste(tile, (x, y))

sheet.save(OUT, format="PNG", optimize=True)
