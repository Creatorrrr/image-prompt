import sys,json,gzip,copy,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
R=Path.cwd()/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/07143a62ae23201a5cceedf155a985e204256740da96fc083e703d8ac5e7ba07');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as n,photo_slot_semantics as slots
bpath=R/'native_batches/review11870-01285-05/BATCH.json';before=hashlib.sha256(bpath.read_bytes()).hexdigest();b=json.loads(bpath.read_text());row=b['records'][0];i=json.loads((R/'native-inputs/prepared/review11870-01285-05/INPUT.json').read_text());s=json.loads(gzip.decompress(Path(i['current_snapshot']['file']).read_bytes()));cat=i['catalog_review']['after'];assert c.digest(cat)=='3655a006e69500662987c829361711a7194c3e297bfc4c408297bcf94f35d645';rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];sig=c.digest(row['proof']);n.validate(rec,cat,catalog_sha256=c.digest(cat),corpus=s);compact=n.compact(rec,corpus=s);cr=copy.deepcopy(row['source_after']);cr['_semantic_evidence_guard']=compact
full=slots.fit(cat['participant_role'],rec,'',realization_id='base');cp=slots.fit(cat['participant_role'],cr,'',realization_id='base');assert full['status']==cp['status']=='eligible';assert c.digest(row['proof'])==sig
facts=[x for x in row['proof']['facts']if x['id']in row['proof']['roles']['participant_role']['fact_refs']]
assert all(x['dimension']=='relationship'and x['property']=='relationship.role.counterpart'for x in facts)
assert hashlib.sha256(bpath.read_bytes()).hexdigest()==before
mods={}
for name,m in sys.modules.copy().items():
 if name.startswith('photo_')and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
out={'schema':'photo-native-generic-role-view-existing-direct-control/v1','task':'/root/review_08250_09250','model':'gpt-6.1-sol','reasoning_effort':'high','frozen_generation':str(G),'modules':mods,'batch_raw_sha256':before,'batch_canonical_sha256':c.digest(b),'full_source_validation':True,'full_fit':full,'compact_fit':cp,'actual_role_facts':facts,'same_original_effects_facts_and_native_signature':True,'new_projection_needed_for_this_actual05_role':False,'new_contract_implemented':False,'source_proof_BATCHevidence_status_production_test_Git_mutations':0,'semantic_entailment_not_inferred_from_shape':True}
f=R/'worker-notes/native-08250-generic-role-view-supplement-20261015-v1.repro.json';assert not f.exists();f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(hashlib.sha256(f.read_bytes()).hexdigest())
