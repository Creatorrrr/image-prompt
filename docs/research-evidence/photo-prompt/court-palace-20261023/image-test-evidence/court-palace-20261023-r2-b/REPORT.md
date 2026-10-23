# B arm — 유럽 궁정 음악 살롱

실제 참조사진 첨부 내장 image_gen **1회**가 반환·저장됐습니다. 관리 신체검증은 **5/5 PASS**, R2V13의 사전 정의한 source test는 **3 PASS / 1 FAIL**, **whole-case FAIL**입니다. 사용자 수용은 pending이며 추가 생성은 없습니다.

## 결과와 판정

- 원본 복사본: [royal-music-salon-r2-b.png](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-b/images/royal-music-salon-r2-b.png) — 1312×1199, SHA256 `d96d5f40de246b6a6065b492064764a7e9d27e3afd585ed94e25b988e82745a0`. 반환 경로에서 바이트 그대로 복사했습니다.
- 양팔과 오른손 건반·왼손 악보 접촉, 벤치의 좌석 지지는 관찰됩니다. 발·하체 전체, 소리, 실제 신원·품계·역사적 진위는 확인하지 않습니다.
- R2V13의 브레이드 조직, 끝에 연결된 술머리, 자유 낱실은 원본에서 보입니다. 다만 장식이 **지정한 왼쪽 악보 소매가 아닌 오른쪽 건반 소매**에 있습니다. 사전에 정한 owner/side gate를 바꾸지 않고 실패로 남겼습니다.
- 원래 bounded source는 좌우를 정하지 않으므로 일반적인 의복 가장자리 장식은 관찰되지만, 이 시험의 구체적 소매 배치까지 충족했다는 주장은 하지 않습니다. `native_approval:false`이며 native chosen 배열은 둘 다 `[]`입니다.

## 자연 노출과 직접 시험 경로

고정한 location/wardrobe_style + request-topic/baseline의 **4개 일반 검색**에서 32 occurrence / 32 unique source를 전부 읽고 조건·효과·대안을 검토했습니다. **이번 R2 신규 모듈의 자연 노출은 0건**입니다. R2V13은 coordinator가 제공한 authoritative source를 별도 postcore로 검토해 전달한 직접 시험입니다. 자연 노출 성과나 native whole-source 채택으로 집계하지 않습니다.

직접 후보 standalone 대안 6개와 일반 검색 standalone 대안 6개를 같은 controls로 비교했습니다. 새 배우나 tabletop 소품 없이 복식의 작은 연결관계를 시험할 수 있어 D13 cuff braid를 선택했습니다. [전체 비교](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-b/composition-comparison.md) · [반환 source 전원 검토](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-b/returned-source-reviews.json) · [R2V13 픽셀 검토](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-b/source-specific-pixel-review.json).

## 실행·해시

| 항목 | 값 |
|---|---|
| H2 pin | `265a75945bda1a1aea3b26ca88e13ab0dcb3139d22ae85197ed2d478ee3f2978` |
| native pin | `eeaafc1952af220bd23823e72fcd1b1fadca8048f8ac334e08e7edbb25705d9a` |
| core canonical SHA | `ba2097eed0238f146baeeab1050e2a86e3b08e0bbb8a08d8a08df16ca50041b2` |
| baseline exact text SHA | `e4a615263d08161df60f34a84eefe8ebf613e1a822c4a051ed562561a03a0aa4` |
| final_prompt_en.txt 파일 SHA | `013dc0c803393b5f45a4dbe0d59ab40933e3812145218c5e066deecfa748b33e` |
| strip/runtime 텍스트 SHA | `7092426f0ddfb980d15f53760c8c5623f6e0b9311f573ba4eb56e015234c0fb1` |
| 참조 이미지 SHA | `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7` |
| ledger run_id | `8f4a0044948e8e54` |

최종 텍스트 파일에는 마지막 개행이 있어 파일 SHA와 `strip`한 실행 텍스트 SHA가 다릅니다. 별도 runtime_prompt_en.txt는 감사된 실행 문자열을 개행 추가 없이 보존합니다. 참조사진은 얼굴·머리 외형 guidance로 실제 view_image에서 보고 동일 파일을 referenced_image_paths로 첨부했습니다. 관측된 모델명은 제공되지 않아 null입니다.

Compose/runtime/native-plan 검사는 통과했고, 동일 reservation의 native-started 검사가 shell session으로 지연됐을 때 이미지 호출 전에 저널을 재확인했습니다. 새 reservation이나 native-started 재발행 없이 저장 plan으로 **이미지 도구 1회**만 호출했습니다.

[Ledger](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-b/image_runs.ndjson) · [사실 기반 manifest](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-b/arm-manifest.json) · [관리 review audit](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-b/review-audit-output.json) · [전체 구조화 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-b/arm-report.json).

## 독립성 경계

기본 controls(sensual1/fetish0/surreal0/creativity1), baseline/core, 중립 feature/embodiment와 slot plan은 후보·연구 접근 전에 독립 고정했습니다. 그 뒤 상태 조회 도구가 과거 arm의 최종 요약까지 반환해 비의도적 노출이 있었습니다. 사전 고정의 독립성은 유지하지만 postcore까지 완전 미노출이었다고 주장하지 않습니다. 이후 다른 arm을 다시 조회하지 않았으며 [노출 기록](/Users/chasoik/Projects/image-prompt/generated/photo-runs/court-palace-20261023-r2-b/postfreeze-exposure-note.json)을 보존했습니다. 이 fresh matrix를 이전 결과 대비 paired improvement로 해석하지 않습니다.
