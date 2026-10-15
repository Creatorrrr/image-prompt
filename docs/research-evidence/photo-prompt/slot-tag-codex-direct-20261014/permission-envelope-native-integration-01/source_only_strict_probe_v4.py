"""Frozen-v4 source-only strict utility denial; original defect artifact remains immutable."""
import sys,json,hashlib
from pathlib import Path
sys.path[:0]=[str(Path.cwd()),str(Path.cwd()/'skills/photo-prompt-image-generator/scripts')]
from tests.test_photo_native_permission_envelope import source_fixture,core_fixture
import photo_semantic_evidence as n,photo_candidate_corpus as c,prompt_generator as g
x=source_fixture();cid=next(iter(x['candidates']));r=x['candidates'][cid];r['content'].pop('role_evidence');c.validate(x);entry=c.entry(x,cid,realization_id='base');core=core_fixture()
try:
    scope_result=n.permission_scope(entry,core)
except ValueError as error:
    scope_result={'denied':True,'exception':type(error).__name__,'reason':str(error)}
out={'schema':'source-only-mandatory-strict-utility-v4-probe/v1','source':x,'core':core,'entry':entry,
 'admission':n.admission(entry,core),'consumer':g.core_entry_eligible(x,core,{'subject_category':'object','intent_constraints':{'domains':[]}},{'subject':{}},'',entry),
 'direct_permission_scope':scope_result,'record_aware_property_scope_allowed':n.property_scope_allowed(core,entry['affected_dimensions'],entry['affected_properties'],record=r,realization_id='base'),
 'native_code_raw_sha256':hashlib.sha256(Path(n.__file__).read_bytes()).hexdigest(),
 'boundary':'Admission and consumer remain denied; required source-only direct permission_scope raises and record-aware property_scope_allowed returns False. Structural source-only preparation still succeeds as unqualified. No source/proof/signature/operating/runtime/Git/model/network change.'}
p=Path(__file__).parent/'SOURCE-ONLY-STRICT-PROBE-v4.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(out['record_aware_property_scope_allowed']);print(c.digest(out))
