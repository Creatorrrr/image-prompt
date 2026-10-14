# EmbeddingGemma 2 로컬 기본값 전환 결과

2026-10-14, Asia/Seoul. 구현·전체 재임베딩·검색 품질·오프라인 실행·기본값 전환·복구 검증 완료.

## 실제 기본값과 보존

현재 기본값은 `embeddinggemma2-local / google/embeddinggemma-2`의 텍스트 구성이다. 모델 revision은 `914f7f89142e33e77833254d9c9b90c3cef7303b`, 실제 파라미터 수는 271,002,624, 패키지는 약 1.116 GB다. 모델·토크나이저·설정·패키지 버전은 스킬의 lock 파일로 고정했다. Mac arm64/Python 3.14.3/MPS FP32에서 검증했다.

공개 CLI는 스킬 전용 Python으로 실행하고 같은 프로세스에서 지연 로드한다. 다른 Python에서 직접 호출할 때는 CLI가 소유하는 파이프 worker를 사용한다. 모델 로드·추론은 요청 의미를 동결한 이후에만 실행한다. 기존 프로젝트 가상환경은 수정하지 않았다.

전체 positive record 18,180개를 새로 임베딩했다. 기존 Gemini 벡터 재사용은 0개다. 기존 18,250개 authored record와 ID·의미·조건·효과를 보존했다. Gemini manifest 원본 bytes와 721개 선언된 search member의 SHA-256이 유지되고, 처음의 무관한 dirty 파일 변경은 0개다. 기존 `GOAL_PLAN.md`도 그대로다.

- 활성 local layout: `f82ab43bc2a5a141ad1aedcc1f415b68737b9e5867af829a6c88d6750f27a285`
- 활성 runtime generation: `7762d28b962e4e3113ab53ace75ec0faf2d1312ace59d678abdf3be6146f9eb1`
- source fingerprint: `15f1d146933c2ad4e212837efeb19948fa3ee55dc046330dfbb258bad8183023`
- Gemini 복구 자료: [activation-backup](/Users/chasoik/Projects/image-prompt/artifacts/embeddinggemma2-migration-20261014/activation-backup)

## 검색 품질

현재 동일한 전체 positive corpus에서 보존한 한국어·영어 질의 1,000개를 비교했다. 모호한 3개를 제외한 유효 997개가 채점 대상이다. Gemini의 보존된 동일 입력 질의 벡터와 현재 Gemini 문서 벡터를 사용했으며, 과거 보고서의 수치를 기준선으로 가져오지 않았다.

| 지표 | Gemini | 로컬 |
|---|---:|---:|
| 한국어 Recall@1 | 60.84% | 68.07% |
| 한국어 Recall@5 | 95.98% | 96.79% |
| 영어 Recall@1 | 64.13% | 67.13% |
| 영어 Recall@5 | 98.40% | 99.00% |

두 언어의 Recall@5는 각각 기준선 대비 -2 percentage points 이내라는 사전 기준을 통과했다. 실제 core/조건으로 구성한 회귀 20개에서는 한국어 5/5·영어 5/5의 필요한 후보가 노출됐고, 제외·문자 인용 사례의 금지 후보 노출은 0건이다. 20개 독립 검색 감사도 통과했다. 과거 `costume_style` 역할은 현재의 `attire_context`로 매핑했으며 요청·정답·기준은 유지했다.

새 Gemini hybrid 호출은 월 지출 한도 초과(`429 RESOURCE_EXHAUSTED`)로 거절됐다. 한도를 바꾸거나 결제하지 않았다. 따라서 새 Gemini hybrid 측정값을 주장하지 않는다. 이 고정 회귀 집합에서 로컬의 positive hit rate가 두 언어 모두 100%이므로, 가능한 Gemini hit rate의 상한 100% 대비 -2pp 기준은 충족한다. 이것은 상한 비교이며 실제 신규 Gemini 측정과 구분한다.

