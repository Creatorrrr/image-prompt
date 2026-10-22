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

from photo_global_index_storage import atomic_write, canonical_bytes, decode, digest, json_digest
from photo_candidate_sources import SourceInventory
import photo_candidate_corpus
import photo_global_index
import photo_native_pack
import photo_search_layout
from photo_search_reader import LazyRuntimeData, identity

SKILL_ROOT = Path(__file__).resolve().parents[1]
GENERATION_SCHEMA = "photo-runtime-generation/v3"
RECEIPT_SCHEMA = "photo-runtime-receipt/v3"
HASH = re.compile(r"[0-9a-f]{64}\Z")
BASE_ASSETS = (photo_candidate_corpus.MANIFEST_NAME, photo_search_layout.MANIFEST)


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
    return {"code": LOADED_CODE, "environment": LOADED_ENVIRONMENT,
            "policy": canonical_bm25f_policy(photo_global_index.POLICY),
            "policy_version": "photo-global-bm25f-policy/v1",
            "tokenizer_recipe": BM25F_TOKENIZER_RECIPE_VERSION,
            "index_recipe": BM25F_INDEX_RECIPE_VERSION,
            "corpus_recipe": "native-global-candidates/v1",
            "field_projection_recipe": photo_global_index.RECIPE}


def algorithm_hash(generator) -> str:
    return json_digest(algorithm_binding(generator))


def default_store() -> Path:
    configured = os.environ.get("PHOTO_RUNTIME_STORE")
    return Path(configured).expanduser() if configured else Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))) / "image-prompt/photo-shared-runtime"


def namespace(root: Path, mode: str, remote: str = "") -> str:
    return json_digest({"schema":"photo-native-runtime-namespace/v3","root": str(Path(root).resolve()), "mode": mode, "remote": remote})


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


_SOURCE_HASH_CACHE = {}

