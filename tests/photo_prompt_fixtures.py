"""Authored, candidate-free inputs shared by current photo contract tests."""

from __future__ import annotations
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "skills/photo-prompt-image-generator/scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
import prompt_generator
import audit_composed_prompt
import audit_image_render_request

_TEST_PROMPT_BUDGET_EXTENSION = (
    "Fine-grained surface cues, coherent near-to-far depth, controlled highlights, legible "
    "shadow detail, and an intentional focal hierarchy keep the completed photographic frame "
    "specific, balanced, natural, and visually unambiguous."
)


def envelope(request_text: str, active_texts: tuple[str, ...] | None = None) -> dict:
    active_texts = active_texts or (request_text,)
    spans = []
    search_from = 0
    for index, text in enumerate(active_texts):
        start = request_text.find(text, search_from)
        if start < 0:
            raise AssertionError(f"active text is not in request: {text!r}")
        end = start + len(text)
        spans.append(
            {
                "span_id": f"scope_{index + 1}",
                "start": start,
                "end": end,
                "text": text,
            }
        )
        search_from = end
    return {
        "contract_version": "photo-request-envelope/v1",
        "provenance": "requesting_user",
        "request_id": "test-request",
        "request_text": request_text,
        "request_sha256": hashlib.sha256(request_text.encode("utf-8")).hexdigest(),
        "active_spans": spans,
    }


def core(
    source_request: str,
    *,
    interpreted_intent: str = (
        "A quiet rainlit still life centered on blue porcelain and restrained domestic calm"
    ),
    subject: str = "one blue porcelain teacup",
    setting: str = "a quiet rainlit kitchen counter",
    event: str = "steam rises while window reflections drift across the glaze",
    visual_priorities: tuple[str, ...] = (
        "blue porcelain glaze",
        "rainlit window reflections",
        "delicate rising steam",
    ),
    baseline_prompt_en: str = (
        "A blue porcelain teacup rests on a dark kitchen counter while delicate rising "
        "steam catches rainlit window reflections, with a quiet domestic mood, restrained "
        "slate colors, shallow focus, and tactile glaze detail."
    ),
    definitions: tuple[dict, ...] = (),
    interpretations: tuple[dict, ...] | None = None,
    exclusions: tuple[str, ...] = (),
    runtime_forbidden_labels: tuple[str, ...] = (),
    locked_dimensions: tuple[str, ...] = ("concept", "subject", "event"),
    open_dimensions: tuple[str, ...] = (
        "framing",
        "composition",
        "lighting",
        "camera",
        "color",
        "material",
        "atmosphere",
        "relationship",
    ),
    anchor_evidence: tuple[str, ...] | None = None,
) -> dict:
    if len(prompt_generator.authorial_request_content_words(baseline_prompt_en)) < (
        prompt_generator.AUTHORIAL_PROMPT_MIN_WORDS
    ):
        baseline_prompt_en = f"{baseline_prompt_en.rstrip()} {_TEST_PROMPT_BUDGET_EXTENSION}"
    if interpretations is None:
        interpretations = (
            {
                "term": "governing request",
                "source_text": source_request,
                "basis": "request_context",
                "resolution": interpreted_intent,
                "sources": [],
            },
        )
    if anchor_evidence is None:
        candidates = [subject, event, *visual_priorities]
        evidence_candidates = [
            phrase for phrase in candidates if phrase.casefold() in baseline_prompt_en.casefold()
        ]
        baseline_tokens = baseline_prompt_en.split()
        for start in range(0, max(len(baseline_tokens) - 3, 0), 2):
            phrase = " ".join(baseline_tokens[start : start + 4]).strip(" ,.;:!?")
            if phrase and phrase.casefold() in baseline_prompt_en.casefold():
                evidence_candidates.append(phrase)
        unique_evidence: list[str] = []
        seen_evidence: set[str] = set()
        for phrase in evidence_candidates:
            key = phrase.strip().casefold()
            if key and key not in seen_evidence:
                seen_evidence.add(key)
                unique_evidence.append(phrase)
        anchor_evidence = tuple(unique_evidence)
    evidence_rows = list(anchor_evidence)
    if len(evidence_rows) < len(locked_dimensions):
        raise AssertionError(
            "test core needs one distinct baseline evidence phrase per locked dimension"
        )
    return {
        "contract_version": "photo-authorial-core/v3",
        "provenance": "agent_prepack",
        "source_request": source_request,
        "interpreted_intent": interpreted_intent,
        "subject": subject,
        "setting": setting,
        "event": event,
        "visual_priorities": list(visual_priorities),
        "baseline_prompt_en": baseline_prompt_en,
        "user_definitions": list(definitions),
        "interpretation_provenance": list(interpretations),
        "unresolved_ambiguities": [],
        "user_exclusions": list(exclusions),
        "runtime_forbidden_labels": list(runtime_forbidden_labels),
        "intent_lock": {
            "contract_version": "photo-intent-lock/v2",
            "priority": "requesting_user",
            "semantic_anchors": [
                {
                    "anchor_id": f"anchor_{dimension}",
                    "source_text": source_request,
                    "dimension": dimension,
                    "prompt_evidence": evidence_rows[index],
                }
                for index, dimension in enumerate(locked_dimensions)
            ],
            "locked_dimensions": list(locked_dimensions),
            "open_dimensions": list(open_dimensions),
        },
        "style": {
            "domain": "general_photo",
            "family": "context-led photographic study",
            "evidence": ["restrained color hierarchy", "tactile material detail"],
        },
        "variation_key": "current-test",
        "semantic_assertions": [],
        "request_lineage": None,
    }


