# B안 이미지 검증 결과

독립 실험 판정은 **FAIL**입니다. 네이티브 이미지 생성은 승인된 1회를 사용해 성공했고, 1536×1024 원본을 공용 generated 경로에 바이트 동일하게 보존했습니다. 외형 참조와 장면 맥락은 보이지만, 동결한 기계 관계 6개 중 2개만 통과했습니다.

- 원본: `/Users/chasoik/Projects/image-prompt/generated/images/clockpunk-20261023-independent-b/original.png`
- 원본 SHA256: `6dee71f150004429b57c11496daab7caca87e38e678485f8edc5858249b78d94`
- 최종 프롬프트: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/arm-b/final-prompt.txt`
- 프롬프트 SHA256: `c761af323de935cf3a3b6ea23637bd0092ce50511904da9f684aa5e92b429428`
- 네이티브 기록: `457b0f4314d039ec`, 모델명은 도구 응답에서 확인되지 않았습니다.

| 기준 | 판정 | 관찰 |
|---|---|---|
| B-R1 추→줄→드럼 | FAIL / partial | 줄과 드럼, 추는 보이나 추 하단이 잘려 완전한 자유 매달림 상태를 관찰할 수 없음 |
| B-R2 드럼→맞물린 기어열 | FAIL / visible | 같은 축의 바퀴들이 떨어져 있어 톱니가 맞물리지 않음 |
| B-R3 피니언→랙→배 표식 | FAIL / visible | 아래 피니언과 위 노선표 랙 사이에 명확한 간격이 있음 |
| B-R4 탈진기→레버→진자 | FAIL / partial | 부품은 보이나 접점과 진자까지의 연속 링크를 추적할 수 없음 |
| B-R5 사람→키/프레임 접촉 | PASS / visible | 한 손의 분리된 감기 키와 반대 손의 외곽 프레임 접촉이 읽힘 |
| B-R6 노선표→실제 운하 배 | PASS / visible | 작은 표식과 뒤의 실물 여객선, 정박장 깊이 관계가 구별됨 |
| B-A1 얼굴·머리 참조 | PASS / visible | 짧은 검은 단발과 가는 앞머리, 얼굴 인상에 참조 단서가 보임. 실제 신원·나이·정확한 동일성 판정은 아님 |

후보 검색은 지정 H-F2 `1357d4e9171988e46ea9825a2ce4bed4afdd875ca4e29cb24c3f93c02ceaa608`에 묶였습니다. 5개 검색에서 24개 고유 자료/24개 occurrence를 모두 검토했습니다. contact_point와 object_structure는 각각 0개, spatial_depth·주제·baseline은 각각 8개였습니다. Clockpunk 세계 설정 CID `cand_cb1f8a7534d15030b51f6652cf24295e`가 노출됐지만, 이미 독립 baseline에 있던 추·기어·탈진기를 데이터 기여로 세지 않았고 자동인형 캠까지 포함한 전체 소스도 채택하지 않았습니다. 새 상세 Clockpunk 연구 카드 본문은 이번 표본에 노출되지 않았습니다. 최종 반영은 일반적인 수평 구도 자료 1개뿐이며, whole native adoption은 0개입니다. 따라서 이 이미지는 새 상세 카드의 효과를 입증하지 않습니다.

구성·런타임 감사는 PASS였습니다. 파생된 관리형 이미지 게이트는 신체 관계 5개이며, 이것이 위의 별도 기계 실험을 대신하지 않습니다. 관리형 검토 감사도 record_valid=true, technical_qualification=pass로 완료됐습니다. 이 결과는 신체 관계 5개에 한정되며, 기계 관계 실험의 FAIL은 그대로입니다.

저장 보조 코드의 PIL 누락은 이미 반환된 같은 PNG의 헤더 확인과 바이트 복사로 복구했습니다. 재생성·API fallback·moderation retry는 없었습니다. 참조 JPEG 경로와 SHA는 실제 native payload 및 manifest에 남겼습니다.

전체 인상은 따뜻한 장인 작업·여행 장면으로 설득력이 있습니다. 다만 뒤 여객선의 굴뚝과 연기는 산업적 증기선 단서를 추가하며, 기계 인과 구조는 장식적 인상에 머뭅니다. 사용자 선호와 수락은 pending입니다.

관리형 `technical_qualification=pass`의 정확한 범위는 `photo-embodiment-preflight/v1`의 신체 소유·도달·지지·접촉·신체 투영 5개입니다. 이번 run에는 상세 Clockpunk source/profile의 whole adoption이 없어 기어열·랙·탈진기의 기계 연결 의무가 그 관리형 체크리스트에 포함되지 않았습니다. 별도로 선동결한 B-R1~B-R6가 그 연결을 검사하며, 이 실험의 FAIL이 최종 전달 판정입니다. 두 결과를 의도적으로 맞추거나 기계 실패를 기술 성공으로 부르지 않습니다.
