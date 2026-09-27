"""Author research artifacts only; no runtime writes, API calls, or image generation."""
from __future__ import annotations
import copy
import csv
import hashlib
import json
import pathlib
import sys
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as cs
from visual_profile_contracts import compile_visual_profile

def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def digest_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

SOURCES = [
('S01','Canon: Shooting a balanced portrait','https://asia.canon/en/support/8200023500','2009-08-28','manufacturer_support','page_read','촬영 범위별로 얼굴·행동·환경이 차지하는 비중이 달라진다.','용어 사용의 한 사례이며 무릎 위·가슴 위의 모든 명칭을 국제 표준으로 고정하지 않는다.'),
('S02','Canon EOS R6 V: Portrait','https://cam.start.canon/en/C023/manual/html/UG-03_ShootingStill_0050.html',None,'manufacturer_manual','page_read','얼굴과 눈에 초점을 두고 주변을 단순화하며 연속 촬영으로 표정·자세 변화를 포착한다.','특정 기종 기능 설명을 모든 장비나 생성 이미지의 EXIF 증명으로 확장하지 않는다.'),
('S03','Nikon: Take Better Portraits','https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/take-better-portraits',None,'manufacturer_tutorial','page_read','어깨와 머리 방향을 분리하고 배경의 돌출 선과 복잡성을 점검한다.','원문의 신체를 날씬하게 만든다는 가치 판단은 채택하지 않는다.'),
('S04','Nikon: Quick Tips for Taking Better Portraits','https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits',None,'manufacturer_tutorial','page_read','중앙에서 벗어난 얼굴도 눈에 초점을 유지해야 한다.','눈 초점은 표정 전달 목표의 기준이며 눈 감은 사진이나 흐림을 요청한 사진을 부정하지 않는다.'),
('S05','Canon Canada / Nicole Ashley: Portrait tips','https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques',None,'photographer_interview','page_read','자세를 고정하기보다 머리·옷·발의 작은 동작을 관찰하고 배경을 보조 역할로 둔다.','행동이 자연스러워 보인다고 실제 성격·진심·촬영 경위를 증명하지 않는다.'),
('S06','Canon SNAPSHOT: Easy Pretty Portraits','https://snapshot.asia.canon/en/article/easy-pretty-portraits-3-quick-convenient-camera-techniques',None,'manufacturer_tutorial','search_excerpt_only_open_403','흐린 전경과 배경 사이에 피사체를 놓는 방식은 얼굴 방향으로 시선을 유도할 수 있다.','본문 열람이 403으로 제한되어 검색에 노출된 전경 흐림·가림 관련 설명만 사용한다.'),
('S07','Adobe: Negative space photography','https://www.adobe.com/creativecloud/photography/type/negative-space-photography.html',None,'photographer_tutorial','page_read','여백은 피사체와 주변의 관계이며 얕은 심도와 함께 사용할 수 있다.','자료의 여백 비율 조언을 모든 인물사진의 필수 수치로 채택하지 않는다.'),
('S08','Adobe: Over the shoulder shot','https://www.adobe.com/sg/creativecloud/video/production/cinematography/camera-shots-and-angles/over-the-shoulder-shot.html',None,'cinematography_tutorial','page_read','가까운 인물의 어깨·머리 일부 너머로 다른 인물을 보는 층화 구도이다.','영상 기법을 정지사진의 공간 관계에 한정해서 전용하며 장면 전환·역숏은 별도이다.'),
('S09','Adobe: Dutch angle shot','https://www.adobe.com/au/creativecloud/video/production/cinematography/camera-shots-and-angles/dutch-angle-shot.html',None,'cinematography_tutorial','page_read','카메라의 롤 회전으로 장면의 수평·수직 기준선이 기울어진다.','자료의 x축·candid angle 표기는 채택하지 않고 roll / canted angle로 기록한다. 긴장 연출은 제안이지 인물의 정신 상태 증명이 아니다.'),
('S10','Adobe: Candid photography','https://www.adobe.com/creativecloud/photography/type/candid-photography.html',None,'photographer_tutorial','page_read','포즈를 지시한 사진과 진행 중인 생활 사건을 관찰한 사진의 촬영 접근이 다르다.','카메라를 보지 않음만으로 비연출·무인지·동의를 판단하지 않는다.'),
('S11','Adobe / Sam Hurd: Prism photography','https://www.adobe.com/creativecloud/photography/technique/prism.html',None,'photographer_tutorial','page_read','프리즘은 굴절·반사·색 분산을 만들며 인물 촬영의 기본 구성을 먼저 확보한다.','가장자리만 쓰기와 얼굴 중심 보존은 이번 목적의 설계 제안이지 모든 프리즘 사진의 정의가 아니다.'),
('S12','Adobe: Reflection photography','https://www.adobe.com/nz/creativecloud/photography/discover/reflection-photography.html',None,'photographer_tutorial','page_read','물·유리·거울의 반사는 카메라 높이와 위치에 따라 포함 범위가 달라진다.','유리 투과와 평면거울 반사, 물 표면 반사를 하나의 프로필로 합치지 않는다.'),
('S13','OpenStax: Images formed by plane mirrors','https://openstax.org/books/university-physics-volume-3/pages/2-1-images-formed-by-plane-mirrors',None,'physics_textbook','page_read','평면거울의 가상상은 거울 뒤에 위치하며 거울에서 물체까지 거리와 상까지 거리가 같다.','거울 표면에 초점이 맞으면 반사된 얼굴도 자동으로 선명하다는 설명은 채택하지 않는다. 곡면·프리즘은 별도 광학이다.'),
('S14','Ward et al.: Nasal distortion in short-distance photographs','https://pubmed.ncbi.nlm.nih.gov/29494735/','2018-03-01','primary_research','pubmed_abstract_read_pmc_fulltext_unavailable','카메라 거리 변화가 얼굴의 원근 비례에 영향을 주는 수학 모델을 제시한다.','PubMed 초록은 확인했고 PMC 본문은 접근 확인 화면으로 제한되었다. 특정 왜곡 비율·미용 판단·진단은 사용하지 않는다.'),
('S15','Canon Creator Lab / Nina Collins: Creative portrait photography','https://www.canoncreatorlab.ca/insights/creative-portrait-photography/','2024-06-11','photographer_interview','page_read','생활 소품은 인물에게 구체적인 상호작용을 부여하고 작은 움직임으로 사진을 변주할 수 있다.','특정 소품·시대·인물 외형을 구도 계약의 의무로 만들지 않는다.'),
('S16','Westcott / Lindsay Adler: Environmental gobos','https://westcottu.com/creating-a-sense-of-environment-with-the-optical-spot-by-lindsay-adler','2021-08-16','photographer_demonstration','page_read','고보는 빛이 통과하는 패턴을 만들며 투사 패턴의 경계를 선명하거나 부드럽게 조절할 수 있다.','원인 장비가 화면 밖이면 특정 고보 장비의 실제 사용을 픽셀만으로 증명하지 않는다.'),
('S17','Adobe: Motion blur photography','https://www.adobe.com/creativecloud/photography/technique/motion-blur.html',None,'photographer_tutorial','page_read','노출 중 움직임과 셔터 시간이 궤적을 만들며 고정 카메라와 패닝은 다른 촬영 관계이다.','흐린 배경만으로 움직임 흐림·패닝·장노출을 판정하지 않는다.'),
('S18','National Galleries of Scotland: Contrapposto','https://www.nationalgalleries.org/art-and-artists/glossary-terms/contrapposto',None,'museum_glossary','page_read','한 다리에 하중을 싣는 자세와 골반·몸의 대응 관계를 설명한다.','일반 비대칭 자세 전부를 콘트라포스토로 하드 활성화하지 않는다.'),
('S19','Adobe: 2026 Creative Trends Forecast','https://business.adobe.com/resources/creative-trends-report.html',None,'industry_trend_report','page_read','2026 전망은 감각·연결·장난스러운 실험·지역성을 제시한다.','SNS 인물 구도별 인기 순위나 성과 측정 자료가 아니다.'),
('S20','Adobe: Connectioneering in the AI era','https://business.adobe.com/uk/blog/connectioneering-creative-trend-human-connection-ai-era','2026-09-16','industry_trend_commentary','page_read','일상 상호작용과 공유된 경험을 중심으로 한 시각 이야기 방향을 설명한다.','업계 자기 전망이며 사진의 진실성·보편적 호감·매출 효과를 보증하지 않는다.'),
('S21','Apple: Ultra Wide camera / macro guide','https://support.apple.com/en-sa/guide/iphone/iphfaacf2eb0/ios',None,'manufacturer_manual','page_read','지원 기종에서는 .5x를 선택해 Ultra Wide 카메라로 전환할 수 있다.','이 문서는 매크로 사용 설명이다. 0.5 셀피의 인기·필수 후면 촬영·모든 기종 지원을 뒷받침하지 않는다.'),
('S22','Julieanne Kost: Pairing diptychs and triptychs','https://jkost.com/blog/2015/06','2015-06-05','creator_tutorial','search_excerpt_only_open_406','색·형태·선·빛과 분위기를 이용해 여러 사진의 관계를 연결한다.','정지사진 한 장의 구도와 사진 간 배치·순서를 구분하며 검색에서 확인한 설명 범위를 넘지 않는다.'),
('S23','Vogue: What is in an Instagram photo dump?','https://www.vogue.com/article/instagram-photo-dump-generation-z','2022-12-01','cultural_commentary','page_read','포토덤프의 느슨한 외관도 선택·편집된 결과일 수 있다는 문화적 해설이다.','2022년 기사이며 2026년 인기 데이터로 사용하지 않는다.'),
('S24','Canon SNAPSHOT: Creative portraitures','https://snapshot.asia.canon/vn/en/article/3-creative-ways-to-shoot-portraitures','2021-02-24','manufacturer_tutorial','search_excerpt_only_open_403','반사·소품·선의 대비를 통한 인물 구도 사례를 소개한다.','검색에 표시된 2026년 업데이트 표기는 유행의 시작일·실험 검증일이 아니다.'),
('S25','Canon SNAPSHOT: Techniques from professional models','https://snapshot.asia.canon/en/article/3-flattering-techniques-to-learn-from-professional-models',None,'photographer_tutorial','search_excerpt_only_open_403','손을 얼굴 주변에 배치하는 포즈 사례를 소개한다.','작은 얼굴·매력의 보편적 이상은 채택하지 않는다. 손 프레이밍의 형상 기준은 자체 제안이다.'),
]
sources = [{'id':i,'title':t,'url':u,'published_or_updated_date':d,'source_type':k,'access_status':a,'supported_claim_ko':c,'limits_ko':l,'checked_on':'2026-09-27'} for i,t,u,d,k,a,c,l in SOURCES]

CONCEPTS = []
def add(i,ko,en,family,components,confounds,refs,reuse,plan,positive,negative,*,scope='single_image',tier='P1'):
    # Every component contains an independently owned observable relation.
    CONCEPTS.append({'id':i,'label_ko':ko,'terms_en':en.split(';'),'family':family,'scope':scope,
      'components':[{'id':f'c{j+1}','slot':s,'evidence_en':e,'owner':o,'dimensions':ds.split(',')} for j,(s,e,o,ds) in enumerate(components)],
      'confusion_boundaries_ko':confounds,'source_ids':refs.split(','),'existing_ids':reuse.split(',') if reuse else [],
      'integration_proposal':plan,'priority':tier,'positive_case_ko':positive,'negative_case_ko':negative,
      'authority':'research_proposal; requester meaning has precedence','factual_basis':'Sources support named photographic principles only; component conjunctions and gates are authored engineering proposals.'})

