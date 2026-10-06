"""Maintenance authoring projection; never imported by the live generator."""
from pathlib import Path
import json
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
RESEARCH = EVIDENCE.parent / 'water-semantics-20261006'
STAGE = ROOT / '.codex-artifacts/water-integration-20261006/skill'
ASSETS = STAGE / 'assets'
sys.path.insert(0, str(STAGE / 'scripts'))
from visual_profile_contracts import compile_visual_profile, validate_visual_profile_source
from photo_candidate_semantics import validate_candidate_entries

def read(p):
    return json.loads(p.read_text())

def save(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

# These are reviewed visual senses, not raw glossary aliases. The short labels
# help optional discovery; hard activation uses a complete owned proposition.
ALIASES = '''
W002|spring outlet;용천 출수점
W004|surface water beading;표면에 맺힌 물방울
W005|edge-attached hanging drop;가장자리에 붙은 물방울
W006|capillary wetting front in fibers;섬유를 따라 번진 젖은 경계
W007|water glass meniscus;물과 유리의 오목 메니스커스
W008|floating object waterline;부유 물체의 수면 경계
W014|exterior condensation droplets;용기 바깥 결로
W015|rain impact on wet ground;빗방울 충돌과 젖은 바닥
W017|dew droplets on a leaf or web;잎과 거미줄의 이슬
W018|low mist depth occlusion;물안개 속 원경 대비 감소
W019|transparent water droplet volume;독립된 투명 물방울
W020|thin water film;얇은 수막
W021|water jet from an outlet;출구에서 이어지는 물줄기
W022|surface rivulet;표면을 흐르는 가는 물길
W023|hanging and falling drops;붙은 낙수와 떨어진 방울
W024|impact spray;충돌 물보라
W025|water impact splash;수면 충돌 스플래시
W026|crown splash;크라운 스플래시
W027|underwater gas bubbles;물속 기포
W028|water foam bubble patch;물 위 포말
W030|wind wave crests;풍파 능선
W031|rounded swell crests;너울 능선
W032|breaking wave lip and foam;쇄파의 접힘과 포말
W033|barrel wave hollow;배럴 파도의 빈 터널
W034|beach swash sheet;해변 처오름
W035|beach backwash channels;해변 되흐름
W036|vessel wake continuity;선박 뒤의 항적파
W040|iceberg waterline continuity;빙산의 수면 경계
W042|pancake ice raised rims;팬케이크 아이스
W043|surface frost crystals;표면 서리 결정
W044|edge attached icicle;가장자리에 붙은 고드름
W045|wet ice slush;얼음과 액체가 섞인 슬러시
W046|sun glitter on wave facets;윤슬;물비늘
W047|owned water reflection;실물과 이어진 수면 반영
W048|refraction of a water-crossing object;수면 경계의 굴절
W049|underwater caustics on a receiver;수중 수광면의 카우스틱
W050|Snell window;스넬의 창
W051|underwater light shaft particles;입자가 보이는 수중 광선
W052|underwater camera backscatter;수중 후방산란
W053|water path color attenuation;물 경로에 따른 색 감쇠
W054|organism bound bioluminescence;생물에 연결된 생물발광
W055|excited organism biofluorescence;여기광과 연결된 생물형광
W056|iridescent water surface film;수면 유막의 간섭색
W057|continuous stream channel;연속된 하천 수로
W060|reservoir managed water edge;저수지 관리 경계
W061|spring pool condensed mist;온천 수면의 응결 안개
W062|geyser vent and jet;간헐천 분출구
W064|river confluence;하천 합류부
W065|shallow riffle bed;얕은 여울
W067|waterfall plunge pool continuity;폭포와 폭포소의 연결
W068|river meander banks;곡류의 연속 제방
W069|isolated oxbow lake;본류와 분리된 우각호
W070|braided river split and rejoin;갈라지고 합치는 망상하천
W071|river floodplain adjacency;하천과 인접한 범람원
W075|lagoon barrier and connection;석호 장벽과 연결
W076|shore-attached spit;해안에서 뻗은 사취
W077|tombolo land connection;섬을 잇는 육계사주
W078|barrier island inner water gap;장벽섬의 안쪽 수역
W080|intertidal wet dry bands;조간대의 젖고 마른 대상
W081|rock tide pool;암반 조수웅덩이
W083|isolated sea stack;해안에서 떨어진 시스택
W088|hydrothermal vent particle plume;열수 굴뚝의 입자 분출
W089|seafloor brine pool interface;해저 염수호 경계
W090|marine snow aggregates;마린 스노
W091|coral colony connected skeleton;산호 군체의 골격 연결
W092|kelp holdfast stipe blade;켈프 고정 부위 줄기 엽체
W093|rooted seagrass meadow;뿌리내린 해초지
W094|mangrove roots trunk canopy continuity;맹그로브 뿌리 수간 수관
W096|submerged aquatic plant;침수식물
W098|emergent aquatic plant;정수식물
W100|jellyfish bell appendage continuity;해파리 종형 몸과 부속지
W101|ctenophore comb rows;빗해파리 빗살판 열
W103|octopus mantle arms suction cups;문어 몸 팔 빨판
W104|squid arms and two tentacles;오징어 팔과 두 촉완
W105|cuttlefish fin margin;갑오징어 지느러미 가장자리
W106|nautilus shell opening appendages;앵무조개 껍데기 입구 부속지
W107|ray disc pectoral fin continuity;가오리 몸과 가슴지느러미
W108|seahorse grasping tail;해마의 감긴 꼬리
W111|separate bodies in a fish school;어군의 개체 분리
W116|shoreline wrack line;해안 표착물 띠
W117|attached aquatic biofilm;물 접촉 기질의 생물막
W119|water stain height boundary;물얼룩 침수선
W120|polygonal desiccation cracks;다각형 건열
W121|localized transferred wet mark;국소 젖은 흔적
W122|salt evaporation pan divisions;염전의 얕은 구획
W126|ice sculpture melt edge;얼음 조각의 녹는 가장자리
W128|infinity pool spill edge;인피니티 풀 넘침 경계
W129|reflecting pool object correspondence;반사 연못 실물 대응
W131|outdoor bathing pool coping;노천탕 수면 경계
W138|buoy waterline and mooring;부표 수면 계류
W139|vessel mooring line attachment;선박 계류줄 연결
W141|drained dry dock exposed hull;건선거의 드러난 선저
W144|surface snorkel air opening;수면 스노클 공기 중 입구
W145|submerged freediver posture;프리다이빙 수중 자세
W146|scuba cylinder regulator hose mouthpiece;스쿠버 실린더 호스 입 연결
W147|surfer board body support;서핑 보드 몸 지지
W150|fin foot pocket blade continuity;오리발 발주머니 날 연결
W151|tewak collection net attachment;테왁 망사리 연결
W152|body waterline continuity;몸을 가르는 수면 경계
W156|damp clumped hair in air;공기 중 젖어 뭉친 머리
W157|underwater floating hair;물속에서 펼쳐진 머리
W159|towel overlap and body contact;수건의 겹침과 몸 접촉
W161|wet fabric cling and folds;젖은 천의 밀착과 주름
W162|wet cloth optical transmission;젖은 직물의 부분 투과
W166|flood water structure boundary;범람한 물과 구조물 경계
W169|rip current seaward corridor;이안류의 바다 방향 통로
W171|plastic fragments scale reference;플라스틱 조각 크기 기준
W172|derelict net strand continuity;유실 어망의 연결된 가닥
W175|submerged room structural continuity;수몰 실내의 구조 연속성
W177|colored underwater diffusion wisps;수중 색 물질 확산
W179|submerged silhouette occlusion;수면 아래 실루엣
W182|mermaid torso tail continuity;인어 상체 꼬리 연결
W183|human bird siren continuity;여성 새 세이렌 연결
W188|water ripple ridge reflection bands;물결 능선 반사 띠
W190|over under split level waterline;오버언더 수면 연속성
W191|water surface level viewpoint;수면 높이 시점
W192|underwater backlit silhouette;밝은 수면 앞 수중 실루엣
'''
aliases = {line.split('|')[0]: line.split('|')[1].split(';') for line in ALIASES.strip().splitlines()}

# Short positive evidence for optional discovery. A match proposes a review;
# it never verifies the relation or removes any selected evidence/pixel gate.
DISCOVERY = {
 'W004': [['rounded droplets','small beads','water beads','둥근 물방울'],['curved contact','rounded beads','domed drops','beads','곡면 경계'],['surface texture','wood grain','varnished rim','leaf veins','표면 질감']],
 'W006': [['damp front','wet patch','wetting front','젖은 경계'],['fibers','paper fibers','cloth fibers','섬유'],['darker wet region','wet darkening','darker patch','어두워진 젖은 부분']],
 'W007': [['curved liquid edge','concave meniscus','메니스커스'],['liquid level','central water level','수위'],['inner glass wall','vessel wall','용기 벽']],
 'W014': [['condensation droplets','exterior droplets','결로 방울'],['merging droplets','coalescing drops','합쳐진 물방울'],['outside glass','outer surface','vessel exterior','용기 바깥']],
 'W017': [['dew drops','dew droplets','이슬'],['leaf edge','web strand','잎 가장자리','거미줄'],['droplet highlights','bead highlights','방울 반짝임']],
 'W018': [['low mist','pale haze','water mist','물안개'],['distant','reduced contrast','softens','먼 풍경'],['foreground','near edges','crisp near','전경']],
 'W019': [['detached drop','individual droplets','separate droplets','독립 물방울'],['rounded drop','transparent droplet','curved drop','둥근 방울'],['background distortion','refracted background','droplet refraction','굴절된 배경']],
 'W020': [['thin sheet','thin water layer','water film','수막'],['localized reflections','wet glints','wet paths shine','반사광'],['material detail','stone','seams','wood grain','바탕 질감']],
 'W021': [['water stream','water jet','discharge stream','outward fan','물줄기'],['outlet hose','nozzle','spout','source opening','분사구'],['puddle','receiving basin','furrow','ground pool','받는 물']],
 'W022': [['rivulets','wet paths','narrow liquid path','가는 물길'],['branching','merging','joints','connected path','갈라진 물길'],['downstream pool','puddle','river below','receiving water','하류 웅덩이']],
 'W023': [['hanging drop','icicle tips','outlet edge','meltwater drops gather','매달린 물방울'],['detached drop','falling drop','separated drop','낙수 방울'],['directly below','receiver','puddle','furrow','아래 받는 면']],
 'W024': [['airborne droplets','spray droplets','비말'],['spray fan','fan of splash','coherent spray','물보라'],['collision zone','wave impact','strikes','충돌 지점']],
 'W025': [['impact','strikes the puddle','fresh impacts','충돌'],['raised sheet','splash','liquid sheet','shallow translucent sheet','솟은 수막'],['separate droplets','detached drops','flicking','분리된 방울']],
 'W026': [['circular liquid rim','crown splash','크라운 스플래시'],['rim spikes','water spikes','rising fingers','테두리 돌기'],['detached droplets','drops beyond the rim','분리된 방울']],
 'W027': [['gas pockets','underwater bubbles','air bubbles in water','수중 기포'],['bubble rims','bright curved rims','기포 테두리'],['water around the bubbles','transparent pockets','bubble background','기포 주변 물']],
 'W028': [['packed bubbles','foam','froth','포말'],['foam edges','foam patch','froth boundary','포말 가장자리'],['water beside foam','adjacent liquid','foam on water','주변 물']],
 'W032': [['breaking crest','breaking wave','쇄파'],['falling lip','curling lip','접히는 파도'],['joined foam','whitewater','crest foam','백파']],
 'W036': [['ferry','hull','vessel','boat','선체'],['wake','trailing ridges','항적파'],['widening wake','trailing disturbed','stern','behind it','뒤쪽 물결']],
 'W042': [['rounded ice discs','pancake ice','팬케이크 아이스'],['raised rims','perimeter rims','융기 테두리'],['water between discs','open gaps','원반 사이 물']],
 'W043': [['frost crystals','branching crystals','서리 결정'],['supporting surface','branch surface','기질 표면'],['crystalline edges','crystal facets','결정 모서리']],
 'W044': [['icicle','icicles','tapered ice','고드름'],['branch','overhead edge','attached ice','붙은 가장자리'],['tips','pointed tip','meltwater','melting tip','녹는 끝']],
 'W046': [['specular glints','water glints','glitter','윤슬'],['sunlight','sidelight','moonlight','lighting direction','광원 방향'],['water surface','crests','wave facets','수면']],
 'W047': [['reflected object','reed stems','branch','object above','반영 소유자'],['reflections','inverted image','wavering reflection','반영'],['water plane','water surface','pool','river','수면']],
 'W048': [['waterline crossing','object through water','수면을 가로지른 물체'],['apparent displacement','optical offset','refraction','굴절'],['same object','continuous material','crossing structure','같은 물체의 연속성']],
 'W049': [['rippled water','transparent water surface','수면 굴절'],['caustics','focused bright curves','카우스틱'],['submerged receiver','pool floor','underwater surface','수중 수광면']],
 'W050': [['underwater upward','looking up underwater','수중 위보기'],['above water scene','Snell window','스넬의 창'],['surrounding reflection','reflected underwater','주변 수면 반사']],
 'W052': [['bright foreground particles','illuminated suspended particles','후방산란'],['camera light','strobe path','조명 경로'],['distant underwater subject','underwater medium','수중 배경']],
 'W064': [['two incoming channels','tributaries','지류'],['joined channel','confluence','합류'],['bank junction','shared downstream','제방 합류점']],
 'W069': [['curved isolated lake','oxbow','우각호'],['nearby river','river channel','본류'],['land separating','separated bend','분리된 옛 하도']],
 'W070': [['channel branches','braided channels','망상 수로'],['sediment bars','bars between','사주'],['reconnections','rejoin','다시 합류']],
 'W092': [['holdfast','substrate attachment','고정 부위'],['stipes','stipe','줄기'],['blades','kelp blades','엽체']],
 'W093': [['seafloor blades','seagrass leaves','해초 잎'],['rooted meadow','rooted seagrass','뿌리내린 해초'],['water gaps','water between leaves','잎 사이 물']],
 'W144': [['snorkel mask','face mask','스노클 마스크'],['mouth connection','snorkel mouthpiece','입 연결'],['opening above water','air opening','수면 위 입구']],
 'W146': [['cylinder','buoyancy device','BCD','실린더'],['regulator hose','continuous hose','레귤레이터 호스'],['mouthpiece','same diver','입에 연결된 마우스피스']],
 'W157': [['scalp attachment','hair rooted','두피 연결'],['floating strands','hair spreading underwater','수중 머리 가닥'],['current aligned','buoyant hair','흐름을 따르는 머리']],
 'W190': [['air and underwater','above and below water','수상 수중'],['single waterline','split level','over under','오버언더'],['continuous crossing object','shared object','같은 물체의 연속성']],
}

# Complete effect declarations use physical owners rather than a carrier slot.
# Environmental structure, material, optical capture, body and garment effects
# remain distinct. No '*' or unknown property is used to bypass a partial lock.
SCOPE = {
 'location': [('setting','water_body','spatial_structure')],
 'surface_material': [('material','selected_surface','wet_surface_structure')],
 'texture': [('material','water_body','surface_structure')],
 'action': [('action','water_body','flow_or_impact'),('relationship','water_body','source_receiver_connection')],
 'motion': [('action','water_body','flow_configuration'),('relationship','water_body','flow_source_connection')],
 'weather': [('atmosphere','scene','rain'),('material','ground','wetness')],
 'ambient_particle': [('atmosphere','water_medium','particle_structure')],
 'light_shape': [('lighting','water_body','optical_pattern')],
 'lighting': [('lighting','water_medium','light_transport')],
 'reflection_logic': [('composition','reflected_object','reflection_continuity')],
 'composition': [('camera','capture_camera','viewpoint'),('composition','waterline','scene_continuity')],
 'lens_artifact': [('camera','capture_camera','backscatter'),('lighting','water_medium','particle_scatter')],
 'color_grading': [('color','water_medium','path_attenuation'),('lighting','water_medium','path_attenuation')],
 'subject': [('species','selected_aquatic_subject','visible_structure'),('body_geometry','selected_aquatic_subject','part_connections')],
 'prop': [('setting','selected_water_prop','structure'),('relationship','selected_water_prop','attachment')],
 'aftermath_trace': [('material','selected_surface','water_trace'),('relationship','selected_surface','trace_source_continuity')],
 'wearable_accessory': [('appearance','main_subject','equipment'),('relationship','main_subject','equipment_attachment')],
 'body_pose': [('pose','main_subject','body_water_configuration'),('relationship','main_subject','water_contact')],
 'hair_style': [('appearance','main_subject','hair.moisture_and_configuration')],
 'garment_detail': [('appearance','main_subject','wardrobe.structure'),('material','main_subject','wardrobe.wetness_and_contact')],
 'camera_height': [('camera','capture_camera','viewpoint.height')],
}
OVERRIDE = {
 'W007': [('material','vessel_water','meniscus'),('relationship','vessel_water','inner_wall_contact')],
 'W008': [('pose','floating_object','orientation'),('relationship','floating_object','waterline_continuity')],
 'W014': [('material','cold_surface','external_condensation')],
 'W027': [('atmosphere','water_medium','gas_bubble_structure')],
 'W026': [('material','impact_water','crown_rim_structure'),('action','impact_water','impact')],
 'W040': [('setting','iceberg','geometry'),('relationship','iceberg','waterline_continuity')],
 'W046': [('lighting','water_body','surface_specular_glitter')],
 'W048': [('material','water_interface','refraction'),('relationship','crossing_object','waterline_continuity')],
 'W049': [('lighting','submerged_receiver','caustic_pattern'),('relationship','submerged_receiver','water_surface_light_path')],
 'W050': [('camera','capture_camera','viewpoint.direction'),('composition','water_surface','transmitted_and_reflected_regions')],
 'W054': [('lighting','selected_organism','localized_emission'),('relationship','selected_organism','emission_location')],
 'W055': [('lighting','selected_organism','excited_emission'),('relationship','selected_organism','excitation_source')],
 'W062': [('action','ground_vent','water_ejection'),('relationship','ground_vent','jet_connection')],
 'W088': [('setting','seafloor_vent','structure'),('relationship','seafloor_vent','particle_plume_connection')],
 'W083': [('setting','sea_stack','geometry'),('relationship','sea_stack','shore_separation')],
 'W117': [('material','selected_substrate','attached_film')],
 'W162': [('material','main_subject','wardrobe.optical_transmission'),('appearance','main_subject','wardrobe.layering')],
 'W169': [('action','shore_water','seaward_flow'),('relationship','shore_water','breaking_wave_corridor')],
 'W177': [('material','water_medium','colored_diffusion'),('relationship','water_medium','colored_release_source')],
 'W126': [('material','ice_sculpture','shape_and_melt_edges')],
 'W179': [('composition','submerged_form','occluded_silhouette'),('relationship','submerged_form','surrounding_scale')],
 'W182': [('species','main_subject','hybrid_structure'),('body_geometry','main_subject','torso_tail_connection')],
 'W183': [('species','main_subject','hybrid_structure'),('body_geometry','main_subject','human_bird_connection')],
 'W190': [('camera','capture_camera','waterline_capture'),('composition','waterline','shared_object_continuity')],
}

def main():
    units = read(RESEARCH/'SEMANTIC-UNITS.json')['units']
    slots, profiles, ledger = {}, [], []
    from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
    for u in units:
        if u['mode'] != 'visual':
            ledger.append({'unit_id':u['id'],'disposition':'INTERPRETATION_CONTEXT_ONLY' if u['mode']=='context' else 'FAMILY_REQUIRES_VARIANT_SELECTION','reason':u['confusion_boundary']})
            continue
        uid=u['id']; cid='water_'+uid.lower(); slot=u['proposed_slot']
        parts=[c['positive_predicate_en'] for c in u['observable_components_proposal']]
        if uid=='W008':parts[1]='its connected submerged portion below the same surface'
        if uid=='W048':parts[2]="the same object's structure continuing on both sides"
        effects=[{'dimension':d,'target':t,'property':p} for d,t,p in OVERRIDE.get(uid,SCOPE[slot])]
        dims=list(dict.fromkeys(x['dimension'] for x in effects))
        en='; '.join(parts)
        terms=[]
        for term in [u['ko'],*aliases[uid]]:
            if term.casefold() not in {t.casefold() for t in terms}:
                terms.append(term)
        # All relation endpoints are source-owned entities. Actual instance
        # binding and literal relation evidence remain adoption-time duties.
        relations=[{k:r[k] for k in ('id','type','subject','object')} for r in u['relations_proposal']]
        row={'id':cid,'ko':u['ko'],'en':en,'weight':0.45,'tags':['water'],
             'aliases':terms[1:],'keywords':terms,'paraphrases':[en],
             'embedding_text':'; '.join([*terms,en]),'concept_terms':parts,
             'concept_units':parts,'relations':relations,'affected_dimensions':dims,
             'affected_properties':effects,'core_assertion_discovery':True,
             'contextual_usage':{'contexts':[{'id':cid+'_boundary','definition':u['confusion_boundary'],
               'observable_interpretation':en,'claim_limits':[u['context_limits']],
               'activation_authority':'interpretation_only_not_a_required_visual_recipe'}]}}
        if slot=='subject':
            category = ('plant' if uid in ('W092','W093','W096','W098') else
                        'animal' if uid in ('W091','W100','W101','W103','W104','W105','W106','W107','W108','W111') else
                        'human' if uid in ('W182','W183') else
                        'object' if uid in ('W126','W179') else 'environment')
            row['kind']=[category]
            row['tags'].append(category)
        if slot in ('hair_style','garment_detail','wearable_accessory') or uid in ('W145','W152','W182','W183'):
            row['for_any']=['human']
        if uid in ('W144','W145','W146','W147','W150','W151','W157','W169','W190','W191','W192'):
            row['requires_primary_any_tags']=['water','underwater','diver','diving','swimming','ocean','sea','pool','river','shore','marine','aquatic','surface']
        slots.setdefault(slot,[]).append(row)
        # Full predicate activation cannot let a single broad noun prescribe
        # a selected camera, carrier, apparel or anatomical realization.
        exact=en+'.'
        components=[]
        for i,part in enumerate(parts,1):
            match_terms=list({term.casefold():term for term in [part,*DISCOVERY.get(uid,[[],[],[]])[i-1]]}.values())
            components.append({'id':f'component_{i}','match_terms':match_terms,
              'evidence_field':f'component_{i}_phrase','evidence_terms':[part],
              'min_content_words':3,'instruction':f'Preserve the selected physical component with its own carrier and connection: {part}.',
              'render_gate':{'id':f'vo_{cid}_{i}','review_scale':'native',
                'description':f'Inspect the original image for this complete component and correct physical owner: {part}. Hidden or partial realization fails this gate.'}})
        profile={'id':'water_rel_'+uid.lower(),'category':'aquatic_component_relation',
          'activation':{'exact_terms':[exact],'requires_adult_character':False,
            'semantic_discovery_requires_component_evidence':True,
            'hard_activation':{'contract_version':'photo-visual-hard-activation/v1',
              'required_any_groups':[{'id':'complete_owned_proposition','any_terms':[exact]}]}},
          'semantics':{'definition':en,'paraphrase_examples':[*terms,en],
            'visual_components':parts,'contrast_examples':[u['confusion_boundary']],
            'claim_limits':[u['context_limits'],'Approximate discovery proposes an optional meaning; it creates no requester duty. A selected complete realization must retain its physical owner and all request locks.']},
          'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':components},
          'concept_candidate':{'concept_terms':[u['ko'],*parts],
            'core_assertion_discovery':True,'affected_dimensions':dims,'affected_properties':effects},
          'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],
            'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},'reject_substitutes':[u['confusion_boundary']]}
        validate_visual_profile_source(profile);compile_visual_profile(profile)
        profiles.append(profile)
        ledger.append({'unit_id':uid,'candidate_id':cid,'profile_id':profile['id'],
          'disposition':'NARROW_RELATIONAL_SIBLING','candidate_slot':slot,
          'affected_properties':effects,'relations':relations,
          'source_refs':u['public_source_refs'],
          'source_status':u['claim_status'],'gate_ids':[c['render_gate']['id'] for c in components],
          'proof_boundary':'authored and contract reviewed; no per-unit pixel claim'})
    candidate={'schema_version':'photo-prompt-research-extension/v1','slots':slots}
    validate_candidate_entries(candidate,AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
    save(ASSETS/'photo_prompt_water_relations_extension.json',candidate)
    save(ASSETS/'photo_prompt_visual_obligations_water_relations.json',
         {'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','profiles':profiles})
    manifest=read(ASSETS/'photo_prompt_source_manifest.json')
    for kind,name in [('candidate','photo_prompt_water_relations_extension.json'),('visual_profile','photo_prompt_visual_obligations_water_relations.json')]:
        if not any(x['file']==name for x in manifest['sources']):
            manifest['sources'].append({'file':name,'kind':kind,'required':True,
              'load_order':max(x['load_order'] for x in manifest['sources'] if x['kind']==kind)+1})
    save(ASSETS/'photo_prompt_source_manifest.json',manifest)
    save(EVIDENCE/'ADOPTION-LEDGER.json',{'schema':'water-adoption-ledger/v1','units':ledger,
      'candidate_count':sum(map(len,slots.values())),'profile_count':len(profiles),
      'gate_count':sum(len(p['authored_components']['components']) for p in profiles),
      'preservation':'Existing authored records are retained. New siblings bind the more complete owned relation; no bare word adds hard authority.'})
    print(json.dumps({'candidates':sum(map(len,slots.values())),'profiles':len(profiles),'gates':3*len(profiles),'stage':str(STAGE)}))

if __name__=='__main__':main()
