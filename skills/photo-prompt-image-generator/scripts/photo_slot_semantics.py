"""Native role definitions and conservative owner/property fit; no source IO."""
from __future__ import annotations
import re

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


def _owned_match(path, prefix):
    return path == prefix.rstrip(".") or path.startswith(prefix if prefix.endswith(".") else prefix + ".")


def _owner_fit(owners, target):
    words = set(re.findall(r"[a-z]+", target.casefold()))
    if "actor" in owners:
        actor = {"actor", "subject", "person", "wearer", "hair", "wig", "face", "skin", "body",
                 "eye", "eyes", "lip", "lips", "head", "hand", "hands", "brow", "lashes", "torso",
                 "nail", "nails", "fingernail", "fingernails", "toenail", "toenails"}
        if words & actor:
            return "compatible"
        if words & {"image", "frame", "camera", "lens", "background", "environment", "garment", "object"}:
            return "incompatible"
        return "unknown"
    if "image" in owners:
        if words & {"image", "frame", "picture", "photograph", "scene", "view", "output", "print", "render", "sensor"}:
            return "compatible"
        return "unknown"
    if "surface" in owners and words & {"image", "camera", "frame", "picture"}:
        return "incompatible"
    return "compatible"


def fit(spec, record, positive_text):
    """Dimensions, tags and source membership cannot establish semantic approval.

Specific effect paths name a carrier property. Text provides corroboration,
not an independent semantic certification. Wildcards remain review_required.
    """
    text = positive_text.casefold()
    terms = [term for term in spec["evidence_terms"] if term.casefold() in text]
    properties = record["effects"]["properties"]
    concrete = [p for p in properties if "*" not in p["property"] and p["target"] != "*"]
    scoped = [p for p in concrete if p["dimension"] in spec["dimensions"]
               and any(_owned_match(p["property"], prefix) for prefix in spec["property_prefixes"])]
    matched = [p for p in scoped if _owner_fit(spec["owners"], p["target"]) == "compatible"]
    uncertain_owner = any(_owner_fit(spec["owners"], p["target"]) == "unknown" for p in scoped)
    if matched and terms:
        status, reason = "eligible", "owned_property_and_meaning_evidence"
    elif concrete and len(concrete) == len(properties) and not matched and not uncertain_owner and spec["semantic_role"] == "direct":
        status, reason = "incompatible", "declared_properties_belong_to_other_role"
    else:
        status, reason = "review_required", "specific_role_evidence_not_established"
    return {"status": status, "reason": reason, "semantic_role": spec["semantic_role"],
            "owner_scope": list(spec["owners"]), "matched_properties": matched, "meaning_terms": terms}
