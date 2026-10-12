# 7단계와 origin/main 통합 검증

7단계 커밋 `47d535d12ab80f1ae99c2f443af3f2846a891b6e`에 origin/main `0b33ae2c18a26060b918436c38d6d77eb2385306`을 pull하여 통합했다. 원격의 한글 라벨, 동물 분류, 임베딩 요청/응답 기록 기능과 7단계의 슬롯 검증 및 골렘 의미 데이터를 보존했다. 파생 semantic index 충돌은 합쳐진 source를 기준으로 재생성했다.

통합 중 참새 장면에 지렁이 subject 후보가 들어오는 회귀를 발견했다. 지렁이·개미·전기뱀장어 3개 source에 기존 primary context prerequisite 형식을 추가했다. 원격의 실제 동물 EN/KO 양성 검사와 인쇄물 음성 검사를 유지하고, 참새 EN/KO 음성 검사를 추가했다. source의 나머지 필드와 기존 테스트 메서드는 그대로다.

- 최종 generation: `5ef4af21887c41b6e890a84ed99da85b0ea5a10f7811202b0ad28656bb91f9ff`.
- 공개 후보 생성·뷰·원본 재계산 40건 통과. 후보 누락 변조 40건 탐지. native 표기 양성 10/10, 인접·제외 문맥 오탐 0/10.
- 필요한 후보 13/13 노출, 채택 가능 12/13. 초기 7단계의 subject 의미, authorial core, creative controls, negative, 후보 cap 유지.
- 최종 source에서 실제 receipt를 검증한 composed/runtime 감사 9건 통과. 48개 최종 프롬프트·negative·선택 ID는 7단계 검증본과 동일하다. 이전 generation의 전체 48건 감사는 역사적 증거이며 최종 source에서 48건을 다시 감사했다는 뜻은 아니다.
- 관련 테스트 60개 고유 selector의 마지막 실행 통과. 추가한 참새 테스트의 초기 setting 입력 오류 2건과 수정 후 통과 결과를 모두 보존했다.
- 합친 원본의 exact 조회 40,380/40,380, 슬롯 cap 내 40,148/40,380. prerequisite 수정 전후 문서·벡터·검색 metadata·코드가 모두 같음을 확인하여 전수 결과를 재사용했다.
- 임베딩 API와 이미지 생성 호출 0. 전체 테스트 suite와 실제 이미지 생성은 실행하지 않았다.

이 파일은 머지 커밋 직전의 통합 검증 기록이다. 푸시와 원본 checkout 보존의 최종 상태는 로컬 `DELIVERY.md`/`DELIVERY.json`에서 별도로 검증한다. 여기에는 요약·해시·로그를 담았고, 실제 candidate-pack/receipt/runtime-store 및 원본 백업은 로컬 검증 디렉터리에 보존했다.
