"""Authored scene proposals, not historical reconstructions or active candidates."""

VISUAL = []
def V(cid, terms, sources, scope, entities, relations, en, ko, boundary, gates, slots, review=False):
    nodes = entities.split(';')
    VISUAL.append(dict(
        id=cid, terms=terms.split(';'), source_ids=sources.split(), scope=scope,
        kind='bounded_visual_proposal',
        components=[dict(id=n, owner=n.split('.')[0], description=n.replace('_',' ')) for n in nodes],
        relations=[dict(subject=a,type=b,object=c) for a,b,c in (r.split('>') for r in relations.split(';'))],
        visible_en=en, visible_ko=ko, confusion_boundary_ko=boundary,
        pixel_gates_ko=gates.split(';'), proposed_slots=slots.split(),
        additional_source_plate_review_required=review,
        source_support_scope='Sources support the named distinction or historical context only. Actors, count, layout, viewpoint, causal staging and fantasy mechanisms are authored choices, not source facts.',
        historical_reconstruction_approved=False, source_image_review='NOT_RUN',
        bilingual_review='paired authored draft; independent review pending',
        automatic_activation=False, native_approval=False, runtime_registration='none',
        pixel_status='NOT_RUN', adoption='optional_after_independent_core',
    ))

V('A01','영지;장원;장원 저택;영지 경영물','S01 S04','authored estate landscape; no inferred title',
 'hall;village;fields;road;storehouse','road>connects>village;road>connects>storehouse;fields>beside>village',
 'A track links the village and field edge to a storehouse below the estate hall; loaded carts occupy that same continuous route.',
 '길 하나가 마을·밭 가장자리와 저택 아래 창고를 연결하고, 짐 실은 수레가 그 이어진 길 위에 놓인다.',
 '성이나 왕좌만 있는 풍경과 구별. 보이는 연결망은 법적 장원·봉토·직영지 소유권을 증명하지 않는다.',
 '마을·밭·창고를 잇는 같은 길;길 위 수레의 접지와 짐;저택과 생산 공간의 공간 구별','location composition narrative_clue')
V('A02','공동경지;띠밭;삼포제;휴경','S07 S13','selected English open-field inspiration',
 'field;field.strips;field.headland;crop;grazing_patch','field.strips>terminate_at>field.headland;crop>grows_on>field.strips;grazing_patch>beside>field.strips',
 'Long narrow cultivated strips end at a shared headland, beside a separate grazed patch with short vegetation.',
 '길고 좁은 경작 띠가 공통 머리땅에서 끝나고, 그 옆 별도 구획에는 짧은 풀이 남아 있다.',
 '격자형 현대 밭과 구별. 세 구획·세 색만으로 삼포제나 해마다의 윤작을 확정하지 않는다.',
 '띠의 길이와 폭 차이;같은 머리땅에서 끝나는 구획;경작·풀 구획의 별도 경계','location composition')
V('A03','토지대장;지적조사;측량·경계 확인;검지','S07 S31','generic manual survey; region-specific tools pending',
 'surveyor;surveyor.hand;line;stake_one;stake_two;scribe;record','surveyor.hand>holds>line;line>stretched_between>stake_one;line>reaches>stake_two;scribe>marks>record',
 'A surveyor holds a taut line between two boundary stakes while a separate scribe records the measured segment.',
 '측량자가 두 경계 말뚝 사이의 팽팽한 줄을 잡고, 별도 기록자는 그 측정 구간을 장부에 적는다.',
 '밭 앞에 지도만 든 인물과 구별. 측량 방식·길이 단위·법적 경계는 지역별 검증 필요.',
 '줄 양끝과 두 말뚝;줄을 잡는 손의 주인;같은 구간을 기록하는 사람과 기록면','hand_pose contact_point prop_placement',True)
V('A04','관개;수로 점검;대규모 관개공사','S14 S16','gravity-fed irrigation proposal',
 'feeder;sluice;branch;field;worker;worker.hand','feeder>feeds>sluice;sluice>opens_into>branch;branch>reaches>field;worker.hand>touches>sluice',
 'An open sluice joins a higher feeder to a branch channel reaching the field edge; a worker grips that sluice beside the junction.',
 '열린 수문이 높은 유입 수로와 밭 가장자리까지 이어진 지류 수로를 잇고, 작업자가 접합부 곁에서 그 수문을 잡는다.',
 '배수와 물 공급 방향 구별. 한 장의 물결만으로 유속·유량·공사 성공은 판정 불가.',
 '유입부·수문·지류·밭의 연결;지형의 높이 차;수문을 잡는 손과 같은 부품','object_structure contact_point location',True)
V('A05','배수;치수;배수로·오물 처리 시설','S13 S16','drainage outlet proposal',
 'wet_plot;ditch;outlet;lower_channel;embankment','ditch>leads_from>wet_plot;ditch>ends_at>outlet;outlet>above>lower_channel;embankment>borders>ditch',
 'A ditch cuts from a waterlogged plot to an outlet above a lower channel, with the bank and outlet mouth visible together.',
 '침수된 밭에서 판 도랑이 낮은 수로 위 배출구까지 이어지고, 둑과 배출구 입구가 함께 보인다.',
 '상수도·관개 수로와 구별. 표면이 말랐다고 토지 개량의 지속 성공을 주장하지 않는다.',
 '밭부터 배출구까지 도랑;배출구와 낮은 수로의 위치;둑이 막는 면과 통과하는 입구','location object_structure',True)
V('A06','역축;경작;농업','S07 S13','ox-drawn plough scene; harness reconstruction pending',
 'oxen;yoke;drawbar;plough;furrow;ploughman;ploughman.hands','yoke>rests_on>oxen;drawbar>joins>yoke;drawbar>joins>plough;plough>enters>furrow;ploughman.hands>hold>plough',
 'The ox team is joined by a yoke and drawbar to a plough entering the furrow; the ploughman holds its handles behind it.',
 '소 무리가 멍에·끌대로 쟁기와 이어지고 쟁기날은 고랑에 닿아 있으며, 뒤의 경작자가 손잡이를 잡는다.',
 '동물·쟁기가 나란히 놓인 장식과 구별. 다른 시대 멍에 구조를 무조건 혼합하지 않는다.',
 '역축부터 쟁기까지 하중 경로;날과 흙의 접촉;작업자의 양손과 몸 지지','body_pose contact_point object_structure',True)
V('A07','종자곡;곡창·식량 비축;곡물 검수','S07 S06','separate grain reserve proposal',
 'bin_one;bin_two;lid;grain;record;clerk','bin_one>contains>grain;lid>covers>bin_two;clerk>compares>record',
 'An open grain bin stands beside a separately closed bin; a clerk checks a record beside both containers.',
 '열린 곡물함 옆에 별도로 닫힌 곡물함이 놓이고, 기록 담당자는 두 함 곁에서 장부를 확인한다.',
 '닫힌 함=종자곡·충분한 비축이라는 판정 금지. 종자/식용 구분은 요청 문맥·읽을 수 있는 기록 필요.',
 '서로 다른 두 용기;열린 함의 실제 곡물;닫힌 뚜껑과 별도 재고 기록','prop_placement narrative_clue')
V('A08','공유지;방목권;채초지·건초','S05 S07','communal-use context; rights remain nonvisual',
 'pasture;gate;animals;haystack;hay_cart','animals>inside>pasture;gate>bounds>pasture;hay_cart>beside>haystack',
 'Animals stand inside a pasture behind its gate, while a hay cart waits beside a separate stacked hay reserve.',
 '가축은 문으로 경계 지은 초지 안에 있고, 건초 수레는 별도로 쌓은 건초 더미 곁에 있다.',
 '열린 초지=누구나 이용 가능한 무주지 아님. 방목권·사료 충족은 외형만으로 판정하지 않는다.',
 '가축·문·초지의 경계;건초와 수레의 분리;지나갈 수 있는 출입구','location prop_placement')

