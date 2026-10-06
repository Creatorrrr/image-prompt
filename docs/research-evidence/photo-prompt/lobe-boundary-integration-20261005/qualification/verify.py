#!/usr/bin/env python3
"""Read-only, standard-library verification of the relocated qualification evidence.

Run from any directory. No generation, network, Git, credentials, or file writes.
The historical compare.py is preserved unchanged as part of its sealed review.
"""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
TARGETS = {
    "visual-concept:orn_profile_gd46_three",
    "visual-concept:orn_profile_gd46_four",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition, message):
    if not condition:
        raise ValueError(message)


def differences(a, b, path=""):
    if type(a) is not type(b):
        yield {"path": path, "before": a, "after": b}
    elif isinstance(a, dict):
        for key in sorted(a.keys() | b.keys()):
            child = path + "/" + key
            if key not in a or key not in b:
                yield {"path": child, "before": a.get(key), "after": b.get(key), "key_missing": True}
            else:
                yield from differences(a[key], b[key], child)
    elif isinstance(a, list):
        if len(a) != len(b):
            yield {"path": path, "before": a, "after": b, "length_changed": True}
        else:
            for index, (old, new) in enumerate(zip(a, b)):
                yield from differences(old, new, path + "/" + str(index))
    elif a != b:
        yield {"path": path, "before": a, "after": b}


def id_list(value):
    return (isinstance(value, list) and bool(value)
            and all(isinstance(item, dict) and isinstance(item.get("id"), str) for item in value)
            and len({item["id"] for item in value}) == len(value))


def align(value):
    if isinstance(value, dict):
        return {key: align(item) for key, item in value.items()}
    if id_list(value):
        return {"ID=" + item["id"]: align(item) for item in value}
    if isinstance(value, list):
        return [align(item) for item in value]
    return value


def inventories(value, path=""):
    result = {}
    if isinstance(value, dict):
        for key, item in value.items():
            result.update(inventories(item, path + "/" + key))
    elif isinstance(value, list):
        if id_list(value):
            result[path] = [item["id"] for item in value]
            for item in value:
                result.update(inventories(item, path + "/ID=" + item["id"]))
        else:
            for index, item in enumerate(value):
                result.update(inventories(item, path + "/" + str(index)))
    return result


