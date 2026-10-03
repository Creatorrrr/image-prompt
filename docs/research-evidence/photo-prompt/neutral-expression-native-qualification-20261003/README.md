# Three independent native image tests

독립 에이전트 세 명이 다른 무작위 복합 컨셉을 정하고 첨부 사진을 참고해 실제 이미지를 한 장씩 생성했다. 정상 V6 후보팩 조회와 선택, 프롬프트 구성 감사, 정확한 생성 요청 감사는 세 사례 모두 통과했다. 원본 픽셀을 별도로 확인한 결과 **A/B는 전체 FAIL, C는 정한 관찰 조건 PASS**다. 루트도 세 원본 이미지를 직접 검토해 이 판정에 동의한다.

| 사례 | 컨셉과 주요 키워드 | 초기 동결 조건 | 선택 profile·embodiment 조건 | 전체 판정 |
| --- | --- | --- | --- | --- |
| A | 비가 그친 골목 제본실. 아래배 `plump`, 몸통 옆선 `curvaceous`, 위팔 `fleshy` | 3/6 PASS | 5/8 PASS | FAIL |
| B | 저녁 광학 시험실. 긴 사지 `willowy`, 좁은 폭 `slender`, 팔의 국소 정의 `sinewy` | 3/6 PASS | 8/9 PASS | FAIL |
| C | 시장 위 옥상 판화실. 현재 `pouty lips`, 종이등 방향 `side-eye`, 피부·도자기 `smooth`, 가죽 입구 `supple` | 6/6 PASS | 9/9 PASS | PASS |

초기 조건과 파생 조건은 일부 같은 관찰을 검사하므로 두 열을 독립적인 품질 표본 수로 합치지 않는다. 부분 충족과 불관측은 FAIL이다. 실제 호출은 **총 3회**, 저장 이미지 **3장**, 차단된 호출은 0회다. 사용자 미적 수락은 별도이며 아직 받지 않았다. Native 도구가 모델 이름을 노출하지 않아 unknown으로 기록했다.

## 이미지와 프롬프트

- **A:** [최종 프롬프트](arm-a/prompt_en.txt) · [negative](arm-a/negative_en.txt) · [원본 PNG](arm-a/generated_images/arm-a-book-repair-20261003T032108Z/native.png) · [최종 arm 결과](arm-a/QUALIFICATION_RESULT.json)
- **B:** [최종 프롬프트](arm-b/standalone_prompt_en.txt) · [negative](arm-b/standalone_negative_en.txt) · [원본 PNG](arm-b/generated_images/optical-bay-attempt-01.png) · [모든 조건의 원장](arm-b/combined_pixel_review.json)
- **C:** [최종 프롬프트](arm-c/prompt_en.txt) · [negative](arm-c/negative_en.txt) · [원본 PNG](arm-c/generated_image.png) · [최종 arm 보고서](arm-c/QUALIFICATION.md)

### A: 부위 볼륨을 옷 주름·가림과 구별

위팔에는 둥근 살집과 어깨·팔꿈치로 이어지는 부드러운 전환이 보인다. 참고한 얼굴·단발과 책·실의 수리 장면도 읽힌다. 아래배는 수평 니트 주름과 늘어진 천의 부피가 주된 단서여서 국소 몸 볼륨을 분리하기 어렵다. 가까운 팔이 옆 몸통을 가려 지정 lower-rib→flank→lower-belly의 안쪽·바깥쪽 곡선과 연속성을 동시에 확인할 수 없다.

일반 후보 `ne_regional_soft_volume`, `ne_regional_contour_transition`과 optional visual concept `ne_regional_contour_transition`을 실제로 채택했다. 후보의 검색 노출과 감사 통과를 곡선 구현 성공으로 간주하지 않았다. [초기 6개 기준](arm-a/initial_pixel_gates.json), [초기 기준 원본 판정](arm-a/supplemental_pixel_review.json), [파생 기준 판정](arm-a/native_hard_gate_review.json), [파생 감사](arm-a/native_hard_gate_review_audit.json).

### B: 길이·폭·표면 정의를 따로 검증

전신에서 몸통 대비 긴 팔다리와 좁은 팔다리 윤곽은 확인된다. 팔 표면은 매끈한 조명 전이가 주로 보여 얕고 길게 이어지는 근육·힘줄 윤곽은 부족하다. 얇다는 이유로 `sinewy`를 통과시키지 않았다. 두 손의 기계 접촉은 있지만 휠 손이 가슴 높이에 있어 양손이 허리 높이에 있어야 한다는 동결 조건에 실패한다. 작은 부품을 새로 놓은 순간도 기존 bracket·control과 구별할 수 없다.

