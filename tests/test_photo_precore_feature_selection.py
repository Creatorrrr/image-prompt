from __future__ import annotations

import ast
import copy
import hashlib
import inspect
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
CATALOG_PATH = SKILL_DIR / "precore" / "visual_feature_catalog.json"
VALIDATOR_PATH = SKILL_DIR / "scripts" / "validate_precore_feature_selection.py"
if str(VALIDATOR_PATH.parent) not in sys.path:
    sys.path.insert(0, str(VALIDATOR_PATH.parent))

import prompt_generator  # noqa: E402
import validate_precore_feature_selection as feature_selection  # noqa: E402
from tests import photo_prompt_fixtures  # noqa: E402


SOURCE_CATEGORIES_SHA256 = "2ba9349110a52be0decff94f0efcb57502db3e7c5846a3a46f4a5b9475b5aecd"
REQUEST = "Two adult friends exchange a book at a train station."
BASELINE = (
    "Two adult friends exchange a book in a busy train station. "
    "One extends a worn book toward the other while the recipient's open hand "
    "reaches across the small gap. Both hands and the book stay in the middle "
    "of the frame, with passing commuters visible behind them. Soft daylight "
    "from the station windows keeps the exchange readable as one candid moment."
)
CONVENIENCE_ACTION = (
    "she draws that same companion's bare left hand against her left cheek "
    "with her gloved right hand"
)
CONVENIENCE_OUTFIT = (
    "a black satin slip dress with a low square neckline and long mirror-gloss black latex gloves"
)


def convenience_artifacts(
    *, action: str = CONVENIENCE_ACTION, outfit: str = CONVENIENCE_OUTFIT
) -> tuple[dict, bytes, dict, dict, dict, dict]:
    catalog, catalog_bytes, selection, envelope, _, review = artifacts()
    request = "An adult convenience-store girlfriend shows soft mock-scolding affection toward her companion."
    baseline = (
        "An adult convenience-store girlfriend shows soft mock-scolding affection toward "
        "her companion at a convenience-store entrance. While making an affectionate "
        f"demand, {action}. She wears {outfit}. Direct flash makes the contact readable "
        "against the softly glowing shop windows during their night outing."
    )
    core = photo_prompt_fixtures.core(
        request,
        interpreted_intent="The affectionate demand is requested; the hand arrangement and clothing are editable choices.",
        subject="an adult convenience-store girlfriend",
        setting="a convenience-store entrance during a night outing",
        event="making an affectionate demand",
        visual_priorities=("soft mock-scolding affection", "a legible affectionate demand"),
        baseline_prompt_en=baseline,
        anchor_evidence=(
            "soft mock-scolding affection",
            "An adult convenience-store girlfriend",
            "making an affectionate demand",
        ),
        open_dimensions=("appearance", "action", "pose", "relationship", "composition", "lighting"),
    )
    core["semantic_assertions"] = [{
        "assertion_id": "affectionate_demand",
        "dimension": "event",
        "polarity": "required",
        "source_span_ids": ["topic"],
        "affected_dimensions": ["event"],
        "axes": {"interaction": "affectionate_demand_toward_companion"},
        "evidence": {
            "primary_action_phrase": "making an affectionate demand",
            "target_phrase": "that same companion",
        },
    }]
    request_sha = hashlib.sha256(request.encode()).hexdigest()
    baseline_sha = hashlib.sha256(core["baseline_prompt_en"].encode()).hexdigest()
    envelope.update(
        request_text=request,
        request_sha256=request_sha,
        active_spans=[{"span_id": "topic", "start": 0, "end": len(request), "text": request}],
    )
    selection.update(request_sha256=request_sha, baseline_prompt_sha256=baseline_sha)
    review["prompt_sha256"] = baseline_sha
    selection["selected"] = [
        {
            "category_id": category_id,
            "basis": basis,
            "source_span_ids": [] if basis == "agent_visual_choice" else ["topic"],
            "source_text": source_text,
            "derivation": derivation,
            "reason": reason,
            "baseline_evidence": evidence,
        }
        for category_id, basis, source_text, derivation, reason, evidence in (
            ("feature.subject", "explicit_request", "adult convenience-store girlfriend", None,
             "The requested adult girlfriend is the subject.", "An adult convenience-store girlfriend"),
            ("feature.situation", "request_derived", None,
             "The requested mock-scolding affection is shown as an affectionate demand.",
             "The affectionate demand carries the requested relationship.", "making an affectionate demand"),
            ("feature.location", "request_derived", None,
             "The requested convenience-store setting is staged at its entrance.",
             "The shop entrance provides a readable place.", "a convenience-store entrance"),
            ("feature.interaction", "agent_visual_choice", None, None,
             "The chosen touch stages the demand with a concrete consequence.", action),
            ("feature.clothing", "agent_visual_choice", None, None,
             "The chosen outfit creates a material contrast during the touch.", outfit),
        )
    ]
    return catalog, catalog_bytes, selection, envelope, core, review


