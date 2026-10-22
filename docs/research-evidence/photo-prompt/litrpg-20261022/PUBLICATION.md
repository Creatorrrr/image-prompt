# LitRPG Git 발행 범위와 검증

2026-10-23 KST. LitRPG 전용 의미·후보·바인딩·가이드, 연구 자료와 세 이미지 실험 기록을 분리했다. 공유 파일은 기본 체크아웃의 전체 수정본을 복사하지 않고 기존 main에 LitRPG 등록 두 개와 설명만 추가했다. 기존 main의 다른 주제·조건·효과·정책·catalog·바인딩을 유지한다.

| 항목 | 결과 |
|---|---:|
| 보존한 기존 후보 | 19,518 |
| 추가 후보 | 78: 양성 60 / 진단 18 |
| 최종 후보 | 19,596 |
| 양성 검색 후보 | 19,276 |
| 추가 바인딩 | 128 |
| 최종 바인딩 | 13,892 |
| 기존 벡터의 정확한 재사용 | 19,216 |
| 신규 로컬 문서 벡터 | 60 |
| 발행 중 원격 모델 / 이미지 호출 | 0 / 0 |

Git main의 v1 global-document 인덱스와 실험에 사용한 설치본의 v2 grounded-document 인덱스는 문서 recipe가 다르다. v2 벡터를 v1으로 재명명하지 않았다. main의 기존 벡터를 그대로 보존하고 신규 60개만 검증된 로컬 EmbeddingGemma 모델로 계산해 v1 전체 통계를 재구성했다. 검증된 새 layout은 `cb5511fb1cc53bd98db5845dec1a8625786fded99f832d5d63db6553a2f993a6`이다. 소스·검색 공간·문서·벡터·샤드의 전체 closure 검증을 통과했다.

사전 실행한 dictionary 검사에서 소스 추가 후 아직 재구성 전이었던 index와의 불일치를 확인했다. 인덱스 재구성 후 검사를 다시 수행한다. 처음 발생한 실험 v2/발행 v1 reader 불일치도 원인을 확인하고 서로 다른 문서 recipe의 벡터 재사용을 거부했다. 소스나 검증 규칙을 완화하지 않았다.

관련 회귀 검사는 source context 47개, primary proof boundaries 15개, sampling 6개, 총 68개가 통과했다. 최종 dictionary·소스/index 검사와 원본 archive hash 결과는 [validation.json](publication-evidence/validation.json)에 있다. [index-build.json](publication-evidence/index-build.json)은 정확한 개수와 실행 증거를 보관한다.

현재 설치 실행 버전과 Git 발행 인덱스를 구분한다. `retrieval-runtime.json`은 upstream main 값을 유지했고, 기본 체크아웃의 로컬 실험 선택값도 변경하지 않았다. 이전 세대와 CURRENT를 보존한다. 이전 이미지 실험은 `ef02180fc06f390a079ecb7727ece11c2dd30e54394f9e1ae8b9112217bd29ac`에 고정된 기록이며 이번 발행 인덱스에서 다시 실행한 이미지라고 주장하지 않는다. 자동 설치 세대 전환이나 production code 변경은 이 Git 발행에 포함하지 않는다.

## 세 이미지 실험의 휴대 가능한 원본과 기록

- A 공원 관리원: [원본](publication-evidence/arms/a/image.png), [프롬프트](publication-evidence/arms/a/final-prompt.txt), [픽셀 판정](publication-evidence/arms/a/litrpg-pixel-review.json).
- B 유리 공방: [원본](publication-evidence/arms/b/generated-original.png), [프롬프트](publication-evidence/arms/b/final-prompt.txt), [픽셀 판정](publication-evidence/arms/b/scene-pixel-review.json).
- C 광산 탐험: [원본](publication-evidence/arms/c/image-original.png), [프롬프트](publication-evidence/arms/c/final-prompt.txt), [픽셀 판정](publication-evidence/arms/c/pixel-testcase-review.json).

[arm-archive.json](publication-evidence/arm-archive.json)은 원래 경로와 archive 경로를 바이트 hash로 연결한다. `.staging` 검색 캐시, `__pycache__`와 빈 실행 잠금 파일을 제외했고 첨부 원본 인물 사진은 복제하지 않았다. 당시 JSON 내부의 절대 경로·hash·실패 판정은 원문 그대로 유지한다. 연구 단계의 SHA256SUMS와 INTEGRATION-SHA256SUMS는 당시 기본 체크아웃의 경로/파일에 대한 증거다. 이번 발행은 저장소 루트 기준 [PUBLICATION-SHA256SUMS](PUBLICATION-SHA256SUMS)로 별도 검증한다.

실제 이미지는 세 장이며 전체 사전 기준 통과는 0/3이다. 공원/공방의 주제 관계는 통과했지만 정확한 손 배치/잡는 위치가 달랐고, 광산은 감시자 방향과 잘린 발/문턱 끝점이 부족했다. 신규 I01 구조의 사용과 픽셀 생존은 공방에서 확인했다. native 전체 원문 적격성, 데이터 추가의 인과적 품질 향상, 사용자 수락은 입증하지 않았다.

커밋은 명시적 경로 allowlist와 staged blob hash를 대조한다. 커밋 후 `origin/main`을 pull하고, 원격 변경이 있으면 의미·등록·문서·인덱스를 보존해 통합한다. main 및 실제 원격 SHA가 일치한 뒤 이 작업 전용 워크트리를 제거한다. 최종 Git 실행 증거는 기본 체크아웃의 `generated/maintenance/litrpg-main-publication-20261023/`에 별도로 기록한다.
