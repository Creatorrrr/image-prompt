# 시각 의미 카드

모든 구체적 장면은 이번 연구에서 작성한 선택적 실현이다. 출처가 이 기하학이나 재질을 직접 규정했다는 뜻이 아니다.

## U01 공간 패널과 손의 앞뒤

분류: 표시 매체 / still. 근거: S08, S10.

기울어진 상태 패널이 손과 방 사이에 있고 손이 패널 모서리 일부를 가린다.

A tilted status panel stands between a hand and the room, with the hand cleanly occluding one panel edge.

소유자: {"panel": "tilted free-standing panel", "hand": "one hand", "room": "visible room"}

관계: hand → occludes → panel; panel → in_front_of → room

혼동 경계: 평평한 화면 자막과 구분; 누가 볼 수 있는지는 가림만으로 확정 불가

## U02 화면 가장자리 HUD

분류: 표시 매체 / displayed. 근거: S04, S06, S10.

작은 자원 표시가 이미지 모서리에 맞고 뒤로 거리가 보인다.

A compact resource display aligns with the image corner while the street remains visible behind it.

소유자: {"frame": "image frame", "hud": "corner resource display", "scene": "street"}

관계: hud → aligned_to → frame; hud → overlays → scene

혼동 경계: 원근 패널과 구분; 카메라 추종은 연속 장면 필요

## U03 손에 든 모험자 카드

분류: 표시 매체 / still. 근거: S16.

한 손이 단단한 모험자 기록 카드를 받치고 접수원의 손이 직업·스킬 행을 가리킨다.

One hand supports a rigid adventurer record card while a clerk points to its separate class and skill rows.

소유자: {"card": "one rigid record card", "hand": "holder hand", "clerk": "clerk hand"}

관계: hand → supports → card; clerk → points_at → card

혼동 경계: 일반 신분증과 비교; 카드 재질·행 구성은 창작 선택

## U04 신체에 기록된 능력

분류: 표시 매체 / still. 근거: S17.

정돈된 어두운 문자 행이 피부 앞에 뜨지 않고 등 굴곡을 따른다.

Ordered dark glyph rows follow the curvature of a person's back rather than floating in front of the skin.

소유자: {"skin": "back skin", "marks": "organized glyph rows"}

관계: marks → conform_to → skin

혼동 경계: 장식 문신과 비교; 기록 내용·성장 효력은 별도 문맥

## U05 장비에 내장된 자원계

분류: 표시 매체 / still. 근거: S09, S19.

분절된 자원계가 테두리와 고정부가 보이는 등 장비 하우징에 내장돼 있다.

A segmented resource meter is physically embedded in a back-mounted equipment housing with visible edges and fasteners.

소유자: {"rig": "back-mounted equipment", "meter": "segmented meter"}

관계: meter → embedded_in → rig

혼동 경계: 피부 문양·공중 막대와 구분; 정확한 HP 여부는 라벨 필요

## U06 안면과 바이저 정보층

분류: 표시 매체 / still. 근거: S07, S21.

바이저 안 얼굴 양쪽에 굽은 정보층을 놓고 눈과 입을 읽을 수 있게 한다.

Curved information layers flank a face inside a visor, leaving the eyes and mouth readable.

소유자: {"face": "face inside visor", "ui": "curved near-face graphics", "visor": "visor rim"}

관계: ui → beside → face; face → inside → visor

혼동 경계: 유리에 인쇄된 글씨와 비교; 시선 추적·심리 상태는 단일 프레임 불가

## U07 본문과 분리된 시스템 행

분류: 표시 매체 / displayed. 근거: S11.

보이는 페이지에서 대괄호 시스템 알림이 일반 서술 문단 사이 독립 행을 차지한다.

A bracketed system notice occupies its own line between ordinary prose paragraphs on a visible page.

소유자: {"page": "text page", "notice": "bracketed isolated line", "prose": "ordinary paragraph"}

관계: notice → separated_from → prose; notice → printed_on → page

혼동 경계: 공중 홀로그램을 추가하지 않음; 소설 표기와 작중 시각을 구분

## U08 두 정보 영역의 대비

분류: 표시 매체 / displayed. 근거: S07.

둥근 아이콘의 개인 화면 옆에 각진 데이터 열의 기관 화면을 별도로 놓는다.

A personal display with rounded icons sits beside a separate institutional display with rigid aligned data columns.

소유자: {"left": "personal display", "right": "institutional display", "divider": "clear separation"}

관계: left → distinct_from → right; divider → between → left

혼동 경계: 브랜드 구도는 창작; UI만으로 선악·기업 정체 확정 불가

## I01 상태 요약과 능력치 표

분류: 정보 구조 / displayed. 근거: S04, S20.

상태 시트에서 식별 머리글·능력치 행·현재값과 최대값의 자원 구획을 나눈다.

A status sheet separates an identity header, labeled attribute rows, and a resource block with current and maximum values.

소유자: {"sheet": "status sheet", "header": "identity header", "stats": "attribute rows", "resources": "resource block"}

관계: header → inside → sheet; stats → inside → sheet; resources → inside → sheet; header → above → stats; resources → separate_from → stats

