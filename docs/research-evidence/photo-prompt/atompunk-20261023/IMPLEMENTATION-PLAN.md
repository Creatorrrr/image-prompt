# 리서치 결과 반영 계획

2026-10-23. 상태: **연구·계획 완료, 구현·운영 반영 전**. 이 문서의 파일명·평가 수량·완료 기준은 구현 제안이다. 실제 등록 수는 재사용 심사를 거쳐 결정하며 191개 키워드나 88개 초안을 그대로 신규 후보 수로 삼지 않는다.

## 목표와 우선순위

아톰펑크 요청에서 필요한 구체적인 형태를 더 잘 발견·선택·표현하면서, 기존 사용자의 의미·고정 성분·허용된 변경 범위를 보존한다. 목표를 다음 네 가지로 나눈다.

1. **가시 구분력:** 위성/조명, 원자로/RTG, CRT/오실로스코프/닉시, 구기/일반 미드센추리, 뉴 룩/시프트 등 서로 다른 구조가 실제로 분리된다.
2. **표현 범위:** 미국 소비문화·소비에트 우주미학·탐사·밝은 자동화·민방위·폐허·성인 공연·괴수를 선택 가능한 분기로 제공한다. 한 장면에 전부 넣지 않는다.
3. **인과·매체의 정직성:** 실물·인쇄물·모형·도해, 현재 상태·연속 작동, 표면·실제 조성, 외형·동의/의도/피폭 원인을 구별한다.
4. **검증 가능성:** source→binding/role→노출→실제 선택→문장→원본 픽셀→사용자 판단을 각각 기록한다.

첫 구현 묶음은 P0의 가시 카드 52개와 문맥 경계 카드 8개를 우선 검토한다. P0 60개 전부를 시각 후보로 만드는 계획은 아니다. P1 41개는 판본 고증·재료·교통·성인 문화·매체의 선택지를 확장한다. 구체 카드 목록과 수는 `semantic-cards.json`의 priority/mode로 산출한다.

## 단계와 완료 증거

| 단계 | 구현할 일 | 완료 증거 | 다음 단계로 넘기지 않을 상태 |
|---|---|---|---|
| 0 기준 고정 | 최신 checkout·dirty·manifest·sealed/installed 세대 재확인 | HEAD·원문 모듈 SHA·catalog·실행 경로·변경 allowlist | 연구 스냅샷과 최신 소스 혼합 |
| 1 의미 심사 | 191개 route·101개 카드·23개 기존 원문의 reuse/refine/new/context/defer 결정 | 실제 CID·RID/분기·조건·role·차이·출처 범위 | lexical 0 또는 label 일치만으로 new/reuse 판정 |
| 2 소스 작성 | 선택된 분기 전체의 자연스러운 한영 원문·소유·조건·효과·의무 | 검토 가능한 전체 source diff와 번역 검토 | 메타데이터·태그·연구 owner graph를 native 권위로 승격 |
| 3 계약·회귀 | 유효 필드·owner/role/락·매체·음성 대조 검증 | 변경에 맞는 validator·focused tests의 결과 | 불완전 endpoint·효과 누락·문맥→direct 승격 |
| 4 별도 검색 빌드 | staging의 소스에 대해 현재 recipe/model로 인덱스 작성·verify | 원문/recipe/model/vector/coverage/closure SHA | 원본 assets나 CURRENT에 미검증 게시 |
| 5 질의 평가 | 60개 한영 개발/대조와 별도 holdout 실행 | query bytes·실제 CID/RID·노출·선택·부적합 이유 | 순위·노출을 의미·픽셀 성공으로 보고 |
| 6 픽셀 비교 | 12사례×3 arms 첫 36장 제안 | 원본 이미지·선택 의무·가시성·장면 품질의 분리 기록 | partial/unobservable을 전체 PASS 처리 |
| 7 설치·마감 | 검증된 source/code/data를 봉인·비활성 설치·검증·필요한 활성화 | generation·포인터·복구 경로·정확한 배포 상태 | source 변경을 설치본 반영으로 보고 |

