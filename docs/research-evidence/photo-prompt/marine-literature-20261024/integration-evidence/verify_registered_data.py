"""Read-only final registration, source preservation and exact layout binding checks."""
from pathlib import Path
import json,hashlib
O=Path(__file__).resolve().parent;R=O.parents[4];A=R/'skills/photo-prompt-image-generator/assets';S=O/'working-source-skill/assets'
read=lambda p:json.loads(p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
registration=read(O/'source-registration.json');raw=read(A/'photo_candidate_marine_literature_20261024.json')['candidates'];native=read(O/'release-new-native-records.json')
assert raw==native
bindings=read(A/'photo_candidate_marine_literature_bindings_20261024.json')['slot_bindings'];assert bindings==read(O/'release-bindings.json')['slot_bindings']
side=read(A/'photo_marine_literature_semantics_20261024.json');assert len(side['cards'])==96 and len(side['keyword_routes'])==247
assert side['card_candidate_map']==registration['card_candidate_map']
manifest=read(A/'photo_candidate_corpus_manifest.json');assert all({'file':f,'kind':kind} in manifest['modules'] for f,kind in [('photo_candidate_marine_literature_20261024.json','candidates'),('photo_candidate_marine_literature_bindings_20261024.json','slot_bindings')])
old=read(O/'protected-source-rebaseline.json');drift=[name for name,h in old.items() if sha(A/name)!=h]
source=read(S/'photo_candidate_corpus_manifest.json');names=['photo_candidate_corpus_manifest.json']+[m['file'] for m in source['modules']];different=[name for name in names if not (A/name).exists() or sha(A/name)!=sha(S/name)]
layout=sha(A/'photo_candidate_search.json')==sha(S/'photo_candidate_search.json')
result={'status':'pass' if not different and layout else 'concurrent_source_or_index_advanced','new_candidate_records_exact':len(raw),'visual_CIDs':len(registration['new_visual_ids']),'diagnostic_CIDs':len(registration['diagnostic_ids']),'bindings_exact':len(bindings),'semantic_cards':len(side['cards']),'original_seed_routes':len(side['keyword_routes']),'all_own_modules_registered':True,'own_source_sha256':{name:sha(A/name) for name in ['photo_candidate_marine_literature_20261024.json','photo_candidate_marine_literature_bindings_20261024.json','photo_marine_literature_semantics_20261024.json']},'preexisting_source_drift_since_rebaseline':drift,'source_files_compared_to_built_index':len(names),'source_files_different_from_built_index':different,'working_layout_exact':layout,'skill_sha256':sha(R/'skills/photo-prompt-image-generator/SKILL.md'),'native_approval':False,'metadata_limit':'Research owner graphs are human review metadata; no claim that all 96 cards or their relations have native pixel qualification.'}
(O/'registered-data-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
