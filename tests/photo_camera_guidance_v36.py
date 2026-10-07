"""Exact current V36 boundary; original history is replayed by its own helper.

The V35-to-latest comparison is observational across runtimes. The latest-to-
documentation comparison is controlled on the same runtime and must be empty.
Neither comparison credits this documentation change with authored DATA.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unicodedata

BASE = "docs/research-evidence/photo-prompt/camera-guidance-v36-20261007/"
PROOF = BASE + "V36-SOURCE-PROOF.json"
PROOF_SHA256 = "5fa361c01df0b3b3e4ec35e2b3d81a5677acaa939400f85aea6edd96f49bf8ce"
UPSTREAM_PACK_SHA256 = "3b36b45978e00f9f70455b5aa7952e26c45b4289e2e49751e5485da324b0a075"
REVIEWED_DELTA_SHA256 = "e17bbc69f0c5ec5348d8b2080a8f1673d11f806fe0aed076928dae36da44d3f7"
# Fresh 42-leaf observation, canonicalized to 33 exact object-member operations
# by replacing three changed arrays. The complete leaf diff remains evidence.
REVIEWED_POINTERS = (
    "/0/candidate_bundles/candidates",
    "/0/core_retrieval/active_slots/transition_stage",
    "/0/core_retrieval/canonical_sha256",
    "/0/core_retrieval/slot_corpus_sha256",
    "/0/core_retrieval/slot_ownership_sha256",
    "/0/creative_augmentation/candidates",
    "/0/creative_augmentation/hard_eligible_pool_sha256",
    "/0/pack_id",
    "/0/provenance/tags_hash",
    "/0/semantic_clarification/candidates/1/applicability/diagnostics",
    "/0/semantic_clarification/candidates/1/applicability/reason",
    "/0/semantic_clarification/candidates/2/applicability/diagnostics",
    "/0/semantic_clarification/candidates/2/applicability/reason",
    "/0/semantic_clarification/candidates/3/applicability/diagnostics",
    "/0/semantic_clarification/candidates/4/applicability/diagnostics",
    "/0/semantic_clarification/candidates/5/applicability/diagnostics",
    "/0/semantic_clarification/candidates/5/applicability/reason",
    "/0/semantic_clarification/candidates/5/applicability/status",
    "/0/semantic_clarification/candidates/6/applicability/diagnostics",
    "/0/semantic_clarification/candidates/7/applicability/diagnostics",
    "/0/semantic_clarification/candidates/8/applicability/diagnostics",
    "/0/semantic_clarification/contract_version",
    "/0/slots/composition/candidate_count",
    "/0/slots/focus/candidate_count",
    "/0/slots/light_type/candidate_count",
    "/0/slots/lighting/candidate_count",
    "/0/slots/medium/candidates",
    "/0/slots/motion/candidate_count",
    "/0/slots/scale_relation/candidate_count",
    "/0/slots/surreal_physics_detail/candidate_count",
    "/0/slots/texture/candidate_count",
    "/0/slots/transition_stage",
    "/0/slots/world/candidate_count",
)
UPSTREAM_PIN = "4f3d524ed035de8592e4b0c6ad5030b41ffc55af"
SKILL_SHA256 = "72e283b4cce42234819849b8d82ab0ac488ca342383bcdd760afa2e93b096e24"
HISTORY = "tests/photo_camera_guidance_history_v36.py"
HISTORY_SHA256 = "d315700703c619ef4e9efb3778ca91981f6f17ee5cae52d0bf1697e1051075f8"
ILL = "skills/subculture-illustration-image-generator"
ASSETS = ILL + "/assets"
PHOTO = "skills/photo-prompt-image-generator"
SKILL = PHOTO + "/SKILL.md"
VALIDATOR = ILL + "/scripts/validate_illustration_assets.py"
DESCRIPTOR = ASSETS + "/universal_scene_baseline_v2.json"
V35_BASELINE = ASSETS + "/photo_regression_baseline_v35.json"
V35_PACK = ASSETS + "/photo_regression_baseline_v35_pack.json"
V35_BASELINE_SHA256 = "7f0f6259088cffb823b1e022a3052e9c25af931af5b252a6eda2680113cc91f8"
V35_PACK_SHA256 = "1f18f0d6f8c79c856c1bd4162585a53fc7ed379607e11d1123cfff7a8eea22b7"
HASH = re.compile(r"[0-9a-f]{64}\Z")
PRESERVED_FIELDS = (
    "adult_appeal", "artistic_final_touch", "authorial_composition", "authorial_core",
    "candidate_semantic_surface_version", "conflicts", "contract_version", "coverage",
    "creative_controls", "embodiment_preflight", "intent_contract", "intent_preservation",
    "mandatory_intents", "negative_en", "negative_intent_guard", "photographic_craft",
    "photographic_integration", "quality_profile", "safety", "uncovered_intents",
    "visual_concept_candidates", "visual_proposition",
)
PRESERVED_BASELINE_FIELDS = (
    "contract_version", "public_candidate_count", "private_fields_absent",
    "negative_en", "preserved_contract_sha256", "frozen_inputs",
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def same(left, right):
    """JSON type-sensitive equality; Python's False == 0 is insufficient."""
    return canonical(left) == canonical(right)