## 0. 기존 작업과 기준 보존

연구 시작 HEAD는 `be52bda69010b94bb444e998fe148b2881e20624`였고 기존 tracked 15,704개 파일 해시와 dirty/untracked 목록을 [BASELINE.json](BASELINE.json)에 보존했다. 변경 중인 다른 작업이 있었으므로 구현 직전에 반드시 재기준화한다. 원본 checkout의 stash/reset/restore로 다른 작업을 치우지 않는다. 필요한 변경만 명시 allowlist로 별도 작업 공간에 옮긴다.

조사 스냅샷은 75모듈·20,054레코드·14,687binding이다. 실행 시 현황을 다시 읽는다. 현행 149개 catalog 중 제안 슬롯 이름의 존재는 확인했지만, 슬롯의 의미 적합성이나 source 승인까지 완료된 것은 아니다. 소스 경로·검색 인덱스·sealed generation·설치 세대는 서로 다른 증거다.

이 연구는 일반 이미지 요청의 precore 자료가 아니다. 실제 평가용 요청은 후보와 이 연구안을 보기 전에 의미·고정 조건·주제·장면을 독립적으로 해석하고 baseline core를 고정한다. 연구자가 붙인 의미가 원래 사용자 요구였던 것처럼 잠그지 않는다. 현재 skill의 창의성 설정과 열린 차원 안에서만 이후 저술을 수행한다.

## 1. 재사용과 신규 작성의 결정

각 결정에는 `card_id`, 실제 기존 `candidate_id`, 선택 가능한 `realization_id`가 있으면 그 값, 전체 source SHA·binding SHA, 조건·효과·role·의무, 필요한 차이, 판본 출처, 심사 이유를 남긴다.

| 결정 | 사용할 조건 | 이번 리서치의 예 |
|---|---|---|
| reuse | 기존 전체 원문·선택 분기·조건·효과·role가 모두 맞음 | 기존 펜슬 윤곽, 점프슈트 연속 구성, 선택한 원자력 계측함 |
| refine | 원래 의미를 지키며 번역·endpoint·질의 지원 등을 정확하게 보완 가능 | 계수기와 선량계의 별도 소유, 계측기 케이블의 양끝 |
| new | 필요한 구체적인 구조나 현재 상태가 기존 complete source로 충족되지 않음 | 위성 네 안테나, 숫자 전극 표시관, 수면 아래 발광 관계 등 심사 후 확정 |
| context | 원인·전략·정치·관계·소리·의도·동의·진단 등 비가시/비사진 의미 | 핵 억지·라벤더 공포·인공 연인·핵겨울·성적 강압 |
| defer | 원전·판본·매체·native 표현을 현재 확정하기 어려움 | 접근 실패한 Orion 유물의 정확 구조, 상세 역사 우주복·불릿 브라 판본 |

기존 atompunk `world` 소스는 **구기+인프라+낙관/위험이 있는 선택지**로 보존한다. 새로운 소비에트·탐사·밝은 생활 분기는 이 소스의 원문을 축약하거나 조건을 약화해서 만들지 않는다. 같은 단어를 공유하는 전체 후보를 무조건 한 번들에 묶지 않는다.

`EXISTING-DECISIONS.tsv`의 23개 판단은 통합 triage 제안이다. 예컨대 현재 점프슈트가 주머니·지퍼를 말하지 않으면 새 카드의 그 부속품까지 ‘이미 충족’으로 계산하지 않는다. 현재 계측함 후보의 effects가 비어 있다는 사실만으로 재사용을 승인하지 않으며, 실제로 도입/변형하는 prop·actor·상태의 영향 전체를 검토한다. 이것은 현행 엔진 결함을 확정한 보고가 아니다.

## 2. 제안 파일과 권위 경계

