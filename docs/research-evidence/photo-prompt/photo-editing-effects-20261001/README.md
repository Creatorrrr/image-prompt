# 사진 편집 용어 리서치와 데이터 반영

후속 요청에 따라 운영 데이터에 후보 133개, optional bundle 28개, 시각 의미 프로필 22개를 추가하고 두 검색 인덱스를 갱신했다. 독립 에이전트 3개가 서로 다른 복잡한 장면에서 프롬프트 작성·이미지 생성·원본 픽셀 검토를 완료했다. 최종 효과 **5/9 PASS**, 장면 전체 **1/3 PASS**, 테스트 후보 노출·선택 **10/10**이다. 현재 적용 내용과 남은 혼동·검증 계획은 [반영 보고서](implementation-report.md), [245행 이행 원장](implementation-disposition-ledger.json), [독립 3개 이미지와 판정](qualification/README.md), [169항목 무결성 원장](qualification/coordinator-review.json)에서 확인한다.

최초 조사에서는 참조 대화의 키워드 표 245행, 설계 의미군 88개, 확인 자료 54개를 연결했다. 당시 merged 데이터에서 재사용할 프로필 17개를 확인했고, 별도 연구용 후보 25개·조합 6개와 후속 통합 검증 사례 42개를 준비했다. 아래의 조사 보고서와 최초 계획은 반영 전 기준 자료이며, 최종 운영 반영·이미지 결과와 구분하여 보존했다.

- [조사 보고서](research-report.md): 용어의 의미·혼동 경계·현재 데이터 공백·출처와 관찰 범위.
- [반영 계획](implementation-plan.md): 우선순위, 변경 파일, 검증·인덱스·픽셀 평가의 순서와 완료 기준.
- [245행 매핑](keyword-matrix.md): 모든 원문 키워드의 적용 영역·우선순위·출처 및 88개 그룹 설명.
- [검토 결과](research-validation.json): 연구 artifact·분리된 구조 검사 35개, context helper probe 7개, 운영 소스 hash 확인.
- [연구용 runtime 초안](runtime-projection-draft.json), [provenance](prototype-provenance.json), [예정 검증](validation-plan.json).
- [출처 원장](sources.md), [참조 대화 수집 기록](reference-conversation.md), [원문 표](reference-keywords.json).

최초 조사에서는 운영 자산·인덱스를 변경하지 않았다. 당시 source helper에서 공존 조합 3개가 거절되는 근거를 확보했고, 이번 반영에서는 독립 효과의 공존과 대체만 요청한 문맥을 구분하도록 제외어를 좁혔다. 이미지 생성·픽셀 충족·사용자 수용은 데이터 검사와 별도 상태로 기록한다.
