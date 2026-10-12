# 6단계: 동일 입력의 fusion·후보 한도 진단

기준선은 5단계 완료 커밋 `a9a211f6617d9ee37567106296855f30396faa7c`이다. 기본 작업 폴더의 다른 수정과 현재 runtime store는 건드리지 않는다. 진단·수정은 별도 관리 작업 폴더와 이 디렉터리의 격리 store를 사용한다.

1. 기존 native alias 고정 사례 20개, 자연어 development 8개·holdout 12개와 원래 `ranking_fusion_or_shared_cap` 49개 probe의 원본 bytes와 정규화된 core/controls를 먼저 고정한다. 자연어 필요 후보 기준 13개와 기존 subject 의미 판정도 고정한다. source 유래 probe는 독립적인 자연어 품질 평가로 합산하지 않는다.
2. 현재 구현을 그대로 재현한 private trace를 실제 `retrieve_core_slots` 결과와 대조한다. eligibility, owning focus, broad/focal pool, RRF, frozen observation, 대표 후보, 슬롯 한도, 전체 admission 중 탈락 위치를 기록한다.
3. 같은 core, source, ranker, caps에서 대표 후보 선택과 observation/admission을 하나씩 바꾸어 비교한다. 의상 2개 영문 사례와 49개 과거 probe의 현재 원인을 확인한다. 주체 잔여 2개는 source/context 문제라면 순위 조정으로 가리지 않는다.
4. 근거가 있는 범용 수정만 채택한다. 대상 ID·언어·주제 whitelist와 새 필수 후보, 기본 padding, quota를 추가하지 않는다. 전체 64, core 4, support 2를 유지한다. scores/ranks/trace는 private 유지보수 증거에만 저장한다.
5. 고정 입력 public CLI, composer view, source 재계산, omission tamper, core 불변·caps·adjacent negative를 검사한다. owner/context·lock·empty/rejected·밀집/희소 회귀와 필요한 전체 unittest discovery를 실행하고 기준선 실패는 같은 A9에서 재현한다. tokenizer/source/index/vector 변경 여부도 확인한다.

완료 조건: 입증된 필요한 후보의 같은 cap 내 노출 개선, 자연어 필요 후보 13개 손실 0, frozen subject 의미 및 holdout 경계 악화 0, adjacent negative 오노출 0, core·lock·optional/public private-field 경계 위반 0. 개선 근거가 없으면 해당 조정은 채택하지 않는다. 7단계의 composition 및 runtime 통합 반영, 이미지·픽셀·사용자 선호 검증은 이 단계 완료로 주장하지 않는다.
