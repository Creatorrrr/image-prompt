#!/usr/bin/env python3
"""Build inert research artifacts only within this directory."""
from collections import Counter
from pathlib import Path
import csv
import hashlib
import json

from research_cards import CARDS
from research_sources import SOURCES

HERE = Path(__file__).resolve().parent
HEADINGS = [
    '1 장르·형식','2-1 신병·선임·위계','2-2 평가어','3-1 구호·소리','3-2 문체·군가',
    '4 행동·작전·규칙','5-1 주요 인물','5-2 기능별 인물','6-1 공간','6-2 차량·소품',
    '7-1 성적 은어·강압','7-2 해병푸드','7-3 금기 소재 분류','8 문학·분석',
    '9-1 현실 차용 복식','9-2 변형 복식','10-1 체형·머리','10-2 표정',
    '11-1 권위 포즈','11-2 반응·도주 포즈','12 화면 연출','13 창작 조합','14 혼동 구분'
]
SOURCE_KEYS = ('id','title','url','publication_date','kind','access_status','supports','limits')
DIAGNOSTIC_CARDS = {'V064','V074','T001','T002','T003','T004'}
MAPPING_SPECS = [
    ('V004','cand_215d7d85acbf5d2ca330892cda495c54','new','기존은 tall suede boots. 발목 높이 끈·두꺼운 밑창의 전체 관계와 달라 재사용 보류.'),
    ('V005','cand_b3c90b8f8552572ab0bce2b4c33bf9db','refine','천 표면 얼룩만 재사용 후보. 상의·바지 관계나 군복 신분을 이 국소 패턴에 주입하지 않는다.'),
    ('V005','cand_8f47ea76dd535dfe937648da31444031','context','기존은 임무별 군복 체계의 attire_context. no_text와 원 조건을 보존하며 붉은 명찰·실제 부대 표식을 강제하지 않는다.'),
    ('V005','cand_25e0f45f02b25ac8a853eb63b8f0fa0f','context','성인 허구 군인 역할 subject이며 의복 형태의 대체 데이터가 아니다. subject를 바꾸는 효과를 보존.'),
    ('V036','cand_59849d02f9cc501bb453ac8d42a8ede7','reuse','같은 사람의 어깨·팔꿈치·손·이마 관계를 가진 일반 경례 전체를 재사용 검토. 손바닥 방향은 원문에서 선택한 경례 변형을 유지. 군대 국가별 규칙은 추가 참조.'),
    ('V038','cand_e64dd1a84521597eb8aa480ca3914d00','refine','기존은 전완 교차·팔꿈치-어깨 연결. 손의 반대 상완 끝점까지 요구하는 연구 제안은 별도 강화 검토.'),
    ('V039','cand_91c2918810b350e6b647b5a306204a35','reuse','일반 뒷짐을 전체 재사용 검토. 기존의 손 연결이 보이거나 미확정이라는 한계를 보존. 후면 검증 장면을 별도로 지정하며 정면 가림을 PASS로 바꾸지 않는다.'),
    ('V075','cand_c1d2449faaac58e997f9ff0d44d63b20','reuse','기존 일반 로우앵글은 장르 독립적으로 재사용. 연구의 관찰 게이트는 장면 검증 제안이며 기존 후보가 모든 3개 게이트를 이미 보장한다는 뜻이 아니다.'),
    ('V072','cand_56fcd8431d0e5067bed376ea3dbde4ef','new','기존은 음식·식판·접이식 탁자·TV의 완결된 장면. 일부를 삭제해 군용 빈 식판으로 재사용하지 않는다.'),
    ('V009','cand_8809d507a5195582bdc7f33ee20cb09c','new','puffed fabric/gathered openings의 모양으로 붉은 사각 하의가 아니다. 영어 gathered shorts 내부 부분문자열 red shorts는 어휘 오탐.'),
    ('V067','cand_ba50d9c82b755c89941eb2e4d4b9b51b','new','복도 공통 소실점의 shared vanishing 표현. red van 부분문자열 적중은 차량의 의미 적중이 아니다.'),
    ('V059','cand_b7ea6fbd250956f2b5751b10045f6d00','new','소셜 재게시 컨테이너는 물리 컨테이너 적층이 아니다.'),
    ('V059','cand_ea114faf6d4f56d89fb328244a078fcc','new','우주선 프레임에 고정된 화물 컨테이너 전체 관계를 지상 성채로 바꾸지 않는다.'),
    ('V002','cand_de01dde25dab5e13b5bbc5a86a31f9b8','new','튜닉 주머니 릴과 줄·카드 집게가 있는 의무용 신분 카드. 가슴에 평평한 적색 천 패치와 구조가 다르다.'),
    ('V061','cand_e910ca5115f153439d808197c7f48356','new','기존은 선량계·승무원·해치·조밀한 수납함의 우주 대피실. 병영 침상·관물함으로 축약 불가.'),
]

