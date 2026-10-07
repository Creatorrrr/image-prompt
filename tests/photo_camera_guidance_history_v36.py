"""Offline, authenticated V35 recovery for the additive V36 boundary.

This module never qualifies V36 pack meaning. The caller must first authenticate
its V36 proof, then pass that proof's complete ``source_files_after`` mapping.
Historical replay executes the original validator, without editing old fixtures,
proofs, tests, or version checks. Missing exact inputs are a blocker, not a pass.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile

PIN = "8c2029ea1fecbe206820da6bffa70d2745ada6e2"
TREE = "48c0107f3ad2387c5d9f7952e9133ece3d59be9c"
UPSTREAM_PIN = "4f3d524ed035de8592e4b0c6ad5030b41ffc55af"
BASE = "docs/research-evidence/photo-prompt/ethereal-gothic-main-merge-20261007/history/"
PROOF = BASE + "V35-ETHEREAL-DATA-PROOF.json"
PROOF_SHA256 = "011713ae5dc0196356405e593af96a150a79bd7af222d76ffa649751d3198261"
PARENT = BASE + "V34-PARENT-SOURCE.json"
PARENT_SHA256 = "2ac6a8db1225298746cddfc27afb14d82a4f0f30994d89f882f994aa82119ab3"
ASSETS = "skills/subculture-illustration-image-generator/assets/"
VALIDATOR = "skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py"
VALIDATOR_SHA256 = "d0c177317a1fc5ef0d71058a44b5a58538094b45297e33f0a661bd1ae58b04d5"
NEW_RUNTIME_PATHS = frozenset(
    "skills/photo-prompt-image-generator/scripts/" + name
    for name in ("photo_api_render.py", "photo_meaning_diagnostics.py")
)
NEW_AUTHORED_PATHS = frozenset(
    "skills/photo-prompt-image-generator/assets/" + name
    for name in ("photo_prompt_visual_grammar_extension.json", "photo_prompt_visual_obligations_visual_grammar.json")
)
NEW_SOURCE_PATHS = NEW_RUNTIME_PATHS | NEW_AUTHORED_PATHS
UPSTREAM_TEST_CHANGES = frozenset({
    "tests/test_photo_action_context_effects_cleanup.py",
    "tests/test_photo_capture_owner_data_cleanup.py",
    "tests/test_photo_character_response_concepts.py",
    "tests/test_photo_composer_view.py",
    "tests/test_photo_cute_visual_forms.py",
    "tests/test_photo_ethereal_gothic_scene.py",
    "tests/test_photo_image_attempt_evidence.py",
    "tests/test_photo_liminal_active_use_korean_data_cleanup.py",
    "tests/test_photo_motion_artifact_owner_data_cleanup.py",
    "tests/test_photo_photorealism_owner_data_cleanup.py",
    "tests/test_photo_pose_vocabulary_semantics.py",
    "tests/test_photo_retrieval_runtime_improvement.py",
    "tests/test_photo_scene_data_cleanup.py",
    "tests/test_photo_seduction_expression_integration.py",
    "tests/test_photo_structure_maintenance.py",
})


class HistoricalReplayUnavailable(RuntimeError):
    """An exact local source object or required historical runtime is missing."""


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _object_id(kind, raw):
    return hashlib.sha1(f"{kind} {len(raw)}\0".encode() + raw).hexdigest()


def _name(name):
    if not isinstance(name, str) or not name or "\0" in name or "\\" in name:
        raise AssertionError("Unsafe historical source path")
    path = PurePosixPath(name)
    if not path.parts or path.is_absolute() or path.as_posix() != name or any(p in (".", "..", ".git") for p in path.parts):
        raise AssertionError("Unsafe historical source path: " + name)
    return path


def _regular(root, name, *, optional=False):
    path = Path(root)
    parts = _name(name).parts
    for index, part in enumerate(parts):
        path = path / part
        if path.is_symlink():
            raise AssertionError("Historical source symlink: " + name)
        if index < len(parts) - 1 and path.exists() and not path.is_dir():
            raise AssertionError("Historical source ancestor is not a directory: " + name)
    if not path.exists() and optional:
        return None
    if not path.is_file() or not stat.S_ISREG(path.stat().st_mode):
        raise AssertionError("Historical source is not a regular file: " + name)
    return path


def _mode(path):
    return path.stat().st_mode & 0o7777


def require_live_payload(root, name, sha256, mode):
    path = _regular(root, name)
    if digest(path.read_bytes()) != sha256 or _mode(path) != int(mode[-3:], 8):
        raise AssertionError("V36 live source payload or mode drift: " + name)


class GitSnapshot:
    """Read exact local Git objects with replacement and lazy fetch disabled.

    Authenticate each commit/tree/blob body independently, including the tree
    entry that carries its mode. No worktree content is trusted as a Git object.
    """

    def __init__(self, root, commit, tree=None):
        self.root = Path(root)
        self.commit = commit
        self._trees = {}
        raw = self.object("commit", commit)
        first = raw.split(b"\n", 1)[0]
        if not first.startswith(b"tree "):
            raise AssertionError("Historical commit has no tree")
        self.tree = first[5:].decode("ascii")
        if tree is not None and self.tree != tree:
            raise AssertionError("Historical commit/tree identity drift")

    def git(self, *args, input=None):
        env = os.environ.copy()
        env.update(GIT_NO_LAZY_FETCH="1", GIT_NO_REPLACE_OBJECTS="1", GIT_TERMINAL_PROMPT="0")
        result = subprocess.run(
            ["git", "--no-lazy-fetch", "-c", "protocol.allow=never", *args],
            cwd=self.root, env=env, input=input, capture_output=True,
        )
        if result.returncode:
            raise HistoricalReplayUnavailable("Exact local Git object unavailable: " + " ".join(args))
        return result.stdout

    def object(self, kind, oid):
        if len(oid) != 40 or any(c not in "0123456789abcdef" for c in oid):
            raise AssertionError("Invalid historical Git object identity")
        raw = self.git("cat-file", kind, oid)
        if _object_id(kind, raw) != oid:
            raise AssertionError("Historical Git object payload drift: " + oid)
        return raw

    def entries(self, oid):
        if oid not in self._trees:
            raw = self.object("tree", oid)
            entries = {}
            while raw:
                header, raw = raw.split(b"\0", 1)
                mode, name = header.decode("utf-8").split(" ", 1)
                if len(raw) < 20 or "/" in name or name in entries:
                    raise AssertionError("Invalid historical Git tree")
                entries[name] = (mode, raw[:20].hex())
                raw = raw[20:]
            self._trees[oid] = entries
        return self._trees[oid]

    def entry(self, name):
        parts = _name(name).parts
        tree = self.tree
        for index, part in enumerate(parts):
            entry = self.entries(tree).get(part)
            if entry is None:
                raise HistoricalReplayUnavailable("Path absent from exact historical tree: " + name)
            mode, oid = entry
            if index < len(parts) - 1:
                if mode != "40000":
                    raise AssertionError("Non-directory historical source ancestor: " + name)
                tree = oid
            elif mode not in ("100644", "100755"):
                raise AssertionError("Non-regular historical Git source: " + name)
        return {"path": name, "mode": mode, "git_blob": oid}

    def payload(self, name, *, sha256=None):
        row = self.entry(name)
        raw = self.object("blob", row["git_blob"])
        if sha256 is not None and digest(raw) != sha256:
            raise AssertionError("Frozen original source SHA256 drift: " + name)
        return raw

    def paths(self, prefix):
        """Enumerate one authenticated subtree without reading its blob bodies."""
        parts = _name(prefix).parts
        tree = self.tree
        for part in parts:
            mode, tree = self.entries(tree)[part]
            if mode != "40000":
                raise AssertionError("Historical subtree is not a directory")
        def walk(oid, stem):
            for name, (mode, child) in self.entries(oid).items():
                path = stem + "/" + name
                if mode == "40000":
                    yield from walk(child, path)
                else:
                    yield path
        return set(walk(tree, prefix))


class ExactV35Sources:
    def __init__(self, source_root):
        self.root = Path(source_root)
        self.original = GitSnapshot(self.root, PIN, TREE)
        self.proof = json.loads(self.retained_payload(PROOF, PROOF_SHA256))
        self.parent = json.loads(self.retained_payload(PARENT, PARENT_SHA256))
        if (self.proof.get("schema") != "photo-ethereal-data-transition/v35"
                or self.proof.get("parent_manifest_sha256") != PARENT_SHA256
                or len(self.proof.get("source_files_after", {})) != 152
                or self.parent.get("schema") != "photo-ethereal-parent-source/v1"):
            raise AssertionError("Frozen V35 proof lineage drift")

    def retained_payload(self, name, sha256=None):
        """Sparse absence may use Git; present-but-changed content may not."""
        raw = self.original.payload(name, sha256=sha256)
        path = _regular(self.root, name, optional=True)
        row = self.original.entry(name)
        if path is not None and (path.read_bytes() != raw or _mode(path) != int(row["mode"][-3:], 8)):
            raise AssertionError("Frozen retained payload or mode drift: " + name)
        return raw

    def original_payload(self, name):
        expected = self.proof["source_files_after"].get(name)
        return self.original.payload(name, sha256=expected)

    def retained_test_payload(self, name):
        if name not in UPSTREAM_TEST_CHANGES:
            return self.retained_payload(name)
        # These existing tests changed in approved upstream 4f3 (P0 + grammar).
        # Their replay payload remains 8c; their live identity is exactly 4f3.
        raw = self.original.payload(name)
        path = _regular(self.root, name, optional=True)
        if path is not None:
            upstream = GitSnapshot(self.root, UPSTREAM_PIN)
            row = upstream.entry(name)
            require_live_payload(self.root, name, digest(upstream.payload(name)), row["mode"])
        return raw

    def verify_live_sources(self, source_files_after):
        """Authenticate the caller's already sealed successor source mapping."""
        expected = set(self.proof["source_files_after"]) | NEW_SOURCE_PATHS
        if not isinstance(source_files_after, dict) or set(source_files_after) != expected:
            raise AssertionError("V36 live source inventory must contain all 156 bound paths")
        upstream = GitSnapshot(self.root, UPSTREAM_PIN)
        for name, sha256 in sorted(source_files_after.items()):
            if not isinstance(sha256, str) or len(sha256) != 64 or any(c not in "0123456789abcdef" for c in sha256):
                raise AssertionError("V36 invalid live source digest: " + name)
            row = upstream.entry(name)
            require_live_payload(self.root, name, sha256, row["mode"])
            if name in self.proof["source_files_after"]:
                self.original_payload(name)

    def verify_retained_history(self, *, include_shards=True):
        """Check present immutable artifacts; recover only absent exact bytes."""
        paths = {PROOF: PROOF_SHA256, PARENT: PARENT_SHA256}
        groups = ["frozen_inputs", "evidence_files"]
        if include_shards:
            groups.extend(("active_shards_after", "retained_shards_before"))
        for group in groups:
            paths.update(self.proof[group])
        asset_paths = self.original.paths(ASSETS.rstrip("/"))
        for version in range(1, 36):
            for suffix in (".json", "_pack.json"):
                name = ASSETS + f"photo_regression_baseline_v{version}" + suffix
                # Early historical manifests do not all have a companion pack.
                if name not in asset_paths:
                    if _regular(self.root, name, optional=True) is not None:
                        raise AssertionError("Unregistered historical baseline: " + name)
                else:
                    paths.setdefault(name, None)
        for name in sorted(self.original.paths("tests")):
            self.retained_test_payload(name)
        for name, sha256 in paths.items():
            self.retained_payload(name, sha256)
        self.original.payload(VALIDATOR, sha256=VALIDATOR_SHA256)

    def replay_paths(self):
        names = {PROOF, PARENT, VALIDATOR, ASSETS + "photo_regression_baseline_v35.json",
                 ASSETS + "photo_regression_baseline_v35_pack.json", "tests/photo_ethereal_history_v35.py"}
        for row in self.parent["members"]:
            names.update((row["path"], row["source_path"]))
        for group in ("source_files_after", "frozen_inputs", "evidence_files", "active_shards_after", "retained_shards_before"):
            names.update(self.proof[group])
        names.update(self.original.paths("tests"))
        return sorted(names)

    def materialize_original(self, directory):
        """Create an exact replay closure only after all object availability checks."""
        directory = Path(directory)
        if directory.exists() or directory.is_symlink():
            raise AssertionError("Original replay destination must not exist")
        rows = [self.original.entry(name) for name in self.replay_paths()]
        ids = sorted({row["git_blob"] for row in rows})
        checked = self.original.git("cat-file", "--batch-check", input=("\n".join(ids) + "\n").encode())
        missing = [line.split()[0] for line in checked.decode().splitlines() if line.endswith(" missing")]
        if missing:
            raise HistoricalReplayUnavailable(f"Exact V35 replay requires {len(missing)} unavailable local Git blobs; first: {missing[0]}")
        directory.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".original-v35-", dir=directory.parent) as temporary:
            staged = Path(temporary) / "tree"
            staged.mkdir()
            for row in rows:
                target = staged / row["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(self.original.payload(row["path"]))
                target.chmod(int(row["mode"][-3:], 8))
            if directory.exists() or directory.is_symlink():
                raise AssertionError("Original replay destination changed")
            staged.replace(directory)


def require_original_environment(expected, python_executable=sys.executable):
    probe = "import json,sys,unicodedata; print(json.dumps({'implementation':sys.implementation.name,'python':list(sys.version_info[:3]),'unicode':unicodedata.unidata_version}))"
    try:
        actual = json.loads(subprocess.check_output([str(python_executable), "-I", "-c", probe], text=True))
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        raise HistoricalReplayUnavailable("Exact V35 Python interpreter unavailable") from exc
    if actual != expected:
        raise HistoricalReplayUnavailable("Exact V35 Python/Unicode environment unavailable: expected " + json.dumps(expected, sort_keys=True) + "; actual " + json.dumps(actual, sort_keys=True))


def dispatch_historical(asset_dir, *, source_root, baseline_version, source_files_after,
                        python_executable=sys.executable):
    """Run V6–V35 through exact V35 code; its original chain still checks V1–V5.

    The caller must authenticate its V36 proof before passing source_files_after.
    This function must never be used as a V36 current-pack qualification result.
    """
    if type(baseline_version) is not int or baseline_version not in range(6, 36):
        raise AssertionError("Unsupported original V35 baseline version")
    root = Path(source_root).resolve()
    if Path(asset_dir).resolve() != root / ASSETS:
        raise AssertionError("Historical dispatch asset directory mismatch")
    return _replay_original(root, source_files_after, python_executable,
                            baseline_version=baseline_version)


def replay_original_tests(source_root, *, test_module, source_files_after,
                          python_executable=sys.executable):
    """Run an original test module in exact 8c code, without rewriting its bytes."""
    if (not isinstance(test_module, str) or not test_module.startswith("tests.test_")
            or any(not part.isidentifier() for part in test_module.split("."))):
        raise AssertionError("Original test module must be a tests.test_* module")
    return _replay_original(Path(source_root).resolve(), source_files_after,
                            python_executable, test_module=test_module)


def _replay_original(root, source_files_after, python_executable, *, baseline_version=None,
                     test_module=None):
    original = ExactV35Sources(root)
    original.verify_live_sources(source_files_after)
    original.verify_retained_history(include_shards=False)
    if test_module is not None:
        original.original.payload(test_module.replace(".", "/") + ".py")
    # Stop before the large historical closure is read or materialized when the
    # exact interpreter is unavailable. No latest-runtime fallback is permitted.
    require_original_environment(original.parent["environment"], python_executable)
    for group in ("active_shards_after", "retained_shards_before"):
        for name, sha256 in original.proof[group].items():
            original.retained_payload(name, sha256)
    with tempfile.TemporaryDirectory(prefix="photo-v36-original-v35-") as temporary:
        tree = Path(temporary) / "tree"
        original.materialize_original(tree)
        executable = tree / ".venv/bin/python"
        executable.parent.mkdir(parents=True)
        executable.symlink_to(Path(python_executable).resolve())
        env = {"PATH": os.environ.get("PATH", ""), "PYTHONPATH": "." + os.pathsep + "tests",
               "GEMINI_API_KEY": "", "GOOGLE_API_KEY": "", "OPENAI_API_KEY": "",
               "PHOTO_RUNTIME_STORE": str(Path(temporary) / "runtime"), "PYTHONDONTWRITEBYTECODE": "1"}
        setup = "import sys; sys.path.insert(0,'skills/photo-prompt-image-generator/scripts'); from photo_runtime_sources import SnapshotPublisher; SnapshotPublisher().publish()"
        prepared = subprocess.run([str(executable), "-c", setup], cwd=tree, env=env, capture_output=True, text=True, timeout=300)
        if prepared.returncode:
            raise AssertionError("Original V35 publisher failed: " + prepared.stderr)
        if test_module is not None:
            command = [str(executable), "-m", "unittest", "-v", test_module]
        else:
            code = "import json,sys; from pathlib import Path; sys.path.insert(0,'skills/subculture-illustration-image-generator/scripts'); import validate_illustration_assets as v; print(json.dumps(v.validate_photo_regression_baseline(Path(" + repr(ASSETS) + "),baseline_version=" + str(baseline_version) + ")))"
            command = [str(executable), "-c", code]
        result = subprocess.run(command, cwd=tree, env=env, capture_output=True, text=True, timeout=1800)
        if result.returncode:
            raise AssertionError("Original V35 replay failed: " + result.stdout + result.stderr)
        return result if test_module is not None else json.loads(result.stdout.strip().splitlines()[-1])
