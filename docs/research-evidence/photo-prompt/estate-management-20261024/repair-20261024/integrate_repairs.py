"""Add bounded optional visibility examples; never rewrite the tested sources."""
from pathlib import Path
import json,hashlib,uuid
R=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent;A=R/'skills/photo-prompt-image-generator/assets'
read=lambda p:json.loads(p.read_bytes())
write=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rows=[
('R01','unbroken_cart_route','한 길의 양 끝과 타작장 출구',
 'A single uninterrupted cart track starts at the village beside the field edge, passes through a wide gap in the threshing-yard curb, and reaches the open store entrance below the estate hall. Two loaded carts stand on different visible stretches of that same track; the entire track and all three junctions are visible together.',
 '하나의 끊기지 않는 수레길이 밭 가장자리의 마을에서 시작해 타작장 낮은 경계의 넓은 출구를 지나 저택 아래 열린 창고 입구에 닿는다. 짐 실은 수레 두 대가 그 같은 길의 서로 다른 보이는 구간에 놓이며, 길 전체와 세 연결 지점이 함께 보인다.',
 ['location','composition','narrative_clue'],['setting','composition','count'],
 ['village','field_edge','track','curb_gap','store_entrance','hall','loaded_cart_one','loaded_cart_two'],
 [['track','starts_at','village'],['track','beside','field_edge'],['track','passes_through','curb_gap'],['track','ends_at','store_entrance'],['store_entrance','below','hall'],['loaded_cart_one','on','track'],['loaded_cart_two','on','track']],
 '서로 다른 도로 조각·여러 수레·방향만 맞는 화살표는 같은 끊기지 않는 길의 증거가 아니다.',
 ['마을/밭 끝점과 창고 문턱이 모두 보임','타작장 경계의 실제 열린 출구와 같은 길이 연결됨','두 수레의 짐과 바퀴 접지가 같은 경로에 보임']),
('R02','drain_visible_outfall','배수구의 시작·출구·받는 지면',
 'An open shallow channel runs from the dry paving of the grain yard to a visible outlet above a lower patch of wet earth. The channel bed, its complete outlet lip and the receiving wet patch remain in the same unobstructed view; a short visible stream bridges the outlet and the wet earth.',
 '얕고 열린 수로가 곡물 마당의 마른 포장에서 더 낮은 젖은 흙 위의 보이는 출구까지 이어진다. 수로 바닥과 출구 턱 전체, 물을 받는 젖은 땅이 가림 없이 같은 화면에 남고, 짧게 보이는 물줄기가 출구와 흙 사이를 잇는다.',
 ['composition','environment_detail','narrative_clue'],['setting','composition','material'],
 ['dry_paving','channel','outlet_lip','visible_stream','lower_wet_earth'],
 [['channel','starts_at','dry_paving'],['channel','ends_at','outlet_lip'],['visible_stream','connects','outlet_lip'],['visible_stream','reaches','lower_wet_earth']],
 '수로의 물만으로 프레임 밖 출구·정상 배수 성능·과거 개선 성공을 입증할 수 없다.',
 ['마른 포장과 수로 시작이 보임','수로 끝의 턱과 물줄기 전체가 보임','낮은 젖은 수용 지면이 프레임 안에 보임']),
('R03','shared_pointed_work_target','지시선과 현장 책임자의 시선',
 'The estate inspector points toward a loaded cart at the grain-store entrance while the foreman turns his face and eyes toward that very cart. He holds a yard plan below chest level, leaving the pointing arm, both faces, the cart and the store doorway visible together. Both standing figures have their boot soles visibly planted on the paved yard.',
 '영지 점검자는 창고 입구의 짐 실은 수레를 가리키고, 현장 책임자는 얼굴과 눈을 바로 그 수레 쪽으로 돌린다. 책임자가 마당 도면을 가슴 아래로 받쳐 두어 지시하는 팔, 두 얼굴, 수레와 창고 문이 함께 보인다. 서 있는 두 인물의 장화 밑창은 포장 마당에 닿아 보인다.',
 ['relational_action','composition'],['action','pose','composition','body_geometry'],
 ['inspector','pointing_arm','foreman','yard_plan','loaded_cart','store_doorway','boot_soles','paving'],
 [['pointing_arm','owned_by','inspector'],['pointing_arm','indicates','loaded_cart'],['foreman','looks_at','loaded_cart'],['foreman','holds','yard_plan'],['loaded_cart','at','store_doorway'],['boot_soles','contact','paving']],
 '지시자의 얼굴을 바라보는 반응과 지시선 끝의 작업 대상을 바라보는 반응은 다르다. 밑창 가림은 숨은 변형 진단이 아니다.',
 ['지시하는 손의 끝점과 책임자의 시선이 같은 수레를 향함','도면·팔·얼굴이 대상과 문을 가리지 않음','선택한 전신 지지 상태의 밑창 접지가 보임']),
('R04','two_fingertips_one_parcel','같은 지도 구획의 두 지시 접점',
 'Two petitioners point from opposite table edges to two separate interior points of one narrow outlined parcel on the same bank of a mapped river. Both fingertips lie inside that single closed parcel boundary, with clear paper between their hands; the complete boundary and both riverbank endpoints remain visible.',
 '두 청원자가 탁자의 반대쪽에서 지도 속 강의 같은 둑에 있는 하나의 좁은 폐곡선 구획 내부의 서로 다른 두 점을 가리킨다. 두 손가락 끝은 같은 닫힌 구획 경계 안에 놓이고 손 사이의 종이가 분명히 보이며, 구획 경계 전체와 강둑의 두 끝점도 보인다.',
 ['relational_action','composition'],['action','pose','composition'],
 ['petitioner_one','petitioner_two','fingertip_one','fingertip_two','parcel_boundary','riverbank_endpoints','map'],
 [['fingertip_one','owned_by','petitioner_one'],['fingertip_two','owned_by','petitioner_two'],['fingertip_one','inside','parcel_boundary'],['fingertip_two','inside','parcel_boundary'],['parcel_boundary','on','map']],
 '같은 지도를 만지는 것만으로 같은 구획을 지시한 것은 아니다. 맞은편 강둑의 다른 색 구획으로 대체하지 않는다.',
 ['두 손의 소유자가 분명함','두 손끝이 같은 하나의 폐곡선 안에 있음','경계·양 끝점을 손과 자가 가리지 않음']),
('R05','map_bound_register_landmarks','지도와 제본 장부의 완전한 대응 도형',
 'A large land map and an open bound register show the same river bend, single bridge and narrow closed parcel outline. The two bridge ends, complete parcel boundary and riverbank junctions are unobstructed on both surfaces. A straightedge rests on the blank map margin, outside these drawn connections.',
 '큰 토지 지도와 열린 제본 장부에 같은 강의 굽이, 다리 하나와 좁고 닫힌 구획 윤곽이 그려져 있다. 두 기록면 모두에서 다리의 양 끝과 구획 경계 전체, 강둑 연결점이 가림 없이 보인다. 곧은 자는 이 연결 그림 바깥의 빈 지도 여백에 놓인다.',
 ['composition','prop','narrative_clue'],['composition','text'],
 ['land_map','bound_register','river_bend','bridge_ends','parcel_boundary','riverbank_junctions','straightedge','blank_margin'],
 [['river_bend','repeated_on','land_map'],['river_bend','repeated_on','bound_register'],['parcel_boundary','repeated_on','land_map'],['parcel_boundary','repeated_on','bound_register'],['straightedge','on','blank_margin']],
 '비슷한 색과 강 모양은 구획 전체의 정확한 대응을 대신하지 않는다. 보이는 대응은 소유권·정확한 측량·실제 판결의 증거가 아니다.',
 ['두 기록면이 같은 강/다리/구획 형태를 보임','두 기록면의 모든 선택된 연결과 끝점이 보임','자와 손이 실제 연결을 덮지 않음']),
('R06','pen_on_bound_register_row','펜촉과 제본 장부 행의 직접 접촉',
 'Beside the land map, a clerk steadies the lower edge of an open bound register with one hand and places the pen tip directly on a ruled entry in that same book with the other. The pen tip, its small ink stroke, the ruled row and the register binding are visible together as one continuous writing contact.',
 '토지 지도 옆에서 서기관이 한 손으로 열린 제본 장부의 아래쪽 가장자리를 받치고, 다른 손의 펜촉을 바로 그 책의 줄 친 기록 행에 직접 댄다. 펜촉과 작은 잉크 획, 기록 행과 장부 제본이 하나의 이어진 필기 접점으로 함께 보인다.',
 ['relational_action','prop','composition'],['action','pose','composition'],
 ['clerk','steadying_hand','writing_hand','pen_tip','ink_stroke','ruled_entry','bound_register'],
 [['steadying_hand','owned_by','clerk'],['writing_hand','owned_by','clerk'],['writing_hand','holds','pen_tip'],['pen_tip','contacts','ruled_entry'],['ruled_entry','on','bound_register'],['ink_stroke','at','pen_tip']],
 '가까운 별도 종이의 필기·공중의 펜·장부 위에 겹친 펜의 투영은 선택한 장부 행과의 실제 접촉을 대신하지 않는다.',
 ['손목-손-펜이 같은 서기관에 연결됨','펜촉이 선택된 제본 장부 행에 닿음','작은 획과 행·제본 경계가 함께 보임']),
('R07','four_separate_loaf_supports','한 빵의 네 손 지지 접점',
 'At the bakehouse table, a woman and a baker hold opposite ends of one mostly connected loaf. Each person cups their end from below with two hands; all four wrists and all four separate hand-to-crust contact patches are visible, with open gaps between neighboring wrists. The loaf stays above the table while the contact edges face the camera.',
 '제빵소 탁자에서 여성과 제빵사가 대부분 이어져 있는 빵 하나의 양 끝을 잡는다. 각 인물이 두 손으로 자기 쪽 끝을 아래에서 받치며, 네 손목과 서로 구별되는 네 손-껍질 접촉면이 모두 보이고 이웃 손목 사이에는 열린 간격이 있다. 빵은 탁자 위쪽에 들려 있고 접촉 가장자리는 카메라를 향한다.',
 ['relational_action','composition'],['pose','body_geometry','composition','action'],
 ['woman','baker','woman_hand_one','woman_hand_two','baker_hand_one','baker_hand_two','loaf','table'],
 [['woman_hand_one','owned_by','woman'],['woman_hand_two','owned_by','woman'],['baker_hand_one','owned_by','baker'],['baker_hand_two','owned_by','baker'],['woman_hand_one','supports','loaf'],['woman_hand_two','supports','loaf'],['baker_hand_one','supports','loaf'],['baker_hand_two','supports','loaf']],
 '세 접점이나 가려진 한 손은 네 접점 전체의 성공이 아니다. 팔이 다른 사람에게 이어지거나 빵·팔 뒤 접촉을 상상해 채우지 않는다.',
 ['두 사람의 네 손목이 각각 몸에 이어짐','각 사람의 두 손이 자기 쪽 빵을 아래에서 받침','네 접촉면과 손목 사이 간격이 동시에 보임']),
('R08','connected_loaf_small_fissure','작은 틈과 남은 빵 연결부',
 'Between the woman and baker, one round loaf has only a narrow central fissure exposing a small line of pale crumb. A broad intact strip of lower crust still joins its two sides, and both people support the still-connected loaf above the bakehouse table. The fissure and the unbroken crust bridge are visible together.',
 '여성과 제빵사 사이의 둥근 빵 하나에 좁은 중앙 틈만 나서 밝은 속살이 작은 선으로 드러난다. 아래 껍질의 넓고 온전한 띠가 아직 양쪽을 잇고, 두 인물은 여전히 연결된 빵을 제빵소 탁자 위에서 받친다. 틈과 끊기지 않은 껍질 연결부가 함께 보인다.',
 ['prop','relational_action','composition'],['material','action','composition'],
 ['woman','baker','single_loaf','small_fissure','pale_crumb','intact_lower_crust','table'],
 [['small_fissure','in','single_loaf'],['pale_crumb','visible_through','small_fissure'],['intact_lower_crust','connects','single_loaf'],['woman','supports','single_loaf'],['baker','supports','single_loaf']],
 '서로 떨어진 두 반쪽이나 큰 틈은 이 상태를 대신하지 않는다. 작은 틈의 모습이 시간상 최초·빵을 누가 찢었는지까지 입증하지 않는다.',
 ['좁은 틈의 속살과 넓은 남은 껍질 연결부가 함께 보임','빵 양쪽이 실제로 이어져 있음','빵 지지와 탁자 경계가 구별됨'])]
