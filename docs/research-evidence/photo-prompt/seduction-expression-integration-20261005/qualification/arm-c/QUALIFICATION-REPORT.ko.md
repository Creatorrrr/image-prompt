# Arm C 독립 이미지 검증

**전체 판정: FAIL.** 이미지 생성은 성공했지만 고정한 11개 픽셀 게이트에서 PASS 4개, FAIL 2개, UNOBSERVABLE 5개가 나왔습니다. `partial_is_fail`에 따라 일부 형태가 보이는 것을 전체 성공으로 바꾸지 않았습니다. 사용자의 픽셀 수용 판단은 아직 없습니다.

독립적으로 고른 장면은 폐쇄된 시골 건널목 신호함 옆에서 케이블 시험 기록을 멈추고 카메라를 바라보는 성인 현장 기술자입니다. 다른 arm, 이전 프롬프트, 리서치 또는 후보를 보기 전에 세 가지 직접 작성한 장소·역할·사건 조합에서 `secrets.choice`로 선택했습니다. 원본 첨부는 보이는 얼굴·머리 외형에만 사용했고, 새 인물의 성인 나이와 역할은 agent-owned 설계입니다. 원 사진의 실제 나이, 정체성, 성격 또는 체형은 추정하지 않았습니다.

| 증거 층 | 결과 | 확인 범위 |
|---|---|---|
| 원본 요청 | 공통 bytes 일치 | requester envelope SHA 및 RAW equality 검증 |
| 초기 core·11 gates | 해시 유지 | 후보 접근 전 freeze, 사전 validator PASS |
| 현재 데이터 존재 | 4/4 | half-kneel, loop, broad, small corneal reflection 후보 존재 |
| 정상 v6 노출 | 1/4 | `core_bm25f`의 각막 반사 후보만 해당 target으로 노출 |
| 후보 선택 | 1/4 | `slot:light_shape:se_cornea_catchlight_without_wetness` 전체 관계 조건 채택 |
| 필수 시각 profile | 선택 0 | exact requester visual profile 및 opt-in 선택 없음; embodiment 5 gates만 active |
| 최종 문장 | 4/4 형태 서술 존재 | 3개는 독립 baseline에서 유지; 반사는 lamp→cornea와 iris/lid 경계로 정밀화 |
| compose/runtime 감사 | PASS / PASS | 정확한 prompt·negative·original reference bytes binding |
| native 이미지 호출 | 1회 성공 | CLI fallback 및 추가 호출 없음 |
| 원본 픽셀 | 전체 FAIL | PASS 4 / FAIL 2 / UNOBSERVABLE 5 |
| embodiment 리뷰 | technical qualification FAIL | 5개 중 support/balance와 visibility/projection 2개 실패, schema failures 0 |

후보에 반무릎 대신 `pv_retire`의 발레 자세, loop 대신 밝은 볼 삼각형 형태가 노출되었습니다. 해당 선택은 현재 시험 형태와 맞지 않아 채택하지 않았습니다. 정상 후보팩에서 loop/broad/half-kneel 후보가 실제로 노출·선택되지 않았으므로, 독립 baseline의 해당 문장을 데이터 반영 성공으로 돌릴 수 없습니다. 각막 반사 후보 선택도 그 profile의 전체 hard visual obligation을 자동 활성화하지 않습니다.

