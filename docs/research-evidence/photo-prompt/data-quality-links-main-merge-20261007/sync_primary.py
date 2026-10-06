"""Fast-forward the primary checkout without discarding unrelated authored work."""
from pathlib import Path
import gc
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile

E = Path(__file__).resolve().parent
W = E.parents[3]
P = Path("/Users/chasoik/Projects/image-prompt")
S = Path("skills/photo-prompt-image-generator")
STORE = Path.home() / ".cache/image-prompt/photo-runtime"
BACKUP = Path.home() / ".cache/image-prompt/data-links-merge-primary-backup-20261007"
BASE = "96e20422316276a4e0b5ed97f44152e4931e7504"
LOCAL = "d9dc3df7012f395c48d536ee9df80df060cd24f9"


def git(*args, cwd=P):
    return subprocess.check_output(["git", *args], cwd=cwd)


def save(name, value):
    (E / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def backup(name):
    source, dest = P / name, BACKUP / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        assert sha(dest) == sha(source), ("Existing backup differs", name)
    else:
        shutil.copy2(source, dest)
    return {"sha256": sha(source), "mode": stat.S_IMODE(source.stat().st_mode), "backup": str(dest)}


before = json.loads((E / "PRIMARY-PREFLIGHT.json").read_text())
target = git("rev-parse", "HEAD", cwd=W).decode().strip()
assert git("rev-parse", "origin/main").decode().strip() == target
assert git("branch", "--show-current").decode().strip() == "main"
assert git("rev-parse", "HEAD").decode().strip() == before["head"]
assert not git("diff", "--cached", "--name-only").strip(), "Concurrent staged work exists"
incoming = set(git("diff", "--name-only", "-z", before["head"], target).decode().split("\0")) - {""}
dirty = set(git("diff", "--name-only", "-z").decode().split("\0")) - {""}
untracked = set(git("ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")) - {""}
derived = {str(S / "assets" / name) for name in ["photo_prompt_semantic_index.json", "photo_prompt_visual_profile_index.json"]}
owned_tracked = derived | {str(S / "assets" / name) for name in [
    "photo_prompt_photorealism_elements_extension.json", "photo_prompt_realistic_background_extension.json",
    "photo_prompt_visual_obligations.json"]} | {"tests/test_photo_instrument_semantics.py"}
overlap = dirty & incoming
assert overlap <= owned_tracked, ("Unexpected dirty tracked overlap", sorted(overlap - owned_tracked))
adoptions = []
ref_updates = {str(S / "assets" / name) for name in [
    "photo_prompt_photorealism_elements_extension.json", "photo_prompt_realistic_background_extension.json"]}
for name in overlap - derived:
    raw, final = (P / name).read_bytes(), git("show", target + ":" + name)
    if raw != final:
        assert name in ref_updates, ("Concurrent authored edit overlaps incoming change", name)
        existing, desired = json.loads(raw), json.loads(final)
        prior_ref = json.loads(git("show", LOCAL + ":" + name))["maintenance_ref"]
        assert existing["maintenance_ref"] in (prior_ref, desired["maintenance_ref"]), ("Concurrent maintenance reference edit", name)
        existing["maintenance_ref"] = desired["maintenance_ref"]
        assert existing == desired, ("Authored differences exceed the reviewed maintenance reference update", name)
        adoptions.append(name)

owned_local = set(git("diff", "--name-only", "-z", BASE, LOCAL, cwd=W).decode().split("\0")) - {""}
collisions = sorted(untracked & incoming)
local_notes = {}
for name in collisions:
    path = P / name
    assert not path.is_symlink() and path.is_file(), ("Collision is not a regular file", name)
    raw = path.read_bytes()
    if raw != git("show", target + ":" + name):
        if name == 'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':
            assert sha(path) == before['files'][name]['sha256'], 'Local qualification note changed since preflight'
            prefix, remainder = raw.split(b'\n\n', 1)
            assert remainder == git('show', target + ':' + name), 'Difference exceeds the existing local qualification note'
            local_notes[name] = raw
            continue
        assert name in owned_local and raw == git("show", LOCAL + ":" + name), ("Untracked file changed outside the reviewed task", name)
        adoptions.append(name)

presync = {}
for name in sorted(dirty | untracked):
    path = P / name
    assert path.is_file() and not path.is_symlink(), ("Non-regular preservation file", name)
    presync[name] = {"sha256": sha(path), "bytes": path.stat().st_size, "mode": stat.S_IMODE(path.stat().st_mode),
                     "tracked_dirty": name in dirty}
concurrent = sorted(name for name, row in before["files"].items() if name in presync and row["sha256"] != presync[name]["sha256"])
save("PRIMARY-PRESYNC.json", {"schema": "photo-data-links-primary-presync/v1", "head": before["head"],
    "target": target, "files": presync, "concurrent_updates_since_first_observation": concurrent})
backups = {name: backup(name) for name in sorted(overlap | set(collisions))}
for name in sorted(derived):
    backup(name)
    for shard in json.loads((P / name).read_text())["shards"]:
        backup(str(Path(name).parent / shard["path"]))
save("PRIMARY-OVERLAP-BACKUP.json", {"files": backups, "owned_canonical_adoptions": adoptions})

os.environ["PHOTO_RUNTIME_STORE"] = str(STORE)
sys.path.insert(0, str(P / S / "scripts"))
from photo_runtime_sources import source_update, SnapshotPublisher
import prompt_generator as pg
import build_semantic_index as semantic
import build_visual_profile_index as visual


def denied(*args, **kwargs):
    raise AssertionError("No embedding calls allowed; exact cached vectors required")


semantic.embed_texts_with_gemini = denied
visual.embed_texts_with_gemini = denied
semantic.load_project_env = lambda: None
visual.load_project_env = lambda: None


def no_network(event, args):
    if event in {"socket.connect", "socket.getaddrinfo"}:
        raise AssertionError("Offline primary rebuild attempted network access")


sys.addaudithook(no_network)
with source_update(P / S, STORE):
    assert all(sha(P / name) == row["sha256"] for name, row in backups.items()), "An incoming path changed during preparation"
    merged = False
    try:
        for name in sorted(overlap):
            (P / name).write_bytes(git("show", before["head"] + ":" + name))
        for name in collisions:
            (P / name).unlink()
        git("merge", "--ff-only", "origin/main")
        merged = True
        for name, raw in local_notes.items():
            (P / name).write_bytes(raw)
        for name, row in presync.items():
            if name not in derived and sha(P / name) == row['sha256']:
                (P / name).chmod(row['mode'])
    finally:
        if not merged:
            for name, row in backups.items():
                shutil.copy2(row["backup"], P / name)
    assets = P / S / "assets"
    sem, vis = assets / "photo_prompt_semantic_index.json", assets / "photo_prompt_visual_profile_index.json"
    old_sem, old_vis = BACKUP / S / "assets" / sem.name, BACKUP / S / "assets" / vis.name
    metadata = json.loads(sem.read_text())
    provider, model, dimensions = (metadata[key] for key in ["provider", "embedding_model", "embedding_dimensions"])
    data = pg.load_json(assets / "photo_prompt_tags.json")
    registry = pg.load_visual_obligation_registry(assets / "photo_prompt_visual_obligations.json")
    vectors = visual.reusable_vectors([old_vis, W / S / "assets" / vis.name], registry, provider=provider, model=model, dimensions=dimensions)
    assert len(vectors) == len(registry["profiles"]), "Uncached working visual profile"
    visual.write_payload(vis, visual.build_visual_profile_index_payload(registry, vectors=vectors, provider=provider, model=model, dimensions=dimensions))
    visual_count = len(registry["profiles"])
    del vectors
    gc.collect()
    expected = semantic.base_payload(data, provider, model, dimensions)
    wanted = {key: pg.semantic_text_for_entry(entry, slot, kind=kind) for key, kind, entry, slot in semantic.iter_semantic_entries(data)}
    compatible = {}
    for path in [old_sem, W / S / "assets" / sem.name]:
        payload = pg.load_semantic_index_payload(path)
        assert semantic.metadata_matches(payload, expected, require_dictionary_hash=False)
        for key, row in payload["entries"].items():
            if key in wanted and row.get("text") == wanted[key] and len(row.get("vector", [])) == dimensions:
                compatible[key] = row
        del payload
        gc.collect()
    assert set(wanted) <= set(compatible), ("Missing exact working vectors", sorted(set(wanted) - set(compatible)))
    with tempfile.TemporaryDirectory(prefix="data-links-primary-index-") as temporary:
        checkpoint = Path(temporary) / "working.partial.json"
        checkpoint.write_text(json.dumps({**expected, "entries": compatible}, ensure_ascii=False, separators=(",", ":")))
        del compatible
        gc.collect()
        payload = semantic.build_resumable_index_payload(data, output=sem, checkpoint=checkpoint, provider=provider, model=model,
            dimensions=dimensions, batch_size=1, request_interval=0, retry_attempts=1, retry_initial_delay=0)
        semantic_count = len(payload["entries"])
        semantic.write_sharded_payload(sem, payload, shard_count=16, keep_stale_generations=True)
        del payload
        gc.collect()
    pg.validate_semantic_index_metadata(pg.load_semantic_index_payload(sem), data)
    pg.validate_visual_profile_index_metadata(pg.load_visual_profile_index_payload(vis), registry)
pointer = SnapshotPublisher(P / S, STORE).publish()
changed = [name for name, row in presync.items() if name not in derived and sha(P / name) != row["sha256"]]
expected_changes = set(adoptions)
unexpected = sorted((set(changed) - expected_changes) & incoming)
concurrent_during_sync = sorted(set(changed) - expected_changes - incoming)
assert not unexpected, ("An incoming file changed during sync", unexpected)
assert all((P / name).is_file() for name in presync), "A preservation file disappeared"
assert all(stat.S_IMODE((P / name).stat().st_mode) == row["mode"] for name, row in presync.items()
           if name not in derived | expected_changes), "A preservation file mode changed"
assert git("rev-parse", "HEAD").decode().strip() == target
assert not git("diff", "--cached", "--name-only").strip()
report = {"schema": "photo-data-links-primary-sync/v1", "before_head": before["head"], "after_head": target,
    "presync_files": len(presync), "unrelated_files_preserved": len(set(presync) - incoming - derived),
    "unexpected_drift": unexpected, "owned_canonical_adoptions": adoptions,
    "owned_local_qualification_notes_preserved": sorted(local_notes),
    "concurrent_unrelated_updates_during_sync": concurrent_during_sync,
    "working_semantic_entries": semantic_count, "working_visual_profiles": visual_count,
    "runtime_generation": pointer["generation_id"], "embedding_calls": 0, "old_shards_removed": 0,
    "working_corpus_boundary": "Additional unrelated authored work remains local; qualified main generation is separate"}
save("PRIMARY-SYNC.json", report)
destination = P / E.relative_to(W)
destination.mkdir(parents=True, exist_ok=True)
(destination / "PRIMARY-SYNC.json").write_bytes((E / "PRIMARY-SYNC.json").read_bytes())
print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
