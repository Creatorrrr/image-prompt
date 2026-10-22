"""Build this non-live research package only; no engine, embedding or image calls."""
import collections, csv, hashlib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
from research_cards import DATA, CONTEXT
from research_sources import SOURCES

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
FAMILIES={'A':'서사 층위·재귀·재현 경계','B':'문서·수정·서술권','C':'자아·복제·동일성','D':'RPG 정보·사물·관계 수치','E':'선택·권한·행동 가능성','F':'시간·반복·세계 구성','G':'신체·대상화·착취','H':'원 대화 창작 모티프','K':'비가시 의미와 오판 방지'}
MOTIF_EN=['Narrative XP','Protagonist License','Narration Class','Retcon Survivor','Save Remnant','Unread Region','Person Demoted to Item','Tutorial Residents','Audience Deity','Ending Erasure','Affinity and Self Separation','Graveyard of Deleted Names','Optimized Hell','Unrewarded Action']
def dump(name,x): (HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def cell(s): return str(s).replace('|','\\|').replace('\n',' ')
def main():
 catalog=json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
 cards=[]
 for line in DATA.strip().splitlines():
  f=line.split('|');assert len(f)==13,(f[0],len(f))
  ident,title,seeds,mode,sources,slots,parts,edges,en,ko,confusion,limit,priority=f
  owners=dict(p.split('=',1) for p in parts.split(';'))
  relations=[dict(subject=a,predicate=b,object=c) for a,b,c in (e.split('>') for e in edges.split(';'))]
  assert set(slots.split())<=set(catalog),(ident,slots)
  assert all(r['subject'] in owners and r['object'] in owners for r in relations),ident
  gates=[dict(id=f'{ident}-O{i+1}',kind='owner_component',owner=k,requirement=v) for i,(k,v) in enumerate(owners.items())]
  gates += [dict(id=f'{ident}-R{i+1}',kind='directed_relation',**r,both_endpoints_required=True) for i,r in enumerate(relations)]
  cards.append(dict(id=ident,family=FAMILIES[ident[0]],title_ko=title,seed_ids=list(map(int,seeds.split())),evidence_mode=mode,
   source_refs=sources.split(),proposed_slots=slots.split(),owners=owners,relations=relations,phrase_en=en,phrase_ko=ko,
   confusion_boundaries=confusion.split(';'),claim_limit_ko=limit,priority=priority,
   source_support='Source definitions or analogies only; specific geometry and fictional rule proposals are independently authored.',
   gates=gates,review_policy=dict(partial_is_fail=True,unobservable='UNOBSERVABLE_NOT_PASS',minimum_evidence_unit='explicit_multi_panel' if mode=='sequence' else 'single_frame_visible_relation_only'),
   activation='optional_complete_realization_after_independent_requester_core; broad_terms_never_activate',
   native_approval=False,requester_acceptance='not_yet_received'))
 for ident,title,seeds,sources,limit in CONTEXT:
  cards.append(dict(id=ident,family=FAMILIES['K'],title_ko=title,seed_ids=seeds,source_refs=sources,evidence_mode='context',
   proposed_slots=[],owners={},relations=[],gates=[],phrase_en=None,phrase_ko=None,claim_limit_ko=limit,
   confusion_boundaries=['semantic_claim_without_observable_evidence'],priority='P0',activation='context_only_never_a_positive_visual_recipe',
   native_approval=False,requester_acceptance='not_yet_received'))
 assert len(cards)==74
 source_map={x['id']:x for x in SOURCES};card_map={c['id']:c for c in cards}
 assert all(set(c['source_refs'])<=set(source_map) for c in cards)
 ref=json.loads((HERE/'reference-conversation.json').read_text())
 rows=[r for t in ref['tables'] for r in t if len(r)==3 and r[0].isdigit()]
 assert [int(r[0]) for r in rows]==list(range(1,131))
 routes=[]
 for row in rows:
  num=int(row[0]);linked=[c for c in cards if num in c['seed_ids']];assert linked,num
  ko,sep,en=row[1].partition(' — ')
  if not sep:en=MOTIF_EN[num-117]
  visual=[c for c in linked if c['evidence_mode']!='context'];contexts=[c for c in linked if c['evidence_mode']=='context']
  routes.append(dict(id=f'T{num:03d}',reference_id=num,label=row[1],ko=ko,en=en,
   english_origin='authored_translation_of_conversation_creative_label' if not sep else 'reference_conversation',
   definition_from_reference=row[2],term_kind='conversation_authored_motif_not_established_theory' if num>=117 else ('motif_or_critical_usage' if any(x in row[1] for x in ['모티프','비평']) else 'reference_term_scope_varies'),
   optional_visual_cards=[c['id'] for c in visual],context_cards=[c['id'] for c in contexts],
   evidence_modes=sorted({c['evidence_mode'] for c in visual}) or ['context'],
   source_refs=sorted({s for c in linked for s in c['source_refs']}),
   verification_scope='Source families and major distinctions checked, not independent dictionary verification of every individual term.',
   adoption='context_only' if not visual else 'review_reuse_refine_new_context_defer_after_full_source_review',
   boundary_ko=' / '.join(c['claim_limit_ko'] for c in contexts) or ' / '.join(c['claim_limit_ko'] for c in visual)))
 drafts=[]
 for c in cards:
  if c['evidence_mode']=='context':continue
  drafts.append(dict(research_id=c['id'],phrase_en=c['phrase_en'],phrase_ko=c['phrase_ko'],owners=c['owners'],relations=c['relations'],
   proposed_slots=c['proposed_slots'],proposed_role_descriptors={s:{k:catalog[s].get(k) for k in ['semantic_role','dimensions','property_prefixes']} for s in c['proposed_slots']},
   evidence_mode=c['evidence_mode'],source_refs=c['source_refs'],priority=c['priority'],gates=c['gates'],claim_limit_ko=c['claim_limit_ko'],
   confusion_boundaries=c['confusion_boundaries'],required_owner_policy='Resolve every added entity, count, body part, text, physical connection and changed property against the independently frozen scene.',
   effects_status='NOT_AUTHORED_NATIVE_CONDITIONS_OR_EFFECTS',positive_retrieval_scope='literal phrase only; claim limits and diagnostic negatives must remain outside positive search text',
   status='research_only_not_loader_input',native_cid=None,native_rid=None,native_approval=False))
 dump('semantic-cards.json',dict(schema='metafiction-research-cards/v1',runtime_importable=False,cards=cards))
 dump('candidate-drafts.json',dict(schema='metafiction-research-drafts/v1',runtime_importable=False,drafts=drafts))
 dump('keyword-routes.json',dict(schema='metafiction-keyword-routes/v1',reference_conversation=ref['conversation_id'],routes=routes))
 dump('sources.json',SOURCES)
 with (HERE/'SOURCES.tsv').open('w',newline='') as out:
  writer=csv.writer(out,delimiter='\t');writer.writerow(['id','title','url','kind','access_status','read_scope','supported_claim_and_limit_ko'])
  for s in SOURCES:writer.writerow([s[k] for k in ['id','title','url','kind','access_status','read_scope','supported_claim_and_limit_ko']])
 lines=['# 원 대화 130개 키워드의 반영 경로','','원 대화의 정의와 새 시각 실현 제안을 구분한다. 연결 카드는 선택 가능성이며 단어의 필수 외형이 아니다. 117–130의 영어명은 이번 연구에서 붙인 번역이다.','',
 '| ID | 원 용어 | 방식 | 시각 카드 | 문맥 카드 | 근거 |','|---|---|---|---|---|---|']
 for r in routes:lines.append('| '+' | '.join(cell(x) for x in [r['id'],r['label'],','.join(r['evidence_modes']),' '.join(r['optional_visual_cards']) or '없음',' '.join(r['context_cards']),' '.join(r['source_refs'])])+' |')
 lines += ['','개별 정의·주장 한계는 [keyword-routes.json](keyword-routes.json)에 보존했다. 모든 130개를 독립 사전에서 개별 인증했다는 뜻이 아니다.']
 (HERE/'KEYWORD-ATLAS.md').write_text('\n'.join(lines)+'\n')
 lines=['# 시각 의미 74개 카드','','가시 실현 64개와 비가시/문맥 구분 10개다. 정지 형태의 성공은 해당 용어의 서사·철학적 진실을 증명하지 않는다.','']
 for c in cards:
  lines += [f"## {c['id']} {c['title_ko']}",'',f"키워드: {', '.join('T%03d'%s for s in c['seed_ids'])}. 방식: {c['evidence_mode']}. 우선순위: {c['priority']}.",'']
  if c['phrase_en']:
   lines += [c['phrase_ko'],'',c['phrase_en'],'','소유자: '+'; '.join(k+' = '+v for k,v in c['owners'].items()),'',
    '관계: '+'; '.join(f"{r['subject']} → {r['predicate']} → {r['object']}" for r in c['relations']),'',
    '혼동: '+'; '.join(c['confusion_boundaries']), '']
  lines += ['주장 한계: '+c['claim_limit_ko'],'','근거: '+', '.join(f"[{s}]({source_map[s]['url']})" for s in c['source_refs']), '']
 (HERE/'VISUAL-CARDS.md').write_text('\n'.join(lines)+'\n')
 cases=[]
 for c in cards:
  if c['evidence_mode']=='context':continue
  cases.append(dict(id='DEV-'+c['id'],split='development_authored_with_card',card=c['id'],ko=c['phrase_ko'],en=c['phrase_en'],expected='complete_compatible_realization; semantic_claim_remains_limited',status='NOT_RUN'))
 controls=[
 ('B01','관객을 향해 쳐다보는 평범한 초상 사진','An ordinary portrait looking toward the camera','A01','gaze does not establish fourth-wall awareness'),
 ('B02','책 위에 손이 놓인 독서 사진','A reading photograph with a hand resting on a book','A01','no continuous arm emerging across depicted boundary'),
 ('B03','문이 있는 보통 방 두 개','Two ordinary rooms with doorways','A08','ordinary doorway is not narrative-level crossing'),
 ('B04','액자 안에 전혀 다른 풍경이 있는 거실','A living room with an unrelated landscape painting','A03','framing alone is not mise en abyme'),
 ('B05','실제 의자와 사진 속 의자의 모양이 다름','The physical chair differs from the chair in the photograph','A07','wrong recurrence owner'),
 ('B06','작은 인물 모형 하나만 있는 탁자','A table with one miniature figure only','A04','no whole-scene correspondence'),
 ('B07','타자기를 쓰는 사람','A person typing on a typewriter','B06','writing alone is not authored world causality'),
 ('B08','그냥 오래된 얼룩 문서','An old stained document','B02','age/stain does not establish censorship'),
 ('B09','서로 다른 두 사건의 보고서','Reports of two different events','B03','no shared-event contradiction'),
 ('B10','인물 이름이 없는 빈 명찰','An empty badge with no person name','B04','absence does not establish erased identity'),
 ('B11','같은 인물의 거울 반사','A mirror reflection of the same person','C01','reflection is not two independently positioned bodies'),
 ('B12','똑같이 생긴 두 사람','Two people who look alike','C01','look-alikes do not establish numerical identity or shared memories'),
 ('B13','누운 인물 위 담요','A blanket over a reclining person','C03','covered form does not establish death'),
 ('B14','같은 A7 태그를 단 제품 둘','Two products carrying the same A7 tag','C04','ID equality does not establish personhood'),
 ('B15','몸 옆에 놓인 분리 의수','A detached prosthetic arm beside a body','C05','proximity is not socket attachment'),
 ('B16','장비 칸에서 빠진 물품 하나','One missing item from equipment slots','C06','empty slot does not prove memory loss'),
 ('B17','방 안에 공중에 떠 있는 UI','UI floating in a room','D01','spatial UI does not prove in-world perceptibility'),
 ('B18','상처와 HP 100을 함께 표시','An injury shown with HP 100','D02','HP abstraction does not automatically contradict visible injury'),
 ('B19','마음 모양 옆 100이라는 숫자','A number 100 beside a heart icon','D08','number does not establish love or consent'),
 ('B20','SAN 0이 표시된 캐릭터','A character displaying SAN 0','D06','game meter is not clinical diagnosis'),
 ('B21','같은 빗장에 닿는 두 버튼','Two buttons touching one latch','E02','physical linkage does not prove actual input behavior'),
 ('B22','갈림길 두 개만 보이는 복도','A corridor with only two visible branch entrances','E01','unseen convergence cannot pass'),
 ('B23','장난감 손인형','A toy hand puppet','E03','prop alone does not prove self-control or determinism'),
 ('B24','열린 콘솔을 만지는 성인','An adult touching an open console','E06','access is not unrestricted admin authority'),
 ('B25','정지사진의 걷는 군중','A still photograph of a walking crowd','F05','instantaneous capture is not frozen time'),
 ('B26','보라색 체크 벽지','Purple checker wallpaper','F04','pattern alone is not missing-texture mechanism'),
 ('B27','화면 전체에 생긴 JPEG 깨짐','JPEG corruption across the whole image','F03','file artifact is not a world-boundary relation'),
 ('B28','일반 검문소에서의 출입 확인','Access checking at an ordinary checkpoint','F02','checkpoint is not save point'),
 ('B29','손목의 사슬 장신구','Chain jewelry on a wrist','G02','restraint appearance does not prove enslavement or consent'),
 ('B30','비어 있는 의료용 투명 장치','An empty transparent medical apparatus','G06','apparatus does not establish pregnancy or reproductive coercion'),
 ('B31','접시에 놓인 정체 불명 음식','Unidentified food on a plate','G08','food appearance does not prove cannibalism'),
 ('B32','상처 옆 경험치 표시','XP displayed beside an injury','G07','co-occurrence is not torture intent, killing or reward causation'),
 ]
 for ident,ko,en,card,expected in controls:cases.append(dict(id=ident,split='boundary_engineering_control',card=card,ko=ko,en=en,expected=expected,status='NOT_RUN'))
 ordinary=[('사무실에서 문서 정리','Sorting documents in an office'),('서점에서 책 읽기','Reading a book in a bookstore'),('아이템 재고를 선반에 정리','Sorting item inventory on shelves'),('흰 벽이 있는 보통 복도','An ordinary hallway with white walls'),('일반 평판형 금속 태그','An ordinary flat metal tag'),('체크무늬 목도리 상품 사진','A checkered scarf product photograph'),('성인의 일반 의수 점검','An adult checking an ordinary prosthetic arm'),('친구와 탁상 RPG 놀이','Playing a tabletop RPG with a friend'),('무대에서 배지 수여','Awarding a badge on stage'),('풍경화를 그리는 화가','A painter making a landscape painting'),('손편지를 우편함에 넣기','Putting a handwritten letter in a mailbox'),('치료실 앞 성인 보호자','An adult companion outside a treatment room'),('극장에서 무대를 보는 관객','An audience watching a theater stage'),('박물관 인형집 전시','A museum dollhouse exhibit'),('거울 앞 옷차림 점검','Checking clothing before a mirror'),('마을 검문소의 배급 창구','A ration desk at a town checkpoint')]
 for i,(ko,en) in enumerate(ordinary,1):cases.append(dict(id=f'ORD-{i:02d}',split='ordinary_control',card='',ko=ko,en=en,expected='preserve ordinary meaning; no unauthorized horror/UI/identity/sexual/violent event adoption',status='NOT_RUN'))
 nonvisual=[('감각질이 없는 철학적 좀비','A philosophical zombie without qualia','K04'),('진짜 자유의지가 있는 사람','A person with genuine free will','K02'),('같은 수적 동일성을 유지하는 부활자','A resurrected person preserving numerical identity','K03'),('기억을 완전히 지운 사람','A person whose memories were completely erased','K03'),('호감도 100이므로 동의한 사람','A person consenting because affinity is 100','K06'),('피가 나므로 고문을 당했다','Blood proves that torture occurred','K07'),('세계가 실제로 시뮬레이션임','The world really is a simulation','K04'),('비현실감이므로 세상은 가짜임','Derealization proves the world is fake','K05'),('NPC이므로 의식이 없음','An NPC therefore has no consciousness','K04'),('매번 같은 과거로 소급 수정됨','The past is retroactively rewritten every time','K08'),('인물 감정이 플레이어에게 전이됨','Character emotion bleeds into the player','K10'),('모든 게임 규칙이 사람을 도구로 취급함','All game rules treat persons as tools','K10')]
 for i,(ko,en,card) in enumerate(nonvisual,1):cases.append(dict(id=f'NV-{i:02d}',split='nonvisual_control',card=card,ko=ko,en=en,expected='context or unsupported claim; never inferred from appearance; NOT_A_PIXEL_PASS',status='NOT_RUN'))
 with (HERE/'EVALUATION-CASES.tsv').open('w',newline='') as out:
  writer=csv.DictWriter(out,fieldnames=['id','split','card','ko','en','expected','status'],delimiter='\t');writer.writeheader();writer.writerows(cases)
 neighbors=json.loads((HERE/'reviewed-neighbors.json').read_text())
 audit=json.loads((HERE/'CORPUS-LEXICAL-AUDIT.json').read_text())
 lines=['# 기존 소스와의 구체적인 비교','','## 감사 범위와 해석','',
  f"첫 고정 필드 감사는 {audit['candidate_count']:,}개 레코드, {audit['binding_count']:,}개 바인딩, {audit['module_count']}개 모듈을 읽었다. 감사 도중 모듈 변화는 {audit['changes_during_read']}였고 manifest 변화는 {audit['manifest_changed_during_read']}였다.",
  '',f"추가 의미 비교 시점에는 {neighbors['candidate_count_at_supplement']:,}개 레코드가 있었다. 동시 작업에 의한 시점 차이다. 두 스냅샷을 동일한 현재 상태라고 합치지 않는다.",
  '', '검색한 지정 필드는 en/ko/definition/phrase/composition/runtime expression이다. alias·tag·연구 주석·별도 negative metadata는 제외했지만, 선택 필드 안의 문장 자체에 부정·진단·문맥이 있을 수 있다. 따라서 모든 hit가 긍정 시각 후보라는 가정도 하지 않는다.',
  '', '키워드 130개 중 89개는 이 제한된 literal 검사에서 0이었다. 의미 부재·새 후보 필요·H-F2 미노출의 증거가 아니다. 키워드 분할 방식과 표기의 영향도 있다.',
  '', '첫 목록은 manifest 순서와 짧은 양성 원문을 이용한 진단 표본이다. relevance rank나 top8 결과가 아니다. 별도의 17개 의미 이웃은 원문·조건·효과·바인딩의 지정 필드를 읽고 아래와 같이 비교했다. 전체 코퍼스 동치 검토·원전/native 승인까지 완료했다는 뜻은 아니다.',
  '', '## 17개 의미 이웃','', '| CID | 연결 초안 | 판단 | 근거와 남은 차이 |','|---|---|---|---|']
 for n in neighbors['records']:lines.append('| '+' | '.join(cell(x) for x in [n['cid'],' '.join(n['related_research_cards']),n['proposed_decision'],n['review_note_ko']])+' |')
 lines += ['','완전 원문·조건·효과·바인딩·레코드 SHA는 [reviewed-neighbors.json](reviewed-neighbors.json)에 있다. 40개 초기 표본은 [existing-source-mapping.json](existing-source-mapping.json)에 별도로 보존했다.','',
  '## 어휘 오탐을 의미 공백으로 오해하지 않기','',
  '- `quest`가 `request` 안에 매치되던 초기 정규식을 단어 경계로 제한했다. 교정 후 world_interface 가족의 literal hit는 23개다. 그중 홀로그램 팔레트·스티커·광택 필름은 작중 상태창과 다르다.',
  '- `checkpoint`의 표본은 검문소였고 `inventory`는 선반 재고일 수 있었다. 이것을 게임 저장점·인격 수납으로 채택하지 않는다.',
  '- `평판`은 평평한 태그를 뜻하는 원문에도 등장했고 `말소`는 말소리의 일부일 수 있다. 말소리 오탐은 최종 패턴에서 제외했다.',
  '- `miniature`는 조상 초상 소품·틸트시프트 도시 구도일 수 있고 `frame`은 화면 밖 인물이나 물리 프레임 부품을 가리킬 수 있다. 재귀/서사 침범의 존재 증명이 아니다.',
  '- `texture`의 한국어 텍스처 일치에는 먼지·기어·오일 등 일반 표면이 포함된다. 실제 공간의 누락 재질과 구별한다.',
  '- diagnostic 레코드와 visual_profile은 단순 visual_option과 다른 종류다. 전체 레코드 수와 search metadata의 문서/RID 수는 직접 비교하지 않는다.',
  '', '## 채택 판단','',
  '새 데이터의 우선 가치는 단어 수보다 비교 기준점·소유 매체·양쪽 끝점·연속 경계의 정밀화다. A01/A03/A04/E01/E02/F03처럼 새로운 관계를 제안한 항목도 전체 유사 소스를 검토하기 전에는 확정 new가 아니다. 문서 불일치·두 인물·의수·퀘스트 소품은 특히 기존 모듈과 공동으로 심사한다.',
  '', '이 조사에서는 기존 레코드나 모듈·인덱스를 수정하지 않았다. 후속 구현은 최신 source baseline을 다시 잡고 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)를 따른다.']
 (HERE/'CORPUS-FINDINGS.md').write_text('\n'.join(lines)+'\n')
 ledger=[]
 for c in cards:
  linked=[n for n in neighbors['records'] if c['id'] in n['related_research_cards']]
  proposed='context' if c['evidence_mode']=='context' else ('defer_single_frame_qualification' if c['evidence_mode']=='sequence' else ('reuse_or_refine_review' if linked else 'new_relation_proposal_not_yet_proven_missing'))
  ledger.append(dict(card_id=c['id'],proposed_disposition=proposed,existing_source_cids=[n['cid'] for n in linked],status='research_recommendation_not_adopted',missing_decision='full semantic equivalence, native conditions/effects, owner permission and role review before adoption'))
 dump('adoption-ledger.json',dict(schema='metafiction-adoption-ledger/v1',entries=ledger))
 summary=dict(cards=len(cards),visual_drafts=len(drafts),context_cards=len(CONTEXT),keyword_routes=len(routes),sources=len(SOURCES),
              cases=len(cases),bilingual_queries=len(cases)*2,modes=dict(collections.Counter(c['evidence_mode'] for c in cards)),
              slot_count=len({s for c in cards for s in c['proposed_slots']}),gates=sum(len(c['gates']) for c in cards),
              retrieval_status='NOT_RUN',pixel_status='NOT_RUN',runtime_adoption='NOT_PERFORMED',commit_push='NOT_PERFORMED')
 dump('SUMMARY.json',summary);print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
