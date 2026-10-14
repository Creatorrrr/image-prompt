"""Mechanical immutable checkpoint assembly after separate literal human-model review.

This helper does not author decisions, fill fact modes/owners/roles/[] or approve.
"""
from pathlib import Path
import hashlib,json,sys
R=Path(__file__).resolve().parent.parent;ROOT=R.parents[3]
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'));import photo_candidate_corpus as c
start,stop=map(int,sys.argv[1:3]);manual_paths=[ROOT/p for p in sys.argv[3:]]
P=R/'authored/native_06250_08250_09250.v6.inputs.json';data=json.loads(P.read_text());cat=data['full_catalog_snapshot'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manual=[row for path in manual_paths for row in json.loads(path.read_text())['records']]
assert [row['ordinal'] for row in manual]==list(range(start,stop))
records=[]
for judgement in manual:
 ordinal=judgement['ordinal'];inp=data['records'][ordinal-8625]
 for fact in judgement['positive_judgements']:
  value=inp['current_source']
  for key in fact[0][1:].split('/'):value=value[int(key)] if isinstance(value,list) else value[key]
  assert fact[1] in value, (ordinal,fact)
 records.append({'ordinal':ordinal,'candidate_id':inp['candidate_id'],'judgement':judgement,
  'actual_record_kind':inp['current_source']['record_kind'],'actual_rids':inp['actual_current_realization_ids'],
  'current_source':inp['current_source'],'current_source_sha256':inp['current_source_sha256'],
  'original_source_sha256':inp['original_source_sha256'],'five_b_source_after':inp['five_b_source_after'],
  'five_b_source_after_sha256':inp['five_b_source_after_sha256'],'original_compiled':inp['original_compiled'],
  'current_own_bindings':inp['current_own_bindings'],'current_closure':inp['current_closure'],
  'role_candidate_spec_sha256':{key:c.digest(cat[key]) for key in judgement['role_candidates']},
  'full_source_read':True,'whole_source_unit_proof_complete':False,'formal_proof':None})
out=R/f'authored/native_06250_08250_09250.{start:05d}_{stop:05d}.draft.json';assert not out.exists()
value={'schema':'photo-native-direct-review-draft-checkpoint/v1','task_name':'/root/review_06250_07250','model':'gpt-6.1-sol','reasoning_effort':'high','range':[start,stop],
 'input':{'file':str(P.relative_to(ROOT)),'raw_sha256':sha(P)},'catalog':data['catalog'],
 'manual_sources':{str(p.relative_to(ROOT)):sha(p) for p in manual_paths},'records':records,
 'actual_read_count':len(records),'root_selection_count':0,'formal_native_proofs':0,'operating_approvals':0,
 'boundary':'All semantic fields come from the separate explicitly authored per-record manual judgements. This assembly only checks exact pointers/hashes/ID order and attaches immutable whole source/compiled/binding closure. Missing qualification, guards, mode, owner, receiver or units remain pending; shape success is not semantic acceptance.'}
out.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');print(out,sha(out),'records',len(records))
