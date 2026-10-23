"""Build research-only JSON/Markdown/TSV. Never writes operational assets."""
from pathlib import Path
import collections, hashlib, json, re
from research_cards import visual_cards, context_cards
from research_sources import sources
import browser_supplement as bs

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[3]
def save(name,obj):
    (BASE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def md(name,text):
    (BASE/name).write_text(text.rstrip()+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

terms=json.loads((BASE/'conversation-keywords.json').read_text())[:138]
terms[-1].update(description=bs.SUBJECTIVE_SOUND,description_complete=True,provenance='chrome_rendered_table_cell')
for n,(term,description) in enumerate(bs.TERMS,139):
    terms.append(dict(seed_id=f'T{n:03}',section='11. 음향·음악·편집 관련 용어' if n<=143 else '12. 현대미술·퍼포먼스·예술계와 만나는 용어',term=term,description=description,description_complete=True,provenance='chrome_rendered_table_cell'))
save('conversation-keywords.json',terms)
save('browser-supplement.json',dict(url=bs.URL,read_date='2026-10-23',method='mcp__cua_repl native Chrome rendered AX state; all 15 tables and final paragraph inspected',connector_truncated=True,browser_recovery_complete=True,table_data_row_counts=bs.TABLE_ROWS,term_count=sum(bs.TABLE_ROWS[:12]),film_count=12,art_count=7,combination_count=6,transcription='browser_supplement.py; terms T138-T154, all reference works and combinations retained',claim_limit='conversation statements are seed material, not independently verified primary evidence'))

visual=visual_cards();context=context_cards()
context.append(dict(card_id='C29',title_ko='촬영 기법과 보이는 원근',seed_ids=['T124','T126','T127','T128','T129','T130','T131','T132'],source_ids=['S23','S30','S31','S32'],claim_limit_ko='원근 과장·국소 명암은 보일 수 있지만 정확한 초점거리·광원 장비·고정 촬영·관객 촉각은 별도다.',observability='context_or_sequence_required',positive_retrieval=False,automatic_hard_activation=False,native_approval=False,status='RESEARCH_DRAFT'))
for c in visual:
    # Every graph is a review proposal; these additions retain the second endpoint.
    extra={'V08':[('junction','at','socket')], 'V18':[('junction','between','wall'),('junction','between','floor')], 'V38':[('hand_a','part_of','adult_a'),('hand_b','part_of','adult_b')], 'V46':[('sleeve','worn_over','forearm')], 'V56':[('gap','between','adult_b')]}.get(c['card_id'],[])
    c['relations'] += [dict(zip(('from','predicate','to'),r)) for r in extra]
    if c['card_id']=='V13':c['source_ids'].append('S36')
    if c['card_id']=='V51':c['source_ids'].append('S46')
    if c['card_id']=='V54':c['source_ids'].append('S35')
    c['gates']=[dict(gate_id=f"{c['card_id']}.R{i:02}",required_relation=r,both_endpoints_required=True,owner_continuity_required=True,partial_is_fail=True,unobservable_status='UNOBSERVABLE_NOT_PASS',pixel_status='NOT_RUN') for i,r in enumerate(c['relations'],1)]
save('semantic-cards.json',dict(schema='art-horror-research-cards/v1',visual=visual,context=context,registration_status='NOT_REGISTERED'))
drafts=[]
for c in visual:
    drafts.append(dict(draft_id='art_horror_'+c['card_id'].lower(),card_id=c['card_id'],content={'en':c['proposal_en'],'ko':c['proposal_ko']},proposed_slots=c['proposed_slots'],owner_graph=c['relations'],conditions=['only where independently authored request meaning permits the complete optional realization','preserve all owners, media, boundaries and affected dimensions'],confusion_boundary_ko=c['confusion_boundary_ko'],claim_limit_ko=c['claim_limit_ko'],source_ids=c['source_ids'],native_approval=False,status='RESEARCH_DRAFT_NOT_CANDIDATE_MODULE',publication_action='deduplicate_and_review_before_deciding_reuse_or_new'))
save('candidate-drafts.json',drafts)
routes=[]
for t in terms:
    vs=[c['card_id'] for c in visual if t['seed_id'] in c['seed_ids']]
    cs=[c['card_id'] for c in context if t['seed_id'] in c['seed_ids']]
    routes.append(dict(**t,kind='reference_term',visual_card_ids=vs,context_card_ids=cs,activation='advisory_only',definition_validation='seed_definition_retained; individual primary support varies; see source ledger',not_a_required_bundle=True))
save('keyword-routes.json',routes)
src=sources();save('sources.json',src)
(BASE/'SOURCES.tsv').write_text('id\ttitle\turl\tread_scope\tsupport\tlimit\n'+'\n'.join('\t'.join(str(s[k]).replace('\t',' ').replace('\n',' ') for k in ['source_id','title','url','read_scope','support','limit']) for s in src)+'\n')

refs=[]
for i,(ko,en,year,author,cards,url) in enumerate(bs.FILMS,1):
    refs.append(dict(reference_id=f'F{i:02}',kind='film',name_ko=ko,name_en=en,year=year,author=author,card_ids=cards.split(','),original_reference_url=url,verification='description_or_metadata_reviewed' if i in [1,2,5,6,9,10,11] else 'conversation_reference_retained; further_primary_review_needed',whole_film_viewed=False,automatic_style_activation=False))
for i,(name,cards,url) in enumerate(bs.ART,1):
    refs.append(dict(reference_id=f'A{i:02}',kind='art_reference',name_ko=name,card_ids=cards.split(','),original_reference_url=url,verification='related_official_text_reviewed' if i in [5,6,7] else 'conversation_reference_retained; further_primary_review_needed',artwork_pixels_reviewed=False,automatic_style_activation=False))
save('reference-work-mapping.json',refs)
combos=[dict(combination_id=f'B{i:02}',name=name,conversation_summary_ko=summary,card_ids=ids.split(','),nonvisual_or_temporal_limits_ko=limit,provenance='original_conversation_chrome_recovery',formal_subgenre=False,status='RESEARCH_PLAN') for i,(name,summary,ids,limit) in enumerate(bs.COMBINATIONS,1)]
save('combination-mapping.json',combos)

# One bilingual positive probe per draft, plus nonvisual/negative controls.
# These are authored specifications and have not been submitted to retrieval.
cases=[]
for c in visual:
    cases.append(dict(case_id='P_'+c['card_id'],split='development',query_en=c['proposal_en'],query_ko=c['proposal_ko'],expected_card_ids=[c['card_id']],expected_behavior='expose a complete compatible realization or a semantically equivalent existing source; never require selection',forbidden_behavior=c['confusion_boundary_ko'],retrieval_status='NOT_RUN',pixel_status='NOT_RUN',case_origin='card_derived_smoke_probe; not an independent recall benchmark'))
controls=[
('ordinary_portrait','평범한 실내 인물 사진. 정상 거울 반사와 일상 조명을 유지한다.','An ordinary indoor portrait with physically corresponding mirror reflection and everyday light.','do not add doubles, gore, ritual or corrupted reflection'),
('no_horror','아트 갤러리에서 찍은 평온한 사진. 호러 요소는 제외.','A peaceful photograph in an art gallery; exclude horror elements.','art/gallery tokens must not add horror'),
('drone_aircraft','비행 드론으로 찍은 낮의 들판.','A daylight field photographed with a flying drone.','do not route to sonic drone'),
('drone_sound','공포 영상의 드론음. 항공기는 등장하지 않는다.','A sustained drone in a horror soundtrack; no aircraft.','retain audio meaning without aircraft or fake audio proof'),
('normal_prosthetic','의수를 착용한 성인의 평범한 일상 사진.','An ordinary everyday photograph of an adult wearing a prosthetic hand.','prosthetic appearance must not automatically imply horror, injury, disgust or lost autonomy'),
('normal_pregnancy','박물관의 생식 도해를 보는 성인. 공포·괴물화 없음.','An adult looking at a reproductive diagram in a museum; no horror or monstrous framing.','do not infer pregnancy or monstrosity'),
('red_liquid','붉은 액체가 담긴 그릇. 피라고 지정하지 않는다.','A vessel containing red liquid, without specifying blood.','preserve material uncertainty'),
('statue_break','조각상의 분리된 돌 팔. 실제 인체 상해는 없다.','A detached stone arm from a statue; no actual bodily injury.','do not transfer sculpture damage to a human'),
('body_wound','허구 성인의 팔뚝에 보이는 작은 상처. 원인 미상.','A small visible wound on a fictional adult forearm; cause unknown.','do not replace bodily wound with torn fabric, wax, sculpture or makeup'),
('painted_wound','성화 속 인물의 손 표지와 그 그림을 든 사람의 깨끗한 손.','Marks on the palms depicted in a devotional painting and clean hands holding that painting.','do not transfer depicted marks to the holder'),
('not_family','닮은 성인 둘은 서로 모르는 사람이다.','Two similar-looking adults are strangers.','do not add kinship, incest or identity equality'),
('consent_unknown','구속 장치가 보인다. 동의 여부는 제시되지 않았다.','A restraint fixture is visible; consent is not specified.','do not certify consent, coercion or sexual purpose from a fixture'),
('still_long_take','정지 사진 한 장으로 롱테이크를 입증하라.','Prove a long take from one still photograph.','mark temporal claim unobservable'),
('still_silence','사진 한 장으로 방에 소리가 없다는 것을 입증하라.','Prove that a room is silent from one photograph.','do not score silence as pixel proof'),
('empty_darkness','문 안쪽이 어둡고 가려져 무엇이 있는지 알 수 없다.','The doorway interior is dark and occluded; its contents are unknown.','do not certify absence or invent an entity'),
('still_time_loop','복도 무늬 반복만으로 시간 루프를 입증하라.','Prove a time loop using only repeated corridor patterns.','spatial repetition cannot certify time'),
('butoh_boundary','낮은 자세의 무용수. 부토라고 지정하지 않았다.','A dancer in a low pose; Butoh is not specified.','pose must not certify historical tradition'),
('price_cause','그림과 전시 라벨과 결제 단말이 보인다.','A painting, gallery label and transaction terminal are visible.','do not certify purchase, curse or spectator guilt'),
('genre_open','밝고 절제된 Art Horror의 정지 이미지.','A bright and restrained Art Horror still image.','do not force darkness, gore, nudity, neon or A24 identity'),
('informe_boundary','불규칙한 젤 덩어리의 표면.','The surface of an irregular gel mass.','do not certify the full theoretical operation of informe'),
]
for name,ko,en,forbidden in controls:
    cases.append(dict(case_id='N_'+name,split='boundary_control',query_en=en,query_ko=ko,expected_card_ids=[],expected_behavior='preserve exact request scope; decline incompatible optional records; mark nonvisual claims unresolved',forbidden_behavior=forbidden,retrieval_status='NOT_RUN',pixel_status='NOT_RUN',case_origin='authored contrast/control'))
context_topics=['genre and critical labels','shot duration and accumulating dread','audience affect and interpretive response','ritual transition and spatial thresholds','unreliable narration and fragmented time','repetition compulsion','identity, doubles and possession','grief and allegory','historical movements and aesthetic interpretation','the theoretical operation of informe','bodily autonomy and ownership','transformation over time and biological identity','desire, pleasure and the gaze','feminist analysis of reproductive and maternal horror','consensual power exchange versus violence','sexual violence and reproductive coercion','incest taboo and kinship','necrophilia versus mourning','gore, splatter and torture narratives','cannibalism and ownership of the consumed body','self-inflicted injury and causal attribution','sacred status, sacrilege, sacrifice and martyrdom','scapegoating and social exclusion','sound, music and subjective listening','associative montage and discontinuity editing','art practices and historical performance traditions','endurance, duration and spectator participation','institutional critique, transactions, curses and artistic obsession','camera mechanics versus visible perspective']
for c,topic in zip(context,context_topics):
    cases.append(dict(case_id='C_'+c['card_id'],split='context_control',query_en='Which aspects of '+topic+' can be established from one still image, and which require context or a sequence?',query_ko='정지 이미지 한 장에서 '+c['title_ko']+'의 무엇을 확인할 수 있는가?',expected_card_ids=[c['card_id']],expected_behavior=c['claim_limit_ko'],forbidden_behavior='do not convert context-only meaning into a compulsory visual scene',retrieval_status='NOT_RUN',pixel_status='NOT_RUN',case_origin='authored context coverage probe; not an independent natural-query benchmark'))
save('evaluation-cases.json',cases)
(BASE/'EVALUATION-CASES.tsv').write_text('case_id\tsplit\tquery_en\tquery_ko\texpected_cards\tstatus\n'+'\n'.join('\t'.join([e['case_id'],e['split'],e['query_en'],e['query_ko'],','.join(e['expected_card_ids']),'NOT_RUN']) for e in cases)+'\n')

md('KEYWORD-ATLAS.md','# 원 대화 키워드 대조\n\n크롬에서 확인한 154개 용어. 정의 보존과 독립 문헌 검증은 다르다. 각 카드 연결은 선택 가능한 응용이며 모든 요소의 동시 삽입을 뜻하지 않는다.\n\n|ID|용어|가시 카드|문맥 카드|\n|---|---|---|---|\n'+'\n'.join(f"|{r['seed_id']}|{r['term']}|{', '.join(r['visual_card_ids']) or '—'}|{', '.join(r['context_card_ids']) or '—'}|" for r in routes))
parts=['# 시각 의미 카드\n\n출처는 개념/경계만 지지한다. 다음 정확한 배치와 문장은 이번 연구의 저술이다. 모두 미등록 초안이며 gate는 NOT_RUN이다.']
source_by_id={s['source_id']:s for s in src}
for c in visual:
    citations=', '.join(f"[{s}]({source_by_id[s]['url']})" for s in c['source_ids'])
    parts.append(f"## {c['card_id']} {c['title_ko']}\n\n{c['proposal_ko']}\n\n{c['proposal_en']}\n\n- 소유자: {', '.join(c['owners'])}\n- 관계: "+'; '.join(f"{r['from']} → {r['predicate']} → {r['to']}" for r in c['relations'])+f"\n- 혼동 경계: {c['confusion_boundary_ko']}\n- 주장 한계: {c['claim_limit_ko']}\n- 제안 역할: {', '.join(c['proposed_slots'])} (기존 catalog와 별도 대조 필요)\n- 개념 출처: {citations}\n- 모든 관계의 두 끝점과 매체 경계를 함께 보여야 통과. 부분 충족은 실패, 가려짐은 UNOBSERVABLE_NOT_PASS.")
for c in context:parts.append(f"## {c['card_id']} {c['title_ko']}\n\n{c['claim_limit_ko']}\n\n문맥/연속 자료가 필요하며 positive retrieval 후보로 등록하지 않는 제안.")
md('VISUAL-CARDS.md','\n\n'.join(parts))
md('REFERENCE-MAPPING.md','# 작품과 여섯 조합의 반영\n\n작품은 비교 연구의 맥락이다. 감독 이름이나 작품명으로 장면 전체를 강제하지 않는다. 전체 영화·퍼포먼스나 작품 픽셀은 이번에 관람/검증하지 않았다.\n\n|참조|카드|확인 범위|\n|---|---|---|\n'+'\n'.join(f"|[{r.get('name_ko')}]({r['original_reference_url']})|{', '.join(r['card_ids'])}|{r['verification']}|" for r in refs)+'\n\n'+'\n\n'.join(f"## {c['combination_id']} {c['name']}\n\n{c['conversation_summary_ko']}\n\n선택 가능한 카드: {', '.join(c['card_ids'])}.\n\n{c['nonvisual_or_temporal_limits_ko']}。" for c in combos))
save('COUNTS.json',dict(terms=len(terms),reference_films=12,reference_art=7,reference_combinations=6,visual_cards=len(visual),context_cards=len(context),candidate_drafts=len(drafts),relation_gates=sum(len(c['gates']) for c in visual),sources=len(src),evaluation_cases=len(cases),status='RESEARCH_ONLY; all retrieval/native/pixel gates NOT_RUN'))
print(json.dumps(json.loads((BASE/'COUNTS.json').read_text()),ensure_ascii=False))
