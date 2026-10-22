# 아날로그 호러 Git 발행 범위와 검증

이번 발행은 아날로그 호러 의미·후보·바인딩·가이드, 원래 연구 자료와 독립 세 이미지 실험 기록을 포함한다. 공유 manifest와 maintenance 문서는 혼합된 기본 체크아웃을 복사하지 않고 기존 main에 이번 등록과 설명만 추가했다. 기존 후보 19,698개·바인딩 14,103개와 catalog·정책은 그대로 보존했다. 다른 미커밋 source/code/runtime 선택값은 포함하지 않았다.

| 항목 | 결과 |
|---|---:|
| 이번에 저술한 새 후보 | 84: 시각 71 / 진단 13 |
| 재사용을 위해 가져온 기존 전제 후보 | 1, 원문 그대로 |
| 이번에 저술한 새 바인딩 / 기존 전제 바인딩 | 126 / 2 |
| 발행 후보 / 바인딩 합계 | 19,783 / 14,231 |
| 양성 검색 후보 | 19,423 |
| main 벡터의 정확한 재사용 / 새 로컬 문서 벡터 | 19,351 / 72 |
| 발행 중 원격 모델 / 이미지 호출 | 0 / 0 |

A064가 참조하는 기존 `cand_8ed5a9486be65af9b7a3e3d39ca477fb`는 작업·설치 코퍼스에는 있었으나 처음 Git main에는 없었다. 그 원문과 바인딩 두 개만 별도 prerequisite 모듈로 보존했다. 다른 미커밋 cosmic/space-horror 데이터는 발행하지 않았다. [prerequisite-source.json](publication-evidence/prerequisite-source.json)은 원래 소유자·내용·조건·효과·출처·바인딩을 바이트 의미 변경 없이 기록한다.

Git main의 v1 global-document 인덱스와 당시 설치본의 v2 grounded-document 인덱스는 document recipe가 다르다. 설치본 벡터를 v1으로 재명명하지 않았다. 기존 main 벡터를 보존하고 72개만 검증된 로컬 EmbeddingGemma 모델로 계산해 전체 통계를 재구성했다. 새 layout은 `d066e5778ee7ee466aac5d0468c5a316c89e502fd26c7b989e6825a36936e216`다. [index-build.json](publication-evidence/index-build.json)과 [validation.json](publication-evidence/validation.json)은 source/index·통계·payload·벡터·routing closure 전체 검증, dictionary 검사 및 관련 회귀 검사 68개의 통과를 기록한다.

`retrieval-runtime.json`은 upstream main 값을 유지했다. 기본 체크아웃의 로컬 실험 선택값도 보존한다. 이전 세대와 CURRENT를 바꾸지 않는다. 이미지 실험은 `d5aec2788e925fb6e8b27831b0055a2545067372edf87a6d5c7ea233a716ebfa`에 고정된 당시 기록이며, 이번 Git 발행 인덱스에서 다시 생성한 이미지라고 주장하지 않는다.

## 세 이미지와 판정의 휴대 가능한 원본

- 1 빈 의자: [이미지](publication-evidence/arms/1/generated-image.png), [프롬프트](publication-evidence/arms/1/final-prompt.txt), [판정](publication-evidence/arms/1/theme-pixel-review.json). 주제 7/7·신체 5/5, 전체 통과.
- 2 입고대장: [이미지](publication-evidence/arms/2/generated_image.png), [프롬프트](publication-evidence/arms/2/final_prompt_en.txt), [판정](publication-evidence/arms/2/arm-result.json). 주제 5/5·신규 VHS 구조 3/3이 보이지만 손가락과 펜의 행/접촉 조건이 실패하여 전체 실패.
- 3 방송 종료: [이미지](publication-evidence/arms/3/generated_image.png), [프롬프트](publication-evidence/arms/3/final_prompt.txt), [판정](publication-evidence/arms/3/arm3_summary.json). 실제 입도 조금 벌어져 닫힌 입 대 열린 입 조건 실패, 전체 실패. 신규 시각 source 노출 0.

세 native 호출이 반환한 세 이미지이며 전체 통과는 1/3이다. 부분 충족을 통과로 바꾸지 않았다. native 전체 원문 자격, 전체 데이터의 이미지 품질 향상이나 사용자 수락은 입증하지 않았다. [arm-archive.json](publication-evidence/arm-archive.json)은 236개 기록의 원래 경로와 저장소 경로를 SHA-256으로 연결한다. 검색 staging/cache, Python cache, 임시 잠금은 제외했고 첨부 원본 인물 사진은 복제하지 않았다. JSON 내부 절대 경로와 해시·실패 판정은 당시 원문 그대로다.

원래 연구 파일 34개의 해시도 보존했다. 원래 SHA256SUMS는 당시 연구 스냅샷의 증거이며, 이번 발행은 저장소 루트 기준 [PUBLICATION-SHA256SUMS](PUBLICATION-SHA256SUMS)로 별도 확인한다. 명시적 경로 allowlist와 staged blob hash를 대조해 커밋한 뒤 origin/main을 pull하고 양쪽 소스·문서·인덱스를 보존해 통합한다. main과 실제 원격 SHA 일치 확인 뒤 작업용 워크트리를 제거한다. 최종 Git 실행 증거는 기본 체크아웃의 `generated/maintenance/analog-main-publication-20261023/`에 보관한다.

일반 staged 경로의 엄격한 whitespace 검사는 통과했다. 원문 해시를 보존한 TSV의 CRLF, 당시 unified diff의 빈 context 행, 실행 비교 기록의 EOF 형식 등 8개 과거 증거 파일은 바이트 보존 예외로 따로 검증했다. 활성 코드·데이터의 오류를 면제하지 않았다. 정확한 경로·해시는 validation.json에 있다.
