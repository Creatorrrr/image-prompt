"""Install source-scoped architectural variants; broad names remain advisory."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parent
A=R/'skills/photo-prompt-image-generator/assets'
draft=json.loads((P/'candidate-drafts.json').read_text())
def digest(d):return hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
# English operationalizations of the three authored research gates, in profile order.
rows='''the tower stands on the raised mound|a separate defended yard lies below the mound|an ascending route connects the two ground levels
the main tower dominates smaller buildings inside the ward|an enclosing boundary contains the service buildings|the tower entrance connects to the courtyard ground
an inner defensive circuit rises behind an outer circuit|a continuous strip separates the two wall circuits|both circuits enclose the same castle
defensive walls enclose multiple houses and connected streets|an entering street passes through the town gate|the urban fabric extends beyond a single castle courtyard
defensive towers project beyond the connecting wall face|a continuous wall joins the adjacent towers|a walkable surface runs behind the parapet
solid parapet blocks alternate with open gaps|the outside background remains visible through the gaps|the repeated blocks belong to the top of the parapet
an outer defended enclosure stands before the main gatehouse|one bounded approach connects the two entrances|the main doorway opens into a gatehouse passage
a heavy gridded gate occupies the entrance opening|the grid edges sit inside vertical guide grooves|the gate is partly lowered along those upright grooves
a raised bridge deck hinges at the gate threshold|the tilted deck exposes the ditch beneath it|a gap separates the deck end from the outer approach
a stone parapet projects beyond the main wall face|openings pierce the underside between supporting corbels|the underside openings lie outside the wall vertical plane
a narrow slit opens through the exterior wall|the slit connects to a wider interior recess|the recess sides expose the thickness of the defensive wall
an exposed dry ditch floor lies beside the wall base|two banks define a visible depression in the ground|a crossing bridges the ditch above its dry floor
angular bastions project from the connected main defensive wall|a wedge-shaped ravelin stands separately across the ditch|the detached outwork shields the main entrance approach
mounted cannon rest on carriages on a broad gun platform|the cannon barrels face outward across the defensive perimeter|the parapet openings align with the cannon positions
a built-in seat occupies the depth of the masonry recess|the side reveals connect the seat space to the outer window|the outer opening sits beyond the seat plane
exposed timber members form the high hall roof|short projecting hammerbeams connect to the upper roof supports|a continuous communal hall floor lies below the roof
stone ribs intersect across the chapel ceiling|the ribs continue toward supports beside pointed openings|a distinct worship area occupies the chapel end
open doorways align along one continuous sightline|wall returns reveal separate rooms beyond successive thresholds|the doorway sequence continues through actual adjoining rooms
one gallery wall carries a repeated sequence of mirrors|actual windows occupy the opposite gallery wall|reflected windows correspond to those real opposite openings
carved ornament belongs to bounded wooden wall panels|curved shell-like and foliate relief has visible depth|the panels integrate around the mirror and wall openings
connected residential wings enclose a palace courtyard|the upper gallery bays align over the lower level|the two adjoining elevations meet around the inner court
two distinct helical stair flights wind around one core|the shared central core remains visibly hollow|each flight retains a separate continuous circulation path
an open-sky court is enclosed by a perimeter arcade|a central basin connects physically to shallow water channels|the channels lead toward the surrounding palace rooms
small cellular niches form successive ceiling tiers|adjacent cells contain distinct recessed volumes|the cell tiers make a three-dimensional wall-to-ceiling transition
individual brick units and mortar courses remain legible|the brickwork continues through thick walls and arched openings|the arches are integrated into the same masonry mass
an open lower arcade faces the waterside|a finer openwork gallery occupies the level above it|a broad upper wall mass rests above the gallery
related classical motifs recur across walls and ceiling panels|the ornamental bands coordinate with the room divisions|a furnishing repeats the same decorative vocabulary
low planting or lawn borders form a ground-level pattern|paths remain distinct from the bounded planting compartments|a legible garden axis faces the palace building
dense greenery encloses a small garden room|a narrow entry opens into a usable interior clearing|a basin or sculpture organizes the enclosed garden space
container-grown citrus trees stand inside a garden gallery|tall windows open through thick masonry reveals|a passable aisle connects the tree containers to the garden-facing entrance
open sky appears above the former room where its roof is missing|surviving walls and window openings enclose the former interior floor|localized fallen masonry lies below the broken upper structure
crafted rockwork surrounds a shaped grotto chamber|a constructed opening joins the chamber to a garden path|a landscaped water feature remains connected to the grotto setting
monumental stair runs connect to usable upper landings|surrounding balconies face the stair interior|the stair and balconies share one tall opera-house space
squared coursed blocks meet an irregular stonework region|mortar joints follow the boundaries of the actual stones|both masonry regions join as parts of the standing wall'''.splitlines()
assert len(rows)==len(draft['profiles'])
ext={'schema_version':'photo-prompt-research-extension/v1','slots':{'location':[],'composition':[]},'visual_semantics':[]}
profiles=[]
for p,row in zip(draft['profiles'],rows):
    phrases=row.split('|');pid=p['id'];components=[]
    for i,phrase in enumerate(phrases,1):
        components.append({'id':f'component_{i}','match_terms':[phrase],'evidence_field':f'component_{i}_phrase','evidence_terms':[phrase],'min_content_words':3,'instruction':'Preserve this architectural relation: '+phrase,'render_gate':{'id':f'vo_{pid}_{i}','review_scale':p['component_gates'][i-1]['review_scale'],'description':phrase+'. The relation must be visible in the saved image; a hidden or substituted connection does not pass.'}})
    profiles.append({'id':pid,'category':'palace_fortification_visible_relation','activation':{'exact_terms':['; '.join(phrases),'; '.join(g['description_ko'] for g in p['component_gates'])],'requires_adult_character':False,'semantic_discovery_requires_component_evidence':True},'semantics':{'definition':p['ko']+' as a selected architectural variant: '+'; '.join(phrases)+'.','paraphrase_examples':[p['scene_en'],*p['aliases']],'contrast_examples':p['reject_substitutes'],'claim_limits':[p['historical_scope'],p['claim_limits'],'Architecture does not establish a person identity, rank, nationality or photograph capture date.']},'concept_candidate':{'concept_terms':list(dict.fromkeys([p['ko'],*p['aliases'],*phrases]))},'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},'reject_substitutes':p['reject_substitutes'],'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':components}})
    candidates=[c for c in draft['candidates'] if c['profile_proposal_id']==pid]
    for c in candidates:
        e={k:c[k] for k in ['id','ko','en','aliases','concept_units','affected_dimensions']}
        e.update(weight=0.55,tags=['palace_fortification_visual_semantics',c['slot']],keywords=[p['ko'],*p['aliases'],c['en']],embedding_text=p['ko']+': '+c['en'])
        ext['slots'][c['slot']].append(e)
    ext['visual_semantics'].append({'id':pid,'primary_visual_proposition':p['scene_en'],'hard_profile_ids':[pid],'component_groups':[{'id':f'component_{i}','visible_evidence':[f]} for i,f in enumerate(phrases,1)],'candidate_ids':[c['id'] for c in candidates],'candidate_slots':{c['id']:c['slot'] for c in candidates},'confusion_boundaries':p['reject_substitutes'],'source_keywords':[p['ko'],*p['aliases']],'candidate_only':True,'activation_mode':'component_complete_exact_only'})
record={'contract_version':'photo-extension-maintenance/v1','record_id':'photo_prompt_palace_fortification_extension','source_filename':'photo_prompt_palace_fortification_extension.json','authored_source_sha256':digest(ext),'runtime_keys':['slots','visual_semantics'],'maintenance_only':{'research_path':str(P.relative_to(R)),'candidate_drafts_sha256':hashlib.sha256((P/'candidate-drafts.json').read_bytes()).hexdigest(),'source_ledger_sha256':hashlib.sha256((P/'sources.json').read_bytes()).hexdigest(),'profile_scope':{p['id']:{'source_ids':p['source_ids'],'limits':[p['historical_scope'],p['claim_limits']]} for p in draft['profiles']},'adoption_scope':'34 selected architectural variants; broad names remain advisory; no general era or provenance classifier'}}
write(R/'docs/research-evidence/photo-prompt/extension-maintenance'/ (record['record_id']+'.json'),record)
ext['maintenance_ref']={'contract_version':'photo-extension-maintenance-ref/v1','record_id':record['record_id'],'sha256':digest(record)}
write(A/'photo_prompt_palace_fortification_extension.json',ext)
write(A/'photo_prompt_visual_obligations_palace_fortification.json',{'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','description':'Selected architectural connections, spatial systems and material relations; no global era defaults.','profiles':profiles})
f=A/'photo_prompt_tags.json';s=f.read_text();marker='      "photo_prompt_historical_womenswear_extension.json"\n'
if 'photo_prompt_palace_fortification_extension.json' not in s:
    assert s.count(marker)==1;s=s.replace(marker,'      "photo_prompt_historical_womenswear_extension.json",\n      "photo_prompt_palace_fortification_extension.json"\n');f.write_text(s)
print('Installed 34 profiles / 102 gates / 68 candidates / 34 bundles')