| 픽셀 게이트 | 결과 | 원본에서 관찰한 점 |
|---|---|---|
| C01 얼굴·머리 참고 | PASS | 짧은 어두운 bob, 분리된 fringe 및 보이는 얼굴 윤곽 관계 유지. 실제 신원·원본 나이 판단은 하지 않음 |
| C02 케이블 시험 사건 | UNOBSERVABLE | 신호함·meter·기록 카드·연필은 보이지만 meter-to-cabinet 연결 전체가 트레이/함 경계에 가려짐 |
| C03 actor-left 무릎 지지 | UNOBSERVABLE | 무릎과 pad의 접점은 보임. 덮인 hip-to-knee chain으로 정확한 좌우 소유 관계는 확정 못함 |
| C04 actor-right 앞발·정강이 | UNOBSERVABLE | 앞발 flat sole와 거의 수직 shin은 보임. actor-right라는 전체 명제를 확정 못함 |
| C05 actor-left 뒤쪽 forefoot·heel | UNOBSERVABLE | 뒤쪽 boot가 보이나 정확한 좌우 소유와 forefoot 접촉·heel lift를 동시에 확정 못함 |
| C06 지지 span·몸 방향 | UNOBSERVABLE | 일반적인 전경 자세/지지는 타당하게 보임. 지정한 좌우 leg chain 및 hip projection은 가려짐 |
| C07 카메라 기준 넓은 밝은 볼 | FAIL | 왼쪽 램프는 보이나 지정한 image-right 코 방향과 넓은 image-left 볼의 밝은 관계를 충족하지 않음 |
| C08 분리된 loop 코 그림자 | FAIL | 얼굴을 볼 해상도는 충분함. 어두운 볼 위 작은 oval nose-shadow와 cheek shadow 사이의 분리된 lit gap이 보이지 않음 |
| C09 두 눈의 작은 반사 | PASS | 각 iris에 작은 흰 반사점이 있고 iris/lid 경계를 구분할 수 있음 |
| C10 표정 | PASS | lens-directed eyes, 편안한 upper lids, 작게 벌어진 입이 동시에 보임 |
| C11 전신·얼굴 관찰 양립 | PASS | 머리·손·두 무릎·두 boots와 얼굴을 한 frame에서 볼 수 있음. 세부 관계 실패를 대체하지 않음 |

원본은 1236×1272 PNG이며 SHA-256은 `6bdb265cf1da487abf9421d96744306e5facf8ec692899442a9a02dc751f5812`입니다. native tool이 반환한 구체적 파일을 byte-identical로 복사했습니다. 편집, 보정, 재생성 또는 여러 이미지의 부분 합산은 하지 않았습니다. 실제 image model은 native tool에서 공개되지 않아 unknown으로 남겼습니다.

전체 사진은 푸른 dusk, amber 젖은 도로 반사, 열린 service cabinet, 작업 손과 카메라 응시를 일관되게 구성합니다. 이는 agent의 사진 인상 평가이며, 정확한 light/support 의미 성공이나 사용자 선호 판정이 아닙니다.

- [생성 원본 사본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/generated_images/rural-signal-native-attempt-1.png)
- [최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/final_prompt.txt)
- [원본 요청 envelope](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/request_envelope.json)
- [독립 초기 core](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/authorial_core.json)
- [고정 픽셀 게이트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/expected_gates.json)
- [정상 v6 후보팩](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/candidate_pack.json)
- [후보 존재·노출·선택 분리](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/source-exposure-selection.json)
- [compose 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/composed-audit.json)
- [runtime 입력](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/runtime_request.json)
- [runtime 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/runtime-audit.json)
- [11개 픽셀 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/agent-pixel-review.json)
- [embodiment 픽셀 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/embodiment-pixel-review-audit.json)
- [호출 ledger](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/image_runs.ndjson)
- [독립 실행 manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/run_manifest.json)
- [현재 source/index 해시 binding](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/postcore-source-binding.json)
- [검증 중 정리한 로컬 오류](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-c/verification-notes.json)

pack ID `c61c4f1646927b02`, canonical core `c250cb9e0dcb1379308e38f26ec2549302433562fe6ef0b518efff7fc5888636`, canonical intent lock `35acbc4b388832c931befb63690a7fd6a0e22d0ff916b230233f127403ee6e53`. 원본 요청/초기 파일 SHA와 generator가 정규화한 canonical SHA는 각각의 artifact에서 따로 기록했습니다. 추가 생성을 통해 이 실패 결과를 교체하지 않았습니다.
