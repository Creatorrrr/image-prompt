"""New V37 reconstruction from retained text and independently recovered sources.

Exact 629 workflow successor, with immutable V36 interpretation preserved.

Only the reviewed documentation bytes differ from upstream. Both accepted
interpreter/Unicode combinations produce the existing complete V36 pack.
Historical requests require their original sources and runtime; current 629
receipts never satisfy an explicit V36 or older request.
"""
from __future__ import annotations

import atexit
import contextlib
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

BASE = "docs/research-evidence/photo-prompt/workflow-boundary-v37-20261007/"
PROOF = BASE + "V37-SOURCE-PROOF.json"
PROOF_SHA256 = "d89c6a0f709d7e42bf1b213adf30345e2913e15189bfae8fbf1e0834fda5be79"
UPSTREAM_PIN = "629bf4a88e1f1f524d177d67c09615a7fdb4f89d"
UPSTREAM_TREE = "9f2782e9c125da5c8adb9578d9c0d00d01ad626a"
PARENT_PIN = "aa5c7622710e97b12a5b9d528dbebc7c4f017d99"
PARENT_TREE = "a3b41983653fb9b902d10e014ea5cc9d1a4c1177"
SKILL_SHA256 = "9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b"
V36_HELPER = "tests/photo_camera_guidance_v36.py"
V36_HELPER_SHA256 = "f9446c1daccdf195b03a6539a6b46cf166482e734565dc25d81b4de54c8c101c"
V36_BASELINE_SHA256 = "b8f2b27ab733a8c647127b83c847b4d2ee9f75552b0ee45883ef011be292ac04"
PACK_SHA256 = "3b36b45978e00f9f70455b5aa7952e26c45b4289e2e49751e5485da324b0a075"
PACK_ID = "f1d5de6f1a273b65"


