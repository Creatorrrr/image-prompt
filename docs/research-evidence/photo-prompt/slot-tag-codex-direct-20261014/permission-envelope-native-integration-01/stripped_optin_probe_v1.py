"""Preserved before-fix exact stripped/rehashed opt-in counterexample."""
import copy,json,hashlib,sys
from pathlib import Path
sys.path[:0]=[str(Path.cwd()),str(Path.cwd()/'skills/photo-prompt-image-generator/scripts')]
from tests.test_photo_native_permission_envelope import source_fixture,core_fixture,entries
from tests.test_photo_semantic_evidence import reattest
import photo_semantic_evidence as n,photo_candidate_corpus as c,prompt_generator as g,audit_composed_prompt as audit
from unittest import mock
actual=source_fixture();core=core_fixture();full,compact=entries(actual,core);forged=copy.deepcopy(compact)
p=forged['_semantic_evidence_guard'];p.pop('permission_envelopes');p['compact_sha256']=c.digest({k:v for k,v in p.items()if k!='compact_sha256'})
record=copy.deepcopy(actual['candidates'][full['source_candidate_id']if 'source_candidate_id'in full else p['candidate_id']]);record['content'].pop('permission_envelope');fp=record['content']['role_evidence'];fp.pop('permission_envelopes');fp['meaning_sha256']=n.meaning_sha256(record)
fakedata=copy.deepcopy(actual);fakedata['candidates'][record['id']]=record;reattest(fakedata)
qualification=None
try:n.validate(record,actual['slot_catalog'],corpus=actual);qualification=True
except ValueError as exc:qualification=str(exc)
result={'actual_source_declared_required':True,'active_trusted_session':None,'compact_admission':n.admission(forged,core),
'compact_consumer_with_actual_source_data':g.core_entry_eligible(actual,core,{'subject_category':'object','intent_constraints':{'domains':[]}},{'subject':{}},'',forged),
'compact_permission_scope':n.permission_scope(forged,core),'full_forged_qualification_against_actual_corpus':qualification}
composed={'chosen_candidate_ids':[record['id']],'candidate_interpretations':[{'candidate_id':record['id'],'realization_id':'base'}],'owner_selections':full['_native_owner_selections'],'prompt_en':'Existing item remains visible in image I with macro shot scale.'}
with mock.patch.object(g,'frozen_core_context',return_value=({'subject_category':'object','intent_constraints':{'domains':[]}},{'subject':{}})):
 result['actual_fullsource_final_audit']=audit.audit_native_adoptions({'authorial_core':core,'creative_controls':{}},composed,actual)
result.update(schema='native-permission-stripped-optin-beforefix-probe/v1',actual_source=actual,actual_core=core,forged_compact_entry=forged,forged_full_record=record,
code_pins={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(n.__file__),Path(g.__file__),Path(audit.__file__)]},boundary='Synthetic before-fix report. Passing stripped paths are defects, never approval; real source final audit rejects missing plan. No actual source/canonical/Git/model/network change.')
out=Path(__file__).parent/'STRIPPED-OPTIN-BEFOREFIX-v1.json';assert not out.exists();out.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print({k:result[k]for k in ['compact_admission','compact_consumer_with_actual_source_data','full_forged_qualification_against_actual_corpus','actual_fullsource_final_audit']})