혼동 경계: 일반 대시보드와 비교; 숫자는 표시값이지 실제 능력 검증 아님

## I02 서로 다른 자원 막대

분류: 정보 구조 / displayed. 근거: S04.

HP·MP·스태미나 막대를 별도 라벨로 식별하고 채움 길이와 현재·최대 수를 다르게 한다.

Three separately labeled HP, MP, and stamina bars show different fill lengths and current/maximum numbers.

소유자: {"hp": "HP bar", "mp": "MP bar", "st": "stamina bar", "labels": "distinct resource labels"}

관계: labels → identify → hp; mp → parallel_to → hp; st → parallel_to → mp

혼동 경계: 색만으로 자원을 추정하지 않음; HP와 상처·피의 양은 비동치

## I03 레벨과 경험치 분리

분류: 정보 구조 / displayed. 근거: S04, S11.

레벨 표식 아래에 다음 기준값이 별도로 적힌 경험치 막대를 둔다.

A level badge sits above an experience bar whose threshold is separately labeled.

소유자: {"level": "level badge", "xp": "experience progress bar", "threshold": "next threshold"}

관계: xp → below → level; threshold → labels → xp

혼동 경계: 가득 찬 막대가 실제 레벨업 순간을 증명하지 않음

## I04 남은 포인트와 배분 선택

분류: 정보 구조 / displayed. 근거: S15, S20.

미사용 포인트 총량을 능력치 행 위에 두고 각 행 옆에 증가 선택을 정렬한다.

An unspent-point total sits above attribute rows with aligned increment controls on each row.

소유자: {"pool": "unspent point total", "rows": "attribute rows", "controls": "increment controls"}

관계: controls → beside → rows; pool → above → rows

혼동 경계: 능력치 증가의 실제 신체 효과와 분리; SP 약어는 풀어 적기

## I05 요구 조건이 있는 해금 그래프

분류: 정보 구조 / displayed. 근거: S05.

시작 노드가 선택된 분기와 연결되고 그 끝 잠금 노드에 요구 조건 라벨이 있다.

An entry node connects to a selected branch and a locked endpoint with a visible requirement label.

소유자: {"root": "entry node", "branch": "connected branch", "locked": "locked endpoint", "edge": "prerequisite connector"}

관계: edge → connects → root; edge → ends_at → branch; locked → beyond → branch

혼동 경계: 장식 별자리와 구분; 선행 연결과 단순 근접을 혼동하지 않음

## I06 직업 분기와 다중 직업

분류: 정보 구조 / displayed. 근거: S04, S05.

하나의 기본 직업 노드가 식별 라벨을 합치지 않은 두 직업 선택으로 갈라진다.

One base class node branches into two distinct class choices without merging their identity labels.

소유자: {"base": "base class node", "choices": "two class alternatives", "connector": "branch connector"}

관계: connector → starts_at → base; connector → reaches → choices

혼동 경계: 승급·전직·멀티클래스는 동일 문법 아님; 활성 상태를 별도 명시

## I07 종족 진화 선택과 현재 신체

분류: 정보 구조 / displayed. 근거: S14, S15.

현재 생물 실루엣에 현재 표식을 두고 두 형태 분기를 따로 표시한다.

A current creature silhouette is marked separately from two possible morphology branches.

소유자: {"body": "current creature silhouette", "choices": "two morphology branches", "marker": "current-state marker"}

관계: marker → labels → body; choices → branch_from → body

혼동 경계: 분기 표시가 실제 변신 완료를 뜻하지 않음; 몸 개수 증가 방지

## I08 비교 가능한 기록 값

분류: 정보 구조 / displayed. 근거: S03, S11.

날짜가 다른 두 상태 기록이 같은 식별자를 공유하되 이전·이후 값을 각각 적는다.

Two dated status records share one identity marker but show separately labeled earlier and later values.

소유자: {"old": "earlier labeled record", "new": "later labeled record", "id": "shared identity marker"}

관계: id → matches → old; id → matches → new; old → beside → new

혼동 경계: 숫자 차이는 기록의 주장; 실제 성장·회귀·동일 인물 입증은 별도

## Q01 퀘스트 목표와 물증 대응

분류: 퀘스트·경제 / still. 근거: S03, S04.

게시판 퀘스트 토큰과 계산대의 봉인 물품이 같은 목표 표식을 가진다.

A quest token on a board and a sealed parcel on the counter carry the same distinct objective symbol.

소유자: {"board": "quest board", "token": "objective-marked token", "parcel": "matching parcel"}

관계: token → attached_to → board; parcel → matches_symbol_of → token

혼동 경계: 심부름 표식과 비교; 수락·완료·보상 지급의 인과는 별도

## Q02 추적기와 장면 속 목표

분류: 퀘스트·경제 / displayed. 근거: S04.

목표 추적기가 장면 속 한 대상에 붙은 표식을 반복한다.

An objective tracker repeats the marker attached to one visible target in the scene.

소유자: {"tracker": "objective tracker", "target": "visible target", "symbol": "shared marker"}

관계: symbol → labels → target; tracker → references → symbol

혼동 경계: 장식 아이콘과 구분; 화살표만으로 정확한 도착지 판단 금지

## Q03 실패 조건과 경고 위계

