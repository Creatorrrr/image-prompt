"""Model/editorial contracts: narrow activation, evidence ownership and guarded adoption."""
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/"skills/photo-prompt-image-generator"
sys.path.insert(0,str(SKILL/"scripts"))
import prompt_generator as pg
import photo_candidate_semantics as cs
from visual_profile_contracts import compile_visual_profile

class ModelEditorialTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ext=json.loads((SKILL/"assets/photo_prompt_model_editorial_extension.json").read_text())
  raw=pg.load_visual_obligation_registry(SKILL/"assets/photo_prompt_visual_obligations.json")
  cls.registry={**raw,"profiles":[p for p in raw["profiles"] if p["id"].startswith("mep_")]}
  cls.profiles={p["id"]:p for p in cls.registry["profiles"]}
  cls.index=pg.build_visual_profile_index_payload(cls.registry)
  cls.data=pg.load_json(SKILL/"assets/photo_prompt_tags.json")
 def hard(self,text,adult=True):
  r=pg.resolve_visual_profile_hits(self.registry,[{"source":"concept_lock","text":text,
   "polarity":"required","priority":"critical","mandatory":True}],visual_profile_index=self.index,adult_context=adult)
  return {h["profile_id"] for h in r["hits"] if h.get("match_basis")=="exact" and h.get("hard_eligible")}
 def test_full_owner_relation_only_and_negation(self):
  for p in self.profiles.values():
   text=p["activation"]["exact_terms"][0]
   with self.subTest(profile=p["id"]):
    self.assertEqual(self.hard(text),{p["id"]})
    self.assertNotIn(p["id"],self.hard("not "+text))
    for c in p["authored_components"]["components"]:
     self.assertNotIn(p["id"],self.hard(c["evidence_terms"][0]))
 def test_broad_career_genre_and_nearby_visual_substitutes_do_not_harden(self):
  cases=["professional model","agency model","fashion editorial","beauty editorial","model digitals",
   "test shoot","lookbook","magazine cover","print-ready","published model","global campaign",
   "Micro-expression","fitness model","S-curve road composition",
   "에디토리얼 모델","전문적인 촬영","파란 배경과 검은 아이라이너",
   "hands covering the jacket buttons","plastic skin with sharp knit background",
   "광점만 있고 반지 윤곽이 없다"]
  for q in cases:
   with self.subTest(query=q):self.assertEqual(self.hard(q),set())
 def test_guarded_nonadult_context_does_not_gain_hard_human_profile(self):
  for p in self.profiles.values():
   self.assertEqual(self.hard(p["activation"]["exact_terms"][0],adult=False),set())
 def test_selected_contract_keeps_every_owner_component_and_rejects_duplicate_evidence(self):
  for p in self.profiles.values():
   with self.subTest(profile=p["id"]):
    compiled=compile_visual_profile(p)
    self.assertEqual(len(compiled["required_evidence_fields"]),3)
    self.assertEqual(len(compiled["render_gates"]),3)
    for c in p["authored_components"]["components"]:
     self.assertIn(c["render_gate"]["id"],{g["id"] for g in compiled["render_gates"]})
    bad=copy.deepcopy(p)
    bad["authored_components"]["components"][1]["evidence_field"]=bad["authored_components"]["components"][0]["evidence_field"]
    with self.assertRaises(ValueError):compile_visual_profile(bad)
 def test_bundles_reject_missing_or_locked_members_and_never_promote_associated_profiles(self):
  for b in [b for b in self.data["candidate_bundles"] if b["id"].startswith("mep_")]:
   with self.subTest(bundle=b["id"]):
    self.assertEqual(b["profile_activation"],"independent_request_evidence_only")
    slots={};dims=set()
    for m in b["member_candidates"]:
     dims.update(m["affected_dimensions"])
     slots.setdefault(m["slot"],{"candidates":[]})["candidates"].append({"id":m["id"],"applicability":{"status":"eligible"}})
    pack={"slots":slots,"authorial_core":{"intent_lock":{"open_dimensions":list(dims)}}}
    data={**self.data,"candidate_bundles":[b]}
    self.assertEqual(len(cs.public_bundles(data,pack)["candidates"]),1)
    missing=copy.deepcopy(pack);next(iter(missing["slots"].values()))["candidates"].clear()
    self.assertEqual(cs.public_bundles(data,missing)["candidates"],[])
    for d in dims:
     closed=copy.deepcopy(pack);closed["authorial_core"]["intent_lock"]["open_dimensions"].remove(d)
     self.assertEqual(cs.public_bundles(data,closed)["candidates"],[])
 def test_bts_context_guards_do_not_leak_into_finished_portraits(self):
  for slot,entries in self.ext["slots"].items():
   for e in entries:
    if e["id"] in {"mep_tether_review_candidate","mep_fitting_adjustment_candidate"}:
     self.assertFalse(pg.compatible_with_slot_context(slot,e,{"subject":{"id":"adult_model","tags":["human","adult","fashion"]}},self.data))
     self.assertTrue(pg.compatible_with_slot_context(slot,e,{"subject":{"id":"adult_model","tags":["human","adult","production_activity"]}},self.data))
 def test_series_layout_and_provenance_stay_outside_single_image_runtime(self):
  ref=self.ext["maintenance_ref"]
  record=json.loads((ROOT/"docs/research-evidence/photo-prompt/extension-maintenance"/(ref["record_id"]+".json")).read_text())
  self.assertEqual(ref["sha256"],cs.digest(record))
  raw=copy.deepcopy(self.ext);raw.pop("maintenance_ref")
  self.assertEqual(record["authored_source_sha256"],cs.digest(raw))
  deferred={p["id"] for p in record["maintenance_only"]["deferred_proposals"]}
  self.assertEqual(deferred,{"mep_spread_gutter","mep_series_lookbook","mep_series_story"})
  self.assertFalse(deferred & set(self.profiles))
  for entries in self.ext["slots"].values():
   for e in entries:
    self.assertNotIn("http",e["embedding_text"])
    self.assertNotIn("identity",e["affected_dimensions"])
    self.assertNotIn("role",e["affected_dimensions"])
 def test_broad_catalog_is_not_a_paraphrase_of_garment_side_depth(self):
  registry={**self.registry,"profiles":[self.profiles["mep_garment_side_depth"]]}
  for text in ["An apparel catalog close-up shows an underarm gusset and reinforced seam",
               "a furniture catalog", "a lookbook overview", "garment-aware styling"]:
   with self.subTest(text=text):
    rows=[{"source":"concept_lock","text":text,"polarity":"required","priority":"critical","mandatory":True}]
    self.assertNotIn("mep_garment_side_depth",pg.candidate_pack_auto_visual_concept_matches(registry,rows))
  rows=[{"source":"concept_lock","text":"side seam detail","polarity":"required"}]
  self.assertIn("mep_garment_side_depth",pg.candidate_pack_auto_visual_concept_matches(registry,rows))
 def test_real_indexes_cover_the_new_source(self):
  si=pg.load_semantic_index_payload(SKILL/"assets/photo_prompt_semantic_index.json")
  pg.validate_semantic_index_metadata(si,self.data)
  expected={f"slot:{slot}:{e['id']}" for slot,entries in self.ext["slots"].items() for e in entries}
  self.assertTrue(expected <= set(si["entries"]))
  registry=pg.load_visual_obligation_registry(SKILL/"assets/photo_prompt_visual_obligations.json")
  vi=json.loads((SKILL/"assets/photo_prompt_visual_profile_index.json").read_text())
  pg.validate_visual_profile_index_metadata(vi,registry)
if __name__=="__main__":unittest.main()

