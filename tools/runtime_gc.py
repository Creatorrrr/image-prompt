#!/usr/bin/env python3
"""Conservative, project-scoped runtime/temp collection (dry run by default).

This deliberately lives outside the sealed skill. It never collects skill
assets, generated results, receipts, Git objects, or research evidence.
Only --apply advances the persistent unused-observation clock.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager, ExitStack
from dataclasses import dataclass
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import time
import uuid

SCHEMA = "image-prompt-runtime-gc/v1"
HEX = re.compile(r"[0-9a-f]{64}\Z")
IDS = re.compile(rb"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")
DAY = 86400
SKIP = {".git", ".venv", ".runtime", "node_modules", "__pycache__",
        "assets", "generations", "h-f2-generations", "body",
        "source-data", "global-index-data"}
OS_INDEXERS = {"mds", "mds_stores", "mdworker", "mdworker_shared", "mdworker_sizing"}
GIT_PROGRAMS = {"git", "git-pack-objects", "git-index-pack", "git-gc", "git-repack",
                "pack-objects", "index-pack"}


class Unsafe(RuntimeError):
    """Missing or changing evidence must stop collection, never broaden it."""


class Deferred(Unsafe):
    """Expected concurrent work; retry on the next scheduled pass."""


def require(test, message):
    if not test:
        raise Unsafe(message)


def defer(test, message):
    if not test:
        raise Deferred(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inside(path, root):
    return path == root or root in path.parents


def no_links(path):
    require(not any(p.is_symlink() for p in (path, *path.parents)),
            "symlink in managed path: " + str(path))


def signature(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns,
            s.st_ctime_ns, s.st_nlink]


def read(path):
    no_links(path)
    return json.loads(path.read_bytes())


def atomic_json(path, value):
    no_links(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with temporary.open("xb") as handle:
            handle.write(canonical(value) + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def walk(root):
    """Never follow a directory link, including links to the Python runtime."""
    if root.is_symlink():
        yield root
        return
    def failed(error):
        raise error
    for base, dirs, files in os.walk(root, followlinks=False, onerror=failed):
        for name in list(dirs):
            path = Path(base) / name
            if path.is_symlink():
                dirs.remove(name)
                yield path
        for name in files:
            yield Path(base) / name


def inventory(root, *, bytecode=True):
    paths = list(walk(root)) if root.is_dir() else [root]
    rows = []
    for p in paths:
        if p.name == ".DS_Store":
            continue
        if not bytecode and ("__pycache__" in p.parts or p.suffix in {".pyc", ".pyo"}):
            continue
        relative = str(p.relative_to(root)) if root.is_dir() else "."
        s = p.lstat()
        require(stat.S_ISREG(s.st_mode) or stat.S_ISLNK(s.st_mode), "special file: " + str(p))
        rows.append([relative, *signature(p), os.readlink(p) if p.is_symlink() else None])
    return sorted(rows)


@dataclass(frozen=True)
class Policy:
    repo: Path
    store: Path
    state: Path
    evidence: tuple = ()
    runtime_age: int = 2 * DAY
    temp_age: int = DAY
    unused_grace: int = DAY
    observation_gap: int = 6 * 3600
    keep_recent: int = 2
    batch: int = 8

    @property
    def stores(self):
        return (self.store, self.store / "h-f2-installed")

    def validate(self):
        for p in (self.repo, self.store, self.state, *self.evidence):
            require(p.is_absolute(), "absolute paths required")
            require(p == Path(os.path.abspath(p)), "managed paths must be normalized")
            no_links(p)
        require(not inside(self.store, self.repo) and not inside(self.repo, self.store),
                "runtime store must be separate from the project")
        require(not inside(self.state, self.repo) and not inside(self.state, self.store)
                and not inside(self.repo, self.state) and not inside(self.store, self.state)
                and not any(inside(p, self.state) for p in self.evidence),
                "collector state must be outside protected/deletion roots")
        require(self.runtime_age >= 2 * DAY and self.temp_age >= DAY
                and self.unused_grace >= DAY and self.observation_gap >= 6 * 3600
                and self.keep_recent >= 2 and 1 <= self.batch <= 8,
                "retention safety floors cannot be disabled")


class Environment:
    def __init__(self, policy):
        self.policy = policy

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.policy.repo), *args], check=True,
                              capture_output=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"),
                              timeout=60).stdout

    def worktrees(self):
        raw = self.git("worktree", "list", "--porcelain", "-z")
        roots = [Path(v[9:].decode()) for v in raw.split(b"\0") if v.startswith(b"worktree ")]
        require(self.policy.repo in roots, "project is not a registered worktree")
        for root in roots:
            no_links(root)
            require(root.is_dir(), "missing registered worktree: " + str(root))
        return roots

    def git_dir(self):
        return Path(self.git("rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip())

    def usage(self):
        result = subprocess.run(["lsof", "-nP", "-Fpcfn"], capture_output=True, timeout=55)
        require(result.returncode == 0 and not result.stderr.strip(), "cannot verify open files with lsof")
        handles = []
        pid = command = fd = ""
        for line in result.stdout.decode(errors="replace").splitlines():
            if line.startswith("p"):
                pid = line[1:]
            elif line.startswith("c"):
                command = line[1:]
            elif line.startswith("f"):
                fd = line[1:]
            elif line.startswith("n/") and int(pid) != os.getpid() and command not in OS_INDEXERS:
                handles.append((pid, command, fd, Path(line[1:].removesuffix(" (deleted)"))))
        processes = subprocess.run(["ps", "-axo", "pid=,comm=,args="], check=True,
                                   capture_output=True, timeout=15).stdout
        # Do not persist raw arguments: unrelated jobs may carry secrets.
        return handles, processes

    def git_busy(self, processes):
        common = self.git_dir()
        if any((common / name).exists() for name in ("index.lock", "packed-refs.lock", "config.lock",
                                                     "shallow.lock", "gc.pid", "gc.log.lock", "maintenance.lock")):
            return True
        names = subprocess.run(["ps", "-axo", "comm="], capture_output=True,
                               check=True, text=True, timeout=15).stdout.splitlines()
        return any(Path(n.strip()).name in GIT_PROGRAMS for n in names)

    def git_garbage(self):
        result = subprocess.run(["git", "-C", str(self.policy.repo), "count-objects", "-v"],
                                check=True, capture_output=True, timeout=60,
                                env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"))
        found = set()
        for line in result.stderr.decode().splitlines():
            require("garbage found: " in line, "unexpected Git inventory warning")
            raw = Path(line.split("garbage found: ", 1)[1])
            found.add(raw if raw.is_absolute() else self.policy.repo / raw)
        return found

    def git_identity(self):
        refs = [row for row in self.git("for-each-ref", "--format=%(refname) %(objectname)").splitlines()
                if not row.startswith(b"refs/codex/")]
        packs = {}
        for p in (self.git_dir() / "objects/pack").glob("pack-*"):
            packs[p.name] = signature(p)[:4]
        return {"head": self.git("rev-parse", "HEAD").decode().strip(),
                "refs": digest([x.decode() for x in refs]),
                "staging": hashlib.sha256(self.git("ls-files", "--stage", "-z")).hexdigest(),
                "flags": hashlib.sha256(self.git("ls-files", "-v", "-z")).hexdigest(),
                "packs": packs}

    def smoke(self):
        """Use the installed code, not an import of the changing working skill."""
        skill = self.policy.repo / "skills/photo-prompt-image-generator"
        config = read(skill / "retrieval-runtime.json")
        native = self.policy.stores[1] / "generations" / config["native_generation_id"]
        lock = read(skill / "embedding-runtime.lock.json")
        python = skill / lock["python"]
        require(inside(python, skill) and python.is_file(), "missing pinned Python")
        program = """import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from photo_installed_h_f2 import release
