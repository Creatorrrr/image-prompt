"""Frozen existing-contract repro only; no new role/proof/signature authored or mutated."""
import sys,json,gzip,hashlib,copy,os
from pathlib import Path
sys.dont_write_bytecode=True
R=Path.cwd()/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/07143a62ae23201a5cceedf155a985e204256740da96fc083e703d8ac5e7ba07')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as n,photo_slot_semantics as rolefit
assert hashlib.sha256(Path(n.__file__).read_bytes()).hexdigest()=='7d9f7e7c69bc1f8186af9a289eb46defd0e953de9c27d1b0b770142ad2660205'
p=R/'native_batches/review11870-01250-01300-04/BATCH.json';raw=hashlib.sha256(p.read_bytes()).hexdigest();b=json.loads(p.read_text());i=json.loads((R/'native-inputs/prepared/review11870-01250-01300-04/INPUT.json').read_text());s=json.loads(gzip.decompress(Path(i['current_snapshot']['file']).read_bytes()));cat=i['catalog_review']['after']
CASES=[(1255,'relational_action','holdingApp'),(1258,'relational_action','checkApp'),(1271,'relational_action','holdingApp'),(1271,'contact_point','holdingApp'),(1286,'apparatus_pov','refApp'),(1296,'relational_action','holdAApp'),(1296,'contact_point','contactApp')]
results=[]
for o,slot,fid in CASES:
 row=next(r for r in b['records']if r['ordinal']==o);record=copy.deepcopy(row['source_after']);proof=row['proof'];unchanged=c.digest(proof);record['content']['role_evidence']=proof
 n.validate(record,cat,catalog_sha256=c.digest(cat),corpus=s)
 compact=n.compact(record,corpus=s);fact=next(f for f in proof['facts']if f['id']==fid)
 direct=next(u for u in proof['source_units']if u['realization_id']==fact['realization_id']and u['pointer']==fact['pointer']and u['disposition']=='semantic'and fid in u['fact_refs'])
 assert fact['quote'] in direct['quote']==n.positive_string(record,fact['pointer'],realization_id=fact['realization_id'])
 q=rolefit.fit(cat[slot],record,'',realization_id='base');cr=copy.deepcopy(row['source_after']);cr['_semantic_evidence_guard']=compact;cq=rolefit.fit(cat[slot],cr,'',realization_id='base')
 assert q['status']==cq['status']==('eligible'if(o,slot)==(1296,'contact_point')else'incompatible')
 assert c.digest(proof)==unchanged
 spec=cat[slot];dimok=fact['dimension']in spec['dimensions'];prefixok=any(fact['property']==z.rstrip('.')or fact['property'].startswith(z if z.endswith('.')else z+'.')for z in spec['property_prefixes'])
 results.append({'ordinal':o,'candidate_id':row['candidate_id'],'slot':slot,'canonical_fact_id':fid,'canonical_fact_sha256':c.digest(fact),'canonical_fact':fact,'normal_full_unit_sha256':c.digest(direct),'owner_map_sha256':c.digest(proof['owner_maps']['base']),'guard_set_sha256':c.digest(proof['guard_sets']['base']),'effect_set_sha256':c.digest(proof['effect_sets']['base']),'full_source_validation_passed':True,'full_role_fit':q,'compact_role_fit':cq,'current_scalar_dimension_match':dimok,'current_scalar_prefix_match':prefixok,'no_new_projection_contract_implemented':True,'facts_source_effects_proof_unchanged':True})
assert hashlib.sha256(p.read_bytes()).hexdigest()==raw
mods={}
for name,m in sorted(sys.modules.items()):
 f=getattr(m,'__file__',None)
 if f and name.startswith('photo_'):
  pth=Path(f).resolve();assert pth.is_relative_to(G);mods[name]={'file':str(pth),'sha256':hashlib.sha256(pth.read_bytes()).hexdigest()}
out={'schema':'photo-native-scalar-role-gap-readonly-repro/v1','task':'/root/review_08250_09250','model':'gpt-6.1-sol','reasoning_effort':'high','frozen_generation':str(G),'modules':mods,'batch_raw_sha256':raw,'batch_canonical_sha256':c.digest(b),'catalog_sha256':c.digest(cat),'results':results,'expected_incompatible_cases':6,'existing_contact_positive_control':1,'all_expected':True,'os_network_denied':True,'provider_keys_absent':all(not os.environ.get(k)for k in ['GEMINI_API_KEY','GOOGLE_API_KEY','OPENAI_API_KEY','ANTHROPIC_API_KEY']),'source_BATCHevidence_status_catalog_production_test_Git_mutations':0,'new_role_native_approval':0,'manual_projection_truth_inferred_by_code':False}
f=R/'worker-notes/native-08250-fact-role-projection-design-20261015-v1.repro.json';assert not f.exists();f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'results':len(results),'all_expected':True,'raw_sha256':hashlib.sha256(f.read_bytes()).hexdigest()}))
