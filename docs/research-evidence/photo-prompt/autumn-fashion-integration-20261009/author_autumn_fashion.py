"""Reviewed selected relationships; family names never become all-of duties."""
from pathlib import Path
import copy
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
RESEARCH = HERE.parent / "autumn-fashion-20261009"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import photo_candidate_semantics as cs
from photo_runtime_sources import source_update
import prompt_generator as pg

# Complete effects of each SELECTED clause, not the research family's axes.
# A vertical bar separates variants. Material behavior has two owning dimensions.
PROPERTY_ROWS = """001|structure.shirt_collar,neckline.outline,details.layer_order
002|color,pattern,structure.front_fastener_state,neckline.height,details.layer_order
003|structure.front_placket,structure.front_panels
004|silhouette.lower_leg_width,footwear.shaft_height,details.layer_order
005|structure.patch_pockets
006|structure.front_fastener_state,material.surface_relief,details.layer_order
007|structure.yoke,details.tassel_fringe_braid,material.surface_relief
008|structure.front_fastener,structure.front_overlap,material.surface_relief
009|color,material.visible_weave,material.transmission,material.surface_relief,details.layer_order
010|structure.wrap_overlap,structure.waist_adjuster
011|length.hem_landmark,fit.waistband_landmark,details.layer_order,coverage.abdominal_gap
012|structure.front_fastener,fit.contact_distribution,structure.tucked_hem,details.layer_order
013|structure.front_fastener_state,material.specular_response,details.layer_order
014|structure.waist_adjuster,structure.belt_loops,structure.front_overlap
015|structure.sleeve_attachment
016|structure.front_fastener|structure.lapel,structure.front_fastener,structure.front_overlap
017|structure.wrap_overlap,structure.waist_adjuster
018|silhouette.convex_volume,fit.hem_taper,length.hem_landmark
019|structure.neck_opening,structure.shoulder_panel,length.hem_landmark
020|length.hem_landmark,structure.front_overlap,fit.body_clearance
021|structure.front_fastener,structure.front_overlap
022|fit.hem_gathering,structure.waist_band,material.visible_weave
023|structure.collar_tabs,structure.front_fastener
024|structure.patch_pockets,structure.front_fastener,material.visible_weave
025|structure.collar,material.visible_weave,material.surface_relief
026|structure.quilt_stitching,material.surface_relief
027|structure.front_fastener,length.hem_landmark,details.layer_order
028|structure.front_fastener_state,structure.inner_top,color,material.visible_weave,details.layer_order
029|structure.front_fastener,neckline.outline
030|structure.front_ties,structure.front_fastener
031|coverage.shoulder,coverage.arm,length.hem_landmark,details.layer_order
032|structure.strap_attachment
033|structure.collar,structure.neck_ties
034|neckline.height,structure.neck_folds|neckline.height,structure.neck_band
035|neckline.outline
036|neckline.outline,neckline.depth
037|neckline.outline,structure.neck_folds,material.drape,material.specular_response|neckline.outline
038|coverage.shoulder,coverage.opening_location,structure.sleeve_attachment|coverage.shoulder,structure.sleeve_attachment
039|coverage.upper_edge,neckline.height,material.visible_weave,material.transmission,structure.panel_connection|structure.strap_attachment,coverage.shoulder
040|fit.contact_distribution,material.visible_weave,material.transmission
041|structure.waist_adjuster,fit.waist_suppression,silhouette.width_distribution
042|coverage.upper_edge,details.layer_order,structure.inner_top
043|structure.cup_seam,structure.bone_casing
044|structure.princess_seam
045|details.peplum,silhouette.lower_fullness,details.layer_order
046|material.drape,structure.waist_attachment,length.hem_landmark
047|structure.stitch_rows,structure.gather_anchor|structure.smock_stitches,structure.pleat_attachment
048|coverage.armhole,fit.armhole_depth,details.layer_order
049|structure.back_strap_connection|structure.back_strap_connection
050|coverage.opening_location,structure.panel_connection
051|coverage.lateral_bust,coverage.armhole|coverage.lower_bust,length.hem_landmark
052|coverage.abdominal_gap,fit.waistband_landmark,length.hem_landmark|coverage.abdominal_gap,fit.waistband_landmark,length.hem_landmark
053|material.transmission,material.visible_weave,details.layer_order,structure.inner_top
054|length.hem_landmark
055|silhouette.width_distribution
056|structure.pleat_direction,structure.fold_attachment|structure.pleat_direction,structure.fold_attachment
057|structure.wrap_overlap,structure.waist_adjuster
058|silhouette.lower_fullness,structure.hem_gathering,structure.inner_hem
059|material.visible_weave,structure.neck_folds,length.hem_landmark
060|structure.inner_top,coverage.arm,structure.collar,details.layer_order
061|coverage.opening_location,structure.slit,length.hem_landmark|structure.vent,structure.panel_overlap
062|structure.leg_bifurcation,silhouette.lower_leg_width,material.drape
063|silhouette.outer_leg_curve,silhouette.volume_peak,fit.hem_taper,length.hem_landmark
064|fit.thigh_contact,silhouette.flare_origin,silhouette.hem_width
065|structure.leg_bifurcation,silhouette.hem_width,length.hem_landmark
066|structure.wrap_overlap,structure.visible_shorts,details.layer_order
067|structure.stirrup_strap,length.hem_landmark
069|material.visible_weave,material.surface_relief|material.visible_weave,material.surface_relief
070|material.visible_weave
071|material.surface_relief,material.specular_response,material.drape
072|material.specular_response,material.drape
073|material.visible_weave,material.transmission,color,details.layer_order,structure.inner_top
074|material.transmission,material.drape,silhouette.sleeve_volume,structure.cuff_gathering
075|material.specular_response,footwear.shaft_height|material.surface_relief,material.specular_response,material.drape
076|material.surface_relief,structure.collar
077|material.visible_weave,material.surface_relief
078|details.cable_knit
079|material.visible_weave,material.transmission,details.layer_order,structure.inner_top
080|material.visible_weave
081|material.surface_relief
082|color,material.visible_weave
083|color,pattern,material.visible_weave|color,pattern,material.visible_weave
084|pattern|pattern,material.visible_weave
085|pattern,material.drape
086|fit.shoulder.seam_position,structure.sleeve_attachment,coverage.shoulder|silhouette.sleeve_volume,structure.cuff_gathering
087|length.sleeve,structure.cuff_edge,coverage.hand
088|structure.lapel,structure.collar
089|structure.lacing,structure.front_fastener,structure.eyelets
090|structure.hem_edge,material.surface_relief
091|structure.strap_anchors,structure.hardware
093|footwear.shaft_height,length.hem_landmark,details.layer_order
094|footwear.elastic_gusset,footwear.upper_panel_connection
095|footwear.oxford_derby_brogue|footwear.strap_attachment
096|footwear.heel_platform_wedge
097|accessories.leg_warmer,details.layer_order,material.visible_weave
098|accessories.sock_stocking_tights,color,material.transmission|accessories.sock_stocking_tights,material.visible_weave,material.transmission
099|details.garter_suspender,details.layer_order
100|accessories.headwear,headwear.crown_brim_geometry
101|accessories.neck_wear_position,details.layer_order
102|structure.strap_anchors,structure.hardware,details.layer_order
103|accessories.glove_mitten,coverage.hand
104|structure.front_fastener_state,length.hem_landmark,details.layer_order|fit.body_clearance,fit.contact_distribution,material.visible_weave,details.layer_order
105|color,material.surface_relief,material.visible_weave,details.layer_order
106|structure.tucked_hem,details.layer_order
107|structure.front_fastener_state,details.cardigan_opening,details.layer_order,structure.inner_top
108|material.transmission,material.visible_weave,details.layer_order,structure.inner_top
109|structure.front_fastener_state,material.visible_weave,details.layer_order,structure.inner_top
110|length.hem_landmark,structure.visible_shorts,details.layer_order
111|coverage.opening_location,material.visible_weave,details.layer_order,structure.inner_top
112|neckline.outline,coverage.upper_chest"""