V('B01','현물납부;지대;조세·세금;가렴주구','S05 S06','grain delivery; fiscal classification declared separately',
 'payer;payer.hands;sack;measure;receiver;receiver.record','payer.hands>tilt>sack;sack>above>measure;receiver>marks>receiver.record',
 'A person tips grain from a sack into a measuring vessel while a receiver records that delivery on a separate page.',
 '한 사람이 자루의 곡물을 계량 용기에 붓고 수취 담당자는 별도 페이지에 그 인도를 적는다.',
 '시장 구매·지대·세금·구휼·수탈의 외형이 겹친다. 납부 근거·자발성·과도함은 별도 문맥.',
 '자루 입구와 계량 용기;곡물의 이어진 낙하;받는 사람과 적는 면의 분리','contact_point hand_pose narrative_clue')
V('B02','금납;재무관;도량형 통일','S06 S12','coin weighing; precise medieval balance pending',
 'clerk;balance;balance.pan_one;balance.pan_two;coins;weights;ledger','coins>on>balance.pan_one;weights>on>balance.pan_two;clerk>checks>ledger',
 'Coins rest in one pan of a balance and separate weights in the other; a clerk checks a ledger beside the balance.',
 '저울 한 접시에는 동전, 다른 접시에는 별도 추를 놓고 담당자가 곁의 장부를 확인한다.',
 '금속 색=화폐 품위·순도 아님. 일치 무게도 진품·합법 세입 증명 아님.',
 '동전 접시와 추 접시 구별;지지대에 이어진 두 접시;같은 거래 기록과의 물리적 배치','prop_placement object_structure',True)
V('B03','감사·회계검사;채무;체납 장부','S07 S12','tally principle; no 1694 specimen relabeling',
 'tally;tally.stock;tally.foil;tally.notches;hands','tally.stock>alongside>tally.foil;tally.notches>align_across>tally.stock;tally.notches>align_across>tally.foil;hands>hold>tally.foil',
 'Two split wooden tally halves are held side by side, their cut profiles and notches aligned across the matching edges.',
 '쪼갠 나무 기록 막대의 두 반쪽을 나란히 잡아 절단면과 홈이 대응하는 가장자리를 맞댄다.',
 '하나의 장식 막대·독립된 두 자와 구별. 실제 채무액·정산 완료는 문맥·기록 검증 필요.',
 '두 반쪽의 별도 몸체;대응하는 홈과 분할면;붙이는 손의 주인과 접촉','object_structure hand_pose',True)
V('B04','제분료;제분소','S04 S05','multure context; visible handover only',
 'miller;miller.hand;customer;customer.hand;grain_scoop;grain_sack;millstone','miller.hand>holds>grain_scoop;grain_scoop>above>grain_sack;customer.hand>supports>grain_sack;millstone>behind>miller',
 'Beside a millstone, a miller holds a small grain scoop above the sack supported by a customer.',
 '맷돌 곁에서 제분자가 작은 곡물 되를 들고, 그 아래 자루는 이용자가 받친다.',
 '제분료와 전체 곡물의 압수는 다르다. 제분 독점권·납부 비율은 외형으로 확정 불가.',
 '곡물 되와 자루의 규모 차;각 손의 주인;제분 작업 공간과 거래의 연결','hand_pose contact_point narrative_clue')
V('B05','통행료;시장세;게이트하우스','S05 S18','checkpoint exchange; toll authority remains contextual',
 'gate;cart;barrier;collector;collector.hand;traveler;traveler.hand;coin','barrier>across>gate;cart>before>barrier;traveler.hand>offers>coin;collector.hand>reaches_for>coin',
 'A loaded cart waits before a gate barrier while the traveler offers a coin toward the collector’s open hand.',
 '짐 실은 수레가 성문 차단대 앞에 기다리고 여행자는 징수 담당자의 열린 손 쪽으로 동전을 내민다.',
 '뇌물·구매·통행료는 같은 손동작일 수 있다. 권한·금액·허가 결과는 별도 정보.',
 '통과로를 가로막는 차단대;동전을 주고받는 서로 다른 손;수레와 통행로 연결','proxemics hand_pose location')
V('B06','장부 대조하기;감사·회계검사;세입·세출','S06 S07','estate-account comparison, no truth judgment',
 'auditor;auditor.hand;clerk;book_one;book_two;entry_one;entry_two','entry_one>on>book_one;entry_two>on>book_two;auditor.hand>points_to>entry_one;clerk>looks_at>entry_two',
 'An auditor points to an entry in one open account book while a clerk checks the corresponding line in a second open book.',
 '감사자가 열린 회계책 한 권의 항목을 가리키고 담당자는 두 번째 책의 대응 행을 확인한다.',
 '책 두 권=횡령 적발·재정 개혁 성공 아님. 대응 의미는 실제 읽을 수 있는 항목 또는 문맥 필요.',
 '서로 다른 두 책;손끝과 첫 행의 접촉;두 번째 행을 향한 상대 시선','hand_pose gaze_target prop_placement')
V('B07','특허장·권리장;인장·봉랍;인장반지;문서에 인장 찍기','S10 S11','matrix versus impression',
 'sealer;sealer.hand;matrix;wax;document;cord','sealer.hand>holds>matrix;matrix>pressed_into>wax;wax>attached_to>cord;cord>through>document',
 'A hand presses an engraved seal matrix into a wax disc attached by cord to a document; the matrix and wax remain separate objects.',
 '손이 새긴 인장 도구를 밀랍 원반에 누르고, 밀랍은 끈으로 문서에 연결되며 도구와 밀랍은 별개 물체다.',
 '도구·밀랍·압인 결과·문서의 구별. 사진만으로 문서 인증·권리 부여의 법적 성립을 보증하지 않는다.',
 '도구와 밀랍의 접촉;밀랍에서 끈을 거쳐 문서까지 연결;누르는 손의 주인','object_structure contact_point hand_pose',True)
V('B08','장원법정;지대명부;사본보유;서기관','S05 S06','different record carriers, legal contents contextual',
 'clerk;roll;bound_book;loose_copy;table','roll>on>table;bound_book>beside>roll;loose_copy>beside>bound_book;clerk>compares>loose_copy',
 'A clerk compares a loose copy with an unrolled record beside a separately bound account book on the same table.',
 '서기관이 낱장 사본과 펼친 기록 두루마리를 대조하고, 같은 탁자에는 별도로 제본한 회계책이 놓인다.',
 '두루마리=법정, 책=회계라는 고정 규칙 없음. copyhold는 사본의 외형이 아니라 보유권 문맥.',
 '낱장·두루마리·책의 다른 carrier;사본과 원기록의 구별;기록자가 보는 실제 면','prop_placement narrative_clue')

V('C01','수차;공업용 수로','S14 S15','selected overshot vertical wheel',
 'leat;chute;wheel;wheel.buckets;axle;tailrace','leat>feeds>chute;chute>above>wheel.buckets;wheel>joined_to>axle;tailrace>below>wheel',
 'A raised chute delivers water to buckets at the top of a vertical wheel; its central axle enters the mill wall and the tailrace lies below.',
 '높은 급수 홈통이 수직 수차 위쪽 물받이에 물을 대고, 중심축은 방앗간 벽으로 이어지며 아래에 배수로가 놓인다.',
 '하사식·중간 급수·양수 수차와 구별. 회전 방향·동력 전달 성공은 정지 화상만으로 증명 불가.',
 '홈통과 위쪽 물받이의 위치;수차 중심과 같은 축;하단의 별도 배수로','object_structure location',True)