# The thirty compositions in the referenced conversation, kept one-to-one.
add('PC01','눈높이의 가까운 상반신','eye-level close portrait;head-and-shoulders portrait','face',[
 ('subject_framing','the frame includes the face and shoulders at a readable portrait scale','main subject','framing'),
 ('camera_height','the viewpoint meets the subject near the visible eye line','camera relative to main subject','camera'),
 ('focus','the visible eye and expression-bearing facial landmarks remain resolved','visible face','camera'),
 ('composition','a simpler surrounding field separates the face and shoulder contour','face and background','composition')],['얼굴만 확대했다고 눈높이가 증명되지는 않는다.','가슴 위 프레이밍과 정면 얼굴 방향은 별개다.'],'S01,S02,S04','head_and_shoulders_crop,eye_level_observer,eye_focus','reuse_atoms','얼굴과 어깨가 보이고 눈높이에서 촬영한 성인 인물','같은 크롭이지만 정수리를 크게 내려다보는 사진',tier='P0')
add('PC02','몸은 사선, 얼굴은 카메라 쪽','angled shoulders facing camera;three-quarter body angle','face',[
 ('body_orientation','the torso and shoulder plane turn obliquely to the camera','main torso','pose'),
 ('body_orientation','the head turns back toward the camera relative to the torso','head relative to torso','pose'),
 ('gaze_engagement','the visible eyes address the lens while the shoulders remain oblique','main eyes and lens','expression'),
 ('composition','neck and shoulder connections remain continuous through the turn','head neck and torso','body_geometry')],['three-quarter-length는 촬영 범위이다.','얼굴과 몸이 함께 측면으로 향하는 사진은 다르다.'],'S03,S04','three_quarter_body_turn,head_shoulder_opposition,direct_camera_aware','new_joint_relation','어깨는 비스듬하지만 머리와 눈은 렌즈를 향한 성인','무릎 위로 찍었을 뿐 얼굴과 어깨가 모두 정면',tier='P0')
add('PC03','맞은편 테이블 구도','across-the-table portrait;table companion perspective','face',[
 ('composition','a near table edge separates the camera position from the seated subject','table and camera and seated subject','composition'),
 ('subject_framing','the subject face remains above the near table plane at readable scale','main face and table','framing'),
 ('hand_pose','the subject hands rest or act on the visible tabletop with plausible contact','subject hands and table','pose,action'),
 ('composition','table objects occupy supporting regions around the primary face','table objects and face','composition')],['카페 배경만 있거나 탑다운 음식 사진인 경우','실제 연애 관계·친밀한 성격의 증거로 사용'],'S01,S05,S15','companion_viewpoint_everyday_candid,hand_on_table_edge','new_joint_relation','맞은편 좌석에서 컵 옆 손과 얼굴을 함께 담은 성인','높은 탑다운 시점에서 음식이 중심이고 얼굴은 프레임 밖',tier='P0')
add('PC04','가까운 동행자의 시점','companion perspective;close handheld portrait','face',[
 ('camera_direction','the view occupies a plausible nearby companion position beside a daily activity','camera and daily activity','camera'),
 ('action','one concrete hand activity remains legible in the near setting','subject hand and activity object','action'),
 ('gaze_engagement','one glance or gesture addresses the nearby camera holder','subject response and camera holder','expression,action'),
 ('composition','the face stays readable within the nearby environmental frame','main face and environment','composition,framing')],['셀피와 카메라 밖 동행자 촬영은 다르다.','소품 없는 인플루언서 포즈만으로 생활 행동을 증명하지 않는다.'],'S05,S10','companion_viewpoint_everyday_candid,off_camera_companion_everyday_capture','reuse_scoped_profile','동행자 좌석에서 일상 동작과 렌즈 쪽 짧은 반응을 담은 성인','팔 길이 전면카메라 셀피',tier='P0')
add('PC05','어깨 너머로 돌아보기','looking back over the shoulder;over-the-shoulder glance','face',[
 ('body_orientation','the main subject torso faces partly away from the camera','main torso','pose'),
 ('body_orientation','the same subject head turns back across the near shoulder','main head and own shoulder','pose'),
 ('composition','the turned face remains readable beyond its own near shoulder','main face and own shoulder','composition'),
 ('body_pose','the head neck and torso retain a plausible connected turning range','main body chain','body_geometry')],['타인의 어깨 너머로 찍는 OTS와 혼동','몸 전체를 카메라 쪽으로 돌린 정면 사진'],'S03','turning_back_over_shoulder_pose,looking_back_over_shoulder_orientation','extend_existing_atoms','등이 일부 보이고 본인의 어깨 너머로 돌아보는 성인','다른 사람의 어깨만 전경에 있고 주인공은 정면')
add('PC06','옆얼굴과 시선 앞 여백','profile with looking room;side-profile portrait','face',[
 ('body_orientation','the visible nose lip and chin form a readable side-face contour','main face','pose'),
 ('gaze_target','the visible eye and head establish one sideward direction','visible eye and head','expression'),
 ('composition','usable open space extends ahead of the stated gaze direction','gaze vector and image field','composition'),
 ('subject_framing','the profile landmarks remain large enough to inspect in the final frame','profile face','framing')],['여백이 시선 뒤에 있으면 looking room과 다르다.','옆을 보는 눈과 완전 옆얼굴은 별개다.'],'S01,S07','mep_casting_profile,look_motion_room_direction_relation','reuse_scoped_profile','옆얼굴이 화면 오른쪽을 보며 그 앞에 넓은 공간이 남음','옆얼굴 앞은 잘리고 뒷머리 뒤쪽에만 여백이 있음')
add('PC07','무릎 위의 약한 로우앵글','knee-up subtle low angle;three-quarter-length portrait','body',[
 ('subject_framing','the frame runs from the head to the explicitly chosen region above the knees','main body and crop edges','framing'),
 ('camera_height','the viewpoint lies modestly below the face with upward spatial cues','camera and main face','camera'),
 ('body_pose','the torso and legs retain coherent near-to-far proportions','main torso and legs','body_geometry'),
 ('composition','the face remains a readable focal region within the larger body frame','main face and body','composition')],['극단적인 지면 시점·벌레 시점은 약한 로우앵글이 아니다.','3/4 얼굴 방향과 knee-up은 별도 축이다.'],'S01,S05,S14','knee_up_framing','extend_existing_atoms','무릎 조금 위에서 잘리고 약하게 올려다보는 성인 인물','지면에서 신발이 크게 돌출되고 얼굴이 아주 작음')
add('PC08','한쪽 다리에 무게를 둔 비대칭 전신','weight-shift pose;asymmetrical standing pose','body',[
 ('subject_framing','the full frame preserves the head and both feet','main body','framing'),
 ('body_pose','one support leg carries the stance while the other remains relatively relaxed','main support and free leg','pose'),
 ('body_orientation','shoulder and pelvis alignment vary with the visible weight shift','shoulders and pelvis','pose'),
 ('contact_point','the supporting foot establishes a plausible ground contact path','support foot and ground','body_geometry')],['S커브·골반 과장·비대칭 의상만으로 하중 분담을 증명하지 않는다.','일반 웨이트 시프트를 고전 콘트라포스토와 동일시하지 않는다.'],'S18','relaxed_standing_weight_shift,contrapposto_full_body,mep_poised_support','reuse_scoped_profile','한 발이 지지하고 반대 무릎이 이완된 전신 성인','양발 지지는 같고 의상만 비대칭')
add('PC09','앉아서 만드는 삼각형','seated triangular composition;triangular pose grouping','body',[
 ('body_pose','the subject sits on a visible supporting surface','subject and seat','pose'),
 ('composition','the face elbow and knee define three separated triangle vertices','face elbow and knee','composition'),
 ('body_pose','the visible arm and leg joints connect plausibly between those vertices','subject limb joints','body_geometry'),
 ('subject_framing','the frame preserves all three nominated vertices and their spacing','nominated body regions','framing')],['삼각 무늬나 세 인물의 배치가 대체하지 않는다.','신체 내부 여백의 삼각형과 세 점의 배치는 다르다.'],'S05,S18','mep_graphic_pose,body_bounded_negative_space','new_joint_relation','앉은 성인의 얼굴·팔꿈치·세운 무릎 세 점이 삼각 배치','팔과 허리 사이만 삼각형이고 무릎은 잘림')
add('PC10','몸이 가로지르는 대각선','diagonal reclining portrait;diagonal body axis','body',[
 ('body_pose','a seat sofa or wall visibly supports the reclining torso','torso and support','pose'),
 ('composition','the shoulder-to-pelvis body axis crosses the image diagonally','main torso axis','composition'),
 ('camera_direction','stable environmental reference lines retain the intended level camera roll','camera and environmental lines','camera'),
 ('composition','the face remains readable near one end of the diagonal body path','main face and body axis','composition')],['더치 앵글은 몸이 아니라 카메라 회전이다.','지지 없이 공중에 누운 형상은 실패한다.'],'S01,S09','propped_elbow_recline_support','new_joint_relation','소파에 지지된 몸만 대각선이고 창틀은 수직인 성인','몸은 수직인데 카메라 전체가 기울어짐')
add('PC11','앉은 인물을 위에서 가까이 보기','high-angle seated portrait;close elevated observer','body',[
 ('body_pose','the subject is visibly seated on a supporting surface','subject and seat','pose'),
 ('camera_height','the camera looks downward from a nearby position above the seated face','camera and seated face','camera'),
 ('gaze_engagement','the raised face or visible eye direction connects toward that camera','main face and elevated lens','expression'),
 ('composition','head torso and near limbs follow one coherent downward perspective','subject body and camera','composition')],['가까운 고각과 수직 탑다운·드론은 다르다.','앉았다는 이유로 자동 overhead 프로필을 강제하지 않는다.'],'S05,S14','overhead_social_snapshot_relation,floor_high_angle_direction','extend_existing_atoms','의자에 앉아 고개를 들어 가까운 위쪽 카메라를 보는 성인','드론 거리의 작은 인물이 바닥만 바라봄')
add('PC12','팔과 손으로 얼굴 주위 공간 만들기','arm framing;hands framing the face','body',[
 ('hand_pose','the subject own arm or hand arcs around the face perimeter','subject own hand and face','pose'),
 ('composition','the face lies within a readable opening formed by that arm or hand','face and body-made opening','composition'),
 ('body_pose','the wrist elbow and shoulder connect plausibly through the framing gesture','main arm joint chain','body_geometry'),
 ('focus','the requested expression-bearing facial region remains readable through the opening','main face','camera')],['눈을 막는 손과 얼굴 주변의 프레이밍은 별개다.','화면 밖 타인의 손을 주인공의 손으로 혼동하지 않는다.'],'S25,S05','arms_raised_overhead,mep_graphic_pose,body_bounded_negative_space','new_joint_relation','자기 팔이 얼굴 둘레에 아치를 만들고 눈은 열린 공간에 있음','두 손바닥이 눈과 표정을 완전히 덮음')
