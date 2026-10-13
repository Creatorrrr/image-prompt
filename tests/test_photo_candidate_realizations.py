"""Conditional source effects, member guards and explicit adoption boundaries."""
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
import photo_candidate_realizations as r
import photo_global_retrieval as guards
import photo_role_proposals as roles
import photo_native_pack as packs
import photo_shared_views as views
import photo_slot_retrieval as retrieval
import audit_global_retrieval as audit
import prompt_generator as g
from photo_contracts import property_effects_allowed
from tests.test_photo_global_retrieval import GlobalDiscoveryTests

class RealizationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  GlobalDiscoveryTests.setUpClass();cls.core=copy.deepcopy(GlobalDiscoveryTests.core);cls.controls=GlobalDiscoveryTests.controls
 def source(self):
  helper=GlobalDiscoveryTests();data=helper.data();cid='cand_'+'a'*32
  data['candidates'][cid]['effects']={'dimensions':[],'properties':[], 'realizations':{'mode':'one','branches':[
   {'id':'left_light','conditions':{},'context_terms':[],'effects':{'dimensions':['lighting'],'properties':[{'dimension':'lighting','target':'cup','property':'lighting.direction.left'}]}},
   {'id':'right_and_pose','conditions':{},'context_terms':[],'effects':{'dimensions':['lighting','pose'],'properties':[{'dimension':'lighting','target':'cup','property':'lighting.direction.right'},{'dimension':'pose','target':'main_subject','property':'body.pose'}]}}]}}
  return data,cid
 def test_one_branch_has_only_its_owned_effects_and_unknown_id_fails(self):
  data,cid=self.source();c.validate({key:data[key] for key in c.CORPUS_FIELDS})
  entry=c.entry(data,cid,realization_id='left_light')
  self.assertEqual(entry['affected_dimensions'],['lighting']);self.assertNotIn('body.pose',[p['property'] for p in entry['affected_properties']])
  self.assertRaises(ValueError,c.entry,data,cid,realization_id='invented')
 def test_unselected_branch_does_not_close_selected_open_scope(self):
  data,cid=self.source();core=copy.deepcopy(self.core);core['intent_lock']['open_dimensions']=['lighting']
  contract,picked=g.frozen_core_context(data,core,self.controls)
  self.assertEqual(r.eligible_ids(data,cid,core,contract,picked),['left_light'])
  allowed,_,_=guards.eligible(data,core,self.controls);self.assertIn(cid,allowed)
 def test_intrinsic_human_guard_survives_a_neutral_alternative(self):
  data,cid=self.source();data['candidates'][cid]['conditions']={'for_any':['human']}
  allowed,_,_=guards.eligible(data,self.core,self.controls);self.assertNotIn(cid,allowed)
 def test_branch_guard_is_anded_with_source_not_an_override(self):
  data,cid=self.source();data['candidates'][cid]['effects']['realizations']['branches'][0]['conditions']={'for_any':['human']}
  core=copy.deepcopy(self.core);core['intent_lock']['open_dimensions']=['lighting']
  contract,picked=g.frozen_core_context(data,core,self.controls)
  self.assertEqual(r.eligible_ids(data,cid,core,contract,picked),[])
 def test_optional_playback_requires_an_existing_positive_witness(self):
  data,cid=self.source();x=data['candidates'][cid];x['effects']['realizations']['mode']='optional';x['effects']['realizations']['branches']=x['effects']['realizations']['branches'][:1]
  x['effects']['realizations']['branches'][0]['context_terms']=['recorded playback'];x['content']['en']='recorded playback'
  contract,picked=g.frozen_core_context(data,self.core,self.controls)
  self.assertEqual(r.eligible_ids(data,cid,self.core,contract,picked),['base'])
  core=copy.deepcopy(self.core);core['baseline_prompt_en']+=' Recorded playback is visible.'
  self.assertIn('left_light',r.eligible_ids(data,cid,core,contract,picked))
 def test_proposal_projects_one_branch_without_copying_the_canonical_body(self):
  data,cid=self.source();p=roles.propose(data,'lighting',cid,[],realization_ids=['left_light'])
  self.assertEqual(p['realization_id'],'left_light');self.assertNotIn('pose',p['effects']['dimensions']);self.assertEqual(roles.entry(data,p)['id'],cid)
 def test_receipt_rank_audit_recomputes_the_same_available_branch_subset(self):
  helper=GlobalDiscoveryTests();data,cid=self.source()
  conditional=data['candidates'][cid]['effects']['realizations']
  conditional['mode']='optional';conditional['branches']=conditional['branches'][:1]
  conditional['branches'][0]['conditions']={'for_any':['human']}
  lazy=helper.lazy(data)
  self.addCleanup(helper.doCleanups)
  cards,record,_=retrieval.retrieve(lazy,self.core,self.controls,helper.context())
  working=packs.WorkingPack({'global_retrieval':record,'authorial_core':self.core,'creative_controls':self.controls},cards)
  pack=packs.finalize(working,lazy,record['selected_candidate_ids'],helper.context())
  self.assertEqual(audit.audit(pack,lazy,helper.context()),[])
  proposals=[x for x in pack['role_proposals'].values() if x['candidate_id']==cid]
  self.assertTrue(proposals)
  self.assertTrue(all(x['eligible_realization_ids']==['base'] for x in proposals))
 def test_adoption_requires_a_presented_explicit_branch(self):
  data,cid=self.source();candidate={'authored_record':data['candidates'][cid],'realization_views':{'left_light':{'realization_id':'left_light','affected_dimensions':['lighting']}}}
  self.assertRaises(ValueError,r.selected_view,candidate,{})
  self.assertRaises(ValueError,r.selected_view,candidate,{'realization_id':'right_and_pose'})
  self.assertEqual(r.selected_view(candidate,{'realization_id':'left_light'})['affected_dimensions'],['lighting'])
 def test_old_corpus_and_pack_are_rejected(self):
  data,_=self.source();old={key:data[key] for key in c.CORPUS_FIELDS};old['schema']='photo-candidate-corpus/v2'
  self.assertRaises(ValueError,c.validate,old);self.assertRaises(ValueError,packs.validate,{'contract_version':'photo-candidate-pack/v9'})
 def test_duplicate_realizations_and_recursive_effects_are_rejected(self):
  for defect in ['duplicate','nested']:
   data,cid=self.source();x=data['candidates'][cid]['effects']['realizations']
   if defect=='duplicate':x['branches'][1]['id']=x['branches'][0]['id']
   else:x['branches'][0]['effects']['realizations']=copy.deepcopy(x)
   with self.subTest(defect=defect),self.assertRaises(ValueError):c.validate({key:data[key] for key in c.CORPUS_FIELDS})
 def test_alternative_bundle_does_not_inherit_an_unselected_member(self):
  data,cid=self.source();other='cand_'+'b'*32;one='cand_'+'c'*32
  x=data['candidates'][cid];x['record_kind']='visual_bundle';x['content']['member_candidates']=[{'candidate_id':other,'binding_id':'bind_'+'f'*32},{'candidate_id':one,'binding_id':'bind_'+'g'*32}]
  x['content']['components']=[{'id':'garment','concept_units':['left garment','right garment'],'minimum_realizations':1}]
  for branch,member,word in zip(x['effects']['realizations']['branches'],[other,one],['left garment','right garment']):
   branch['member_candidate_ids']=[member];branch['component_units']={'garment':[word]}
  projected=c.entry(data,cid,realization_id='left_light')
  self.assertEqual([p['candidate_id'] for p in projected['member_candidates']],[other]);self.assertEqual(projected['components'][0]['concept_units'],['left garment'])
 def test_native_garment_owner_keeps_original_wearer_property_lock_scope(self):
  source=c.load(ROOT/'skills/photo-prompt-image-generator/assets')
  record=source['candidates']['cand_cb45aeb918bc58e1b6dec41185207523']
  for rid in r.ids(record):
   effects=r.effects(record,rid)
   lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'appearance','target':'main_subject','property':'wardrobe.color'}]}
   self.assertFalse(property_effects_allowed(lock,effects['dimensions'],effects['properties']))
   self.assertEqual({p['target'] for p in effects['properties']},{'main_subject'})
 def test_public_bundle_exposes_two_complete_choices_with_one_member_each(self):
  helper=GlobalDiscoveryTests();fixture=helper.data();source=views.source(fixture)
  a,b,parent=['cand_'+letter*32 for letter in ['a','b','d']]
  left,right=['bind_'+letter*32 for letter in ['d','e']]
  source['slot_bindings'][right]['candidate_id']=b
  for cid,property_path in [(a,'lighting.direction.left'),(b,'lighting.distribution.edge')]:
   source['candidates'][cid]['content']['concept_units']=['porcelain teacup']
   source['candidates'][cid]['effects']['properties']=[{'dimension':'lighting','target':'main_subject','property':property_path}]
  pointers=[{'candidate_id':cid,'binding_id':bid,'requirements':{'relations':[]},'adoption':'optional'} for cid,bid in [(a,left),(b,right)]]
  source['candidates'][parent]={'id':parent,'record_kind':'visual_bundle','conditions':{},'provenance':[{'source':'authored-test','sha256':'a'*64}],
   'content':{'source_sha256':'a'*64,'associated_profile_ids':[],'components':[{'id':'one_light','concept_units':['left source light','edge source light'],'minimum_realizations':1}],
    'member_candidates':pointers,'confusion_boundaries':['Do not combine two alternative sources.'],'relations':[],'adoption':'optional','profile_activation':'independent_request_evidence_only'},
   'effects':{'dimensions':[],'properties':[],'realizations':{'mode':'one','branches':[
    {'id':rid,'conditions':{},'context_terms':[],'effects':copy.deepcopy(source['candidates'][cid]['effects']),'member_candidate_ids':[cid],'component_units':{'one_light':[unit]}}
    for rid,cid,unit in [('left_source',a,'left source light'),('edge_source',b,'edge source light')]]}}}
  source['policies']['bundle_refs']=[parent]
  source['policies']['candidate_semantic_policy']={'joint_adoption':{'maximum_members_per_bundle':4,'maximum_bundles':4,'minimum_shared_content_words':1,'context_policy':'source_declared_members_only'}}
  c.validate(source)
  data=views.RequestCandidates(views.assemble(source,{}),[parent])
  # Isolate branch publication with lighting properties open. The original
  # blue-cup fixture otherwise has requester-owned lighting property locks.
  core=copy.deepcopy(self.core);core['intent_lock']['semantic_anchors']=[row for row in core['intent_lock']['semantic_anchors'] if row['dimension']!='lighting']
  pack=packs.WorkingPack({'authorial_core':core,'creative_controls':self.controls,'provenance':{'seed':5}}, {})
  public=g.candidate_pack_candidate_bundles(data,pack)
  self.assertEqual(len(public['candidates']),1)
  master=public['candidates'][0];choices=master['realization_choices'];self.assertEqual(len(choices),2)
  self.assertEqual({row['realization_id'] for row in choices},{'left_source','edge_source'})
  self.assertTrue(all(len(row['member_candidates'])==1 for row in choices))
  self.assertTrue(all(row['joint_admission']['external_context_assumed'] is False for row in choices))
  master['authored_record']=source['candidates'][parent]
  selected=r.selected_view(master,{'realization_id':'left_source'})
  self.assertEqual([row['id'] for row in selected['member_candidates']],[a])
  self.assertEqual(selected['components'][0]['concept_units'],['left source light'])

if __name__=='__main__':unittest.main()