# Positive paraphrases preserve these existing contracts in full. No new alias
# replaces their stronger component/gate set or turns the whole family into one.
REUSE = {
 (18,1):("wardrobe_style","fit_ff07_v1_candidate","fit_ff07_v1", "cocoon coat sides bow outward at the torso and narrow again toward its lower hem"),
 (38,2):("garment_detail","fit_ff19_v2_candidate","fit_ff19_v2", "off-shoulder bodice edge below both shoulder tips with sleeves joined to that lowered edge"),
 (39,2):("garment_detail","clt_ct038_v1","clothing_ct038_v1", "the halter bodice strap continues around the back of the same wearer's neck"),
 (44,1):("garment_detail","fit_ff34_v2_candidate","fit_ff34_v2", "a princess seam joins the bodice front and side-front panels through the shaped waist"),
 (47,1):("garment_detail","fit_ff37_v2_candidate","fit_ff37_v2", "parallel stitch rows enclose repeated small gathers on the same shirred panel"),
 (49,1):("garment_detail","fit_ff52_v2_candidate","fit_ff52_v2", "two cross-back straps intersect once and continue to opposite lower anchors on the same top"),
 (49,2):("garment_detail","fit_ff52_v1_candidate","fit_ff52_v1", "racerback shoulder straps converge into a central yoke that joins the same top's lower band"),
 (51,1):("garment_detail","pfe_lateral_chest_candidate","pfe_lateral_chest", "bounded adult lateral breast contour beside the arm opening of an opaque bodice that covers the central breast and retains its continuous side edge"),
 (51,2):("garment_detail","pfe_lower_chest_candidate","pfe_lower_chest", "bounded adult lower breast contour below the identifiable hem of an opaque top covering the central breast, distinct from the abdomen"),
 (52,2):("garment_detail","pfe_navel_candidate","pfe_navel", "the adult navel landmark on continuous abdominal skin is uncovered between a separate upper hem and lower waistband"),
 (54,1):("garment_detail","clt_ct076_v1","clothing_ct076_v1", "a visible midi textile hem ends below the knee and above the ankle"),
 (56,1):("garment_detail","clt_ct063_v1","clothing_ct063_v1", "parallel knife pleat folds overlap toward one shared direction"),
 (78,1):("wardrobe_style","clt_ct008_v1","clothing_ct008_v1", "raised cable-knit strands cross in repeating columns on the same sweater surface"),
 (86,1):("garment_detail","fit_ff09_v1_candidate","fit_ff09_v1", "the drop-shoulder shirt sleeve joins beyond the shoulder tip on the upper arm and hangs from that lower seam"),
 (86,2):("garment_detail","clt_ct047_v1","clothing_ct047_v1", "the full bishop sleeve gathers into its own narrow wrist cuff"),
 (95,1):("footwear","clt_ct122_v1","clothing_ct122_v1", "Derby eyelet facings lie stitched over the vamp of that same shoe"),
 (99,1):("garment_detail","pfe_garter_path_candidate","pfe_garter_path", "the adult waist belt and stocking welt have distinct edges joined by a descending garter strap and its visible lower clip"),
}

