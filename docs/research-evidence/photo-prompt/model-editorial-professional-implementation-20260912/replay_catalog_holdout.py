from pathlib import Path
import json,tempfile,hashlib,sys,time
ROOT=Path.cwd();sys.path.insert(0,str(ROOT));from tests.test_photo_visual_obligations import PhotoVisualObligationTests,ROUTING_HOLDOUT_PATH
OUT=ROOT/'docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912';rows=[json.loads(l) for l in ROUTING_HOLDOUT_PATH.read_text().splitlines() if l.strip()];case=next(r for r in rows if r['id']=='holdout_negative_tailoring');start=time.monotonic();PhotoVisualObligationTests.setUpClass();test=PhotoVisualObligationTests('test_frozen_visual_concept_routing_holdout')
with tempfile.TemporaryDirectory() as directory:
 p=Path(directory)/ROUTING_HOLDOUT_PATH.name;p.write_text(json.dumps(case)+'\n');test.assert_routing_fixture(p)
result={'status':'PASS','case_id':case['id'],'case':case,'original_fixture_sha256':hashlib.sha256(ROUTING_HOLDOUT_PATH.read_bytes()).hexdigest(),'test_logic':'Unchanged PhotoVisualObligationTests.assert_routing_fixture applied to an exact copy of the one failed case. Original fixture remains unchanged.','seconds':round(time.monotonic()-start,2),'image_generation':False}
(OUT/'post-correction-holdout.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS',case['id'])
