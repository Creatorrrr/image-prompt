"""Verify staged parent preservation, derived files, and focused test evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[4]
ASSETS = Path("skills/photo-prompt-image-generator/assets")
sys.path.insert(0, str(ROOT / ASSETS.parent / "scripts"))
import prompt_generator as pg


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main(evidence: Path, test_evidence: Path):
    source = json.loads((evidence / "source-preservation.json").read_text())
    index = json.loads((evidence / "index-reconciliation.json").read_text())
    compatibility_file = evidence / "test-compatibility.json"
    adjustments = json.loads(compatibility_file.read_text())["adjustments"] if compatibility_file.exists() else []
    adjusted = {row["path"]: row for row in adjustments}
    concurrent = []
    for row in source["exclusive_files"]:
        path = row["path"]
        staged = git("show", f":{path}")
        if path in adjusted:
            assert row["sha256"] == adjusted[path]["parent_sha256"]
            assert digest(staged) == adjusted[path]["merged_sha256"]
        else:
            assert digest(staged) == row["sha256"], f"Parent blob changed in index: {path}"
        working = (ROOT / path).read_bytes()
        if working != staged:
            assert path.startswith("docs/"), f"Concurrent runtime source changed: {path}"
            concurrent.append(path)
    for path, key in [(ASSETS / "photo_prompt_visual_obligations.json", "merged_raw_registry_sha256"),
                      (ASSETS / "photo_prompt_tags.json", "merged_raw_tags_sha256")]:
        raw = (ROOT / path).read_bytes()
        assert digest(raw) == source[key], str(path)
        assert git("show", f":{path}") == raw, f"Staged source differs: {path}"
    data = pg.load_json(ROOT / ASSETS / "photo_prompt_tags.json")
    registry = pg.load_visual_obligation_registry(ROOT / ASSETS / "photo_prompt_visual_obligations.json")
    semantic = pg.load_semantic_index_payload(ROOT / ASSETS / "photo_prompt_semantic_index.json")
    pg.validate_semantic_index_metadata(semantic, data)
    visual = pg.load_visual_profile_index(ROOT / ASSETS / "photo_prompt_visual_profile_index.json", registry)
    assert semantic["dictionary_hash"] == index["dictionary_hash"]
    assert visual["registry_sha256"] == index["registry_sha256"]
    assert len(semantic["entries"]) == index["semantic_entries"]
    assert len(visual["entries"]) == index["visual_profiles"]
    derived_paths = [ASSETS / "photo_prompt_semantic_index.json",
                     ASSETS / "photo_prompt_visual_profile_index.json",
                     *(Path(p) for p in index["semantic_shards"])]
    for path in derived_paths:
        assert git("show", f":{path}") == (ROOT / path).read_bytes(), f"Derived file not staged: {path}"
    assert not git("diff", "--name-only", "--diff-filter=U").strip(), "Unresolved merge entries"
    assert git("rev-parse", "HEAD").decode().strip() == source["local_parent"]
    assert git("rev-parse", "MERGE_HEAD").decode().strip() == source["remote_parent"]
    subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
    unstaged = git("diff", "--name-only").decode().splitlines()
    assert all(p.startswith("docs/") for p in unstaged), f"Unstaged runtime changes: {unstaged}"

    suites = ET.parse(test_evidence / "merged-tests.xml").getroot().findall("testsuite")
    tests = {key: sum(int(s.attrib.get(key, 0)) for s in suites)
             for key in ("tests", "failures", "errors", "skipped")}
    assert tests["tests"] > 0 and tests["failures"] == tests["errors"] == 0, tests
    log = (test_evidence / "merged-tests.log").read_text()
    assert " passed" in log and "failed" not in log.lower(), "Test completion missing or failed"

    objects = {line.split()[0] for line in git("rev-list", "--objects", "origin/main..HEAD").decode().splitlines()}
    staged_changed = set(git("diff", "--cached", "--name-only", "--diff-filter=ACMR").decode().splitlines())
    upstream_paths = set(git("diff", "--name-only", source["merge_base"], source["remote_parent"]).decode().splitlines())
    allowed_derived = {str(p) for p in derived_paths}
    own_evidence_prefix = str(Path(__file__).resolve().parent.relative_to(ROOT)) + "/"
    unexpected = sorted(p for p in staged_changed if p not in upstream_paths | allowed_derived | set(adjusted)
                        and not p.startswith(own_evidence_prefix))
    assert not unexpected, f"Unexpected staged concurrent work: {unexpected}"
    for item in git("ls-files", "-s", "-z").decode().split("\0"):
        if item:
            metadata, path = item.split("\t", 1)
            if path in staged_changed:
                objects.add(metadata.split()[1])
    object_info = subprocess.check_output(["git", "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"],
        input=("\n".join(sorted(objects)) + "\n").encode(), cwd=ROOT).decode().splitlines()
    blobs = [(oid, int(size)) for oid, kind, size in (r.split() for r in object_info) if kind == "blob"]
    oversized = [(oid, size) for oid, size in blobs if size >= 100 * 1024 * 1024]
    assert not oversized, oversized
    report = {
        "status": "PASS", "local_parent": source["local_parent"], "remote_parent": source["remote_parent"],
        "staged_exclusive_parent_blobs_verified": len(source["exclusive_files"]) - len(adjusted),
        "explicit_test_compatibility_adjustments": adjustments,
        "authored_source_hashes_verified": True, "derived_files_staged_and_metadata_valid": True,
        "semantic_entries": len(semantic["entries"]), "visual_profiles": len(visual["entries"]),
        "tests_junit": tests, "tests_log_summary": log.splitlines()[-1],
        "tests_xml_sha256": digest((test_evidence / "merged-tests.xml").read_bytes()),
        "test_evidence": str(test_evidence.relative_to(ROOT)),
        "staged_whitespace_check": "PASS", "unresolved_paths": 0,
        "staged_paths_scoped_to_upstream_derived_and_merge_evidence": True,
        "maximum_unpublished_or_staged_blob_bytes": max(size for _, size in blobs),
        "oversized_blobs": 0, "concurrent_working_documents_preserved_unstaged": concurrent,
        "all_unstaged_paths": unstaged, "image_generation_or_pixel_validation": "not run",
    }
    (evidence / "final-validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--test-evidence", type=Path)
    args = parser.parse_args()
    evidence = args.evidence.resolve()
    main(evidence, args.test_evidence.resolve() if args.test_evidence else evidence)
