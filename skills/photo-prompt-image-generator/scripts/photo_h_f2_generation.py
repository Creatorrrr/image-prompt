"""Content-addressed H/F2 data generations. No publisher or CURRENT writes."""
import argparse,hashlib,json,os,shutil,tempfile
from pathlib import Path
import numpy as np
import photo_candidate_corpus as corpus
import photo_recall_first as rf
from photo_recall_generation import read,write,file_sha,BodyReader
from photo_h_f2_search import Index
from photo_h_f2_query_scope import RECIPE as QUERY_SCOPE_RECIPE
from photo_h_f2_query_scope import CORRECTION_RECIPE
from photo_h_f2_literal_text import RECIPE as LITERAL_ORDER_RECIPE
from photo_h_f2_event_phase import RECIPE as EVENT_PHASE_RECIPE, primary_units
from photo_h_f2_source_relevance import (RECIPE as SOURCE_RELEVANCE_RECIPE,
 SCORING_POLICY as SOURCE_RELEVANCE_POLICY, DEFAULT_RELATION_LANE_WEIGHT,
 ATTRIBUTE_LANE_WEIGHT, SINGLE_PROPERTY_ORDERING_POLICY,
 PROPERTY_ANSWER_RECIPE, PROPERTY_ANSWER_ORDERING_POLICY)
SCHEMA='photo-h-f2-generation/v1'
POLICY={'k1':1.2,'rrf':10,'query_terms':QUERY_SCOPE_RECIPE,'query_correction':CORRECTION_RECIPE,'literal_order':LITERAL_ORDER_RECIPE,'event_phase_order':EVENT_PHASE_RECIPE,'natural_source_relevance':{'recipe':SOURCE_RELEVANCE_RECIPE,'scoring_policy':SOURCE_RELEVANCE_POLICY,'relation_weight':DEFAULT_RELATION_LANE_WEIGHT,'attribute_weight':ATTRIBUTE_LANE_WEIGHT,'relation_scope':'interrogative_property_with_two_or_more_features','coverage':'all_eligible_features_in_one_primary_unit','attribute_scope':'all_requests_and_nonempty_nearest_query_source_owner_witnesses_in_one_primary_unit','contextual_posture':'exclude_stance_terms_inside_locative_pose_adjuncts','ankle_scope':'literal_query_and_primary_source_ankle_witness_with_unbound_question_value','single_property_ordering':SINGLE_PROPERTY_ORDERING_POLICY,'single_property_scope':'reflection_identity_or_tilt_owner_disambiguation_open_question','single_property_evidence':'exact_primary_text_spans_plus_same_selected_rid_effect','unknown_modifiers':'do_not_rank_if_gloss_or_pattern_constraint_is_unmodeled','source_direct_witness_budget_per_unit':12,'legacy_relation_selection':'first_option_semantic_lexical_advisory','property_answer_recipe':PROPERTY_ANSWER_RECIPE,'property_answer_ordering':PROPERTY_ANSWER_ORDERING_POLICY,'property_answer_evidence':'all_requested_features_and_explicit_scene_contexts_in_one_primary_unit_with_same_selected_rid_effect','property_answer_scope':'unstructured_interrogative_property_only','property_answer_abstention':'alternatives_colors_numbers_page_unmodeled_modifiers_unmapped_relations_and_unmodeled_bound_values','property_answer_approval':'advisory_no_semantic_or_native_approval','owned_support_scope':'open_support_direction_with_explicit_bench_and_owned_arm_question','owned_support_evidence':'same_primary_text_bench_support_owned_arm_and_same_selected_rid_effects','owned_support_ordering':'stable_positive_same_primary_and_selected_rid_effects','owned_support_abstention':'alternatives_colors_numbers_unmodeled_modifiers_additional_recognized_relations_or_explicit_arm_side_or_action'},'documents':'D meaning-first then exact original lookup','float':'<f8','cutoff':None}
WEIGHTS={'aliases':4.,'applicability':1.,'concept_units':2.,'core_meaning':2.,'definition':2.,'discovery_hints':1.,'keywords':1.,'labels':3.,'manifestations':1.,'paraphrases':2.,'semantic_caption':1.,'semantic_relations':2.,'source_requirements':2.}
NONEMPTY={'applicability','core_meaning','discovery_hints','source_requirements'}
MEANING=frozenset({'source_definition','source_core_meaning','source_concept_units','source_semantic_relations','selected_branch_unit','selected_branch_component'})
CUES=frozenset({'source_labels','lookup'})
def code_binding():
 root=Path(__file__).parent
 return {p.name:file_sha(p) for p in sorted(root.glob('photo_h_f2*.py'))}
