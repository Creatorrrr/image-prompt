# 흙·땅 데이터 반영과 독립 이미지 검증

2026-10-08 KST · 기존 리서치 후속 실행

## 원본에 반영한 내용

후보 96개와 시각 의미 프로필 96개를 새 원본에 등록했다. 한국어·영어 관찰 표현, 소유 대상, 방향 있는 관계, 혼동 경계, 변경하는 속성을 작성했다. 프로필의 288개 픽셀 의무는 선택한 전체 구현을 검사하며, 출처의 과학·문화 분류나 냄새·의도를 외형으로 판정하지 않는다.

- 후보: `skills/photo-prompt-image-generator/assets/photo_prompt_soil_earth_extension.json`
- 시각 의미: `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_soil_earth.json`
- 등록: `photo_prompt_source_manifest.json`에 후보·프로필 원본 2개를 추가했다.
- 재사용: 건열·샘·우각호·망상하천·육계사주 후보와 프로필 5쌍의 기존 ID를 유지했다. 후보는 새 extension의 equivalent context 보강으로, 프로필은 기존 물 원본의 paraphrase 추가로 반영했다.

전체 연구 단위 120개에 신규·동등 보강·공유 구현·문맥 유지 결정을 기록했다. 기존 얼음 쐐기·빙하 가장자리·골렘 인접 항목은 owner와 전체 의미가 같다고 간주하지 않고 필요한 별도 물리 구현으로 작성했다. 밝은/어두운 토양 띠의 E018/E023은 동일 물리 구현을 공유한다. 봉분과 석실, 둥근 자갈과 각진 쇄석, 판상/주상 입단, 습곡/단층, 코일/판 성형은 변형을 분리했다.

일반 사진용 모래·흙 단면·토색·도랑·사련에는 조사용 눈금자나 색 기준표를 강제하지 않았다. 의복 진흙 후보는 기존 천의 봉제선·주름·광학 속성을 유지하며 표면 부착물을 보강한다. 피부 위 손가락 자국은 과거 흔적으로 표현하고 현재 손의 접촉을 자동 추가하지 않는다.

## 발견과 의무의 경계

넓은 ‘흙’·‘진흙’·분류·다의어는 특정 전체 외형의 exact alias로 등록하지 않았다. 선택적 발견은 한국어·영어 구성 표현을 사용한다. 43개 프로필에는 소유 관계가 있는 짧은 관찰 표현도 추가했다.

`authored_components/v2`의 collective 의무는 주요 물리 형태를 포함한 2개 구성 그룹에서 선택적 발견을 허용한다. 실제 선택하면 3개 evidence와 3개 gate가 모두 필수다. v1→v2 정리에서 evidence requirement, instruction, native gate의 바이트와 순서를 유지해 검증했다. 발견 조건을 만족했다는 이유로 누락된 픽셀 의무를 제거하지 않는다.

프로필 exact proposition과 semantic paraphrase는 분리했다. 초기 전역 dictionary 검사에서 중복된 exact/semantic 표현을 발견해 수정했다. 수정 전 검사 로그도 보존했으며 최종 검사는 통과했다. 초기 회귀 실행에서 인덱스 갱신 중 발생한 stale registry 오류는 최종 인덱스·runtime 검증 뒤 재실행해 통과했다.

## 검증과 게시

- [최종 데이터 대응표](integration-final.json): 연구 단위별 실제 candidate/profile ID, 재사용·보류, 원본 해시, 게시 정보.
- [원본 dictionary 검사](dictionary-validation-final.log): PASS.
- [visual index 깊이 검사](visual-index-check.log): PASS.
- [관련 회귀 27개](focused-regressions-final.log): 흙·물 관계, 후보 의미, 다의어·부정, 속성 잠금, 기존 ID/효과 보존.
- [런타임 게시](runtime-publication-final.log): 검증된 새 generation을 완료했다.
- [작업공간 지문 비교](preservation-check.json): 초기 파일 4,763개의 변화와 기존 물 원본/manifest의 보존 범위.

