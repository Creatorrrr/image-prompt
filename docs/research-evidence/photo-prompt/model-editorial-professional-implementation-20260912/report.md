# 모델·에디토리얼 시각 의미 반영 및 독립 이미지 테스트

시각 의미 프로필 21개, 후보 항목 21개, 선택형 번들 11개를 런타임에 연결했다. 참조 사진으로 세 독립 에이전트가 서로 다른 복잡한 장면을 작성하고 각각 한 장씩 생성했다. **전체 장면의 엄격한 통과는 0/3이다. 신규 의미의 실제 노출·선택·픽셀 통과까지 확인한 것은 뷰티 디테일 프로필 1개이며, 그 3개 게이트는 모두 통과했다.** 의상·주얼리 신규 항목은 해당 팩에 노출되지 않아 이 두 이미지로 새 데이터 효과를 주장할 수 없다.

## 반영 범위

기초 리서치는 [사진 촬영 용어 조사 기반 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/report.md)와 그 출처 목록에 보존했다. 연구 단계의 24개 제안 중 한 장에서 판단할 수 있는 21개를 반영했다. 펼침면 중앙부, 룩북 컷 간 일관성, 서사 시퀀스 3개와 관련 번들 4개는 별도 레이아웃·연작 계약이 필요하므로 유지보수 기록에 보존했다.

- [후보 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_model_editorial_extension.json): 기존 슬롯에 후보 21개 및 선택형 번들 11개.

- [시각 의미 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_model_editorial.json): 프로필마다 관찰 구성요소 3개, 지정 대상·영역과 연결된 all-of 픽셀 게이트 3개.

- 기존 medium 3종(fashion_editorial, lookbook, campaign_photo)의 검색·표현 메타데이터를 강화했다. 기존 명칭·가중치는 보존했다.

- 일반적인 professional/model/editorial/campaign 명칭으로 직업·경력·출판 이력이나 특정 포즈를 하드 강제하지 않는다. 전체 관찰 관계를 직접 요청했거나 선택형 의미를 실제 채택했을 때만 해당 계약을 적용한다.

- 생성기에는 두 확장 파일의 로더 등록을 추가했다. 의미 인덱스는 8,553개 항목, 시각 프로필 인덱스는 587개 프로필·2,092개 exact term으로 재생성했다. 인덱스 빌더가 정리한 기존 tracked shard 48개는 HEAD의 원본 바이트로 복구했다.

| 프로필 | 내용 | 후보 슬롯 |
|---|---|---|
| `mep_casting_front` | 정면 캐스팅 기록 | `capture_context` |
| `mep_casting_profile` | 측면 캐스팅 기록 | `subject_framing` |
| `mep_casting_full_length` | 전신 캐스팅 기록 | `subject_framing` |
| `mep_garment_clearance` | 의상 핵심 디테일과 손의 분리 | `composition` |
| `mep_garment_side_depth` | 의상 옆선·두께 읽기 | `subject_framing` |
| `mep_garment_movement` | 움직임과 직물 지연 | `motion` |
| `mep_product_hero` | 제품 중심의 시각 위계 | `composition` |
| `mep_jewelry_contact` | 주얼리 착용 접점 | `contact_point` |
| `mep_beauty_detail` | 메이크업 디테일의 부위 소유권 | `composition` |
| `mep_hair_outline` | 헤어 볼륨과 외곽 분리 | `lighting` |
| `mep_cover_copy_space` | 표지 사진의 지정 문구 영역 | `composition` |
| `mep_environment_relation` | 인물 행동과 환경의 관계 | `capture_context` |
| `mep_graphic_pose` | 사지와 몸통의 그래픽 간격 | `body_pose` |
| `mep_gaze_target` | 시선 방향과 화면 내 목표 | `gaze_target` |
| `mep_poised_support` | 차분한 자세의 지지 관계 | `body_orientation` |
| `mep_in_between` | 동작 전환의 미완 상태 | `action` |
| `mep_surface_texture` | 피부·직물의 국소 질감 | `texture` |
| `mep_selective_imperfection` | 국소 흐트러짐과 정돈의 대비 | `composition` |
| `mep_visual_juxtaposition` | 지정한 두 요소의 병치 | `composition` |
| `mep_tether_review` | 테더 촬영 검토 장면 | `capture_context` |
| `mep_fitting_adjustment` | 의상 피팅의 실제 조정 | `action` |

