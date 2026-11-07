# 간호복 데이터 반영 및 시험 기록

2026-11-07. 원 대화에서 추출한 표 407행을 source inventory와 연구 전용 context view 407개에 보존했다. 이는 해당 대화의 표가 모두 개별적으로 검증됐다는 뜻이 아니다. 세 독립 검토의 3차 대조 결과는 조건부 정확 재사용 1행, 296행 부분 사례, 21행 진단용 맥락, 8행 맥락 전용, 81행 보류다. 81행은 기존 원본과 전체 의미 대조가 미완료이며 후보 부재라는 뜻은 아니다. 양쪽 검토 결과와 관련 후보·조건·효과·바인딩 증거는 assets의 photo_nurse_uniform_coverage_review_* 파일들에 보존했다. 자동 생성한 영문·한글 토큰 기반 382행의 어휘 후보 목록은 의미 동등성 검증이 아니다.

신규 시각 선택지 45개, optional binding 45개, 원본 결합 retrieval view 90개를 작성하고 source manifest에 등록했다. 슬롯과 뷰는 native 역할 승인, owner 선택, 효과 권한, 이미지 품질을 보증하지 않는다. 현대 의료복·역사·PPE·성인 코스튬·호러·소품/포즈를 예시로 포함하고, 한 원문 행은 맥락 전용 또는 중복 재사용일 수도 있다.

기존 최신 봉인 세대에 다른 동시 작업의 코스프레 후속분과 이번 간호복 자료를 결합했다. 세대 `c74b67a6f4bf8b63ded6c9305bcbb34bcf34b101a07f4f0d663ca46869c451bf`, native `829a08ca68ebf997f80fc76fc697382daaf11d0cd54c96ff9ea792ee5b4f7a6e`. native source round-trip, 27,835 후보 및 25,067 binding ID의 working corpus 대조(설치본의 기존 role_evidence 한 건 보존), 45 문서 및 90 뷰 추가, 임베딩·전체 봉인 검증 통과. 로컬에 `--no-activate`로 설치하고 독립 시험에서 해당 세대를 명시적으로 사용한 뒤, source/config 불변 검증과 전체 설치 검증을 재실행하고 기본 릴리스로 선택했다. 이전 설정은 `generated/nurse-uniform-combined-hf2-20261107-v2/pre-activation-retrieval-runtime.json`에 백업했다. `CURRENT`는 변경하지 않았다.

개발자 작성 질의 6개(N02/N10/N13/N18/N42/N48)에서 해당 후보가 각각 1위였다. 저자 인지된 시험이며 독립 holdout·전역 회귀·이미지 개선 증거가 아니다. 구조 테스트 2개 통과, 기존 뷰/complete-meaning 테스트는 9 통과, 12 스킵, 4 subtests 통과했다. 스킵은 통과가 아니다.

각 시험의 첫 검색은 staged native parent의 모델 부재로 실패했으나 쿼리와 preflight/transaction 전에 실패했다. 동일 세대에 검증된 동일 모델을 materialize하고 오류 증거를 보존한 뒤 frozen run에서 최초 검색을 실행했다. 3개 모두 4개 질의와 receipt audit 통과, 합성 감사 통과(quality warn 각 4). 3개 모두 전체 native candidate 선택은 0개다.

- A 현대 의료 튜닉: `generated/images/nurse-medical-tunic-20261107-a/image.png`; `generated/photo-runs/nurse-20261107-a-prep/pixel-observation.md`. 새 후보의 중앙 지퍼를 그대로 채택하지 않았고 일반 지퍼 발상을 주머니 여밈에 재해석했다. 실제 이미지는 바지·V넥 튜닉과 비스듬한 포켓 지퍼를 보여준다. 공식 리뷰는 기록 유효, 기술 판정 fail: 발의 지면 접점이 프레임 밖으로 미관찰이며 나머지 네 신체·접촉 게이트는 통과했다.
- B 사이버 의료복: `generated/images/nurse-cyber-20261107-b/image.png`. 새 후보를 조회했으나 허용된 native 채택은 없었다. 이미지의 V넥 튜닉, 디지털 패널과 터치 동작은 관찰되지만 새 복합 후보로 인한 결과로 볼 수 없다. 최초 자동 recorder 오류는 추가 호출 없이 resume으로 복구되어 native operation complete가 됐다. 공식 리뷰는 기록 유효, 기술 판정 fail: 발과 지면 접점이 프레임 밖으로 미관찰이며 나머지 네 신체·접촉 게이트는 통과했다.
- C 고딕 호러 간호사: `generated/photo-runs/nurse-20261107-c/images/nurse-gothic.png`; `generated/photo-runs/nurse-20261107-c/pixel-observations.md`. 하얀 단추식 드레스, 어두운 복도와 등불을 확인했다. 생성된 캡은 프롬프트에 없던 요소로, 검색된 신규 후보의 기여가 아니다. 등불 손잡이와 손가락의 정확한 접점은 부분 관찰. 공식 리뷰는 기록 유효, 기술 판정 fail이며 연결·접촉·투영의 세 게이트는 관찰이 불충분했다.