semantic index와 visual index는 canonical builder에서 갱신했다. 기존 벡터는 entry key·전체 입력 텍스트·provider·model·차원이 같을 때만 재사용했고 새/변경 텍스트는 batch size 1로 임베딩했다. 기존 shard generation은 유지했다. 인덱스 전체 count에는 기존 및 동시에 진행되던 작업 원본이 포함되므로 이번 추가 수량과 구별한다.

이 통과 기록은 데이터 계약·검색 무결성·런타임 세대의 증거다. 이미지 품질과 사용자 수용의 증거는 별도 이미지 검증 결과에 기록한다. 이 작업에서는 commit/push/PR을 수행하지 않았다. 최종 전달 시 공유 HEAD 이동이 관측됐으며, 원본 지문·보호 파일 내용을 재대조한 [최종 기록](../image-tests/parent-final-validation.json)과 [HEAD 관측](../image-tests/parent-head-observation.json)을 별도로 보존했다.

## 독립 이미지 테스트

사용자 원문과 active spans를 부모가 서브에이전트 실행 전에 동결했다. 세 에이전트는 `fork_turns=none`으로 시작했고, 다른 arm이나 연구/후보 자료를 보기 전에 현재 neutral controls·일반 지식·참조 사진으로 무작위 컨셉과 독립 core를 작성했다. seed와 후보 가능성, 선택 결과, baseline hash를 각 arm에 기록했다. 저장 controls를 변경하지 않았으며 부모가 개별 프롬프트를 제공하지 않았다.

각 arm의 작성 영역은 중복을 줄이기 위한 에이전트 탐색 범위다. 이를 요청자가 정한 의복·행위·카메라·하드 의무로 승격하지 않았다. 테스트 기대도 에이전트 소유의 관찰 계획과 실제 pack의 하드 의무로 구분했다.

| arm | 탐색 영역 | 독립 컨셉 |
|---|---|---|
| 1 | 야외 실제 현장 | 비에 손상된 클레이 코트를 수동 롤러로 복구 |
| 2 | 실내 제작·복원 공간 | 흙 안료 작업실에서 부서진 흙 미장 부조를 복원 |
| 3 | 시간감·공간규모가 다른 허구 장소 | 미래 세대 우주선 온실에서 토양 유실과 노출 뿌리를 복구 |

[공통 요청·참조 지문](../image-tests/COORDINATOR.json), [게시 완료 통지](../image-tests/READY.json)에 근거해 각 arm이 post-core 후보 검토·최종 프롬프트 감사·native 이미지 호출·저장·픽셀 심사를 완료했다. 실제 후보 노출/선택/프롬프트 evidence는 각 arm의 `DATA-CONTRIBUTION.json`에 남겼다. baseline에 이미 있던 물리 의미와 데이터가 보강한 부분을 구별했다.

첨부 사진은 얼굴과 머리카락의 보이는 외형 참고이며 정체성·성격·생애의 근거로 쓰지 않았다. 이미지 도구는 native `image_gen`을 사용하고, 결과의 실제 로컬 경로·정확한 runtime bytes·ledger·독립 manifest를 보존했다. 기본 1회, 실제 픽셀 실패에 한해 최소 범위의 추가 1회를 허용했으며 실제 호출은 각 1회, 총 3회였다. 부분 구현은 fail이며 사용자 수용은 직접 판단을 받기 전까지 pending이다.

세 이미지 모두 흙 주제와 참조 외형을 확인했다. 신규 후보는 부조의 토색 E021과 우주선 온실의 같은 식물 뿌리 연결 E081에서 채택됐고 각각의 성분이 원본 픽셀에 보였다. 코트의 자체 기대는 6/8, 부조는 7/8, 온실은 8/8을 통과했다. 코트의 물길·입자 분급과 부조의 안도 표정은 fail을 보존했다. 신체 하드 게이트는 15/15지만 신규 흙 프로필은 실제 후보팩에서 선택되지 않았으므로 프로필 활성화·96개 전체 렌더 효과를 검증했다고 주장하지 않는다.

최종 이미지/관찰/실패/미수행 항목은 [독립 테스트 종합 결과](../image-tests/qualification-report.md)에 모은다.
