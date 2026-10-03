# 서브컬처 외형 보강 pull·보존·push 검증

`git fetch origin` 뒤 `git pull --no-rebase --no-edit`를 실행했다. 원격과 로컬은 모두 `8077d5108cbf67a1b0b276056ed330e2bcba6e8e`로 이미 일치해 새 충돌은 없었다. 현재 원격의 의미와 이번 대체 표현 보강이 함께 남는지 별도로 검사했다.

[원격 보존 검사](UPSTREAM-PRESERVATION.json)는 원격의 프로필 1,576개와 일반 후보 9,795개가 모두 남아 있음을 확인했다. 기존 36개 프로필은 긍정 대체 표현만 늘었고, 정의·활성화·owner·잠금·게이트·최소 증거는 그대로다. 기존 35개 후보도 대체 표현만 추가했다. 새 프로필 46개와 후보 45개는 별도 안정 ID로 유지했다. 생성기 소스 변경은 공통 로더의 두 파일 등록뿐이다.

사진 회귀 기준 V1–V8은 원격 바이트와 동일하다. V9은 현재 후보팩 관찰을 연결하며 네 동결 입력과 장면 계약을 바꾸지 않는다. universal oracle은 validator 바이트 해시 외에는 변경하지 않았다.

시각 의미·후보 인덱스는 앞선 반영에서 재생성한 데이터다. pull로 입력이 바뀌지 않았으며, 현재 로더와 두 인덱스의 일치 검사를 다시 통과했다. 전체 회귀 테스트 1,362개를 통과한 이후 source와 asset 해시도 그대로다. pull 후 추가한 [핵심 재검증 8개](POST-PULL-TARGETED.log)가 통과했다. 큰 생성 인덱스를 ours/theirs로 선택하지 않았다.

커밋 범위는 이번 시각 의미·후보 반영, 연결된 연구와 세 독립 원본 이미지 시험, 회귀 이력, 현재 인덱스가 참조하는 16개 shard와 이 검증 기록이다. 별도 종교 연구의 임시 replay와 현재 인덱스가 사용하지 않는 이전 shard 세대는 포함하지 않는다. 원본 연구·이미지 시험의 실패와 미확인 사용자 수락도 그대로 보존한다.

[반영과 이미지 시험 상세](../subculture-appearance-integration-20261003/README.md), [완전한 테스트 집계](../subculture-appearance-integration-20261003/TEST-RESULTS.json), [보존 검사 스크립트](verify_upstream_preservation.py)를 연결했다.

커밋 직후 두 번째 pull에서 원격 마감 커밋 `37bc654e6116131cd3fb7030a41ae203082480e1`의 문서·archive 6개가 추가되어 자동 머지됐다. 로컬 반영 커밋 `34f1efff3d8e1159ff1ce02881ddea732ce1f015`와 원격 마감 커밋을 두 부모로 보존한다. 양쪽 변경 파일은 각 부모 바이트와 동일하며, runtime source와 83개 asset은 전체 1,362개 테스트 당시 해시와 계속 일치한다. [최종 양쪽 부모 보존 검사](MERGE-PARENT-PRESERVATION.json)를 기록했다.
