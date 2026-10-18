"""Dispatch new managed runs to an installed, sealed H-only/F2 release.

The release carries its own code and candidate snapshots. CURRENT and the
working source corpus remain independent. No research checkout is consulted.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

SCHEMA = "photo-installed-h-f2/v1"
SKILL_ROOT = Path(__file__).resolve().parents[1]
CONFIG = "retrieval-runtime.json"


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def file_sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def default_store():
    configured = os.environ.get("PHOTO_RUNTIME_STORE")
    base = Path(configured).expanduser() if configured else Path(os.environ.get(
        "XDG_CACHE_HOME", str(Path.home() / ".cache"))) / "image-prompt/photo-shared-runtime"
    return base / "h-f2-installed"


def release(store, generation_id, *, full=False):
    """Verify the executable closure before running any release code."""
    import re
    require(isinstance(generation_id, str) and re.fullmatch(r"[0-9a-f]{64}", generation_id), "invalid H-F2 generation")
    store = Path(store).resolve()
    root = store / "h-f2-generations" / generation_id
    manifest = read(root / "manifest.json")
    require(digest(manifest) == generation_id and manifest["schema"] == "photo-h-f2-generation/v1", "H-F2 manifest changed")
    native_id = manifest["native_generation_id"]
    require(isinstance(native_id, str) and re.fullmatch(r"[0-9a-f]{64}", native_id), "invalid native generation")
    native = store / "generations" / native_id
    native_manifest = read(native / "manifest.json")
    require(digest(native_manifest) == native_id and native_manifest["schema"] == "photo-runtime-generation/v3", "native manifest changed")
    require(native_manifest["search_layout"]["corpus_sha256"] == read(root / "source-manifest.json")["source_sha256"], "mixed candidate pools")
    for base, members in ((root, manifest["files"]), (native, native_manifest["members"])):
        for relative, row in members.items():
            path = base / relative
            require(not Path(relative).is_absolute() and ".." not in Path(relative).parts and path.is_file() and not path.is_symlink(), "missing or unsafe release member")
            if full or relative in native_manifest["source"]["code"]:
                expected = row["sha256"] if isinstance(row, dict) else row
                require(file_sha(path) == expected, "release member changed: " + relative)
    code = {str(p.relative_to(native)): file_sha(p) for directory in ("scripts", "precore")
            for p in sorted((native / directory).glob("*.py"))}
    require(code == native_manifest["source"]["code"], "release executable closure changed")
    return native, manifest, native_manifest


def option(arguments, name):
    """Read one non-abbreviated argparse option without interpreting its value."""
    values = []
    for i, item in enumerate(arguments):
        if item == name:
            require(i + 1 < len(arguments), "missing value: " + name)
            values.append(arguments[i + 1])
        elif item.startswith(name + "="):
            values.append(item.split("=", 1)[1])
    require(len(values) <= 1, "duplicate option: " + name)
    return values[0] if values else None


def runtime_python(skill_root, manifest):
    """Use the skill-owned, proof-bound local runtime, including NumPy."""
    skill_root = Path(skill_root).resolve()
    lock = read(skill_root / "embedding-runtime.lock.json")
    binding = manifest["binding"]
    require(lock["schema"] == "photo-local-embedding-installation/v1"
            and lock["space"]["provider"] == "embeddinggemma2-local"
            and digest(lock) == binding["installation_hash"]
            and lock["space"] == binding["space"], "installed local model differs from release")
    require(file_sha(skill_root / "scripts/photo_local_embedding.py") == binding["worker_sha256"], "local worker changed")
    python = skill_root / lock["python"]
    require(python.is_file(), "skill-owned local Python runtime missing")
    return python


def dispatch(argv=None, *, skill_root=SKILL_ROOT):
    """Return a CLI exit code, or None for an already bound native run."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    try:
        config = read(Path(skill_root) / CONFIG)
        require(config["schema"] == SCHEMA and config["policy"] == "photo-h-f2/v1"
                and config["store_subdirectory"] == "h-f2-installed", "invalid installed search configuration")
        state = {}
        run = option(arguments, "--run")
        if run and (Path(run) / "workflow.json").is_file():
            state = read(Path(run) / "workflow.json")
        # Existing native receipts keep their original implementation and source.
        # Every new frozen/authored run takes the installed H-F2 path.
        if "pack" in state.get("artifacts", {}) and not state.get("h_f2_binding"):
            return None
        bound = state.get("h_f2_binding")
        explicit_store = option(arguments, "--runtime-store")
        explicit_id = option(arguments, "--generation-id")
        if bool(explicit_store) != bool(explicit_id):
            raise ValueError("supply both generation and store, or omit both for the installed default")
        store = Path(explicit_store or (bound or {}).get("store") or default_store())
        generation_id = explicit_id or (bound or {}).get("generation_id") or config["generation_id"]
        native, manifest, native_manifest = release(store, generation_id)
        if not bound and not explicit_id:
            require(manifest["native_generation_id"] == config["native_generation_id"]
                    and digest(native_manifest["source"]["code"]) == config["code_sha256"], "installed release binding changed")
        if arguments and arguments[0] in {"retrieve", "resume"}:
            policy = option(arguments, "--retrieval-policy")
            require(policy in (None, "h-f2"), "the installed default requires H-F2")
            if policy is None:
                arguments += ["--retrieval-policy", "h-f2"]
            if not explicit_id:
                arguments += ["--generation-id", generation_id, "--runtime-store", str(store)]
            if option(arguments, "--local-embedding-skill") is None:
                arguments += ["--local-embedding-skill", str(Path(skill_root).resolve())]
        env = dict(os.environ, HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1",
                   HF_HUB_DISABLE_TELEMETRY="1", PYTHONNOUSERSITE="1")
        env.pop("PYTHONPATH", None)
        stripped_keys = ["GEMINI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY"]
        if not arguments or arguments[0] != "render-api":
            stripped_keys.append("OPENAI_API_KEY")
        for key in stripped_keys:
            env.pop(key, None)
        launcher = ("import sys,runpy;from pathlib import Path;"
                    "entry=sys.argv.pop(1);sys.path.insert(0,str(Path(entry).parent));"
                    "runpy.run_path(entry,run_name='__main__')")
        return subprocess.run([str(runtime_python(skill_root, manifest)), "-I", "-c", launcher,
                               str(native / "scripts/photo_workflow.py"), *arguments], env=env).returncode
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"status": "error", "code": "installed_h_f2_unavailable",
                          "detail": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
