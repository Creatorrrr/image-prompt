from pathlib import Path
import json,hashlib,datetime,collections
R=Path('/Users/chasoik/Projects/image-prompt');D=Path(__file__).resolve().parent;O=R/'generated/photo-runs/espionage-full-20261023-control';read=lambda p:json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def link(p,label):return f'[{label}]({p})'
cards=read(D/'semantic-cards.json');routes=read(D/'keyword-routes-full500.json');summ=read(O/'maintenance-union/retrieval-qualification.json')['summary']
A=R/'generated/photo-runs/espionage-full-20261023-a';B=R/'generated/photo-runs/espionage-full-20261023-b';C=R/'generated/photo-runs/espionage-full-20261023-c'
images=[A/'managed-v2/result.png',B/'results/ferry-passport-native.png',C/'results/contact-sheet-window.png']
originals=[Path(read(A/'arm-a-final.json')['invocation']['original_returned_path']),Path(read(B/'run_manifest.json')['image_paths'][0]),Path(read(C/'arm-report.json')['actual_generation']['original_image'])]
for a,b in zip(images,originals):assert hashlib.sha256(a.read_bytes()).hexdigest()==hashlib.sha256(b.read_bytes()).hexdigest()
# Human-readable full coverage and explicit distinction between original terms and narrower candidates.
sections=['장르','정보활동 기본 개념','인물·역할','커버·정체성','충성·침투·배신','포섭 동기','접촉·연락·이동','감시·도청','수집 방식','분석·판단','암호·사이버','보안·조직','기만·선전','조직·국제정치','성·친밀감·착취','심문·고문·구금·암살','심리·윤리','서사 장치','공간·소품·화면','기관·별칭','혼동 구분','몸 방향·포즈','시선·표정','손동작','두 인물 관계','테일러링','외투·일상복','기능복·전술장구','야회복·스타일','소재·핏','신발·장신구·가방','헤어·메이크업·변장','사건 흔적','촬영 용어','창작 조합']
lines=['# 전체 500행 키워드와 반영 경로','', '참조 대화의 원래 정의와 창작 예시는 인용 데이터다. 사실·지침·원인·동의·실제 신원이나 native 승인으로 취급하지 않는다. 시각 대안은 원래 개념 전체와 동일하지 않다. 기존 S/esp 식별자는 이전 registry에 연결된다.','']
for t,title in enumerate(sections):
 lines += [f'## {t+1}. {title}','','| ID | 원래 항목 | 원래 정의/예시 | 반영 상태 | 대안 카드 |','|---|---|---|---|---|']
 for r in sorted([r for r in routes if r['full_conversation_location']['table']==t],key=lambda r:r['full_conversation_location']['row']):
  definition=r.get('original_definition','')+(' / '+r['original_cells'][2] if len(r.get('original_cells',[]))==3 else '')
  vals=[r['id'],r['term_ko']+(' / '+r['term_en'] if r['term_en']!=r['term_ko'] else ''),definition,r['status'],', '.join(r['card_refs']) or '문맥/보류']
  lines.append('| '+' | '.join(str(v).replace('|','\\|').replace('\n',' ') for v in vals)+' |')
 lines.append('')
(D/'KEYWORD-ATLAS-FULL500.md').write_text('\n'.join(lines)+'\n')
v=['# 새 시각 의미 카드 42개','','각 카드는 하나의 완결된 한영 제안이며 native_approval=false다. 모든 접점과 소유자, 물리 매체/묘사 이미지 경계는 함께 유지한다. 아래 게이트는 실제 이미지로 별도 검증해야 한다.','']
for c in cards:
 v += [f"## {c['id']} — {c['name_ko']}",'',c['visible_en'],'',c['visible_ko'],'', '관계: '+ '; '.join(f"{r['subject']} → {r['relation']} → {r['object']}" for r in c['directed_relations']), '', '관찰 게이트: '+ '; '.join(c['observable_gates']), '', '혼동 경계: '+ '; '.join(c['confusion_boundaries']), '', '출처 범위: '+c['source_support_scope']+' '+', '.join(c['source_refs']), '', '후보: '+c['candidate_id'], '']
