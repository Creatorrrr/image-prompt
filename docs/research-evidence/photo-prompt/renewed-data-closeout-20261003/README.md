# 두 번째 24시간 DATA 개선 작업 — 12:25 UTC 검증 현황

이 보고서는 2026-10-03 12:25 UTC 기준 확인된 결과입니다. 작업 구간은 아직 종료되지 않았으며 종료 예정 시각은 아래와 같습니다.

예정 기간: 2026-10-02 22:52:49–2026-10-03 22:52:49 KST. 이번 연장분만 집계합니다.

## 현재 확인된 결과

- 검증 후 게시한 DATA cycle 29개
- 레코드 편집 사건 56회, 중복을 제거한 대상 53개
- 고유 대상은 프로필 51개와 슬롯 행 2개입니다. 같은 레코드를 재검토한 경우가 있으므로 위 두 수치는 다릅니다. 조사만 한 KEEP·보류·문서 작업을 수정 수로 세지 않았습니다
- 마지막 확인된 게시 SHA: `fcb7f88920fbca0e65b892d2774faa84e74a7cb2`
- 검색용 문장이 바뀐 경우 실제 벡터를 갱신하고, 게이트/표현만 바뀐 경우 모든 기존 텍스트·벡터/BM25F를 보존하며 source fingerprint만 갱신했습니다

이번 작업의 대부분은 기존 의도에 맞게 설명·소유관계·조건·원래 허용된 대안을 정렬한 것입니다. 새로운 키워드 수를 무조건 늘리지 않았습니다. 원문이 이미 허용한 대안의 누락을 복구하면서 필수 의무와 별도의 누락·충돌 음성 대조를 보존했습니다. 일부 허용 경로를 넓힌 수정이 있으므로 모든 검사 조건이 동일했다고 주장하지 않습니다. 이 수치는 채택한 DATA 수정 주기 수이며 검색·이미지 품질 향상 건수는 아닙니다. 후보 검색 정확도나 생성 이미지 품질이 전반적으로 향상됐다고 단정하지 않습니다.

일부 같은 입력에서는 주변 선택 후보의 순위·구성원·설명 목록이 바뀌었습니다. 차이를 기록하고 해당 대조 구성에서 무관한 후보를 채택하지 않았으므로, 전체 검색 무퇴보나 이후 작성자의 선택까지 같다는 증거는 아닙니다. 일부 주기는 전후 감사 통과율이 같고 출력 지시의 내부 모순만 줄였습니다. 주요 분기 검증은 원문을 참고한 합성 정규 사례이며 자연어 전반의 검색률 개선을 입증하지 않습니다.

## 게시한 수정