REWRITE = {
 (3,1):("The coat's uninterrupted front panels hang beside a narrow front placket.", {"type":"flank","subject":"coat front panels","object":"same coat's narrow center-front placket"}),
 (24,1):("Two flap chest pockets sit beside the denim jacket's button-front opening.", {"type":"flank","subject":"denim jacket chest pockets","object":"same jacket's button-front opening"}),
 (25,1):("The barn jacket's ribbed corduroy collar rests above its smooth body panels.", {"type":"rest_above","subject":"barn-jacket corduroy collar","object":"same jacket's smooth body panels"}),
 (87,1):("The same wearer's thumb passes through the cuff opening; the extended sleeve covers the back of that same hand.", None),
 (107,1):("One fastened cardigan button joins the front edges; below it, the edges diverge over a separate camisole.", None),
 (110,1):("The long sweater hem covers most of the separate shorts; a short edge of those same shorts remains visible below it.", None),
 (112,1):("The adult wearer's collarbones and upper chest remain visible above the blouse's broad neckline.", None),
}

# Positive Korean phrases describe only the selected realization. Source tables
# and family alternatives remain in the external research/term mapping.
KO = {
16:["짝 루프를 통과하는 더플 토글","겹친 앞판의 두 버튼 열 위 피코트 라펠"],
28:["색과 편성 표면이 맞는 별도 니트 두 겹"],
34:["위쪽 가장자리가 되접힌 롤넥","한 가장자리를 갖는 짧은 모크넥"],
37:["캐미솔 목선 양끝 사이의 처진 새틴 접힘","중앙에서 내려앉는 스위트하트 목선의 두 호"],
38:["목선과 소매 사이 양 어깨의 둥근 개구"],
47:["평행 스티치 사이의 작은 반복 모음 주름","인접 플리트를 연결하는 스모킹 장식 스티치"],
53:["별도 캐미솔 목선 위를 덮는 얇은 블라우스 조직"],
56:["한 방향으로 겹치는 나이프 플리트","넓은 평면 양쪽의 서로 반대 박스 접힘"],
61:["허벅지 지점부터 발목 밑단까지 열린 옆 슬릿","하단 패널이 서로 겹치는 뒤 벤트"],
69:["치마 표면을 따라 선 세로 코듀로이 웨일","재킷 표면에서 솟는 작은 부클레 실 루프"],
75:["부츠 샤프트 위의 경계 뚜렷한 페이턴트 하이라이트","소매 접힘 위 짧은 스웨이드 기모 표면"],
79:["별도 캐미솔 위 카디건 코 사이에 반복된 작은 편성 눈구멍"],
83:["스웨터 편성 앞판의 작은 배색 모티프 가로 띠","실제 코 격자를 따르는 넓은 배색 경계"],
84:["반복 V자를 이루는 헤링본 대각선","편성 마름모 위를 교차하는 아가일 사선"],
98:["같은 다리에 피부색이 비치는 연속된 어두운 타이츠","같은 다리 위 반복 마름모 피시넷 구멍"],
104:["열린 긴 코트 사이로 보이는 무릎 위 짧은 치마","별도 밀착 니트에서 떨어져 선 넓은 블레이저 앞판"],
107:["한 버튼 여밈 아래 별도 캐미솔 위로 벌어지는 카디건"],
108:["별도 캐미솔 목선이 읽히는 시어 메시 겹"],
110:["대부분 덮이면서 밑단 일부는 보이는 별도 숏 팬츠"],
111:["블라우스 상부의 경계 있는 개구로 보이는 별도 레이스 겹"],
}