## 테스트 방법

코디네이터가 원래 사용자 텍스트의 바이트를 보존한 요청 envelope를 먼저 고정했다. 세 에이전트는 공통 참조 사진과 절차만 받은 상태에서 각자 선택 풀·시드, 테스트 기준, 기본 프롬프트, 신체·접촉 검토를 작성했다. 이를 고정한 뒤에만 데이터와 후보팩을 조회했다. 각 에이전트는 다른 팔의 프롬프트·팩·이미지를 입력으로 쓰지 않았다고 기록했으며 별도 manifest와 ledger를 남겼다. 해시는 산출물의 일관성을 검증하지만, 독립성 선언 자체를 암호학적으로 입증하지는 않는다.

각 팔에서 candidate-pack v6 한 개와 native image_gen 이미지 한 개를 사용했다. 총 3회 생성했으며 재시도는 없었다. 실제 첨부 이미지 바이트는 세 런타임 감사에 연결됐다. 프롬프트·negative·참조 바이트 감사 후 생성했고, 에이전트별 저장 이미지 검토에 이어 부모가 세 파일을 직접 다시 검토했다.

| 항목 | A 의상 룩북 | B 뷰티 | C 주얼리 |
|---|---|---|
| 장면 무작위 시드 | 4078680847 | 2026091202 | 2026091203 |
| 신규 일반 후보 노출 | 0 | 0 | 0 |
| 신규 시각 프로필 노출·선택 | 0 / 0 | 1 / 1 | 0 / 0 |
| 신규 번들 노출 | 0 | 0 | 0 |
| 프롬프트·런타임 감사 | PASS / PASS | PASS / PASS | PASS / PASS |
| 형식화된 픽셀 게이트 | 신체 5/5 | 뷰티 3/3 + 신체 4/5 | 신체 2/5 |
| 사전 고정 전체 장면 | FAIL | FAIL | FAIL |
| 신규 데이터 효과 판정 | 미노출로 미검증 | 뷰티 1개 단일 이미지 실증 | 미노출로 미검증 |

A의 형식화된 감사가 technical_qualified로 나오는 것은 신체 5개 게이트만 평가하기 때문이다. 의복 의미 계약 자체는 선택되지 않았으며 사전 고정 보충 테스트에서 따뜻한 의복 반사가 실패했다. 이 보고서는 부분 감사 PASS를 전체 성공으로 올리지 않는다. ledger와 manifest의 success 역시 이미지 전달 성공이며, 시각적 자격 통과가 아니다.

## 저장 이미지와 직접 관찰

### A · 해안 여객터미널 의상 룩북

![A · 해안 여객터미널 의상 룩북](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-a/generated_images/cape-lookbook.png)

버건디 케이프의 넓은 앞면, 어깨 봉제선, 손으로 집은 옷자락, 전신과 부츠 지지는 보인다. 따뜻한 빛은 바닥·벽에 선명하지만 지정한 의복 가장자리에는 뚜렷하지 않다.

[팔별 보고서](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-a/arm-report.md) · [완성 프롬프트 및 채택 근거](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-a/composed_prompt.json) · [원본 크기 이미지](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-a/generated_images/cape-lookbook.png)

### B · 빗물 맺힌 루프톱 뷰티 에디토리얼

![B · 빗물 맺힌 루프톱 뷰티 에디토리얼](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-b/generated_images/beauty-editorial-20260912/image.png)

