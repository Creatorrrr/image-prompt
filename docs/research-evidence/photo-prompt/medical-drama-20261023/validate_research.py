"""Validate research integrity, not clinical truth, live retrieval, native facts or pixels."""
import ast
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
def read(name):return json.loads((ROOT/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(obj):return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    cards=read('semantic-cards.json')['cards'];routes=read('keyword-routes.json')['routes']
    drafts=read('candidate-drafts.json')['drafts'];sources=read('sources.json')['sources']
    existing=read('existing-source-mapping.json')['selected'];snap=read('corpus-snapshot.json')
    ref=read('reference-conversation.json');baseline=read('BASELINE.json')
    cases=read('evaluation-cases.json')['cases'];pixels=read('pixel-cases.json')
    checks=[]
    def check(name,result):checks.append({'name':name,'pass':bool(result)})
    byid={c['id']:c for c in cards};sids={s['id'] for s in sources};visual=[c for c in cards if c['positive_en'] is not None]
    check('reference full 19 sections and 24 tables',len(ref['tables'])==24 and ref['tables'][-1]['section'].startswith('19.'))
    check('346 exact source rows and 8 combinations',sum(len(t['rows'])-1 for t in ref['tables'][:-1])==346 and len(ref['tables'][-1]['rows'])-1==8)
    check('sidebar removed and response includes final paragraph','프로젝트\n' not in ref['text'] and '훨씬 명확해집니다.' in ref['text'])
    check('unique card and source IDs',len(byid)==len(cards) and len(sids)==len(sources))
    check('100 new 22 reuse 42 context 8 held',collections.Counter(c['mode'] for c in cards)=={'authored_visual_option':100,'existing_visual_reuse_proposal':22,'context_only':42,'held_reference_needed':8})
    check('50 source records and inaccessible sources unanchored',len(sources)==50 and all(s['access']!='unavailable' or not s['can_anchor'] for s in sources))
    check('all used evidence anchors accessible within declared scope',all(set(c['source_ids'])<=sids and all(next(s for s in sources if s['id']==sid)['can_anchor'] for sid in c['source_ids']) for c in cards))
    check('source access and limits explicit',all(s['access'] and s['supported_scope'] and s['claim_limit'] and s['reviewed_date_kst']=='2026-10-23' and not s['quotation_used'] for s in sources))
    seeds=[(t['table_index'],i,row[0],row[1]) for t in ref['tables'][:-1] for i,row in enumerate(t['rows'][1:],1)]
    check('routes preserve exact original order and descriptions',[(r['table_index'],r['row_index'],r['term'],r['seed_definition']) for r in routes]==seeds)
    check('every seed has a boundary or held record',len(routes)==346 and all(r['context_card_ids'] or r['held_card_ids'] for r in routes))
    check('all route references exist',all(set(r['context_card_ids']+r['held_card_ids']+r['optional_visual_card_ids'])<=byid.keys() for r in routes))
    check('route type separation',all(all(byid[x]['positive_en'] is not None for x in r['optional_visual_card_ids']) and all(byid[x]['mode']=='context_only' for x in r['context_card_ids']) and all(byid[x]['mode']=='held_reference_needed' for x in r['held_card_ids']) for r in routes))
    check('advisory routes never assert equivalence',all(r['activation']=='advisory_only' and r['mapping_semantics']=='related_optional_realization_not_synonym_or_sufficient_definition' for r in routes))
    check('every card has reciprocal seed coverage',all(c['source_keyword_ids'] and c['source_keyword_ids']==[r['id'] for r in routes if c['id'] in r['context_card_ids']+r['held_card_ids']+r['optional_visual_card_ids']] for c in cards))
    check('visual cards have bilingual complete literals and review metadata',all(c['positive_en'] and c['positive_ko'] and c['owner_nodes'] and c['relations'] and c['observable_gates'] and c['confusion_boundary'] and c['claim_limit'] and c['suggested_slots'] for c in visual))
    check('graph endpoints belong to each card',all(e['from'] in c['owner_nodes'] and e['to'] in c['owner_nodes'] for c in visual for e in c['relations']))
    check('part ownership uses declared nodes',all(o['owner'] in c['owner_nodes'] and o['part'] in c['owner_nodes'] for c in visual for o in c.get('part_ownership',[])))
    check('suggested slots exist in read catalog',all(set(c['suggested_slots'])<=set(snap['catalog_slots']) for c in visual))
    check('contexts and held records have no positive literals or slot authority',all(c['positive_en'] is None and c['positive_ko'] is None and not c['relations'] and not c['owner_nodes'] and not c['suggested_slots'] for c in cards if c not in visual))
    check('all records remain inert and unqualified',all(c['native_approval'] is False and c['runtime_importable'] is False for c in cards))
    check('all visual cards retain strict pixel policy',all(c['unobservable_policy']=='UNOBSERVABLE_NOT_PASS' and c['whole_case_policy']=='partial_is_fail' for c in visual))
    check('drafts correspond exactly to complete bilingual visual sources',len(drafts)==122 and {d['card_id'] for d in drafts}=={c['id'] for c in visual} and all(d['en']==byid[d['card_id']]['positive_en'] and d['ko']==byid[d['card_id']]['positive_ko'] and d['preserve_complete_proposition'] and not d['native_approval'] and not d['runtime_importable'] for d in drafts))
    check('22 complete reused records and binding ownership',len(existing)==22 and all(x['source_record']['id']==x['candidate_id'] and canonical(x['source_record'])==x['source_record_sha256'] and x['binding_records'] and all(b['record']['candidate_id']==x['candidate_id'] for b in x['binding_records'].values()) for x in existing))
    check('reused canonical literals guards and effects unchanged',all(byid[x['id']]['positive_en']==x['source_record']['content']['en'] and byid[x['id']]['positive_ko']==x['source_record']['content']['ko'] and byid[x['id']]['inherited_conditions']==x['source_record'].get('conditions',{}) and byid[x['id']]['inherited_effects']==x['source_record'].get('effects',{}) for x in existing))
    check('registry mismatch and overlapping role-play explicitly identified',byid['R15']['source_file']=='photo_candidate_biopunk_body_horror_20261021.json' and bool(byid['R15']['registry_drift_note']) and byid['G06']['overlap_review']['existing_card']=='R20')
    check('development cases complete bilingual not run and not holdout',len(cases)==60 and collections.Counter(x['kind'] for x in cases)=={'boundary':48,'ordinary':12} and all(x['query_en'] and x['query_ko'] and x['expected'] and x['result']=='NOT_RUN' and not x['independent_holdout'] and set(x['card_ids'])<=byid.keys() for x in cases))
    check('pixel plan distinct requests and no executed images',len(pixels['cases'])==16 and pixels['executed_images']==0 and all(x['status']=='NOT_RUN' and set(x['card_ids'])<=byid.keys() for x in pixels['cases']))
    check('snapshot read showed no module drift',not snap['read_consistency']['changed_modules'])
    for f in ROOT.glob('*.py'):ast.parse(f.read_text())
    check('research scripts parse',True)
    links=[];whitespace=[]
    for f in ROOT.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
            if '://' not in target and not target.startswith('#') and target not in ['VALIDATION.json','SHA256SUMS']:
                if not (f.parent/target.split('#',1)[0]).exists():links.append((f.name,target))
    for f in ROOT.glob('*'):
        if f.suffix in ['.py','.md']:
            whitespace.extend(f'{f.name}:{i}' for i,line in enumerate(f.read_text().splitlines(),1) if line.rstrip()!=line)
    check('local document links resolve',not links)
    check('no trailing whitespace in authored prose and scripts',not whitespace)
    changed=[];missing=[]
    for name,h in baseline['protected_sha256'].items():
        f=REPO/name
        if not f.exists():missing.append(name)
        elif sha(f)!=h:changed.append(name)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    module_drift=[name for name,h in snap['module_sha256'].items() if not (REPO/'skills/photo-prompt-image-generator/assets'/name).exists() or sha(REPO/'skills/photo-prompt-image-generator/assets'/name)!=h]
    passed=all(c['pass'] for c in checks);drift=bool(changed or missing or module_drift or head!=baseline['head'])
    status='STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE' if passed and drift else ('STRUCTURE_PASS_PROTECTED_FILES_STABLE' if passed else 'STRUCTURE_FAIL')
    result=dict(schema='medical-drama-research-validation/v1',status=status,checks=checks,
        counts=read('SUMMARY.json')['counts'],baseline_head=baseline['head'],observed_head=head,
        protected_state=dict(count=len(baseline['protected_sha256']),changed=changed,missing=missing,module_drift=module_drift),
        task_write_scope='docs/research-evidence/photo-prompt/medical-drama-20261023 only',
        runtime_mutations_by_this_task=0,embedding_calls=0,image_calls=0,
        evidence_limits=['Structure and source preservation are not full clinical verification.',
            'Authored geometry is not an observed clinical photograph.',
            'Live retrieval, source-native qualification, pixels, installation and user acceptance NOT_RUN.',
            'Observed protected-file drift belongs to shared-checkout state; no reset or revert was performed.'],
        local_link_errors=links,whitespace_errors=whitespace,commit='NOT_RUN',push='NOT_RUN')
    (ROOT/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    report=['# 연구 무결성 검증','',f"상태: `{status}`. 구조 검사 {sum(c['pass'] for c in checks)}/{len(checks)} 통과.",'',
        '검사 범위는 원문 행 보존, 출처 접근 범위, 카드/경로 역참조, 한영 완전 문장, 소유·관계 노드, 정본 조건·효과 복사, 평가 입력 상태, 문서 링크와 파일 해시다. 임상 정확성 전체·실제 검색·native 승인·생성 이미지 성공을 검증한 것이 아니다.','',
        f"보호 파일 {len(baseline['protected_sha256'])}개 중 변경 {len(changed)}개, 누락 {len(missing)}개. 읽은 코퍼스 payload 모듈의 현재 해시 변화 {len(module_drift)}개. HEAD 변경: {head!=baseline['head']}.",'',
        '공유 checkout에서 관측한 변경은 별도 기록하며 reset/revert하지 않았다. 반영 직전에 manifest와 selected runtime을 다시 기준화한다. 원 코퍼스 스캔 중 manifest의 별도 전후 해시는 저장하지 않았으므로, payload의 해시 일치만으로 전체 manifest의 원자적 스냅샷을 주장하지 않는다.','']
    report += ['- `'+name+'`' for name in changed]
    report += ['', '이미지·임베딩 호출 0회. 운영 파일 변경·등록·설치·활성화·commit/push를 수행하지 않았다. 읽기 전용 recorder/dependency 검사는 [runtime-readonly-check.json](runtime-readonly-check.json)에 별도 기록했다.','',
        '기계 판독 결과는 [VALIDATION.json](VALIDATION.json), 수량은 [SUMMARY.json](SUMMARY.json), 파일 해시는 [SHA256SUMS](SHA256SUMS)를 참조한다.']
    (ROOT/'VALIDATION.md').write_text('\n'.join(report)+'\n')
    summary=read('SUMMARY.json');summary['evidence']['research_structure']=status
    summary['counts'].update(evaluation_cases=len(cases),bilingual_evaluation_queries=len(cases)*2,pixel_test_families=16)
    (ROOT/'SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    files=sorted(f for f in ROOT.rglob('*') if f.is_file() and f.name!='SHA256SUMS' and '__pycache__' not in f.parts)
    (ROOT/'SHA256SUMS').write_text(''.join(f'{sha(f)}  {f.relative_to(ROOT)}\n' for f in files))
    print(json.dumps(dict(status=status,passed=sum(c['pass'] for c in checks),total=len(checks),failed=[c['name'] for c in checks if not c['pass']],protected_changed=len(changed),protected_missing=len(missing),module_drift=module_drift,head_changed=head!=baseline['head'],links=links,whitespace=whitespace),ensure_ascii=False))
    if not passed:raise SystemExit(1)

if __name__=='__main__':main()