분류: 퀘스트·경제 / displayed. 근거: S04, S06.

경고창에서 목표·실패 조건·두 선택을 강조 차이를 두고 나눈다.

A warning dialog separates the objective, failure condition, and two choice controls with distinct emphasis.

소유자: {"dialog": "warning dialog", "condition": "separate failure condition", "choices": "choice controls"}

관계: condition → inside → dialog; choices → below → condition

혼동 경계: 붉은색이 즉시 죽음이라는 공통 규칙은 아님; 거부 가능성은 실제 규칙 필요

## Q04 물건의 크기를 보존한 격자

분류: 퀘스트·경제 / displayed. 근거: S04, S05.

긴 아이템 하나가 인벤토리의 이웃한 여러 칸을 차지하고 빈칸은 구분된다.

One long item spans several adjacent inventory cells, leaving the empty cells visibly separate.

소유자: {"grid": "inventory grid", "item": "long item icon", "cells": "occupied adjacent cells"}

관계: item → spans → cells; cells → inside → grid

혼동 경계: 격자는 소지품 표현; 물체의 실제 차원 수납은 미증명

## Q05 장비 슬롯과 신체 부위

분류: 퀘스트·경제 / displayed. 근거: S04.

인체 도식의 머리·손 장비 슬롯을 각각 대응 부위와 연결한다.

A body diagram links distinct head and hand equipment slots to their corresponding regions.

소유자: {"figure": "body diagram", "head": "head slot", "hand": "hand slot", "lines": "slot connectors"}

관계: lines → connect_to → head; lines → connect_to → hand; head → above → figure

혼동 경계: 슬롯 아이콘과 실제 착용 구분; 화면 표시는 물리 접촉이 아님

## Q06 감정창과 조사 대상 연결

분류: 퀘스트·경제 / still. 근거: S04, S05.

감정창의 안내선 하나가 탁자의 고립된 물건 하나에 닿는다.

An inspection panel connects by one leader line to a single isolated item on the table.

소유자: {"item": "single inspected object", "panel": "inspection panel", "line": "leader line"}

관계: line → starts_at → panel; line → ends_at → item

혼동 경계: 다른 물건으로 연결하면 실패; 창의 내용은 진실성 보증 아님

## Q07 등급·옵션·내구도 분리

분류: 퀘스트·경제 / displayed. 근거: S05.

아이템 카드의 희귀도·옵션 목록·내구도 칸을 하나의 점수로 합치지 않고 구분한다.

An item card separates a rarity label, modifier list, and durability field rather than collapsing them into one score.

소유자: {"card": "item card", "rarity": "rarity label", "mods": "modifier block", "wear": "durability field"}

관계: rarity → separate_from → mods; wear → below → mods; mods → inside → card

혼동 경계: 보라색이 항상 고등급은 아님; 희귀도·성능·상태는 다른 축

## Q08 보석 소켓과 장착 경계

분류: 퀘스트·경제 / still. 근거: S05.

무기 몸체의 오목한 소켓 안에 보석이 놓이고 테두리가 보석 가장자리를 덮는다.

A gem sits within a recessed socket in a weapon, and the socket rim overlaps the gem edge.

소유자: {"weapon": "weapon body", "socket": "recessed socket", "gem": "inserted gem", "rim": "socket rim"}

관계: socket → part_of → weapon; gem → inside → socket; rim → occludes_edge_of → gem

혼동 경계: 장식 보석과 구분; 마법 효력·귀속 규칙은 외형만으로 불가

## Q09 제작 재료·작업·결과의 자리

분류: 퀘스트·경제 / still. 근거: S03, S04.

분리된 재료가 제작법 도식과 대응하고 도구는 미완성 작업물에 닿는다.

Separated recipe materials match a recipe diagram while a tool touches an unfinished workpiece.

소유자: {"recipe": "recipe diagram", "materials": "separated materials", "tool": "tool at workpiece", "workpiece": "unfinished object"}

관계: recipe → corresponds_to → materials; tool → contacts → workpiece

혼동 경계: 제작 성공·품질 상승은 미증명; 보통 공방과 시스템 정보 구별

## Q10 경매의 서로 다른 거래 위치

분류: 퀘스트·경제 / displayed. 근거: S05.

매물 하나에 아이템 식별자·희망 가격·현재 입찰가를 별도 칸으로 놓는다.

An item listing shows one item identifier, an asking price, and a distinct current bid field.

소유자: {"listing": "item listing", "price": "asking price", "bid": "separate bid", "item": "item identifier"}

관계: listing → references → item; price → inside → listing; bid → distinct_from → price

혼동 경계: 시스템 상점·플레이어 경매는 비동치; 거래 완료를 추정하지 않음

## Q11 덱·손패·버림패 구분

분류: 퀘스트·경제 / displayed. 근거: S18.

앞면 손패가 뒤집힌 드로 더미와 별도 라벨의 버림 더미 사이에 놓인다.

A face-up hand fan sits between a face-down draw stack and a separately labeled discard stack.

소유자: {"deck": "face-down draw stack", "hand": "face-up hand fan", "discard": "separate discard stack"}

관계: hand → between → deck; discard → separate_from → deck

