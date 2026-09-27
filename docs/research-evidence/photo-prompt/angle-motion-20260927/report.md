# 하이 앵글·로우 앵글·동적 구도 독립 이미지 테스트

2026-09-27. 이전에 첨부한 동일 사진과 현재 반영된 시각 의미·후보팩 데이터를 사용했다. 독립 서브에이전트 3개가 각각 랜덤 복합 장면을 정하고, 기준을 고정한 뒤 후보팩·프롬프트·native 이미지 생성·픽셀 검증까지 완료했다.

**엄격한 주제 판정은 2/3 통과, 고정한 전체 복합 장면은 1/3 통과**다. 하이 앵글과 로우 앵글은 뚜렷하게 구현됐다. 동적 장면은 일반적인 동세·앞 여백·공간 깊이를 구현했지만, 고정한 정확한 사선 방향과 가방 동세 조건을 충족하지 못했다. 생성·저장 성공과 픽셀 통과는 별도 결과다.

## 결과 비교

| 주제 | 독립 랜덤 장면 | 일반 주제 기준 | 정확한 필수 의미 | 엄격한 주제 판정 | 전체 복합 장면 | 몸·접촉 판정 |
|---|---|---:|---:|---|---|---:|
| 하이 앵글 | 종이 보존 공간에서 붓으로 종이를 눌러 펴기 | 5/5 통과 | 4/4 통과 | 통과 | 실패: 손바닥·먼 모서리 지지가 손끝·가까운 가장자리로 변경 | 4/5 통과, 전체 실패 |
| 로우 앵글 | 유리 온실에서 작업대 앞면을 닦고 여분 타월 들기 | 4/4 통과 | 4/4 통과 | 통과 | 통과 | 5/5 통과 |
| 동적 구도 | 젖은 강변 지하 통로에서 낮은 턱을 넘는 도약 | 4/4 통과 | 3/5 통과 | 실패 | 실패: 도면 통을 든 손과 지지·선행 발의 좌우 반전 | 3/5 통과, 전체 실패 |

동적 구도의 일반 4/4 통과를 엄격한 주제 통과로 승격하지 않았다. 생성 전에 고정한 필수 의미에는 전경 배수 턱까지 같은 사선 방향을 따라야 한다는 조건과 머리·가방 가장자리의 국소 동세가 포함되어 있다. 일반적인 달리는 자세가 이 두 조건을 대신하지 않는다.

## 같은 방식으로 실행한 절차

현재 요청문 전체를 그대로 보존한 봉투를 주 에이전트가 위임 전에 만들었다. 각 봉투에는 해당 주제의 정확한 부분과 첨부 사진·이전 방식이라는 공통 부분을 비중첩 active span으로 기록했다. 에이전트의 실행 브리프나 창작 설정을 사용자 정의로 기록하지 않았다.

세 에이전트는 대화 이력을 공유하지 않고 시작했다. 초기 입력은 요청 봉투, 직접 확인한 참조 사진, 일반 지식, photo-prompt 및 imagegen 스킬, 중립적인 사전 선택 카테고리뿐이다. 다른 에이전트의 컨셉·프롬프트·후보·이미지와 과거 실험 결과는 입력으로 사용하지 않았다.

1. 독립 랜덤 시드로 장소·행동·소품·빛을 정하고 카테고리 9개·9개·10개를 선택했다.
2. 기준 프롬프트, `photo-authorial-core/v3`, 몸·접촉 검토, 주제의 required typed assertion, 픽셀 테스트케이스를 먼저 고정했다.
3. 사전 선택 validator는 세 케이스 모두 `valid: true`, `warnings: []`였다.
4. 그 뒤에만 현재 데이터로 일반 semantic v6 후보팩을 각 1개 생성했다. compact view를 먼저 읽고 실제 노출된 후보를 선택·변형하거나 거절했다.
5. 최종 프롬프트와 실제 native 요청 감사를 통과한 뒤 참조 이미지를 실제로 첨부해 각 1회 생성했다.
6. 반환된 원본을 각 실험 폴더에 동일 바이트로 복사하고, 원본·축소에서 픽셀을 검토했다. 주 에이전트도 같은 원본과 축소를 다시 확인했다.

