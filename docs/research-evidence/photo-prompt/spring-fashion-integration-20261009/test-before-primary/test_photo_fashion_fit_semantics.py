"""Fit means an owned garment relation; labels, alternatives and measurements differ."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"skills/photo-prompt-image-generator/assets"
sys.path.insert(0,str(ASSETS.parent/"scripts"))
import prompt_generator as pg
import photo_candidate_semantics as cs
from photo_contracts import property_effects_allowed


class FashionFitSemanticsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=pg.load_json(ASSETS/"photo_prompt_tags.json")
  cls.full_registry=pg.load_visual_obligation_registry(ASSETS/"photo_prompt_visual_obligations.json")
  cls.profiles={p["id"]:p for p in cls.full_registry["profiles"] if p["id"].startswith("fit_ff")}
  cls.registry={**cls.full_registry,"profiles":list(cls.profiles.values())}
  cls.index=pg.build_visual_profile_index_payload(cls.registry)
  cls.extension=json.loads((ASSETS/"photo_prompt_fashion_fit_extension.json").read_text())
  cls.entries={r["id"]:(s,r) for s,rows in cls.extension["slots"].items() for r in rows}

 def hard(self,text,source="concept_lock",polarity="required"):
  result=pg.resolve_visual_profile_hits(self.registry,
    [{"source":source,"text":text,"polarity":polarity,"priority":"critical","mandatory":polarity=="required"}],
    visual_profile_index=self.index,adult_context=True)
  return {r["profile_id"] for r in result["hits"] if r.get("hard_eligible")}

 def test_complete_selected_variant_activates_without_sibling(self):
  for pid,p in self.profiles.items():
   with self.subTest(profile=pid):
    self.assertEqual(self.hard(p["activation"]["exact_terms"][0]),{pid})

 def test_labels_homonyms_measurements_and_negation_never_harden(self):
  for text in ["curvy fit","athletic fit","negative ease","30 percent stretch","compression fit",
     "mermaid","a mermaid character underwater","princess","darting eyes","tapered eyeliner",
     "a relaxed expression","trouser break","Wedgie jeans","lantern sleeve","plus size","comfort fit",
     "racerback","cross-back","a fully canvassed jacket","shirt softness proves its fiber blend"]:
   with self.subTest(text=text): self.assertEqual(self.hard(text),set())
  for p in self.profiles.values():
   with self.subTest(negation=p["id"]):
    self.assertNotIn(p["id"],self.hard("not "+p["activation"]["exact_terms"][0]))

 def test_advisory_baseline_is_not_requester_hard_activation(self):
  for p in self.profiles.values():
   text=p["activation"]["exact_terms"][0]
   with self.subTest(profile=p["id"]):
    self.assertNotIn(p["id"],self.hard(text,"authorial_core_interpretation","advisory"))

 def test_partial_components_cannot_establish_complete_selected_relation(self):
  for pid in ["fit_ff01_v1","fit_ff05_v1","fit_ff09_v1","fit_ff24_v1","fit_ff42_v1","fit_ff52_v1","fit_ff52_v2","fit_ff62_v3"]:
   p=self.profiles[pid]
   parts=[c["evidence_terms"][0] for c in p["authored_components"]["components"]]
   self.assertEqual(pg.candidate_pack_visual_component_match(p,"; ".join(parts)),"component_semantics")
   for omitted in range(len(parts)):
    partial="; ".join(x for i,x in enumerate(parts) if i!=omitted)
    with self.subTest(profile=pid,omitted=omitted):
     self.assertIsNone(pg.candidate_pack_visual_component_match(p,partial))

 def test_partial_property_locks_protect_actual_fit_axes(self):
  for cid,prop in [
    ("fit_ff05_v1_candidate","wardrobe.fit.waist_to_hip_distribution"),
    ("fit_ff09_v1_candidate","wardrobe.fit.shoulder.seam_position"),
    ("fit_ff24_v1_candidate","wardrobe.silhouette.knee_to_hem_width"),
    ("fit_ff33_v1_candidate","wardrobe.structure.front_fastener_state"),
    ("fit_ff52_v2_candidate","wardrobe.structure.back_strap_connection"),
    ("fit_ff62_v3_candidate","wardrobe.structure.strap_fastener")]:
   slot,e=self.entries[cid]
   semantic=cs.semantic_source(e,slot,self.data["candidate_semantic_policy"])
   lock={"contract_version":"photo-intent-lock/v2","semantic_anchors":[
     {"dimension":"appearance","target":"main_subject","property":prop}]}
   with self.subTest(candidate=cid):
    self.assertFalse(property_effects_allowed(lock,semantic["affected_dimensions"],semantic["affected_properties"]))
    lock["semantic_anchors"][0]["property"]="wardrobe.color"
    self.assertTrue(property_effects_allowed(lock,semantic["affected_dimensions"],semantic["affected_properties"]))
    lock["semantic_anchors"][0]["property"]="wardrobe"
    self.assertFalse(property_effects_allowed(lock,semantic["affected_dimensions"],semantic["affected_properties"]))

 def test_same_owner_effects_do_not_rewrite_body_or_infer_hidden_performance(self):
  for cid,(slot,e) in self.entries.items():
   with self.subTest(candidate=cid):
    self.assertNotIn("body_geometry",e["affected_dimensions"])
    self.assertNotIn("identity",e["affected_dimensions"])
    self.assertTrue(e["relations"])
    self.assertTrue(all(r["target"]=="main_subject" and r["property"].startswith(("wardrobe.","posture."))
                        for r in e["affected_properties"]))
    self.assertNotIn("<bound_garment_id>",json.dumps(e))
    self.assertFalse(any("_or_" in r["type"] for r in e["relations"]))
    self.assertNotIn("http",json.dumps(e).lower())
  curvy=self.entries["fit_ff05_v1_candidate"][1]
  self.assertIn("same trousers",curvy["relations"][0]["object"])
  x=self.entries["fit_ff52_v2_candidate"][1];y=self.entries["fit_ff52_v1_candidate"][1]
  self.assertNotEqual(x["relations"][0]["type"],y["relations"][0]["type"])
  self.assertNotEqual(x["relations"][0]["object"],y["relations"][0]["object"])

 def test_material_and_pose_prerequisites_cannot_bypass_their_locked_axes(self):
  for cid,dimension,prop in [
    ("fit_ff49_v1_candidate","material","wardrobe.material.transmission"),
    ("fit_ff38_v2_candidate","material","wardrobe.material.drape"),
    ("fit_ff12_v1_candidate","pose","posture.arm_elevation"),
    ("fit_ff54_v2_candidate","pose","posture.seated")]:
   slot,e=self.entries[cid]
   semantic=cs.semantic_source(e,slot,self.data["candidate_semantic_policy"])
   lock={"contract_version":"photo-intent-lock/v2","semantic_anchors":[
      {"dimension":dimension,"target":"main_subject","property":prop}]}
   with self.subTest(candidate=cid):
    self.assertIn(dimension,semantic["affected_dimensions"])
    self.assertFalse(property_effects_allowed(lock,semantic["affected_dimensions"],semantic["affected_properties"]))

 def test_bundles_are_optional_and_not_alternative_all_of(self):
  selected=[b for b in self.data["candidate_bundles"] if b["id"].startswith("fit_ff")]
  self.assertEqual(len(selected),len(self.entries))
  for b in selected:
   with self.subTest(bundle=b["id"]):
    self.assertEqual(b["adoption"],"optional")
    self.assertEqual(b["profile_activation"],"independent_request_evidence_only")
    self.assertEqual(len(b["associated_profile_ids"]),1)
    self.assertEqual(len(b["member_candidates"]),1)
  highleg=self.profiles["fit_ff48_v1"]["concept_candidate"]["affected_properties"]
  highwaist=self.profiles["fit_ff23_v1"]["concept_candidate"]["affected_properties"]
  self.assertNotEqual(highleg,highwaist)
  self.assertEqual(highleg[0]["property"],"wardrobe.coverage.leg_opening")
  self.assertEqual(highwaist[0]["property"],"wardrobe.fit.waistband_landmark")

 def test_authored_compiler_and_maintenance_bindings_are_complete(self):
  source=json.loads((ASSETS/"photo_prompt_visual_obligations_fashion_fit.json").read_text())
  for raw in source["profiles"]:
   compiled=self.profiles[raw["id"]]
   components=raw["authored_components"]["components"]
   with self.subTest(profile=raw["id"]):
    self.assertEqual(compiled["semantics"]["component_semantics"]["minimum_component_groups"],len(components))
    self.assertEqual(len(compiled["render_gates"]),len(components))
    self.assertEqual(compiled["required_evidence_fields"],[c["evidence_field"] for c in components])
    self.assertTrue(all(g["review_scale"]=="native" for g in compiled["render_gates"]))
  ext=copy.deepcopy(self.extension);ref=ext.pop("maintenance_ref")
  record=json.loads((ROOT/"docs/research-evidence/photo-prompt/extension-maintenance"/(ref["record_id"]+".json")).read_text())
  self.assertEqual(cs.digest(record),ref["sha256"])
  self.assertEqual(cs.digest(ext),record["authored_source_sha256"])

 def test_real_indexes_include_variants_and_reject_stale_registry(self):
  semantic=pg.load_semantic_index_payload(ASSETS/"photo_prompt_semantic_index.json")
  pg.validate_semantic_index_metadata(semantic,self.data)
  visual=pg.load_visual_profile_index(ASSETS/"photo_prompt_visual_profile_index.json",self.full_registry)
  self.assertTrue(set(self.profiles)<=set(visual["entries"]))
  self.assertTrue({f"slot:{s}:{cid}" for cid,(s,e) in self.entries.items()}<=set(semantic["entries"]))
  stale=copy.deepcopy(visual);stale["registry_sha256"]="0"*64
  with self.assertRaisesRegex(ValueError,"registry_sha256"):pg.validate_visual_profile_index_metadata(stale,self.full_registry)


if __name__=="__main__":unittest.main()
