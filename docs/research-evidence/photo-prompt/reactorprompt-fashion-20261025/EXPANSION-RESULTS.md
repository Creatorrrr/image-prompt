# ReactorPrompt 패션 후보 보강 실행 결과

최초 **2,556개 용어를 전수 처리**하고, 신규 후보 **2,430개**와 binding **5,887개**를 등록·인덱싱했다. 검증된 설치 버전을 기본 런타임으로 선택했다. 완료 시각(UTC): 2026-10-25T20:51:57.742626+00:00.

원본은 2026-10-25 수집 snapshot의 중복 제거 프롬프트 2,974개다. 2,556은 프롬프트 수가 아니라 추출 용어 수다. 이번 실행 중 원본 corpus·첫 추출 ledger·첫 export를 보존했다.

| 최종 용어 처리 | 개수 |
|---|---:|
| 새 후보 생성 | 1,932 |
| 기존 후보 재사용 | 57 |
| 검토된 부분 의미 연결 | 295 |
| 진단 | 231 |
| 비의상·일반 맥락 | 35 |
| 근거 부족 보류 | 6 |
| 합계 | 2,556 |

실제 후보 ID가 연결된 용어는 **2,284개**다. 진단·일반 맥락·보류 272개를 긍정 후보 성과에 더하지 않았다. 의미 연결은 특정 원문에서의 기여 범위를 표시하며, 용어 전체와 완전한 착장을 동등시하지 않는다. 기존 선택 CID 68개는 원래 sealed 상태를 보존했다.

최종 대조에서 발견한 빈 의미 연결 17개는 독립 재검토 후 모두 해결했다. 10개는 검토된 카드에 범위를 명시해 연결했고, 1개는 기존 스커트의 드로스트링 의미로 연결했다. 원문에 회중시계 체인만 있는 1개는 시계 본체와 구별해 진단으로 고쳤다. 실제 의미가 빠져 있던 5개는 새 후보로 작성했다. 기존 확장 후보 2,425개와 binding 5,876개는 record 단위로 그대로 보존했다.

## 실제 자격과 적용 조건

신규 후보 중 **4개**는 실제 설치된 source authority와 검토된 `hair_color` 역할 검사를 통과했다. 나머지 **2,426개**는 검색·발견용이며 native 사용 자격을 얻지 않았다. 전체 어휘나 연결된 큰 후보에 일괄 승인을 부여하지 않았다. 기존 재사용 CID 68개도 모두 기존 unqualified 상태다.

네 머리색 후보의 실제 bound-binding 합성 fixture에서는 정상 대상·명시적 선택을 갖춘 요청이 허용됐고, 다른 대상 또는 선택 누락은 strict admission에서 거절됐다. 외형 잠금은 source admission은 통과하지만 property scope가 변경을 거절했다. 두 검사를 함께 통과해야 적용할 수 있다. 이 fixture는 실제 프롬프트 채택이나 이미지 생성 결과가 아니다.

기존 재사용 binding의 상태는 {'review_required': 40, 'deferred_source_binding': 28}이며, deferred 상태를 unbound entry로 우회하지 않았다. 추가 authored 조건이 있는 96개 discovery 후보의 105개 절은 75개 원자적 전제 식별자로 보존했으며 자동 충족시키지 않는다.

## 검색 검증

고정된 영·한 어휘 질의 **5,112개**를 최종 설치 generation에서 실행했다. 연결된 신규 후보 중 1,624개가 해당 질의의 상위 8개에 한 번 이상 노출됐다. 이는 어휘 기반 노출 확인이며 의미 정확도나 native 승인 수치가 아니다. 원래 용어 표기와 번역의 제한도 유지했다.

별도로 고정한 자연어 질의 **46개**의 상위 8개를 같은 코드·모델·질의 벡터로 비교했다. 요청한 패션 하위 명제 전체(필수 속성·대상·관계·제외)를 충족하는 후보가 나온 질의는 **3/46 → 14/46**이었다. 최종 32개는 부분 일치다. 적절한 기존 CID도 전체 일치로 인정했다. 새 CID가 나왔다는 이유만으로 성공으로 세지 않았다.

| 평가 노출 구분 | 질의 수 | 기존 전체 의미 일치 | 최종 전체 의미 일치 |
|---|---:|---:|---:|
| 먼저 의미를 검토한 7개 사례 | 14 | 0 | 3 |
| 원문을 기준으로 먼저 고정한 나머지 16개 사례 | 32 | 3 | 11 |

