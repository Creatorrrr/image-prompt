from pathlib import Path
import json,hashlib
O=Path(__file__).resolve().parent
positives=[
('U06','en','A sleeveless school pinafore over a collared blouse, with the shoulder straps and continuous bodice-to-skirt panel visible.'),
('D03','ko','셔츠 앞단 단추와 별개로 양쪽 깃끝을 몸판에 고정하는 작은 단추가 보이는 버튼다운 칼라'),
('P03','en','At the skirt front two folded edges converge inward along a center line, with the extra fabric behind the meeting.'),
('M02','ko','치마 위 가로세로 색띠가 서로 다른 폭을 가지며 같은 색 순서가 반복되는 타탄 무늬'),
('X03','en','A hooded coat fastened across the front with long toggles inserted through opposite cord loops.'),
('B03','ko','발등의 중앙 세로 스트랩과 가로 발목 스트랩이 T자로 만나는 낮은 구두'),
('H10','en','A raised Dutch braid follows the scalp with side sections joining beneath the center ridge.'),
('I02','ko','코 아래로 내려온 안경 브리지 밑에 손끝이 닿고 눈은 테 위로 보이는 자세'),
('V02','en','School fashion with lightened curled hair, pronounced eyeliner and slouched socks gathered over low shoes.'),
('Q01','ko','왼다리에 체중을 싣고 오른 무릎은 풀어 어깨와 골반 기울기가 대응하는 선 자세'),
('A08','en','On a low bench the student bends toward one shoe and holds opposite ends of that same shoe lace in separate hands.'),
('R03','ko','친구가 다른 학생의 깃 아래 타이 매듭을 집어 고치고 착용자는 턱을 올려 친구 얼굴을 보는 모습'),
('F04','en','In a staged school confrontation one hand grips the other student jacket near the collar, with fabric tension converging on that grip.'),
('E03','ko','삽화 캐릭터의 관자 옆 큰 땀방울 기호가 실제 피부 음영과 분리된 학원 만화 장면'),
('T01','en','Both shirt sleeves have been rolled twice below the elbows, leaving the forearms beneath stacked cuff folds.'),
('C03','ko','전경 한쪽의 친구 어깨와 뒤통수 너머 책상 건너 다른 학생 얼굴이 보이는 오버숄더 구도')]
boundary=[
('en','A-line skirt shape without a required pleat type','silhouette is independent of pleat construction'),
('ko','옥스퍼드 원단 셔츠와 옥스퍼드 구두를 서로 구분','textile and footwear are independent constructions'),
('en','The figure is in three-quarter rotation, independently of a waist-up crop','body rotation is not crop extent'),
('ko','수직 문틀이 기운 카메라 구도와 수평 화면에서 몸만 기운 자세의 구별','camera roll is separate from body lean'),
('en','One hand near another person tie, without a visible fingertip contact','proximity is not established contact'),
('ko','교복과 붉은 볼만 보고 실제 나이와 호감을 알 수 있는가','no age or inner-state inference'),
('en','A reddish stain and a knee brace without verified injury cause or timing','no chemistry, cause, diagnosis or chronology inference'),
('ko','사진 피부의 실제 땀과 삽화 땀방울 기호를 분리','drawn symbol is not literal anatomy')]
controls=[('en','A ceramic coffee cup on a wooden table beside a window'),('ko','바닷가 모래 위 둥근 조약돌과 파도'),('en','A city tram passing a stone bridge at dusk'),('ko','흰 배경 위 포장 상자와 유리 향수병')]
cases=[{'id':'P%02d'%(i+1),'set':'development','language':l,'query':q,'expected_cards':[c]} for i,(c,l,q) in enumerate(positives)]
cases +=[{'id':'B%02d'%(i+1),'set':'boundary','language':l,'query':q,'boundary':b,'expected_cards':[]} for i,(l,q,b) in enumerate(boundary)]
cases +=[{'id':'C%02d'%(i+1),'set':'general_control','language':l,'query':q,'expected_cards':[]} for i,(l,q) in enumerate(controls)]
p=O/'retrieval-development-cases.json';assert not p.exists();p.write_text(json.dumps({'cases':cases,'scope':'28 authored development probes: 16 positives spanning every section, 8 distinction probes, 4 ordinary controls. Not independent holdout. No post-result trimming.','pass_gate':'All 140 new visual CIDs indexed, all 28 diagnostic CIDs excluded; all 16 expected targets at rank <=32. Boundary probes are reviewed, not proof of inferred intent.','baseline_comparison':'General controls compared against installed baseline before activation.'},ensure_ascii=False,indent=2)+'\n')
(O/'retrieval-cases-freeze.json').write_text(json.dumps({'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'queries':len(cases),'before_retrieval':True},indent=2)+'\n')
print(len(cases))
