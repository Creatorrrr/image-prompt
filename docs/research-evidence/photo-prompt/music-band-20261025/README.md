# 음악물·밴드물 리서치와 반영 계획

2026-10-25 KST. [참조 대화](https://chatgpt.com/c/6adc0815-34c4-83ec-86c5-1f374795dad0)를 전체 확인해 시각 의미 데이터와 후보 데이터의 확장안을 만들었다. 도구 응답이 잘려 로그인된 Chrome에서 14절·마지막 예시까지 읽었다.

- 원문 **25개 표·392행** 보존. 복합어·중복·작품·조합 행을 포함한 수다.
- 공개 **1차 출처 52개**: 본문 38개, 발췌 14개. 실제 원격 이미지/영상 표본 검토는 미실행.
- 한영 **시각 카드 124개**, 선택 시 함께 보여야 할 **가시 관계 판정점 372개**, 문맥 구분 **20개**, 후속 연구 **12주제**.
- 리서치 baseline authored source **22,899건 / 모듈 121개**의 해시 조사. 음악 관련 어휘 hit **90건**에는 오탐이 포함됨. 상세 재사용 제안 **9건**.
- 검색 개발 **44사례·한영 88질의**, 카드 파생 smoke **124사례·248질의**, 향후 픽셀 검증 **16사례** 설계. 이후 실행 결과는 [반영 및 이미지 검증 결과](INTEGRATION-RESULTS.md)에 기록했다.

## 읽는 순서

1. [주요 조사 결과와 근거](RESEARCH.md)
2. [구체적인 데이터 반영 순서·파일·검증·설치 계획](IMPLEMENTATION-PLAN.md)
3. [한영 시각 의미 카드 124개](VISUAL-CARDS.md)
4. [원문 키워드 392행 추적표](KEYWORD-ATLAS.md)
5. [시각과 문맥의 20개 구분](CONTEXT-DISTINCTIONS.md)
6. [출처·확인 범위·접근 한계](SOURCES.md)
7. [검색·선택·픽셀 평가 계획](EVALUATION-PLAN.md)
8. [남은 연구 범위](GAPS.md)

## 기계 판독 자료와 재현

`keyword-atlas.json`, `semantic-cards.json`, `context-distinctions.json`, `sources.json`, `remaining-research.json`이 연구의 구조화 자료다. 모두 연구용이며 운영 후보 import·native 승인·자동 강제 활성화를 제공하지 않는다. `existing-records.json`은 현재 후보 원문·조건·effects·binding 스냅샷, `existing-triage.json`은 9건의 제안이다. `corpus-audit.json`에 조사 필드·정규식·오탐 한계와 source 해시가 있다.

```bash
python3 docs/research-evidence/photo-prompt/music-band-20261025/build_research.py
python3 docs/research-evidence/photo-prompt/music-band-20261025/build_evaluation.py
python3 docs/research-evidence/photo-prompt/music-band-20261025/validate_research.py
```

`audit_corpus.py`는 실행 시점의 corpus를 다시 조사하므로 기존 연구 baseline을 덮어쓰지 않으려면 별도 복사본에서 실행한다. `validation.json`은 연구 구조·출처 참조·원문 보존·해시 확인 **27개 항목 통과** 결과다. 조사한 authored source 121개와 manifest의 해시도 유지됐다. 사실성 전체·native·검색 품질·이미지 합격과는 별개다.

## 현재 상태

시각 카드 124개를 새 선택형 후보 122개와 기존 완전 원문 재사용 2개로 반영했다. 문맥·연구 보류 진단 32개, 선택형 바인딩 370개와 키워드 392행을 보존했다. 현재 기본 검색 버전에 동일한 음악 데이터가 포함된 것을 검증했다.

독립 서브에이전트 세 곳에서 첨부 사진을 실제 참조로 한 이미지 3장을 생성했다. 주제·얼굴과 머리 참고는 3/3에 보였지만, 사전 엄격 전체 장면 기준은 0/3 통과했다. 새 음악 후보 채택과 인과적 이미지 개선은 입증되지 않았다. 자세한 결과, 이미지, 프롬프트와 테스트케이스는 [반영 및 이미지 검증 결과](INTEGRATION-RESULTS.md)에 있다.

이후 미채택 원인과 가림·좌우 역할 오류를 분석해 후보 검토 지침과 장면 투영을 수리했다. 같은 참고 파일과 기존 21개 기준으로 새 독립 에이전트 세 곳에서 3장을 재생성했다. 부모 직접 판정은 13/21 → 16/21, 독립 팔 판정은 17/21이며, 고개 큐 한 항목의 판정자 차이를 보존했다. 엄격 전체 장면 통과는 0/3을 유지했다. 신규 음악 source 14개를 실제 읽었으나 최종 추가 기여는 0이었다. [원인 분석·수정·재시험 결과](round2-20261025/RETEST-RESULTS.md)에 세 원본 이미지, 실제 프롬프트와 동일 testcase를 모았다.

validation.json과 기존 SHA256SUMS는 최초 연구 완료 당시의 기록이다. 적용 후 검증과 파일 해시는 integration-evidence에 별도로 보존한다. 최초 완료 시점에는 commit/push를 실행하지 않았다. 이후 게시·정리 범위는 [게시 기록](PUBLISHING.md)에 있다.
