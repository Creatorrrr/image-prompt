"""Post-core source registration shared by loaders and maintenance checks.

Importing this module never reads assets. The ordered manifest is the only
authored extension inventory; filename views and required-file lists are derived.
"""
from __future__ import annotations

import json
import re
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path


CONTRACT_VERSION = "photo-source-manifest/v1"
DEFAULT_MANIFEST = Path(__file__).resolve().parents[1] / "assets/photo_prompt_source_manifest.json"
KINDS = {"candidate", "visual_profile"}


@dataclass(frozen=True)
class SourceInventory:
    """One registration snapshot, explicitly bound to one assets directory."""
    assets: Path
    rows: tuple[tuple[str, str, bool, int], ...]
    synthetic: bool = False
    test_candidate_files: tuple[str, ...] | None = None

    @classmethod
    def load(cls, assets: Path) -> SourceInventory:
        assets = Path(assets).resolve()
        payload = load_source_manifest(assets / DEFAULT_MANIFEST.name)
        return cls(assets, tuple((row["file"], row["kind"], row["required"], row["load_order"])
                                 for row in payload["sources"]))

    @classmethod
    def for_test(cls, assets: Path, *, candidate_files=None) -> SourceInventory:
        """Explicit synthetic/historical scope, never a publication inventory.

        A historical overlay test can select candidates from its own manifest
        while preserving that manifest's required-source policy projection.
        """
        assets = Path(assets).resolve()
        if candidate_files is None:
            return cls(assets, (), synthetic=True)
        inventory = cls.load(assets)
        selected = tuple(candidate_files)
        registered = inventory.files("candidate")
        if (len(set(selected)) != len(selected) or set(selected) - set(registered)
                or selected != tuple(name for name in registered if name in selected)):
            raise ValueError("test candidate selection must preserve its own manifest order")
        return cls(assets, inventory.rows, synthetic=True, test_candidate_files=selected)

    def files(self, kind: str) -> tuple[str, ...]:
        if kind not in KINDS:
            raise ValueError(f"unknown source kind: {kind}")
        if kind == "candidate" and self.synthetic and self.test_candidate_files is not None:
            return self.test_candidate_files
        return tuple(row[0] for row in sorted(self.rows, key=lambda row: row[3]) if row[1] == kind)

    def required(self, kind: str) -> list[str]:
        if kind not in KINDS:
            raise ValueError(f"unknown source kind: {kind}")
        return [row[0] for row in self.rows if row[1] == kind and row[2]]

    def check_root(self, path: Path) -> None:
        if Path(path).parent.resolve() != self.assets:
            raise ValueError("source inventory belongs to a different assets directory")

    def validate(self) -> None:
        registered = {row[0] for row in self.rows}
        missing = [row[0] for row in self.rows if row[2] and not (self.assets / row[0]).is_file()]
        discovered = {p.name for pattern in ("photo_prompt_*_extension.json", "photo_prompt_visual_obligations_*.json")
                      for p in self.assets.glob(pattern) if p.is_file()}
        if missing:
            raise ValueError(f"required photo sources are missing: {missing}")
        if discovered - registered:
            raise ValueError(f"unregistered photo sources: {sorted(discovered - registered)}")


def load_source_manifest(path: Path = DEFAULT_MANIFEST) -> dict:
    def unique_object(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate source manifest key: {key}")
            value[key] = item
        return value

    payload = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if (not isinstance(payload, dict) or set(payload) != {"contract_version", "sources"}
            or payload["contract_version"] != CONTRACT_VERSION
            or not isinstance(payload["sources"], list) or not payload["sources"]):
        raise ValueError("source manifest requires its contract version and non-empty sources")
    names = set()
    orders = {kind: set() for kind in KINDS}
    for row in payload["sources"]:
        if not isinstance(row, dict) or set(row) != {"file", "kind", "required", "load_order"}:
            raise ValueError("source registration requires file, kind, required and load_order")
        name, kind, order = row["file"], row["kind"], row["load_order"]
        if not isinstance(name, str) or not re.fullmatch(r"photo_prompt_[a-z0-9_]+\.json", name):
            raise ValueError("source files must be photo_prompt JSON basenames")
        if (not isinstance(kind, str) or kind not in KINDS
                or type(row["required"]) is not bool or type(order) is not int or order < 0):
            raise ValueError("invalid source kind, required flag or load_order")
        if kind == "candidate" and not name.endswith("_extension.json"):
            raise ValueError("candidate sources must be extension files")
        if kind == "visual_profile" and not name.startswith("photo_prompt_visual_obligations_"):
            raise ValueError("visual-profile sources must be obligation extension files")
        if name in names or order in orders[kind]:
            raise ValueError("duplicate source file or load_order")
        names.add(name)
        orders[kind].add(order)
    if any(values != set(range(len(values))) for values in orders.values()):
        raise ValueError("source load_order must be contiguous within each kind")
    return payload


def extension_files(kind: str, path: Path = DEFAULT_MANIFEST) -> tuple[str, ...]:
    if kind not in KINDS:
        raise ValueError(f"unknown source kind: {kind}")
    rows = [row for row in load_source_manifest(path)["sources"] if row["kind"] == kind]
    return tuple(row["file"] for row in sorted(rows, key=lambda row: row["load_order"]))


def required_files(kind: str, path: Path = DEFAULT_MANIFEST) -> list[str]:
    if kind not in KINDS:
        raise ValueError(f"unknown source kind: {kind}")
    # Manifest order preserves the published policy projection independently of
    # extension overlay order. Neither list is authored a second time.
    return [row["file"] for row in load_source_manifest(path)["sources"]
            if row["kind"] == kind and row["required"]]


class SourceFiles(Sequence[str]):
    """A filename view resolved only when post-core code accesses it."""
    def __init__(self, kind: str):
        self.kind = kind

    def __iter__(self) -> Iterator[str]:
        return iter(extension_files(self.kind))

    def __len__(self) -> int:
        return len(extension_files(self.kind))

    def __getitem__(self, index):
        return extension_files(self.kind)[index]


def validate_source_files(assets: Path, errors: list[str], path: Path | None = None) -> None:
    """Report missing registrations and required files without adopting new data."""
    try:
        manifest = load_source_manifest(path or Path(assets) / DEFAULT_MANIFEST.name)
    except (OSError, ValueError) as exc:
        errors.append(f"source manifest: {exc}")
        return
    registered = {row["file"] for row in manifest["sources"]}
    for row in manifest["sources"]:
        if row["required"] and not (assets / row["file"]).is_file():
            errors.append(f"required {row['kind']} source is missing: {row['file']}")
    discovered = {p.name for pattern in ("photo_prompt_*_extension.json", "photo_prompt_visual_obligations_*.json")
                  for p in assets.glob(pattern) if p.is_file()}
    for name in sorted(discovered - registered):
        errors.append(f"unregistered photo source: {name}")
