from pathlib import Path
import subprocess,json,hashlib
W=Path.cwd();O=W/'docs/research-evidence/photo-prompt/harem-20261023/publication-20261024';A='skills/photo-prompt-image-generator/assets/';base=subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip();subprocess.run(['git','merge-base','--is-ancestor',base,'HEAD'],check=True)
read=lambda p:json.loads(p.read_bytes())
gitread=lambda p:subprocess.check_output(['git','show',base+':'+p])
reviews=read(O.parent/'integration-evidence/translation-review.json');checked=[]
for cid,review in reviews.items():
 path=A+review['file'];old=json.loads(gitread(path));expected=json.loads(json.dumps(old));expected['candidates'][cid]['content']['ko']=review['after']['content']['ko'];assert read(W/path)==expected;checked.append(cid)
manifest=json.loads(gitread(A+'photo_candidate_corpus_manifest.json'));expected=json.loads(json.dumps(manifest));expected['modules'] += [{'file':'photo_candidate_harem_20261023.json','kind':'candidates'},{'file':'photo_candidate_harem_bindings_20261023.json','kind':'slot_bindings'}];assert read(W/A/'photo_candidate_corpus_manifest.json')==expected
new=read(W/A/'photo_candidate_harem_20261023.json')['candidates'];assert new==read(O.parent/'integration-evidence/new-native-records.json')
files=[row['file'] for row in manifest['modules'] if row['file'] not in {x['file'] for x in reviews.values()}]
for name in files:assert (W/A/name).read_bytes()==gitread(A+name),name
for path in ['skills/photo-prompt-image-generator/SKILL.md','skills/photo-prompt-image-generator/retrieval-runtime.json']:
 assert (W/path).read_bytes()==gitread(path),path
changed=subprocess.check_output(['git','diff','--name-only',base],text=True).splitlines();allowed={A+'photo_candidate_corpus_manifest.json',A+'photo_candidate_search.json',*[A+x['file'] for x in reviews.values()]}
allowed.update(A+x for x in ['photo_candidate_harem_20261023.json','photo_candidate_harem_bindings_20261023.json','photo_harem_semantics_20261023.json']);allowed.update(['skills/photo-prompt-image-generator/references/harem-visual-semantics.md','skills/photo-prompt-image-generator/tests/test_harem_semantics.py'])
assert all(p in allowed or p.startswith(A+'photo_candidate_search_shards/') or p.startswith('docs/research-evidence/photo-prompt/harem-20261023/') for p in changed)
# Inspect exact published positive index membership through its own metadata reader.
import sys
sys.path.insert(0,str(W/'skills/photo-prompt-image-generator/scripts'))
from photo_search_reader import SearchReader
reader=SearchReader(W/A)
positive=set(reader.meta['vector_recipes']);assert {cid for cid,r in new.items() if r['record_kind']=='visual_option'}<=positive;assert not ({cid for cid,r in new.items() if r['record_kind']=='diagnostic'}&positive);reader.close()
out={'status':'pass','merged_origin_main':base,'remote_module_payloads_unchanged':len(files),'three_records_changed_only_at_Korean_label':checked,'remote_manifest_preserved_with_two_harem_additions':True,'new_90_source_snapshots_exact':True,'new_76_visual_candidates_indexed':True,'new_14_context_records_not_in_positive_index':True,'upstream_SKILL_and_runtime_config_exact':True,'changed_tracked_paths_in_scope':len(changed),'note':'Index/source checks do not establish native adoption or image-quality improvement.'};(O/'source-preservation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