V('C02','제분소;곡물 생산','S14 S15','grain milling working parts; exact gears pending',
 'hopper;grain;millstones;meal_spout;meal_sack','hopper>above>millstones;grain>inside>hopper;meal_spout>leads_from>millstones;meal_sack>under>meal_spout',
 'A grain hopper stands above the millstone casing, with a meal spout leading to a flour sack below.',
 '곡물 호퍼가 맷돌 덮개 위에 놓이고, 그 아래 배출구가 밀가루 자루까지 이어진다.',
 '물레바퀴가 보인다고 제분소인 것은 아니다. 원료 투입·가공부·제품 수취를 구별한다.',
 '호퍼와 가공부의 상하 관계;가공부부터 배출구 연결;배출구와 받는 자루','object_structure prop_placement',True)
V('C03','축융','S15 S37','fulling stocks proposal; mechanism detail pending',
 'frame;mallets;trough;cloth','mallets>suspended_from>frame;mallets>above>cloth;cloth>inside>trough',
 'Wooden fulling mallets hang from a frame above wet cloth gathered in a trough, with each striking face aimed at the cloth.',
 '목제 축융 망치가 틀에 매달려 물통 속 젖은 천 위에 놓이고 각 타격면이 그 천을 향한다.',
 '방적·직조·염색·제분과 구별. 실제 치댐·축융 완료·구동축은 따로 확인.',
 '망치의 지지 틀;통 속 같은 천;천을 향하는 망치 타격면','object_structure',True)
V('C04','대장간;제련소;대장장이 작업','S15 S23','forging a worked bar, not ore smelting',
 'smith;smith.hand_one;smith.hand_two;tongs;bar;anvil;hammer','smith.hand_one>holds>tongs;tongs>grip>bar;bar>rests_on>anvil;smith.hand_two>holds>hammer;hammer>above>bar',
 'A smith grips a heated bar with tongs on an anvil while the other hand holds a hammer poised above that same bar.',
 '대장장이가 집게로 뜨거운 막대를 잡아 모루 위에 놓고, 반대 손은 같은 막대 위에 망치를 든다.',
 '광석을 녹여 금속을 얻는 제련과 이미 얻은 금속의 단조 구별. 불꽃=고온·강철 품질 아님.',
 '집게 손과 망치 손 소유;집게가 물고 있는 같은 막대;막대와 모루 접촉','body_pose hand_pose contact_point',True)
V('C05','방적','S17 S20','spindle proposal; equipment dating pending',
 'spinner;spinner.fingers;fiber;thread;spindle','spinner.fingers>draw_from>fiber;thread>joins>fiber;thread>reaches>spindle',
 'A spinner draws a thin strand from a loose fiber bundle, with the strand continuing down to a suspended spindle.',
 '방적자가 느슨한 섬유 뭉치에서 가는 실가닥을 뽑고, 그 가닥은 아래 매달린 방추까지 이어진다.',
 '직조와 구별. 흐릿한 실의 연결이 보이지 않으면 공정 관계 미관측.',
 '섬유 뭉치와 가는 실의 경계;손가락부터 방추까지 연결;방추의 매달린 상태','hand_pose object_structure',True)
V('C06','직조','S17 S20','loom proposal; region-specific loom pending',
 'loom;warp;weft;shuttle;weaver;weaver.hand','warp>tensioned_in>loom;weft>crosses>warp;weaver.hand>holds>shuttle;shuttle>between>warp',
 'A weaver holds a shuttle through separated warp threads on a loom, where a transverse weft meets the already woven cloth.',
 '직조자가 직기의 벌어진 날실 사이로 북을 잡고, 가로 씨실이 이미 짠 천 부분과 만나는 곳이 보인다.',
 '방적·천 재단·자수와 구별. 실마다 방향·같은 직기 소속을 확인한다.',
 '긴 날실과 가로 씨실;북이 통과하는 벌어진 날실;짜인 천과 느슨한 실의 경계','hand_pose object_structure',True)
V('C07','길드;도제;직인;마스터·공방주','S17','sample review; legal rank not inferred',
 'craftsperson;learner;sample;benchmark;bench','sample>on>bench;benchmark>beside>sample;craftsperson>points_to>sample;learner>looks_at>benchmark',
 'A craftsperson points to a worked sample beside a separate benchmark piece while another worker compares the two at the bench.',
 '작업대에서 한 장인이 작업 견본을 가리키고 다른 작업자는 그 옆 별도 기준품과 두 물건을 비교한다.',
 '외모·나이로 도제/직인/마스터 지위를 확정하지 않는다. 길드 가입·자격 취득은 별도 문맥.',
 '실제 다른 견본·기준품;가리키는 대상;상대의 비교 시선','gaze_target hand_pose narrative_clue')
V('C08','부두·하역장·창고지구;병목;상단·대상;병참','S01 S06','logistics staging, no measured productivity',
 'boat;plank;dock;porter;porter.hands;barrel;cart;warehouse','plank>connects>boat;plank>reaches>dock;porter.hands>support>barrel;cart>between>dock;warehouse>behind>cart',
 'A porter supports a barrel on the plank linking boat and dock; a cart waits between the landing and warehouse doors.',
 '운반자가 배와 부두를 잇는 널판에서 통을 받쳐 들고, 수레가 하역장과 창고 문 사이에 기다린다.',
 '일렬 수레=실제 병목·무역 흑자 아님. 하중·발 지지·통과 폭을 함께 검토.',
 '배부터 부두까지 널판;손·통·발의 지지;하역장·수레·창고 출입 동선','body_pose contact_point composition',True)

V('D01','그레이트 홀;데이스;접견 자세','S18 S20','selected hall hierarchy; not a courtroom identity',
 'hall;dais;chair;seated_person;petitioners;floor','dais>above>floor;chair>on>dais;seated_person>in>chair;petitioners>on>floor',
 'A seated person faces petitioners from a chair on a low dais within the hall, with both floor levels visible.',
 '홀의 낮은 단상 위 의자에 앉은 사람이 청원자들을 마주하며 두 바닥 높이가 함께 보인다.',
 '의자=왕좌·단상=정통성·복종 아님. 통치 관계는 요청된 문맥이며 높이는 시각 관계.',
 '두 바닥 높이;의자·앉은 몸의 접촉;청원자와의 시선·거리','body_pose proxemics location')
V('D02','포트컬리스;게이트하우스;성문','S18','part-lowered portcullis, static state',
 'gatehouse;opening;grid;groove_left;groove_right','opening>inside>gatehouse;grid>inside>opening;grid>aligned_with>groove_left;grid>aligned_with>groove_right',
 'A partly lowered gridded gate sits in the gatehouse opening, its two edges aligned with upright guide grooves.',
 '반쯤 내려온 격자문이 성문 건물의 통로 안에 있고 양쪽 가장자리가 수직 안내 홈과 맞물린다.',
 '경첩문·도개교·문장 속 격자 도상과 구별. 정지 상태와 실제 하강 운동 구별.',
 '통로 안 격자문;양쪽 홈과 가장자리;문 아래 남은 통과 공간','object_structure location')
V('D03','도개교;해자;바비칸','S18','hinged bridge over ditch',
 'gate;bridge;hinge;ditch;chain_left;chain_right','bridge>attached_at>hinge;hinge>below>gate;bridge>over>ditch;chain_left>attached_to>bridge;chain_right>attached_to>bridge',
 'A partly raised bridge is hinged at the gate threshold over a ditch, with a lifting chain attached to each outer corner.',
 '성문 문턱에 축으로 연결된 다리가 해자 위에서 일부 들려 있고 바깥 두 모서리에 들어 올리는 사슬이 붙는다.',
 '포트컬리스와 구별. 해자에 반드시 물을 채우지 않으며 임의 시대의 권양 장치 혼합 금지.',
 '문턱·회전축·상판 연결;두 사슬의 실제 부착점;상판 아래 도랑의 분리','object_structure',True)
