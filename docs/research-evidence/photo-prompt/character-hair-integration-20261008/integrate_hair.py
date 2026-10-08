"""Author reviewed hair relations. Research/holds stay outside runtime assets."""
from __future__ import annotations
import argparse,copy,hashlib,json,re,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SKILL=ROOT/'skills/photo-prompt-image-generator'
ASSETS=SKILL/'assets'
RESEARCH=HERE.parent/'character-hair-20261008'
sys.path.insert(0,str(SKILL/'scripts'))
import photo_candidate_semantics as cs
import prompt_generator as pg
from photo_contracts import INTENT_LOCK_DIMENSIONS
from visual_profile_contracts import compile_visual_profile,validate_visual_profile_source
from photo_runtime_sources import source_update

def read(p):return json.loads(p.read_text())
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def unique(values):return list(dict.fromkeys(v for v in values if v))
def unique_effects(values):
 out=[]
 for row in values:
  if row not in out:out.append(row)
 return out

# These are reviewed equivalent relations, not label-only equivalence guesses.
REUSE={
 'hair-cut-hime':('hair_style','hime_cut','hime_cut_structural'),
 'hair-cut-center_part':('hair_style','y2kr_center_part',None),
 'hair-cut-deep_side_part':('hair_style','y2kr_deep_side_part',None),
 'hair-cut-supp-two_block':('hair_style','two_block_korean_cut','two_block_disconnected_cut'),
 'hair-cut-supp-buzz':('hair_style','buzz_cut',None),
 'hair-cut-pixie':('hair_style','pixie_cut',None),
 'hair-cut-wolf':('hair_style','wolf_cut',None),
 'hair-cut-curtain_bangs':('hair_style','curtain_bangs',None),
 'hair.topology.high_ponytail':('hair_style','y2kr_high_pony',None),
 'hair.topology.side_ponytail':('hair_style','sca_h09',None),
 'hair.topology.twintails':('hair_style','bilateral_twin_tail_gather','bilateral_twin_tail_gather'),
 'hair.topology.braided_pigtails':('hair_style','sca_h11',None),
 'hair.topology.bubble_ponytail':('hair_style','y2kr_bubble_pony',None),
 'hair.topology.half_up':('hair_style','y2kr_half_up',None),
 'hair.topology.space_buns':('hair_style','y2kr_space_buns',None),
 'hair.topology.crown_braid':('hair_style','sca_h10',None),
 'hair.topology.cornrows':('hair_style','cornrows','cornrow_scalp_row_topology'),
 'hair.topology.locs':('hair_style','dreadlocks','locs_cord_structure'),
 'hair.topology.curly':('hair_style','appearance_h042',None),
 'hair_color_state.split_color':('hair_color','sca_h19',None),
 'hair_color_state.peekaboo':('hair_color','sca_h20',None),
 'hair_color_state.ombre':('hair_color','sca_h21',None),
 'hair_color_state.money_piece':('hair_color','y2kr_money_piece',None),
 'hair_color_state.chunky_highlights':('hair_color','y2kr_chunky_highlights',None),
 'hair_color_state.colored_streak':('hair_color','y2kr_color_streak',None),
 'hair_color_state.ahoge':('hair_style','sca_h01',None),
 'hair_color_state.antenna_hair':('hair_style','sca_h02',None),
 'hair_color_state.twin_drills':('hair_style','sca_h05',None),
 'hair.main.ribbon_or_fabric_bow':('hair_style','appearance_h106',None),
 'hair.main.scrunchie':('wearable_accessory','y2kr_scrunchie',None),
 'hair.main.tinsel_attachment':('wearable_accessory','y2kr_hair_tinsel',None),
}