일반 후보 `willowy_long_limb_proportion`, `bm_wiry_definition`, optional profile `bm_long_limb_build`를 채택했다. 길이 profile의 4개 조건은 통과해도 wiry 일반 후보의 근육·힘줄 구현은 실패다. 기존 `slender_linear_build` optional profile은 긍정적인 좁은 폭 구성요소와 비시각적 owner-separation 문구가 맞지 않아 채택을 거절했다. 별도로 동결한 폭 조건은 픽셀에서 판정했다. [초기 6개 기준](arm-b/initial_pixel_gates.json), [초기 기준 원본 판정](arm-b/pixel_test_review.json), [모든 조건의 합집합](arm-b/combined_pixel_review.json), [파생 기준 판정](arm-b/render_review.json), [파생 감사](arm-b/render_review_audit.json).

### C: 현재 동작과 물체별 표면을 구별

눈동자는 거의 정면인 얼굴에 비해 화면 오른쪽 위 종이등으로 향한다. 위·아래 입술은 작은 둥근 전방 모양과 중앙으로 모인 양끝을 보이며, 원래 입술의 볼륨만으로 동작을 대신하지 않는다. 피부의 미세결과 도자기의 연속된 유약 반사는 서로 구별된다. 가죽 윗입구는 엄지 접촉 지점에서 안으로 굽고 주름이 이어진다. 이는 현재 굽힘 상태만의 관찰이며 복원성·반복 탄성·전체 재료 거동을 입증하지 않는다.

일반 `pv_side_eye`, optional visual concepts `ne_current_lip_protrusion`, `pe_texture_preserving_tone_evening_relation`을 채택했다. 선택 profile 4개와 embodiment 5개 조건도 모두 통과했다. 세로 방향보다 정사각형에 가까운 출력, 열린 손바닥보다는 감싸 쥔 도자기 grip, 낡은 파우치 아랫면은 별도 장면 차이로 남겼다. PASS는 정한 관찰 조건의 통과이며 작성한 모든 세부나 미적 선호를 완벽히 재현했다는 뜻은 아니다. [초기 6개 기준](arm-c/pixel_gates.json), [초기 기준 원본 판정](arm-c/independent_pixel_review.json), [파생 기준 판정](arm-c/render_review.json), [파생 감사](arm-c/render_review_audit.json).

## 독립성과 생성 입력

각 arm은 `SystemRandom`으로 컨셉을 선택하고 장면·대체 표현의 뜻·범위·관찰 조건을 따로 작성했다. 실제 인간 요청은 coordinator envelope로 보존했다. synthetic 장면과 키워드 정의를 사용자 정의로 꾸미지 않고 `user_definitions=[]`를 유지했다. 연구 데이터, 운영 후보, 다른 arm 결과를 보기 전에 baseline·core·controls·embodiment·초기 픽셀 조건을 동결했다. 동결 파일 A15/B14/C16개는 끝까지 같은 해시다.

공유 운영 입력 [92개 manifest](../neutral-expression-integration-20261003/OPERATIONAL-INPUTS.json)의 파일 해시가 모두 일치한 뒤 일반 CLI 후보팩을 만들었다. 자유로운 dimension에서 의미가 맞는 후보를 선택하고 구성 감사에 통과한 문구로 생성했다. 제출한 native argument의 prompt hash는 runtime audit의 prompt ID와 일치하고, 첨부 reference 파일 해시도 실제 파일과 같다. 얼굴·머리 외관만 참고했으며 각 인물의 28/29세 성인 조건, 체형, 직업, 사건은 합성 작성값이다. 원본의 실제 정체성·나이·체형·특성은 판정하지 않았다.

원본 PNG는 A 1237×1272, B 1024×1536, C 1237×1272이며 이미지 바이트를 변경하지 않았다. 각 arm에 V2 manifest와 image ledger를 저장했다. [루트의 원본 검토·해시·합집합 판정](ROOT-INDEPENDENT-PIXEL-REVIEW.json), [A ledger](arm-a/runs/image_runs.ndjson), [B ledger](arm-b/image_runs.ndjson), [C ledger](arm-c/image_runs.ndjson).

이 실행은 후보 접근→선택→감사→실제 생성→원본 관찰의 연결을 검증한다. 같은 장면의 데이터 보강 전·후 생성 대조 실험은 하지 않았으므로 대체 표현 추가만의 인과 효과나 전체 어휘의 보편적 성공률을 주장하지 않는다. 실패 조건도 동결 원장과 함께 보존했다.