이번 연구는 아래 운영 파일을 만들거나 등록하지 않았다.

| 제안 경로: `skills/photo-prompt-image-generator/` 기준 | 역할 |
|---|---|
| `assets/photo_atompunk_semantics_20261023.json` | 원문 항목·출처·카드·채택 경로 추적용 registry. native 소스의 두 번째 조건/효과 권위가 되지 않음 |
| `assets/photo_candidate_atompunk_20261023.json` | 심사된 신규 V3 source만 등록; 연구용 ID를 operating CID로 그대로 취급하지 않음 |
| `assets/photo_candidate_atompunk_bindings_20261023.json` | actual catalog 의미에 맞는 검토된 role 연결 |
| 기존 CID의 소유 모듈 | refine가 필요하다고 결정한 원문만 국소 수정; shard 전체 재작성 금지 |
| `assets/photo_candidate_corpus_manifest.json` | 승인된 모듈만 명시 등록 |
| `references/atompunk-semantics.md` | 유지보수용 혼동 경계·판본·비가시 의미 원칙 |
| 실제 영향받은 tests/fixtures | 태그 자동 강제·소유/효과·role·매체·다국어의 회귀 |

loader가 허용하지 않는 필드를 `research_*`로 넣고 무시되길 기대하지 않는다. 현재 V3 source와 V10 pack 계약을 구현 시 다시 확인한다. 새 원문은 자연스러운 한영 **전체 문장**, 실제 source unit, 전제, 모든 mutation receiver, intrinsic effects, 선택된 완전 분기, literal 의무를 갖춰야 한다. 연구 JSON의 짧은 성분 목록과 방향 관계를 바로 importer 입력으로 바꾸지 않는다.

별칭·source 설명·혼동 금지·주장 한계를 긍정 프롬프트에 넣지 않는다. ‘방사성 오염을 확정하지 않음’이라는 연구 주석을 embedding positive에 넣으면 오염 후보로 역유입될 수 있다. negative는 기존 사용자·소유·승인 경로로 관리한다. 출처 registry와 label은 새로운 semantic permission을 만들지 않는다.

## 3. 조건·owner·effects·role 심사

아래 항목은 source와 binding을 별도로 검토한다. binding은 intrinsic guard/effect를 덮거나 다른 role의 실패를 우회하지 않는다. deferred role를 unbound proposal로 되살리지 않는다.

| 카드 | 반드시 확인할 관계와 영향 |
|---|---|
| E05 계수기 | 본체·케이블·프로브·표본을 구별; 케이블 양끝과 손 소유; 계측값은 별도 |
| E06 배지 | 동일 작업자 가슴에 붙음; 사람·의복·직업 표현을 임의 생성하지 않음 |
| E08 수조 | 발광은 물 아래, 반사는 같은 수면; 주변 통로의 빛과 전체 색보정 분리 |
| S01 / F03 | 네 안테나와 여러 전구의 수·부착부·분포; 명칭 공유로 구조 union 금지 |
| S07 / B04 | 거주 돔의 내부/외부와 삼각 골격은 별개 분기; 재료·밀폐의 claim 분리 |
| S09 헬멧 | 얼굴→같은 착용자→목링→투명 셸; 표면 반사·내부 얼굴·배경의 깊이 |
| M09 릴 | 왼쪽 릴→중앙 헤드→오른쪽 릴의 테이프 경로; 실제 데이터·회전은 문맥 |
| M11 로봇 | 같은 팔·집게·쟁반 접촉·컵의 지지; 인물/기계/컵 수와 자세 변화 |
| W01 / W04 | 의복의 허리·치마 폭·기하학 패널과 실제 신체 비율을 분리 |
| V01 / G02 | 종이·그림 속 사람/괴물·실물 프레임의 수와 위치; 인물 수를 늘리지 않음 |
| H03 곤충 | 여섯 다리·세 마디·더듬이·차량 대비 크기; 거미는 별도 구조 |
| R06 시험 마을 | 시험 인형·실제 사람·모형·실제 건물을 분리; 피해자를 props로 바꾸지 않음 |