방향·소유자·관계·부정·형태의 pure-vector 혼동 쌍 40개도 확인했다. Gemini는 35/40, 로컬은 34/40이다. 미세 의미 구분에는 여전히 오류가 있으며 aggregate 검색 개선을 완전한 의미 정확성으로 주장하지 않는다. 이 진단은 후보 채택·이미지 평가와 다르다. 문맥·소유자·제외·요청 의미 동결과 선택 조건은 그대로 유지한다.

질의는 과거 사용한 source-conditioned 합성 자료와 회귀 fixture다. 미사용 실사용 holdout·생성 이미지·사용자 선호의 증거로 확대하지 않는다.

## 오프라인 실행과 체감 비용

OS sandbox의 `deny network*`와 API 키 제거 상태에서 공개 CLI·새 질의·72개 슬롯 검색·candidate pack·issued receipt가 성공했다. 캐시 적중만으로 오프라인 추론을 주장하지 않았다.

- cold: 57.44초, 슬롯 72개, cache hit 0개.
- cache_warm: 40.15초, 슬롯 72개, cache hit 72개.
- 해당 비교의 최대 child/process RSS: 2.72 GB. 총 GPU 메모리라는 뜻은 아니다.
- 전환한 실제 기본 경로의 추가 uncached 실행: 60.81초. 복구 publication이 병행된 상태의 관측값이며, 사전 isolated 비교와 구분한다.

전체 source/index closure와 모든 로컬 문서 실행 증거를 검증했다. 정확한 cosine 순위·top-K·64MiB vector cache·슬롯 독립성·RRF·표현 한도를 유지했다. NumPy는 보수적인 경계와 경쟁 후보 screening에만 쓰고 최종 점수는 기존 `math.sumprod`로 확정한다. 독립 full-scan oracle과 일치했고 전체 pruning proof가 통과했다.

비용을 줄이기 위해 없는 용어의 부정 표현 정규식 컴파일을 생략했고 원본 함수와 13,274개 입력 쌍이 같았다. immutable guard projection은 전체 18,250개에서 원본과 같았고 동일 core의 재구성을 재사용했다. 모델·숫자 의존성의 버전 혼합은 거부한다.

## 복구와 최종 검증

별도 완전한 source 복사본에서 Gemini rollback → local 재활성화를 실행해 두 상태의 manifest/default/publication을 확인했다. 실제 로컬 generation의 issued receipt 재생과 72개 슬롯의 독립 검색 감사도 통과했다. 관련 회귀 테스트 72개와 `git diff --check`가 통과했다.

플랫폼·Python 버전에 맞는 모델/고정 wheel/코드/라이선스를 담은 오프라인 묶음을 생성하고, 새 설치 경로에서 OS 네트워크 차단 상태의 설치와 추론을 검증했다. 스킬 code와 설치 안내는 [local-embeddings.md](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/local-embeddings.md)에 있다.

## 자료와 복구 명령

- [채택 판정](/Users/chasoik/Projects/image-prompt/artifacts/embeddinggemma2-migration-20261014/qualification/ADOPTION.json)
- [검색 지표](/Users/chasoik/Projects/image-prompt/artifacts/embeddinggemma2-migration-20261014/qualification/vector-summary.json)
- [혼동 진단](/Users/chasoik/Projects/image-prompt/artifacts/embeddinggemma2-migration-20261014/evidence/boundary-diagnostic.json)
- [실제 receipt 감사](/Users/chasoik/Projects/image-prompt/artifacts/embeddinggemma2-migration-20261014/evidence/live-receipt-audit.json)
- [기존 자료 보존](/Users/chasoik/Projects/image-prompt/artifacts/embeddinggemma2-migration-20261014/evidence/preservation-final.json)
- [오프라인 묶음](/Users/chasoik/Projects/image-prompt/artifacts/embeddinggemma2-migration-20261014/offline-bundle)

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/activate_local_embeddings.py rollback   --backup artifacts/embeddinggemma2-migration-20261014/activation-backup
```

복구는 현재 authored corpus와 보존된 Gemini manifest가 일치할 때만 허용한다. 새 모델 또는 변경한 소스로 이동하려면 별도 재임베딩·검증·publication을 수행한다. 별도 서버 앱·지속 daemon·자동 cloud fallback은 없다.