from photo_runtime_sources import RuntimeSnapshotProvider
root,m,_=release(sys.argv[2],sys.argv[3],full=True)
lock=json.loads((root/'embedding-runtime.lock.json').read_bytes())
for relative,row in lock['files'].items():
    path=root/lock['package']/relative
    if path.is_symlink() or '..' in Path(relative).parts or Path(relative).is_absolute():
        raise ValueError('unsafe model member')
    with path.open('rb') as f:
        if hashlib.file_digest(f,'sha256').hexdigest()!=row['sha256']:
            raise ValueError('installed model changed')
snapshot=RuntimeSnapshotProvider(store=sys.argv[2]).load_generation(m['native_generation_id'])
snapshot.data.reader.check_presence()
print('installed release and native reader PASS')
"""
        env = dict(os.environ, HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", PYTHONNOUSERSITE="1",
                   PYTHONDONTWRITEBYTECODE="1")
        env.pop("PYTHONPATH", None)
        for key in ("OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY"):
            env.pop(key, None)
        result = subprocess.run([str(python), "-B", "-I", "-c", program, str(native / "scripts"),
                                 str(self.policy.stores[1]), config["generation_id"]],
                                capture_output=True, env=env, timeout=180)
        require(result.returncode == 0, "installed runtime smoke failed")


class Collector:
    def __init__(self, policy, env=None, now=None, *, waive_runtime_observation_wait=False):
        policy.validate()
        self.policy = policy
        self.env = env or Environment(policy)
        self.now = time.time() if now is None else now
        self.waive_runtime_observation_wait = waive_runtime_observation_wait
        self.controls = {}

    def control(self, path):
        before = signature(path)
        raw = path.read_bytes()
        require(signature(path) == before, "reference changed during read: " + str(path))
        self.controls[str(path)] = hashlib.sha256(raw).hexdigest()
        return raw

    def nodes(self):
        out = {}
        for store in self.policy.stores:
            no_links(store)
            for group in ("generations", "h-f2-generations"):
                parent = store / group
                no_links(parent)
                if not parent.exists():
                    continue
                for root in parent.iterdir():
                    if not HEX.fullmatch(root.name):
                        continue
                    no_links(root)
                    m = read(root / "manifest.json")
                    expected = "photo-h-f2-generation/v1" if group == "h-f2-generations" else "photo-runtime-generation/v3"
                    require(isinstance(m, dict) and m.get("schema") == expected and digest(m) == root.name,
                            "invalid generation seal: " + str(root))
                    require(isinstance(m.get("files", m.get("members")), dict)
                            and bool(m.get("files", m.get("members"))), "missing generation members")
                    native = m.get("native_generation_id")
                    if group == "h-f2-generations":
                        require(isinstance(native, str) and HEX.fullmatch(native), "invalid native dependency")
                    inv = inventory(root)
                    out[str(root)] = {"kind": "runtime", "group": group, "store": str(store),
                                      "native": native, "manifest": m, "inventory": inv,
                                      "fingerprint": digest(inv), "latest": max(
                                          [root.stat().st_mtime] + [max(r[5], r[6]) / 1e9 for r in inv])}
        for row in out.values():
            if row["native"]:
                require(str(Path(row["store"]) / "generations" / row["native"]) in out,
                        "missing paired native generation")
        return out

    def references(self, nodes):
        self.controls = {}
        self.reference_text = []
        pins = defaultdict(set)
        missing = []
        roots = self.env.worktrees()
        known_ids = {Path(p).name for p in nodes}
        # Explicitly retired historical records stay on disk as evidence.
        # Only the exact reviewed bytes lose their runtime pin; any change
        # automatically restores the ordinary conservative reference scan.
        retirement_file = self.policy.state / "retired-references.json"
        retired = {}
        if retirement_file.exists():
            no_links(retirement_file)
            record = json.loads(self.control(retirement_file))
            require(isinstance(record, dict) and record.get("schema") == "image-prompt-retired-references/v1"
                    and isinstance(record.get("entries"), list), "invalid retirement record")
            for entry in record["entries"]:
                require(isinstance(entry, dict) and entry.get("kind") in {"workflow", "historical_script"}
                        and isinstance(entry.get("path"), str) and isinstance(entry.get("sha256"), str)
                        and HEX.fullmatch(entry["sha256"]), "invalid retired reference")
                path = Path(entry["path"])
                require(path.is_absolute() and path == Path(os.path.abspath(path))
                        and any(inside(path, root) for root in roots)
                        and str(path) not in retired, "unsafe retired reference")
                require((entry["kind"] == "workflow" and path.name == "workflow.json") or
                        (entry["kind"] == "historical_script" and path.suffix in {".py", ".sh", ".toml"}),
                        "retired reference kind mismatch")
                retired[str(path)] = entry
        retired_active_paths = []

        def is_retired(path, raw, kind):
            item = retired.get(str(path))
            if item is None or item["kind"] != kind or hashlib.sha256(raw).hexdigest() != item["sha256"]:
                return False
            retired_active_paths.append(path.parent if kind == "workflow" else path)
            return True

        def pin(path, why, required=False):
            key = str(path)
            pins[key].add(why)
            if required:
                require(path.is_dir() and key in nodes, "missing current generation: " + key)

        def text(raw, why):
            self.reference_text.append(raw)
            ids = {m.decode() for m in IDS.findall(raw)} & known_ids
            for p in nodes:
                if Path(p).name in ids:
                    pin(Path(p), why)

        for repo in roots:
            config_path = repo / "skills/photo-prompt-image-generator/retrieval-runtime.json"
            no_links(config_path)
            c = json.loads(self.control(config_path))
            require(isinstance(c, dict) and c.get("schema") == "photo-installed-h-f2/v1"
                    and c.get("store_subdirectory") == "h-f2-installed",
                    "unknown installed configuration")
            for field, group in (("generation_id", "h-f2-generations"), ("native_generation_id", "generations")):
                require(isinstance(c.get(field), str) and HEX.fullmatch(c[field]), "invalid installed ID")
                pin(self.policy.stores[1] / group / c[field], "installed default", True)
            row = nodes[str(self.policy.stores[1] / "h-f2-generations" / c["generation_id"])]
            require(row["native"] == c["native_generation_id"], "installed pair differs")
        for store in self.policy.stores:
            for kind in ("local", "remote"):
                parent = store / kind
                no_links(parent)
                for p in parent.glob("*/CURRENT.json"):
                    no_links(p)
                    v = json.loads(self.control(p))
                    require(isinstance(v, dict) and v.get("schema") == "photo-runtime-current/v3"
                            and isinstance(v.get("generation_id"), str) and HEX.fullmatch(v["generation_id"]),
                            "unknown CURRENT pointer")
                    pin(store / "generations" / v["generation_id"], "CURRENT", True)
                for p in parent.glob("*/SOURCE.json"):
                    no_links(p)
                    v = json.loads(self.control(p))
                    require(isinstance(v, dict) and type(v.get("epoch")) is int and v["epoch"] >= 0,
                            "unknown source revision state")
                    defer(v.get("editing") is None, "source revision is in progress")

        scanned = set()
        count = 0
        search_roots = [*roots, *self.policy.evidence, self.policy.store]
        for root in search_roots:
            require(root.is_dir(), "missing reference scan root: " + str(root))
            def failed(error):
                raise error
            for base, ds, fs in os.walk(root, followlinks=False, onerror=failed):
                here = Path(base)
                if here in scanned:
                    ds[:] = []
                    continue
                scanned.add(here)
                if inside(here, self.policy.state):
                    ds[:] = []
                    continue
                for name in list(ds):
                    p = here / name
                    if p.is_symlink():
                        target = p.resolve(strict=False)
                        for q in (target, *target.parents):
                            if str(q) in nodes:
                                pin(q, "working symlink")
                        ds.remove(name)
                # Raw trend corpora contain copied fixture workflows, not live
                # runs.  A similarly named directory under photo-runs or
                # research evidence can contain a real unfinished workflow.
                raw_roots = (repo / "generated/trend-scout/raw" for repo in roots)
                in_trend_raw = any(inside(here, raw_root) for raw_root in raw_roots)
                ds[:] = [d for d in ds if d not in SKIP and not
                         (in_trend_raw and "reactorprompt" in d.lower())]
                for name in fs:
                    p = here / name
                    if p.is_symlink():
                        target = p.resolve(strict=False)
                        for q in (target, *target.parents):
                            if str(q) in nodes:
                                pin(q, "working symlink")
                if "workflow.json" in fs:
                    p = here / "workflow.json"
                    no_links(p)
                    raw = self.control(p)
                    v = json.loads(raw)
                    require(isinstance(v, dict) and isinstance(v.get("operations", []), list), "unknown workflow")
                    count += 1
                    terminal = (v.get("schema_version") == "photo-workflow-run/v2"
                                and v.get("phase") == "review_record_validated"
                                and all(isinstance(op, dict) and op.get("status") in
                                        {"complete", "provider_blocked", "preflight_failed"}
                                        and op.get("last_event", {}).get("terminal") is True
                                        for op in v.get("operations", [])))
                    if not terminal and not is_retired(p, raw, "workflow"):
                        text(raw, "unfinished workflow: " + str(p))
                        for key, group in (("h_f2_binding", "h-f2-generations"), ("source_binding", "generations")):
                            binding = v.get(key)
                            if not binding:
                                continue
                            require(isinstance(binding, dict), "invalid workflow binding")
                            location = binding.get("store") or binding.get("runtime_store")
                            gid = binding.get("generation_id")
                            require(isinstance(location, str) and isinstance(gid, str) and HEX.fullmatch(gid),
                                    "invalid workflow generation")
                            q = Path(location) / group / gid
                            pin(q, "unfinished workflow: " + str(p))
                            if not q.exists():
                                missing.append({"workflow": str(p), "generation": str(q)})
                        for role, artifact in v.get("artifacts", {}).items():
                            # Core prose/configuration cannot select an installed
                            # generation. Only runtime/retry bindings need replay.
                            if not any(token in role for token in ("runtime", "h_f2", "retry", "pack")):
                                continue
                            if not isinstance(artifact, dict) or "path" not in artifact:
                                raise Unsafe("unknown workflow artifact")
                            q = Path(artifact["path"])
                            self.reference_text.append(str(q).encode())
                            if q.suffix == ".json":
                                require(q.is_absolute(), "relative workflow artifact")
                                no_links(q)
                                require(q.is_file(), "missing unfinished workflow artifact: " + str(q))
                                text(self.control(q), "unfinished workflow artifact")
                # Code/configuration pins outside generated research archives.
                if any(inside(here, repo) for repo in roots):
                    for name in fs:
                        p = here / name
                        if p.suffix in {".py", ".sh", ".toml"} and not p.is_symlink():
                            raw = self.control(p)
                            if not is_retired(p, raw, "historical_script"):
                                text(raw, "skill executable reference")

        pin_file = self.policy.state / "pins.json"
        if pin_file.exists():
            v = json.loads(self.control(pin_file))
            require(isinstance(v, list) and all(isinstance(x, str) and HEX.fullmatch(x) for x in v),
                    "pins.json must contain generation IDs")
            text(canonical(v), "explicit user pin")
        handles, processes = self.env.usage()
        for path in retired_active_paths:
            spellings = [str(path)] + [str(path.relative_to(root)) for root in roots if inside(path, root)]
            defer(not any(s.encode() in processes for s in spellings),
                  "retired workflow or historical script is running: " + str(path))
        text(processes, "running process")
        for _pid, _cmd, _fd, path in handles:
            for q in (path, *path.parents):
                if str(q) in nodes:
                    pin(q, "open file or mapping")
        # Maintenance commands can be between copying and activating a release.
        producer = any(token in line for line in processes.splitlines()
                       if not line.lstrip().startswith(str(os.getpid()).encode() + b" ")
                       for token in (b"install_photo_h_f2_runtime", b"publish_photo_runtime_snapshot",
                                     b"photo_runtime_sources import", b"photo_h_f2_generation import"))
        if producer:
            for p in nodes:
                pin(Path(p), "runtime publication/installation process")

        for store in self.policy.stores:
            for group in ("generations", "h-f2-generations"):
                choices = [p for p, row in nodes.items() if row["store"] == str(store) and row["group"] == group]
                for p in sorted(choices, key=lambda p: nodes[p]["latest"], reverse=True)[:self.policy.keep_recent]:
                    pin(Path(p), "recent rollback generation")
        changed = True
        while changed:
            before = set(pins)
            for p in list(pins):
                if p not in nodes:
                    continue
                row = nodes[p]
                if row["native"]:
                    pin(Path(row["store"]) / "generations" / row["native"], "paired native dependency")
                for rel, *_ in row["inventory"]:
                    q = Path(p) / rel
                    if q.is_symlink():
                        target = q.resolve(strict=False)
                        for parent in (target, *target.parents):
                            if str(parent) in nodes:
                                pin(parent, "retained runtime symlink")
            changed = before != set(pins)
        return pins, {"workflows_scanned": count, "missing_unfinished_bindings": missing}, handles, processes

    def temps(self):
        targets = []
        for store in self.policy.stores:
            targets.extend(store.glob(".generation-*"))
            targets.extend(store.glob(".h-f2-*"))
            for group in ("generations", "h-f2-generations"):
                targets.extend((store / group).glob(".install-*"))
        common = self.env.git_dir()
        no_links(common)
        targets.extend((common / "objects/pack").glob("tmp_pack_*"))
        targets.extend((common / "objects").glob("??/tmp_obj_*"))
        rows = {}
        for p in targets:
            no_links(p)
            inv = inventory(p)
            rows[str(p)] = {"kind": "git-temp" if inside(p, common) else "runtime-temp",
                            "inventory": inv, "fingerprint": digest(inv), "latest": max(
                                [p.stat().st_mtime] + [max(r[5], r[6]) / 1e9 for r in inv])}
        return rows

    def allowed(self, path, row, *, missing=False):
        p = Path(path)
        no_links(p)
        if row["kind"] == "runtime":
            return (HEX.fullmatch(p.name) is not None and any(
                p.parent == s / g for s in self.policy.stores for g in ("generations", "h-f2-generations")))
        if row["kind"] == "runtime-temp":
            return any((p.parent == s and p.name.startswith((".generation-", ".h-f2-"))) or
                       (p.parent in {s / "generations", s / "h-f2-generations"} and p.name.startswith(".install-"))
                       for s in self.policy.stores)
        common = self.env.git_dir()
        return row["kind"] == "git-temp" and (missing or p.is_file()) and (
            (p.parent == common / "objects/pack" and p.name.startswith("tmp_pack_")) or
            (p.parent.parent == common / "objects" and re.fullmatch("[0-9a-f]{2}", p.parent.name)
             and p.name.startswith("tmp_obj_")))

    def plan(self, previous):
        nodes = self.nodes()
        pins, evidence, handles, processes = self.references(nodes)
        items = {**nodes, **self.temps()}
        for p, row in items.items():
            require(self.allowed(p, row), "path outside deletion allowlist: " + p)
            if self.now - row["latest"] < (self.policy.runtime_age if row["kind"] == "runtime" else self.policy.temp_age):
                pins[p].add("retention age")
            for _pid, _cmd, _fd, path in handles:
                if inside(path, Path(p)):
                    pins[p].add("open file or mapping")
            if str(p).encode() in processes:
                pins[p].add("running process path")
            if row["kind"] != "runtime" and any(p.encode() in raw for raw in self.reference_text):
                pins[p].add("live temporary path reference")
        if any(r["kind"] == "git-temp" for r in items.values()):
            garbage = self.env.git_garbage()
            busy = self.env.git_busy(processes)
            for p, row in items.items():
                if row["kind"] == "git-temp" and (busy or Path(p) not in garbage):
                    pins[p].add("Git active or temporary not confirmed as garbage")
        # Publication is also a veto for abandoned runtime staging directories.
        if any("runtime publication/installation process" in why for why in pins.values()):
            for p, row in items.items():
                if row["kind"] == "runtime-temp":
                    pins[p].add("runtime publication/installation process")
        # Never change the ctime of an inode still linked from a retained tree.
        while True:
            selected = set(items) - set(pins)
            links = Counter((r[1], r[2]) for p in selected for r in items[p]["inventory"] if stat.S_ISREG(r[3]))
            blocked = {p for p in selected if any(stat.S_ISREG(r[3]) and links[(r[1], r[2])] < r[7]
                                                 for r in items[p]["inventory"])}
            for p in blocked:
                pins[p].add("external hardlink")
            for p in list(pins):
                if p in nodes and nodes[p]["native"]:
                    pins[str(Path(nodes[p]["store"]) / "generations" / nodes[p]["native"])].add("paired native dependency")
            if selected == set(items) - set(pins):
                break
        observations = {}
        eligible = []
        for p in sorted(set(items) - set(pins)):
            row = items[p]
            old = previous.get(p, {})
            require(isinstance(old, dict), "invalid observation record")
            observed_before = old.get("fingerprint") == row["fingerprint"]
            if old.get("fingerprint") != row["fingerprint"]:
                old = {"fingerprint": row["fingerprint"], "since": self.now, "last": self.now, "count": 1}
            else:
                old = dict(old)
                require(type(old.get("count")) is int and old["count"] >= 1
                        and 0 <= old["since"] <= old["last"], "invalid observation clock")
                if old["last"] > self.now:
                    observed_before = False
                    old = {"fingerprint": row["fingerprint"], "since": self.now, "last": self.now, "count": 1}
                if self.now - old["last"] >= self.policy.observation_gap:
                    old.update(last=self.now, count=old["count"] + 1)
            observations[p] = old
            normal_wait = old["count"] >= 2 and self.now - old["since"] >= self.policy.unused_grace
            explicit_exception = (self.waive_runtime_observation_wait and row["kind"] == "runtime"
                                  and observed_before)
            if normal_wait or explicit_exception:
                eligible.append(p)
        # H-F2 releases go first. A native may disappear only with/after all its H-F2 dependants.
        eligible.sort(key=lambda p: (items[p].get("group") == "generations", p))
        batch = eligible[:self.policy.batch]
        while True:
            links = Counter((r[1], r[2]) for p in batch for r in items[p]["inventory"] if stat.S_ISREG(r[3]))
            keep = [p for p in batch if not any(stat.S_ISREG(r[3]) and links[(r[1], r[2])] < r[7]
                                               for r in items[p]["inventory"])]
            keep = [p for p in keep if not any(q not in keep and row["native"] and
                    str(Path(row["store"]) / "generations" / row["native"]) == p for q, row in nodes.items())]
            if keep == batch:
                break
            batch = keep
        return {"items": items, "nodes": nodes, "pins": {p: sorted(v) for p, v in pins.items()},
                "observations": observations, "eligible": batch, "evidence": evidence,
                "controls": dict(self.controls)}

    def verify_tree(self, root, row, *, renamed=False):
        def same_inventory():
            current = inventory(root)
            if renamed and not root.is_dir() and len(current) == 1:
                # rename changes a standalone file's ctime. Its inode, extent,
                # mtime and full checksum must still agree on both sides.
                current[0][6] = row["inventory"][0][6]
            return current == row["inventory"]
        require(same_inventory(), "candidate changed: " + str(root))
        if row["kind"] != "runtime":
            # Stability is checked again after the full content checksum.
            hashes = {r[0]: sha(root / r[0] if root.is_dir() else root)
                      for r in row["inventory"] if stat.S_ISREG(r[3])}
        else:
            manifest = row["manifest"]
            hashes = {}
            for rel, expected in manifest.get("files", manifest.get("members", {})).items():
                p = root / rel
                require(not Path(rel).is_absolute() and ".." not in Path(rel).parts, "unsafe member")
                no_links(p)
                hashes[rel] = sha(p)
                require(hashes[rel] == (expected["sha256"] if isinstance(expected, dict) else expected),
                        "generation member seal changed")
        require(same_inventory(), "candidate changed during hashing")
        return hashes

    def protected(self, plan):
        return {p: inventory(Path(p), bytecode=False) for p in plan["nodes"] if p not in plan["eligible"]}

    def guard(self, plan, hidden=()):
        present = set()
        for store in self.policy.stores:
            for group in ("generations", "h-f2-generations"):
                parent = store / group
                no_links(parent)
                if parent.is_dir():
                    for p in parent.iterdir():
                        if HEX.fullmatch(p.name):
                            no_links(p)
                            require(p.is_dir(), "generation directory was replaced")
                            present.add(str(p))
        defer(present == set(plan["nodes"]) - {p for p, q in hidden},
              "runtime generation set changed; re-evaluate dependencies next pass")
        pins, _evidence, handles, processes = self.references(plan["nodes"])
        defer(self.controls == plan["controls"], "reference files changed; retry next run")
        defer(not any(p in pins for p in plan["eligible"]), "candidate acquired a reference")
        for p, q in hidden:
            require(not Path(p).exists(), "original candidate path was recreated")
            require(not any(inside(path, q) or inside(path, Path(p)) for _, _, _, path in handles),
                    "quarantined candidate is open")
            require(str(q).encode() not in processes and str(p).encode() not in processes,
                    "quarantined candidate process")
        if any(plan["items"][p]["kind"] == "git-temp" for p in plan["eligible"]):
            defer(not self.env.git_busy(processes), "Git became active")
        for p, row in plan["items"].items():
            if p in plan["eligible"] and row["kind"] != "runtime":
                defer(not any(p.encode() in raw for raw in self.reference_text), "temporary acquired a reference")
            if p in plan["eligible"] and row["kind"] == "runtime-temp":
                defer(not any("runtime publication/installation process" in why for why in pins.values()),
                        "runtime producer became active")

    def recover(self):
        journal = self.policy.state / "transaction.json"
        if not journal.exists():
            return
        v = read(journal)
        require(v.get("schema") == SCHEMA and v.get("scope") == self.scope(), "foreign collector transaction")
        require(v.get("phase") == "quarantine", "interrupted deletion requires inspection; files preserved")
        for row in reversed(v["moves"]):
            p, q = Path(row["original"]), Path(row["hidden"])
            require(self.allowed(str(p), row, missing=True), "unsafe recovery source")
            require(q.parent == p.parent and q.name.startswith(".runtime-gc-") and q.name.endswith("-" + p.name),
                    "unsafe recovery quarantine")
            no_links(q)
            if q.exists():
                require(not p.exists(), "recovery collision; both copies preserved")
                os.rename(q, p)
        journal.unlink()

    def scope(self):
        return digest({"repo": str(self.policy.repo), "store": str(self.policy.store),
                       "evidence": [str(p) for p in self.policy.evidence]})

    @contextmanager
    def producer_locks(self, plan):
        # Writers already share these locks. A busy writer vetoes this pass.
        # Missing locks are not created inside user research directories.
        ids = {Path(p).name.encode() for p in plan["eligible"] if plan["items"][p]["kind"] == "runtime"}
        paths = {Path(p).parent / ".LOCK" for p in plan["controls"]
                 if Path(p).name == "workflow.json" and ids.intersection(IDS.findall(Path(p).read_bytes()))}
        paths |= {Path(p).parent / "LOCK" for p in plan["controls"] if Path(p).name in {"CURRENT.json", "SOURCE.json"}}
        with ExitStack() as stack:
            for p in sorted(paths):
                if not p.exists():
                    continue
                no_links(p)
                handle = stack.enter_context(p.open("rb"))
                try:
                    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    raise Deferred("workflow/publication writer is active")
            yield

    def collect(self, plan):
        with self.producer_locks(plan):
            return self._collect_locked(plan)

    def _collect_locked(self, plan):
        hidden = []
        journal = self.policy.state / "transaction.json"
        record = {"schema": SCHEMA, "scope": self.scope(), "phase": "quarantine", "moves": [],
                  "runtime_observation_wait_waived": self.waive_runtime_observation_wait}
        self.env.smoke()
        protected = self.protected(plan)
        git_before = self.env.git_identity()
        hashes = {p: self.verify_tree(Path(p), plan["items"][p]) for p in plan["eligible"]}
        self.guard(plan)
        try:
            for p in plan["eligible"]:
                row = plan["items"][p]
                require(self.allowed(p, row), "candidate path changed")
                require(inventory(Path(p)) == row["inventory"], "candidate changed before quarantine")
                q = Path(p).with_name(".runtime-gc-" + uuid.uuid4().hex + "-" + Path(p).name)
                require(not q.exists(), "quarantine collision")
                record["moves"].append({"original": p, "hidden": str(q), "kind": row["kind"]})
                atomic_json(journal, record)
                os.rename(p, q)
                hidden.append((p, q))
            self.guard(plan, hidden)
            for p, q in hidden:
                require(self.verify_tree(q, plan["items"][p], renamed=True) == hashes[p], "quarantine content changed")
            self.env.smoke()
            require(self.protected(plan) == protected, "retained runtime changed")
            defer(self.env.git_identity() == git_before, "Git state changed")
            self.guard(plan, hidden)
        except BaseException:
            # Keep the journal if rollback collides; never overwrite a producer.
            for p, q in reversed(hidden):
                require(not Path(p).exists(), "rollback collision; both copies preserved")
                if q.exists():
                    os.rename(q, p)
            if journal.exists():
                journal.unlink()
            raise
        record["phase"] = "deleting"
        atomic_json(journal, record)
        for p, q in hidden:
            if q.is_dir():
                remove_owned_tree(q)
            else:
                q.unlink()
        journal.unlink()
        require(self.protected(plan) == protected, "retained runtime changed after collection")
        require(self.env.git_identity() == git_before, "Git state changed after collection")
        self.env.smoke()
        return [p for p, q in hidden]

    def run(self, apply=False):
        if apply:
            self.recover()
        require(not (self.policy.state / "transaction.json").exists(), "pending collector recovery")
        state_file = self.policy.state / "observations.json"
        previous = read(state_file) if state_file.exists() else {}
        require(isinstance(previous, dict), "invalid observation state")
        if previous:
            require(previous.get("schema") == SCHEMA and previous.get("scope") == self.scope(), "foreign observation state")
        plan = self.plan(previous.get("observations", {}))
        deleted = self.collect(plan) if apply and plan["eligible"] else []
        report = {"schema": SCHEMA, "status": "pass", "apply": apply, "observed_at": self.now,
                  "runtime_observation_wait_waived": self.waive_runtime_observation_wait,
                  "runtime_generations": len(plan["nodes"]), "retained_generations": sum(
                      p in plan["pins"] for p in plan["nodes"]),
                  "waiting_for_grace": len(plan["observations"]) - len(plan["eligible"]),
                  "eligible": plan["eligible"], "deleted": deleted, "preserved": plan["pins"],
                  **plan["evidence"]}
        if apply:
            atomic_json(state_file, {"schema": SCHEMA, "scope": self.scope(), "observations": {
                p: v for p, v in plan["observations"].items() if p not in deleted}})
            atomic_json(self.policy.state / "last-report.json", report)
        return report


def remove_owned_tree(root):
    def failed(function, name, info):
        error = info[1]
        if isinstance(error, FileNotFoundError):
            return
        # Finder may recreate this one metadata file during an otherwise
        # successful removal. A normal new file always stops collection.
        if isinstance(error, OSError) and error.errno == errno.ENOTEMPTY:
            p = Path(name)
            left = list(walk(p))
            if left and all(q.name == ".DS_Store" and not q.is_symlink() for q in left):
                for q in left:
                    q.unlink()
                shutil.rmtree(p)
                return
        raise error
    shutil.rmtree(root, onerror=failed)


@contextmanager
def collector_lock(state):
    no_links(state)
    state.mkdir(parents=True, exist_ok=True)
    no_links(state / "LOCK")
    with (state / "LOCK").open("a+b") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Deferred("another collector is running")
        yield


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--store", type=Path, default=Path.home() / ".cache/image-prompt/photo-shared-runtime")
    parser.add_argument("--state", type=Path, default=Path.home() / ".cache/image-prompt/runtime-cleanup")
    parser.add_argument("--evidence-root", type=Path, action="append", default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--waive-runtime-observation-wait", action="store_true",
                        help="One-time exception for runtime observations only; requires an earlier unchanged observation.")
    args = parser.parse_args(argv)
    policy = Policy(args.repo.absolute(), args.store.absolute(), args.state.absolute(),
                    tuple(args.evidence_root or [Path.home() / "Documents/Codex"]))
    try:
        policy.validate()
        if args.apply:
            with collector_lock(policy.state):
                report = Collector(policy, waive_runtime_observation_wait=args.waive_runtime_observation_wait).run(apply=True)
        else:
            report = Collector(policy, waive_runtime_observation_wait=args.waive_runtime_observation_wait).run()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except Deferred as error:
        print(json.dumps({"schema": SCHEMA, "status": "deferred", "reason": str(error)}, ensure_ascii=False))
        return 0
    except (Unsafe, OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        # A failed scan never advances an unused clock or triggers a fallback.
        print(json.dumps({"schema": SCHEMA, "status": "blocked", "reason": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
