# source102 전체 문맥·승인77 부분 검증 완료

운영에 적용하지 않는 **source102 연구 체크포인트**에서 기존 표준 처리 경로를 실행했다. 전체 18,250개 ID, catalog149, 기존 binding12,089개와 모든 정책·참조를 보존했다. 승인77개의 정확한 proof만 연결했고, 그 proof의 역할 관계162개는 request-local proposal 경로로 검사했다. 새로운 의미 승인·영구 binding·운영 자격·운영 pointer 변경은 모두 0건이다. 전체 18,250/pending0 채택 gate는 그대로다.

## 실제 완료한 경로

- 7개 배치의 `verify_batch`와 루트 acceptance, 현재 CID 전체 after·참조 closure·binding 일치를 재검증했다. 전체 컨테이너의 구조/native 검증을 통과했다. 이 검사는 승인되지 않은 나머지18,173개의 의미를 승인하지 않는다.
- 고정 G 소비자 코드로 전체 positive18,198개를 구축했다. 같은 로컬 공간의 ID/본문/recipe/실행증거가 맞는 벡터18,161개를 재사용하고, 변경되거나 positive로 복원된 문서37개만 실제 로컬 추론했다. Gemini/외부 API/모델 다운로드는 0건이다. native metadata 전후 검색 document projection은 동일하며 CID당 positive 문서는 하나다.
- R 안의 전용 `research-runtime-store`에 표준 API로 봉인한 generation은 `200d5a8b3e8bbe8e31e69c7a290aa641bd39832fe4d372eff30337ea78b6acb8`이다. 운영 runtime store와 고정 G는 읽기만 했다.
- 기존 blue-cup core에 대해 catalog149 각각의 실제 로컬 질의를 만들고, 각 슬롯에서 전체 공통 positive pool의 BM25F·local cosine·RRF를 실행했다. 독립 core/source 조건에 따라 eligible10,193개가 됐다. public pack은 고유 CID19개와 역할 제안288개이며, 283개 제안은 그 역할의 persistent binding 없이 제시됐다. 모든 lane/RRF에는 CID 중복이 없다.
- 같은 실제 query context를 담은 issued receipt 발급·독립 replay·baseline 유지 구성을 감사했다. **구조 감사 PASS, quality WARN/경고6**이다. 이 blue-cup pack에는 승인77개가 제시되지 않았고 optional native 채택은 0건이다.
- 루트가 complete core/envelope/controls/8개 typed assertions/embodiment를 직접 읽어 수용한 6220 통제 사례도 별도로 실행했다. image_detail의 실제 전체 검색에서 6220은 BM25F4위/local cosine1위/RRF1위로 정식 제시됐다. 실제 pack·issued receipt·replay를 거쳐 한 건을 선택했고, 기존 전체 image_A·원 style/image.detail E·연속 윤곽/세부 가독성 두 PR·other_A 분리를 유지한 최종 구성은 **03에서 PASS, quality WARN/경고7**이다. 이는 실제 사용자 이미지나 픽셀 관찰의 증명이 아니다.

## 근거와 실패 보존

- [SOURCE-VERIFICATION.json](SOURCE-VERIFICATION.json), [APPROVED-ROLE-RELATIONS.json](APPROVED-ROLE-RELATIONS.json), [REQUEST-ROLE-VERIFICATION.json](REQUEST-ROLE-VERIFICATION.json)
- [BUILD-PREFLIGHT.json](BUILD-PREFLIGHT.json), [DOCUMENT-EXECUTIONS.json](DOCUMENT-EXECUTIONS.json), [BUILD-VERIFICATION.json](BUILD-VERIFICATION.json)
- [RESEARCH-GENERATION-MANIFEST.json](RESEARCH-GENERATION-MANIFEST.json), [SLOT-SEARCH-SUMMARY.json](SLOT-SEARCH-SUMMARY.json), [CONSUMER-VERIFICATION.json](CONSUMER-VERIFICATION.json), [실제 issued receipt 압축본](archives/ISSUED-RECEIPT.json.gz), [COMPOSE-AUDIT.json](COMPOSE-AUDIT.json)
- [6220 루트 full-core 검토](native6220-proposal-04/ROOT-CORE-REVIEW.json), [최종03 구성](native6220-adoption-03/COMPOSED.json), [최종03 감사](native6220-adoption-03/COMPOSE-AUDIT.json), [최종03 대조](native6220-adoption-03/VERIFICATION.json)

최초 압축 JSON decode 오류는 추론 전에 거부했다. 소비자 첫 시도는 generation에 모델 설치가 없어서 봉인 전에 거부됐고, 다음 시도는 system Python의 다른 numpy 때문에 검색 전에 거부됐다. 동일 바이트의 기존 설치 주소와 pinned numerical runtime만 명시해 해결했다. 최초149개 local query 실행증거를 그대로 검증·재사용했으며 실패를 새 local 성공으로 바꿔 쓰지 않았다. 각 ATTEMPT/log는 보존한다.

