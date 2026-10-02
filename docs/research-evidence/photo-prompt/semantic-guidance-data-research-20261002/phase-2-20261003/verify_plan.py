"""Check research pack consistency and local evidence contracts; no model calls."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from build_plan import OUT, ROOT, at, draft_after, read, sha, write, NEUTRAL

def main():
    snapshot = read("current-snapshot.json")
    drift = []
    for relative, expected in snapshot["protected_file_sha256"].items():
        path = ROOT / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        if actual != expected: drift.append(relative)
    sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
    import prompt_generator as pg
    from visual_profile_contracts import compile_visual_profile

    plans = read("profile-change-plan.json")["plans"]
    assert len(plans) == len({p["profile_id"] for p in plans}) == 15
    compiled = {}
    for plan in plans:
        pid = plan["profile_id"]
        before = snapshot["raw_owners"][pid]["raw_profile"]
        assert sha(before) == plan["before_raw_profile_sha256"]
        after = draft_after(before, plan["operations"])
        assert sha(after) == plan["after_raw_profile_sha256"]
        b, a = compile_visual_profile(before), compile_visual_profile(after)
        assert a["id"] == b["id"]
        assert a["required_evidence_fields"] == b["required_evidence_fields"]
        assert a["runtime_expression"] == b["runtime_expression"]
        assert [(g["id"], g["review_scale"]) for g in a["render_gates"]] == [(g["id"], g["review_scale"]) for g in b["render_gates"]]
        assert a["activation"].get("exact_terms") == b["activation"].get("exact_terms")
        assert a["activation"].get("hard_activation") == b["activation"].get("hard_activation")
        if before.get("authored_components"):
            assert a["semantics"]["component_semantics"]["required_group_ids"] == b["semantics"]["component_semantics"]["required_group_ids"]
        for field in a["required_evidence_fields"]:
            assert a["evidence_requirements"][field]["min_content_words"] == b["evidence_requirements"][field]["min_content_words"]
        compiled[pid] = a

    # These deliberately reproduce string-anchor rejection, then acceptance.
    # They do not test contextual retrieval, generated prose or image pixels.
    fixtures = [
        (pid, "visible_relation_phrase", row["en"]) for pid, row in NEUTRAL.items()
    ] + [
        ("sheer_garment_optical_layering", "layer_contrast_phrase", "underlying body contours remain partly visible beneath the readable garment fibers"),
        ("sheer_garment_optical_layering", "translucent_textile_phrase", "a garment textile layer that partially transmits the view behind it"),
    ]
    results = []
    for pid, field, phrase in fixtures:
        old = snapshot["selected_profiles"][pid]["evidence_requirements"][field]
        try:
            pg.validate_visual_intent_binding(obligation_index=0, field=field, phrase=phrase, requirement=old)
            before_result = "ACCEPTED"
        except ValueError:
            before_result = "REJECTED_BY_EXISTING_STRING_ANCHORS"
        assert before_result == "REJECTED_BY_EXISTING_STRING_ANCHORS"
        pg.validate_visual_intent_binding(obligation_index=0, field=field, phrase=phrase, requirement=compiled[pid]["evidence_requirements"][field])
        results.append({"profile_id": pid, "field": field, "phrase": phrase, "before": before_result, "draft_after": "ACCEPTED_BY_LOCAL_BINDING_CONTRACT"})

    for pid in NEUTRAL:
        requirement = compiled[pid]["evidence_requirements"]["visible_relation_phrase"]
        try:
            pg.validate_visual_intent_binding(obligation_index=0, field="visible_relation_phrase", phrase="an ordinary garment with some decorative details", requirement=requirement)
        except ValueError:
            pass
        else:
            raise AssertionError("Generic description unexpectedly accepted")

    graph_plan = read("character-scope-plan.json")
    graph = json.loads((ROOT / graph_plan["source_file"]).read_text())
    target = next(x for x in graph["character_mechanism_graph"]["concept_profiles"] if x["id"] == "kuudere")
    assert sha(target) == graph_plan["before_sha256"]
    updated = draft_after(target, graph_plan["operations"])
    assert sha(updated) == graph_plan["after_sha256"]
    assert set(updated) == set(target)
    assert all(updated[k] == target[k] for k in target if k not in {"definition", "en", "ko", "ja"})
    trial = copy.deepcopy(graph)
    trial["character_mechanism_graph"]["concept_profiles"] = [updated if x["id"] == "kuudere" else x for x in trial["character_mechanism_graph"]["concept_profiles"]]
    pg.validate_character_mechanism_graph(trial)

    known_sources = {r["id"] for r in read("source-evidence.json")["items"]}
    known_sources.update(r["id"] for r in json.loads((OUT.parent / "phase-1/sources.json").read_text())["items"])
    for plan in plans: assert set(plan["source_ids"]) <= known_sources
    pairs = [json.loads(line) for line in (OUT / "semantic-minimal-pairs.jsonl").read_text().splitlines()]
    assert len(pairs) == len({r["id"] for r in pairs}) == 14
    for row in pairs:
        assert set(row["profile_ids"]) <= set(compiled)
        assert set(row["source_ids"]) <= known_sources
        assert set(row["positive"]) == set(row["contrast"]) == {"ko", "en"}
    for path in OUT.glob("*.json"): json.loads(path.read_text())
    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not drift else "SOURCE_DRIFT_REBASE_REQUIRED",
        "protected_source_files": len(snapshot["protected_file_sha256"]),
        "changed_protected_files": drift,
        "raw_profile_plans_compiled_in_memory": len(compiled),
        "graph_schema_check": "PASS",
        "local_anchor_fixtures": results,
        "generic_anchor_negatives_rejected": len(NEUTRAL),
        "preserved_profile_gates": sum(len(r["render_gates"]) for r in compiled.values()),
        "preserved_evidence_fields": sum(len(r["required_evidence_fields"]) for r in compiled.values()),
        "development_minimal_pairs": len(pairs),
        "development_utterances": len(pairs) * 4,
        "production_changes_applied": 0,
        "embedding_calls": 0, "llm_evaluation_calls": 0, "image_generation_calls": 0,
        "unverified": ["independent language/semantic judgment", "approximate retrieval precision and recall", "full composed-prompt integration", "model moderation outcomes", "image structure preservation", "user acceptance"],
    }
    write("validation-results.json", result)
    print(json.dumps({k:v for k,v in result.items() if k not in ["local_anchor_fixtures", "unverified"]}))
    if drift: raise SystemExit(1)

if __name__ == "__main__": main()
