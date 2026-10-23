"""Build inert research artifacts. No runtime imports, API calls or source writes."""
import collections
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent

def read_rows(name, delimiter='|'):
    with (ROOT/name).open() as f:
        return list(csv.DictReader(f, delimiter=delimiter))

def put(name, value):
    (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def main():
    seeds = json.loads((ROOT/'reference-prefix.json').read_text())['seeds']
    for line in (ROOT/'reference-tail-terms.txt').read_text().splitlines():
        n,term=line.split('\t',1)
        seeds.append({'n':int(n),'term':term,'definition_capture':'Full term and definition read in authenticated browser; only term transcribed here.'})
    assert [s['n'] for s in seeds] == list(range(1,211))
    sources=read_rows('sources.tsv','\t')
    sources.insert(0,{'id':'S00','publisher':'Referenced ChatGPT conversation','title':'학원물 용어 정리',
        'url':'https://chatgpt.com/c/6adafc0d-dc50-83ee-b22e-eec239f83ca7','access':'authenticated_browser_dom',
        'read_scope':'210 numbered rows in 14 categories, plus 13 example works in category 15',
        'supports':'Keyword scope and original glossary claims only',
        'limits':'Untrusted secondary synthesis; not an independent fact source or generation instruction.'})
    for s in sources:s['access_date']='2026-10-23';s['media_pixels_reviewed']=False
    put('sources.json',{'schema':'school-life-research-sources/v1','sources':sources})
    cards=[]
    for r in read_rows('cards-authored.tsv'):
        edges=[];nodes=set()
        for e in r['relations'].split(';'):
            a,p,b=e.split('>');nodes.update((a,b));edges.append({'from':a,'relation':p,'to':b})
        cards.append({'id':r['id'],'name_ko':r['name'],'source_keyword_ids':[int(x) for x in r['seeds'].split(',')],
            'mode':r['mode'],'priority':r['priority'],'source_ids':r['sources'].split(','),'suggested_slots':r['slots'].split(','),
            'scope':r['scope'],'evidence_status':'authored_optional_realization_with_context_sources_not_source_proven_geometry',
            'positive_en':r['positive_en'],'positive_ko':r['positive_ko'],'research_owner_nodes':sorted(nodes),'research_relations':edges,
            'confusion_boundary':r['confusion_boundary'],'observable_gate':r['pixel_gate'],
            'not_provable_from_still':r['confusion_boundary'],'activation':'requester_selection_and_native_review_required',
            'source_status':'research_only','native_approval':False,'pixel_status':'NOT_RUN',
            'owner_policy':'Bind to independently declared requester owners; graph node labels create no entity or permission.',
            'effects_review':'Review every introduced or changed person/object/count/wardrobe/pose/contact/setting/light/text/media property before adoption.'})
    for r in read_rows('contexts-authored.tsv'):
        cards.append({'id':r['id'],'name_ko':r['name'],'source_keyword_ids':[int(x) for x in r['seeds'].split(',')],
            'mode':'audio' if r['id']=='C24' else ('sequence' if r['id']=='C22' else 'context'),
            'priority':r['priority'],'source_ids':r['sources'].split(','),'suggested_slots':[],
            'not_provable_from_still':r['not_provable_from_still'],'handling':r['handling'],
            'positive_en':None,'positive_ko':None,'research_owner_nodes':[],'research_relations':[],
            'activation':'advisory_only_no_hard_visual_obligations','native_approval':False,'pixel_status':'NOT_APPLICABLE_TO_NONVISUAL_CLAIM'})
    put('semantic-cards.json',{'schema':'school-life-research-semantic-cards/v1','runtime_importable':False,'cards':cards})
    routes=[]
    for s in seeds:
        linked=[c for c in cards if s['n'] in c['source_keyword_ids']]
        if not linked:raise AssertionError('Unmapped seed '+str(s))
        routes.append({**s,'category':(s['n']-1)//15+1,'activation':'advisory_only',
            'optional_visual_card_ids':[c['id'] for c in linked if c['mode'] in {'visible','proxy'}],
            'context_card_ids':[c['id'] for c in linked if c['mode'] not in {'visible','proxy'}],
            'coverage_status':'routed_for_research_not_independently_verified_definition'})
    put('keyword-routes.json',{'schema':'school-life-research-keyword-routes/v1','routes':routes})
    drafts=[]
    for c in cards:
        if c['mode'] not in {'visible','proxy'}:continue
        drafts.append({'draft_id':'draft_'+c['id'],'card_id':c['id'],'status':'research_only_not_operating_CID',
            'prompt_fragment_en':c['positive_en'],'prompt_fragment_ko':c['positive_ko'],
            'suggested_slots':c['suggested_slots'],'scope':c['scope'],'research_relations':c['research_relations'],
            'claim_limit':c['confusion_boundary'],'gate':c['observable_gate'],
            'requires_before_adoption':['complete bilingual semantic review','actual existing owner binding',
            'intrinsic conditions and complete effects','actual catalog role fit','duplicate and existing-CID review',
            'source-unit coverage and selected-realization obligations','native qualification'],
            'runtime_importable':False,'native_approval':False})
    put('candidate-drafts.json',{'schema':'school-life-research-candidate-drafts/v1','drafts':drafts})
    text=['# 学園 / 학원물 키워드 연결표','',
          '원 대화의 14개 범주 × 15개 = 210개 항목. 15번째 작품 사례 범주는 번호 항목에 합산하지 않는다.',
          '각 연결은 탐색 안내이며 가시 의무·사실 검증·실제 후보 채택을 의미하지 않는다.','',
          '|번호|원문 용어|선택적 가시 카드|문맥/시간/음향 카드|','|---|---|---|---|']
    for r in routes:text.append(f"|{r['n']}|{r['term']}|{', '.join(r['optional_visual_card_ids']) or '—'}|{', '.join(r['context_card_ids']) or '—'}|")
    (ROOT/'KEYWORD-ATLAS.md').write_text('\n'.join(text)+'\n')
    text=['# 의미 카드와 선택적 실현','',
          '이 문서의 구도·소유 그래프·한영 문장은 연구자가 저술한 제안이다. source_ids는 주제·혼동 경계의 근거이며 모든 배치의 실물 고증을 증명하지 않는다.',
          'visible은 제안한 성분의 가시성, proxy는 비가시 개념의 선택적 대리 장면이다. proxy가 그 원개념을 증명하지 않는다.','']
    for c in cards:
        text.extend([f"## {c['id']} {c['name_ko']}",'',f"- 분류/우선순위: `{c['mode']}` / {c['priority']}",f"- 원 항목: {', '.join(map(str,c['source_keyword_ids']))}",f"- 근거 범위: {', '.join(c['source_ids'])}"])
        if c['mode'] in {'visible','proxy'}:
            text.extend([f"- EN 제안: {c['positive_en']}",f"- KO 제안: {c['positive_ko']}",
                         '- 소유/관계: '+'; '.join(f"{e['from']} → {e['relation']} → {e['to']}" for e in c['research_relations']),
                         f"- 혼동 경계: {c['confusion_boundary']}",f"- 원본 픽셀 gate: {c['observable_gate']}",f"- 제안 슬롯: {', '.join(c['suggested_slots'])}; scope: {c['scope']}"])
        else:text.extend([f"- 한 장에서 증명 불가: {c['not_provable_from_still']}",f"- 처리: {c['handling']}"])
        text.append('')
    (ROOT/'VISUAL-CARDS.md').write_text('\n'.join(text)+'\n')
    context_queries={r['card_id']:r for r in read_rows('contexts-development.tsv','\t')}
    cases=[]
    for c in cards:
        visual=c['mode'] in {'visible','proxy'}
        cases.append({'case_id':'DEV_'+c['id'],'case_kind':'card_derived_development_scaffold','card_ids':[c['id']],
            'input_ko':c['positive_ko'] if visual else context_queries[c['id']]['query_ko'],
            'input_en':c['positive_en'] if visual else context_queries[c['id']]['query_en'],
            'language_status':'full_bilingual_visual_fragment' if visual else 'full_bilingual_context_development_query',
            'expected':'Offer semantically matching eligible optional source; preserve unrelated core locks.' if visual else 'Preserve declared context without asserting it as a still-image fact.',
            'negative_target':c.get('confusion_boundary',c['not_provable_from_still']),
            'result':'NOT_RUN','independent_holdout':False})
    put('development-cases.json',{'schema':'school-life-development-scaffold/v1','cases':cases,
        'limits':'Card-derived cases are development queries, not independent evaluation. See BOUNDARY-CASES.tsv and IMPLEMENTATION-PLAN.'})
    snap=json.loads((ROOT/'corpus-snapshot.json').read_text())
    text=['# 기존 source 조사와 반영 판단','',
        '현재 원문 모듈을 읽은 스냅샷이며 검색 실행·native source 심사·설치본 검증은 수행하지 않았다.',
        f"관찰: {snap['counts']['modules']}개 모듈, {snap['counts']['candidates']:,}개 CID, {snap['counts']['slot_bindings']:,}개 binding, {snap['counts']['catalog_slots']}개 catalog 슬롯.",'',
        '|좁힌 가시 원문 검색|CID 수|','|---|---|']
    for k,v in snap['lexical_scan'].items():text.append(f"|{k}|{v['count']}|")
    text.extend(['','검색은 en/ko/phrase 필드만 대상으로 한다. aliases·예시·설명에 대한 넓은 검색과 수치가 다르다. `exam`이 `example`, `boarding`이 승차, `prom`이 텔레프롬프터를 잡는 오류를 줄였다. 검색 0건은 의미적 부재나 신규 후보 확정의 증거가 아니다.','',
        '각 기존 CID의 전체 record·조건·effects·binding은 corpus-snapshot.json에 저장했다. 아래는 채택 전 triage 제안이다.','',
        '|실제 CID|제안|카드|이유|','|---|---|---|---|'])
    for e in snap['existing_source_triage']:text.append(f"|{e['candidate_id']}|{e['decision_proposal']}|{', '.join(e['card_ids'])}|{e['reason']}|")
    text.extend(['','운영 인덱스는 `photo_candidate_search.json`; 관찰된 layout 및 space는 corpus-snapshot.json에 보존한다. 이 연구는 source 총수와 index metadata_count를 직접 동일시하지 않으며, positive/diagnostic 투영과 source SHA closure를 검증하지 않았다.','',
        '현재 maintenance 문서의 native V3 source / V10 pack / issued receipt / 설치 세대 경계를 따른다. 연구 owner graph는 actual native fact·guard·effect·permission·role view를 생성하지 않는다. 모든 조건과 의무는 전체 선택 분기를 검토해 후속 작성해야 한다.'])
    (ROOT/'CORPUS-FINDINGS.md').write_text('\n'.join(text)+'\n')
    print(json.dumps({'seeds':len(seeds),'cards':len(cards),'modes':dict(collections.Counter(c['mode'] for c in cards)),'drafts':len(drafts),'sources':len(sources),'development_scaffolds':len(cases)},ensure_ascii=False))

if __name__=='__main__':main()
