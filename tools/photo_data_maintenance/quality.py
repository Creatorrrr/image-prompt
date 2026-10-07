from __future__ import annotations

from collections import defaultdict
import re

from .common import digest, finding, normalized


def analyze(inventory: dict, initial=()) -> list:
    results = list(initial)
    groups = defaultdict(list)
    nodes = {row["id"]: row for row in inventory["nodes"]}
    by_entry = defaultdict(list)
    for row in inventory["nodes"]:
        if row["kind"] == "candidate":
            by_entry[row["record"].get("id")].append(row)
    for node in inventory["nodes"]:
        record = node["record"]
        kind = node["kind"]
        if kind == "bundle" and "member_candidates" not in record:
            members = record.get("candidate_ids") or []
            scopes = record.get("candidate_slots") or {}
            if not isinstance(members, list) or not members or any(not isinstance(member, str) for member in members):
                results.append(finding("bundle_members_invalid", "error", [node["id"]], "bundle needs a nonempty string member list"))
                members = []
            if len(set(members)) != len(members):
                results.append(finding("bundle_members_duplicate", "error", [node["id"]], "bundle has duplicate member IDs"))
            if not isinstance(scopes, dict) or set(scopes) - set(members):
                results.append(finding("bundle_scopes_invalid", "error", [node["id"]], "bundle member slot scopes are invalid"))
                scopes = {}
            for member in members:
                matches = [row for row in by_entry.get(member, []) if member not in scopes or row["slot"] == scopes[member]]
                if len(matches) != 1:
                    results.append(finding("bundle_member_unresolved", "error", [node["id"]], "member reference is missing or ambiguous",
                                           field="candidate_ids:" + member, candidate_id=member, matched_ids=[row["id"] for row in matches]))
            profiles = record.get("hard_profile_ids") or []
            if not isinstance(profiles, list) or any(not isinstance(profile, str) for profile in profiles):
                results.append(finding("bundle_profiles_invalid", "error", [node["id"]], "bundle profile references must be strings"))
                profiles = []
            if record.get("hard_profile_id"):
                profiles = [*profiles, record["hard_profile_id"]]
            for profile in profiles:
                if not isinstance(profile, str) or "profile:" + profile not in nodes:
                    results.append(finding("bundle_profile_unresolved", "error", [node["id"]], "unknown visual profile reference",
                                           field="hard_profile_ids:" + str(profile), profile_id=profile))
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
        if kind == "candidate" and record.get("canonical_concept_id"):
            seen = {node["id"]}
            current = node
            while current["record"].get("canonical_concept_id"):
                target = f"slot:{node['slot']}:{current['record']['canonical_concept_id']}"
                if target not in nodes or target in seen:
                    results.append(finding("canonical_reference_invalid", "error", [node["id"]],
                                           "canonical reference is missing or cyclic", field="canonical_concept_id", target=target))
                    break
                seen.add(target)
                current = nodes[target]
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
