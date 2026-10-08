"""Apply reviewed selfie research as authored sources; never write indexes here."""
from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
RESEARCH = OUT.parent / 'selfie-pose-semantics-20261008'
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
from photo_candidate_semantics import validate_candidate_entries, validate_extension_keys, digest
from visual_profile_contracts import validate_visual_profile_source, compile_visual_profile
from photo_source_manifest import SourceInventory
from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS

def read(path): return json.loads(path.read_text())
def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

# Positive observations, not aliases. English component terms remain preserved.
KOREAN = {
22:['손바닥이 볼 아래와 옆면에 닿는다','손바닥과 볼의 접점에서 볼 윤곽이 살짝 눌린다','팔뚝이 같은 손목까지 이어진다'],
23:['접힌 손가락의 주먹 윗면이 턱 아래에 닿는다','턱과 손가락 마디의 접점이 함께 보인다','주먹과 손목이 같은 팔에 이어진다'],
26:['한 손의 펼친 손바닥이 턱 아래에 놓인다','펴진 손가락이 턱 옆으로 벌어진다','반대 손은 이 꽃받침 구성에 포함되지 않는다'],
27:['엄지가 턱 아래를 따라 놓인다','검지는 볼 옆으로 올라가 엄지와 L자를 만든다','나머지 손가락은 같은 손바닥 쪽으로 접힌다'],
29:['엄지와 검지 끝이 볼의 작은 피부 부위 양쪽에 닿는다','두 손가락 사이의 볼 표면이 국소적으로 모인다','코와 입의 나머지 윤곽은 별도로 유지된다'],
30:['한 손바닥이 한쪽 볼 바깥에 닿는다','다른 손바닥이 반대쪽 볼 바깥에 닿는다','두 손과 손목의 소유가 같은 인물로 이어진다'],
31:['손목이 느슨하게 굽혀져 손이 얼굴 가까이에 놓인다','손가락은 주먹처럼 꽉 닫히지 않고 느슨하게 말린다','손이 자신의 손목과 팔에 이어진다'],
32:['검지 끝이 입술 바깥 가장자리에 닿는다','검지는 입 안으로 들어가지 않고 입술 옆에 놓인다','손목과 입술의 접점이 같은 화면에서 구별된다'],
37:['손바닥이나 손가락이 이마에 닿는다','손목은 이마에서 같은 팔로 이어진다','선택한 눈과 입의 영역이 손 아래로 구별된다'],
38:['펴진 손이 눈썹 위에 놓인다','손바닥의 면이 이마 앞쪽을 따라 향한다','눈은 손 아래의 남은 영역에 보인다'],
42:['검지와 중지가 눈 바깥쪽에 가로로 벌어진다','V자 틈이 눈 옆의 빈 공간과 이어진다','약지와 새끼손가락은 같은 손바닥 쪽으로 접힌다'],
43:['검지와 중지가 턱 아래에서 V자로 벌어진다','V자 두 손가락은 턱과 겹치지 않는 아래 영역에 놓인다','접힌 나머지 손가락과 손목이 같은 손에 이어진다'],
47:['양손 각각의 검지와 중지가 V자로 벌어진다','한 손이 다른 손보다 높은 위치에 놓인다','두 손은 각각 자신의 손목과 팔에 이어진다'],
49:['펴서 모은 손가락들이 이마 바깥 가장자리 옆에 놓인다','손끝의 방향과 손목의 연결이 보인다','다른 손의 위치는 별도로 유지된다'],
50:['엄지와 새끼손가락이 서로 벌어져 펴진다','검지와 중지와 약지는 손바닥 쪽으로 접힌다','두 펴진 손가락이 같은 손에서 갈라진다'],
52:['한 손이 볼 옆에서 반쪽 하트의 곡선을 만든다','볼 윤곽과 손의 곡선이 옆으로 이어진다','손은 같은 인물의 손목에 연결된다'],
53:['양손이 각각 양 볼 옆에서 곡선을 만든다','각 곡선과 대응하는 볼의 윤곽이 나란히 보인다','두 손의 손목이 각각 자신의 팔에 이어진다'],
57:['한 손이 반쪽 하트의 곡선을 만든다','열린 반쪽 옆에 다른 손이 들어갈 빈 공간이 남는다','빈 공간은 완성된 양손 하트와 구별된다'],
58:['작은 하트 모양의 손가락 틈이 한쪽 눈 앞에 놓인다','눈이 그 빈 공간 안에서 보인다','하트 틈과 눈과 손목의 소유가 함께 구별된다'],
60:['검지가 촬영 렌즈 방향으로 뻗는다','나머지 손가락은 같은 손에서 접히거나 따로 선택된 형태를 유지한다','전경 손가락과 뒤쪽 얼굴 사이의 깊이가 구별된다'],
62:['손가락이 이마 위 머리카락 사이에 놓인다','머리카락이 손가락의 진행 방향을 따라 옮겨진다','손목은 자신의 팔에 이어지고 머리카락은 같은 두피에 붙어 있다'],
63:['손가락들이 이미 있는 포니테일을 감싼다','묶인 머리카락이 두피의 묶음 뿌리에서 손의 그립까지 이어진다','손과 머리카락의 접점이 보인다'],
64:['손가락이 같은 두피에서 이어진 한 가닥의 머리카락에 닿는다','그 가닥은 손가락 옆이나 둘레로 휘어진다','나머지 머리카락의 길이와 색은 유지된다'],
68:['손가락이 이미 착용한 선글라스 프레임을 잡는다','프레임이 눈보다 낮아져 눈 일부가 위로 보인다','안경 다리는 같은 얼굴의 귀 방향으로 이어진다'],
69:['손가락이 이미 착용한 안경 프레임의 코받침이나 다리에 닿는다','렌즈와 눈과 프레임이 별도로 구별된다','그립한 손은 자신의 손목으로 이어진다'],
70:['손가락이 이미 착용한 모자의 챙을 잡는다','모자 챙은 같은 모자의 크라운에 이어진다','챙과 손의 접점이 얼굴 가까이에서 보인다'],
72:['얼굴의 위쪽 면이 약간 내려다보이는 시점으로 보인다','얼굴 아래쪽의 투영은 그보다 약하게 드러난다','주변 공간의 깊이 단서가 같은 시점에 맞는다'],
75:['얼굴 아래쪽 면이 위로 바라보는 시점으로 보인다','머리 위 공간이 얼굴 뒤로 이어진다','몸통과 얼굴의 투영이 같은 낮은 시점에 맞는다'],
79:['이미지의 한쪽 끝선이 얼굴 한쪽을 가로질러 자른다','얼굴의 나머지 반쪽이 프레임 안에 남는다','잘린 경계는 손이나 폰으로 가리는 경계와 구별된다'],
80:['인물의 투영 면적이 주변 공간보다 작게 놓인다','주변 장소를 알아볼 수 있는 넓은 영역이 남는다','인물과 배경의 겹침이 같은 촬영 시점에 맞는다'],
88:['머리와 어깨 뒤에 하늘이 보인다','인물의 얼굴 아래쪽이 올려다보이는 투영으로 드러난다','몸과 하늘의 겹침이 같은 시점에 맞는다'],
89:['인물이 방 전체의 화면 면적 중 작은 부분을 차지한다','방 모서리와 바닥 선이 넓은 영역에 걸쳐 보인다','인물과 방의 투영 크기가 같은 시점에 맞는다'],
98:['반사된 인물이 거울의 한쪽 측면에 놓인다','거울 중앙에 인물이 차지하지 않은 영역이 남는다','그 빈 공간에 같은 방의 반사가 이어진다'],
100:['크롭이 이미 지정된 상의 영역을 중심으로 자른다','이미 있는 칼라나 목걸이 또는 소매의 선택한 디테일이 크롭 안에 남는다','얼굴은 그 선택한 상의 크롭 밖에 놓일 수 있다'],
102:['한 발이 다른 발보다 지면 위에서 앞에 놓인다','뒤쪽 다리는 별도로 정한 지지 역할을 유지한다','골반은 두 다리의 경로 위에 연결된다'],
103:['선 자세에서 종아리가 발목 가까이 교차한다','각 발이 자신의 교차한 정강이 끝으로 이어진다','좌면 없이 서 있는 발의 바닥 접점이 구별된다'],
112:['앉은 자세에서 한쪽 무릎이 다른 무릎보다 높다','각 무릎이 자신의 허벅지와 정강이에 이어진다','골반의 좌면 또는 바닥 지지가 따로 보인다'],
113:['한 무릎이 위로 서고 반대 다리는 낮게 접힌다','선 무릎이 같은 다리의 정강이와 발에 이어진다','골반은 바닥이나 좌면에 지지된다'],
117:['골반이 의자 좌면의 앞쪽에 닿는다','허벅지가 그 앞쪽 접점에서 두 무릎으로 이어진다','의자 등받이는 골반 뒤쪽에 따로 보인다'],
120:['골반은 소파 앞의 바닥에 놓인다','등이 같은 소파의 앞면에 닿는다','다리와 소파 좌면이 서로 다른 높이에 보인다'],
126:['한쪽 팔이 굽혀져 손이 머리 뒤쪽에 놓인다','팔꿈치가 머리의 옆이나 위에 이어진다','반대 팔은 이 한 팔 구성에 포함되지 않는다'],
132:['손이 이미 요청된 음식이나 도구를 잡는다','음식은 얼굴 전체를 덮지 않는 옆 영역에 놓인다','얼굴과 소품이 각각 알아볼 수 있는 영역으로 남는다'],
134:['손이 꽃의 줄기를 잡는다','꽃머리가 코 아래 또는 볼 옆에 놓인다','코나 눈의 방향이 같은 꽃을 향한다'],
136:['손이 칫솔 손잡이를 잡는다','칫솔모가 입술 틈의 치아 쪽에 닿는다','치아와 칫솔과 입술의 경계가 구별된다'],
137:['한 다리가 선택한 한 걸음의 단계에서 앞으로 나간다','발의 접지나 지면에서 떨어진 틈이 그 단계에 맞는다','몸통이 두 다리의 경로 위에서 이어진다'],
138:['머리카락 가닥들이 두피의 뿌리에서 옆으로 휘어진다','가닥들은 같은 머리에 붙어 있다','선택한 눈과 입이 가닥 사이로 구별된다'],
141:['두 얼굴이 비슷한 깊이에 나란히 놓인다','각 얼굴이 겹침 사이에서도 따로 보인다','두 얼굴의 투영 크기가 선택한 시점에 맞는다'],
147:['앞쪽 반사 인물이 촬영 폰을 잡는다','다른 반사 얼굴들이 서로 다른 뒤쪽 위치에 보인다','모든 인물과 폰이 같은 물리 거울 공간을 공유한다'],
149:['요청된 얼굴들 중 다수가 같은 표정 구성을 보인다','지정한 한 얼굴만 대비되는 표정을 보인다','각 얼굴이 자신의 몸에 이어진다'],
150:['사람이 이미 요청된 동물 옆으로 몸을 낮춘다','동물의 눈이 사람 얼굴 높이 가까이에 놓인다','두 피사체의 투영이 같은 눈높이 시점에 맞는다'],
151:['이미 있는 오프숄더 의상의 경계 위로 선택한 어깨가 보인다','그 어깨가 촬영 렌즈 쪽으로 약간 돌아선다','목과 얼굴이 같은 어깨선에서 이어진다'],
161:['양팔의 전완이 몸통 앞에서 교차한다','각 손이 자신의 교차한 팔 끝으로 이어진다','어깨 높이는 그 교차와 별도로 선택된 상태를 유지한다'],
163:['양팔꿈치가 몸통 양옆으로 굽혀져 올라간다','각 주먹은 같은 쪽의 굽힌 팔 끝에 놓인다','상완과 어깨의 연결이 양쪽에서 보인다'],
164:['양손의 주먹이 얼굴 앞과 옆에 올라간다','팔꿈치와 전완이 같은 쪽 주먹으로 이어진다','두 주먹 사이에 얼굴 일부가 보인다'],
171:['넓은 창에서 오는 빛이 인물 앞쪽의 얼굴 면을 비춘다','얼굴의 밝음과 그림자 경계가 부드럽게 바뀐다','몸의 방향은 광원 방향과 별도로 유지된다'],
172:['창을 향한 얼굴 면이 반대 면보다 밝다','광원은 인물의 한쪽 옆에 놓인다','고개 회전은 창의 위치와 별도로 유지된다'],
173:['얼굴 한쪽이 다른 쪽보다 밝다','밝음과 어둠의 경계가 얼굴 중앙 가까이에 놓인다','눈과 코와 입이 그 밝기 경계와 함께 구별된다'],
174:['머리카락 가장자리에 밝은 테두리나 투과광이 보인다','밝은 가닥은 같은 머리카락 뿌리로 이어진다','얼굴 노출은 그 테두리와 별도로 유지된다'],
177:['평행한 그림자 띠가 지정된 얼굴이나 몸 영역을 가로지른다','그 띠가 받는 표면의 굴곡을 따라 변한다','창틀이나 블라인드의 배열이 같은 띠 방향과 맞는다'],
}