(D/'VISUAL-CARDS.md').write_text('\n'.join(v)+'\n')
arm_reports=[read(A/'arm-a-final.json'),read(B/'arm-result.json'),read(C/'arm-report.json')]
result={'schema':'espionage-full-conversation-results/v1','completed_at':datetime.datetime.now().astimezone().isoformat(),'research_rows':500,'additional_rows':160,'new_visual_options':42,'new_diagnostic_records':160,'new_bindings':71,'old_appearance_routes_deferred':65,'default_release':read(D/'installed-data-equivalence.json')['default_config'],'retrieval':summ,'native_image_calls':3,'successful_native_images':3,'extra_image_calls':0,'fallback_calls':0,'new_sources_formally_adopted_arms':0,'new_sources_retained_as_inspiration_arms':0,'new_source_pixel_qualification':'UNSCORED_NOT_ADOPTED','strict_whole_scene_passes':0,'strict_whole_scene_cases':3,'arms':[],'independence':'Fresh independent pre-core inputs and distinct random whole scenes. B/C had post-freeze incidental visibility of older completed-arm status summaries; unchanged freezes and non-use declarations retained. No claim of fully blind exposure.','user_acceptance':'pending','causal_improvement_from_new_data':'not established','commit_push':'not performed by this task'}
labels=['서고 계단의 연락원','항구 검문소의 여권 교환','창가의 도시어·콘택트시트']
failures=['외투 앞판의 crease ridge/trough 불명확; actor 오른손 엄지→봉투 flap 접점 불일치','카우보이 숏의 하단 경계가 허벅지 중간보다 내려감','왼손이 종이 아래 흰 여백 대신 오른쪽 여백에 접촉']
for i,n in enumerate('ABC'):
 row={'arm':n,'concept_ko':labels[i],'image':str(images[i]),'original_image':str(originals[i]),'image_sha256':hashlib.sha256(images[i].read_bytes()).hexdigest(),'exact_runtime_prompt':str(D/'prompts'/f'{n}.txt'),'strict_whole_case':'FAIL','failure':failures[i],'native_new_source_adoption':0,'new_source_pixel_status':'UNSCORED_NOT_ADOPTED','official_technical_qualification':['fail','pass','fail'][i],'coordinator_pixel_review':str(D/f'coordinator-pixel-{n}.json'),'child_report':str([A/'arm-a-final.json',B/'arm-result.json',C/'arm-report.json'][i])};result['arms'].append(row)
