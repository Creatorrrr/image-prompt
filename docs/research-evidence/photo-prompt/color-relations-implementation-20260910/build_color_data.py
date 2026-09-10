"""Maintenance authoring projection; research grouping is never an exact alias map."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
from photo_candidate_semantics import digest

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent / 'color-combination-patterns-20260910'
research = {r['id'].removeprefix('ccp_'): r for r in json.loads((RESEARCH/'candidate-research.json').read_text())['records']}

# id | source family | truly coextensive search labels | two all-of visible components.
# No fixed hue pair, ethnicity, costume, narrative, Kelvin value or area ratio is a default.
AUTHORED = '''
monochromatic|monochromatic|Monochromatic/유채색 단색 배색|the selected chromatic regions share one recognizable hue family|lightness or chroma differences keep their separate surfaces readable
achromatic|achromatic|Achromatic/무채색 배색|the selected image scope contains only neutral gray black and white tones|tonal differences preserve material detail inside that achromatic scope
analogous|analogous|Analogous/유사색 배색|the principal palette occupies one neighboring hue sector on the specified color wheel|separate neighboring hues remain recognizable on their assigned regions
complementary|complementary|Complementary/Complementary Contrast/보색 대비|two principal colored regions occupy opposite hue sectors on the specified color wheel|each opposing hue retains a bounded visible region
near_complementary|near_complementary|Near-Complementary/근접 보색|one principal hue is visibly offset from the exact opposite of the other on the specified wheel|the two owners retain distinct contrasting hue families
split_complementary|split_complementary|Split Complementary/분열 보색|a base hue occupies one named region while two other regions carry hues flanking its opposite on the specified wheel|the two flanking hue regions remain distinct from each other and from the base
triadic|triadic|Triadic/삼각 배색|three principal hue families occupy approximately equal intervals around the specified color wheel|each of the three hues remains visible on a separate assigned region
tetradic_rectangle|tetradic|Rectangle Scheme/직사각 사각 배색|four assigned hue families form two opposing pairs on the specified color wheel|the hue intervals alternate shorter and longer around the wheel
square|square|Square Scheme/정사각 배색|four principal hue families occupy approximately equal intervals around the specified color wheel|all four assigned hue regions remain separately visible
accented_analogous|accented_analogous|Accented Analogous/강조 유사색|the main colored field stays within neighboring hue families|a bounded accent uses a hue outside that neighboring family sector
restricted_subject|limited_palette|Restricted Subject Palette/피사체 제한 팔레트|the subject uses only the explicitly selected principal hue families|the restriction ends at the subject boundary and leaves background colors independently assigned
restricted_background|limited_palette|Restricted Background Palette/배경 제한 팔레트|the background uses only the explicitly selected principal hue families|the restriction ends at the background boundary and leaves subject colors independently assigned
hue_contrast|hue_contrast|Hue Contrast/색상 대비|the two assigned regions have visibly different hue families|both hues remain identifiable independently of their lightness difference
high_chroma|chroma_field|High-Chroma Palette/고채도 팔레트|the selected colored field has strong chroma across its principal hue families|hue differences and surface shading remain readable within that vivid field
low_chroma|chroma_field|Low-Chroma Palette/Muted Palette/저채도 팔레트|the selected colored field has restrained chroma across its principal hue families|faint hue differences remain visible instead of collapsing into grayscale
vivid_on_muted|chroma_separation|Vivid-on-Muted/Saturated Accent/선명한 피사체와 저채도 배경|the named focal region has visibly stronger chroma than its surrounding field|the surrounding field retains faint readable hues and separate material tones
muted_on_vivid|chroma_separation|Muted-on-Vivid/저채도 피사체와 선명한 배경|the named focal region has visibly lower chroma than its surrounding field|the surrounding field retains stronger distinct hues along the focal boundary
chroma_gradient|chroma_gradient|Chroma Gradient/채도 그라데이션|chroma changes progressively along the specified surface path|the hue family stays recognizable throughout the chroma transition
uniform_chroma|chroma_distribution|Uniform Saturation/균일 채도|the assigned hue groups have comparable visible chroma strength|their different hue identities remain readable across the field
mixed_chroma|chroma_distribution|Mixed Saturation/혼합 채도|the assigned hue groups have deliberately unequal visible chroma strength|the stronger and weaker chroma groups each retain identifiable hue regions
high_value_contrast|value_contrast|High-Value Contrast/강한 명도 대비|the named regions have a large visible lightness difference|material detail remains readable within both the light and dark regions
low_value_contrast|value_contrast|Low-Value Contrast/약한 명도 대비|the named regions have only a small visible lightness difference|their shared boundary remains readable through hue material or edge cues
dark_on_dark|tonal_layering|Dark-on-Dark/어두운 톤온톤|a dark subject is layered against a dark surrounding field|small local lightness differences preserve the subject contour and surface detail
light_on_light|tonal_layering|Light-on-Light/밝은 톤온톤|a light subject is layered against a light surrounding field|small local lightness differences preserve the subject contour and surface detail
achromatic_accent|single_accent|Achromatic + Accent/무채색과 단일 강조색|one named owner retains a single principal chromatic accent|the rest of the specified scope remains achromatic with readable shading
isolated_accent|isolated_accent|Isolated Accent/고립 강조색|a bounded chromatic accent occupies the named owner|a readable surrounding interval separates it from other competing chromatic regions
micro_accent|micro_accent|Micro Accent/미세 강조색|a small localized chromatic mark occupies the named owner|the mark remains identifiable at the specified review size while covering little of the chosen scope
accent_cluster|accent_distribution|Accent Cluster/Clustered Color/군집 강조색|multiple accent elements gather into one compact spatial group|a quieter surrounding interval separates that group from the rest of the composition
scattered_accent|accent_distribution|Scattered Accent/Distributed Color/분산 강조색|multiple accent elements occupy separated parts of the composition|visible intervals keep the accent elements spatially dispersed
color_repetition|color_repetition|Repeated Accent/Color Echo/Color Repetition/Color Link/색 반복|the same recognizable hue family recurs on separate scene elements|visible spatial gaps distinguish the repeated owners
alternating_color|color_rhythm|Alternating Color/교대 색 리듬|two assigned hue families alternate along a visible sequence of elements|at least two cycles and their intervening boundaries remain readable
color_bridge|color_bridge|Color Bridge/Transitional Color/연결색|a visible intermediate color region lies between two principal colored regions|the intermediate region provides a readable transition to both neighboring colors
warm_subject|temperature_separation|Warm Subject Cool Environment/따뜻한 피사체 차가운 배경|the named subject has relatively warm color tendencies|the visible environment has relatively cool color tendencies across the subject boundary
cool_subject|temperature_separation|Cool Subject Warm Environment/차가운 피사체 따뜻한 배경|the named subject has relatively cool color tendencies|the visible environment has relatively warm color tendencies across the subject boundary
warm_foreground|depth_temperature|Warm Foreground Cool Background/따뜻한 전경 차가운 배경|a readable foreground plane carries relatively warm hues|a separate distant plane carries relatively cool hues with visible depth cues
cool_foreground|depth_temperature|Cool Foreground Warm Background/차가운 전경 따뜻한 배경|a readable foreground plane carries relatively cool hues|a separate distant plane carries relatively warm hues with visible depth cues
warm_highlights|tone_temperature|Warm Highlight Cool Shadow/따뜻한 하이라이트 차가운 그림자|highlight tonal regions share a warm color tendency across separate surfaces|shadow tonal regions share a cool tendency with controlled transitions through midtones
cool_highlights|tone_temperature|Cool Highlight Warm Shadow/차가운 하이라이트 따뜻한 그림자|highlight tonal regions share a cool color tendency across separate surfaces|shadow tonal regions share a warm tendency with controlled transitions through midtones
two_color_lights|multicolor_lighting|Two-Color Lighting/Dual-Tone Lighting/두 색 조명|two differently colored light contributions reach visible receiving surfaces|each contribution has a readable footprint following form and occlusion
three_color_lights|multicolor_lighting|Tri-Color Lighting/세 색 조명|three differently colored light contributions reach visible receiving surfaces|all three contributions retain separate readable footprints following form and occlusion
colored_key|key_fill_color|Colored Key Neutral Fill/유색 키라이트 중성 필라이트|the dominant directional illumination has a visible color tint|the weaker fill contribution remains relatively neutral on its receiving regions
colored_fill|key_fill_color|Neutral Key Colored Fill/중성 키라이트 유색 필라이트|the dominant directional illumination remains relatively neutral|the weaker fill contribution adds visible color to its receiving regions
colored_rim|colored_rim|Colored Rim Light/유색 림라이트|colored illumination follows a narrow source-facing contour of the subject|the contour light remains spatially distinct from the interior key-lit surfaces
background_wash|color_wash|Background Color Wash/배경 컬러 워시|colored illumination covers a broad named background receiving area|its spill boundary preserves the separately specified subject illumination
cross_color_light|cross_color_light|Cross-Color Lighting/Color Separation Lighting/교차 색 조명|differently colored light contributions arrive from distinct visible directions|their separate receiving footprints follow surface orientation and occlusion
chromatic_subject|figure_ground|Neutral Field Chromatic Subject/중성 배경 유채색 피사체|the subject retains visible chromatic hues within its contour|the surrounding background remains relatively neutral along that contour
neutral_subject|figure_ground|Chromatic Field Neutral Subject/유채색 배경 중성 피사체|the subject remains relatively neutral within its contour|the surrounding background retains visible chromatic hues along that contour
depth_palette|depth_palette|Foreground Midground Background Palette/Layered Color Palette/Color Depth Separation/전중후경 배색|foreground middle and background planes each carry a distinct assigned palette role|overlap scale or perspective makes all three spatial planes independently readable
atmospheric_color|atmospheric_color|Atmospheric Color Separation/대기 색 분리|distant planes show weaker chroma and local tonal contrast than nearer planes|overlapping depth cues and intervening atmosphere make the distance order readable
color_framing|color_framing|Color Framing/색 프레이밍|colored scene regions visibly bracket or surround the focal subject|the focal subject remains readable inside the colored framing regions
color_blocks|color_blocks|Color Blocking/Large Color Fields/컬러 블로킹|large bounded color fields organize the principal composition|each field retains photographic surface shading or depth cues
diagonal_split|color_split|Diagonal Color Split/대각 색 분할|two large colored regions occupy opposite sides of a diagonal boundary|the directional division remains readable across the principal composition
horizontal_bands|color_bands|Horizontal Color Bands/가로 색 띠|assigned colored regions form an ordered stack of horizontal bands|each band has a readable boundary and visible horizontal extent
vertical_bands|color_bands|Vertical Color Bands/세로 색 띠|assigned colored regions form an ordered row of vertical bands|each band has a readable boundary and visible vertical extent
radial_color|radial_color|Radial Color Arrangement/방사형 배색|colored regions extend as rays from a shared visible center|the separate rays remain readable along their outward directions
concentric_color|radial_color|Concentric Color Structure/동심 배색|colored regions form nested surrounding zones around a shared visible center|the inner and outer zones retain separate readable boundaries
spatial_gradient|spatial_gradient|Spatial Gradient/Ombré/공간 그라데이션|color changes smoothly along a specified physical surface or spatial path|the transition follows position along that path across the visible surface
complex_subject|palette_complexity|Simple Background Complex Subject Palette/단순 배경 복합 피사체 배색|the subject contains more distinct principal hue families than the background|the background keeps fewer hue families even where its texture is detailed
complex_background|palette_complexity|Complex Background Simple Subject Palette/복합 배경 단순 피사체 배색|the background contains more distinct principal hue families than the subject|the subject keeps fewer hue families even where its texture is detailed
split_toning|split_toning|Split Toning/스플릿 토닝|shadows and highlights carry distinct assigned color tendencies across the selected scope|midtone transitions connect the tonal color regions while preserving readable surface shading
duotone|duotone|Duotone/듀오톤|the selected scope remaps dark and light tonal regions through two declared color endpoints|the two-color tonal treatment recurs across differently oriented surfaces and preserves shading
tritone|duotone|Tritone/트라이톤|the selected scope remaps dark middle and light tonal regions through three declared color anchors|the three-color tonal treatment recurs across differently oriented surfaces and preserves shading
global_tint|global_tint|Global Tint/Color Cast Unification/전역 틴트|a shared color bias affects the explicitly selected image scope|relative shading and material distinctions remain readable inside that tinted scope
gradient_mapping|gradient_mapping|Gradient Mapping/그라디언트 맵|the selected scope maps dark middle and light tonal values to an ordered sequence of declared color stops|matching tonal values share the mapped color treatment across different screen positions
'''

lighting = {'multicolor_lighting','key_fill_color','colored_rim','color_wash','cross_color_light'}
grading = {'tone_temperature','split_toning','duotone','global_tint','gradient_mapping'}
spatial = {'color_framing','color_blocks','color_split','color_bands','radial_color','depth_palette','accent_distribution','color_rhythm','color_bridge'}
rows=[]
for line in AUTHORED.strip().splitlines():
    ident,family,labels,a,b=line.split('|')
    rows.append(dict(id=ident,family=family,labels=labels.split('/'),components=[a,b]))

# Remaining broad names are search-only inspiration. They never define all-of profiles.
advisory = {
 'limited_palette':['Limited Palette'], 'polychromatic':['Polychromatic'],
 'chroma_separation':['Saturation / Chroma Contrast','Subject–Background Saturation Separation','Color Pop'],
 'chroma_distribution':['Soft-on-Soft'], 'tonal_layering':['Tonal Harmony','Tone-on-Tone'],
 'single_accent':['Single Color Accent','Chromatic Accent'], 'color_rhythm':['Color Rhythm'],
 'color_anchor':research['color_anchor']['source_terms'],
 'temperature_field':['Warm-Dominant','Cool-Dominant'],
 'temperature_separation':['Warm–Cool Contrast','Subject–Background Temperature Separation'],
 'depth_temperature':['Temperature Gradient'],
 'tone_temperature':['Shadow Tint','Midtone Tint','Highlight Tint'],
 'multicolor_lighting':['Bi-Color Lighting','RGB Lighting','Gel Contrast'],
 'colored_rim':['Contrasting Rim Light'], 'color_wash':['Color Wash'],
 'figure_ground':['Subject–Background Color Separation','Figure–Ground Color Contrast','Character–Environment Palette Contrast'],
 'color_split':['Split Color Composition'], 'spatial_gradient':['Gradient'],
 'color_zones':['Color Zoning'], 'palette_complexity':['Palette Density Contrast'],
 'three_way_grade':['Three-Way Color Grading'], 'cross_processed':['Cross-Processed Palette'],
 'discord':research['discord']['source_terms'],
 'tetradic':['Tetradic','Double Complementary'],
 'value_contrast':['Light–Dark / Value Contrast'],
}
extension={'schema_version':'photo-prompt-research-extension/v1','slots':{},'visual_semantics':[]}
profiles=[]
scope={}
coverage={key:{'candidates':[],'profiles':[],'source_terms':r['source_terms']} for key,r in research.items()}
for row in rows:
    ident='cr_'+row['id']; family=row['family']; r=research[family]
    slot='lighting' if family in lighting else 'color_grading' if family in grading else 'color'
    dims=['lighting','color'] if family in lighting else ['color','composition'] if family in spatial else ['color']
    parts=row['components']; phrase='; '.join(parts); cid='cr_candidate_'+row['id']
    entry={'id':cid,'ko':row['labels'][-1],'en':phrase,'aliases':row['labels'],'concept_units':parts,
      'affected_dimensions':dims,'weight':0.45,'tags':['color_relations_visual_semantics',slot],
      'keywords':row['labels']+parts,'embedding_text':'Selected visible color relation: '+phrase}
    extension['slots'].setdefault(slot,[]).append(entry)
    profiles.append({'id':ident,'category':'selected_color_region_relation',
      'activation':{'exact_terms':[phrase],'requires_adult_character':False,'semantic_discovery_requires_component_evidence':False},
      'semantics':{'definition':phrase,'paraphrase_examples':row['labels'],
        'contrast_examples':r['reject_substitutes'],
        'claim_limits':['Broad color labels alone do not specify this complete selected relation.','Hue-wheel geometry requires a declared wheel; no fixed hues, area ratio, skin treatment or physical production method is implied.']},
      'concept_candidate':{'concept_terms':row['labels']+parts},
      'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
      'reject_substitutes':r['reject_substitutes'],
      'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':[
         {'id':f'component_{i}','match_terms':[part],'evidence_field':f'component_{i}_phrase','evidence_terms':[part],
          'min_content_words':3,'instruction':'Keep this selected color relation visible: '+part,
          'render_gate':{'id':f'vo_{ident}_{i}','review_scale':'native' if row['id']=='micro_accent' else 'both',
           'description':part+'. Judge the declared owners and scope in saved pixels; missing, merged, reversed or unclear relations fail.'}}
          for i,part in enumerate(parts,1)]}})
    extension['visual_semantics'].append({'id':'cr_variant_'+row['id'],'primary_visual_proposition':phrase,
      'hard_profile_ids':[ident],'component_groups':[{'id':f'component_{i}','visible_evidence':[part]} for i,part in enumerate(parts,1)],
      'candidate_ids':[cid],'candidate_slots':{cid:slot},'confusion_boundaries':r['reject_substitutes'],
      'source_keywords':row['labels'],'candidate_only':True,'activation_mode':'component_complete_exact_only'})
    coverage[family]['candidates'].append(cid); coverage[family]['profiles'].append(ident)
    scope[ident]={'source_ids':r['source_ids'],'source_support_level':r['source_support_level'],
      'claim':'Authored observable variant; not a universal synonym definition, aesthetic guarantee, or proof of capture process.'}

for family,labels in advisory.items():
    r=research[family]; cid='cr_advisory_'+family
    slot='lighting' if family in lighting else 'color_grading' if family in grading or family in {'three_way_grade','cross_processed'} else 'color'
    # Broad entries carry open interpretation, never candidate-to-hard-profile links.
    en=r['candidate_proposal']['positive_literal']
    dims=['lighting','color'] if slot=='lighting' else ['color']
    extension['slots'].setdefault(slot,[]).append({'id':cid,'ko':r['name_ko'],'en':en,
       'aliases':labels,'concept_units':[en],'affected_dimensions':dims,'weight':0.25,
       'tags':['color_relations_visual_semantics',slot],'keywords':labels+[en],'embedding_text':en})
    coverage[family]['candidates'].append(cid)

reuse={
 'tonal_key':['high_key_tonal_distribution','low_key_selective_illumination'],
 'role_hierarchy':['palette_role_hierarchy_relation'],
 'mixed_illuminants':['mixed_illuminant_white_balance_relation'],
 'selective_retention':['selective_color_same_surface_exception_relation'],
}
for family,c in coverage.items():
    c['status']='implemented_selected_variants' if c['profiles'] else 'advisory_only' if c['candidates'] else 'reuse_existing_with_scope_limits' if family in reuse else 'excluded_from_single_frame_runtime'
    if family in reuse:c['existing_ids']=reuse[family]
    c['qualification']='not_yet_render_qualified'
record={'contract_version':'photo-extension-maintenance/v1','record_id':'photo_prompt_color_relations_extension',
 'source_filename':'photo_prompt_color_relations_extension.json','authored_source_sha256':digest(extension),
 'runtime_keys':['slots','visual_semantics'],
 'maintenance_only':{'research_path':str(RESEARCH.relative_to(ROOT)),
  'source_ledger_sha256':hashlib.sha256((RESEARCH/'sources.json').read_bytes()).hexdigest(),
  'profile_scope':scope,'family_coverage':coverage,
  'limitations':['Warm/cool means relative appearance; a still does not establish CCT or capture process.',
    'Exact equiluminance and simultaneous contrast need separate measurement and perception protocols.',
    'Sequence-only patterns remain research data until a multi-frame runtime exists.',
    'Generic mid-key and low-key palette are not aliases for selective low-key lighting.',
    'Selective Color software adjustment is not equivalent to selective color retention.',
    'Ratios, exact color coordinates, preserved regions and palette owners must be authored for each selection.']},
 'adoption_scope':'Optional visible color relations; full selected components become all-of gates; broad labels remain advisory.'}
extension['maintenance_ref']={'contract_version':'photo-extension-maintenance-ref/v1','record_id':record['record_id'],'sha256':digest(record)}

def write(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
write(SKILL/'assets/photo_prompt_color_relations_extension.json',extension)
write(SKILL/'assets/photo_prompt_visual_obligations_color_relations.json',{
 'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1',
 'description':'Owner-bound color relationships; full components exact, broad palette labels advisory.', 'profiles':profiles})
write(HERE.parent/'extension-maintenance/photo_prompt_color_relations_extension.json',record)
write(HERE/'coverage.json',{'families':coverage,'counts':{'research_families':len(coverage),'candidates':sum(map(len,extension['slots'].values())),'profiles':len(profiles),'bundles':len(extension['visual_semantics'])}})
print(json.dumps({'candidates':sum(map(len,extension['slots'].values())),'profiles':len(profiles),'bundles':len(extension['visual_semantics'])}))
