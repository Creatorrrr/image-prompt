Arm a의 최초 이미지 1장 생성과 원본 픽셀 리뷰를 완료했습니다. 코트 옆 공기 틈(WK008)은 실패, 동일 가방의 두 연결부 지지(WK080)는 통과했습니다. 전체 파생 hard-gate 7개는 통과 3개·실패 4개로 픽셀 자격은 FAIL입니다.

여객선 대합실에서 함께 짐 잠금장치를 다루는 상황, 소재 표면과 지역 색상, 스카프 두 꼬리 및 시계 소유 관계는 읽힙니다. 집중한 얼굴과 작은 미소, 공유 행동이 따뜻한 여행 사진을 만들지만, 코트 옆 틈과 버클 혀를 하우징으로 넣는 정확한 접합 동작은 확인되지 않습니다. 한 발이 들린 교차 다리 자세도 최종 검토된 두 발 바닥 지지 상태와 다릅니다.

| 검증 층 | 결과 |
| --- | --- |
| Prompt audit | PASS, quality WARN 4개: 최소 requester anchor를 자유 서술·assertion으로 보존 |
| Runtime text/reference audit | PASS |
| 리뷰 기록 유효성 | PASS |
| WK008 전체 관계 | FAIL: 몸통 옆 패널의 독립 공기 틈이 가려짐 |
| WK080 전체 관계 | PASS: 동일 가방 양쪽 연결부와 스트랩 가지가 보임 |
| 전체 픽셀 hard-gate | 3 PASS / 4 FAIL, technical qualification FAIL |
| 원장·manifest 무결성 | PASS, 공식 recorder 단일 행·첫 기록에 독립 metadata 포함 |
| 전체 상황·미학 | 공유 도움과 출항 맥락이 읽히며 은근한 얼굴 중심 매력 유지 |
| 사용자 수용 | PENDING, 비교 렌더 없음 |

내장 image_gen 생성은 정확히 1회이며 수리 렌더·API fallback은 0회입니다. 실제 모델명은 도구가 반환하지 않았습니다. 원본 1237×1272 픽셀과 byte-identical 복사본을 보존했습니다. 조회는 최초 진단 1 pack과 동일 frozen 입력의 requalification 1 pack, 총 2회이며 최초 pack은 최종 구성에 재사용하지 않았습니다. 새 qualification pack에 신규 ordinary 1개·bundle 0개·visual concept 3개가 노출됐습니다. WK008/WK080을 선택했고 WK006 조끼와 WK077 샌들은 얼굴·손·코트·가방 구성을 유지하려는 미학적 판단으로 거절했습니다.

형식 오류(0 강도 축 누락, null 사용자 판단), 로컬 준비 오류(메타데이터 출력 잘림, PIL 부재 및 미생성 복사 경로), 최종 prompt 내보내기의 추가 개행과 보고 helper의 중첩 필드 접근 오류를 모두 보존했습니다. metadata·로컬 복사·텍스트 내보내기·보고 helper만 보완했으며 실제 생성 prompt·이미지·gate 판정은 바꾸지 않았습니다. 현재 도구나 스키마 때문에 막힌 항목은 없습니다.

- [이미지](images/ferry-waiting-room-native-01.png)
- [최종 positive prompt](final_prompt.txt) · [실제 호출 prompt](runtime_prompt_exact.txt)
- [전체 상세 보고](final_report.json) · [원본 픽셀 판정](native_pixel_review_02.json)
- [원장](image_runs.ndjson) · [공식 manifest](run_manifest.json) · [최종 무결성 검사](final_integrity_check.json)

Core SHA256: `1239b6a1477a4ef455c9e8d6094dc2a447918f4935be640b7449bd69161dcb25`

Qualification generation: `c68a7d2e44db608a6372800dae6f51dc99ca907bfb561e6e5c8fd05aae262f14`

Image SHA256: `d248ec57c0347300b72ea93634d0c62b8d302a8841bc064e2dcbd3f1698d1353`
