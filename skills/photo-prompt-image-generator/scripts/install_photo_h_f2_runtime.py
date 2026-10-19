"""Install an already qualified H-F2 release without writing any CURRENT.

All candidate, code and embedding members are verified and independently
copied. The installed config selects the release for new managed CLI runs.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from photo_installed_h_f2 import (CONFIG, SCHEMA, SKILL_ROOT, default_store,
                                digest, file_sha, read, release, require, runtime_python)


def install(source_store, generation_id, *, destination=None, skill_root=SKILL_ROOT):
    source_store = Path(source_store).resolve()
    destination = Path(destination or default_store()).resolve()
    native, manifest, native_manifest = release(source_store, generation_id, full=True)
    require(manifest["CID_count"] > 0 and manifest["RID_count"] >= manifest["CID_count"], "empty candidate release")
    before = {str(p): file_sha(p) for p in destination.parent.rglob("CURRENT.json")}
    destination.mkdir(parents=True, exist_ok=True)
    for parent, identifier in (("generations", manifest["native_generation_id"]),
                               ("h-f2-generations", generation_id)):
        target = destination / parent / identifier
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".install-", dir=target.parent) as tmp:
            staged = Path(tmp) / "release"
            shutil.copytree(source_store / parent / identifier, staged)
            # A copied tree is never executable authority until its full seal passes.
            source_manifest = read(staged / "manifest.json")
            require(digest(source_manifest) == identifier, "copy manifest changed")
            members = source_manifest.get("members", source_manifest.get("files"))
            for relative, row in members.items():
                require(file_sha(staged / relative) == (row["sha256"] if isinstance(row, dict) else row), "copy changed")
            os.rename(staged, target)
    installed, _, _ = release(destination, generation_id, full=True)
    # Native validation resolves model files relative to its sealed skill root.
    # Materialize those immutable data files; link only the skill-owned Python
    # environment, never a model package or any research checkout.
    lock = read(Path(skill_root) / "embedding-runtime.lock.json")
    runtime_python(skill_root, manifest)
    for relative, expected in lock["files"].items():
        source = Path(skill_root) / lock["package"] / relative
        target = installed / lock["package"] / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            temporary = target.with_name(target.name + ".partial")
            shutil.copyfile(source, temporary)
            require(file_sha(temporary) == expected["sha256"], "local model copy changed")
            os.replace(temporary, target)
        require(file_sha(target) == expected["sha256"], "installed local model changed")
    environment = installed / Path(lock["python"]).parents[1]
    expected_environment = (Path(skill_root) / Path(lock["python"]).parents[1]).resolve()
    if environment.is_symlink():
        require(environment.resolve() == expected_environment, "foreign local Python environment")
    else:
        require(not environment.exists(), "unexpected local Python environment")
        environment.parent.mkdir(parents=True, exist_ok=True)
        environment.symlink_to(expected_environment, target_is_directory=True)
    # Run the deployed implementation's own complete validators, not a facsimile.
    program = """import sys;sys.path.insert(0,sys.argv[1])
from photo_h_f2_generation import Generation
from photo_runtime_sources import RuntimeSnapshotProvider
g=Generation(sys.argv[2],sys.argv[3],full=True)
RuntimeSnapshotProvider(store=sys.argv[2]).load_generation(g.manifest['native_generation_id'])
print('deployed H-F2 and native validators PASS')
"""
    env = dict(os.environ, HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", PYTHONNOUSERSITE="1")
    env.pop("PYTHONPATH", None)
    for key in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        env.pop(key, None)
    check = subprocess.run([str(runtime_python(skill_root, manifest)), "-I", "-c", program, str(installed / "scripts"),
                            str(destination), generation_id], env=env, capture_output=True, text=True)
    require(check.returncode == 0, check.stderr)
    require({str(p): file_sha(p) for p in destination.parent.rglob("CURRENT.json")} == before, "CURRENT changed during install")
    config = {"schema": SCHEMA, "policy": "photo-h-f2/v1", "store_subdirectory": "h-f2-installed",
              "generation_id": generation_id, "native_generation_id": manifest["native_generation_id"],
              "code_sha256": digest(native_manifest["source"]["code"])}
    require(destination == default_store().resolve(), "default config must refer to the default installed store")
    path = Path(skill_root) / CONFIG
    temporary = path.with_suffix(".partial")
    temporary.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n")
    os.replace(temporary, path)
    return {"status": "pass", "store": str(destination), "generation_id": generation_id,
            "positive_CIDs": manifest["CID_count"], "RIDs": manifest["RID_count"],
            "CURRENT_writes": 0, "config": str(path)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-store", type=Path, required=True)
    parser.add_argument("--generation-id", required=True)
    args = parser.parse_args()
    print(json.dumps(install(args.source_store, args.generation_id), ensure_ascii=False, indent=2))
