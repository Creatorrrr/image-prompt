"""Post-core source generations, freshness checks and request-bound receipts.

Only Python source is captured at import. Assets, Git and runtime storage are
accessed by explicit post-core/maintenance calls. No embedding or image APIs.
"""
from __future__ import annotations

import contextlib
import copy
import fcntl
import os
import re
import subprocess
import sys
import tempfile
import threading
import unicodedata
import uuid
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path

from core_slot_index_storage import CoreSlotIndexStore, atomic_write, canonical_bytes, decode, digest, json_digest
from photo_source_manifest import SourceInventory

SKILL_ROOT = Path(__file__).resolve().parents[1]
GENERATION_SCHEMA = "photo-runtime-generation/v1"
RECEIPT_SCHEMA = "photo-runtime-receipt/v1"
HASH = re.compile(r"[0-9a-f]{64}\Z")
BASE_ASSETS = ("photo_prompt_source_manifest.json", "photo_prompt_tags.json", "photo_prompt_quality_layers.json",
               "photo_prompt_visual_obligations.json", "photo_prompt_semantic_index.json", "photo_prompt_visual_profile_index.json")


class FreshnessError(ValueError):
    def __init__(self, state: str, message: str):
        self.state = state
        super().__init__(f"{state}: {message}")


def environment_binding() -> dict:
    return {"implementation": sys.implementation.name, "python": list(sys.version_info[:3]),
            "unicode": unicodedata.unidata_version}


def code_inventory(root: Path) -> dict:
    return {str(path.relative_to(root)): digest(path.read_bytes())
            for directory in ("scripts", "precore") for path in sorted((root / directory).glob("*.py"))}


# Captured before any live source access. An edited disk is never relabeled as
# the implementation already imported by this process.
LOADED_CODE = code_inventory(SKILL_ROOT)
LOADED_ENVIRONMENT = environment_binding()


def algorithm_binding(generator) -> dict:
    from bm25f_retrieval import BM25F_INDEX_RECIPE_VERSION, BM25F_TOKENIZER_RECIPE_VERSION, canonical_bm25f_policy
    get = generator.get if isinstance(generator, dict) else lambda key: getattr(generator, key)
    return {"code": LOADED_CODE, "environment": LOADED_ENVIRONMENT,
            "policy": canonical_bm25f_policy(get("SEMANTIC_BM25F_POLICY")),
            "policy_version": get("SEMANTIC_BM25F_POLICY_VERSION"),
            "tokenizer_recipe": BM25F_TOKENIZER_RECIPE_VERSION,
            "index_recipe": BM25F_INDEX_RECIPE_VERSION,
            "corpus_recipe": "authored-slot-only/v1",
            "field_projection_recipe": get("SEMANTIC_TEXT_RECIPE_VERSION")}


def algorithm_hash(generator) -> str:
    return json_digest(algorithm_binding(generator))


def default_store() -> Path:
    configured = os.environ.get("PHOTO_RUNTIME_STORE")
    return Path(configured).expanduser() if configured else Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))) / "image-prompt/photo-runtime"


def namespace(root: Path, mode: str, remote: str = "") -> str:
    return json_digest({"root": str(Path(root).resolve()), "mode": mode, "remote": remote})


def _regular(root: Path, relative: str) -> Path:
    parts = relative.split("/")
    if not relative or any(part in ("", ".", "..") for part in parts) or "\\" in relative or ":" in relative:
        raise FreshnessError("source_invalid", "unsafe snapshot path")
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise FreshnessError("source_invalid", f"mutable/symlink snapshot member: {relative}")
    if not path.is_file():
        raise FreshnessError("source_invalid", f"missing snapshot member: {relative}")
    return path


