from pathlib import Path
import importlib.abc,sys,json,time,unittest
ROOT=Path(__file__).resolve().parents[5];sys.path[:0]=[str(ROOT),str(ROOT/'skills/photo-prompt-image-generator/scripts')]
class DenyModels(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'photo_local_embedding','torch','transformers','sentence_transformers','tensorflow','jax','mlx'}:raise AssertionError('model import forbidden: '+fullname)
sys.meta_path.insert(0,DenyModels())
import photo_embedding_provider as p
calls=[]
def no(*a,**k):calls.append('embedding');raise AssertionError('embedding forbidden')
p.embed=no;p.embed_many=no
class R(unittest.TextTestResult):
 def __init__(self,*a,**k):super().__init__(*a,**k);self.ids=[];self.subtests=0
 def startTest(self,t):self.ids.append(t.id());super().startTest(t)
 def addSubTest(self,t,s,e):self.subtests+=1;super().addSubTest(t,s,e)
from tests.test_photo_native_member_scope_transport import MemberScopeClosureTests
from tests import test_photo_native_existing_member_scope as fixture
import copy,hashlib
import photo_candidate_corpus as c
import photo_semantic_evidence as e
from unittest import mock
import photo_native_owner_resolution as resolver
data=MemberScopeClosureTests().compound(True);core=fixture.scope_core()
selection=fixture.choices(data,core);selection['entries']+=fixture.choices(data,core,cid=fixture.B)['entries']
selected=c.entry(data,fixture.A,realization_id='base',dependency_selections={fixture.B:'base'},owner_selections=selection)
dropped=copy.deepcopy(selected);dropped['_native_dependency_selections']={}
before={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in [
 'skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py','tests/test_photo_native_existing_member_scope.py','tests/test_photo_native_member_scope_transport.py']}
standalone=e.admission(dropped,core)
with e.bound_selected_resolution([selected],core) as context:
 covers=e._context_covers(context,[dropped],core)
 with mock.patch.object(resolver,'resolve_selected_contracts',wraps=resolver.resolve_selected_contracts) as observed:
  cached=e.admission(dropped,core);calls_in_context=observed.call_count
 stale_children=copy.deepcopy(context['nodes'][fixture.A]['selected_children'])
after={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in before}
report={'schema':'photo-B2-root-closure-cache-read-only-diagnostic/v1','task':'/root/native_evidence',
 'source_fixture':'MemberScopeClosureTests.compound(optional=True); qualified synthetic full source sealed by c.entry',
 'before_hashes':before,'after_hashes':after,'bytes_unchanged':before==after,
 'selected_dependency_selections':selected['_native_dependency_selections'],
 'dropped_dependency_selections':dropped['_native_dependency_selections'],
 'actual_standalone_admission':standalone,'actual_cached_admission':cached,
 'actual_context_covers_dropped_root':covers,'B1_calls_during_cached_admission':calls_in_context,
 'cached_selected_children':stale_children,
 'finding':'Same root CID lost its explicit optional selection but reused the active selected-child view; standalone denies its now-unused child owner selection, cached admission allows and reports no dependencies. Strict root context must bind exact selected closure.',
 'limits':'No final composed/runtime bypass claimed. Final used-owner validation independently rejects the unused child mapping. Production/test/B1 untouched; separate small diagnostic only.',
 'calls':calls}
out=Path(__file__).with_suffix('.json');assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'standalone_allowed':standalone['allowed'],'cached_allowed':cached['allowed'],'context_covers':covers,'B1_calls':calls_in_context,'bytes_unchanged':before==after}))