catalog=read(A/'photo_candidate_slot_catalog.json')['slot_catalog'];records={};bindings={};cards=[]
contract=('Optional complete authored estate visibility realization, not an historical or causal claim. Preserve every named actor, carrier, part, count, endpoint, state and connection together in the selected view. Respect the independently frozen requester meaning and actual allowed dimensions/properties. Neither a role nor a matching alias grants adoption permission. Whole-source adoption cannot evade source conditions by being called inspiration. partial_is_fail; UNOBSERVABLE_NOT_PASS. Research metadata creates no native facts or qualification. A still image cannot prove title, rights, identity, consent, motive, chronology or successful engineering performance.')
for rid,key,label,en,ko,slots,dimensions,components,relations,boundary,gates in rows:
 cid='cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'estate-visibility-repair-20261024/'+key).hex
 card={'id':rid,'label_ko':label,'kind':'authored_optional_visibility_variant','components':[{'id':x,'owner':x} for x in components],'relations':[{'subject':s,'type':rel,'object':ob} for s,rel,ob in relations],'visible_en':en,'visible_ko':ko,'confusion_boundary_ko':boundary,'pixel_gates_ko':gates,'support':'Observed prior pixel failure motivates this authored option. It does not establish that this option causes success.','native_approval':False,'historical_reconstruction_approved':False,'automatic_activation':False,'candidate_id':cid,'source_observations':'docs/research-evidence/photo-prompt/estate-management-20261024/integration-evidence/pixel-regression-observations.json','pixel_status':'NOT_RUN'}
 cards.append(card);records[cid]={'id':cid,'record_kind':'visual_option','content':{'en':en,'ko':ko,'definition':'Optional complete authored visibility realization: '+en,'aliases':[label,key.replace('_',' ')],'application_contract':contract,'research_semantics':card},'conditions':{},'effects':{'dimensions':dimensions,'properties':[]},'provenance':[{'source':'authored estate repair analysis 20261024#'+rid,'sha256':hashlib.sha256((en+'\n'+ko+'\n'+boundary).encode()).hexdigest()}]}
 for slot in slots:
  assert slot in catalog,slot
  bid='bind_'+uuid.uuid5(uuid.NAMESPACE_URL,cid+'/'+slot).hex
  bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':catalog[slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':2}