add('PC13','포즈 사이의 순간','in-between moment;mid-gesture portrait','event',[
 ('action','one nominated body or hand action remains visibly underway','main subject and action','action'),
 ('motion','a displaced limb hair group or cloth edge indicates the unfinished phase','main action-bearing region','timing'),
 ('body_pose','the rest of the stance supports the same action phase','main body support','pose'),
 ('composition','the facial reaction remains legible beside the incomplete gesture','face and action','composition')],['고정된 옆시선만으로 중간 순간을 증명하지 않는다.','실제 비연출·진심·성격을 픽셀에서 확정하지 않는다.'],'S05,S10','mep_in_between,camera_acknowledged_observer_frame','reuse_scoped_profile','옷깃을 고쳐 잡는 중 손과 옷 가장자리가 이동한 성인','옆을 본 정지 포즈에 candid라는 이름만 붙음')
add('PC14','비스듬히 걸어 들어오기','walking portrait;diagonal movement','event',[
 ('action','one subject step establishes a readable walking phase','main walker','action,timing'),
 ('composition','the walking path runs obliquely across the image plane','walker path and frame','composition'),
 ('body_pose','feet support and fabric displacement agree with the same step','main feet and attached cloth','pose'),
 ('subject_framing','the moving face remains readable within the chosen mid-distance frame','main face','framing')],['기울어진 카메라가 보행 방향을 대체하지 않는다.','걷는 포즈·실제 이동 궤적·장노출은 별개다.'],'S05,S17','mep_garment_movement,stepping_into_frame_pose','extend_existing_atoms','성인 인물이 화면을 사선으로 지나며 한 걸음의 지지가 보임','양발 정지인데 난간만 사선')
add('PC15','활동 중심 환경 인물','environmental portrait;activity-based portrait','event',[
 ('action','the subject contacts or attends to one task-relevant scene element','subject and task element','action'),
 ('composition','a contextual fixture explains where the activity takes place','task and contextual fixture','composition'),
 ('subject_framing','the frame retains the face and task-bearing hand action together','main face and hands','framing'),
 ('composition','the environment supports the activity while the subject remains readable','main subject and environment','composition')],['공간만 넓고 행동이 없는 원경과 다르다.','도구 소유만으로 취향·직업·숙련을 확정하지 않는다.'],'S05,S15','pr_environmental_portrait_subject_place,mep_environment_relation','reuse_scoped_profile','작업대에서 손의 작업과 얼굴·관련 도구가 같은 화면에 있음','풍경 속 아주 작은 인물에게 직업 라벨만 부여',tier='P0')
add('PC16','카메라 쪽으로 건네기','offering gesture;reaching toward camera','event',[
 ('hand_pose','the subject attached hand extends toward the camera position','subject hand and camera','pose,action'),
 ('contact_point','the offered object follows the visible subject hand contact','subject hand and offered object','action'),
 ('composition','the offered hand or object occupies a nearer plane than the face','near object and main face','composition'),
 ('composition','the near object leaves the requested facial expression region readable','offered object and main face','composition')],['카메라를 잡은 셀피 팔과 구분한다.','프레임 밖 관객의 손을 주인공의 팔로 연결하지 않는다.'],'S15','reaching_toward_camera,hands_foreground_face_behind','new_joint_relation','자기 팔로 작은 물건을 렌즈 쪽에 내밀고 뒤 얼굴이 보이는 성인','누구의 손인지 불명확하거나 물건이 얼굴 전체를 덮음',tier='P0')
add('PC17','타인의 어깨 너머 주인공','over-the-shoulder shot;OTS portrait','event',[
 ('partner_framing','another person shoulder forms a partial near-plane silhouette','secondary companion shoulder','relationship,composition'),
 ('composition','the camera observes the main face beyond that secondary shoulder','camera secondary shoulder and main face','camera,composition'),
 ('gaze_target','the main response relates to the companion position indicated by the near shoulder','main response and secondary companion','expression,relationship'),
 ('focus','the main face receives the requested focus priority over the foreground shoulder','main face and secondary shoulder','camera')],['주인공 자신의 돌아보는 어깨가 아니다.','어깨가 아니라 의자·소품 전경인 경우는 별도이다.'],'S08','over_partner_shoulder_subject_face,over_the_shoulder_dialogue','new_joint_relation','화면 왼쪽 타인의 흐린 어깨 너머로 성인 주인공 얼굴이 선명','주인공이 본인 어깨 너머로 돌아보기만 함',tier='P0')
add('PC18','타인의 손만 보이는 상호작용','cropped companion interaction;companion hands-only portrait','event',[
 ('partner_framing','a secondary person hand enters from a traceable frame edge','secondary companion hand','relationship,framing'),
 ('contact_point','that hand contacts or transfers the specified garment or small object','secondary hand and nominated target','action'),
 ('action','the main subject reaction relates to the same visible contact or transfer','main subject and companion contact','action,expression'),
 ('composition','the secondary hand stays subordinate while the main face remains readable','secondary hand and main face','composition')],['떠 있는 손·주인공의 세 번째 팔·자기 옷깃 조정과 구분한다.','손만 등장했다고 연인·친구·동의를 추론하지 않는다.'],'S08,S15','mep_fitting_adjustment','new_joint_relation','가장자리에서 들어온 타인 손이 옷깃을 정리하고 성인 주인공이 반응','주인공 자신의 손이 옷깃을 만짐')
add('PC19','흐릿한 전경 사이 얼굴','foreground framing;foreground bokeh portrait','optical',[
 ('composition','a scene-owned near object occupies a peripheral foreground region','near object and frame edge','composition'),
 ('focus','that near object remains softer than the resolved main face','near object and main face','camera'),
 ('composition','a clear opening through the foreground reveals the intended face region','foreground opening and main face','composition'),
 ('composition','overlap and softness separate foreground subject and farther setting','three scene planes','composition')],['배경 보케만 있는 사진·디지털 비네팅과 구분한다.','부드러움이 눈·표정을 덮으면 목적에 실패한다.'],'S06,S04','botanical_editorial_portrait_context,rb_foreground_occlusion','new_joint_relation','흐린 전경 잎이 양쪽 가장자리에 있고 성인 얼굴은 빈 틈에서 선명','얼굴은 선명하지만 보케가 배경에만 있음',tier='P0')
add('PC20','문·창문 속 인물','frame within a frame;doorway portrait','optical',[
 ('composition','a physical scene boundary forms an opening around the primary subject','scene opening and main subject','composition'),
 ('composition','readable boundary thickness or overlap establishes a near plane','opening boundary','composition'),
 ('subject_framing','the main face stays readable inside the opening','main face and opening','framing'),
 ('composition','the intended opening enclosure is preserved within the final crop','opening edges and frame','composition')],['디지털 테두리·비네팅·배경에 그린 아치와 구분한다.','기존 hard 프로필은 최소 세 면의 경계를 요구하므로 한쪽 창틀만 요청하면 강제하지 않는다.'],'S01,S06','frame_within_frame_boundary_relation,architectural_threshold_frame_depth_relation','reuse_scoped_profile','실제 문틀의 세 면과 깊이가 성인 얼굴 주변을 감싸는 사진','사진 파일에 테두리만 추가')
add('PC21','유리 너머 얼굴과 도시 반사','through-glass portrait;window reflection portrait','optical',[
 ('composition','a visible pane edge or frame locates the glass plane between camera and subject','glass plane','composition'),
 ('composition','the subject face is seen through the pane in the transmitted scene','transmitted main face','composition'),
 ('reflection_logic','a restrained exterior reflection overlays a distinct region of the pane','reflected exterior scene and glass','composition'),
 ('focus','the transmitted expression-bearing face remains readable through the layered pane','transmitted face and reflection','camera')],['평면거울 속 얼굴·이중노출·비닐 필름 흐림과 구분한다.','창문 반사만으로 도시 위치·특정 장소를 확정하지 않는다.'],'S12,S13','rb_glass_reflection_transmission,pr_reflection_scene_binding_candidate','new_joint_relation','창틀 너머 성인 얼굴과 약한 거리 반사가 분리돼 읽힘','불투명 거울에 얼굴 하나만 반사됨',tier='P0')
add('PC22','거울 속 얼굴이 주인공','mirror-led portrait;reflected face as main subject','optical',[
 ('reflection_logic','a physical mirror boundary contains a reflected face in one coherent view','mirror and reflected face','composition'),
 ('composition','the reflected face receives the primary visual emphasis','reflected main face','composition'),
 ('body_orientation','a partial direct body view corresponds plausibly to that reflection','direct body and reflected body','pose,composition'),
 ('focus','the reflected eye or expression region remains resolved within the visible mirror boundary','reflected face','camera')],['거울 셀피는 휴대폰의 주체·접촉·반사까지 요구하는 다른 계약이다.','유령·지연 반사·이중 자아 라우트가 섞이면 실패한다.'],'S12,S13','faithful_reflection,pr_reflection_scene_binding_candidate','new_joint_relation','실제 뒷어깨와 거울 속 성인 얼굴이 같은 순간에 대응함','거울 테두리만 선명하고 반사 얼굴은 흐림',tier='P0')
add('PC23','작은 손거울 안의 얼굴','handheld mirror portrait;selective face reflection','optical',[
 ('contact_point','a visible hand supports one small mirror at plausible contact points','hand and small mirror','action'),
 ('reflection_logic','the mirror boundary encloses the selected reflected face region','small mirror and reflected face','composition'),
 ('composition','the reflected expression remains readable at the mirror image scale','reflected face and image scale','framing'),
 ('focus','the reflected face and direct surroundings retain a coherent focus hierarchy','reflected face and direct scene','camera')],['손거울이 보여도 얼굴 반사가 없으면 실패한다.','눈 한 조각만 요청한 경우 표정 전체를 요구하지 않는다.'],'S12,S13,S15','','new_joint_relation','손이 잡은 작은 거울 안에 표정이 읽히는 성인 얼굴이 담김','손거울 밖 직접 얼굴만 보이고 거울 안은 하늘',tier='P0')
add('PC24','가장자리 프리즘·굴절','edge refraction portrait;prism edge effect','optical',[
 ('lens_artifact','a localized peripheral region shows refracted displacement or spectral separation','peripheral optical effect','camera'),
 ('composition','the optical effect remains near a chosen image edge','optical region and frame','composition'),
 ('focus','the central requested facial features remain coherent and resolved','central main face','camera'),
 ('composition','the shifted edge detail remains connected to the same scene or light source','edge effect and scene owner','composition')],['얼굴 전체 분해·무지개 조명만 있는 사진·원인 없는 복제와 구분한다.','굴절 결과는 관찰 가능하지만 실제 프리즘 장비 사용은 메타데이터이다.'],'S11','','new_joint_relation','한쪽 가장자리만 굴절되고 성인 얼굴 중심은 선명','얼굴 전부가 여러 조각으로 반복됨')
