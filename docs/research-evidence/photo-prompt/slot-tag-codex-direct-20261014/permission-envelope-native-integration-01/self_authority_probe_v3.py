"""Same independent peer attack after separating validation and trust issuance."""
import copy,hashlib,json,sys
from pathlib import Path
from unittest import mock
sys.path[:0]=[str(Path.cwd()),str(Path.cwd()/'skills/photo-prompt-image-generator/scripts')]
from tests.test_photo_native_permission_envelope import source_fixture,core_fixture,entries
from tests.test_photo_semantic_evidence import reattest
import photo_native_permission as p,photo_semantic_evidence as n,photo_candidate_corpus as c,prompt_generator as g
actual=source_fixture();core=core_fixture();original=entries(actual,core)[0];before=copy.deepcopy(p._TRANSPORTS)
forged=copy.deepcopy(actual);r=forged['candidates'][original['id']];r['content'].pop('permission_envelope');r['content']['role_evidence'].pop('permission_envelopes');r['content']['role_evidence']['meaning_sha256']=n.meaning_sha256(r)
calls=[]
def call(label,fn):
 try:
  v=fn();calls.append({'label':label,'returned':v});return v
 except (ValueError,KeyError,TypeError)as exc:
  calls.append({'label':label,'exception':type(exc).__name__,'reason':str(exc)})
with mock.patch.object(p,'freeze_source_authority',wraps=p.freeze_source_authority)as trust:
 reattest(forged)  # Mechanical fixture rehash explicitly does NOT issue trust.
 call('structural_validate_without_corpus',lambda:n.validate(r,forged['slot_catalog']))
 call('structural_validate_own_corpus',lambda:n.validate(r,forged['slot_catalog'],corpus=forged))
 call('structural_compact',lambda:n.compact(r,forged))
 for wire,entry in zip(['full','compact'],entries(forged,core)):
  call(wire+'_direct_admission',lambda entry=entry:n.admission(entry,core))
  call(wire+'_direct_permission',lambda entry=entry:n.permission_scope(entry,core))
  call(wire+'_self_supplied_corpus_consumer',lambda entry=entry:g.core_entry_eligible(forged,core,{'subject_category':'object','intent_constraints':{'domains':[]}},{'subject':{}},'',entry))
 call('original_source_still_mandatory',lambda:n.admission(original,core))
 call('forged_role_qualification',lambda:n.qualification(forged['slot_catalog']['fixture_shot'],r))
 assert trust.call_count==0
 assert p._TRANSPORTS==before
checks=[x for x in calls if '_direct_admission'in x['label']];assert all(x['returned']['allowed']is False for x in checks)
assert all(x.get('exception')=='ValueError'for x in calls if '_direct_permission'in x['label'])
assert all(x['returned']is False for x in calls if '_corpus_consumer'in x['label'])
x={'schema':'photo-native-permission-self-authority-afterfix/v3','task':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high',
 'original_fixture_explicit_authority_setup':True,'trusted_freeze_calls_during_attack':0,'active_session':p.session_binding(),'transport_registry_unchanged_by_validate_compact_reattest':True,
 'calls':calls,'actual_mandatory_source':actual,'forged_source':forged,'actual_core':core,
 'code_pins':{str(Path(m.__file__)):hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()for m in [p,n,c,g]},
 'boundary':'Synthetic independent source/core only. Validators and mechanical rehash do not mint authority. Every stripped full/compact admission/permission/consumer rejects without explicit new trusted freeze; original mandatory proof still requires its plan. No actual1299 proof, source edit, runtime publish, Git, model or network.'}
out=Path(__file__).parent/'SELF-AUTHORITY-AFTERFIX-v3.json';assert not out.exists();out.write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(c.digest(x));print([(q['label'],q.get('exception'),q.get('returned',{}).get('allowed')if isinstance(q.get('returned'),dict)else type(q.get('returned')).__name__)for q in calls])
