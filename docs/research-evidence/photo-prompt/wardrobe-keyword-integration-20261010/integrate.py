"""Reviewed wardrobe relations. Research provenance stays outside runtime assets."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
RESEARCH = HERE.with_name('wardrobe-keyword-semantics-20261010')
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
sys.path.insert(0, str(SKILL / 'scripts'))
from photo_candidate_semantics import digest, MAINTENANCE_VERSION
from photo_runtime_sources import source_update


def load(path):
    return json.loads(path.read_text())


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


# These four keep their existing candidate identities. Other superficially close
# entries do not express the additional layer/contrast relation in the new card.
REUSE = {
    'WK024': ('photo_prompt_clothing_structure_extension.json', 'garment_detail', 'clt_ct037_v1'),
    'WK029': ('photo_prompt_clothing_structure_extension.json', 'garment_detail', 'clt_ct047_v1'),
    'WK038': ('photo_prompt_clothing_structure_extension.json', 'garment_detail', 'clt_ct031_v1'),
    'WK046': ('photo_prompt_visual_grammar_extension.json', 'garment_detail', 'vg_ribbon_to_garment_seam'),
}

LABELS = {
1:'같은 셔츠 앞판을 잇는 버튼 줄',3:'짧은 소매와 허리 위 밑단의 피티드 티',4:'열린 셔츠 안의 골지 민소매 상의',5:'반도 상의와 낮게 분리된 소매',6:'소매 있는 니트 위의 열린 조끼',7:'내층 상의를 드러내는 열린 셔츠와 접은 소매',8:'몸통에서 떨어져 늘어진 긴 겉옷',9:'열린 로브와 별도 드레스·속슬립',10:'검정 드레스 목선에서 내려오는 붉은 짧은 케이프',11:'착용 블라우스 옆 탁자에 놓인 블레이저',12:'두 아일릿 줄 사이의 보디스 레이싱',13:'주름 패널을 잇는 긴 치마의 티어 봉제선',15:'몸판과 하단이 이어진 수영복과 별도 등 개방부',17:'허리단에서 내려오는 치마 주름 능선',18:'허리 아래 겹친 러플과 측면 조절 채널',19:'뒤보다 짧은 앞밑단과 별도 사선 패널',20:'쇼츠 바깥에 겹친 곡선 오버스커트',21:'몸판 접합 위로 선 직립 칼라',22:'대각으로 겹쳐 V 목선을 만드는 앞판',23:'같은 상의의 목선 윤곽',25:'목선 안쪽을 따라가는 좁은 스캘럽 레이스',26:'몸판과 어깨·목 사이의 지지 연결',27:'높은 목선 아래를 둘러싼 키홀 가장자리',28:'같은 옷의 등 개방부를 둘러싼 천 가장자리',30:'같은 소매의 국소 퍼프 볼륨',31:'같은 소매의 길이와 처진 천',32:'위팔 밴드에 고정된 분리 시어 소매',33:'같은 소매 옆의 커프 가장자리',34:'몸통 접촉 사이에 처진 의상 주름',35:'같은 착용자의 무릎에 닿는 치마 밑단',36:'착용자 허리 기준의 허리단 위치',37:'같은 치마의 폭과 볼륨 분포',39:'같은 의상 표면의 별도 패널 가장자리',40:'겉패널 아래 드러나는 같은 치마 안감',41:'같은 의상의 개방부와 조절 끝점',42:'겹친 몸판 바깥의 짧게 묶인 허리띠',43:'저고리 앞섶을 묶는 고름과 별도 치마',44:'등에서 교차해 매듭으로 이어지는 에이프런 끈',45:'같은 바지의 지퍼·버튼·별도 주머니',47:'같은 천 표면의 얽힌 가는 실',48:'별도 내층이 읽히는 투광성 바깥 천',49:'부착 장식 아래 반복되는 메시 구멍',50:'직물 패널의 골과 매끈한 광택 대안',51:'같은 의상에서 대비되는 파일과 매끈한 반사 패널',52:'같은 크레이프형 패널의 불규칙한 미세 입자',53:'같은 니트 패널의 골·교차·작은 구멍 대안',54:'같은 데님 패널의 밝은 접힌 자국',55:'의상 곡면을 따라가는 광택과 별도 봉제선',56:'바탕천 안의 작은 구멍과 스캘럽 끝단',57:'스포츠 의상 패널의 메시와 별도 봉제선',58:'같은 직물 표면에 짜인 낮은 대비 문양',59:'같은 의상 패널과 주름을 따르는 반복 무늬',60:'같은 천 위 솟은 자수 실과 별도 버튼',61:'같은 저지 앞판에 찍힌 숫자 10',62:'같은 의상에 부착된 입체·반사 장식',63:'같은 의상 옆의 한 매듭과 두 리본 꼬리',64:'패널 내부와 구별되는 얇은 배색 파이핑',65:'같은 프릴 닳은 끝을 잇는 수선 실',66:'보디스 표면 한 접합점의 나비 장식',67:'배경과 경계가 분리된 아이보리 몸판',68:'같은 치마의 흰색에서 분홍색으로 이어지는 그라데이션',70:'같은 검정 의상 허리에서 시작하는 붉은 면 하나',72:'같은 금속 고리의 국소 어두운 면과 밝은 가장자리',73:'같은 검정 의상 내부의 질감·반사 대비',74:'같은 의상의 불투명 몸판과 시어 소매 접합',75:'같은 레그웨어의 상단 위치와 연결',76:'같은 착용자 양말 상단을 잡는 손가락',77:'같은 신발·다리의 스트랩 또는 샤프트 끝',78:'엄지와 나머지 발가락 쪽으로 갈라진 부츠 앞코',80:'두 고정점에서 가방을 지지하는 스트랩',81:'같은 헤어·헤드밴드에 부착된 장식',82:'같은 팔의 긴 장갑과 별도 의상 커프',83:'같은 착용자의 펜던트·브로치·목 장식 대안',84:'한쪽 긴 귀걸이와 반대쪽 작은 스터드',85:'같은 의상 두 고정점 사이 처진 체인',87:'올린 팔 옆 암홀로 모이는 셔츠 주름',88:'같은 치맛단을 아래로 당기는 손가락',89:'착용 블라우스 밑단의 주름을 잡는 손가락',90:'걸음 중 같은 치마 옆단을 잡아 드러난 안감',91:'주는 손과 받는 손 사이에 지지된 트레이 하나',92:'같은 그릇 옆에서 사탕 하나를 건네는 손',93:'얼굴 가까이 든 종이 음식 봉투와 열린 입구',94:'지지된 발과 열린 높은 찬장으로 뻗은 손',95:'의자와 접촉한 치마에 모인 압축 주름',96:'수면에 등을 댄 몸통 주변의 물 접촉',97:'방파제에서 틈을 두고 고양이를 보는 웅크린 인물',98:'고정점은 이어지고 같은 방향으로 뻗은 리본·치맛단',99:'같은 천 안 물 접촉부의 국소 어두운 값',100:'같은 닳은 접합 가장자리를 따라가는 바느질',101:'원 의상의 색·무늬가 이어진 떠 있는 천 조각',103:'양팔 밴드와 몸판의 틈이 보이는 허리 위 프레임',104:'위팔 밴드와 몸판 틈을 드러내는 사선 시점',105:'가까운 손과 뒤의 몸통 크기가 다른 원근',106:'어두운 배경 앞 직접 플래시와 살짝 기운 프레임',107:'직물 릴리프와 별도 금속을 드러내는 측면광',108:'밝은 배경에서 읽히는 흰 의상 봉제선·주름',109:'따뜻한 전경과 차가운 배경의 별도 광원',110:'천 골과 구별되는 균일한 영상 그레인',111:'어깨 일부를 가리고 리본 접합은 드러낸 전경 가장자리',113:'문턱을 넘으며 같은 치마 옆단을 잡는 상황',115:'열린 조끼 안의 별도 러플 셔츠',116:'열린 짧은 소매 커버업 안의 별도 수영복',117:'같은 허리를 감싸 매듭으로 끝나는 좁은 어두운 띠',118:'허리 접합 아래 한 벌로 이어지는 플레어 치마',119:'같은 힙 부분에서 내려오는 두 와이드 바짓단',121:'같은 타이를 가로질러 고정하는 타이바',122:'같은 손목의 시계와 별도 얇은 뱅글',123:'같은 무릎에서 굽어 뒤로 간 아랫다리',124:'같은 인물 눈 아래로 선글라스를 내리는 손',125:'크림 천 접합에 부착된 작은 어두운 금속 장식',
}

# Variant-specific endpoints replace the 53 unset prototype relations. No family
# label is an alias for all variants. Each row names a single observable relation.
VARIANTS = {
'wk023_crew':('크루넥','bounds','shallow rounded neckline edge','same neck base'),
'wk023_scoop':('스쿠프넥','opens_below','wide rounded neckline edge','same neck base'),
'wk023_square':('스퀘어넥','joins','two neckline corners','same horizontal lower neckline edge'),
'wk023_bateau':('보트넥','runs_near','broad shallow neckline','same collarbones'),
'wk023_asymmetric_bateau':('비대칭 보트넥','differs_in_height_across','broad neckline edge','same two shoulders'),
'wk026_strapless':('스트랩리스','bounds','continuous bodice upper edge','same torso'),
'wk026_off_shoulder':('오프숄더','sits_below','garment and sleeve attachment edges','same shoulder tops'),
'wk026_spaghetti':('스파게티 끈','joins_over','two narrow bodice straps','same shoulders between front and back bodice'),
'wk026_halter':('홀터','joins_at','same bodice support straps','neck attachment'),
'wk030_short_puff':('짧은 퍼프','gathers_between','rounded short sleeve fabric','same shoulder attachment and lower edge'),
'wk030_shoulder_puff_long':('어깨 퍼프 긴소매','widens_relative_to','same upper sleeve','narrow lower sleeve'),
'wk031_three_quarter':('칠부','ends_between','same sleeve hem','elbow and wrist on same forearm'),
'wk031_lower_drape':('팔꿈치 아래 드레이프','hangs_below','attached lower sleeve cloth','same elbow'),
'wk031_column':('긴 기둥형 주름','runs_between','same sleeve long folds','upper sleeve attachment and wrist edge'),
'wk033_lace_cuff':('레이스 커프','joins','lace cuff','same opaque sleeve wrist edge'),
'wk033_rolled':('롤업','folds_into','same shirt sleeve layers','forearm rolled edge'),
'wk033_detachable':('독립 흰 커프','closes_beside','separate white wrist cuff','same garment sleeve edge'),
'wk036_high':('하이웨이스트','sits_above','same waistband','wearer natural waist'),
'wk036_natural':('내추럴 웨이스트','follows','same waistband','wearer natural waist'),
'wk036_low':('로라이즈','sits_below','same waistband','wearer natural waist'),
'wk037_a_line':('A라인','widens_toward','same skirt side outlines','hem below waist'),
'wk037_bell':('벨 실루엣','rounds_below','same skirt outward volume','gathered waistband above returning hem'),
'wk037_narrow_layers':('좁은 겹치마','hangs_within','two distinct skirt layers','same narrow outer silhouette'),
'wk037_lower_volume':('하단 볼륨','widens_below','same gown lower skirt','narrow upper bodice'),
'wk039_diagonal':('사선 겹침','overlaps','same skirt diagonal panel edge','adjacent skirt panel'),
'wk039_crescent':('초승달 패널','bounds','crescent textile edge','same attached panel'),
'wk039_curved_overlay':('부츠 곡선 오버레이','follows','separate curved leather-like overlay','same boot surface'),
'wk041_slit':('슬릿','separates_between','single skirt opening','upper endpoint and hem on same skirt'),
'wk041_wrap_gap':('랩 틈','lies_between','visible skirt gap','same skirt overlapping panels'),
'wk041_drawstring':('드로스트링','emerges_and_joins_at','two cord ends','same gathered side channel adjustment point'),
'wk050_faille_surface':('파유형 골','runs_across','fine transverse ribs','same faille-like textile panel'),
'wk050_satin_surface':('새틴형 광택','follows','broad smooth sheen','same satin-like panel folds'),
'wk053_rib':('골지','runs_along','parallel raised knit ribs','same garment panel'),
'wk053_cable':('케이블','crosses_along','raised knit columns','same sweater panel'),
'wk053_pointelle':('포인텔','opens_within','ordered small knit openings','same sock panel'),
'wk059_floral':('꽃무늬','repeats_within','small flower motifs','same garment panel folds'),
'wk059_plaid':('체크','intersects_on','two stripe directions','same skirt panel checks'),
'wk059_pinstripe':('핀스트라이프','repeats_along','thin parallel stripes','same skirt panel fold direction'),
'wk062_petal_relief':('꽃잎 입체','rises_above','attached flower petals','same fabric surface'),
'wk062_rhinestone':('라인스톤','attaches_at','small faceted reflective ornaments','same garment distinct attachment points'),
'wk062_pearl_like':('진주형','attaches_at','small rounded pearl-like ornaments','same garment distinct attachment points'),
'wk075_knee_sock':('무릎 아래 양말','ends_below','same knitted sock top edge','same knee'),
'wk075_thigh_high':('허벅지 레그웨어','ends_above','same legwear top band','same knee on thigh'),
'wk075_tights':('타이츠','continues_into','same legwear two legs','same covered hip section'),
'wk077_mary_jane':('메리제인','crosses_and_joins','same shoe instep strap','same shoe fastening point'),
'wk077_ankle_sandal':('발목 샌들','wraps_and_joins','same sandal ankle strap','same sandal supporting straps'),
'wk077_knee_boot':('무릎 부츠','ends_near','same boot shaft','knee beside separate legwear edge'),
'wk081_horn_headband':('뿔 헤드밴드','attaches_to','two costume horns','same visible headband'),
'wk081_bunny_headband':('토끼귀 헤드밴드','attaches_to','two long costume ears','same visible headband'),
'wk081_hair_ribbon':('헤어 리본','joins','hair ribbon knot and tails','same hair fastening'),
'wk083_pendant':('펜던트','hangs_from','distinct pendant','same wearer chain'),
'wk083_brooch':('브로치','attaches_at','brooch','same garment single visible point'),
'wk083_neck_armor':('갑옷형 목 장식','surrounds_above','separate armor-like collar','same neck above garment neckline'),
}

# Resolve research variables to usable choices, and keep unknowable annotations
# out of the positive retrieval text. A supported example is not a universal rule.
TEXT = {
'WK026:strapless':'A continuous upper edge crosses the same bodice; its front and side panels remain joined around the torso.',
'WK035':'The same skirt hem reaches the wearer\'s knee, with the knee and textile edge visible together.',
'WK045':'A closed zipper joins the same trousers\' front edges below the waistband button; the pocket opening remains a separate edge.',
'WK047':'Fine interlaced yarns remain visible across the same textile surface beside its stitched edge.',
'WK051':'The same garment has a soft directional pile panel beside a separate smooth reflective panel; their joining edge remains visible.',
'WK066':'A butterfly-shaped ornament attaches to the same bodice panel at one visible junction.',
'WK067':'The ivory color remains on the same bodice panel, whose textile edge separates it from the blue background.',
'WK068':'The same skirt surface changes from white at the waist to pale pink at its hem along one continuous vertical gradient.',
'WK070':'One saturated red fabric plane begins at the same black garment\'s waist attachment and extends down one side; the remaining garment panels stay black.',
'WK075:tights':'The same tights extend from both legs into one hip section, with the upper textile boundary readable at the waist.',
'WK080':'The same bag\'s strap supports its body from two visible attachment fittings.',
'WK082':'The long glove ends above the same elbow, with a separate garment cuff edge beside it.',
'WK087':'The same person raises one arm; folds in that person\'s shirt converge toward the armhole beneath the raised arm.',
'WK091':'One tray rests on the giver\'s hands while the receiver\'s hands approach its opposite edge; the two people remain distinct.',
'WK092':'The giver holds a bowl and extends one wrapped candy toward the receiver\'s approaching hand.',
'WK094':'The same person stands with both feet on the floor and reaches one connected arm toward an open upper cabinet.',
'WK095':'The seated person\'s skirt gathers into compressed folds where the same skirt meets the chair seat.',
'WK096':'The person floats with the back at the water surface; visible water contact traces the sides of the supported torso.',
'WK098':'The same skirt hem and its attached ribbon\'s free tail extend toward the same side; the ribbon knot and skirt waistband remain attached.',
'WK101':'A suspended textile fragment carries the same floral print and color as the visible edge of the source dress beside it.',
'WK103':'A waist-up frame includes both upper-arm sleeve bands and the visible gaps separating those sleeves from the bodice.',
'WK104':'A front three-quarter viewpoint keeps the upper-arm sleeve band, its separate sleeve, and the gap beside the bodice visible.',
'WK105':'The hand nearest the camera appears larger than the same person\'s torso behind it in the close, wide-perspective frame.',
'WK107':'Side light casts small shadows along the same garment\'s raised embroidery while its separate metal buttons carry sharper highlights.',
'WK110':'Fine image grain is spread across the frame while the sweater\'s raised knit ribs stay distinct local textile relief.',
'WK111':'A foreground door edge overlaps part of the shoulder while the ribbon knot and its garment-seam junction remain visible beside it.',
'WK113':'At the raised doorway threshold, the person holds the same skirt\'s side edge above that threshold while stepping across it.',
}

RELATIONS = {
'WK035':[('ends_at','same skirt hem','same wearer visible knee')],
'WK045':[('joins_below','closed trouser zipper','same waistband button'),('is_separate_from','same trousers pocket opening','front zipper edge')],
'WK047':[('forms','fine interlaced yarns','same textile surface beside stitched edge')],
'WK066':[('attaches_at','butterfly-shaped ornament','same bodice visible junction')],
'WK067':[('belongs_to','ivory surface region','same bodice panel'),('ends_at','same ivory panel','textile edge beside blue background')],
'WK068':[('changes_along','same skirt white-to-pink gradient','vertical waist-to-hem axis')],
'WK070':[('extends_from','one saturated red fabric plane','same black garment waist attachment'),('remains_separate_from','same single red plane','other black garment panels')],
'WK075:tights':[('continues_into','same tights two legs','one hip section with waist textile boundary')],
'WK080':[('supports_at','same bag strap','bag body two attachment fittings')],
'WK082':[('ends_above','same long glove upper edge','same elbow beside garment cuff')],
'WK091':[('rests_on','one tray','giver hands'),('is_approached_by','same tray opposite edge','distinct receiver hands')],
'WK092':[('offers_toward','giver hand with one wrapped candy','receiver approaching hand'),('is_held_by','same bowl','giver other hand')],
'WK094':[('supports','floor','same person two feet'),('reaches_toward','same person connected arm','open upper cabinet')],
'WK095':[('gathers_at','same skirt compressed folds','same chair-seat contact')],
'WK096':[('meets','same person back and torso sides','water surface')],
'WK098':[('extends_same_direction_as','attached ribbon free tail','same skirt hem'),('remains_attached_to','same ribbon knot','same garment attachment')],
'WK101':[('matches','suspended fragment floral print and color','source dress visible edge')],
'WK103':[('includes','waist-up frame','both sleeve bands and gaps beside same bodice')],
'WK104':[('projects_visibly','front three-quarter camera','same upper-arm band sleeve and bodice gap')],
'WK105':[('appears_larger_than','same person near hand','same person farther torso')],
'WK107':[('casts_shadows_on','side light','same garment raised embroidery'),('produces_highlights_on','same side light','separate metal buttons')],
'WK110':[('is_separate_from','frame-wide fine image grain','same sweater local raised knit ribs')],
'WK111':[('overlaps','foreground door edge','part of same shoulder'),('leaves_visible','same foreground door edge','ribbon knot and seam junction')],
'WK113':[('holds_above','same person hand and skirt side edge','raised doorway threshold')],
}


def endpoint(value):
    value = re.sub(r'_([AB])\b', '', value)
    return value.replace('_', ' ').replace('.', "'s ")


def effect_review(card, draft, suffix):
    dims = list(draft['affected_dimensions'])
    props = copy.deepcopy(draft['affected_properties'])
    # Relations that name cloth motion, limbs or additional scene objects carry
    # those effects too. Never change identity, age or species to fit a candidate.
    extra = {}
    num = int(card['id'][2:])
    if num in {15,32,48,74,116}:
        extra['material'] = ('main_subject','wardrobe.material.transmission')
    if num in {3,4,5,6,7,8,9,10,12,13,15,17,18,19,20,21,22,23,25,26,27,28,30,31,32,33,34,35,36,37,39,40,41,42,43,44,45,115,116,117,118,119}:
        extra['appearance'] = ('main_subject','wardrobe.garment_type')
    if num in {47,48,49,50,51,52,53,54,55,56,57,58,60,72,73,74}:
        extra['material'] = ('main_subject','wardrobe.material.appearance')
    if num in {61}:
        extra['text'] = ('main_subject','wardrobe.printed_text')
    if num in {67,68,70}:
        extra['color'] = ('main_subject','wardrobe.color')
    if num in {11}:
        extra['appearance'] = ('main_subject','wardrobe.blouse')
        extra['setting'] = ('scene','props.blazer_and_support')
    if num in {63,66,80,81,82,83,84,85,121,122,125}:
        extra['appearance'] = ('main_subject','accessories')
    if num == 39 and suffix == 'curved_overlay':
        props = [{'dimension':'appearance','target':'main_subject','property':'footwear.overlay'}]
        extra={'appearance':('main_subject','footwear.boot')}
    if num == 53 and suffix == 'pointelle':
        extra['appearance'] = ('main_subject','legwear.sock')
    if num == 75 and suffix == 'tights':
        extra['framing'] = ('scene','legwear_upper_boundary_visibility')
    if num in {76,87,88,89,90,94,97,123,124}:
        extra['pose'] = ('main_subject','posture.limb_contact')
    if num in {76,88,89,90}:
        extra['material'] = ('main_subject','wardrobe.local_contact_folds')
    if num in {91,92}:
        extra['setting'] = ('scene','props.exchange')
        extra['pose'] = ('*','posture.exchange_contact')
        # Both actors are prerequisites. This entry does not introduce a person
        # on a locked count/subject merely to make its scene possible.
    if num in {93,94,96,97}:
        extra['setting'] = ('scene','spatial_support_and_props')
    if num in {95,96,97}:
        extra['pose'] = ('main_subject','posture.body_support')
    if num in {98,99,101}:
        extra['material'] = ('main_subject','wardrobe.material.state')
    if num in {103,104}:
        extra['appearance'] = ('main_subject','wardrobe.detached_sleeves')
    if num in {105}:
        extra['pose'] = ('main_subject','posture.near_hand')
    if num in {107,108,110}:
        extra['appearance'] = ('main_subject','wardrobe.surface')
    if num == 107:
        extra['appearance'] = ('main_subject','wardrobe.embroidery_and_buttons')
    if num == 108:
        extra['color'] = ('main_subject','wardrobe.color')
    if num == 111:
        extra['setting'] = ('scene','props.foreground_door')
        extra['appearance'] = ('main_subject','wardrobe.ribbon_seam_junction')
    if num == 113:
        extra['action'] = ('main_subject','step_and_cloth_contact')
        extra['pose'] = ('main_subject','posture.step')
        extra['appearance'] = ('main_subject','wardrobe.hem_displacement')
    # Existing prototypes included an attention change that pulling a hem does
    # not actually require. Remove that unnecessary restriction.
    if num == 88:
        dims = [x for x in dims if x != 'relationship']
        props = [x for x in props if x['dimension'] != 'relationship']
    # A limb articulation changes pose, not the person's body morphology.
    if num == 123:
        dims = [x for x in dims if x != 'body_geometry']
        props = [x for x in props if x['dimension'] != 'body_geometry']
    for dim, (target, prop) in extra.items():
        if dim not in dims: dims.append(dim)
        row={'dimension':dim,'target':target,'property':prop}
        if row not in props: props.append(row)
    if num in {15,32,48,74,116}:
        # Material transmission and visible opacity are the same protected
        # wardrobe property across carriers, even when another material effect
        # was added for the texture of this particular variant.
        for dim in ['appearance','material']:
            if dim not in dims: dims.append(dim)
            for prop in ['wardrobe.material.transmission','wardrobe.opacity']:
                row={'dimension':dim,'target':'main_subject','property':prop}
                if row not in props: props.append(row)
    # Parent properties cover multiple declared visual changes conservatively.
    # Keep cross-carrier ownership consistent for camera viewpoint locks.
    for row in props:
        if row['dimension']=='camera': row['target']='camera'
    return dims, props


def main():
    cards = {x['id']:x for x in load(RESEARCH/'SEMANTIC-CARDS.json')['cards']}
    drafts = load(RESEARCH/'CANDIDATE-BLUEPRINTS.json')['drafts']
    extension={'schema_version':'photo-prompt-research-extension/v1','slots':{},'visual_semantics':[]}
    profiles={'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','profiles':[]}
    rows=[]
    annotations=[]
    for card in cards.values():
        if card['observation_mode']=='annotation_or_context_only':
            annotations.append({'card_id':card['id'],'disposition':'maintenance_only_no_candidate_or_profile','annotation':card,'source_keyword_ids_are_aliases':False})
    for draft in drafts:
        card=cards[draft['card_id']]
        if card['id'] in REUSE:
            filename,slot,cid=REUSE[card['id']]
            old=next(x for x in load(ASSETS/filename)['slots'][slot] if x['id']==cid)
            rows.append({'card_id':card['id'],'draft_id':draft['id'],'decision':'reuse_existing_candidate_identity','candidate_id':cid,'source_file':filename,'source_row_sha256':digest(old),'original_card':card})
            continue
        suffix=draft['id'].removeprefix('draft_'+card['id'].lower()+'_')
        key=card['id']+':'+suffix
        text=TEXT.get(key,TEXT.get(card['id'],draft['candidate_text_en']))
        label=LABELS[int(card['id'][2:])]
        vkey=draft['id'].removeprefix('draft_')
        if vkey in VARIANTS:
            variant_ko,typ,subject,obj=VARIANTS[vkey]
            label=label+' · '+variant_ko
            pairs=[(typ,subject,obj)]
        else:
            pairs=[(r['type'],endpoint(r['subject']),endpoint(r['object'])) for r in draft['relations']]
        pairs=RELATIONS.get(key,RELATIONS.get(card['id'],pairs))
        cid='wkr_'+vkey+'_candidate'
        pid='wkr_'+vkey
        # Unsupported fiber chronology or hidden support is not positive prose.
        units=[x.strip() for x in text.split(';') if x.strip()]
        relations=[{'id':f'{pid}_relation_{i+1}','type':t,'subject':s,'object':o} for i,(t,s,o) in enumerate(pairs)]
        assert relations and all(r['subject'] and r['object'] for r in relations)
        dims,props=effect_review(card,draft,suffix)
        entry={'id':cid,'ko':label,'en':text,'weight':0.35,
               'tags':['clothing'] if card['group'] not in {'capture','scene','action'} else ['photography'],
               'aliases':[label,text],'keywords':[label,*units],'paraphrases':[text],
               'embedding_text':text,'concept_terms':[label,*units],
               'concept_units':units,'relations':relations,
               'affected_dimensions':dims,'affected_properties':props,
               'core_assertion_discovery':True,'for_any':['human'],
               'contextual_usage':{'contexts':[{'id':'selected_owner_relation','observable_interpretation':text,
                  'claim_limits':['Every named actor, garment, body part and support must already exist or be developed within the declared open effects. A candidate does not add an undeclared person or species.',
                                  'One still image establishes visible geometry and local surface appearance, not fiber chemistry, force, chronology, identity or private motive.',
                                  'This is one optional realization; neighboring variants remain independent choices.'],
                  'activation_authority':'interpretation_only_not_required'}]}}
        if card['id'] in {'WK091','WK092'}:
            entry['contextual_usage']['contexts'][0]['claim_limits'].insert(0,'The scene must contain two distinct permitted human actors before this exchange candidate is adopted; its effects do not authorize a new actor.')
        slot=draft['slot'];extension['slots'].setdefault(slot,[]).append(entry)
        components=[{'id':f'component_{i+1}','match_terms':[unit],'evidence_field':f'component_{i+1}_phrase',
                     'evidence_terms':[unit],'min_content_words':3,
                     'instruction':'Keep the selected owner and complete visible relation together: '+unit,
                     'render_gate':{'id':f'vo_{pid}_{i+1}','review_scale':'native',
                         'description':unit+' Inspect the declared owner, both endpoints and the connecting edge or distinguishing state in this same image. Hidden or partial evidence fails.'}}
                    for i,unit in enumerate(units)]
        p={'id':pid,'category':'wardrobe_owner_selected_relation',
           'activation':{'exact_terms':[text],'requires_adult_character':False,'semantic_discovery_requires_component_evidence':True,
              'hard_activation':{'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[{'id':'complete_selected_relation','any_terms':[text]}]}},
           'semantics':{'definition':text,'paraphrase_examples':[label],
              'visual_components':units,'contrast_examples':card['confusion_boundaries_ko'],
              'claim_limits':['A complete selected relation; broad garment labels, palette inventories and historical combinations create no automatic duty.',
                              'Only the visible owner, endpoints and state can be assessed; hidden manufacture, identity and temporal claims need separate evidence.']},
           'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':components},
           'concept_candidate':{'concept_terms':[label,*units],'core_assertion_discovery':True,'affected_dimensions':dims,'affected_properties':props},
           'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
           'reject_substitutes':card['confusion_boundaries_ko']}
        profiles['profiles'].append(p)
        extension['visual_semantics'].append({'id':pid+'_bundle','primary_visual_proposition':text,'hard_profile_ids':[pid],
            'component_groups':[{'id':c['id'],'visible_evidence':[c['evidence_terms'][0]]} for c in components],
            'candidate_ids':[cid],'candidate_slots':{cid:slot},'confusion_boundaries':card['confusion_boundaries_ko'],
            'source_keywords':[label,text],'candidate_only':True,'activation_mode':'component_complete_exact_only','relations':relations})
        rows.append({'card_id':card['id'],'draft_id':draft['id'],'decision':'add_reviewed_selected_variant',
            'candidate_id':cid,'profile_id':pid,'bundle_id':pid+'_bundle','slot':slot,'reviewed_text':text,
            'variant_endpoints_settled':True,'complete_effects_reviewed':True,'affected_dimensions':dims,
            'affected_properties':props,'relations':relations,'original_card':card,'native_pixels_verified':False})
    candidate_file='photo_prompt_wardrobe_owner_relations_extension.json'
    profile_file='photo_prompt_visual_obligations_wardrobe_owner_relations.json'
    record_id='wardrobe-owner-relations-20261010-v1'
    decisions={'schema_version':'wardrobe-owner-integration-decisions/v1','rows':rows,'annotations':annotations,
       'source_catalog_sha256':hashlib.sha256((RESEARCH/'inputs/wardrobe_keyword_catalog.json').read_bytes()).hexdigest(),
       'source_catalog_scope':'503 normalized headwords from 45 selected library items; original library inputs not independently reopened',
       'past_combinations':load(RESEARCH/'COMBINATION-ANALYSIS.json'),
       'past_exclusions':load(RESEARCH/'CONTEXT-BOUNDARIES.json'),
       'default_global_exclusion_added':False,'runtime_seed_aliases_added':False}
    record={'schema_version':'photo-extension-maintenance/v1','record_id':record_id,'maintenance_only':True,
       'source_filename':candidate_file,'authored_source_sha256':digest(extension),
       'profile_filename':profile_file,'profile_source_sha256':digest(profiles),
       'decisions_sha256':digest(decisions),
       'research_sources_sha256':digest(load(RESEARCH/'SOURCES.json')),
       'source_card_ids':[x['card_id'] for x in rows],
       'affected_candidate_ids':[x['candidate_id'] for x in rows],
       'source_urls':[x['url'] for x in load(RESEARCH/'SOURCES.json')['sources']],
       'limits':['Research citations are bounded support, not original prompt revalidation.','11 annotations and 23 past exclusions stay external.','150 drafts reviewed: 4 candidate identities reused; new variants have explicit endpoints and reviewed effects.','Native qualification is recorded per generated case, not for every candidate.']}
    extension['maintenance_ref']={'contract_version':MAINTENANCE_VERSION,'record_id':record_id,'sha256':digest(record)}
    manifest=load(ASSETS/'photo_prompt_source_manifest.json')
    for filename,kind,required in [(candidate_file,'candidate',True),(profile_file,'visual_profile',True)]:
        if any(x['file']==filename for x in manifest['sources']): raise SystemExit('already registered; refusing overwrite')
        order=max(x['load_order'] for x in manifest['sources'] if x['kind']==kind)+1
        manifest['sources'].append({'file':filename,'kind':kind,'required':required,'load_order':order})
    # Hash preservation protects concurrent source editors between read and write.
    before=load(HERE/'PRIMARY-BEFORE.json')['assets_before']
    rel=str((ASSETS/'photo_prompt_source_manifest.json').relative_to(ROOT))
    if hashlib.sha256((ASSETS/'photo_prompt_source_manifest.json').read_bytes()).hexdigest()!=before[rel]:
        raise SystemExit('manifest advanced since task snapshot; rebase reviewed additive registration')
    with source_update(SKILL):
        write(HERE/'INTEGRATION-DECISIONS.json',decisions)
        write(ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/f'{record_id}.json',record)
        write(ASSETS/candidate_file,extension)
        write(ASSETS/profile_file,profiles)
        write(ASSETS/'photo_prompt_source_manifest.json',manifest)
    summary={'research_cards':len(cards),'visible_cards':len({x['card_id'] for x in rows}),
       'new_candidates':sum(len(x) for x in extension['slots'].values()),'new_profiles':len(profiles['profiles']),
       'new_bundles':len(extension['visual_semantics']),'reused_candidates':len(REUSE),'external_annotations':len(annotations),
       'slots':{s:len(x) for s,x in extension['slots'].items()},'generation_tests_requested':3,'indexes_rebuilt':False}
    write(HERE/'INTEGRATION-COUNTS.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
