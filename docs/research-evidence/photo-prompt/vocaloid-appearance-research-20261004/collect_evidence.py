"""Collect public source receipts for this research only; never edit runtime data."""
from __future__ import annotations

import csv
import datetime
import hashlib
import io
import json
import pathlib
import tempfile
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
STAMP = datetime.datetime.now(datetime.timezone.utc).isoformat()
CACHE = pathlib.Path(tempfile.mkdtemp(prefix="vocaloid-appearance-research-"))
with (HERE / "source-cases.tsv").open() as handle:
    CASES = list(csv.DictReader(handle, delimiter="\t"))
URLS = list(dict.fromkeys(row["url"] for row in CASES))


def acquire(item):
    number, url = item
    record = {"source_id": f"S{number:03d}", "requested_url": url, "retrieved_at_utc": STAMP}
    if "fandom.com" in url:
        return {**record, "status": "secondary_reference_only", "limitation": "Original reference uses a fan wiki; primary artwork has not been independently recovered."}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=18) as response:
            blob = response.read(12 * 1024 * 1024)
            record.update({"http_status": response.status, "resolved_url": response.url, "content_type": response.headers.get("Content-Type", ""), "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
        try:
            picture = Image.open(io.BytesIO(blob))
            picture.load()
            record.update({"status": "retrieved_image", "width": picture.width, "height": picture.height, "format": picture.format, "visual_review_status": "not_reviewed"})
            path = CACHE / (record["source_id"] + "." + (picture.format or "bin").lower())
            path.write_bytes(blob)
            record["cache_path"] = str(path)
        except Exception:
            record.update({"status": "retrieved_html", "visual_review_status": "not_reviewed", "limitation": "HTTP/page receipt alone does not verify the depicted shape."})
    except Exception as error:
        record.update({"status": "unavailable", "error": f"{type(error).__name__}: {error}"})
    return record


with ThreadPoolExecutor(max_workers=6) as pool:
    RECEIPTS = list(pool.map(acquire, enumerate(URLS, 1)))
INDEX = {row["requested_url"]: row for row in RECEIPTS}
for number, case in enumerate(CASES, 1):
    case["case_id"] = f"C{number:03d}"
    case["source_id"] = INDEX[case["url"]]["source_id"]
    case["case_status"] = "reference_seed_with_source_receipt"
    case["limitation"] = "A reference row is not an independently qualified whole-character contract; inspect each selected relation separately."

IMAGES = [row for row in RECEIPTS if row["status"] == "retrieved_image"]
font_candidates = [pathlib.Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"), pathlib.Path("/Library/Fonts/Arial Unicode.ttf")]
font = next((ImageFont.truetype(str(path), 18) for path in font_candidates if path.exists()), ImageFont.load_default())
SHEETS = []
for offset in range(0, len(IMAGES), 12):
    sheet = Image.new("RGB", (1800, 1560), "#dddddd")
    painter = ImageDraw.Draw(sheet)
    for position, receipt in enumerate(IMAGES[offset:offset + 12]):
        x, y = (position % 4) * 450, (position // 4) * 520
        picture = Image.open(receipt["cache_path"]).convert("RGBA")
        picture.thumbnail((430, 460))
        sheet.paste(picture, (x + (450 - picture.width) // 2, y + 45), picture)
        labels = [case["case_id"] + " " + case["case_label"] for case in CASES if case["source_id"] == receipt["source_id"]]
        painter.text((x + 8, y + 7), receipt["source_id"] + " " + labels[0][:32], fill="black", font=font)
    target = CACHE / f"triage-{offset // 12 + 1:02d}.jpg"
    sheet.save(target, quality=92)
    SHEETS.append({"path": str(target), "source_ids": [row["source_id"] for row in IMAGES[offset:offset + 12]], "purpose": "Triage only; resized thumbnails do not establish native-detail visibility."})

payload = {"schema_version": "vocaloid-appearance-research-receipts/v1", "runtime_artifact": False, "reference_conversation_id": "6ac1910a-eff8-83ee-9e25-7fc4df001776", "reference_recovery": "read_thread returned a 20000-character truncated preview; all 17 rendered tables were then read through the browser", "reference_case_count": len(CASES), "reference_case_groups": dict(Counter(row["group"] for row in CASES)), "unique_reference_url_count": len(URLS), "acquisition_counts": dict(Counter(row["status"] for row in RECEIPTS)), "cache_root": str(CACHE), "cases": CASES, "receipts": RECEIPTS, "triage_sheets": SHEETS}
(HERE / "SOURCE-RECEIPTS.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({key: payload[key] for key in ["reference_case_count", "unique_reference_url_count", "acquisition_counts", "cache_root"]}, ensure_ascii=False))
print(json.dumps(SHEETS, ensure_ascii=False))
