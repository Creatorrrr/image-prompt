#!/usr/bin/env python3
"""Validate local research references and selected contract fields, without runtime mutation."""
import collections, hashlib, json, pathlib, re, subprocess, sys

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_semantics as cs
import visual_profile_contracts as vc

def read(name): return json.loads((HERE/name).read_text())
def dump(name,obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
inv=read('keyword-inventory.json')
audit=read('current-data-audit.json')
sem=read('semantic-records.json')
coverage=read('coverage-ledger.json')
sources=read('sources.json')
bp=read('profile-candidate-blueprints.json')
qual=read('qualification-plan.json')

for name in ['keyword-inventory.json','current-data-audit.json','semantic-records.json','coverage-ledger.json','sources.json','profile-candidate-blueprints.json','qualification-plan.json','referenced-conversation-cached.json']:
    read(name)
kid={k['id'] for k in inv['keywords']}
sid={s['id'] for s in sources['sources']}
rid={r['id'] for r in sem['records']}
assert len(kid)==len(inv['keywords'])
assert len(sid)==len(sources['sources'])
assert len(rid)==len(sem['records'])
assert len(inv['keywords'])==audit['keyword_count']==len(coverage['keywords'])
assert kid=={k['keyword_id'] for k in audit['keywords']}=={k['keyword_id'] for k in coverage['keywords']}
for r in sem['records']:
    assert set(r['source_ids'])<=sid
    assert set(r['keyword_ids_exactly_mapped'])<=kid
    assert r['primary_slot_proposal'] in audit['relevant_slots']
    assert len(r['candidate_phrase_drafts'])==2
    assert r['runtime_ready'] is False
for k in coverage['keywords']: assert set(k['research_record_ids'])<=rid
assert sem['counts']==coverage['counts']
assert all(f['scope_covered'] for f in coverage['families'])
assert all(k['runtime_qualification']=='not_tested' for k in coverage['keywords'])
assert len(qual['cases'])==qual['case_count']
assert len(qual['pixel_arms'])==qual['pixel_arm_count']
assert all(c['state']=='planned_not_executed' for c in qual['cases'])
assert len({c['id'] for c in qual['cases']})==len(qual['cases'])

slots=collections.defaultdict(list)
gate_ids=[]
for b in bp['blueprints']:
    p=b['profile_draft']
    vc.validate_hard_activation(p['activation']['hard_activation'])
    compiled=vc.compile_visual_profile(p)
    gate_ids.extend(g['id'] for g in compiled['render_gates'])
    slots[b['slot_proposal']].append(b['candidate_draft'])
    assert b['qualification']['routing']=='not_tested'
    b['qualification']['schema_subset']='passed_authored_components_hard_activation_candidate_relations_only'
assert len(gate_ids)==len(set(gate_ids))
cs.validate_candidate_entries({'slots':dict(slots)}, {'appearance'})
dump('profile-candidate-blueprints.json',bp)

before=audit['source_hashes_before']
after={path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in before}
changed=[p for p in before if before[p]!=after[p]]
assert not changed, changed
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==audit['git_head']
tracked_diff=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT,text=True).splitlines()
assert not tracked_diff, tracked_diff

# The family table does not promote partial source coverage into qualification.
lines=['| 분류 | 원문 분류 | 용어 항목 | 설계 레코드 | 용어 연결 | 정의 후속 확인 |',
       '|---|---|---:|---:|---:|---:|']
for f in coverage['families']:
    lines.append(f"| {f['section']} | {f['name']} | {f['seed_terms']} | {f['record_count']} | {f['specific_keyword_mappings']} | {len(f['definition_backlog_keywords'])} |")
report=HERE/'research-report.md'
body=report.read_text()
if '<!-- GENERATED_FAMILY_TABLE -->' in body:
    report.write_text(body.replace('<!-- GENERATED_FAMILY_TABLE -->','\n'.join(lines)))

status_names={'body_read':'본문 확인','index_only':'색인만 확인','search_excerpt_only':'검색 발췌 확인','blocked_human_verification':'본문 차단'}
srcmd=['# 출처와 확인 범위','',
       '각 자료가 직접 지지하는 사실만 아래에 요약했다. 시각 후보·게이트는 별도로 작성한 연구자 적용안이다. 외부 표본의 픽셀 검토는 이번에 실행하지 않았다.','',
       '| ID | 자료 | 조회 범위 | 확인 사실 | 사용 한계 |','|---|---|---|---|---|']
for s in sources['sources']:
    srcmd.append(f"| {s['id']} | [{s['title']}]({s['url']}) | {status_names[s['retrieval_status']]} | {s['supported_claim']} | {s['limit']} |")
(HERE/'sources.md').write_text('\n'.join(srcmd)+'\n')

artifact_refs=[m[1] for m in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',report.read_text())]
artifact_refs += [m[1] for m in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',(HERE/'integration-plan.md').read_text())]
missing=[]
for target in artifact_refs:
    if '://' in target or target.startswith('/'): continue
    if not (HERE/target.split('#')[0]).exists() and target!='artifact-validation.json': missing.append(target)
assert not missing, missing

validation={
    'schema_version':'clothing-artifact-validation/v1','as_of':'2026-10-01',
    'result':'pass','counts':sem['counts'],'blueprints':len(bp['blueprints']),'authored_render_gates':len(gate_ids),
    'qualification_cases_planned':len(qual['cases']),'pixel_arms_planned':len(qual['pixel_arms']),
    'checks':['research JSON syntax','unique IDs','cross-file keyword/record/source references',
        'all conversation families have a scope record','counts and source status remain separate from qualification',
        'candidate slot proposals exist in the current merged data',
        '15 blueprint hard_activation and authored_components contract subsets compile',
        'candidate concept_units/relations/affected_dimensions subset validates',
        'local report and plan links resolve','snapshotted runtime source/index hashes unchanged',
        'git HEAD unchanged and no tracked diff'],
    'source_hashes_verified':len(before),'runtime_hash_differences':changed,
    'source_hashes_after':after,'git_head':audit['git_head'],'tracked_diff':tracked_diff,
    'limitations':['No full runtime registry loading of the draft blueprints.',
        'No candidate bundle compilation of the proposals.',
        'No semantic embedding, index rebuild, live candidate-pack run, routing regression, image generation, pixel qualification or user acceptance.',
        'Contract subset checks validate shape, not factual completeness or effectiveness.',
        'Another untracked research directory may exist and is outside this task.']
}
dump('artifact-validation.json',validation)

# Keep generated reports honest about their canonical counts.
assert '155' in report.read_text() and '310' in report.read_text()
assert sem['counts']['records']==155 and sem['counts']['candidate_phrase_drafts']==310
assert sem['counts']['inventory_rows']==1151 and sem['counts']['specific_keyword_mappings']==449
manifest={}
for f in sorted(HERE.iterdir()):
    if f.is_file() and f.name!='artifact-manifest.json':
        manifest[f.name]={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size}
dump('artifact-manifest.json',{'schema_version':'clothing-research-manifest/v1','files':manifest})
print(json.dumps({'result':'pass','runtime_hashes_unchanged':len(before),'blueprints':len(bp['blueprints']),
    'component_gates':len(gate_ids),'families':len(coverage['families']),'artifacts':len(manifest)},ensure_ascii=False))
