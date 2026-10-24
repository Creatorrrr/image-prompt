# 독립 재시험 C

C는 병영 출입문에서 청소가 다시 더러워지는 환경적 풍자를 만들었습니다. 실제 imagegen 호출은 1회이며, 최종 원본은 whole contract **FAIL**입니다.

- 원본: /Users/chasoik/Projects/image-prompt/generated/photo-runs/marine-literature-retest-20261024-c-v5/original.png
- 정확한 최종 프롬프트: /Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/c/v5/final-prompt.txt
- 프롬프트 SHA256: 961934ae2c5c1729c24b2876c6267ea50f56ca255cff41e5349f37b101bcd253
- 원본 SHA256: 0e0bb7788225af92fadffc3f44280a63a9c10f2007d0c8f859608b79ae7cb096

최종 v5는 처음 후보를 보기 전에 쓴 baseline·controls seed·사전 게이트·slot query 문자를 그대로 유지한 처리 보정입니다. v4의 `해병문학 용어 조사`를 실제 이전 사용자 메시지의 정확한 주제 `해병문학`으로 좁혔으며, 새 blind 저술시험으로 주장하지 않습니다.

5개 query의 40개 발급 occurrence / 36개 source 전체를 읽고 baseline과 6개 완성 대안을 비교했습니다. 새 87개 visual source는 contact rank-window에 2개, topic에 1개, baseline에 1개 들어왔지만 uniform 8/32 최종 sample에는 0개였습니다. 따라서 신규 해병 데이터의 최종 prompt·tool·pixel 전이는 **미실현**입니다. 새 seed를 고르거나 CID를 강제로 넣지 않았습니다. 이전 v4에서 읽은 V014의 단추 속성도 v5에 발급되지 않았으므로 사용하지 않았습니다.

기존 source의 일반적인 발밑 국소 음영만 최종 문구에 남겼습니다. 복도·군복처럼 보이는 작업복·걸레·발자국·문턱은 독립 baseline에 먼저 있었고, 전신 프레임 보완도 후보 검색 전에 확인한 지지면 가시성 문제에서 나왔습니다. 이것들을 신규 데이터 반영으로 세지 않습니다.

원본에는 참조의 어두운 보브·성긴 앞머리·큰 갈색 눈·부드러운 얼굴형이 관찰되며, 주인공의 손→자루→걸레머리→바닥과 양발 지지는 보입니다. 그러나 도착자의 두 번째 발과 바깥 계단 지지점이 화면 밖입니다. 한 발만 보인 상태를 두 발 전체 관계의 PASS로 바꾸지 않았습니다. managed embodiment는 소유/관절 연결 2 PASS, 지지/접촉/가시성 3 FAIL이며, 사전 whole 관계도 FAIL입니다. 사용자 수락은 pending이고 실제 응답 모델 ID는 unknown입니다.

기록 과정에서 원래 native-result 명령에 SKILL SHA를 잘못 하드코딩한 오류가 있습니다. 원본 ledger·manifest·operation은 보존했고, `metadata-correction.append.json`에 원본 row hash, 잘못된 값, 실제 파일 경로와 실측 SHA/UTC 시각을 명시했습니다. 별도의 corrected-metadata ledger는 같은 실제 operation을 재기록한 사본이며 추가 이미지나 추가 성공 시도가 아닙니다. native 검증이 원래 잘못된 메타를 검증했다고 주장하지 않습니다.

전체 근거: /Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/c/v5/report.json
비교와 source별 판단: /Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/c/v5/composition-comparison.md
원본 픽셀 판정: /Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/c/v5/pixel-review.json
메타데이터 명시적 보정: /Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/marine-literature-20261024/retest-20261024/c/v5/metadata-correction.append.json
