# Scoped source publication to main

2026-10-22. 게시 기준은 `66feb49d8d3b58b8f2ad0f4118efb2a499922a7c`이며, 다른 작업의 미커밋 변경을 포함하지 않는 독립 source/index 구성을 검증했다.

|항목|게시 기준 main + 이번 변경|기존 로컬 생성 실험 환경|
|---|---|---|
|전체 source 후보|19,076|19,275|
|긍정 source 후보|18,864|19,029|
|진단 source 후보|212|246|
|binding|13,004|13,328|
|이번 추가|84 긍정 + 12 진단, 168 binding|동일|
|source/index 범위|기준 main의 모든 source + 이번 genre-fusion 추가|다른 미커밋 source/코드도 포함한 로컬 실험 snapshot|

차이는 이번 카드의 누락이 아니다. 기준 main의 SCP 재사용 모듈을 포함한 기존 후보 18,980개와 binding 12,836개, catalog, policy를 보존했다. 이번 96개 CID와 source 내용은 로컬 실험에서 반영한 원문과 같다. 다른 미커밋 cosmic 데이터, 기존 후보의 수정, 스킬/엔진 코드는 이 커밋에 넣지 않았다.

## 게시용 검증

- Source SHA-256: `8028317dd1ec66fbd8d5c72f393fa9285d9f4502159eb130d72c4bf3278578c1`
- Lazy index layout: `fe49822afa10799d088aeb41e7c71d6e903147704115e4ba21030fac7f7c2338`
- 전체 source/index closure 검증 PASS; dictionary 오류 0개.
- 관련 회귀 테스트 97개 PASS.
- 정확히 일치하는 기존 문서 벡터 18,850개 재사용; 나머지 14개는 로컬 EmbeddingGemma로 생성. 외부 embedding API 호출 없음.
- 기존 source, binding, catalog, policy의 의미와 기존 source module 바이트를 보존했다.
- `retrieval-runtime.json`과 native CURRENT를 변경하지 않는다. 게시용 source/index 갱신과 installed release 활성화는 별개다.

기준 main의 installed 설정은 H-F2 `13d885356aa63c72ec29b0409e8cce23469b3cbc0f9c0adbaf840ff7584d70db`를 유지한다. 로컬 세 장의 생성 실험은 기존 보고서대로 `428446b6ed22975dedacde13ce29fe2d0d4b2de8991442e84eda59553410e184`에서 실행됐다. 그 로컬 설정과 생성 이미지, 원본 ledger는 기본 체크아웃에 보존하며 이 source 게시로 덮지 않는다.

임시 워크트리의 첫 dictionary 검사는 gitignore 대상인 로컬 모델이 없어 실행할 수 없었다. 기존 lock과 정확히 같은 모델 파일을 독립 복사하고 기존 bound Python에 연결한 뒤, 같은 워크트리의 코드와 검증 규칙으로 재실행해 통과했다. 네트워크 다운로드, 모델 변경, 검증 규칙 완화는 없었다. 임시 모델 복사본은 기본 체크아웃에 같은 바이트가 있어 워크트리 정리로 고유 파일이 사라지지 않는다.

[INTEGRATION-RESULTS.md](INTEGRATION-RESULTS.md), [IMAGE-TEST-RESULTS.json](IMAGE-TEST-RESULTS.json), [INTEGRATION-VALIDATION.json](INTEGRATION-VALIDATION.json)은 선행 로컬 반영과 생성 실험의 시점별 증거다. 이번 게시 수량과 closure 검증은 [publication-evidence](publication-evidence/)를 따른다. 사전 복합 이미지 gate의 완전 통과 0/3, 신규 whole-source 채택 0이라는 결론은 그대로다.

이 검증 후 커밋, pull, 병합, push와 원격 SHA 확인을 진행한다. 결과는 Git 이력 및 기본 체크아웃의 `generated/maintenance/genre-fusion-20261022/publication-main/` 실행 기록에 별도 보존한다. 이 문서는 아직 수행하지 않은 원격 동작을 성공으로 주장하지 않는다.

게시 전 문서 whitespace 검사에서 발견한 VISUAL-CARDS의 빈 필드 뒤 공백과 마지막 빈 줄만 정리하고 생성기에도 같은 포맷을 적용했다. 원래 markdown과 생성기 UTF-8 원문은 publication-evidence/research-document-formatting.json에 원래 hash와 함께 보존했다. TSV의 CRLF 바이트는 보존하고 CRLF를 인식하는 whitespace 검사로 검증했다.