def main():
    qualification = read(HERE.parent / "QUALIFICATION.json")
    check(qualification["status"] == "qualified_with_disclosed_order_change", "Qualification is not finalized")
    mapping = read(HERE / "PATH-MAP.json")
    for relative, expected in qualification["files"].items():
        check(digest(ROOT / relative) == expected, "Qualification hash mismatch: " + relative)
    for original, row in mapping["files"].items():
        path = ROOT / row["repository_path"]
        check(digest(path) == row["sha256"] and path.stat().st_size == row["bytes"], "Relocation mismatch: " + original)

    for folder in ("lobe-before-independent-review", "lobe-after-independent-review"):
        manifest = HERE / folder / "inventory_manifest.json"
        check(digest(manifest) == qualification["independent_review_manifests"][folder], "Review manifest changed")
        for row in read(manifest)["files"]:
            check(digest(manifest.parent / row["path"]) == row["sha256"], "Review file changed: " + row["path"])

    for folder in ("lobed-opening-authoring", "lobed-opening-authoring-setting-adapter-01"):
        manifest = read(HERE / folder / "inventory_manifest.json")
        for name, row in manifest["support_files"].items():
            check(digest(HERE / folder / name) == row["sha256"], "Frozen support file changed")
        for case in manifest["cases"]:
            directory = case.get("artifact_directory")
            for name, row in case["artifacts"].items():
                original = str(Path(directory) / name) if directory else str(Path(mapping["source_evidence_root"]) / folder / case["case_id"] / name)
                check(digest(ROOT / mapping["files"][original]["repository_path"]) == row["sha256"], "Frozen authoring file changed")

    original = read(HERE / "lobed-opening-authoring/four_lobed_timber/authorial_core.json")
    adapter = read(HERE / "lobed-opening-authoring-setting-adapter-01/four_lobed_timber/authorial_core.json")
    check(list(differences(original, adapter)) == [{"path": "/setting", "before": "A riverside garden", "after": "a weathered timber gate at a riverside garden"}], "Adapter changed more than setting")
    adapter_change = read(HERE / "lobed-opening-authoring-setting-adapter-01/adapter_change.json")
    for name in adapter_change["unchanged"]:
        check((HERE / "lobed-opening-authoring/four_lobed_timber" / name).read_bytes() == (HERE / "lobed-opening-authoring-setting-adapter-01/four_lobed_timber" / name).read_bytes(), "Adapter ancillary input changed")
    for name in ("raw_request.txt", "baseline_prompt_en.txt"):
        check(adapter["setting"] in (HERE / "lobed-opening-authoring/four_lobed_timber" / name).read_text(), "Adapter invented setting text")
    before_commands = {row["case"]: row for row in read(HERE / "lobed-opening-before-900/COMMANDS.json")}
    check(before_commands["four_lobed_timber"]["returncode"] == 1, "Original admission failure is missing")
    check((HERE / "lobed-opening-before-900/four_lobed_timber.stderr").read_text().strip() == "Error: authorial core setting needs at least 3 concrete content words", "Original admission error changed")
    check(not (HERE / "lobed-opening-before-900/four_lobed_timber.pack.json").exists(), "Failed original case cannot have a pack")
    before_commands.update({row["case"]: row for row in read(HERE / "lobed-opening-before-900-setting-adapter-01/COMMANDS.json")})
    after_commands = {row["case"]: row for row in read(HERE / "lobed-opening-after-900/COMMANDS.json")}

    summary = read(HERE / "lobe-after-independent-review/summary.json")
    deltas = read(HERE / "lobe-after-independent-review/all-public-pack-deltas.json")
    changed_order_cases = []
    case_results = []
    for case in summary["cases"]:
        name = case["case"]
        before = read(ROOT / mapping["files"][case["before_path"]]["repository_path"])
        after = read(ROOT / mapping["files"][case["after_path"]]["repository_path"])
        for receipt, side in ((before_commands[name], "before"), (after_commands[name], "after")):
            check(receipt["returncode"] == 0 and not receipt["blocked_attempt"], "Natural command receipt failed")
            check(receipt["pack_sha256"] == case[side + "_sha256"], "Natural receipt hash differs")
        positional = list(differences(before, after))
        aligned = list(differences(align(before), align(after)))
        check(positional == deltas[name]["exact_positional_delta"], "Full positional comparison differs")
        check(aligned == deltas[name]["id_aligned_delta"], "Full ID-aligned comparison differs")
        old_lists, new_lists = inventories(before), inventories(after)
        check(old_lists.keys() == new_lists.keys(), "Candidate surfaces differ")
        changes = []
        for path, old in old_lists.items():
            new = new_lists[path]
            check(sorted(old) == sorted(new), "Candidate IDs differ: " + path)
            if old != new:
                changes.append({"path": path, "before": old, "after": new, "added_ids": [], "removed_ids": []})
        check(changes == case["order_changes"], "Recorded order effect differs")
        if changes:
            changed_order_cases.append(name)
        a, b = before[0], after[0]
        frozen_input = HERE / "lobed-opening-authoring" / name
        check(a["authorial_core"]["source_request"] == (frozen_input / "raw_request.txt").read_text(), "Natural pack request differs from frozen text")
        check(a["authorial_core"]["baseline_prompt_en"] == (frozen_input / "baseline_prompt_en.txt").read_text(), "Natural pack baseline differs from frozen text")
        visual_before, visual_after = a["visual_concept_candidates"]["candidates"], b["visual_concept_candidates"]["candidates"]
        material = "|".join([str(a["provenance"].get("seed") or ""), str(a["provenance"].get("batch_index") or 0)])
        def sort_key(item):
            canonical = json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            return hashlib.sha256(f"authorial-order|{material}|visual-concepts|{canonical}".encode()).hexdigest()
        check(sorted(visual_before, key=sort_key) == visual_before, "Original full-candidate ordering does not reproduce")
        prediction = copy.deepcopy(visual_before)
        after_by_id = {item["id"]: item for item in visual_after}
        for item in prediction:
            if item["id"] in TARGETS:
                item["opt_in_contract"]["obligation"]["reject_substitutes"] = after_by_id[item["id"]]["opt_in_contract"]["obligation"]["reject_substitutes"]
        check(sorted(prediction, key=sort_key) == visual_after, "Rejection-only content changes do not reproduce actual after ordering")
        for field in ("slots", "creative_augmentation", "semantic_clarification", "semantic_assertion_obligations", "authorial_core"):
            check(a[field] == b[field], "Preserved semantic surface changed: " + field)
        check("visual_obligations" not in a and "visual_obligations" not in b, "Unexpected active obligation section")
        case_results.append({"case": name, "positional_differences": len(positional), "id_aligned_differences": len(aligned), "exact_order_preserved": not changes})
    check(changed_order_cases == ["three_lobed_stone", "four_lobed_timber", "painted_solid_panel"], "Failed order-invariance hypothesis was not retained")
    check(summary["strict_requested_order_invariance_pass"] is False, "Order-invariance limitation was lost")

    actual = qualification["actual_frozen_case"]
    old, new = ROOT / actual["before_pack"], ROOT / actual["after_pack"]
    actual_delta = list(differences(read(old), read(new)))
    recorded_delta = read(HERE / "actual-lobe-after-boundary/PACK-DELTA.json")
    check(sorted(actual_delta, key=lambda row: row["path"]) == sorted(recorded_delta, key=lambda row: row["path"]), "Frozen actual-case comparison differs")
    check({row["path"] for row in actual_delta} == {"/0/pack_id", "/0/provenance/tags_hash"}, "Frozen actual case changed beyond IDs/hashes")
    for path, receipt_dir in ((old, "actual-v22-before"), (new, "actual-lobe-after-boundary")):
        receipt = read(HERE / receipt_dir / "receipt.json")
        check(receipt["returncode"] == 0 and digest(path) == receipt["sha256"], "Actual frozen receipt differs")

    seal_path = HERE / "lobe-boundary-candidate/candidate-20-file-seal.json"
    check(digest(seal_path) == qualification["candidate_20_file_seal_sha256"], "Original candidate seal changed")
    seal = read(seal_path)
    check(seal["base_commit"] == qualification["parent_commit"] and len(seal["files"]) == 20, "Candidate seal scope changed")
    for row in seal["files"]:
        path = ROOT / row["path"]
        check(digest(path) == row["sha256"] and path.stat().st_size == row["bytes"], "Candidate seal no longer matches repository")
    for row in read(HERE / "lobe-after-independent-review/candidate-seal-verification.json"):
        check(digest(ROOT / row["path"]) == row["expected_sha256"] == row["actual_sha256"], "Sealed candidate file differs")
    for manifest in read(HERE / "lobe-after-independent-review/index-binding-verification.json"):
        for row in manifest["shards"]:
            assets = ROOT / "skills/photo-prompt-image-generator/assets"
            old_path, new_path = assets / row["before_path"], assets / row["after_path"]
            check(old_path.read_bytes() == new_path.read_bytes() and digest(new_path) == row["sha256"], "Index shard identity check differs")
    check(digest(ROOT / "skills/photo-prompt-image-generator/scripts/prompt_generator.py") == summary["runtime_file_sha256"], "Runtime bytes differ from reviewed version")
    print(json.dumps({"verified": True, "source_commit": qualification["source_commit"], "sealed_files": len(qualification["files"]), "cases": case_results, "exact_order_invariance": False, "ordering_effect_reproduced": True, "actual_frozen_differences": len(actual_delta), "claim": "Narrow semantic boundary correction; no adoption, final-audit, or image claim"}, indent=2))


if __name__ == "__main__":
    main()