EVAL = [
    ('R01','각진 짧은 챙 모자와 야구모자를 구분','distinguish a faceted short-brim cap from a baseball cap','V001','faceted crown and brim required','cap alone proves Marine identity'),
    ('R02','상의 가슴의 붉은 천 명찰','a red cloth name tape on the shirt chest','V002','patch on cloth','lanyard badge or red light'),
    ('R03','맨가슴 표면 위 별도 패치','a separate patch against an adult upper chest','V003','skin versus cloth carrier','piercing or wound automatically added'),
    ('R04','발목 높이 끈 부츠와 매트한 갑피','ankle-height laced boots with matte uppers','V004','height laces sole','tall fashion suede boots'),
    ('R05','삼각 붉은 하의','opaque red adult briefs','V008','high-cut separate openings','puffed gathered shorts'),
    ('R06','두 짧은 다리가 있는 붉은 사각 하의','red boxer shorts with two fabric legs','V009','short legs and hems','briefs or red scene illumination'),
    ('R07','불투명 하의의 성인 맨상체','adult uncovered torso above opaque lower clothing','V011','adult and clothing boundary','sexual orientation or act'),
    ('R08','같은 사람 모자챙 아래의 얼굴 암부','a shadow beneath the same person’s cap brim','V018','brim and face relation','window grid shadow or skin colour'),
    ('R09','기계 목 관절이 지지하는 모니터 머리','a monitor head supported by a mechanical neck joint','V023','head neck torso continuity','hand-held monitor'),
    ('R10','큰 눈과 작은 굳은 입','wide eyes and a small rigid mouth','V031','eye and mouth shape','diagnosis or consent'),
    ('R11','한 성인이 자기 이마 옆으로 경례','one adult salutes beside their own forehead','V036','shoulder elbow wrist endpoint','another person’s hand or visor gesture'),
    ('R12','같은 사람 가슴 앞의 교차 전완','forearms crossed in front of the same person’s chest','V038','owned arms','two people arm in arm'),
    ('R13','후면에서 보이는 뒷짐 손 연결','rear view showing both hands behind the back','V039','rear endpoints observable','front-view occlusion passed'),
    ('R14','자기 허리에 얹은 양손','both hands resting on the actor’s own waist','V040','correct hand ownership','hands on another person'),
    ('R15','성인 A가 성인 B를 내려다보기','adult A looks down toward adult B','V042','observer and target distinct','camera direction substituted for gaze'),
    ('R16','별도 대상을 향한 검지 축','index finger axis directed toward a separate target','V043','owner hand target','finger target swapped'),
    ('R17','전신 성인의 손바닥과 발끝 지지','a clothed adult supported on palms and toes','V054','floor support endpoints','pose proves hazing'),
    ('R18','장애물에서 멀어지는 쪽으로 기운 주자','runner oriented away from a visible obstacle','V056','proxy only with obstacle','still pose proves elapsed retreat'),
    ('R19','17층이 모두 보이는 컨테이너 탑','a container tower with all seventeen tiers visible','V060','count 17 distinct tiers','label 17 or merely tall'),
    ('R20','침상 줄 사이 통로와 옆 관물함','bunk rows with an aisle and adjacent lockers','V061','ground room topology','space shelter or social container'),
    ('R21','옆창이 있는 닫힌 승객실의 붉은 승합차','red minibus with an enclosed windowed passenger cabin','V067','vehicle shell and wheels','shared vanishing-point lexical hit'),
    ('R22','고정 턱과 조절 나사가 있는 몽키스패너','adjustable wrench with fixed jaw and adjusting screw','V071','moving fixed jaws and handle','pliers or pipe wrench'),
    ('R23','칸막이와 외곽 테두리가 보이는 식판','compartmented meal tray with dividers and outer rim','V072','tray topology','decorative chest panel or TV dinner bundle'),
    ('R24','아래에서 올려다보는 화면','an upward-looking low-angle frame','V075','camera framing','downward gaze alone'),
    ('R25','성인 둘의 같은 깊이 체격 대비','two adult figures with different proportions at equal depth','V077','shared scale reference','one actor nearer to camera'),
    ('R26','한 인물로 수렴하는 만화 집중선','comic focus lines converging toward one figure','V082','graphic radial marks','real rays or parallel speed lines'),
    ('R27','만화의 평행 속도선','parallel graphic speed lines in a comic','V083','medium-compatible graphic marks','real motion speed certified'),
    ('R28','물체 위 만화 냄새선','drawn odour lines above an object','V088','graphic proxy','odour or toxin chemistry proven'),
    ('R29','해병문학 장르만 요청','request only the Marine-literature genre','NONE','context only; no hard visual activation','red briefs gore or sexual styling forced'),
    ('R30','전우 간 평범한 우애','ordinary camaraderie among comrades','NONE','polysemy unresolved without explicit context','homosexuality or sexual violence inferred'),
    ('R31','해병맥주라는 이름의 덮인 용기','a covered vessel labelled with a fictional menu name','V074','contents UNKNOWN; diagnostic proxy only','urine or semen inferred from colour'),
    ('R32','원래의 민간인 자원입대','literal voluntary enlistment by an adult civilian','NONE','literal versus ironic sense explicit','abduction inferred from the word enlistment'),
    ('R33','현실 포항의 거리 사진','documentary street photography in real Pohang','NONE','real place boundary','17-tier fortress automatically inserted'),
    ('R34','일반 성인 운동의 플랭크','an adult performing a normal exercise plank','V054','exercise context distinct','abuse inferred from identical pose'),
    ('R35','황근출 이름만 입력','only the character name Hwang Geun-chul','NONE','version choice required','single face body or costume fixed'),
    ('R36','부활을 한 장의 사진으로 증명','prove resurrection from one photograph','T002','UNOBSERVABLE_NOT_PASS','presence treated as life history proof'),
    ('R37','정면에서 가려진 뒷짐 손가락','hidden fingers behind the back in a front view','V039','UNOBSERVABLE_NOT_PASS','hidden interlacing accepted'),
    ('R38','해병 도게자의 일반 절과 원문 변형 비교','compare a clothed bow with the source-specific altered dogeza','V053','different realizations; context retained','clothed bow called exact explicit scene reproduction'),
    ('R39','작은 지위의 성인과 거구의 성인','an ordinary-sized adult beside an exaggerated adult','V024','both adult','small body recast as child'),
    ('R40','색 표면만으로 물질 정체 알 수 없음','surface colour cannot identify a substance','NONE','composition stays UNKNOWN','brown substance proved feces or meat proved human'),
]