최초 짧은 keyword 질의의 3/68과 exact-text 자기 검색 68/68은 다른 검사로 보존한다. 위 46개·5,112개 결과와 같은 지표로 합치지 않는다. 검색 알고리즘·모델·고정 질의를 바꾸거나 alias를 늘려 통과시키지 않았다. 실제 prompt 채택·전체 장면 렌더링·픽셀 품질·사용자 수용은 **NOT RUN**이다.

## 검증과 설치

- 2,974개 문서 hash 및 원래 51,771개 출현 참조의 literal 검사가 통과했다. 최종 교정 overlay는 357개이며 원래 ledger는 보존했다. 이 수치는 모든 출현의 의미 정확도를 전수 수동 판정했다는 뜻이 아니다.
- 최초 8개 작성 묶음과 추가 교정 묶음의 source·한영 의미·owner·조건·effects·binding을 독립 검토했다. 원문·형식 검사와 정확한 전체 후보 중복 검사는 통과했다. 다른 문장의 모든 기존 후보에 대해 수작업 동등성을 전수 판정했다는 주장은 하지 않는다.
- 작업 원본 V3 전체 dictionary **PASS**: 26,087 candidates / 24,508 bindings. 최종 primary index는 이전 벡터 24,071개를 재사용하고 5개만 새로 계산했다. source revision은 종료됐고 현재 editing은 null이다.
- 설치용 sealed V4 전체 dictionary에는 기존 Sports-fiction 관계 형식 오류 1개가 그대로 남아 있다. 새 패션 후보 오류는 0개다. V4 전체 dictionary가 PASS했다고 보고하지 않는다.
- 기존 131개 원본 모듈, sealed 코드·기존 records/bindings/catalog, H-F2 baseline RID·벡터 21,648개를 보존했다. 무관한 dirty 작업 코드를 설치하지 않았다. 지원 installer로 검증 후 기본값을 선택했고 실제 runtime check와 dispatch smoke가 통과했다. CURRENT pointer는 변경하지 않았다.
- 모델은 로컬 EmbeddingGemma2이며 고정 질의 벡터를 재사용했다. 외부 유료 embedding API 호출과 이미지 생성은 0회다. 중간 실패·도구 수정·최초 비활성 generation·검사 기록도 보존했다.

기본 H-F2: `a55eef7a1c3972cb463fa38f437c9e2198d021d8a10f69b04f11eafa9adda031`  
기본 native: `07dc8e671afaed7f6ef1a74966107c7dff2a143087eaeb3df4bd774098fa4e1d`

## 남은 근거 공백

- **false eyelashes**: 직접 false eyelashes/false lashes를 선언하고 자연 모발, 연장, 마스카라와 구분하는 source occurrence가 필요하다.
- **shimmer finish**: 이 유일한 긍정 용례는 highlighter, shimmer, jewelry를 별도 열거하고 shimmer의 소유자나 표면 마감 여부를 지정하지 않는다. 의복/장신구의 특정 소재 마감이라는 직접 근거가 추가되어야 해제할 수 있다.
- **light sneakers**: 원문 문맥으로 light의 시각 속성(밝은 색 vs 경량)이 결정되지 않는다.
- **tabi shoes**: 원문은 “white tabi”라고만 하며 신발/양말 종류를 구별할 구조 증거가 없다.
- **navy cap**: 모자 안감만 언급되어 모자 실루엣과 착용 owner/관계가 없다.
- **beading**: 원문만으로 실제 비즈 장식과 광택 하이라이트를 구별할 수 없다. 소유 표면이 명시된 구조 또는 광학 반응 증거가 필요하다.

6개는 실제 원문 공백 때문에 보류했다. 미작성 항목을 근거 부족으로 돌리지 않았다. 검색의 부분 일치와 discovery-only 자격 제한은 위 결과대로 남는다.

## 산출물

- [전체 용어 CSV](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-fashion-20261025/exports/fashion-keywords-expanded.csv)
- [근거·처리·실제 자격 JSON](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-fashion-20261025/exports/fashion-keywords-expanded.json)
- [최종 실행·검증 receipt](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-fashion-20261025/expansion/FINAL-RESULT.json)
- [46개 질의 의미 판정](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-fashion-20261025/expansion/runtime/natural46-meaning-comparison.json)
- [출현 교정 overlay](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-fashion-20261025/expansion/merged-draft/occurrence-corrections-final.json)
