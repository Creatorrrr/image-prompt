시각 의미 데이터의 대체 표현과 후보 데이터 반영을 완료했다. 기존 후보 67개의 한국어·영어 대체 표현 134개를 보강하고, 다른 접촉·소유·형태를 갖는 좁은 후보 15개를 추가했다. 새 시각 프로필 26개와 선택형 묶음 26개, 기존 프로필 11개의 대체 표현도 반영했다. 후보·프로필 인덱스를 모두 재생성했다.

독립된 서브에이전트 3개가 첨부 사진을 활용해 서로 다른 복잡한 컨셉을 만들고 실제 생성과 원본 픽셀 검사를 수행했다. 최종 판정은 **공방 PASS, 축제 BLOCKED_UNSCORED, 박물관 FAIL**이다. 내장 image_gen 호출은 총 5회, 반환된 원본은 3장이다. 이미지가 있는 두 컨셉에서 키워드 조건 9개 중 7개가 통과했다. 전체 컨셉 기준은 1개 통과, 1개 실패, 1개 미평가다. 사용자 수락은 아직 pending이다.

| 반영 대상 | 최종 반영량 | 확인 근거 |
|---|---:|---|
| 기존 후보 대체 표현 | 67개 후보 / 134개 KO·EN 문장 | 의미·효과·소유·기존 전제 조건 유지 검사 |
| 새 후보 | 15개 | 다른 형태·접촉은 독립 ID로 작성 |
| 새 시각 프로필 / 선택형 묶음 | 26개 / 26개 | 구성요소와 관계를 모두 요구하고 원본 가시성 gate 유지 |
| 기존 시각 프로필 대체 표현 | 11개 / 22개 KO·EN 예문 | 기존 activation·정의·효과·원본 gate 유지 |
| 후보 인덱스 | 10,000 → 10,015 | 동일 텍스트·벡터 9,933개 재사용; 67개 변경·15개 신규 |
| 시각 프로필 인덱스 | 1,787 → 1,813 | 동일 텍스트·벡터 1,776개 재사용; 11개 변경·26개 신규 |

대체 표현은 단순 감정·귀여움 수식어보다 관찰 가능한 상태로 작성했다. 예를 들어 윙크는 한쪽 눈이 닫히고 같은 얼굴의 반대 눈은 열린 상태, 고양이 앞발은 굽힌 손목과 느슨하게 접힌 손가락, 보케는 초점 밖 배경 광점의 부드러운 원반으로 표현한다. 모에소데는 자기 소매 끝이 손목을 지나 손의 지정된 부분을 덮는 관계다. 옷·손·얼굴의 소유와 기존 성인 교류 전제 조건을 함께 유지한다.

한쪽 볼 부풀림, 작은 O형 입, 넓은 눈꺼풀 틈, 엄지·검지 교차, 양손 하트 끝 맞닿음, 볼 찌르기·손바닥 받침·양볼 누르기, 양 검지 끝 맞닿음, 손가락 사이로 눈 보이기, 한쪽 뒤꿈치 들기, 양손 컵 잡기, 인형 안기, 상대 소매 집기, 일반 캐치라이트는 좁은 신규 후보로 분리했다. 기존 보류된 `pv_finger_heart`를 복구하거나 엄지·검지 교차를 무조건 finger heart로 취급하지 않는다. 일반 캐치라이트를 젖은 눈이나 고정된 두 광원과 동일시하지 않는다.

원래 조사한 140개 항목 모두에 처리 상태를 남겼다. 57개는 동등 표현으로 보강, 16개는 좁은 가시 변형 추가, 17개는 독립 core의 맥락 해석을 유지, 2개는 이름 붙은 변형의 근거 검토를 보류, 46개는 새 고정 형태 alias를 만들지 않았고 2개는 기존의 제한된 구성 표현을 재사용한다. 카와이·모에·애교·큐트 어그레션 같은 넓은 맥락을 고정 나이·큰 눈·분홍·리본으로 치환하지 않는다. `NO_NEW_FIXED_ALIAS` 항목의 관련 원시 요소 링크는 해당 문화적 의미나 모든 변형의 완전한 구현을 뜻하지 않는다.

