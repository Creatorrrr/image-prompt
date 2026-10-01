"""Compare failing unrelated routing cases against the verified HEAD registry.

The runtime registry is not edited. A process-local extension-list override
loads only byte-verified pre-existing source files, while the actual routing
functions are verified to be unchanged from HEAD before comparing outcomes.
"""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from unittest import mock

ROOT = Path(__file__).resolve().parents[5]
SCRIPTS = ROOT / "skills/photo-prompt-image-generator/scripts"
sys.path.insert(0, str(SCRIPTS))
import prompt_generator as pg

NEW = {
    "photo_prompt_visual_obligations_clothing_structure.json",
    "photo_prompt_visual_obligations_textile_surface.json",
    "photo_prompt_visual_obligations_accessory_structure.json",
    "photo_prompt_visual_obligations_traditional_clothing_detail.json",
}
NAMES = {
    "positive_inner_thigh_en", "candidate_contained_affect_components",
    "positive_yandere_en", "positive_yandere_ko",
    "candidate_yandere_relation_components", "negative_yandere_expression_only",
    "negative_yandere_role_prop_only", "candidate_kuudere_relation_components",
}


def head_bytes(path):
    return subprocess.check_output(["git", "show", "HEAD:" + str(path.relative_to(ROOT))], cwd=ROOT)


def selected_functions(source):
    tree = ast.parse(source)
    wanted = {
        "load_visual_obligation_registry", "resolve_visual_profile_hits",
        "candidate_pack_auto_visual_obligation_matches",
        "candidate_pack_auto_visual_concept_matches", "candidate_pack_visual_component_match",
        "build_visual_profile_index_payload",
    }
    return {node.name: ast.dump(node, include_attributes=False)
            for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in wanted}


script = SCRIPTS / "prompt_generator.py"
assert selected_functions(script.read_text()) == selected_functions(head_bytes(script).decode())
all_names = pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES
old_names = tuple(name for name in all_names if name not in NEW)
assets = ROOT / "skills/photo-prompt-image-generator/assets"
for name in ("photo_prompt_visual_obligations.json", *old_names):
    path = assets / name
    assert path.read_bytes() == head_bytes(path), name

fixture = ROOT / "tests/fixtures/photo_prompt/visual_obligation_routing_v1.jsonl"
cases = [json.loads(line) for line in fixture.read_text().splitlines() if line.strip()]
cases = [case for case in cases if case["id"] in NAMES]
observed = {}
hashes = {}
for label, names in (("baseline_HEAD", old_names), ("integrated", all_names)):
    pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES = names
    registry = pg.load_visual_obligation_registry(assets / "photo_prompt_visual_obligations.json")
    hashes[label] = {"registry_sha256": pg.visual_profile_registry_sha256(registry), "profiles": len(registry["profiles"])}
    index = pg.build_visual_profile_index_payload(registry)
    with mock.patch.object(pg, "build_visual_profile_index_payload", return_value=index):
        observed[label] = {}
        for case in cases:
            rows = [{"source": "concept_lock", "text": case["text"], "polarity": "required", "priority": "critical", "mandatory": True}]
            hard = sorted(pg.candidate_pack_auto_visual_obligation_matches(registry, rows))
            optional = sorted(pg.candidate_pack_auto_visual_concept_matches(registry, rows))
            observed[label][case["id"]] = {"hard": hard, "optional": optional,
                "expected_hard": sorted(case["expected_profile_ids"]),
                "expected_optional": sorted(case["expected_candidate_profile_ids"])}
pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES = all_names
payload = {
    "contract_version": "clothing-adjacent-routing-baseline-comparison/v1",
    "baseline_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "baseline_source_bytes_verified": True,
    "routing_function_AST_unchanged": True,
    "registries": hashes,
    "case_count": len(cases),
    "same_outcomes": observed["baseline_HEAD"] == observed["integrated"],
    "outcomes": observed,
}
destination = Path(__file__).with_name("routing-baseline-comparison.json")
destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"same_outcomes": payload["same_outcomes"], "case_count": len(cases), "registries": hashes}))