# Actual input conditions stay in evidence. Profiles observe their projections.
PIXEL_OVERRIDES = {
72:['upper face planes are viewed from a mildly elevated perspective','the lower face planes show the corresponding mild downward projection','surrounding depth cues agree with that same viewpoint'],
75:['the underside of face planes is visible from a lower perspective','upper room or sky extends behind the head','face and torso projection agree with one upward viewpoint'],
79:['frame edge cuts through one lateral face region','the other face region remains inside the image','the remaining visible face meets that image boundary directly'],
80:['actor occupies a comparatively small image region','recognizable surrounding space occupies a broad area','actor and background overlap agree with one viewpoint'],
88:['sky occupies the background behind head and shoulders','lower facial planes are visible from an upward viewpoint','body sky overlap agrees with one perspective'],
89:['actor occupies a small part of the room image','room corners and floor lines span a wide field','actor and room scale agree with one perspective'],
100:['crop isolates the declared upper garment region','the selected already present collar necklace or sleeve detail lies inside that crop','the garment crop is independently bounded from any face region'],
150:['human lowers beside the already requested animal','animal eyes lie near the human face height','both subjects projection agrees with that shared eye level'],
171:['broad window light illuminates the front face planes','face planes show soft light shadow transitions','body orientation remains independent of the source direction'],
172:['window facing face planes are brighter than opposite planes','light reaches those planes from one lateral direction','face turn remains independent of the source placement'],
174:['hair edges receive bright rim or transmitted light','illuminated strands remain attached to the same hair roots','face exposure is independently selected'],
177:['parallel shadow bands cross the selected face or body region','bands conform to the receiving body surface','blind or frame arrangement agrees with the shadow direction'],
}