모든 이미지가 간호복 주제를 보여 주더라도 임의 모델 출력과 baseline의 기여를 새 데이터의 인과 효과로 간주하지 않는다. 눈가림 대조·반복 실험·사용자 수용은 수행하지 않았다. 보류 행의 기존 후보 의미 검토와 부분 후보의 부족한 면, 후속 후보의 필요 여부는 미완료다.

## 보충 반영과 남은 범위

81개 보류 항목을 다시 살펴 59행에 61개 선택적 시각 후보 및 각 binding 61개, retrieval view 122개를 추가했다. 15행은 맥락으로 남겼고 7행은 근거·대상 확정 부족으로 보류했다. 전체의 현재 분류는 조건부 정확 재사용 1, 부분 사례 355, 진단용 맥락 21, 맥락 전용 23, 보류 7이다. 이는 407개 출처 행이 추적 가능하다는 뜻이며, 각 행의 시각 의미가 완전히 구현됐다는 뜻은 아니다. 407개의 연구 맥락 뷰와 실제 양성 검색 뷰를 혼동하지 않는다.

보류 7행은 간호 업무용 신발, 에드워드풍 간호복, 군간호 제복, VAD 복장, 의료용 가위, 수녀풍 간호 코스튬, 누드 에이프런이다. 그 이유는 각각 상위 범주, 특정 시대·기관의 출처 부재, 국가·시대·제복 종류의 차이, 자원 구호대의 기관·시대 차이, 기존 가위의 재질·용도 미확정, 외형만으로 창작과 역사 고증 구별의 한계, 단일 시점의 전체 의복 부재 미관찰이다. 조건이 충족되는 하위 사례를 추가하더라도 행 전체가 검증된 것은 아니다.

보충 세대 `a4dd818b8ec0d6a20fcacae5c1f3cce80cb00170cc1dc18b86bfde6b96b01f70`, native `64dcc6e90d564fbcffbdabbc8eb2f00cf20776283bd39fddeedc6df0c64393d6`에 신규 양성 후보 106개와 검색 뷰 212개를 합산했다. 현 working manifest 및 staged corpus에서 27,896 후보와 25,128 binding의 ID가 일치했고, 이전 세대부터 설치본에만 있던 role_evidence 하나를 제외하면 원본 내용도 일치했다. 6개 개발 질의 중 5개는 목표 1위, 1개는 3위였다. 이 결과는 저자 인지 점검이며 독립 회귀·시각 품질 증거가 아니다. 15개 자동 테스트 통과, 12개 건너뜀, 4개 subtest 통과했다.

설치 첫 시도에서 테스트용 staged 트리의 복사된 Python 환경이 설치기의 symlink 조건과 달라 실패했다. 설치된 새 native 세대의 해당 복사본을 별도 보존하고, 사용 중인 skill 소유 환경에 대한 심볼릭 링크로 바로잡아 `--no-activate` 전체 검증을 통과했다. 시험용 staged 세대는 수정하지 않았다.

보충 세대를 기본 H-F2 설정으로 선택했다. 변경 전 설정은 `generated/nurse-uniform-supplement-hf2-20261107/pre-activation-retrieval-runtime.json`에 보존했으며 설치기의 full validation이 통과했다. `CURRENT` 파일은 변경하지 않았다.

## 보충 세대의 최종 독립 이미지 시험

세 콘셉트는 6개 풀에서 `secrets.SystemRandom().sample`로 중복 없이 뽑았고 각 에이전트는 검색 전 별도 코어를 동결했다. 고정한 사용자 요청과 참조 이미지, 세대 a4dd818b를 사용하여 각 1회 생성했다. 7/6/4개 질의와 각 receipt audit, compose audit을 통과했다. native 전체 후보 선택은 각 0건이며 일반 영감과 baseline을 별도로 기록했다. 모든 이미지에 사용자 수용 여부는 미확인이다.

