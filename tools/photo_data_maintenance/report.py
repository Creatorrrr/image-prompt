from __future__ import annotations

import contextlib
import fcntl
import os
import shutil
import tempfile
from pathlib import Path

from .common import MaintenanceError, RECIPES, LOADED_TOOL_CODE, atomic, canonical, decode, digest, now, require_tool, sha
from .corpus import capture_generation, current_generation
from .links import build_links
from .quality import analyze
from .reviews import review_states


@contextlib.contextmanager
def lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def pointer_directory(store: Path, source_root: str) -> Path:
    return store / "namespaces" / digest({"source_root": str(Path(source_root).resolve())})


def read_pointer(directory: Path):
    path = directory / "CURRENT.json"
    return decode(path.read_bytes()) if path.is_file() else None


def write_report(captured: dict, output: Path, reviews=()) -> dict:
    require_tool()
    output = output.resolve()
    if output.exists():
        raise MaintenanceError("output_exists", "use a new report output directory")
    inventory = captured["inventory"]
    findings = analyze(inventory, captured["findings"])
    errors = sum(row["severity"] == "error" for row in findings)
    generation = captured["binding"]["input_mode"] == "generation"
    if generation and errors:
        raise MaintenanceError("source_invalid", "validated input has structural diagnostic errors")
    links = build_links(inventory) if generation else None
    decisions = review_states(list(reviews), inventory, findings, links)
    for row in findings:
        row["review"] = decisions.get(row["id"], {"status": "unreviewed"})
    bodies = {"inventory.json": canonical(inventory), "findings.json": canonical({"schema": "photo-data-findings/v1", "findings": findings}),
              "reviews.json": canonical({"records": list(reviews), "states": decisions})}
    if links is not None:
        bodies["links.json"] = canonical(links)
    counts = {severity: sum(row["severity"] == severity for row in findings) for severity in ("error", "review", "info")}
    summary = ("# 후보·시각 의미 관리 보고서\n\n"
               f"입력: {captured['binding']['input_mode']} · 세대: {captured['binding'].get('generation_id') or 'draft'}\n\n"
               f"항목: {inventory['counts']}\n\n오류: {counts['error']} · 검토 의심: {counts['review']} · 정보: {counts['info']}\n\n"
               f"명시적 edge: {len(links['edges']) if links else '정상 조회 미게시'} · 미연결 항목: {len(links['unlinked']) if links else 'draft'}\n\n"
               "같은 문장은 중복 검토의 단서이며 의미 동등성이나 제거 필요성을 확정하지 않습니다. "
               "번들 경유 연결은 의미 전체 충족이나 필수 활성화를 뜻하지 않습니다. "
               "자동 점검은 전체 의미 검토·검색 노출·이미지 품질 검증이 아닙니다.\n")
    bodies["SUMMARY.md"] = summary.encode()
    for name, raw in captured["source_files"].items():
        if raw is not None:
            bodies["inputs/" + name] = raw
    manifest = {"schema": "photo-data-report/v1", "binding": captured["binding"], "recipes": RECIPES,
                "tool_code": LOADED_TOOL_CODE, "created_at": now(), "findings_count": counts,
                "validation_status": "generation_validated" if generation else "invalid" if errors else "incomplete" if captured["binding"].get("editing_pending") else "structurally_checked",
                "files": {name: sha(raw) for name, raw in sorted(bodies.items())}}
    manifest["report_id"] = digest(manifest)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".report-", dir=output.parent) as temporary:
        staging = Path(temporary)
        for name, raw in bodies.items():
            atomic(staging / name, raw)
        atomic(staging / "manifest.json", canonical(manifest))
        load_report(staging)
        # Do not replace a report created by another worker.
        if output.exists():
            raise MaintenanceError("output_exists", "report destination was concurrently created")
        os.rename(staging, output)
    return manifest


def _member(directory: Path, name: str) -> Path:
    parts = name.split("/")
    if not name or any(part in {"", ".", ".."} for part in parts) or "\\" in name or ":" in name:
        raise MaintenanceError("report_invalid", "unsafe report member")
    path = directory
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise MaintenanceError("report_invalid", "symlink report member")
    return path


