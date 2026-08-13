#!/usr/bin/env python3
"""Build neutral full-frame and face-detail sheets for the sole v9-direction render."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
TILE_WIDTH = 520
FULL_HEIGHT = 780
FACE_HEIGHT = 620
LABEL_HEIGHT = 72

PANELS = [
    (
        "IDENTITY REFERENCE",
        OUT_DIR / "reference_identity/fictional_adult_reference.jpeg",
        (0.16, 0.07, 0.84, 0.61),
    ),
    (
        "A — V3 BASELINE",
        OUT_DIR / "ko_tsundere_nekomimi_maid/render_identity_control.png",
        (0.16, 0.09, 0.84, 0.57),
    ),
    (
        "C — V8",
        OUT_DIR / "ko_tsundere_nekomimi_maid/render_peer_liking_v8.png",
        (0.16, 0.09, 0.84, 0.57),
    ),
    (
        "D — V9 DIRECTION",
        OUT_DIR / "ko_tsundere_nekomimi_maid/render_peer_liking_v9.png",
        (0.16, 0.09, 0.84, 0.57),
    ),
]


def label_tile(tile: Image.Image, label: str, font: ImageFont.FreeTypeFont) -> None:
    draw = ImageDraw.Draw(tile)
    bounds = draw.textbbox((0, 0), label, font=font)
    draw.text(
        ((TILE_WIDTH - (bounds[2] - bounds[0])) / 2, 21),
        label,
        font=font,
        fill="white",
    )


def build_full_sheet(font: ImageFont.FreeTypeFont) -> Path:
    sheet = Image.new(
        "RGB", (TILE_WIDTH * len(PANELS), FULL_HEIGHT + LABEL_HEIGHT), "black"
    )
    for index, (label, path, _) in enumerate(PANELS):
        with Image.open(path) as source:
            fitted = ImageOps.contain(source.convert("RGB"), (TILE_WIDTH, FULL_HEIGHT))
        tile = Image.new("RGB", (TILE_WIDTH, FULL_HEIGHT + LABEL_HEIGHT), "black")
        tile.paste(fitted, ((TILE_WIDTH - fitted.width) // 2, LABEL_HEIGHT))
        label_tile(tile, label, font)
        sheet.paste(tile, (index * TILE_WIDTH, 0))
    output = OUT_DIR / "peer_liking_v9_comparison.png"
    sheet.save(output, format="PNG", optimize=True)
    return output


def build_face_sheet(font: ImageFont.FreeTypeFont) -> Path:
    sheet = Image.new(
        "RGB", (TILE_WIDTH * len(PANELS), FACE_HEIGHT + LABEL_HEIGHT), "black"
    )
    for index, (label, path, relative_crop) in enumerate(PANELS):
        with Image.open(path) as source:
            source = source.convert("RGB")
            left, top, right, bottom = relative_crop
            crop = source.crop(
                (
                    round(source.width * left),
                    round(source.height * top),
                    round(source.width * right),
                    round(source.height * bottom),
                )
            )
            fitted = ImageOps.fit(
                crop,
                (TILE_WIDTH, FACE_HEIGHT),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
        tile = Image.new("RGB", (TILE_WIDTH, FACE_HEIGHT + LABEL_HEIGHT), "black")
        tile.paste(fitted, (0, LABEL_HEIGHT))
        label_tile(tile, label, font)
        sheet.paste(tile, (index * TILE_WIDTH, 0))
    output = OUT_DIR / "peer_liking_v9_face_comparison.png"
    sheet.save(output, format="PNG", optimize=True)
    return output


def main() -> None:
    font = ImageFont.truetype(str(FONT_PATH), 23)
    print(build_full_sheet(font))
    print(build_face_sheet(font))


if __name__ == "__main__":
    main()
