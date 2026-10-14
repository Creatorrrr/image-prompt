"""Both representations, exact actual oldbinding override and all five requested roles. No source or operating updates."""
from pathlib import Path
O=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01250-01300-05');src=O/'check_01264_v1.py';exec(compile(src.read_text().split('base=core()',1)[0],str(src),'exec'))
base=core();records=[]
for view in ['full','compact']:
 for category,domains,want in [('human',[],True),('object',[],False),('object',['visual_structure'],True),('object',['visual_structure','product'],False),('human',['product'],False),('human',['jewelry'],False),('human',['food'],False),('human',['wildlife'],False)]:
  e,k=select(ent(S,cid,True,view),base,p);result=n.admission(e,k);assert result['allowed'];got=generator.core_entry_eligible(S,k,contract(category,domains),picked(category),'aftermath_trace',e);assert got==want,(view,category,domains,got)
  records.append({'view':view,'category':category,'domains':domains,'expected':want,'actual_allowed':got,'actual_entry_block_reason':generator.entry_block_reason(e,'aftermath_trace',contract(category,domains),catalog=CAT),'source_admission':result})
 # All newly source-qualified roles share this same oldbinding and complete E scope; no appearance E from part guard.
 for role in ['prop','prop_placement','prop_state','aftermath_trace','object_structure']:
  e,k=select(ent(S,cid,True,view),base,p);got=generator.core_entry_eligible(S,k,contract('object',['visual_structure']),picked('object'),role,e);assert got,(view,role)
  dims,props,_=n.permission_scope(e,k);assert set(dims)=={'pose','role','timing'}and len(props)==3
  records.append({'view':view,'requested_source_role':role,'category':'object','domains':['visual_structure'],'actual_oldbinding_consumer_allowed':got,'same_complete_E_dimensions':dims,'same_complete_E_properties':props})
mods=modules();assert mods['prompt_generator']['sha256']=='c7cba5732ef623c32ad3ac13459985fc8d1a2d00b26194d3d0ce2fd41f8c6138'
b={'schema':'photo-native-1264-final-runtime-actual-binding-override-recheck/v1','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'candidate_id':cid,'actual_binding':S['slot_bindings']['bind_'+cid[5:]],'records':records,'case_count':len(records),'module_paths_sha256':mods,'frozen_generation':str(G),'all_passed':True,'historical_188c_failedconsumer_files_immutable':True,'boundary':'Fresh149 exact current proof and same actual independently frozen C/S partgraph under corrected final50fd92. Object+visual_structure positive checked full/compact; original denied domains still reject. Every new role consumes original oldbinding guards and SAME whole E footprint, guard support adds no appearance permission. Controlled synthetic core only, no real runtime/source activation/root acceptance/pixels.','root_accepted':0,'operating':0,'source_proof_status_changes':0}
f=O/'CHECKS-01264-FULL-COMPACT-OVERRIDE-v1.json';assert not f.exists();f.write_text(json.dumps(b,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(b),hashlib.sha256(f.read_bytes()).hexdigest(),b['case_count'])