혼동 경계: 카드 한 장으로 덱빌딩 입증 불가; 뽑기·수집·덱 구성 구별

## Q12 추첨 보상과 확률 표시

분류: 퀘스트·경제 / displayed. 근거: S13, S18.

확률 라벨을 붙인 보상 집합과 공개 결과 하나를 별도 영역에 표시한다.

A reward pool with labeled probabilities is displayed apart from one revealed result.

소유자: {"pool": "reward pool", "weights": "probability labels", "result": "separate revealed result"}

관계: weights → label → pool; result → separate_from → pool

혼동 경계: RNG·가챠·일반 드롭은 동의어 아님; 표시 확률의 실제 정확성 미증명

## C01 보호자와 피보호자의 위치

분류: 전투·협업 / still. 근거: S04.

방패 든 보호자가 적과 별도 아군 사이에 서서 방패를 적 쪽으로 향한다.

A shield-bearing protector stands between an opponent and a separate ally, with the shield facing the opponent.

소유자: {"tank": "shield-bearing protector", "ally": "protected ally", "enemy": "opponent", "shield": "shield"}

관계: tank → between → enemy; ally → behind → tank; shield → faces → enemy

혼동 경계: 갑옷 외형만으로 탱커 확정 금지; 어그로 수치는 별도

## C02 지원 효과의 발신자와 수신자

분류: 전투·협업 / still. 근거: S04.

지원 궤적 하나가 시전자의 손에서 시작해 별도 아군 장비에 닿는다.

One support arc visibly starts at a caster's hand and ends at a separate ally's equipment.

소유자: {"healer": "support caster", "ally": "separate recipient", "effect": "continuous support arc"}

관계: effect → starts_at → healer; effect → ends_at → ally

혼동 경계: 빛만으로 치유·강화 수치 단정 불가; 공격 궤적과 문맥 구별

## C03 시전 진행과 대기 음영

분류: 전투·협업 / displayed. 근거: S04.

시전 진행 막대와 일부가 부채꼴 대기 음영으로 덮인 스킬 아이콘을 분리한다.

A cast progress bar is separate from a skill icon covered by a partial radial cooldown mask.

소유자: {"cast": "cast progress bar", "icon": "skill icon", "mask": "radial cooldown mask"}

관계: mask → covers_part_of → icon; cast → separate_from → icon

혼동 경계: 시전·쿨다운·지속시간은 세 타이머; 정지 화면은 감소 속도 미증명

## C04 효과 아이콘의 소유 대상

분류: 전투·협업 / displayed. 근거: S04.

상태 아이콘이 선택 생물의 타깃 막대 옆에 있고 연결선은 해당 생물에 닿는다.

Status icons sit beside the selected creature's target bar with a clear connector to that creature.

소유자: {"target": "selected creature", "bar": "target bar", "effects": "status icons", "leader": "target connector"}

관계: effects → adjacent_to → bar; leader → connects → bar; leader → ends_at → target

혼동 경계: 버프·디버프 소유자 혼동 방지; 독·정신지배 원인은 아이콘만으로 미확정

## C05 범위 경계와 안팎 위치

분류: 전투·협업 / still. 근거: S04.

연속 바닥의 경계 표식 안에 한 인물, 경계 밖에 다른 인물을 분명히 둔다.

A bounded marker lies on continuous ground with one figure inside and another clearly outside its edge.

소유자: {"zone": "bounded ground marker", "inside": "one figure inside", "outside": "one figure outside", "floor": "continuous floor"}

관계: zone → lies_on → floor; inside → inside → zone; outside → outside → zone

혼동 경계: 마법진 자체가 광역 피해 아님; 친구·적·피해 규칙은 문맥

## C06 공격 수치와 타격 대상

분류: 전투·협업 / displayed. 근거: S04, S06.

전투 숫자 하나를 단일 대상의 타격 지점 가까이에 두고 다른 이름표와 분리한다.

One combat number sits near a visible impact point on a single target, apart from other nameplates.

소유자: {"number": "combat number", "target": "one struck target", "impact": "visible impact point"}

관계: number → near → impact; impact → on → target

혼동 경계: 피해·치명·회복은 라벨과 규칙 필요; 큰 글씨가 치명타 보증 아님

## C07 분리된 소환·동료 개체

분류: 전투·협업 / still. 근거: S04.

별도 생물이 시전자 옆 바닥에 서고 두 존재 사이에 독립된 연결 표식을 둔다.

A separate creature stands on the ground beside a caster with one distinct linking indicator between them.

소유자: {"caster": "one caster", "companion": "separate creature", "connection": "control indicator", "floor": "floor"}

관계: connection → starts_at → caster; connection → ends_at → companion; companion → supported_by → floor

혼동 경계: 분신·야생동물·소환·조련은 비동치; 자율성과 소유권 미확정

## C08 파티 목록과 인물 대응

분류: 전투·협업 / displayed. 근거: S04.

서로 다른 인물 위 역할 표식이 개별 자원 행을 가진 파티 목록에 반복된다.

Distinct role markers above separate figures repeat in a compact party list with individual resource rows.

소유자: {"party": "list of members", "figures": "distinct party figures", "marks": "matching role markers"}

관계: marks → identify → figures; party → repeats → marks

