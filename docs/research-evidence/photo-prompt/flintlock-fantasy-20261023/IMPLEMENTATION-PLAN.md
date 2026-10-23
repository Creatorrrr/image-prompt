# 조사 결과 반영 계획

2026-10-23. 이 파일은 후속 구현의 입력·작업·종료 조건을 정한다. 현재 완료한 범위는 리서치·원문 감사·연구 초안·평가 설계다. 운영 source/manifest/index/installed runtime 변경, 실제 검색·이미지 생성·commit/push는 이번에 수행하지 않았다.

## 1. 목표와 입력

목표는 플린트록 요청에서 **의미가 맞는 부품·집단·공간·생활 관계를 검색하고, 요청자 의미 안에서 선택한 후보의 전체 뜻이 프롬프트와 저장 픽셀까지 보존**되게 하는 것이다. 장르 태그 추가나 후보 수 증가를 완료 지표로 삼지 않는다.

입력은 `REFERENCE-ACCESS.json`, `reference-chrome-supplement.md`, `sources.json`, `semantic-cards.json`, `candidate-drafts.json`, `keyword-routes.json`, 두 existing-source snapshot, `evaluation-cases.json`, `BASELINE.json`이다. 크롬에서 원문 17절 전체를 확인했다. 81개 초안을 모두 새 CID로 등록하는 계획이 아니다. 현재 제안은 new 52 / refine 6 / reuse 1 / defer 22이며 카드 단위다. 21개 문맥 카드는 양성 시각 대안과 분리한다.

## 2. 단계 0 — 재기준화·변경 범위 확정

구현 시작 시 HEAD, dirty/untracked 목록, manifest 및 모든 authored module hash, slot catalog/policy, runtime pointer, installed CURRENT와 실제 CLI 버전을 다시 기록한다. 연구 시점에는 source 20,341개·binding 15,120개·slot 149개였으나 이것을 미래 기준으로 고정하지 않는다.

공유 checkout에 다른 연구·runtime·index 변경이 많다. 기존 변경을 되돌리거나 stash/cleanup하지 않는다. source 수정이 필요한 CID와 신규 파일의 명시적 allowlist를 만든다. 병행 작업과 같은 파일을 고칠 때는 변경 주체와 현재 blob을 대조하고, 필요하면 적합한 기존 worktree를 확인한 후 별도 작업 트리에 좁은 변경을 재구성한다.

종료 조건: 기준 시점·변경 allowlist·보호 hash·현재 계약이 있고, 이후 drift를 발견하면 병합 전에 다시 기준화한다. 연구 원본은 덮어쓰지 않는다.

## 3. 단계 1 — 출처·도판·한영 검토

| 묶음 | 실행할 일 | 채택 조건 |
|---|---|---|
| A03/A04/A05/A08 | wheel 노출/별도 pan cover/미켈레트/초기 후장식의 특정 실물 도판 선정 | lock·총열·총상·연대를 구분한 관찰 기록; 내부 구조를 추측하지 않음 |
| B03/C07/D08/E04/F05 | 총구 프로파일, pelisse 소매·끈, 포차 결합, bar 양끝, 말 마구 연결 | 실제 변형 하나를 선택하고 불가능한 접촉·하중·겹침 제거 |
| E05/E08 | chain shot 직접 원전과 weather gauge 전술·도식의 의미 보완 | 미확보 상태에서는 defer 유지; bar shot/돛 모양으로 대체하지 않음 |
| H03/H07 | 궤적의 표현 층, 용의 마구·발판 하중·해부 경계 검토 | 창작 제안으로 명시하며 작품 정본/현실 물리라고 주장하지 않음 |
| J01/J02/J04/J07/J08/J09/J10/J14/J15 | 세부 모자·코티·무릎바지·목천·stays·노출 후프·구호마차·마이소르 lock의 실물 도판 | 이름/시각 silhouette와 실제 부품을 구별; 곡률·구멍·연결·연대 확인 |
| 색인만 읽은 9건 | 본문/대체 공식 원전을 확보하거나 제한 유지 | 열리지 않은 자료를 열린 것으로 바꾸지 않음; 인용 범위 보존 |
| I군 사회·성·폭력·제도 | 시대/지역별 전문 정의와 사료 보완 | 근거가 부족한 정의는 context/defer로 남김; 외형 사실로 승격하지 않음 |