V('D04','우물·저수조;공업용 수로;배수로·오물 처리 시설','S16','Rievaulx-inspired separation, not reconstructed site plan',
 'spring_pipe;cistern;industrial_channel;drain;workshop','spring_pipe>reaches>cistern;industrial_channel>beside>workshop;drain>separate_from>spring_pipe',
 'A covered spring-fed conduit reaches a cistern while a separate open channel passes the workshop, apart from the waste drain.',
 '덮인 샘물 도관이 저수조로 이어지고 별도 열린 수로가 작업장 곁을 지나며 오물 배수로와 구분된다.',
 '수도원 사례를 모든 영지 표준으로 취급하지 않는다. 깨끗해 보이는 물=음용 안전성 아님.',
 '도관부터 저수조 연결;작업장 수로의 별도 경로;식수·오물 경로의 분리','location object_structure',True)
V('D05','충차·파성추;공성전','S19','suspended ram proposal',
 'frame;beam;beam.head;slings;gate;operators','slings>suspend>beam;slings>attached_to>frame;beam.head>faces>gate;operators>beside>beam',
 'A heavy ram beam hangs in slings from a covered frame, its head facing the gate while the operators stand beside its length.',
 '무거운 충차 목재가 덮개 틀의 줄에 매달리고 머리는 성문을 향하며 조작자들은 목재 길이 옆에 선다.',
 '대포·손에 든 통나무·이미 부서진 문만으로 대체 불가. 타격 성공은 별도 시간 증거.',
 '틀과 목재를 잇는 매달림;충차 머리와 같은 문;조작자가 움직일 실제 공간','object_structure composition',True)
V('D06','트레뷰셋;평형추식','S19','counterweight trebuchet at rest',
 'frame;pivot;arm;short_end;long_end;counterweight;sling','arm>supported_at>pivot;pivot>on>frame;short_end>part_of>arm;long_end>part_of>arm;counterweight>hangs_from>short_end;sling>attached_to>long_end',
 'A pivoted beam rests between two supports, with a hanging counterweight on its short end and a separate sling on the long end.',
 '회전축의 지렛대가 두 지지대 사이에 놓이고 짧은 팔에는 평형추, 긴 팔에는 별도 투석 주머니가 연결된다.',
 '인력식 당김줄·토션식 발사기와 구별. 축·짧은 팔·긴 팔을 다른 기구에서 빌리지 않는다.',
 '한 지렛대의 회전축과 두 팔;짧은 쪽 평형추 부착;긴 쪽 투석 줄과 주머니','object_structure',True)
V('D07','트레뷰셋;인력식','S19','traction machine at rest; no counterweight branch',
 'frame;pivot;beam;short_end;long_end;pull_ropes;sling;crew','beam>supported_at>pivot;pivot>on>frame;short_end>part_of>beam;long_end>part_of>beam;pull_ropes>attached_to>short_end;sling>attached_to>long_end;crew>holds>pull_ropes',
 'A crew holds several ropes descending from the short end of a pivoted throwing beam; a sling is attached to the long end.',
 '여러 조작자가 지렛대 짧은 팔에서 내려온 당김줄을 잡고 긴 팔에는 투석 주머니가 연결된다.',
 '평형추식과 별도 realization. 줄이 누구 손과 어느 팔에 이어지는지 모두 확인.',
 '같은 축·지렛대의 짧은 팔;각 당김줄과 잡은 사람;긴 팔의 별도 투석 주머니','object_structure hand_pose',True)
V('D08','봉쇄·농성;병참;포위된 성의 마지막 회의','S19 S06','supply under siege; scarcity magnitude contextual',
 'wall;gate;barricade;store;bins;defenders;ledger','barricade>across>gate;bins>inside>store;defenders>beside>ledger;store>inside>wall',
 'Behind a barred gate inside the walls, defenders inspect several partly empty bins beside an open supply record.',
 '성벽 안의 막힌 성문 뒤에서 수비자들이 열린 보급 기록 옆 일부 비어 있는 저장함을 점검한다.',
 '빈 용기=기근·패전 임박 아님. 포위·수량 부족·남은 날짜는 외부 맥락과 따로 판정.',
 '안쪽 성벽·성문 차단;함 안쪽의 보이는 내용;보급 기록과 실제 점검의 연결','location narrative_clue')

V('E01','봉신예;봉신의 충성 의례','S08','c.1275 English ceremony inspired, static gesture',
 'vassal;vassal.hand_left;vassal.hand_right;lord;lord.hand_left;lord.hand_right','vassal.hand_left>touches>vassal.hand_right;lord.hand_left>outside>vassal.hand_left;lord.hand_right>outside>vassal.hand_right',
 'One person holds both hands together between the enclosing hands of the other person, with the four hands and the wrists of both people visible.',
 '한 사람이 모은 두 손을 상대의 두 손 사이에 두고 네 손과 양쪽 인물의 손목 연결이 보인다.',
 '악수·입맞춤·검으로 어깨 대기·책에 손 얹기와 구별. 법적 봉신 관계·진심은 사진 밖 정보.',
 '안쪽 두 손의 한 주인;감싸는 바깥 두 손의 다른 주인;네 손의 포개짐과 손목 연결','hand_pose contact_point proxemics')
V('E02','충성선서;Swearing Fealty','S08','c.1275 English text-inspired right-hand contact',
 'oath_taker;oath_taker.right_hand;book;table;witness','oath_taker.right_hand>on>book;book>on>table;witness>faces>oath_taker',
 'The oath-taker rests the right hand on an open book on the table while a separate witness faces the gesture.',
 '선서자가 탁자 위 펼친 책에 오른손을 얹고 별도 입회자는 그 동작을 마주한다.',
 '책은 보이지만 성서 내용·맹세 음성·진실성은 외형만으로 확인 못 한다. 봉신예와 분리.',
 '오른손과 같은 인물 팔;손바닥과 책 접촉;별도 입회자와 시선','hand_pose contact_point')
V('E03','청원·진정;청원서 받기;폭정에 대한 공개 청원','S04 S06','petition handover; grievance truth not inferred',
 'petitioner;petitioner.hand;receiver;receiver.hand;sheet','petitioner.hand>offers>sheet;receiver.hand>reaches_for>sheet;receiver>faces>petitioner',
 'A petitioner extends a document toward the receiver’s reaching hand, with the sheet bridging the space between them.',
 '청원자가 문서를 내밀고 받는 사람은 손을 뻗으며 종이가 두 사람 사이 공간을 잇는다.',
 '계약·보고·납부 영수증과 형태가 겹친다. 청원 사유·통치자 폭정·수락은 문맥.',
 '내미는 손의 주인;받는 손의 다른 주인;같은 문서의 양끝과 전달 공간','hand_pose contact_point proxemics')
V('E04','집정관;장원 총관리;리브;장원관리인;영지 내려다보기','S07','estate inspection rather than generic personal service',
 'manager;manager.hand;field;plan;scribe','manager.hand>points_to>field;plan>beside>manager;scribe>looks_at>plan',
 'At the field edge, a manager points across the measured plots while a separate clerk studies the plan held beside the same view.',
 '밭 가장자리에서 관리자가 측량된 구획을 가리키고 별도 서기관은 같은 풍경 곁에 든 도면을 살핀다.',
 '검은 연미복 집사 고정 금지. steward·bailiff·reeve의 지위와 임무는 해당 지역 문맥.',
 '손이 향하는 실제 구획;도면과 현장 공간;별도 기록 담당자의 소유와 시선','gaze_target hand_pose location')
