# 반영 후 실행할 검증 사례

아래 36개 holdout과 8개 pixel family는 설계만 작성했다. 현재 retrieval 결과나 생성 이미지 합격 기록이 아니다.

## 요청·문맥·소유자 holdout 36개

|ID|문맥/요청|기대 결과|
|---|---|---|
|H01 regional_hair|뒷머리는 목덜미 위에서 끝나고 얼굴 양옆의 두 묶인 가닥만 가슴까지 내려오는 머리.|새 regional-length 후보를 노출하며 긴 전체 뒷머리는 추가하지 않는다.|
|H02 regional_hair|뒷머리 전체도 허리까지 길고 얼굴 옆 짧은 두 패널만 턱에서 일자로 잘린 히메컷.|K09는 채택하지 않고 긴 후면을 유지하는 hime_cut_structural을 대조한다.|
|H03 headset|귓가 수신부에서 얇은 마이크 막대가 연결되어 같은 인물의 입 옆에서 끝난다.|earpiece-mouth 연결을 same owner로 보존한다.|
|H04 headset|마이크 없는 헤드폰을 쓰고 다른 사람이 앞에서 손 마이크를 든다.|K51 hard activation 0; 두 인물/장치를 결합하지 않는다.|
|H05 equalizer|치마 면에 같은 간격의 세로 블록 열이 있으며 각 열의 높이가 다르다. 전부 납작한 프린트다.|평면 높이차 막대 후보를 노출하고 음향 작동을 추가하지 않는다.|
|H06 equalizer|뒤쪽 독립 모니터에 이퀄라이저가 보이고 인물의 치마는 아무 무늬도 없다.|의복 K53 채택 0; 배경 모니터에서 의복으로 carrier를 옮기지 않는다.|
|H07 keyboard|밑단 천에 긴 흰 직사각형 열과 그 위쪽에 어긋난 짧은 검정 칸이 인쇄되어 있다.|flat garment motif를 보존하며 악기를 추가하지 않는다.|
|H08 keyboard|손으로 실제 키보드 악기를 들고 있다. 치마에는 건반무늬가 없다.|K54 hard activation 0; MIDI 외부 sound-source도 요청 없이 추가하지 않는다.|
|H09 panel_graphic|분리 소매 바깥의 사각 테두리 안에 작은 선과 버튼 모양이 납작하게 인쇄되어 있다.|그래픽 패널의 평면 carrier를 보존한다.|
|H10 panel_graphic|소매 표면에 실제 단추들이 돌출되어 있지만 표시창이나 인쇄 패널은 없다.|K55는 채택하지 않고 surface fastener의 입체 조건을 대조한다.|
|H11 crop_length|상의 밑단이 자연 허리보다 높고 높은 하의는 피부를 완전히 가린다.|crop 길이만 노출; 피부 간격/복부 cutout 의무 0.|
|H12 crop_length|목부터 골반까지 한 벌로 이어진 옷의 중앙에만 구멍이 있고 상의가 따로 끊기지는 않는다.|K34는 채택하지 않고 K35의 한 벌 개방 구조와 대조한다.|
|H13 abdominal_opening|같은 몸판의 배 부분에 테두리가 닫힌 타원형 구멍이 있고 주변 천은 계속 이어진다.|bounded opening과 fabric bridge를 보존한다.|
|H14 abdominal_opening|짧은 상의와 치마 사이로 배가 보일 뿐 몸판에 구멍은 없다.|K35 hard activation 0; 두 벌 간격을 구멍으로 바꾸지 않는다.|
|H15 rear_panel|앞은 짧고 허리 뒷부분에만 긴 장식 패널 하나가 붙는다. 바닥에는 닿지 않는다.|attached rear panel을 유지하며 train/tailcoat 전체를 추가하지 않는다.|
|H16 rear_panel|별도 짧은 재킷 뒤 배경에 긴 천이 떠 있을 뿐 두 천은 연결되지 않는다.|K44 hard activation 0; 무관한 천을 의상 뒷자락으로 연결하지 않는다.|
|H17 hair_hardware|양갈래 묶음 뿌리 바로 옆에 단단한 각진 고리를 고정한다. 빛나지는 않는다.|hair tie carrier를 보존; 자체 발광/귀 장치 강제 0.|
|H18 hair_hardware|머리에는 리본만 있으며 각진 장치는 옆 탁자 위에 따로 놓여 있다.|K52 hard activation 0; prop를 머리 장식으로 붙이지 않는다.|
|H19 arm_gear|양팔 지지부에 손보다 큰 원형 장치가 연결되고 바깥 고리 안에 동심원 면이 보인다.|팔 연결·원형 구조·상대 크기를 모두 요구한다.|
|H20 arm_gear|배경의 큰 원형 스피커 앞에 인물이 서 있지만 손과 팔은 장치와 떨어져 있다.|K56 hard activation 0; 배경과 팔의 owner를 섞지 않는다.|
|H21 cap_cross|작은 모자의 앞면에 주황 십자 그림이 있다. 얼굴에는 아무 표식도 없다.|cap carrier와 선택한 주황색을 보존; 붉은 십자 기본값 0.|
|H22 cap_cross|모자는 없고 한쪽 볼에 작은 십자만 그려져 있다.|K68 hard activation 0; cheek glyph와 cap glyph를 구분한다.|
|H23 membrane_wings|등의 외부 의상 지지대에 가는 골격과 오목한 막 가장자리를 가진 날개를 달았다.|wearable external wings를 보존; human anatomy 변경 0.|
|H24 membrane_wings|명시한 비인간 생물의 몸에서 막 날개가 자라며 외부 의상 지지대는 없다.|K61 wearer-accessory 채택 0; creature ca_membrane_wings의 범위를 대조한다.|
|H25 thin_wing_plates|등 뒤 외부 프레임에 얇은 판 날개가 있고 선무늬는 판 안에 인쇄되어 있다. 판의 불투명 재질은 변경 금지다.|판·프린트·부착 후보만 채택하고 고정된 불투명 재질을 투명/발광으로 바꾸지 않는다.|
|H26 thin_wing_plates|배경에 투명 나비 그림이 있지만 인물 등에는 아무 부속도 없다.|K62 hard activation 0; 배경 장식을 착용자에 붙이지 않는다.|
|H27 cheek_glyph|한쪽 뺨 피부 위의 작은 닫힌 별 도상이 경계 안에 붙어 있다.|피부 glyph를 보존; 상처/혈액/홍채 전이 0.|
|H28 cheek_glyph|붉은 별은 모자에만 있고 뺨에는 그림자만 드리워져 있다.|K17 hard activation 0; cap/body, mark/shadow를 구분한다.|
|H29 negation|이퀄라이저 무늬가 없는 치마와 마이크 없는 헤드폰. 분리 소매는 요청하지 않는다.|K53/K51의 negated exact terms로 hard activation을 만들지 않는다.|
|H30 property_lock|낮은 양갈래의 묶임 높이는 변경 금지. 옷 무늬만 열려 있다.|high twin-tail와 hair geometry 후보는 locked property를 변경하지 않는다.|
|H31 year_unspecified_geometry|Snow Miku 2026 느낌이라는 이름만 있고 모자·치마·장식 구조는 아직 정하지 않았다.|연도/고유명사로 2010 얼음 배색과 2026 디저트 장식을 자동 묶지 않는다. 필요한 구조를 의미 clarification으로 둔다.|
|H32 module_name|모듈 이름 堕悪天使만 적혀 있고 날개의 형태나 부착 요청은 없다.|이름으로 K61/K62 hard obligation을 만들지 않는다.|
|H33 chibi_boundary|같은 캐릭터의 공식 chibi 그림에서 머리가 매우 크다. 사진 인물의 체형은 고정한다.|chibi ratio를 adult morphology로 자동 전이하거나 연령을 추론하지 않는다.|
|H34 adult_reference|명시된 성인 인물을 같은 깊이의 기준자 옆에서 작게 보이게 한다. 사지 굵기는 고정이다.|기존 bm_stature_scale만 조건부 검토; chibi/가느다란 사지 추가 0.|
|H35 unresolved_prop_scope|인물은 봉제 토끼 소품 하나를 손에 든다. 인물의 몸은 봉제 재질이 아니다.|plush prop source inspiration은 유지하되 현재 비어 있는 prop effect scope로 자동 morphology obligation을 만들지 않는다.|
|H36 companion_owner|사람 옆 별도 둥근 로봇이 있고 둘 사이 코드가 보인다. 사람 모자와 등 장치의 형태는 고정이다.|동료를 사람의 관절/장식으로 합치지 않으며 no-tether/floating 의미도 추가하지 않는다.|

