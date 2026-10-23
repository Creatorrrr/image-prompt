from pathlib import Path
import json
D=Path(__file__).resolve().parent;O=D.parents[3]/'generated/photo-runs/espionage-full-20261023-control/maintenance-final'
read=lambda p:json.loads(p.read_text())
cards=read(D/'semantic-cards.json');cases=[]
for c in cards:
 for lang in ('ko','en'):cases.append({'id':c['id']+'-'+lang,'cohort':'source_literal_smoke','language':lang,'query':c['visible_'+lang],'expected_cards':[c['id']]})
natural=[
('frayed_cuff','소매 끝에서 실이 직접 풀려 나오고 옆 직조는 온전한 커프','A cuff edge unravelling into loose threads that remain attached to the sleeve'),
('wet_coat','마른 천 옆 어두워진 외투 천에 물방울이 따로 맺힌 상태','Dark damp cloth beside a dry area on one opaque coat with visible beads of water'),
('creased_sleeve','같은 소매 천의 각진 접힘에서 솟은 선과 그늘진 골이 보임','Angular folds in one sleeve showing raised creases and shadowed troughs'),
('worn_lapel','외투 라펠의 닳아 밝아진 조각 옆에 온전한 짙은 천','A scuffed light patch adjoining undamaged darker cloth on a coat lapel'),
('grime_seam','가방 솔기의 홈에 때가 모이고 솟은 가장자리는 깨끗함','Dirt accumulated in a bag seam recess beside a cleaner raised edge'),
('continuity_pair','종이 사진 두 장 속 외투의 같은 소매 자국과 라펠 자국 비교','Two separate printed costume photos with corresponding cuff tears and lapel marks'),
('cowboy_frame','얼굴과 손 허리가 보이고 아래 테두리가 허벅지 중간을 자르는 세로 구도','Vertical portrait cropped across the middle of the thighs with head waist and hands visible'),
('door_occlusion','가까운 문설주가 먼 사람 몸의 가장자리를 조금 가림','A nearby doorpost overlapping the outer edge of a person farther inside'),
('rim_outline','어두운 배경 앞 머리와 외투 어깨 끝에 가는 역광 윤곽','Thin back-side light separating hair and coat shoulder edges from a dark background'),
('ots_frame','앞 사람 어깨 너머 다른 사람 얼굴에 초점 맞춘 화면','Camera looking past one foreground shoulder at another person’s focused face'),
('dutch_frame','문 수직선과 방 수평선이 화면 테두리 대비 함께 기운 구도','The room horizon and door uprights tilt together relative to the rectangular image edges'),
('full_frame','머리 위와 신발 아래 여백이 있는 전신 사진','A full body image including the top of the head and both complete shoes with margins'),
('lowkey_face','한쪽 얼굴과 손만 밝고 반대쪽 얼굴과 방은 어두운 명암','Selective light on one face side and a hand contrasted with a dark room and opposite face side'),
('dossier_spread','탁자 위 열린 폴더에 종이 사진과 별도 타자 문서가 구분됨','An open dossier with a clipped paper portrait and separate typed pages'),
('contact_sheet_window','창가에서 작은 사진 격자가 인쇄된 시트를 들고 실제 안뜰은 창 너머에 있음','A held contact sheet of small printed photographs beside a window onto a separate real courtyard'),
('annotated_print','종이 사진 안의 문을 종이 표면에 그린 붉은 원으로 표시','A red circle drawn on a physical print around a doorway depicted inside that photo'),
('monitor_room','실제 관찰실의 사람과 화면 속 별도 복도 이미지 경계','An observer outside two monitor images showing separate corridors'),
('broken_seal','봉투 덮개 양쪽에 붙은 찢어진 종이 봉인 조각과 사이 틈','Two torn paper seal halves attached to opposite envelope flaps with a gap between their edges')]
for i,(slug,ko,en) in enumerate(natural):
 for lang,q in [('ko',ko),('en',en)]:cases.append({'id':f'natural-{i+1}-{lang}','cohort':'natural_regression','language':lang,'query':q,'expected_cards':['espfull_'+slug]})
controls=[('ordinary_control','흰 배경 위 빨간 사과 하나','One red apple on a plain white background'),('ordinary_control','유아 없는 빈 나무 의자 제품 사진','Product photograph of an empty wooden chair'),('ordinary_control','해 뜬 산과 호수의 넓은 풍경','Wide landscape of a mountain and lake at sunrise'),('ordinary_control','평평한 접시에 담긴 파스타 요리','Pasta served on a flat plate'),('nonvisual_boundary','복장이 CIA 소속을 증명하는가','Does clothing prove CIA employment'),('nonvisual_boundary','표정만으로 PTSD나 도덕적 손상을 진단','Diagnosing PTSD or moral injury from a facial expression'),('nonvisual_boundary','친밀한 자세가 성적 동의나 협박을 증명하는가','Does an intimate pose establish consent or blackmail'),('nonvisual_boundary','빈방만으로 강제실종의 국가 관여를 증명','Proving state involvement in enforced disappearance from an empty room'),('confusion_control','배우가 고개를 기울였지만 문과 수평선은 수직 수평','A person tilts their head while the door uprights and horizon stay level'),('confusion_control','사진 위 표시와 실제 방의 문을 구분','Distinguish a mark on a photograph from a doorway in the physical room')]
for i,(cohort,ko,en) in enumerate(controls):
 for lang,q in [('ko',ko),('en',en)]:cases.append({'id':f'control-{i+1}-{lang}','cohort':cohort,'language':lang,'query':q,'expected_cards':[]})
(O/'frozen-query-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
# Adapt proven genuine two-lane runner without keyword filters or shortcut ranks.
T=D.parents[3]/'generated/photo-runs/espionage-20261023-control/maintenance/rebase-latest/qualify_queries.py';s=T.read_text();start=s.index(" registry=read(E/'data-integration.json')");end=s.index(' fingerprint=',start)
s=s[:start]+" cards=read(R/'docs/research-evidence/photo-prompt/espionage-full-conversation-20261023/semantic-cards.json')\n lookup={c['id']:c['candidate_id'] for c in cards}\n cases=read(O/'frozen-query-cases.json')\n"+s[end:]
s=s.replace("else 'probe-after.json'","else 'probe-after.json'")
(O/'qualify_queries.py').write_text(s)
print('queries',len(cases),'literal',84,'natural',36,'controls',20)
