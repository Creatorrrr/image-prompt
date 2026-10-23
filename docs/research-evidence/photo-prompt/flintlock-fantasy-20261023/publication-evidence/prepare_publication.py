from pathlib import Path
import copy, hashlib, json, os, re, shutil, subprocess, datetime

ROOT=Path('/Users/chasoik/Projects/image-prompt')
WT=Path('/Users/chasoik/.codex/worktrees/flintlock-publication/image-prompt')
TASK=ROOT/'generated/maintenance/flintlock-publication-20261023'
REL=Path('docs/research-evidence/photo-prompt/flintlock-fantasy-20261023')
OLD=ROOT/REL; NEW=WT/REL; IN=OLD/'integration-evidence'
AS=Path('skills/photo-prompt-image-generator/assets')
def read(p):return json.loads(p.read_bytes())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

# The primary checkout stays in place. Record all non-ignored unrelated bytes,
# staged entries and explicit private/runtime selections before publication.
names=subprocess.check_output(['git','ls-files','-z','--cached','--others','--exclude-standard'],cwd=ROOT).decode().split('\0')
protected={}
own_new={str(AS/n) for n in ['photo_candidate_flintlock_fantasy_20261023.json','photo_candidate_flintlock_fantasy_bindings_20261023.json','photo_flintlock_fantasy_semantics_20261023.json']}
own_new.add('skills/photo-prompt-image-generator/references/flintlock-fantasy-semantics.md')
for name in sorted(set(names)-{''}):
 if name.startswith(str(REL)+'/') or name in own_new:continue
 p=ROOT/name
 protected[name]={'kind':'symlink','target':os.readlink(p)} if p.is_symlink() else {'kind':'file','sha256':sha(p)} if p.is_file() else {'kind':'absent'}