혼동 경계: 사람 수와 목록 수 일치 확인; 단순 군중이 레이드 아님

## W01 게이트 경계와 목적 공간

분류: 세계·성장 주체 / still. 근거: S14.

연속된 입구 테두리가 가까운 바닥과 그 너머 다른 공간을 가른다.

A continuous aperture rim separates near ground from a different visible space beyond it.

소유자: {"gate": "freestanding aperture", "near": "near ground", "far": "different space", "rim": "continuous rim"}

관계: rim → bounds → gate; gate → between → near; far → visible_through → gate

혼동 경계: 문·마법진·던전은 동일하지 않음; 인스턴스 복제 여부 미증명

## W02 층별 경로와 도달 지점

분류: 세계·성장 주체 / still. 근거: S18.

보이는 경로가 층들을 연결하며 뚜렷한 표식의 층 도착점에 닿는다.

A visible route connects stacked levels and reaches a distinctly marked landing.

소유자: {"tower": "stacked levels", "route": "connecting route", "landing": "marked landing"}

관계: route → connects_levels_of → tower; landing → on → route

혼동 경계: 수직 건물만으로 탑등반 장르 아님; 층별 시험은 문맥

## W03 코어와 관리 공간의 대응

분류: 세계·성장 주체 / still. 근거: S14.

중앙 코어 물체에서 독립된 연결선들이 별도 방 모형들에 닿는다.

A central core object connects to separate room models through distinct visible lines.

소유자: {"core": "central core object", "rooms": "separate room models", "links": "room-control connectors"}

관계: links → start_at → core; links → end_at → rooms

혼동 경계: 보석 보물과 구분; 코어의 의식·던전 전체 지배는 미확정

## W04 안전 경계와 접근 조건

분류: 세계·성장 주체 / displayed. 근거: S04, S12.

표시 경계가 진입점과 위험 구역을 나누고 입구 옆에 접근 조건 표지가 있다.

A marked boundary separates an entry point from a hazard area, with an explicit access-condition sign at the entry.

소유자: {"boundary": "marked boundary", "outside": "hazard area", "sign": "access condition", "entry": "entry point"}

관계: sign → beside → entry; boundary → separates → outside

혼동 경계: 밝은 원=절대 안전 아님; 레벨 제한·면역의 작동은 미검증

## W05 거점의 생산 흐름

분류: 세계·성장 주체 / still. 근거: S03, S14.

거점 도면 안 자원 저장소와 작업장을 생산 경로로 연결한다.

Marked production routes connect a resource store to a workshop within a settlement plan.

소유자: {"store": "resource store", "workshop": "workshop", "settlement": "settlement plan", "routes": "marked production routes"}

관계: routes → connect → store; routes → end_at → workshop; workshop → part_of → settlement

혼동 경계: 일반 건축 모형과 비교; 인구 성장·왕국 통치·자동 생산은 문맥

## W06 생활 기술과 시스템 기록

분류: 세계·성장 주체 / still. 근거: S03, S11.

작업 도구가 음식에 닿고 요리 작업대 옆에 별도 숙련 기록을 둔다.

A working utensil contacts prepared food while a separate skill record stands beside the cook's workspace.

소유자: {"cook": "working cook", "tool": "working utensil", "food": "prepared food", "record": "skill record"}

관계: tool → contacts → food; record → beside → cook

혼동 경계: 생활물과 cozy 정서는 비동치; 도구 배치가 실제 숙련 상승은 아님

## D01 재출현 지점과 남은 장비

분류: 죽음·이력 / still. 근거: S12, S03.

재시작 표식과 남겨진 장비를 서로 다른 위치에 놓고 보이는 경로로 잇는다.

A restart marker and abandoned equipment occupy separate locations linked by a visible route.

소유자: {"marker": "restart marker", "gear": "abandoned gear", "route": "route between locations"}

관계: route → starts_at → marker; route → ends_at → gear

혼동 경계: 시체 회수·리스폰·부활·회귀는 비동치; 과거 죽음은 정지 사진 미증명

## D02 손실 항목의 명시

분류: 죽음·이력 / displayed. 근거: S12.

사망 손실 기록에서 경험치·장비 손실 칸을 나누고 규칙 적용 범위를 적는다.

A death-loss record separates experience and equipment loss fields and names the scope of the rule.

소유자: {"record": "death-loss record", "xp": "experience loss field", "gear": "equipment loss field", "scope": "rule scope"}

관계: xp → inside → record; gear → separate_from → xp; scope → labels → record

혼동 경계: 붉은 창만으로 영구 사망·전체 약탈 추정 금지

## D03 같은 식별자의 반복 기록

분류: 죽음·이력 / displayed. 근거: S03.

서로 다른 시도 행마다 한 식별자를 반복하고 결과·시각을 다르게 적는다.

Separate attempt rows repeat one identifier while displaying distinct outcomes and timestamps.

소유자: {"rows": "separate attempt rows", "id": "shared identifier", "outcomes": "distinct outcomes"}

관계: id → repeats_in → rows; outcomes → label → rows

혼동 경계: 시도 기록과 실제 시간 반복 구분; 동일 인격 연속성은 별도

## H01 손상된 장비와 신체 경계

