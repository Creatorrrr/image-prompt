from pathlib import Path
import json,hashlib,struct
O=Path(__file__).resolve().parent;R=O.parents[4]
cases=[
{'arm':'a','image':R/'generated/images/marine-literature-20261024-a/barracks-inspection-couture.png','tool_original':Path('/Users/chasoik/.codex/generated_images/01a1699e-9546-7783-8749-012ec8519cba/exec-7fec9052-1abf-4cbd-b364-531b17cd8e80.png'),'expected':'e2d2663790355a79d63722042a9cb70389e41d1b03dd6e5b7eec8936a6836c4d','testcase':'image-tests/a/testcase.precore.json','status':'PASS_FROZEN_OBSERVATION_GATES_ONLY','gates':[
('genre_military_context','PASS','베레모·각진 정복·견장·메달이 같은 인물에 함께 보인다. 빨강만으로 판정하지 않았다.'),
('genre_absurd_hierarchy','PASS','큰 장식의 정복을 입은 인물이 평범한 끈 군화를 벨벳 받침 위에서 엄숙하게 살핀다. 사람·군화·받침·검사 행동이 한 프레임에 연결된다.'),
('physical_inspection_relation','PASS','같은 인물의 장갑 낀 한 손이 받침 아래를 지지하고, 다른 검지가 군화 앞코 가죽 상단에 닿는다. 두 접점과 부츠 지지가 보인다. 해부학적 좌우는 지정한 손 역할과 반대다.'),
('reference_appearance','PASS','큰 얼굴과 어두운 턱선 길이 단발·가는 앞머리, 얼굴 비율이 참조와 시각 비교 가능한 크기로 보인다. 실존 정체성은 판정하지 않았다.'),
('fashion_presence','PASS','과장된 금장·정복 재단·편집 사진 조명과 집중한 얼굴이 함께 읽힌다.')], 'limit':'선택한 부조리 군복 패션 장면의 합격이다. 특정 한국 팬 설정·캐릭터·해병문학 전체의 고유성은 입증하지 않는다.'},
{'arm':'b','image':R/'generated/images/marine-literature-20261024-b/native-result.png','tool_original':Path('/Users/chasoik/.codex/generated_images/01a1699e-e241-78b1-bd17-255158f67f2d/exec-3a276e03-b822-4f3a-a770-0db24d4e4b74.png'),'expected':'8807860835e9c14aadb53d466eb9d26ab8be3ee40122bab76deb0b76ab5180f3','testcase':'image-tests/b/testcase.json','status':'FAIL_PARTIAL','gates':[
('B01','PASS','짧고 어두운 둥근 단발·분리된 앞머리와 부드러운 얼굴이 비교 가능한 크기로 보인다. 참조 사용의 도구 증거는 별도 transport 기록이다.'),
('B02','PASS','해안 도로·승합차·차체에 붙은 눌린 뒷바퀴·분리된 예비 바퀴가 함께 보인다.'),
('B03','UNOBSERVABLE_NOT_PASS','두 손의 깃대 그립은 연결되지만, 같은 깃발이 예비 바퀴를 덮는 투사 그늘은 추적할 수 없다. 검은 타이어 재질이나 전경 도로의 어두운 부분을 그 관계의 증거로 대체하지 않았다.'),
('B04','PASS','별도 인물이 관자 쪽으로 경례하고 고개와 몸을 낮은 예비 바퀴 쪽으로 향한다. 실제 지위·명령·의도는 판정하지 않았다.'),
('B05','PASS','군복·붉은 의전 깃발·고장 난 차량과 예비 바퀴를 향한 경례가 한 장면의 부조리한 의전으로 읽힌다.')], 'limit':'그늘 게이트 미충족으로 전체 FAIL. 실제 부대·국가 소속이나 특정 팬 판본은 이미지의 문양만으로 확정하지 않는다.'},
{'arm':'c','image':R/'generated/photo-runs/marine-literature-20261024-c/results/c-inspection.png','tool_original':Path('/Users/chasoik/.codex/generated_images/01a1699f-3200-7c80-9529-5bece03e2925/exec-dc5c3a07-66f8-442e-9872-3527e5148e4b.png'),'expected':'8221331f2767683c5090a24b9c3bea0bb906bcdcaf171eadbaa529d71e2cd81d','testcase':'image-tests/c/testcase.json','status':'FAIL_PARTIAL','gates':[
('c_genre','PASS','훈련복·베레모·침상·관물함·클립보드 검사 관계가 같은 생활관 복도에 공존한다. 가시적 단서와 장르 해석을 분리했다.'),
('c_absurd_space','UNOBSERVABLE_NOT_PASS','이어진 복도·얕은 물·고무보트·마른 검사대·앉은 검사자는 보인다. 보트의 하부/바닥 접촉은 프레임 밖 또는 불투명한 선체 뒤에 있어 접지를 확인할 수 없다. 떠 있다고 단정하지도 않았다.'),
('c_action_chain','PASS','한 손의 경례, 다른 손의 그립, 연속된 대걸레 자루·헤드와 부츠 옆 젖은 바닥 접점이 함께 보인다.'),
('c_reference','PASS','얼굴 비율·어두운 턱선 길이 단발·부드러운 앞머리를 비교할 수 있다. 실제 정체성이나 나이는 추론하지 않았다.'),
('c_scene_legibility','PASS','신병과 검사자의 방향, 클립보드·자와 침수 복도의 실내 보트 행정대가 연결된다. 소리·명령·강요·시간 경과는 판정하지 않았다.')], 'limit':'보트 접지 게이트 미충족으로 전체 FAIL. 물에 잠긴 공간과 검사 관계의 표현은 관찰되지만 숨은 지지를 통과시키지 않았다.'}
]
for c in cases:
 data=c['image'].read_bytes();h=hashlib.sha256(data).hexdigest();assert h==c['expected']==hashlib.sha256(c['tool_original'].read_bytes()).hexdigest();assert data[:8]==b'\x89PNG\r\n\x1a\n'
 c['sha256']=h;c['width'],c['height']=struct.unpack('>II',data[16:24]);c['image']=str(c['image']);c['tool_original']=str(c['tool_original']);c['testcase']=str(O.parent/c['testcase']);c['gates']=[{'id':i,'status':s,'observation':x} for i,s,x in c['gates']];c['passed_gates']=sum(g['status']=='PASS' for g in c['gates']);c['new_data_effect_status']='NO_NEW_SOURCE_TRANSFER';c['inspected']='Whole original PNG through view_image(detail=original); no altered pixels or composited preview.'