extra={}
for p in [ROOT/'.env',ROOT/'skills/photo-prompt-image-generator/retrieval-runtime.json',ROOT/'skills/photo-prompt-image-generator/embedding-runtime.lock.json',*Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime').rglob('CURRENT.json')]:
 if p.is_file():extra[str(p)]=sha(p)
write(TASK/'primary-before.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'protected':protected,'extra':extra,'index_stage':subprocess.check_output(['git','ls-files','--stage','-z'],cwd=ROOT).decode(),'staged_diff':subprocess.check_output(['git','diff','--cached','--binary'],cwd=ROOT).decode(),'own_new':sorted(own_new)})

# Keep research and compact immutable execution evidence; omit model copies,
# temporary indexes and request caches from the commit.
NEW.mkdir(parents=True,exist_ok=True)
for p in OLD.iterdir():
 if p.is_file():shutil.copy2(p,NEW/p.name)
(NEW/'integration-evidence').mkdir(exist_ok=True)
for p in IN.iterdir():
 if p.is_file() and p.stat().st_size:shutil.copy2(p,NEW/'integration-evidence'/p.name)
shutil.copytree(IN/'coordinator-inputs',NEW/'integration-evidence/coordinator-inputs')
mapping=[]
for arm in 'abc':
 run=ROOT/('generated/photo-runs/flintlock-fantasy-20261023-'+arm);target=NEW/'image-test-evidence'/arm
 for p in run.rglob('*'):
  if not p.is_file() or p.suffix not in {'.json','.jsonl','.ndjson','.md','.txt'}:continue
  rel=p.relative_to(run)
  if any(x in {'.staging','__pycache__'} for x in rel.parts):continue
  dest=target/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
  mapping.append({'original':str(p),'archive':str(dest.relative_to(WT)),'sha256':sha(p)})
write(NEW/'image-test-evidence/ARCHIVE-MAP.json',{'files':mapping,'generated_images':'Original native images and complete managed run history remain local; no reference portrait or generated raster is added to Git. Exact image hashes are retained in manifests and image-file-validation.json.'})

for name in ['photo_candidate_flintlock_fantasy_20261023.json','photo_candidate_flintlock_fantasy_bindings_20261023.json','photo_flintlock_fantasy_semantics_20261023.json']:
 shutil.copy2(ROOT/AS/name,WT/AS/name)
reference=Path('skills/photo-prompt-image-generator/references/flintlock-fantasy-semantics.md')
shutil.copy2(ROOT/reference,WT/reference)

# Change only the two reviewed translation/discovery fields, retaining every
# other byte in each shared module from the publication base.
changes=read(IN/'changed-native-records.json');receipts=[]
module_for={'cand_fc38c2780414540280a85f200fec999e':0,'cand_9c0d3821b9ae5cc49781a59f278b4f29':2,'cand_e55f66332e315f20bf90ddbb61f8d36b':6,'cand_f25347e368185c8780231631bf099418':10,'cand_42d2b29291fe52db93a6bf09617d266e':13}
for cid,new in changes.items():
 p=WT/AS/f'photo_candidate_candidates_{module_for[cid]:03d}.json';text=p.read_text();start=text.index('{',text.index('"'+cid+'":'));record,offset=json.JSONDecoder().raw_decode(text[start:]);end=start+offset;segment=text[start:end]
 assert record['content']['en']==new['content']['en'],cid+' English source changed'
 expected=copy.deepcopy(record)
 for field in ['ko','embedding_text']:
  pattern=r'("'+field+r'"\s*:\s*)("(?:\\.|[^"\\])*")';matches=list(re.finditer(pattern,segment));assert len(matches)==1
  match=matches[0];assert json.loads(match.group(2))==record['content'][field]
  value=json.dumps(new['content'][field],ensure_ascii=False);segment=segment[:match.start(2)]+value+segment[match.end(2):];expected['content'][field]=new['content'][field]
 assert json.loads(segment)==expected
 p.write_text(text[:start]+segment+text[end:]);receipts.append({'candidate_id':cid,'file':str(p.relative_to(WT)),'changed_fields':['content.ko','content.embedding_text'],'all_other_fields_and_bytes_preserved':True})

manifest=WT/AS/'photo_candidate_corpus_manifest.json';m=read(manifest)
for name,kind in [('photo_candidate_flintlock_fantasy_20261023.json','candidates'),('photo_candidate_flintlock_fantasy_bindings_20261023.json','slot_bindings')]:
 assert not any(x['file']==name for x in m['modules']);m['modules'].append({'file':name,'kind':kind})
write(manifest,m)
maintenance=Path('skills/photo-prompt-image-generator/references/maintenance.md');paragraph=re.search(r'The \[flintlock fantasy extension\].*?separate results\.',(ROOT/maintenance).read_text(),re.S).group()
base=(WT/maintenance).read_text();assert '[flintlock fantasy extension]' not in base;(WT/maintenance).write_text(base.rstrip()+'\n\n'+paragraph+'\n')

# Make report links to text evidence portable. Images stay at their delivered
# local paths and are explicitly identified as local retained deliverables.
report=NEW/'INTEGRATION-RESULTS.md';text=report.read_text()
for row in mapping:
 text=text.replace(']('+row['original']+')',']('+str(Path(row['archive']).relative_to(REL))+')')
text=text.replace('현재 작업 소스에는 동시 작업을 포함한 20,703 CID','이미지 통합시험 종료 시 작업 소스에는 동시 작업을 포함한 20,703 CID')
text=text.replace('이번 작업에서 전역 기본판 활성화, 커밋, 푸시, PR, 배포는 실행하지 않았다.','이미지 통합시험 종료 시에는 전역 기본판 활성화, 커밋, 푸시, PR, 배포를 실행하지 않았다. 후속 Git 발행 상태는 [PUBLICATION.md](PUBLICATION.md)를 따른다.')
text=text.replace('이번 작업은 커밋·푸시·PR을 만들지 않았다.','이미지 통합시험 당시에는 커밋·푸시·PR을 만들지 않았다. 후속 발행은 [PUBLICATION.md](PUBLICATION.md)에 기록한다.')
text=text.replace('이 문서는 이번 작업의 소스 반영, 검색 검증, 실제 생성물 검토를 연결한다.','이 문서는 이미지 통합시험 시점의 소스 반영, 검색 검증, 실제 생성물 검토를 연결한다. 이후 Git 발행·병합 검증은 [PUBLICATION.md](PUBLICATION.md)에 별도로 기록한다.')
text+='\n생성 이미지와 원본 참조는 로컬 전달 결과로 보존하며 Git에 추가하지 않았다. 저장소의 `image-test-evidence/`에는 실제 프롬프트, 고정 기준, 판정, 감사 및 해시 증거를 보존했다.\n';report.write_text(text)
original=NEW/'integration-evidence/SHA256SUMS.integration'
if original.exists():original.rename(original.with_suffix('.integration.original'))
write(NEW/'publication-evidence/source-extraction.json',{'base':subprocess.check_output(['git','rev-parse','HEAD'],cwd=WT,text=True).strip(),'new_records':73,'new_visual':52,'new_diagnostics':21,'new_bindings':99,'refined_CIDs':receipts,'excluded':'Other dirty primary sources, code, runtime selector and mixed working index; staging/model/cache directories','compact_native_evidence_files':len(mapping)})
write(TASK/'publication-allowlist-initial.json',[str(p.relative_to(WT)) for p in NEW.rglob('*') if p.is_file()]+sorted(own_new)+[str(manifest.relative_to(WT)),str(maintenance)]+[x['file'] for x in receipts])
print(json.dumps({'protected_primary_paths':len(protected),'copied_native_text_evidence':len(mapping),'source_extraction':'pass','worktree':str(WT)}))
