from pathlib import Path
import hashlib,json
R=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).parent;rd=lambda p:json.loads(p.read_bytes());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 cfg=rd(R/'skills/photo-prompt-image-generator/retrieval-runtime.json');s=rd(O/'successor.json');assert cfg['generation_id']==s['generation_id'];skill=sha(R/'skills/photo-prompt-image-generator/SKILL.md');ref=sha(Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg'));rows=[]
 for a in ['a','b2','c']:
  r=R/'generated/photo-runs'/('surreal-expansion-20261024-'+a);w=rd(r/'workflow.json');m=rd(r/'run_manifest.json');assert w['phase']=='review_record_validated';assert w['h_f2_binding']['generation_id']==cfg['generation_id'];assert m['skill_sha256']==skill and m['reference_sha256']==[ref];assert m['image_call_count']==1 and m['cross_arm_inputs_used'] is False
  assert all(sha(Path(v['path']))==v['sha256'] for v in m['image_hashes']);assert len(m['image_hashes'])==1
  render=rd(Path(w['artifacts']['render_request']['path']));runtime=render['runtime_prompt_en'];assert hashlib.sha256(runtime.encode()).hexdigest()==m['runtime_prompt_sha256'];aud=rd(Path(w['artifacts']['review_audit']['path']));core=rd(Path(w['artifacts']['authorial_core']['path'])) if 'authorial_core' in w['artifacts'] else None
  row={'arm':a,'phase':w['phase'],'manifest':str(r/'run_manifest.json'),'ledger_run_id':m['ledger_run_id'],'image_calls':1,'image_hashes_verified':True,'runtime_prompt_hash_verified':True,'reference_hash_verified':True,'skill_hash_verified':True,'generation_id':w['h_f2_binding']['generation_id'],'review_audit':aud,'technical_qualified':aud['visual']['technical_qualified'],'no_cross_arm_input_declared':True};rows.append(row)
 original=rd(R/'generated/photo-runs/surreal-expansion-20261024-b/workflow.json');assert not original.get('h_f2_binding') and 'native_plan' not in original['artifacts']
 out={'status':'pass_evidence_integrity','active_generation':cfg['generation_id'],'actual_image_calls':sum(x['image_calls'] for x in rows),'original_duplicate_b_calls':0,'requester_acceptance':'not_yet_received','pixel_review':'coordinator-pixel-review.json','native_complete_new_source_qualification':'NOT_TESTED','arms':rows};(O/'FINAL-VALIDATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':out['status'],'calls':out['actual_image_calls'],'review_statuses':[(x['arm'],x['technical_qualified']) for x in rows]}))
if __name__=='__main__':main()
