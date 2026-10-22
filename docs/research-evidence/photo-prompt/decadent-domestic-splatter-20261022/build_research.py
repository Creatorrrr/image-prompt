"""Build only research documents/data in HERE; never builds/activates runtime."""
import collections,csv,hashlib,json,pathlib,re
from research_cards import cards,FAMILIES
from research_sources import sources
from evaluation_cases import cases
from reference_supplement import supplement
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def save(name,x):
    (HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def md(x):return str(x).replace('|',' / ').replace('\n',' ')

def main():
    cs=cards();ss=sources();es=cases();source_by={s['source_id']:s for s in ss}
    ref=json.loads((HERE/'REFERENCE-THREAD-BOUNDED.json').read_text());seeds=[];section='combination_axes'
    for line in ref['answer_text'].splitlines():
        if re.match(r'^#{1,3} ',line):section=line.lstrip('# ')
        if line.startswith('| **'):
            fields=line.split('|');term=re.search(r'\*\*(.*?)\*\*',fields[1]).group(1)
            seeds.append({'seed_id':len(seeds)+1,'term':term,'reference_section':section,'reference_explanation':fields[2].strip() if len(fields)>2 else '',
              'reference_row_complete':line.rstrip().endswith('|'),'origin':'returned_reference_text','independent_definition_verification':'concept_family_only_not_every_term','automatic_hard_activation':False})
    assert len(seeds)==149 and sum(s['reference_row_complete'] for s in seeds)==148
    browser=supplement();save('REFERENCE-BROWSER-SUPPLEMENT.json',browser)
    extra={r['seed_id']:r for r in browser['rows']}
    seeds[-1].update(reference_row_complete=True,reference_explanation=extra[149]['reference_explanation_summary'],origin=extra[149]['origin'],kind='term')
    for row in browser['rows']:
        if row['seed_id']>149:
            seeds.append({'seed_id':row['seed_id'],'term':row['term'],'reference_section':row['kind'],'kind':row['kind'],'reference_explanation':row['reference_explanation_summary'],'reference_row_complete':True,'origin':row['origin'],'independent_definition_verification':'concept_family_only_not_every_term','automatic_hard_activation':False})
        for c in cs:
            if c['card_id'] in row['card_ids'] and row['seed_id'] not in c['reference_seed_ids']:c['reference_seed_ids'].append(row['seed_id'])
    for seed in seeds:seed.setdefault('kind','combination_axis' if seed['seed_id']<=3 else 'term')
    routes=[]
    for seed in seeds:
        linked=[c for c in cs if seed['seed_id'] in c['reference_seed_ids']];assert linked,seed
        routes.append({'seed_id':seed['seed_id'],'term':seed['term'],'reference_row_complete':seed['reference_row_complete'],'kind':seed['kind'],'optional_visual_card_ids':[c['card_id'] for c in linked if c['observability']!='context'],'context_card_ids':[c['card_id'] for c in linked if c['observability']=='context'],'related_source_ids':sorted({s for c in linked for s in c['source_ids']}|set(extra.get(seed['seed_id'],{}).get('source_ids',[]))),'route_authority':'advisory_only_after_independent_core','automatic_hard_activation':False,'definition_verification':seed['independent_definition_verification']})
    save('reference-seeds.json',{'seeds':seeds,'coverage':'189 complete table rows: 3 axes + 170 terms, 8 coined expressions, 8 works; 17 rendered tables; bounded connector source retained'})
    save('keyword-routes.json',{'routes':routes,'not_an_alias_activation_registry':True})
    save('semantic-cards.json',{'schema':'decadent-domestic-splatter-research-semantics/v1','cards':cs,'runtime_registration':'none','native_approval':False})
    save('sources.json',{'sources':ss,'source_count_is_not_books_fully_read':True})
    drafts=[]
    for c in cs:
        if c['observability']=='context':continue
        drafts.append({'draft_id':'research_'+c['card_id'],'card_id':c['card_id'],'candidate_id':None,'realization_id':None,'proposal_en':c['proposal_en'],'proposal_ko':c['proposal_ko'],'owners':c['owners'],'relations':c['relations'],'proposed_slots':c['proposed_slots'],'source_ids':c['source_ids'],'card_sha256':hashlib.sha256(canonical(c)).hexdigest(),'disposition':'PENDING_REUSE_REFINE_NEW_CONTEXT_DEFER_REVIEW','source_contract_authoring':'NOT_RUN','native_source_qualification':'NOT_RUN','runtime_registration':'none','native_approval':False,'source_is_executable':False})
    save('candidate-drafts.json',{'drafts':drafts,'count_overlaps_semantic_cards':True,'not_runtime_loader_input':True})
    with (HERE/'SOURCES.tsv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(ss[0]),delimiter='\t');w.writeheader();w.writerows(ss)
    with (HERE/'EVALUATION-CASES.tsv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(es[0]),delimiter='\t');w.writeheader();w.writerows(es)
    atlas=['# 참조 대화 키워드 대응표','','연결 도구의 149행을 브라우저의 17개 표와 대조·보완했다. 총 189행은 조합 축3·용어170·제안 조합명8·참고 작품8이다. 원 149번 설명도 브라우저에서 확인했다. 표의 관련 출처는 연결된 카드의 개념군/재료 경계를 지원한다. **189행의 정의·작품 분석이 각각 독립 검증됐다는 뜻은 아니다.** 제안 조합명은 정식 장르가 아니다.','', '|번호|용어|가시 선택안|문맥 경로|원 행 완전성|','|---:|---|---|---|---|']
    for r in routes:atlas.append(f"|{r['seed_id']}|{md(r['term'])}|{','.join(r['optional_visual_card_ids']) or '없음'}|{','.join(r['context_card_ids']) or '없음'}|{'완전' if r['reference_row_complete'] else '설명 중단'}|")
    (HERE/'KEYWORD-ATLAS.md').write_text('\n'.join(atlas)+'\n')
    lines=['# 시각 의미 카드','','모든 배열·장면은 새로 저술한 선택안이다. 출처가 같은 모양의 장면을 묘사했다는 뜻이 아니다. 관계별 gate와 소유자는 JSON에 보존한다. 프록시는 서사 의미 자체의 통과 증거가 아니며 H 카드는 긍정 시각 초안을 만들지 않는다.','']
    for fam,title in FAMILIES.items():
        lines+=['## '+title,'']
        for c in cs:
            if not c['card_id'].startswith(fam):continue
            lines += [f"### {c['card_id']} {c['title_ko']}",'',f"- 모드/우선순위: {c['observability']} / {c['priority']}; 제안 역할: {', '.join(c['proposed_slots'])}",f"- 한글: {c['proposal_ko']}",f"- English: {c['proposal_en']}",f"- 소유자: {json.dumps(c['owners'],ensure_ascii=False)}",'- 관계: '+('; '.join(f"{r['from']} → {r['predicate']} → {r['to']}" for r in c['relations']) or '문맥 전용; 시각 관계 없음'),f"- 혼동: {c['confusion_boundary_ko']}",f"- 주장 한계: {c['claim_limit_ko']}",'- 출처: '+', '.join(f"[{i} {source_by[i]['title']}]({source_by[i]['url']})" for i in c['source_ids']),'']
    (HERE/'VISUAL-CARDS.md').write_text('\n'.join(lines))
    audit=json.loads((HERE/'CORPUS-LEXICAL-AUDIT.json').read_text());mapping=json.loads((HERE/'existing-source-mapping.json').read_text())
    lines=['# 기존 corpus 관찰','','관찰 시각: '+audit['captured_at_kst'],f"후보 {audit['candidate_count']:,}개, 긍정 {audit['positive_count']:,}개, diagnostic {audit['record_kinds']['diagnostic']}개, 모듈 {audit['module_count']}개, binding {audit['binding_count']:,}개를 읽었다. source/index의 현재 상태이며 installed 세대에 같은 내용이 포함됐다는 뜻이 아니다.",'','검사 필드는 content.en / content.ko / content.additional_details다. definition·embedding_text·alias·tag·조건·연구 metadata는 이 수량 검사에서 제외했다. 선택한 원문 28개는 조건·effect·binding까지 별도 스냅샷에 포함했다. 이 수량은 검색 노출·의미 부재·native 자격 증거가 아니다.','', '|어휘군|일치 레코드|','|---|---:|']
    lines += [f"|{key}|{value['count']}|" for key,value in audit['patterns'].items()]
    lines += ['','`vanitas` 일치가 0이어도 `cand_eb165802b276591084b42c4285daa130`에는 새 음식·시든 꽃·꺼진 촛불의 실현안이 이미 있다. 반대로 keyhole은 문이 아닌 의복 구멍을 찾기도 한다. 따라서 이름 0건→신규 CID 결론을 내리지 않는다.','', '|기존 CID|제안|관련 카드|원문 대조 판단|','|---|---|---|---|']
    for s in mapping:lines.append(f"|{s['candidate_id']}|{s['proposed_disposition']}|{','.join(s['related_cards'])}|{s['rationale_ko']}|")
    lines+=['','`reuse`는 정확한 해당 원자 의미를 먼저 재사용하자는 조사 판단이다. 카드 전체의 역할 자격·추가 소유자·가구/의복 전용 guard·native proof까지 승인했다는 뜻이 아니다. `reject_neighbor`는 이 연구와의 이웃 오탐 판정이며 기존 레코드 삭제 요청이 아니다. 새 후보 수는 86개로 확정하지 않는다.']
    (HERE/'CORPUS-FINDINGS.md').write_text('\n'.join(lines)+'\n')
    lines=['# 출처와 접근 범위','','모든 열람일은 2026-10-22 KST다. 61개 URL은 61권 완독을 뜻하지 않는다. 검색 반환 본문만 읽은 자료, 출판사 소개·초록·서지, 직접 열기에 실패한 자료를 구별했다. 원 대화의 `chatgpt-content-reference` 인덱스 자체는 서지로 사용하지 않았다. 브라우저에서 복원한 실제 URL은 별도로 열어 읽고 source ledger에 기록했다.','']
    for s in ss:lines += [f"## {s['source_id']} {s['title']}",'',f"[{s['title']}]({s['url']})",f"- 읽은 범위: {s['read_scope']}",f"- 지원: {s['supports_ko']}",f"- 한계: {s['limits_ko']}",'']
    lines+=['## 참조 복원 한계','','read_thread 반환본은 20,000자에서 잘렸고 cursor가 없었다. 이후 CUA로 동일 대화의 렌더링 본문과 표 셀을 읽어 17개 표·189개 데이터 행을 확인했다. 149번 설명을 완성하고 성유물함·서사/촬영/음향 용어·창작 조합명8·참고 작품8을 추가했다. REFERENCE-BROWSER-SUPPLEMENT.json은 추가 표의 정확한 명칭과 연구자의 설명 요약을 보존하며 완전한 원문 DOM 덤프가 아니다. 원 bounded snapshot은 그대로 유지했다. 본문 내 모든 출처 팝오버를 펼치거나 영화를 관람한 것은 아니다.','']
    (HERE/'ACCESS-LIMITS.md').write_text('\n'.join(lines))
    print(json.dumps({'reference_rows':len(seeds),'complete_reference_rows':189,'cards':len(cs),'visual_drafts':len(drafts),'context_cards':len(cs)-len(drafts),'relation_gates':sum(len(c['gates']) for c in cs),'sources':len(ss),'cases':len(es),'bilingual_queries':2*len(es),'cohorts':dict(collections.Counter(e['cohort'] for e in es))},ensure_ascii=False))
if __name__=='__main__':main()
