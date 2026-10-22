"""Nonvisual boundaries and supplementary visible proposals."""
from research_data import card

card('D17','바늘과 떨어진 손의 거리','Trypanophobia;Iatrophobia;Tomophobia',
 'A clothed adult holds one hand against their own chest while an unused capped syringe remains on a tray at arm’s length, without touching the body.',
 '옷을 입은 성인이 한 손을 자기 가슴에 대고 있으며, 쓰지 않은 뚜껑 달린 주사기가 팔 길이만큼 떨어진 트레이에 놓여 몸에 닿지 않는다.',
 'syringe>on>tray;hand>against>adult.chest;syringe>separate_from>adult','body_pose,prop_placement,proxemics','S06','바늘 접촉;공포증 진단;통증의 증명','거리·손 자세는 창작 대리형이다. 실제 공포·회피 동기·공포증은 판정하지 않는다.',mode='proxy')
card('D18','머리 표면의 전극과 별도 장치','Electroconvulsive Therapy, ECT',
 'An adult anatomical mannequin has two separate electrode pads on the scalp, with visible leads ending at a separate tabletop device.',
 '성인 해부 마네킹의 두피에 전극 패드 두 개가 따로 놓이고, 보이는 전선이 별도의 탁상 장치로 이어진다.',
 'pads>on>mannequin.scalp;leads>connect>pads_and_device','contact_point,object_structure,prop','S09','전기고문;로보토미;전극만으로 ECT 확정','외부 장치 도식이며 실제 ECT·전류·치료·동의·의식을 입증하지 않는다. 절차나 설정값은 제공하지 않는다.',mode='proxy',priority='P1')
card('L09','서로 다른 코드가 붙은 같은 외형의 시료','Chimerism;Mosaicism;Cloning / Genetic Engineering;Xenotransplantation',
 'Two visually similar sealed sample tubes stand side by side, labeled "SOURCE A" and "SOURCE B"; neither contains a visible miniature organism.',
 '외형이 비슷한 밀봉 시료 튜브 두 개가 나란히 있고 각각 "SOURCE A", "SOURCE B"로 표시되며, 어느 쪽에도 육안으로 보이는 소형 생물은 없다.',
 'label_a>on>tube_a;label_b>on>tube_b;tubes>beside>each_other','visible_text,prop_placement,object_structure','S20,S23','동일 외형을 복제 증거로 취급;라벨을 유전자 검사로 취급','보이는 것은 표기 차이뿐이다. 키메라·모자이크·이종이식·복제·유전자 조작은 입증하지 않는다.',mode='proxy',priority='P1')
card('E11','얼굴은 보이고 작업부는 가려진 시선','Accidental Awareness;Local / Regional Anesthesia;General Anesthesia',
 'An adult’s open eyes face the lower edge of an opaque surgical drape while the covered work area remains entirely hidden behind it.',
 '성인의 열린 눈이 불투명 수술포의 아래 가장자리를 향하고 있으며, 덮인 작업 구역은 수술포 뒤에 완전히 가려져 있다.',
 'eyes>oriented_toward>drape.edge;drape>occludes>work_area','gaze_target,subject_framing,prop_placement','S06,S07','눈이 열렸으므로 각성 사고 확정;통증·의식·기억 등치','눈·수술포의 관계만 제안한다. 의식 보존 국소마취·전신마취 우발적 각성·단순 연출을 사진만으로 구별하지 않는다.',mode='proxy')
card('E12','하나의 신체 일부로 제한된 프레이밍','Anatomical Fragmentation;Medical Gaze',
 'A tight photograph frames one adult forearm on a clinical support, excluding the face and the rest of the body while keeping the forearm continuous within the frame.',
 '조밀한 사진 구도가 진료 받침대 위 성인의 팔뚝 하나를 담고, 얼굴과 나머지 신체는 화면 밖에 두되 팔뚝은 화면 안에서 연속적으로 보인다.',
 'frame>includes>adult.forearm;frame>excludes>adult.face','subject_framing,body_region,composition','S01','실제 절단;신체 파편을 자동 생성','프레이밍과 신체 절단은 다른 의미다. 얼굴 부재는 비인간화·신원 상실의 증거가 아니다.')
