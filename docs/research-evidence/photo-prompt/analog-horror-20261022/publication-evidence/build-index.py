"""Build an isolated Git v1 index; never reuse the installed v2 document recipe."""
import gc
gc.disable()
from pathlib import Path
import json,sys,os,hashlib
R=Path(sys.argv[1]).resolve();CACHE=Path(sys.argv[2]).resolve();S=R/'skills/photo-prompt-image-generator';O=R/'docs/research-evidence/photo-prompt/analog-horror-20261022/publication-evidence';sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as c
import build_shared_candidate_index as build
read=lambda p:json.loads(p.read_bytes())
write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
corpus=c.load(S/'assets');fresh=read(S/'assets/photo_candidate_analog_horror_20261022.json')['candidates'];bindings=read(S/'assets/photo_candidate_analog_horror_bindings_20261022.json')['slot_bindings']
assert len(fresh)==84 and len(bindings)==126
fresh={**fresh,**read(S/'assets/photo_candidate_analog_horror_reused_sources_20261023.json')['candidates']}
bindings={**bindings,**read(S/'assets/photo_candidate_analog_horror_reused_bindings_20261023.json')['slot_bindings']}
assert len(fresh)==85 and len(bindings)==128
assert corpus['candidates']['cand_8ed5a9486be65af9b7a3e3d39ca477fb']
base={'candidates':{k:c.digest(v) for k,v in corpus['candidates'].items() if k not in fresh},'bindings':{k:c.digest(v) for k,v in corpus['slot_bindings'].items() if k not in bindings},'slot_catalog_sha256':c.digest(corpus['slot_catalog']),'policies_sha256':c.digest(corpus['policies'])}
write(O/'base-source-preservation.json',base)
space=read(S/'assets/photo_candidate_search.json')['space'];assert space['provider']=='embeddinggemma2-local'
for key in ('OPENAI_API_KEY','GOOGLE_API_KEY','GEMINI_API_KEY','ANTHROPIC_API_KEY'):os.environ.pop(key,None)
os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',PYTHONNOUSERSITE='1')
report=build.build(S/'assets',CACHE,space=space,batch_size=32);write(O/'index-build.json',report)
after=c.load(S/'assets');assert all(c.digest(after['candidates'][k])==v for k,v in base['candidates'].items());assert all(c.digest(after['slot_bindings'][k])==v for k,v in base['bindings'].items());assert c.digest(after['slot_catalog'])==base['slot_catalog_sha256'] and c.digest(after['policies'])==base['policies_sha256']
assert all(after['candidates'][k]==v for k,v in fresh.items()) and all(after['slot_bindings'][k]==v for k,v in bindings.items())
write(O/'source-accounting.json',{'status':'pass','preserved_candidates':len(base['candidates']),'added_candidates':len(fresh),'total_candidates':len(after['candidates']),'authored_new_candidates':84,'exact_reused_prerequisite_source':1,'authored_new_bindings':126,'exact_reused_prerequisite_bindings':2,'added_positive':sum(v['record_kind']!='diagnostic' for v in fresh.values()),'added_diagnostics':sum(v['record_kind']=='diagnostic' for v in fresh.values()),'preserved_bindings':len(base['bindings']),'added_bindings':len(bindings),'total_bindings':len(after['slot_bindings']),'catalog_and_policies_unchanged':True,'source_updated_old_records':0,'scope':'Git publication source/index; installed image-test generations and primary working runtime remain unchanged'})
print(json.dumps(report),flush=True)
