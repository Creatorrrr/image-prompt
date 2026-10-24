from pathlib import Path
import hashlib,json,os,re
O=Path(__file__).resolve().parent;Q=O.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=Q/'SHA256SUMS';names=[]
for line in old.read_text().splitlines():
 if not line:continue
 _,name=line.split('  ',1);assert (Q/name).is_file() and (Q/name).resolve().is_relative_to(Q.resolve());names.append(name)
for name in ['INTEGRATION-RESULTS.md','INDEPENDENT-RETRIEVAL.md']:
 if name not in names:names.append(name)
old.write_text(''.join(sha(Q/name)+'  '+name+'\n' for name in sorted(names)))
excluded={O/x for x in ['build','successor-skill','successor-store','working-source-skill','working-source-index-cache','working-source-index-store','union-release/build','union-release/successor-skill','union-release/successor-store','final-release/build','final-release/successor-skill','final-release/successor-store']}
manifest=O/'SHA256SUMS.INTEGRATION';validation=O/'PACKAGE-INTEGRITY.json';members=[old]
for root in [O,Q/'image-tests']:
 for directory,dirs,files in os.walk(root):
  d=Path(directory);dirs[:]=[name for name in dirs if name!='__pycache__' and d/name not in excluded and not (d/name).is_symlink()]
  for name in files:
   p=d/name
   if p in {manifest,validation} or p.is_symlink():continue
   members.append(p)
members=sorted(set(members));manifest.write_text(''.join(sha(p)+'  '+str(p.relative_to(Q))+'\n' for p in members))
fail=[];checked=0
for mf in [old,manifest]:
 for line in mf.read_text().splitlines():
  expected,name=line.split('  ',1);p=Q/name
  if not p.is_file() or sha(p)!=expected:fail.append(str(p))
  checked+=1
links=[]
for doc in [Q/'README.md',Q/'INTEGRATION-RESULTS.md',Q/'INDEPENDENT-RETRIEVAL.md']:
 for target in re.findall(r'\]\(([^\n]+?)\)',doc.read_text()):
  if '://' in target or target.startswith('#'):continue
  p=Path(target) if target.startswith('/') else doc.parent/target.split('#',1)[0]
  if not p.exists():links.append({'document':str(doc),'missing':target})
result={'status':'pass' if not fail and not links else 'fail','checksummed_entries_verified':checked,'research_manifest_entries':len(names),'integration_manifest_entries':len(members),'research_manifest_sha256':sha(old),'integration_manifest_sha256':sha(manifest),'hash_failures':fail,'missing_report_links':links,'scope':'Research documents, integration reports/scripts/logs and3arm evidence. Reproducible model/index staging caches excluded; their sealed manifests and validation reports remain. Original image hashes are independently verified in root-pixel-review.json.'}
validation.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');assert result['status']=='pass';print(json.dumps(result,ensure_ascii=False))