# English component realizations deliberately remove incidental colours, gender,
# poses, covering garments, processes and administrative prose from research.
COLOR={
 'highlights':['selected hair sections are lighter than the surrounding base','the lighter sections remain bounded by those same strands'],
 'lowlights':['selected hair sections are darker than the surrounding base','the darker sections follow the same strand lengths'],
 'babylights':['very fine lighter hair sections run among the base strands','the individual narrow sections remain visually separate'],
 'chunky_highlights':['broad lighter ribbons contrast with the darker base hair','base-colored strands remain visible between the broad ribbons'],
 'reverse_ombre':['the selected hair roots are lighter than the terminal lengths','the color deepens gradually along the same continuous strands'],
 'dip_dye':['a contrasting color occupies the selected terminal hair region','a readable color boundary separates that tip region from the upper lengths'],
 'color_melt':['neighboring hair colors connect through intermediate colors','the blended transitions remain inside the same continuous hair strands'],
 'shadow_root':['a darker region occupies the selected hair roots','the root color transitions softly into lighter neighboring lengths'],
 'underlights':['a contrasting color occupies the selected lower or inner hair layer','the colored strands remain part of the same hairstyle beneath the outer layer'],
 'colored_bangs':['the selected front fringe has a contrasting chosen color','that color remains bounded by the front-fringe hair region'],
 'colored_tips':['a different chosen color occupies the selected hair tips','the tip color continues along the ends of the same strands'],
 'white_forelock':['a localized white hair section occupies the front hairline','the white section remains continuous with the same scalp hair'],
 'salt_and_pepper':['white and darker strands intermingle in the selected hair region','both strand colors remain readable under the same light'],
 'white_appearance':['the chosen pale white color stays inside the hair contours','the pale hue remains readable across the selected strands'],
 'neon_color':['the selected hair region carries a vivid highly saturated chosen color','the vivid color remains bounded by the hair strands'],
 'emissive_hair':['light visibly originates along the selected hair strands','a corresponding glow reaches the neighboring surface from those strands'],
 'rainbow_hair':['several chosen colors occupy distinct regions of the same hair','the arrangement preserves a readable sequence across those hair regions'],
 'wet_look':['the selected hair sections carry a glossy wet-looking set finish','aligned strand groups and narrow reflections make that surface finish readable'],
 'ahoge':['one long isolated lock projects above the crown','the raised lock remains continuous with the same scalp hair'],
 'antenna_hair':['two or more thin locks project separately above the scalp','each raised lock remains attached to its own visible hair root'],
 'drill_hair':['a selected hair mass coils into a conical spiral','the spiral narrows toward its terminal tip'],
 'twin_drills':['two separately gathered hair masses coil into conical spirals','each spiral narrows continuously toward its own terminal tip'],
 'hair_intakes':['two hair arches face forward above the front of the head','the scooped arches remain continuous with the same scalp hair'],
 'hair_body_overlap':['long hair continues from the head across the selected body region','the hair occupies the foreground of that same body region'],
 'hair_bikini_structure':['continuous hair lengths wrap around the declared torso region','those same lengths connect through visible ties into a garment-like arrangement'],
}
COLOR.update({
 'split_color':['two substantial lateral hair regions carry distinct chosen colors','the division belongs to the same hairstyle rather than an illumination boundary'],
 'peekaboo':['a differently colored inner hair layer is partly visible beneath the outer layer','the outer hair layer partly occludes the colored inner strands'],
 'ombre':['the chosen hair color changes gradually from roots toward tips','intermediate colors follow the same continuous strand lengths'],
 'money_piece':['chosen lighter front hair sections frame the face','the lighter sections remain distinct from the base-colored hair behind them'],
 'colored_streak':['one or more bounded colored sections follow the hair lengths','the adjacent base color remains visible beside those same sections'],
})