def review(prompt: str, provenance: str = "agent_prepack") -> dict:
    """Synthetic review binding for tests of contracts other than embodiment.

    Actual body-action review cases live in test_photo_embodiment. This helper
    does not claim physical or rendered-image qualification.
    """
    return {
        "contract_version": "photo-embodiment-review/v1",
        "provenance": provenance,
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "scope": "not_applicable",
        "summary": "Synthetic contract fixture; physical review is tested in the dedicated embodiment suite.",
        "checks": {},
    }


def candidate_source(data: dict, frozen: dict, *, seed: int = 7, controls: dict | None = None,
                     overrides: dict | None = None, context: dict | None = None,
                     visual_intent: dict | None = None) -> dict:
    """Supply complete current inputs for tests of downstream contracts."""
    import copy
    snapshot = controls
    if snapshot is None:
        values = {"sensual": 0, "fetish": 0, "creativity": 1, "surreal": 0, **(overrides or {})}
        snapshot = prompt_generator.creative_controls.resolve(
            frozen["source_request"], overrides=values, context=context or {}, seed=7)
        binding = frozen["request_binding"]
        request = prompt_generator.normalize_request_envelope({
            "contract_version": "photo-request-envelope/v1", "provenance": "requesting_user",
            "request_id": binding["request_id"], "request_text": frozen["source_request"],
            "request_sha256": binding["request_sha256"], "active_spans": binding["active_spans"],
        })
        raw = copy.deepcopy(frozen)
        for key in ("canonical_sha256", "core_id", "request_binding"):
            raw.pop(key, None)
        raw["intent_lock"] = {key: value for key,value in raw["intent_lock"].items()
                              if key in {"contract_version","priority","semantic_anchors","locked_dimensions","open_dimensions"}}
        if isinstance(raw.get("request_lineage"),dict):raw["request_lineage"].pop("canonical_sha256",None)
        raw["creative_controls_sha256"] = snapshot["canonical_sha256"]
        bound = prompt_generator.normalize_authorial_core(raw,request_envelope=request,creative_control_snapshot=snapshot)
        frozen.clear();frozen.update(bound)
    return prompt_generator.prepare_candidate_source(data,frozen,snapshot,
        review(frozen["baseline_prompt_en"]),seed=seed,visual_intent=visual_intent)


def composition_review(pack: dict, prompt: str) -> dict:
    return {
        "source_contract_sha256": pack["embodiment_preflight"]["canonical_sha256"],
        "review": review(prompt, "agent_postcomposition"),
    }


def run_current(
    core_input: dict,
    *,
    seed: int = 91,
    creativity: int = 1,
    envelope_input: dict | None = None,
    extra_args: tuple = (),
) -> dict:
    """Invoke the normal public CLI with all authored current inputs."""
    import copy
    import json
    import subprocess
    import tempfile

    raw = copy.deepcopy(core_input)
    request = envelope_input or envelope(raw["source_request"])
    snapshot = prompt_generator.creative_controls.resolve(
        raw["source_request"],
        overrides={"sensual": 0, "fetish": 0, "creativity": creativity, "surreal": 0},
        seed=7,
    )
    raw["creative_controls_sha256"] = snapshot["canonical_sha256"]
    with tempfile.TemporaryDirectory() as tmp:
        paths = {}
        for name, value in {
            "core": raw,
            "envelope": request,
            "controls": snapshot,
            "review": review(raw["baseline_prompt_en"]),
        }.items():
            path = Path(tmp) / (name + ".json")
            path.write_text(json.dumps(value, ensure_ascii=False))
            paths[name] = str(path)
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "generate_photo_prompt.py"),
                "--seed",
                str(seed),
                "--authorial-core-json",
                paths["core"],
                "--request-envelope-json",
                paths["envelope"],
                "--creative-controls-json",
                paths["controls"],
                "--embodiment-review-json",
                paths["review"],
                *extra_args,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode:
            raise AssertionError(result.stderr)
        return json.loads(result.stdout)[0]


