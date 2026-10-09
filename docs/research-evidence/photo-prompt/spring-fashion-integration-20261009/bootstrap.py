"""Capture an owned baseline and prepare three immutable user-text envelopes."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess

PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
WORKTREE = Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt')
OUT = Path(__file__).resolve().parent
REQUEST = '시각 의미 데이터와 후보 데이터에 반영해줘. 그 다음 스킬의 최신 버전을 사용하여 독립된 서브에이전트 3개에서 각각 서로 다른 컨셉으로 이번에 반영한 주제가 이미지에 실제로 반영되는지까지 테스트할 수 있는 랜덤한 복잡한 컨셉을 정하여 테스트케이스를 마련하고 첨부한 이미지를 활용하여 프롬프트 작성하고 이미지 생성하도록 하여 잘 반영되었는지 테스트해줘.'
REFERENCE = Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda:handle.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

tracked=subprocess.check_output(['git','ls-files','-z'],cwd=PRIMARY).decode().split('\0')
baseline={p:sha(PRIMARY/p) for p in tracked if p and (PRIMARY/p).is_file()}
write(OUT/'PRIMARY-BEFORE.json',{'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=PRIMARY).decode().strip(),
    'status_porcelain':subprocess.check_output(['git','status','--porcelain=v1','-z','--untracked-files=all'],cwd=PRIMARY).decode(),
    'tracked_sha256':baseline,'scope':'Pre-integration baseline; research writes only its declared owned paths.'})

# Worktree authoring begins with the current edited authored corpus and its
# indexes, rather than silently dropping registered dirty/untracked sources.
source_assets=PRIMARY/'skills/photo-prompt-image-generator/assets'
target_assets=WORKTREE/'skills/photo-prompt-image-generator/assets'
copied=[]
for source in source_assets.rglob('*'):
    if not source.is_file():continue
    relative=source.relative_to(source_assets)
    target=target_assets/relative
    before_hash=sha(source)
    if not target.is_file() or sha(target)!=before_hash:
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    if sha(source)!=before_hash or sha(target)!=before_hash:raise RuntimeError(f'Concurrent baseline drift: {relative}')
    copied.append({'path':str(relative),'sha256':before_hash})
write(OUT/'WORKTREE-BASELINE.json',{'source':str(source_assets),'target':str(target_assets),'files':copied,
    'skill_sha256':sha(PRIMARY/'skills/photo-prompt-image-generator/SKILL.md'),
    'worktree_skill_sha256':sha(WORKTREE/'skills/photo-prompt-image-generator/SKILL.md'),
    'reference':str(REFERENCE),'reference_sha256':sha(REFERENCE)})
assert sha(PRIMARY/'skills/photo-prompt-image-generator/SKILL.md')==sha(WORKTREE/'skills/photo-prompt-image-generator/SKILL.md')
write(OUT/'SOURCE-BASELINE.json',{'files':[{**r,'bytes':(source_assets/r['path']).stat().st_size} for r in copied],
    'note':'All before-source bytes remain in primary until the identity-preserving application; hashes bind the snapshot.'})

spans=[]
for name,text in [('concept_scope','서로 다른 컨셉으로 이번에 반영한 주제가 이미지에 실제로 반영되는지까지 테스트할 수 있는 랜덤한 복잡한 컨셉을 정하여'),
                  ('reference_use','첨부한 이미지를 활용하여')]:
    start=REQUEST.index(text);spans.append({'span_id':name,'start':start,'end':start+len(text),'text':text})
request_sha=hashlib.sha256(REQUEST.encode()).hexdigest()
for arm in ['knit_layer','bodice_hem','ornament_shoe']:
    folder=OUT/'arms'/arm;folder.mkdir(parents=True,exist_ok=True)
    (folder/'request.txt').write_bytes(REQUEST.encode())
    write(folder/'request_envelope.json',{'contract_version':'photo-request-envelope/v1','provenance':'requesting_user',
        'request_id':f'spring-fashion-{arm}-20261009','request_text':REQUEST,'request_sha256':request_sha,'active_spans':spans})
    write(folder/'spans.json',[{k:s[k] for k in ('span_id','start','end')} for s in spans])
write(OUT/'DELEGATION-REQUEST.json',{'request_text':REQUEST,'request_sha256':request_sha,
    'arms':{arm:{'envelope_path':str(OUT/'arms'/arm/'request_envelope.json'),
                'envelope_file_sha256':sha(OUT/'arms'/arm/'request_envelope.json')} for arm in ['knit_layer','bodice_hem','ornament_shoe']},
    'note':'Topic allocation and independent scene staging are coordinator/agent choices, not extra requester spans.'})
print(json.dumps({'tracked_baseline':len(baseline),'asset_files_bound':len(copied),'worktree':str(WORKTREE),
    'request_sha256':request_sha,'envelopes':{arm:sha(OUT/'arms'/arm/'request_envelope.json') for arm in ['knit_layer','bodice_hem','ornament_shoe']}},indent=2))
