"""Garment labels, selected topology, visible layers and specifications differ."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(ASSETS.parent/'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as cs
from photo_contracts import property_effects_allowed

class AutumnFashionSemanticsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=pg.load_json(ASSETS/'photo_prompt_tags.json')
  cls.full=pg.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
  cls.profiles={p['id']:p for p in cls.full['profiles'] if p['id'].startswith('autumn_afr')}
  cls.registry={**cls.full,'profiles':list(cls.profiles.values())}
  cls.index=pg.build_visual_profile_index_payload(cls.registry)
  cls.extension=json.loads((ASSETS/'photo_prompt_autumn_fashion_extension.json').read_text())
  cls.entries={e['id']:(s,e) for s,rows in cls.extension['slots'].items() for e in rows}

 def hard(self,text,source='concept_lock',polarity='required',adult=True):
  result=pg.resolve_visual_profile_hits(self.registry,[{'source':source,'text':text,'polarity':polarity,'priority':'critical','mandatory':polarity=='required'}],visual_profile_index=self.index,adult_context=adult)
  return {r['profile_id'] for r in result['hits'] if r.get('hard_eligible')}

 def test_exact_selected_clause_activates_only_its_own_variant(self):
  self.assertEqual(len(self.profiles),112)
  for pid,p in self.profiles.items():
   with self.subTest(pid=pid):self.assertEqual(self.hard(p['activation']['exact_terms'][0]),{pid})

 def test_family_label_or_hidden_specification_never_hardens(self):
  for term in ['twinset','pointelle','one-button cardigan','no pants look','old money','quiet luxury','cashmere','100 percent mohair','20 DEN','silk fiber','bias cut','Fair Isle technique','intarsia manufacturing','shearling leather','off-shoulder','drop shoulder','underbust corset','navel-baring','cold-shoulder','Balmacaan coat','Harrington jacket','a bubble tea']:
   with self.subTest(term=term):self.assertEqual(self.hard(term),set())

 def test_negation_and_advisory_discovery_are_not_requester_duties(self):
  for pid,p in self.profiles.items():
   text=p['activation']['exact_terms'][0]
   with self.subTest(pid=pid):
    self.assertNotIn(pid,self.hard('not '+text))
    self.assertNotIn(pid,self.hard(text,'authorial_core_interpretation','advisory'))

 def test_embedding_paraphrases_are_optional_even_with_perfect_similarity(self):
  ids=list(self.profiles);size=len(ids)
  vectors={pid:[float(i==j) for j in range(size)] for i,pid in enumerate(ids)}
  index=pg.build_visual_profile_index_payload(self.registry,vectors=vectors,dimensions=size)
  # Controlled vectors exercise the embedding lane. This is not a claim that
  # a live provider assigns these similarities or that the image used this lane.
  for i,pid in enumerate(ids):
   text=self.profiles[pid]['semantics']['paraphrase_examples'][0]
   result=pg.resolve_visual_profile_hits(self.registry,[{'source':'authorial_core_interpretation','text':text,'polarity':'advisory'}],
      visual_profile_index=index,query_vector=vectors[pid],adult_context=True)
   hit=next(r for r in result['hits'] if r['profile_id']==pid)
   with self.subTest(pid=pid):
    self.assertEqual(hit['match_basis'],'embedding')
    self.assertFalse(hit['hard_eligible']);self.assertTrue(hit['optional_eligible'])

 def test_relations_cannot_be_completed_by_one_partial_endpoint(self):
  for pid in ['autumn_afr087_v1','autumn_afr107_v1','autumn_afr110_v1']:
   p=self.profiles[pid];parts=[c['evidence_terms'][0] for c in p['authored_components']['components']]
   self.assertEqual(pg.candidate_pack_visual_component_match(p,'; '.join(parts)),'component_semantics')
   for part in parts:
    with self.subTest(pid=pid,partial=part):self.assertIsNone(pg.candidate_pack_visual_component_match(p,part))

 def test_sheer_cutout_eyelet_and_hidden_bottom_are_separate(self):
  sheer=self.profiles['autumn_afr108_v1']['semantics']['definition']
  pointelle=self.profiles['autumn_afr079_v1']['semantics']['definition']
  cutout=self.profiles['autumn_afr050_v1']['semantics']['definition']
  bottom=self.profiles['autumn_afr110_v1']['semantics']['definition']
  self.assertEqual(self.hard(sheer),{'autumn_afr108_v1'})
  self.assertEqual(self.hard(pointelle),{'autumn_afr079_v1'})
  self.assertEqual(self.hard(cutout),{'autumn_afr050_v1'})
  self.assertEqual(self.hard(bottom),{'autumn_afr110_v1'})
  for false in ["a printed camisole neckline on an opaque blouse","an open cardigan above invisible shorts","a crochet pattern printed on a solid cardigan","a sheer-looking highlight without a readable underlayer"]:
   self.assertEqual(self.hard(false),set())
  self.assertIn('separate',bottom);self.assertIn('visible',bottom)

 def test_variant_effects_preserve_each_owned_property_lock(self):
  for cid,(slot,e) in self.entries.items():
   semantic=cs.semantic_source(e,slot,self.data['candidate_semantic_policy'])
   for prop in e['affected_properties']:
    lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[prop]}
    with self.subTest(candidate=cid,property=prop):
     self.assertFalse(property_effects_allowed(lock,semantic['affected_dimensions'],semantic['affected_properties']))
   lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'appearance','target':'main_subject','property':'hair.style'}]}
   self.assertTrue(property_effects_allowed(lock,semantic['affected_dimensions'],semantic['affected_properties']))

 def test_material_color_and_pose_prerequisites_have_complete_effects(self):
  for cid,dimension,prop in [
   ('autumn_afr108_v1_candidate','material','wardrobe.material.transmission'),
   ('autumn_afr079_v1_candidate','material','wardrobe.material.visible_weave'),
   ('autumn_afr028_v1_candidate','appearance','wardrobe.color'),
   ('autumn_afr087_v1_candidate','pose','posture.thumb_cuff_contact'),
   ('autumn_afr107_v1_candidate','appearance','wardrobe.structure.front_fastener_state'),
   ('autumn_afr110_v1_candidate','appearance','wardrobe.structure.visible_shorts')]:
   _,e=self.entries[cid]
   with self.subTest(cid=cid):self.assertIn({'dimension':dimension,'target':'main_subject','property':prop},e['affected_properties'])
  for _,e in self.entries.values():
   self.assertNotIn('body_geometry',e['affected_dimensions']);self.assertNotIn('identity',e['affected_dimensions'])
   self.assertTrue(e['relations']);self.assertTrue(all(p['target']=='main_subject' for p in e['affected_properties']))
   self.assertNotIn('http',json.dumps(e).lower());self.assertNotIn('<bound',json.dumps(e))

 def test_sibling_neckline_pleat_and_surface_choices_are_independent(self):
  for a,b in [('autumn_afr034_v1','autumn_afr034_v2'),('autumn_afr037_v1','autumn_afr037_v2'),('autumn_afr061_v1','autumn_afr061_v2'),('autumn_afr069_v1','autumn_afr069_v2'),('autumn_afr083_v1','autumn_afr083_v2'),('autumn_afr098_v1','autumn_afr098_v2')]:
   with self.subTest(a=a,b=b):
    self.assertEqual(self.hard(self.profiles[a]['semantics']['definition']),{a})
    self.assertEqual(self.hard(self.profiles[b]['semantics']['definition']),{b})

 def test_adult_scoped_upper_chest_contract_does_not_activate_without_adult(self):
  p=self.profiles['autumn_afr112_v1']
  self.assertFalse(self.hard(p['semantics']['definition'],adult=False))
  self.assertEqual(self.hard(p['semantics']['definition']),{p['id']})

 def test_compilation_and_opt_in_bundles_preserve_all_gates(self):
  raw=json.loads((ASSETS/'photo_prompt_visual_obligations_autumn_fashion.json').read_text())
  derived={'required_evidence_fields','evidence_requirements','render_gates','composition_instruction'}
  for p in raw['profiles']:
   compiled=self.profiles[p['id']];parts=p['authored_components']['components']
   with self.subTest(pid=p['id']):
    self.assertFalse(derived.intersection(p))
    self.assertEqual(compiled['required_evidence_fields'],[c['evidence_field'] for c in parts])
    self.assertEqual(compiled['render_gates'],[c['render_gate'] for c in parts])
    self.assertTrue(all(g['review_scale']=='native' and 'partial' in g['description'] for g in compiled['render_gates']))
  bundles=[b for b in self.data['candidate_bundles'] if b['id'].startswith('autumn_afr')]
  self.assertEqual(len(bundles),112)
  for b in bundles:
   self.assertEqual(b['adoption'],'optional');self.assertEqual(b['profile_activation'],'independent_request_evidence_only')
   self.assertEqual(len(b['associated_profile_ids']),1);self.assertEqual(len(b['member_candidates']),1)

 def test_maintenance_provenance_and_all_347_term_dispositions(self):
  ext=copy.deepcopy(self.extension);ref=ext.pop('maintenance_ref')
  record=json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/(ref['record_id']+'.json')).read_text())
  self.assertEqual(cs.digest(record),ref['sha256']);self.assertEqual(cs.digest(ext),record['authored_source_sha256'])
  evidence=ROOT/'docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009'
  mapping=json.loads((evidence/'term-runtime-map.json').read_text());integration=json.loads((evidence/'runtime-integration.json').read_text())
  self.assertEqual(mapping['count'],347);self.assertEqual(len({t['term_id'] for t in mapping['terms']}),347)
  self.assertEqual(integration['reused_candidate_count'],17)
  self.assertEqual({b['card_id'] for b in integration['specification_backlog']},{'AFR068','AFR092','AFR113'})
  known={p['id'] for p in self.full['profiles']}
  self.assertTrue(all(v['profile_id'] in known for t in mapping['terms'] for v in t['runtime_variants']))

 def test_real_indices_match_sources_and_detect_tampering(self):
  semantic=pg.load_semantic_index_payload(ASSETS/'photo_prompt_semantic_index.json');pg.validate_semantic_index_metadata(semantic,self.data)
  visual=pg.load_visual_profile_index(ASSETS/'photo_prompt_visual_profile_index.json',self.full)
  self.assertTrue(set(self.profiles)<=set(visual['entries']))
  self.assertTrue({f'slot:{s}:{cid}' for cid,(s,_) in self.entries.items()}<=set(semantic['entries']))
  stale=copy.deepcopy(visual);stale['registry_sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'registry_sha256'):pg.validate_visual_profile_index_metadata(stale,self.full)

if __name__=='__main__':unittest.main()