def dump(path, value):
 path.parent.mkdir(parents=True, exist_ok=True)
 path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n")

def main():
 cards = json.loads((RESEARCH / "semantic-cards.json").read_text())
 cards = cards if isinstance(cards,list) else cards["cards"]
 props={int(line.split('|')[0]):[part.split(',') for part in line.split('|')[1:]] for line in PROPERTY_ROWS.splitlines()}
 ext={"schema_version":"photo-prompt-research-extension/v1","slots":{},"visual_semantics":[],"existing_slot_context_extensions":{}}
 profiles=[];decisions=[];backlog=[]
 data=pg.load_json(ASSETS/"photo_prompt_tags.json")
 known={(slot,row['id']):row for slot,rows in data['slots'].items() for row in rows if isinstance(row,dict)}
 oldprofiles={p['id']:p for p in pg.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')['profiles']}
 for c in cards:
  num=int(c['id'][3:])
  if not c['drafts']:
   backlog.append({'card_id':c['id'],'disposition':'specification_metadata_not_a_native_pixel_contract','reason':c['claim_limits_ko'],'source_ids':c['source_ids']});continue
  assert len(props[num])==len(c['drafts']),c['id']
  for variant,d in enumerate(c['drafts'],1):
   key=(num,variant)
   if key in REUSE:
    slot,cid,pid,paraphrase=REUSE[key]; assert (slot,cid) in known and pid in oldprofiles
    ext['existing_slot_context_extensions'].setdefault(slot,{})[cid]={
      'paraphrases':[paraphrase], 'contexts':[{'id':f'autumn_reuse_{num}_{variant}', 'meaning':oldprofiles[pid]['semantics']['definition'],'claim_limits':c['claim_limits_ko']}]}
    decisions.append({'card_id':c['id'],'variant':variant,'candidate_id':cid,'profile_id':pid,'slot':slot,'disposition':'reuse_existing_complete_contract','source_ids':c['source_ids'],'reviewed_existing_definition':oldprofiles[pid]['semantics']['definition'],'positive_paraphrase':paraphrase});continue
   clause,relation=REWRITE.get(key,(d['phrase_en'],None));relation=relation or d['relation']
   pid=f'autumn_afr{num:03}_v{variant}';cid=pid+'_candidate'
   parts=[part.strip().rstrip('.')+'.' for part in clause.split(';')]
   effects=[{'dimension':'appearance','target':'main_subject','property':'wardrobe.'+p} for p in props[num][variant-1]]
   # The literal identifies its garment instance. Adding that garment is allowed
   # only when garment type is open, as well as its structural/surface axes.
   effects.insert(0,{'dimension':'appearance','target':'main_subject','property':'wardrobe.garment_type'})
   effects += [{'dimension':'material','target':'main_subject','property':'wardrobe.'+p} for p in props[num][variant-1] if p.startswith('material.')]
   if num==87:effects.append({'dimension':'pose','target':'main_subject','property':'posture.thumb_cuff_contact'})
   dims=list(dict.fromkeys(e['dimension'] for e in effects))
   slot='surface_material' if 69<=num<=85 else ('wardrobe_style' if num<=13 or 104<=num<=111 else ('footwear' if 93<=num<=96 else ('wardrobe_accessory' if 97<=num<=103 else 'garment_detail')))
   # Existing runtime slots are the authority; there is no new slot family.
   if slot not in data['slots']:slot='garment_detail'
   ko=KO.get(num,[relation['subject']+' → '+relation['object']]*len(c['drafts']))[variant-1]
   terms=[ko,clause]
   row={'id':cid,'ko':ko,'en':clause,'weight':0.35,'tags':['clothing'],'aliases':terms,'keywords':list(dict.fromkeys(terms+parts)),
        'embedding_text':clause+' | '+relation['subject']+' '+relation['type'].replace('_',' ')+' '+relation['object'],
        'concept_units':parts,'relations':[{'id':pid+'_owner_relation',**relation}],
        'affected_dimensions':dims,'affected_properties':effects,'core_assertion_discovery':True,'for_any':['human']}
   adult=num==112
   if adult:row['for_any']=['adult'];row['facets']={'safety_tier':['adult_only']}
   ext['slots'].setdefault(slot,[]).append(row)
   components=[]
   for i,part in enumerate(parts,1):
    components.append({'id':f'component_{i}','match_terms':[part],'evidence_field':f'component_{i}_phrase','evidence_terms':[part],
      'min_content_words':3,'instruction':'Keep this selected same-owner visible relation readable: '+part,
      'render_gate':{'id':f'vo_{pid}_{i}','review_scale':'native','description':part+' The declared garment boundaries, owner and both relation endpoints must be readable in this same saved image. Missing, occluded, substituted or partial evidence fails.'}})
   profiles.append({'id':pid,'category':'autumn_fashion_selected_visible_relation',
    'activation':{'exact_terms':[clause],'requires_adult_character':adult,'semantic_discovery_requires_component_evidence':True,
      'hard_activation':{'contract_version':'photo-visual-hard-activation/v1','required_any_groups':[{'id':'selected_visible_variant','any_terms':[clause]}]}},
    'semantics':{'definition':clause,'paraphrase_examples':[ko,'Observable relation between '+relation['subject']+' and '+relation['object']],
      'visual_components':parts,'contrast_examples':c['confusion_boundaries_ko'],
      'claim_limits':[c['claim_limits_ko'],'Only this selected visible realization is asserted. Family labels, sibling variants and optional discovery do not activate a combined duty.',
       'Garment boundaries, layer order and wearing state belong to the same wearer. A cropped hem, slit or opening never alone establishes the visibility of another body region.',
       'Pixels do not establish fiber composition, DEN value, hidden garment presence, manufacturing technique, social class, age, personality or performance.']},
    'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':components},
    'concept_candidate':{'concept_terms':terms,'core_assertion_discovery':True,'affected_dimensions':dims,'affected_properties':effects},
    'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
    'reject_substitutes':c['confusion_boundaries_ko']})
   ext['visual_semantics'].append({'id':pid+'_bundle','primary_visual_proposition':clause,'hard_profile_ids':[pid],
      'component_groups':[{'id':f'component_{i}','visible_evidence':[part]} for i,part in enumerate(parts,1)],
      'candidate_ids':[cid],'candidate_slots':{cid:slot},'confusion_boundaries':c['confusion_boundaries_ko'],
      'source_keywords':terms,'candidate_only':True,'activation_mode':'component_complete_exact_only','relations':copy.deepcopy(row['relations'])})
   decisions.append({'card_id':c['id'],'variant':variant,'candidate_id':cid,'profile_id':pid,'slot':slot,'disposition':'new_scoped_selected_relation','source_ids':c['source_ids'],
       'relation':relation,'affected_properties':effects,'equivalence_review':'Owner-bound clause adds the listed selected endpoints or combination beyond existing general garment/family labels; stronger equivalent contracts are reused separately.',
       'revised_research_clause':clause!=d['phrase_en']})
 previous_path=ASSETS/'photo_prompt_autumn_fashion_extension.json'
 prior_ref=json.loads(previous_path.read_text()).get('maintenance_ref') if previous_path.exists() else None
 revision=1
 while (ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/f'autumn-fashion-selected-relations-20261009-v{revision}.json').exists():revision+=1
 record_id=f'autumn-fashion-selected-relations-20261009-v{revision}'
 record={'schema_version':'photo-extension-maintenance/v1','record_id':record_id,'maintenance_only':True,
  'source_filename':'photo_prompt_autumn_fashion_extension.json','authored_source_sha256':cs.digest(ext),
  'scope':'113 research cards; individually reviewed visible clauses, stronger existing contracts reused, three specification-only families held outside pixels.',
  'candidate_changes':decisions,'evidence_basis':'42 source pages with term-specific interpretation and claim boundaries in autumn-fashion-20261009.',
  'validation_status':{'authored':'pending','retrieval':'pending','native_pixels':'pending','user_acceptance':'not_tested'}}
 if prior_ref:record['prior_maintenance_ref']=prior_ref
 ext['maintenance_ref']={'contract_version':cs.MAINTENANCE_VERSION,'record_id':record_id,'sha256':cs.digest(record)}
 manifest=json.loads((ASSETS/'photo_prompt_source_manifest.json').read_text())
 for filename,kind in [('photo_prompt_autumn_fashion_extension.json','candidate'),('photo_prompt_visual_obligations_autumn_fashion.json','visual_profile')]:
  present=[s for s in manifest['sources'] if s['file']==filename]
  if present:
   assert len(present)==1 and present[0]['kind']==kind and present[0]['required'] is True,filename
   continue
  manifest['sources'].append({'file':filename,'kind':kind,'required':True,'load_order':1+max(s['load_order'] for s in manifest['sources'] if s['kind']==kind)})
 with source_update(ASSETS.parent):
  dump(ASSETS/'photo_prompt_autumn_fashion_extension.json',ext)
  shape=json.loads((ASSETS/'photo_prompt_visual_obligations_fashion_fit.json').read_text())
  dump(ASSETS/'photo_prompt_visual_obligations_autumn_fashion.json',{'schema_version':shape['schema_version'],'relation_contract_version':shape['relation_contract_version'],
     'description':'Individually selected garment topology, surface, hem, layering and current wearing-state relations. Family alternatives remain independent.', 'profiles':profiles})
  dump(ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/(record_id+'.json'),record)
  dump(ASSETS/'photo_prompt_source_manifest.json',manifest)
 dump(HERE/'runtime-integration.json',{'state':'authored_pending_validation','new_candidate_count':sum(map(len,ext['slots'].values())),
    'new_profile_count':len(profiles),'reused_candidate_count':len(REUSE),'research_card_count':len(cards),'decisions':decisions,'specification_backlog':backlog})
 terms=json.loads((RESEARCH/'term-plan.json').read_text())['terms']
 mapping=[{'term_id':t['term_id'],'source_term':t['source_term'],'card_id':t['card_id'],'status':'family_related_selected_variants_not_universal_alias_activation',
    'runtime_variants':[{'candidate_id':d['candidate_id'],'profile_id':d['profile_id'],'disposition':d['disposition']} for d in decisions if d['card_id']==t['card_id']],
    'specification_metadata':[b for b in backlog if b['card_id']==t['card_id']]} for t in terms]
 dump(HERE/'term-runtime-map.json',{'count':len(mapping),'terms':mapping})
 print(json.dumps({'new_candidates':sum(map(len,ext['slots'].values())),'new_profiles':len(profiles),'reused':len(REUSE),'metadata_cards':len(backlog),'mapped_terms':len(mapping)}))

if __name__=='__main__':main()