add('PC25','가장자리 타이트 크롭','off-center close-up;tight face crop','graphic',[
 ('subject_framing','the face occupies a close portrait scale near one image edge','main face and crop edge','framing'),
 ('composition','the face focal point lies visibly away from the geometric center','main face and frame center','composition'),
 ('focus','the explicitly requested eye and expression region remains resolved','main face','camera'),
 ('subject_framing','the crop preserves the requested diagnostic facial region','nominated facial region','framing')],['의도적 두상 크롭과 요청한 눈·입을 잘라버린 크롭은 다르다.','프로필·눈 감음 요청에 양쪽 눈 가시성을 일괄 적용하지 않는다.'],'S01,S04','pr_casual_crop_subject_legibility,beauty_tight_face_crop','reuse_scoped_profile','머리 위는 일부 잘리지만 성인 눈과 입이 읽히며 중심에서 벗어남','요청한 눈이 화면 밖으로 잘림')
add('PC26','여백을 바라보는 인물','negative-space portrait;looking room','graphic',[
 ('gaze_target','one visible head or gaze vector points toward a nominated side','main head and gaze','expression'),
 ('composition','a contiguous low-detail field extends ahead of that vector','gaze and open field','composition'),
 ('subject_framing','the subject facial signal remains readable at the final display size','main face','framing'),
 ('composition','the subject outline separates from the simple field','subject contour and field','composition')],['negative space·headroom·look room·move room은 서로 다른 측정이다.','시선 앞 공간이 있어도 복잡한 간판으로 가득하면 저정보 여백과 다르다.'],'S07','look_motion_room_direction_relation,subject_field_negative_space_relation','reuse_scoped_profile','성인이 향한 쪽에 단순한 벽 여백이 있고 얼굴이 읽힘','뒷머리 뒤쪽에만 여백',tier='P0')
add('PC27','대칭 공간 속 비대칭 인물','symmetrical setting asymmetrical pose;axial portrait contrast','graphic',[
 ('composition','architectural pairs form a readable symmetry axis in the scene','architecture axis and paired elements','composition'),
 ('body_pose','the main subject limb or head arrangement departs visibly from that symmetry','main subject pose','pose'),
 ('composition','the two spatial roles remain simultaneously readable in one frame','architecture and pose','composition'),
 ('composition','the face retains focal priority within the paired architecture','main face and architecture','composition')],['단순 중앙 배치는 배경 대칭을 증명하지 않는다.','인물까지 좌우 완전 복제인 경우는 다른 구도이다.'],'S01,S05','centered_symmetric,mep_graphic_pose','new_joint_relation','대칭 복도 중앙에서 성인 한쪽 팔과 고개만 비대칭','비대칭 배경에서 인물만 중앙에 둠')
add('PC28','빛·그림자의 면 분할','graphic shadows;gobo portrait;shadow framing','graphic',[
 ('lighting','a coherent patterned light and shadow region crosses a visible scene surface','light pattern and receiving surface','lighting'),
 ('light_shape','the pattern defines graphic areas distinct from permanent material markings','light pattern and surface material','lighting'),
 ('composition','the pattern boundary organizes the image around the main face','pattern and main face','composition'),
 ('focus','the requested facial expression survives the patterned illumination','main face','camera')],['의복 프린트·피부 무늬·벽지와 광원 패턴을 혼동하지 않는다.','프레임 밖 광원인 경우 장비 사용 증명보다 패턴 결과만 판정한다.'],'S16','','optional_relation_candidate','벽과 어깨에 창 그림자가 이어지고 성인 표정은 읽힘','얼굴의 무늬가 조명과 무관한 타투')
add('PC29','정지 인물과 움직이는 주변','still subject motion contrast;sharp stationary portrait with trails','graphic',[
 ('body_pose','the primary subject keeps a readable stationary support and pose','main subject and support','pose'),
 ('focus','the requested facial region remains comparatively resolved','main face','camera'),
 ('motion','a separate moving peripheral element leaves a directional exposure trail','moving peripheral element','timing,camera'),
 ('composition','the trail and sharp subject occupy coherently related scene planes','trail owner and main subject','composition')],['보케 원·얕은 심도·렌즈 흔들림만으로 모션 궤적을 증명하지 않는다.','주인공을 추적하는 패닝과 정지 인물 대비는 다른 계약이다.'],'S17','panning_subject_tracking_motion_relation,rear_curtain_flash_motion_trace','new_joint_relation','선명한 정지 성인 옆으로 이동하는 빛이 방향 궤적을 남김','배경은 흐리지만 모든 빛 점이 동그란 보케',tier='P0')
add('PC30','프레임을 기울이기','Dutch angle;Dutch tilt;canted angle;camera roll','graphic',[
 ('camera_direction','the camera roll rotates a stable scene reference relative to the image axes','camera and reference lines','camera'),
 ('composition','multiple normally level scene lines share a coherent tilt direction','scene reference lines','composition'),
 ('body_pose','the subject stance remains plausible in the tilted scene coordinates','main support and tilted scene','pose'),
 ('subject_framing','the nominated facial region remains readable after the rotated crop','main face and crop','framing')],['몸 자체 대각선·경사진 지면·우연히 비스듬한 물체와 구분한다.','더치 앵글을 캔디드 촬영의 동의어로 사용하지 않는다.'],'S09','dutch_tilt_direction,dutch_angle_tension','new_joint_relation','창틀과 수평 난간이 함께 기울어진 프레임의 성인 인물','창틀은 수직인데 인물 몸만 기대어 사선')

# Additional reusable primitives needed to encode the original compositions.
add('PX01','촬영 범위와 얼굴 방향의 분리','shot scale versus facial orientation;three-quarter ambiguity','primitive',[
 ('subject_framing','the crop endpoint explicitly describes the included body extent','main crop','framing'),
 ('body_orientation','the facial direction is specified independently of that crop endpoint','main face','pose'),
 ('composition','the visible result simultaneously preserves the two requested axes','crop and facial direction','composition')],['three-quarter 단독 표현은 길이인지 방향인지 불명확하다.','새 후보가 원래 요청의 모호성을 사후에 대신 해석하지 않는다.'],'S01,S03','knee_up_framing,restrained_three_quarter_face_depth_read','reuse_atoms','무릎 위 프레이밍이며 얼굴은 비스듬히 보임','3/4라는 단어만으로 얼굴·몸 방향을 모두 고정',tier='P0')
add('PX02','머리 위 여백','headroom;top frame clearance','primitive',[
 ('composition','a nominated top margin separates the head contour from the upper frame edge','head contour and top frame','composition'),
 ('subject_framing','the same frame preserves the requested facial region and shot scale','face and crop','framing'),
 ('composition','the top margin remains independent of lateral gaze space','top margin and lateral field','composition')],['headroom은 시선 앞 여백이 아니다.','타이트 크롭 요청이면 머리 위 여백을 강제하지 않는다.'],'S01','head_and_shoulders_crop','optional_relation_candidate','머리 위 공간은 작고 시선 앞 공간은 넓음','머리 위 여백을 주기 위해 요청한 상반신 범위를 원경으로 바꿈')
add('PX03','주인공의 첫 읽기 위계','subject visual hierarchy;face priority','primitive',[
 ('composition','the intended face is separable from competing bright or high-detail regions','main face and distractors','composition'),
 ('focus','the intended facial signal resolves at the nominated output display size','main face','camera'),
 ('composition','supporting props preserve their role relative to the main face','props and main face','composition')],['호감·매력 점수와 가시성은 다른 지표다.','도구가 주인공인 제품 사진에 얼굴 우선 원칙을 강제하지 않는다.'],'S04,S05','face_hands_prop_visibility_budget','reuse_atoms','작은 썸네일에서도 성인 얼굴이 읽히고 밝은 소품이 가리지 않음','얼굴은 네이티브 확대에서만 보이고 간판이 화면을 지배',tier='P0')
add('PX04','초점의 소유자','focus ownership;visible eye focus','primitive',[
 ('focus','the nominated direct or reflected facial region receives the focus priority','nominated face surface','camera'),
 ('composition','the foreground and background softness agree with that selected owner','scene planes and focus owner','composition'),
 ('subject_framing','the focused feature is large enough for the intended review scale','focused feature','framing')],['거울 테두리의 선명함은 반사된 눈의 선명함이 아니다.','포커스 스태킹·스플릿 디옵터는 단일 초점 이행과 다른 선택이다.'],'S04,S13','eye_focus,shallow_depth_focus_falloff_relation','reuse_scoped_profile','거울 테두리는 부드럽고 안의 성인 눈이 선명','거울 테두리만 날카롭고 반사된 얼굴이 흐림',tier='P0')
add('PX05','가림의 소유자와 범위','occlusion owner;partial occlusion','primitive',[
 ('composition','the nominated occluder has a traceable scene or body owner','occluder owner','composition'),
 ('composition','the occluder overlaps only the requested image region','occluder and target region','composition'),
 ('composition','the requested surviving facial or action evidence remains exposed','surviving diagnostic region','composition')],['친밀감·몰래 촬영·얼굴 숨김을 같은 상태로 합치지 않는다.','전체 얼굴 노출보다 특정 남길 영역을 요청 기준으로 쓴다.'],'S06,S08','rb_foreground_occlusion,intentional_face_occluded_mood_portrait','reuse_scoped_profile','커튼이 한쪽 어깨만 가리고 표정은 보이는 성인','커튼이 요청한 눈까지 막음',tier='P0')
add('PX06','손의 소유자와 접촉','hand ownership;contact continuity','primitive',[
 ('contact_point','each visible hand connects to a plausible subject or entering frame-edge owner','hand and owner','body_geometry'),
 ('contact_point','the nominated hand contacts the object at a traceable grip or support point','hand and object','action'),
 ('composition','the contact remains visible at the required final review scale','contact region','composition')],['새 팔 생성·떠 있는 소품·손가락 수만 맞는 경우','피사체 수 한 명과 타인 손의 존재는 충돌할 수 있으므로 count와 relationship에 요청 근거 필요'],'S15','pr_object_contact_shadow_support','reuse_scoped_profile','자기 팔이 이어진 손으로 손거울 테두리를 지지함','손은 보이지만 팔·가장자리 소유자가 없고 거울이 떠 있음',tier='P0')
add('PX07','얼굴 비례와 카메라 거리','camera-distance perspective;near-field facial perspective','primitive',[
 ('camera_direction','the camera viewpoint defines a coherent near-to-far relation across the face','camera and face depth','camera'),
 ('composition','near facial or hand regions change scale coherently with the chosen distance','near and farther facial regions','composition'),
 ('subject_framing','the intended crop is preserved independently of the perspective choice','crop and camera position','framing')],['초점거리 숫자만으로 원근 비례를 증명하지 않는다.','초광각 셀피 요청을 무조건 자연 비례 사진으로 치환하지 않는다.'],'S14','wide_angle_near_field_perspective,distortion_controlled_portrait_perspective','reuse_scoped_profile','같은 크롭이라도 가까운 시점의 코·손과 먼 시점의 비례를 구분','24mm 라벨만 있고 원근 단서가 없음',tier='P0')
add('PX08','몸 대각선과 카메라 롤의 분리','body diagonal versus camera roll;diagonal versus canted','primitive',[
 ('composition','the body axis is measured against the image frame','main body axis','composition'),
 ('camera_direction','camera roll is evaluated through independent stable scene lines','camera and scene lines','camera'),
 ('composition','the two angle relations remain independently describable in the same image','body and scene angle axes','composition')],['자세 변경을 카메라 변경으로 교정하지 않는다.','배경 기준선이 없으면 카메라 롤 판정은 unscorable이다.'],'S01,S09','','optional_relation_candidate','소파의 성인 몸은 대각선이고 창틀은 수직','인물만 사선인데 Dutch angle이라고 판정',tier='P0')
