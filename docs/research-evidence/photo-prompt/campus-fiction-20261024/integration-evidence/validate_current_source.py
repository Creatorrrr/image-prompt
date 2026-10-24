"""Read-only full validation of the current active union layout after concurrent rebuild."""
import gc,json,sys,hashlib
from pathlib import Path
gc.disable()
S=Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator');O=Path(__file__).resolve().parent;sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as c,photo_search_layout as layout
from validate_photo_prompt_dictionary import validate_source_corpus
source=c.load(S/'assets');mp=S/'assets'/layout.MANIFEST;before=mp.read_bytes();manifest=json.loads(before);build=json.loads((O/'working-index-final.json').read_bytes())
assert manifest['corpus_sha256']==c.digest(source)
(O/'concurrent-layout-observation.json').write_text(json.dumps({'own_verified_layout':build['build']['layout_id'],'active_layout':manifest['layout_id'],'same_source_sha256':manifest['corpus_sha256'],'reason':'Another writer built the same source union after our activation; full active validation rerun rather than claiming own layout remains active.'},indent=2)+'\n')
errors=validate_source_corpus(S,source)
assert mp.read_bytes()==before,'Active layout changed during validation'
assert c.digest(c.load(S/'assets'))==manifest['corpus_sha256'],'Source changed during validation'
fresh=json.loads((O/'new-native-records.json').read_bytes());assert all(source['candidates'][k]==v for k,v in fresh.items())
r={'status':'pass' if not errors else 'fail','scope':'Full current dictionary and active layout closure validation, with source/layout unchanged before and after.','native_candidates':len(source['candidates']),'bindings':len(source['slot_bindings']),'positive_candidates':manifest['metadata']['count'],'layout_id':manifest['layout_id'],'corpus_sha256':manifest['corpus_sha256'],'campus_exact_records':len(fresh),'errors':errors}
(O/'source-validation.final.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True);assert not errors