def artifacts() -> tuple[dict, bytes, dict, dict, dict, dict]:
    catalog_bytes = CATALOG_PATH.read_bytes()
    catalog = json.loads(catalog_bytes)
    request_sha = hashlib.sha256(REQUEST.encode("utf-8")).hexdigest()
    baseline_sha = hashlib.sha256(BASELINE.encode("utf-8")).hexdigest()
    envelope = {
        "contract_version": "photo-request-envelope/v1",
        "provenance": "requesting_user",
        "request_id": "feature-test-arm",
        "request_text": REQUEST,
        "request_sha256": request_sha,
        "active_spans": [
            {"span_id": "topic", "start": 0, "end": len(REQUEST), "text": REQUEST}
        ],
    }
    core = {
        "contract_version": "photo-authorial-core/v3",
        "provenance": "agent_prepack",
        "source_request": REQUEST,
        "baseline_prompt_en": BASELINE,
    }
    review = {
        "contract_version": "photo-embodiment-review/v1",
        "provenance": "agent_prepack",
        "prompt_sha256": baseline_sha,
    }
    selected = [
        {
            "category_id": "feature.situation",
            "basis": "explicit_request",
            "source_span_ids": ["topic"],
            "source_text": "Two adult friends",
            "derivation": None,
            "reason": "The relationship defines the scene.",
            "baseline_evidence": "Two adult friends exchange a book",
        },
        {
            "category_id": "feature.interaction",
            "basis": "request_derived",
            "source_span_ids": ["topic"],
            "source_text": None,
            "derivation": "The requested exchange needs a legible transfer between people.",
            "reason": "The handoff must be visible.",
            "baseline_evidence": "One extends a worn book toward the other",
        },
        {
            "category_id": "feature.props",
            "basis": "explicit_request",
            "source_span_ids": ["topic"],
            "source_text": "book",
            "derivation": None,
            "reason": "The book is the exchanged object.",
            "baseline_evidence": "worn book",
        },
        {
            "category_id": "feature.location",
            "basis": "explicit_request",
            "source_span_ids": ["topic"],
            "source_text": "train station",
            "derivation": None,
            "reason": "The setting distinguishes the request.",
            "baseline_evidence": "busy train station",
        },
        {
            "category_id": "feature.composition",
            "basis": "agent_visual_choice",
            "source_span_ids": [],
            "source_text": None,
            "derivation": None,
            "reason": "Keep the handoff readable amid the station activity.",
            "baseline_evidence": "Both hands and the book stay in the middle of the frame",
        },
    ]
    selection = {
        "contract_version": "photo-precore-feature-selection/v1",
        "request_id": "feature-test-arm",
        "active_span_ids": ["topic"],
        "catalog_path": feature_selection.CATALOG_PATH,
        "catalog_schema_version": "photo-precore-feature-catalog/v1",
        "catalog_sha256": hashlib.sha256(catalog_bytes).hexdigest(),
        "request_sha256": request_sha,
        "baseline_prompt_sha256": baseline_sha,
        "selected": selected,
    }
    return catalog, catalog_bytes, selection, envelope, core, review