[140개 항목별 처리표](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/TERM-DISPOSITIONS.md>) · [의미 검토 중 바로잡은 세 대체 표현](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/SEMANTIC-REVIEW-CORRECTIONS.json>) · [반영 명세](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/AUTHORED-RECEIPT.json>)

| 독립 arm | 컨셉과 주요 조건 | 최종 키워드 조건 | 전체 testcase / 실제 pack gate | 판정 |
|---|---|---|---|---|
| A | 도자기 공방: 꽃받침·윙크·한쪽 뒤꿈치·보케 + 유약 컵·점토 흔적·창빛·바닥 접지 | 4/4 | 9/9 · 5/5 | PASS |
| B | 등불 축제: 보케·고양이 앞발·윙크·눈물 고임과 미소·모에소데 + 젖은 계단·수레·증기·천막 | 미평가 5개 | 미평가 · 미평가 | BLOCKED_UNSCORED |
| C | 구름 박물관: 고개 갸웃·꽃받침·하이키·복슬복슬·캐치라이트 + 황동·유리·섬유·전후경 | 3/5 | 6/8 · 4/5 | FAIL |

A의 원본은 양손과 턱의 접촉·연결된 팔, 한쪽 감긴 눈, 한쪽 뒤꿈치 아래의 바닥 간격과 앞발 접지, 배경 광점의 흐림을 보여 준다. 공방의 유약광과 점토 흔적은 묘사된 작업 맥락의 외형으로 평가했고, 실제 과거 활동이나 물리적 젖음을 입증했다고 주장하지 않는다. B는 원래 입력을 그대로 유지한 두 번의 내장 도구 호출 모두에서 이미지가 반환되지 않았다. 다른 생성 경로로 우회하지 않았으며 다섯 조건을 PASS나 FAIL로 채점하지 않았다.

C의 첫 원본은 고개 방향과 손 가시성에서 실패했다. 동일 core·pack·키워드를 유지하고 고개 방향·손 가시성만 국소 수정한 두 번째 원본은 화면 오른쪽 기울기를 얻었지만 눈 선의 관찰 각도가 약 27°로 사전 고정한 약 10–20° 범위를 초과했다. 손바닥과 턱의 접촉은 보이지만 일부 엄지와 화면 오른쪽 손가락이 겹쳐 열 손가락의 개별 연결을 확인할 수 없다. 이 부분은 UNOBSERVABLE이며 필수 조건에서는 FAIL로 처리했다. 밝은 톤·긴 크림색 섬유·양안 캐치라이트와 박물관 공간은 통과했다. 일반적인 고개 갸웃·꽃받침 인식이 더 세밀한 사전 조건의 실패를 덮지 않는다.

[A 상세 판정](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-a/RESULT.json>) · [B 차단 기록](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-b/qualification_result.json>) · [C 최초·재시도 판정](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-c/ARM-C-RESULT.json>) · [코디네이터 원본 재검토](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/COORDINATOR-NATIVE-REVIEW.json>) · [동결 baseline과 실제 전송 프롬프트](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/PROMPTS.md>)

각 arm은 데이터·후보팩을 읽기 전에 독립 컨셉, 무작위 추출 기록, testcase, baseline prompt, core, creative controls 및 사전 특징 선택을 동결했다. 코디네이터가 보존한 실제 요청 envelope와 에이전트가 만든 장면 설명을 분리했다. 다른 arm의 생성 결과를 보지 않고 자기 작업 경로에서 진행했다. 첨부 사진은 보이는 얼굴·짧은 검은 단발·앞머리 외형 지침으로 사용했고 실제 신원·나이·성격을 추론하지 않았다. 생성 장면은 가상 성인으로 작성했다. 최종 DATA 148개 파일과 모든 사전 동결 파일의 해시는 종료 시 일치했다.

