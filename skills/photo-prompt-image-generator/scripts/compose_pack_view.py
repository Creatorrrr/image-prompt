#!/usr/bin/env python3
"""Create a lossless, on-demand composition view of an immutable native v7 pack.

Only known optional candidate inventories are deferred. Every other field,
including unknown future requirements, remains visible. This is a reading aid;
the original pack remains the sole input to composition and runtime audits.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

VERSION = "photo-composer-view/v3"
OPTIONAL_PATHS = (
    ("photographic_integration", "category_candidates"),
    ("visual_proposition", "core_candidates"),
    ("visual_proposition", "tension_candidates"),
    ("photographic_craft", "dimension_candidates"),
    ("visual_concept_candidates", "candidates"),
    ("creative_augmentation", "candidates"),
    ("character_response", "advisory_retrieval", "candidates"),
    ("candidate_bundles", "candidates"),
)
SUMMARY_FIELDS = (
    "concept_terms", "applicability", "conflicts_with", "affected_dimensions",
    "slot", "axis", "source_candidate_id", "semantic_band", "hard_eligible", "semantic_consistency",
    "concept_units", "relations", "adoption", "semantic_surface_version",
    "affected_properties", "expression_scope", "contextual_status", "retrieval_evidence",
    "context_requirements", "context_prerequisites", "context_preflight",
    "scene_retrieval_support", "retrieval_status",
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def source_pack(payload: Any) -> dict[str, Any]:
    if isinstance(payload, list) and len(payload) == 1:
        payload = payload[0]
    if not isinstance(payload, dict) or payload.get("contract_version") != "photo-candidate-pack/v7":
        raise ValueError("composer view requires exactly one original v7 candidate pack")
    hashable = dict(payload, pack_id=None)
    if payload.get("pack_id") != digest(hashable)[:16]:
        raise ValueError("source pack_id does not match the immutable pack content")
    return payload


def pointer(path: tuple[str, ...]) -> str:
    return "/" + "/".join(part.replace("~", "~0").replace("/", "~1") for part in path)


def build_view(payload, candidate_ids=None, *, version=VERSION):
    if version != VERSION:raise ValueError('unsupported native composer view version')
    pack=source_pack(payload)
    import photo_native_pack
    photo_native_pack.validate(pack)
    pool=pack['candidate_pool'];binding={'source_pack_id':pack['pack_id'],'source_pack_sha256':digest(pack)}
    if candidate_ids:
        ids=list(dict.fromkeys(candidate_ids));missing=set(ids)-set(pool)
        if missing:raise ValueError('unknown native candidate IDs: '+', '.join(sorted(missing)))
        result={'contract_version':version,'mode':'candidate_details',**binding,
            'candidates':[{'id':cid,'source_pointer':pointer(('candidate_pool',cid)),'candidate':copy.deepcopy(pool[cid]),
                'role_bindings':[copy.deepcopy(row) for row in pack['candidate_bindings'].values() if row['candidate_id']==cid]} for cid in ids]}
    else:
        projection=copy.deepcopy(pack)
        projection['candidate_pool']={cid:{'deferred_candidate_id':cid,'read_details_before_selection':True} for cid in pool}
        catalog=[{'id':cid,'source_pointer':pointer(('candidate_pool',cid)),
            **{field:copy.deepcopy(row[field]) for field in ('label_en','label_ko','record_kind','applicability','affected_dimensions','adoption') if field in row},
            'role_tags':sorted({b['slot_id'] for b in pack['candidate_bindings'].values() if b['candidate_id']==cid})} for cid,row in pool.items()]
        result={'contract_version':version,'mode':'composition_overview',**binding,'required_and_active_contracts':projection,'candidate_catalog':catalog}
    result['view_sha256']=digest(result)
    return result


def verify_view(pack: Any, view: Any) -> None:
    if not isinstance(view, dict):
        raise ValueError("view must contain one JSON object")
    ids = None
    if view.get("mode") == "candidate_details":
        ids = list(dict.fromkeys(row["id"] for row in view.get("candidates", [])))
        if not ids:
            raise ValueError("candidate detail view must contain selected records")
    if view != build_view(pack, ids, version=view.get("contract_version")):
        raise ValueError("view differs from its original pack projection")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", required=True, type=Path)
    parser.add_argument("--candidate-id", action="append")
    parser.add_argument("--verify-view", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        pack = json.loads(args.pack.read_text(encoding="utf-8"))
        if args.verify_view:
            verify_view(pack, json.loads(args.verify_view.read_text(encoding="utf-8")))
            result = {"status": "pass", "source_pack_id": source_pack(pack)["pack_id"]}
        else:
            result = build_view(pack, args.candidate_id)
        serialized = json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n"
        if args.output:
            if args.output.resolve() == args.pack.resolve():
                raise ValueError("output cannot overwrite the original candidate pack")
            args.output.write_text(serialized, encoding="utf-8")
        else:
            print(serialized, end="")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"composer view: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