add('PX09','배경 선과 윤곽의 접선 분리','background tangency;contour separation','primitive',[
 ('composition','the nominated background line remains separable from the subject contour','background line and subject contour','composition'),
 ('composition','the hair and shoulder edges retain a readable depth boundary','hair shoulders and background','composition'),
 ('subject_framing','the separation survives the final crop and display size','subject contour in final crop','framing')],['인물 머리에서 자라는 전봇대·어깨에 붙은 난간','모든 겹침을 금지하는 규칙으로 확장하지 않는다.'],'S03,S05','','optional_relation_candidate','머리 옆 간판 지지대가 떨어져 보임','지지대가 정수리 윤곽과 이어짐')
add('PX10','팔·몸 사이 여백의 형상','body-bounded negative space;arm-torso aperture','primitive',[
 ('body_pose','connected body contours bound one readable opening','main body contours','pose'),
 ('composition','the opening contains continuous scene background','body opening and background','composition'),
 ('subject_framing','all nominated contour boundaries remain visible in the crop','opening boundary','framing')],['앉은 삼각형의 세 점 배치와 다르다.','의상 무늬·배경 삼각형이 대체하지 않는다.'],'S18','body_bounded_negative_space,mep_graphic_pose','reuse_scoped_profile','굽힌 팔과 허리 사이에 배경이 보이는 삼각 틈','셔츠에 그려진 삼각형')
add('PX11','얼굴로 수렴하는 장면 선','leading lines to face;scene-owned directional line','primitive',[
 ('composition','a scene-owned line has a traceable beginning and continuation','scene line','composition'),
 ('composition','its visible direction leads toward the nominated subject region','scene line and target face','composition'),
 ('composition','the line remains subordinate to the target facial signal','line and face hierarchy','composition')],['사선이라는 이유만으로 유도선이 되지 않는다.','얼굴을 가로지르는 강한 선은 집중을 분산할 수 있다.'],'S03,S01','','optional_relation_candidate','테이블 가장자리와 난간이 성인 얼굴 근처로 이어짐','강한 선이 얼굴 반대쪽 화면 밖으로 흐름')
add('PX12','원본 구도와 게시 크롭','output crop preservation;display-scale portrait','primitive',[
 ('subject_framing','the nominated facial and action regions remain inside the declared output crop','face action and output crop','framing,format'),
 ('composition','the selected optical or framing device remains visible after that crop','selected device and crop','composition'),
 ('focus','the required feature remains legible at the nominated display scale','required feature and display','camera')],['SNS 비율을 모든 플랫폼의 영구 규격으로 고정하지 않는다.','미리보기 재크롭을 검증하지 않고 최종 게시 성공이라고 보고하지 않는다.'],'S01,S04','face_hands_prop_visibility_budget','reuse_atoms','세로 크롭 후에도 손거울 테두리와 성인 눈이 남음','크롭이 거울 테두리를 잘라 일반 얼굴 사진으로 바뀜',tier='P0')

# Styles and series are research records, excluded from single-image runtime proposals.
add('PS01','포토덤프·꾸민 듯 안 꾸민 듯한 스냅','photo dump;curated candid','style',[
 ('capture_context','one frame depicts a specific interrupted everyday action','subject and everyday action','action,timing'),
 ('composition','one restrained crop or gesture irregularity remains visible','scene irregularity','composition'),
 ('focus','the chosen portrait signal remains readable despite that irregularity','main face','camera')],['느슨한 외관과 실제 무편집·무연출은 다르다.','여러 장의 묶음이라는 의미를 한 장 안의 콜라주로 치환하지 않는다.'],'S23,S10','mep_in_between,photodump_candid_sequence_context','maintenance_style','생활 행동의 순간을 골라 묶은 시리즈의 한 장','2026 인기 1위라는 근거 없는 라벨',scope='capture_style',tier='P2')
add('PS02','디카·직광 플래시 스냅','digicam aesthetic;direct-flash snapshot','style',[
 ('lighting','a near-axis flash-like source creates direct highlights and scene-owned cast shadows','main subject and near-axis source','lighting'),
 ('texture','one nominated low-resolution or compression texture remains locally visible','selected image texture','style'),
 ('focus','the intended facial expression remains legible through the chosen texture','main face','camera')],['직광 플래시·노이즈·JPEG는 독립 조건이며 CCD 장비를 픽셀에서 확정하지 않는다.','Y2K 의상·2000년대 시대·디카를 자동 동의어로 묶지 않는다.'],'S03,S02','early_2000s_digicam_social_repost_capture','maintenance_style','정면광 그림자와 약한 압축이 있으면서 성인 얼굴은 읽힘','노이즈만 추가하고 디카 촬영·2026 유행을 확정',scope='capture_style',tier='P2')
add('PS03','0.5 셀피·초광각 셀피','0.5 selfie;ultrawide selfie','style',[
 ('camera_direction','a close self-held camera viewpoint produces a wide surrounding field','camera holder and environment','camera'),
 ('composition','near and farther body regions show coherent close-range scale differences','subject body depth','composition'),
 ('subject_framing','the requested face region remains recognizable within that wide field','main face','framing')],['.5x는 카메라 선택 메타데이터이고 0.5 셀피는 촬영 관행이다.','후면·화면 비확인·손의 위치를 라벨만으로 일괄 강제하지 않는다.'],'S21,S14','wide_angle_near_field_perspective','maintenance_style','넓은 주변과 근접 원근을 의도한 성인 셀피','초광각 요청을 자동 망원 얼굴 사진으로 치환',scope='capture_style',tier='P2')
add('PS04','관계·반응 중심 인물','relational portrait;interaction-led portrait','style',[
 ('action','one visible gesture or response relates to a specific interaction target','subject and target','action,relationship'),
 ('composition','the frame preserves evidence of that same target or its position','target cue and frame','composition'),
 ('focus','the subject reaction remains readable within the interaction frame','main face or gesture','camera')],['진정성·성격·실제 관계는 단일 픽셀의 확정 사실이 아니다.','기쁨·대화·호감을 모든 인물에게 기본 주입하지 않는다.'],'S19,S20,S08','mep_gaze_target','maintenance_style','타인에게 건네는 행동과 상대 위치 단서가 같은 화면에 있음','표정 하나로 실제 연애 관계·진심을 판정',scope='capture_style',tier='P1')
add('PS05','생활 도구를 이용한 시각 실험','creative portrait;everyday optical device','style',[
 ('composition','one nominated scene-owned device changes a visible spatial relation','selected device and scene','composition'),
 ('action','the subject action or visible placement relates coherently to that device','subject and device','action'),
 ('focus','the requested portrait signal survives the optical intervention','main face','camera')],['creative·cinematic·editorial은 특정 시각 의무가 아니다.','새로움 점수와 장비·인물의 매력은 서로 다른 평가다.'],'S11,S15,S24','','maintenance_style','손거울 한 가지로 얼굴 중심의 구도를 변주','굴절·기울기·강한 그림자·얼굴 가림을 모두 자동 추가',scope='capture_style',tier='P1')
add('PM01','딥틱','diptych;paired portraits','series',[
 ('format','two independently readable images form one explicitly ordered pair','two images','format'),
 ('composition','a declared visual attribute links the paired images','pair relation','composition'),
 ('action','a declared change distinguishes their portrait roles','pair role difference','action')],['두 사람 투샷과 두 이미지의 쌍은 다르다.','기본 single-image 생성에 두 패널을 몰래 추가하지 않는다.'],'S22','','maintenance_series','정면 눈맞춤과 옆시선 두 사진의 쌍','한 프레임 두 인물을 diptych라고 판정',scope='multi_image',tier='P2')
add('PM02','트립틱','triptych;three-image portrait set','series',[
 ('format','three independently readable images form one nominated group','three images','format'),
 ('composition','a declared color shape or light relation connects all three','series linking attribute','composition'),
 ('action','each image contributes a distinct declared portrait function','series image roles','action')],['세 사람 단체사진과 세 이미지의 그룹은 다르다.','같은 시드·외형 연속성이 자동 보장되지 않는다.'],'S22','','maintenance_series','얼굴·행동·공간이라는 세 기능의 사진 묶음','단체사진 한 장을 세 이미지 시리즈로 판정',scope='multi_image',tier='P2')
add('PM03','시간 순서 인물 시퀀스','portrait sequence;temporal portrait progression','series',[
 ('format','separate images have an explicit ordered sequence','ordered image set','format'),
 ('action','one declared event phase changes between the ordered frames','event phase across frames','timing,action'),
 ('composition','declared appearance and setting anchors maintain permitted continuity','series continuity anchors','composition')],['단일 중간 순간은 시간 순서를 증명하지 않는다.','인물의 진짜 감정 변화·성격을 사진의 순서만으로 확정하지 않는다.'],'S22,S10','','maintenance_series','대화 듣기·반응·정리라는 세 상태를 순서대로 제시','거의 같은 정지 포즈 세 장에 시간 라벨만 부여',scope='multi_image',tier='P2')

RELATION_PROFILE_CONCEPTS = {'PC02','PC03','PC09','PC10','PC12','PC16','PC17','PC18','PC19','PC21','PC22','PC23','PC24','PC27','PC29','PC30'}

