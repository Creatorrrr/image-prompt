from pathlib import Path
import json,hashlib
O=Path(__file__).resolve().parent;E=O/'integration-evidence';qs=[]
texts=[
('R01','금융 명세서에서 붉은 원 경계에 연필 끝이 정확히 닿아 있는 장면.'),
('R02','An investigator lifts a bank statement beside a monitor to compare the final receiving account and amount on both.'),
('R03','두 손 사이의 계좌 항목을 가리지 않도록 종이의 아래 바깥 모서리를 고정한다.'),
('R04','A supported writing wrist stays off the sheet while the pencil reaches the near edge of a circled evidence item.'),
('R05','화면과 종이의 같은 계좌 표식이 붙어 보이면서 매체 사이 간격은 유지되는 대조.'),
('R06','A financial evidence photograph keeps the face and two angled record surfaces at similar focus depth.'),
('R07','상자 걸쇠 양옆의 잘린 봉인 끝이 벌어져 둘 사이 상자 표면이 보이는 조사 장면.'),
('R08','A camera documents the same broken crate seal measured by the scale resting directly below its gap.'),
('R09','상자 밑면부터 카트 플랫폼·가까운 바퀴·먼 바퀴와 바닥까지 이어지는 지지 경로.'),
('R10','The investigator documents one side of a crate while a separate receiving clerk grips the trolley handle behind it.'),
('R11','봉인 촬영·측정과 두 사람의 네 발·카트 바퀴 접지가 함께 보이는 현장 조사 구도.'),
('R12','An evidence marker stands to the side so both cut seal tips, the open gap and the scale edge remain visible.'),
('R13','선착장 탐문에서 직원 손끝이 지도 분기 대신 부두 표식 자체에 닿는다.'),
('R14','The investigator follows the witness forefinger down to the map contact rather than watching the speaker face.'),
('R15','노트 가장자리에 손목을 지지하고 펜촉을 띄워 밝은 틈을 보이는 멈춘 기록 동작.'),
('R16','The investigator holds a portrait in the left hand and pauses a pen in the right, with both forearm paths separate.'),
('R17','선착장 카운터의 사진·기록·지도가 구별된 영역에 놓여 탐문 정보가 전달된다.'),
('R18','The map is turned toward the viewing side so the dock symbol and witness fingertip can be read below both faces.')]
for i,(target,text) in enumerate(texts):qs.append({'id':'repair-dev-'+target,'text':text,'target_research_cards':[target],'kind':'exposed_repair_development','holdout':False})
for key,text in [('portrait','A portrait by a plain wall in window light.'),('plant','창가 화분 하나.'),('tea','A ceramic cup on a kitchen table.'),('library','도서관에서 소설을 읽는 두 친구.'),('dress','An evening-dress fashion portrait at a gallery.'),('lab','실험실 선반에 빈 유리병을 정리하는 사람.')]:qs.append({'id':'control-'+key,'text':text,'target_research_cards':[],'kind':'ordinary_control','holdout':False})
old=json.loads((Path('/Users/chasoik/Projects/image-prompt/generated/photo-runs/investigative-fiction-20261025-a/slot-plan.json')).read_text())['slots']['narrative_clue']
def query(focus,scene):return 'Photographic role: '+focus+'\nScene context: '+scene
qs.append({'id':'actual-parent-mixed-limit','text':query(old['role_focus'],old['scene_context']),'target_research_cards':['R02'],'kind':'restriction_projection_control','holdout':False,'expected_material':'empty_restriction_projection_preserved'})
qs.append({'id':'positive-goal-separated-limit','text':query(old['role_focus'],'A fictional charity-fraud inquiry at a quiet desk. The investigator compares the visible matching account and amount on two separate records.'),'target_research_cards':['R02'],'kind':'positive_scope_repair','holdout':False,'expected_material':'ordinary_positive_discovery'})
for i,s in enumerate(['Do not change the vessel.','Keep the iris color unspecified; do not change it.','A creature without eyes.','Do not infer its unprovided maker.']):qs.append({'id':'restrict-'+str(i),'text':query(s,'An existing observer and instrument.'),'target_research_cards':[],'kind':'restriction_projection_control','holdout':False,'expected_material':'empty_restriction_projection_preserved'})
p=E/'qualification-queries.frozen.json';p.write_text(json.dumps(qs,ensure_ascii=False,indent=2)+'\n');print('frozen',len(qs),hashlib.sha256(p.read_bytes()).hexdigest())