분류: 폭력·신체 / still. 근거: S12, S13.

파손 갑옷 판의 틈과 그 뒤 착용자의 신체 표면을 구분한다.

A broken armor plate has a visible fracture gap while the wearer's body remains a separate surface behind it.

소유자: {"armor": "damaged armor plate", "body": "wearer's body", "gap": "broken plate gap"}

관계: gap → inside → armor; armor → worn_by → body

혼동 경계: 방어구 손상·신체 손상·성적 노출은 독립; 자동 탈의 금지

## H02 변형 부위와 정상 부위 경계

분류: 폭력·신체 / still. 근거: S13, S17.

연속된 사지 하나의 변형 표면과 정상 표면 사이에 경계를 둔다.

One continuous limb carries a sharply bounded changed surface next to an ordinary surface region.

소유자: {"limb": "one limb", "changed": "changed surface region", "ordinary": "ordinary region", "seam": "continuous transition"}

관계: changed → part_of → limb; ordinary → part_of → limb; seam → between → changed

혼동 경계: 바디 호러·단순 유혈 구별; 강제성·원인·통증은 미확정

## H03 부착체와 숙주의 경계

분류: 폭력·신체 / still. 근거: S13.

부착 생물은 독립 윤곽을 가지며 숙주 표면의 접합 경계가 보인다.

An attached organism has its own outline and a visible contact seam on the host surface.

소유자: {"host": "host surface", "organism": "attached organism", "attachment": "contact seam"}

관계: organism → distinct_from → host; attachment → connects → organism; attachment → touches → host

혼동 경계: 장식·기생·공생의 인과 차이; 촉수 존재가 성적 내용은 아님

## H04 오염 표시와 변화 대상

분류: 폭력·신체 / displayed. 근거: S13.

오염 라벨의 게이지가 장면 전체가 아닌 특정 인물 하나와 연결된다.

A labeled corruption meter connects to one specific figure rather than the whole scene.

소유자: {"meter": "corruption meter", "body": "affected figure", "connector": "ownership connector"}

관계: connector → starts_at → meter; connector → ends_at → body

혼동 경계: 오염=도덕적 악·정신질환 아님; 색·게이지만으로 진단 금지

## R01 관계도와 복수 인물

분류: 관계·권한 / displayed. 근거: S13.

관계 라벨을 붙인 선이 중심 인물 노드와 여러 개별 인물 노드를 잇는다.

Labeled relationship edges connect a central person node to several separate person nodes.

소유자: {"center": "central person node", "others": "separate person nodes", "edges": "labeled relationship edges"}

관계: edges → start_at → center; edges → end_at → others

혼동 경계: 하렘·역하렘·합의된 다자관계·단순 파티 비동치; 동의는 외형 미증명

## R02 호감도 표시와 감정의 구별

분류: 관계·권한 / displayed. 근거: S13.

관계 패널이 특정 인물을 식별하고 호감도라는 라벨의 값을 표시한다.

A relationship panel names one referenced person and shows a clearly labeled affinity value.

소유자: {"panel": "relationship panel", "person": "referenced person", "value": "displayed affinity value", "id": "identifier"}

관계: id → links → panel; id → identifies → person; value → inside → panel

혼동 경계: 수치가 실제 감정·복종·동의임을 뜻하지 않음; 미소는 검증 대체 불가

## R03 명령 권한과 구속 계약

분류: 관계·권한 / displayed. 근거: S13.

계약 기록에서 발행자·대상자 칸과 구체적인 제한 조항을 구분한다.

A contract record separates issuer and recipient fields from a specific restriction clause.

소유자: {"contract": "contract record", "issuer": "issuer field", "recipient": "recipient field", "restriction": "restriction clause"}

관계: issuer → inside → contract; recipient → distinct_from → issuer; restriction → below → recipient

혼동 경계: 구속 계약·노예제·합의된 권력교환은 동의어 아님; 목걸이로 판정 금지

## R04 관전·후원 정보와 대상

분류: 관계·권한 / displayed. 근거: S06, S07.

관전 피드의 누적 메시지와 별도 후원 표식을 특정 수신자 식별자 옆에 둔다.

An observer feed contains stacked messages and a separate donation badge beside one recipient identifier.

소유자: {"feed": "observer feed", "recipient": "recipient identifier", "messages": "stacked messages", "reward": "separate donation badge"}

관계: messages → inside → feed; reward → beside → recipient

혼동 경계: 별·채팅창만으로 성좌 후원 확정 불가; 실시간 갱신은 시간 증거

## R05 혈통 도식과 생식 기록

분류: 관계·권한 / displayed. 근거: S13.

세대별 노드의 혈통 도식과 허구의 생식력 수치 기록을 분리한다.

A family chart connects separate generation nodes while a fictional fertility field is kept in a separate record.

소유자: {"chart": "family chart", "nodes": "separate family nodes", "links": "descent links", "record": "separate fictional fertility field"}

관계: links → connect → nodes; record → separate_from → chart

혼동 경계: 임신·성행위·강제 생식은 도식·복부 외형으로 입증 불가

## E01 이름표와 정확한 대상

분류: UI 구성 / displayed. 근거: S04.

