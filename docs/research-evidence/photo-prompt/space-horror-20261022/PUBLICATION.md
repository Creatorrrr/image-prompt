# 스페이스 호러 변경의 Git 발행 범위

2026-10-23 KST. 깨끗한 main 기준 작업용 워크트리에서 이번 스페이스 호러 자료만 분리했다. 현재 기본 체크아웃의 다른 미커밋 코드·후보 수정, analog-horror/cosmic-relation 작업은 복사하지 않았다. 공유 source manifest는 기존 main의 모든 행을 그대로 유지하고 스페이스 호러 module 두 개만 추가했다. maintenance 문서도 기존 main 내용에 이번 설명만 추가했다.

- 추가 기록 79개: 선택형 시각 후보 53개, 진단·문맥 26개.
- 기존 source 5개를 수정 없이 참조하고 바인딩 146개 추가.
- 분리한 원본 main 후보 19,698개와 기존 조건·효과·catalog·정책·바인딩 보존.
- 초기 분리 커밋의 source 후보 19,777개, 바인딩 14,249개.

Git main의 global-document v1 색인과 이미지 실험에 사용한 설치본의 grounded-document v2 색인은 문서 recipe가 다르다. 실험 벡터를 다른 recipe로 재명명하지 않는다. 기존 main의 벡터는 정확히 재사용하고, 새 양성 후보 53개만 검증된 로컬 EmbeddingGemma 모델로 계산한다. 이미지 재생성이나 원격 모델 호출은 없다. 기존 벡터 19,351개를 정확히 재사용했으며 새 layout은 `cfac524dd01561017d80a03d06e28c405bcb3039c07fc7a4f426aa0c26bf3d31`이다. 전체 source/문서/벡터/통계/샤드 closure 799개 member 검증 결과는 [index-build.json](publication-evidence/index-build.json)에 기록한다.

source context 47개, primary proof boundary 15개, sampling 6개, 총 68개 회귀가 통과했다. 추가 source/index 및 checksum 검증 결과는 [validation.json](publication-evidence/validation.json)에 기록한다.

`retrieval-runtime.json`은 upstream main 선택값을 보존한다. 기본 체크아웃의 로컬 실험 선택값과 이미 설치된 실행 세대도 변경하지 않는다. production Python code 변경, 자동 실행 세대 전환이나 CURRENT 쓰기는 포함하지 않는다. 이미지 기록은 당시 `c34c69bb6a031f2938987cc687a51481e01d24710e7ba06f5e05f4130a91f849`에 고정된 실험이며 이 Git 발행 색인에서 다시 생성한 이미지로 해석하지 않는다.

## 이미지와 실행 기록

세 arm의 파일은 원래 경로와 byte hash를 [arm-archive.json](publication-evidence/arm-archive.json)으로 연결했다. 실제 생성된 세 장과 프롬프트·source 검토·고정 입력·ledger·독립 manifest·실패 판정을 보존했다. C의 최초 고정본과 `/active` 실행본도 함께 보존했다. `.staging`, Python cache와 실행 잠금 파일은 제외했으며 첨부 원본 인물 사진은 복제하지 않았다. JSON 내부의 당시 절대 경로와 hash는 역사적 근거로 그대로 유지한다. C의 정적 검토용 crop 1개와 원본 복사본 1개도 보존했으며 추가 생성 호출로 세지 않는다. [image-inventory.json](publication-evidence/image-inventory.json)이 실제 생성 3회와 정적 검토 파일을 구분한다.

- A: [이미지](publication-evidence/arms/a/the-listening-nursery.png), [전체 보고서](publication-evidence/arms/a/final-report.md).
- B: [이미지](publication-evidence/arms/b/images/native-attempt1.png), [전체 보고서](publication-evidence/arms/b/final-report.md).
- C: [이미지](publication-evidence/arms/c/active/images/missing-calibration-observer-native.png), [전체 보고서](publication-evidence/arms/c/active/C-final-report.md).

엄격한 전체 픽셀 판정은 0/3이다. A는 4/6, B는 3/6, C는 5/6 항목을 통과했다. 신규 후보는 세 실행에 노출됐지만 최종 채택은 0개다. 새 데이터에 따른 인과적 이미지 품질 향상, source 전체 native qualification, 사용자 수락은 입증하지 않았다. 앞선 연구·통합 문서에 적힌 당시 미커밋 상태와 기본 실행 버전은 역사적 기록이며, 이번 Git 발행과 구분한다.

커밋은 명시적 파일 allowlist와 staged blob hash를 대조한다. 커밋 후 `git pull --no-rebase origin main`으로 원격 main을 통합하며, 원격과 변경이 겹치면 양쪽 source·조건·바인딩·문서를 보존하고 파생 색인을 다시 검증한다. 실제 원격 반영까지 확인한 뒤 작업 전용 워크트리만 제거한다. 최종 Git SHA와 기본 작업 폴더 보존 증거는 `generated/maintenance/space-horror-main-publication-20261023/`에 별도 보관한다.

원본 TSV의 CRLF, diff 문맥의 빈 줄 접두사, 과거 코드 snapshot EOF로 발생한 whitespace 지적은 원본과 동일한 11개 역사 자료에 한정된다. 해당 파일의 발행 전·원본·발행본 SHA256 일치를 확인하고 기존 hash를 보존했다. 다른 모든 경로는 엄격한 whitespace 검사를 통과한다([세부 기록](publication-evidence/whitespace-exceptions.json)).

## origin/main과의 실제 통합

첫 커밋 `c072429a731e51273859e8f67a28168e645fbdbe` 뒤 `git pull --no-rebase origin main`은 처음에 최신 상태였으나, 곧 원격 main에 analog-horror 커밋 `9b654b631653719774c276148daeadc308c0b50b`가 추가됐다. 로컬 main 갱신 전 비교 가드가 이를 발견해 기본 작업 파일을 쓰기 전에 멈췄다. 그때의 `git push origin main`은 이미 반영된 main에 대한 no-op이었다. 이후 원격 main을 다시 pull하고 실제 충돌 세 곳을 통합했다.

- source manifest: incoming main 등록 75개를 모두 유지하고 스페이스 호러 2개를 더해 77개 등록으로 합쳤다.
- maintenance 문서: incoming 본문과 analog-horror 설명을 유지하고 스페이스 호러 설명을 추가했다.
- 파생 검색 색인: 한쪽 파일을 선택하지 않고 합쳐진 전체 source로 재구성했다.

최종 source는 19,862개(양성 19,476, 진단 386), 바인딩 14,377개다. incoming main의 후보 19,783개와 바인딩 14,231개가 보존됐고 이번 79개/146개만 더해졌다. 기존 벡터 19,423개를 정확히 재사용하고 스페이스 호러 53개는 앞서 계산한 같은 recipe·text·model의 로컬 캐시로 재사용했다. 추가 문서 inference는 0회다. 새 layout은 `43dd677206365b6ed899887fb1da1b0ee5ba12a8ddddc29c22e40d0c7e6f789a`이며 802개 member 전체가 검증됐다.

관련 회귀 68개를 합친 소스에서 다시 실행했고 dictionary의 source/index 검사도 오류 0개다. incoming의 비공유 파일 1,187개는 incoming commit blob과 바이트가 동일하다. 최초 분리 커밋의 색인·검증·문서·checksum은 [pre-merge](publication-evidence/pre-merge/README.md)에 별도 보존했다. 다른 주제의 역사적 publication checksum은 해당 당시 commit의 기록으로 유지하며 이번 합친 tree는 새 PUBLICATION-SHA256SUMS로 별도 검증한다.
