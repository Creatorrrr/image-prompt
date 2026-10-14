"""Native role definitions and conservative owner/property fit; no source IO."""
from __future__ import annotations

FIELDS = frozenset({"id", "description", "description_ko", "dimensions", "applicability",
    "semantic_role", "owners", "property_prefixes", "evidence_terms", "includes", "excludes",
    "neighbors", "core_fields", "priority"})
CORE_FIELDS = frozenset({"subject", "setting", "event", "style", "visual_priorities"})
ROLES = frozenset({"direct", "contextual"})


def validate(tag, row, catalog_ids, strings):
    if (set(row) != FIELDS or row.get("id") != tag
            or any(not isinstance(row.get(key), str) or not row[key].strip()
                   for key in ("description", "description_ko"))
            or row["description"] == tag.replace("_", " ")
            or row.get("semantic_role") not in ROLES
            or row.get("priority") not in {"core", "support"}
            or not isinstance(row.get("applicability"), dict)):
        raise ValueError("invalid native semantic role: " + tag)
    for key in ("owners", "property_prefixes", "evidence_terms", "includes", "excludes", "neighbors", "core_fields"):
        if not strings(row[key], tag + "." + key) and key != "neighbors":
            raise ValueError("missing role boundary: " + tag + "." + key)
    if not set(row["neighbors"]) <= catalog_ids or tag in row["neighbors"]:
        raise ValueError("unknown or self role neighbor: " + tag)
    if not set(row["core_fields"]) <= CORE_FIELDS:
        raise ValueError("unknown core focus field: " + tag)


def fit(spec, record, positive_text, *, realization_id='base', source_data=None):
    """Dimensions, tags and source membership cannot establish semantic approval.

Specific effect paths name a carrier property. Text provides corroboration,
not an independent semantic certification. Wildcards remain review_required.
    """
    import photo_semantic_evidence
    reviewed = photo_semantic_evidence.qualification(spec, record, realization_id, source_data=source_data)
    return {**reviewed, 'semantic_role': spec['semantic_role'], 'owner_scope': list(spec['owners'])}