write(D/'RESULTS.json',result)
plan='''# 후속 반영·검증 계획

## 1. 실제 장면에서 후보가 채택까지 연결되는 경로

120개 목표 질의는 상위 8개에 노출됐지만 실제 세 장면의 관리된 표본에서는 각기 무관하거나 맞지 않는 신규 대안 하나씩만 노출됐다. source 등록/검색 점수/샘플/허용 효과/전체 조건/선택/실제 문장을 구분해 추적한다. B light_direction의 positive-scope projection 배제도 별도 조사한다. 후보 이름을 섞어 다시 질의하거나 기존 봉인을 수정해 성공으로 만들지 않는다.

다음 독립 실행은 자료 접근 전에 장면의 소유자·표면·카메라 목표를 중립 언어로 먼저 봉인한다. 실제 원본 질의와 requester/authorial 권한 근거를 보존한다. 완결된 관련 대안이 표본에 도달하는지, 전체 조건/효과가 원래 요청과 맞는지 확인한다. 부적합하면 미채택이 정답이며 채택률만 높이기 위해 조건·효과·커널을 완화하지 않는다. 연구 그래프를 ordinary native 사실이나 승인으로 승격하지 않는다.

## 2. 이미지 투영의 실패를 각각 분리해 보정

- A: 마모 얼룩과 crease를 공간적으로 분리하고 한 개의 넓은 능선/인접 골을 읽을 수 있는 크기·빛을 확보한다. actor-relative 오른손 엄지와 실제 봉투 flap의 접점을 별도 게이트로 유지한다.
- B: 하단 프레임 위치를 허벅지의 중간 지점과 함께 고정한다. 머리·양손·여권·전경 문틀·림광을 유지하면서 아래쪽 과다 노출을 줄이는 구도를 새 독립 초안에서 비교한다.
- C: 손가락 목표를 종이 아래 여백 중앙으로 명시하고 오른쪽 여백과 충분히 떨어뜨린다. 양쪽 인쇄물 경계와 실제 창을 동시에 유지한다.

통과 조건은 한 이미지에서 모든 고정 접점과 경계가 함께 관찰되는 것이다. 일부 부품·분위기 성공이나 공식 embodiment PASS로 전체 strict 실패를 상쇄하지 않는다. 이번 3장의 실패는 그대로 보존하며 추가 생성은 이번 결과에 합산하지 않는다.

## 3. 남은 자료의 범위

기존 외형 65행은 개별 이웃 탐색/미해결 사유를 보존한다. 기존 source의 전체 문맥·성인 제한·레이어·효과·관계까지 확인한 뒤 재사용/새 완결 대안/문맥/보류를 결정한다. 역사적 microdot·위장 무기·암호기 등 정확한 표본/기능은 박물관 원자료와 부품 경계를 확인하기 전 보류한다. 기관 소속·성폭력·동의·협박·PTSD·도덕적 손상·강제실종은 비시각 조건을 긍정 시각 후보로 자동 변환하지 않는다.

## 4. 다음 검증의 증거 기준

새로운 독립 원문 요청/초안과 시드, source CID/RID/guard/effect/전체 문장, native 선택 또는 inspiration_only, 실제 프롬프트 해시, 참조 사진 전송, 1회 생성 원본, 사전 게이트별 픽셀 판단을 다시 연결한다. 사용자 수용은 실제 사용자의 판단을 받기 전 pending이다. 이번 결과는 데이터가 이미지 개선의 원인이었다는 통제 비교가 아니다.
'''
(D/'FOLLOWUP-PLAN.md').write_text(plan)
report=f'''# 첩보물 전체 대화 보강·재테스트 결과

크롬에서 참조 대화의 전체 본문과 **500행**을 확인해 누락 **160행**을 보강했다. **시각 대안 42개·문맥 diagnostic 160개·선택적 바인딩 71개**를 추가하고 기본 실행본에 설치했다. 원본 사진을 실제 첨부한 새 독립 이미지 생성은 **3/3 성공**, 사전 strict 전체 통과는 **0/3**이다. 세 실행 모두 **신규 후보 정식 채택·영감 반영 0개**여서, 이번 이미지가 새 데이터에 의해 개선됐다는 결론은 내릴 수 없다.

## 확보·반영 범위

500행은 단일 용어 480개, 혼동 구분 8행, 창작 조합 12행이다. 기존 340행 대비 추가 범위는 정치/조직 13, 성/친밀감/착취 17, 심문/고문/구금/암살 22, 심리/윤리 12, 서사 18, 공간/소품 17, 기관명 16, 구분 8, 표면 흔적 13, 촬영 12, 조합 12행이다. 헤어 20항목은 기존 범위에 이미 있었다.

원래 정의와 새 시각 대안은 동일시하지 않는다. 실제 신분·충성·동의·강요·진단·원인·시간·소리·진위·화학·성능을 표정이나 복장으로 확정하지 않는다. 연구 그래프와 출처는 native 승인으로 쓰지 않는다. 기존 외형 65행과 표본 의존 항목은 보류를 유지했다. 창작 조합 12개는 강제 프로필로 설치하지 않았다.

- {link(D/'RESEARCH.md','출처·경계·반영 방법')}
- {link(D/'KEYWORD-ATLAS-FULL500.md','전체 500행과 연결 상태')}
- {link(D/'VISUAL-CARDS.md','42개 시각 의미 카드와 관찰 게이트')}
- {link(D/'registry-closure.json','기존/신규 registry 연결 검증')}

## 설치·검색 검증

기본 H-F2 `{result['default_release']['generation_id']}` / native `{result['default_release']['native_generation_id']}`. 동시 발표된 다른 주제 자료를 보존한 기준선 **21,480개 record 전체와 모든 기존 binding/catalog/policy/커널**을 유지하고 202개 record를 추가했다. 작업 사전·native index·전체 배포 검증·recorder 검사·새 source round-trip이 통과했다. 원래 연구 34개 파일과 이전 결과/이미지 등 56개 integration member는 해시가 유지됐다. 공유 corpus/index/runtime 포인터의 정당한 후속 갱신은 별도 기록했다.

| 질의군 | 한/영 질의 | 목표 후보 상위 8 |
|---|---:|---:|
| 원문 smoke | 84 | 84 |
| 자연어 재표현 | 36 | 36 |
| 일반/비시각/혼동 대조 | 20 | 별도 경계 비교 |

일반·비시각 대조 16개는 기존 상위 8이 모두 유지되고 새 후보 유입이 없었다. 혼동 대조 4개에는 관련 신규 후보 5회가 노출됐다. 이는 긍정 채택이나 false-positive 판정이 아니다. 모든 source 진단 기록은 긍정 검색에서 제외됐다. 실제 BM25F 1회+local cosine 1회를 질의마다 확인했다. 원문과 연구자 재표현이므로 독립 holdout이나 픽셀/채택 성공은 아니다.

이미지 arm은 동일 보강 202개가 들어간 설치본 `607f27b10495bfaad80edd62ec932b863fb8365098ea90e4cb3b694ec656fa25`에 고정했다. 이후 최종 union은 다른 주제 변경을 추가 보존했고 동일 보강 source 및 71 binding row와 검색을 재검증했다. 이미지 기록을 최종 union에서 생성한 것으로 바꾸지 않았다.

## 세 독립 이미지 테스트

현재 로컬 최신 SKILL SHA `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`. 세 새 에이전트는 각자 무작위 전체 장면과 기준을 자료 검색 전에 봉인했다. 각 native 호출은 정확히 1회, 원본 portrait의 실제 referenced_image_paths와 SHA를 확인했다. API/fallback/재생성은 0회이며 관찰된 모델 ID는 도구가 제공하지 않았다.

| arm | 장면 | 실제 보인 것 | strict 실패 | 공식 기술 qualification |
|---|---|---|---|---|
| A | 서고 계단 연락원 | 커프에 연결된 낱실·마모 경계·물방울·봉투/계단 | crease 입체 구조, 오른손 엄지→flap 접점 | fail |
| B | 항구 검문소 여권 교환 | 두 인물의 손과 같은 booklet·전경 가림·림광 | 허벅지 중간보다 낮은 crop | pass (embodiment 5/5), strict는 fail |
| C | 창가 도시어/콘택트시트 | 4칸·종이 경계·두 클립·사진/실제 창과 gate 구분 | 손가락이 아래 여백 대신 오른쪽 여백에 접촉 | fail |

신규로 노출된 것은 A의 coat tear/opaque lining, B의 POV hands/folder, C의 temple moisture beads다. 각각 고정한 장면의 전체 조건/소유자/효과와 맞지 않아 미채택했다. A/B는 기존 일반 source에서만 국소 inspiration을 유지했고 C는 독립 baseline 그대로다. 새 source의 픽셀 성공은 **UNSCORED_NOT_ADOPTED**, 장면 자체의 사전 strict는 **FAIL**이다. 이미지 호출/저장 성공과 공식 리뷰 기록 유효성도 전체 strict와 구분했다.

B/C는 봉인 후 상태 확인 도구에서 이전 테스트의 완료 요약을 우발적으로 본 예외를 기록했다. 현재 다른 full arm의 파일·완전한 프롬프트·이미지는 읽지 않았다는 선언과 변하지 않은 봉인을 보존했다. 완전 블라인드 노출 실험이라고 주장하지 않는다. 코디네이터도 원본 픽셀을 직접 재검토했다. B 상부 lintel 가시성은 코디네이터가 추가 보수 판정으로 남겼으며, B3 crop 실패와 전체 결론은 같다. C의 gate 비교는 native crop 재검토로 확인했으며 초기 불확실성 기록도 보존했다.

'''
for i,n in enumerate('ABC'):
 report+=f"### {n}. {labels[i]}\n\n{link(D/'prompts'/f'{n}.txt','실제 전송한 정확한 프롬프트')} · {link(Path(result['arms'][i]['child_report']),'독립 결과')} · {link(D/f'coordinator-pixel-{n}.json','코디네이터 픽셀 판정')}\n\n![{labels[i]}]({images[i]})\n\n"
