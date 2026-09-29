#!/usr/bin/env python3
"""Resolve a small, candidate-free artistic brief before baseline authoring.

Only this module, its adjacent definitions, and caller-supplied request/control
inputs are read. No dictionaries, presets, previous renders or network access.
The embedded definition makes archived snapshots independent of later defaults.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import secrets

VERSION = "photo-creative-controls/v4"
DEFINITION_VERSION = "photo-creative-control-definitions/v4"
DEFAULT_PATH = Path(__file__).with_name("creative_controls.json")
AXES = ("sensual", "fetish")
INTENSITY_CONTROLS = (*AXES, "surreal")
LEVEL_CONTROLS = (*INTENSITY_CONTROLS, "creativity")
CONTROL_NAMES = {*LEVEL_CONTROLS, "adult_appeal_emphasis", "viewer_experience",
                 "reference_edit_mode", "trend_layer"}

# Deliberately narrow syntax: only explicit name=value/name:value assignments
# are configuration. Natural-language or mixed visual instructions stay visual.
ASSIGNMENT = re.compile(
    r"(?<![\w])`?(?P<name>" + "|".join(sorted(CONTROL_NAMES))
    + r")`?\s*[:=]\s*`?(?P<value>[A-Za-z0-9_.+\-]+)`?(?![\w])"
)
QUOTED_TEXT = re.compile(
    r'"(?:\\.|[^"\\])*"'
    r"|(?<!\w)'(?:\\.|[^'\\])*'"
)


def configuration_assignments(text):
    """Quoted image text is content, not a configuration instruction."""
    quoted = [(match.start(), match.end()) for match in QUOTED_TEXT.finditer(text)]
    return [match for match in ASSIGNMENT.finditer(text)
            if not any(start <= match.start() < end for start, end in quoted)]


def strip_assignments(text):
    for match in reversed(configuration_assignments(text)):
        text = text[:match.start()] + " " + text[match.end():]
    return text


def split_request_spans(envelope, snapshot=None):
    """Return visual fragments and verified assignments, leaving raw text intact.

    Only a byte-bound snapshot with matching explicit overrides covers controls.
    Fragments on either side of assignments each retain their coverage duty.
    No span ID or caller-authored label grants an exemption.
    """
    visual, assignments = [], []

    def add_fragment(span, start, end, index):
        separators = " \t\r\n,;:|()[]`"
        raw = span["text"][start:end]
        left = len(raw) - len(raw.lstrip(separators))
        fragment = raw.strip(separators)
        if re.search(r"[^\W_]", fragment):
            offset = span["start"] + start + left
            visual.append({**span, "span_id": f"{span['span_id']}:visual{index}",
                           "source_span_id": span["span_id"], "start": offset,
                           "end": offset + len(fragment), "text": fragment})

    for span in envelope.get("active_spans", []):
        text = span["text"]
        matches = configuration_assignments(text)
        if not matches:
            visual.append(dict(span))
            continue
        if not assignments:
            validate(snapshot, envelope.get("request_text"))
        cursor = 0
        for index, match in enumerate(matches):
            name, raw = match.group("name", "value")
            kind = snapshot["definitions"]["controls"][name]["type"]
            try:
                value = raw if kind == "enum" else json.loads(raw)
            except (ValueError, TypeError) as exc:
                raise ValueError(f"invalid explicit control assignment: {match.group()}") from exc
            check_value(name, value, snapshot["definitions"]["controls"][name])
            resolved = snapshot["controls"][name]
            if resolved["source"] != "request_override" or resolved["value"] != value:
                raise ValueError(f"explicit {name} assignment differs from the frozen override")
            assignments.append({"span_id": span["span_id"], "name": name, "value": value,
                                "start": span["start"] + match.start(),
                                "end": span["start"] + match.end(), "text": match.group()})
            add_fragment(span, cursor, match.start(), index)
            cursor = match.end()
        add_fragment(span, cursor, len(text), len(matches))
    return visual, assignments


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def check_value(name, value, definition):
    kind = definition["type"]
    if kind == "integer" and type(value) is not int:
        raise ValueError(f"{name} must be an integer")
    if kind == "number" and (type(value) not in (int, float) or not math.isfinite(value)):
        raise ValueError(f"{name} must be a finite number")
    if kind == "boolean" and type(value) is not bool:
        raise ValueError(f"{name} must be boolean")
    if kind == "enum" and value not in definition["choices"]:
        raise ValueError(f"{name} must be one of {definition['choices']}")
    if "range" in definition and not definition["range"][0] <= value <= definition["range"][1]:
        raise ValueError(f"{name} must be in {definition['range']}")


def validate_definitions(spec):
    if not isinstance(spec, dict) or set(spec) != {"contract_version", "principle", "controls"}:
        raise ValueError("creative-control definitions have an invalid shape")
    if spec["contract_version"] != DEFINITION_VERSION or not isinstance(spec["principle"], str):
        raise ValueError("unsupported creative-control definitions")
    if not isinstance(spec["controls"], dict) or set(spec["controls"]) != CONTROL_NAMES:
        raise ValueError("creative-control definitions must contain exactly the supported controls")
    for name, definition in spec["controls"].items():
        if not isinstance(definition, dict) or set(definition) - {"type", "range", "choices", "default", "definition", "levels", "choice_descriptions"}:
            raise ValueError(f"unsupported creative-control definition: {name}")
        if definition.get("type") not in {"integer", "number", "boolean", "enum"}:
            raise ValueError(f"invalid creative-control type: {name}")
        if not isinstance(definition.get("definition"), str) or not definition["definition"].strip():
            raise ValueError(f"missing creative-control meaning: {name}")
        if definition["type"] in {"integer", "number"}:
            bounds = definition.get("range")
            if not isinstance(bounds, list) or len(bounds) != 2 or bounds[0] > bounds[1]:
                raise ValueError(f"invalid creative-control range: {name}")
        if name in LEVEL_CONTROLS:
            levels = definition.get("levels", {})
            if (definition["type"] != "integer" or definition.get("range") != [0, 3]
                    or not isinstance(levels, dict) or set(levels) != {"0", "1", "2", "3"}
                    or any(not isinstance(text, str) or not text.strip() for text in levels.values())):
                raise ValueError(f"{name} requires all four level descriptions")
        if name == "adult_appeal_emphasis":
            descriptions = definition.get("choice_descriptions", {})
            if (not isinstance(descriptions, dict)
                    or set(descriptions) != set(definition.get("choices", []))
                    or any(not isinstance(text, str) or not text.strip() for text in descriptions.values())):
                raise ValueError("adult_appeal_emphasis requires a description for every choice")
        check_value(name, definition.get("default"), definition)
    return spec


def load_definitions(path=DEFAULT_PATH):
    return validate_definitions(json.loads(Path(path).read_text(encoding="utf-8")))


def resolve(request_text, *, overrides=None, context=None, seed=None, definitions=None):
    spec = copy.deepcopy(validate_definitions(definitions) if definitions is not None else load_definitions())
    overrides = copy.deepcopy(overrides if overrides is not None else {})
    context = copy.deepcopy(context if context is not None else {})
    if not isinstance(request_text, str) or not request_text:
        raise ValueError("creative controls require the byte-exact request text")
    if not isinstance(overrides, dict) or set(overrides) - CONTROL_NAMES:
        raise ValueError("unsupported creative-control override")
    if not isinstance(context, dict) or set(context) - {"subject_category", "no_people", "explicit_nonsexual"}:
        raise ValueError("context permits only request-resolved subject_category, no_people and explicit_nonsexual")
    category = context.get("subject_category", "unspecified")
    if category not in {"human", "nonhuman", "unspecified"}:
        raise ValueError("subject_category must be human, nonhuman or unspecified")
    for name in ("no_people", "explicit_nonsexual"):
        if name in context and type(context[name]) is not bool:
            raise ValueError(f"{name} must be boolean")
    context = {"subject_category": category, "no_people": context.get("no_people", False),
               "explicit_nonsexual": context.get("explicit_nonsexual", False)}
    if seed is None:
        seed = secrets.randbits(63)
    if type(seed) is not int:
        raise ValueError("creative-control seed must be an integer")
    controls = {}
    for name, definition in spec["controls"].items():
        value = overrides.get(name, definition["default"])
        check_value(name, value, definition)
        controls[name] = {"value": value, "source": "request_override" if name in overrides else "saved_setting"}
    values = {name: row["value"] for name, row in controls.items()}
    eligibility = {}
    for axis in AXES:
        reason = "eligible"
        if context["no_people"]:
            reason = "explicit_no_people"
        elif context["explicit_nonsexual"]:
            reason = "explicit_nonsexual_request"
        elif axis not in overrides and category != "human":
            reason = "default_requires_eligible_human_subject"
        effective = values[axis] if reason == "eligible" else 0
        eligibility[axis] = {"requested_intensity": values[axis], "effective_intensity": effective, "reason": reason}
    sensual, fetish = (eligibility[axis]["effective_intensity"] for axis in AXES)
    requested_emphasis = values["adult_appeal_emphasis"]
    emphasis = "balanced" if sensual == fetish else ("sensual_led" if sensual > fetish else "fetish_led")
    if requested_emphasis != "auto" and (sensual or fetish):
        if ((requested_emphasis == "sensual_led" and not sensual)
                or (requested_emphasis == "fetish_led" and not fetish)
                or (requested_emphasis == "balanced" and not (sensual and fetish))):
            raise ValueError("adult_appeal_emphasis conflicts with the active axes")
        emphasis = requested_emphasis
    if not (sensual or fetish):
        emphasis_reason = "Both effective intensities are zero; no added emphasis is active."
    elif requested_emphasis != "auto":
        emphasis_reason = "The selected emphasis leads without changing either effective intensity."
    elif sensual == fetish:
        emphasis_reason = f"Both effective intensities are {sensual}; the active axes share leadership."
    else:
        emphasis_reason = f"Effective sensual={sensual}, fetish={fetish}; the higher intensity leads."
    result = {"contract_version": VERSION, "provenance": "resolved_precore",
              "source_request_sha256": hashlib.sha256(request_text.encode()).hexdigest(),
              "definitions": spec, "definitions_sha256": digest(spec),
              "overrides": overrides, "context": context, "seed": seed,
              "controls": controls, "adult_appeal": eligibility,
              "resolved_emphasis": emphasis,
              "emphasis_resolution": {"active": bool(sensual or fetish), "reason": emphasis_reason}}
    result["authoring_brief"] = authoring_brief(result)
    result["canonical_sha256"] = digest(result)
    return result


def validate(snapshot, request_text):
    if not isinstance(snapshot, dict):
        raise ValueError("creative-control snapshot must be an object")
    expected = resolve(request_text, overrides=snapshot.get("overrides"), context=snapshot.get("context"),
                       seed=snapshot.get("seed"), definitions=snapshot.get("definitions"))
    if snapshot != expected:
        raise ValueError("creative-control snapshot is stale, malformed or differs from its frozen inputs")
    return snapshot


def runtime_values(snapshot):
    values = {name: row["value"] for name, row in snapshot["controls"].items()}
    for axis in AXES:
        values[axis + "_intensity"] = snapshot["adult_appeal"][axis]["effective_intensity"]
    values["adult_appeal_emphasis"] = snapshot["resolved_emphasis"]
    return values


def authoring_brief(snapshot):
    """Small writer-facing view of resolved inputs, without candidate examples."""
    definitions = snapshot["definitions"]["controls"]
    lines = []
    for name in LEVEL_CONTROLS:
        value = (snapshot["adult_appeal"][name]["effective_intensity"]
                 if name in AXES else snapshot["controls"][name]["value"])
        bounds = definitions[name]["range"]
        lines.extend([f"{name}: {value} (range: {bounds[0]}–{bounds[1]})",
                      "Meaning: " + definitions[name]["definition"],
                      "Level: " + definitions[name]["levels"][str(value)], ""])
    name = "adult_appeal_emphasis"
    definition = definitions[name]
    selected = snapshot["controls"][name]["value"]
    resolution = snapshot["emphasis_resolution"]
    resolved = snapshot["resolved_emphasis"]
    lines.extend([f"{name}: {selected} (choices: {', '.join(definition['choices'])})",
                  "Meaning: " + definition["definition"],
                  "Selected: " + definition["choice_descriptions"][selected],
                  "Effective: " + (resolved if resolution["active"] else "inactive"),
                  "Resolution: " + resolution["reason"]])
    if resolution["active"]:
        lines.append("Effective meaning: " + definition["choice_descriptions"][resolved])
    lines.extend(["", "Choose a coherent expression suited to this particular scene.",
                  "Sensual and fetish may share the same expressive choice.",
                  "Expression levels describe prominence; creativity describes interpretive freedom. Neither requires a garment or detail count.",
                  "", "Other resolved controls:"])
    for name, row in snapshot["controls"].items():
        if name not in (*LEVEL_CONTROLS, "adult_appeal_emphasis"):
            value = row["value"]
            lines.append(f"{name}: {json.dumps(value, ensure_ascii=False)}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request-envelope-json", required=True)
    parser.add_argument("--context-json", required=True, help="Request-resolved category and explicit exclusions; no reference-based inference.")
    parser.add_argument("--overrides-json", help="Only controls explicitly selected for this request; omit to use saved settings.")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    read = lambda path: json.loads(Path(path).read_text(encoding="utf-8"))
    envelope = read(args.request_envelope_json)
    if envelope.get("contract_version") != "photo-request-envelope/v1" or envelope.get("provenance") != "requesting_user":
        raise ValueError("use the actual requesting-user envelope")
    request = envelope.get("request_text")
    if not isinstance(request, str) or envelope.get("request_sha256") != hashlib.sha256(request.encode()).hexdigest():
        raise ValueError("request envelope text/hash mismatch")
    snapshot = resolve(request, overrides=read(args.overrides_json) if args.overrides_json else {},
                       context=read(args.context_json), seed=args.seed)
    split_request_spans(envelope, snapshot)
    Path(args.output).write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": args.output, "canonical_sha256": snapshot["canonical_sha256"],
                      "authoring_brief": snapshot["authoring_brief"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
