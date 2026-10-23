from pathlib import Path
import json,hashlib,os
R=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent;E=O.parent/'integration-evidence';STORE=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed')
read=lambda p:json.loads(p.read_bytes())
H={'efd7374e4d2f3a6718cbf227723a5d9aa576345a2d927127886ca681d52823c2','d63b465fe1471d65ffdf0765b2d67dcc4b9d88b85202866093100f1564aa2240'}
N={'3422612d5a11674a25fd7fccdc20e3dfe43562a61774094e07bd61e7bb1ef13c','fdce7240c730b42c5263a03c3fabff8c3c8ebe7d0c7b594adbca1e6da52605bd'}
own_runs={'harem-20261023-independent-1','harem-20261023-independent-2','harem-20261023-independent-2b','harem-20261023-independent-3'}
used_H=set();used_N=set();protected=[]
for root,dirs,files in os.walk(R/'generated/photo-runs'):
 dirs[:]=[x for x in dirs if x not in ['.runtime','successor-skill','successor-store','build','__pycache__','.staging']]
 if 'workflow.json' not in files:continue
 p=Path(root)/'workflow.json'
 if any(x in own_runs for x in p.parts):continue
 try:
  d=read(p);h=(d.get('h_f2_binding') or {}).get('generation_id');n=(d.get('source_binding') or {}).get('generation_id')
  if h in H:used_H.add(h);protected.append({'run':str(p),'H_F2':h})
  if n in N:used_N.add(n);protected.append({'run':str(p),'native':n})
 except (ValueError,KeyError):pass
c=read(R/'skills/photo-prompt-image-generator/retrieval-runtime.json');used_H.add(c['generation_id']);used_N.add(c['native_generation_id'])
targets=[]
for base in [E,E/'latest-default-successor',E/'final-default-successor']:
 for name in ['build','successor-skill','successor-store']:
  p=base/name
  if p.exists():targets.append({'path':str(p),'kind':'private_duplicate_build_tree'})
for name in own_runs:
 p=R/'generated/photo-runs'/name
 for child in ['.staging','.LOCK','inspection-contact-crop.png']:
  q=p/child
  if q.exists():targets.append({'path':str(q),'kind':'archived_run_temporary'})
for gid in sorted(H-used_H):
 p=STORE/'h-f2-generations'/gid
 if p.exists():targets.append({'path':str(p),'kind':'retired_private_H_F2_cache'})
for gid in sorted(N-used_N):
 p=STORE/'generations'/gid
 if p.exists():targets.append({'path':str(p),'kind':'retired_private_native_cache'})
for p in [Path('/tmp/harem-commit-20261024.log'),Path('/tmp/harem-merge-20261024.log')]:
 if p.exists():targets.append({'path':str(p),'kind':'temporary_git_log'})
# Only these exact image-tool originals are duplicate cache files; original user portrait is excluded.
for path,sha in [('/Users/chasoik/.codex/generated_images/01a1691f-cc4a-77d0-bab2-85da8a126f8c/exec-77b0e179-265a-4b20-9454-359ebedcb47a.png','56eeb97852c9459bd6275c799440b8836007f2748d90b8511cebd84c3670996b'),('/Users/chasoik/.codex/generated_images/01a16920-02fd-71b0-8f0f-304db3660596/exec-0dbdf7ad-591f-4c31-b790-c3e454d3b199.png','2e79610d334853baddd79c3c468881666d53a32fcecfaea316ace3d0a978c99b'),('/Users/chasoik/.codex/generated_images/01a16920-3cbc-76b1-92e5-68a813f9b5a5/exec-d9e17039-4403-4a6c-a727-db9b9459f873.png','fa447190158223766f532e2e139e71ed539685186106ab86f7392fcb7d9d5b8c')]:
 p=Path(path)
 if p.exists():assert hashlib.sha256(p.read_bytes()).hexdigest()==sha;targets.append({'path':str(p),'kind':'duplicated_tool_image_cache','sha256':sha})
plan={'status':'planned_only_NOT_DELETED','requires':'Successful main push plus remote ancestry/SHA verification, verified archive copies, recheck active/reference usage.','targets':targets,'protected_external_references':protected,'active_runtime_preserved':c,'preserved':['original user portrait','original three generated deliverable PNGs','research and image evidence','shared embedding model and Python environment','unrelated working changes and worktrees']}
(O/'cleanup-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');print({'private_cleanup_targets':len(targets),'protected_other_run_references':len(protected),'retired_cache_targets':[x['path'] for x in targets if 'retired_' in x['kind']]})
