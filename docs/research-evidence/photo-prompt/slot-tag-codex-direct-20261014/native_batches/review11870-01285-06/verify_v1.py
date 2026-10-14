"""Read-only exact batch verifier using frozen188c plus separately pinned research verifier."""
from fixture_v1 import *
D=R/'native-inputs/prepared/review11870-01285-06'
sys.path.insert(0,str(R));import direct_review as dr
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import native_reviews as nr
assert Path(nr.native.__file__).resolve().is_relative_to(G) and Path(dr.c.__file__).resolve().is_relative_to(G)
value=nr.verify_batch(str(D/'ASSIGNMENT.json'),str(O/'BATCH.json'),str(O/'NOTE.json'))
result={k:v for k,v in value.items()if k!='records'}
result.update(schema='photo-native-single06-exact-batch-verification/v1',module_paths_sha256=modules(),research_verifiers={name:{'file':str(Path(m.__file__).resolve()),'sha256':hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()}for name,m in [('direct_review',dr),('native_reviews',nr)]},frozen_generation=str(G),root_native_accepted=False,operating_count=0,actual_runtime_request_render_pixels=False,os_network_denied=True,provider_keys_absent=True,model_import_harddeny=True)
f=O/'VERIFICATION-v1.json';assert not f.exists();f.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print('VERIFY',c.digest(result),json.dumps({k:v for k,v in value.items()if k!='records'},ensure_ascii=False))