변경 effect는 setting·prop·subject count·body·wardrobe·pose·color·lighting·medium·scale 등 실제 영향 전부를 목록화한다. 빈 effect나 ‘기존 값과 같음’으로 permission 심사를 피하지 않는다. 기존 owner를 변형하면 독립적으로 고정된 core의 정확한 owner를 선택한다. 연구에서 만든 owner 이름은 요청자가 허용한 owner 선택의 근거가 아니다.

`location`의 구기 건물을 `mood`에서 direct fact로 자동 승인하지 않는다. `genre`·`world`·`aesthetic_trend` 같은 문맥 role은 geometry의 대체 증거가 아니다. 성인 등장 자체가 `adult_presentation_context`·성적 강조·fetish 활성화의 근거가 되지 않는다. 실제 요청과 현재 설정을 따른다.

## 4. 회귀와 별도 인덱스

소스·role·guard/lock·native qualification·다국어 투영 중 실제로 바뀐 경로의 validator와 focused tests를 실행한다. 현재 관련 테스트 파일을 확인하고 영향받은 사례를 추가한다. 이 연구 폴더의 validator는 참조·소유 그래프·파일 보존만 검사하므로 엔진·검색·의미의 회귀 테스트를 대신하지 않는다.

반드시 음성 결과를 확인할 사례는 다음과 같다.

1. `atompunk`만으로 기존 world core·폐허·고어·미국 다이너·녹색 발광을 강제한다.
2. 구기·소비에트·raypunk의 모든 특징을 단일 bundle에 union한다.
3. `monochrome`·치즈케이크 디저트·비키니 환초·핵가족에 잘못된 의미를 붙인다.
4. Sputnik 조명에 네 안테나 또는 실제 위성에 전구를 잘못 붙인다.
5. 닉시관 대신 7세그먼트가 나오거나 계수기와 선량계를 하나로 채택한다.
6. 모델·포스터 속 사람/도시를 실물 subject count와 world scale에 더한다.
7. 의상 실루엣을 신체 비율 변경으로 구현하고 잠긴 body/wardrobe를 우회한다.
8. 비닐·목걸이·흰 가운으로 fetish·동의·강압·정신질환을 확정한다.
9. 방사선 원인·질환·지능·충성·가족·핵겨울·회전 중력을 픽셀 PASS로 만든다.
10. source·RID·role·전체 의무가 바뀌었는데 과거 proof/receipt를 재사용한다.

검색 빌드는 **별도의 완전한 staged skill**에서 한다. 현행 manifest가 선언한 backend·model·revision·dimensions·recipe·vector integrity를 읽어 기록한다. 정확한 ID·text bytes/hash·recipe·embedding space·벡터 검증이 일치하는 것만 재사용하고, 변경된 텍스트는 해당 provider로 다시 계산한다. 원격 provider로 조용히 우회하지 않는다.

현재 스크립트에는 `--assets`, `--backend`, `--cache`, `--verify`, `--output-assets`, `--publish`가 있다. 아래는 **미실행 예시**이며 staging 경로·runtime Python·backend는 구현 시 확정한다. `--output-assets`와 `--publish`를 함께 쓰지 않는다.

```sh
"$TASK_RUNTIME_PYTHON" "$TASK_STAGED_SKILL/scripts/build_shared_candidate_index.py" \
  --assets "$TASK_STAGED_SKILL/assets" --backend embeddinggemma2-local \
  --cache "$TASK_BUILD_CACHE" --batch-size 32
"$TASK_RUNTIME_PYTHON" "$TASK_STAGED_SKILL/scripts/build_shared_candidate_index.py" \
  --assets "$TASK_STAGED_SKILL/assets" --backend embeddinggemma2-local --verify
```

