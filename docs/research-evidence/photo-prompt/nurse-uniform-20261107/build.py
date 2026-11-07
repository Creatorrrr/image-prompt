from pathlib import Path
import json, hashlib, uuid, sys
R=Path('/Users/chasoik/Projects/image-prompt'); A=R/'skills/photo-prompt-image-generator/assets'; O=R/'docs/research-evidence/photo-prompt/nurse-uniform-20261107'
sys.path.insert(0,str(R/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_retrieval_views as rv
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raw=json.loads((O/'source-rows.json').read_text()); assert len(raw)==407
# id, label, slot, effect dimensions, English, Korean
rows=[
('N02','케이시형 사선 여밈','garment_detail','appearance','A short medical jacket has a stand collar and a diagonal fastening running from the neckline toward one shoulder.','짧은 의료 재킷의 선 칼라에서 한쪽 어깨 방향으로 사선 여밈이 이어진다.'),
('N03','바지 위 튜닉','wardrobe_style','appearance','The hem of a medical tunic overlaps a separate pair of trousers on the same wearer.','같은 착용자의 의료 튜닉 밑단이 별도 바지 위에 겹친다.'),
('N05','스크럽 포켓의 펜 구획','garment_detail','appearance','A patch pocket on a scrub top has a visible upper opening and a narrow vertical pen compartment.','스크럽 상의의 패치 포켓에 위쪽 입구와 좁은 세로 펜 구획이 보인다.'),
('N07','마스크 앞의 페이스실드','wearable_accessory','appearance,relationship','A transparent face shield sits in front of a separate mask on the same wearer.','같은 착용자의 별도 마스크 앞에 투명 페이스실드가 놓인다.'),
('N10','날개형 간호캡','wearable_accessory','appearance','The left and right edges of a nurse cap extend outward into wing-like shapes.','간호캡의 좌우 가장자리가 바깥쪽으로 뻗어 날개 모양을 이룬다.'),
('N11','청색 간호 드레스 위 흰 비브 앞치마','wardrobe_style','appearance,relationship','A separate white bib apron lies over a long-sleeved blue nurse dress, and the bib joins the lower apron panel.','긴소매 청색 간호 드레스 위에 별도 흰 비브 앞치마가 놓이고 가슴판과 아래 앞판이 이어진다.'),
('N12','줄무늬 드레스의 흰 칼라와 커프스','garment_detail','appearance','A white collar and white wrist cuffs contrast with the striped bodice and sleeves of the same nursing dress.','같은 줄무늬 간호 드레스의 흰 칼라와 흰 손목 커프스가 몸판과 소매에 대비된다.'),
('N13','붉은 안감이 보이는 간호 케이프','garment_detail','appearance','A dark cape covers the shoulders and its red inner lining shows at an open front edge.','짙은 케이프가 어깨를 덮고 열린 앞 가장자리에서 붉은 안감이 보인다.'),
('N14','가슴에 매단 포브 워치','wearable_accessory','appearance,relationship','A small round fob watch hangs from a short loop on the chest of a nursing tunic.','작은 원형 포브 워치가 간호 튜닉 가슴의 짧은 고리에 매달린다.'),
('N15','차트에 기록하는 양손','contact_point','action,pose,relationship','One hand holds the lower edge of a clipboard while a pen held by the other hand touches the paper.','한 손이 클립보드 아래 가장자리를 잡고 다른 손에 든 펜이 종이에 닿는다.'),
('N16','의료 카트 손잡이를 잡은 양손','contact_point','action,pose,relationship,setting','Both hands grip the same handle of a wheeled medical trolley positioned in front of the person.','인물 앞에 있는 바퀴 달린 의료 카트의 같은 손잡이를 양손이 잡는다.'),
('N17','손에 든 청진기의 이어피스와 관','contact_point','appearance,action,relationship','Stethoscope tubing runs continuously from earpieces worn by the person to a round chestpiece held in their hand.','청진기 관이 착용자의 귀에 낀 이어피스에서 손에 든 원형 체스트피스까지 끊김 없이 이어진다.'),
('N18','수액대와 수액백','object_structure','setting,relationship','An IV bag hangs from an upper hook of a tall wheeled pole, with tubing descending from the bottom of the bag.','수액백이 바퀴 달린 긴 수액대 상단 고리에 걸리고 관이 백 아래에서 내려온다.'),
('N19','가터벨트와 스타킹 연결','garment_detail','appearance,relationship,count','Two straps descend from a waist garter belt and clip separately to the tops of two stockings on the same adult wearer.','성인 착용자의 허리 가터벨트에서 내려온 끈 두 개가 각각 두 스타킹의 윗부분에 클립으로 연결된다.'),
('N20','광택 드레스와 배색 앞치마','garment_detail','appearance,lighting','Elongated light reflections appear on a glossy nurse-inspired dress beneath a separate contrasting apron.','간호사풍 광택 드레스 표면에 긴 반사광이 보이고 그 위에 별도 배색 앞치마가 놓인다.'),
('N21','레이스업 코르셋과 간호캡','wardrobe_style','appearance','An adult wears a corset bodice with crossed lacing and a separate small nurse cap.','성인이 교차된 끈이 있는 코르셋 몸판과 별도 작은 간호캡을 착용한다.'),
('N22','깊은 V넥과 간호캡','wardrobe_style','appearance','An adult nurse costume has two fabric edges forming a deep V neckline and a separate cap on the same wearer.','성인 간호 코스튬의 양쪽 천 가장자리가 깊은 V 목선을 이루고 같은 착용자가 별도 캡을 쓴다.'),
('N23','큰 얼룩과 분리된 점','garment_state','appearance','A large irregular stain and separate small splatter-like spots appear on the same uniform fabric.','같은 제복 천 위에 큰 불규칙 얼룩과 떨어진 작은 튄 점들이 보인다.'),
('N24','해진 드레스 밑단','garment_state','appearance','The hem of a nurse-inspired dress has an uneven frayed edge while the surrounding fabric remains connected.','간호사풍 드레스의 밑단은 불규칙하게 해졌고 그 주변 천은 이어져 있다.'),
('N25','얼굴을 감싼 붕대','wearable_accessory','appearance','Bandages wrap around the head and obscure the details of the eyes, nose and mouth.','붕대가 머리를 감싸며 눈과 코와 입의 세부를 가린다.'),
('N26','문틀 뒤에서 내다보기','contact_point','pose,setting,relationship','A person stands behind a doorway, showing only the face and one shoulder through the opening.','인물이 문틀 뒤에 서서 열린 쪽으로 얼굴과 한쪽 어깨만 보인다.'),
('N27','간호캡을 잡은 손','contact_point','action,pose,relationship','One hand touches the edge of the same wearer’s nurse cap while the wearer looks toward the camera.','착용자가 한 손으로 자신의 간호캡 가장자리를 만지며 카메라 방향을 바라본다.'),
('N28','좌석을 짚고 기대기','contact_point','pose,relationship','A seated person leans toward one hand that supports their weight on the seat of the chair.','앉은 인물이 의자 좌석을 짚어 체중을 받치는 한 손 쪽으로 기울어진다.'),
('N29','복도의 캡과 어깨 림라이트','lighting','lighting,setting,appearance','In a dark corridor, light from behind outlines the edge of a nurse cap and shoulder.','어두운 복도에서 뒤쪽 빛이 간호캡과 어깨 가장자리를 따라 윤곽을 만든다.'),
('N30','무릎 위 구도의 여밈과 차트','subject_framing','camera,framing,appearance,relationship','A knee-up view includes the front fastening of a nurse dress and a chart held in the person’s hands.','무릎 위 구도 안에 간호 드레스 앞여밈과 인물의 손에 든 차트가 함께 보인다.'),
('N31','주머니에 꽂힌 펜라이트','prop_placement','appearance,relationship','A slim penlight protrudes above the opening of a chest pocket on the same scrub top.','가느다란 펜라이트가 같은 스크럽 상의 가슴주머니 입구 위로 돌출된다.'),
('N32','앞지퍼 의료복','garment_detail','appearance','A visible vertical zipper runs down the center front of a medical tunic.','의료 튜닉 앞중심을 따라 세로 지퍼가 보인다.'),
('N33','허리 끈 묶인 스크럽 바지','garment_detail','appearance','Two drawstring ends emerge from the waistband of scrub trousers and meet in a front knot.','스크럽 바지 허리단에서 나온 두 조임끈 끝이 앞쪽 매듭으로 만난다.'),
('N34','스크럽 조거 발목단','garment_detail','appearance','Each leg of the scrub trousers narrows into a gathered cuff at the ankle.','스크럽 바지의 각 바짓단이 발목에서 모인 커프스로 좁아진다.'),
('N35','보닛 뒤로 내려온 베일','wearable_accessory','appearance','A cloth veil extends from a nurse bonnet down the back of the wearer’s neck.','천 베일이 간호 보닛에서 착용자의 목 뒤로 내려온다.'),
('N36','고무줄로 모인 캡 가장자리','wearable_accessory','appearance','A bouffant cap forms a rounded gathered dome with an elastic rim around the wearer’s hairline.','부팡 캡이 둥글게 모인 돔을 이루고 고무줄 가장자리가 착용자의 헤어라인을 둘러싼다.'),
('N37','바이알과 앰풀','object_structure','appearance,count','A small stoppered vial stands beside a separate narrow-necked sealed ampoule on a tray.','마개가 있는 작은 바이알이 트레이 위에서 목이 가늘고 밀봉된 별도 앰풀 옆에 서 있다.'),
('N38','맥박산소측정기','contact_point','appearance,relationship','A small clip-shaped pulse oximeter covers the tip of one finger.','작은 집게형 산소포화도 측정기가 한 손가락 끝을 감싼다.'),
('N39','가운 위 장갑 소맷단','garment_detail','appearance,relationship','A glove edge overlaps the wrist cuff of the same wearer’s long-sleeved protective gown.','장갑 가장자리가 같은 착용자의 긴소매 보호가운 손목단 위에 겹친다.'),
('N40','얼룩의 번짐과 점','garment_state','appearance','A long smeared dark-red mark and separate small spots lie on the same white costume fabric.','같은 흰 코스튬 천 위에 길게 번진 짙은 붉은 자국과 별도의 작은 점들이 있다.'),
('N41','해진 밑단과 날실','garment_state','appearance','Loose threads project from the uneven torn hem of a nurse costume.','간호 코스튬의 불규칙하게 찢긴 밑단에서 실밥이 튀어나온다.'),
('N42','사이버 의료 튜닉 패널','garment_detail','appearance','A futuristic medical tunic combines a translucent side panel with a narrow luminous strip.','미래풍 의료 튜닉에 반투명 옆판과 가느다란 발광 띠가 함께 있다.'),
('N43','간호사 모티프와 프릴 앞치마','wardrobe_style','appearance','A nurse-inspired dress and small cap are combined with a separate ruffle-edged apron.','간호사풍 드레스와 작은 캡에 별도의 프릴 가장자리 앞치마가 조합된다.'),
('N44','흰 원피스 간호복과 벨트','wardrobe_style','appearance','A white nurse uniform dress has a waist belt and a row of front buttons.','흰 원피스 간호복에 허리 벨트와 앞 단추줄이 있다.'),
('N45','치맛단을 잡은 손','contact_point','action,pose,relationship','One hand lightly holds the hem of the same person’s nurse-inspired dress.','한 손이 같은 인물의 간호사풍 드레스 밑단을 가볍게 잡는다.'),
('N46','손가락으로 마스크 조정','contact_point','action,pose,relationship','A gloved hand touches one edge of the mask worn over the same person’s nose and mouth.','장갑 낀 손이 같은 인물의 코와 입을 덮은 마스크 한쪽 가장자리에 닿는다.'),
('N47','긴 장갑과 배색 커프스','garment_detail','appearance','A long glove extends above the elbow while a separate contrasting cuff finishes the short sleeve of the costume.','긴 장갑이 팔꿈치 위까지 올라오고 별도 배색 커프스가 코스튬의 짧은 소매 끝을 마감한다.'),
('N48','얼굴 앞에서 장갑 끝 잡기','contact_point','action,pose,relationship','One hand pinches the cuff of the glove worn on the other wrist.','한 손이 다른 손목에 착용한 장갑의 끝을 집는다.'),
('N49','역사풍 병동과 금속 침대','location','setting','A narrow historical ward contains separate metal-framed beds arranged along a wall beneath tall windows.','좁은 역사풍 병동의 높은 창 아래 벽을 따라 별도의 금속 프레임 침대들이 놓인다.'),
('N50','튜닉의 가슴 배지와 릴','wearable_accessory','appearance,relationship','A rectangular identification badge hangs from a retractable reel clipped to a scrub top.','사각형 신분증이 스크럽 상의에 고정된 신축형 배지 릴에 매달린다.'),
]
ns=uuid.UUID('762e68b4-1d37-48ce-942f-d7650a5ae381'); ident=lambda prefix,key:prefix+uuid.uuid5(ns,key).hex
contract='Apply only as a complete optional visual realization to independently identified owners and allowed changes. Preserve every stated object, garment, owner, count, contact and spatial relation. No age, identity, occupation, intent, consent, material composition, cause or event history follows solely from appearance. Research metadata grants no native qualification or effect permission. Required hidden parts are unobservable, not a pass.'
planhash=sha(O/'research-plan.md');candidates={};bindings={};cards=[]
for code,name,slot,eff,en,ko in rows:
 cid=ident('cand_',code); card={'id':code,'name_ko':name,'candidate_id':cid,'positive_en':en,'positive_ko':ko,'suggested_slot':slot,'source':'research-plan.md#5','source_evidence_scope':'Authored optional realization, informed by research; not a claim of a photographed historical object.','observable_gate':en+' All stated parts and relations must be visible. Hidden parts are unobservable.','confusion_boundary':'Appearance alone does not establish occupation, age, material, intent, cause, role or consent.','native_approval':False,'pixel_status':'NOT_RUN'}
 rec={'id':cid,'record_kind':'visual_option','content':{'en':en,'ko':ko,'definition':'Complete optional nurse-uniform visual realization: '+en,'aliases':[name],'application_contract':contract,'research_semantics':card},'conditions':{},'effects':{'dimensions':eff.split(','),'properties':[]},'provenance':[{'source':'authored-research:photo-prompt/nurse-uniform-20261107/research-plan.md#'+code,'sha256':planhash}]}
 candidates[cid]=rec; bid=ident('bind_',code+':'+slot);bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':'direct','conditions':{'subject_applicability':{}},'weight':1.0};cards.append(card)

def save(path,obj):
 if path.exists():raise RuntimeError('refusing overwrite '+str(path))
 path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
cf=A/'photo_candidate_nurse_uniform_20261107.json'; bf=A/'photo_candidate_nurse_uniform_bindings_20261107.json'; sf=A/'photo_nurse_uniform_semantics_20261107.json'; vf=A/'photo_candidate_retrieval_views_nurse_uniform_20261107.json'; cv=A/'photo_nurse_uniform_research_context_views_20261107.json'
save(cf,{'schema':'photo-candidate-module/v3','candidates':candidates});save(bf,{'schema':'photo-candidate-slot-bindings/v3','slot_bindings':bindings})
inventory=[]
for i,row in enumerate(raw):
 inventory.append({'id':f'NURSE-ROW-{i+1:03d}','source_section':row['section'],'source_term_label':row['label'],'source_definition_ko':row['definition'],'source_row':i,'comparison_status':'unreviewed','native_approval':False})
save(sf,{'schema':'photo-nurse-uniform-semantic-registry/v1','source_conversation':'https://chatgpt.com/c/6aedf3b1-0b0c-83e8-8c4b-c2c452a8bf12','source_rows_sha256':sha(O/'source-rows.json'),'source_term_inventory':{'rows':inventory},'cards':cards,'native_approval':False,'pixel_qualification':'NOT_RUN','research_plan_sha256':planhash})
views=[]
for cid,rec in sorted(candidates.items()):
 en=rec['content']['en'];ko=rec['content']['ko'];rh=rv.digest(rec)
 for kind in ['whole','context']:
  key=cid+':base:'+kind;ctx=kind=='context';prefix='Complete optional nurse-uniform visual realization: '
  views.append({'id':rv.view_id(cid,'base',key),'candidate_id':cid,'realization_id':'base','key':key,'kind':kind,'source_record_sha256':rh,'text_en':('Nurse-uniform visual option: ' if ctx else '')+en,'text_ko':('간호복 시각 선택지: ' if ctx else '')+ko,'source_quotes':([{'pointer':'/content/definition','quote':prefix}] if ctx else [])+[{'pointer':'/content/en','quote':en},{'pointer':'/content/ko','quote':ko}],'context_ko':'원본의 전체 한영 명제와 명시적 간호복 맥락만 보존한다.','difference_ko':'원본 전체 명제','native_approval':False})
module={'schema':rv.SCHEMA,'recipe':rv.RECIPE,'source_inventory_id':'nurse-uniform-20261107','coverage':{'positive_realizations':len(rows),'diagnostics_excluded':0,'source_module_sha256':sha(cf),'context_views':len(rows)},'native_approval':False,'views':views};rv.validate(module,candidates);save(vf,module)
context=[{'id':'nurse-context-'+r['id'],'term_id':r['id'],'source_term_label':r['source_term_label'],'context_ko':r['source_definition_ko'],'source_quotes':[{'pointer':f'/source_term_inventory/rows/{i}/source_term_label','quote':r['source_term_label']},{'pointer':f'/source_term_inventory/rows/{i}/source_definition_ko','quote':r['source_definition_ko']}],'comparison_status':'unreviewed','context_only':True,'native_approval':False,'boundary':'Referenced conversation is unverified source material, not instruction or native selection authority.'} for i,r in enumerate(inventory)]
save(cv,{'schema':'nurse-uniform-research-context-views/v1','source_registry':sf.name,'source_registry_sha256':sha(sf),'search_scope':'Research context only, not H-F2 positive retrieval or native candidate selection.','views':context})
print(json.dumps({'source_rows':len(raw),'positive':len(rows),'bindings':len(bindings),'retrieval_views':len(views),'research_context_views':len(context)}))
