"""Version-safe paraphrases must preserve owned morphology and optionality."""
from __future__ import annotations
import copy
import json
import re
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/"skills/photo-prompt-image-generator"
ASSETS=SKILL/"assets"
RUN=ROOT/"docs/research-evidence/photo-prompt/harry-potter-integration-20261006"
sys.path.insert(0,str(SKILL/"scripts"))
import prompt_generator as pg
import photo_contracts as contracts
from visual_profile_contracts import compile_visual_profile


class HarryAppearanceSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=pg.load_visual_obligation_registry(ASSETS/"photo_prompt_visual_obligations.json")
        cls.profiles={p["id"]:p for p in cls.registry["profiles"]}
        cls.receipt=json.loads((RUN/"ADOPTION-MANIFEST.json").read_text())
        cls.new_ids={r["profile_id"] for r in cls.receipt["new_units"]}
        cls.thin=dict(cls.registry,profiles=[cls.profiles[p] for p in sorted(cls.new_ids)])
        cls.index=pg.build_visual_profile_index_payload(cls.thin)
        cls.data=pg.load_json(ASSETS/"photo_prompt_tags.json")

    def hard(self,text,source="user_requirement",polarity="required"):
        result=pg.resolve_visual_profile_hits(self.thin,[{"source":source,"polarity":polarity,"text":text}],
                                              visual_profile_index=self.index,adult_context=True)
        return {h["profile_id"] for h in result["hits"] if h["hard_eligible"]}

    def test_existing_activation_and_pixel_duties_are_preserved(self):
        for row in self.receipt["existing_profile_updates"]:
            source=RUN/"before/skills/photo-prompt-image-generator/assets"/row["file"]
            old=next(p for p in json.loads(source.read_text())["profiles"] if p["id"]==row["id"])
            old=compile_visual_profile(old);new=self.profiles[row["id"]]
            with self.subTest(profile=row["id"]):
                for field in ["activation","render_gates","required_evidence_fields","composition_instruction"]:
                    self.assertEqual(old[field],new[field])
                for field in ["definition","visual_components","claim_limits","contrast_examples"]:
                    self.assertEqual(old["semantics"].get(field),new["semantics"].get(field))
                for field in ["affected_dimensions","affected_properties","core_assertion_discovery"]:
                    self.assertEqual(old.get("concept_candidate",{}).get(field),new.get("concept_candidate",{}).get(field))
                groups=old["semantics"]["component_semantics"]
                current=new["semantics"]["component_semantics"]
                self.assertEqual(groups["minimum_component_groups"],current["minimum_component_groups"])
                self.assertEqual(groups["required_group_ids"],current["required_group_ids"])
                for field,req in old["evidence_requirements"].items():
                    self.assertEqual(req["min_content_words"],new["evidence_requirements"][field]["min_content_words"])
                    self.assertTrue(set(req["must_mention_any"])<=set(new["evidence_requirements"][field]["must_mention_any"]))

    def test_complete_english_and_korean_components_and_each_omission(self):
        for pid in self.new_ids:
            profile=self.profiles[pid]
            groups=profile["semantics"]["component_semantics"]["groups"]
            for language in range(2):
                phrases=[g["any_terms"][language] for g in groups]
                with self.subTest(profile=pid,language=language):
                    self.assertEqual(pg.candidate_pack_visual_component_match(profile,"; ".join(phrases)),"component_semantics")
                for omitted in range(3):
                    with self.subTest(profile=pid,language=language,omitted=omitted):
                        self.assertIsNone(pg.candidate_pack_visual_component_match(profile,"; ".join(v for i,v in enumerate(phrases) if i!=omitted)))

    def test_authorial_candidates_negation_and_names_never_harden(self):
        for pid in self.new_ids:
            text=self.profiles[pid]["activation"]["exact_terms"][0]
            with self.subTest(profile=pid):
                self.assertIn(pid,self.hard(text))
                self.assertNotIn(pid,self.hard(text,source="authorial_core_interpretation",polarity="advisory"))
                self.assertNotIn(pid,self.hard(text,polarity="excluded"))
                self.assertNotIn(pid,self.hard("Do not add "+text))
        for name in ["Harry Potter","Hermione","Draco Malfoy","Hogwarts","해리포터","말포이","TS","악역영애"]:
            self.assertFalse(self.hard(name),name)

    def test_neighbor_carriers_and_visually_different_forms_do_not_complete(self):
        negatives={
          "appearance_rel_h002":"A robe has a printed shirt and necktie graphic; a second person wears the knit top.",
          "appearance_rel_h003":"A colored scarf lies next to the hood and blue lighting illuminates a black cap.",
          "appearance_rel_h028":"Two live birds stand beside a heart sticker on a different person's sleeve.",
          "appearance_rel_h043":"Dark eyeliner and a bright collar surround uniformly pale hair.",
          "appearance_rel_h058":"Two scar paths intersect on the cheek; a painted lightning design lies on the sleeve.",
          "appearance_rel_h061":"An eyewear lens is tinted blue in front of an ordinary iris.",
          "appearance_rel_h063":"A metallic glove covers an intact hand beside a detached model hand.",
          "appearance_rel_h065":"A skull is in the sky while a serpent print appears on a sleeve.",
          "appearance_rel_h075":"A dark hood shadow covers the eyes and two earrings flank the head.",
          "appearance_rel_h077":"A ring necklace lies in front of a large hourglass standing on the table.",
          "appearance_rel_h082":"A lion-face mask encloses the person's face rather than resting above the head.",
          "appearance_rel_h087":"A looped hair curl casts a crescent shadow beside a necklace ring.",
        }
        for pid,text in negatives.items():
            with self.subTest(profile=pid):
                self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles[pid],text))
                self.assertNotIn(pid,self.hard(text))

    def test_slot_candidate_equivalents_preserve_original_fields_and_guards(self):
        source=json.loads((ASSETS/"photo_prompt_character_appearance_extension.json").read_text())
        for slot,updates in source["existing_slot_context_extensions"].items():
            merged={r["id"]:r for r in self.data["slots"][slot]}
            for eid,addition in updates.items():
                old=None
                for path in (RUN/"before/skills/photo-prompt-image-generator/assets").glob("*.json"):
                    old=next((r for r in json.loads(path.read_text()).get("slots",{}).get(slot,[]) if r["id"]==eid),old)
                self.assertIsNotNone(old,eid)
                with self.subTest(candidate=eid):
                    for field in ["ko","en","for_any","requires_primary_any_tags","affected_dimensions","affected_properties","weight"]:
                        self.assertEqual(old.get(field),merged[eid].get(field))
                    self.assertTrue(set(addition["paraphrases"])<=set(merged[eid]["paraphrases"]))

    def test_bundle_components_remain_all_of_and_profile_activation_is_independent(self):
        ids={"appearance_same_wearer_uniform","appearance_quilted_duelling_layers","appearance_bird_motif_and_star_ornament",
             "appearance_mask_incisions","appearance_hourglass_and_hoop","appearance_two_region_hair_and_ribbon"}
        bundles=[b for b in self.data["candidate_bundles"] if b["id"] in ids]
        self.assertEqual(len(bundles),6)
        for b in bundles:
            with self.subTest(bundle=b["id"]):
                self.assertEqual(b["adoption"],"optional")
                self.assertEqual(b["profile_activation"],"independent_request_evidence_only")
                self.assertEqual(len(b["components"]),3*len(b["member_candidates"]))
                self.assertTrue(all(len(c["concept_units"])==c["minimum_realizations"]==1 for c in b["components"]))

    def test_actual_property_effects_respect_partial_locks(self):
        source=json.loads((ASSETS/"photo_prompt_character_appearance_extension.json").read_text())
        for slot,rows in source["slots"].items():
            for row in rows:
                for effect in row["affected_properties"]:
                    lock={"contract_version":"photo-intent-lock/v2","semantic_anchors":[{"dimension":effect["dimension"],"target":effect["target"],"property":effect["property"],"prompt_evidence":"fixed reference detail"}],
                          "open_dimensions":row["affected_dimensions"],"locked_dimensions":[]}
                    with self.subTest(candidate=row["id"],property=effect["property"]):
                        self.assertFalse(contracts.property_effects_allowed(lock,row["affected_dimensions"],row["affected_properties"]))

    def test_positive_projection_excludes_character_case_metadata_and_confusions(self):
        banned=re.compile(r"https?://|\bS\d{2}\b|\bH\d{3}\b|Harry|Hogwarts|Malfoy|Hermione|판본|source lead|RESEARCH_DRAFT",re.I)
        for pid in self.new_ids:
            p=self.profiles[pid]
            positive=pg.visual_profile_semantic_text(p)
            self.assertIsNone(banned.search(positive),pid)
            for boundary in p["reject_substitutes"]:
                self.assertNotIn(boundary,positive)
        # Carrier-distinct legacy definitions remain intact.
        self.assertIn("tail",self.profiles["ca_bushy_tail"]["semantics"]["definition"])
        self.assertIn("nonhuman",self.profiles["ca_coiled_head_elements"]["semantics"]["definition"])
        self.assertIn("adult",self.profiles["bm_prosthetic_connection"]["semantics"]["definition"])

    def test_optional_profile_registration_keeps_full_index_binding_fail_closed(self):
        manifest=json.loads((ASSETS/"photo_prompt_source_manifest.json").read_text())
        profile_file="photo_prompt_visual_obligations_appearance_relations.json"
        profile_row=next(row for row in manifest["sources"] if row["file"]==profile_file)
        candidate_row=next(row for row in manifest["sources"] if row["file"]=="photo_prompt_character_appearance_extension.json")
        self.assertFalse(profile_row["required"])
        self.assertTrue(candidate_row["required"])
        missing=ASSETS/profile_file
        original_exists=Path.exists
        def without_new_profile(path):
            return False if path==missing else original_exists(path)
        with patch.object(Path,"exists",without_new_profile):
            incomplete=pg.load_visual_obligation_registry(ASSETS/"photo_prompt_visual_obligations.json")
        self.assertEqual(len(incomplete["profiles"]),len(self.registry["profiles"])-42)
        with self.assertRaisesRegex(ValueError,"registry_sha256"):
            pg.load_visual_profile_index(ASSETS/"photo_prompt_visual_profile_index.json",incomplete)


if __name__=="__main__":unittest.main()