모든 EN/KO 문구에서 명사·수량·부품·소유자·관계 방향·재료처럼 보이는 외형·텍스트·모형/도식/실물의 층을 대조한다. G07의 앞트임/속치마와 G09의 등 주름은 별도 실현을 유지한다. 하나의 정면 컷에서 앞뒤 전체를 증명하도록 요구하지 않는다.

연구 출처는 기술 구별이나 문맥을 지원한다. 연구자가 만든 장면의 수량·배치·마법 효과까지 출처가 보증하는 것은 아니다. source-image 검토, candidate literal 검토, native source 자격, 생성 픽셀 검토를 각각 남긴다.

종료 조건: 각 초안의 `reuse / refine / new / context / defer` 결정과 근거, language review, 추가 원전 보류 여부가 확정된다. 정밀 검토 22건 외의 카드도 자동 승인하지 않는다.

## 4. 단계 2 — 기존 원문부터 보정

| 기존 CID | 제안 | 변경 시 지킬 의미 |
|---|---|---|
| `cand_42d2b29291fe52db93a6bf09617d266e` | 보루/라블랭의 KO를 완전 관계로 보정 | 본체에 붙은 보루 + 해자 건너 분리된 외보 + 출입구 차폐 전체를 보존. D05/D06 두 카드라고 두 기존 CID로 세지 않음 |
| `cand_9c0d3821b9ae5cc49781a59f278b4f29` | 포대 KO·embedding·effects 검토 | 포좌 뒤 흉벽과 대응 포문을 통하는 포신 정렬 보존 |
| `cand_c79a072f53df533cb9a46d96e9ced116` | 휠록 재사용 검토 | wheel 구조·전시·위치 한정을 보존. 비교 alias의 flintlock을 양성 의미로 승인하지 않음 |
| 세이버·장식 견장 관련 원문 | 전체 원문이 맞을 때 재사용 | 소품/실제 무기·칼집/뽑힌 칼·장식/왕실 문맥을 구별 |
| 삼각모·흉갑+러프·왕실 근위 제복 | 보조/경계 사례로 유지 | 해적·공주·러프·왕실 의미를 삭제해 일반 시대복으로 만들지 않음 |
| 현대 소총·camera bayonet·data cartridge | 회귀 control로 유지 | 역사 무기·총검·종이 탄약의 정답으로 오인하지 않음 |

수정 전 해당 원문과 binding의 canonical hash 및 현재 diff를 보존한다. 번역 정정과 의미 변경을 구별한다. 원래 완전 bundle을 분해해야 한다면 기존 CID의 뜻을 몰래 바꾸지 말고 새 실현 여부를 명시적으로 결정한다.

추가 감사의 별도 열린 조끼/엠파이어 이음선/부두아르 공간은 신규 중복보다 재사용을 먼저 검토한다. 반대로 붙박이 조끼 패널과 겉치마 silhouette에서 독립 조끼/숨은 후프를 승인하지 않는다. 현대 구급차 후보의 monitor를 삭제해 역사적 구호마차라고 부르지 않는다.

완전 초안의 최종 결정에서는 B08의 뽑힌 칼+별도 빈 칼집을 기존 sheathed prop에서 가져올 수 없어 new로 둔다. C08·J06·J11은 기존 가까운 EN 관계가 있어도 KO 축약과 전체 부품/경계 보강이 필요해 refine으로 둔다. J13의 화장대/거울/문 너머 침대는 기존 완전 원문에 직접 대응하여 reuse 제안이다. 기존 부품 일부의 재사용 가능성과 새 완전 초안의 reuse를 구별한다.

종료 조건: 중복 제거한 기존 25개 수동 감사 항목의 결정이 최신 source에 대응하고, 각 수정이 원래의 실제 조건·효과·표현 층과 충돌하지 않는다.

## 5. 단계 3 — source·binding·문서 반영

후속 반영의 제안 파일은 아래와 같다. **아래 파일을 이번 연구에서 생성·수정한 것은 아니다.** `assets/`와 `references/`는 `/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/` 아래다.