짧은 연결선이 이름표 하나와 인물 하나를 잇고 다른 머리를 가로지르지 않는다.

A short line joins one nameplate to exactly one character without crossing another person's head.

소유자: {"plate": "nameplate", "target": "single character", "line": "short ownership line"}

관계: line → starts_at → plate; line → ends_at → target

혼동 경계: 이름표와 일반 자막 구분; 정체성·플레이어/NPC 여부는 문맥

## E02 원형 선택과 한 선택지

분류: UI 구성 / displayed. 근거: S04, S06.

원형 선택기에 구분된 부채꼴들을 두고 그중 하나만 선택 상태로 표시한다.

A radial choice ring contains separated wedges with exactly one visibly selected wedge.

소유자: {"ring": "radial choice ring", "segments": "separate wedges", "selected": "one highlighted wedge"}

관계: segments → part_of → ring; selected → one_of → segments

혼동 경계: 조준기·마법진과 구분; 입력 방식·선택 완료는 미증명

## E03 하위 정보의 펼침

분류: UI 구성 / displayed. 근거: S04.

선택 행과 펼친 상세창이 같은 표식을 공유하며 다른 행과 분리된다.

A selected row and an expanded detail panel share one marker with clear separation from other rows.

소유자: {"row": "selected item row", "detail": "expanded detail panel", "anchor": "shared row marker"}

관계: anchor → labels → row; anchor → repeats_in → detail; detail → beside → row

혼동 경계: 정보 확장의 현재 배치만; 열리는 애니메이션은 시간 필요

## E04 탐색 지도와 미탐색 경계

분류: UI 구성 / displayed. 근거: S04, S18.

지도에서 윤곽이 있는 탐색 영역과 가려진 미탐색 영역의 경계를 구분한다.

A map separates an outlined known region from a masked unknown region with a clean boundary.

소유자: {"map": "map field", "known": "known region", "hidden": "masked region", "edge": "mask boundary"}

관계: known → inside → map; hidden → inside → map; edge → between → known

혼동 경계: 구름·검열·안개 날씨와 구분; 일반 지도만으로 실제 탐색 이력 불가

## E05 잠금·알 수 없음·손상 분리

분류: UI 구성 / displayed. 근거: S04, S10.

한 패널에서 잠금 칸·값 미확인 칸·정렬 손상 칸을 서로 다르게 표시한다.

One panel distinguishes a locked field, an unknown-value field, and a visibly misaligned damaged field.

소유자: {"locked": "locked field", "unknown": "unknown field", "broken": "misaligned field", "panel": "containing panel"}

관계: locked → inside → panel; unknown → distinct_from → locked; broken → distinct_from → unknown

혼동 경계: 검열·미해금·오류·불신뢰 시스템을 하나로 합치지 않음

## E06 정돈된 로그와 단발 알림

분류: UI 구성 / displayed. 근거: S04, S11.

시각이 붙은 로그 행 영역과 단일 획득 알림을 떨어뜨려 놓는다.

Timestamped log rows occupy one area while a single isolated acquisition notice sits apart from them.

소유자: {"log": "timestamped log rows", "toast": "one isolated notice", "gap": "visible separation"}

관계: toast → separate_from → log; gap → between → toast

혼동 경계: 알림의 잠깐 출현·중복 재발은 단일 프레임으로 불가

## X01 장르 분류는 규칙·서사 문맥

분류: 비시각 문맥 / context. 근거: S01, S02.

장르 분류에는 게임 규칙의 서사적 역할이 필요하며 푸른 패널만으로 충분하지 않다.

Genre classification needs the role of game rules in the story; a blue panel alone is insufficient.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: LitRPG·GameLit·성장물·이세계·VR·헌터물·코지의 비동치

## X02 사적 시각과 작중 존재

분류: 비시각 문맥 / context. 근거: S08, S09.

인터페이스를 누가 인지하는지와 화면 어디에 놓이는지를 별도로 명시한다.

Specify who can perceive the interface separately from where it appears in the frame.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 다른 사람이 반응하지 않는 한 장면은 안 보인다는 증거 아님

## X03 머리·시야·세계 고정

분류: 비시각 문맥 / sequence. 근거: S10.

머리를 따르거나 세계에 고정됐다는 판정은 여러 시점 비교가 필요하다.

Compare multiple views before claiming an interface follows the head or stays fixed in the world.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 한 프레임의 원근·모서리 위치만으로 추종 규칙 확정 금지

## X04 스탯의 계산 의미

분류: 비시각 문맥 / context. 근거: S20.

DEX·AGI·SP·HP·파생 수치의 작품별 뜻을 확인한 뒤 라벨을 선택한다.

Resolve local definitions for DEX, AGI, SP, HP, and derived values before choosing visual labels.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: CHA=미모·INT=IQ·HP=혈액량으로 치환 금지

## X05 전투 효율·확률·빌드

분류: 비시각 문맥 / context. 근거: S04, S05.

DPS·치명 확률·최적화·시너지·유리대포 빌드는 규칙이나 비교 결과가 필요하다.

Damage rate, critical chance, min-maxing, synergy, and a glass-cannon build need rules or comparative outcomes.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 큰 무기·빛·가녀린 체형은 전투 성능 증거가 아님