def load_report(directory: Path, *, require_links=False) -> dict:
    require_tool()
    manifest_path = _member(directory, "manifest.json")
    raw = manifest_path.read_bytes()
    manifest = decode(raw)
    body = {key: value for key, value in manifest.items() if key != "report_id"}
    if (manifest.get("schema") != "photo-data-report/v1" or manifest.get("report_id") != digest(body)
            or manifest.get("recipes") != RECIPES or manifest.get("tool_code") != LOADED_TOOL_CODE):
        raise MaintenanceError("report_invalid", "manifest/recipe/implementation checksum mismatch")
    files = {}
    for name, expected in manifest["files"].items():
        member = _member(directory, name).read_bytes()
        if sha(member) != expected:
            raise MaintenanceError("report_invalid", f"report member checksum mismatch: {name}")
        files[name] = member
    inventory = decode(files["inventory.json"])
    for node in inventory["nodes"]:
        if node["entity_sha256"] != digest([node["kind"], node["slot"], node["record"]]):
            raise MaintenanceError("report_invalid", "entity content checksum mismatch")
    if len({node["id"] for node in inventory["nodes"]}) != len(inventory["nodes"]):
        raise MaintenanceError("report_invalid", "duplicate report entity")
    links = decode(files["links.json"]) if "links.json" in files else None
    if links is not None and (manifest["binding"]["input_mode"] != "generation"
                              or manifest["validation_status"] != "generation_validated"
                              or links != build_links(inventory)):
        raise MaintenanceError("report_invalid", "graph is not the projection of validated bundle references")
    if require_links and links is None:
        raise MaintenanceError("draft_not_queryable", "draft diagnostics cannot serve normal relationship queries")
    findings = decode(files["findings.json"])["findings"]
    reviews = decode(files["reviews.json"])
    if reviews["states"] != review_states(reviews["records"], inventory, findings, links):
        raise MaintenanceError("report_invalid", "review binding mismatch")
    if manifest_path.read_bytes() != raw:
        raise MaintenanceError("report_changed", "report manifest changed during read")
    return {"manifest": manifest, "inventory": inventory, "findings": findings, "links": links, "reviews": reviews["states"]}


def require_current(report: dict, root: Path, runtime_store: Path) -> None:
    binding = report["manifest"]["binding"]
    if binding["input_mode"] != "generation" or binding["source_root"] != str(root.resolve()):
        raise MaintenanceError("report_not_current", "report authority/root differs from requested source")
    snapshot = current_generation(root, runtime_store)
    if (snapshot.generation_id != binding["generation_id"]
            or snapshot.manifest["source_fingerprint"] != binding["source_fingerprint"]):
        raise MaintenanceError("report_not_current", "report does not match current verified source")
    # Independently reproject the immutable source. Self-consistent rewritten
    # report checksums must not make altered records authoritative.
    captured = capture_generation(root, runtime_store, snapshot.generation_id)
    if captured["inventory"] != report["inventory"]:
        raise MaintenanceError("report_invalid", "report inventory differs from verified generation")


def current_report(store: Path, root: Path) -> Path:
    import re
    pointer = read_pointer(pointer_directory(store, str(root)))
    if (not isinstance(pointer, dict) or pointer.get("schema") != "photo-data-current/v1"
            or pointer.get("source_root") != str(root.resolve())
            or not re.fullmatch(r"[0-9a-f]{64}", pointer.get("report_id", ""))
            or pointer.get("recipe_sha256") != digest([RECIPES, LOADED_TOOL_CODE])):
        raise MaintenanceError("report_not_current", "missing or invalid management CURRENT binding")
    directory = store / "reports" / pointer["report_id"]
    report = load_report(directory, require_links=True)
    manifest = report["manifest"]
    if (manifest["report_id"] != pointer["report_id"]
            or pointer.get("report_manifest_sha256") != sha((directory / "manifest.json").read_bytes())
            or pointer.get("generation_id") != manifest["binding"]["generation_id"]
            or pointer.get("source_fingerprint") != manifest["binding"]["source_fingerprint"]):
        raise MaintenanceError("report_not_current", "management CURRENT differs from report bindings")
    return directory


def activate(report_directory: Path, store: Path, root: Path, runtime_store: Path, expected_pointer) -> dict:
    report = load_report(report_directory, require_links=True)
    directory = pointer_directory(store, str(root))
    with lock(directory / "LOCK"):
        if read_pointer(directory) != expected_pointer:
            raise MaintenanceError("publication_superseded", "another report publisher completed first")
        require_current(report, root, runtime_store)
        manifest = report["manifest"]
        destination = store / "reports" / manifest["report_id"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            staging = Path(tempfile.mkdtemp(prefix=".publication-", dir=destination.parent))
            try:
                shutil.copytree(report_directory, staging, dirs_exist_ok=True)
                load_report(staging, require_links=True)
                os.rename(staging, destination)
            finally:
                if staging.exists():
                    shutil.rmtree(staging)
        else:
            load_report(destination, require_links=True)
        # Recheck current source after staging before the atomic pointer write.
        require_current(report, root, runtime_store)
        pointer = {"schema": "photo-data-current/v1", "report_id": manifest["report_id"],
                   "generation_id": manifest["binding"]["generation_id"],
                   "source_root": str(root.resolve()), "source_fingerprint": manifest["binding"]["source_fingerprint"],
                   "report_manifest_sha256": sha((destination / "manifest.json").read_bytes()),
                   "recipe_sha256": digest([RECIPES, LOADED_TOOL_CODE])}
        atomic(directory / "CURRENT.json", canonical(pointer))
        return pointer


def difference(before: dict, after: dict) -> dict:
    old = {node["id"]: node for node in before["inventory"]["nodes"]}
    new = {node["id"]: node for node in after["inventory"]["nodes"]}
    return {"added": sorted(new.keys() - old.keys()), "removed": sorted(old.keys() - new.keys()),
            "meaning_changed": sorted(key for key in old.keys() & new.keys() if old[key]["entity_sha256"] != new[key]["entity_sha256"]),
            "source_moved": sorted(key for key in old.keys() & new.keys() if old[key]["source_refs"] != new[key]["source_refs"]),
            "stale_reviews": sorted(key for key, row in after["reviews"].items() if row["status"] == "stale")}
