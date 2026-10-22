"""Build local research views, never operating assets or model calls."""
import collections,csv,hashlib,json,pathlib,re
from research_sources import ROWS,ACCESS_GAPS
from reference_supplement import TAIL,SCENE_NAMES,RECOVERY
from research_cards import cards,FAMILIES
from keyword_routes import DATA as ROUTES
from evaluation_cases import DATA as CASES
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def write(name,obj):
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    bounded=json.loads((HERE/'REFERENCE-THREAD-BOUNDED.json').read_text())
    text=next(i['text'] for t in bounded['turns'] for i in t['items'] if i['type']=='agentMessage')
    found=re.findall(r'^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$',text,re.M)
    seeds={int(n):{'seed_id':int(n),'term':term.replace('**',''),'reference_description_ko':desc,
      'reference_origin':'read_thread numbered table'} for n,term,desc in found if int(n)<=135}
    for n,term,desc in TAIL:seeds[n]={'seed_id':n,'term':term,'reference_description_ko':desc,'reference_origin':'rendered browser numbered table'}
    assert set(seeds)==set(range(1,151))
    route_rows=[]
    for line in ROUTES.strip().splitlines():
        n,mode,ids,boundary=line.split('|');row=dict(seeds[int(n)])
        row.update({'route_mode':mode,'card_ids':ids.split(','),'distinction_ko':boundary,
          'automatic_hard_activation':False,'definition_verification':'reference seed preserved; external checks at cited concept-family scope, not 150 individually sourced definitions'})
        route_rows.append(row)
    catalog_raw=(ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_bytes()
    catalog=json.loads(catalog_raw)['slot_catalog'];cs=cards()
    for c in cs:
        c['routed_seed_ids']=[r['seed_id'] for r in route_rows if c['card_id'] in r['card_ids']]
        c['proposed_role_descriptors']={s:{'semantic_role':catalog[s]['semantic_role'],'dimensions':catalog[s]['dimensions'],
          'property_prefixes':catalog[s]['property_prefixes']} for s in c['proposed_slots']}
        c['role_descriptor_limit']='Current slot vocabulary only; no approved role fit, owner selector, effect declaration, source guard, or runtime registration.'
    source_rows=[{'source_id':n,'title':title,'url':url,'read_scope':access,'supported_scope_and_limit_ko':scope,
                  'reviewed_date_kst':'2026-10-22','concrete_geometry':'authored_optional_realization_not_a_source_quote'} for n,title,url,access,scope in ROWS]
    drafts=[]
    for c in cs:
        if c['observability']=='context':continue
        canonical=json.dumps(c,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
        drafts.append({'draft_id':'draft_'+c['card_id'],'card_id':c['card_id'],'semantic_card_sha256':sha(canonical),
          'proposal_en':c['proposal_en'],'proposal_ko':c['proposal_ko'],'owners':c['owners'],
          'directed_relations':c['directed_relations'],'proposed_slots':c['proposed_slots'],
          'source_ids':c['source_ids'],'claim_limit_ko':c['claim_limit_ko'],
          'source_disposition':'reuse/refine/new still to be resolved from complete source contracts',
          'effect_and_guard_review':'PENDING: enumerate every changed dimension, owner and property before authoring loader-ready records',
          'candidate_id':None,'realization_id':None,'native_approval':False,'runtime_registration':'none'})
    write('sources.json',{'schema':'genre-fusion-sources/v1','sources':source_rows,'access_gaps':ACCESS_GAPS})
    write('reference-seeds.json',{'schema':'genre-fusion-reference-seeds/v1','recovery':RECOVERY,'seeds':list(seeds.values())})
    write('keyword-routes.json',{'schema':'genre-fusion-keyword-routes/v1','routes':route_rows})
    write('semantic-cards.json',{'schema':'genre-fusion-research-cards/v1','catalog_sha256':sha(catalog_raw),'catalog_slot_count':len(catalog),
      'runtime_registration':'none','cards':cs})
    write('candidate-drafts.json',{'schema':'genre-fusion-candidate-drafts/v1','not_loader_input':True,'drafts':drafts})
    md=['# 키워드 전체 경로','', '원 대화의 번호 150개를 모두 보존했다. 경로는 탐색·의미 구분이며 하드 활성화 규칙이 아니다. 개념군의 출처 확인과 각 개별 정의의 검증을 구분한다.','',
        '|번호|용어|경로|관련 카드|보존할 구분|','|---:|---|---|---|---|']
    for r in route_rows:md.append(f"|{r['seed_id']}|{r['term']}|{r['route_mode']}|{', '.join(r['card_ids'])}|{r['distinction_ko']}|")
    (HERE/'KEYWORD-ATLAS.md').write_text('\n'.join(md)+'\n')
    md=['# 시각 의미 카드','', '96개 중 84개는 선택적 가시 실현안, 12개는 비가시 문맥 전용이다. proxy는 넓은 개념 전체를 입증하지 않는다. 모든 구체적 기하·사물 결합은 새 저술이며 인용한 원작의 정본 디자인이 아니다.','']
    for c in cs:
        md.extend([f"## {c['card_id']} · {c['title_ko']}",'',f"{c['family']} / {c['priority']} / `{c['observability']}` / 관련 번호 {', '.join(map(str,c['routed_seed_ids']))}",'',c['proposal_ko'],'',c['proposal_en'],'',
           '**소유자:** '+ '; '.join(f'{k}: {v}' for k,v in c['owners'].items()),'',
           '**방향 관계:** '+ '; '.join(f"{r['from']} → {r['predicate']} → {r['to']}" for r in c['directed_relations']), '',
           '**혼동:** '+c['nearest_confusion_ko'],'','**주장 한계:** '+c['claim_limit_ko'],'',
           '**제안 슬롯:** '+', '.join(c['proposed_slots'])+' — 현행 카탈로그 어휘 제안, 자격 승인 아님.','',
           '**출처:** '+', '.join('['+s+']('+next(x['url'] for x in source_rows if x['source_id']==s)+')' for s in c['source_ids']),'',
           '**검토:** '+('긍정 후보·픽셀 gate 생성 안 함.' if c['observability']=='context' else '관계의 양 끝·연결·소유자를 함께 식별해야 함. partial/unobservable은 완전 통과 아님. 픽셀 NOT_RUN.'),''])
    (HERE/'VISUAL-CARDS.md').write_text('\n'.join(line.rstrip() for line in md).rstrip()+'\n')
    with (HERE/'SOURCES.tsv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(source_rows[0]),delimiter='\t');w.writeheader();w.writerows(source_rows)
    cases=[]
    for idx,line in enumerate(CASES.strip().splitlines(),1):
        cohort,target,slots,ko,en,boundary=line.split('|')
        cases.append({'case_id':f'Q{idx:03d}','cohort':cohort,'target_cards':target,'slots':slots,'query_ko':ko,'query_en':en,
          'review_boundary_ko':boundary,'gold_cid_rid':'PENDING','execution_status':'NOT_RUN'})
    with (HERE/'EVALUATION-CASES.tsv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(cases[0]),delimiter='\t');w.writeheader();w.writerows(cases)
    combination_cards=[['A03','D06','E01'],['A01','D01','D04'],['G02','D11','E11'],['B06','C09','E08'],
      ['B03','B05','D07'],['C04','C05','C12'],['D03','F07','G10'],['A09','A12','D05'],
      ['D02','G01','G07'],['E01','F02','B11'],['H01','D08','E10'],['C01','C09','A06']]
    scene_proposals=[
      '화덕 연료를 계량하는 주민의 국자 아래 이웃이 기운 주머니를 받친다. 뒤의 관 이음매에는 현재 쥔 클램프가 보인다. 연료의 부족 이유와 세계의 남은 수명은 서사로 남긴다.',
      '차광판 줄무늬가 드는 여관에서 주인이 문턱을 넘는 낯선 손님에게 그릇을 내민다. 붉은 원반을 쓰더라도 항성의 수명은 판정하지 않는다.',
      '비인간 이웃의 연속된 부속지가 문고리를 잡는 동안 다른 주민이 꼬리 홈이 있는 공동 벤치 자리를 비켜 준다. 종의 정체와 합의 제도 전체는 확정하지 않는다.',
      '뼈 같은 거대 아치 밑 경작 상자 옆으로 화물 틀을 멘 운송체가 지나간다. 잔해와 주민의 동선은 분리한다. 신성·식용성·영양 경로는 허구 맥락이다.',
      '무너진 아치 안 빨랫줄 아래에서 주민이 일하고 기둥 홈에는 작은 배관이 붙어 있다. 유적을 현재 생활에 쓰는 접점이 중심이며 재난 연대는 열어 둔다.',
      '쟁반의 분리된 외피를 받치는 돌봄자 옆으로, 등에 맞춘 담요를 두른 주민이 앉는다. 프레임에는 하나의 주된 접촉만 선명하게 두고 탈피 공정 전체를 압축하지 않는다.',
      '성인 지성 비인간이 성인 인간이 받친 컵 손잡이를 잡는다. 옆의 이름 표찰은 별도 선택 사항이다. 접촉은 보여도 사랑·동의·상대의 본질을 입증하지 않는다.',
      '씨앗 상자를 둔 공동 제빵 자리에서 각 작업자가 자기 반죽판과 빵삽을 다룬다. 마지막 계절이라는 시간 전제는 이미지 검증 대상에서 분리한다.',
      '서로 다른 형태의 식기 사이로 공동 접시가 놓이고 창밖 거대 형상은 식사 행위를 압도하지 않는 정도로만 드러난다. 기록 불일치는 선택할 때만 별도 비교 대상으로 둔다.',
      '주민이 문턱의 새 삽입물에서 이어지는 도형 선을 확인하고 옆 배관을 클램프로 받친다. 두 수선은 같은 장소의 별개 소유자이며 실제 보호 효능은 보증하지 않는다.',
      '빈 의자 앞에서 성인이 닫힌 기념함에 꽃을 놓는다. 접은 천과 수레는 별도 선택 사항이다. 함의 내용물·사망 사실·마지막 종의 애도는 서사에 남긴다.',
      '생활 좌판 옆 벽에는 가지줄이 퍼지고 배수 호스는 별도 컵에 끝난다. 오래된 층위는 배경으로 두고 생태의 복잡성과 쇠락의 인과를 사진에서 확정하지 않는다.',
    ]
    combinations=[]
    for i,(name,ids) in enumerate(zip(SCENE_NAMES,combination_cards),1):
        combinations.append({'scene_id':f'SC{i:02d}','reference_expression':name,'optional_cards':ids,
          'selection_rule':'Choose one primary action and only supporting compatible details; never union all owners/effects or impose a fixed motif.',
          'authored_scene_proposal_ko':scene_proposals[i-1],
          'context_remaining':[c['claim_limit_ko'] for c in cs if c['card_id'] in ids],
          'genre_balance':'Evaluate care/action clarity, strange material relations, exhaustion cues and interpretive unknowns separately; none is a mandatory motif quota.'})
    write('scene-blueprints.json',{'schema':'genre-fusion-scene-blueprints/v1','blueprints':combinations})
    md=['# 원 대화의 조합 표현을 장면으로 옮기는 법','', '카드의 단순 합집합이 아니다. 하나의 행동이 장면을 이끌고 다른 요소가 그 행동의 필요·조건·단서를 만든다. 아래 조합도 선택적 제안이다.','',
        '|표현|우선 검토할 관계|남겨 둘 서사 경계|','|---|---|---|']
    for s in combinations:md.append('|'+s['reference_expression']+'|'+', '.join(s['optional_cards'])+' · '+s['authored_scene_proposal_ko']+'|'+' / '.join(s['context_remaining'])+'|')
    (HERE/'SCENE-BLUEPRINTS.md').write_text('\n'.join(md)+'\n')
    print(json.dumps({'seeds':len(seeds),'sources':len(source_rows),'cards':len(cs),'drafts':len(drafts),'relations':sum(len(c['gates']) for c in cs),'cases':len(cases),'cohorts':dict(collections.Counter(x['cohort'] for x in cases)),'blueprints':len(combinations)},ensure_ascii=False))
if __name__=='__main__':main()