EXCLUDE={
 'hair-cut-uniform_layers','hair-cut-hush','hair-cut-tassel','hair-cut-leaf','hair-cut-guile','hair-cut-as_style','hair-cut-comma','hair-cut-supp-pageboy',
 'hair.topology.fine_strands','hair.topology.apparent_density','hair.topology.faux_locs','hair.topology.feed_in_braids','hair.topology.stitch_braids','hair.topology.lace_braid','hair.topology.wet_look',
 'hair.main.fabric_scarf','hair.main.hair_formed_bow','hair.main.pin_insertion','hair.main.threaded_or_clamped_adornment','hair.main.tape_attachment',
 'hair.main.clip_in_weft','hair.main.ponytail_piece','hair.main.lace_front','hair.main.topper',
}
MAIN_OVERRIDES={
 'ribbon_or_fabric_bow':['a separate fabric ribbon wraps the selected hair base','the ribbon knot and cloth tails stay distinct from the hair strands'],
 'baby_hair':['short hair strands trace the forehead hairline','those short strands remain continuous with the same hairline'],
 'flyaway':['fine strands lift away from the main hair flow','the lifted strands remain attached to the same hairstyle'],
 'laid_edges':['short hairline strands follow a visible curved swoop close to the forehead','the curved strands remain continuous with the same hairline'],
 'scrunchie':['a ruched fabric band encircles the selected gathered hair base','the hair tail continues from inside that same band'],
 'claw_clip':['a separate claw clip grips the selected gathered hair section','the clip and gathered hair remain in visible contact'],
 'tinsel_attachment':['fine reflective tinsel strands attach within the hair','the tinsel follows the same hair lengths while retaining separate reflective edges'],
 'hair_neck_wrap':['one continuous hair length extends from the scalp toward the neck','that same hair length curves around the neck'],
 'daenggi':['a cloth daenggi attaches to the end of the selected braid','the cloth remains distinct from the interlaced hair above it'],
 'sangtu':['hair lengths converge upward toward the crown','the gathered lengths wrap into one continuous crown knot'],
}

def refs(c):
 return [x.get('source_id',x.get('id')) if isinstance(x,dict) else x for x in c.get('source_refs',c.get('source_support',[]))]
def hids(c):
 return unique(c.get('reference_keyword_ids',[])+[q['id'] for k in ['reference_keywords','input_keywords'] for q in c.get(k,[])])
def relations(c,key):
 out=[dict(id=key+'_owner',type='declared_owner_scope',subject='the selected hair arrangement',object='main_subject')]
 for i,r in enumerate(c.get('directed_relations',[]),1):
  a=r.get('from',r.get('source'));b=r.get('predicate',r.get('relation'));z=r.get('to',r.get('target'))
  if a and b and z:out.append(dict(id=key+'_r'+str(i),type=b,subject=a,object=z))
 return out
def property_for(c,slot):
 if slot=='hair_color':return 'hair.color.'+c['id'].split('.')[-1]
 if slot=='wearable_accessory':return 'hair.accessories.'+c['id'].split('.')[-1]
 suffix=c['id'].split('.')[-1].removeprefix('hair-cut-supp-').removeprefix('hair-cut-').replace('-','_')
 if c['id'].startswith('hair-cut-') and ('bangs' in suffix):return 'hair.fringe.'+suffix
 return 'hair.style.'+suffix

