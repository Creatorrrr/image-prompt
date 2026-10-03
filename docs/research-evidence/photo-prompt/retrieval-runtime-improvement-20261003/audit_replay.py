"""Audit unchanged frozen prose with zero optional candidate adoptions."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from unittest import mock


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--packs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.repo))
    sys.path.insert(0, str(args.repo / "skills/photo-prompt-image-generator/scripts"))
    import prompt_generator as pg
    import audit_composed_prompt as auditor
    from tests.test_photo_authorship_policy import PhotoAuthorshipPolicyTests

    rows = []
    for path in sorted(args.packs.glob("*-pack.json")):
        pack = json.loads(path.read_text())
        composed = PhotoAuthorshipPolicyTests.composed(pack)
        with mock.patch.object(pg, "cached_gemini_client", side_effect=AssertionError("offline audit forbids provider calls")):
            result = auditor.audit_composed_prompt(pack, composed)
        row = {"case": path.name, "pack_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "status": result["status"], "failures": result["failures"], "warnings": result["warnings"],
            "chosen_candidate_ids": composed["chosen_candidate_ids"],
            "prompt_unchanged": composed["prompt_en"] == pack["authorial_core"]["baseline_prompt_en"]}
        rows.append(row)
        print(path.name, row["status"], flush=True)
    assert len(rows) == 24, "both archived twelve-scene arms must be present"
    args.output.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
    if any(r["status"] != "pass" or not r["prompt_unchanged"] or r["chosen_candidate_ids"] for r in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