V('E05','곡물 검수','S07','grain inspection only; soil is separate future variant',
 'inspector;inspector.palm;grain;sample_sack;clerk;record','grain>on>inspector.palm;sample_sack>below>inspector.palm;clerk>marks>record',
 'An inspector holds a small grain sample in an open palm above its source sack while a clerk records the inspection.',
 '검수자가 원래 자루 위 펼친 손바닥에 소량의 곡물을 올려 살피고 담당자는 검수 기록을 적는다.',
 '단순 손바닥 제스처와 구별. 수분·발아율·식용 안전·토질은 눈으로 확정 불가; 흙 검사는 같은 후보로 대체 불가.',
 '손바닥 위 실제 곡립;견본과 원 자루의 관계;검수 기록의 별도 carrier','hand_pose prop_placement')
V('E06','지도 위로 몸 기울이기;도면 가리키기','S06 S07','map review with supported posture',
 'planner;planner.hand;map;table;builder;marker','planner.hand>points_to>marker;marker>on>map;map>on>table;builder>looks_at>marker',
 'A planner leans over a map supported by the table and points to one marked junction while the builder looks at that same mark.',
 '계획자가 탁자에 받친 지도 위로 몸을 기울여 표시한 접합점을 가리키고 시공자는 같은 표시를 본다.',
 '아무 지도=측량 정밀도·계획 실현 아님. 인물 몸과 탁자의 지지·손가락 실제 지점 확인.',
 '지도·탁자 지지;손끝과 특정 표시;둘이 공유하는 같은 지점','body_pose gaze_target hand_pose')
V('E07','구휼·배급;빵·식량 나눠주기;흉작·기근','S07 S19','ration transfer; cause and adequacy contextual',
 'server;server.hand;recipient;recipient.hands;bread;basket;queue','server.hand>offers>bread;recipient.hands>under>bread;basket>beside>server;queue>behind>recipient',
 'A server passes bread toward a recipient’s cupped hands from a basket beside the distribution table, with a queue behind.',
 '배급자가 탁자 곁 바구니에서 빵을 건네고 수령자는 두 손으로 받으며 그 뒤에 대기 줄이 이어진다.',
 '가난·난민·기근·선정은 외모·대기 줄만으로 확정하지 않는다. 양과 대상 자격 별도.',
 '같은 빵의 전달;받는 두 손의 주인;공급 바구니·탁자·대기 줄의 공간','contact_point hand_pose proxemics')
V('E08','부상자 곁에 무릎 꿇기;전쟁 난민·부상병·폐허','S19 S29','non-graphic care proposal; injury cause contextual',
 'helper;helper.hands;injured_person;injured_person.forearm;bandage;bench','helper.hands>hold>bandage;bandage>around>injured_person.forearm;injured_person>supported_by>bench',
 'A helper kneels beside a seated person and winds a bandage around the supported forearm, keeping the hand and limb owners distinct.',
 '돕는 사람이 앉은 인물 곁에 무릎을 꿇고 받쳐 놓은 팔뚝에 붕대를 감으며 손과 팔다리의 주인은 구별된다.',
 '무릎 꿇음=복종 아님. 부상 원인·전쟁 피해자 신분·치료 성공·사망 여부는 별도.',
 '붕대와 같은 팔뚝;돕는 손의 다른 주인;다친 팔과 몸의 지지','body_pose contact_point',True)

V('F01','우플랑드·오플랑드','S20','French court inspiration c.1400–1409; robe only',
 'wearer;robe;robe.sleeves;belt;robe.folds','robe>worn_by>wearer;robe.sleeves>part_of>robe;belt>gathers>robe.folds',
 'A full outer robe falls in deep folds beneath a belt, with sleeves widening away from the upper arms into long funnels.',
 '풍성한 겉옷이 허리띠 아래 깊은 주름으로 내려오고 소매는 위팔에서 긴 깔때기 모양으로 넓어진다.',
 '샤프롱·대깅은 이 robe 후보에 자동 추가하지 않는다. 풍성한 소매=모든 시대 귀족 기본복 아님.',
 '몸통과 이어진 같은 겉옷;허리띠에 모이는 주름;위팔부터 넓어지는 소매','garment_detail attire_context')
V('F02','키르틀;가운;슈미즈·시프트;보디스','S20','layer relationship proposal; named cut requires more evidence',
 'wearer;underlayer;dress;dress.bodice;dress.skirt;neck_edge','underlayer>under>dress;dress.bodice>joined_to>dress.skirt;neck_edge>bounds>underlayer',
 'A fitted dress has a bodice joined to its skirt, with a separate light underlayer visible at the neckline inside the outer edge.',
 '몸에 맞는 드레스의 몸통은 치마와 이어지고, 네크라인 안쪽에는 밝은 별도 속옷층의 가장자리가 드러난다.',
 '보디스=별도 코르셋 아님. 속옷층 색만으로 리넨 재질·키르틀의 세부 시대형 확정 불가.',
 '몸통과 치마의 연결;독립된 속옷 가장자리;옷층과 몸 피부의 별도 경계','garment_detail',True)
V('F03','더블릿;호즈','S20','early fifteenth-century connected garments',
 'wearer;doublet;hose;points;waist','doublet>worn_by>wearer;hose>worn_by>wearer;points>join>doublet;points>join>hose;points>at>waist',
 'A short fitted doublet meets cloth hose at the waist, with visible lacing points joining the two separate garments.',
 '짧고 몸에 맞는 더블릿이 허리에서 천 호즈와 만나고, 두 별도 의복을 잇는 고정 끈이 보인다.',
 '현대 레깅스·얇은 스타킹으로 자동 치환하지 않는다. 브레이즈는 이 바깥 층만으로 보였다고 하지 않는다.',
 '더블릿 아래단·호즈 위쪽 경계;두 옷을 잇는 실제 끈;신체와 옷층 구별','garment_detail object_structure',True)
V('F04','타바드;슈르코·서코트;리버리','S20 S25','open-sided tabard proposal; separate historical cut review',
 'wearer;tabard;tabard.front;tabard.back;side_gap;undercoat','tabard>worn_by>wearer;tabard.front>separate_at>side_gap;tabard.back>separate_at>side_gap;undercoat>visible_through>side_gap',
 'A sleeveless overgarment has separate front and back panels joined at the shoulders, with the undercoat visible through the open sides.',
 '소매 없는 겉옷은 어깨에서 앞뒤 패널이 이어지고 열린 옆면 사이로 속의 옷이 보인다.',
 '문장 있는 모든 겉옷=타바드 아님. 서코트와 세부 절개·시대별 용례는 별도 확인.',
 '어깨 연결;열린 양 옆과 패널;안쪽 옷이 독립된 층','garment_detail',True)
V('F05','패튼;신발','S26','15c London patten-inspired support relation',
 'wearer;shoe;patten;strap;ground','shoe>rests_on>patten;strap>over>shoe;patten>raises_above>ground',
 'A leather shoe rests on a raised wooden patten held by an over-foot strap, leaving the shoe sole above the wet ground.',
 '가죽 신발이 발등 끈으로 고정된 목제 패튼 위에 놓이고 신발 밑창은 젖은 지면보다 높이 떠 있다.',
 '풀렌의 긴 앞코·현대 하이힐과 구별. 일부는 호즈 위에 신었으므로 모든 패튼이 신발 위라는 정의 아님.',
 '신발·목재 받침 별도 물체;같은 발등 고정 끈;밑창과 지면 사이 간격','wearable_accessory contact_point')
V('F06','스테이즈;코르셋;보디스','S22','18c support garment displayed; no hidden-structure inference',
 'stays;stays.channels;stays.eyelets;lace;table','stays.channels>on>stays;stays.eyelets>on>stays;lace>through>stays.eyelets;stays>on>table',
 'A separate structured pair of stays lies open on a table, showing stitched channels and a lace passing through the edge eyelets.',
 '별도 구조 의복인 스테이즈를 탁자에 펼쳐 누빔 통로와 가장자리 고리를 통과하는 끈을 보인다.',
 '옷의 몸통 부분=독립 지지 의복 아님. 숨은 보강재·착용자의 허리 변형·고통은 추정하지 않는다.',
 '독립 의복의 가장자리;누빔 통로;끈과 실제 고리의 관통','object_structure garment_detail',True)
