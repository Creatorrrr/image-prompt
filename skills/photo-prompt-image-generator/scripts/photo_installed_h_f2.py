"""Dispatch new managed runs to an installed, sealed H-only/F2 release.

The release carries its own code and candidate snapshots. CURRENT and the
working source corpus remain independent. No research checkout is consulted.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

SCHEMA = "photo-installed-h-f2/v1"
SKILL_ROOT = Path(__file__).resolve().parents[1]
CONFIG = "retrieval-runtime.json"


class ExpressionDispatchError(ValueError):
    def __init__(self, code, **details):
        self.code = code
        self.details = details
        super().__init__(code)


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


def _flag(arguments, name):
    count = sum(item == name for item in arguments)
    require(count <= 1, "duplicate option: " + name)
    return count == 1


def _neutral_run_files(skill_root):
    """Load only the named neutral freeze verifier before any release read."""
    from importlib.util import module_from_spec, spec_from_file_location
    path = Path(skill_root) / "precore/photo_run_files.py"
    require(path.is_file() and not path.is_symlink(), "neutral_run_file_verifier_unavailable")
    directory = str(path.parent.resolve())
    added = directory not in sys.path
    if added:
        sys.path.insert(0, directory)
    try:
        spec = spec_from_file_location("_photo_expression_neutral_run_files", path)
        require(spec is not None and spec.loader is not None, "neutral_run_file_verifier_unavailable")
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if added:
            sys.path.remove(directory)


def _expression_config(skill_root):
    config = read(Path(skill_root) / CONFIG)
    require(config["schema"] == SCHEMA and config["policy"] == "photo-h-f2/v1"
            and config["store_subdirectory"] == "h-f2-installed", "invalid installed search configuration")
    return config


def _dispatch_expression_view(arguments, *, skill_root):
    """Verify a frozen authoring run before config, release, or candidate access."""
    run = option(arguments, "--run")
    maintenance = _flag(arguments, "--maintenance")
    explicit_store = option(arguments, "--runtime-store")
    explicit_id = option(arguments, "--generation-id")
    require(option(arguments, "--_resolved-runtime-store") is None
            and option(arguments, "--_resolved-generation-id") is None
            and option(arguments, "--_resolved-lookup-source") is None,
            "reserved_expression_view_option")

    state = None
    if maintenance:
        require(run is None, "maintenance_and_authoring_run_are_mutually_exclusive")
        require(bool(explicit_store) == bool(explicit_id),
                "maintenance_requires_store_and_generation_together")
        if explicit_store:
            store = Path(explicit_store).expanduser().resolve()
            generation_id = explicit_id
            resolution = "maintenance_explicit_override"
        else:
            config = _expression_config(skill_root)
            store = Path(default_store()).resolve()
            generation_id = config["generation_id"]
            resolution = "maintenance_current_configuration"
    else:
        require(run is not None, "authoring_requires_valid_frozen_run")
        require(explicit_store is None and explicit_id is None,
                "runtime_overrides_require_explicit_maintenance_mode")
        verifier = _neutral_run_files(skill_root)
        state = verifier.load_state(Path(run))
        if state.get("phase") in {"request_prepared", "controls_bound"} or "freeze_receipt" not in state.get("artifacts", {}):
            raise ValueError("pre_core_expression_lookup_blocked")
        if state.get("mode") not in {"prompt_only", "image"}:
            raise ValueError("authoring_requires_valid_frozen_run")
        if verifier.status(state).get("phase") == "stale":
            raise ValueError("stale_frozen_run")
        verifier.verify_freeze(state)
        if "retry_proof" in state.get("artifacts", {}):
            retry_path = Path(skill_root) / "scripts/prepare_retry_context.py"
            spec = importlib.util.spec_from_file_location("_photo_expression_retry_context", retry_path)
            require(spec is not None and spec.loader is not None, "retry_context_verifier_unavailable")
            retry_context = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(retry_context)
            retry_context.verify_child(state)
        bound = state.get("h_f2_binding") or {}
        if "pack" in state.get("artifacts", {}) and not bound:
            raise ValueError("legacy_run_has_no_h_f2_generation_binding")
        if bound:
            require(isinstance(bound, dict) and bound.get("store") and bound.get("generation_id"),
                    "invalid_run_h_f2_binding")
            store = Path(bound["store"]).resolve()
            generation_id = bound["generation_id"]
            resolution = "run_bound_generation"
        else:
            config = _expression_config(skill_root)
            store = Path(default_store()).resolve()
            generation_id = config["generation_id"]
            resolution = "current_installed_configuration"

    run_bound_generation_id = (state.get("h_f2_binding") or {}).get("generation_id") if state else None
    try:
        native, manifest, native_manifest = release(store, generation_id)
    except (ValueError, OSError, KeyError, TypeError) as error:
        raise ExpressionDispatchError("sealed_h2_generation_unavailable",
                                      lookup_generation_id=generation_id,
                                      run_bound_generation_id=run_bound_generation_id) from error
    if "scripts/photo_expression_view.py" not in native_manifest.get("source", {}).get("code", {}):
        raise ExpressionDispatchError("expression_view_not_in_bound_generation",
                                      lookup_generation_id=generation_id,
                                      run_bound_generation_id=run_bound_generation_id)
    if resolution in {"current_installed_configuration", "maintenance_current_configuration"}:
        config = _expression_config(skill_root)
        require(manifest["native_generation_id"] == config["native_generation_id"]
                and digest(native_manifest["source"]["code"]) == config["code_sha256"],
                "installed release binding changed")
    runtime_python(skill_root, manifest)

    # The native workflow validates this binding again before it reads the
    # module. These arguments carry the resolver's actual choice into its view.
    forwarded = list(arguments) + [
        "--_resolved-runtime-store", str(store),
        "--_resolved-generation-id", generation_id,
        "--_resolved-lookup-source", resolution,
    ]
    env = dict(os.environ, HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1",
               HF_HUB_DISABLE_TELEMETRY="1", PYTHONNOUSERSITE="1")
    env["PHOTO_EXPRESSION_SKILL_ROOT"] = str(Path(skill_root).resolve())
    env.pop("PYTHONPATH", None)
    for key in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"):
        env.pop(key, None)
    launcher = ("import sys,runpy;from pathlib import Path;"
                "entry=sys.argv.pop(1);sys.argv=[entry,*sys.argv[1:]];"
                "sys.path.insert(0,str(Path(entry).parent));"
                "runpy.run_path(entry,run_name='__main__')")
    return subprocess.run([str(runtime_python(skill_root, manifest)), "-I", "-c", launcher,
                           str(native / "scripts/photo_workflow.py"), *forwarded], env=env).returncode


def _validate_forwarded_expression_view(arguments, *, skill_root, workflow_entrypoint):
    """Accept internal flags only inside the exact sealed native code that issued them."""
    resolved_store = option(arguments, "--_resolved-runtime-store")
    resolved_id = option(arguments, "--_resolved-generation-id")
    resolved_source = option(arguments, "--_resolved-lookup-source")
    require(resolved_store and resolved_id and resolved_source,
            "reserved_expression_view_options_require_sealed_dispatch")
    run = option(arguments, "--run")
    maintenance = _flag(arguments, "--maintenance")
    explicit_store = option(arguments, "--runtime-store")
    explicit_id = option(arguments, "--generation-id")
    require(bool(explicit_store) == bool(explicit_id),
            "maintenance_requires_store_and_generation_together")
    state = None
    if maintenance:
        require(run is None, "maintenance_and_authoring_run_are_mutually_exclusive")
        if explicit_store:
            expected_store = Path(explicit_store).expanduser().resolve()
            expected_id = explicit_id
            expected_source = "maintenance_explicit_override"
        else:
            config_root = Path(os.environ.get("PHOTO_EXPRESSION_SKILL_ROOT") or skill_root).resolve()
            config = _expression_config(config_root)
            expected_store = Path(default_store()).resolve()
            expected_id = config["generation_id"]
            expected_source = "maintenance_current_configuration"
    else:
        require(run is not None, "authoring_requires_valid_frozen_run")
        require(explicit_store is None and explicit_id is None,
                "runtime_overrides_require_explicit_maintenance_mode")
        verifier = _neutral_run_files(skill_root)
        state = verifier.load_state(Path(run))
        if state.get("phase") in {"request_prepared", "controls_bound"} or "freeze_receipt" not in state.get("artifacts", {}):
            raise ValueError("pre_core_expression_lookup_blocked")
        if state.get("mode") not in {"prompt_only", "image"}:
            raise ValueError("authoring_requires_valid_frozen_run")
        if verifier.status(state).get("phase") == "stale":
            raise ValueError("stale_frozen_run")
        verifier.verify_freeze(state)
        if "retry_proof" in state.get("artifacts", {}):
            retry_path = Path(skill_root) / "scripts/prepare_retry_context.py"
            spec = importlib.util.spec_from_file_location("_photo_expression_retry_context", retry_path)
            require(spec is not None and spec.loader is not None, "retry_context_verifier_unavailable")
            retry_context = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(retry_context)
            retry_context.verify_child(state)
        bound = state.get("h_f2_binding") or {}
        if "pack" in state.get("artifacts", {}) and not bound:
            raise ValueError("legacy_run_has_no_h_f2_generation_binding")
        if bound:
            require(isinstance(bound, dict) and bound.get("store") and bound.get("generation_id"),
                    "invalid_run_h_f2_binding")
            expected_store = Path(bound["store"]).resolve()
            expected_id = bound["generation_id"]
            expected_source = "run_bound_generation"
        else:
            config_root = Path(os.environ.get("PHOTO_EXPRESSION_SKILL_ROOT") or skill_root).resolve()
            config = _expression_config(config_root)
            expected_store = Path(default_store()).resolve()
            expected_id = config["generation_id"]
            expected_source = "current_installed_configuration"

    run_bound_id = (state.get("h_f2_binding") or {}).get("generation_id") if state else None
    require(Path(resolved_store).expanduser().resolve() == expected_store
            and resolved_id == expected_id and resolved_source == expected_source,
            "forwarded_expression_view_binding_mismatch")
    try:
        native, manifest, native_manifest = release(expected_store, expected_id)
    except (ValueError, OSError, KeyError, TypeError) as error:
        raise ExpressionDispatchError("sealed_h2_generation_unavailable",
                                      lookup_generation_id=expected_id,
                                      run_bound_generation_id=run_bound_id) from error
    code = native_manifest.get("source", {}).get("code", {})
    if "scripts/photo_expression_view.py" not in code:
        raise ExpressionDispatchError("expression_view_not_in_bound_generation",
                                      lookup_generation_id=expected_id,
                                      run_bound_generation_id=run_bound_id)
    if expected_source in {"current_installed_configuration", "maintenance_current_configuration"}:
        config_root = Path(os.environ.get("PHOTO_EXPRESSION_SKILL_ROOT") or skill_root).resolve()
        config = _expression_config(config_root)
        require(manifest["native_generation_id"] == config["native_generation_id"]
                and digest(code) == config["code_sha256"], "installed release binding changed")

    expected_dispatcher = (native / "scripts/photo_installed_h_f2.py").resolve()
    expected_workflow = (native / "scripts/photo_workflow.py").resolve()
    actual_dispatcher = Path(__file__).resolve()
    actual_workflow = Path(workflow_entrypoint).resolve() if workflow_entrypoint else None
    dispatcher_sha = code.get("scripts/photo_installed_h_f2.py")
    workflow_sha = code.get("scripts/photo_workflow.py")
    if (actual_dispatcher != expected_dispatcher or actual_workflow != expected_workflow
            or not dispatcher_sha or file_sha(actual_dispatcher) != dispatcher_sha
            or not workflow_sha or file_sha(actual_workflow) != workflow_sha):
        raise ExpressionDispatchError("reserved_expression_view_options_require_sealed_dispatch",
                                      lookup_generation_id=expected_id,
                                      run_bound_generation_id=run_bound_id)


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


def dispatch(argv=None, *, skill_root=SKILL_ROOT, workflow_entrypoint=None):
    """Return a CLI exit code, or None for an already bound native run."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    # The installed H2 entrypoint always performs the neutral freeze check
    # before resolving the release used by an expression view. The private
    # resolved flags are only consumed by the already-dispatched workflow.
    try:
        is_expression_view = bool(arguments and arguments[0] == "view"
                                  and option(arguments, "--expression") is not None)
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"status": "error", "code": str(error),
                          "native_approval": False, "lookup_authority": False}, ensure_ascii=False),
              file=sys.stderr)
        return 2
    if is_expression_view:
        if any(item in {"--_resolved-runtime-store", "--_resolved-generation-id",
                        "--_resolved-lookup-source"} for item in arguments):
            try:
                _validate_forwarded_expression_view(arguments, skill_root=skill_root,
                                                    workflow_entrypoint=workflow_entrypoint)
                return None
            except (ValueError, OSError, KeyError, TypeError) as error:
                code = getattr(error, "code", None) or str(error) or "expression_view_unavailable"
                payload = {"status": "error", "code": code,
                           "native_approval": False, "lookup_authority": False}
                payload.update(getattr(error, "details", {}))
                print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
                return 2
        try:
            return _dispatch_expression_view(arguments, skill_root=skill_root)
        except (ValueError, OSError, KeyError, TypeError) as error:
            code = getattr(error, "code", None) or str(error) or "expression_view_unavailable"
            payload = {"status": "error", "code": code,
                       "native_approval": False, "lookup_authority": False}
            payload.update(getattr(error, "details", {}))
            print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
            return 2
    try:
        if any(item in {"--_resolved-runtime-store", "--_resolved-generation-id",
                        "--_resolved-lookup-source"} for item in arguments):
            raise ValueError("reserved_expression_view_options_require_sealed_dispatch")
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


