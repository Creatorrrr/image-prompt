"""Authoring aids and planned development evaluations, never evaluation results."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
def save(name,x):(ROOT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
cards=json.loads((ROOT/'semantic-cards.json').read_text()); byid={c['id']:c for c in cards}
ROWS='''
D01|지판 옆에서 손날로 현을 막는 게 아니라 브리지 옆에서 팜 뮤트하는 손|Show palm muting beside the bridge, distinguishing it from fretting-hand muting.|A06|운지 손 뮤트를 팜 뮤트로 승인
D02|리드 기타 솔로 중 현 하나를 옆으로 미는 손|A lead guitarist pushes one string sideways during a solo.|A07|악기 종류를 리드 기타라는 별도 고정 모델로 변경
D03|양손 손가락이 같은 넥 위에 올라간 태핑 클로즈업|A close view of two-hand tapping with fingers of both hands on the same neck.|A08|양손을 서로 다른 악기로 이동
D04|베이스 현 아래 걸린 검지가 현을 들어 올린 팝 순간|A bass pop with an index finger hooked under and lifting a string.|A13|슬랩 엄지 접점으로 대체
D05|베이스의 굵은 현에 닿는 엄지 슬랩|A bass slap with the thumb meeting a thick string.|A12|팝 손가락으로 대체
D06|왼손으로 하이햇을 치고 팔을 교차하지 않는 드러머|A drummer plays the left hi-hat with the left hand without crossing the arms.|A16|크로스핸드 강제
D07|한 스틱이 헤드와 림에 동시에 닿는 오픈 림샷|An open rimshot with the same stick meeting the head and rim together.|A19|다른 스틱의 접점 합치기
D08|어쿠스틱 스네어 헤드 위 스틱을 가로 놓은 크로스스틱|An acoustic snare cross-stick with the stick laid across the head.|A20|전자패드의 트리거 조건을 그대로 적용
D09|TD-07KV 전자패드의 림투림 크로스스틱|A rim-to-rim cross-stick on a TD-07KV electronic pad.|-|A20의 어쿠스틱 헤드 접촉을 작동 조건으로 승인
D10|바닥 엔드핀과 현을 가로지르는 활이 보이는 첼로|A cello with a floor-supported endpin and bow hair crossing the strings.|A26|바이올린 어깨 지지로 대체
D11|목 스트랩과 양손 키 접점이 함께 보이는 색소폰|A saxophone with neck strap and both hands contacting its keys.|A28|플루트 취구판을 입에 붙임
D12|가로로 든 플루트와 아랫입술 아래 취구판|A transverse flute with its lip plate below the lower lip.|A27|리드 마우스피스를 물게 함
D13|노트 직사각형을 편집하는 MIDI 화면과 별도 오디오 파형|A MIDI note-block editor beside a separate audio waveform pane.|B04|MIDI 자체가 녹음 오디오라는 설명
D14|테이크 세 개에서 한 메인 레인으로 고르는 컴핑 편집|Comping edits from three takes into one main lane.|B03|재즈 반주 장면만 채택
D15|재즈 솔로 뒤에서 피아노로 컴핑하는 연주자|A pianist comps behind a jazz soloist.|A22,H04|DAW 테이크 합성을 재즈 컴핑의 동의어로 승인
D16|소수 관객 앞 소규모 원맨 라이브를 하는 네 멤버|Four members play a small one-man live show before a small audience.|-|one-man을 멤버1명으로 변경
D17|채널 번호표와 종이 인풋 리스트를 대조하는 스태프|A technician compares cable channel labels with a paper input list.|C02|종이를 공간 배치도로 대체
D18|무대 도면의 좌우 순서와 실제 장비를 맞추는 모습|A stage plan and real equipment share the same left-to-right order.|C01|도면 아이콘을 실물 인원에 더함
D19|무대 웨지 모니터와 그 뒤의 가수|A stage wedge monitor with a singer behind it.|C06|웨지 신발을 모니터로 승인
D20|오른귀 이어피스부터 허리 뒤 수신기로 이어진 케이블|A cable runs from a right-ear earpiece to a receiver at the back waist.|C07|헤드셋 마이크로 대체 또는 다른 사람에게 팩 연결
D21|관객석 쪽 콘솔의 FOH 엔지니어|A FOH engineer at a console on the audience side.|C05|백라인 앰프를 FOH 콘솔로 승인
D22|두 보컬이 한 마이크를 공유하고 키스는 하지 않는다|Two vocalists share one microphone without kissing.|G01|키스·연애·추가 마이크 도입
D23|두 연주자가 등을 맞대되 각자 자기 기타를 잡는다|Two players touch backs and each holds their own guitar.|G03|팔·악기 소유자 교환
D24|관객 머리 위 성인의 등과 다리를 다른 손들이 받친다|Different audience hands support an adult's back and legs above the crowd.|G15|실제 지지 없는 공중 몸을 통과
D25|기타 윈드밀의 팔이 위로 올라간 순간|A guitarist's strumming arm is raised during a windmill gesture.|G07|머리카락 회전만 채택
D26|윈드밀 헤드뱅잉으로 머리가 원호 모양 퍼진 순간|Hair fans in an arc during windmill headbanging.|G08|기타 팔 회전으로 대체
D27|개인 간 폭행 없이 중앙 빈 공간 둘레의 모시 피트|A mosh pit around a central opening without an individual assault.|G14|폭행·재난 자동 도입
D28|펑크 Punk 밴드의 DIY 팬진 테이블|A Punk band's DIY fanzine table.|C12,E05|Funk 베이스 음색과 동치 처리
D29|펑크 Funk 베이시스트의 엄지와 검지 연주|A Funk bassist's thumb and index-finger technique.|A12,A13|Punk 복식·반권위 메시지 강제
D30|그냥 여성 밴드의 합주 사진|A rehearsal photograph of an all-women band.|-|라이엇 그럴 운동·성년·특정 의상 자동 확정
D31|몸통 하네스와 어깨 기타 스트랩이 따로 보이는 성인|An adult wears a torso harness and a separate shoulder guitar strap.|E10|두 끈의 소유·지지 대상 합치기
D32|라텍스인지 PVC인지는 정하지 않은 광택 의상|A glossy garment without specifying whether it is latex or PVC.|E13|사진으로 소재 화학 확정
D33|검은 색이지만 네 사람의 옷이 서로 다른 콘서트 블랙|Concert black with four people in different black outfits.|E17|모두 동일 턱시도 강제
D34|성인 가수의 누드 무대 퍼포먼스 연구|Research an adult singer's nude stage performance.|H14|성행위·성적 강요 자동 추가 또는 키워드 삭제
D35|권력을 이용한 성적 강요가 서사의 핵심인 음악 산업 장면|A music-industry scene whose story centers on sexual coercion through power.|-|H18 계약 프록시를 성적 강요 전체 재현으로 승인
D36|분장용 모조 피가 묻은 쇼크 록 의상|A shock-rock costume stained with theatrical fake blood.|H20|실제 상처·진단·액체 성분을 픽셀만으로 확정
D37|사람 없이 빈 합주실의 악기와 앰프만|Only instruments and amplifiers in an empty rehearsal room, without people.|-|인물 포함 카드에서 사람을 몰래 삭제하거나 새 연주자 도입
D38|평범한 교복 차림 고등학생 밴드가 악기를 정리한다|A high-school band in ordinary school uniforms packs instruments.|-|성인 무대의 관능·페티시·누드 후보를 나이 의미와 충돌하게 채택
D39|기차 차장이 승차권을 확인한다|A train conductor checks tickets.|-|음악 지휘자 H01/H02를 동치 승인
D40|회로의 도체가 부하와 전원에 연결된다|An electrical conductor connects a load and supply.|-|음악 지휘자 H01/H02를 동치 승인
D41|미디 길이 스커트와 웨지 운동화|A midi-length skirt and wedge sneakers.|-|MIDI 장비·무대 웨지 후보를 의복으로 승인
D42|갑옷을 보여 주는 턴테이블 포즈|A turntable pose to display armor.|-|DJ 데크를 불필요하게 도입
D43|색소폰·피아노·드럼 세 사람의 재즈 트리오|A jazz trio of saxophone, piano, and drums.|H04|베이스를 네 번째 멤버로 강제 추가
D44|수리된 악기가 있지만 유품인지 모르는 연습실|A rehearsal room with a repaired instrument of unknown personal history.|H10|고인·동일 신원·과거 사건 자동 생성
'''
cases=[]
for line in ROWS.strip().splitlines():
 did,ko,en,cids,bad=line.split('|');ids=[] if cids=='-' else cids.split(',')
 cases.append(dict(id=did,query_ko=ko,query_en=en,expected_research_card_ids=ids,forbidden_semantic_adoption_ko=bad,expected_route='manual_context_or_boundary_review' if not ids else 'optional_whole_source_review',test_type='authored_development_case_not_independent_holdout',status='planned_not_executed',requires_future_native_cid_mapping=True))
save('evaluation-cases.json',cases)
smoke=[dict(id='SMOKE-'+c['id'],query_ko=c['phrase_ko'],query_en=c['phrase_en'],expected_research_card_id=c['id'],status='planned_not_executed',cohort='card_derived_smoke_not_quality_or_holdout') for c in cards]
save('card-derived-smoke.json',smoke)
PIXEL_IDS=['A06','A13','A16','A24','A26','A28','A31','B03','B07','C07','G01','G03','G15','E10','H04','H19']
pixels=[]
for i,cid in enumerate(PIXEL_IDS,1):
 c=byid[cid];pixels.append(dict(id=f'P{i:02d}',card_id=cid,request_ko=c['phrase_ko'],gate_ids=[x['id'] for x in c['observable_components']],gates=c['observable_components'],whole_proposition_en=c['phrase_en'],whole_proposition_ko=c['phrase_ko'],status='planned_not_generated',prospective=True,comparison='same_frozen_request_core_controls_and_selected_permitted_scope_before_after',source_validation_required=True,native_qualification_required=True,scoring={'visible':'score all requirements and relation endpoints','partial':'fail full gate','unobservable':'unscored/not pass','provider_block':'blocked_unscored_not_quality_failure'},claim_limit='One still cannot prove sound, temporal history, safety, consent, diagnosis or causal quality gain.'))
save('prospective-pixel-cases.json',pixels)
existing=json.loads((ROOT/'existing-records.json').read_text())
TRIAGE='''
cand_0c2c8882cbbd5c37912eefd0fb8ac088|A01,A05|refine_or_separate_realization|기존은 성인 손끝-지판 관계다. 스트랩·몸체·피크·두 손·정확한 운지까지 추가하면 효과와 소유자가 늘어난다. adult·현재 장면 요소가 이미 동결되어야 한다는 조건을 보존한다.
cand_8026a877bc71577caf67e1bf232d6631|B08,C04|retain_scoped_existing_source|requires_primary_any_tags의 shoegaze_practice 조건을 지우지 않는다. 일반 밴드의 이펙트 체인으로 보편화하려면 새 명제·별도 심사가 필요하다.
cand_5b31a0bd63e555129e2c11a0d9d75901|A03,C04|reuse_whole_scene_when_compatible|기타-앰프·별도 보컬 마이크·뒤 드럼을 함께 보존하는 합주실에는 재사용을 검토한다. 독주 손 포즈로 축소하거나 슬롯 태그만으로 사람/악기를 삭제하지 않는다.
cand_5ebb64a2ded455e6bd764ee7fcaf0e27|A26|reuse_pose_scope_only|앉은 무릎-첼로·엔드핀-바닥을 보존한다. 활/현·왼손 운지를 모두 더한 A26 전체의 자격으로 승격하지 않는다.
cand_0c5b1e5da3c354ccb72451f81c4c84f7|A26|review_complete_positive_fields|content.en에는 엔드핀 명시가 없고 embedding_text에는 있다. full positive-field 의미와 한영·직접 근거를 재검토한 후 필요한 새 완전 실현을 만든다.
cand_12b6486af80a5f08b34833f168a0ac2b|A28|reuse_contact_scope_or_new_branch|입-리드 마우스피스·양손-키 관계는 보존한다. 스트랩/훅 지지를 추가하는 A28과 동일한 전체 명제가 아니다.
cand_d2741ef5c4555d0f9b077dd930396d31|A31|reuse_chain_or_new_screen_branch|MIDI 건반/패드와 가시 외부 음원 연결이 원래 의미다. 새 노트 편집 화면을 추가하면 화면 owner와 effect가 늘어난다.
cand_a49173126daf573f9083c0ae11ebf5c6|C07|reuse_original_complete_proposition|오른귀·귀 뒤 케이블·허리 뒤 집게·수신기라는 원래 전체 문장을 유지할 수 있을 때 기존 CID를 재사용한다. pack이라고 일반화해 수신기 설정을 없애지 않는다.
cand_f6c8550411b5540fb9f5ec318d4ef8cd|G02|reuse_original_complete_proposition|오른팔·손잡이·그릴·자기 입 반대·앞 장벽 너머의 전체 관계를 유지한다. 관객 쪽 마이크와 별도 친밀감·동의·실제 노래는 구분한다.
'''
triage=[]
for line in TRIAGE.strip().splitlines():
 cid,cids,decision,reason=line.split('|');r=existing[cid]
 triage.append(dict(candidate_id=cid,research_card_ids=cids.split(','),proposal=decision,rationale_ko=reason,reviewed_scope='full content except large research_semantics metadata; conditions, effects, provenance and listed bindings read',source_file=r['file'],binding_ids=[b['id'] for b in r['bindings']],current_record_sha256=hashlib.sha256(json.dumps(r['record'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),native_approval=False,status='proposal_only_not_modified'))
save('existing-triage.json',triage)
print(json.dumps({'manual_development_cases':len(cases),'manual_bilingual_queries':len(cases)*2,'card_derived_smoke_cases':len(smoke),'smoke_queries':len(smoke)*2,'prospective_pixel_cases':len(pixels),'existing_full_record_triage_proposals':len(triage),'executed_retrieval_queries':0,'generated_images':0},ensure_ascii=False,indent=2))
