"""Freeze authored coverage cases after the candidate-centred pilot review."""
import collections
import hashlib
import json
from pathlib import Path
import sys
from sample import ROOT, HERE, SKILL, refs

sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_corpus as c
import photo_global_index as index

# These IDs were selected after reading complete native content, not by tag
# count or by assuming that a search hit establishes a role.
SELECTION = {
    "cand_eab72b61fbcb513b85ac2a4b8a147e43": "calendar_context: Sunday and calm, no clock time",
    "cand_d58aec2481c05d83be683b2ac3defbab": "calendar_context: Sunday plus afternoon",
    "cand_d569e3c0429c508d92cb22e48da86476": "calendar_context: Sunday plus concrete cleaning actions",
    "cand_5e117a2caddd50de98baaac38191cbfa": "light_quality: soft physical window illumination",
    "cand_e8195c29077e5735ad3b15ff2375fdc5": "light_quality negative: film halation and bloom are image effects",
    "cand_4d98100a180758dfa912d1a51d4f63ec": "light_quality: shadow transition with reflection; retain tag prerequisite",
    "cand_7a87d85822e3524097967a7b3e5c67b5": "skin_tone: local apparent skin color with declared light reference",
    "cand_1b2010c843b5557cac3d0a57cd869f28": "visual_hierarchy: primary/support/background reading order",
    "cand_e05c2ed26c475458af415295cf55b6b8": "visual_hierarchy: primary focal anchor with legible surrounding field",
}


def main():
    target = HERE / "SUPPLEMENT.jsonl"
    if target.exists():
        raise ValueError("Supplement is frozen; do not replace reviewed inputs")
    source = c.validate(c.load(SKILL / "assets"))
    frozen = [json.loads(line) for line in (HERE / "SAMPLE.jsonl").read_text().splitlines()]
    assert not set(SELECTION) & {row["candidate_id"] for row in frozen}
    bindings = collections.defaultdict(list)
    for binding in source["slot_bindings"].values():
        bindings[binding["candidate_id"]].append(binding)
    manifest = c.decode((SKILL / "assets" / c.MANIFEST_NAME).read_bytes())
    owners = {cid: module["file"] for module in manifest["modules"]
        for cid in c.decode((SKILL / "assets" / module["file"]).read_bytes()).get("candidates", {})}
    rows = []
    for number, (cid, reason) in enumerate(SELECTION.items(), len(frozen) + 1):
        record = source["candidates"][cid]
        recipe, body = index.text(record)
        rows.append({"number": number, "candidate_id": cid, "record_kind": record["record_kind"],
            "payload_owner": owners[cid], "record_sha256": c.digest(record),
            "meaning_sha256": c.digest({key: record[key] for key in ("content", "conditions", "effects")}),
            "text_recipe": recipe, "text_sha256": hashlib.sha256(body.encode()).hexdigest(),
            "selection_reasons": ["authored_coverage_" + reason],
            "source_bindings": sorted(bindings[cid], key=lambda b: b["id"]),
            "reference_ids": sorted(set(refs(record["content"]))), "record": record})
    target.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    print(json.dumps({"supplement": len(rows), "total": len(frozen) + len(rows)}))


if __name__ == "__main__":
    main()
