# 아이돌물 데이터 게시 및 정리

2026-10-24 KST. 기본 작업 폴더의 다른 변경은 포함하지 않고, 최신 main의 기존 데이터·코드·문서 위에 이번 아이돌물 확장만 합친다.

게시 범위는 시각 선택 명제120개, positive 검색 제외 문맥45개, 선택 binding219개, 자문형 용어 경로325개와 연구·검색·이미지 평가 증거다. 기존 source payload·조건·효과·catalog·policy를 덮어쓰지 않는다. 공유 corpus manifest와 maintenance 문서는 이번 항목만 추가한다. 로컬 설치 버전 포인터나 다른 작업의 미게시 코드 변경은 복사하지 않는다.

## 보존한 평가 결과

세 독립 native 이미지 호출은 각1회다. 세 장면에서 주제와 참조 외형은 읽히지만 엄격 전체 장면 기준0/3이며 신규 후보 실제 채택도0이다. 기록·전달 감사 통과를 이미지 성공이나 새 데이터의 품질 개선으로 바꾸지 않는다. 최초 판정과 수정 근거를 함께 보존한다.

## 영구 증거와 경로

- `image-test-evidence/`: 세 원본 생성 이미지, 프롬프트, freeze/core, 검색·구성·실행·recorder·평가 기록. 원본 참조 인물 사진은 포함하지 않는다.
- `runtime-evidence/`: 최초 설치/검색 평가의 작은 JSON·로그·빌드 스크립트. 모델·거대한 파생 generation 복제본·request cache는 게시하지 않는다.
- `publication-evidence/`: main 통합 시 source 보존·dictionary·index·기존 의미 경계 테스트 결과.
- `ARCHIVE-MAP.json`: 과거 생성 경로와 현재 보존 경로의 대응.

Raw JSON/receipt/ledger와 child report는 해시·실행 바인딩을 보존하기 위해 바이트를 바꾸지 않았다. 그 안의 절대 경로는 실행 당시 provenance다. 현재 최상위 보고서의 이미지·프롬프트 링크는 영구 증거를 가리키며, 원래 보고서도 `publication-evidence/original-reports/`에 보존했다. 기존 DELIVERY/INTEGRATION 해시 목록은 원래 실행 스냅샷이고, 게시 패키지에는 별도 `publication-evidence/SHA256SUMS`를 사용한다.

## 검증과 정리 순서

먼저 이번 source와 증거를 커밋한 뒤 `git pull --no-rebase --no-edit origin main`으로 원격 변경을 통합한다. 충돌은 기존 main의 모든 항목과 이번 source를 보존하고, 파생 검색 index는 합쳐진 전체 source에서 다시 만든다. dictionary/index 및 관련 기존 테스트를 통과한 최종 상태만 main에 정상 fast-forward push한다.

원격 main SHA와 최종 커밋을 확인한 뒤, 영구 증거 복사본의 해시를 검증하고 이번 전용 생성·빌드·캐시 폴더 및 publication worktree를 정리한다. 현재 설치된 공유 runtime과 다른 작업의 파일·worktree·캐시, 사용자의 원본 참조 사진은 유지한다. 정리 대상의 정확한 파일·해시는 `publication-evidence/cleanup-plan.json` 및 압축 inventory로 커밋하고, 실행 후 영구 감사 영수증은 `/Users/chasoik/.codex/cleanup-receipts/idol-fiction-publication-20261024.json`에 남긴다.

## 최초 main 기준 검증 (03be907ad)

최초 source 커밋 `ef037a66981c` 후 origin/main을 pull했으며 `03be907adda9a3e9c3ef94a3bbfacaeb6dba7968`과 충돌 없이 통합됐다. 기존 후보20,791개·binding15,636개의 source 바이트를 보존했다. 최종 후보20,956개·binding15,855개, positive20,264개에 대해 dictionary 오류0과 전체 index 재검증 PASS를 확인했다. 기존 의미 경계21개·원문 처리24개 테스트도 통과했다. 이 결과는 데이터/검색 무결성 검증이며 이전 이미지의 미통과 판정을 바꾸지 않는다.

## 최종 동시 변경 통합

마지막 pull에서 스파이물 게시 커밋 `52128de98276e8987abe28ded90292affaaf7768`이 추가되어 공유 파일3개가 충돌했다. 원격 후보21,286개·binding15,865개를 바이트 그대로 유지하고 아이돌물165개·219개를 추가했다. 최종 후보21,451개·binding16,084개·positive20,417개로 전체 index를 다시 만들고 dictionary 오류0 및 별도 index 재검증 PASS를 확인했다. 스파이물 회귀11개를 포함한 관련 테스트56개가 통과했다. 미참조 중간 index35adb02c의 파일842개는 해시·Git 복구 이력을 남기고 최종 트리에서 제외했다.

원격에 이미 커밋된 스파이물 증거의 CRLF·후행 공백은 원문 바이트 그대로 유지했다. 새 main을 기준으로 이번 패치에 수행한 whitespace 검사는 통과했으며, 이전 우리 HEAD 대비 보이는 기존 원격 공백 경고는 별도 기록했다.
