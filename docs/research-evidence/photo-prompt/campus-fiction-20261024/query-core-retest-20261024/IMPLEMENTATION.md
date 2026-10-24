# 검색 질의와 코어 소유권 개선

사용자 요청: 실제 캠퍼스물 신규 후보가 같은 참조 이미지와 최신 스킬을 쓰는 독립 서브에이전트 3개에서 프롬프트와 픽셀까지 전달되는지 재시험한다.

## 적용한 수정

- `photo-request-query-scope/v1`: 사용자 원문과 활성 구간을 바꾸지 않고 정확한 원문 구간에 visual/topic_reference/reference_use/workflow 용도를 검토해 기록한다. 주제 발견에는 시각 요구와 정확히 인용된 이전 사용자 주제만 전달한다. 실행·참조 전달 문구는 봉투에 보존한다. 부정·설정 firewall, baseline 및 슬롯 질의는 유지한다.
- 생성기와 독립 감사기가 scope와 이전 사용자 문맥을 같은 봉투 해시로 재구성한다. 변조된 구간·문맥·hash를 거절한다.
- `photo-requester-ownership-review/v1`: 새 managed freeze는 모든 requester anchor와 모든 agent_visual_choice category의 구체 atomic literal 검토를 요구한다. 긴 필수 문구에 숨은 저자 선택도 잡으며, 정의와 required assertion에도 적용한다. 전체 선택 기록이 기존 freeze hash에 묶인다. 과거 선택과 코어의 재검증은 그대로 지원한다.
- 스킬은 주제를 잠그되 저자가 정한 장소·소품·행동을 잠그지 않도록 갱신했다. 자동 자연어 소유권 판단을 주장하지 않으며 부모가 각 코어의 의미를 직접 검토했다.

## 배포 경계

기존 sealed H-F2 `bb77d341...`의 데이터 위에 검토된 Python 8개 멤버만 교체했다. 별도 overlay는 설치본을 기준으로 만들어 다른 작업의 prompt_generator 변경을 함께 배포하지 않았다. 후보 본문·색인·문서 벡터는 바꾸지 않았다. `REVIEWED-CODE-PATCH.diff`, `STAGED.json`, `PRESERVATION.json` 참조.

새 기본 H-F2: `4a05dd82d952b3df246e9d0375a2e4c91a4e7a3cca6a7d3e15fbfb4d3ffc2878`

새 native closure: `987f06480d79a68c492250334ae610e0665f7abc9475358dd7d01c11cf83240a`

전체 설치 검증 및 집중 테스트 후 기본값으로 선택했다. 미바인딩 prepare/build CLI가 명시 release 옵션을 받지 않는 제약 때문에 실제 신규 코어 검색 검증은 선택 직후 실행했다. 그 전의 거절된 prepare 명령은 검색·이미지 호출 0이며 동결 코어를 고치지 않았다. CURRENT 쓰기 0, commit/push 없음.

## 검증

- 집중 테스트 64개 PASS. 주제/워크플로 분리, 부정/설정 보존, 변경하지 않은 슬롯/기본 질의, 과거 기록, 독립 감사기, 원자적 소유권 충돌 검사를 포함한다.
- 실제 neutral freeze에서 review 누락을 거절하고, feature 전체 문구보다 짧은 cafeteria table 원자가 긴 필수 anchor에 들어가면 거절하며, 같은 baseline의 좁은 anchor는 통과했다. `REAL-FREEZE-REGRESSION.json`.
- 모든 재시험 코어의 생성기/독립 감사기 provenance가 같고, scope 변조는 거절된다. 실제 주제 projection은 모두 캠퍼스물이며 baseline 질의는 그대로다.
- 신규 3개 에이전트는 후보 전에 각각 무작위 컨셉과 baseline을 동결했다. 다른 arm이나 이전 후보·프롬프트·이미지를 읽지 않았다. B가 broad campus 주제까지 열어둔 것은 후보 접근 전에 부모가 발견했다. B 원본을 보존하고 B2에 동일 추첨/동일 baseline을 유지하며 broad 주제만 보호했다.

## 결과 해석

후보 노출, source에 근거한 새 prompt 문구, 생성 픽셀 관찰, 원본 source 전체의 native qualification은 서로 다른 판정이다. H-F2 material ID를 native chosen ID에 임의로 넣지 않는다. inspiration_only는 source 전체의 승인으로 세지 않는다. 원래 baseline에 있던 요소나 단지 캠퍼스 같은 외관은 신규 source 기여 증거로 세지 않는다. 부분 충족과 관찰 불가는 PASS가 아니다. 참조 외양 유사성은 실제 신원 확인을 뜻하지 않는다.

최종 3개 이미지와 부모 픽셀 재검토는 RESULTS.md에 기록한다.

## 동일 풀 질의 비교와 남은 데이터 경계

`QUERY-ABLATION.json`은 같은 21,053 CID / 21,055 RID 풀, 같은 검색 알고리즘·벡터·실험 난수에서 scope만 바꾼 별도 읽기 전용 비교다. `신규 후보 | 같은 첨부 이미지 | 캠퍼스물`에서 `캠퍼스물`로 바뀌며 상위20의 신규 CID는1→11, 상위100은8→50, A와 같은 난수의 제공 표본은1→8이었다. 수정 후 표본이 실제 A의 발행 기록과 일치한다. 이는 이번 질의의 근거이며 일반적인 검색 정확도 통계나 이미지 성공률은 아니다. 비교 결과를 arm의 창작 입력으로 제공하지 않았다.

신규 positive100건 중94건은 source에 broad subject effect가 선언되어 있다. 항상 잠기는 subject를 열거나 그 effect를 지워 반영률을 만들지 않았다. broad 선언이 정확한지 별도 근거를 갖고 owner/property 단위로 다시 검토할 여지는 있으나, 이번 재시험 중 데이터를 바꾸지 않았다. 다음 변경은 완전한 양국어 명제에서 소유자·대상·count·접촉·관계를 재도출하고, 호환/충돌 회귀와 픽셀 게이트 및 새로운 source/index release로 검증해야 한다. `REMAINING-SOURCE-SCOPE-REVIEW.json` 참조.

## 동시 작업 보존

테스트 중 다른 데이터 발행이 기본값을 `9e45ed86...` / native `8e4303b2...` 후속으로 갱신했다. 그 후속의 검토된8개 코드 멤버 SHA가 본 수정 overlay와 전부 동일함을 확인했고, 되돌리지 않았다. 세 실험은 이미 발행된 `4a05dd82...` receipt에 고정되어 계속된다. working corpus manifest는 동시 작업으로 달라졌으나 캠퍼스 candidate/bindings/semantics 세 파일은 시작 SHA 그대로다. 코드만 발행한 본 release의4,087개 H-F2 데이터 manifest는 이전 release와 완전히 같다. `CONCURRENT-DEFAULT-OBSERVATION.json`, `PRESERVATION-LATEST.json` 참조.

후속 managed CLI 호출의 대형 객체 수집 비용을 줄이기 위해 run-local `run_cli_gc_disabled.py`를 제공했다. 기존 dispatcher와 seal·assertion·arguments·산출물 검사는 그대로 실행되며, 부모/정확한 child launcher에 cyclic GC 비활성 설정만 추가한다. 설치 코드, source, 조건, 스코어 또는 검사는 변경하지 않는다. 이미 실행 중인 명령은 중단하지 않았다.