6220의 최초 최종 감사는 whole-image 관계의 literal `relation_evidence` 누락을 거부했다. 02는 root-approved 최종문구를 그 관계 증거로 명시했다. 루트의 후속 읽기에서 공통 helper의 잘못된 cup rationale을 발견해, **동일 pack/receipt/core/prompt/선택을 유지한 rationale 한 필드만** 03에서 고쳤다. 01·02를 덮어쓰지 않았다. 최종 근거는03이다. 경고는 uncovered-intent를 원문으로 보존했다는 설명6개와 visual_proposition 경고1개이며, 구조 PASS가 미적·시각적 품질 성공을 뜻하지 않는다.

## 검색 누락·측정의 한계

태그로 검색 pool을 나누지 않았지만 intrinsic 조건과 frozen request scope가 먼저 eligibility를 제한한다. 역할 적용성·실제 RID 조건, lane prefix·역할별 예산·고유64개 예산도 public presentation을 제한한다. 현재 diagnostic52개는 positive 문서가 아니다. 따라서19개 public 후보를 전수 의미 recall이나 catalog149의 의미 정확도로 해석하지 않는다. 162개 관계의 proposal 생성 역시 native 최종 채택 허가가 아니다.

원 snapshot reader의 누적 IO는 payload reads1,098/posting reads19,214/vector reads603,624, 총10,497,670,427 bytes이고 cache peak는67,108,862 bytes다. 이는 pack 생성과 그 reader를 재사용하는 독립 검증의 누적치이며, 하나의 질의 비용이나 전체 프로세스의 모든 reader 합계가 아니다. 최종 compose API가 새로 여는 audit reader의 IO는 이 수치에 합쳐지지 않는다.

## 다음 정확한 경계

이 체크포인트의 source는 `39ab970ec8a42550f6afb41163ae6e2e76c1403f60f76cb9e5a962e3197dd65c`이고, proof를 연결한 연구 컨테이너는 `db0875e12046787f59461a346f76a53fb9f6102089a98cd0b467f9813996f6b0`이다. 이후 루트가 선택한 source24 `841cf085cff0a9c6977f0b1ac0c20f4525e158647b51de092ce6c15105d6c7d8`와 구별한다.

[SOURCE24-INCREMENTAL-PLAN.json](SOURCE24-INCREMENTAL-PLAN.json)은 14건의 kind-only 복원을 직접 대조했다. 기존18,198 벡터를 정확히 재사용하고 새 positive14개만 로컬 추론하면 된다. 전체18,212개의 전역 DF/field length/포스팅·guard를 다시 검증하고 새 source의 검색·pack·receipt를 실행해야 한다. 같은 core/catalog/controls/space의 질의는 exact binding 검증 후 재사용할 수 있다. source24 증분 실행·새 native 승인·운영 적용은 아직 하지 않았다.

재실행과 후속 CID 표준 경로는 [COMMANDS.ko.md](COMMANDS.ko.md)에 기록했다. 현재 완료는 **전체 데이터 문맥의 승인77 부분 검증과 정확한 통제 사례1개**다. 전체149/18,250 전수 의미 확정, 5~8단계 전체 완료, 운영 적용·활성화·이미지·사용자 수용을 주장하지 않는다.

큰 baseline pack·issued receipt·149 query context는 [ARCHIVES.json](ARCHIVES.json)에 원바이트 hash와 압축 hash를 대응시킨 gzip으로 Git에 보존한다. 압축 해제 결과는 원파일과 바이트 단위로 같다. 원 raw파일과 9.4MB의 파생 전체 연구 컨테이너·index·전용 generation은 로컬 R에 그대로 남긴다. 전체 컨테이너는 기존 source102와 정확한77 proof를 `run.py prepare`로 결합해 재생성할 수 있다. 압축/문법/해시 검증은 의미 정확도 인증이 아니다.

루트 통합에서 `run.py`의 오래된 “publication API 미사용” 설명을 실제 격리 연구 발행 범위에 맞춰 정정했다. 실행 함수·동작은 AST 대조상 동일하다. 실제 실행 당시 전체 바이트는 `run.executed-before-docnote-v1.py`에 보존하며 기존 `FINAL-FILE-SHA256.json`은 정정 전 역사 대장이다. 현재 커밋 바이트의 최종 대장은 `FINAL-FILE-SHA256-ROOT-02.json`이다. 첫 설명 정정 검사의 AST 비교 호출 형식 오류는 코드나 실행 결과를 바꾸지 않았고, 올바른 모듈 단위 비교로 확인했다.
