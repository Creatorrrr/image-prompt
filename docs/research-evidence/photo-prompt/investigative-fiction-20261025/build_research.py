"""Build research artifacts in this folder only; never write runtime assets."""
from pathlib import Path
import collections, csv, hashlib, json, re
from research_sources import SOURCES

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def read_tsv(name): return list(csv.DictReader((HERE/name).open(),delimiter='\t'))
def write(name,data): (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def sha(data): return hashlib.sha256(data).hexdigest()
DEFAULT_CONTEXT={1:'C01',2:'C06',3:'C08',4:'C02',5:'C36',6:'C12',7:'C33',8:'C32',9:'C16',10:'C15',11:'C39',12:'C17',13:'C34',14:'C20',15:'C31',16:'C29',17:'C13',18:'C01',19:'C31',20:'C31',21:'C01',22:'C30',23:'C39',24:'C37',0:'C38'}
SECTIONS=['장르와 하위 유형','추리 질문','독자의 의심과 발견','인물과 직무','캐릭터 관계','수사 절차','면담 추가 용어','증거와 판단','사망 조사','물질과 흔적','디지털·영상·금융','범죄행동 분석','폭력 사건 소재','성적·착취 소재','형사·탐정 복식','보호구·성인 복식','소품·기록물','현장 포즈','면담·잠복·이후 포즈','외형 상태','장소','조명과 화면','혼동 경계','창작 조합']
DECISIONS={
 'cand_0537b275d1ae521882cf15be7252c546':('refine','A02','표지 소품을 재사용하되 ko가 영어이고 흔적과의 거리·비접촉 관계가 없다. 역할 소품의 뜻을 유지한 번역 수정과 완결 배치 대안을 구별한다.'),
 'cand_f33ca96f48b15c13af416859d150bbbf':('separate_new','A02,A06','전체 뜻은 표지 자체를 검사하는 행위다. 단순히 흔적 관찰로 고치면 기존 의미가 바뀐다. 번역은 별도 수정하고 흔적을 관찰하는 새 완결 행위와 분리한다.'),
 'cand_2b800be525185932840b422eb39a7318':('refine','A02,A03','표지 있는 매크로 구도는 재사용 가능한 조각이나 ko 영어 복제와 표지/흔적의 대응 부족이 있다. composition-only effects가 표지 추가까지 포괄하는지 재심사한다.'),
 'cand_1eb3b0a78fe45e6fa7caefdc756de87e':('refine','A06,A10','감식요원 역할의 일반 source이며 구체 손·도구·대상은 없다. 직무를 유지하는 한영 보완과 구체 절차 후보를 구분한다.'),
 'cand_48c178c2f95e517a9d48c01f263e72d7':('refine','V10','evidence table을 장소로 쓴 in a table 구문과 ko 영어 복제를 수정할 필요가 있다. 실험실/탁자/검체 배치의 서로 다른 효과를 확인한다.'),
 'cand_57948cd35b145601acfaf456e48c4773':('reuse_review','A10','사진·측정·기록·수집의 분리된 팀이 이미 있다. forensic_documentation primary tag 조건과 인원·subject effects를 유지하고 새 요청에 임의 팀을 추가하지 않는다.'),
 'cand_473a01898b8f56a89b570b6abeaa2cb3':('reuse_review','A02,A03,A09','번호·눈금·방향·기록 묶음이 이미 있다. 전체 묶음을 유지하거나 독립 source를 만든다. 현재 effects가 비어 있어 실제 물체·텍스트 효과 심사가 먼저다.'),
 'cand_f2f53ecfabb85d73a05cc58669d5f687':('context_or_scope_review','A01,A07','절차극 분위기와 여러 기록 단계가 style source에 함께 들어 있다. 전체 과정 완료를 단일 사진 근거로 만들지 않으며 primary guard와 binding 도메인 제한을 우회하지 않는다.'),
 'cand_0b4636efd87b5c8698ae491b5fb9ded3':('sequence_review','A03,A07','전체→중경→근접 sequence를 명시한다. 단일 프레임 대안으로 몰래 축소하지 말고 시간/다중 매체 경로 또는 별도 현재 상태 후보로 구분한다.'),
 'cand_fea8812d28385f49a500aff5bae27f89':('sequence_review','A07','수집 전 여러 단계를 완료하는 행위다. 현재 촬영하는 한 순간과 전 단계 완료를 구별하고 action-only effects의 전체 범위를 심사한다.'),
 'cand_c992d70a7fff5b75a846be777713b817':('reuse_review','A08,A09','봉투·검체관·별도 식별/인계 칸의 기존 완결 대안. 종이 봉투 봉인 경계나 전체 chain을 추가로 보장한다고 보지 않으며 폭넓은 현재 effects를 유지한다.'),
 'cand_07f13b5beb5d52568d47442d169b817c':('reuse_review','A05,F06','참여자의 검체와 기록 대응은 이미 있다. 채취된 표본이라는 문맥·실제 참여자·기존 relationship/appearance 효과를 보존해야 하며 단순 튜브 정물과 동의어가 아니다.'),
 'cand_0f1f2271459359a58559420f53e4be31':('separate_new','D01,D08','write-blocked reader가 있으나 anomalous_archive_world_audit_scene guard와 파형 모니터를 포함한 완결 묶음이다. 일반 디지털 수사를 위해 guard를 제거하거나 일부만 재명명하지 않는다.'),
 'cand_b9d95dc56e3f58188880f67e800e45de':('separate_new','N05','ko는 붉은 실 수사 보드지만 en/embedding에는 스스로 다시 팽팽해지는 마법이 있다. 원 마법 후보를 보존하고 현실 보드 후보를 별도로 만든다. effects도 전체 마법/물체 범위 재검토.'),
 'cand_9e1b54a3ca52524a8198a37aa7087ea3':('reuse_review','I06','사복 형사 역할은 이미 있으나 사복 외형이 경찰 신분을 입증하지 않는다. 역할 선언 source를 복식·배지 후보로 바꾸지 않는다.'),
 'cand_c256061df5145318a308ad06b3071546':('reuse_review','W01','탐정풍 트렌치 코스튬의 기존 범위를 보존. 현대 수사자의 공통 의상으로 등록하지 않고 구조적인 코트 대안과 구분한다.'),
 'cand_5ccf05cc8bd152caaf61d576b37698b8':('reuse_review','W01','견장·가슴 플랩·벨트/고리의 완결 대안이 이미 있다. 장르별 복제보다 재사용하고 긴 밑단·다른 부품의 추가는 별도 선택으로 심사한다.'),
 'cand_33a5a891d9a15891993a3a0c962a5519':('reuse_review','N01','문 빗장→문틀 받이의 직접 이웃이다. 밀실 alias를 모든 출입 불가능성의 증거로 쓰지 않으며 기존 material/relationship/setting effects도 함께 검토한다.'),
 'cand_4ff5a93163635a4e976d045fead48f93':('reuse_review','V05','앉은 성인의 앞쪽 두 수갑과 체인은 이미 있다. 앉음·성인·동일 소유자·두 손목을 보존하며 서 있는 호송으로 무심히 확장하지 않는다.'),
 'cand_a7847a8c92c5559f8001e7ed0b6b2e07':('reuse_limited','V03','인조 피부의 무대 분장 표본이다. 실제 멍·찰과상·방어흔·삭흔 source의 대체 충족으로 쓸 수 없다.'),
 'cand_22a2d3f315f755a8ae3583b5c94771e1':('reuse_limited','I04','성인 단독 인터뷰와 작은 마이크의 완결 대안이다. requires_adult_context와 촬영 거리 및 현재 폭넓은 효과를 보존. 두 사람 경찰 면담의 자동 대안은 아님.'),
 'cand_2a1177bfade25ab8a30a636640689689':('context_or_scope_review','','모집·이동·통제·착취를 한 경로로 잇는 서사 전체다. 일반 인신매매 정의에 이동을 필수화하지 않도록 좁은 선택적 이동 사례로 유지할지 심사한다.'),
 'cand_83b142140a9e565fbeeddab1c3698880':('context_or_scope_review','','다중 장소/단계 source이며 한 장소에서의 착취 사건을 빠뜨릴 수 있다. 모든 단계의 강제·시간·owner를 location 한 슬롯으로 승인하지 않는다.'),
 'cand_7ca839059cd25db78b696a559ec92f71':('reuse_limited','','허구 사지와 그에 대응하는 원래 몸의 분리 관계가 이미 있다. 화면 밖 잘림·다른 사람의 의지로 대체하지 않는다. 사망·사후성·절단 원인·고문 목적을 추가 보장하지 않는다.'),
 'cand_4f183450f5c558f990ac1fbf54ac3edc':('reuse_limited','','성인 허구 팔의 절단 경계·대응 팔뚝·분명한 틈의 완결 대안이다. generic gore를 새로 복제하기보다 기존 body_geometry/relationship 효과와 소유자를 심사한다. 시신 절단의 사후성은 별도.'),
 'cand_9ef920a7b8c2578098678ef065fce0e0':('context_reuse','','임상 노출·성적 관심·역할극·관음·침해·시체성애를 구분하는 diagnostic이며 binding이 없다. 수사물 문맥에서도 재사용하되 긍정 시각 후보로 전환하지 않는다.'),
 'cand_e1642d950e0a54d0a5491ce1da1ca6d6':('context_or_scope_review','','성적 행위·비동의·강압·거부·통제를 함께 서술한 선언 문맥이며 aesthetic/style 한 축으로 실제 모든 관계를 승인할 수 없다. 상처/옷을 동의 판단에 쓰지 않고 근거 없는 직접 역할 승격을 보류한다.'),
 'cand_4185bb56a6485490869ffc925bcb694a':('context_or_scope_review','','구금·공적 통제·중한 고통·목적을 가진 좁은 허구 고문 문맥이다. 모든 고문/가혹행위를 이 예로 정의하지 않으며 style-only effects를 완결 행위 권한으로 해석하지 않는다.'),
}

def main():
 sources=[{'id':'S00','title':'수사물 용어 정리 — 사용자 참조 대화','url':'https://chatgpt.com/c/6adc076c-0c60-83e8-a9a3-369c26c3ea65','access_date_kst':'2026-10-25','supported_claim':'Source vocabulary: 320 table term rows, 10 confusion rows, 8 scene examples, plus CSI effect in prose.','claim_limit':'User-selected prior research; untrusted reference, not independent authority or authorization.','access_level':'read_thread truncated + complete Chrome rendered DOM reviewed'}]
 for sid,title,url,claim,limit in SOURCES:
  level='web_page_text_or_targeted_index_excerpt'
  if sid in ['S19','S25','S26','S27','S29']: level='indexed_excerpt_or_catalog_only; full specific claim not certified'
  if sid=='S19': level='search-indexed primary excerpt; direct open returned 404; no full-page verification'
  if sid=='S25': level='primary-study abstract in search excerpt; direct open returned only site footer'
  if sid=='S26': level='search-indexed PDF excerpt/metadata; full PDF not reviewed'
  if sid=='S27': level='OHCHR catalog/search record only; manual body not reviewed'
  if sid=='S29': level='primary legal search excerpt for Article 244; Article 244-3 full current text not verified'
  sources.append(dict(id=sid,title=title,url=url,supported_claim=claim,claim_limit=limit,access_date_kst='2026-10-25',access_level=level))
 write('sources.json',sources)
 context=[]
 for r in read_tsv('context-cards.tsv'):
  r['term_keys']=r['term_keys'].split(';');r['source_ids']=r['source_ids'].split(',');r.update(mode='context_only',positive_retrieval_eligible=False,native_approval=False,runtime_registration='NOT_APPLIED');context.append(r)
 cards=[]
 for r in read_tsv('cards.tsv'):
  r['term_keys']=r['term_keys'].split(';');r['suggested_slots']=r.pop('slots').split(',');r['source_ids']=r['source_ids'].split(',')
  if r['id']=='W17': r['suggested_slots']=['object_structure','wardrobe_layering']
  if r['id']=='V05': r['suggested_slots']=['body_pose','contact_point']
  if r['id'] in ['W03','W04','W16','W17','W18']: r['source_ids']=['S00']
  r['source_ids']=list(dict.fromkeys(['S00']+r['source_ids']))
  triples=[]
  for triple in r['relations'].split(';'):
   a,b,c=triple.split('>');triples.append({'from':a,'relation':b,'to':c})
  r['relations']=triples;r['owner_nodes']=sorted({n for t in triples for n in [t['from'],t['to']]})
  r.update(provenance='agent_authored_research_option',source_support_scope='Bounded definitions and limits in sources.json only; geometry is an authored alternative, not a sourced universal definition.',native_approval=False,automatic_hard_activation=False,runtime_registration='NOT_APPLIED',native_qualification='NOT_RUN',retrieval_status='NOT_RUN',pixel_status='NOT_RUN',graph_scope='advisory review metadata, not native facts or owner/effect permission',medium='explicit teaching diagram' if r['mode']=='diagram_only' else 'photographic scene proposal')
  cards.append(r)
 table_rows=[]
 for ti,table in enumerate(json.loads((HERE/'reference-first13-tables.json').read_text()),1):
  for ri,row in enumerate(table[1:],1): table_rows.append({'id':f'T{ti:02}-R{ri:02}','table':ti,'row':ri,'term':row[0],'meaning_ko':row[1],'meaning_provenance':'verbatim_tool_table; source is not independent authority'})
 counters=collections.Counter()
 for r in read_tsv('keyword-supplement.tsv'):
  ti=int(r['table']); counters[ti]+=1;table_rows.append({'id':f'T{ti:02}-R{counters[ti]:02}' if ti else 'P01','table':ti,'row':counters[ti],'term':r['term'],'meaning_ko':r['meaning_ko'],'meaning_provenance':'agent paraphrase of complete Chrome-rendered reference; term label transcribed'})
 routes=[]
 for r in table_rows:
  term=r['term'];ko=term.split(' — ')[0]
  vs=[c['id'] for c in cards if any(k.lower() in term.lower() for k in c['term_keys'])]
  cs=[c['id'] for c in context if any(k.lower() in term.lower() for k in c['term_keys'])]
  if not cs:cs=[DEFAULT_CONTEXT[r['table']]]
  routes.append({**r,'section':SECTIONS[r['table']-1] if r['table'] else '본문 추가 용어','row_kind':'confusion' if r['table']==23 else 'authored_scene_example' if r['table']==24 else 'keyword','original_source_ids':['S00'],'independent_full_lexical_verification':'NOT_CLAIMED','optional_or_adjacent_visual_cards':vs,'context_cards':cs,'route_scope':'advisory, not synonym, exhaustive definition, automatic activation or proof','next_step':'Whole-source reuse/meaning review before adding a new realization' if vs else 'Retain context; select a justified existing source or author a separate visible realization only when requested'})
 for c in cards+context: c['source_keyword_ids']=[r['id'] for r in routes if c['id'] in r['optional_or_adjacent_visual_cards']+r['context_cards']]
 write('keyword-routes.json',routes);write('semantic-cards.json',{'visual_cards':cards,'context_cards':context})
 drafts=[]
 for c in cards:
  drafts.append({'draft_id':'DRAFT-'+c['id'],'source_card_id':c['id'],'positive_en':c['positive_en'],'positive_ko':c['positive_ko'],'suggested_slots':c['suggested_slots'],'status':'HOLD_FOR_REFERENCES' if c['mode']=='defer_visual' else 'SEPARATE_DIAGRAM_PATH' if c['mode']=='diagram_only' else 'DRAFT_REQUIRES_WHOLE_SOURCE_REVIEW','required_review':{'owners_and_connections':c['relations'],'observable_gate':c['observable_gate'],'source_claim_limit':c['claim_limit'],'effects':'Derive every actual person/object/pose/garment/setting/text/representation mutation from the whole chosen proposition; slot name grants no permission.','conditions':'Establish actual requester-grounded owners, materials, age/medium/context as applicable and every intrinsic/binding guard; diagram is never still-photo evidence.','deduplication':'Compare entire bilingual source and realized alternatives with manifest-owned corpus before assigning CID.','unobservable_policy':'UNOBSERVABLE_NOT_PASS','partial_policy':'partial_is_fail'},'candidate_id':None,'native_approval':False,'runtime_registration':'NOT_APPLIED'})
 write('candidate-drafts.json',drafts)
 snap=json.loads((HERE/'corpus-snapshot.json').read_text()); details=json.loads((HERE/'corpus-hit-details.json').read_text()); decisions=[]
 for cid,(action,cardids,reason) in DECISIONS.items():
  original=details[cid]; decisions.append({'cid':cid,'proposed_decision':action,'draft_card_ids':cardids.split(',') if cardids else [],'reason_ko':reason,'source_snapshot':original,'source_sha256':sha(json.dumps(original['record'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),'comparison_status':'whole bilingual content, contract, guards, effects and bindings reviewed; native status not revalidated','runtime_change':'NOT_APPLIED'})
 write('existing-source-decisions.json',decisions)
 dev=[]
 for c in cards:
  if c['mode'] in ['defer_visual','diagram_only']:continue
  for lang in ['ko','en']: dev.append({'id':f'DEV-{c["id"]}-{lang}','language':lang,'request':c['positive_'+lang],'expected_review_cards':[c['id']],'fixture_kind':'card_wording_exposed_development_only','independent_holdout':False,'status':'NOT_RUN'})
 bounds=read_tsv('boundary-cases.tsv');write('boundary-cases.json',bounds)
 for b in bounds:
  for lang in ['ko','en']:
   for polarity,key in [('positive','positive_'),('contrast','contrast_')]:dev.append({'id':f'{b["id"]}-{polarity}-{lang}','language':lang,'request':b[key+lang],'expected_boundary':b['expected_boundary'],'related_cards':b['card_ids'].split(','),'fixture_kind':'authored_contrast_development_only','independent_holdout':False,'status':'NOT_RUN'})
 write('development-cases.json',dev)
 capture={'conversation_id':'6adc076c-0c60-83e8-a9a3-369c26c3ea65','title':'수사물 용어 정리','tool_message_chars':20000,'tool_truncated':True,'tool_has_older_turns':False,'chrome_url':'https://chatgpt.com/c/6adc076c-0c60-83e8-a9a3-369c26c3ea65','chrome_rendered_region_chars':30689,'main_sections_seen':17,'table_count':24,'table_rows_including_headers':[21,9,16,17,9,23,5,19,15,15,15,12,18,19,19,17,21,11,16,13,13,19,11,9],'keyword_table_rows':320,'prose_additional_keyword':'CSI 효과 — CSI effect','confusion_rows':10,'scene_examples':8,'visible_citation_links':25,'last_section_verified':'17. 창작·이미지 설정으로 묶는 조합 예시','last_content_verified':'인물의 역할 → 조사 중인 행동 → 의상·장비 → 장소 → 조명 → 사건을 암시하는 작은 흔적','preservation_scope':'First 13 tables and truncated tool JSON retained verbatim; remaining term labels transcribed, meanings summarized. Complete browser body reviewed but not archived byte-for-byte. Collapsed +N citation menus were not expanded; original citations were independently researched as listed in sources.json.'}
 write('reference-capture.json',capture)
 lines=['# 수사물 전체 키워드 지도','','표 1–22의 용어 320개 + 본문 CSI 효과 1개, 혼동 10개, 창작 조합 8개. 표제 전사와 설명 요약의 출처 상태를 JSON에 구분했다. 모든 항목의 독립 사전 검증 완료를 뜻하지 않는다. 카드는 선택적·인접 대안이지 동의어나 자동 활성화 규칙이 아니다.','']
 for ti in list(range(1,25))+[0]:
  rows=[r for r in routes if r['table']==ti];lines+=['## '+(SECTIONS[ti-1] if ti else '본문 추가 용어'),'','|ID|원 용어|원문 보존/요약 의미|선택 대안|문맥 경계|','|---|---|---|---|---|']
  for r in rows:lines.append('|'+ '|'.join([r['id'],r['term'],r['meaning_ko'].replace('|','/'),', '.join(r['optional_or_adjacent_visual_cards']) or '별도 정의·형태 확인',', '.join(r['context_cards'])])+'|')
  lines.append('')
 (HERE/'KEYWORD-ATLAS.md').write_text('\n'.join(lines)+'\n')
 lines=['# 시각 대안과 문맥 경계','','정지사진에 보이는 명제, 서사적 proxy, 다이어그램, 근거 보류를 구분한다. 아래 기하는 연구자가 저작한 대안이며 출처는 각 문서의 제한된 정의·경계만 지원한다. 실제 native facts/effects가 아니다.','']
 for c in cards:
  lines += [f'## {c["id"]} {c["label_ko"]}', '',f'**상태:** {c["mode"]} / 제안 슬롯: {", ".join(c["suggested_slots"])}', '',c['positive_ko'],'',c['positive_en'],'',f'**가시 판정:** {c["observable_gate"]}', '',f'**추론 한계:** {c["claim_limit"]}', '',f'**관계:** '+ '; '.join(f'{t["from"]} → {t["relation"]} → {t["to"]}' for t in c['relations']), '', '**출처:** '+', '.join('['+sid+']('+next(s['url'] for s in sources if s['id']==sid)+')' for sid in c['source_ids']), '']
 for c in context:lines += [f'## {c["id"]} {c["label_ko"]}','',c['meaning_boundary'],'',c['integration_action'],'','원 용어: '+ '; '.join(c['term_keys']), '']
 (HERE/'VISUAL-CARDS.md').write_text('\n'.join(lines)+'\n')
 lines=['# 출처와 주장 한계','','확인일 2026-10-25 KST. 본문·검색 발췌·서지 기록의 접근 수준을 구분했다. 링크가 있다는 사실은 용어 전체·형태·법적 효력·실제 이미지의 검증이 아니다.','']
 for s in sources:lines += [f'## {s["id"]} [{s["title"]}]({s["url"]})','',s['supported_claim'],'','한계: '+s['claim_limit'],'','접근 수준: '+s['access_level'],'']
 (HERE/'SOURCES.md').write_text('\n'.join(lines)+'\n')
 summary={'source_keyword_rows':sum(r['row_kind']=='keyword' for r in routes),'confusion_rows':10,'scene_examples':8,'visual_cards':len(cards),'visual_mode_counts':dict(collections.Counter(c['mode'] for c in cards)),'context_cards':len(context),'drafts':len(drafts),'externally_researched_sources':len(SOURCES),'existing_source_decisions':len(decisions),'development_requests':len(dev),'contrast_pairs':len(bounds),'native_qualification':'NOT_RUN','retrieval_evaluation':'NOT_RUN','pixel_evaluation':'NOT_RUN','runtime_source_changes':'NOT_APPLIED','commit_push':'NOT_RUN'}
 write('BUILD-SUMMARY.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
