"""Read semantic cards, keeping full frozen source in SAMPLE.jsonl."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def card(row):
    r = row["record"]
    x = r["content"]
    if r["record_kind"] == "visual_profile":
        body = {"activation": x.get("activation"), "definition": x.get("semantics", {}).get("definition"),
            "instruction": x.get("composition_instruction"), "obligations": [
                {k: item[k] for k in ("id", "instruction", "when", "condition", "required", "optional") if k in item}
                for item in (x.get("authored_components") or {}).get("obligations", [])],
            "limits": x.get("semantics", {}).get("claim_limits"), "reject": x.get("reject_substitutes"),
            "concept": x.get("concept_candidate"), "gates": x.get("render_gates")}
    elif r["record_kind"] == "visual_bundle":
        body = {key: x.get(key) for key in ("components", "relations", "confusion_boundaries", "member_candidates", "profile_activation", "adoption")}
    elif r["record_kind"] == "relationship_concept":
        body = {key: x.get(key) for key in ("definition", "en", "ko", "required_relations", "required_evidence_roles", "applicability", "axis_requirements", "axis_exclusions")}
    else:
        body = x
    return {"n": row["number"], "id": row["candidate_id"][5:13], "kind": r["record_kind"],
        "slots": [b["slot_id"] for b in row["source_bindings"]], "meaning": body,
        "effects": r["effects"], "conditions": r["conditions"],
        "role_conditions": [{"slot": b["slot_id"], **b["conditions"]} for b in row["source_bindings"]]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("start", type=int)
    p.add_argument("end", type=int)
    p.add_argument("--brief", action="store_true")
    p.add_argument("--review-line", action="store_true")
    args = p.parse_args()
    rows = [json.loads(line) for line in (HERE / "SAMPLE.jsonl").read_text().splitlines()]
    if (HERE / "SUPPLEMENT.jsonl").exists():
        rows += [json.loads(line) for line in (HERE / "SUPPLEMENT.jsonl").read_text().splitlines()]
    for row in rows:
        if args.start <= row["number"] <= args.end:
            value = card(row)
            if args.brief:
                value.pop("role_conditions")
                if row["record_kind"] == "visual_profile":
                    value["meaning"].pop("gates")
            if args.review_line:
                x = row["record"]["content"]
                if row["record_kind"] == "visual_option":
                    value["meaning"] = {k: x[k] for k in ("en", "ko", "concept_units", "relations") if k in x}
                    contexts = x.get("contextual_usage", {}).get("contexts", [])
                    if contexts:
                        value["meaning"]["context_limits"] = [{k: v[k] for k in ("definition", "limits") if k in v} for v in contexts]
                if row["record_kind"] == "visual_profile":
                    for k in ("gates", "concept"):
                        value["meaning"].pop(k, None)
                    activation = value["meaning"].get("activation") or {}
                    value["meaning"]["activation"] = {k: v for k, v in activation.items() if k not in {"exact_terms", "project_glossary_aliases"}}
                value.pop("role_conditions", None)
                value["effects"] = {"dimensions": row["record"]["effects"]["dimensions"], "properties": [
                    p["dimension"] + ":" + p["target"] + "/" + p["property"] for p in row["record"]["effects"]["properties"]]}
            print(json.dumps(value, ensure_ascii=False))


if __name__ == "__main__":
    main()