| arm | 실제 채택한 이번 반영 경로 | 직접 대상 프로필 노출 / 선택 | 남은 후보 노출 gap |
|---|---|---|---|
| A | `bundle:cv_bundle_flower_chin` | 0 / 0 | 윙크·한쪽 뒤꿈치·보케 대상 후보 |
| B | `bundle:cv_bundle_wink` | 0 / 0 | 보케·고양이 앞발·눈물 미소·모에소데 |
| C | `bundle:cv_bundle_flower_chin`, `slot:color_grading:pe_high_key_tones` | 0 / 0 | 고개 갸웃·복슬복슬·캐치라이트 |

14개의 키워드 probe 중 대상 후보를 채택한 경로는 4개다. 꽃받침·윙크 묶음에서 관련 프로필 ID가 참조되지만 이는 advisory이며 그 프로필의 직접 활성화를 뜻하지 않는다. 선택한 묶음 자체의 구성·관계와 실제 pack의 hard gates는 별도로 검사했다. A에서는 성인 flirt 표현 후보도 노출됐으나 독립 core의 전제 조건이 없어 채택하지 않았다. 따라서 중립적인 작업 중 장난스러움을 임의로 성인 flirt로 바꾸지 않았다.

성공한 픽셀에는 이미 독립 baseline에 들어 있던 요구도 포함된다. 이번 실행은 새 데이터가 실제 팩에 연결되고 선택될 수 있음을 보여 주지만, 이전 데이터와 비교한 A/B 실험은 수행하지 않았다. 후보 노출·선택·감사 통과와 이미지 품질 개선의 인과 증거는 분리한다. 특히 직접 프로필 노출 0/3은 다음 보강 시 우선 확인할 빈틈이다. 새 후보 15개 전부의 원본 이미지 적합성을 이번 세 컨셉으로 검증한 것은 아니다. 후속 조사·반영 순서는 다음 계획에 남겼다.

[후속 보강 계획](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/FOLLOW-UP-PLAN.md>)

검증 상태: 관련 검사 61개가 통과했고 사전 contexts 보존 강화 검사도 통과했다. 전체 1,536개 검사를 실행·분류했으며, 초기 class setup으로 실행되지 못한 17개는 수정 후 재검사했다. 최종 집계는 통과 1,496개, 기존 데이터·과거 증거 불일치에서 관찰된 미통과 40개(실패 method 13개·오류 method 27개)다. 실패 subtest 39개와 오류 27개를 원문 로그에 보존했다. 전체 suite는 PASS가 아니다.

사전 기준·holdout·과거 증거를 새 데이터에 맞춰 다시 작성하지 않았다. 뒤에 추가된 context overlay가 역사적 테스트의 제외 대상에 의존하는 경우에만 해당 oracle의 읽기 범위를 조정했다. 현재 전체 데이터의 기존 label·효과·전제 조건·기존 contexts 보존은 별도 검사했다. 이번 확장을 비활성화한 좁은 진단 재현에서도 기존의 목덜미 헤어 길이·원단 투명도 문제와 과거 registry oracle·baseline fixture 불일치가 남는다. 관련 원본들은 작업 시작 당시 해시와 일치하며 기존 수정된 V10–V12를 이 작업에서 재작성하지 않았다.

[검사 분류와 최종 재검사](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/TEST-TRIAGE.json>) · [기존 실패 분리 재현](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/EXISTING-FAILURE-REPLAY.json>) · [인덱스 재사용과 갱신 검증](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/INDEX-VERIFICATION.json>) · [기존 작성 데이터 보존](</Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/SOURCE-PRESERVATION.json>)

실제 runtime 반영 파일은 [후보 확장](</Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_cute_visual_forms_extension.json>), [시각 프로필 확장](</Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_cute_visual_forms.json>), 두 기존 pose/acting 프로필과 등록 파일이다. `prompt_generator.py`에는 두 확장 파일의 등록만 추가했다. 주제별 런타임 분기나 고정 장면 recipe는 추가하지 않았다. 기존 authored JSON 83개와 모든 이전 shard 세대를 보존했다. 커밋·푸시는 수행하지 않았다.

![공방: 최종 PASS](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-a/attempt-1-original.png)

![박물관: 최종 FAIL, 고개 각도와 손가락 가시성 실패](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/cute-semantics-integration-20261005/qualification/arm-c/attempt2_original.png)
