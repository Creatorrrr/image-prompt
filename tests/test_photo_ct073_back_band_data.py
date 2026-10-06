"""The CT073 successor changes eight DATA leaves and two genuine index vectors.

The original V24 source is authenticated by the offline parent fixture. Provider
receipts retain their original c907 provenance; this test verifies their exact
input and numeric-response linkage, not the unavailable original HTTP bytes.
"""
from __future__ import annotations

import copy
from unittest import mock

import hashlib
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest

from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/photo-prompt-image-generator")
ASSETS = ROOT / SKILL / "assets"
EVIDENCE = ROOT / "docs/research-evidence/photo-prompt/ct073-back-band-maintenance-integration-20261006"
PRIOR_EVIDENCE = EVIDENCE / "prior-ct073"
sys.path.insert(0, str(ROOT / SKILL / "scripts"))
import prompt_generator as pg

ORDINARY_SOURCE = "photo_prompt_clothing_structure_extension.json"
VISUAL_SOURCE = "photo_prompt_visual_obligations_clothing_structure.json"
ORDINARY_INDEX = "photo_prompt_semantic_index.json"
VISUAL_INDEX = "photo_prompt_visual_profile_index.json"
ORDINARY_KEY = "slot:garment_detail:clt_ct073_v2"
VISUAL_KEY = "clothing_ct073_v2"
PARENT_COMMIT = "3b481ca94fdbbeeb453e1d3ec657db0f5baf6a80"
RECEIPT_COMMIT = "c907513925cea26e263173247c7e0c8d837c1fbe"
MAINTENANCE_ID = "photo_prompt_clothing_structure_extension-ct073-back-band-owner-20261005"
MAINTENANCE_SHA = "a85bd1c477a534bf000d453e601bcbf080435929161b375d65373a0636bd09c4"
SPACE = {"provider": "gemini", "embedding_model": "gemini-embedding-2", "embedding_dimensions": 768}