card('E13','해부 기록과 덮인 운반대의 역사 대리형','Resurrectionists / Body Snatchers;Corpse Medicine / Medicinal Cannibalism;Medical Gothic',
 'In a clearly fictional historical study, a canvas-covered stretcher rests beside an open ledger labeled "1811"; no contents are visible beneath the cover.',
 '명백한 허구의 역사적 서재에서 천으로 덮인 운반대가 "1811"이라고 적힌 펼친 장부 옆에 있고, 덮개 아래 내용은 보이지 않는다.',
 'cover>occludes>stretcher.contents;ledger>beside>stretcher','historical_period,prop_placement,narrative_clue','S29','도굴 사건 재현을 실제 사료로 취급;덮개 아래 시신 확정','1811–12년 런던 기록에서 착안한 창작 소품 배치다. 거래·도굴·시체 약재·내용물은 입증하지 않는다.',mode='proxy',priority='P2')

# id, title, exact reference terms, channel, definition/limit sources, boundary.
CONTEXTS = [
 ('X01','장르·하위 경향','Medical Horror;Medical Gothic;Biomedical Horror;Body Horror;Surgical Horror;Clinical Horror;Hospital Horror;Institutional Horror;Medical Thriller;Dental Horror;Cosmetic Surgery Horror;Reproductive Horror;Gynaehorror;Transplantation Gothic;Corporate Medical Horror;Biopunk;Splatter / Gore;Torture Porn','advisory','S01,S02,S03,S04','장르 라벨은 검색 문맥이다. 병원·어둠·고어·나체·성적 의미·폭력 강도를 자동 의무로 만들지 않는다.'),
 ('X02','비평 개념과 관측의 경계','Medical Gaze;Bodily Autonomy;Bodily Integrity;Abjection;The Uncanny;Grotesque;Biopower;Medicalization / Pathologization;Dehumanization / Objectification;Monstrous-Feminine','context','S01,S04,S25','비평 용례와 창작 해석을 구별한다. 개인의 신체·여성·장애·질병에 본질적 괴물성·열등성을 부여하지 않는다. 개별 이론의 원전 정의는 추가 확인 대상이다.'),
 ('X03','진단 불확실성과 오류','Diagnostic Uncertainty;Differential Diagnosis;Diagnostic Error;False Negative / False Positive;Idiopathic;Iatrogenic;Adverse Event;Medical Gaslighting;Diagnostic Overshadowing','context','S45','증상·검사·실제 상태·시점·원인의 관계를 필요로 한다. 차트 불일치나 불안한 얼굴로 오진·과실·악의·가스라이팅을 확정하지 않는다.'),
 ('X04','마취·진정·진통·운동·기억의 독립 축','General Anesthesia;Local / Regional Anesthesia;Sedation;Analgesia;Neuromuscular Blockade;Accidental Awareness;Amnesia','context','S06,S07','의식·통증·움직임·회상은 다른 축이다. 국소마취 중 깨어 있음은 곧 실패가 아니며, 움직이지 않는 모습만으로 통증이나 무의식을 단정하지 않는다. 약리 세부는 후속 전문 자료로 검토한다.'),
 ('X05','혼수·폐쇄증후군·뇌사','Coma;Locked-in Syndrome;Brain Death','context','S08','세 상태를 같은 병상 외형으로 합치지 않는다. 혼수 정의는 확인했으나 폐쇄증후군·뇌사의 세부 판정 기준은 이 연구에서 승인하지 않는다. 표정·열린 눈·장치만으로 진단 금지.'),
 ('X06','공포증·지각·망상','Iatrophobia;Nosocomephobia;Trypanophobia;Tomophobia;Nosophobia;Mysophobia / Germophobia;Hallucination;Depersonalization / Derealization;Capgras Delusion;Cotard Delusion;Delirium','context','S45','특정 공포·망상·섬망의 임상 정의·진단은 별도 조사 대상이다. 장면은 주관적 지각의 허구적 대리형으로만 저술하고 외형을 실제 개인 진단으로 사용하지 않는다.'),
 ('X07','주관적 통증과 기대 효과','Phantom Limb Pain;Nocebo Effect','context','S06','부위 부재·약병·괴로운 표정만으로 통증·노시보 원인을 입증하지 않는다. 환상지통·노시보의 전문 정의는 후속 확인 대상으로 유지한다.'),
 ('X08','혈류·산소·위축의 비가시성','Ischemia;Hypoxia;Atrophy','context','S11','어두운 피부·창백함·가는 사지를 곧 허혈·저산소·위축으로 명명하지 않는다. 병태생리와 전후 변화는 후속 전문 검증 및 비교 자료가 필요하다.'),
 ('X09','오염·집락화·감염·생물막','Pathogen;Contamination;Colonization;Healthcare-Associated Infection;Surgical Site Infection;Biofilm','context','S17','표면에 물질이 묻음, 미생물 존재, 조직 감염, 발병, 의료관련성은 각각 다르다. 현미경·배양·병력을 장식 소품만으로 대체하지 않는다.'),
 ('X10','전염·기생·프리온·패혈증','Parasitism;Zoonosis;Prion Disease;Sepsis','context','S18,S19','기생은 관계, 인수공통 전염은 전파 경로, 프리온은 접힘 이상, 패혈증은 감염 반응의 위기다. 동물·관·검은 혈액 하나를 공통 증거로 사용하지 않는다.'),
 ('X11','면역 반응·이물·이식의 구별','Transplantation;Transplant Rejection;Immunosuppression;Foreign-Body Reaction;Xenotransplantation','context','S22,S23','이식의 종·재료·면역 반응과 외부 봉합선은 별개다. 이종이식을 동물 외형으로 바꾸거나 모든 임플란트 문제를 이식 거부반응으로 부르지 않는다.'),
 ('X12','유전적 기원과 외형','Chimerism;Mosaicism;Cloning / Genetic Engineering','context','S20,S23','서로 다른 세포 기원·발달 과정·유전정보 조작은 외형만으로 확인되지 않는다. 모자이크의 세부 정의는 추가 조사 대상이며 복제는 기억·인격의 동일성 증거가 아니다.'),
 ('X13','배양·인공자궁·세포의 지속성','Organoid;Tissue Engineering;Immortal Cell Line;Ectogenesis / Artificial Womb;Organ Farm;Donor-Memory Transfer;Connected Implant','context','S21,S24','배양 구조·실험 장치와 사람의 의식·생식 기능·기억 전이·통신 침해를 분리한다. 기증자 기억 전이는 허구 가정이며 인공자궁 자료는 2023년 연구 목적까지만 지지한다.'),
 ('X14','동의·능력·강요','Informed Consent;Decision-Making Capacity;Coercion;Undue Influence;Therapeutic Misconception;Medical Paternalism;Non-Maleficence','context','S25,S26','동의는 정보·이해·자발성과 범위·시점이 필요하다. 서명·미소·고개 끄덕임을 충분한 동의 또는 의사결정능력의 증명으로 사용하지 않는다. 상세 능력·법역 기준은 별도다.'),
 ('X15','제도·노동·권한·착취','Research Exploitation;Dual Loyalty;Institutional Betrayal;Involuntary Admission;Physical / Chemical Restraint;Biobanking / Nonconsensual Tissue Use;Organ Trafficking','context','S02,S25','기관의 의도·법적 권한·거래·동의 이력은 외형 밖의 사실이다. 합법적 기증·돌봄·약물치료를 장기밀매·약물적 억제로 자동 재명명하지 않는다.'),
 ('X16','생식권과 강제 변경','Reproductive Coercion;Forced Pregnancy;Forced Abortion;Forced / Coerced Sterilization;Obstetric Violence;Forced Alteration of Sex Characteristics;Castration / Genital Mutilation','context','S26,S27','임신·출산·불임화·성징 변경의 강제·선택 여부는 몸의 외형으로 확정되지 않는다. 치료·자기 선택·폭력·차별의 문맥을 각각 보존한다. 특정 법률 정의는 별도 검증한다.'),
 ('X17','성적 경계·관음·역할극의 분리','Nonconsensual Intimate Examination;Sexual Boundary Violation;Medical Voyeurism;Medical Fetishism;Consensual Medical Roleplay;Forced Exposure;Surgical Eroticism;Necrophilia','context','S26,S28,S42','임상 노출·성적 관심·연출·동의·비동의·시신 대상 행위는 별개다. 의료복만으로 페티시·장애·동의·성폭력 또는 시체성애를 판정하지 않는다. 비동의 성행위는 선정적 시각 후보로 변환하지 않는다.'),
 ('X18','실험·고문·살아 있음·사후 검사','Mad Scientist / Rogue Surgeon;Medical Torture;Nonconsensual Human Experimentation;Vivisection;Dissection / Autopsy;Lobotomy / Leucotomy;Self-Surgery;Electroconvulsive Therapy, ECT','context','S09,S25,S29','기구·절개·전극은 고문·실험 목적·동의·생존·사망의 증거가 아니다. 현대 ECT·역사적 정신외과·형벌적 전기폭력을 합치지 않는다. 具体的 처치나 위해 방법은 후보 내용으로 넣지 않는다.'),
 ('X19','시신·부활·약용 신체의 역사와 허구','Resurrectionists / Body Snatchers;Reanimation;Corpse Medicine / Medicinal Cannibalism;Necrophilia','context','S29,S46','도굴 역사와 허구적 재활성화·의학적 소생은 구별한다. 약용 식인·시체성애의 개별 역사·진단 정의는 후속 원전 조사가 필요하며, 덮인 운반대·해부 관심으로 추정하지 않는다.'),
 ('X20','전후·원인·결과가 필요한 연출','Clinical Detachment;The Unreliable Chart;Escalating Treatment;The False Cure;Discharge Denial;Consent Trap;The Perfect Replacement;Caregiver–Captor;Menstrual Horror;Maternal Horror;Reproductive Commodification;Parasitic Gestation;Medical Cover-up','sequence','S01,S02,S04','치료가 커짐·효과·기억·규정 변경·정체성·은폐는 시간·대사·서사가 필요하다. 한 장의 기구 수·서류·붉은 액체로 전후 인과·월경·임신·악의를 입증하지 않는다.'),
 ('X21','시간적 호흡과 음향','Mechanical Breathing;Fluorescent Hum;Somatic Sound','audio','S33','기계 주기·호흡 동기화·형광등 소음·조직 마찰음은 정지 이미지에서 청취할 수 없다. 주름관·조명·습한 표면은 소리의 대리형일 뿐이다.'),
 ('X22','역사적 사례와 잘못된 과학','Eugenics;Nonconsensual Human Experimentation;Biobanking / Nonconsensual Tissue Use;Forced / Coerced Sterilization','historical','S30,S31,S32','터스키기는 고의 감염으로 바꾸지 않는다. 우생학적 서열은 사실이 아닌 차별적 주장이다. HeLa 관련 세부는 이번 NIH 본문 접근 실패로 보류하며 세포 지속성을 개인 의식의 지속성으로 설명하지 않는다.'),
]