def build():
    data = pg.load_json(SKILL / 'assets/photo_prompt_tags.json')
    registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
    entries = {}
    for slot, rows in data['slots'].items():
        for row in rows:
            entries.setdefault(row['id'], []).append({'slot':slot,'en':row.get('en','')})
    profiles = {p['id']:p for p in registry['profiles']}
    inputs = [SKILL / 'scripts/prompt_generator.py', SKILL / 'scripts/photo_candidate_semantics.py', SKILL / 'scripts/visual_profile_contracts.py']
    inputs += [SKILL/'assets'/n for n in ['photo_prompt_tags.json','photo_prompt_visual_obligations.json','photo_prompt_visual_profile_index.json','photo_prompt_semantic_index.json',*pg.RESEARCH_EXTENSION_FILENAMES,*pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES] if (SKILL/'assets'/n).is_file()]
    input_hashes = {str(p.relative_to(ROOT)):digest_file(p) for p in dict.fromkeys(inputs)}
    coverage = []
    for c in CONCEPTS:
        resolved = [{'id':i,'kind':'profile' if i in profiles else 'candidate_atom','found':i in profiles or i in entries,'candidate_slots':[v['slot'] for v in entries.get(i,[])]} for i in c['existing_ids']]
        coverage.append({'concept_id':c['id'],'proposal':c['integration_proposal'],'references':resolved,
          'coverage_claim':'Authored IDs and components inspected. No retrieval ranking, live exposure, or rendered fidelity inferred.',
          'existing_profile_gate_counts':{i:len(profiles[i].get('render_gates',[])) for i in c['existing_ids'] if i in profiles}})
    write('sources.json',{'schema_version':'portrait-research-sources/v1','sources':sources})
    write('concept-catalog.json',{'schema_version':'portrait-composition-research/v1','concepts':CONCEPTS})
    write('coverage-audit.json',{'schema_version':'portrait-research-coverage/v1','checked_on':'2026-09-27','merged_counts':{'slots':len(data['slots']),'candidate_entries':sum(map(len,data['slots'].values())),'candidate_bundles':len(data.get('candidate_bundles',[])),'visual_profiles':len(profiles)},'input_sha256':input_hashes,'concept_coverage':coverage})
    draft_profiles = []
    for c in CONCEPTS:
        if c['id'] not in RELATION_PROFILE_CONCEPTS:
            continue
        evidence = [v['evidence_en'] for v in c['components']]
        pid = 'pc_' + c['id'].lower() + '_owner_relation'
        # Full conjunction is the only exact trigger; broad labels remain candidates.
        draft_profiles.append({'id':pid,'category':'portrait_composition_owner_relation',
          'activation':{'exact_terms':['; '.join(evidence)],'requires_adult_character':False,'semantic_discovery_requires_component_evidence':False},
          'semantics':{'definition':'; '.join(evidence),'paraphrase_examples':[c['label_ko'],*c['terms_en']],
            'contrast_examples':c['confusion_boundaries_ko'],'claim_limits':['Only the requester-supported owner and visible scope are hard.','Attractiveness, authenticity, biography and actual relationship are not pixel claims.']},
          'concept_candidate':{'concept_terms':[c['label_ko'],*c['terms_en'],*evidence]},
          'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
          'reject_substitutes':c['confusion_boundaries_ko'],
          'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':[
            {'id':f'component_{j+1}','match_terms':[v['evidence_en']],'evidence_field':f'component_{j+1}_phrase','evidence_terms':[v['evidence_en']],
             'min_content_words':3,'instruction':'Preserve the requester-supported owner and make this relation visible: '+v['evidence_en'],
             'render_gate':{'id':f'vo_{pid}_{j+1}','review_scale':'native' if v['slot'] in {'contact_point','focus'} else 'both',
                 'description':v['evidence_en']+'. Judge the declared owner in the same saved image; missing or unclear evidence fails.'}}
             for j,v in enumerate(c['components'])]}})
    extension = {'schema_version':'photo-prompt-research-extension/v1','slots':{},'visual_semantics':[]}
    proposal_mapping=[]
    for c in CONCEPTS:
        if c['scope'] != 'single_image':continue
        member_ids=[];scopes={}
        for j,v in enumerate(c['components']):
            # Existing atoms are reviewed for reuse; these are alternative authored relation candidates, not mandatory replacements.
            aid=f'pc_{c["id"].lower()}_component_{j+1}'
            atom={'id':aid,'ko':f'{c["label_ko"]}: 구성요소 {j+1}','en':v['evidence_en'], 'weight':0.45,
             'tags':['human','portrait','composition'],'for_any':['human'],
             'aliases':[], 'keywords':[c['terms_en'][0]],'embedding_text':v['evidence_en'],
             'concept_units':[v['evidence_en']],
             'relations':[{'id':aid+'_owner','type':'declared_owner_scope','subject':v['owner'],'object':'the requester-supported main portrait and frame'}],
             'affected_dimensions':v['dimensions']}
            extension['slots'].setdefault(v['slot'],[]).append(atom);member_ids.append(aid);scopes[aid]=v['slot']
            proposal_mapping.append({'candidate_id':aid,'concept_id':c['id'],'component_id':v['id'],'source_ids':c['source_ids'],
              'basis':'independent relation synthesis from supported photographic dimensions; sources do not prescribe this exact wording',
              'review_before_adoption':'deduplicate against existing atom and profile dimensions; preserve requester count, face visibility and locked axes'})
        pid='pc_'+c['id'].lower()+'_owner_relation'
        extension['visual_semantics'].append({'id':'pc_bundle_'+c['id'].lower(),'primary_visual_proposition':c['label_ko'],
          'component_groups':[{'id':v['id'],'visible_evidence':[v['evidence_en']]} for v in c['components']],
          'candidate_ids':member_ids,'candidate_slots':scopes,
          'hard_profile_ids':[pid] if c['id'] in RELATION_PROFILE_CONCEPTS else [],
          'confusion_boundaries':c['confusion_boundaries_ko'],'source_keywords':c['terms_en'],
          'relations':[{'id':'pc_bundle_'+c['id'].lower()+'_joint','type':'co_realized_with_same_subject_and_event','subject':'the declared component owners','object':'one requester-supported portrait in the same saved image'}]})
    write('visual-profiles.proposed.json',{'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','description':'Research draft, not installed; narrow requester-supported portrait relations.','profiles':draft_profiles})
    write('candidate-extension.proposed.json',extension)
    write('candidate-source-map.json',{'schema_version':'portrait-candidate-source-map/v1','candidate_source_map':proposal_mapping,
      'promotion_status':'research_draft_not_installed','runtime_exposure':'not_tested','pixels':'not_generated'})
    # Multilingual fixtures are authored alongside data and are development cases, never independent holdouts.
    cases=[]
    for c in CONCEPTS:
        pid='pc_'+c['id'].lower()+'_owner_relation'
        expected=[pid] if c['id'] in RELATION_PROFILE_CONCEPTS else []
        cases += [
          {'id':c['id']+'_definition_en','concept_id':c['id'],'kind':'exact_definition','query':'; '.join(v['evidence_en'] for v in c['components']), 'expected_new_hard_profiles':expected,'status':'development_fixture'},
          {'id':c['id']+'_broad_en','concept_id':c['id'],'kind':'broad_label_no_hard','query':c['terms_en'][0], 'expected_new_hard_profiles':[],'status':'development_fixture'},
          {'id':c['id']+'_positive_ko','concept_id':c['id'],'kind':'semantic_paraphrase_advisory','query':c['positive_case_ko'], 'expected_candidate_concepts':[c['id']],'expected_new_hard_profiles':[],'status':'authored_not_independent'},
          {'id':c['id']+'_negative_ko','concept_id':c['id'],'kind':'confusion_boundary','query':c['negative_case_ko'], 'expected_complete_concept':False,'expected_new_hard_profiles':[],'status':'pixel_or_semantic_review_pending'},
        ]
        if c['id'] in RELATION_PROFILE_CONCEPTS:
            evidence='; '.join(v['evidence_en'] for v in c['components'])
            cases += [{'id':c['id']+'_negated_en','concept_id':c['id'],'kind':'negated_definition','query':'not '+evidence,'expected_new_hard_profiles':[],'status':'development_fixture'},
                      {'id':c['id']+'_incomplete_en','concept_id':c['id'],'kind':'single_component_no_hard','query':c['components'][0]['evidence_en'],'expected_new_hard_profiles':[],'status':'development_fixture'}]
    special=[
      ('R01','bare_three_quarter','three-quarter portrait','meaning clarification: distinguish shot length and orientation'),
      ('R02','own_vs_other_shoulder','the main subject looks back over their own shoulder','must not add another person'),
      ('R03','camera_vs_body_diagonal','a reclining diagonal body with upright window lines','must not rotate the camera'),
      ('R04','literal_face_occlusion','a portrait with the face fully hidden by the phone','must not force the face-visible goal'),
      ('R05','profile_one_eye','a strict side profile with one visible eye','must not force both eyes'),
      ('R06','eyes_closed','an eyes-closed adult portrait','must not add eye contact'),
      ('R07','mirror_no_phone','a reflected face in a mirror with a partial back view','must not add a selfie device'),
      ('R08','hand_only_companion_count','one full adult subject and another person hand entering from the edge','count and relationship must be requester grounded'),
      ('R09','locked_camera','eye-level camera locked; low-angle candidate offered','reject candidate when camera dimension is locked'),
      ('R10','locked_pose','front-facing torso locked; angled-shoulder candidate offered','reject candidate when pose dimension is locked'),
      ('R11','unknown_roll','a face close-up against a featureless background','camera-roll evidence unscorable without a reference'),
      ('R12','reflection_focus','the mirror rim is sharp and the reflected face soft','cannot pass reflected-face-focus gate'),
      ('R13','bokeh_vs_motion','a stationary adult with round blurred background light spots','cannot pass motion-trail relation'),
      ('R14','vignette_vs_frame','a digital dark vignette around a portrait','cannot pass physical-opening relation'),
      ('R15','series_vs_frame','three separate portraits requested as a sequence','route to multi-image workflow; no silent single-image collage'),
      ('R16','near_field_requested','an exaggerated close ultrawide adult selfie','preserve requested exaggeration; no forced telephoto repair'),
      ('R17','window_vs_double_exposure','a portrait overlay with city lights and no glass evidence','do not claim glass-plane support'),
      ('R18','reverse_look_room','a person looks toward the tightly cropped left edge with space on the right','intentional short-sided choice must remain possible'),
      ('R19','blur_requested','an intentionally blurred abstract portrait','do not force sharp eyes globally'),
      ('R20','locked_no_companion','one person alone with no other visible body parts','reject a cropped companion hand or OTS proposal'),
    ]
    cases += [{'id':i,'kind':k,'query':q,'expected':e,'status':'design_fixture_not_executed'} for i,k,q,e in special]
    (HERE/'regression-cases.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in cases),encoding='utf-8')
    with (HERE/'keyword-coverage.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['concept_id','한국어','English terms','scope','priority','integration','sources','existing IDs','component_count'])
        for c in CONCEPTS:w.writerow([c['id'],c['label_ko'],'; '.join(c['terms_en']),c['scope'],c['priority'],c['integration_proposal'],','.join(c['source_ids']),','.join(c['existing_ids']),len(c['components'])])
    write('qualification-plan.json',{
      'schema_version':'portrait-composition-qualification-plan/v1','status':'planned_not_executed','policy':'partial_is_fail',
      'request_boundary':'No rendering requested in this research turn; independent pre-core meaning must be authored on each later generation run.',
      'arms':[
        {'id':'Q1','target_concepts':['PC02','PC03'],'scene_variants':['table edge','seat edge','counter edge'],'hard_owner_checks':['torso-head separation','table-camera geometry','face legibility','hand contact']},
        {'id':'Q2','target_concepts':['PC17','PC18'],'scene_variants':['dialogue shoulder','collar adjustment','small object handoff'],'hard_owner_checks':['secondary owner','main versus secondary hands','reaction target','requested count']},
        {'id':'Q3','target_concepts':['PC19','PC20'],'scene_variants':['plant foreground','curtain opening','door opening'],'hard_owner_checks':['actual foreground plane','focus owner','opening not vignette','surviving face region']},
        {'id':'Q4','target_concepts':['PC21','PC22','PC23'],'scene_variants':['window transmission','wall mirror','hand mirror'],'hard_owner_checks':['surface type','reflected versus transmitted face','physical correspondence','reflected-face sharpness']},
        {'id':'Q5','target_concepts':['PC09','PC10','PC27'],'scene_variants':['seated triangle','reclining diagonal','symmetric corridor'],'hard_owner_checks':['nominated body points','support path','camera roll versus body axis','background versus pose symmetry']},
        {'id':'Q6','target_concepts':['PC24','PC29','PC30'],'scene_variants':['edge prism','stationary subject with moving lights','canted window portrait'],'hard_owner_checks':['local optical owner','motion versus defocus','global reference tilt','face survives device']},
      ],
      'experimental_design':{'minimum_per_target_relation':'3 genuinely different scene contexts × 2 independent attempts; final sample size chosen before renders',
        'baseline_comparison':'paired baseline and selected-candidate conditions; each baseline frozen before local retrieval; same requester constraints and documented randomized condition order',
        'avoid_claim':'same seed does not guarantee equal stochastic conditions across models; exposure and selection are measured separately',
        'holdout':'Freeze independently authored paraphrases, counterexamples and image criteria before implementation; development fixtures here are not those holdouts.'},
      'evidence_layers':['authored_source','schema_compile','index_current','retrieval_candidate_exposure','composer_selection','literal_prompt_actuation','runtime_request_binding','same_image_pixels','requester_preference'],
      'report_counts':['source coverage','exposure per requested target','selection among exposed targets','all-hard-gates pass per target','whole-scene pass','unscorable or blocked count','requester acceptance'],
      'pixel_review':{'views':['whole_image_thumbnail','native_resolution_owner_crop'],'statuses':['pass','fail','unscorable'],'aggregate':'A scene qualifies only when every applicable hard gate passes in the same image. No averaging, retry cherry-picking or cross-image evidence pooling.',
        'separate_user_judgment':['face readability','felt engagement','composition interest','subjective appeal preference']}})
    build_report(data,profiles,coverage,extension,draft_profiles,cases)
    print(json.dumps({'concepts':len(CONCEPTS),'original_compositions':sum(c['id'].startswith('PC') for c in CONCEPTS),'single_image_concepts':sum(c['scope']=='single_image' for c in CONCEPTS),'sources':len(sources),'draft_profiles':len(draft_profiles),'draft_atoms':len(proposal_mapping),'draft_bundles':len(extension['visual_semantics']),'development_cases':len(cases)},ensure_ascii=False))

def build_report(data,profiles,coverage,extension,draft_profiles,cases):
    source_lookup={s['id']:s for s in sources}
    def refs(ids):return ', '.join(f'[{i}: {source_lookup[i]["title"]}]({source_lookup[i]["url"]})' for i in ids)
    text='''# 인물 사진 구도: 시각 의미·후보팩 보강 리서치

조사일: 2026-09-27. 참조 대화: 「인물 사진 구도 조사」(6ab8c04c-6820-83ee-9d4c-6b4241474930).

## 1. 결론과 산출물의 범위

가장 필요한 보강은 구도 이름의 추가보다 **인물·카메라·몸·시선·전경·반사면·초점·프레임 사이의 관계를 분리하고, 같은 사진에서 그 관계가 함께 보이는지 판정하는 데이터**이다. 원 대화의 30개 구도, 재사용할 12개 구성 원리, 5개 촬영 표현, 3개 사진 묶음을 총 50개 연구 레코드로 정리했다. 25개 출처는 열람 방식과 확인 범위를 함께 기록했다.

이번 결과는 연구와 적용 가능한 초안이다. 런타임 사전·레지스트리·인덱스·생성기는 변경하지 않았다. 연구 폴더 안의 `.proposed.json`은 현재 컴파일러에 대조하는 검토용 데이터이며 자동 로딩되지 않는다. 기존 Y2K 변경, 미완료 인덱스 파일, 다른 출력은 보존한다. 실제 이미지 생성·픽셀 통과·사용자 매력 판단·후보팩 효과는 이 턴의 검증 범위가 아니다.

| 파일 | 용도 |
|---|---|
| `source-conversation.json` | 조사한 원 대화의 조회 스냅샷; 이전 인용 마커는 새 출처로 취급하지 않음 |
| `sources.json` | 출처별 URL·확인일·사실 범위·열람 제한 |
| `concept-catalog.json` | 50개 개념의 구성요소·소유자·차원·혼동 경계·적용안 |
| `coverage-audit.json` | 현재 합쳐진 데이터의 개수·기존 ID 대조·입력 파일 SHA-256 |
| `candidate-extension.proposed.json` | 42개 단일사진 개념의 관계 후보와 선택 번들 초안 |
| `visual-profiles.proposed.json` | 기존 개념만으로 부족한 16개 관계의 좁은 의무 초안 |
| `candidate-source-map.json` | 후보와 출처의 유지보수 연결; 런타임에 출처 URL을 노출하지 않음 |
| `keyword-coverage.csv` | 한국어·영어 키워드별 범위와 재사용 여부 |
| `regression-cases.jsonl` | 개발용 정의·넓은 라벨·한국어 설명·반례·변이 사례 |
| `qualification-plan.json` | 이후 독립 렌더와 동일 이미지 픽셀 검증 계획 |
| `verification.json` | 실제 실행한 구조·좁은 활성화·번들 경계 검사 결과 |

## 2. 출처가 말하는 사실과 이번 설계 제안을 구분한다

촬영 범위가 얼굴·행동·환경의 비중을 바꾸고, 눈 초점과 단순한 배경이 얼굴 전달에 도움이 된다는 점은 촬영 자료에서 확인했다. 몸과 머리의 방향을 분리하는 예시도 확인된다. [Canon 프레이밍](https://asia.canon/en/support/8200023500), [Nikon 눈 초점](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits), [Nikon 몸과 머리 방향](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/take-better-portraits).

전경 흐림, 거울, 프리즘, 고보, 움직임 궤적은 서로 다른 공간·광학 원리를 가진다. 프리즘은 굴절·색 분산 등, 고보는 광원 패턴, 움직임 흐림은 노출 시간 중 위치 변화에 관한 자료를 바탕으로 분리했다. [Adobe 프리즘](https://www.adobe.com/creativecloud/photography/technique/prism.html), [Westcott 고보](https://westcottu.com/creating-a-sense-of-environment-with-the-optical-spot-by-lindsay-adler), [Adobe 모션 블러](https://www.adobe.com/creativecloud/photography/technique/motion-blur.html).

평면거울의 얼굴상은 거울 뒤의 가상상에 해당한다. 카메라에서 거울을 거쳐 인물까지의 광학 경로와 표면까지 거리를 분리해야 한다. 단순 정면 배치에서는 경로를 `카메라→거울 + 거울→인물`로 이해할 수 있으며, 비스듬한 배치는 실제 반사 광선을 기준으로 판단한다. 따라서 거울 테두리·얼룩 초점과 반사 얼굴 초점은 같은 조건이 아니다. 곡면 거울에는 이 평면거울 모델을 그대로 적용하지 않는다. [OpenStax 평면거울](https://openstax.org/books/university-physics-volume-3/pages/2-1-images-formed-by-plane-mirrors).

다음은 이번 목적을 위한 자체 설계 판단이다: 얼굴이 중요한 요청에는 살아남아야 할 표정 영역을 선언하고, 강한 장치의 범위를 제한하며, 장치와 주인공의 우선순위를 함께 검토한다. 이는 모든 인물사진에 눈맞춤·양쪽 눈·예쁜 얼굴·단순 배경을 강제하는 규칙이 아니다. 옆얼굴·눈 감음·완전 얼굴 가림·의도적 흐림·작은 환경 인물을 명시한 요청은 그대로 보존한다. 특정 카메라 수치·얼굴 면적 비율·기울기 각도를 보편적 통과 기준으로 만들 근거는 확보하지 못했다.

## 3. 용어를 분해할 최소 의미 축

`출력 범위 → 촬영 범위 → 카메라 높이/피치/롤 → 얼굴 방향 → 몸통 방향 → 눈의 목표 → 몸의 지지 → 행동/순간 → 전경 소유자 → 반사면 종류 → 초점 소유자 → 가림 범위 → 배경 위계 → 후처리/질감`

| 혼동하기 쉬운 표현 | 별도로 보존할 의미 |
|---|---|
| three-quarter view / three-quarter-length | 얼굴·몸의 방향 / 몸을 포함하는 길이. 단독 three-quarter가 핵심이면 먼저 의미를 확인 |
| own over-the-shoulder glance / OTS shot | 본인의 몸과 고개 회전 / 타인의 어깨와 주인공 사이 카메라 관계 |
| diagonal body / Dutch roll | 몸의 축 / 장면 기준선의 공통 기울기 |
| negative space / looking room / headroom / move room | 저정보 영역 / 시선 벡터 앞 / 머리 위 / 이동 벡터 앞 |
| foreground bokeh / background bokeh / motion blur | 가까운 물체의 초점 이탈 / 먼 배경의 초점 이탈 / 노출 중 움직임 |
| mirror / window glass / prism | 반사 가상상 / 투과와 반사의 중첩 / 굴절·분산·반사 효과 |
| candid / off-camera gaze / mid-action | 촬영 방식 / 눈의 방향 / 화면에서 보이는 사건 단계 |
| photo dump / diptych / triptych / sequence | 선택·게시 묶음 / 두 이미지 / 세 이미지 / 명시적 시간 순서 |

이 분리는 원 대화에 명시된 혼동 경계를 보존한 것이다. 영상 OTS와 Dutch angle의 구조는 정지사진에 필요한 공간 관계만 사용했다. [Adobe OTS](https://www.adobe.com/sg/creativecloud/video/production/cinematography/camera-shots-and-angles/over-the-shoulder-shot.html), [Adobe Dutch angle](https://www.adobe.com/au/creativecloud/video/production/cinematography/camera-shots-and-angles/dutch-angle-shot.html).

## 4. 현재 저장소 데이터와 보강 경계

'''
    text+=f'조회 시 합쳐진 데이터는 **{sum(map(len,data["slots"].values())):,}개 후보 항목·{len(data.get("candidate_bundles",[])):,}개 번들·{len(profiles):,}개 시각 프로필**이다. 이 숫자는 전체 사전의 크기이며 인물 구도 30개가 충분히 검증되었다는 수치가 아니다. 각 파일의 해시를 `coverage-audit.json`에 고정했다.\n\n'
    text+='''재사용 우선 영역은 `look_motion_room_direction_relation`, `subject_field_negative_space_relation`, `frame_within_frame_boundary_relation`, `companion_viewpoint_everyday_candid`, `mep_in_between`, `mep_graphic_pose`, `mep_gaze_target`, `mep_environment_relation`, `pr_environmental_portrait_subject_place`, `pr_casual_crop_subject_legibility`, `rb_glass_reflection_transmission`이다.

다만 기존 계약에는 추가 조건이 있다. 동행자 프로필은 생활 행동과 반응, 프레임 속 프레임은 세 면의 둘레, overhead 프로필은 가까운 위쪽 시점과 바닥·원근 등의 증거를 요구한다. 맞은편 테이블·창틀 한쪽·앉은 고각을 요청했다고 이 모든 조건을 자동 강제하면 원래 의미가 바뀐다. 미러 셀피는 휴대폰과 손의 접촉까지 요구하므로 일반 거울 인물사진에 쓰면 안 된다. 가시 얼굴을 가리는 기존 감성 사진 계약도 기본 얼굴 우선 목표에 무조건 섞지 않는다.

신규 관계 초안은 어깨–머리 분리, 맞은편 테이블 위계, 앉은 삼각 점, 지지된 몸 대각선, 자기 팔의 얼굴 프레이밍, 렌즈 쪽 전달, 타인의 어깨·손 소유자, 전경 흐림 틈, 유리 투과 얼굴과 외부 반사, 거울 속 주 얼굴, 손거울의 얼굴 범위, 국소 프리즘, 대칭 배경과 비대칭 포즈, 정지 인물과 주변 궤적, 카메라 롤의 16개이다. 모두 넓은 이름이 아니라 요청 근거가 있는 구성요소의 전체 결합에서만 하드가 되는 초안이다.

기존 항목을 확장·재사용할 수 있는 곳도 관계 후보 초안에 포함했다. 따라서 아래 초안의 총 항목 수를 실제 신규 항목으로 그대로 추가할 수량으로 해석하면 안 된다. 채택 전에 같은 소유자·관계의 기존 원자를 합치고 ID는 유지하는 중복 제거 검토가 필요하다.

## 5. 원 대화의 30개 구도와 12개 추가 원리

아래 구성요소와 통과 조건은 출처 문장의 번역·보편적 미학 정의가 아니라 자체 데이터 설계이다. 출처는 해당 기법의 기초 원리만 지지한다. 장면 예시는 개발용으로 작성했고 실제 렌더 통과 사례가 아니다.

'''
    for c in CONCEPTS:
        if c['scope']!='single_image':continue
        text+=f'### {c["id"]}. {c["label_ko"]}\n\n'
        text+='검색어: '+', '.join('`'+t+'`' for t in c['terms_en'])+'.\n\n'
        text+='| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |\n|---|---|---|\n'
        for v in c['components']:text+=f'| {v["id"]} · `{v["slot"]}` | {v["owner"]} / {", ".join(v["dimensions"])} | {v["evidence_en"]} |\n'
        text+='\n혼동 경계: '+' / '.join(c['confusion_boundaries_ko'])+'\n\n'
        text+='현재 근거: '+(', '.join('`'+i+'`' for i in c['existing_ids']) or '전용 관계는 신규 초안 또는 선택 후보로 검토')+f'. 적용안: `{c["integration_proposal"]}` · {c["priority"]}.\n\n'
        text+=f'개발 사례: {c["positive_case_ko"]}. 반례: {c["negative_case_ko"]}.\n\n'
        text+='기초 원리 출처: '+refs(c['source_ids'])+'.\n\n'
    text+='''## 6. SNS 표현과 여러 장의 구성은 별도 범위로 둔다

'''
    for c in CONCEPTS:
        if c['scope']=='single_image':continue
        text+=f'### {c["id"]}. {c["label_ko"]}\n\n'
        text+='검색어: '+', '.join(c['terms_en'])+f'. 범위: `{c["scope"]}`.\n\n'
        text+='보이는 요소: '+'; '.join(v['evidence_en'] for v in c['components'])+'.\n\n'
        text+='경계: '+' / '.join(c['confusion_boundaries_ko'])+'\n\n'
        text+='출처와 범위: '+refs(c['source_ids'])+'.\n\n'
    text+='''Adobe의 2026 자료와 2026-09-16 해설은 관계·일상·감정 전달을 강조한다. 이는 산업 전망이며 특정 인물 구도의 SNS 인기 순위·조회수·전환 효과를 측정한 자료가 아니다. 포토덤프 자료는 2022년 문화 해설이다. 디카·0.5 셀피는 이 연구에서 시각 표현과 촬영 메타데이터를 나눠 기록했으며 2026 상승 추세를 별도 주장하지 않는다. [Adobe 2026 전망](https://business.adobe.com/resources/creative-trends-report.html), [Adobe 9월 해설](https://business.adobe.com/uk/blog/connectioneering-creative-trend-human-connection-ai-era), [Vogue 포토덤프](https://www.vogue.com/article/instagram-photo-dump-generation-z).

## 7. 후보팩용 데이터 설계와 채택 규칙

'''
    text+=f'초안은 **{sum(map(len,extension["slots"].values()))}개 원자 후보, {len(extension["visual_semantics"])}개 선택 번들, {len(draft_profiles)}개 관계 프로필**을 포함한다. 기본 컨텍스트는 human portrait이지만 연구 예시의 성인 지정은 고정 캐스팅·나이·성별·외형 기본값으로 이식하지 않았다. 새로운 장면·인물·소품을 자동 추가하는 프리셋은 만들지 않았다.\n\n'
    text+='''후보는 `concept_units`를 짧은 관계 단위로 보존하고 `relations`에서 소유자와 대상, `affected_dimensions`에서 변경 차원을 선언한다. 얼굴·몸·카메라·표정·초점을 하나의 무차별 구도 태그로 합치지 않는다. 타인의 어깨나 손을 선택하려면 `relationship`과 관련 `composition/framing` 차원이 열려 있고 요청한 인원 조건과도 맞아야 한다. 닫힌 pose/camera/relationship을 번들이 열어서는 안 된다.

번들의 `associated_profile_ids`는 연구 연관 정보이다. 선택된 번들이 독립 요청 근거 없이 프로필을 자동 하드 활성화하지 않는다. 반면 시각 개념을 명시적으로 opt-in하여 그 의무를 선택한 경우에는 해당 계약의 모든 구성요소와 render gate를 인계해야 한다. 번들 선택과 프로필 opt-in은 서로 다른 행동이다. 선택하지 않은 후보는 의무가 아니며 모든 후보를 거절해도 된다.

프로필의 exact trigger는 구성요소의 전체 결합만 사용한다. `mirror portrait`, `candid`, `Dutch angle`, `pretty`, `three-quarter` 등 단독 라벨을 곧바로 새 하드 프로필로 만들지 않는다. 한국어 자연 설명과 가까운 표현은 선택 후보의 검색 회수 대상이다. 이 초안의 영어 전체 정의는 컴파일·변이 검증용이며 실사용자의 발화 문장을 exact alias로 박아 넣는 방식으로 일반화할 계획이 아니다.

`source_ids`, URL, 시대 유행 근거, 후보–출처 맵은 유지보수 파일에만 둔다. 런타임 후보의 embedding text·concept units·최종 프롬프트에 연구 제목·검색 과정·출처 문장을 복사하지 않는다. 초안의 부정 경계는 평가·후보 거절을 위한 데이터이며 positive prompt에 포괄적인 금지문으로 주입하지 않는다.

### 원자 후보의 추가 개선이 필요한 부분

각 원자는 의미를 보존하는 일차 분해안이며 아직 독립 후보 노출률을 검증하지 않았다. 단일 구성요소가 너무 일반적이면 번들 키워드 회수와 실제 선택이 떨어질 수 있다. 전체 의미를 문장 템플릿 하나로 만들기보다 `전경 위치–얼굴 틈–초점 소유자`, `거울 경계–반사 얼굴–직접 몸 대응` 같은 필수 공동 관계를 번들의 구성요소와 relation evidence로 묶어야 한다. 가벼운 유사도 히트가 없는 관계를 대신 증명하게 두지 않는다.

## 8. 검증 사례와 이후 픽셀 시험

'''
    text+=f'개발용 사례는 총 {len(cases)}개이다. 각 개념의 영어 전체 정의·넓은 영어 라벨·한국어 설명·한국어 혼동 반례, 신규 프로필의 부정·일부 구성요소 변이, 20개 요청 우선 경계 사례를 포함한다. 한국어 사례는 데이터와 같이 작성했으므로 독립 holdout이나 임베딩 일반화 성공으로 부르지 않는다. 이번 실행 결과는 `verification.json`에 있는 검사만 유효하다.\n\n'
    text+='''이후 단계는 다음 순서로 진행한다.

1. 30개 구도의 요청 의미·반례·평가 기준을 런타임 데이터와 독립적으로 동결한다. 12개 원리는 재사용 검사에 포함한다.
2. 기존 원자와 신규 관계를 중복 제거하고, 관계별 source/component/profile/bundle을 확인한다.
3. 임베딩·BM25F 인덱스를 실제 채택된 소스에서 갱신하고 해시·정확 경로·의미 재표현·인접 반례를 검사한다. 이 연구에서는 인덱스를 갱신하지 않았다.
4. 후보 노출과 작가 선택을 별도로 기록한다. 노출되지 않은 목표가 프롬프트나 이미지에서 나타났다고 후보팩 효과라고 해석하지 않는다.
5. 관계별 서로 다른 세 장면과 독립 두 시도로 적합 범위를 시험한다. 예산과 표본 수는 실제 실행 전 결정한다. 같은 코어를 동결한 baseline/후보 선택 조건을 비교하되 시드만 같다고 모든 조건이 동일하다고 가정하지 않는다.
6. 전체 썸네일에서 주인공·구도 장치의 첫 읽기를 보고, 네이티브 크롭에서 손 접촉·눈 초점·반사 대응·몸의 지지·세부 가림을 판정한다. 적용되는 모든 hard gate가 같은 이미지에서 통과해야 장면 통과이다.
7. 가시성·초점·물리 관계의 통과와 사용자가 느끼는 매력·친밀감·흥미를 분리한다. 사용자 수락을 받기 전 대표 구도로 승격하지 않는다.

특히 실패를 예상하고 대비할 대상은 전경이 눈을 덮는 경우, 손거울이 너무 작아 얼굴을 읽을 수 없는 경우, 유리 투과와 거울 반사가 혼합되는 경우, 타인의 손이 주인공의 추가 팔로 이어지는 경우, 단순 보케를 움직임 궤적으로 오인하는 경우, 기울어진 몸을 더치 앵글로 판정하는 경우이다. 실패·가림·판정 불가를 평균 점수로 상쇄하지 않는다.

## 9. 적용 우선순위

P0은 원 대화의 주된 얼굴 전달 목표와 혼동 위험을 해결하는 순서이다: 촬영 범위/방향 분리 → 얼굴·손·초점 소유자 → 맞은편 테이블과 방향 분리 → 전경 틈 → 유리/거울/손거울 분리 → 타인의 어깨/손 → 여백과 모션 대비. 이는 인기순위나 필수 추천 템플릿이 아니다.

P1은 몸과 배경의 그래픽 관계, 자세 지지, 국소 광학 변주이다. P2는 유행 표현의 날짜·근거 갱신과 다중 이미지 시리즈 계약이다. 한 장의 사진만 요청하면 다중 이미지 모드는 후보 노출에서 제외한다.

현재 research-only 결과에 대해 완료라고 말할 수 있는 것은 출처 회수, 용어 분해, 현재 사전 대조, 적용 초안 작성과 실행된 구조 검사이다. 검색 노출, 임베딩 일반화, 실제 후보팩 전달, 이미지 의미 성공, 사용자 매력 판단은 별도의 미검증 상태로 남긴다.

## 10. 출처 기록과 제한

'''
    text+='| ID | 자료 | 확인 범위 | 제한 |\n|---|---|---|---|\n'
    for s in sources:text+=f'| {s["id"]} | [{s["title"]}]({s["url"]}) | {s["supported_claim_ko"]} · `{s["access_status"]}` | {s["limits_ko"]} |\n'
    text+='\n참조 대화에 등장한 Rosie Lugg·Eletrico 관련 원문 URL은 조회된 대화에서 복원되지 않았고 이번 검색에서도 해당 Canon 원문을 확인하지 못했다. 이 이름들을 신규 기술 계약이나 유행 근거로 사용하지 않았다. Nina Collins 자료는 Canon Creator Lab 원문에서 확인했다. 일부 Canon SNAPSHOT와 Julieanne Kost 원문은 검색 발췌만 확인했으므로 위와 같이 열람 범위를 제한했다. 외부 참고 이미지의 픽셀·라이선스·데이터셋 수집 가능성은 이번에 조사·승인된 범위가 아니며 이미지를 수집하거나 학습 데이터라고 부르지 않았다.\n'
    (HERE/'report.md').write_text(text,encoding='utf-8')

if __name__=='__main__':build()
