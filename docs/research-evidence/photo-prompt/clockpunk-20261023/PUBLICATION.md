# Clockpunk 변경의 Git 발행 범위

2026-10-23 KST. 깨끗한 `main` 기준의 별도 워크트리에서 이번 Clockpunk
변경만 분리했다. 기본 체크아웃의 다른 주제, 미커밋 코드와 설치 실행본 선택은
복사하지 않았다. source manifest의 기존 등록을 보존하고 Clockpunk module
두 개만 추가했다. maintenance 문서도 기존 본문에 해당 설명만 추가했다.

- 의미 카드 88개와 검색 보조 경로 213개를 연결한다.
- 시각 후보 74개, 양성 검색에서 제외되는 진단 17개, 선택적 바인딩 137개를 추가한다.
- 기존 후보 6개의 표현을 교정하고 조건·효과·출처를 유지한다.
- 추가 기술 검토가 필요한 카드 7개는 보류하며 전체 native source 자격을 부여하지 않는다.

공유 파일은 레코드 단위로 분리했다. 각 교정 대상은 원래 `main` 레코드와
사전 snapshot을 비교한 뒤 적용했으며, 다른 기존 레코드·바인딩·카탈로그·정책을
보존한다. 파생 검색 색인은 이 발행 범위의 전체 source로 다시 검증한다.
동시에 작업 중인 다른 주제의 로컬 파생 색인은 발행하지 않는다.

Git 색인의 `photo-global-visual-text/v1`과 이미지 실험 설치본의 별도 문서 recipe를
혼동하지 않는다. 기존 Git 색인의 호환 벡터는 정확히 재사용하며 새로 필요한
문서는 고정된 로컬 EmbeddingGemma-2 모델로 계산한다. 원격 임베딩 호출,
이미지 재생성, production Python 코드 변경이나 CURRENT 쓰기는 없다.
`retrieval-runtime.json`은 upstream main 선택값을 유지한다. 실험은 당시 고정
H-F2 `1357d4e9171988e46ea9825a2ce4bed4afdd875ca4e29cb24c3f93c02ceaa608`의
기록이며 이번 Git 색인에서 다시 생성한 이미지로 해석하지 않는다.

## 생성 이미지와 시험 근거

세 독립 서브에이전트가 만든 사전 기준·추첨·프롬프트·관리형 실행 기록과
실제 반환된 세 PNG를 보존했다. 원본 업로드 인물 JPEG는 Git 발행본에
복제하지 않았다. 원래 실행 파일과 발행 사본의 byte hash 대응은
[archive-inventory.json](publication-evidence/archive-inventory.json)에 있다.
잠금 파일, 임시 staging과 대형 모델·실행본 closure는 제외했다.
JSON 내부의 당시 절대 경로와 SHA는 역사적 근거로 유지했다.

| Arm | 실제 생성 이미지 | 원래 상세 판정 |
|---|---|---|
| A | [태엽식 모종 관수 장치](publication-evidence/images/a.png) | [보고서](image-tests/arm-a/arm-a-report.md) |
| B | [운하 출발소의 기계식 노선표](publication-evidence/images/b.png) | [보고서](image-tests/arm-b/arm-report.md) |
| C | [정오 독서 마당의 그늘 관리인](publication-evidence/images/c.png) | [보고서](image-tests/arm-c/result-report.md) |

이미지 생성은 총 3회, 반환 3회, 재시도와 fallback 0회다. 장르 인상과 참고
외형은 세 장에서 확인했으나 엄격한 전체 픽셀 기준은 **0/3**이다. A는 관계
2/5, B는 2/6, C는 참고 외형을 포함해 3/6이다. 기어 맞물림과 연속된 출력
경로 등의 실패를 보존한다. 새 자료의 직접 프롬프트 영향은 A의 A01
`inspiration_only`에서만 확인됐다. B/C는 노출된 자료를 제외했다. 전체
source 채택, 새 데이터에 따른 인과적 품질 향상과 사용자 수용은 입증되지 않았다.

[통합·이미지 보고서](INTEGRATION-AND-IMAGE-TESTS.md)와
[검색 후속 계획](RETRIEVAL-FOLLOWUP.md)은 당시 작업 실행의 기록이다.
기계 구조를 해부학으로 오분류한 실제 검색 실패도 그대로 유지했다.
원래 `SHA256SUMS`와 `INTEGRATION-SHA256SUMS`는 각각 연구 단계와 로컬
통합 단계의 snapshot으로, 제외된 로컬 자료나 당시 공유 파일을 참조할 수 있다.
이번 Git 발행 파일은 별도의 `PUBLICATION-SHA256SUMS`로 검증한다.
원래 문서의 미커밋 상태와 실행 선택값도 당시 기록이며 후속 Git 상태와 구분한다.

커밋은 명시적 파일 allowlist와 staged blob hash를 대조한다. 커밋 후
`git pull --no-rebase origin main`으로 원격 변경을 통합하고, 겹치는 source와
문서는 양쪽 의미를 보존한다. 파생 색인은 합친 전체 source로 다시 검증한다.
푸시 후 local HEAD/main, origin/main, 실제 원격 main을 확인한 다음 이번
임시 워크트리만 제거한다. 최종 SHA와 기본 체크아웃 보존 기록은
`generated/maintenance/clockpunk-main-publication-20261023/`에 별도 보관한다.

## 분리한 source와 색인 검증

분리 발행 source는 19,953개(양성 19,550개, 진단 403개), 바인딩 14,514개다.
기존 후보 19,856개와 모든 기존 바인딩·카탈로그·정책을 그대로 보존했다.
교정한 6개 후보의 조건·효과·출처도 유지했다.
[레코드 보존 검사](publication-evidence/source-preservation.json)와
[원래 서식 보존](publication-evidence/format-preservation.json)에 근거를 남겼다.

기존 벡터 19,470개를 정확히 재사용했다. 교정 후보 6개와 신규 양성 74개의
문서 80개만 검증된 로컬 모델로 계산했다. 새 layout은
`103c2a04978752b81fd55927c550070173de276b5f1de8bf61a1a227fa4bc86a`이며
[전체 색인 검증](publication-evidence/index-build.json)을 통과했다.
source context 47개, primary proof boundary 15개, sampling 6개로
총 68개 기존 회귀를 통과했다. 이 검사는 앞선 이미지 실패를 성공으로
바꾸거나 새 source의 전체 native 자격을 부여하지 않는다.

source/index dictionary의 전체 검사도 오류 0개다. 색인 closure는 805개
member이며 발행 파일 1,138개를 명시적으로 대조했다. 원본 TSV의 빈 필드와
과거 산출물의 EOF·서식에 따른 whitespace 지적은 정확한 원본 byte hash가
일치하는 9개 역사 자료에 한정된다. 다른 모든 파일은 엄격한 whitespace
검사를 통과했다([원본 일치 근거](publication-evidence/whitespace-exceptions.json)).
