# 포크 호러 자료의 main 게시 범위

2026-10-22. 기준 main `332d98937a69021e80846619526fe1d851bb6ada`의 기존 source·binding·catalog·policy를 모두 유지하고 포크 호러의 후보 88개(가시 69·진단 19), optional 연결 133개, 의미 카드 89개와 원 대화 키워드 경로 150개를 추가했다. 기존 R01 후보 1개는 원문을 바꾸지 않고 재사용하며 선행 로컬 실험의 동일 source임을 확인했다.

| 항목 | 게시용 main | 선행 로컬 실험 |
|---|---:|---:|
| 전체 후보 | 19,360 | 19,559 |
| 양성 검색 CID | 19,091 | 19,256 |
| 진단 | 269 | 303 |
| binding | 13,453 | 13,777 |

수량 차이는 다른 미커밋 자료·기존 source 수정의 포함 여부다. 이번 게시에는 포크 호러의 동일 신규 CID/원문/effects만 추가하며, 다른 미커밋 코드·source·설치 선택은 포함하지 않는다. 기존 main 후보 19,272개와 binding 13,320개를 모두 보존했다.

- source SHA256: `418f43e64c2ad5ac966cd1033b7ffe9d370aced7134bb2af7969c1845d74cca6`
- 검색 layout: `42d406d9b8935c485507fd0bc98daecc17442529e91008a035eea7d02bb29de8`
- source/index 전체 closure 검증 PASS, dictionary 오류 0개, 관련 회귀 242개 PASS.
- 검증된 부모 layout 두 개에서 CID·전체 text hash·recipe·model/space가 일치하는 벡터 19,091개를 재사용했다. 새 임베딩/외부 API/이미지 호출 0회다.
- 연구·통합·이미지 실험의 원본 파일과 기존 SHA256SUMS/APPLY-SHA256SUMS는 보존했다. 현재 게시 범위는 PUBLICATION-SHA256SUMS로 확인한다.

## 설치와 이미지 증거의 범위

게시용 `retrieval-runtime.json`은 main의 기존 H-F2 `13d885356aa63c72ec29b0409e8cce23469b3cbc0f9c0adbaf840ff7584d70db`를 유지한다. 앞선 이미지 실험은 최신 작업 SKILL `7fe5b6cfc2da6e65dd9b9dc999e46d70a1fac7dce8c47157e53c1cba43b00f35`와 로컬 설치 H-F2 `0ad30ffe246d77f7c711ea49244b407b71ff747cbc33b380f6f12aaacd657cf2`에서 수행했다. 기본 체크아웃의 그 실행 선택과 다른 저자의 미커밋 작업, native CURRENT는 바꾸지 않는다. source/index 게시와 설치 세대 활성화는 별개다.

세 생성 원본·프롬프트·독립 manifest·사전 테스트·원본 판정을 함께 게시한다. 참조 외형은 세 장에서 유지됐으나 엄격한 technical qualification은 0/3이며 실패를 그대로 보존한다. Korea는 우물 크롭/발자국 경로, Harvest는 강압감 부족과 지지 미관측, Winter는 문턱 전체 폭 가림이 남았다. 신규 L03의 문턱 바깥 그릇 관계는 Winter에서 부분 확인했으며 다른 두 arm은 신규 source 전달을 검증한 것으로 세지 않는다. native approval·사용자 수락·생성 품질의 인과 개선을 주장하지 않는다.

| 컨셉 | 실제 프롬프트 | 원본 |
|---|---|---|
| 닫힌 공동 우물 | [프롬프트](integration-evidence/arms/korea/actual-tool-prompt.txt) | [PNG](images/korea-closed-well.png) |
| 씨앗 공납 | [프롬프트](integration-evidence/arms/harvest/actual-tool-prompt.txt) | [PNG](images/harvest-seed-levy.png) |
| 겨울 과수원 문턱 | [프롬프트](integration-evidence/arms/winter/actual-tool-prompt.txt) | [PNG](images/winter-threshold.png) |

상세 결과는 [이미지 테스트](IMAGE-TEST-RESULTS.md), [초기 통합](INTEGRATION-RESULTS.md), [게시 검증](publication-evidence/)에서 구분한다. 일부 절대 경로는 당시 실행 위치의 기록이며 향후 워크트리 제거로 바뀔 수 있다. 원본 PNG와 실제 tool prompt는 이 폴더에 독립 복사본으로 보존되어 있다.

이 검증 다음 commit·origin/main pull·양쪽 source를 유지하는 main 병합·push·실제 remote SHA 대조를 수행한다. 그 Git 실행 결과와 정리 증거는 기본 체크아웃 `generated/maintenance/folk-horror-20261022/publication-main/`에 보존한다. 제거 대상 워크트리의 ignored 모델 12개는 기본 체크아웃과 동일 hash의 중복 복사본이며 Python 링크도 기존 runtime을 가리킨다.