소스가 빌드 중 바뀌면 activate하지 않고 재기준화한다. 원문·문서 수·통계·payload·posting/vector 범위·routing residual/closure를 검증한다. 캐시 재사용·새 추론·실패/미확인 시도를 따로 기록한다. 별도 인덱스 verify는 게시·설치·활성화가 아니다.

## 5. 검색·선택 평가와 사전 고정할 기준

[60개 평가 사례](EVALUATION-CASES.tsv)는 카드와 함께 작성했으므로 개발 자료다. 실제 실행 전에 **별도의 자연어 holdout 20사례/40질의**를 데이터 저술에서 분리해 고정한다. 기존 문장을 단순 재서술한 것을 독립 holdout이라고 부르지 않는다.

각 질의에 requester text·frozen core·role/slot·언어·통제값·query bytes·source/index/code SHA·현재 resolver의 실제 순위 창/표본 규칙·receipt를 기록한다. 149개 슬롯 모두에 장르 단어 하나를 강제로 넣지 않는다. `rank→offered→selected→composed`는 서로 다른 단계다. 정답은 연구 card ID가 아니라 실제 reviewed CID/RID/role와 허용된 조건이다.

후속 실행 전에 확정할 **제안 gate**:

- 개발 양성 24사례 중 각 언어에서 최소 22사례에 의미가 맞는 qualified source가 실제 노출되어야 한다. 노출된 것의 완전한 의미·조건·role 적합성은 별도로 검토한다.
- 경계 16·일반 12·비가시 8사례의 한영 72질의에서 **잘못된 자동 의무·락 우회·비가시 사실 확정 0건**이어야 한다. 단순히 관련 후보가 선택 가능한 목록에 등장하는 것과 강제 채택은 구별한다.
- 고정된 ordinary control의 성분·subject count·매체·성적 맥락 오염은 0건이어야 한다.
- 실제 선택 source의 한영 owner·endpoint·전제·의무·effect 의미 차이는 0건이어야 한다. 문자열 점수만으로 통과시키지 않는다.
- holdout 양성 노출은 제안 목표 90% 이상, 경계의 잘못된 채택은 0건으로 정한다. 성능 목표를 결과를 본 후 새 데이터에 유리하게 바꾸지 않는다.
- 현재 corpus와 proposed corpus를 같은 code/settings로 비교한다. 관련 coverage가 늘어도 어떤 family에서 오류가 생기면 해당 family를 HOLD한다. 전체 평균으로 실패를 덮지 않는다.

위 수치는 **목표이지 현재 성과가 아니다.** baseline이 이미 높으면 노출률의 임의 증가를 강요하기보다 잘못된 형태 선택 감소와 새 시각 분기의 추가 가치를 보고한다. 검색 성공만으로 생성 품질이 개선됐다고 결론 내리지 않는다.

## 6. 픽셀·설치·롤백

[픽셀 계획](PIXEL-PLAN.md)의 첫 36장은 frozen candidate-free baseline, 현재 corpus 보강, proposed corpus 보강을 같은 조건으로 비교한다. 필수 성분과 endpoint의 동시 가시성은 기술 판정, 전체 장면의 가독성·시선 흐름·상황 의미는 별도 예술적 판정, 사용자 수용은 별도 상태로 남긴다.

stage source/index를 봉인하고 native/installed 절차로 qualification·비활성 설치·검증을 거친다. 기존 CURRENT·sealed generation·발급 receipt·과거 run은 복구 가능하게 보존한다. 실패한 family는 새 source revision에서 보류 또는 수정하며 과거 proof를 다시 쓰지 않는다.

공유·출판이 요청된 뒤에는 변경 파일의 명시 allowlist와 staged blob을 검증하고 커밋·푸시·PR·설치·활성화 상태를 따로 보고한다. 현재 연구 요청에서는 구현·검색 빌드·이미지 호출·설치·커밋·푸시를 수행하지 않았다.