## X06 반복 성장과 시간 변화

분류: 비시각 문맥 / sequence. 근거: S03.

그라인딩·파밍·로테이션·지속 피해·반복 퀘스트에는 순서 있는 사건 또는 표시 기록이 필요하다.

Grinding, farming, rotations, damage-over-time, and repeated quests require ordered events or explicitly displayed records.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 기록의 주장을 실제 시간 증거와 구분

## X07 죽음 이후의 동일성과 복귀

분류: 비시각 문맥 / sequence. 근거: S12, S03.

리스폰·부활·회귀·환생·시간 루프는 규칙과 사건 순서로 구분한다.

Distinguish respawn, resurrection, regression, reincarnation, and time loops using the rule and ordered events.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 같은 얼굴 두 명·문·묘비는 동치 증거가 아님

## X08 권한·자각·신뢰

분류: 비시각 문맥 / context. 근거: S07, S08.

관리자 권한·NPC 자각·거짓 시스템 정보는 서사 문맥이 필요하다.

Administrator authority, NPC self-awareness, and deceptive system information require narrative context.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 왕관·로봇 얼굴·글리치·관객 응시만으로 판정 금지

## X09 동의와 강요

분류: 비시각 문맥 / context. 근거: S13.

동의·강요·불분명한 동의·비동의는 매력이나 장신구와 독립된 문맥 주장으로 둔다.

Keep consent, coercion, ambiguous consent, and non-consent as contextual claims, independent of attractiveness or accessories.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 미소·침묵·수치·목걸이·노출로 동의 추론 금지

## X10 관계 구성과 표현 수위

분류: 비시각 문맥 / context. 근거: S13.

관계 구성·성적 상세함·페티시 강조·장면 생략 전환을 분리한다.

Separate relationship topology from sexual explicitness, fetish emphasis, and a fade-to-black narrative transition.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: BL·GL·하렘·다자연애·비인간 로맨스 자체는 노골적 성행위 아님

## X11 기억·정체성·원작 지식

분류: 비시각 문맥 / context. 근거: S02, S03.

사전 지식·메타게이밍·몸 교환·기억 소실에는 지식·정체성 이력이 필요하다.

Foreknowledge, metagaming, body swaps, and erased memory require a specified knowledge or identity history.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 거울·동일 얼굴·화면 오류가 기억이나 성 정체성을 증명하지 않음

## X12 통증·정신 안정·영혼

분류: 비시각 문맥 / context. 근거: S13.

통증 피드백·정신 안정 수치·영혼 손상·소멸은 허구 문맥이며 의학적 진단이 아니다.

Pain feedback, sanity points, soul damage, and soul destruction are fictional context claims rather than medical diagnoses.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 표정·게이지·기하학 효과만으로 통증·정신건강·영혼 존재 판단 금지

## X13 상해 강도·원인·반복 가해

분류: 비시각 문맥 / context. 근거: S13.

보이는 상해·묘사 상세함·고문 의도·부활 반복 가해를 구분한다.

Separate visible injury, graphic detail, torture intent, and repeated harm through resurrection.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 피가 많음=고문·스플래터·바디 호러·잔혹한 정치 모두 아님

## X14 출산·생식·혈통·금기

분류: 비시각 문맥 / context. 근거: S13.

생식력·생식 통제·배신·금기 관계에는 명시적인 허구 문맥이 필요하다.

Fertility, reproductive control, betrayal, and taboo relationships need explicit fictional context.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 배의 형태·나이 추정·혈통 도식으로 임신·성적 행위·강요 판정 금지

## X15 공개 정보와 감시·후원

분류: 비시각 문맥 / context. 근거: S06, S07.

파티 정보·관전·후원·평판·업보의 수신자와 권한을 명시한다.

Resolve the recipients and permissions of party information, spectatorship, sponsorship, reputation, and karma.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 채팅창·군중·별무늬만으로 성좌·감시·도덕 판단 증명 금지

## X16 오류·허점·쉬운 공략

분류: 비시각 문맥 / context. 근거: S05, S08.

오류·허점 이용·치트 능력·쉬운 전술을 의도된 규칙과의 관계로 구분한다.

Distinguish a glitch, exploit, cheat ability, and easy tactic by their relation to the intended rules.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 깨진 글자나 승리 장면만으로 해킹·버그·부정행위 확정 금지

## X17 표시의 진실성

분류: 비시각 문맥 / context. 근거: S08, S13.

스탯·계약·확률·관계 수치는 무엇이 표시됐는지 입증하며 시스템의 진실성을 보증하지 않는다.

A displayed stat, contract, probability, or relationship score proves what is shown, not that the system reports truth.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 숫자 정확도와 사실 정확도는 독립

## X18 등장·소멸·거부 가능성

분류: 비시각 문맥 / sequence. 근거: S04, S21.

개폐·강제 재등장·제스처 조작·카운트다운 움직임은 연속 증거가 필요하다.

Opening, closing, forced reappearance, gesture control, and countdown motion need sequential evidence.

소유자: {}

관계: 시각 후보 없음. 문맥 또는 연속 증거 필요.

혼동 경계: 손을 댄 한 장면은 실제 입력 반응·거부 가능성을 증명하지 않음

