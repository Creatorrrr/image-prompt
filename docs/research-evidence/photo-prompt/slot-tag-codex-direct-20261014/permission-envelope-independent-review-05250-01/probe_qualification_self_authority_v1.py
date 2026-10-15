"""Independent serialized-source poisoning probe; no freeze/trusted-session call.
Uses the existing writer-controlled source/core fixture as the common test setup;
the attack record/corpus is an independently authored adversarial mutation.
"""
import copy,hashlib,json,pathlib,sys
ROOT=pathlib.Path.cwd();sys.path[:0]=[str(ROOT),str(ROOT/'skills/photo-prompt-image-generator/scripts')]
from tests.test_photo_native_permission_envelope import source_fixture,core_fixture,entries
from tests.test_photo_semantic_evidence import reattest
import photo_native_permission as p,photo_semantic_evidence as n,photo_candidate_corpus as c,prompt_generator as g,photo_search_layout as layout
OUT=pathlib.Path(__file__).parent/'SELF-AUTHORITY-PROBE-v1.json';assert not OUT.exists()
actual=source_fixture();core=core_fixture();full,compact=entries(actual,core)
cid=full.get('source_candidate_id',full.get('id'));assert cid in actual['candidates']
oldproof=copy.deepcopy(n.proof_of(actual['candidates'][cid]));oldentry=copy.deepcopy(full)
forged=copy.deepcopy(actual);r=forged['candidates'][cid]
r['content'].pop('permission_envelope');r['content']['role_evidence'].pop('permission_envelopes');r['content']['role_evidence']['meaning_sha256']=n.meaning_sha256(r);reattest(forged)
rows=[]
def call(label,fn):
 try:v=fn();rows.append({'label':label,'returned':v});return v
 except Exception as e:rows.append({'label':label,'exception':type(e).__name__,'reason':str(e)});return None
call('baseline_actual_mandatory_direct_without_trusted_session',lambda:n.admission(full,core))
call('forged_validate_against_actual_corpus',lambda:n.validate(r,actual['slot_catalog'],corpus=actual))
call('forged_validate_no_corpus',lambda:n.validate(r,forged['slot_catalog']))
ff,fc=entries(forged,core)
call('forged_full_direct_admission_after_self_qualification',lambda:n.admission(ff,core))
call('forged_compact_direct_admission_after_self_qualification',lambda:n.admission(fc,core))
call('forged_full_permission_scope_after_self_qualification',lambda:n.permission_scope(ff,core))
call('forged_compact_permission_scope_after_self_qualification',lambda:n.permission_scope(fc,core))
kwargs=(core,{'subject_category':'object','intent_constraints':{'domains':[]}},{'subject':{}},'')
call('actual_source_consumer_rejects_forged',lambda:g.core_entry_eligible(actual,*kwargs,fc))
call('self_supplied_forged_source_consumer',lambda:g.core_entry_eligible(forged,*kwargs,fc))
call('forged_validate_own_corpus',lambda:n.validate(r,forged['slot_catalog'],corpus=forged))
call('original_mandatory_still_rejected_without_session',lambda:n.admission(oldentry,core))
result={'schema':'independent-native-permission-self-authority-probe/v1','task':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high','active_trusted_permission_session':p.session_binding(),'trusted_freeze_calls':0,'actual_mandatory_source':actual,'adversarial_full_source':forged,'actual_core':core,'forged_full_entry':ff,'forged_compact_entry':fc,'calls':rows,'code_pins':[{'file':m.__file__,'raw_sha256':hashlib.sha256(pathlib.Path(m.__file__).read_bytes()).hexdigest()}for m in [p,n,c,g,layout]],'boundary':'Controlled synthetic core/fixture. An allowed direct-admission result here is a trust-boundary counterexample, never approval. Consumer with actual source is contrasted with independently supplied forged source. No trusted freeze function or session, production/source/Git/network/model call.'}
OUT.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(json.dumps({'calls':rows,'code_pins':result['code_pins'],'artifact':str(OUT)},ensure_ascii=False))
