# Native v3 계약과 runtime 통합 검증

후보의 실제 효과, 전제, 보존, 맥락을 구별하고 전체 원문·실제 선택지·참조 폐쇄를 결속하는 계약을 구현했다. 슬롯 태그와 효과 범위를 자동 추론하지 않는다. 부분 속성 잠금에는 같은 실제 소유자의 보호된 속성만 frozen 사실로 사용할 수 있다. 복합 후보는 부모 자체 의무를 유지하며 실제 선택한 자식만 추가한다. member의 concept_units/relations는 적용 조건과 구별하고 실제 자식 사실 및 최종 프롬프트의 문자 근거를 요구한다.

직접 작성한 fixture 검증은 루트가 독립 재실행했다. 196회 실행, 166개 고유 테스트, 358개 하위 사례가 통과했다. 네트워크를 OS에서 거부했고 provider 키를 제거했다. 기존 projection worker가 기록한 중간 통합 실패는 이후 최종 suite에서 모두 해소됐다. 제품 지침은 skill-creator 지침에 따라 후보와 독립적인 owner/fact 계약을 precore 문서로 분리했고 전용 venv의 quick_validate를 통과했다.

실제 canonical source 18,250개, positive 18,180개, catalog 139개는 변경하지 않았다. 동일 모델·revision·전체 텍스트·recipe·768차원을 대조하여 벡터 18,180개를 재사용했다. 빌더의 embed/embed_many를 호출 즉시 실패하도록 고정한 상태에서 전체 인덱스 검증, runtime publication, RuntimeSnapshotProvider.acquire 및 실제 payload의 source 일치를 확인했다. 새 임베딩·Gemini 호출은 0이다. 실제 publication generation은 c74a576ceca0f72b6f2c529640d708268068763b76ae44646c613de69a02719b이다.

이는 실행 계약과 fixture 통합 완료 증거다. 운영 후보 native 자격화는 0개이며 전수 의미 승인, catalog 141 제안 적용, 실제 frozen-core hybrid 검색, 단계 6–8 완료를 주장하지 않는다. 미자격 원문은 검색 발견용으로만 남고 최종 채택은 거부한다. source/member binding-ID 경로 제거와 조건의 명시 이관은 단계 6–8에서 수행한다.

정확한 실행값은 NATIVE-V3-ROOT-TEST-VERIFICATION.json, native-v3-runtime-01/PREFLIGHT.json 및 VERIFICATION.json에 보존했다. worker hash manifest 이후 루트가 workflow 문서에 실제 selected member literal evidence 안내만 추가했다. 이전 guide/fixture는 역사 증빙으로 보존했고 최종 계약은 compound-and-partial-lock supplement가 명시한다.