LOADED_CODE=code_binding()

def configs():
 return {f:{'b':.75,'weight':w,**({'normalization_population':'nonempty_documents'} if f in NONEMPTY else {})} for f,w in WEIGHTS.items()}
def stage(store,inputs):
 """inputs are maintenance paths only; resulting manifest has no external dependency."""
 rf.require(code_binding()==LOADED_CODE,'loaded H-F2 implementation changed')
 store=Path(store);store.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='.h-f2-',dir=store) as tmp:
  dest=Path(tmp);G=Path(inputs['generation'])
  for n in ('source-manifest.json','body-locator.json.gz','source-header.json.gz','indexed-documents.json.gz'):
   shutil.copyfile(G/n,dest/n)
  shutil.copytree(G/'body',dest/'body')
  source=read(dest/'source-manifest.json')
  source['files']={p:h for p,h in source['files'].items() if (dest/p).is_file()}
  source['recipe']='photo-h-f2-source-snapshot/v1'
  write(dest/'source-manifest.json',source)
  for k,n in [('documents','documents.json.gz'),('fields','fields.json.gz'),('field_documents','field-documents.json.gz'),('vectors','vectors.f64'),('proofs','document-proofs.json.gz')]:shutil.copyfile(inputs[k],dest/n)
  binding=inputs['binding'];rf.require(binding['space']['provider']=='embeddinggemma2-local','local document space required')
  meta=read(dest/'indexed-documents.json.gz');docs=read(dest/'documents.json.gz')['rows'];field=read(dest/'fields.json.gz')
  fdocs=read(dest/'field-documents.json.gz')['rows'];proofs=read(dest/'document-proofs.json.gz')['rows']
  rf.require(field['fields']==configs(),'not frozen F2 field policy')
  rf.require([d['id'] for d in meta]==[d['id'] for d in docs]==[d['id'] for d in fdocs],'RID coverage mismatch')
  matrix=np.memmap(dest/'vectors.f64',dtype='<f8',mode='r',shape=(len(meta),768))
  rf.require((dest/'vectors.f64').stat().st_size==len(meta)*768*8,'vector extent mismatch')
  body=BodyReader(dest)
  for i,(m,d,f) in enumerate(zip(meta,docs,fdocs,strict=True)):
   record=body.record(m['cid']);rf.require(corpus.digest(record)==m['source_sha256']==d['source_sha256']==f['source_sha256'],'source mismatch')
   original=next(x for x in rf.documents(record) if x['rid']==m['rid'])
   core=[p for p in original['parts'] if {s['role'] for s in p['sources']}&MEANING]
   cues=[p for p in original['parts'] if not ({s['role'] for s in p['sources']}&MEANING) and {s['role'] for s in p['sources']}&CUES]
   expected='\n'.join(p['text'] for p in core+cues) if core+cues else original['text']
   rf.require(d['text']==expected and d['text_sha256']==rf.sha(expected),'D text or lookup cues changed')
   selected=core+cues if core+cues else [{'text':original['text'],'sources':[]}]
   expected_fields={k:[] for k in WEIGHTS}
   for part in selected:
    roles={v['role'] for v in part['sources']};name=None
    for role in ('source_definition','source_core_meaning','source_concept_units','source_semantic_relations','selected_branch_unit','selected_branch_component'):
     if role in roles:name='concept_units' if role.startswith('selected_branch') else role.removeprefix('source_');break
    if name is None and 'source_labels' in roles:name='labels'
    if name is None:name=next((v.get('ref',{}).get('field') for v in part['sources'] if v['role']=='lookup' and v.get('ref',{}).get('field') in expected_fields),'definition')
    expected_fields[name].append(part['text'])
   rf.require(f['fields']==expected_fields,'D part field ownership changed')
   h=d['text_sha256'];proof=proofs[h]
   rf.require(proof['input_sha256']==rf.sha('title: none | text: '+expected),'document input mismatch')
   rf.require(proof['space']==binding['space'] and proof['installation_sha256']==binding['installation_hash'] and proof['kind']=='document' and proof['provider_executed'] is True,'document local execution missing')
   rf.require(proof['vector_sha256']==corpus.digest(matrix[i].tolist()),'document vector proof mismatch')
  # Independently rebuild global field postings, DF/lengths and text coverage.
  from collections import Counter
  lengths={f:[] for f in WEIGHTS};counts={f:0 for f in WEIGHTS};posting={}
  for i,(d,f) in enumerate(zip(docs,fdocs,strict=True)):
   rf.require(Counter(rf.tokens(d['text']))==Counter(t for values in f['fields'].values() for v in values for t in rf.tokens(v)),'field token loss')
   terms={}
   for name in WEIGHTS:
    bag=Counter(t for v in f['fields'][name] for t in rf.tokens(v));size=sum(bag.values());lengths[name].append(size);counts[name]+=bool(size)
    for term,tf in bag.items():terms.setdefault(term,{})[name]=tf
   for term,tf in terms.items():posting.setdefault(term,[]).append([i,tf])
  rf.require(posting==field['postings'] and lengths==field['lengths'] and counts==field['nonempty_counts'],'global F2 statistics changed')
  for f in WEIGHTS:
   denominator=counts[f] if f in NONEMPTY else len(meta)
   rf.require(field['average_lengths'][f]==(sum(lengths[f])/denominator if denominator else 0.),'field normalization changed')
  files={str(p.relative_to(dest)):file_sha(p) for p in sorted(dest.rglob('*')) if p.is_file() and p.name!='.DS_Store'}
  manifest={'schema':SCHEMA,'policy':POLICY,'binding':binding,'files':files,'code':LOADED_CODE,'RID_count':len(meta),'CID_count':len({d['cid'] for d in meta}),'qualification':'source/D/F2/statistics/local-execution/vector coverage verified','native_generation_id':inputs.get('native_generation_id')}
  gid=corpus.digest(manifest);write(dest/'manifest.json',manifest)
  target=store/'h-f2-generations'/gid;target.parent.mkdir(parents=True,exist_ok=True)
  if target.exists():Generation(store,gid,full=True)
  else:os.rename(dest,target)
  return gid
