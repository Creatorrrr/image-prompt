"""Verify saved three-arm assets and their actual run/ledger bindings, never score pixels."""
from pathlib import Path
import hashlib,json,struct
R=Path('/Users/chasoik/Projects/image-prompt');E=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_bytes())
G='3300bd369483c394610b29a53b8421934dacba4a9039e6cdd017deec7c4c26b7'
S='f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089'
ref=Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
rows=[]
for arm,sub,manifest,ledger,composed in [
 ('a','exec','run_manifest.json','image_runs.ndjson','composed-prompt.json'),
 ('b','','native-manifest.json','native-image-runs.ndjson','composed_prompt.json'),
 ('c','exec','independent-manifest.json','image-runs.ndjson','composed-prompt.json')]:
 run=R/'generated/photo-runs'/('espionage-20261023-integration-'+arm)/sub
 m=read(run/manifest);ls=[json.loads(l) for l in (run/ledger).read_text().splitlines() if l.strip()]
 assert len(ls)==1
 l=ls[0];assert l['run_id']==m['ledger_run_id'] and l['status']==m['status']=='success'
 for x in (l,m):
  assert x['image_call_count']==1 and not x['cross_arm_inputs_used']
  assert x['skill_sha256']==S and x['source_ref'].removeprefix('sealed-h-f2:')==G
  assert x['reference_sha256']==[sha(ref)]
  assert x['tool']=='image_gen' and x['generation_environment']=='native_imagegen'
 prompt=read(run/composed)['prompt_en'];h=hashlib.sha256(prompt.encode()).hexdigest()
 assert h==m['runtime_prompt_sha256']==l['runtime_prompt_sha256']
 assert (run/'final-prompt.txt').read_text().rstrip('\n')==prompt
 assert l['image_paths']==m['image_paths'] and len(m['image_paths'])==1
 image=Path(m['image_paths'][0]);assert str(image.resolve()).startswith(str(run.resolve())+'/')
 actual=sha(image);assert m['image_hashes']==l['image_hashes']==[{'path':str(image),'sha256':actual}]
 raw=image.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n' and raw[12:16]==b'IHDR';size=list(struct.unpack('>II',raw[16:24]));assert size==[1536,1024]
 root=read(E/('root-pixel-review-'+arm+'.json'));assert root['image_sha256']==actual
 rows.append({'arm':arm,'run':str(run),'manifest':str(run/manifest),'ledger':str(run/ledger),'ledger_run_id':l['run_id'],'image':str(image),'image_sha256':actual,'dimensions':size,'prompt':str(run/'final-prompt.txt'),'runtime_prompt_sha256':h,'actual_calls':1,'source_ref':G,'reference_sha256':sha(ref),'root_review':str(E/('root-pixel-review-'+arm+'.json'))})
assert sha(R/'skills/photo-prompt-image-generator/SKILL.md')==S
out={'status':'pass','scope':'Three actual saved images, manifest/ledger/prompt/reference/skill/generation bindings. Image content scored separately from original pixels.','image_calls':3,'images':3,'api_fallback_calls':0,'rows':rows}
(E/'completed-image-closure.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':out['status'],'images':3,'image_calls':3,'all_bindings_verified':True},indent=2))