## 원본 픽셀 family 8개

|ID|검증 대상|필수 관계|선행 조건|
|---|---|---|---|
|P01 머리 지역 길이|성인 인물/가발, 뒤 짧은 영역과 두 긴 앞다발이 함께 읽히는 시점|후두부 길이와 얼굴 옆 두 긴 다발이 같은 머리에 속한다.|data/profile/index/holdout gates complete|
|P02 평면 의상 무늬|일러스트, 소매와 치마 면이 충분히 큰 구도|막대 높이차·긴/짧은 건반 배치·사각 패널이 각 지정 의복면에 붙어 있다. 실제 악기/돌출 버튼/발광으로 바뀌면 FAIL.|data/profile/index/holdout gates complete|
|P03 머리 장치와 입 마이크|같은 착용자의 머리 묶임점과 귀/입이 함께 보이는 구도|머리 hardware의 모발 부착과 earpiece-boom-mouth 연결을 서로 다른 조립체로 모두 확인한다.|data/profile/index/holdout gates complete|
|P04 의상 개방 구조|별도 두 frozen requests: crop hem / 한 벌의 bounded abdominal opening|각 request에 해당하는 밑단 또는 closed cutout만 요구한다. 두 벌 간격을 한 벌 구멍으로 치환하면 FAIL.|data/profile/index/holdout gates complete|
|P05 팔의 원형 착용 장치|상반신과 장치 지지부가 가려지지 않는 일러스트|원형 외곽·동심원 면·팔 부착·상대 크기가 모두 동일한 owner 관계를 만족한다.|data/profile/index/holdout gates complete|
|P06 외부 날개 판|외부 프레임이 보이는 피규어 표현|얇은 판과 내부 선무늬·판 사이 겹침/투과·외부 지지부를 확인한다. 생물 관절이나 발광 기능으로 바뀌면 FAIL.|data/profile/index/holdout gates complete|
|P07 뺨 표식과 모자 표식|성인 인물/모자, 피부 표식과 모자 앞면을 모두 읽는 구도|별은 뺨 피부, 십자는 모자 앞면에 각각 귀속되고 도상/위치가 맞는다. owner가 뒤바뀌면 FAIL.|data/profile/index/holdout gates complete|
|P08 독립 소품/동료 소유자|사람·봉제 소품·별도 동료를 요청이 명시한 장면|소품과 동료의 경계·부착/손 접촉·가시 코드 등 요청된 연결만 확인한다. 신체융합/무연결 부유 추정은 FAIL.|P2 independent prop owner/effect routing must be resolved first; otherwise do not execute|

baseline/enriched 두 arm은 각각 동일하게 독립 작성한 frozen request/core를 사용한다. P04는 crop/cutout 두 요청으로 분리한다. 실제 이미지 수·반복 수·비용은 실행 시 확정하며 이번 작업에서는 생성하지 않았다.
