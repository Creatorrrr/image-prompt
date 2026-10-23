from pathlib import Path
import json,shutil,hashlib
R=Path('/Users/chasoik/Projects/image-prompt');W=Path('/Users/chasoik/.codex/worktrees/harem-publication-20261024/image-prompt');REL=Path('docs/research-evidence/photo-prompt/harem-20261023');A=Path('skills/photo-prompt-image-generator/assets');P=R/REL/'publication-20261024'
read=lambda p:json.loads(p.read_bytes())
write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
manifest=[]
def copy(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);manifest.append({'source':str(src),'destination':str(dst.relative_to(W)),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
skip={'build','successor-skill','successor-store','__pycache__','.runtime'}
for src in (R/REL).rglob('*'):
 if not src.is_file() or src.is_symlink() or set(src.relative_to(R/REL).parts)&skip:continue
 if src.name.endswith(('.pyc','.LOCK','.partial','.tmp')):continue
 copy(src,W/REL/src.relative_to(R/REL))
for f in ['photo_harem_semantics_20261023.json','photo_candidate_harem_20261023.json','photo_candidate_harem_bindings_20261023.json']:copy(R/A/f,W/A/f)
for f in ['references/harem-visual-semantics.md','tests/test_harem_semantics.py']:copy(R/'skills/photo-prompt-image-generator'/f,W/'skills/photo-prompt-image-generator'/f)
m=read(W/A/'photo_candidate_corpus_manifest.json');prior=list(m['modules'])
for f,kind in [('photo_candidate_harem_20261023.json','candidates'),('photo_candidate_harem_bindings_20261023.json','slot_bindings')]:
 assert not any(x['file']==f for x in m['modules']);m['modules'].append({'file':f,'kind':kind})
write(W/A/'photo_candidate_corpus_manifest.json',m);assert m['modules'][:len(prior)]==prior
reviews=read(R/REL/'integration-evidence/translation-review.json');refinements=[]
for cid,d in reviews.items():
 p=W/A/d['file'];body=read(p);record=body['candidates'][cid];assert record['content']['en']==d['before']['content']['en'],cid
 assert record['content']['ko'] in [d['before']['content']['ko'],d['after']['content']['ko']],cid
 before=json.loads(json.dumps(record));record['content']['ko']=d['after']['content']['ko'];raw=p.read_text();needle='\"ko\": '+json.dumps(before['content']['ko'],ensure_ascii=False);replacement='\"ko\": '+json.dumps(record['content']['ko'],ensure_ascii=False);assert raw.count(needle)==1;p.write_text(raw.replace(needle,replacement,1));assert read(p)==body
 assert all(record[k]==before[k] for k in record if k!='content');assert all(record['content'][k]==before['content'][k] for k in record['content'] if k!='ko')
 refinements.append({'cid':cid,'file':str(p.relative_to(W)),'before':before['content']['ko'],'after':record['content']['ko']})
for name in ['harem-20261023-independent-1','harem-20261023-independent-2','harem-20261023-independent-2b','harem-20261023-independent-3']:
 run=R/'generated/photo-runs'/name;dest=W/REL/'publication-evidence/arms'/name
 for src in run.rglob('*'):
  rel=src.relative_to(run)
  if not src.is_file() or src.is_symlink() or '__pycache__' in rel.parts or src.name.endswith(('.LOCK','.pyc')) or 'inspection-contact-crop' in src.name:continue
  if '.staging' in rel.parts:
   if rel.parts[:2]!=('.staging','h-f2'):continue
   out=dest/'issued-retrieval'/Path(*rel.parts[2:])
  else:out=dest/rel
  copy(src,out)
write(W/REL/'publication-20261024/copy-manifest.json',manifest);write(W/REL/'publication-20261024/source-delta.json',{'modules_added':m['modules'][len(prior):],'translation_refinements':refinements,'other_source_fields_changed':False,'research_and_image_copies':len(manifest)})
print({'files_copied':len(manifest),'bytes':sum((W/x['destination']).stat().st_size for x in manifest),'modified_existing_records':len(refinements)})