- A 역사 병동: `generated/images/nurse-supplement-20261107-a/image.png`, pixel observation `generated/photo-runs/nurse-supplement-20261107-a/pixel-observation.md`, review `generated/photo-runs/nurse-supplement-20261107-a/review-audit-result.json`. 파란색은 검색 영감으로 프롬프트에 반영했고 이미지에도 보인다. 다섯 신체 게이트와 리뷰·기술 판정이 통과했다. 보충 61 후보는 적용하지 않아 그 영향은 시험하지 못했다.
- B 현대 스크럽: `generated/photo-runs/nurse-supplement-20261107-b/generated.png`, pixel `generated/photo-runs/nurse-supplement-20261107-b/pixel-review.md`. 보충 후보 `cand_077175b64b27505eafb80944e5ec4ed4`의 둥근 목선과 짧은 V 절개를 일반 영감으로 적용했고 화면에서도 보인다. 리뷰 기록은 유효하나 발과 바닥의 접촉이 프레임 밖이어서 기술 판정은 실패다. 나머지 네 게이트는 통과했다.
- C 고딕 병동: `generated/photo-runs/nurse-supplement-20261107-c/nurse-gothic.png`, pixel `generated/nurse-supplement-prep-20261107-c/pixel-observation.md`, review `generated/nurse-supplement-prep-20261107-c/visual-review.json`. 초기 45개에 속한 N29 / `cand_9704d53ab6ea5c8fb6c7659fcfb4a63f`의 캡·어깨 뒤쪽 윤곽광을 일반 영감으로 적용했다. 어깨 윤곽광은 보이나 캡의 뒤쪽 광원 관계는 불명확하다. 리뷰 기록은 유효하나 랜턴과 손가락 접촉·가시성 두 게이트의 부분 관찰로 기술 판정은 실패다. 지지·균형 pass는 보이는 상체 범위에만 적용했고 발과 발-바닥 접촉은 관찰되지 않았다.

A와 B의 recorder_failed는 반환된 동일 결과를 재호출 없이 복구해 operation complete가 됐다. 결과가 눈에 보인다는 사실은 완전한 후보 native 승인, 객관적 품질 개선, 또는 기여의 인과 증명이 아니다. 비교 baseline 이미지를 생성하지 않았고, 반복·블라인드 평가도 하지 않았다.

## 2026-11-07 후속 362행 조사

기존 부분 355행과 보류 7행을 모두 세 구간으로 나누어 원문과 이전 후보 근거 및 한계를 재추적했다. 82행에 직접적인 추가 외부 출처를 연결했으며 나머지 행의 외부 출처 검증은 여전히 미완료다. 각 파일은 `assets/photo_nurse_uniform_deep_review_{a,b,c}_20261107.json`, 연구 맥락은 `assets/photo_nurse_uniform_deep_context_views_20261107.json`에 있다. 둘은 양성 검색 결과나 native 선택 권한이 아니다.

