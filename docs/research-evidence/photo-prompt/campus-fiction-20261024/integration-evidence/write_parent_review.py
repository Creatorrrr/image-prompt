"""Parent's direct original-pixel review; does not qualify source candidates."""
from pathlib import Path
from PIL import Image
import hashlib,json,datetime
R=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent
entries=[
 {'arm':'a','concept':'도예 공동 작업','image':R/'generated/photo-runs/campus-20261024-a/image-original.png','gates':[
  ('campus_place','visible','pass','CERAMICS II course timetable, critique sheet, kiln-layout board, repeated test pieces and shared workbench jointly support a university-style teaching-studio scene; no factual enrollment inferred.'),
  ('same_artifact_collaboration','visible','pass','Protagonist hand steadies the jug while a separately owned pair of hands holds the adjacent handled bowl on the same shelf.'),
  ('connected_plan','visible','pass','Third character has pencil-to-layout contact beside the same two-vessel arrangement and directs attention toward that work.'),
  ('ceramics_state','partial','fail','Pale unglazed vessels and removable shelf on a workbench are visible. The adjacent handle gap is too narrow/unclear to establish the requested clear finger-width spacing. Actual temperature/firing history cannot be proved from pixels.'),
  ('reference_appearance','visible','pass','Useful face scale, short dark bob, wispy fringe, eyes and facial proportions visibly resemble the supplied reference; real identity not established.'),
  ('whole_scene','partial','fail','Context and coordinated work are clear, but the promised spacing result is not fully assessable. Partial central result cannot pass the whole case.')],
  'overall':'FAIL_PARTIAL','strength':'학과 실습 공간, 세 인물의 공동 목표와 기록 행위가 읽힌다.','limit':'정확한 손잡이 간격의 해결 결과를 통과로 세지 않는다.'},
 {'arm':'b','concept':'천문 동아리 축제 부스','image':R/'generated/photo-runs/campus-20261024-b/original.png','gates':[
  ('b_campus_context','visible','pass','ASTRO CLUB header, CAMPUS FESTIVAL banner, courtyard/entrance and neighboring tables jointly locate a university festival booth.'),
  ('b_shared_preparation','visible','pass','Protagonist fingers meet the lens ring; a distinct peer visibly holds the screen corner. Separate bodies and target contacts are readable.'),
  ('b_optical_result','partial','fail','Housing, screen and star dots are visible, but the front lens faces toward the camera/foreground while the screen is behind the device. The required projector-to-screen direction is inconsistent; a star image alone cannot pass.'),
  ('b_reference_scope','visible','pass','The main face at usable scale, short dark bob and wispy fringe retain visible reference appearance without proving identity or age.')],
  'overall':'FAIL_PARTIAL','strength':'동아리 축제 부스와 서로 다른 준비 동작이 명확하다.','limit':'별무늬가 보이는 사실을 장치와 연결된 투사 결과의 증거로 바꾸지 않는다.'},
 {'arm':'c','concept':'졸업 가운 반납대','image':R/'generated/photo-runs/campus-20261024-c/campus-gown-return-original.png','gates':[
  ('C01_reference_appearance','visible','pass','Usable face scale, short dark bob, wispy fringe and facial proportions visibly retain the reference appearance.'),
  ('C02_university_setting','visible','pass','UNIVERSITY GOWN RETURN sign, return counter and rail of matching gowns are jointly visible.'),
  ('C03_graduation_components','visible','pass','The main subject wears an academic gown; square mortarboard and closed navy diploma cover are recognizable together.'),
  ('C04_end_of_ceremony_relation','visible','pass','The still-robed subject with both academic objects is adjacent to the counter; a recognizable empty wooden hanger and returned-gown rail occur in the same frame. One hanger end meets the image edge, but its empty state and counter relation remain visible.'),
  ('C05_embodiment','visible','pass','Both consequential hands visibly belong to the subject and support the cap/folder coherently. Standing body balance is plausible. Feet/floor contact is outside the frame and is not scored as observed; latest SKILL line 144 allows ordinary off-frame support when not central to the action.')],
  'overall':'PASS_SCENE_GATES','strength':'학사 의복·물품과 반납 장소의 관계가 한 프레임에 읽힌다.','limit':'실제 졸업 여부·시간적 전후 관계·원본 인물의 신원·보이지 않는 발 접점은 증명하지 않는다.'}
]
for e in entries:
 p=e['image'];im=Image.open(p);e['image']=str(p);e['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();e['actual_pixels']={'width':im.width,'height':im.height};e['gates']=[{'id':i,'observability':o,'status':s,'evidence':v} for i,o,s,v in e['gates']];e['passed_gates']=sum(g['status']=='pass' for g in e['gates']);e['total_gates']=len(e['gates']);e['campus_theme_visible']=True;e['source_candidate_adoption']=[];e['new_source_pixel_qualification']='NOT_ESTABLISHED';e['observed_model']=None;e['user_acceptance']='PENDING'
r={'status':'complete','reviewer':'parent direct review of original images','reviewed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'summary':{'images_generated':3,'image_calls':3,'scene_gate_pass_cases':1,'scene_gate_fail_partial_cases':2,'campus_theme_visible_cases':3,'new_CID_adoption_cases':0,'new_source_pixel_qualification_cases':0,'observed_model_verified_cases':0,'user_acceptance':'PENDING'},'rule':'Apply frozen scene gates and current skill; partial central contract fails. Do not invent a universal full-body/feet requirement or count ordinary off-frame support as visually proved. No before/after improvement or real-person identity claim.','arms':entries}
(O/'parent-pixel-review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r['summary']))