cm='photo_candidate_estate_visibility_repairs_20261024.json';bm='photo_candidate_estate_visibility_repair_bindings_20261024.json';sc='photo_estate_management_repair_semantics_20261024.json'
for name in (cm,bm,sc):assert not (A/name).exists(),name
candidate_schema=read(A/'photo_candidate_estate_management_20261024.json')['schema'];binding_schema=read(A/'photo_candidate_estate_management_bindings_20261024.json')['schema']
write(A/cm,{'schema':candidate_schema,'candidates':records});write(A/bm,{'schema':binding_schema,'slot_bindings':bindings});write(A/sc,{'schema':'estate-visibility-repair-semantics/v1','cards':cards,'comparison_baseline':'Original three outputs and all their failed gates remain unchanged.','qualification':'Bounded authored alternatives; actual exposure, use, pixels and user judgment require separate evidence.','native_approval':False})
mp=A/'photo_candidate_corpus_manifest.json';raw=mp.read_bytes();m=json.loads(raw);m['modules'] += [{'file':cm,'kind':'candidates'},{'file':bm,'kind':'slot_bindings'}];assert mp.read_bytes()==raw;write(mp,m)
write(O/'new-native-records.json',records);write(O/'new-bindings.json',bindings);write(O/'changed-native-records.json',{});write(O/'card-candidate-map.json',[{'card_id':c['id'],'candidate_id':c['candidate_id']} for c in cards]);write(O/'DATA-REPAIRS.json',{'new_optional_visual_sources':len(records),'optional_bindings':len(bindings),'original_sources_modified':0,'native_qualification':False,'modules':[cm,bm,sc],'purpose':'Concrete source/owner/contact/endpoint visibility alternatives after observed failure; no assumed image success.'})
print(json.dumps({'new_sources':len(records),'bindings':len(bindings),'old_estate_sources_changed':0}))