# These reviewed values are deliberately independent of the mutable V25 proof.
ORDINARY_DELTAS = {
    "/affected_properties/0/property": (
        "wardrobe.details.bra_strap_adjust", "wardrobe.details.bra_back_band_closure"),
    "/embedding_text": (
        "hook-and-eye rows aligned across the back band opening | 뒷밴드 개구 양쪽에 맞춰진 훅앤아이 줄 | bra strap | hook-and-eye rows aligned across the back band opening",
        "hook-and-eye rows aligned across the back band opening | 뒷밴드 개구 양쪽에 맞춰진 훅앤아이 줄 | bra back band | hook-and-eye rows aligned across the back band opening"),
    "/keywords/2": ("브라 스트랩의 연결", "브라 뒷밴드의 여밈"),
    "/relations/0/subject": ("bra strap", "bra back band"),
}
VISUAL_DELTAS = {
    "/concept_candidate/affected_properties/0/property": (
        "wardrobe.details.bra_strap_adjust", "wardrobe.details.bra_back_band_closure"),
    "/reject_substitutes/0": (
        "링은 떠 있는 장식이 아니며 끈 조절 상태로 실제 지지력을 판단하지 않는다",
        "뒷밴드 개구 양쪽의 훅앤아이 줄을 대신해 제시된 어깨 스트랩의 링과 슬라이더"),
    "/semantics/contrast_examples/0": (
        "링은 떠 있는 장식이 아니며 끈 조절 상태로 실제 지지력을 판단하지 않는다",
        "뒷밴드 개구 양쪽에 정렬된 훅앤아이 줄은 보이는 여밈 하드웨어이며, 정렬만으로 실제 체결 여부나 지지 성능을 판단하지 않는다"),
    "/semantics/paraphrase_examples/0": (
        "observable bra strap detail showing hook-and-eye rows aligned across the back band opening",
        "observable bra back band detail showing hook-and-eye rows aligned across the back band opening"),
}
MAINTENANCE_DELTAS = {
    "/maintenance_ref/record_id": (
        "photo_prompt_clothing_structure_extension-uniform-maintenance-seal-20261004", MAINTENANCE_ID),
    "/maintenance_ref/sha256": (
        "302adba31b0b3c2a8071b5426822007ab71b6f9f44c7595ceaaa3475786e920b", MAINTENANCE_SHA),
}
SOURCE_HASHES = {
    ORDINARY_SOURCE: ("7055f19fda53c93748c3085b61b344ca1918dcae6caf7afa99f073779b1ab367",
                      "c870c525974604a8f504615586ab1fe5af3b6e0c2467f99349ca117af436c22c"),
    VISUAL_SOURCE: ("0c4117e038d51e12af2747360deada285b1a6dbb1b9998a58d8e5cd47b42e7b1",
                    "6a2c1aadf66a8c1969c365f95856e19bd33a8441521b88ee00edd091e328ae83"),
}
PROJECTIONS = {
    "ordinary": {
        "key": ORDINARY_KEY, "slot": "01", "file": "ordinary-input.txt", "bytes": 859,
        "sha256": "5aa2d9dfabe4574fae3aebe6c97acc4f0fd6f017ea31e6a5f9ca37e5819f333c",
        "receipt_sha256": "12b18e61a2bcfbca1a47c9b08a6951a36c2dad53c3c849dbd1226192f1988815",
        "vector_sha256": "7d862753fe50fbfc4458854cbfe2fcca0c3beee82c35d35fa6fca11666eb87a3",
        "old_vector_sha256": "29b54defa7b86c40bef407dd635efa3405919636a6e1503b1ed8ac884991d194",
        "text": "Photo prompt slot concept for garment_detail: hook-and-eye rows aligned across the back band opening | 뒷밴드 개구 양쪽에 맞춰진 훅앤아이 줄 | bra back band | hook-and-eye rows aligned across the back band opening. It should retrieve visually compatible photographic details for this slot. en label: hook-and-eye rows aligned across the back band opening. ko label: 뒷밴드 개구 양쪽에 맞춰진 훅앤아이 줄. aliases: 뒷밴드 개구 양쪽에 맞춰진 훅앤아이 줄. keywords: 뒷밴드 개구 양쪽에 맞춰진 훅앤아이 줄, hook-and-eye rows aligned across the back band opening, 브라 뒷밴드의 여밈. slot: garment_detail. visual concepts: hook-and-eye rows aligned across the back band opening. semantic relations: bra back band has visible construction hook-and-eye rows aligned across the back band opening.",
    },
    "visual_profile": {
        "key": VISUAL_KEY, "slot": "02", "file": "visual-profile-input.txt", "bytes": 207,
        "sha256": "906211c2c67770cc7d680c9f538c96dcdb6e36fbf052a9913949b1a4abdaad3e",
        "receipt_sha256": "df29fd43d76d83452e7171dd7a8d3d7b012965a43f76f1e3c44e43cb7a46aff4",
        "vector_sha256": "d0dde0a4726ccc814f52d2de234fa5e5c702dcc01cfa45c519add0acc7ef458a",
        "old_vector_sha256": "326229e3e8ee5af43fe3fb370f575aebb15a41b9e77d450cc4b43ff35062600b",
        "text": "hook-and-eye rows aligned across the back band opening | observable bra back band detail showing hook-and-eye rows aligned across the back band opening | 뒷밴드 개구 양쪽에 맞춰진 훅앤아이 줄",
    },
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical_sha(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode())


def read(path):
    return json.loads(path.read_bytes())


def leaf_delta(before, after, pointer=""):
    """Preserve key membership, array order and scalar types in an exact diff."""
    if type(before) is not type(after):
        return {pointer: (before, after)}
    if isinstance(before, dict):
        if before.keys() != after.keys():
            return {pointer: (before, after)}
        return {p: pair for key in before for p, pair in leaf_delta(
            before[key], after[key], pointer + "/" + key.replace("~", "~0").replace("/", "~1")).items()}
    if isinstance(before, list):
        if len(before) != len(after):
            return {pointer: (before, after)}
        return {p: pair for i, (old, new) in enumerate(zip(before, after))
                for p, pair in leaf_delta(old, new, pointer + "/" + str(i)).items()}
    return {} if before == after else {pointer: (before, after)}


class CT073BackBandDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Keep the five-file CT073 transition bound to its original V25 tree.
        # The current compiler also verifies compatibility with these frozen DATA.
        original_globals = {name: globals()[name] for name in ('ROOT', 'ASSETS', 'EVIDENCE', 'PRIOR_EVIDENCE')}
        frozen = tempfile.TemporaryDirectory(prefix='sealed-v25-ct073-data-')
        cls.addClassCleanup(frozen.cleanup)
        root = Path(frozen.name)
        fixtures.materialize_v25_parent_source(root, source_root=ROOT)
        evidence = root / 'docs/research-evidence/photo-prompt/ct073-back-band-maintenance-integration-20261006'
        cls.addClassCleanup(lambda: globals().update(original_globals))
        globals().update(ROOT=root, ASSETS=root / SKILL / 'assets', EVIDENCE=evidence,
                         PRIOR_EVIDENCE=evidence / 'prior-ct073')
        cls.directory = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.directory.cleanup)
        cls.parent = Path(cls.directory.name) / "v24"
        fixtures.materialize_v24_parent_source(cls.parent)
        cls.parent_assets = cls.parent / SKILL / "assets"
        cls.original = {name: read(cls.parent_assets / name) for name in SOURCE_HASHES}
        cls.current = {name: read(ASSETS / name) for name in SOURCE_HASHES}
        # Exercise the current compiler against the authenticated predecessor
        # registration. Current additive sources are outside this sealed tree.
        manifest = ASSETS / "photo_prompt_source_manifest.json"
        registered_candidates = pg.photo_source_manifest.extension_files("candidate", manifest)
        registered_profiles = pg.photo_source_manifest.extension_files("visual_profile", manifest)
        required = pg.photo_source_manifest.required_files
        for registration_patch in (
                mock.patch.object(pg, "RESEARCH_EXTENSION_FILENAMES", registered_candidates),
                mock.patch.object(pg, "VISUAL_OBLIGATION_EXTENSION_FILENAMES", registered_profiles),
                mock.patch.object(pg.photo_source_manifest, "required_files",
                                  side_effect=lambda kind: required(kind, manifest))):
            registration_patch.start()
            cls.addClassCleanup(registration_patch.stop)
        cls.data = pg.load_json(ASSETS / "photo_prompt_tags.json")
        cls.old_data = pg.load_json(cls.parent_assets / "photo_prompt_tags.json")
        cls.registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.old_registry = pg.load_visual_obligation_registry(cls.parent_assets / "photo_prompt_visual_obligations.json")
        cls.rows = {row[0]: row for row in pg.iter_semantic_entries(cls.data)}
        cls.old_rows = {row[0]: row for row in pg.iter_semantic_entries(cls.old_data)}
        cls.profiles = {row["id"]: row for row in cls.registry["profiles"]}
        cls.old_profiles = {row["id"]: row for row in cls.old_registry["profiles"]}
        cls.indexes = {
            "ordinary": pg.load_semantic_index_payload(ASSETS / ORDINARY_INDEX),
            "visual_profile": pg.load_visual_profile_index(ASSETS / VISUAL_INDEX, cls.registry),
        }
        cls.old_indexes = {
            "ordinary": pg.load_semantic_index_payload(cls.parent_assets / ORDINARY_INDEX),
            "visual_profile": pg.load_visual_profile_index(cls.parent_assets / VISUAL_INDEX, cls.old_registry),
        }

    def test_authored_source_has_exact_eight_string_and_two_maintenance_deltas(self):
        expected = {
            ORDINARY_SOURCE: {**{"/slots/garment_detail/89" + p: pair for p, pair in ORDINARY_DELTAS.items()},
                              **MAINTENANCE_DELTAS},
            VISUAL_SOURCE: {"/profiles/144" + p: pair for p, pair in VISUAL_DELTAS.items()},
        }
        self.assertEqual(8, len(ORDINARY_DELTAS) + len(VISUAL_DELTAS))
        self.assertEqual(2, len(MAINTENANCE_DELTAS))
        for name, changes in expected.items():
            with self.subTest(source=name):
                self.assertEqual(SOURCE_HASHES[name], (
                    sha((self.parent_assets / name).read_bytes()), sha((ASSETS / name).read_bytes())))
                self.assertEqual(changes, leaf_delta(self.original[name], self.current[name]))
                self.assertTrue(all(type(value) is str for pair in changes.values() for value in pair))
        for sources in (self.original, self.current):
            self.assertEqual("clt_ct073_v2", sources[ORDINARY_SOURCE]["slots"]["garment_detail"][89]["id"])
            self.assertEqual(VISUAL_KEY, sources[VISUAL_SOURCE]["profiles"][144]["id"])

    def test_all_136_source_members_and_exact_top_level_asset_inventory_preserved(self):
        manifest = fixtures._v24_parent_manifest()
        self.assertEqual(PARENT_COMMIT, manifest["source_pin"])
        members = [row for row in manifest["members"] if row["path"].startswith(str(SKILL) + "/")
                   and ("/assets/" not in row["path"] or Path(row["path"]).parent == SKILL / "assets")]
        self.assertEqual(136, len(members))
        changed = {str(SKILL / "assets" / name) for name in
                   (ORDINARY_SOURCE, VISUAL_SOURCE, "photo_prompt_textile_surface_extension.json", ORDINARY_INDEX, VISUAL_INDEX)}
        observed = {row["path"] for row in members if sha((ROOT / row["path"]).read_bytes()) != row["sha256"]}
        self.assertEqual(changed, observed)
        self.assertEqual({p.name for p in self.parent_assets.glob("*.json")},
                         {p.name for p in ASSETS.glob("*.json")})

    def test_compilation_changes_only_the_reviewed_two_rows_and_eight_leaves(self):
        self.assertEqual(10082, len(self.rows))
        self.assertEqual(1879, len(self.profiles))
        self.assertEqual(list(self.old_rows), list(self.rows))
        self.assertEqual(list(self.old_profiles), list(self.profiles))
        self.assertEqual([ORDINARY_KEY], [key for key in self.rows if self.rows[key] != self.old_rows[key]])
        self.assertEqual([VISUAL_KEY], [key for key in self.profiles if self.profiles[key] != self.old_profiles[key]])
        self.assertEqual(ORDINARY_DELTAS, leaf_delta(self.old_rows[ORDINARY_KEY][2], self.rows[ORDINARY_KEY][2]))
        self.assertEqual(VISUAL_DELTAS, leaf_delta(self.old_profiles[VISUAL_KEY], self.profiles[VISUAL_KEY]))
        self.assertEqual("df51b0c2691ddd2fb5811fa8e6adedbb45b35dcb25d8c0b509c98d15daaa12e3", pg.dictionary_hash(self.old_data))
        self.assertEqual("0707c32d3c184f155f65c48e7200f1d459b612a0734678e0cbedb4c1a2989786", pg.dictionary_hash(self.data))
        self.assertEqual("f0ff85a9f173df22f32f2d2d5bd32edd14af45f41d1a47a9335a721df97fed9d", canonical_sha(self.old_registry))
        self.assertEqual("0c2c57b6512564761cc159267dee7a76423785a7cb71c9edc4321d6f313ef208", canonical_sha(self.registry))

    def test_v1_siblings_activation_evidence_adult_context_and_native_gates_are_unchanged(self):
        sibling = "slot:garment_detail:clt_ct073_v1"
        self.assertEqual(self.old_rows[sibling], self.rows[sibling])
        self.assertEqual(self.old_profiles["clothing_ct073_v1"], self.profiles["clothing_ct073_v1"])
        old, new = self.old_profiles[VISUAL_KEY], self.profiles[VISUAL_KEY]
        for field in ("id", "category", "activation", "authored_components", "required_evidence_fields",
                      "evidence_requirements", "render_gates", "runtime_expression", "composition_instruction"):
            with self.subTest(field=field):
                self.assertIn(field, old)
                self.assertEqual(old[field], new[field])
        self.assertIs(False, new["activation"]["requires_adult_character"])
        self.assertIs(True, new["activation"]["semantic_discovery_requires_component_evidence"])
        self.assertTrue(new["render_gates"])
        self.assertTrue(all(gate["review_scale"] == "native" for gate in new["render_gates"]))
        for field in ("definition", "claim_limits", "visual_components", "component_semantics"):
            self.assertEqual(old["semantics"][field], new["semantics"][field])
        old_entry, entry = self.old_rows[ORDINARY_KEY][2], self.rows[ORDINARY_KEY][2]
        for field in ("en", "ko", "aliases", "concept_units", "affected_dimensions", "core_assertion_discovery"):
            self.assertEqual(old_entry[field], entry[field])
        self.assertEqual(old_entry["relations"][0]["object"], entry["relations"][0]["object"])
        # The property remains category metadata; no activation/eligibility fix is implied.
        self.assertEqual({"dimension": "appearance", "target": "main_subject",
                          "property": "wardrobe.details.bra_back_band_closure"}, entry["affected_properties"][0])

    def test_maintenance_hashes_lineage_and_historical_pending_wording(self):
        path = ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (MAINTENANCE_ID + ".json")
        raw = path.read_bytes()
        self.assertEqual("fe853a1df4eef3bb63f26ca0a54d62da13d918df9f8b86a6e78393c4c6ff0590", sha(raw))
        record = json.loads(raw)
        self.assertEqual(MAINTENANCE_SHA, canonical_sha(record))
        self.assertEqual({"contract_version": "photo-extension-maintenance-ref/v1",
                          "record_id": record["record_id"], "sha256": canonical_sha(record)},
                         self.current[ORDINARY_SOURCE]["maintenance_ref"])
        authored = {k: v for k, v in self.current[ORDINARY_SOURCE].items() if k != "maintenance_ref"}
        self.assertEqual("29d526bb60b4968d52408fd25ebaf06f9dda63882ad955b51da9179055ddfe56", canonical_sha(authored))
        self.assertEqual(record["authored_source_sha256"], canonical_sha(authored))
        self.assertEqual(self.original[ORDINARY_SOURCE]["maintenance_ref"], record["prior_maintenance_ref"])
        self.assertIn("900bf2efdd17fbc6a6ef3aa340f3526b1e01f223", record["evidence_basis"])
        self.assertEqual("current900_offline_preparation", record["validation_status"]["source_and_projection"])
        for stage in ("new_embeddings", "complete_index_regeneration", "independent_review"):
            self.assertEqual("pending", record["validation_status"][stage])

    def source_texts(self, old=False):
        rows = self.old_rows if old else self.rows
        profiles = self.old_profiles if old else self.profiles
        return {
            "ordinary": {key: pg.semantic_text_for_entry(entry, slot, kind=kind)
                         for key, kind, entry, slot in rows.values()},
            "visual_profile": {key: pg.visual_profile_semantic_text(profile) for key, profile in profiles.items()},
        }

    def test_only_two_embedding_projections_change_and_match_exact_reviewed_inputs(self):
        old_texts, texts = self.source_texts(old=True), self.source_texts()
        for corpus, binding in PROJECTIONS.items():
            with self.subTest(corpus=corpus):
                self.assertEqual([binding["key"]], [k for k in texts[corpus] if texts[corpus][k] != old_texts[corpus][k]])
                text = texts[corpus][binding["key"]]
                self.assertEqual(binding["text"], text)
                self.assertEqual(binding["bytes"], len(text.encode()))
                self.assertEqual(binding["sha256"], sha(text.encode()))
                self.assertEqual(text.encode(), (PRIOR_EVIDENCE / "embeddings" / binding["file"]).read_bytes())

    def test_complete_current_indexes_bind_every_source_text_identity_and_vector_space(self):
        texts = self.source_texts()
        for corpus, index in self.indexes.items():
            with self.subTest(corpus=corpus):
                self.assertEqual(SPACE, {key: index[key] for key in SPACE})
                self.assertEqual(SPACE, {key: self.old_indexes[corpus][key] for key in SPACE})
                self.assertEqual(list(texts[corpus]), list(index["entries"]))
                self.assertEqual({key: value["text"] for key, value in index["entries"].items()}, texts[corpus])
                for key, entry in index["entries"].items():
                    vector = entry["vector"]
                    self.assertEqual(768, len(vector), key)
                    self.assertTrue(all(type(x) in (int, float) and math.isfinite(x) for x in vector), key)
                    self.assertTrue(any(vector), key)
                    if corpus == "visual_profile":
                        self.assertEqual(sha(entry["text"].encode()), entry["text_sha256"], key)
                    else:
                        _, kind, source, slot = self.rows[key]
                        self.assertEqual((kind, slot, source["id"]), (entry["kind"], entry["slot"], entry["id"]), key)
        pg.validate_semantic_index_metadata(self.indexes["ordinary"], self.data)
        pg.validate_semantic_index_metadata(self.old_indexes["ordinary"], self.old_data)
        pg.validate_visual_profile_index_metadata(self.indexes["visual_profile"], self.registry)
        pg.validate_visual_profile_index_metadata(self.old_indexes["visual_profile"], self.old_registry)

    def test_complete_bm25f_documents_statistics_policies_and_exact_lookup(self):
        ordinary = pg.semantic_bm25f_payload_from_index(self.indexes["ordinary"], copy_values=False)
        visual = self.indexes["visual_profile"]["bm25f"]
        self.assertEqual(pg.build_semantic_bm25f_payload(self.data), ordinary)
        self.assertEqual(pg.build_visual_profile_bm25f_payload(self.registry), visual)
        for count, lexical in ((10082, ordinary), (1879, visual)):
            self.assertEqual(count, len(lexical["documents"]))
            lengths = dict.fromkeys(lexical["policy"]["fields"], 0)
            frequencies = {}
            for document in lexical["documents"].values():
                terms = set()
                for field, entry in document["fields"].items():
                    self.assertEqual(sum(entry["term_frequencies"].values()), entry["length"])
                    lengths[field] += entry["length"]
                    terms.update(entry["term_frequencies"])
                for term in terms:
                    frequencies[term] = frequencies.get(term, 0) + 1
            self.assertEqual(frequencies, lexical["document_frequencies"])
            self.assertEqual({key: value / count for key, value in lengths.items()}, lexical["average_field_lengths"])
        exact = []
        for profile in self.profiles.values():
            for field, kind in (("exact_terms", "exact_term"), ("project_glossary_aliases", "project_glossary_alias")):
                for term in profile.get("activation", {}).get(field, []):
                    term = " ".join(str(term or "").split())
                    if term:
                        exact.append({"term": term, "term_key": term.casefold(),
                                      "profile_id": profile["id"], "term_type": kind})
        exact.sort(key=lambda row: (row["term_key"], row["profile_id"], row["term_type"]))
        self.assertEqual(4351, len(exact))
        self.assertEqual(exact, self.indexes["visual_profile"]["exact_lookup"])
        self.assertEqual(exact, self.old_indexes["visual_profile"]["exact_lookup"])
        self.assertEqual(self.old_registry["retrieval_policy"], self.registry["retrieval_policy"])
        self.assertEqual(self.registry["retrieval_policy"], self.indexes["visual_profile"]["retrieval_policy"])

    def test_all_11959_cached_vectors_are_exact_and_two_replacements_match_genuine_receipts(self):
        reused = 0
        for corpus, binding in PROJECTIONS.items():
            entries, old_entries = self.indexes[corpus]["entries"], self.old_indexes[corpus]["entries"]
            self.assertEqual(list(old_entries), list(entries))
            self.assertEqual([binding["key"]], [key for key in entries if entries[key] != old_entries[key]])
            for key, entry in entries.items():
                if key != binding["key"]:
                    self.assertEqual(old_entries[key], entry, key)
                    reused += 1
            receipt_path = PRIOR_EVIDENCE / "embeddings" / ("call-" + binding["slot"]) / "30-verified-receipt.json"
            self.assertEqual(binding["receipt_sha256"], sha(receipt_path.read_bytes()))
            receipt = read(receipt_path)
            response_path = receipt_path.with_name("response.sanitized.json")
            self.assertEqual(receipt["saved_response_sha256"], sha(response_path.read_bytes()))
            response = read(response_path)
            self.assertEqual((corpus, binding["key"], binding["sha256"], binding["bytes"]),
                             (receipt["corpus"], receipt["key"], receipt["input_utf8_sha256"], receipt["input_utf8_bytes"]))
            self.assertEqual(("verified_success", 200, "gemini-embedding-2", 768, "SEMANTIC_SIMILARITY", RECEIPT_COMMIT),
                             (receipt["status"], receipt["http_status"], receipt["model"], receipt["dimensions"],
                              receipt["task_type"], receipt["source_commit"]))
            self.assertEqual([round(float(x), 6) for x in response["embedding"]["values"]], receipt["embedding"])
            self.assertEqual(receipt["embedding"], entries[binding["key"]]["vector"])
            self.assertEqual(binding["vector_sha256"], canonical_sha(receipt["embedding"]))
            self.assertEqual(binding["old_vector_sha256"], canonical_sha(old_entries[binding["key"]]["vector"]))
            self.assertNotEqual(old_entries[binding["key"]]["vector"], receipt["embedding"])
            self.assertIs(False, receipt["raw_response_reproducible_from_saved_bytes"])
        self.assertEqual(11959, reused)
        checkpoint = read(PRIOR_EVIDENCE / "embeddings/ordinary-genuine-vector.checkpoint.json")
        self.assertEqual([ORDINARY_KEY], list(checkpoint["entries"]))
        self.assertEqual(self.indexes["ordinary"]["dictionary_hash"], checkpoint["dictionary_hash"])
        self.assertEqual(self.indexes["ordinary"]["semantic_text_recipe"], checkpoint["semantic_text_recipe"])
        self.assertEqual(SPACE, {key: checkpoint[key] for key in SPACE})
        self.assertEqual(self.indexes["ordinary"]["entries"][ORDINARY_KEY]["vector"], checkpoint["entries"][ORDINARY_KEY]["vector"])
        self.assertEqual(PROJECTIONS["ordinary"]["text"], checkpoint["entries"][ORDINARY_KEY]["text"])

    def test_exact_current_shard_layout_and_predecessor_active_payloads_remain_intact(self):
        for corpus, name, expected_count, changed_bucket, manifest_sha in (
                ("ordinary", ORDINARY_INDEX, 10082, "000",
                 "30561d14ed591dd256b1fb687173201171d55ca88dd7ecd8c76ffc94f953b810"),
                ("visual_profile", VISUAL_INDEX, 1879, "012",
                 "6bc972e5e617de6c4025653c662b3ab142f41714249268fe0a6661b86220f9f4")):
            self.assertEqual(manifest_sha, sha((ASSETS / name).read_bytes()))
            old, new = read(self.parent_assets / name), read(ASSETS / name)
            self.assertEqual(expected_count, new["entry_count"])
            self.assertEqual(old["entry_order"], new["entry_order"])
            self.assertEqual(list(self.indexes[corpus]["entries"]), new["entry_order"])
            self.assertEqual(16, new["storage"]["shard_count"])
            self.assertEqual("sha256", new["storage"]["hash_algorithm"])
            self.assertEqual([f"{i:03d}" for i in range(16)], [row["id"] for row in new["shards"]])
            self.assertEqual([changed_bucket], [row["id"] for row, prior in zip(new["shards"], old["shards"])
                                               if row["sha256"] != prior["sha256"]])
            expected_paths = [f"{i:03d}" for i in range(16)] if corpus == "ordinary" else ["012"]
            self.assertEqual(expected_paths, [row["id"] for row, prior in zip(new["shards"], old["shards"])
                                             if row["path"] != prior["path"]])
            if corpus == "ordinary":
                self.assertTrue(all(Path(row["path"]).parent.name == "0707c32d3c184f15" for row in new["shards"]))
            for row in old["shards"] + new["shards"]:
                self.assertEqual(row["sha256"], sha((ASSETS / row["path"]).read_bytes()), row["path"])

    def test_old_and_new_indexes_reject_the_other_source_hash(self):
        for payload, data in ((self.old_indexes["ordinary"], self.data), (self.indexes["ordinary"], self.old_data)):
            with self.assertRaisesRegex(ValueError, "dictionary_hash"):
                pg.validate_semantic_index_metadata(payload, data)
        for payload, registry in ((self.old_indexes["visual_profile"], self.registry),
                                  (self.indexes["visual_profile"], self.old_registry)):
            with self.assertRaisesRegex(ValueError, "registry_sha256"):
                pg.validate_visual_profile_index_metadata(payload, registry)

    def test_textile_changes_only_two_reference_leaves_to_the_existing_matching_record(self):
        name = "photo_prompt_textile_surface_extension.json"
        before, after = read(self.parent_assets / name), read(ASSETS / name)
        self.assertEqual("5ab096f23d510c7c72163fa3862473c7e890224de45397500658d6380a7b5b57",
                         sha((self.parent_assets / name).read_bytes()))
        self.assertEqual("7047c44cb9013a58102835f529f44a570b61bd7d4f4851b89e86d3d48005ef5a",
                         sha((ASSETS / name).read_bytes()))
        self.assertEqual({
            "/maintenance_ref/record_id": (
                "photo_prompt_textile_surface_extension-vocaloid-equivalents-20261004",
                "photo_prompt_textile_surface_extension-vocaloid-main-merge-20261004"),
            "/maintenance_ref/sha256": (
                "5a2404637db39da191f543b9709db000543a9c617da0a3d7b68383d378fcfc90",
                "2c0e49831e8287fc8aa5290c455e6be3195deb4dcdd67c9fd3295dfeac5eeb65"),
        }, leaf_delta(before, after))
        authored = {key: value for key, value in after.items() if key != "maintenance_ref"}
        self.assertEqual(authored, {key: value for key, value in before.items() if key != "maintenance_ref"})
        self.assertEqual("8d279023481b6569dc35437889fe744efee574e2fe3d37e7574236a148147b54", canonical_sha(authored))
        record_path = ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (
            "photo_prompt_textile_surface_extension-vocaloid-main-merge-20261004.json")
        self.assertEqual("7d8933f1db6a61eaea1aa79bc01f8063ef2c64b6c4b7bd496bb71552fb9d465a", sha(record_path.read_bytes()))
        record = read(record_path)
        self.assertEqual(after["maintenance_ref"]["sha256"], canonical_sha(record))
        self.assertEqual(after["maintenance_ref"]["record_id"], record["record_id"])
        self.assertEqual(canonical_sha(authored), record["authored_source_sha256"])
        for index, identity in ((24, "clt_ct091_v1"), (25, "clt_ct091_v2")):
            self.assertEqual(identity, after["slots"]["surface_material"][index]["id"])
            self.assertEqual(before["slots"]["surface_material"][index], after["slots"]["surface_material"][index])

    def test_textile_reference_repair_changes_no_complete_compiled_object_or_index_binding(self):
        path = ASSETS / "photo_prompt_textile_surface_extension.json"
        old_ref = read(self.parent_assets / path.name)["maintenance_ref"]
        uncorrected = read(path)
        uncorrected["maintenance_ref"] = old_ref
        original_load = json.load

        def original_reference(stream, *args, **kwargs):
            value = original_load(stream, *args, **kwargs)
            return copy.deepcopy(uncorrected) if Path(str(getattr(stream, "name", ""))) == path else value

        with mock.patch.object(json, "load", side_effect=original_reference):
            old_reference_data = pg.load_json(ASSETS / "photo_prompt_tags.json")
            old_reference_registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        self.assertEqual(self.data, old_reference_data)
        self.assertEqual(self.registry, old_reference_registry)
        self.assertEqual(pg.dictionary_hash(self.data), pg.dictionary_hash(old_reference_data))
        self.assertEqual(canonical_sha(self.registry), canonical_sha(old_reference_registry))
        pg.validate_semantic_index_metadata(self.indexes["ordinary"], old_reference_data)
        pg.validate_visual_profile_index_metadata(self.indexes["visual_profile"], old_reference_registry)


if __name__ == "__main__":
    unittest.main()