class PhotoPrecoreFeatureSelectionTests(unittest.TestCase):
    def test_baseline_normalizer_matches_the_generator(self) -> None:
        def body_tree(function: object) -> str:
            statements = ast.parse(inspect.getsource(function)).body[0].body
            if (
                isinstance(statements[0], ast.Expr)
                and isinstance(statements[0].value, ast.Constant)
                and isinstance(statements[0].value.value, str)
            ):
                statements = statements[1:]
            return ast.dump(
                ast.Module(body=statements, type_ignores=[]),
                include_attributes=False,
            )

        self.assertEqual(
            body_tree(feature_selection.clean_spaces),
            body_tree(prompt_generator.clean_spaces),
        )

    def test_catalog_preserves_all_source_examples_and_marks_additions(self) -> None:
        catalog, _, _, _, _, _ = artifacts()
        by_id = feature_selection.validate_catalog(catalog)
        source = [row for row in catalog["categories"] if row["source_number"] is not None]
        additions = [
            row for row in catalog["categories"] if row["source_number"] is None
        ]
        self.assertEqual(len(source), 45)
        self.assertEqual(sum(len(row["source_examples"]) for row in source), 527)
        self.assertEqual(
            {row["id"] for row in additions},
            {
                "feature.primary_object",
                "feature.in_frame_text",
                "feature.format_and_aspect_ratio",
            },
        )
        frozen_source = [
            {
                "id": row["id"],
                "source_number": row["source_number"],
                "group": row["group"],
                "name_ko": row["name_ko"],
                "name_en": row["name_en"],
                "source_examples": row["source_examples"],
                "added_examples": row["added_examples"],
            }
            for row in source
        ]
        source_digest = hashlib.sha256(
            json.dumps(
                frozen_source, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(source_digest, SOURCE_CATEGORIES_SHA256)
        self.assertEqual(len(by_id), 48)

    def test_selection_binds_five_categories_to_request_and_baseline(self) -> None:
        catalog, catalog_bytes, selection, envelope, core, review = artifacts()
        result = feature_selection.validate_selection(
            catalog, catalog_bytes, selection, envelope, core, review
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["selected_count"], 5)
        self.assertEqual(result["warnings"], [])
        self.assertEqual(
            feature_selection.clean_spaces(BASELINE),
            prompt_generator.clean_spaces(BASELINE),
        )
        self.assertEqual(
            feature_selection.clean_spaces("A  scene , here!!"),
            prompt_generator.clean_spaces("A  scene , here!!"),
        )

    def test_ten_categories_are_accepted_and_overlap_is_reported(self) -> None:
        catalog, catalog_bytes, selection, envelope, core, review = artifacts()
        for category_id, phrase in (
            ("feature.lighting_source", "Soft daylight"),
            ("feature.light_quality", "station windows"),
            ("feature.framing", "passing commuters visible behind them"),
            ("feature.shot_size", "in the middle of the frame"),
            ("feature.visual_hierarchy", "one candid moment"),
        ):
            selection["selected"].append(
                {
                    "category_id": category_id,
                    "basis": "agent_visual_choice",
                    "source_span_ids": [],
                    "source_text": None,
                    "derivation": None,
                    "reason": f"Review {category_id} for this frame.",
                    "baseline_evidence": phrase,
                }
            )
        result = feature_selection.validate_selection(
            catalog, catalog_bytes, selection, envelope, core, review
        )
        self.assertEqual(result["selected_count"], 10)

        selection = artifacts()[2]
        selection["selected"][1]["reason"] = selection["selected"][0]["reason"]
        warnings = feature_selection.validate_selection(
            catalog, catalog_bytes, selection, envelope, core, review
        )["warnings"]
        self.assertIn("repeated_reason", warnings)
        self.assertNotIn("repeated_evidence", warnings)

        selection = artifacts()[2]
        selection["selected"][1]["baseline_evidence"] = selection["selected"][0][
            "baseline_evidence"
        ]
        warnings = feature_selection.validate_selection(
            catalog, catalog_bytes, selection, envelope, core, review
        )["warnings"]
        self.assertIn("repeated_evidence", warnings)
        self.assertNotIn("repeated_reason", warnings)

        selection = artifacts()[2]
        for item, category_id in zip(
            selection["selected"][:3],
            ("feature.lighting_source", "feature.light_quality", "feature.exposure"),
        ):
            item["category_id"] = category_id
        warnings = feature_selection.validate_selection(
            catalog, catalog_bytes, selection, envelope, core, review
        )["warnings"]
        self.assertIn("technique_categories_are_majority", warnings)

    def test_rejects_stale_or_forged_selection_binding(self) -> None:
        catalog, catalog_bytes, selection, envelope, core, review = artifacts()
        cases = [
            (
                "under minimum",
                lambda record, env, authored, body: record["selected"].pop(),
            ),
            (
                "duplicate category",
                lambda record, env, authored, body: record["selected"].append(
                    copy.deepcopy(record["selected"][0])
                ),
            ),
            (
                "over maximum",
                lambda record, env, authored, body: record["selected"].extend(
                    {
                        "category_id": category_id,
                        "basis": "agent_visual_choice",
                        "source_span_ids": [],
                        "source_text": None,
                        "derivation": None,
                        "reason": category_id,
                        "baseline_evidence": "Soft daylight",
                    }
                    for category_id in (
                        "feature.lighting_source",
                        "feature.light_quality",
                        "feature.framing",
                        "feature.shot_size",
                        "feature.visual_hierarchy",
                        "feature.capture_medium",
                    )
                ),
            ),
            (
                "unknown category",
                lambda record, env, authored, body: record["selected"][0].__setitem__(
                    "category_id", "feature.unknown"
                ),
            ),
            (
                "catalog hash",
                lambda record, env, authored, body: record.__setitem__(
                    "catalog_sha256", "0" * 64
                ),
            ),
            (
                "wrong request span",
                lambda record, env, authored, body: record["selected"][0].__setitem__(
                    "source_text", "strangers"
                ),
            ),
            (
                "invented requester basis",
                lambda record, env, authored, body: record["selected"][4].__setitem__(
                    "basis", "explicit_request"
                ),
            ),
            (
                "missing baseline evidence",
                lambda record, env, authored, body: record["selected"][1].__setitem__(
                    "baseline_evidence", "a floating book"
                ),
            ),
            (
                "stale embodiment review",
                lambda record, env, authored, body: body.__setitem__(
                    "prompt_sha256", "0" * 64
                ),
            ),
            (
                "different arm",
                lambda record, env, authored, body: record.__setitem__(
                    "request_id", "other-arm"
                ),
            ),
            (
                "wrong envelope provenance",
                lambda record, env, authored, body: env.__setitem__(
                    "provenance", "agent_prepack"
                ),
            ),
            (
                "wrong core version",
                lambda record, env, authored, body: authored.__setitem__(
                    "contract_version", "photo-authorial-core/v2"
                ),
            ),
            (
                "wrong review version",
                lambda record, env, authored, body: body.__setitem__(
                    "contract_version", "photo-embodiment-review/v0"
                ),
            ),
            (
                "wrong catalog path",
                lambda record, env, authored, body: record.__setitem__(
                    "catalog_path", "different/catalog.json"
                ),
            ),
            (
                "wrong active span",
                lambda record, env, authored, body: record.__setitem__(
                    "active_span_ids", ["other-arm"]
                ),
            ),
            (
                "noncanonical baseline",
                lambda record, env, authored, body: authored.__setitem__(
                    "baseline_prompt_en", "  " + BASELINE
                ),
            ),
            (
                "unsupported selection field",
                lambda record, env, authored, body: record.__setitem__(
                    "extra", "unsupported"
                ),
            ),
        ]
        for name, mutate in cases:
            with self.subTest(name=name):
                record = copy.deepcopy(selection)
                env = copy.deepcopy(envelope)
                authored = copy.deepcopy(core)
                body = copy.deepcopy(review)
                mutate(record, env, authored, body)
                with self.assertRaises(feature_selection.SelectionValidationError):
                    feature_selection.validate_selection(
                        catalog, catalog_bytes, record, env, authored, body
                    )

    def test_rejects_complete_agent_action_at_each_required_evidence_boundary(self) -> None:
        for boundary in ("definition", "anchor", "assertion"):
            for wrapped in (False, True):
                with self.subTest(boundary=boundary, wrapped=wrapped):
                    args = convenience_artifacts()
                    core = args[4]
                    phrase = CONVENIENCE_ACTION
                    if wrapped:
                        phrase = "making an affectionate demand, " + phrase
                    if boundary == "definition":
                        core["user_definitions"] = [{
                            "term": "affectionate demand",
                            "source_text": core["source_request"],
                            "interpreted_meaning": "Soft mock-scolding affection directed toward the same adult companion",
                            "prompt_evidence": phrase,
                        }]
                        expected_path = "user_definitions[0].prompt_evidence"
                    elif boundary == "anchor":
                        core["intent_lock"]["semantic_anchors"][-1]["prompt_evidence"] = phrase
                        expected_path = "intent_lock.semantic_anchors[2].prompt_evidence"
                    else:
                        core["semantic_assertions"][0]["evidence"]["primary_action_phrase"] = phrase
                        expected_path = "semantic_assertions[0].evidence.primary_action_phrase"
                    with self.assertRaises(feature_selection.SelectionValidationError) as raised:
                        feature_selection.validate_selection(*args)
                    self.assertIn("feature.interaction", str(raised.exception))
                    self.assertIn("agent_visual_choice", str(raised.exception))
                    self.assertIn(expected_path, str(raised.exception))

    def test_property_anchor_in_an_open_dimension_still_binds_literal_evidence(self) -> None:
        args = convenience_artifacts()
        core = args[4]
        core["intent_lock"]["semantic_anchors"].append({
            "anchor_id": "requested_outfit",
            "source_text": core["source_request"],
            "dimension": "appearance",
            "target": "main_subject",
            "property": "clothing",
            "prompt_evidence": CONVENIENCE_OUTFIT,
        })
        with self.assertRaises(feature_selection.SelectionValidationError) as raised:
            feature_selection.validate_selection(*args)
        self.assertIn("feature.clothing", str(raised.exception))
        self.assertIn("intent_lock.semantic_anchors[3].prompt_evidence", str(raised.exception))

    def test_narrow_requester_meaning_allows_glove_handedness_and_outfit_choices(self) -> None:
        for action, outfit in (
            (CONVENIENCE_ACTION, CONVENIENCE_OUTFIT),
            (CONVENIENCE_ACTION.replace("gloved right hand", "bare right hand"), CONVENIENCE_OUTFIT),
            (CONVENIENCE_ACTION.replace("bare left hand", "bare right hand")
             .replace("left cheek", "right cheek").replace("gloved right hand", "gloved left hand"),
             "a fitted cotton T-shirt and high-rise jeans"),
        ):
            with self.subTest(action=action, outfit=outfit):
                args = convenience_artifacts(action=action, outfit=outfit)
                before = copy.deepcopy(args[4])
                self.assertTrue(feature_selection.validate_selection(*args)["valid"])
                self.assertEqual(args[4], before)
                # The required target phrase is inside the longer authored gesture.
                self.assertIn(before["semantic_assertions"][0]["evidence"]["target_phrase"], action)

    def test_advisory_excluded_and_nonliteral_direction_do_not_create_locks(self) -> None:
        args = convenience_artifacts()
        core = args[4]
        core["interpreted_intent"] += " " + CONVENIENCE_ACTION
        core["visual_priorities"].append(CONVENIENCE_OUTFIT)
        core["semantic_assertions"][0]["axes"]["primary_action"] = CONVENIENCE_ACTION
        for polarity in ("advisory", "excluded"):
            core["semantic_assertions"].append({
                "assertion_id": polarity + "_gesture",
                "dimension": "action",
                "polarity": polarity,
                "source_span_ids": ["topic"],
                "affected_dimensions": ["action"],
                "axes": {"action": "hand_contact"},
                "evidence": {"action_phrase": CONVENIENCE_ACTION},
            })
        self.assertTrue(feature_selection.validate_selection(*args)["valid"])

    def test_shared_words_and_paraphrases_do_not_establish_literal_ownership_conflict(self) -> None:
        for phrase in (
            "bare left hand",
            "with her gloved right hand",
            "she brings her companion's hand to her cheek",
        ):
            with self.subTest(phrase=phrase):
                args = convenience_artifacts()
                args[4]["semantic_assertions"][0]["evidence"]["primary_action_phrase"] = phrase
                self.assertTrue(feature_selection.validate_selection(*args)["valid"])

    def test_case_and_whitespace_variants_still_conflict_with_complete_agent_evidence(self) -> None:
        for phrase in (
            CONVENIENCE_ACTION.capitalize(),
            CONVENIENCE_ACTION.upper(),
            "  " + CONVENIENCE_ACTION.replace(" ", "  \n\t") + "  ",
            "Making an affectionate demand, " + CONVENIENCE_ACTION.upper().replace(" ", "\n"),
        ):
            with self.subTest(phrase=phrase):
                args = convenience_artifacts()
                args[4]["intent_lock"]["semantic_anchors"][-1]["prompt_evidence"] = phrase
                with self.assertRaises(feature_selection.SelectionValidationError) as raised:
                    feature_selection.validate_selection(*args)
                self.assertIn("intent_lock.semantic_anchors[2].prompt_evidence", str(raised.exception))

        args = convenience_artifacts(action=CONVENIENCE_ACTION.upper())
        args[4]["semantic_assertions"][0]["evidence"]["primary_action_phrase"] = CONVENIENCE_ACTION
        with self.assertRaises(feature_selection.SelectionValidationError):
            feature_selection.validate_selection(*args)

    def test_ascii_word_boundaries_prevent_hand_from_matching_handmade(self) -> None:
        for required_phrase, conflicts in (
            ("handmade fabric", False),
            ("offhand gesture", False),
            ("hand2 print", False),
            ("2hand print", False),
            ("a held hand", True),
            ("(hand)", True),
            ("hand-held", True),
            ("hand's grip", True),
        ):
            with self.subTest(required_phrase=required_phrase):
                args = convenience_artifacts(
                    outfit="a black satin dress carrying the words " + required_phrase
                )
                args[2]["selected"][3]["baseline_evidence"] = "hand"
                args[4]["semantic_assertions"][0]["evidence"]["primary_action_phrase"] = required_phrase
                self.assertEqual(
                    photo_prompt_fixtures.audit_composed_prompt.text_contains_term(required_phrase, "hand"),
                    conflicts,
                )
                if conflicts:
                    with self.assertRaises(feature_selection.SelectionValidationError):
                        feature_selection.validate_selection(*args)
                else:
                    self.assertTrue(feature_selection.validate_selection(*args)["valid"])

    def test_explicit_requested_gesture_keeps_its_existing_hard_binding(self) -> None:
        catalog, catalog_bytes, selection, envelope, core, review = convenience_artifacts()
        request = core["source_request"] + " Preserve this action: " + CONVENIENCE_ACTION + "."
        request_sha = hashlib.sha256(request.encode()).hexdigest()
        envelope.update(
            request_text=request, request_sha256=request_sha,
            active_spans=[{"span_id": "topic", "start": 0, "end": len(request), "text": request}],
        )
        core["source_request"] = request
        selection["request_sha256"] = request_sha
        gesture = selection["selected"][3]
        gesture.update(basis="explicit_request", source_span_ids=["topic"], source_text=CONVENIENCE_ACTION)
        core["intent_lock"]["semantic_anchors"][-1]["prompt_evidence"] = CONVENIENCE_ACTION
        core["semantic_assertions"][0]["evidence"]["primary_action_phrase"] = CONVENIENCE_ACTION
        normalized = prompt_generator.normalize_authorial_core(
            core, request_envelope=prompt_generator.normalize_request_envelope(envelope)
        )
        self.assertTrue(feature_selection.validate_selection(
            catalog, catalog_bytes, selection, envelope, normalized, review
        )["valid"])
        # Inspect the existing literal anchor check without claiming a complete pack audit.
        def anchor_failures(prompt: str) -> list[dict]:
            return [row for row in photo_prompt_fixtures.audit_composed_prompt.audit_authorial_core(
                {"authorial_core": normalized}, {}, prompt
            ) if row["check"] == "intent_lock_prompt_evidence"]

        baseline = normalized["baseline_prompt_en"]
        self.assertEqual(anchor_failures(baseline), [])
        self.assertEqual(len(anchor_failures(baseline.replace("gloved right hand", "bare right hand"))), 1)

        gesture.update(basis="agent_visual_choice", source_span_ids=[], source_text=None)
        with self.assertRaises(feature_selection.SelectionValidationError):
            feature_selection.validate_selection(
                catalog, catalog_bytes, selection, envelope, normalized, review
            )

    def test_cli_accepts_records_without_echoing_source_examples(self) -> None:
        _, _, selection, envelope, core, review = artifacts()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, value in (
                ("selection.json", selection),
                ("envelope.json", envelope),
                ("core.json", core),
                ("review.json", review),
            ):
                (root / name).write_text(
                    json.dumps(value, ensure_ascii=False), encoding="utf-8"
                )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR_PATH),
                    "--catalog",
                    str(CATALOG_PATH),
                    "--request-envelope",
                    str(root / "envelope.json"),
                    "--authorial-core",
                    str(root / "core.json"),
                    "--embodiment-review",
                    str(root / "review.json"),
                    "--selection",
                    str(root / "selection.json"),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["selected_count"], 5)
        self.assertEqual(json.loads(completed.stdout)["catalog_mode"], "current")
        self.assertNotIn("행동 중간의 순간", completed.stdout)

    def test_live_cli_rejects_a_self_consistent_alternate_catalog(self) -> None:
        catalog, _, selection, envelope, core, review = artifacts()
        catalog["categories"][0]["source_examples"][0] = "Changed source example"
        alternate_bytes = json.dumps(catalog, ensure_ascii=False).encode("utf-8")
        selection["catalog_sha256"] = hashlib.sha256(alternate_bytes).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "catalog.json").write_bytes(alternate_bytes)
            for name, value in (
                ("selection.json", selection),
                ("envelope.json", envelope),
                ("core.json", core),
                ("review.json", review),
            ):
                (root / name).write_text(
                    json.dumps(value, ensure_ascii=False), encoding="utf-8"
                )
            command = [
                sys.executable,
                str(VALIDATOR_PATH),
                "--catalog",
                str(root / "catalog.json"),
                "--request-envelope",
                str(root / "envelope.json"),
                "--authorial-core",
                str(root / "core.json"),
                "--embodiment-review",
                str(root / "review.json"),
                "--selection",
                str(root / "selection.json"),
            ]
            live = subprocess.run(command, capture_output=True, text=True, check=False)
            historical = subprocess.run(
                command + ["--historical-catalog"],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(live.returncode, 2)
        self.assertIn("differ from the current", live.stderr)
        self.assertEqual(historical.returncode, 0, historical.stderr)
        self.assertEqual(json.loads(historical.stdout)["catalog_mode"], "historical")

    def test_catalog_is_not_an_index_input(self) -> None:
        for name in (
            "build_visual_profile_index.py",
            "build_semantic_index.py",
            "bm25f_retrieval.py",
            "photo_visual_retrieval.py",
        ):
            script = (SKILL_DIR / "scripts" / name).read_text(encoding="utf-8")
            self.assertNotIn("precore/visual_feature_catalog.json", script)
            self.assertNotIn("visual_feature_catalog", script)


if __name__ == "__main__":
    unittest.main()