V('F07','파니에;페티코트','S21 S22','18c lateral support fitting, no era mixture by default',
 'wearer;waistband;side_support;outer_skirt','waistband>around>wearer;side_support>attached_to>waistband;outer_skirt>over>side_support',
 'At a fitting, the skirt is lifted enough to show a waist-attached side support spreading farther left and right than front to back.',
 '피팅 중 치마를 일부 들어 허리에 연결된 옆 받침이 앞뒤보다 좌우로 더 넓게 퍼진 모습을 보인다.',
 '원형 크리놀린·뒤쪽 버슬과 구별. 옷 받침의 폭을 신체 골격 변화로 기록하지 않는다.',
 '허리띠와 받침 연결;겉치마 아래 같은 받침;앞뒤 깊이보다 큰 좌우 폭','garment_detail object_structure',True)
V('F08','레이싱;시종이 옷의 여밈을 돕기;탈의·착의 중인 상태','S20 S22','adult dressing interaction; specific period cut declared',
 'wearer;garment;garment.eyelets;lace;attendant;attendant.hands','garment>worn_by>wearer;lace>through>garment.eyelets;attendant.hands>grip>lace',
 'An adult wearer stands while a separate adult attendant grips the laces threaded through eyelets on that wearer’s garment.',
 '성인 착용자가 서 있고 별도의 성인 시종은 착용자 의복의 고리를 통과한 끈을 두 손으로 잡는다.',
 '성적 관계·고용 지위·동의·강요는 이 손동작으로 확정 불가. 끈·여밈 위치와 양 인물 소유를 보존.',
 '입은 옷의 한 주인;끈을 잡은 손의 다른 주인;실제 고리를 통과한 같은 끈','hand_pose contact_point garment_detail',True)

V('G01','메일;호버크','S23','linked-ring armor; textile coif separate',
 'wearer;mail_shirt;mail_rings;sleeve','mail_shirt>worn_by>wearer;mail_rings>interlink_on>mail_shirt;sleeve>part_of>mail_shirt',
 'An armor shirt wraps the torso and sleeve in linked metal rings, with individual interlocking openings visible at the cuff.',
 '갑옷 셔츠가 몸통과 소매를 연결된 금속 고리로 덮고 소맷단에서 고리들이 맞물린 구멍이 보인다.',
 '반짝이는 니트·비늘·리벳 천과 구별. 천 코이프·메일 코이프와 숨은 안감을 하나로 합치지 않는다.',
 '고리의 개구부;고리끼리의 맞물림;몸통부터 소매까지 같은 갑옷','garment_detail surface_material',True)
V('G02','브리건딘;코트 오브 플레이트','S24','turned-edge brigandine proposal',
 'garment;outer_cloth;rivets;inner_plates;turned_edge','outer_cloth>outside>inner_plates;rivets>through>outer_cloth;rivets>fasten>inner_plates;turned_edge>reveals>inner_plates',
 'A turned-back garment edge reveals overlapping internal plates behind a cloth exterior whose rivet heads align with the plate attachments.',
 '옷 가장자리를 뒤집어 겉천 뒤의 겹친 내부 판을 드러내고, 겉 리벳 머리는 그 판의 고정부와 대응한다.',
 '스터드 장식=방어판 증거 아님. 외부만 보이면 내부 판 gate는 미관측; 역사 세부 형식 검토 필요.',
 '겉천과 안쪽 판의 별도 층;겹친 판의 가장자리;같은 고정점의 겉 리벳과 안쪽 판','object_structure garment_detail',True)
V('G03','판금갑옷;건틀릿','S23 S24','articulated gauntlet state, no movement proof',
 'wearer;wearer.hand;gauntlet;gauntlet.finger_plates;gauntlet.cuff;forearm','gauntlet>worn_on>wearer.hand;gauntlet.finger_plates>overlap_on>gauntlet;gauntlet.cuff>over>forearm',
 'An armored hand rests partly open, with overlapping finger plates leading back to a separate cuff over the forearm.',
 '갑주 손이 일부 펼쳐져 있고 겹친 손가락 판이 팔뚝 위 별도 소맷단으로 이어진다.',
 '금속 장갑의 장식=모든 관절 가동 입증 아님. 벗는 중과 착용 완료는 별도 상태 후보로 나눌 것.',
 '같은 손의 손가락 판;판끼리 겹침;손부터 cuff·팔뚝 연결','garment_detail hand_pose',True)
V('G04','문장;가문 배지·리버리 배지','S25','14c harness pendant-inspired attachment',
 'horse;bridle;pendant;pendant.loop','bridle>on>horse;pendant.loop>through>bridle;pendant>hangs_from>pendant.loop',
 'A small shield-shaped pendant hangs by its top loop from a horse’s bridle strap, distinct from the horse and cloth covering.',
 '작은 방패형 펜던트가 위쪽 고리로 말 굴레 띠에 매달리고 말 몸·덮개 천과 구별된다.',
 '마구 펜던트·캐퍼리슨·금속 마갑은 서로 다름. 방패 모양·색만으로 문장 소유자·혈통 판정 금지.',
 '굴레와 말의 관계;고리의 부착점;분리된 매달린 펜던트','wearable_accessory object_structure')
V('G05','문장;크레스트;가문 배지·리버리 배지','S25','heraldic carrier comparison; full blazon review pending',
 'shield;shield.device;helmet;crest;badge;coat','shield.device>on>shield;crest>above>helmet;badge>attached_to>coat',
 'A shield bears a painted device, a separate helmet carries a crest above it, and a small badge is attached to a coat nearby.',
 '방패에는 그린 도상이 있고 별도 투구 위에는 크레스트, 근처 옷에는 작은 배지가 부착되어 있다.',
 '크레스트=문장 전체 아님. 실제 제도·소유 가문·수행원 권리는 도상만으로 확정 못 함.',
 '방패의 표면 도상;투구 위의 별도 입체 장식;옷에 붙은 독립 배지','object_structure prop_placement',True)
V('G06','리넨·아마포;모직물;벨벳;브로케이드;다마스크;수선 자국;잉크 얼룩','S20 S26','surface and wear evidence, no class diagnosis',
 'sleeve;patch;stitches;ink_mark;swatch;pile','patch>over>sleeve;stitches>join>patch;stitches>join>sleeve;ink_mark>on>sleeve;pile>on>swatch',
 'A stitched patch overlaps a worn sleeve beside a small ink mark; a separate fabric swatch shows a directional pile surface.',
 '닳은 소매에 바느질한 덧댐과 작은 잉크 자국이 보이고, 별도 천 견본에는 방향성 있는 털결 표면이 드러난다.',
 '수선=가난·피부색=농노·광택=실크·금색=금실 아님. 재료 동정·직무·경제 사정 별도.',
 '패치와 원 소매의 중첩;바느질의 연결;얼룩과 별도 견본의 다른 carrier','texture surface_material garment_detail',True)

V('H01','영지 상태창;민심·충성도 수치','S02','authored fantasy interface; no historical authority',
 'scene;panel;panel.labels;panel.bars;viewer','panel>overlays>scene;panel.labels>inside>panel;panel.bars>inside>panel;viewer>looks_at>panel',
 'A floating panel overlays the estate scene with separately labeled food, population and treasury bars, while its declared viewer faces it.',
 '영지 풍경 앞에 뜬 패널이 식량·인구·금고의 별도 이름과 막대를 보이며 설정된 관찰자가 패널을 향한다.',
 '표시 수치=현실 민심·재고의 진실 아님. 누가 패널을 볼 수 있는지는 설정; 신체 발광·HUD 자동 추가 금지.',
 '풍경과 패널의 표현 층;항목과 각 막대 연결;관찰자의 시선과 표시 carrier','narrative_clue prop_placement',True)
