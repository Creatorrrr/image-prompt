독립 실험 arm-a는 기본 image_gen 한 번으로 사용 가능한 1024×1536 이미지를 만들었다. 선택한 건네기 시각 프로필의 4개 관계와 신체 동작 5개 hard gate는 원본에서 PASS로 기록했다. 그러나 표정 슬롯 ae_smize의 볼 상승·열린 눈 좁힘이 분명하지 않아, 선택 DATA 전체의 픽셀 판정은 **FAIL**이다. 전체 작품 인상은 따뜻하고 은근한 초대로 읽힌다는 작성자 판단이며, 사용자 수용은 아직 없다.

컨셉은 ‘마지막 무화과, 문을 닫기 전에’다. 비 오는 저녁 동네 카페의 종료 시간에 새로 설정한 28세 성인 여성이 관람자에게 마지막 무화과 반쪽을 건넨다. 참조 사진에서 직접 본 얼굴·머리만 사용했다. 성인 나이, 카페, 옷, 몸, 제안 행동과 내적 의미는 참조 인물에 대한 추론이 아니라 새 작성자의 설정이다.

저장된 기본값 sensual1/fetish0/creativity1/surreal0, auto→sensual_led를 바꾸지 않았다. 정적인 바 화보 방향과 카페의 실제 제안 방향을 비교했고, 후자가 특정 상대와의 관계를 한 장에서 더 분명하게 보여 준다고 판단했다. WHO/WHERE/HOW/WHY NOW와 SIR를 공개 작성 기록에 짧게 남겼다. 사용자 원문 envelope와 과거 시험 방식의 문맥을 유지했고, 실험 주제 ‘유혹적인’이나 제가 고른 의상·장소·행동을 사용자 정의나 잠금으로 넣지 않았다.

284단어 baseline, 코어, 신체 검토, feature selection10개, CASE와 해시를 검색 전에 동결했다. 모든 동결 파일은 마지막에 다시 해시를 검증해 그대로 남아 있음을 확인했다. 순서상의 편차도 남겼다. 중립 catalog를 전체 컨셉 비교를 글로 정리하기 전에 읽었으므로 strict theme-before-catalog 절차 PASS는 주장하지 않는다. candidate/profile/assets/references/scripts/다른 arm은 동결 전에 읽지 않았다.

keyword/offline 경로로 후보팩을 **1회** 생성했다. 시각 프로필8개, ordinary slot64개, sensual inventory12개, creative sample5개, optional bundle5개가 반환됐다. 선택과 고려한 후보, 필수 contextual shortlist, creative sample의 완전 계약을 읽었다. 다른 미채택 슬롯은 catalog에서 선별했으며 읽지 않은 완전 계약까지 검토했다고 주장하지 않는다. 모든 반환 계약과 출처는 DATA-APPLICATION에 보존했다.

시각 프로필 `visual-concept:pc_pc16_owner_relation`을 선택했다. 연결된 주인공 손의 카메라 방향 뻗기, 손과 건네는 물체의 접촉, 얼굴보다 가까운 평면, 물체 뒤 표정 가독성의 네 구성요소를 모두 적용했다. 무화과 제안과 손 접촉은 독립 baseline에 이미 있었으므로 DATA의 새 착상으로 세지 않는다. 새 구체화는 ‘the fig remains below her chin’이며, 기존 제안의 앞뒤 평면과 얼굴 가독성을 명확히 한다.

슬롯 `slot:expression:ae_smize`는 기존 작은 비대칭 미소를 볼·열린 눈까지 연결하도록 선택했다. 적용한 정확한 문구는 ‘Her mouth corners turn up unequally; the cheeks lift softly, narrowing the open eyes a little as she offers the red fig toward us’다. 작은 미소 자체는 이미 baseline이었고, 새로 적용한 구성요소는 부드러운 볼 상승과 열린 눈의 가벼운 좁힘이다. 기본 강도에서 steadier gaze, robe, scarf/hair ornament 방향을 구체적으로 비교했지만 작품의 시선·과일 중심 관계를 더 분명하게 하는 선택을 유지했다. 그 거절은 작성자의 미적 판단이며 사용자 금지 조건이 아니다.