def author(c,units,slot):
 key=re.sub('[^a-z0-9_]+','_',c['id'].lower()).strip('_');eid='chrh_'+key;pid='chrh_rel_'+key
 ko=c['labels']['ko'];en='; '.join(units)
 aliases=unique([c['labels']['en'],ko])
 # Shared ambiguous bare surfaces are research labels, never exact aliases.
 if any(x in c['id'] for x in ['graduation','hair_neck_wrap','ribbon_or_fabric_bow']):aliases=[]
 effects=[dict(dimension='appearance',target='main_subject',property=property_for(c,slot))]
 # Hair configuration can affect regional length/part/fringe locks too. Until
 # a narrower effect has been separately verified, this conservative parent
 # declaration prevents a new label path from bypassing an existing lock.
 if slot=='hair_style':effects=unique_effects(effects+[dict(dimension='appearance',target='main_subject',property='hair.style')])
 candidate=dict(id=eid,ko=ko,en=en,weight=0.45,tags=['human','hair','observable_relation'],for_any=['human'],
  aliases=aliases,keywords=units,paraphrases=[en,ko],embedding_text=en,concept_units=units,
  relations=relations(c,key),affected_dimensions=['appearance'],affected_properties=effects,core_assertion_discovery=True)
 boundary=unique(c.get('confusion_boundaries',c.get('exclusions_confusion_boundaries',[])))
 if not boundary:boundary=['A glossy dry surface alone does not establish regional moisture.','A cropped state boundary cannot establish both adjoining hair regions.']
 signature=c.get('minimum_visible_signature',c.get('minimum_signature',c.get('minimum_visual_signature',{})))
 if isinstance(signature,dict):signature=signature.get('all_of',[])
 components=[dict(id='owned_arrangement',match_terms=unique([en,*units,ko]))]
 gates=[dict(id='vo_'+key+'_all',review_scale='native',description='Inspect the same declared hair owner in original pixels: '+en+'. Every selected relation must be visible together; a cropped or occluded endpoint is unobservable, not a pass.')]
 for i,phrase in enumerate(signature,1):
  gates.append(dict(id='vo_'+key+'_sig_'+str(i),review_scale='native',description='Inspect this selected minimum relation on the same visible owner and region: '+phrase+'. Partial or substituted evidence fails; hidden evidence is unobservable.'))
 profile=dict(id=pid,category='character_hair_owned_relation',
  activation=dict(exact_terms=[en],requires_adult_character=False,semantic_discovery_requires_component_evidence=True,
   hard_activation=dict(contract_version='photo-visual-hard-activation/v1',required_any_groups=[dict(id='complete_owned_proposition',any_terms=[en])])),
  semantics=dict(definition='On the selected hair owner and visible region, '+en+'.',paraphrase_examples=['Visible hair relation: '+en,ko],visual_components=units,contrast_examples=boundary,
   claim_limits=['This selected visible arrangement preserves the declared owner, region and property locks.','Names and approximate retrieval do not prove process, origin, identity, age, personality or medical cause.']),
  concept_candidate=dict(concept_terms=unique([*units,*aliases,ko]),core_assertion_discovery=True,affected_dimensions=['appearance'],affected_properties=effects),
  runtime_expression=dict(default_mode='definition_with_optional_label',prompt_label_terms=[],forbidden_prompt_terms=[],runtime_forbidden_labels=[]),
  authored_components=dict(contract_version='photo-authored-visual-components/v2',components=components,
   discovery=dict(minimum_component_groups=1,required_group_ids=['owned_arrangement']),obligations=[dict(component_ids=['owned_arrangement'],
    evidence=[dict(field='owned_arrangement_phrase',requirement=dict(min_content_words=3,must_mention_any=unique([en,*units])))],
    instruction='Preserve every selected relation on this same hair owner and region: '+en+'.',render_gates=gates)]),
  reject_substitutes=boundary)
 validate_visual_profile_source(profile);compile_visual_profile(profile)
 return candidate,profile

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');parser.add_argument('--refresh-owned',action='store_true');a=parser.parse_args()
 if a.apply and ((HERE/'RUNTIME-PUBLICATION.json').exists() or (ROOT/'docs/research-evidence/photo-prompt/extension-maintenance/character-hair-owned-relations-20261008-v2.json').exists()):
  raise RuntimeError('This initial drafting helper cannot overwrite published source history. Create a reviewed successor maintenance record for a later revision.')
 cards=[c for n in ['cuts-cards.json','cuts-supplement-cards.json','topology-cards.json','color-state-cards.json','main-cards.json'] for c in read(RESEARCH/n)['cards']]
 current=pg.load_json(ASSETS/'photo_prompt_tags.json');existing={(s,e['id']):e for s,rows in current['slots'].items() for e in rows}
 extension=dict(schema_version='photo-prompt-research-extension/v1',slots={},existing_slot_context_extensions={},visual_semantics=[])
 visual=dict(schema_version='photo-visual-obligation-registry-extension/v1',relation_contract_version='photo-visual-relation/v1',profiles=[])
 decisions=[]
 for c in cards:
  cid=c['id'];family=cid.split('.')[-1];units=[];slot='hair_style';reason=''
  if cid in EXCLUDE:reason='Specific name/measurement/installation requires more evidence; preserve research hold and existing compatible variants.'
  elif cid.startswith('hair_color_state.'):
   if family not in COLOR:reason='Process, diagnostic, causal, temporal or broad context is not a default single-frame appearance duty.'
   else:units=COLOR[family];slot='hair_style' if family in {'wet_look','ahoge','antenna_hair','drill_hair','twin_drills','hair_intakes','hair_body_overlap','hair_bikini_structure'} else 'hair_color'
  elif cid.startswith('hair.main.'):
   if family in MAIN_OVERRIDES:units=MAIN_OVERRIDES[family];slot='wearable_accessory' if family in {'scrunchie','claw_clip','tinsel_attachment','daenggi'} else 'hair_style'
   else:reason='Keep researched context pending subtype/installation verification.'
  elif cid.startswith('hair.topology.'):
   if c.get('source_support_status')=='partial_label_support' and cid not in REUSE:reason='Specific label support remains partial; do not silently standardize it.'
   else:
    text=c['proposed_candidate_wording']['en'];text=text.split('; keep')[0].strip().rstrip('.')
    text={'hair.topology.knotless_braids':'Individual interlaced braids continue from small, low-profile root transitions on the same scalp', 'hair.topology.locs':'Several elongated fiber-textured hair bundles retain continuous cord-shaped bodies from their roots toward their tips'}.get(cid,text)
    units=[text]
  else:
   text=c['proposed_candidate']['wording_en']
   overrides={'hair-cut-one_length':'a continuous one-length outer perimeter follows the selected natural fall','hair-cut-supp-undercut':'a selected side or nape hair region remains much shorter than the adjacent upper hair','hair-cut-see_through_bangs':'small visible skin gaps separate the selected forehead fringe sections'}
   units=[overrides.get(cid,text)]
  if reason:
   decisions.append(dict(card_id=cid,glossary_ids=hids(c),disposition='maintenance_context_or_explicit_hold',reason=reason,source_refs=refs(c)));continue
  # A proposal's administrative instructions and incidental constraints never
  # become retrieval prototypes. Review such rows explicitly before emission.
  assert units and all(not re.search(r'\b(no |without |keep |preserve |do not|not prove)',u,re.I) for u in units),(cid,units)
  candidate,profile=author(c,units,slot)
  if cid in REUSE:
   reuse_slot,eid,pid=REUSE[cid];assert (reuse_slot,eid) in existing,(cid,eid)
   extension['existing_slot_context_extensions'].setdefault(reuse_slot,{})[eid]=dict(paraphrases=unique([candidate['en'],c['labels']['ko']]))
   decisions.append(dict(card_id=cid,glossary_ids=hids(c),disposition='reviewed_equivalent_paraphrase_enrichment',slot=reuse_slot,candidate_ids=[eid],profile_ids=[pid] if pid else [],source_refs=refs(c)))
   continue
  extension['slots'].setdefault(slot,[]).append(candidate);visual['profiles'].append(profile)
  extension['visual_semantics'].append(dict(id='chrh_bundle_'+candidate['id'],primary_visual_proposition=candidate['en'],hard_profile_id=profile['id'],
    component_groups=units,candidate_ids=[candidate['id']],candidate_slots={candidate['id']:slot},confusion_boundaries=profile['reject_substitutes'],relations=candidate['relations'],source_keywords=[],activation_mode='optional_postcore'))
  decisions.append(dict(card_id=cid,glossary_ids=hids(c),disposition='new_owned_visible_relation',slot=slot,candidate_ids=[candidate['id']],profile_ids=[profile['id']],source_refs=refs(c)))
 # A moisture state is scoped to its declared region; dry/wet regions can coexist.
 extra=dict(id='hair.integration.regional_moisture',labels=dict(ko='부위별 수분 경계',en='Localized damp hair'),minimum_signature=['수분 단서가 선택한 같은 모발 구역에 있다','젖은 구역의 가닥 뭉침·무게와 인접 구역의 상태가 각각 보인다'],directed_relations=[dict(source='damp_region',relation='adjoins',target='remaining_hair')],source_refs=['M06','hc_src_15'],reference_keyword_ids=['H369'])
 c,p=author(extra,['a selected hair region carries visible moisture cues and compact strand bundles','the state boundary remains readable beside the other hair regions'],'hair_style')
 c['affected_properties']=[dict(dimension='appearance',target='main_subject',property='hair.moisture_and_configuration')];p['concept_candidate']['affected_properties']=copy.deepcopy(c['affected_properties'])
 extension['slots']['hair_style'].append(c);visual['profiles'].append(p)
 decisions.append(dict(card_id=extra['id'],glossary_ids=['H369'],disposition='regional_state_projection',slot='hair_style',candidate_ids=[c['id']],profile_ids=[p['id']],source_refs=['M06','hc_src_15']))
 cs.validate_candidate_entries(extension,set(INTENT_LOCK_DIMENSIONS));cs.validate_extension_keys(extension)
 dump(HERE/'candidate-source.proposed.json',extension);dump(HERE/'visual-source.proposed.json',visual)
 mapping=dict(status='reviewed_authored_projection',new_candidates=sum(map(len,extension['slots'].values())),new_profiles=len(visual['profiles']),existing_enrichments=sum(map(len,extension['existing_slot_context_extensions'].values())),decisions=decisions,
  boundary='Research definitions and minimum pixel gates are not render success. No hidden origin, process or demographic inference is serialized as a visible duty.')
 dump(HERE/'INTEGRATION-MAP.json',mapping)
 if not a.apply:print(json.dumps({k:v for k,v in mapping.items() if k!='decisions'}));return
 newfile='photo_prompt_character_hair_extension.json';profilefile='photo_prompt_visual_obligations_character_hair.json'
 if a.refresh_owned:
  assert read(ASSETS/newfile)['maintenance_ref']['record_id']=='character-hair-owned-relations-20261008'
  assert all(q['id'].startswith('chrh_rel_') for q in read(ASSETS/profilefile)['profiles'])
 else:assert not (ASSETS/newfile).exists() and not (ASSETS/profilefile).exists()
 base=read(ASSETS/'photo_prompt_visual_obligations.json');tags=read(ASSETS/'photo_prompt_tags.json');manifest=read(ASSETS/'photo_prompt_source_manifest.json')
 wet=next(q for q in base['profiles'] if q['id']=='wet_damp_clumped_hair_state')
 wet['activation']['exact_terms']=[t for t in wet['activation']['exact_terms'] if t not in {'wet-look hair','wet look hair'}]
 wet['semantics']['paraphrase_examples']=[t for t in wet['semantics']['paraphrase_examples'] if 'wet-looking' not in t or 'moisture' not in t]
 wet['concept_candidate']['concept_terms']=[t for t in wet['concept_candidate']['concept_terms'] if not t.startswith('not ') and not t.startswith('wet-looking') and t!='temporary finish state']
 wc=next(q for q in tags['slots']['hair_style'] if q['id']=='wet_damp_clumped_hair_state')
 wc['aliases']=[t for t in wc.get('aliases',[]) if t not in {'wet-look hair','wet look hair'}]
 wc['embedding_text']='actual damp hair on the selected region with reduced airy volume, grouped strands and coherent moisture weight or local adherence'
 wc['keywords']=['visible moisture in the selected hair region','reduced airy volume and compact strand bundles','coherent downward weight or localized contact adherence']
 balayage=next(q for q in base['profiles'] if q['id']=='balayage_ribbon_color_placement')
 balayage['activation']['exact_terms']=['irregular lighter ribbon hair placement','selected balayage ribbon pattern','불규칙한 밝은 리본 헤어 배색']
 balayage['semantics']['definition']='A selected distributed color pattern with irregular lighter ribbons, a darker base, soft root transitions and readable base continuity. Coloring method and any coexisting root-to-tip gradient are separate axes.'
 balayage['semantics']['contrast_examples']=['a uniform gradient with no separately readable color ribbons','lighting reflections on otherwise uniform pigment']
 balayage['reject_substitutes']=['gradient_without_ribbon_structure','uniform_lightening_without_base_gaps','lighting_specular_only']
 balayage['concept_candidate']['concept_terms']=['irregular lighter hair ribbons','soft root transition','varied mid-length and end placement','visible base color between ribbons','nonuniform ribbon widths']
 bc=next(q for q in tags['slots']['hair_color'] if q['id']=='balayage_ribbon_color_placement')
 bc['ko']='불규칙한 밝은 리본 헤어 배색';bc['en']='irregular lighter hair ribbons with soft root transitions and base-colored gaps'
 bc['aliases']=copy.deepcopy(balayage['activation']['exact_terms'])
 bc['keywords']=copy.deepcopy(balayage['concept_candidate']['concept_terms'])
 bc['embedding_text']='irregular lighter ribbons follow the selected hair lengths through soft root transitions and varied mid-length and end placement; base-colored gaps remain visible beside the same ribbons'
 source=balayage['authored_components'];last=source['components'][-1];last['match_terms']=['the irregular colored ribbons remain separately readable along the strands','각 색 리본과 바탕의 구분되는 영역']
 obligation=source['obligations'][-1];evidence=obligation['evidence'][-1];evidence['requirement']['must_mention_any']=['the irregular colored ribbons remain separately readable along the strands','base-colored gaps separate those same irregular lighter ribbons']
 obligation['instruction']='Show irregular lighter ribbons, soft root transitions, varied mid-length and end placement, and base-colored gaps on the same visible hair. A coexisting root-to-tip gradient preserves the independently readable ribbons and gaps.'
 obligation['render_gates'][-1]['description']='Colored ribbons and intervening base regions remain readable as hair color, including when a length gradient coexists; specular reflection alone cannot establish them.'
 validate_visual_profile_source(wet);validate_visual_profile_source(balayage)
 record=dict(contract_version='photo-extension-maintenance-record/v1',record_id='character-hair-owned-relations-20261008',authored_source_sha256=cs.digest(extension),
  maintenance_only=dict(source_revision=dict(research='docs/research-evidence/photo-prompt/character-hair-20261008',mapping='INTEGRATION-MAP.json',phase='authored_not_render_qualified',holds='INTEGRATION-MAP.json decisions retain process/diagnostic/partial-source boundaries')))
 extension['maintenance_ref']=dict(contract_version='photo-extension-maintenance-ref/v1',record_id=record['record_id'],sha256=cs.digest(record))
 record_path=ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/ (record['record_id']+'.json')
 with source_update(SKILL):
  dump(record_path,record);dump(ASSETS/newfile,extension);dump(ASSETS/profilefile,visual);dump(ASSETS/'photo_prompt_visual_obligations.json',base);dump(ASSETS/'photo_prompt_tags.json',tags)
  for file,kind in [(newfile,'candidate'),(profilefile,'visual_profile')]:
   if a.refresh_owned:
    assert len([row for row in manifest['sources'] if row['file']==file and row['kind']==kind])==1
    continue
   order=max(row['load_order'] for row in manifest['sources'] if row['kind']==kind)+1
   manifest['sources'].append(dict(file=file,kind=kind,required=True,load_order=order))
  dump(ASSETS/'photo_prompt_source_manifest.json',manifest)
 dump(HERE/'AUTHORED-APPLICATION.json',dict(mapping,changed_existing_sources=['photo_prompt_tags.json','photo_prompt_visual_obligations.json','photo_prompt_source_manifest.json'],new_sources=[newfile,profilefile],metadata_record=str(record_path.relative_to(ROOT))))
 print(json.dumps({k:v for k,v in mapping.items() if k!='decisions'}))

if __name__=='__main__':main()