| 경로 | 반영 내용 | 권위 범위 |
|---|---|---|
| `assets/photo_flintlock_fantasy_semantics_20261023.json` | 검토한 카드·출처·혼동·주장 한계·결정 | 유지보수 sidecar; 실행 사실/owner 권한 아님 |
| `assets/photo_candidate_flintlock_fantasy_20261023.json` | 채택한 완전 시각 실현과 별도 diagnostic/context | 실제 canonical candidate source; 연구 ID와 CID/RID 구별 |
| `assets/photo_candidate_flintlock_fantasy_bindings_20261023.json` | 직접 검토한 CID→slot 연결 | role 적합성만 표현; intrinsic guards/effects 복제·우회 금지 |
| `assets/photo_candidate_corpus_manifest.json` | 확정한 candidate/binding module 등록 | authored source 진입점 |
| 기존 `_000/_002/_006/_010/_013`의 실제 대상 module | 확정한 좁은 원문 정정 | 현재 module 소유/병행 변경을 재확인한 뒤 수정 |
| `references/flintlock-fantasy-semantics.md` | taxonomy·세부 의미·source 상태·불확실성 | 사람용 실행 안내 |
| `references/maintenance.md` | 위 문서와 검증 상태 링크 | 유지보수 탐색 |

현재 확인한 source loader는 `photo-candidate-corpus/v3` 및 `photo-candidate-corpus-source/v3` 계약을 사용한다. 실제 구현 때 `photo_candidate_corpus.py`, `photo_native_pack.py`, `photo_h_f2_generation.py`, `photo_semantic_evidence.py`, `photo_native_owner_resolution.py`를 다시 읽는다. 옛 메모의 pack 버전이나 다른 장르의 자격 proof를 재사용하지 않는다.

역할은 실제 149-slot catalog에서 선택한다. 예를 들어 부품은 object_structure, 부착은 contact_point, 집단 배치는 proxemics/composition, 연기는 ambient_particle/atmospheric_medium, 옷의 층은 wardrobe_layering, 인쇄는 visible_text로 검토한다. **slot descriptor의 dimensions 합집합을 실제 effects 완성본으로 간주하지 않는다.**

각 candidate의 모든 긍정 내용에 대해 새 인물·손·총·말·군중 수·부품·글자·위치·방향·빛·배경·행동과 실제 owner/property 범위를 직접 작성한다. 사람 수가 고정된 요청에 새 병사를 붙이거나 no_people 정물에 손을 추가하지 않는다. source 문구가 없는 사실을 alias·태그·출처 URL·연구 graph로 보충하지 않는다. 조건부 branch와 대안은 실제 선택 RID별로 완전하게 분리한다.

종료 조건: 각 CID/RID의 전체 문구·conditions·effects·bindings·owner 양끝·선택 조건을 검토한 증거가 있다. schema 통과·연구 카드·역할 태그만으로 native qualification을 승인하지 않는다.

## 6. 단계 4 — 구조 검사와 변경 관련 회귀

staged assets를 대상으로 `scripts/validate_photo_prompt_dictionary.py --assets <staged-assets>`를 실행하고 실제 현행 CLI 옵션을 확인한다. 원문 중복 ID, 잘못된 참조, 등록 누락, slot/guard/owner/effect 충돌과 변경에 맞는 기존 테스트를 검증한다. 현재 턴에는 운영 파일을 바꾸지 않았으므로 전체 runtime 테스트는 실행하지 않았다.

필수 의미 회귀는 점화/총열/장전 축, camera bayonet/총검, magazine 다의어, broadside 다의어, modern rifle/역사 장총, wheel alias/flintlock, canister/shrapnel, attached bastion/detached ravelin, 모형/실물/후대 상징, 인물 수/손 owner, camp follower/성매매, clothes/rank/국적, 장르→전투·폭력·성적 의미 강제다.

종료 조건: 실제 변경과 관련된 체크가 통과하고 미실행·실패·보류가 기록된다. JSON을 다시 읽는 단순 테스트가 의미 정확성 증거를 대신하지 않는다.

## 7. 단계 5 — 별도 인덱스와 실제 검색 비교

`build_shared_candidate_index.py`의 현행 CLI를 확인해 별도 staging generation을 만든다. 현재 사용 중인 recipe/model/embedding space/layout/source fingerprint를 보존한다. 새 문구·번역·embedding_text에는 필요한 벡터를 다시 계산하고 v1/v2 layout을 이름만 바꾸어 섞지 않는다. `--verify` 성공은 source/index 정합성 증거이며 의미 품질 증거가 아니다.

slot별 검색과 whole-scene discovery는 각각 유지하고 별도로 계측한다. H-F2의 실제 issued query·receipt·top-k·source 세대를 남긴다. 점수/노출만으로 원문 채택이나 native approval을 주장하지 않는다.