cases[0]['prompt_fidelity']='PARTIAL: global mirroring reverses authored support/inspection hand roles and boot-toe direction. Frozen five gates require owned contact/support endpoints, without anatomical side; their5/5 PASS is narrower than exact prompt fidelity.'
cases[0]['limit']+=' 좌우가 반전되어 원래 프롬프트의 손 역할과 군화 방향은 완전히 보존되지 않았다.'
out={'schema':'root-pixel-adjudication/v1','generation_calls_observed_from_agent_reports':3,'copies_exact_to_tool_originals':3,'frozen_gate_set_passes':1,'frozen_gate_set_partial_failures':2,'full_prompt_passes':0,'full_prompt_partial_failures':3,'blocked':0,'new_visual_source_adoption_arms':0,'new_source_pixel_qualification':'NOT_DEMONSTRATED','named_genre_specificity':'Not fully proven; rendered military-absurdist facets are separately observed.','user_acceptance':'NOT_OBSERVED','review_process':'Root viewed all original PNGs and compared frozen testcases. This is a second review, not claimed blinded; agent C had mentioned possible occluded grounding before root viewed C.','cases':cases}
out['full_prompt_pixel_qualification']='NOT_FULLY_PASSED: A has mirrored handedness/toe direction, B lacks observable flag shade on wheel, C lacks observable grounding.'
out['request_level_new_data_to_prompt_to_pixel_status']='FAIL_NOT_DEMONSTRATED'
(O/'root-pixel-review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['frozen_gate_set_passes','full_prompt_passes','new_source_pixel_qualification']}))