양쪽 위눈꺼풀의 구릿빛 쉬머와 입술의 플럼 색이 각 부위에 있다. 입술 윤곽과 피부 미세 질감도 구분된다. 손가락은 석재 상판 위에 놓이지 않고 전면 가장자리 아래로 드리워져 있으며 전완이 안쪽으로 모인다.

[팔별 보고서](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-b/arm-report.md) · [완성 프롬프트 및 채택 근거](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-b/composed_prompt.json) · [원본 크기 이미지](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-b/generated_images/beauty-editorial-20260912/image.png)

### C · 블루아워 천문대 주얼리 캠페인

![C · 블루아워 천문대 주얼리 캠페인](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-c/generated.png)

은색 커프와 초록 보석·베젤, 손목 소유권, 천문대 망원경과 푸른 창은 보인다. 커프는 트레이 테두리 아래에 있고 트레이는 낮은 가슴 높이까지 올라왔다. 받치는 손끝 일부는 겹쳐 숨고 열린 커프 끝도 확인되지 않는다. 얼굴이 제품보다 더 큰 시각적 비중을 차지한다.

[팔별 보고서](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-c/arm-report.md) · [완성 프롬프트 및 채택 근거](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-c/composed_prompt.json) · [원본 크기 이미지](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/model-editorial-three-arm-20260912/arm-c/generated.png)

## 노출 부족의 진단

[동결된 팩의 읽기 전용 진단](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912/exposure-diagnostics.json)에서 실제 새 슬롯·번들 노출은 세 팔 모두 0이었다. 의상·주얼리의 BM25F 단독 진단 순위는 각각 garment_clearance 30위, jewelry_contact 20위, product_hero 25위였다. 뷰티 프로필은 BM25F 단독으로 12위지만 최종 융합 팩에 노출되었다. 이 수치는 임베딩과 RRF의 실제 최종 순위를 재구성한 결과가 아니므로 BM25F만을 유일 원인으로 단정할 수 없다.

룩북 번들은 포즈·재질 변경 범위를 함께 요구하지만 A의 열린 범위에는 이들이 없다. 뷰티 번들은 appearance가 필요한데 B는 그 범위를 열지 않았다. 또한 묶음 자체의 구성원만으로 primary human context를 충족하지 못하는 문맥 조건이 있다. 따라서 현재 데이터가 로드된 것만으로 매번 번들이 나온다고 기대할 수 없다. 개별 슬롯 샘플러의 모든 필터 경로는 이 진단에서 재현하지 않았다.

이 결과에 맞춰 테스트 기준이나 기본 프롬프트를 사후 수정하지 않았다. 의미의 이름을 강제로 삽입하거나 노출·하드 활성화 경계를 완화하는 방식도 적용하지 않았다. 남은 과제는 동결 코어와 별도의 미사용 사례에서 검색 재현율·잘못된 노출을 함께 평가하고, 열린 변경 범위를 존중하는 번들 구성을 개선하는 것이다.

## 생성 이후의 검색 별칭 수정

전체 회귀에서 새로 생긴 실패 1개를 확인했다. 원래 holdout 문장 `An apparel catalog close-up shows an underarm gusset and reinforced seam`은 후보 없음이 정답인데, `Catalog`라는 넓은 paraphrase가 `mep_garment_side_depth`를 직접 노출했다. `Catalog`, `Lookbook`, `Garment-aware`를 이 한 프로필의 직접 paraphrase에서 제거했다. 일반 후보의 맥락 검색 키워드는 유지했으며, 원래 holdout의 문장과 기대값은 변경하지 않았다.

시각 프로필 인덱스를 재생성했고, 보강한 전용 회귀 9개 및 원래 실패 사례의 동일 검사 로직 재실행이 모두 통과했다. 다른 완료된 실패 항목들은 HEAD에서 재현됐다. 전체 회귀를 이 수정 뒤 다시 전부 실행한 것은 아니다.

