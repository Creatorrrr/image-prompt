# 인물 패션 시각 의미 — 독립 3개 에이전트 이미지 검증

시각 의미 프로필 28개·일반 후보 40개·선택 번들 14개가 실제 소스와 색인에 반영된 상태를 확인한 뒤, 독립 에이전트 3개가 서로 다른 복잡한 장면을 구성했다. 실제 이미지 3장을 보존하고 원본과 축소본의 픽셀을 검토했다. 렌더링한 프로필 7개 중 6개가 모든 구성 요소를 충족했다. **전체 고정 장면은 1/3 통과이며, 확장 데이터 전체의 qualification은 성립하지 않는다.**

| 에이전트·장면 | 채택한 새 시각 프로필 | 픽셀 결과 | 전체 장면 |
|---|---|---|---|
| A — 비 온 뒤 블루아워, 아르데코 전차 차고에서 노선도 액자 설치 | 시어 스타킹·스타킹 광택·양쪽 허벅지 피부 띠 | 시어·피부 띠 PASS, 광택 FAIL. 별도 미니스커트 외곽 PASS | FAIL — 손 좌우 반전, 광택 부족; 열린 블라우스 상단·건조 바닥 조건도 미충족 |
| B 대안 — 유리 지붕 환승 홀의 빈티지 조명 조절 | 불투명 피트·밀착 안쪽과 느슨한 바깥쪽의 볼륨 대비 | 모든 프로필 6개 성분 및 손잡이 접촉 PASS | PASS — 11/11 파생 게이트, 6/6 대상 게이트. 발은 프레임 밖이므로 발바닥 접촉을 직접 검증한 결과는 아님 |
| C 대안 — 도자기 가마의 황동 크랭크 조절 | 원숄더 지지·몸을 따라 여유 있게 흐르는 드레이프 | 두 프로필의 모든 6개 성분 PASS. 수동 셔링 위치 FAIL | FAIL — 지정한 배우 왼쪽 대신 오른쪽 허리에 셔링 생성 |

프롬프트 감사와 픽셀 판정은 분리했다. 5개 사례 모두 precore/composed/runtime 감사가 통과했으며 실제 semantic 모드로 팩을 생성했다. 보존 이미지들의 새 프로필 구성 요소는 19/21, coordinator 파생 게이트는 32/36 통과했다. 이 수치는 같은 세 이미지에서 집계한 관찰이며 성능 추정치나 데이터 개선의 인과 증거가 아니다. 사용자 수용 판정은 아직 없다.

**출력 차단과 별도 사례의 경계.** B의 원래 메쉬·배꼽 사례와 C의 원래 가슴골·카울 목선 사례는 image_gen 출력 검사가 sexual로 분류해 이미지를 반환하지 않았다. 각각 한 번 호출했고 원래 프롬프트·팩·기준을 변경하지 않은 채 UNSCORED로 보존했다. 이후 같은 독립 에이전트들이 완전 착의 의복 구조의 별도 사례를 만들었다. 총 호출은 원래 3회와 별도 대안 2회, 합계 5회다. 품질 재시도나 CLI 대체 생성은 없었다. 대안은 자기 arm의 기존 팩을 본 뒤 만든 developmental test이며, 원래 차단 키워드의 통과나 처음 보는 holdout으로 계산하지 않는다.

| 원래 차단 사례 | 팩 | 픽셀 판정 | 기록 |
|---|---|---|---|
| B 메쉬·실제 배꼽·불투명 인접 패널 | fd6b46616ef86ac3 | UNSCORED — 출력물 없음 | [판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-b-mesh/qualification_result.json) · [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-b-mesh/prompt_en.txt) |
| C 가슴골·카울·레이어 대비·얼굴과 의상 동시 가독성 | 68ccb35c65161521 | UNSCORED — 출력물 없음 | [판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-c-neckline/qualification.json) · [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-c-neckline/prompt_en.txt) |

**검색과 채택의 경계.** 5개 팩 전체에서 새 pfe_ 시각 프로필 18종이 노출되고 11종이 채택됐다. 그중 이미지가 반환된 세 사례에서 채택한 7종을 픽셀 평가했다. 새 일반 의상 후보 40개는 노출·채택 모두 0개이고, 새 선택 번들 14개도 노출·채택 모두 0개다. 기존 다른 번들의 노출을 새 번들의 성공으로 계산하지 않았다. 팩 데이터 등록·색인 성공을 후보의 렌더 효과로 해석할 수 없다.

