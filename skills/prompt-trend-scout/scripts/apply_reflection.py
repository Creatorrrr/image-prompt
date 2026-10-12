#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import TARGET_SKILL_DIR, load_json, write_json


def selected_candidates(report: dict[str, Any], select: str) -> list[dict[str, Any]]:
    selected = {item.strip() for item in select.split(",") if item.strip()}
    if not selected:
        raise SystemExit("--select must include at least one candidate id")
    candidates = [c for c in report.get("candidates", []) if c.get("candidate_id") in selected]
    missing = selected - {c.get("candidate_id") for c in candidates}
    if missing:
        raise SystemExit(f"Unknown candidate ids: {', '.join(sorted(missing))}")
    return candidates


def dry_run_lines(candidates: list[dict[str, Any]]) -> list[str]:
    lines = ["DRY RUN - no files changed"]
    for candidate in candidates:
        proposed = candidate.get("proposed", {})
        lines.append(
            "{candidate_id}: {kind} -> {target_asset} :: {proposed}".format(
                candidate_id=candidate["candidate_id"],
                kind=candidate["kind"],
                target_asset=candidate["target_asset"],
                proposed=proposed.get("en") or proposed.get("id"),
            )
        )
    return lines


def apply_candidates(candidates: list[dict[str, Any]]) -> list[str]:
    """Apply only complete reviewed native records; shorthand leads need authorship."""
    import copy,sys,uuid
    sys.path.insert(0,str(TARGET_SKILL_DIR/'scripts'))
    import photo_candidate_corpus as c
    from photo_embedding_provider import atomic
    from photo_runtime_sources import source_update
    source=c.load(TARGET_SKILL_DIR/'assets'); manifest=load_json(TARGET_SKILL_DIR/'assets'/c.MANIFEST_NAME)
    owners={field:next(row['file'] for row in manifest['modules'] if row['kind']==field) for field in ('candidates','slot_bindings','policies')}
    changed=[];edited=copy.deepcopy(source)
    for lead in candidates:
        proposal=lead.get('proposed',{});record=proposal.get('native_record');bindings=proposal.get('native_bindings',[])
        if lead['kind']=='tag' and record:
            cid=record['id']
            if cid in edited['candidates']:
                changed.append(f"SKIP {lead['candidate_id']}: native candidate already exists");continue
            edited['candidates'][cid]=record
            for row in bindings:
                if row['id'] in edited['slot_bindings']:raise ValueError('duplicate native role binding')
                edited['slot_bindings'][row['id']]=row
            changed.append(f"ADD native candidate {cid}")
        elif lead['kind']=='facet_value':
            facet=proposal.get('facet_name');value=proposal.get('value') or proposal.get('id')
            vocabulary=edited['policies'].get('facet_vocab',{})
            if facet not in vocabulary:changed.append(f"SKIP {lead['candidate_id']}: unknown facet")
            elif value not in vocabulary[facet]:vocabulary[facet].append(value);changed.append(f"ADD facet {facet}.{value}")
        else:changed.append(f"MANUAL {lead['candidate_id']}: author a complete native record, effects, provenance and role bindings")
    c.validate(edited)
    if edited==source:return changed
    # The epoch remains pending until explicit index rebuild and publication.
    with source_update(TARGET_SKILL_DIR):
        for field,filename in owners.items():
            module=load_json(TARGET_SKILL_DIR/'assets'/filename)
            if field=='policies':module[field]=edited[field]
            else:
                for identifier in edited[field].keys()-source[field].keys():module[field][identifier]=edited[field][identifier]
            atomic(TARGET_SKILL_DIR/'assets'/filename,module)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply approved prompt trend reflection candidates.")
    parser.add_argument("--report", required=True)
    parser.add_argument("--select", required=True)
    parser.add_argument("--approved-by", required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True)
    mode.add_argument("--no-dry-run", action="store_true")
    args = parser.parse_args()

    if not args.approved_by.strip():
        raise SystemExit("--approved-by is required")
    report = load_json(Path(args.report))
    if report.get("no_changes_applied") is not True:
        raise SystemExit("Refusing to apply a report that lacks no_changes_applied=true")
    candidates = selected_candidates(report, args.select)
    if args.no_dry_run:
        for line in apply_candidates(candidates):
            print(line)
        print("Approved changes applied. Run photo-prompt-image-generator validation next.")
    else:
        for line in dry_run_lines(candidates):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
