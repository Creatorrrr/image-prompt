"""Exact frozen-v3 source-only strict utility boundary, not adoption success."""
import sys,json,hashlib
from pathlib import Path
sys.path[:0]=[str(Path.cwd()),str(Path.cwd()/'skills/photo-prompt-image-generator/scripts')]
from tests.test_photo_native_permission_envelope import source_fixture,core_fixture
import photo_semantic_evidence as n,photo_candidate_corpus as c,prompt_generator as g
x=source_fixture();cid=next(iter(x['candidates']));r=x['candidates'][cid];r['content'].pop('role_evidence');c.validate(x);entry=c.entry(x,cid,realization_id='base');core=core_fixture()
out={'schema':'source-only-mandatory-strict-utility-v3-probe/v1','source':x,'core':core,'entry':entry,
 'admission':n.admission(entry,core),'consumer':g.core_entry_eligible(x,core,{'subject_category':'object','intent_constraints':{'domains':[]}},{'subject':{}},'',entry),
 'direct_permission_scope':n.permission_scope(entry,core),'record_aware_property_scope_allowed':n.property_scope_allowed(core,entry['affected_dimensions'],entry['affected_properties'],record=r,realization_id='base'),
 'native_code_raw_sha256':hashlib.sha256(Path(n.__file__).read_bytes()).hexdigest(),
 'boundary':'Actual adoption rejects. Direct legacy scope/property utilities do not yet reject a known mandatory source-only declaration; proposed narrowly scoped explicit deny. Production v3 remains frozen pending root selection. No proof/signature/source operating/runtime/Git/model/network change.'}
p=Path(__file__).parent/'SOURCE-ONLY-STRICT-PROBE-v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(out['record_aware_property_scope_allowed']);print(c.digest(out))