def dump(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')


def main():
    tables = json.loads((HERE / 'conversation-tables.json').read_text())
    sources = [dict(zip(SOURCE_KEYS, row), accessed_at='2026-10-24 Asia/Seoul') for row in SOURCES]
    dump('sources.json', sources)
    source_md = ['# 출처와 주장 범위', '', '접근일: 2026-10-24 KST. 원문·이용자 사용례·비평·제조사·제작 문서를 구분한다. 링크 하나는 하나의 고유 출처이며 재조회 결과를 중복 집계하지 않는다.', '']
    for s in sources:
        source_md += [f"## {s['id']} [{s['title']}]({s['url']})", '', f"- 발행: {s['publication_date']} / 종류: `{s['kind']}` / 열람: `{s['access_status']}`", f"- 확인 범위: {s['supports']}", f"- 한계: {s['limits']}", '']
    (HERE / 'SOURCES.md').write_text('\n'.join(source_md))
    routes = []
    for ti, table in enumerate(tables):
        for ri, row in enumerate(table[1:]):
            term, description = row[0], ' | '.join(row[1:])
            matched = [c['id'] for c in CARDS if term in c['seed_terms']]
            if ti == 22:
                mode = 'confusion_boundary'
            elif ti == 21:
                mode = 'authored_scene_example'
            elif ti in (10, 11, 12):
                mode = 'sensitive_context_diagnostic'
            elif ti in (6, 7):
                mode = 'versioned_character_context'
            elif ti in (0, 1, 2, 13):
                mode = 'advisory_context'
            elif ti in (3, 4):
                mode = 'audio_or_rhetorical_context'
            elif matched:
                mode = 'optional_visual_realization'
            else:
                mode = 'context_or_deferred_visual_definition'
            routes.append({
                'id': f'K{len(routes)+1:03}', 'table_index': ti+1, 'row_index': ri+1,
                'section': HEADINGS[ti], 'term': term, 'original_definition': description,
                'classification': mode, 'source_ids': ['S00'],
                'independent_definition_verification': 'not blanket-verified; see RESEARCH and specific source scope',
                'optional_realization_ids': matched,
                'hard_activation': False, 'automatic_bundle': False,
                'unresolved_visual_route': not matched,
                'adoption': 'context' if mode != 'optional_visual_realization' else 'review realisations individually',
            })
    dump('keyword-routes.json', routes)
    atlas = ['# 전체 대화 키워드 지도', '', '247행 = 용어·외형 등 231행 + 창작 조합 7행 + 혼동 9행. 중복·다의어를 임의 합치지 않았다. 연결된 카드도 개념 전체와 동일하지 않으며 명시적 선택 전에는 hard activation을 하지 않는다.', '', '|ID|절|원래 항목|원래 뜻·설명|분류|선택형 카드|', '|---|---|---|---|---|---|']
    for r in routes:
        values = [r['id'],r['section'],r['term'],r['original_definition'],r['classification'],', '.join(r['optional_realization_ids']) or '문맥 보존 / 구체화 대기']
        atlas.append('|'+ '|'.join(str(x).replace('|',' / ').replace('\n',' ') for x in values)+'|')
    (HERE / 'KEYWORD-ATLAS.md').write_text('\n'.join(atlas)+'\n')
    dump('semantic-cards.json', CARDS)
    visual = ['# 시각 의미 카드', '', '모든 구체적 장면은 연구자의 선택형 제안이다. 인물 이름·장르명·출처만으로 활성화하지 않는다. 원본 이미지 생성·픽셀 평가는 수행하지 않았다.', '']
    for c in CARDS:
        visual += [f"## {c['id']} {c['label']}", '', f"- 모드 / 우선순위: `{c['mode']}` / `{c['priority']}`", f"- 연결 입력: {', '.join(c['seed_terms'])}", f"- 슬롯 제안: {', '.join(c['planned_slots'])}", f"- 소유자: {' / '.join(n['id']+': '+n['description'] for n in c['owners'])}", f"- 방향 관계: {' / '.join(e['subject']+' → '+e['predicate']+' → '+e['object'] for e in c['relations'])}", f"- KO: {c['proposal_ko']}", f"- EN: {c['proposal_en']}", f"- 혼동 경계: {c['confusion_boundary']}", f"- 출처: {', '.join(c['source_ids'])}. {c['source_scope']}", '- 게이트: 아래 세 그룹을 같은 이미지 또는 지정된 칸 안에서 함께 확인한다. 가림은 UNOBSERVABLE_NOT_PASS, 일부 충족은 PARTIAL, 차단은 BLOCKED_UNSCORED.', '']
        visual += [f"  - {g['id']}: {g['ko']} / {g['en']}" for g in c['components']]
        visual += ['']
    (HERE / 'VISUAL-CARDS.md').write_text('\n'.join(visual))
    audit = json.loads((HERE / 'corpus-positive-audit.json').read_text())
    examples = {r['id']:r for q in audit['queries'].values() for r in q['full_record_examples']}
    # The narrow discovery retains all chosen records in its full example closure.
    mappings = []
    for card, cid, decision, reason in MAPPING_SPECS:
        row = examples[cid]
        mappings.append({'card_id':card,'existing_id':cid,'decision':decision,'reason':reason,
                         'record_file':row['file'],'record_sha256':row['record_sha256'],
                         'existing_record':row['record'],'existing_bindings':row['bindings'],
                         'review_scope':'full candidate conditions/content/effects/provenance and every attached binding inspected; no runtime execution'})
    dump('existing-source-mapping.json', mappings)
    decisions = {}
    for c in CARDS:
        known = [m for m in mappings if m['card_id']==c['id']]
        decision = 'context' if c['id'] in DIAGNOSTIC_CARDS else next((m['decision'] for m in known if m['decision'] in ('reuse','refine')), 'new')
        decisions[c['id']] = {'decision':decision,'status':'tentative research recommendation; rebaseline and semantic deduplication required before source mutation',
                               'existing_ids':[m['existing_id'] for m in known],
                               'rationale':' | '.join(m['reason'] for m in known) if known else 'No reviewed equivalent selected in bounded lexical discovery; this does not establish semantic absence. Review complete adjacent records before creating anything.'}
    with (HERE / 'DATA-ADOPTION.tsv').open('w', newline='') as f:
        w = csv.writer(f, delimiter='\t');w.writerow(['card_id','label','decision','existing_ids','status','rationale'])
        for c in CARDS:
            d=decisions[c['id']];w.writerow([c['id'],c['label'],d['decision'],','.join(d['existing_ids']),d['status'],d['rationale']])
    drafts=[]
    for c in CARDS:
        if c['id'] in DIAGNOSTIC_CARDS:
            continue
        drafts.append({
            'draft_id':'D_'+c['id'],'research_card_id':c['id'],'schema':'marine-literature-research-draft/v1',
            'planned_record_kind':'visual_option','registration_status':'not_in_operating_manifest',
            'proposed_positive_text':{'ko':c['proposal_ko'],'en':c['proposal_en']},
            'planned_slots':c['planned_slots'],'owner_graph':{'nodes':c['owners'],'edges':c['relations']},
            'required_component_groups':c['components'],'mode':c['mode'],
            'preconditions':['Requester explicitly adopts this full realization within already frozen counts, people and locked dimensions.',
                             'Bind every node to the requester-owned actor, garment, object or representation.',
                             'A human figure here is an adult. This is not permission for sexual presentation.',
                             'Graphic modes require an explicitly compatible comic/illustrated medium.',
                             'Check source and binding conditions and full effects, including all inherited exclusions.',
                             'Choose sibling alternatives separately; never union mutually exclusive garment or medium forms.'],
            'adoption_recommendation':decisions[c['id']],
            'excluded_from_positive_projection':['original sensitive definitions','claim_limits','negative cases','source labels','adoption rationale','unselected character identity'],
            'native_qualification':'NOT_RUN','runtime_registered':False,
        })
    dump('candidate-drafts.json',drafts)
    evals = []
    for eid, ko, en, card, required, forbidden in EVAL:
        evals.append(dict(id=eid,query_ko=ko,query_en=en,expected_card=card,
                          required_boundary=required,forbidden_inference=forbidden,
                          execution_status='NOT_RUN',results=None))
    dump('evaluation-cases.json',evals)
    counts={'keyword_rows':len(routes),'tables':len(tables),'semantic_cards':len(CARDS),'candidate_drafts':len(drafts),
            'sources':len(sources),'body_or_selected_section_reviewed_sources':sum(s['access_status'] in ('body_reviewed','marine_section_reviewed','relevant_body_reviewed','selected_body_reviewed') for s in sources),
            'existing_full_record_comparisons':len(mappings),'evaluation_cases':len(evals),'bilingual_query_strings':2*len(evals),
            'card_modes':dict(Counter(c['mode'] for c in CARDS)),'route_classes':dict(Counter(r['classification'] for r in routes)),
            'adoption_recommendations':dict(Counter(d['decision'] for d in decisions.values())),
            'runtime_changes':0,'image_generations':0,'actual_retrieval_runs':0}
    dump('PACKAGE-COUNTS.json',counts)
    print(json.dumps(counts,ensure_ascii=False))


if __name__ == '__main__':
    main()
