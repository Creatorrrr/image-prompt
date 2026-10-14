"""Serialize individually authored source alternatives. Root selections remain zero.
No proposal is signed against the current formal input and none is applied.
"""
import json,copy,hashlib
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
P=R/'native-inputs/prepared/review06250-00000-00020-149-02'
K=json.loads((P/'PREPARED-PACKET.json').read_text());A=json.loads((P/'ASSIGNMENT.json').read_text())
digest=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def effect(prop,target='illuminating_light',dimension='lighting'):
 return {'dimension':dimension,'target':target,'property':prop}

# These literal applications are editorial alternatives, not entailment claims
# about a bare original, universal noun rules, or automatic migrations.
MANUAL={
0:[('existing_neon_illumination',
 'For this explicitly bounded application, select neon-source illumination on an independently identified existing illuminating light and its independently identified existing illuminated receiver. Change the declared source type to neon. Preserve their established illumination relation and receiving scope. This selection does not add a light fixture, visible neon sign, text, person, object, place, color, intensity or direction.',
 [effect('lighting.source.type')],
 [('lighting.source.type','neon','lighting.source.type/v1')],['light_type'],
 'Neon as a lighting-source type is an editorial disambiguation. Applying it to an existing selected source/receiver is a new bounded application, not the unique interpretation of the original bare neon. No new fixture branch has been reviewed.')],
1:[('existing_lab_led_illumination',
 'For this explicitly bounded application, select LED illumination designated for laboratory use on an independently identified existing illuminating light and its independently identified existing illuminated receiver. Change the declared source type to LED and retain the laboratory-use designation as external application context for that same source. Preserve their established illumination relation and receiving scope. This selection does not add a laboratory room, research worker, medical purpose, person, fixture, other object, color, intensity or direction.',
 [effect('lighting.source.type')],
 [('lighting.source.type','led','lighting.source.type/v1')],['light_type'],
 'Both lab and led remain positive. LED is the source-type E; laboratory use is declared contextual designation, not a new laboratory location or an inferred capability. The new existing-source application is root-unselected. The original bare wording alone does not settle the lab qualifier attachment.')],
2:[('existing_softbox_modifier',
 'For this explicitly bounded application, select a softbox modifier for an independently identified existing illuminating light and its independently identified existing illuminated receiver. Change the declared illumination source modifier to softbox. Preserve their established illumination relation and receiving scope. This selection does not add a light fixture, support, window, room, person or other object, and does not assert a measured softness, direction, intensity, distance, color or shadow transition.',
 [effect('lighting.source.modifier')],
 [('lighting.source.modifier','softbox','lighting.source.modifier/v1')],['light_type'],
 'Softbox names the declared source modifier. The source does not state universal soft quality, so no light_quality E is invented. This editor-selected modifier application cannot authorize adding a new apparatus; apparatus addition remains a separately unreviewed possible application.')],
6:[('existing_hard_flash',
 'For this explicitly bounded application, select flash illumination with hard light quality on an independently identified existing illuminating light and its independently identified existing illuminated receiver. Change the declared source type to flash and the received illumination quality to hard. Preserve their established illumination relation and receiving scope. This selection does not add a flash unit, person, place or other object, or assert frontal direction, color, power, exposure, numeric angular extent or a complete lighting setup.',
 [effect('lighting.source.type'),effect('lighting.quality.hardness')],
 [('lighting.source.type','flash','lighting.source.type/v1'),('lighting.quality.hardness','hard','lighting.quality.hardness/v1')],['light_type','light_quality'],
 'Flash and hard are both explicit original meaning. Two actual E are retained; neither is downgraded to context/P. Existing-source/receiver selection is a proposed new bounded application and needs independent presence and relation witnesses.')],
7:[('existing_fluorescent_light_source',
 'For this explicitly bounded application, fluorescent means fluorescent-source illumination on an independently identified existing illuminating light and its independently identified existing illuminated receiver. Change the declared light source type to fluorescent. Preserve their established illumination relation and receiving scope. This selection does not add a lamp, fixture, fluorescent material, dye, person, laboratory, hospital, room or other object, and does not assert green color, flicker, intensity or direction.',
 [effect('lighting.source.type')],
 [('lighting.source.type','fluorescent','lighting.source.type/v1')],['light_type'],
 'The application explicitly chooses fluorescent light-source type rather than fluorescent surface material. This is new editorial disambiguation, not a fact donated by lighting metadata, a historical tag, or a claim that the original label uniquely selected a source.')],
8:[('travel_photographic_genre',
 'Select the travel-photograph genre and its travel subject-matter conventions for this image. Retain the complete travel-photograph meaning as the declared genre value. This application changes the image genre; it does not assert an actual journey or a travel history and does not add or replace a traveler, destination, scene, camera, object or physical photographic medium.',
 [effect('genre.selection','image','style')],
 [('genre.selection','travel_photography','genre.selection/v1')],['genre'],
 'Travel is retained in the whole genre value, not erased as metadata and not promoted into factual travel history/location. Photograph does not identify film/digital substrate. The genre application is explicitly proposed; any stronger factual travel-context interpretation remains unresolved rather than being silently lost.')],
10:[('pet_photographic_genre',
 'Select the pet-photography genre and its pet subject-matter theme for this image. Retain the complete pet-photography meaning as the declared genre value. This application changes the image genre and requires independently established image content compatible with that pet theme. It does not add or replace a pet, person or other subject, select a species, change count or establish pet identity from appearance.',
 [effect('genre.selection','image','style')],
 [('genre.selection','pet_photography','genre.selection/v1')],['genre'],
 'The pet qualifier remains in the actual selected genre. Existing compatible subject matter is an explicitly proposed applicability restriction, not an entailment that the original genre noun was existing-only. A proper independent pet identity/carrier witness and exact no-creation boundary must be root-selected before proof; no desired pet value is pre-frozen.')],
11:[('actual_natural_golden_hour',
 'For this explicitly selected interpretation, golden hour declares the actual natural-light day phase of this same scene and the corresponding golden-hour illumination of its independently identified existing illumination and receiver scope. Select the scene day phase as golden hour and the declared illumination phase treatment as natural golden hour. Preserve the established illumination relation and receiving scope. This application adds no light fixture, person, place or other object, and does not specify sunrise versus sunset, a clock time, weather, hue, numeric color temperature, direction, intensity or a complete lighting arrangement.',
 [effect('lighting.phase_treatment'),effect('timing.time_of_day','scene','timing')],
 [('lighting.phase_treatment','natural_golden_hour','lighting.phase_treatment/v1'),('timing.time_of_day','golden_hour','timing.time_of_day/v1')],['time_of_day'],
 'This alternative expressly chooses an actual natural-light day phase; it is not inferred from the old light_type binding. Original lighting E remains and timing E is added openly. Precise illumination treatment retains its own fact even if it supplies no eligible 149 lighting role. Source/receivers, guard witnesses and the complete new footprint require root selection.'),
 ('named_golden_hour_light_treatment_only',
 'For this explicitly selected interpretation, golden hour names an imitated golden-hour illumination treatment on an independently identified existing illuminating light and its independently identified existing illuminated receiver. Select that named illumination treatment while preserving their established illumination relation and receiving scope. The application does not establish the actual day phase and does not add a fixture, person, place or other object, or specify hue, numeric color temperature, direction, intensity, shadow transition or a complete lighting arrangement.',
 [effect('lighting.named_treatment')],
 [('lighting.named_treatment','imitated_golden_hour','lighting.named_treatment/v1')],[],
 'This is an expressly new imitation-treatment reading, not the unique meaning of golden hour and not the same source as the actual-day-phase alternative. Actual lighting E is retained; time_of_day, light_type, light_quality, lighting setup and aesthetic_trend are not justified by the named look alone. Current149 may leave a role gap; it stays pending, never diagnostic/no-op.')],
12:[('existing_soft_window_illumination',
 'For this explicitly bounded application, select soft window-mediated illumination on an independently identified existing illuminating light and its independently identified existing illuminated receiver, with an independently established window-mediated illumination path. Change the declared source route to window-mediated light and the received illumination quality to soft. Preserve the established light, path, receiver and receiving scope. This selection does not add a window, room, curtain, fixture, person or other object, or choose a window location, numeric softness, light direction, color or intensity.',
 [effect('lighting.source.route'),effect('lighting.quality.hardness')],
 [('lighting.source.route','window_mediated','lighting.source.route/v1'),('lighting.quality.hardness','soft','lighting.quality.hardness/v1')],['light_type','light_quality'],
 'Both window mediation and soft quality are preserved. The window path is independently established, not a new window/location inferred from light. Source/receiver/path selection is a proposed bounded application. Whether source-route metadata is enough to express the full owned path in the final native contract remains pending.')],
13:[('food_photographic_genre',
 'Select the food-photography genre and its food subject-matter theme for this image. Retain the complete food-photography meaning as the declared genre value. This application changes the image genre and requires independently established image content compatible with that food theme. It does not add or replace food, a person, tableware, a table or other objects, choose a dish, change count or declare cooking, stillness or a physical photographic medium.',
 [effect('genre.selection','image','style')],
 [('genre.selection','food_photography','genre.selection/v1')],['genre'],
 'The food qualifier remains in the actual genre. Existing-compatible content is a new explicit bounded application, not proof that every food-photography noun is existing-only. The food carrier/type and independent witness must be reviewed before fresh proof; old still_life tags do not create stillness facts.')],
14:[('dieselpunk_aesthetic_keep_setting_footprint',
 'Apply a dieselpunk aesthetic reading to this image. This selects its declared dieselpunk sensibility; it is an actual interpretive aesthetic change, not a statement of persistent world rules, institutions, history, fuel machinery, industrial fixtures, a particular emotion, new people or new objects. Preserve the original setting permission dimension for this application; any aesthetic retrieval role must be an explicitly reviewed view of that same canonical effect, without renaming its property or replacing its original permission footprint with a style-only footprint.',
 [effect('setting.aesthetic_reading','image','setting')],
 [('setting.aesthetic_reading','dieselpunk','setting.aesthetic_reading/v1')],['aesthetic_trend'],
 'Dieselpunk mood/감성 supports an actual aesthetic interpretation rather than world systems. The original setting dimension is intentionally retained while the previously coarse property is explicitly refined. A reviewed same-canonical-fact manual aesthetic view may be considered; it must not create a duplicate style effect or bypass original setting locks. Root selection, exact generic-view contract and all original/current lock comparisons are still required.')],
15:[('street_photographic_genre',
 'Select the street-photography genre and its photographic conventions for this image. Retain street photography as the complete genre value. This application changes the image genre, without choosing or replacing a physical street or city, adding a person or crowd, selecting a place, changing count, asserting unposed or candid capture, or choosing a physical photographic medium.',
 [effect('genre.selection','image','style')],
 [('genre.selection','street_photography','genre.selection/v1')],['genre'],
 'Street remains the named photographic genre/convention, not a physical location command or an inferred candid condition. This is an explicit genre-only application proposal; a factual street-location reading is neither merged into this alternative nor automatically erased from all possible interpretations.')],
19:[('interior_photographic_genre',
 'Select the interior-photography genre and its interior-space subject-matter theme for this image. Retain interior photography as the complete genre value. This application changes the image genre and requires independently established image content compatible with that interior-space theme. It does not add or replace a room, architectural structure, person, furniture or other objects, choose a lens, change count or establish a physical photographic medium.',
 [effect('genre.selection','image','style')],
 [('genre.selection','interior_photography','genre.selection/v1')],['genre'],
 'The interior-space qualifier is retained as the thematic photographic category. Independent compatible interior-space content is a proposed explicit applicability restriction, not an automatic existing-only reading of the original noun. The actual space/carrier and witness remain pending before a new source proof.')]
}

