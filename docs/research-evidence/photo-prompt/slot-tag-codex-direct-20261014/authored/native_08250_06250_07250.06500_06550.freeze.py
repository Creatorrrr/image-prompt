"""Quote/shape/integrity checks only; manual source decisions remain pending."""
import collections,copy,gzip,hashlib,json,runpy
from pathlib import Path
A=Path(__file__).resolve().parent;R=A.parent
author=A/'native_08250_06250_07250.06500_06550.author.py'
m=runpy.run_path(str(author));out=m['build'](6500,6550);c=m['c'];s=m['s']
assert len(out['records'])==50
source=json.loads(gzip.decompress((R/'SOURCE.json.gz').read_bytes()))
assert c.digest(source)==out['frozen_source_sha256']
checks=[]
for row in out['records']:
 cid=row['candidate_id'];o=row['ordinal'];original=source['candidates'][cid]
 assert original==row['original_record']
 locator=row['compiled_review_locator'];compiled=json.loads(Path(locator['file']).read_text())
 reviewed=compiled['decisions'][locator['item']-1]
 assert locator['json_pointer']==f'/decisions/{locator["item"]-1}'
 assert c.digest(reviewed)==locator['row_sha256']
 own={k:v for k,v in source['slot_bindings'].items() if v['candidate_id']==cid}
 assert own==row['all_own_source_bindings']
 assert s.referenced_records(row['exact_5B_after'],source)=={}
 assert row['complete_reference_records']==row['complete_reference_bindings']=={}
 assert row['actual_realization_ids']==['base']
 assert not row['uncovered_positive_paths']
 assert row['native_proof_complete'] is False
 groups=collections.defaultdict(set)
 for fact in row['fact_drafts']:
  s._fact_valid(fact)
  assert fact['quote'] in s.positive_string(row['proposed_after'],fact['pointer'],realization_id='base')
  if fact['mode']=='effect':
   groups[(fact['realization_id'],fact['target'],fact['property'])].add(json.dumps([fact['value'],fact['operation'],fact['receivers']],sort_keys=True))
 assert all(len(values)==1 for values in groups.values())
 assert {f['target'] for f in row['fact_drafts']}<={x[0] for x in row['owner_intents']}
 checks.append({'ordinal':o,'candidate_id':cid,'original_source_exact':True,'compiled_locator_row_hash_exact':True,'all_own_bindings_exact':True,'reference_closure_empty_verified':True,'quote_substrings_and_fact_shape':True,'positive_paths_disposition_present':True,'same_property_effect_assignment_conflicts':0,'manual_owner_intent_names_cover_targets':True,'semantic_approval':False})
draft=A/'native_08250_06250_07250.06500_06550.draft.json'
assert not draft.exists(), 'immutable draft already exists'
draft.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
modules={name:{'file':mod.__file__,'sha256':hashlib.sha256(Path(mod.__file__).read_bytes()).hexdigest()} for name,mod in [('photo_candidate_corpus',c),('photo_candidate_realizations',m['rr']),('photo_semantic_evidence',s),('photo_semantic_witnesses',s.witnesses)]}
for name,item in modules.items():assert '/generations/1871bafa0e008e186ccce4e92908f2b177529b215c22e2fb46d07f0b28679bfd/' in item['file']
result={'schema':'native-manual-draft-integrity-only/v1','task_name':'/root/review_08250_09250','model':'gpt-6.1-sol','reasoning_effort':'high','start':6500,'stop':6550,'actual_directly_read_count':50,'prepared_total':1000,'facts':sum(len(r['fact_drafts']) for r in out['records']),'positive_units':sum(len(r['whole_positive_units']) for r in out['records']),'frozen_modules':modules,'checks':checks,'all_checks_pass':True,'semantic_approval':False,'native_proof':None,'full_compact_admission_tested':False,'operating_native_qualified_count':0}
p=A/'native_08250_06250_07250.06500_06550.checks.json';assert not p.exists();p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'draft':str(draft),'raw_sha256':hashlib.sha256(draft.read_bytes()).hexdigest(),'rows':50,'facts':result['facts'],'units':result['positive_units'],'integrity_pass':True,'semantic_approval':False}))