def historical_freeze(evidence: Path) -> dict:
    """Validate archived evidence bytes without executing its retired runtime."""
    import json
    raw = (evidence / "frozen-inventory-queries.json").read_bytes()
    expected = (evidence / "frozen-sha256.txt").read_text().split()[0]
    assert hashlib.sha256(raw).hexdigest() == expected, "historical freeze changed"
    frozen = json.loads(raw)
    for name, digest in frozen["artifact_sha256"].items():
        original = evidence / name
        preserved = evidence / "preparation-revisions/pre-maintenance-binding" / name
        candidates = [original, preserved]
        assert any(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == digest
                   for p in candidates), "historical artifact changed: " + name
    return frozen


def historical_states(evidence: Path, frozen: dict) -> dict:
    """Read the frozen source delta; source hashes belong to that prior run."""
    import copy
    import gzip
    import json
    baseline = json.loads(gzip.decompress((evidence / "baseline-merged-data.json.gz").read_bytes()))
    states = {label: copy.deepcopy(baseline) for label in frozen["state_dictionary_hashes"]}
    for item in frozen["inventory"]:
        for label, data in states.items():
            rows = data["slots"][item["slot"]]
            position = next(i for i, row in enumerate(rows) if row["id"] == item["id"])
            assert rows[position] == item["before"]
            rows[position] = copy.deepcopy(item["before"] if label == "baseline"
                                          else item.get(label, item.get("proposal", item["before"])))
    return states


def bundle_meanings(bundles: list, *, within: list | None = None) -> list:
    """Compare authored meanings, optionally projecting a historical ID inventory.

    Projection keeps order and missing entries remain visible in the comparison;
    later optional bundles do not rewrite a frozen historical inventory.
    """
    if within is not None:
        historical_ids = {row['id'] for row in within}
        bundles = [row for row in bundles if row['id'] in historical_ids]
    return [{key: value for key, value in row.items() if key != "source_sha256"}
            for row in bundles]


def seduction_scope_delta() -> dict:
    """Read the sealed metadata delta; historical expected rows stay untouched."""
    import json
    path = ROOT / 'tests/fixtures/photo_prompt/seduction_expression_scope_delta.json'
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == 'd8fba33b9a40ac6bf190fb785fb001ab70582a0112f67ca4394f7301f25250a4'
    return json.loads(raw)


def seduction_historical_source_scope(data: dict) -> dict:
    """Reverse only ten exact metadata edits for an older source comparison."""
    import copy
    result = copy.deepcopy(data)
    for change in seduction_scope_delta()['metadata_rows']:
        row = next((r for r in result['slots'].get(change['slot'], [])
                    if r['id'] == change['id']), None)
        if row is None:
            continue  # The historical loader may exclude the owning extension.
        for field in change['changed_fields']:
            assert row.get(field) == change['after'].get(field), (change['id'], field)
            if field in change['before']:
                row[field] = copy.deepcopy(change['before'][field])
            else:
                row.pop(field, None)
    return result


def seduction_historical_bundles(bundles: list) -> list:
    """Reverse exact scoped member metadata, preserving every bundle duty."""
    import copy
    import json
    import photo_candidate_semantics as semantics
    policy = json.loads((ROOT / 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json').read_text())['candidate_semantic_policy']
    changes = {(row['slot'], row['id']): row for row in seduction_scope_delta()['metadata_rows']}
    result = copy.deepcopy(bundles)
    for bundle in result:
        for member in bundle['member_candidates']:
            change = changes.get((member['slot'], member['entry_id']))
            if change is None:
                continue
            before = semantics.semantic_source(change['before'], member['slot'], policy)
            after = semantics.semantic_source(change['after'], member['slot'], policy)
            actual = {key: value for key, value in member.items() if key not in {'id', 'slot', 'entry_id'}}
            assert actual in (before, after), f'Unsealed bundle member change: {member["id"]}'
            for field in set(before) | set(after):
                if field in before:
                    member[field] = copy.deepcopy(before[field])
                else:
                    member.pop(field, None)
    return result


def project_slot_candidate(data: dict, slot: str, entry: dict) -> tuple[dict, dict]:
    """Exercise current public projection and lossless detail, without retrieval."""
    import copy
    import compose_pack_view as views
    import photo_candidate_semantics as semantics
    variant = dict(data, slots=dict(data["slots"]))
    variant["slots"][slot] = [entry if row["id"] == entry["id"] else row
                              for row in data["slots"][slot]]
    candidate, _ = prompt_generator.candidate_pack_summarize_slot_candidate(
        variant, slot, {"id": entry["id"], "applicability_status": "eligible"})
    projected = {"contract_version": "photo-candidate-pack/v6",
                 "slots": {slot: {"slot": slot, "candidates": [candidate]}}}
    prompt_generator.candidate_pack_project_candidate_surfaces(projected)
    semantics.apply_public_semantics(projected, {
        candidate["id"]: semantics.semantic_source(entry, slot, data["candidate_semantic_policy"])})
    prompt_generator.candidate_pack_recompute_id(projected)
    detail = views.build_view(projected, [candidate["id"]])
    views.verify_view(projected, detail)
    return candidate, detail