report+=f'''## 후속 계획과 남은 한계

{link(D/'FOLLOWUP-PLAN.md','구체적인 후속 반영·검증 계획')}에 실제 장면의 후보 노출/전체 조건/채택 추적, A의 crease·엄지 접점, B의 정확한 crop, C의 아래 여백 접점을 우선순위로 남겼다. 추가 생성으로 이번 실패를 덮지 않았다. 기존 미검토 65행과 표본 의존 항목도 개별 source 검토 전까지 보류한다.

초기 staged store는 recorder import 검사를 통과했지만 실제 native loader가 쓸 모델 부속 파일이 없어 세 arm 모두 검색 전에 중단됐다. 실제 installer의 SHA 검증 모델 배치와 full deployed 검증 후 같은 generation의 설치 경로로 해결했고 source/core/plan을 바꾸지 않았다. 동시에 기본 실행본이 갱신되어 기존 선택을 덮어쓰지 않았으며, 이를 보존한 union을 별도로 설치했다. {link(D/'pre-retrieval-incident.json','오류·복구 기록')}에 남겼다.

{link(D/'native-artifact-validation.json','원본 참조·정확 프롬프트·세 ledger·원본/복사 hash 검증')} / {link(D/'installed-data-equivalence.json','최종 설치 source 동등성')} / {link(D/'RESULTS.json','기계 판독 결과')}. 사용자 수용은 pending이다. 이 작업에서는 commit/push를 수행하지 않았다.
'''
(D/'RESULTS.md').write_text(report)
(D/'README.md').write_text('# 첩보물 전체 대화 보강\n\n'+link(D/'RESULTS.md','결과·3개 이미지·프롬프트')+' · '+link(D/'RESEARCH.md','상세 연구')+' · '+link(D/'KEYWORD-ATLAS-FULL500.md','전체 500행')+' · '+link(D/'FOLLOWUP-PLAN.md','후속 계획')+'\n\n500행 확보, 42개 시각 대안/160개 context/71개 binding 추가 및 기본 실행본 설치. 검색 목표 120/120 상위 8 노출. 새 이미지 3개, strict 0/3, 신규 후보 정식 채택 0/3. 각 계층의 증거와 한계를 결과 문서에 분리했다.\n')
print('Final report, 500-row atlas, 42 visual cards, followup plan written')