class Generation:
 def __init__(self,store,gid,*,full=False):
  import re
  rf.require(isinstance(gid,str) and re.fullmatch('[0-9a-f]{64}',gid) is not None,'explicit generation ID required')
  self.store=Path(store);self.root=self.store/'h-f2-generations'/gid;self.id=gid
  self.manifest=read(self.root/'manifest.json');m=self.manifest
  rf.require(corpus.digest(m)==gid and m['schema']==SCHEMA and m['policy']==POLICY,'generation binding mismatch')
  rf.require(m['code']==LOADED_CODE==code_binding(),'H-F2 implementation changed;stage a new generation')
  for p,h in m['files'].items():
   path=self.root/p
   rf.require(not Path(p).is_absolute() and '..' not in Path(p).parts and not path.is_symlink(),'unsafe generation member')
   rf.require(path.is_file(),'missing sealed member')
   if full or not p.startswith('body/'):rf.require(file_sha(path)==h,'sealed member changed:'+p)
  self.metadata=read(self.root/'indexed-documents.json.gz');self.fields=read(self.root/'fields.json.gz')
  rf.require(len(self.metadata)==m['RID_count'] and len({d['cid'] for d in self.metadata})==m['CID_count'],'generation population mismatch')
  self.binding=m['binding'];self.body=BodyReader(self.root)
  self.by_identity={row['id']:row for row in self.metadata}
 def primary_units(self,identity):
  row=self.by_identity[identity];record=self.body.record(row['cid'])
  rf.require(corpus.digest(record)==row['source_sha256'],'primary source witness changed')
  return primary_units(record,row['rid'],row['source_sha256'])
 def effect_footprint(self,identity):
  import photo_candidate_realizations as realizations
  row=self.by_identity[identity];record=self.body.record(row['cid'])
  rf.require(corpus.digest(record)==row['source_sha256'],'effect source changed')
  return realizations.effects(record,row['rid'])
 def focus_constraints(self,identity):
  import photo_candidate_realizations as realizations
  row=self.by_identity[identity];record=self.body.record(row['cid'])
  rf.require(corpus.digest(record)==row['source_sha256'],'constraint source changed')
  selected=realizations.branch(record,row['rid'])
  return {'source_conditions':record['conditions'],
          'realization_conditions':selected.get('conditions',{}) if selected else {}}
 def index(self):
  return Index(self.metadata,self.fields,np.memmap(self.root/'vectors.f64',dtype='<f8',mode='r',shape=(len(self.metadata),768)),read(self.root/'documents.json.gz')['rows'],source_units=self.primary_units,source_effects=self.effect_footprint,source_constraints=self.focus_constraints)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--store',type=Path,required=True);p.add_argument('--inputs-json',type=Path,required=True)
 a=p.parse_args();print(json.dumps({'generation_id':stage(a.store,read(a.inputs_json)),'CURRENT_writes':0}))