1. 악기 연주 손 역할: 2개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/ebd10bcb9bfd963d585cc4bdacf6e28cbe19940c)
2. 촬영 프로필의 양성 설명 경계: 7개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/a21a08cb6e95fda0dd8f430fe68481878e5ea581)
3. 조명·구도 양성 설명과 완전한 paraphrase: 7개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/56fa035716021c9129e310141a8facb4c2162126)
4. 패닝의 요청된 방향: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/57e29730f0b5c2df336fd1e9dd58374b2025ee03)
5. 남은 양성 설명의 자기 배제: 7개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/904b5893c94e2d59d646e977c8400e270635a568)
6. 롤링셔터 동작 소유와 분할 초점: 2개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/2549f45230fe37dbc4224929b0d661ceac8004cc)
7. 무기 형태의 사람·방향 조건: 2개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/6adabfe4cf9255733686d61c5bff3288a7ef8138)
8. 받는 재료별 빛 반응: 2개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/326a9321c93d7fe5b484fb62fff6d3d393ed46c7)
9. 오버헤드 장면의 가까운 손 대안: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/1feea7ceb7ec55b34aaf0c521a0c56714dcfa2e7)
10. 리딩라인의 리듬 정렬 대안: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/99ebda65bab0efbf6476ce222ab40391494dc25f)
11. 유령·의복·수선 양성 설명 대안: 3개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/b85dcbca17156526e0a61b24e34a2c77829c06aa)
12. 랩스커트 옆 겹침: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/7a98e2dcf18a9d60e3505b71e735b88543a99b24)
13. 케바야 가벼운 직물: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/cad6f90549d9fd6348310a71a23025f003fd00d6)
14. 젖은 머리의 무게로 내려오는 대안: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/7bc6d8bc759f9c14da95afc8be54bca44caf3830)
15. 습지 포화·사구 모래 이동: 2개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/dbfd897ce20b5c7c21456af2234ec140e42676a9)
16. 빙하 표면의 방향 단서: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/ef0ea3f6a396d06bad42b92bfe7915f71089a5a5)
17. 적란운의 줄무늬 모루: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/fb21b964f0f740e6cf846df89154e603a1280b00)
18. 할버드·쇠뇌의 조건부 손 접촉: 2개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/5330300e31684f495510470de08221d4e9279416)
19. 원피스 양성 설명: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/4f992caf73099cf677b65ebb59e73fb817d2bbd2)
20. 바이오하이브리드 증거·소환의 국소 결과: 2개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/8c1bc9a0269c20bc63862f994acfd22d6bd2345c)
21. 리미널 공간의 관리된 흔적: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/7d1bb2a5104198804512b2b93082f9a100ee7238)
22. 같은 성인이 같은 음식 원천을 배분: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/978f38defbc70ea47dbd028af47baf701eada1bd)
23. 격자 투사 그림자: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/6b9381a0585049cbaca1522dde405b4e6203b295)
24. 아세테이트 필름 왜곡 단독 증거: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/5bf8142304f484138474fff4af9b0660439fa331)
25. 사진 슬라이드 필름 두께: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/2c4e06ea9ea5f98f8d82c115a6ee354d5d180766)
26. 유령선 국소 투명화: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/280ea12de8c2886a6cf160ccc7bbf05e7be32e16)
27. 표국 운송 수단별 경로: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/53de56524d69b5c6597a74328e663aef03653a3a)
28. 오로라 대기 기준과 기존 지평선 표현: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/120f07d025340bd067097f947ca23d4dd828e7cf)
29. 꿈 논리 단절의 패턴·문턱 비교: 1개 레코드 편집 — [커밋](https://github.com/Creatorrrr/image-prompt/commit/31dbed9f0d22af97025cebcbceffc07b4250de35)

## 검증과 남은 한계

고정 `120f07d0` 전체 발견 실행에서는 149개 모듈의 1,302개 ID를 빠짐없이 실행했습니다. 1,297개 메서드가 성공했고 5개 과거 실패 메서드가 동일하게 남았습니다(10개 assertion/subtest 실패와 1개 파일 오류). skip·새 실패·정규화 traceback 변경은 없고 추가된 18개 메서드는 모두 통과했습니다. 전체 green이나 이후 main/새 런타임의 전체 검증이라고 부르지 않습니다.

`31dbed9f`의 별도 파일 존재 검사에서도 같은 참조 파일들이 여전히 존재하지 않았습니다. 이는 현재 전체 suite 실행을 대신하지 않습니다.

후보 자료를 보지 않은 새 작성자의 합성 입력 8개를 동결한 대조에서는, 사전 조건을 충족한 4개의 팩이 DATA25–29 유무에 관계없이 바이트 단위로 같았습니다. 나머지 4개는 원래 문장의 사전검사 거부를 그대로 유지했습니다. 실행 가능한 표본에는 수정 대상이 노출되지 않았으므로 일반화 향상이 아니라 제한된 부수 안정성 증거입니다. 이미지 생성/픽셀 품질 증거는 아닙니다. 초기 장면 작성자는 후보를 보지 않았지만 이후 메타데이터 구성은 소스를 아는 작업자가 수행했습니다. 사물 사례 두 개는 모두 사전검사에서 차단됐으며 실행된 네 구성은 선택 보강을 채택하지 않은 기준 구성이고 각 구성에 기존 coverage 경고 3개가 남았습니다. 따라서 전체 pre-core 경로의 독립 블라인드 평가로 해석하지 않습니다.

독립 upstream의 종교 도상 54개는 157개 의무를 보존해 KEEP했습니다. 조명/반사 8개와 별도 축음기 사례도 무리하게 넓히지 않았습니다. 기존 어휘 검사만으로 실제 물리나 픽셀 관계를 확인할 수 없고, 일부 부분적인 paraphrase는 advisory 후보를 찾는 데 사용되므로 그것을 완성된 장면 증거로 세지 않습니다.

기존 악기의 정물/연주 범위, 일부 원래 상향 시점·속성 잠금 문제 등은 별도 런타임 또는 추가 원문 판단이 필요한 과제로 구분합니다. 별도 Codex Cloud 런타임 개발은 이 DATA cycle에 합산하지 않습니다. PR4의 상향 시점 런타임은 `fcb7f889`에 합류했습니다. 기존 알려진 사례는 0→2, 별도로 교정된 사례는 1→1이고 한 motion 후보가 밀려났습니다. 새 V2 대조의 양성은 두 버전 모두 0/6, 음성 abstention은 모두 8/8이며 KO_TWO의 core 사전검사 거부도 양쪽에 남았습니다. 따라서 전반적인 재현율 향상은 입증되지 않았습니다. PR4의 별도 전체 실행 보고는 1,341개 중 1,336개 메서드 성공, 과거 누락 자산 관련 5개 실패입니다. 이것을 이번 DATA 대조의 성과로 세지 않습니다.

최신 `fcb7f889` 합류 후에는 DATA25–29 다섯 모듈, 현재 경계 두 모듈, 카메라 의무 18개를 포함한 8개 모듈의 51개 메서드가 모두 통과했습니다. 486개 소스 해시와 HEAD는 실행 전후 같았습니다. 별도의 현재 인덱스 검사에서도 1,564개 프로필·9,819개 일반 항목의 텍스트·결합·BM25F·16개 shard와 768차원 유한 벡터가 검증됐습니다. 이 검사에 추가 provider 호출은 없었고 PR4에서 자산/임베딩 입력 변경도 없었습니다. 벡터 수치만으로 제공자 출처를 재구성하거나 최신 전체 suite가 모두 성공했다고 주장하지 않습니다.

## 비용

이번 연장분의 보수적 요청 예약 증가: $0.0933888. 전체 프로젝트의 기록된 요청 추정은 $1.4385152입니다.

과거 SDK 전송 재시도 불확실성 준비금 $5.7081856를 따로 합치면 계획 상한은 $7.1467008, 기존 $10 한도 내 여유는 $2.8532992입니다. 이는 실제 청구액이 아니며 독립적인 다른 작업/계정 사용료는 포함하지 않습니다. 이 루프에서 전송 재시도 불확실성을 인지한 뒤 실행한 임베딩 유지보수 요청은 SDK 전체 전송 시도 제한을 1로 두었습니다. 일반 런타임의 모든 미래 요청 정책을 바꿨다는 뜻은 아닙니다. 실패·불확실·사전검사 차단 기록도 비용 추정에서 임의로 지우지 않았습니다.

## 합류와 게시

다른 작업의 기존 프로필/후보 확장은 별도로 보존했습니다. 예를 들어 종교 도상 합류의 신규 54개 프로필·80개 후보 및 기존 보강은 이번 loop가 만든 항목이 아닙니다. 실제 source/index 검증과 레코드별 합류 검증을 수행하고, 이전 벡터를 쓸 수 없는 텍스트 변경은 새 벡터가 있을 때만 게시했습니다.

마감 확인에는 최신 origin/main, 작업 트리, source/index 결합, 미완료 provider 요청 유무, 비용 기록 및 CI 실행 여부를 다시 확인해야 합니다. 이전 CI 조회에서는 실행이 없었으며 이를 CI 성공으로 표현하지 않습니다.


## 추가 KEEP 검증

독립 upstream의 종교 도상 54개에서 작성된 양성 문구 772회(고유 profile/text 쌍 497개)를 점검했습니다. 자기 배제·자기 alias 부정·자기 프로필 발견 누락은 없었고 완전한 양성 108개는 정확한 hard eligibility를 보존했습니다. 명시적 전체 alias 음성 54개는 모두 차단됐습니다. scoped registry와 full registry 결과는 같았습니다. 이 실행은 `bcb671ba`의 이미 로드된 코드/데이터를 사용했고, 마지막 live-file 해시 검사가 실행 중 `fcb7f889` 합류를 탐지해 실패했습니다. 직접 점검한 네 helper의 AST는 두 커밋에서 동일합니다. 이 사실을 현재 CLI 재실행 성공으로 바꾸어 해석하지 않습니다. 수정할 근거가 없어 54개 모두 유지했습니다.

## 증거 묶음

- [추가 검증 증거](closeout-evidence.tar.gz)에는 최근 합류의 51개 테스트, source/index 검사, 양성 경계와 조명·축음기 KEEP, 회계 검증 및 다음 작업 검토가 들어 있습니다
- [파일 개수·해시](archives.json): archive 내부 publication-manifest.json으로 게시 바이트를 확인할 수 있습니다
- 큰 pinned-source 사본은 제외했으며 저장된 커밋·원래 해시 목록으로 원본을 확인할 수 있습니다
- 공개용 경로를 REPOSITORY_ROOT/EVIDENCE_ROOT/WORKSPACE_ROOT 및 외부 사용자 홈 자리표시자로 정규화했습니다. 원래 실행 manifest와 공개용 바이트 manifest는 구별됩니다
- [다음 작업 우선순위](NEXT_WORK.md)는 추가 실행 승인이나 이미 해결된 결과를 뜻하지 않습니다