def previous_module(root):
    """Authenticate retained code before executing it, without changing globals."""
    path = Path(root)
    for part in V36_HELPER.split("/"):
        path /= part
        if path.is_symlink():
            raise AssertionError("V37 prior helper symlink")
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != V36_HELPER_SHA256:
        raise AssertionError("V37 prior helper drift")
    spec = importlib.util.spec_from_file_location("_v37_immutable_v36", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Pure utilities and the immutable child guard are shared by reference. All
# version-specific source, pack, environment and history gates below are V37's.
previous = previous_module(Path(__file__).resolve().parents[1])
require, digest, canonical = previous.require, previous.digest, previous.canonical
same, strict_json, regular = previous.same, previous.strict_json, previous.regular
verify_files, verify_command = previous.verify_files, previous.verify_command
PHOTO, SKILL, ASSETS = previous.PHOTO, previous.SKILL, previous.ASSETS
VALIDATOR, DESCRIPTOR, HASH = previous.VALIDATOR, previous.DESCRIPTOR, previous.HASH
GUARDED_CHILD = previous.GUARDED_CHILD
CURRENT_BASELINE = ASSETS + "/photo_regression_baseline_v37.json"
V36_BASELINE = ASSETS + "/photo_regression_baseline_v36.json"
CURRENT_PACK = ASSETS + "/photo_regression_baseline_v36_pack.json"
ORIGINAL_TESTS = {
    "tests/test_photo_camera_authoring_guidance_contract.py": "09bb1e12887eacca7191b2d59ea158be96893c1b54e9d6561fd7612985b58ebb",
    "tests/test_photo_camera_guidance_v36_compatibility.py": "3a5938ffa4a5ade61e6db5c8cddc750ad8607ecd8cd3b7acfbbb1b96f11f656e",
}


def retained_name(name):
    return BASE + "history/" + name if name in ORIGINAL_TESTS else name
RUNTIME_IDENTITY_FIELDS = previous.RUNTIME_IDENTITY_FIELDS
REFERENCE_RUNTIME = previous.REFERENCE_RUNTIME
current_environment = previous.current_environment
environment_key = previous.environment_key
VERIFIED_RUNTIME_RECORDS = {
    ("cpython", (3, 12, 14), "15.0.0"): "fae35801d8d0c86e805db503e11c66cea4baec440939f335146fab5ea7a7bd8d",
    ("cpython", (3, 14, 3), "16.0.0"): "0833e12ab9da117160c94f529436c5229138be69cec8e734f017c044280bbe20",
}
NEW_SOURCE_PATHS = frozenset(PHOTO + "/" + name for name in (
    "precore/photo_authoring_contracts.py", "precore/photo_authoring_wire.py",
    "precore/photo_camera_authoring.py", "precore/photo_embodiment_review.py",
    "precore/photo_feature_selection.py", "precore/photo_run_files.py",
    "precore/photo_workflow_shapes.json", "precore/prepare_photo_run.py",
    "references/photo-workflow.md", "scripts/photo_native_bridge.py",
    "scripts/photo_precore_bridge.py", "scripts/photo_retry_projection.py",
    "scripts/photo_workflow.py", "scripts/photo_workflow_reviews.py",
    "scripts/photo_workflow_state.py", "scripts/photo_workflow_worker.py",
    "scripts/prepare_retry_context.py",
))


def bound_root(asset_dir, source_root):
    root = Path(source_root).resolve()
    require(Path(asset_dir).resolve() == root / ASSETS, "V37 asset directory mismatch")
    return root


def proof_document(root):
    raw = regular(root, PROOF).read_bytes()
    require(digest(raw) == PROOF_SHA256, "V37 proof seal drift")
    proof = strict_json(raw)
    require(proof.get("schema") == "photo-workflow-source-transition/v37"
            and proof.get("upstream_commit") == UPSTREAM_PIN
            and proof.get("upstream_tree") == UPSTREAM_TREE
            and proof.get("parent_boundary_commit") == PARENT_PIN
            and proof.get("parent_boundary_tree") == PARENT_TREE
            and proof.get("reviewed_skill_sha256") == SKILL_SHA256
            and type(proof.get("data_improvement_count_delta")) is int
            and proof["data_improvement_count_delta"] == 0
            and proof.get("doc_only_comparison_control") == "same_runtime",
            "V37 proof lineage or comparison attribution drift")
    return proof


def load_proof(source_root):
    return proof_document(Path(source_root).resolve())


def parent_context(root):
    history = previous.history_module(root)
    parent = history.GitSnapshot(root, PARENT_PIN, PARENT_TREE)
    raw = parent.payload(previous.PROOF, sha256=previous.PROOF_SHA256)
    require(regular(root, previous.PROOF).read_bytes() == raw, "V37 immutable V36 proof drift")
    return history, parent, strict_json(raw)


def live_source_paths(root):
    names = {SKILL, "tests/test_photo_visual_profile_shards.py"}
    for directory, suffixes in (("assets", {".json"}), ("precore", {".py", ".json"}),
                                ("references", {".md"}), ("scripts", {".py"})):
        path = Path(root) / PHOTO / directory
        require(path.is_dir() and not path.is_symlink(), "V37 source directory drift")
        names.update(str(p.relative_to(root)) for p in path.iterdir() if p.suffix in suffixes)
    return names


def verify_sources(root, mapping, upstream, old_proof, history):
    expected = set(old_proof["source_files_after"]) | NEW_SOURCE_PATHS
    require(type(mapping) is dict and len(mapping) == len(expected) == 173
            and set(mapping) == expected and live_source_paths(root) == expected,
            "V37 source inventory must contain exactly 173 bound paths")
    for name, sha256 in sorted(mapping.items()):
        require(type(sha256) is str and HASH.fullmatch(sha256), "V37 invalid source digest")
        upstream_raw = upstream.payload(name)
        expected_hash = SKILL_SHA256 if name == SKILL else digest(upstream_raw)
        require(sha256 == expected_hash, "V37 source exceeds exact upstream/documentation scope: " + name)
        history.require_live_payload(root, name, sha256, upstream.entry(name)["mode"])


def verify_parent_artifacts(root, proof, parent, old_proof):
    mapping = proof.get("parent_artifacts")
    required = {V36_HELPER, previous.HISTORY, previous.PROOF, V36_BASELINE, CURRENT_PACK, *ORIGINAL_TESTS}
    for group in ("historical_baselines", "frozen_inputs", "evidence_files"):
        required.update(old_proof[group])
    require(type(mapping) is dict and required <= set(mapping), "V37 immutable parent inventory drift")
    for name, sha256 in mapping.items():
        require(name not in {SKILL, VALIDATOR, DESCRIPTOR}, "V37 mutable path in immutable parent inventory")
        row = parent.entry(name)
        require(digest(parent.payload(name)) == sha256, "V37 parent Git binding drift: " + name)
        path = regular(root, retained_name(name))
        require(digest(path.read_bytes()) == sha256 and path.stat().st_mode & 0o7777 == int(row["mode"][-3:], 8),
                "V37 immutable parent bytes or mode drift: " + name)


def qualify_pack(proof, baseline, pack, raw, original_raw, unedited_raw):
    require(digest(original_raw) == PACK_SHA256, "V37 prior pack anchor drift")
    require(same(strict_json(raw), [pack]), "V37 pack JSON shape drift")
    require(digest(unedited_raw) == PACK_SHA256, "V37 unedited latest pack anchor drift")
    require(raw == unedited_raw, "V37 documentation pack differs from unedited latest bytes")
    require(proof.get("reviewed_upstream_pack_delta") == []
            and proof.get("reviewed_doc_only_pack_delta") == [], "V37 reviewed pack deltas must be empty")
    original = strict_json(original_raw)
    previous.preserved_surfaces(original[0], pack)
    require(same(original, [pack]), "V37 entire pack contains unreviewed semantics")
    require(raw == original_raw, "V37 complete pack bytes differ from immutable V36")
    count = sum(len(slot["candidates"]) for slot in pack["slots"].values())
    require(digest(raw) == proof.get("current_pack_sha256") == baseline.get("sha256") == PACK_SHA256
            and pack["pack_id"] == proof.get("current_pack_id") == baseline.get("pack_id") == PACK_ID
            and type(proof.get("preserved_public_candidate_count")) is int
            and type(baseline.get("public_candidate_count")) is int
            and count == proof["preserved_public_candidate_count"] == baseline["public_candidate_count"] == 64,
            "V37 pack descriptor binding drift")


def qualification_context(root, baseline=None):
    proof = proof_document(root)
    history, parent, old_proof = parent_context(root)
    require(proof.get("previous_manifest_sha256") == V36_BASELINE_SHA256
            and proof.get("previous_pack_sha256") == PACK_SHA256
            and proof.get("previous_proof_sha256") == previous.PROOF_SHA256,
            "V37 predecessor anchors drift")
    old = strict_json(parent.payload(V36_BASELINE, sha256=V36_BASELINE_SHA256))
    original_raw = parent.payload(CURRENT_PACK, sha256=PACK_SHA256)
    upstream = history.GitSnapshot(root, UPSTREAM_PIN, UPSTREAM_TREE)
    verify_sources(root, proof.get("source_files_after"), upstream, old_proof, history)
    require(same(proof.get("active_shards_after"), previous.active_shards(upstream)),
            "V37 active shards differ from exact upstream registration")
    verify_files(root, proof["active_shards_after"], "active shards", 32)
    require(same(proof.get("historical_baselines"), old_proof["historical_baselines"]),
            "V37 historical baseline inventory drift")
    verify_files(root, proof["historical_baselines"], "historical baselines", 63)
    verify_parent_artifacts(root, proof, parent, old_proof)
    require(same(proof.get("frozen_inputs"), old["frozen_inputs"]), "V37 frozen input inventory drift")
    verify_files(root, proof["frozen_inputs"], "frozen inputs", 4)
    verify_files(root, proof.get("evidence_files"), "evidence")
    require(proof.get("current_pack_path") == CURRENT_PACK, "V37 existing pack path drift")
    for key in ("baseline_composed_path", "runtime_request_path"):
        name = proof.get(key)
        require(name == old_proof[key] and name in proof["evidence_files"]
                and proof["evidence_files"][name] == old_proof["evidence_files"][name],
                "V37 reused evidence binding drift: " + key)
    descriptor = parent.payload(DESCRIPTOR)
    old_hash = digest(parent.payload(VALIDATOR)).encode()
    require(descriptor.count(old_hash) == 1 and regular(root, DESCRIPTOR).read_bytes()
            == descriptor.replace(old_hash, digest(regular(root, VALIDATOR).read_bytes()).encode(), 1),
            "V37 universal descriptor changed beyond validator binding")
    actual = strict_json(regular(root, CURRENT_BASELINE).read_bytes())
    require(baseline is None or same(baseline, actual), "V37 supplied baseline differs from committed descriptor")
    require(actual.get("schema") == "photo_regression_baseline/v37", "V37 schema drift")
    require(actual.get("workflow_source_transition") == {
        "evidence_path": PROOF, "evidence_sha256": PROOF_SHA256, "upstream_commit": UPSTREAM_PIN},
        "V37 transition binding drift")
    require(actual.get("historical_baseline") == {
        "path": "photo_regression_baseline_v36.json", "schema": "photo_regression_baseline/v36",
        "sha256": V36_BASELINE_SHA256}, "V37 predecessor binding drift")
    for field in previous.PRESERVED_BASELINE_FIELDS:
        require(same(actual.get(field), old[field]), "V37 protected descriptor field drift: " + field)
    verify_command(actual.get("command"), old["command"])
    return proof, actual, original_raw


def qualify_current(root, baseline, pack, raw, *, asset_dir=None):
    root = bound_root(asset_dir or Path(root) / ASSETS, root)
    proof, baseline, original_raw = qualification_context(root, baseline)
    require(raw == regular(root, CURRENT_PACK).read_bytes(), "V37 CLI bytes differ from committed pack")
    qualify_pack(proof, baseline, pack, raw, original_raw, regular(root, proof["current_pack_path"]).read_bytes())
    return proof


def selected_runtime_record(proof):
    rows = proof.get("verified_runtime_environments")
    require(type(rows) is list and len(rows) == len(VERIFIED_RUNTIME_RECORDS), "V37 verified runtime inventory drift")
    records, identities = {}, {field: set() for field in RUNTIME_IDENTITY_FIELDS}
    for row in rows:
        require(type(row) is dict and set(row) == {"environment", *RUNTIME_IDENTITY_FIELDS}, "V37 runtime record fields drift")
        key = environment_key(row["environment"])
        require(key in VERIFIED_RUNTIME_RECORDS, "V37 unverified runtime environment")
        require(key not in records, "V37 duplicate runtime environment")
        for field in RUNTIME_IDENTITY_FIELDS:
            value = row[field]
            require(type(value) is str and HASH.fullmatch(value), "V37 invalid runtime identity: " + field)
            require(value not in identities[field], "V37 duplicate runtime identity: " + field)
            identities[field].add(value)
        require(digest(canonical(row)) == VERIFIED_RUNTIME_RECORDS[key], "V37 runtime record seal drift")
        records[key] = row
    require(set(records) == set(VERIFIED_RUNTIME_RECORDS), "V37 verified runtime inventory drift")
    reference = {field: proof.get(field) for field in ("environment", *RUNTIME_IDENTITY_FIELDS)}
    require(same(reference, records[REFERENCE_RUNTIME]), "V37 reference runtime identity drift")
    key = environment_key(current_environment())
    require(key in records, "V37 exact runtime environment unavailable")
    return copy.deepcopy(records[key])


def qualify_snapshot(root, baseline, pack, raw, receipt, *, runtime_store):
    root = Path(root).resolve()
    proof = qualify_current(root, baseline, pack, raw)
    require(runtime_store is not None and Path(runtime_store).is_dir(), "V37 explicit runtime store unavailable")
    record = selected_runtime_record(proof)
    require(isinstance(receipt, dict) and all(receipt.get(k) == record[k] for k in RUNTIME_IDENTITY_FIELDS), "V37 receipt identity drift")
    scripts = root / PHOTO / "scripts"
    sys.path.insert(0, str(scripts))
    try:
        import photo_runtime_sources as runtime
        import audit_composed_prompt as composed_audit
        import audit_image_render_request as render_audit
        for module in (runtime, composed_audit, render_audit):
            require(Path(module.__file__).resolve().parent == scripts, "V37 production module root mismatch")
        provider = runtime.RuntimeSnapshotProvider(root / PHOTO, Path(runtime_store))
        snapshot = provider.from_receipt(pack, receipt)
        captured, _ = runtime.capture_sources(root / PHOTO)
        require(same(captured, snapshot.manifest["source"]), "V37 live source differs from receipt generation")
        require(snapshot.generation_id == record["generation_id"] and all(snapshot.manifest[k] == record[k] for k in ("source_fingerprint", "algorithm_sha256"))
                and same(snapshot.manifest["source"]["environment"], record["environment"]), "V37 snapshot identity drift")
        composed = strict_json(regular(root, proof["baseline_composed_path"]).read_bytes())
        request_path = regular(root, proof["runtime_request_path"])
        request = strict_json(request_path.read_bytes())
        require(composed["prompt_en"] == pack["authorial_core"]["baseline_prompt_en"]
                and composed["prompt_en"] in request["runtime_prompt_en"], "V37 baseline prompt changed")
        result = composed_audit.audit_composed_prompt(pack, composed, runtime_receipt=receipt, runtime_store=Path(runtime_store))
        request_result = render_audit.audit_image_render_request(pack, composed, request, request_path=request_path)
        require(result.get("status") == request_result.get("status") == "pass", "V37 production audits failed: " + json.dumps({"composed": result, "runtime": request_result}))
    finally:
        sys.path.pop(0)
    return {"status": "pass", "schema": baseline["schema"], "historical_sha256": V36_BASELINE_SHA256,
            "sha256": digest(raw), "pack_id": pack["pack_id"], "generation_id": snapshot.generation_id,
            "private_runtime_receipt": copy.deepcopy(receipt)}


def validate_current(asset_dir, *, source_root, runtime_store=None):
    root = bound_root(asset_dir, source_root)
    proof, baseline, original_raw = qualification_context(root)
    raw = regular(root, CURRENT_PACK).read_bytes()
    payload = strict_json(raw)
    require(isinstance(payload, list) and len(payload) == 1, "V37 committed pack shape drift")
    qualify_pack(proof, baseline, payload[0], raw, original_raw, regular(root, proof["current_pack_path"]).read_bytes())
    source_store = runtime_store or os.environ.get("PHOTO_RUNTIME_STORE")
    require(source_store is not None, "V37 requires an explicit existing PHOTO_RUNTIME_STORE")
    selected_runtime_record(proof)
    with tempfile.TemporaryDirectory(prefix="photo-v37-current-") as temporary:
        work = Path(temporary)
        store, output = work / "runtime", work / "pack.json"
        copy_runtime(source_store, store, root, proof)
        command = baseline["command"].copy()
        command[command.index("--output-file") + 1] = str(output)
        env = {k: os.environ[k] for k in ("PATH", "LANG", "LC_ALL", "TZ") if k in os.environ}
        env.setdefault("LANG", "C.UTF-8")
        env["PHOTO_RUNTIME_STORE"] = str(store)
        result = subprocess.run([sys.executable, "-I", "-S", "-B", "-c", GUARDED_CHILD, str(root),
                                 str(root / command[1]), str(output), str(store), *command[2:]],
                                cwd=root, env=env, capture_output=True, text=True, timeout=900)
        require(result.returncode == 0, "V37 public CLI failed: " + result.stdout + result.stderr)
        actual = output.read_bytes()
        packs = strict_json(actual)
        require(isinstance(packs, list) and len(packs) == 1, "V37 CLI pack shape drift")
        receipt = strict_json(Path(str(output) + ".runtime-receipt.json").read_bytes())
        return qualify_snapshot(root, baseline, packs[0], actual, receipt, runtime_store=store)



def _copy_store(source, target):
    """Share only runtime-owned immutable payloads; copy mutable state."""
    def copy_file(name, destination):
        relative = Path(name).relative_to(source)
        if relative.parts[0] in {"generations", "source-data", "core-slot-index-data"}:
            os.link(name, destination)
        else:
            shutil.copy2(name, destination)
        return destination
    shutil.copytree(source, target, copy_function=copy_file)


def _source_revision(store, namespace):
    path = store / "local" / namespace / "SOURCE.json"
    revision = strict_json(regular(store, str(path.relative_to(store))).read_bytes()) if path.exists() else {"epoch": 0, "editing": None}
    require(type(revision) is dict and type(revision.get("epoch")) is int
            and revision["epoch"] >= 0 and revision.get("editing") is None,
            "V37 unfinished source revision")
    return revision


def _binding_modules(root):
    scripts = root / PHOTO / "scripts"
    sys.path.insert(0, str(scripts))
    try:
        import photo_runtime_sources as runtime
        import prompt_generator as generator
        for module in (runtime, generator):
            require(Path(module.__file__).resolve().parent == scripts,
                    "V37 binding module root mismatch")
        return runtime, generator
    finally:
        sys.path.pop(0)


def bind_runtime_root(source, target, root, record):
    """Bind an exact existing generation to a new root in an isolated store.

    This is a namespace change, not publication. The generation identity and
    official source/algorithm capture must already agree before any write.
    """
    source, target, root = Path(source), Path(target), Path(root).resolve()
    require(source.is_dir() and not source.is_symlink() and not target.exists(),
            "V37 existing runtime or isolated destination unavailable")
    source = source.resolve()
    for path in source.rglob("*"):
        require(not path.is_symlink(), "V37 runtime symlink")
    pointers = sorted(source.glob("local/*/CURRENT.json"))
    require(len(pointers) == 1, "V37 runtime source namespace is absent or ambiguous")
    original_path = pointers[0]
    original_raw = regular(source, str(original_path.relative_to(source))).read_bytes()
    pointer = strict_json(original_raw)
    require(type(pointer) is dict and pointer.get("schema") == "photo-runtime-current/v1"
            and type(pointer.get("revision")) is int and pointer["revision"] >= 1
            and pointer.get("generation_id") == record["generation_id"]
            and pointer.get("source_fingerprint") == record["source_fingerprint"],
            "V37 source-root runtime pointer drift")
    observation = pointer.get("observation")
    require(type(observation) is dict and observation.get("mode") == "local_current"
            and type(observation.get("root")) is str and Path(observation["root"]).is_absolute()
            and str(Path(observation["root"]).resolve()) == observation["root"],
            "V37 original namespace observation drift")
    original_namespace = digest(canonical({"root": observation["root"], "mode": "local_current", "remote": ""}))
    require(original_path.parent.name == original_namespace, "V37 original namespace digest drift")
    revision = _source_revision(source, original_namespace)
    require(type(observation.get("local_epoch")) is int and observation["local_epoch"] == revision["epoch"],
            "V37 original namespace epoch drift")
    manifest_path = "generations/" + record["generation_id"] + "/manifest.json"
    manifest_raw = regular(source, manifest_path).read_bytes()
    manifest = strict_json(manifest_raw)
    require(type(manifest) is dict and type(manifest.get("source")) is dict
            and digest(canonical(manifest)) == record["generation_id"]
            and manifest.get("schema") == "photo-runtime-generation/v1"
            and all(manifest.get(k) == record[k] for k in ("source_fingerprint", "algorithm_sha256"))
            and same(manifest.get("source", {}).get("environment"), record["environment"])
            and digest(canonical(manifest["source"])) == record["source_fingerprint"],
            "V37 namespace generation binding drift")
    runtime, generator = _binding_modules(root)
    captured, _ = runtime.capture_sources(root / PHOTO)
    require(same(captured, manifest["source"]) and runtime.algorithm_hash(generator) == record["algorithm_sha256"],
            "V37 new-root source/algorithm capture drift")
    runtime.SnapshotPublisher._verify_generation(source / "generations" / record["generation_id"], record["generation_id"])
    cache = manifest["slot_cache"]["payload"]
    cache_raw = regular(source, cache["path"]).read_bytes()
    require(cache["path"] == "core-slot-index-data/" + cache["sha256"] + ".json"
            and type(cache["bytes"]) is int and len(cache_raw) == cache["bytes"]
            and digest(cache_raw) == cache["sha256"], "V37 immutable cache binding drift")
    require(regular(source, str(original_path.relative_to(source))).read_bytes() == original_raw
            and same(_source_revision(source, original_namespace), revision), "V37 source namespace changed during binding")
    _copy_store(source, target)
    namespace = digest(canonical({"root": str(root / PHOTO), "mode": "local_current", "remote": ""}))
    directory = target / "local" / namespace
    require(not directory.exists(), "V37 temporary namespace already exists")
    directory.mkdir(parents=True)
    bound = copy.deepcopy(pointer)
    bound["observation"]["root"] = str(root / PHOTO)
    (directory / "CURRENT.json").write_bytes(canonical(bound))
    (directory / "SOURCE.json").write_bytes(canonical(revision))
    checked, _ = runtime.capture_sources(root / PHOTO)
    require(same(checked, captured) and same(_source_revision(source, original_namespace), revision)
            and regular(source, str(original_path.relative_to(source))).read_bytes() == original_raw,
            "V37 source changed after namespace binding")


def copy_runtime(source, target, root, proof):
    record = selected_runtime_record(proof)
    source = Path(source)
    require(not source.is_symlink(), "V37 runtime symlink")
    source = source.resolve()
    require(source.is_dir() and not target.exists(), "V37 existing runtime or isolated destination unavailable")
    for path in source.rglob("*"):
        require(not path.is_symlink(), "V37 runtime symlink")
    require((source / "generations" / record["generation_id"]).is_dir(), "V37 published generation unavailable")
    namespace = digest(canonical({"root": str(root / PHOTO), "mode": "local_current", "remote": ""}))
    pointer_path = source / "local" / namespace / "CURRENT.json"
    if not pointer_path.exists():
        bind_runtime_root(source, target, root, record)
    else:
        pointer = strict_json(regular(source, str(pointer_path.relative_to(source))).read_bytes())
        require(type(pointer) is dict and pointer.get("generation_id") == record["generation_id"]
                and pointer.get("source_fingerprint") == record["source_fingerprint"],
                "V37 source-root runtime pointer drift")
        _copy_store(source, target)


def _git_context(root, directory, history):
    probe = history.GitSnapshot(root, PARENT_PIN, PARENT_TREE)
    git_dir = probe.git("rev-parse", "--absolute-git-dir").decode().strip()
    (directory / ".git").write_text("gitdir: " + git_dir + "\n")


def _parent_payload(root, snapshot, name, sha256=None):
    """Use live bytes only after authenticating their exact old Git identity."""
    row = snapshot.entry(name)
    candidate = Path(root) / retained_name(name)
    if candidate.is_file() and not candidate.is_symlink():
        raw = regular(root, retained_name(name)).read_bytes()
        oid = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        if oid == row["git_blob"] and candidate.stat().st_mode & 0o7777 == int(row["mode"][-3:], 8):
            require(sha256 is None or digest(raw) == sha256, "V37 parent payload digest drift")
            return raw, row
    return snapshot.payload(name, sha256=sha256), row


def materialize_parent_projection(directory, *, source_root, names):
    """Materialize only a declared exact aa5 closure; never fetch or publish."""
    root, directory = Path(source_root).resolve(), Path(directory)
    require(not directory.exists() and not directory.is_symlink(), "V37 parent projection destination exists")
    history, parent, _ = parent_context(root)
    payloads = [(name, *_parent_payload(root, parent, name)) for name in sorted(set(names))]
    directory.mkdir(parents=True)
    for name, raw, row in payloads:
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        target.chmod(int(row["mode"][-3:], 8))
    _git_context(root, directory, history)
    return directory


COMPATIBILITY_IMPORTS = (
    "test_photo_current_boundary_snapshot", "test_photo_nape_metadata_boundary_history",
    "test_photo_latest_metadata_boundary_history", "test_photo_religion_iconography_boundary_history",
    "test_photo_slang_boundary_history", "test_photo_subculture_appearance_boundary_history",
    "test_photo_uniform_metadata_boundary_history", "test_photo_vocaloid_metadata_boundary_history",
)
COMPATIBILITY_PROOFS = (
    "camera-evidence-structure-20261003/pr-review-followup/V11-four-leaf-proof.json",
    "vocaloid-appearance-integration-20261004/main-merge/V12-FOUR-LEAF-PROOF.json",
    "uniform-costume-integration-20261004/main-merge/V13-FOUR-LEAF-PROOF.json",
)


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@contextlib.contextmanager
def _projected_imports(tree, bindings):
    import tests as package
    package_names = (*COMPATIBILITY_IMPORTS, "photo_camera_guidance_history_v36")
    names = {"tests." + item for item in package_names} | {
        "universal_scene_runtime", "illustration_runtime", "illustration_audit", "validate_illustration_assets"}
    missing = object()
    old_modules = {name: sys.modules.get(name, missing) for name in names}
    old_attributes = {name: getattr(package, name, missing) for name in package_names}
    old_path = sys.path[:]
    sys.path[:0] = [str(tree), str(tree / previous.ILL / "scripts")]
    try:
        sys.modules.update(bindings)
        for name in package_names:
            if "tests." + name in bindings:
                setattr(package, name, bindings["tests." + name])
        yield
    finally:
        for name, old in old_modules.items():
            if old is missing:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old
        for name, old in old_attributes.items():
            if old is missing:
                if hasattr(package, name):
                    delattr(package, name)
            else:
                setattr(package, name, old)
        sys.path[:] = old_path


class _ProjectedTestSuite(unittest.TestSuite):
    def __init__(self, suite, tree, bindings):
        super().__init__(suite)
        self.tree, self.bindings = tree, bindings

    def run(self, result, debug=False):
        with _projected_imports(self.tree, self.bindings):
            return super().run(result, debug)


def historical_test_suite(module_name, *, source_root, loader):
    """Deliver unchanged original test bodies through exact small fixtures."""
    root = Path(source_root).resolve()
    name = module_name.replace(".", "/") + ".py"
    require(name in ORIGINAL_TESTS, "V37 unregistered historical test entry")
    history, parent, old_proof = parent_context(root)
    raw, _ = _parent_payload(root, parent, name, ORIGINAL_TESTS[name])
    require(regular(root, retained_name(name)).read_bytes() == raw, "V37 original test artifact drift")
    names = {name}
    camera = name.endswith("test_photo_camera_authoring_guidance_contract.py")
    if camera:
        names.update(PHOTO + "/scripts/" + item for item in
                     ("photo_contracts.py", "prompt_generator.py", "photo_camera_evidence.py"))
    else:
        names.update(old_proof["historical_baselines"])
        names.update(old_proof["frozen_inputs"])
        names.update({V36_BASELINE, CURRENT_PACK, VALIDATOR, ASSETS + "/universal_scene_baseline_v1.json"})
        names.update("docs/research-evidence/photo-prompt/" + item for item in COMPATIBILITY_PROOFS)
        names.update("tests/" + item + ".py" for item in COMPATIBILITY_IMPORTS)
        names.update(previous.ILL + "/scripts/" + item + ".py" for item in
                     ("universal_scene_runtime", "illustration_runtime", "illustration_audit"))
    temporary = tempfile.TemporaryDirectory(prefix="photo-v37-original-tests-")
    atexit.register(temporary.cleanup)
    tree = materialize_parent_projection(Path(temporary.name) / "tree", source_root=root, names=names)
    frozen_name = "_photo_v37_original_" + Path(name).stem
    if camera:
        return loader.loadTestsFromModule(_load_module(tree / name, frozen_name))
    bindings = {"tests.photo_camera_guidance_history_v36": history}
    with _projected_imports(tree, bindings):
        for imported in ("universal_scene_runtime", "illustration_runtime", "illustration_audit", "validate_illustration_assets"):
            bindings[imported] = _load_module(tree / previous.ILL / "scripts" / (imported + ".py"), imported)
        import tests as package
        for imported in COMPATIBILITY_IMPORTS:
            full_name = "tests." + imported
            module = _load_module(tree / "tests" / (imported + ".py"), full_name)
            bindings[full_name] = module
            setattr(package, imported, module)
        module = _load_module(tree / name, frozen_name)
        # This unique module stays registered for unittest's module fixtures.
        # Shared package/import names are restored by _projected_imports.
        bindings[frozen_name] = module
        suite = loader.loadTestsFromModule(module)
    return _ProjectedTestSuite(suite, tree, bindings)


def historical_projection_names(root, old_proof):
    history = previous.history_module(root)
    names = {V36_HELPER, previous.HISTORY, previous.PROOF, V36_BASELINE, CURRENT_PACK,
             VALIDATOR, DESCRIPTOR, history.PROOF, history.PARENT, "tests/__init__.py"}
    for group in ("source_files_after", "active_shards_after", "historical_baselines", "frozen_inputs", "evidence_files"):
        names.update(old_proof[group])
    return names


def dispatch_historical(asset_dir, *, source_root, baseline_version):
    root = bound_root(asset_dir, source_root)
    require(type(baseline_version) is int and baseline_version in range(6, 37),
            "Unsupported historical V37 dispatch version")
    proof = proof_document(root)
    history, parent, old_proof = parent_context(root)
    verify_parent_artifacts(root, proof, parent, old_proof)
    if baseline_version < 36:
        # The original helper retains its own environment/closure checks and
        # publisher behavior. This does not replace an unavailable replay.
        names = historical_projection_names(root, old_proof)
        with tempfile.TemporaryDirectory(prefix="photo-v37-original-v35-") as temporary:
            tree = materialize_parent_projection(Path(temporary) / "tree", source_root=root, names=names)
            return previous.dispatch(tree / ASSETS, source_root=tree, baseline_version=baseline_version)
    source_store = os.environ.get("PHOTO_V36_RUNTIME_STORE") or os.environ.get("PHOTO_RUNTIME_STORE")
    if source_store is None:
        raise history.HistoricalReplayUnavailable("Exact V36 requires an existing recorded 4f runtime store")
    record = previous.selected_runtime_record(old_proof)
    if not (Path(source_store) / "generations" / record["generation_id"]).is_dir():
        raise history.HistoricalReplayUnavailable("Exact V36 recorded 4f generation unavailable; current 629 cannot satisfy V36")
    with tempfile.TemporaryDirectory(prefix="photo-v37-original-v36-") as temporary:
        work = Path(temporary)
        tree = materialize_parent_projection(work / "tree", source_root=root,
                                            names=historical_projection_names(root, old_proof))
        # A fresh worker keeps historical imports separate from current code.
        instruction = (
            "import importlib.util,json,os,sys; from pathlib import Path; "
            "root,tree,source,store=map(Path,sys.argv[1:5]); "
            "spec=importlib.util.spec_from_file_location('v37_binding',root/'tests/photo_workflow_boundary_v37.py'); "
            "v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v); "
            "old=v.previous.proof_document(tree);record=v.previous.selected_runtime_record(old); "
            "v.bind_runtime_root(source,store,tree,record); "
            "print(json.dumps(v.previous.validate_current(tree/v.ASSETS,source_root=tree,runtime_store=store)))"
        )
        result = subprocess.run([sys.executable, "-I", "-S", "-B", "-c", instruction,
                                 str(root), str(tree), str(Path(source_store).resolve()), str(work / "runtime")],
                                cwd=tree, capture_output=True, text=True, timeout=1800)
        require(result.returncode == 0, "V37 exact V36 replay failed: " + result.stdout + result.stderr)
        return strict_json(result.stdout.strip().splitlines()[-1])


def dispatch(asset_dir, *, source_root, baseline_version=None):
    root = bound_root(asset_dir, source_root)
    if baseline_version is None or (type(baseline_version) is int and baseline_version == 37):
        return validate_current(asset_dir, source_root=root)
    require(type(baseline_version) is int and baseline_version in range(6, 37), "Unsupported V37 version")
    return dispatch_historical(asset_dir, source_root=root, baseline_version=baseline_version)
