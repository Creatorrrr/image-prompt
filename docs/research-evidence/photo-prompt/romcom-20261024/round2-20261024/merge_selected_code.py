from pathlib import Path
import json,sys,shutil
O=Path(__file__).resolve().parent;R=Path('/Users/chasoik/Projects/image-prompt');S=R/'skills/photo-prompt-image-generator';sys.path.insert(0,str(S/'scripts'))
from stage_photo_h_f2_code import stage
read=lambda p:json.loads(p.read_bytes())
b=read(O/'BASELINE.json');cur={'schema':'photo-installed-h-f2/v1','policy':'photo-h-f2/v1','store_subdirectory':'h-f2-installed','generation_id':'4a05dd82d952b3df246e9d0375a2e4c91a4e7a3cca6a7d3e15fbfb4d3ffc2878','native_generation_id':'987f06480d79a68c492250334ae610e0665f7abc9475358dd7d01c11cf83240a','code_sha256':'b6536c01e6853044b4ca4c6a53277699123be192134f8c6ff8c76e79a91b4653'};n=Path(b['store'])/'generations'/cur['native_generation_id'];old=read(Path(b['native'])/'manifest.json');new=read(n/'manifest.json')
assert all(old['source'][k]==new['source'][k] for k in old['source'] if k!='code'),'Concurrent source changed; requires merged-data rebuild'
changed=[k for k,v in new['source']['code'].items() if old['source']['code'].get(k)!=v]
assert 'scripts/prepare_retry_context.py' not in changed,'Retry code needs explicit merge'
(O/'MERGE-BASELINE.json').write_text(json.dumps({'config':cur,'source_assets_embedding_environment_exactly_same':True,'inherited_current_sealed_members':changed},indent=2)+'\n')
overlay=O/'selected-code-overlay'
for rel in changed:
 p=overlay/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(n/rel,p)
parent=read(O/'code-successor.json');result=stage(O/'merged-successor-store',source_store=parent['store'],generation_id=parent['generation_id'],members=changed,overlay_root=overlay)
(O/'merged-successor.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
