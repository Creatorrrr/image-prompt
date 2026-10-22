# 초현실 포스트휴먼 자료의 main 게시 범위와 검증

2026-10-22. 기준 main `17c0dd349304a18abac290beae114f199114e379`의 기존 원문·연결·catalog·policy를 보존하고, 이번 Surrealism, Surreal Horror, Posthuman Fiction, Science Fantasy 확장만 추가했다. 다른 미커밋 source·코드·로컬 설치 선택은 게시에 포함하지 않았다.

| 항목 | 게시용 main 구성 | 선행 로컬 실험 snapshot |
|---|---:|---:|
| 전체 후보 | 19,272 | 19,471 |
| 긍정 검색 후보 | 19,022 | 19,187 |
| 문맥 진단 | 250 | 284 |
| 선택적 슬롯 연결 | 13,320 | 13,644 |
| 이번 추가 | 72 가시 장면, 16 문맥 진단, 144 연결 | 동일한 CID와 한영 원문 |

수량 차이는 이번 추가가 빠졌다는 뜻이 아니다. 로컬 실험에는 다른 미커밋 후보와 기존 source 수정이 포함돼 있었다. 게시에서는 기준 main의 후보 19,184개와 연결 13,176개를 모두 유지한다. 기존-source 이웃 스냅샷과 검색·이미지 평가는 해당 로컬 실험 시점의 증거로 보존한다.

- 의미 레지스트리의 88개 기록과 182개 키워드 경로, 혼동 경계와 원전 열람 범위를 그대로 게시한다.
- source SHA256: `ce034b85ca3c3e27dec7bc7d835d26f1e78c552dc4865c8590ecfbdab823407a`
- 검색 인덱스 layout: `a1d6f9ca15aade602b71b851f5728bc877f87357c118e936e8b41918db1f1b3c`
- source/index closure 검증 PASS, dictionary 오류 0개, 기존 관련 회귀 테스트 275개 PASS.
- 기존 일치 벡터 18,950개 재사용, pinned 로컬 EmbeddingGemma 신규 문서 72개 생성, cache hit 0개. 외부 embedding API 호출 없음.
- 새 자료의 native approval은 false다. 검색 등록, 후보별 사용 판단, 전체 원문 구현과 실제 이미지 품질을 구분한다.

게시하는 `retrieval-runtime.json`은 기준 main의 H-F2 `13d885356aa63c72ec29b0409e8cce23469b3cbc0f9c0adbaf840ff7584d70db`를 유지한다. 선행 이미지 실험은 로컬 설치 세대 `0df1fb14b8c36b9580c218e0e931039dc695593c3f5d9cdc30f61d6c8ede42b9`에서 수행했다. 기본 체크아웃의 그 선택과 다른 미커밋 파일 바이트를 보존하고 native CURRENT는 쓰지 않는다. source/index 게시와 설치 릴리스 활성화는 별개다.

## 실제 생성 원본과 실패 판정

세 서브에이전트가 독립적으로 core를 확정하고 첨부 참조로 각각 한 장을 생성했다. root도 세 원본을 직접 확인했다. 요청 주제 모티프와 참조 얼굴·헤어는 가시적이지만, 완전한 장면 조건은 세 경우 모두 일부 실패했다. 신규 후보의 자연 노출은 4·1·1개였고, 1번의 일반적 이음 경계 영감도 픽셀에서는 실패했다. 새 데이터의 품질 개선 인과 효과를 입증하지 않는다. 보정 호출은 재시도 계약 검증에서 차단돼 0회이며 실패를 우회하지 않았다.

| 컨셉 | 실제 프롬프트 | 원본 판정 |
|---|---|---|
| 궤도 관측소 | [프롬프트](integration-evidence/arm1-final-prompt.txt) | 가슴 부품의 피부 통합 실패, 장치 가장자리 일부 잘림 |
| 유기적인 씨앗집 | [프롬프트](integration-evidence/arm2-prompt.txt) | 핵심 손–벽 뿌리망 구현, 단일 역전 문 조건 부분 실패 |
| 그림자 갱신 창구 | [프롬프트](integration-evidence/arm3-final-prompt.txt) | 반대 손목 접촉, 전달 경로 일부 누락 |

![궤도 관측소 생성 원본](publication-evidence/images/arm1.png)

![씨앗집 생성 원본](publication-evidence/images/arm2.png)

![그림자 갱신 창구 생성 원본](publication-evidence/images/arm3.png)

원본 바이트는 [image preservation](publication-evidence/image-preservation.json)으로 확인한다. 자세한 당시 판정과 보정 절차 이탈은 [이미지 결과](IMAGE-TEST-RESULTS.md)와 [integration evidence](integration-evidence/)에 보존했다. 사용자 수용은 미확인이다.

원래 연구·통합 문서와 `SHA256SUMS`, `APPLY-SHA256SUMS`는 변경하지 않았다. NOT_RUN과 당시 수치를 후속 검사의 성공으로 바꾸지 않는다. 이 게시 검증은 [publication evidence](publication-evidence/)와 `PUBLICATION-SHA256SUMS`로 구별한다.

워크트리의 ignored 모델은 기본 체크아웃에 있는 동일 hash 파일의 독립 복사본이고 Python 링크는 기존 전용 runtime을 가리킨다. 제거 전에 고유 증거를 게시하거나 기본 체크아웃에 보존한다.

이 검증 뒤 커밋·origin/main pull·병합·push·실제 원격 SHA 확인을 수행한다. Git 결과는 이력 및 기본 체크아웃의 `generated/maintenance/surreal-posthuman-science-fantasy-20261022/publication-main/`에 기록한다. 이 문서는 아직 실행하지 않은 Git 동작을 성공으로 주장하지 않는다.
