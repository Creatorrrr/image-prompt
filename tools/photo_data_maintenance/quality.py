from __future__ import annotations

from collections import defaultdict
import re

from .common import digest, finding, normalized


def analyze(inventory: dict, initial=()) -> list:
    results = list(initial)
    groups = defaultdict(list)
    nodes = {row["id"]: row for row in inventory["nodes"]}
    for node in inventory["nodes"]:
        record = node["record"]
        kind = node["kind"]
        if kind == "bundle":
            for member in record.get("member_candidates", []):
                if member["candidate_id"] not in nodes:
                    results.append(finding("bundle_member_unresolved", "error", [node["id"]], "unknown native member"))
        fields = {key: record.get(key) for key in ("label_en", "en", "description", "positive_text")}
        if kind == "profile":
            semantics = record.get("semantics")
            fields["semantics.definition"] = semantics.get("definition") if isinstance(semantics, dict) else None
        for field, text in fields.items():
            if not isinstance(text, str) or not text.strip():
                continue
            groups[(kind, field, normalized(text))].append(node)
            if re.search(r"\b(?:TODO|TBD|FIXME)\b|<[^>]*(?:placeholder|describe|insert)[^>]*>", text, re.I):
                results.append(finding("unfinished_description", "review", [node["id"]],
                                       "description contains an explicit unresolved placeholder", field=field, text=text))
        # Empty authored descriptive units are concrete diagnostics. Short
        # phrases and mood concepts alone are not evidence of poor quality.
        for field in ("concept_units", "visual_components"):
            if field in record and (not isinstance(record[field], list) or not record[field]):
                results.append(finding("empty_descriptive_units", "review", [node["id"]],
                                       "declared descriptive units are empty or malformed", field=field))
    for (kind, field, text), members in sorted(groups.items()):
        if len(members) < 2:
            continue
        # Keep every condition, relation, scope and obligation in this comparison.
        signatures = []
        for row in members:
            meaning = {key: value for key, value in row["record"].items() if key not in {"id", "label_en", "label_ko", "en", "ko"}}
            signatures.append(digest([row["kind"], row["slot"], meaning]))
        results.append(finding("shared_description", "review", [row["id"] for row in members],
                               "shared text is a review lead; identity and equivalence are not inferred",
                               field=field, normalized_text=text, distinct_scope_signatures=len(set(signatures)),
                               sources={row["id"]: row["source_refs"] for row in members}))
    unique = {row["id"]: row for row in results}
    return sorted(unique.values(), key=lambda row: ({"error": 0, "review": 1, "info": 2}[row["severity"]], row["id"]))