def strict_json(raw):
    def pairs(rows):
        result = {}
        for key, value in rows:
            require(key not in result, "Duplicate JSON key: " + key)
            result[key] = value
        return result
    def invalid(value):
        raise AssertionError("Non-finite JSON value: " + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)


def regular(root, name):
    require(isinstance(name, str) and name and "\\" not in name and "\0" not in name, "Unsafe V36 path")
    path = PurePosixPath(name)
    require(not path.is_absolute() and path.as_posix() == name
            and all(p not in (".", "..", ".git") for p in path.parts), "Unsafe V36 path: " + name)
    result = Path(root)
    for part in path.parts:
        result = result / part
        require(not result.is_symlink(), "V36 symlink: " + name)
    require(result.is_file() and stat.S_ISREG(result.stat().st_mode), "V36 missing regular file: " + name)
    return result


def bound_root(asset_dir, source_root):
    """This precedes imports, proof reads, source checks, and CLI execution."""
    root = Path(source_root).resolve()
    require(Path(asset_dir).resolve() == root / ASSETS, "V36 asset directory mismatch")
    return root


def history_module(root):
    path = regular(root, HISTORY)
    require(digest(path.read_bytes()) == HISTORY_SHA256, "V36 history helper drift")
    spec = importlib.util.spec_from_file_location("_authenticated_v36_history", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def proof_document(root):
    raw = regular(root, PROOF).read_bytes()
    require(digest(raw) == PROOF_SHA256, "V36 proof seal drift")
    proof = strict_json(raw)
    require(proof.get("schema") == "photo-camera-guidance-transition/v36"
            and proof.get("upstream_commit") == UPSTREAM_PIN
            and proof.get("reviewed_skill_sha256") == SKILL_SHA256
            and type(proof.get("data_improvement_count_delta")) is int
            and proof["data_improvement_count_delta"] == 0
            and proof.get("historical_comparison_control") == "observational_runtime_mismatch"
            and proof.get("doc_only_comparison_control") == "same_runtime", "V36 proof lineage or comparison attribution drift")
    return proof


def load_proof(source_root):
    return proof_document(Path(source_root).resolve())


def verify_files(root, mapping, label, count=None):
    require(isinstance(mapping, dict) and (count is None or len(mapping) == count), "V36 " + label + " inventory drift")
    for name, expected in mapping.items():
        require(isinstance(expected, str) and HASH.fullmatch(expected), "V36 invalid " + label + " digest")
        require(digest(regular(root, name).read_bytes()) == expected, "V36 " + label + " bytes drift: " + name)


def active_shards(snapshot):
    result = {}
    for filename in ("photo_prompt_semantic_index.json", "photo_prompt_visual_profile_index.json"):
        manifest = strict_json(snapshot.payload(PHOTO + "/assets/" + filename))
        require(isinstance(manifest.get("shards"), list), "V36 invalid active shard manifest")
        for row in manifest["shards"]:
            require(isinstance(row.get("path"), str) and isinstance(row.get("sha256"), str)
                    and HASH.fullmatch(row["sha256"]), "V36 invalid shard registration")
            name = PHOTO + "/assets/" + row["path"]
            require(name not in result, "V36 duplicate shard registration")
            result[name] = row["sha256"]
    require(len(result) == 32, "V36 active shard count drift")
    return result


def verify_shards(root, claimed, upstream, original):
    require(claimed == active_shards(upstream), "V36 current shards differ from exact upstream registration")
    previous = active_shards(original.original)
    require(previous == original.proof["active_shards_after"], "V36 original shard registration drift")
    for name, sha256 in previous.items():
        original.original.payload(name, sha256=sha256)
    verify_files(root, claimed, "active shards", 32)


def verify_command(command, old):
    require(isinstance(command, list) and all(isinstance(x, str) for x in command), "V36 command shape drift")
    require(old.count("--output-file") == command.count("--output-file") == 1, "V36 output option drift")
    index = old.index("--output-file") + 1
    require(len(command) == len(old) and index < len(command) and command[index]
            and command[:index] == old[:index] and command[index + 1:] == old[index + 1:]
            and command.count("--seed") == 1 and command[command.index("--seed") + 1] == "910000",
            "V36 frozen command/input/seed drift")


def pointer_parts(pointer):
    require(isinstance(pointer, str) and pointer.startswith("/0/")
            and not re.search(r"~(?![01])", pointer), "V36 invalid delta pointer")
    return [p.replace("~1", "/").replace("~0", "~") for p in pointer[1:].split("/")]


def pointer_get(value, parts):
    for part in parts:
        if isinstance(value, list):
            require(re.fullmatch(r"0|[1-9][0-9]*", part) and int(part) < len(value), "V36 delta list index drift")
            value = value[int(part)]
        else:
            require(isinstance(value, dict) and part in value, "V36 delta path absent")
            value = value[part]
    return value


def apply_delta(original, changes):
    require(isinstance(changes, list), "V36 delta shape drift")
    expected, seen = copy.deepcopy(original), set()
    for row in changes:
        require(isinstance(row, dict) and row.get("operation") in ("replace", "add"), "V36 unsupported delta operation")
        operation, path = row["operation"], row.get("pointer")
        require(set(row) == {"operation", "pointer", "after"} | ({"before"} if operation == "replace" else set()), "V36 delta fields drift")
        parts = pointer_parts(path)
        require(path in REVIEWED_POINTERS, "V36 unreviewed delta pointer: " + path)
        require(path not in seen and not any(path.startswith(p + "/") or p.startswith(path + "/") for p in seen), "V36 duplicate/overlapping delta")
        seen.add(path)
        parent, key = pointer_get(expected, parts[:-1]), parts[-1]
        require(isinstance(parent, dict), "V36 delta must change an object member")
        if operation == "replace":
            require(key in parent and same(parent[key], row["before"]), "V36 delta BEFORE drift: " + path)
            require(not same(parent[key], row["after"]), "V36 redundant delta")
        else:
            require(key not in parent, "V36 ADD requires a fresh key: " + path)
        parent[key] = copy.deepcopy(row["after"])
    return expected


def preserved_surfaces(old, current):
    for field in PRESERVED_FIELDS:
        require(field in old and field in current and same(old[field], current[field]), "V36 protected surface drift: " + field)
    require(current["provenance"]["seed"] == old["provenance"]["seed"] == 910000, "V36 frozen seed drift")


def qualify_pack(proof, baseline, pack, raw, original_raw, unedited_raw):
    require(digest(original_raw) == V35_PACK_SHA256, "V36 original pack anchor drift")
    require(same(strict_json(raw), [pack]), "V36 pack JSON shape drift")
    require(digest(unedited_raw) == UPSTREAM_PACK_SHA256, "V36 unedited latest pack anchor drift")
    require(raw == unedited_raw, "V36 documentation pack differs from unedited latest bytes")
    require(proof.get("reviewed_doc_only_pack_delta") == [], "V36 documentation-only delta must be empty")
    changes = proof.get("reviewed_upstream_pack_delta")
    require(digest(canonical(changes)) == REVIEWED_DELTA_SHA256, "V36 exact reviewed delta seal drift")
    original = strict_json(original_raw)
    expected = apply_delta(original, changes)
    preserved_surfaces(original[0], pack)
    require(same(expected, [pack]), "V36 entire pack contains unreviewed semantics")
    count = sum(len(slot["candidates"]) for slot in pack["slots"].values())
    require(digest(raw) == proof.get("current_pack_sha256") == baseline.get("sha256")
            and pack["pack_id"] == proof.get("current_pack_id") == baseline.get("pack_id")
            and count == proof.get("preserved_public_candidate_count") == baseline.get("public_candidate_count"), "V36 pack descriptor binding drift")


def qualification_context(root, baseline=None):
    proof, history = proof_document(root), history_module(root)
    original = history.ExactV35Sources(root)
    require(proof.get("previous_manifest_sha256") == V35_BASELINE_SHA256
            and proof.get("previous_pack_sha256") == V35_PACK_SHA256, "V36 original descriptor anchors drift")
    old = strict_json(original.retained_payload(V35_BASELINE, V35_BASELINE_SHA256))
    previous_raw = original.retained_payload(V35_PACK, V35_PACK_SHA256)
    mapping = proof.get("source_files_after")
    original.verify_live_sources(mapping)
    upstream = history.GitSnapshot(root, UPSTREAM_PIN)
    for name, sha256 in mapping.items():
        require(sha256 == (SKILL_SHA256 if name == SKILL else digest(upstream.payload(name))), "V36 source exceeds exact upstream/documentation scope: " + name)
    require(mapping.get(SKILL) == SKILL_SHA256, "V36 reviewed SKILL binding drift")
    verify_shards(root, proof.get("active_shards_after"), upstream, original)
    historical = proof.get("historical_baselines")
    names = {p for p in original.original.paths(ASSETS)
             if re.fullmatch(re.escape(ASSETS) + r"/photo_regression_baseline_v[0-9]+(?:_pack|_religion_iconography)?\.json", p)}
    require(isinstance(historical, dict) and set(historical) == names and len(names) == 63, "V36 original baseline inventory drift")
    for name, sha256 in historical.items():
        require(digest(original.retained_payload(name)) == sha256, "V36 original baseline binding drift")
    verify_files(root, historical, "historical baselines", 63)
    require(proof.get("frozen_inputs") == old["frozen_inputs"] == original.proof["frozen_inputs"], "V36 frozen input inventory drift")
    verify_files(root, proof["frozen_inputs"], "frozen inputs", 4)
    verify_files(root, proof.get("evidence_files"), "evidence")
    for key in ("unedited_upstream_pack_path", "baseline_composed_path", "runtime_request_path"):
        require(proof.get(key) in proof["evidence_files"], "V36 required evidence unbound: " + key)
    require(proof["evidence_files"][proof["unedited_upstream_pack_path"]] == UPSTREAM_PACK_SHA256, "V36 latest evidence anchor drift")
    old_descriptor = original.original.payload(DESCRIPTOR)
    old_hash = history.VALIDATOR_SHA256.encode()
    require(old_descriptor.count(old_hash) == 1 and regular(root, DESCRIPTOR).read_bytes()
            == old_descriptor.replace(old_hash, digest(regular(root, VALIDATOR).read_bytes()).encode(), 1), "V36 universal descriptor changed beyond validator binding")
    actual = strict_json(regular(root, ASSETS + "/photo_regression_baseline_v36.json").read_bytes())
    require(baseline is None or same(baseline, actual), "V36 supplied baseline differs from committed descriptor")
    require(actual.get("schema") == "photo_regression_baseline/v36", "V36 schema drift")
    require(actual.get("camera_guidance_transition") == {"evidence_path": PROOF, "evidence_sha256": PROOF_SHA256, "upstream_commit": UPSTREAM_PIN}, "V36 transition binding drift")
    require(actual.get("historical_baseline") == {"path": "photo_regression_baseline_v35.json", "schema": "photo_regression_baseline/v35", "sha256": V35_BASELINE_SHA256}, "V36 predecessor binding drift")
    for field in PRESERVED_BASELINE_FIELDS:
        require(same(actual.get(field), old[field]), "V36 protected descriptor field drift: " + field)
    verify_command(actual.get("command"), old["command"])
    return proof, actual, previous_raw


def qualify_current(root, baseline, pack, raw, *, asset_dir=None):
    root = bound_root(asset_dir or Path(root) / ASSETS, root)
    proof, baseline, original_raw = qualification_context(root, baseline)
    require(raw == regular(root, ASSETS + "/photo_regression_baseline_v36_pack.json").read_bytes(), "V36 CLI bytes differ from committed pack")
    qualify_pack(proof, baseline, pack, raw, original_raw, regular(root, proof["unedited_upstream_pack_path"]).read_bytes())
    return proof


def current_environment():
    return {"implementation": sys.implementation.name, "python": list(sys.version_info[:3]), "unicode": unicodedata.unidata_version}


RUNTIME_IDENTITY_FIELDS = ("generation_id", "source_fingerprint", "algorithm_sha256")
# Seals cover each complete environment/identity row, not interchangeable fields.
VERIFIED_RUNTIME_RECORDS = {
    ("cpython", (3, 12, 14), "15.0.0"): "60d44679dbe24a3232943d6632949432d57cc29e36fe236e90a409979cb70bcf",
    ("cpython", (3, 14, 3), "16.0.0"): "4490b2c9add46d024d7998c84a8c00bbc077940b77004171cd7fd0e71119b726",
}
REFERENCE_RUNTIME = ("cpython", (3, 12, 14), "15.0.0")


def environment_key(environment):
    require(type(environment) is dict and set(environment) == {"implementation", "python", "unicode"},
            "V36 runtime environment shape drift")
    version = environment["python"]
    require(type(environment["implementation"]) is str and type(environment["unicode"]) is str
            and type(version) is list and len(version) == 3 and all(type(part) is int for part in version),
            "V36 runtime environment types drift")
    return environment["implementation"], tuple(version), environment["unicode"]


def selected_runtime_record(proof):
    rows = proof.get("verified_runtime_environments")
    require(type(rows) is list and len(rows) == len(VERIFIED_RUNTIME_RECORDS), "V36 verified runtime inventory drift")
    records, identities = {}, {field: set() for field in RUNTIME_IDENTITY_FIELDS}
    for row in rows:
        require(type(row) is dict and set(row) == {"environment", *RUNTIME_IDENTITY_FIELDS}, "V36 runtime record fields drift")
        key = environment_key(row["environment"])
        require(key in VERIFIED_RUNTIME_RECORDS, "V36 unverified runtime environment")
        require(key not in records, "V36 duplicate runtime environment")
        for field in RUNTIME_IDENTITY_FIELDS:
            value = row[field]
            require(type(value) is str and HASH.fullmatch(value), "V36 invalid runtime identity: " + field)
            require(value not in identities[field], "V36 duplicate runtime identity: " + field)
            identities[field].add(value)
        require(digest(canonical(row)) == VERIFIED_RUNTIME_RECORDS[key], "V36 runtime record seal drift")
        records[key] = row
    require(set(records) == set(VERIFIED_RUNTIME_RECORDS), "V36 verified runtime inventory drift")
    reference = {field: proof.get(field) for field in ("environment", *RUNTIME_IDENTITY_FIELDS)}
    require(same(reference, records[REFERENCE_RUNTIME]), "V36 reference runtime identity drift")
    key = environment_key(current_environment())
    require(key in records, "V36 exact runtime environment unavailable")
    return copy.deepcopy(records[key])


def qualify_snapshot(root, baseline, pack, raw, receipt, *, runtime_store):
    root = Path(root).resolve()
    proof = qualify_current(root, baseline, pack, raw)
    require(runtime_store is not None and Path(runtime_store).is_dir(), "V36 explicit runtime store unavailable")
    record = selected_runtime_record(proof)
    require(isinstance(receipt, dict) and all(receipt.get(k) == record[k] for k in RUNTIME_IDENTITY_FIELDS), "V36 receipt identity drift")
    scripts = root / PHOTO / "scripts"
    sys.path.insert(0, str(scripts))
    try:
        import photo_runtime_sources as runtime
        import audit_composed_prompt as composed_audit
        import audit_image_render_request as render_audit
        for module in (runtime, composed_audit, render_audit):
            require(Path(module.__file__).resolve().parent == scripts, "V36 production module root mismatch")
        provider = runtime.RuntimeSnapshotProvider(root / PHOTO, Path(runtime_store))
        snapshot = provider.from_receipt(pack, receipt)
        captured, _ = runtime.capture_sources(root / PHOTO)
        require(same(captured, snapshot.manifest["source"]), "V36 live source differs from receipt generation")
        require(snapshot.generation_id == record["generation_id"] and all(snapshot.manifest[k] == record[k] for k in ("source_fingerprint", "algorithm_sha256"))
                and same(snapshot.manifest["source"]["environment"], record["environment"]), "V36 snapshot identity drift")
        composed = strict_json(regular(root, proof["baseline_composed_path"]).read_bytes())
        request_path = regular(root, proof["runtime_request_path"])
        request = strict_json(request_path.read_bytes())
        require(composed["prompt_en"] == pack["authorial_core"]["baseline_prompt_en"]
                and composed["prompt_en"] in request["runtime_prompt_en"], "V36 baseline prompt changed")
        result = composed_audit.audit_composed_prompt(pack, composed, runtime_receipt=receipt, runtime_store=Path(runtime_store))
        request_result = render_audit.audit_image_render_request(pack, composed, request, request_path=request_path)
        require(result.get("status") == request_result.get("status") == "pass", "V36 production audits failed: " + json.dumps({"composed": result, "runtime": request_result}))
    finally:
        sys.path.pop(0)
    return {"status": "pass", "schema": baseline["schema"], "historical_sha256": V35_BASELINE_SHA256,
            "sha256": digest(raw), "pack_id": pack["pack_id"], "generation_id": snapshot.generation_id,
            "private_runtime_receipt": copy.deepcopy(receipt)}


GUARDED_CHILD = r'''
import os, runpy, sys
from pathlib import Path
root, target, output, store = map(Path, sys.argv[1:5])
arguments = sys.argv[5:]
assert sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
assert set(os.environ) <= {'PATH','LANG','LC_ALL','TZ','PHOTO_RUNTIME_STORE'}
assert Path(os.environ['PHOTO_RUNTIME_STORE']) == store
def deny(reason): raise RuntimeError('V36 guard denied: ' + reason)
def normalized(value, dir_fd=None):
    path = Path(os.fsdecode(value))
    if not path.is_absolute() and isinstance(dir_fd, int) and dir_fd >= 0:
        path = Path(os.readlink('/proc/self/fd/' + str(dir_fd))) / path
    return path.resolve()
def check_write(value, dir_fd=None):
    path = normalized(value, dir_fd)
    if not path.is_relative_to(output.parent): deny('write outside isolated output')
    if path.is_relative_to(store):
        parts = path.relative_to(store).parts
        if parts and parts[0] not in {'receipts','receipt-index'} and path.name != 'LOCK': deny('immutable runtime mutation')
def audit(event, args):
    if event.startswith('socket.') or event in {'subprocess.Popen','os.system','os.posix_spawn','os.fork','os.exec','pty.spawn'}: deny(event)
    if event == 'import' and args[0].split('.')[0] in {'google','openai','requests','httpx','aiohttp','keyring','dotenv'}: deny('provider/credential import')
    if event == 'open' and isinstance(args[0], (str, bytes)):
        path = normalized(args[0])
        if path.name in {'.env','.netrc','.npmrc','credentials'} or '.ssh' in path.parts or '.aws' in path.parts: deny('credential file access')
        flags = args[2] if isinstance(args[2], int) else 0
        if flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND): check_write(args[0])
    if event in {'os.mkdir','os.remove','os.rmdir','os.chmod','os.utime','os.truncate'} and isinstance(args[0], (str, bytes)):
        if event == 'os.mkdir' and normalized(args[0], args[-1]).is_dir(): return
        check_write(args[0], args[-1] if isinstance(args[-1], int) else None)
    if event in {'os.rename','os.link'}:
        check_write(args[0], args[2] if len(args) > 2 else None)
        check_write(args[1], args[3] if len(args) > 3 else None)
    if event == 'os.symlink': deny('symlink creation')
def profile(frame, event, arg):
    if event != 'call': return
    module, name = frame.f_globals.get('__name__',''), frame.f_code.co_name
    if module in {'build_semantic_index','build_visual_profile_index','generate_images_via_api','photo_api_render','sync_photo_runtime_source'} and name not in {'<module>','<dictcomp>','<listcomp>','<lambda>'}: deny('provider/key function')
    if name in {'get_gemini_api_key','cached_gemini_client','embed_texts_with_gemini','embed_single_semantic_text','load_api_key','call_api'}: deny('provider/key function')
    if module == 'photo_runtime_sources' and name in {'publish','fetch','source_update','complete_source_update'}: deny('publisher/fetch fallback')
    if module == 'core_slot_index_storage' and name == 'create': deny('cache creation')
    if module == 'prompt_generator' and name == 'build_core_slot_index': deny('lexical cache fallback')
sys.addaudithook(audit)
sys.setprofile(profile)
sys.path.insert(0, str(root/'skills/photo-prompt-image-generator/scripts'))
sys.argv = [str(target), *arguments]
runpy.run_path(str(target), run_name='__main__')
'''


def copy_runtime(source, target, root, proof):
    record = selected_runtime_record(proof)
    source = Path(source).resolve()
    require(source.is_dir() and not target.exists(), "V36 existing runtime or isolated destination unavailable")
    for path in source.rglob("*"):
        require(not path.is_symlink(), "V36 runtime symlink")
    shutil.copytree(source, target)
    require((target / "generations" / record["generation_id"]).is_dir(), "V36 published generation unavailable")
    namespace = digest(canonical({"root": str(root / PHOTO), "mode": "local_current", "remote": ""}))
    pointer = strict_json(regular(target, "local/" + namespace + "/CURRENT.json").read_bytes())
    require(pointer.get("generation_id") == record["generation_id"] and pointer.get("source_fingerprint") == record["source_fingerprint"], "V36 source-root runtime pointer drift")


def validate_current(asset_dir, *, source_root, runtime_store=None):
    root = bound_root(asset_dir, source_root)
    proof, baseline, original_raw = qualification_context(root)
    raw = regular(root, ASSETS + "/photo_regression_baseline_v36_pack.json").read_bytes()
    payload = strict_json(raw)
    require(isinstance(payload, list) and len(payload) == 1, "V36 committed pack shape drift")
    qualify_pack(proof, baseline, payload[0], raw, original_raw, regular(root, proof["unedited_upstream_pack_path"]).read_bytes())
    source_store = runtime_store or os.environ.get("PHOTO_RUNTIME_STORE")
    require(source_store is not None, "V36 requires an explicit existing PHOTO_RUNTIME_STORE")
    selected_runtime_record(proof)
    with tempfile.TemporaryDirectory(prefix="photo-v36-current-") as temporary:
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
        require(result.returncode == 0, "V36 public CLI failed: " + result.stdout + result.stderr)
        actual = output.read_bytes()
        packs = strict_json(actual)
        require(isinstance(packs, list) and len(packs) == 1, "V36 CLI pack shape drift")
        receipt = strict_json(Path(str(output) + ".runtime-receipt.json").read_bytes())
        return qualify_snapshot(root, baseline, packs[0], actual, receipt, runtime_store=store)


def dispatch(asset_dir, *, source_root, baseline_version=None):
    root = bound_root(asset_dir, source_root)
    if baseline_version is None or (type(baseline_version) is int and baseline_version == 36):
        return validate_current(asset_dir, source_root=root)
    require(type(baseline_version) is int and baseline_version in range(6, 36), "Unsupported V36 version")
    proof = proof_document(root)
    return history_module(root).dispatch_historical(asset_dir, source_root=root,
            baseline_version=baseline_version, source_files_after=proof["source_files_after"])


def dispatch_historical(asset_dir, *, source_root, baseline_version):
    root = bound_root(asset_dir, source_root)
    require(type(baseline_version) is int and baseline_version in range(6, 36), "Unsupported historical V36 dispatch version")
    return dispatch(asset_dir, source_root=root, baseline_version=baseline_version)
