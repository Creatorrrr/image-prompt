# 학원물 연구·외형/포즈 확장 배포

학교 기본 연구 90개와 추가 외형·포즈 168개, 총 258개 자료를 함께 배포한다.
완결된 optional visual source는 206개, positive 검색에서 제외된 diagnostic은
52개이며, optional binding은 350개다. 기존 자료는 수정하거나 삭제하지 않는다.
공용 manifest는 기존 모듈과 이번 네 모듈을 filename/kind 기준으로 합친다.
검색 인덱스는 병합된 실제 소스와 그 checkout의 레시피로 다시 계산한다.

[추가 연구 보고서](REPORT.md), [기본 연구](../school-life-20261023/README.md),
[추가 결과 집계](RESULTS.json), [아카이브 경로표](publication-evidence/PATH-MAP.json).

| 추가 테스트 | 사전 원본 판정 | 원본 및 정확한 프롬프트 |
|---|---|---|
| A 앞치마 풀기 | 4/6, FAIL: 고리를 잡고 있으며 풀리는 매듭 상태가 없음 | [image](image-test-evidence/a/native-images/original.png), [prompt](integration-evidence/arms/a/native-prompt-exact.txt) |
| B 신발끈 조이기 | 4/5, FAIL: 각 손의 독립 끈끝 경로가 불명확 | [image](image-test-evidence/b/results/school-life-b-original.png), [prompt](integration-evidence/arms/b/native-prompt-exact.txt) |
| C 친구의 리본 정돈 | 5/5, PASS | [image](image-test-evidence/c/native-images/native-original-0b1ce71013b2.png), [prompt](integration-evidence/arms/c/native-prompt-exact.txt) |

기본 학교 연구의 이전 세 생성은 각각 7/9, 11/14, 7/8로 모두 전체 FAIL이다.
그 원본과 판단도 `../school-life-20261023/image-test-evidence/`에 보존했다.
추가 테스트는 원본 세 장·각 1회 호출이며 재생성이 없다. 모든 새 후보 최종
채택은 0이므로 데이터가 이미지 개선을 일으켰다고 주장하지 않는다.
source/index 검증, prompt 전달, pixel qualification과 사용자 판단은 별개다.

기존 역사 JSON·프롬프트·이미지의 바이트는 유지했다. 큰 텍스트 자료 일부는
`.gz`로 보존하고 원본/압축 해시를 PATH-MAP에 기록했다. 경로표의 압축 자료를
풀면 원래 바이트를 복원할 수 있다. 역사 자료의 사용자 로컬 절대 경로는 원래
기록이며, 위 링크와 경로표가 배포된 상대 경로를 제공한다.

중복 source/build/store 복사본·다운로드 원문·일시 실행 파일은 배포에서 제외했다.
푸시와 원격 SHA 확인 후 이 작업 소유의 임시 파일과 캐시를 제거한다. 활성 설치
runtime과 모델 환경, 원본 참조 사진, 결과 이미지·프롬프트·판정 증거, 다른 작업의
수정/삭제/미추적 데이터는 보호한다. 설치 runtime의 역사적 세대와 저장소의
재구축 인덱스는 서로 다른 산출물이므로 역사적 평가를 새 소스 평가로 바꾸지 않는다.