세 이미지와 팩은 이 수정 전 소스 스냅샷에 속한다. 수정 이후 이미지를 다시 생성하지 않았다. 실제 선택된 뷰티 프로필의 픽셀 게이트, 필수 증거 필드 및 증거 조건은 최종 소스와 완전히 같음을 비교했다. [소스 버전 연결과 동일성 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912/source-version-lineage.json) · [별칭 수정 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912/post-render-alias-correction.json) · [원래 실패 사례 재검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912/post-correction-holdout.json)

## 검증 상태

- 최초 생성 시점의 신규 전용 회귀 8개 PASS: 전체 관계/부정/성인 문맥, 일반 이름의 비강제, 3개 all-of 증거, 누락·닫힌 범위의 번들 거부, BTS 문맥 가드, 연작 제외, 실제 인덱스 일치.

- 사전 메타데이터 검사, 장면 의미 감사, visual profile index --check, git diff --check PASS.

- 생성 시점 소스 기준 납품 무결성 30개 검사 PASS: 세 이미지·참조 해시, 코어·팩·manifest 연결, 단일 호출 ledger, 런타임 소스 불변, 감사 형식, 사용자 판단 미수신.

- 별칭 수정 전 스냅샷에서 전체 회귀 1164개를 발견했고, 80개 모듈 실행 및 시간 제한 후 표적 재개로 고유 1163개 테스트 실행을 완료했다. 완료된 unittest 요약에 기록된 결과: {'failures': 36, 'errors': 3}; 요약 출력 전에 중단된 로그에서 완료가 확인된 앞부분 실패 사례 2건은 별도 기록했다. 미완료 fixture의 부분 결과는 전체 실패 수로 합산하지 않았다. 전체 상태는 FAIL다. 최초 시간 제한 모듈은 ['tests.test_photo_prompt_contract_v2', 'tests.test_photo_visual_obligations']이며 재개 완료 모듈은 ['tests.test_photo_prompt_contract_v2']이다. 현재 실패 항목이 수정 전 HEAD에서도 재현됐는지: False. 비교는 실패 항목 기준이며 모든 출력 동일성이나 회귀가 전혀 없음을 증명하지 않는다. 추가 제한: ['tests.test_photo_visual_obligations.PhotoVisualObligationTests.test_registry_and_request_scoped_routing_fixture']는 현재 코드와 HEAD 모두 시간 제한 내 전체 fixture 순회를 끝내지 못했다. 나머지 시각 의무 메서드는 완료된 앞부분 로그와 별도 후반부 실행으로 확인했다. 완료 수는 전체 1,164개 통과나 완료를 뜻하지 않는다. 최초 완료된 실패 비교의 HEAD 재현 여부는 False다. 차이는 후속 수정한 Catalog 오노출 사례이며, 그 사례를 제외한 완료된 실패 항목의 HEAD 재현 여부는 True다.

[전용 회귀 로그](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912/focused-tests.log) · [전체 회귀 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912/full-suite/summary.json) · [수정 전 HEAD 비교](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912/head-comparison/summary.json) · [납품 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912/delivery-validation.json) · [부모 픽셀 검토](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912/parent-pixel-review.json)

## 판단 범위와 남은 사항

3개 사례의 실패는 숨기지 않고 보존했다. 뷰티 한 이미지에서 새 프로필의 조건이 보인다는 것은 데이터가 성공을 유발했다는 인과 증거가 아니다. 수정 전·후 동일 조건 이미지 비교는 없으며, 새 프로필 21개 중 20개는 생성 이미지의 선택 계약으로 시험되지 않았다. 최초 리서치의 46개 설계 사례도 이번에 모두 실행된 것으로 바꾸지 않았다.

시각 의미·후보팩 반영과 요청한 세 독립 생성·검토 작업은 완료했다. 자동 노출의 충분성, 모든 새 키워드의 신뢰도, 사용자 미적 선호까지 통과한 상태는 아니다. 사용자 판단은 not_yet_received로 유지한다. 커밋·푸시·외부 게시는 수행하지 않았다.