V('H02','기술 트리;건물 업그레이드;현대 지식 치트','S01 S02','authored design diagram, not actual chronology',
 'diagram;node_one;node_two;node_three;connectors','node_one>on>diagram;node_two>on>diagram;node_three>on>diagram;connectors>link>node_one;connectors>reach>node_two;connectors>reach>node_three',
 'An explicit planning diagram connects one prerequisite node to two separate later nodes using visible arrows on the same surface.',
 '계획 도식의 한 선행 노드에서 별도 두 후속 노드로 같은 면 위 화살표가 이어진다.',
 '도식은 설계된 선행 관계를 나타냄. 실제 발명·생산량 증가·기억·회귀를 증명하지 않는다.',
 '별도 세 노드;한 면 위 연결선;화살표의 출발·도착 방향','object_structure narrative_clue',True)
V('H03','골렘·소환수 노동력;마왕 영지물·던전 경영물','S01','authored nonhuman labor, no universal golem anatomy',
 'golem;golem.arms;stone;foundation;controller','golem.arms>support>stone;stone>above>foundation;controller>beside>foundation',
 'An articulated stone worker supports a building block over the foundation while a separate foreperson stands clear of the load.',
 '관절 있는 돌 작업자가 기초 위에서 건축 블록을 받치고 별도 현장 책임자는 하중 밖에 선다.',
 '돌 재질·통제 방식은 선택한 허구 구현. 노동 계약·의식·자유의지·노예 여부는 외형으로 판단 불가.',
 '같은 비인간 몸과 두 팔;받치는 블록의 접촉;기초·하중·별도 감독 위치','body_pose contact_point',True)
V('H04','마법 인프라;마정석·마나 자원','S01 S16','authored magic-water utility',
 'crystal;socket;conduit;reservoir;tap','crystal>in>socket;socket>joins>conduit;conduit>reaches>reservoir;tap>attached_to>reservoir',
 'A crystal sits in a distinct socket connected by a continuous conduit to a reservoir with a visible outlet tap.',
 '수정이 별도 소켓에 들어 있고 끊김 없는 도관이 배출 꼭지가 있는 저장조까지 이어진다.',
 '빛나는 돌 하나=전력·마력 공급 아님. 기능·물질·효율은 창작 설정; 실제 과학 고증 근거로 내보내지 않음.',
 '수정과 소켓의 경계;소켓부터 저장조의 도관;저장조에 붙은 꼭지','object_structure location',True)

V('I01','검지;검지장;석고','S31 S33','late16c Japan record context; tools/handwriting pending',
 'surveyor;rope;stakes;clerk;book;book.columns','rope>between>stakes;surveyor>holds>rope;book.columns>on>book;clerk>writes_in>book',
 'At a measured field boundary, a surveyor holds a rope between stakes while a separate clerk writes in a columned land register.',
 '측량된 밭 경계에서 측량자가 말뚝 사이 줄을 잡고 별도 기록자는 칸을 나눈 토지대장에 적는다.',
 '일본 검지 문맥과 서양 장원대장을 같은 제도로 합치지 않음. 석고는 현물 재고와 구별.',
 '말뚝과 줄의 두 끝;측량자와 기록자 구별;실제 대장의 칸과 필기면','hand_pose narrative_clue location',True)
V('I02','조카마치·성하도시;다이묘;번','S32','Nagoya-inspired regional town pattern, no universal plan',
 'castle;street;warrior_quarter;shops;workshops','street>connects>castle;shops>along>street;workshops>beside>shops;warrior_quarter>apart_from>shops',
 'A street runs from the castle toward shopfronts and workshops, with a separate residential quarter set away from the commercial frontage.',
 '성에서 상점·공방 앞으로 길이 이어지고 별도 거주 구역은 상업 가로와 떨어져 놓인다.',
 '성하=서양 남작령 아님. 모든 번의 방위·비율·성의 형태·행정권을 고정하지 않는다.',
 '성부터 상업 가로 연결;상점·공방의 기능상 구별;거주 구역의 별도 공간','location composition',True)

CONTEXT = []
def K(cid,terms,sources,distinction,not_proven,route):
    CONTEXT.append(dict(id=cid,terms=terms.split(';'),source_ids=sources.split(),
        kind='context_diagnostic',distinction_ko=distinction,not_proven_by_pixels=not_proven,
        routing_ko=route,positive_visual_candidate=False,automatic_activation=False,
        runtime_registration='none',pixel_status='NOT_APPLICABLE_CONTEXT',native_approval=False))