def effects(unit):
    es=copy.deepcopy(unit['effects'])
    for e in es:
        if e['dimension']=='camera':
            e['target']='camera'
            e['property']={'camera.position':'viewpoint','reflection_path':'capture.reflection_path','flash':'exposure.flash'}.get(e['property'],e['property'])
    n=unit['seed_number']
    if n in (72,75,88):es += [{'dimension':'camera','target':'camera','property':'viewpoint.direction'},{'dimension':'camera','target':'camera','property':'viewpoint.height'}]
    if n in (71,73,74,76,150):
        es=[e for e in es if not(e['dimension']=='camera' and e['property']=='viewpoint')]
        es += [{'dimension':'camera','target':'camera','property':'viewpoint.height'}]
        if n in (73,74,76):es += [{'dimension':'camera','target':'camera','property':'viewpoint.direction'}]
    if n in (61,62):es += [{'dimension':'appearance','target':'main_subject','property':'hair.arrangement'}]
    if n in (96,97):
        for e in es:
            if e['property']=='body.gaze_target':e.update(dimension='expression',property='face.gaze_target')
    if n==138:
        es=[{'dimension':'appearance','target':'main_subject','property':'hair.arrangement'},{'dimension':'timing','target':'image','property':'moment'}]
    return es

def profile_from_unit(u, c):
    phrases=[x['visible_phrase_en'] for x in u['components']]
    return {
      'id':f"sf_profile_{u['seed_number']:03d}_base",'category':'observable_selfie_configuration',
      'activation':{'exact_terms':u['proposed_exact_terms'],'requires_adult_character':False,'semantic_discovery_requires_component_evidence':True,
        'hard_activation':{'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[{'id':'visible_human_configuration','any_terms':['selfie','self portrait','portrait','pose','woman','man','person','human','hand','face','셀카','셀피','포즈','인물','손','얼굴']}]}},
      'semantics':{'definition':'; '.join(phrases),'paraphrase_examples':phrases,'visual_components':phrases,'contrast_examples':[u['confusion_boundary_ko']],'claim_limits':u['claim_limits']},
      'concept_candidate':{'concept_terms':phrases+[u['label_ko']],'core_assertion_discovery':True,'affected_dimensions':c['affected_dimensions'],'affected_properties':c['affected_properties']},
      'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
      'reject_substitutes':[u['confusion_boundary_id']],
      'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':[
        {'id':f'component_{i}','match_terms':[ph],'evidence_field':f'component_{i}_phrase','evidence_terms':[ph],'min_content_words':3,
         'instruction':f'Bind the complete requested or explicitly adopted visible relation to its declared actor and target: {ph}.',
         'render_gate':{'id':f"vo_sf_{u['seed_number']:03d}_base_{i}",'review_scale':'native','description':f'{ph}. Inspect this complete relation in original pixels; partial fails and occluded prerequisites are unobservable.'}}
        for i,ph in enumerate(phrases,1)]}}

def add_korean(profile,n):
    terms=KOREAN.get(n)
    if not terms:return
    for component,ko in zip(profile['authored_components']['components'],terms):
        component['match_terms']=list(dict.fromkeys(component['match_terms']+[ko]))
    profile['semantics']['paraphrase_examples']=list(dict.fromkeys(profile['semantics']['paraphrase_examples']+terms))
    profile['concept_candidate']['concept_terms']=list(dict.fromkeys(profile['concept_candidate']['concept_terms']+terms))

def main():
    units=read(RESEARCH/'research-units.json')['units']; um={u['id']:u for u in units}
    cps=read(RESEARCH/'candidate-proposals.json')['proposals']; pps=read(RESEARCH/'visual-profile-proposals.json')['proposals']
    profiles={p['candidate_id']:copy.deepcopy(p['profile_draft']) for p in pps}
    reviewed=[]
    for p in cps:
        u=um[p['research_unit_id']];c=copy.deepcopy(p['candidate_draft']);c['affected_properties']=effects(u);c['affected_dimensions']=list(dict.fromkeys(x['dimension']for x in c['affected_properties']))
        reviewed.append((u,c,profiles[c['id']],p.get('capture_spec_checks',[])))
    for u in units:
        if u['integration_decision']!='literal_research_then_inventory_review':continue
        phrases=[x['visible_phrase_en']for x in u['components']]
        c={'id':f"sf_{u['seed_number']:03d}_base",'ko':u['label_ko'],'en':'; '.join(phrases),'weight':0.5,'tags':['human','selfie_visible_configuration',u['proposed_slot']],'for_any':['human'],
           'aliases':[u['label_ko']],'keywords':[u['label_ko'],u['label_en']],'embedding_text':'; '.join([u['label_ko'],u['label_en'],*phrases]),
           'concept_units':phrases,'relations':u['relations'],'affected_properties':effects(u),'core_assertion_discovery':True}
        c['affected_dimensions']=list(dict.fromkeys(e['dimension']for e in c['affected_properties']))
        reviewed.append((u,c,profile_from_unit(u,c),[]))
    slots={};receipt=[];specs=[];profile_rows=[]
    mirror_words=['mirror selfie','mirror-selfie','physical mirror','reflection','거울 셀카','거울셀카','거셀','미러 셀피']
    for u,c,p,input_checks in reviewed:
        n=u['seed_number']
        # Ordinary semantic discovery remains advisory. Literal component
        # phrases are evidence duties after adoption, not a prerequisite that
        # makes embedding paraphrases unreachable before adoption.
        p['activation'].pop('semantic_discovery_requires_component_evidence',None)
        c['for_any']=['human'];c['tags']=list(dict.fromkeys(['human',*c['tags']]))
        # Only an explicitly qualified mouth-neutral variant receives exact activation.
        if n==4:
            c['ko']='입 중립형 눈웃음';c['aliases']=['입 중립형 눈웃음'];c['keywords']=['입 중립형 눈웃음','neutral mouth eye smile'];p['activation']['exact_terms']=['입 중립형 눈웃음','neutral-mouth eye smile']
            p['concept_candidate']['concept_terms']=[t for t in p['concept_candidate']['concept_terms']if t not in ['눈웃음','Smize']]
        if n==6:
            old=c['concept_units'][1];new='lower lip retains a comparatively relaxed contour beneath the slightly projecting upper lip'
            c['concept_units'][1]=new;c['en']='; '.join(c['concept_units'])
            for field in ('definition','paraphrase_examples','visual_components'):
                v=p['semantics'][field];p['semantics'][field]=v.replace(old,new)if isinstance(v,str)else[new if t==old else t for t in v]
            p['concept_candidate']['concept_terms']=[new if t==old else t for t in p['concept_candidate']['concept_terms']]
            co=p['authored_components']['components'][1]
            for field in ('match_terms','evidence_terms'):co[field]=[new if t==old else t for t in co[field]]
            co['instruction']=co['instruction'].replace(old,new);co['render_gate']['description']=co['render_gate']['description'].replace(old,new)
        if n==56:
            c['ko']='하트 틈과 두 귀 봉우리가 함께 보이는 양손 형태';c['aliases']=[];c['keywords']=[c['ko']]
            p['concept_candidate']['concept_terms']=[t for t in p['concept_candidate']['concept_terms']if t!='고양이 하트']
        if 91<=n<=100 or n in (147,175):
            c['ko']='물리 거울 셀카 / '+c['ko'];c['aliases']=[c['ko']];c['keywords']=[c['ko'],'physical mirror selfie '+u['label_en']]
            p['activation']['exact_terms']=[c['ko'],'physical mirror selfie '+u['label_en']]
            p['activation']['hard_activation']['required_any_groups'].append({'id':'physical_mirror_capture_context','any_terms':mirror_words})
            p['activation']['context_disambiguation']={'required_with_authorial_core':True,'any_terms':mirror_words,'exclude_if_any_terms':['empty mirror','software mirror frame','빈 거울','소프트웨어 거울 테두리']}
            c['requires_any_tags']=['mirror']
        prerequisites={63:['ponytail'],67:['sleeves','long_sleeves'],68:['sunglasses'],69:['glasses'],70:['hat','cap'],
                       132:['food','utensil'],133:['book'],134:['flower'],136:['toothbrush'],140:['vehicle','car'],150:['animal','pet'],151:['off_shoulder','off-shoulder']}
        if n==135:prerequisites[n]=[{'lipstick':'lipstick','brush':'makeup_brush','puff':'makeup_puff'}[c['id'].split('_')[-1]]]
        if n in prerequisites:c['requires_any_tags']=list(dict.fromkeys(c.get('requires_any_tags',[])+prerequisites[n]))
        if n in (141,143,147,149):
            if n==147:c['requires_all_tags']=['mirror']
            c['requires_any_tags']=['partner','pair','couple','group']
            p['activation']['hard_activation']['required_any_groups'].append({'id':'declared_multiple_actor_context','any_terms':['two people','two women','two actors','two declared people','pair','couple','group','duo','두 사람','두 인물','두명','커플','그룹','단체']})
        if n in (24,30,46,47,53,54,56,58,161,163,164) or c['id']=='sf_133_two_hand':
            if c['id']=='sf_133_two_hand':c['requires_all_tags']=['book']
            c['requires_any_tags']=['tripod','timer','remote','fixed_camera','photographer']
            c['contextual_usage']={'contexts':[{'id':c['id']+'_hand_roles','meaning_scope':'Both hands of this actor perform the declared pose or grip. Capture support is independently resolved before adoption.','ordinary_readings':[],'claim_limits':['The same hand cannot also grip a separate capture phone. A second declared capture operator or fixed supported camera can supply capture.']} ]}
        if n in (49,151):
            p['activation']['exact_terms']=['모은 손가락의 이마 옆 경례','grouped fingers salute beside forehead'] if n==49 else ['기존 오프숄더의 어깨를 렌즈 쪽으로 돌리기','turn an existing off shoulder neckline toward lens']
        if n in PIXEL_OVERRIDES:
            phs=PIXEL_OVERRIDES[n];specs.append({'research_unit_id':u['id'],'candidate_id':c['id'],'input_capture_conditions':c['concept_units'],'pixel_projections':phs})
            for i,(co,ph) in enumerate(zip(p['authored_components']['components'],phs),1):
                co['match_terms']=[ph];co['evidence_terms']=[ph];co['instruction']=f'Bind the visible projection to its declared actor and image region: {ph}.';co['render_gate']['description']=f'{ph}. Review visible consistency, not actual camera position, lens setting, source history or shutter cause.'
            p['semantics']['definition']='; '.join(phs);p['semantics']['paraphrase_examples']=phs;p['semantics']['visual_components']=phs;p['concept_candidate']['concept_terms']=phs+[c['ko']]
        add_korean(p,n)
        p['concept_candidate']['affected_dimensions']=c['affected_dimensions'];p['concept_candidate']['affected_properties']=c['affected_properties']
        positive_ko=[x for x in p['semantics']['paraphrase_examples']if any('\uac00'<=a<='\ud7a3' for a in x)]
        c['embedding_text']='; '.join(dict.fromkeys([c['ko'],*c['keywords'],*c['concept_units'],*positive_ko]))
        # The legacy capture_context slot is a genre-scoped social register.
        # Capture mechanics apply independently of that register. A separate
        # data-owned slot leaves all existing genre applicability guards intact.
        slot='capture_mode' if u['proposed_slot']=='capture_context' else u['proposed_slot']
        if slot=='capture_mode':c['tags']=[slot if t=='capture_context' else t for t in c['tags']]
        slots.setdefault(slot,[]).append(c);profile_rows.append(p)
        receipt.append({'research_unit_id':u['id'],'variant':c['id'].split('_',2)[-1],'candidate_id':c['id'],'profile_id':p['id'],'slot':slot,'decision':'new_context_or_contact_variant','source_ids':u['source_ids'],'named_activation_deferred':n==56,'observability_ko':u['observability_ko']})
        if input_checks:specs.append({'research_unit_id':u['id'],'candidate_id':c['id'],'input_capture_conditions':input_checks,'proof_scope':'Declared capture inputs are not inferred or measured from pixels.'})
    # Capture prerequisites are inputs and candidate meaning, not an artificial pixel gate.
    capture=[
      ('sf_capture_direct_handheld','직접 손에 든 셀카','direct handheld self portrait with one capture hand holding the active camera; the remaining hand has its separately declared pose or contact role; capture device visibility follows the chosen framing',['direct handheld selfie','직접 손에 든 셀카']),
      ('sf_capture_physical_mirror','물리 거울을 통한 셀카','physical mirror self portrait with the capture phone visibly gripped by its declared operator in the reflection; reflected subjects and phone share one physical reflected space; actor count follows the declared subjects',['physical mirror selfie','물리 거울 셀카']),
      ('sf_capture_fixed_self_portrait','고정 장치 셀프포트레이트','fixed camera self portrait with a stable independently supported capture device and a declared timer or remote trigger; actor hands retain their separately declared pose contact or prop roles; apparatus visibility follows the requested frame',['fixed camera self portrait','고정 장치 셀프포트레이트'])]
    for cid,ko,en,aliases in capture:
        entry={'id':cid,'ko':ko,'en':en,'weight':0.5,'tags':['human','capture_mode'],'for_any':['human'],'aliases':aliases,'keywords':aliases,'embedding_text':'; '.join([ko,en]),'concept_units':en.split('; '),'relations':[{'id':'capture_owner','type':'assigned_to','subject':'camera.capture','object':'declared_capture_operator'}],'affected_dimensions':['camera'],'affected_properties':[{'dimension':'camera','target':'camera','property':'capture.mode'}],'core_assertion_discovery':True}
        if cid!='sf_capture_fixed_self_portrait':
            entry['affected_dimensions'].append('pose');entry['affected_properties'].append({'dimension':'pose','target':'main_subject'if cid=='sf_capture_direct_handheld'else'declared_capture_operator','property':'body.capture_hand_role'})
        if cid=='sf_capture_physical_mirror':entry['requires_any_tags']=['mirror']
        slots.setdefault('capture_mode',[]).append(entry)
    maintenance={'schema_version':'photo-extension-maintenance/v1','record_id':'selfie_pose_reviewed_20261008','source_filename':'photo_prompt_selfie_pose_extension.json','maintenance_only':True,'research_directory':'docs/research-evidence/photo-prompt/selfie-pose-semantics-20261008','reviewed_variants':receipt,'capture_input_candidates':[x[0]for x in capture],'authored_candidate_contracts':slots,
                 'provenance_boundary':'Named usage and photographic principles have source-specific support. Owned component geometry is a reviewed design, not a quotation of every article. New named cat-heart and bare bambi activation remain deferred.'}
    write(OUT/'maintenance-record.json',maintenance)
    write(OUT.parent/'extension-maintenance'/(maintenance['record_id']+'.json'),maintenance)
    extension={'schema_version':'photo-prompt-research-extension/v1','slots':slots,'existing_slot_context_extensions':{},'visual_semantics':[],
               'maintenance_ref':{'contract_version':'photo-extension-maintenance-ref/v1','record_id':maintenance['record_id'],'sha256':digest(maintenance)}}
    visual_contract=read(ASSETS/'photo_prompt_visual_obligations_pose_vocabulary.json')
    visual={'schema_version':visual_contract['schema_version'],'relation_contract_version':visual_contract['relation_contract_version'],'profiles':profile_rows}
    # Reuse the original mirror profile ID and gates; remove unintended age/count/gender requirements.
    base=read(ASSETS/'photo_prompt_visual_obligations.json')
    mirror=next(x for x in base['profiles']if x['id']=='mirror_selfie_reflection_device_topology')
    mirror['activation']['requires_adult_character']=False
    mirror['semantics']['definition']='A physical mirror boundary contains the declared reflected subjects and the capture phone visibly gripped by its declared operator. Hand device contact, reflected room depth, specified gaze target and any phone occlusion agree with one physical reflection. Age, actor count, gender and clothing follow the request.'
    mirror['semantics']['paraphrase_examples']=['the declared subjects and the phone held by the capture operator occupy one physical reflected room','지정된 인물들과 촬영자가 쥔 폰이 같은 물리 반사 공간에 놓인다','phone occlusion and specified gaze target agree with the same mirror plane']
    mirror['concept_candidate']['concept_terms']=['physical mirror plane','declared subjects and held capture phone inside reflection','coherent specified gaze and phone occlusion','hand device contact']
    cc=mirror['authored_components']['components'];oo=mirror['authored_components']['obligations'][0]
    replacements={
      'mirror_subject_inside':(['the declared subjects occupy the same physically reflected room as the visibly held capture phone','지정된 인물들이 손에 쥔 촬영 폰과 같은 물리 반사 공간에 보인다'],'mirror_subject_phrase'),
      'mirror_device_contact':(['the declared capture operator visibly grips the capture phone with coherent wrist ownership and finger device contact','지정된 촬영자의 손목과 손가락이 촬영 폰의 그립에 일관되게 이어진다'],'mirror_device_phrase'),
      'mirror_topology_boundary':(['the physical mirror reflection contains the declared subjects and visibly gripped capture phone with coherent contact specified gaze and any facial occlusion','물리 거울 안에서 지정된 인물들과 쥔 폰의 접촉 시선 가림이 일관된다'],'mirror_boundary_phrase')}
    for co in cc:
        if co['id']in replacements:
            phrases,field=replacements[co['id']];co['match_terms']=phrases
            ev=next(x for x in oo['evidence']if x['field']==field);ev['requirement']['must_mention_any']=[phrases[0]];ev['requirement']['min_content_words']=min(ev['requirement']['min_content_words'],len(phrases[0].split())-2)
    oo['instruction']='Keep a readable physical mirror boundary and the declared subjects in one reflected room with the capture phone visibly gripped by its declared operator. Preserve declared age, count, gender, clothing, crop, gaze target and phone occlusion; a hidden face region need not become visible.'
    next(x for x in oo['render_gates']if x['id']=='vo_social_mirror_subject_and_phone_inside')['description']='The declared subjects and the phone held by the declared capture operator appear in the same physical reflection, preserving declared actor count and any requested facial occlusion.'
    next(x for x in oo['render_gates']if x['id']=='vo_social_mirror_hand_device_contact')['description']='The capture operator visibly grips the phone with coherent wrist ownership and finger device contact.'
    manifest=read(ASSETS/'photo_prompt_source_manifest.json')
    registrations=[('photo_prompt_selfie_pose_extension.json','candidate'),('photo_prompt_visual_obligations_selfie_pose.json','visual_profile')]
    for filename,kind in registrations:
        existing=next((x for x in manifest['sources']if x['file']==filename),None)
        if existing:
            assert existing['kind']==kind and existing['required'],filename
            continue
        manifest['sources'].append({'file':filename,'kind':kind,'required':True,'load_order':1+max(x['load_order']for x in manifest['sources']if x['kind']==kind)})
    validate_extension_keys(extension);validate_candidate_entries(extension,set(AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS))
    for p in profile_rows+[mirror]:validate_visual_profile_source(p);compile_visual_profile(p)
    before={f:hashlib.sha256((ASSETS/f).read_bytes()).hexdigest()for f in ['photo_prompt_source_manifest.json','photo_prompt_visual_obligations.json']}
    write(ASSETS/registrations[0][0],extension);write(ASSETS/registrations[1][0],visual);write(ASSETS/'photo_prompt_source_manifest.json',manifest);write(ASSETS/'photo_prompt_visual_obligations.json',base)
    SourceInventory.load(ASSETS).validate()
    from prompt_generator import load_json, load_visual_obligation_registry
    load_json(ASSETS/'photo_prompt_tags.json');load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
    reuse=read(RESEARCH/'reuse-plan.json')['reuse'];rm={x['research_unit_id']:x['existing_refs']for x in reuse}
    coverage=[]
    for u in units:
        new=[x for x in receipt if x['research_unit_id']==u['id']]
        refs=rm.get(u['id'],[])
        assert new or refs,u['id']
        coverage.append({'research_unit_id':u['id'],'label_ko':u['label_ko'],'new_variants':new,'existing_component_refs':refs,'integration_decision':'new_reviewed_variants'if new else 'compose_existing_components','claim_boundary':'Existing refs preserve their own full meaning; a component match does not establish entire-pose equivalence. No new bare bambi or cat-heart activation.'})
    write(OUT/'coverage-180.json',coverage);write(OUT/'capture-input-proof-boundaries.json',specs)
    write(OUT/'authored-receipt.json',{'new_candidate_count':sum(len(v)for v in slots.values()),'new_profile_count':len(profile_rows),'existing_profile_revised':['mirror_selfie_reflection_device_topology'],'research_units_covered':len(coverage),'new_variant_unit_count':len({x['research_unit_id']for x in receipt}),'existing_component_unit_count':sum(not x['new_variants']for x in coverage),'source_before_sha256':before,'registered_sources':[x[0]for x in registrations],'candidate_drafts_reviewed':receipt,'proof_status':'Authored source contracts only; indexes, live retrieval and pixels pending.'})
    print(json.dumps({'candidates':sum(len(v)for v in slots.values()),'profiles':len(profile_rows),'coverage':len(coverage)},ensure_ascii=False))

if __name__=='__main__':
    from photo_runtime_sources import source_update
    with source_update(ASSETS.parent,OUT/'runtime-store'):
        main()
