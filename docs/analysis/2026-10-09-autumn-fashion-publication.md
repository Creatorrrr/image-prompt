# 가을 패션 데이터 main 반영 검증

가을 조사·통합·독립 이미지 테스트의 원본을 `f44d8cc4b55def2c095b06d102027407877eaedc`로 먼저 커밋했다. 부모는 `f081ac7305210def8348cc76d3a8f9f48393b4de`이며, 별도 작업 폴더에 있던 무관한 미커밋 변경 13개는 포함하지 않았다. ZIP 보존 백업과 중복 런타임 저장소도 배포 범위에서 제외했다.

그 다음 깨끗한 발행 워크트리에서 `git pull --no-rebase --no-commit origin main`을 실행해 `440edec6b6efa5c34146785b1dc6016cf8e5f24d`를 합쳤다. 충돌한 source manifest는 원격의 128개 등록 행과 순서를 그대로 유지하고 가을 source 2개를 덧붙였다. 원격의 등록 source 128개는 바이트 단위로 동일하다.

원격 semantic identity 11,616개는 삭제 없이 유지했다. 그중 11,599개는 완전히 동일하고, 기존 후보 17개에는 가을 조사에서 검토한 paraphrase와 해석 문맥만 추가했다. 제약·효과·소유자·기존 문맥은 그대로 보존했다. 가을 후보 112개가 추가됐다. 원격 시각 프로필 3,369개는 완전히 동일하며 가을 프로필 112개가 추가됐다. 이를 다시 컴파일한 인덱스는 semantic 11,728개, visual profile 3,481개, active shard 32개다.

원격 캐시, 가을 테스트 캐시, 기본 작업 폴더의 캐시에서 identity·전문·provider·model·차원·recipe가 일치하는 벡터만 재사용했다. 기본 작업 폴더의 다른 미커밋 source는 가져오지 않았다. 양쪽 변경이 함께 적용된 drop-shoulder·racerback·cross-back 후보 3개만 새로 임베딩했다. 배치는 1이며 visual profile 임베딩은 0회다.

사전 검증과 실제 인덱스 검증은 통과했다. 봄·여름·가을·fit 및 인덱스/후보 계약 회귀 98개도 모두 통과했다. 결과는 [발행 검증 자료](../research-evidence/photo-prompt/autumn-fashion-main-merge-20261009/)에 보존한다. 이 문서는 머지 직전의 검증 범위를 기록하며, 최종 푸시·기본 main 동기화·워크트리 정리 결과는 같은 폴더의 로컬 DELIVERY.json에 별도로 기록한다.

통합 runtime generation: `d8303e2f33500233c6778116bcc2bfadcbc4acbd170ec4cbc3e54b378c3a35ec`. Source fingerprint: `12e355b8e4c3d08fc87bab7bfaaa9592ddb6bd544037d959f02a0f520d2d9dbb`. 기존 이미지 3장의 generation은 변경하지 않았다.

이미지 테스트 판정도 그대로 유지한다. 실제 native 생성 3회 중 1번의 hard gate는 8/8, 2번은 6/8, 3번은 6/9였다. 2번·3번의 인과 행동과 의복 관계는 실패했고, 새 autumn visual profile이 실제 채택된 사례는 없었다. 347개 용어 전체나 신규 프로필의 이미지 반영을 통과로 인증하지 않는다. 사용자 판단은 아직 받지 않았다. 자세한 실패·선택·이미지·원본 프롬프트는 [통합 및 native 테스트 보고서](2026-10-09-autumn-fashion-integration-and-native-tests.md)에 있다.

기존 전체 suite의 실패와 환경 의존성 분류는 앞선 보고서와 원본 로그에 유지하며, 이번 발행 검증을 전체 suite 통과로 확대하지 않는다. 푸시에는 검토한 가을 원본·테스트·증거와 합쳐진 source manifest/파생 인덱스만 포함한다. 기존 기본 작업 폴더의 무관한 dirty/untracked 경로는 SHA-256·권한으로 보호한다.