| 검증 층 | 실제 결과 |
| --- | --- |
| precore feature/body binding | PASS, warnings0 |
| composed prompt | PASS, failures0; baseline으로 보존한 intent에 대한 warning4 |
| 정확한 runtime request | PASS, reference1과 해시·prompt/negative·시각 계약 일치 |
| 실제 image_gen | SUCCESS, 실제 호출1, retry0, API fallback0 |
| opt-in offering 프로필과 embodiment hard gate | PASS,9/9 |
| 선택 슬롯 전체 의미 | FAIL, 볼 상승·눈 좁힘 미확인 |
| 동결 CASE의 작품 관찰 기준 | 작성자 PASS, 구체적 연출 차이는 별도 기록 |
| 공유 render-review 감사 | technical_qualified=true, schema failure0; 사용자 판단 pending으로 exit1 |
| 최종 선택 DATA 전체 | FAIL, partial_is_fail 적용 |
| 유지보수 DATA의 인과적 개선/사용자 선호 | 미입증/미수신 |

이미지에는 앞으로 향하는 손·무화과와 뒤의 얼굴이 명확하게 나뉜다. 눈과 입은 가리지 않고, 두 손이 각각 무화과와 접시를 일관되게 갖고 있다. 따뜻한 벽등과 젖은 유리, 치운 테이블 위의 뒤집힌 의자는 종료 시간의 분위기를 만든다. 상체는 계획보다 더 기울었고, 카메라도 약간 더 높게 읽히며, 의자는 baseline의 seat-to-seat 대신 테이블에 올린 형태다. 이것을 초기 기준을 바꿔 숨기지 않고 원본 관찰로 기록했다.

실제 tool prompt SHA-256은 `7db6d5a2037b7112bed63d2ba2939e774bb933555fd9513f50f3d8bcb1f2c292`다. 이미지 SHA-256은 `e56cc72e7e8b2cd4c4ffbb92e1835789ba5110c5661a5247ed6b03c3555b80cf`이며 tool이 알려 준 원본 경로에서 동일 bytes로 arm에 복사했다. 원본을 삭제하지 않았고 local view_image로 확인했다. 생성 전 JSON 저장 따옴표 오류와 첫 복사 준비에서 PIL 부재가 있었지만 각각 저장/복사만 수정했으며 이미지 도구를 다시 호출하지 않았다.

composed/runtime PASS는 실제 픽셀이나 미적 성공을 뜻하지 않는다. 이미지를 읽은 작성자 판정과 그 기록을 감사한 결과도 별개다. baseline의 별도 렌더나 이전 DATA 반사실 비교가 없으므로 최신 DATA 반영이 이미지를 개선했다는 인과 결론은 낼 수 없다. 현재 한 장에서 실제 노출·선택·문구 적용과 살아남은 관계, 미완성 슬롯을 확인한 시험이다.

검토 파일은 [CASE](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/universal-authorship-qualification-20261005/arm-a/CASE.json), [작성 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/universal-authorship-qualification-20261005/arm-a/AUTHORING-NOTES.md), [DATA 적용](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/universal-authorship-qualification-20261005/arm-a/DATA-APPLICATION.json), [최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/universal-authorship-qualification-20261005/arm-a/final_prompt_en.txt), [원본 픽셀 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/universal-authorship-qualification-20261005/arm-a/render_review.json), [DATA gate 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/universal-authorship-qualification-20261005/arm-a/DATA-GATE-REVIEW.json), [machine-readable 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/universal-authorship-qualification-20261005/arm-a/RESULT.json)다. [이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/universal-authorship-qualification-20261005/arm-a/generated_images/last-fig-at-closing-20261005/exec-ca9caaa7-017c-47bc-b821-73a3f27ae57b.png)와 [run manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/universal-authorship-qualification-20261005/arm-a/run_manifest.json), [ledger](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/universal-authorship-qualification-20261005/arm-a/runs/image_runs.ndjson)도 arm-a에 보존했다.