일본 간호화의 구체적 상품 유형은 [제조사 카탈로그](https://www.fg-nurse.co.jp/fgdata/wp-content/uploads/2023/12/fujigom-nurse-catalog-2024.pdf), 1911년 VAD는 [영국 적십자 자료](https://vad.redcross.org.uk/medical-care-during-ww1/nursing-during-the-first-world-war), 1905년 지역간호 사진은 [Victorian Collections 설명](https://victoriancollections.net.au/items/5c3ffb3321ea67129c5ff515), 1953년 케이프는 [National Army Museum 소장품](https://collection.nam.ac.uk/detail.php?acc=1996-06-7--1) 범위로 기록했다. 이 사례로 모든 일본 간호화나 모든 시대·국가의 군간호복을 정의하지 않는다. 인물·재질·역사·의료 용도는 그림만 보고 판정하지 않는다.

별도 후보 75개, binding 75개, 양성 검색 뷰 150개를 등록해 대상 73행에 새 부분 사례를 추가하고 대상 밖 진단 행 테디에 전시용 예시 하나를 두었다. 보류 7행 중 6행은 제한된 예를 갖지만 전체 원문 의미가 자동 완결된 것은 아니다. 285행은 가려진 전신 의복 부재와 나이를 확인할 수 없어 보류를 유지한다. 영어 토큰 중복 탐색에서 높은 표면 중복은 나오지 않았지만 전체 코퍼스의 의미 중복 제거를 증명하지 않는다. 자동 테스트 17개 통과, 12개 건너뜀, 4개 하위검사 통과했다. 검색 릴리스 설치와 이미지 시험은 별도로 기록한다.

후속 H-F2 세대 `af54730fa3a9806e1e1c5d4f2aec96f89a800fe7421e82245defe4fec45b2327`, native `ed575a01c0213c1270ed1eaea596620d28e32d1a928f9617295a50015b04ee9f`에 75개 문서와 150개 뷰를 더해 임베딩·전체 봉인·설치를 검증하고 기본 런타임으로 활성화했다. 이전 설정은 `generated/nurse-deep-hf2-20261107/pre-activation-retrieval-runtime.json`에 보존했고 CURRENT를 바꾸지 않았다. 작업 소스 후보 27,971개 및 binding 25,203개의 ID는 staged 소스와 일치했으며, 기존 설치본에만 있던 role_evidence 차이 1건을 보존했다. 개발 질의 6건은 목표가 모두 1위로 검색됐다. 이는 저자가 답을 아는 탐침이며 독립 회귀나 픽셀 적합의 증거는 아니다.

### 362행 보강 후 독립 API 이미지 시험

무작위로 서로 다른 콘셉트를 정하고 사용자 원문과 각 arm 설정을 별도 envelope에 보존했다. 스킬 기본값을 제외하고 각 arm의 sensual, fetish, creativity 중 하나만 3으로 설정했다. 각 run은 독립 baseline 동결 후 세대 `af54730fa3a9806e1e1c5d4f2aec96f89a800fe7421e82245defe4fec45b2327`에서 검색했다. 요청한 모델은 `gpt-image-2.6-sunburst`, 참조는 실제 첨부 JPEG와 일치하는 SHA-256 바이트다. 관능/페티시 arm은 나이를 확인할 수 없는 원본 인물의 외모를 성적 변형하지 않기 위해 참조의 빛·색만 사용하고 별도의 성인 인물로 설정했다. API 성공 응답에 관찰된 모델명을 기록할 수 없었으며 로컬 외부 결과 연결은 self-reported 근거다.

- sensual=3, 다른 설정 기본값(페티시 0·창의성 1): 구성 및 참조 전송 감사와 dry-run은 통과했지만 API 1회가 `moderation_blocked` HTTP 400으로 거부되어 이미지·픽셀 검토 없음. 프롬프트를 바꾸거나 재호출하지 않았다. `generated/photo-runs/nurse-deep-20261107-sensual/test-report.json`, 오류 `generated/nurse-deep-research-20261107/api-results/97840a10ca8140e5ab4e5ff31808cf63/outcome.json`.
- fetish=3, 다른 설정 기본값(관능 1·창의성 1): `generated/nurse-deep-research-20261107/api-results/bf8fde0f24034815a9ba4c9f89e0323b/result.png` 1회 생성. 새 deep 후보 `cand_241362295c715dee8d938e53d7a6b1fa`에서 선택적 일반 영감으로 가져온 낮은 대비의 의복 주름 음영은 보이나, 전체 밝은 배경 관계는 관찰되지 않았고 native 전체 후보 채택은 0이다. 전체 인상은 단정한 제복 화보로 강도 3이 주도한다고 보기 어렵다. 리뷰 기록은 유효하지만 발 지지 및 일부 팔 경로가 프레임 밖이라 기술 적합성은 fail이다. `generated/photo-runs/nurse-deep-20261107-fetish/pixel-review-observed.md` 및 `review-audit-result.json`.
- creativity=3, 다른 설정 기본값: `generated/nurse-deep-research-20261107/api-results/4ec08e98a4fa43d98d890f02a6af3a3e/result.png` 1회 생성. 독립 baseline과 다른 전경 유리·커튼 동작의 전체 재구성을 작성했다. 새 후보 A-DEEP-014 `cand_f4704f6031b4578e9c84dfd446a23a3a`에서 영감을 받은 접힌 칼라는 보이지만 전체 source/native 채택은 0이다. 리뷰 기록은 유효하고 발과 바닥 접촉이 프레임 밖이어서 기술 적합성은 fail이다. `generated/photo-runs/nurse-deep-20261107-creativity/pixel-observation.md`, `visual-review.json`, `review-audit-output.json`.

후보의 검색·부분 영감·픽셀 관찰과 전체 source/native 적용은 다르다. 세 실행 모두 원본 대조 이미지를 생성하지 않아 인과적 개선 및 사용자 선호는 판단하지 않았다.

### 외부 출처 미확인 280행 후속

280행 전수의 이전 판정과 원문을 유지하고, 이 중 244행에 한정된 추가 출처를 연결했다(기본 검토 194행, 별도 보충 22행과 28행). 남은 36행은 새 외부 근거가 없으며, 출처가 있는 행도 전체 의미나 해당 동작 전체가 검증됐다는 뜻은 아니다. 보류 285행은 280행에 포함된다. 용어 뜻을 문헌에 연결하고 앞치마 단독 시각 사례와 진단을 분리했지만 전신 의복 부재와 나이는 여전히 관찰 불충분이다. 맥락 뷰 280개는 연구 전용이며, 선택적 시각 후보 26개·binding 26개·양성 뷰 52개 및 진단 1개는 전수 시각 완결을 뜻하지 않는다. 진단은 양성 검색에서 제외한다. 개별 지원 범위와 미해결 조건은 `nurse-uniform-external-20261107/README.md`와 assets의 해당 검토·보충 파일을 참조한다.

H-F2 세대 `eae571b44cbd70ff9a7610ca6b9f9043322077f5c16f1967f174f737b68674ae`, native `12d105d04df909c8187468cf25d720c380cb3ad823f6fd2e0f94f39aa30d1056`를 임베딩·봉인하고 설치 검증 후 기본 설정으로 선택했다. 추가 양성 문서는 26개, 양성 검색 뷰는 52개다. 보류 285 진단 CID는 봉인된 양성 문서와 뷰에서 모두 제외됐다. 작업 소스 27,998개 후보 및 25,229개 binding의 ID는 설치 소스와 일치했고, 이전 설치본에만 존재한 별도 role_evidence 1건을 그대로 보존했다. CURRENT는 쓰지 않았다. 저자 인지 개발 질의 6개에서 목표 후보가 모두 1위였으나 이는 독립 검증이나 픽셀 품질을 뜻하지 않는다. 자동 검사는 20개 통과, 12개 스킵, 4개 하위 검사 통과했다.

### 마지막 36행과 보류 1행의 외부 근거 보충

이전 단계에서 새 외부 출처를 확보하지 못했던 36행과 별도의 285 보류행 총 37행에 대해 관련 자료를 추가했다. 일부는 복합 용어의 한 요소나 한 사례만 뒷받침하며, 사전 의미의 확인과 시각적 입증은 구분한다. 연구 맥락 37개, 선택적 시각 후보 25개, 신규 진단 후보 3개, binding 25개, 양성 뷰 50개를 추가하고 기존 후보 7개를 8행에 부분 연결했다. 262·263·264·285의 진단은 양성 검색에서 제외된다. 285의 가려진 의복 부재와 연령을 사진 한 장으로 확인할 수 없다는 보류는 유지한다. 개별 출처와 연결은 `nurse-uniform-final-followup-20261107/README.md`에 기록했다.

검색 릴리스 `d737e9d8c1ba5e037c255ddfab896c66c41b83aa3ca228c7314fc9bffc21ce2e`, native `8b892a9a4353d9225d0edd4cc9724bafe7d99516fac5c51a00d171a1f6c50a12`를 이전 봉인 뷰 26,877개와 새 양성 문서 25개·뷰 50개로 구성해 임베딩·전체 봉인·설치 후 기본 설정으로 활성화했다. 네 진단은 양성 문서와 뷰에 없다. source ID는 후보 28,026개, binding 25,254개가 일치했으며 이전 설치본의 role_evidence 차이 한 건을 보존했다. 개발자가 답을 아는 상세 질의 6개 목표는 각각 1위였다. 짧은 용어 질의 네 개는 단서 보강 전 110·34·1·70위에서 40·5·1·5위로 바뀌었다. 첫 질의는 여전히 40위다. 테스트 22개 통과, 12개 스킵, 4개 하위 검사 통과. 이미지 생성은 없었다. 구형 검토 뷰 기준 중 1,250개가 현재 후보와 해시 불일치해 표준 과거 오버레이 전체 재생은 통과하지 못했다. 현 활성 직전 봉인본을 기준으로 한 뷰 결합만 통과했으며 과거 의미 동등성을 주장하지 않는다.