def capture_sources(root: Path) -> tuple[dict, SourceInventory]:
    """Hash mutable authored files and manifests, not vector bodies per request."""
    root = Path(root).resolve()
    try:
        inventory = SourceInventory.load(root / "assets")
        inventory.validate()
        names = set(BASE_ASSETS) | {row[0] for row in inventory.rows}
        files = {}
        for name in sorted(names):
            path = root / "assets" / name
            if name in BASE_ASSETS and not path.is_file():
                raise ValueError(f"required runtime source is missing: {name}")
            files[f"assets/{name}"] = digest(_regular(root, f"assets/{name}").read_bytes()) if path.exists() else None
        for path in sorted((root / "precore").glob("*.json")):
            files[str(path.relative_to(root))] = digest(_regular(root, str(path.relative_to(root))).read_bytes())
        value = {"files": files, "code": code_inventory(root), "environment": environment_binding()}
        return value, inventory
    except (OSError, ValueError) as exc:
        if isinstance(exc, FreshnessError):
            raise
        raise FreshnessError("source_invalid", str(exc)) from exc


@contextlib.contextmanager
def file_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _read(path: Path, default=None):
    return decode(path.read_bytes()) if path.exists() else default


def _read_current(directory: Path):
    pointer = _read(directory / "CURRENT.json")
    if pointer is not None and (not isinstance(pointer, dict)
            or pointer.get("schema") != "photo-runtime-current/v1"
            or not isinstance(pointer.get("generation_id"), str)
            or not HASH.fullmatch(pointer["generation_id"])
            or not isinstance(pointer.get("source_fingerprint"), str)
            or not HASH.fullmatch(pointer["source_fingerprint"])
            or type(pointer.get("revision")) is not int or pointer["revision"] < 1
            or not isinstance(pointer.get("observation"), dict)):
        raise FreshnessError("source_invalid", "invalid CURRENT generation/source pointer")
    return pointer


def _pointer_directory(store: Path, root: Path, mode: str, remote: str = "") -> Path:
    return store / ("remote" if mode == "remote_before_retrieval" else "local") / namespace(root, mode, remote)


@contextlib.contextmanager
def source_update(root: Path, store: Path | None = None):
    """Cooperative maintenance writers declare an unfinished source revision."""
    directory = _pointer_directory(Path(store or default_store()), Path(root), "local_current")
    token = uuid.uuid4().hex
    with file_lock(directory / "LOCK"):
        revision = _read(directory / "SOURCE.json", {"epoch": 0})
        if revision.get("editing"):
            raise FreshnessError("source_revision_pending", "another maintenance writer owns this source")
        atomic_write(directory / "SOURCE.json", canonical_bytes({"epoch": revision["epoch"] + 1, "editing": token}))
    try:
        yield
    except BaseException:
        # An aborted/incomplete build remains pending until maintenance repairs
        # it and explicitly completes that revision; old CURRENT is preserved.
        raise
    else:
        complete_source_update(root, store, token=token)


def complete_source_update(root: Path, store: Path | None = None, *, token: str | None = None):
    directory = _pointer_directory(Path(store or default_store()), Path(root), "local_current")
    with file_lock(directory / "LOCK"):
        revision = _read(directory / "SOURCE.json", {"epoch": 0})
        if token is not None and revision.get("editing") != token:
            raise FreshnessError("source_revision_pending", "maintenance source revision ownership changed")
        atomic_write(directory / "SOURCE.json", canonical_bytes({"epoch": revision["epoch"] + 1, "editing": None}))


def _require_implementation(source: dict, generator) -> None:
    if source["code"] != LOADED_CODE or source["environment"] != LOADED_ENVIRONMENT:
        raise FreshnessError("runtime_restart_required", "source code/environment differs from this imported implementation; start its CLI worker")