A의 미니스커트 외곽, C의 셔링은 해당 팩에서 프로필/일반 후보가 발견되지 않았다. 미니스커트 외곽은 사전 수동 대상 기준으로만 통과했고, 셔링은 수동 의복 디테일로만 검토했다. 노출되지 않은 데이터를 사후 주입하거나 채택했다고 기록하지 않았다. B 원래 사례의 배꼽 프로필은 노출됐지만, 맨살 기준과 메쉬 통과 가독성 기준이 일치하지 않아 채택하지 않았다.

**독립성·참조·파일 검증.** 장면 seed는 A 287413, B 739821, C 463907이다. 원래 세 arm은 실제 사용자 문장을 담은 각자의 immutable envelope, 독립 baseline/core/테스트 기준을 먼저 고정하고 neutral precore 검증 뒤 한 번의 v6 팩 조회를 수행했다. 서로 다른 arm의 프롬프트·팩·이미지를 입력으로 사용하지 않았다. 대안도 자기 baseline/core/테스트를 새로 고정하고 별도 팩·원장·manifest를 기록했다. 원래 세 케이스의 root 고정 해시는 유지된다.

첨부 사진은 모든 호출에 실제 로컬 참조로 전달했다. 역할은 보이는 얼굴·단발·앞머리 외관 안내이며 신원, 보이지 않는 체형 또는 성격의 근거가 아니다. 이미지들은 단발·앞머리·읽을 수 있는 얼굴을 유지하지만 정확한 동일 인물 인증이나 사용자 선호의 확인은 하지 않았다. 동일 참조 SHA256은 048adbd3e4343a3725fec6aa0455aa1f367878560bc15d4493a18fde1ce8604c다.

소스 snapshot 5f05890f84b1eb0c9b39d1dbbd76ab40fef5688b3ff9f6cbabb2785fdca37df8의 97개 파일은 테스트 후에도 변경되지 않았다. 5개 사례의 reference/pack/선택/프롬프트/런타임/원장/manifest/이미지 해시 연결도 통과했다. 무결성 PASS는 픽셀 PASS와 별개다. Root는 이미지가 반환되는 순서대로 원본을 읽고 같은 결과의 축소본을 검토했으며, B/C는 각 arm 자체 판정 전에 원본을 검토했다. 계획의 ‘모든 이미지 완료 후 root 리뷰’와 달랐지만 다른 arm 프롬프트로 결과를 전달하지 않았다.

C의 independent arm은 위치 조건을 보조 디테일로 해석해 공식 게이트 11/11 PASS를 기록했다. Root는 사전 고정된 공식 visibility/projection 설명에도 배우 왼쪽 셔링이 보인다고 적혀 있어 그 완전한 조건을 FAIL로 평가했다. 두 원본 리뷰를 모두 보존한다. 6개 채택 프로필 구성 요소의 통과와 수동 셔링의 좌우 오류에는 두 리뷰가 일치한다. 전체 장면의 최종 보고는 FAIL이다. [해석 차이](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-c-neckline/covered-alternative/coordinator_disagreement.json)

A 이미지 — 전차 차고

![전차 차고 스타킹 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-a-hosiery/generated_images/tram-depot-hosiery.png)

[작성 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-a-hosiery/prompt_en.txt) · [실제 도구 입력](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-a-hosiery/runtime_prompt.txt) · [고정 테스트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-a-hosiery/test_case.json) · [root 픽셀 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-a-hosiery/coordinator_pixel_review.json) · [manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-a-hosiery/run_manifest.json)

B 이미지 — 환승 홀 조명

![불투명 피트와 느슨한 코트 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-b-mesh/covered-alternative/generated_images/covered-concourse.png)

[작성 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-b-mesh/covered-alternative/prompt_en.txt) · [실제 도구 입력](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-b-mesh/covered-alternative/runtime_prompt.txt) · [고정 테스트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-b-mesh/covered-alternative/test_case.json) · [root 픽셀 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-b-mesh/covered-alternative/coordinator_pixel_review.json) · [manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-b-mesh/covered-alternative/run_manifest.json)

C 이미지 — 도자기 가마

![원숄더와 드레이프 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-c-neckline/covered-alternative/generated_images/covered-kiln-fashion.png)

[작성 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-c-neckline/covered-alternative/prompt_en.txt) · [실제 도구 입력](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-c-neckline/covered-alternative/runtime_prompt_en.txt) · [고정 테스트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-c-neckline/covered-alternative/test_case.json) · [root 픽셀 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-c-neckline/covered-alternative/coordinator_pixel_review.json) · [manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/arm-c-neckline/covered-alternative/run_manifest.json)

[집계 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/qualification.json) · [저장 결과 무결성](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/saved-runs-verification.json) · [재검증 스크립트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/verify_saved_runs.py) · [독립성·호출 정책](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/qualification/independent-20260928-053217/protocol.json) · [원래 리서치](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/RESEARCH.md) · [추가 분석 반영 리서치](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928/ADDENDUM.md)
