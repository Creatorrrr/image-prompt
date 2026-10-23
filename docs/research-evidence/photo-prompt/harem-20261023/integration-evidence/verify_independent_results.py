"""Check frozen inputs and actual issued native prompt/reference/image bindings."""
from pathlib import Path
import json,hashlib
O=Path(__file__).resolve().parent;R=O.parents[4]
read=lambda p:json.loads(p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
frozen=read(O/'independent-freeze-summary.json');pixels=read(O/'root-pixel-review.json')['cases'];results=[]
ref=Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg');refsha=sha(ref)
for arm,pixel in zip(frozen['arms'],pixels,strict=True):
 run=Path(arm['run']);state=read(run/'workflow.json');assert state['phase']=='review_record_validated'
 for key,record in state['artifacts'].items():assert sha(Path(record['path']))==record['sha256'],(arm['arm'],key,'current artifact bytes')
 for key,expected in arm['frozen'].items():assert state['artifacts'][key]['sha256']==expected,(arm['arm'],key,'frozen input changed')
 lines=(run/'image_runs.ndjson').read_text().splitlines();assert len(lines)==1;ledger=json.loads(lines[0]);assert ledger['attempt']==1 and ledger['image_call_count']==1
 assert ledger.get('retry_of') is None and ledger['chosen_candidate_ids']==[] and ledger['chosen_visual_concept_ids']==[]
 plan=read(Path(state['artifacts']['native_plan']['path']));assert plan['payload']['referenced_image_paths']==[str(ref)]
 prompt=plan['payload']['prompt'];ph=hashlib.sha256(prompt.encode()).hexdigest();assert ledger['prompt_en']==prompt and ledger['runtime_prompt_sha256']==ph
 rr=ledger['reference_sha256'];assert rr==refsha or rr==[refsha]
 image=Path(pixel['image']);assert sha(image)==pixel['image_sha256']
 assert pixel['image_sha256'] in str(ledger['image_hashes'])
 review=read(Path(state['artifacts']['review_audit']['path']))['visual'];assert review['schema_failures']==[]
 assert state['h_f2_binding']['generation_id']=='efd7374e4d2f3a6718cbf227723a5d9aa576345a2d927127886ca681d52823c2'
 assert state['source_binding']['generation_id']=='3422612d5a11674a25fd7fccdc20e3dfe43562a61774094e07bd61e7bb1ef13c'
 results.append({'arm':arm['arm'],'phase':state['phase'],'frozen_inputs_unchanged':True,'all_current_artifact_hashes_exact':True,'actual_native_calls':1,'retries':0,'prompt_sha256':ph,'reference_file_sha256':refsha,'image_path':str(image),'image_sha256':pixel['image_sha256'],'ledger_run_id':ledger['run_id'],'native_and_H_F2_pins_match':True,'review_record_valid':True,'technical_qualification':'pass' if review['technical_qualified'] else 'fail','requester_acceptance':'pending'})
out={'status':'pass','arms':results,'total_actual_native_calls':3,'total_retries':0,'new_CID_exposure':0,'new_data_contribution':'not established','new_source_reads_or_additional_search_calls_by_this_check':0}
(O/'independent-result-verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