class SnapshotPublisher:
    def __init__(self, root: Path = SKILL_ROOT, store: Path | None = None, *, mode="local_current", remote=""):
        self.root = Path(root).resolve()
        self.store = Path(store or default_store()).resolve()
        self.mode, self.remote = mode, remote
        self.directory = _pointer_directory(self.store, self.root, mode, remote)

    def publish(self, *, observation: dict | None = None, proposed_slot_index=None, before_publish=None) -> dict:
        import prompt_generator as generator
        with file_lock(self.directory / "LOCK"):
            source, _ = capture_sources(self.root)
            _require_implementation(source, generator)
            revision = _read(self.directory / "SOURCE.json", {"epoch": 0, "editing": None})
            if revision.get("editing"):
                raise FreshnessError("source_revision_pending", "maintenance revision is unfinished")
            previous = _read_current(self.directory)
            algorithm = algorithm_hash(generator)
        self.store.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".generation-", dir=self.store) as temporary:
            staging = Path(temporary)
            members = {}
            paths = {name: sha for name, sha in source["files"].items() if sha is not None} | source["code"]
            # Include only referenced vector shards. They stay inside this
            # generation's assets boundary, independent of the mutable checkout.
            for name in ("photo_prompt_semantic_index.json", "photo_prompt_visual_profile_index.json"):
                manifest = decode(_regular(self.root, f"assets/{name}").read_bytes())
                for row in manifest.get("shards") or []:
                    relative = "assets/" + row["path"]
                    paths[relative] = row["sha256"]
            for relative, sha in sorted(paths.items()):
                raw = _regular(self.root, relative).read_bytes()
                if digest(raw) != sha:
                    raise FreshnessError("source_revision_pending", f"source changed during capture: {relative}")
                target = staging / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                # Shares only runtime-owned, independently copied, immutable
                # bytes. Never links back to the user's mutable source files.
                content = self.store / "source-data" / sha
                if not content.exists() or content.is_symlink() or content.read_bytes() != raw:
                    atomic_write(content, raw)
                    content.chmod(0o444)
                os.link(content, target)
                members[relative] = {"sha256": sha, "bytes": len(raw)}
            try:
                inventory = SourceInventory.load(staging / "assets")
                data = generator.load_runtime_data(staging / "assets/photo_prompt_tags.json", inventory=inventory)
                from validate_photo_prompt_dictionary import validate_source_corpus
                errors = validate_source_corpus(staging, data, inventory)
                if errors:
                    raise ValueError("; ".join(errors))
                corpus = canonical_bytes(data["slots"]).decode("utf-8")
                cache = CoreSlotIndexStore(self.store).create(corpus, algorithm,
                    generator.build_core_slot_index, proposed=proposed_slot_index)
            except (OSError, ValueError, KeyError, TypeError) as exc:
                raise FreshnessError("source_invalid", f"snapshot validation failed: {exc}") from exc
            manifest = {"schema": GENERATION_SCHEMA, "source": source, "source_fingerprint": json_digest(source),
                        "members": members, "algorithm_sha256": algorithm, "slot_cache": cache}
            generation = json_digest(manifest)
            atomic_write(staging / "manifest.json", canonical_bytes(manifest))
            if before_publish:
                before_publish()
            with file_lock(self.directory / "LOCK"):
                current_source, _ = capture_sources(self.root)
                if algorithm_hash(generator) != algorithm:
                    raise FreshnessError("runtime_restart_required", "algorithm changed during publication")
                if (current_source != source or _read(self.directory / "SOURCE.json", {"epoch": 0, "editing": None}) != revision
                        or _read_current(self.directory) != previous):
                    raise FreshnessError("source_revision_pending", "source/pointer revision changed before publication")
                target = self.store / "generations" / generation
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    self._verify_generation(target, generation)
                else:
                    os.rename(staging, target)
                pointer = {"schema": "photo-runtime-current/v1", "generation_id": generation,
                           "source_fingerprint": manifest["source_fingerprint"],
                           "revision": (previous or {}).get("revision", 0) + 1,
                           "observation": observation or {"mode": self.mode, "root": str(self.root),
                               "observed_at": datetime.now(timezone.utc).isoformat(), "local_epoch": revision["epoch"]}}
                atomic_write(self.directory / "CURRENT.json", canonical_bytes(pointer))
                return pointer

    @staticmethod
    def _verify_generation(root: Path, generation: str) -> dict:
        if not HASH.fullmatch(generation):
            raise FreshnessError("source_invalid", "invalid generation ID")
        manifest = decode(_regular(root, "manifest.json").read_bytes())
        if manifest.get("schema") != GENERATION_SCHEMA or json_digest(manifest) != generation:
            raise FreshnessError("source_invalid", "generation manifest checksum mismatch")
        if manifest.get("source_fingerprint") != json_digest(manifest.get("source")):
            raise FreshnessError("source_invalid", "generation source fingerprint mismatch")
        for relative, expected in manifest["members"].items():
            raw = _regular(root, relative).read_bytes()
            if digest(raw) != expected["sha256"] or len(raw) != expected["bytes"]:
                raise FreshnessError("source_invalid", f"generation member checksum mismatch: {relative}")
        return manifest