K('K01','영지물;내정물;국가 경영물;건국물;도시 건설물;변경 개척물;영지 재건물;가문 경영물;왕조물;산업 발전물;대체역사물;슬로 라이프물;군상극','S01 S02','영지 경영은 지역·생산·재정·주민을 연결하는 서사 범주. 왕조·도시·국가 운영과 겹치되 범위는 요청마다 다르다.','성·왕좌·갑옷이 있다고 영지 경영이 성립하거나 필수가 되지 않는다.','장르 검색 advisory; 실제 운영 관계는 A/B/C/E 카드에서 선택.')
K('K02','영주;여성 영주;공작;후작;변경백;백작;자작;남작;상급영주;봉신;가신;기사;종자;성주;집정관;장원관리인;리브;재무관;서기관;섭정','S07 S08 S34','작위·업무 직책·봉사 관계·소유권은 별도 축. 영국식 오작위 서열을 전 유럽 행정 피라미드로 확장하지 않는다.','왕관·망토·성별·갑옷·앉은 위치만으로 작위·본인 통치권·배우자 지위를 확정할 수 없다.','선언된 역할 문맥을 보존하고 업무·도구의 직접 관계만 선택.')
K('K03','영지;봉토;장원;직영지;보유지;왕령;교회령;공유지;변경;월경지;봉건제;장원제;영주권;자치도시;자유도시;자유농;농노;소작농;노예;영민;시민','S04 S05 S35','영토·수입권·법정 단위·직영 경영·보유·공동 이용권·법적 신분은 별개이며 지역 차가 크다.','같은 밭·일하는 사람·수선 옷·사슬의 유무로 법적 권리 묶음이나 신분을 판정하지 않는다.','제도 용어 병합 금지; 특정 지역 정의는 별도 사료와 문맥 레코드로 보강.')
K('K04','재판권;고등재판권;관습법;특허장;사본보유;호구조사;면세;면역;파문;성역;피난권','S04 S05 S06','문서 carrier와 문서 내용·관할권·효력은 구별. 모든 영주에게 고등재판권이 있는 것은 아니다.','문서를 내밀거나 봉인했다고 특정 권리·동의·법적 효력이 성립한 것은 아니다.','읽을 수 있는 내용 또는 명시 설정을 따로 보존; 긍정 시각 후보는 B07/B08의 물리 관계 한정.')
K('K05','조세;지대;부역;십일조;통행료;시장세;군역대납금;제분료;입주;사망공납;체납;국고;세입;세출','S05 S06','부담의 근거·수취자·대상·납부 방식은 독립. 현물/금납은 납부 매체이며 세목 자체가 아니다.','곡물·동전 인도 장면 하나로 국가세·지대·종교 부담·매매·수탈을 확정하지 않는다.','S36 접근 실패 항목은 세부 정의 보류. B01/B02/B04/B05의 외형을 세목 alias로 강제하지 않음.')
K('K06','윤작;휴경;삼포제;인클로저;개간;흉작;기근;민심;성장 선순환;스노볼;재난;유지비','S07 S13','공간 상태와 해마다의 순환·권리 재편·누적 성장·부족 원인은 별도 검증 대상.','세 색 밭=삼포제, 큰 수확=증산, 폐허=이번 전쟁, 빈 함=기근이라는 단정 금지.','비교·연속 기록이 필요하면 별도 다중 시점 작업으로 설계; 단일 이미지 pass에 합치지 않음.')
K('K07','화폐 주조권;화폐 품위 저하;환어음;신용 거래;채무;영지 저당;전매권;독점권;밀수;암시장','S06 S12','주조·순도·권한·채무·신용·불법성은 물체의 모습과 분리. tally 표본의 연대는 보존한다.','색·크기·저울·은밀한 운반으로 품위 저하·위조·불법 거래를 증명하지 않는다.','공정·운반·기록 후보만 optional; exact financial definition은 지역 사료 보완 전 보류.')
K('K08','민심;정통성;통치 정당성;파벌;귀족 연합;충성도;인질;볼모;인재 영입;이주민 유치','S02 S04','행동·지위·감정·강요 여부·정책 성과는 다른 층. 주민 군중은 단일 감정 집단이 아니다.','미소·절·박수·경비·폐쇄 공간이 지지·충성·납치·자발적 이주를 입증하지 않는다.','보이는 몸·시선·출입·교환 관계를 쓰고 동기·법적 신분은 서사 metadata로 유지.')
K('K09','정략혼;혼인 동맹;지참금;과부산;부양재산;계승 분쟁;장자상속;분할상속;적통;적자;혼외 출생;서자;사생아;인지;적출화;약혼 파기;혼인 무효','S27','런던 사례의 dowry/dower는 재산의 제공·부양 맥락이 다르며 지역별 제도가 다르다. 혼인·혈통·승계도 독립.','상자·보석·가족 초상·자리 배치·임신 외형으로 합법 상속·친자·혼인 성립을 판정하지 않는다.','원 개념 보존; 혼인 재산/후계는 문맥 또는 판독 가능한 문서로 별도 표현.')
K('K10','첩;후궁;정부;애인;하렘;후궁 집단;불륜;간통;밀회;비밀 연애','S02 S27','지속 관계·공적 지위·사적 공간·독점 관계 위반은 별개. 원 대화의 민감한 용어도 삭제하지 않는다.','친밀한 거리·노출·침실·여러 인물만으로 성적 관계·혼인·배신·동의를 확정하지 않는다.','세부 제도는 원전 보강 대기. 외형·인원·접촉을 원 용어의 자동 시각 의무로 만들지 않음.')
K('K11','NTR;코르티잔;매춘업소·브로델;성접대·성적 거래','S02 S28','현대 서브컬처 태그와 역사적 직업·거래·공간은 분리. 현재 확보 출처는 이들 세부 제도 전체를 지지하지 않는다.','복식·매혹적 표정·금전·밀회 장면으로 직업·성적 서비스·배신을 판정할 수 없다.','정확한 시대·지역·개념의 추가 학술 출처 확보 전 definition_deferred. 원 키워드만 보존.')
K('K12','강제혼인;후계 생산 압박·재생산 강요','S27','혼인의 정치적 목적과 당사자 동의는 별도. 후계 기대와 재생산 강요도 등치하지 않는다.','불행한 표정·권력자와의 거리·성인 착의 장면이 강요·임신·동의를 증명하지 않는다.','비가시 claim과 직접 보이는 통제 관계를 분리. 세부 역사 정의는 추가 사료 필요.')
K('K13','권력형 성폭력;성노예·성적 착취;강간·전시 성폭력','S19 S35','폭력·신분 제약·성적 착취의 연구 범주를 유지하되 외형·피해 주장·법적 판단은 구별한다.','노출·찢어진 옷·상처·구속만으로 성행위·동의·가해자·원인을 판정하지 않는다.','context only. 성적 폭력의 긍정 시각 후보를 만들지 않으며 외형을 성적 이용 증거로 전환하지 않음.')
K('K14','초야권','S28','확립된 보편 중세 제도가 아니라 역사적 신화와 그 이용을 검토하는 항목으로 보존.','신방·영주·신부 구도가 역사적 권리의 실재나 사건을 증명하지 않는다.','historical_myth_context. 원 소재를 지우거나 실제 보편 제도로 등록하는 두 오류를 피함.')
K('K15','가렴주구;채무 예속;채무노예;인신매매;징발;약탈;추방;재산 몰수;연좌;집단 처벌;종교 박해;희생양','S04 S19 S35','물자 인도·이동 제한·채무·신분 제약·강탈·제재는 별도 관계.','빈곤 외모·피부색·사슬·경비·이동만으로 범죄·동의·법적 신분을 판정하지 않는다.','요구→행동→제약→결과 관계를 구체화하되 죄·의도·제도를 미관측으로 남김.')
K('K16','농민 봉기;민란;도적;산적;무법자;방화;초토화;학살;민간인 살해;고문;강압 심문;형틀;공개 모욕형;채찍형;낙인형;절단형;교수형;참수형;화형;효수;흉터;핏자국','S19 S29','기구·상해 흔적·처벌·살해·피해 원인을 분리. 특정 고문 기록을 모든 중세 성으로 일반화하지 않는다.','상처=범죄·구속=유죄·정지한 몸=사망·불탄 건물=의도적 방화 아님.','원 용어 전부 보존. 개별 형벌 도구·지역 적용의 출처/도판 보강 전 새 시각 실현은 보류.')
K('K17','튜닉;코트하디;클로크;맨틀;에이프런;거들;후드;윔플;에냉;브레이즈;크리놀린;버슬;러프;데콜테;오프숄더;시어 패브릭;슬릿;가터·스타킹;실내 가운;네글리제;노출형 판타지 갑옷;대깅;슬래싱;파르티컬러','S20 S21 S22','의복 형태·착용 상태·시대·지역·소재·성적 연출은 별도 축. 여러 세기 의복을 중세 귀족 기본 세트로 합치지 않는다.','피부 노출=성적 목적·보강 의복=고통·화려함=귀족 아님. 가려진 내부 부속은 보였다고 하지 않는다.','원 키워드 보존. 세부 복식별 유물 도판/연대 확보 후 단독 시각 카드로 분할; 판타지 혼합은 명시 허구로 유지.')
K('K18','갬비슨;아밍 더블릿;퀴라스;폴드런;그리브;그레이트 헬름;바시넷;살레;캐퍼리슨;의장용 갑주;토너먼트 갑주;직위의 사슬;서클릿;열쇠 꾸러미','S23 S24 S25','방어구 부품·의복·마구·직책 표장은 carrier와 기능별로 분리.','갑옷=기사·말 덮개=금속 마갑·고리 사슬=공직·서클릿=왕족 아님.','특정 도구의 정확한 단면·연결·시기 확인 후 확장. 기존 candidate의 전체 조건/effects와 재사용 검토.')
K('K19','회귀;빙의;환생·전생 지식;내정 치트;영지 코어;던전 경제;다종족 영지;골렘·소환수 노동력','S01 S02','허구 설정의 정체·기억·시간·정보 접근·의식·노동 관계는 보이는 장치와 별도.','동일 얼굴·상태창·빛나는 수정·돌 신체가 회귀·영혼·통제·노예 신분을 증명하지 않는다.','HUD carrier·관찰자·표시된 주장·현실 상태를 분리; 설정을 요청 의미에 맞춰 optional 실현.')
K('K20','식읍;녹읍;수조권;다이묘;번;석고;검지;검지장;조카마치','S30 S31 S32 S33','한국의 경제 기반·수취권과 일본 검지·석고·성하도시는 각 제도와 연대를 유지한다.','쌀 포대 수=석고, 토지대장=소유권, 다이묘=서양 남작이라는 등치 금지.','지역 provenance를 mandatory review metadata로 유지. 직접 보이는 측량/기록/도시 관계만 후보화.')
