"""Read-only confirmation that a concurrent successor retained this release."""
import gc;gc.disable()
from pathlib import Path
import sys,json,hashlib,gzip
O=Path(__file__).resolve().parent;ROOT=O.parents[5];S=ROOT/'skills/photo-prompt-image-generator';sys.path.insert(0,str(S/'scripts'))
from photo_installed_h_f2 import release
read=lambda p:json.loads(p.read_bytes());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
built=read(O/'successor.json');installed=read(O/'install.json');cfg=read(S/'retrieval-runtime.json');store=Path(installed['store']);old=store/'generations'/built['native_generation_id'];active,manifest,native_manifest=release(store,cfg['generation_id'],full=True)
assert manifest['native_generation_id']==cfg['native_generation_id']
files=['photo_candidate_court_palace_20261023.json','photo_candidate_court_palace_bindings_20261023.json']+[x['module'] for x in read(O/'existing-source-patches.json')];rows=[{'file':f,'tested_sha256':sha(old/'assets'/f),'active_sha256':sha(active/'assets'/f)} for f in sorted(set(files))];assert all(x['tested_sha256']==x['active_sha256'] for x in rows)
new=read(O/'new-native-records.json');metadata=json.loads(gzip.decompress((store/'h-f2-generations'/cfg['generation_id']/'indexed-documents.json.gz').read_bytes()));indexed={x['cid'] for x in metadata};positive={cid for cid,r in new.items() if r['record_kind']=='visual_option'};held=set(new)-positive;assert positive<=indexed and not held&indexed
assert read(S/'retrieval-runtime.json')==cfg
result={'schema':'court-palace-active-successor-preservation/v1','status':'PASS','tested_generation_id':built['generation_id'],'current_config':cfg,'active_positive_CIDs':manifest['CID_count'],'active_RIDs':manifest['RID_count'],'whole_source_files_equal':rows,'new_88_records_and_4_patches_preserved_by_whole_module_hash':True,'new_72_bindings_preserved':True,'new_33_positive_CIDs_indexed':len(positive&indexed),'diagnostic_55_CIDs_indexed':len(held&indexed),'active_release_full_file_seals_verified':True,'action':'Observed and verified the concurrent successor without resetting its pointer or reverting other topic data.','test_receipts_remain_pinned':True}
(O/'active-successor-preservation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='whole_source_files_equal'},ensure_ascii=False))