COMBINATIONS = [
 ('Clinical Horror × Institutional Betrayal × Unreliable Chart','A11,D11,E03','차트 문자 불일치와 정돈된 공간','입원 이력 삭제·수술 사실·직원의 반복 대사는 별도 서사'),
 ('Transplantation Gothic × Bodily Autonomy × Perfect Replacement','W12,D01,E10','가상의 패치 경계·시야 차단·초현실적 반사 차이','이식 성공·결정권 상실·본래 정체성은 외형으로 판정 불가'),
 ('Reproductive Horror × Eugenics × Corporate Medical Horror','L03,L07,E03','재고 격자·빈 허구 챔버·가려진 서류','유전적 적격성·생식 강제·미래 직업 통제는 서사 주장'),
 ('Surgical Horror × Medical Gaze × Surgical Spectacle','A10,E04,E06','중앙대·관람 경계·전경 영상의 화면 구도','치료 목적이 관객 평가로 대체되었다는 변화는 대사·시퀀스 필요'),
 ('Hospital Horror × Delirium × Caregiver–Captor','A09,E01,E09','누운 시점·닿지 않는 호출기·문 너머 서류','섬망·간병인의 악의·실제 감금은 단정하지 않음'),
 ('Biopunk × Organ Farm × Immortal Cell Line','L02,L03,L09','표본과 배양·동일 격자·서로 다른 표기','불멸성·유전·사후 계약의 효력·가족 관계는 서사 필요'),
 ('Medical Gothic × Corpse Medicine × Reanimation','A06,E13,D12','요양시설 제안·역사 장부·투명 표본병','약용 인체·실제 시신·부활·대물림은 별도 원전과 서사 필요'),
]
WORKS = ['Frankenstein (1818)','Eyes Without a Face (1960)','Coma (1977 novel / 1978 film)',
 'Re-Animator (1985)','Dead Ringers (1988)','The Skin I Live In (2011)','American Mary (2012)',
 'Antiviral (2012)','The Autopsy of Jane Doe (2016)','Crimes of the Future (2022)','The Substance (2024)']
