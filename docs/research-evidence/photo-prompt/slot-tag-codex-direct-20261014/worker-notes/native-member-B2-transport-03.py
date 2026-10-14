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
names=['tests.test_photo_native_existing_member_scope','tests.test_photo_native_member_scope_transport','tests.test_photo_native_owner_selection','tests.test_photo_native_source_guards_v2','tests.test_photo_native_guard_role_support','tests.test_photo_native_joint_assignments']
start=time.monotonic();r=unittest.TextTestRunner(verbosity=2,resultclass=R).run(unittest.defaultTestLoader.loadTestsFromNames(names))
out=Path(__file__).with_suffix('.json');assert not out.exists()
out.write_text(json.dumps({'executions':r.testsRun,'unique':len(set(r.ids)),'subtests':r.subtests,'failures':[(t.id(),s) for t,s in r.failures],'errors':[(t.id(),s) for t,s in r.errors],'skips':[(t.id(),s) for t,s in r.skipped],'successful':r.wasSuccessful(),'calls':calls,'elapsed':time.monotonic()-start},indent=2)+'\n')
raise SystemExit(0 if r.wasSuccessful() else 1)