def check_runtime(*, skill_root=SKILL_ROOT, source_store=None, generation_id=None):
    """Read-only dependency and installed-writer check, using its bound Python."""
    skill_root = Path(skill_root).resolve()
    config = read(skill_root / CONFIG)
    require(bool(source_store) == bool(generation_id), "supply both source store and generation")
    store = Path(source_store or default_store()).resolve()
    native, manifest, _ = release(store, generation_id or config["generation_id"])
    python = runtime_python(skill_root, manifest)
    program = """import json,sys;sys.path.insert(0,sys.argv[1])
import numpy
import record_image_run as recorder
print(json.dumps({'python':sys.executable,'numpy':numpy.__version__,
 'recorder_file':recorder.__file__,
 'new_record_versions':sorted(recorder.VALID_CANDIDATE_PACK_VERSIONS),
 'bound_pack_version_derivation':callable(getattr(recorder,'candidate_pack_version',None))}))
"""
    result = subprocess.run([str(python), "-I", "-c", program, str(native / "scripts")],
                            capture_output=True, text=True)
    require(result.returncode == 0, "bound Python dependency check failed: " + result.stderr)
    details = json.loads(result.stdout)
    compatible = set(details["new_record_versions"]) in ({"v10"}, {"v10", "h-f2-v2"}) and details["bound_pack_version_derivation"]
    return {"status": "pass" if compatible else "fail", "generation_id": generation_id or config["generation_id"],
            "native_generation_id": manifest["native_generation_id"], "runtime_python": str(python),
            "check": "dependencies_and_installed_recorder", **details,
            "reason": None if compatible else "installed_recorder_version_mismatch",
            "image_calls": 0, "source_writes": 0}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Check the bound maintenance Python and actual installed writer.", allow_abbrev=False)
    parser.add_argument("--check-runtime", action="store_true", required=True)
    parser.add_argument("--source-store", type=Path)
    parser.add_argument("--generation-id")
    args = parser.parse_args()
    try:
        result = check_runtime(source_store=args.source_store, generation_id=args.generation_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(0 if result["status"] == "pass" else 1)
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"status": "error", "check": "dependencies_and_installed_recorder", "detail": str(error)}))
        raise SystemExit(2)
