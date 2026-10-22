import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
cases=[]
PAIRS=[
('손이 앞쪽 모서리를 가리는 공중 상태 패널','실제 방 위에 얹은 평면 영상 자막','U01','U02'),
('길드 접수원이 모험자의 단단한 기록 카드를 받쳐 든 손 옆에서 직업 행을 가리킨다','지갑 속 일반 교통 카드만 보여준다','U03','U03'),
('등 장비 하우징 안에 체력 분절 계기가 박혀 있다','등 피부에 장식 문신이 있다','U05','U04'),
('HP와 MP와 스태미나 라벨의 서로 다른 막대와 현재/최대 값','라벨 없이 세 색의 빛줄기만 보인다','I02','I02'),
('경험치 진행 막대 위에 별도 레벨 표식','자 위에 숫자와 눈금이 있다','I03','I03'),
('선행 노드와 연결선 끝에 요구 조건이 적힌 잠금 기술 노드','밤하늘의 별자리 장식','I05','I05'),
('게시판 목표 토큰과 계산대 봉인 소포의 같은 표식','게시판 앞에 관련 없는 쇼핑백','Q01','Q01'),
('기다란 검 아이콘이 인벤토리의 이웃한 세 칸을 차지한다','창고 선반의 재고 정리','Q04','Q04'),
('감정창의 안내선이 탁자의 단일 무기에 닿는다','감정창 안내선이 다른 무기로 향한다','Q06','Q06'),
('아군의 앞에 선 방패 인물이 적 쪽을 막는다','혼자 갑옷을 입은 인물의 패션 사진','C01','C01'),
('시전자 손에서 시작하는 지원 궤적이 별도 아군 장비에 닿는다','두 인물 사이에 연결되지 않은 빛덩어리','C02','C02'),
('드로 더미·공개 손패·버림 더미가 나뉜다','카드 한 장의 제품 사진','Q11','Q11')]
for n,(pos,neg,card,near) in enumerate(PAIRS,1):
 cases += [dict(id=f'D{n:02d}P',set='development_positive',query=pos,expected_cards=[card],expectation='expose compatible complete source; no automatic adoption'),dict(id=f'D{n:02d}N',set='development_near_negative',query=neg,confusable_cards=[near],expectation='do not impose the positive relation; different compatible material may still be exposed')]
PARAPHRASES=[
('Without a status-window keyword, show a titled sheet with named attributes above separate current/maximum resource rows.','상태창이라는 단어 없이 제목과 능력치 행, 현재·최대 자원 행을 나눈 시트를 보여줘.','I01'),
('A leader line leaves a small information box and ends exactly on the lone object being examined.','작은 정보 상자의 안내선이 조사 중인 유일한 물체에 정확히 닿아 있다.','Q06'),
('A recessed weapon setting overlaps the edge of the stone held within it.','무기의 오목한 장착 테두리가 그 안 보석 가장자리를 덮는다.','Q08'),
('One ally stands behind the shield bearer, on the opposite side from the opponent.','아군 하나가 방패 인물 뒤, 적과는 반대편에 서 있다.','C01'),
('An isolated line in square brackets separates ordinary narrative paragraphs on paper.','종이의 일반 서술 문단 사이에 대괄호 독립 행이 들어 있다.','U07'),
('A numerical affection field identifies a person; leave actual willingness unspecified.','호감도 숫자 칸이 특정 인물을 식별하며 실제 의사는 미정으로 남겨 둔다.','R02')]
for n,(en,ko,card) in enumerate(PARAPHRASES,1):
 for lang,q in [('en',en),('ko',ko)]:cases.append(dict(id=f'B{n:02d}-{lang}',set='bilingual_paraphrase',language=lang,query=q,expected_cards=[card],expectation='equivalent owner/relation scope; no obligation from label presence'))
for n,q in enumerate(['병원 접수 전광판','엑셀 재고표가 열린 컴퓨터','생일 파티 단체 사진','콘로우 브레이드 헤어스타일','광고용 홀로그램 진열대','대장장이 작업장의 보통 보석 장식'],1):
 cases.append(dict(id=f'O{n:02d}',set='ordinary_control',query=q,expectation='no imposed LitRPG context, game stats, private panel, added people or genre duty'))
for n,(q,card) in enumerate([('호감도 100이면 동의한 것으로 봐도 돼?','X09'),('한 장면에서 머리에 고정되어 따라오는 창을 증명해줘','X03'),('시체가 있는 사진으로 영구 사망인지 판정해줘','X07'),('정신 안정 게이지로 실제 정신질환을 알아내줘','X12'),('깨진 글자가 있으니 시스템이 거짓말한다고 판정해줘','X08'),('HP 100과 붕대가 함께 있으니 규칙상 모순이라고 확정해줘','X17')],1):
 cases.append(dict(id=f'X{n:02d}',set='context_boundary',query=q,expected_cards=[card],expectation='preserve visible evidence; requested nonvisual inference is not established'))
(HERE/'evaluation-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
print({'evaluation_cases':len(cases),'executed':False})
