"""Offline four manually authored proofs: exact GEN188c full/compact consumers only."""
import sys,json,gzip,copy,hashlib
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(G/'scripts/photo_semantic_evidence.py')=='6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9'
sys.path[:0]=[str(G/'scripts'),str(G/'precore'),str(R)]
import photo_semantic_evidence as e
import photo_candidate_corpus as c
import photo_search_layout as layout
import prompt_generator as g
import native_reviews as nr
# direct_review prepends the working scripts directory. Remove that import side
# effect before any lazy legacy provenance/eligibility imports; every photo module
# must resolve from the exact published generation, with no working-tree fallback.
sys.path[:]=[str(G/'scripts'),str(G/'precore')]+[p for p in sys.path if p not in {str(ROOT/'skills/photo-prompt-image-generator/scripts'),str(G/'scripts'),str(G/'precore')}]
S=json.loads(gzip.decompress((R/'native-inputs/bare-prop-applications-plan-06/CURRENT-PROPOSAL.json.gz').read_bytes()))
# Explicit isolated frozen request fixtures; no core or candidate is authored by a classifier.
# Human context is already supplied outside the proposed prop. No native-existing owner address is needed for a new prop.
def core(locked=(),occupied=False):
 text='An independently declared human scene. The requester explicitly permits adding one separate scene prop.'
 rows=[]
 if occupied:
  for aid,kind,axes in [('owner_existing','owner',{'owner':'existing_prop','owner_kind':'entity'}),('role_existing','role',{'role':'primary_prop','owner':'existing_prop'})]:
   rows.append({'assertion_id':aid,'dimension':'subject','polarity':'required','source_span_ids':['request_1'],'axes':{'native_schema':e.witnesses.SCHEMA,'kind':kind,**axes},'evidence':{'meaning':text},'affected_dimensions':['subject']})
  locked=set(locked)|{'subject'}
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'request_1','text':text}]},'semantic_assertions':rows,'user_exclusions':[], 'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':sorted(locked),'open_dimensions':[d for d in ['subject','count'] if d not in locked],'semantic_anchors':[]}}
contract={'subject_category':'human','adult_allowed':True,'intent_constraints':{'domains':[],'subject_categories':[]}}
picked={'subject':{'en':'An independently declared human scene','tags':['human']},'action':{},'location':{}}
results=[]
for ordinal in [1236,259,807,924]:
 stem=f'review06250-{ordinal:05d}-06';P=R/'native-inputs/prepared'/stem;O=R/'native_batches'/stem
 batch=json.loads((O/'BATCH.json').read_text());row=batch['records'][0];cid=row['candidate_id'];record=copy.deepcopy(row['source_after']);record['content']['role_evidence']=row['proof']
 data={**S,'candidates':{**S['candidates'],cid:record}};e.validate(record,data['slot_catalog'],corpus=data)
 verified=nr.verify_batch(str((P/'ASSIGNMENT.json').relative_to(ROOT)),str((O/'BATCH.json').relative_to(ROOT)),str((O/'NOTE.json').relative_to(ROOT)))
 assert verified['statuses']['approved']==1 and not verified['root_accepted']
 own=[v for v in S['slot_bindings'].values() if v['candidate_id']==cid];assert len(own)==1
 matrix=[]
 for label,view in [('full',data),('compact',{**data,'candidates':{**data['candidates'],cid:layout.guard_record(record,data)}})]:
  for bid in [None,own[0]['id']]:
   entry=c.entry(view,cid,bid,realization_id='base');frozen=core()
   admission=e.admission(entry,frozen);assert admission['allowed'],admission
   assert g.core_entry_eligible(view,frozen,contract,picked,'prop',entry)
   dimensions,effects,graph=e.permission_scope(entry,frozen)
   assert dimensions==['count','subject'] and len(effects)==3,(dimensions,effects)
   assert all(p['target'].startswith('native-introduced:') for p in effects)
   for lock in ['subject','count']:
    assert not g.core_entry_eligible(view,core([lock]),contract,picked,'prop',entry),lock
   occupied=e.admission(entry,core(occupied=True));assert not occupied['allowed'],occupied
   absent={'subject':{},'action':{},'location':{}}
   assert not g.core_entry_eligible(view,frozen,{'subject_category':'object','intent_constraints':{'domains':[]}},absent,'prop',entry)
   # Candidate's own human tag is never donated to this independent picked context.
   assert not g.core_entry_eligible(view,frozen,contract,absent,'prop',entry)
   matrix.append({'view':label,'binding_id':bid,'open_subject_count_allowed':True,'whole_subject_lock_rejected':True,'whole_count_lock_rejected':True,'occupied_primary_prop_rejected':True,'missing_external_human_rejected':True,'candidate_human_tag_not_self_witness':True,'actual_effects':effects,'admission':admission})
 # A newly introduced owner cannot satisfy a frozen prerequisite, even if the property matches its new type.
 bad=copy.deepcopy(row['proof']);pr=copy.deepcopy(bad['facts'][1]);pr.update(id='forged_existing_self',mode='prerequisite');pr.pop('operation');pr.pop('receivers');bad['facts'].append(pr)
 badentry={'role_evidence':bad,'_realization_id':'base','affected_dimensions':bad['effect_sets']['base']['dimensions'],'affected_properties':bad['effect_sets']['base']['properties']}
 self_reject=e.admission(badentry,core());assert not self_reject['allowed'],self_reject
 # Foreign/duplicate original field anchors must not donate add/count.
 assert all(u['fact_refs']==['new_type'] for u in row['proof']['source_units'] if u['pointer']!='/content/application_contract')
 result={'ordinal':ordinal,'candidate_id':cid,'verification':{k:v for k,v in verified.items() if k!='records'},'own_binding':own[0],'matrix':matrix,'introduced_self_prerequisite_rejected':self_reject,'fact_count':3,'source_unit_count':len(row['proof']['source_units']),'root_acceptance_count':0,'operational_adoption_count':0};results.append(result)
mods={}
for name,m in sorted(sys.modules.items()):
 if name.startswith(('photo_','photo_precore_')) and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'raw_sha256':sha(p)}
out=R/'worker-notes/native-06250-C4-formal06-diagnostic-20261015.json';assert not out.exists();out.write_text(json.dumps({'generation':str(G),'native_module_sha256':sha(G/'scripts/photo_semantic_evidence.py'),'actual_modules':mods,'results':results,'root_acceptance_count':0,'operational_adoption_count':0,'boundary':'Explicit manual C selections were freshly reread. Offline exact-source/native_batch integrity and full/compact admission/oldbinding/lock matrix are technical evidence, not root acceptance or production adoption. Legacy human guard is independently cumulative through actual final eligibility using externally frozen human request context; native admission alone is not legacy policy admission.'},ensure_ascii=False,indent=2)+'\n');print(out,sha(out),'four_proofs','16view_binding_rows','32whole_lock_rejections')