rows=[]
for ordinal,alternatives in MANUAL.items():
 cid=A['ids'][ordinal];before=K['current_records'][cid]
 for key,app,properties,values,roles,reason in alternatives:
  after=copy.deepcopy(before);after['content']['application_contract']=app
  after['effects']={'dimensions':sorted({p['dimension'] for p in properties}),'properties':sorted(properties,key=lambda p:(p['dimension'],p['target'],p['property']))}
  retained=before['effects']['dimensions'];assert set(retained)<=set(after['effects']['dimensions'])
  effects=[]
  for prop,value,vt in values:
   triples=[p for p in properties if p['property']==prop];assert len(triples)==1
   triple=triples[0]
   effects.append({**triple,'mode':'effect','operation':'set_value','value':{'type':vt,'value':value},'receiver_plan':'The actual independently selected existing receiver scope must be represented for illumination effects; none is chosen by this proposal. Image genre/aesthetic and scene day-phase effects do not add a separate receiver owner.' if triple['dimension']=='lighting' else 'Explicitly no separate receiver; the affected image or scene is the target itself.'})
  if ordinal in [0,1,2,6,7,11,12]:
   owners='Explicit selected-existing illumination source and explicit existing receiver scope, plus their independently frozen illumination relation. These targets are generic, not automatically light_source/light_receiver or main_subject. Presence P uses entity.presence/v1,present only after exact existing carrier selection; no desired neon/LED/flash/soft/fluorescent/golden-hour value is pre-frozen. Ordinal11 actual-day-phase alternative additionally owns scene day phase; ordinal12 additionally needs an independently frozen window-mediated path. No new entity is introduced.'
   guards='Preserve the actual intrinsic {} and actual own binding subject_applicability {}. New independently selected existing-carrier presence/relation obligations are a proposed bounded application; exact native targets, selected scope/member semantics and guard/fact witnesses must be manually authored against a root-selected source. Missing/unknown source, receiver, window path or relation stays pending; never default to a primary owner or empty receiver set.'
  else:
   owners='Image attributes bind only the independently declared image, not a new participant/place/prop. '+('The required independently established pet/food/interior-theme carrier is not supplied by a genre role; exact carrier identity/type and owner-selection protocol remain pending. No count or entity creation is authorized.' if ordinal in [10,13,19] else 'No candidate entity creation or desired-value prerequisite is supplied.')
   guards='Keep actual intrinsic {} and old own binding subject_applicability {}. The proposed named genre/aesthetic selection is an actual effect. Any new explicit compatibility restriction must be separately reviewed and expressed as source-grounded P/guard witnesses; candidate values cannot self-witness. For dieselpunk, original setting permission remains, and the aesthetic_trend spec deny_domains documentary/craft/wildlife remains independently cumulative if root selects that role.'
  rows.append({'ordinal':ordinal,'candidate_id':cid,'alternative_id':key,'status':'pending_root_editorial_selection','root_selected':False,'formal_proof':None,'source_before':before,'source_before_sha256':digest(before),'source_after':after,'source_after_sha256':digest(after),'delta':[{'pointer':'/content/application_contract','before_exists':False,'before':None,'after_exists':True,'after':app,'reason':reason},{'pointer':'/effects','before_exists':True,'before':before['effects'],'after_exists':True,'after':after['effects'],'reason':'Explicit coarse-effect precision preserving every original permission dimension. Added timing is disclosed only for the explicitly actual golden-hour alternative. No canonical property is renamed for a tag prefix.'}],'individual_reason':reason,'proposed_actual_effects':effects,'proposed_roles':roles,'owner_and_carrier_plan':owners,'sourceguard_and_binding_plan':guards,'ordinary_source_coverage_plan':'The new application_contract alone must directly ground its new application, owner restrictions and effects. The untouched bare EN/KO can only restate the source meaning actually present in that exact field; they do not donate new application, presence, relation, receiver or operation wording. Metadata/tags remain excluded. All fields need a fresh whole-source review after root selection.','native_pending_boundary':'Complete after source is supplied for editorial review only. No current-input signature, completed native proof, approval, inferred old-source OR, source application or operating activation is made.'})
out={'schema':'photo-explicit-source-editorial-alternatives/v1','task_name':'/root/review_06250_07250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':A['input']['sha256'],'catalog_sha256':'d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15','current_source_sha256':'8acdd741cdb846c8bb33b53ded16471363ece5747280b5b4893c25acdeed302d','prepared_candidate_count':13,'proposal_count':len(rows),'actual_whole_after_read_count':0,'root_selection_count':0,'formal_proof_count':0,'operational_count':0,'records':rows}
p=R/'authored/native_06250_first20_149_02.source-alternatives.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(p,hashlib.sha256(p.read_bytes()).hexdigest(),len(rows))
