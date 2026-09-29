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


def generate_once(*args, **kwargs):
    """Prepare complete current inputs before invoking the real sampler."""
    import copy

    creative_controls = prompt_generator.creative_controls
    import photo_embodiment

    fixture_context = kwargs.pop("fixture_context", {})
    frozen = kwargs.get("authorial_core")
    if isinstance(frozen, dict):
        snapshot = kwargs.get("creative_control_snapshot")
        if snapshot is None:
            overrides = {
                "sensual": kwargs.get("sensual_intensity", 0),
                "fetish": kwargs.get("fetish_intensity", 0),
                "creativity": (
                    kwargs.get("creativity") if kwargs.get("creativity") is not None else 2
                ),
                "surreal": kwargs.get("surreal", 0),
            }
            if kwargs.get("adult_appeal_emphasis"):
                overrides["adult_appeal_emphasis"] = kwargs["adult_appeal_emphasis"]
            snapshot = creative_controls.resolve(
                frozen["source_request"], overrides=overrides, context=fixture_context, seed=7
            )
            binding = frozen["request_binding"]
            request = prompt_generator.normalize_request_envelope(
                {
                    "contract_version": "photo-request-envelope/v1",
                    "provenance": "requesting_user",
                    "request_id": binding["request_id"],
                    "request_text": frozen["source_request"],
                    "request_sha256": binding["request_sha256"],
                    "active_spans": binding["active_spans"],
                }
            )
            raw = copy.deepcopy(frozen)
            for key in ("canonical_sha256", "core_id", "request_binding"):
                raw.pop(key, None)
            raw["intent_lock"] = {
                key: value
                for key, value in raw["intent_lock"].items()
                if key
                in {
                    "contract_version",
                    "priority",
                    "semantic_anchors",
                    "locked_dimensions",
                    "open_dimensions",
                }
            }
            if isinstance(raw.get("request_lineage"), dict):
                raw["request_lineage"].pop("canonical_sha256", None)
            raw["creative_controls_sha256"] = snapshot["canonical_sha256"]
            bound = prompt_generator.normalize_authorial_core(
                raw, request_envelope=request, creative_control_snapshot=snapshot
            )
            frozen.clear()
            frozen.update(bound)
            kwargs["creative_control_snapshot"] = snapshot
        result = prompt_generator.generate_once(*args, **kwargs)
        result["provenance"]["embodiment_preflight"] = photo_embodiment.build_policy(
            frozen, review(frozen["baseline_prompt_en"])
        )
        return result
    return prompt_generator.generate_once(*args, **kwargs)


def composition_review(pack: dict, prompt: str) -> dict:
    return {
        "source_contract_sha256": pack["embodiment_preflight"]["canonical_sha256"],
        "review": review(prompt, "agent_postcomposition"),
    }


def run_current(
    core_input: dict,
    *,
    seed: int = 91,
    creativity: int = 2,
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
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--emit-candidate-pack",
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