평가 입력은 card-derived 개발 81사례와 경계 control 32사례, 각 2언어로 **226질의**다. 추가 control은 flying ambulance/몰리 하우스/성별 표현/royal mistress/성적 비방/숨은 후프/stays/약품 라벨/지역 총기/조용한 전후 생활/트라우마 진단을 다룬다. 이것은 독립 holdout이 아니다. source 문구를 보지 않은 별도 작성자가 만든 자연 요청 최소 24개를 후속 확보·고정하여 개발과 분리한다. 이 턴에서 독립 평가가 이뤄졌다고 보고하지 않는다.

| 측정 항목 | 판정 방식 |
|---|---|
| 의미 recall@5/@10 | 전체 원문을 검토해 고정한 허용 CID/RID 집합이 노출됐는지; 카드 label만 정답 아님 |
| precision@5 | owner·관계·시대 한정·표현 층·실제 역할이 요청 전체와 맞는지 |
| 한국어/영어 차이 | 부품·수량·방향·대상의 교체/소실이 없는지 |
| 경계 침범 | context→양성 사실, no_people/인물 수/시대 lock 위반이 생기는지 |
| 채택 단계 | 노출 → 검토 → 선택 → literal prompt 근거 → native adoption을 분리 |
| 보류 | 자격/원전/효과/owner/시점/번역/가시성 때문에 decline한 이유 |

통과의 제안 기준은 P0 구별의 회귀 0건, hard lock 및 신분·동의·시간 주장 오승격 0건, baseline보다 paired 의미 지표 개선, 독립 자연 요청에서 개선의 방향 유지다. 임계값이 추가로 필요하면 실행 전에 고정하며 결과를 보고 바꾸지 않는다. 일반 구성품의 관련 노출과 부당한 장르/의미 채택은 별개다.

종료 조건: 동일 frozen 요청과 controls에서 baseline/staged 비교 결과·오답 원문·보류·언어 차이가 남는다. 실패가 후보 원문인지 검색 pool인지 ranking인지 qualification인지 구분된다.

## 8. 단계 6 — 프롬프트·픽셀 검증

`PIXEL-PLAN.md`의 여덟 의미군을 사용한다. 첫 실행 제안은 부품/요새 관계/민간 노동의 세 요청 × baseline·staged 두 arm = 6장이다. 추가 다섯 의미군은 첫 결과와 적용 범위를 검토한 뒤 확장한다. 원인 구분이 필요한 경우에만 선택적 retrieval을 뺀 ablation을 추가한다. 이 수량은 실행 결과나 자동 생성 약속이 아니다.

requester 의미와 controls를 독립적으로 freeze한 뒤 후보를 검색한다. 연구의 소품·군복·문구를 requester-owned anchor로 자동 승격하지 않는다. 여러 후보를 합집합으로 붙이지 않고 장면 전체의 authorial decision과 decline을 기록한다. 정물·단면/도식·실물·인물의 표현 층을 선택한 요청에 맞춰 고정한다.

정확한 최종 prompt/전송 hash와 저장 이미지·모델 provenance를 연결한다. 관계의 양끝·접점·방향·수량·표현 층을 실제 픽셀에서 확인한다. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`를 유지하고 차단/미생성은 `BLOCKED_UNSCORED`로 분리한다. local source gate와 whole-scene 통과, 사용자 수용을 따로 기록한다.

종료 조건: 단순 전송 성공을 이미지 의미 통과로 세지 않으며, 요구 관계가 숨거나 잘리면 해당 전체 사례를 통과시키지 않는다. 사용자 수용은 실제 피드백 전까지 pending이다.

## 9. 단계 7 — 설치·게시와 보고

후속 실행 범위에 설치가 포함되면 현행 release 절차로 sealed source/code/index를 만들고 installed fingerprint와 CURRENT를 별도 확인한다. 작업 트리 파일을 고친 것과 installed runtime 변경은 다른 상태다. 검색·qualification 실패 시 active 세대는 유지한다.

commit/push가 요청되면 명시적 allowlist만 stage하고 staged 경로·blob·diff를 비교한다. 제외한 dirty 파일과 runtime pointer를 보호하며 local/tracking/remote SHA를 각각 확인한다. 임시 worktree는 검토한 결과 보존과 실제 원격 SHA 확인 뒤 정리한다.

최종 보고는 연구, source 반영, native 자격, 인덱스, 실제 검색, installed 활성화, prompt 전송, 저장 픽셀, 사용자 수용, commit/push를 각각 표시한다. 한 단계의 PASS가 다음 단계의 증거를 대체하지 않는다.
