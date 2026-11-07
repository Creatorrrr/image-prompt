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
