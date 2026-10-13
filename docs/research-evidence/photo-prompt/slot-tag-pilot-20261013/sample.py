"""Freeze a stratified native-source pilot; sampling is not semantic approval."""
from __future__ import annotations
import collections
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_corpus as c
import photo_global_index as index
import photo_runtime_sources as runtime

SEED = 2026101304
SIZE = 600


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def refs(value):
    if isinstance(value, str):
        return [value] if c.ID.fullmatch(value) or c.BINDING_ID.fullmatch(value) else []
    if isinstance(value, dict):
        return [ref for key, item in value.items() for ref in refs(key) + refs(item)]
    if isinstance(value, list):
        return [ref for item in value for ref in refs(item)]
    return []


def main():
    if (HERE / "SAMPLE.jsonl").exists():
        raise ValueError("The frozen pilot already exists; do not replace reviewed inputs")
    source = c.load(SKILL / "assets")
    c.validate(source)
    rng = random.Random(SEED)
    chosen = collections.defaultdict(set)
    bindings = collections.defaultdict(list)
    for bid, row in sorted(source["slot_bindings"].items()):
        bindings[row["candidate_id"]].append(row)
    def add(cid, reason):
        assert cid in source["candidates"]
        chosen[cid].add(reason)
    old = ROOT / "docs/research-evidence/photo-prompt/candidate-quality-random-1000-20261013/reviews.jsonl"
    previous = [json.loads(line) for line in old.read_text().splitlines()]
    prior_cases = [row for row in previous if row["slot"] in {"broad", "wrong"}]
    assert len(prior_cases) == 39
    for row in prior_cases:
        add(row["candidate_id"], "previous_" + row["slot"] + "_sample_" + str(row["sample_number"]))
    for cid, row in sorted(source["candidates"].items()):
        if row["record_kind"] in {"diagnostic", "relationship_concept"}:
            add(cid, "entire_sparse_kind")
    for role in sorted(source["slot_catalog"]):
        ids = sorted(cid for cid, rows in bindings.items() if any(row["slot_id"] == role for row in rows))
        if ids:
            add(rng.choice(ids), "persistent_role_" + role)
    # All broad-quality property refinements and the seven final carrier/cause
    # corrections are regression inputs, rather than labels for this review.
    prior = ROOT / "docs/research-evidence/photo-prompt/slot-taxonomy-revision-20261013"
    effects = json.loads((prior / "EFFECT-REFINEMENTS.json").read_text())
    for row in effects:
        add(row["candidate_id"], "previous_effect_refinement")
    corrections = json.loads((prior / "FINAL-BOUNDARY-CORRECTIONS.json").read_text())
    for row in corrections["corrections"]:
        matches = [cid for cid in source["candidates"] if cid.startswith("cand_" + row["candidate_short_id"])]
        assert len(matches) == 1
        add(matches[0], "previous_carrier_boundary")
    # Previously verified whole-pool hybrid results add discovery inputs for
    # roles with no persistent binding. They do not assign those roles.
    sparse = sorted(role for role in source["slot_catalog"]
        if not any(b["slot_id"] == role for b in source["slot_bindings"].values()))
    for case in ("human", "object"):
        traces = json.loads((prior / ("stage03-" + case + "-en-retrieval.json")).read_text())
        assert traces["corpus_sha256"] == c.digest(source)
        for role in sparse:
            ranked = traces["slot_searches"][role]["rrf"]
            if ranked:
                add(ranked[0]["document_id"], "sparse_role_discovery_" + role + "_" + case)
    # A candidate-centred random fill covers untagged profiles/bundles and
    # abstract mechanisms even when they never enter a slot's top-k.
    quotas = {"visual_profile": 100, "visual_bundle": 100, "relationship_mechanism": 40}
    for kind, count in quotas.items():
        current = sum(source["candidates"][cid]["record_kind"] == kind for cid in chosen)
        ids = sorted(cid for cid, row in source["candidates"].items() if row["record_kind"] == kind and cid not in chosen)
        for cid in rng.sample(ids, max(0, count - current)):
            add(cid, "stratified_random_" + kind)
    remaining = SIZE - len(chosen)
    assert remaining >= 0, len(chosen)
    ids = sorted(cid for cid, row in source["candidates"].items() if row["record_kind"] == "visual_option" and cid not in chosen)
    for cid in rng.sample(ids, remaining):
        add(cid, "stratified_random_visual_option")
    manifest = c.decode((SKILL / "assets" / c.MANIFEST_NAME).read_bytes())
    owners = {}
    for module in manifest["modules"]:
        for cid in c.decode((SKILL / "assets" / module["file"]).read_bytes()).get("candidates", {}):
            assert cid not in owners
            owners[cid] = module["file"]
    order = {kind: i for i, kind in enumerate(["visual_option", "visual_profile", "visual_bundle", "relationship_mechanism", "relationship_concept", "diagnostic"])}
    ids = sorted(chosen, key=lambda cid: (order[source["candidates"][cid]["record_kind"]],
        min((b["slot_id"] for b in bindings[cid]), default=""), cid))
    cards = []
    for number, cid in enumerate(ids, 1):
        row = source["candidates"][cid]
        recipe, text = index.text(row)
        cards.append({"number": number, "candidate_id": cid, "record_kind": row["record_kind"],
            "payload_owner": owners[cid], "record_sha256": c.digest(row),
            "meaning_sha256": c.digest({key: row[key] for key in ("content", "conditions", "effects")}),
            "text_recipe": recipe, "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "selection_reasons": sorted(chosen[cid]), "source_bindings": bindings[cid],
            "reference_ids": sorted(set(refs(row["content"]))), "record": row})
    (HERE / "SAMPLE.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in cards))
    write("CATALOG.json", source["slot_catalog"])
    pointer_path = runtime._pointer_directory(runtime.default_store(), SKILL, "local_current") / "CURRENT.json"
    protected = ["docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md",
        "docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md"]
    write("BASELINE.json", {"schema": "photo-slot-tag-pilot-baseline/v1", "git_head": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "corpus_sha256": c.digest(source),
        "candidate_count": len(source["candidates"]), "binding_count": len(source["slot_bindings"]),
        "catalog_sha256": c.digest(source["slot_catalog"]), "module_sha256": {
            row["file"]: sha(SKILL / "assets" / row["file"]) for row in manifest["modules"]},
        "manifest_sha256": sha(SKILL / "assets" / c.MANIFEST_NAME),
        "search_manifest_sha256": sha(SKILL / "assets/photo_candidate_search.json"),
        "runtime_pointer": c.decode(pointer_path.read_bytes()), "runtime_pointer_sha256": sha(pointer_path),
        "operating_code": runtime.code_inventory(SKILL),
        "protected_dirty_files": {name: sha(ROOT / name) for name in protected}})
    write("SAMPLE-MANIFEST.json", {"schema": "photo-slot-tag-pilot-sample/v1", "seed": SEED, "sample_size": SIZE,
        "sample_sha256": sha(HERE / "SAMPLE.jsonl"), "record_kinds": dict(collections.Counter(row["record_kind"] for row in cards)),
        "previous_broad_cases": 30, "previous_wrong_cases": 9, "entire_diagnostic_kind": 64,
        "entire_relationship_concept_kind": 3, "sparse_role_discovery_inputs": sparse,
        "persistent_role_inputs": sorted({b["slot_id"] for row in cards for b in row["source_bindings"]}),
        "tagged": sum(bool(row["source_bindings"]) for row in cards),
        "untagged": sum(not row["source_bindings"] for row in cards),
        "sampling_boundary": "Purposeful regression coverage plus stratified random fill; not a prevalence estimate or held-out quality score."})
    print(json.dumps({"count": len(cards), "kinds": dict(collections.Counter(row["record_kind"] for row in cards))}))


if __name__ == "__main__":
    main()
