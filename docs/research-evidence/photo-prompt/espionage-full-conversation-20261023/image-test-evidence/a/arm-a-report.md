# Arm A: 첩보물 재검증 — FAIL

원본 JPEG를 실제 첨부한 native imagegen 1회 생성에 성공했다. 실제 저장·원장·독립 manifest와 compose/runtime audit는 완료됐고, 픽셀 판정은 FAIL이다. 사용자 수용은 pending이다.

랜덤 선택은 폐관 자료실 서비스 계단에서 봉투를 확인하는 귀환 장면(archive_stair_return)이다. 계단·봉투·옷의 위치와 손상은 작가 선택이며 실제 임무, 원인, 신원·나이 또는 연혁의 증거가 아니다. 초기 freeze는 자료를 읽기 전에 마쳤고, 옷 상태가 사용자 hard lock으로 넓어지지 않도록 이미지·검색 전 managed-v2로 소유권만 좁혀 재freeze했다. 이전 frozen 자료도 보존했다.

## 결과 파일

- 생성 원본: `/Users/chasoik/.codex/generated_images/01a16923-4035-7eb0-bce7-c3d8f6d69b14/exec-eae080c2-0128-41ea-83ad-75aa0a4116e4.png`
- 동일 바이트 복사본: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/espionage-full-20261023-a/managed-v2/result.png`
- 이미지 SHA256: `6a9a08c4f5b56b59b90dfc9c0198c2d16b94616a5ffd627c8bc91a7cb7fa7d5f` (1024×1536)
- 최종 literal prompt: `managed-v2/final_prompt.txt`
- 전체 비교: `managed-v2/composition-comparison.md`
- 모든 source 검토: `managed-v2/source-reviews.authored.json`
- 모든 component/endpoints 판정: `managed-v2/pixel-test-result.json`
- 원장: `image_runs.ndjson` (1행), manifest: `run_manifest.json`
- 모든 경로·해시·gate·감사 binding: `arm-a-final.json`

## 후보 반영 계층

고정 generation은 `607f27b10495bfaad80edd62ec932b863fb8365098ea90e4cb3b694ec656fa25`, 실행 store는 `/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed`이다. 역할 3개(texture, surface_moisture, narrative_clue)와 whole-scene 2개를 독립 검색해 40 occurrences/39 unique sources를 전부 읽고 각각 CID/RID/source hash 결정을 기록했다.

신규 `cand_d5edfac258ee57d097318c5437b07269`가 texture에 노출됐다. 이 source는 벌어진 ragged coat edges 두 개와 틈 사이 온전한 opaque lining의 완전한 관계를 요구한다. `native_approval=false`이며 실제로 미채택했다. 이 source의 literal final evidence와 픽셀 성공 증거는 없다. 독립 초안의 헤진 cuff를 신규 tear/lining source의 성공으로 바꾸어 부르지 않았다.

기존 `cand_d1e9e34418165e99b21cc1e5dc59a8e5`에서는 일반적인 가림 감소에만 inspiration_only를 기록했다. source의 seam/closure-length 전체 cue는 채택하지 않았고, independently justified composition으로 봉투와 테스트할 옷 표면을 분리했다. B0·door dust 안·ALT-CLEAR를 완전한 프롬프트로 비교하고 ALT-CLEAR를 선택했다. native chosen CID와 visual concept 목록은 모두 빈 배열이다.

## 직접 본 픽셀

| Gate | 판정 | 근거 |
|---|---|---|
| cuff 천→헤진 경계→붙은 실밥 | PASS | 실 끝이 동일 cuff 경계에서 이어지고 온전한 sleeve 천과 함께 보임 |
| 앞판→diagonal ridge→dark trough | FAIL / partial | 옷 앞판의 밝은 대각선은 마모·오염 무늬와 구분되는 단일 ridge/trough를 입증하지 못함 |
| 동일 코트→젖은 부분→물방울 | PASS | 하단 panel의 실제 물방울과 국소 어두운 젖은 점들이 더 마른 위쪽 천과 구분됨 |
| 라펠 경계→닳은 패치→인접 정상 천 | PASS | 밝은 닳은 가장자리와 바로 옆의 어두운 온전한 천이 함께 보임 |
| 인물·코트·봉투·서비스 계단 | PASS, 해석 제한 | 닫힌 문 옆에서 아래 계단을 의식하는 한 프레임의 pause가 성립함. 실제 첩보원·임무를 증명하지 않음 |

Native 원본과 원본 해상도 그대로 자른 hands/coat 검토 crop을 직접 봤다. Embodiment 5개 중 ownership/reach/balance/visibility는 PASS, contact-and-space는 FAIL이다. 이미지 왼쪽의 인물 오른손 엄지는 sealed flap 아래를 받치고 있어, 계획했던 right thumb→sealed flap 접촉의 역할이 그대로 살아남지 않았다. 인체 기형이라고 진단하지 않고 구체적인 손/대상 역할 불일치로 기록했다.

전체 장면은 얼굴·봉투·문·계단·코트가 연결되어 긴장 있는 귀환 장면으로 읽히며, 참조의 bob/bangs와 얼굴 외관을 안내 수준으로 반영했다. 다만 대각선 wear 무늬가 crease relief를 대신했고 봉투 동작이 두 손의 hold로 바뀌었다. 좋은 전체 인상은 개별 실패를 상쇄하지 않는다. `partial_is_fail` 및 `UNOBSERVABLE_NOT_PASS`를 유지했다.

## 감사와 호출

- Compose PASS, runtime PASS, native plan/start fresh audit PASS.
- 원본 JPEG의 경로와 SHA가 exact payload의 `referenced_image_paths` 및 reference record에 실제 포함됐다.
- 실제 native 1회, 추가 이미지·재시도·대체모델 0회. native tool이 image model 식별자는 반환하지 않아 observed model은 unknown이다.
- 원장/manifest 저장 완료. manifest의 success는 호출·저장 성공이며 픽셀 qualification과 별개다.
- Review audit PASS(record_valid=true), technical_qualification=fail, 사용자 판단 pending.
- 최초 review가 run copy의 경로를 사용해 observed attempt path binding에서 거부된 기록을 보존하고, 동일 SHA의 정확한 tool 원본 경로로만 recovery_only 수정했다. 판단·픽셀·생성은 바꾸지 않았다.

스킬 SHA `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`. 다른 arm의 prompt·후보·이미지·결과를 사용하지 않았다. 최종 전체 판정은 FAIL이며 추가 생성 없이 종료한다.