주 에이전트는 **09:27:18 UTC**, 세 이미지와 실제 요청 파일이 생기기 전에 각 core·기준·검토·봉투 등 7개 파일의 해시를 별도로 고정했다. 최종 검증에서 21개 파일 모두 그대로였다. [생성 전 독립 읽기 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/coordinator-pre-render-freeze.json)에 확인 시점과 해시가 있다.

첨부 원본은 얼굴·머리의 보이는 외형 참고다. 성인 창작 캐릭터의 활동을 연출하며 실제 인물의 정체성·실제 나이·직업·성격을 추론하지 않는다. 미적 만족이나 사용자 수용 판정은 아직 받지 않았다.

- 참조: [이전 첨부 사진](</Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg>)
- 참조 SHA-256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`
- 생성: native `image_gen.imagegen` 합계 3회, 각 ledger 1행·manifest v2.
- 재생성·대체 API·전달 이미지 수정: 0회. 축소본은 검토용이며 전달 원본과 구분했다.
- 카메라 판정: 보이는 원근·투영으로 상대적인 시점을 판단했다. 실제 높이·각도·초점거리 수치를 측정한 결과가 아니다.

## 하이 앵글

시드 `7350812925794127079`, pack `14641278dd8e497c`, run `345aa373062f1a5c`.

종이 보존 공간, 부드러운 넓은 붓, 금속 자와 얕은 안료 접시, 창 빛을 독립적으로 골랐다. 머리 윗면·어깨·넓은 작업대·주변 바닥이 동시에 보이고, 윗몸에서 작은 무릎·신발로 원근이 후퇴한다. 얼굴과 작업대 앞면은 유지되며 창틀의 안정된 방향도 읽힌다. 눈높이에서 고개만 숙이거나 화면만 기울인 장면과 구별되는 하이 앵글이다.

전체 장면은 실패했다. 오른손 붓의 종이 접촉은 보이지만, 왼손이 먼 모서리를 손바닥으로 받쳐야 하는 기준이 가까운 오른쪽 가장자리를 손끝으로 잡는 형태로 바뀌었다. 붓 옆 들린 종이 모서리가 펴지는 결과도 충분히 식별되지 않는다. 전체 장면 항목은 5/6 통과이며 몸·접촉의 `embodiment_contact_and_space`가 실패했다.

채택한 후보는 창 조명, 전신 범위, 물리 접촉, 재료 흔적 4개다. 전신 범위는 두 신발과 지지를 보이게 했고 종이 섬유·덱클 가장자리는 재료를 설명한다. 접촉 후보의 일부 구현이 정확한 왼손 지지 성공을 보장하지는 않았다.

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/high_angle/final_prompt_en.txt) · [고정 테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/high_angle/test_case.json) · [개별 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/high_angle/report.md) · [주 에이전트 재검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/high_angle/coordinator_pixel_review.json)

![하이 앵글 — 종이 보존 작업 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/high_angle/generated.png)

## 로우 앵글

시드 `14321191467143688212`, pack `482fc3c82b9776b0`, run `6cb6497278c7f7b2`.

철제 리브가 있는 유리 온실에서 아연 도금 작업대의 수직 앞면을 오른손 천으로 닦고, 왼손에는 별도 타월을 든 장면이다. 가까운 부츠가 크게 보이고 몸과 얼굴이 위쪽으로 후퇴한다. 턱 아래와 작업대 밑면, 머리 위 유리 지붕이 보이며 철제 기둥의 위쪽 수렴이 같은 시점을 뒷받침한다. 단순 전신 촬영·광각·화면 기울기와 구별되는 낮은 시점이다.

구도뿐 아니라 고정한 장면도 통과했다. 두 손의 천 역할, 작업대 앞면 접촉, 엇갈린 두 부츠의 바닥 지지, 전신과 지붕을 포함한 투영이 한 이미지에서 읽힌다. 천 옆의 반사와 세로 흐름 흔적을 렌더된 젖은 상태의 단서로 판단했다. 정지 이미지가 실제 습도나 시간에 따른 닦기 완료를 증명한다는 의미는 아니다.

전신 프레이밍, 창에서 실내로 이어지는 밝기 변화, 인물의 한쪽 배치 3개 후보를 채택했다. 프레임에 발 아래 여백과 머리 위 지붕을 함께 보존했고, 작업대의 사선이 손의 접촉과 공간 깊이를 연결한다. 몸·접촉 5개 항목도 모두 통과했다.

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/final_prompt_en.txt) · [고정 테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/test_case.json) · [개별 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/report.md) · [주 에이전트 재검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/coordinator_pixel_review.json)

![로우 앵글 — 온실 작업대 청소 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/generated.png)

## 동적인 구도

시드 `13179358549791421548`, pack `86fc1969557e7bec`, run `d7d1a19f5da1dc78`.

독립적으로 선택한 구도는 사선 깊이와 진행 방향의 비대칭 배치다. 젖은 강변 지하 통로에서 도면 통과 크로스백을 들고 낮은 턱을 넘는 도약으로 연출했다. 인물은 왼쪽에 있고 진행 방향 앞에 넓은 여백이 있다. 전경 턱·중간 인물·먼 출구가 깊이를 만들며, 기울어진 몸과 큰 보폭도 선명하다. 일반적인 동적 인상 기준 4개는 모두 통과했다.

그러나 정확한 required assertion은 3/5 통과에 그쳤다. 고정 문구는 바닥 이음선과 **전경 배수 턱이 모두 왼쪽 아래에서 오른쪽 위 출구로 이어질 것**을 요구한다. 실제 배수 턱은 반대 대각선으로 놓였다. 머리카락의 일부 흐름은 보이지만 가방 가장자리의 독립적인 흔들림 단서는 불명확하다. 다른 사선이나 달리는 자세로 이 두 필수 의미를 대체하지 않았다.

전체 장면도 실패했다. 도면 통을 든 손은 배우 기준 오른손으로 읽히는데 기준은 왼손이다. 뒤쪽 지지 발과 앞쪽으로 든 발도 고정한 왼발 지지·오른발 통과 관계와 반대로 읽힌다. 개별 에이전트는 얼굴과 재킷을 함께 가로지르는 정확한 따뜻한 빛 띠도 부족한 것으로 기록했다. 지지·균형과 접촉·공간 항목이 실패했다.

35mm 시점, 거리 범위 초점, 얼굴·손·소품 가시성 3개 후보를 채택해 인물과 공간을 한 프레임에 읽히게 했다. 실제 초점거리나 움직임 속도를 측정한 결과가 아니며, 후보 선택이 좌우 오류를 해결하지는 못했다.

주 에이전트는 최초 재검토에서 가방의 자세를 동세 단서로 판단했으나, 정확한 머리·가방 복합 문구를 다시 확인하면서 가방 가장자리의 독립적인 단서가 부족하다고 수정했다. [최초 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/coordinator_pixel_review.initial.json)을 보존했고, 고정 기준·원본·전체 실패 상태는 바꾸지 않았다.

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/final_prompt_en.txt) · [고정 테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/test_case.json) · [개별 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/report.md) · [주 에이전트 최종 재검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/coordinator_pixel_review.json)

![동적 구도 — 강변 지하 통로 도약 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/dynamic_composition/generated.png)

## 후보팩과 데이터 검증 범위

현재 dictionary hash는 `2f25dd52e76a52be07fd44f6b573259bbea7f39bae4ee6f9dda2071ba935baf4`다. 시각 인덱스 검사에서 960개 프로필·2,481개 exact term 바인딩이 통과했다. 이번 실험 중 운영 소스·데이터·인덱스 78개 파일은 시작 해시를 그대로 유지했다.

이번 신규 PC/PX 확장 후보는 compact catalog에 각각 4개·5개·6개 노출됐지만, 세 에이전트 모두 고정한 의미와 맞지 않는 후보를 거절했다. **이번에는 신규 PC/PX 후보나 선택형 시각 프로필·번들을 채택하지 않았다.** 각 구도의 필수 뜻은 후보 검색 전에 작성한 required typed assertion이 담당한다. 따라서 이 결과는 현재 후보팩 흐름을 사용한 구도 생성 테스트이며, 신규 16개 프로필의 추가 픽셀 자격 획득으로 계산하지 않는다. 후보팩 없이 만든 대조군이 없으므로 후보팩 자체의 인과적 개선 효과도 측정하지 않았다.

하이 앵글 pack에서는 `pigment dish`의 `dish`가 음식 도메인으로 노출되는 검색 혼동을 관찰했다. 에이전트는 음식·체형·성격·시점 변경 후보를 채택하지 않고 종이 작업 의미를 유지했다. 이 한 건을 검색 오염 관찰로 보존하며, 전체 검색 성능의 추정치로 일반화하지 않는다.

프롬프트·요청 감사는 각각 3/3 통과했다. 일부 candidate-pack 발견 단계의 미포괄 의도·품질 경고는 개별 기록에 남겨 두었고, 최종 문구에는 고정한 의미를 문자 그대로 보존했다. 전체 몸·접촉 판정은 12/15 통과지만, 모든 항목이 통과한 이미지는 로우 앵글 1개다. 판정 JSON 감사는 픽셀을 자동으로 읽는 기능이 아니므로 직접 관찰 근거와 구분했다. 사용자 판정이 pending인 로우 앵글의 감사 exit 1은 기술 실패가 아니며 JSON의 `technical_qualified: true`, 오류 없음이 실제 기술 결과다.

코드·데이터를 변경한 작업이 아니므로 이번에는 전체 저장소 회귀 검사를 실행하지 않았다. 이전 실험의 회귀 통과 수나 미완료 검사를 이번 이미지 실험 결과에 합산하지 않았다.

## 저장과 독립 읽기 검증

| 원본 | 크기 | SHA-256 |
|---|---:|---|
| 하이 앵글 | 1,237 × 1,272 | `1a8f9cf36313cda20de09cbb68ab4d440d52610996f43ee4353ed679e9c28e59` |
| 로우 앵글 | 1,024 × 1,536 | `97f8ec5f8c17f908c2ebb083084ee8f3d83c499f01f0ae5fcffee6a114a8ac84` |
| 동적 구도 | 1,448 × 1,086 | `8a0365d80e489f3db0960dcce54bf13c4f892abd3944dff51649dcb726e1779a` |

[최종 검증 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/verification.json)에 시드·pack/run ID·선택 후보·이미지 해시·크기·구도/장면/몸 판정을 모았다. [재확인 스크립트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/verify_saved_runs.py)는 이미지 생성 없이 다음을 확인한다.

- 운영 파일 78개와 생성 전 고정한 arm 파일 21개의 해시 유지.
- 참조 원본, 요청 봉투, 기준 프롬프트 문자열과 source request 일치.
- 각 1개 semantic v6 pack·ledger 1행·manifest의 pack/run/core/intent/reference 바인딩.
- 최종 선택한 후보가 실제 compact catalog에 노출되어 있었는지.
- 필수 의미 문구가 최종 프롬프트에 그대로 있는지와 실제 native 인자·감사 요청의 동일성.
- 도구가 반환한 원본과 저장된 PNG의 동일 SHA-256, 크기 및 픽셀 리뷰의 이미지 바인딩.
- 오류 없는 리뷰 스키마와 주 에이전트의 엄격 판정, 실제 실패 항목의 보존.

최종 저장 무결성 검증은 통과했다. 이 통과는 하이 앵글의 손 지지 오류나 동적 구도의 사선·좌우 오류를 통과로 변경하지 않는다.