def capture_sources(root: Path, *, pinned=None, full=False) -> tuple[dict, SourceInventory]:
    """Reuse publication-sealed identities; checksum changed bytes."""
    root=Path(root).resolve()
    try:
        inventory=SourceInventory.load(root/'assets')
        names=set(BASE_ASSETS)|{row[0] for row in inventory.rows}
        layout=decode(_regular(root,'assets/'+photo_search_layout.MANIFEST).read_bytes())
        if layout.get('schema')!=photo_search_layout.SCHEMA:raise ValueError('native lazy layout required')
        rows=layout['shards']+[layout['metadata']]
        if len({r['path'] for r in rows})!=len(rows):raise ValueError('duplicate search shard owner')
        declared={'assets/'+r['path']:r['sha256'] for r in rows}
        names={'assets/'+name for name in names}|set(declared)
        names|={name for name in ('embedding-runtime.lock.json','embedding-default.json','requirements-local-embeddings.txt') if (root/name).is_file()}
        names|={str(p.relative_to(root)) for p in (root/'precore').glob('*.json')}
        files={};sealed=(pinned or {}).get('origin_identity',{});known=(pinned or {}).get('source',{}).get('files',{})
        for name in sorted(names):
            path=_regular(root,name);current=identity(path);key=str(path);cached=_SOURCE_HASH_CACHE.get(key)
            if not full and list(current)==sealed.get(name) and name in known:sha=known[name]
            elif not full and cached and cached[0]==current:sha=cached[1]
            else:
                sha=digest(path.read_bytes())
                if identity(path)!=current:raise ValueError('source changed while hashing: '+name)
                _SOURCE_HASH_CACHE[key]=(current,sha)
            if name in declared and sha!=declared[name]:raise ValueError('live search shard checksum mismatch: '+name)
            files[name]=sha
        source={'files':files,'code':code_inventory(root),'environment':environment_binding()}
        if layout['space'].get('provider')=='embeddinggemma2-local':
            from photo_local_embedding import installed_binding
            source['embedding']=installed_binding()
        return source,inventory
    except (OSError,ValueError) as exc:
        if isinstance(exc,FreshnessError):raise
        raise FreshnessError('source_invalid',str(exc)) from exc


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
            or pointer.get("schema") != "photo-runtime-current/v3"
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

    def publish(self, *, observation=None, before_publish=None) -> dict:
        import prompt_generator as generator
        with file_lock(self.directory/'LOCK'):
            source,_=capture_sources(self.root,full=True);_require_implementation(source,generator)
            revision=_read(self.directory/'SOURCE.json',{'epoch':0,'editing':None})
            if revision.get('editing'):raise FreshnessError('source_revision_pending','maintenance revision unfinished')
            previous=_read_current(self.directory);algorithm=algorithm_hash(generator)
            origin_identity={rel:list(identity(_regular(self.root,rel))) for rel in source['files']}
        self.store.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.generation-',dir=self.store) as temporary:
            staging=Path(temporary);members={}
            paths=source['files']|source['code']
            for relative,sha in sorted(paths.items()):
                raw=_regular(self.root,relative).read_bytes()
                if digest(raw)!=sha:raise FreshnessError('source_revision_pending','source changed during copy: '+relative)
                target=staging/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);target.chmod(0o444)
                members[relative]={'sha256':sha,'bytes':len(raw),'identity':list(identity(target))}
            try:
                corpus=photo_candidate_corpus.load(staging/'assets');layout=decode((staging/'assets'/photo_search_layout.MANIFEST).read_bytes())
                qualification=photo_search_layout.verify(staging/'assets',corpus,layout)
            except (OSError,ValueError,KeyError,TypeError) as exc:raise FreshnessError('source_invalid','complete publication verification failed: '+str(exc)) from exc
            manifest={'schema':GENERATION_SCHEMA,'source':source,'source_fingerprint':json_digest(source),'origin_identity':origin_identity,
                      'members':members,'algorithm_sha256':algorithm,'search_layout':{'corpus_sha256':layout['corpus_sha256'],'layout_sha256':json_digest(layout),'layout_id':layout['layout_id'],'qualification':qualification}}
            generation=json_digest(manifest);atomic_write(staging/'manifest.json',canonical_bytes(manifest))
            if before_publish:before_publish()
            with file_lock(self.directory/'LOCK'):
                checked,_=capture_sources(self.root,full=True)
                if checked!=source or _read(self.directory/'SOURCE.json',{'epoch':0,'editing':None})!=revision or _read_current(self.directory)!=previous:
                    raise FreshnessError('source_revision_pending','source/pointer changed before publication')
                target=self.store/'generations'/generation;target.parent.mkdir(parents=True,exist_ok=True)
                if target.exists():self._verify_generation(target,generation,full=True)
                else:os.rename(staging,target)
                pointer={'schema':'photo-runtime-current/v3','generation_id':generation,'source_fingerprint':manifest['source_fingerprint'],'revision':int((previous or {}).get('revision',0))+1,
                         'observation':observation or {'mode':self.mode,'root':str(self.root),'observed_at':datetime.now(timezone.utc).isoformat(),'local_epoch':revision['epoch']}}
                atomic_write(self.directory/'CURRENT.json',canonical_bytes(pointer));return pointer

    @staticmethod
    def _verify_generation(root: Path, generation: str, *, full=False) -> dict:
        if not HASH.fullmatch(generation):raise FreshnessError('source_invalid','invalid generation ID')
        manifest=decode(_regular(root,'manifest.json').read_bytes())
        if manifest.get('schema')!=GENERATION_SCHEMA or json_digest(manifest)!=generation or manifest.get('source_fingerprint')!=json_digest(manifest.get('source')):
            raise FreshnessError('source_invalid','generation manifest checksum/schema mismatch')
        for relative,row in manifest['members'].items():
            path=_regular(root,relative)
            if full or list(identity(path))!=row['identity']:
                raw=path.read_bytes()
                if digest(raw)!=row['sha256'] or len(raw)!=row['bytes']:raise FreshnessError('source_invalid','generation member checksum mismatch: '+relative)
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
    if isinstance(value,(FrozenDict,FrozenList)):return value
    if isinstance(value, dict):
        return FrozenDict({key: freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return FrozenList(freeze(item) if isinstance(item, (dict, list)) else item for item in value)
    return value


class BoundRuntimeData(FrozenDict):
    __slots__=('reader',)
    def __init__(self,data):
        dict.__init__(self,freeze(dict(data)));object.__setattr__(self,'reader',data.reader)
    def __setattr__(self,*args):raise FreshnessError('source_invalid','bound snapshot object mutation')
    def for_core(self,core):return LazyRuntimeData(self.reader).for_core(core)


@dataclass(frozen=True)
class RuntimeSnapshot:
    generation_id: str
    root: Path
    manifest: dict
    data: BoundRuntimeData
    cache_status: str
    observation: dict | None = None
    query_context: dict | None = None


class RuntimeSnapshotProvider:
    def __init__(self, root: Path = SKILL_ROOT, store: Path | None = None, *, mode="local_current", remote="", ref="main"):
        if mode not in ("local_current", "remote_before_retrieval"):
            raise ValueError("unsupported photo source mode")
        self.publisher = SnapshotPublisher(root, store, mode=mode, remote=remote)
        self.mode, self.remote, self.ref = mode, remote, ref
        self._snapshots = {}
        self._lock = threading.RLock()
        self.last_observation = None

    def acquire(self, *, bootstrap=False) -> RuntimeSnapshot:
        import prompt_generator as generator
        with self._lock:
            if self.mode=='remote_before_retrieval':
                root,observation=RemoteSourceUpdater(self.publisher.store,self.remote,self.ref).fetch()
                self.publisher=SnapshotPublisher(root,self.publisher.store,mode=self.mode,remote=self.remote);self.last_observation=observation
            with file_lock(self.publisher.directory/'LOCK'):
                revision=_read(self.publisher.directory/'SOURCE.json',{'epoch':0,'editing':None});pointer=_read_current(self.publisher.directory)
            if revision.get('editing'):raise FreshnessError('source_revision_pending','maintenance revision unfinished')
            if pointer is None:raise FreshnessError('source_revision_pending','publish the fully verified search generation before retrieval')
            manifest=SnapshotPublisher._verify_generation(self.publisher.store/'generations'/pointer['generation_id'],pointer['generation_id'])
            source,_=capture_sources(self.publisher.root,pinned=manifest);_require_implementation(source,generator)
            if pointer['source_fingerprint']!=json_digest(source):raise FreshnessError('source_revision_pending','source changed; complete maintenance publication')
            checked,_=capture_sources(self.publisher.root,pinned=manifest)
            with file_lock(self.publisher.directory/'LOCK'):
                if checked!=source or _read_current(self.publisher.directory)!=pointer or _read(self.publisher.directory/'SOURCE.json',{'epoch':0,'editing':None})!=revision:
                    raise FreshnessError('source_revision_pending','source changed during acquisition')
            self.last_observation=self.last_observation if self.mode=='remote_before_retrieval' else {'mode':self.mode,'root':str(self.publisher.root),'local_epoch':revision['epoch'],'observed_at':datetime.now(timezone.utc).isoformat()}
            snapshot=self.load_generation(pointer['generation_id']);snapshot.data.reader.check_presence()
            return replace(snapshot,observation=freeze(self.last_observation))

    def load_generation(self,generation:str,*,independent_audit=False)->RuntimeSnapshot:
        import prompt_generator as generator
        with self._lock:
            root=self.publisher.store/'generations'/generation;manifest=SnapshotPublisher._verify_generation(root,generation)
            _require_implementation(manifest['source'],generator)
            if manifest['algorithm_sha256']!=algorithm_hash(generator):raise FreshnessError('runtime_restart_required','bound snapshot algorithm changed')
            if generation in self._snapshots:
                snapshot=self._snapshots[generation];snapshot.data.reader.check_presence();return snapshot
            try:
                data=generator.load_runtime_data(root/'assets');bound=BoundRuntimeData(data)
                if bound['_corpus_sha256']!=manifest['search_layout']['corpus_sha256'] or bound['_global_index_sha256']!=manifest['search_layout']['layout_sha256']:raise ValueError('generation layout binding mismatch')
            except (OSError,ValueError,KeyError,TypeError) as exc:raise FreshnessError('source_invalid','lazy generation load failed: '+str(exc)) from exc
            import photo_native_permission
            photo_native_permission._register_generation_transports(bound['_guard_source']['candidates'],
                source_fingerprint=manifest['source_fingerprint'],corpus_sha256=manifest['search_layout']['corpus_sha256'])
            snapshot=RuntimeSnapshot(generation,root,freeze(manifest),bound,'lazy_verified');self._snapshots[generation]=snapshot
            while len(self._snapshots)>2:self._snapshots.pop(next(iter(self._snapshots)))
            return snapshot

    def receipt(self, snapshot: RuntimeSnapshot, pack: dict) -> dict:
        import prompt_generator as generator
        pack_hash = json_digest(pack)
        if pack.get("global_retrieval", {}).get("corpus_sha256") != snapshot.manifest["search_layout"]["corpus_sha256"]:
            raise FreshnessError("source_invalid", "pack corpus binding differs from acquired generation")
        value = {"schema": RECEIPT_SCHEMA, "query_context": getattr(pack,"query_context",None), "request_id": uuid.uuid4().hex, "generation_id": snapshot.generation_id,
                 "pack_sha256": pack_hash, "observation": snapshot.observation,
                 "source_fingerprint": snapshot.manifest["source_fingerprint"],
                 "algorithm_sha256": snapshot.manifest["algorithm_sha256"],
                 "search_layout_sha256": snapshot.manifest["search_layout"]["layout_sha256"],
                 "cache_status": snapshot.cache_status, "bindings": pack_bindings(pack)}
        verify_pack_bindings(pack, snapshot, generator, query_context=getattr(pack,"query_context",None))
        value["canonical_sha256"] = json_digest(value)
        atomic_write(self.publisher.store / "receipts" / f"{value['request_id']}.json", canonical_bytes(value))
        with file_lock(self.publisher.store / "receipts/LOCK"):
            target = self.publisher.store / "receipt-index" / f"{pack_hash}.json"
            previous = _read(target, {"schema": "photo-runtime-receipt-index/v3", "generations": {}})
            previous["generations"][snapshot.generation_id] = value["request_id"]
            atomic_write(target, canonical_bytes(previous))
        return value

    def from_receipt(self, pack: dict, receipt: dict | None = None) -> RuntimeSnapshot:
        import prompt_generator as generator
        if receipt is None:
            index = _read(self.publisher.store / "receipt-index" / f"{json_digest(pack)}.json")
            if index is not None:
                if index.get("schema") != "photo-runtime-receipt-index/v3" or not isinstance(index.get("generations"), dict):
                    raise FreshnessError("source_invalid", "invalid runtime receipt index")
                if len(index["generations"]) != 1:
                    raise FreshnessError("source_invalid", "ambiguous runtime receipt: supply the exact request receipt")
                request = next(iter(index["generations"].values()))
                if not isinstance(request, str) or not re.fullmatch(r"[0-9a-f]{32}", request):
                    raise FreshnessError("source_invalid", "invalid runtime receipt request ID")
                receipt = _read(self.publisher.store / "receipts" / f"{request}.json")
        if not isinstance(receipt, dict):
            raise FreshnessError("source_invalid", "missing runtime receipt; a native v10 request receipt is required")
        request_id=receipt.get('request_id','')
        if not re.fullmatch(r'[0-9a-f]{32}',request_id):raise FreshnessError('source_invalid','invalid native receipt identity')
        stored=_read(self.publisher.store/'receipts'/f'{request_id}.json')
        if stored!=receipt:raise FreshnessError('source_invalid','receipt is not the original runtime-issued request evidence')
        body = {key: value for key, value in receipt.items() if key != "canonical_sha256"}
        if (receipt.get("schema") != RECEIPT_SCHEMA or receipt.get("canonical_sha256") != json_digest(body)
                or receipt.get("pack_sha256") != json_digest(pack) or receipt.get("bindings") != pack_bindings(pack)):
            raise FreshnessError("source_invalid", "receipt/pack binding mismatch")
        snapshot = self.load_generation(receipt["generation_id"], independent_audit=True)
        if (receipt["source_fingerprint"] != snapshot.manifest["source_fingerprint"]
                or receipt["algorithm_sha256"] != snapshot.manifest["algorithm_sha256"]
                or receipt["search_layout_sha256"] != snapshot.manifest["search_layout"]["layout_sha256"]):
            raise FreshnessError("source_invalid", "receipt generation binding mismatch")
        verify_pack_bindings(pack, snapshot, generator, recompute_visual=True, query_context=receipt.get("query_context"))
        return replace(snapshot,query_context=freeze(receipt.get("query_context")))


def pack_bindings(pack: dict) -> dict:
    return {"tags_hash": (pack.get("provenance") or {}).get("tags_hash"), "authorial_core_sha256": (pack.get("authorial_core") or {}).get("canonical_sha256"),
            "global_retrieval_sha256": (pack.get("global_retrieval") or {}).get("canonical_sha256"),
            "corpus_sha256": (pack.get("global_retrieval") or {}).get("corpus_sha256"),
            "visual": {key: json_digest(pack.get(key)) for key in ("visual_obligations", "visual_concept_candidates", "semantic_clarification")}}


def verify_pack_bindings(pack: dict, snapshot: RuntimeSnapshot, generator, *, recompute_visual=False, query_context=None) -> None:
    from photo_validation_context import is_context, validate as validate_context, build as build_context
    if is_context(pack):
        validate_context(pack)
        if (pack['global_retrieval']['corpus_sha256'] != snapshot.manifest['search_layout']['corpus_sha256']
                or pack['provenance']['tags_hash'] != generator.dictionary_hash(snapshot.data)):
            raise FreshnessError('source_invalid', 'validation context source changed')
        if query_context is not None:
            raise FreshnessError('source_invalid', 'validation context must not carry native slot queries')
        if recompute_visual and pack != build_context(snapshot.data, pack['authorial_core'], pack['creative_controls'],
                                                      pack['embodiment_preflight']['baseline_review']):
            raise FreshnessError('source_invalid', 'validation context differs from pinned core compilation')
        return
    photo_native_pack.validate(pack)
    import photo_slot_queries,photo_slot_retrieval
    record=pack['global_retrieval'];mode=record['mode'];data=snapshot.data.for_core(pack['authorial_core'])
    slots=photo_slot_retrieval.active_slots(data,pack['authorial_core'],pack['creative_controls'],record['requested_slot_ids'])
    if mode=='hybrid_required':
        photo_slot_queries.validate_set(query_context,pack['authorial_core'],pack['creative_controls'],data['slot_catalog'],slots,space=data.reader.manifest['space'])
        if record['query_context_sha256']!=query_context['canonical_sha256']:raise FreshnessError('source_invalid','receipt slot context mismatch')
    elif mode!='keyword_only' or query_context is not None:raise FreshnessError('source_invalid','invalid query execution mode')
    if ((pack.get("provenance") or {}).get("tags_hash") != generator.dictionary_hash(snapshot.data)
            or (pack.get("global_retrieval") or {}).get("corpus_sha256") != snapshot.manifest["search_layout"]["corpus_sha256"]):
        raise FreshnessError("source_invalid", "pack shared corpus source binding mismatch")
    if recompute_visual:
        expected = generator.generate_candidate_pack(snapshot.data, pack["authorial_core"], pack["creative_controls"],
            pack["embodiment_preflight"]["baseline_review"], seed=pack["provenance"]["seed"],
            visual_intent=pack.get("visual_intent"),query_context=query_context,retrieval_mode=pack["global_retrieval"]["mode"],requested_slots=record["requested_slot_ids"],query_language=record["query_language"])
        if pack != expected:
            raise FreshnessError("source_invalid", "full candidate pack differs from pinned generation recomputation")




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