class FrozenDict(dict):
    __slots__ = ()
    def _changed(self, *args, **kwargs):
        raise FreshnessError("source_invalid", "bound snapshot object mutation")
    __setitem__ = __delitem__ = clear = pop = popitem = setdefault = update = __ior__ = _changed
    def __deepcopy__(self, memo):
        result = {copy.deepcopy(key, memo): copy.deepcopy(value, memo) for key, value in self.items()}
        memo[id(self)] = result
        return result


class FrozenList(list):
    __slots__ = ()
    def _changed(self, *args, **kwargs):
        raise FreshnessError("source_invalid", "bound snapshot object mutation")
    __setitem__ = __delitem__ = append = clear = extend = insert = pop = remove = reverse = sort = __iadd__ = __imul__ = _changed
    def __deepcopy__(self, memo):
        result = [copy.deepcopy(value, memo) for value in self]
        memo[id(self)] = result
        return result


def freeze(value):
    if isinstance(value, dict):
        return FrozenDict({key: freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return FrozenList(freeze(item) if isinstance(item, (dict, list)) else item for item in value)
    return value


class BoundRuntimeData(FrozenDict):
    __slots__ = ("__index", "__corpus_hash", "__algorithm")
    def __init__(self, data: dict, index: dict, corpus_hash: str, algorithm: str):
        dict.__init__(self, freeze(data))
        object.__setattr__(self, "_BoundRuntimeData__index", freeze(index))
        object.__setattr__(self, "_BoundRuntimeData__corpus_hash", corpus_hash)
        object.__setattr__(self, "_BoundRuntimeData__algorithm", algorithm)

    def __setattr__(self, *args):
        raise FreshnessError("source_invalid", "bound snapshot object mutation")

    def slot_index(self, corpus_json: str):
        import prompt_generator as generator
        if digest(corpus_json.encode("utf-8")) != self.__corpus_hash:
            raise FreshnessError("source_invalid", "bound snapshot slot corpus changed")
        if algorithm_hash(generator) != self.__algorithm:
            raise FreshnessError("runtime_restart_required", "bound snapshot algorithm changed")
        return self.__index


@dataclass(frozen=True)
class RuntimeSnapshot:
    generation_id: str
    root: Path
    manifest: dict
    data: BoundRuntimeData
    cache_status: str
    observation: dict | None = None


class RuntimeSnapshotProvider:
    def __init__(self, root: Path = SKILL_ROOT, store: Path | None = None, *, mode="local_current", remote="", ref="main"):
        if mode not in ("local_current", "remote_before_retrieval"):
            raise ValueError("unsupported photo source mode")
        self.publisher = SnapshotPublisher(root, store, mode=mode, remote=remote)
        self.mode, self.remote, self.ref = mode, remote, ref
        self._snapshots = {}
        self._lock = threading.RLock()
        self.last_observation = None

    def acquire(self, *, bootstrap=True) -> RuntimeSnapshot:
        """Call only after validating the request's frozen authorial inputs."""
        import prompt_generator as generator
        with self._lock:
            if self.mode == "remote_before_retrieval":
                if not self.remote:
                    raise ValueError("remote_before_retrieval requires an explicit remote URL")
                root, observation = RemoteSourceUpdater(self.publisher.store, self.remote, self.ref).fetch()
                self.publisher = SnapshotPublisher(root, self.publisher.store, mode=self.mode, remote=self.remote)
                source, _ = capture_sources(root)
                _require_implementation(source, generator)
                pointer = _read_current(self.publisher.directory)
                if not pointer or pointer["source_fingerprint"] != json_digest(source):
                    self.publisher.publish(observation=observation)
                self.last_observation = observation
            source, _ = capture_sources(self.publisher.root)
            _require_implementation(source, generator)
            with file_lock(self.publisher.directory / "LOCK"):
                revision = _read(self.publisher.directory / "SOURCE.json", {"epoch": 0, "editing": None})
                pointer = _read_current(self.publisher.directory)
            if revision.get("editing"):
                raise FreshnessError("source_revision_pending", "maintenance revision is unfinished")
            if pointer is None and bootstrap:
                pointer = self.publisher.publish()
            elif pointer is not None and pointer["source_fingerprint"] != json_digest(source) and bootstrap:
                # A new matching worker can bootstrap a changed implementation.
                # Data-only revisions still require maintenance publication.
                previous_manifest = SnapshotPublisher._verify_generation(self.publisher.store / "generations" / pointer["generation_id"], pointer["generation_id"])
                if previous_manifest["source"]["code"] != LOADED_CODE or previous_manifest["source"]["environment"] != LOADED_ENVIRONMENT:
                    pointer = self.publisher.publish()
            if pointer is None or pointer["source_fingerprint"] != json_digest(source):
                raise FreshnessError("source_revision_pending", "current source has no completed validated publication; finish maintenance and publish")
            # Capture is optimistic; validate the source/pointer pair again
            # immediately before admitting a new request.
            checked, _ = capture_sources(self.publisher.root)
            with file_lock(self.publisher.directory / "LOCK"):
                if (checked != source or _read_current(self.publisher.directory) != pointer
                        or _read(self.publisher.directory / "SOURCE.json", {"epoch": 0, "editing": None}) != revision):
                    raise FreshnessError("source_revision_pending", "source changed while acquiring request snapshot")
            self.last_observation = self.last_observation if self.mode == "remote_before_retrieval" else {
                "mode": self.mode, "root": str(self.publisher.root), "local_epoch": revision["epoch"],
                "observed_at": datetime.now(timezone.utc).isoformat()}
            snapshot = self.load_generation(pointer["generation_id"])
            if (snapshot.manifest["source"] != source
                    or snapshot.manifest["source_fingerprint"] != pointer["source_fingerprint"]):
                raise FreshnessError("source_invalid", "CURRENT generation differs from the observed source binding")
            return replace(snapshot, observation=freeze(self.last_observation))

    def load_generation(self, generation: str, *, independent_audit=False) -> RuntimeSnapshot:
        import prompt_generator as generator
        with self._lock:
            if not HASH.fullmatch(generation):
                raise FreshnessError("source_invalid", "invalid generation ID")
            if generation in self._snapshots and not independent_audit:
                if self._snapshots[generation].manifest["algorithm_sha256"] != algorithm_hash(generator):
                    raise FreshnessError("runtime_restart_required", "bound snapshot algorithm changed")
                return self._snapshots[generation]
            root = self.publisher.store / "generations" / generation
            manifest = SnapshotPublisher._verify_generation(root, generation)
            _require_implementation(manifest["source"], generator)
            captured, _ = capture_sources(root)
            if captured != manifest["source"]:
                raise FreshnessError("source_invalid", "generation source inventory/presence changed")
            if manifest["algorithm_sha256"] != algorithm_hash(generator):
                raise FreshnessError("runtime_restart_required", "generation BM25F policy/environment differs from loaded worker")
            try:
                data = generator.load_runtime_data(root / "assets/photo_prompt_tags.json")
                corpus = canonical_bytes(data["slots"]).decode("utf-8")
                if independent_audit:
                    index, status = generator.build_core_slot_index(corpus), "independent_audit"
                else:
                    index, status = CoreSlotIndexStore(self.publisher.store).load(manifest["slot_cache"], corpus,
                        algorithm_hash(generator), generator.build_core_slot_index)
                bound = BoundRuntimeData(data, index, digest(corpus.encode()), algorithm_hash(generator))
            except (OSError, ValueError, KeyError, TypeError) as exc:
                if isinstance(exc, FreshnessError):
                    raise
                raise FreshnessError("source_invalid", f"generation deep validation failed: {exc}") from exc
            snapshot = RuntimeSnapshot(generation, root, freeze(manifest), bound, status)
            if not independent_audit:
                self._snapshots[generation] = snapshot
                while len(self._snapshots) > 2:
                    self._snapshots.pop(next(iter(self._snapshots)))
            return snapshot

    def receipt(self, snapshot: RuntimeSnapshot, pack: dict) -> dict:
        import prompt_generator as generator
        pack_hash = json_digest(pack)
        if pack.get("core_retrieval", {}).get("slot_corpus_sha256") != snapshot.manifest["slot_cache"]["slot_corpus_sha256"]:
            raise FreshnessError("source_invalid", "pack slot binding differs from acquired generation")
        value = {"schema": RECEIPT_SCHEMA, "request_id": uuid.uuid4().hex, "generation_id": snapshot.generation_id,
                 "pack_sha256": pack_hash, "observation": snapshot.observation,
                 "source_fingerprint": snapshot.manifest["source_fingerprint"],
                 "algorithm_sha256": snapshot.manifest["algorithm_sha256"],
                 "slot_cache_key": snapshot.manifest["slot_cache"]["slot_cache_key"],
                 "cache_status": snapshot.cache_status, "bindings": pack_bindings(pack)}
        verify_pack_bindings(pack, snapshot, generator)
        value["canonical_sha256"] = json_digest(value)
        atomic_write(self.publisher.store / "receipts" / f"{value['request_id']}.json", canonical_bytes(value))
        with file_lock(self.publisher.store / "receipts/LOCK"):
            target = self.publisher.store / "receipt-index" / f"{pack_hash}.json"
            previous = _read(target, {"schema": "photo-runtime-receipt-index/v1", "generations": {}})
            previous["generations"][snapshot.generation_id] = value["request_id"]
            atomic_write(target, canonical_bytes(previous))
        return value

    def from_receipt(self, pack: dict, receipt: dict | None = None) -> RuntimeSnapshot:
        import prompt_generator as generator
        if receipt is None:
            index = _read(self.publisher.store / "receipt-index" / f"{json_digest(pack)}.json")
            if index is not None:
                if index.get("schema") != "photo-runtime-receipt-index/v1" or not isinstance(index.get("generations"), dict):
                    raise FreshnessError("source_invalid", "invalid runtime receipt index")
                if len(index["generations"]) != 1:
                    raise FreshnessError("source_invalid", "ambiguous runtime receipt: supply the exact request receipt")
                request = next(iter(index["generations"].values()))
                if not isinstance(request, str) or not re.fullmatch(r"[0-9a-f]{32}", request):
                    raise FreshnessError("source_invalid", "invalid runtime receipt request ID")
                receipt = _read(self.publisher.store / "receipts" / f"{request}.json")
        if not isinstance(receipt, dict):
            raise FreshnessError("source_invalid", "missing runtime receipt; use the sealed historical implementation for legacy packs")
        body = {key: value for key, value in receipt.items() if key != "canonical_sha256"}
        if (receipt.get("schema") != RECEIPT_SCHEMA or receipt.get("canonical_sha256") != json_digest(body)
                or receipt.get("pack_sha256") != json_digest(pack) or receipt.get("bindings") != pack_bindings(pack)):
            raise FreshnessError("source_invalid", "receipt/pack binding mismatch")
        snapshot = self.load_generation(receipt["generation_id"], independent_audit=True)
        if (receipt["source_fingerprint"] != snapshot.manifest["source_fingerprint"]
                or receipt["algorithm_sha256"] != snapshot.manifest["algorithm_sha256"]
                or receipt["slot_cache_key"] != snapshot.manifest["slot_cache"]["slot_cache_key"]):
            raise FreshnessError("source_invalid", "receipt generation binding mismatch")
        verify_pack_bindings(pack, snapshot, generator, recompute_visual=True)
        return snapshot


def pack_bindings(pack: dict) -> dict:
    return {"tags_hash": (pack.get("provenance") or {}).get("tags_hash"), "authorial_core_sha256": (pack.get("authorial_core") or {}).get("canonical_sha256"),
            "core_retrieval_sha256": (pack.get("core_retrieval") or {}).get("canonical_sha256"),
            "slot_corpus_sha256": (pack.get("core_retrieval") or {}).get("slot_corpus_sha256"),
            "visual": {key: json_digest(pack.get(key)) for key in ("visual_obligations", "visual_concept_candidates", "semantic_clarification")}}


def verify_pack_bindings(pack: dict, snapshot: RuntimeSnapshot, generator, *, recompute_visual=False) -> None:
    if ((pack.get("provenance") or {}).get("tags_hash") != generator.dictionary_hash(snapshot.data)
            or (pack.get("core_retrieval") or {}).get("slot_corpus_sha256") != snapshot.manifest["slot_cache"]["slot_corpus_sha256"]):
        raise FreshnessError("source_invalid", "pack dictionary/slot source binding mismatch")
    if recompute_visual:
        expected = generator.generate_candidate_pack(snapshot.data, pack["authorial_core"], pack["creative_controls"],
            pack["embodiment_preflight"]["baseline_review"], seed=pack["provenance"]["seed"],
            visual_intent=pack.get("visual_intent"))
        if pack != expected:
            raise FreshnessError("source_invalid", "full candidate pack differs from pinned generation recomputation")


def publish_if_ready(root: Path, store: Path | None = None) -> bool:
    """Post-success maintenance hook; an unfinished other index stays pending."""
    try:
        SnapshotPublisher(root, store).publish()
        return True
    except (OSError, ValueError) as exc:
        print(f"Runtime publication pending: {exc}", file=sys.stderr)
        return False


class RemoteSourceUpdater:
    def __init__(self, store: Path, remote: str, ref="main"):
        if not remote or remote.startswith("-") or not re.fullmatch(r"[A-Za-z0-9_./-]+", ref) or ref.startswith("-"):
            raise ValueError("invalid remote/ref configuration")
        self.store, self.remote, self.ref = Path(store), remote, ref

    def fetch(self) -> tuple[Path, dict]:
        owner = self.store / "remote-checkouts" / json_digest({"remote": self.remote, "ref": self.ref})
        owner.mkdir(parents=True, exist_ok=True)
        repository = owner / "repository.git"
        def git(*arguments):
            result = subprocess.run(["git", *arguments], capture_output=True, text=True, timeout=60)
            if result.returncode:
                raise FreshnessError("remote_unverified", "fresh Git fetch/materialization failed")
            return result.stdout.strip()
        try:
            with file_lock(owner / "LOCK"):
                if not repository.exists():
                    git("init", "--bare", str(repository))
                git("--git-dir", str(repository), "fetch", "--no-tags", "--", self.remote, self.ref)
                commit = git("--git-dir", str(repository), "rev-parse", "FETCH_HEAD^{commit}")
                observed = datetime.now(timezone.utc).isoformat()
                checkout = owner / "commits" / commit
                if not checkout.exists():
                    checkout.parent.mkdir(parents=True, exist_ok=True)
                    git("--git-dir", str(repository), "worktree", "add", "--detach", str(checkout), commit)
                if git("-C", str(checkout), "rev-parse", "HEAD") != commit or git("-C", str(checkout), "status", "--porcelain", "--untracked-files=no"):
                    raise FreshnessError("source_invalid", "remote-owned checkout differs from its fetched immutable commit")
                root = checkout / "skills/photo-prompt-image-generator"
                if not root.is_dir():
                    raise FreshnessError("source_invalid", "remote commit has no photo skill")
                return root, {"mode": "remote_before_retrieval", "remote": self.remote, "ref": self.ref,
                              "commit": commit, "observed_at": observed}
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise FreshnessError("remote_unverified", "fresh Git fetch failed or timed out") from exc
