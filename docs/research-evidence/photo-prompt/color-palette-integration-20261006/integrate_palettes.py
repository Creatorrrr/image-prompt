"""Project researched palettes into reviewed optional runtime applications.

Never copies research placeholder effects or hardens a palette/style name.
The original candidate/profile sources remain byte-for-byte intact.
"""
from pathlib import Path
import json
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
EVIDENCE = Path(__file__).resolve().parent
RESEARCH = EVIDENCE.parent / 'color-palette-semantics-20261006'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
from photo_candidate_semantics import digest

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

# Distinct owner/mechanism applications, not an entry for every style label.
# Targets stay generic until a run declares its actual owners. Property paths
# describe the real carrier effects, so reference face/hair preservation does
# not masquerade as a lock on unrelated cloth, object or lighting properties.
APPLICATIONS = {
  2: ('color', ['color'], 'warm-white, oatmeal and taupe local colors remain on their declared wall, cloth and seam regions, separated by small readable tonal steps'),
  4: ('color', ['color'], 'cream cloth, camel-brown leather and chocolate-brown wood retain three distinct local-color regions through their existing texture boundaries'),
  7: ('color', ['color'], 'one bounded olive detail retains visible green among larger ivory and mushroom-gray regions'),
  8: ('color', ['color'], 'one small cobalt-blue object stands apart from a larger off-white and graphite neutral field; the cobalt color remains confined to that object'),
  9: ('surface_material', ['color','material'], 'warm gold-colored reflections stay on the declared metallic trim against a larger dark field; the trim retains bounded reflective highlights rather than a flat yellow fill'),
  10: ('surface_material', ['color','material'], 'a leading ivory field, champagne-colored cloth and smaller warm gold-colored reflective fittings retain separate material surfaces'),
  11: ('surface_material', ['color','material'], 'warm brass-colored reflective trim remains separate from navy local-color panels and cream cloth'),
  12: ('surface_material', ['color','material'], 'deep emerald textile, a separate black ground and smaller gold-colored reflective fittings retain their own material boundaries'),
  14: ('surface_material', ['color','material'], 'muted warm gold-colored metallic trim remains readable against a dark aubergine field through bounded reflections'),
  15: ('surface_material', ['color','material'], 'cool platinum-colored metallic reflections remain separate from an ice-white field and a darker steel-gray boundary'),
  17: ('texture', ['color','appearance','material'], 'navy stripes repeat on the same white fabric carrier while a red trim remains localized along its declared edge'),
  18: ('texture', ['color','appearance','material'], 'black, white and red line families cross on the same beige fabric carrier with independently readable line widths and spacing'),
  19: ('texture', ['color','appearance','material'], 'green and red bands share the same bounded ribbon-shaped region over a cream carrier, with a readable boundary between the two bands'),
  20: ('surface_material', ['color','material'], 'aqua local color stays on the declared package, white stays on its ribbon and small silver-colored reflections stay on separate metallic fittings'),
  24: ('surface_material', ['color','material'], 'signal orange stays on the bounded trim against black local surfaces while silver-colored metallic fittings retain separate reflective highlights'),
  33: ('color', ['color'], 'the declared cobalt-blue, off-white and terracotta architectural surfaces retain three separate local-color owners'),
  41: ('color', ['color'], 'rose-pink and soft serenity-blue local surfaces remain separately bounded at comparably gentle chroma'),
  45: ('color', ['color'], 'blush, rose and wine-red regions retain three readable lightness tiers within the selected pink-red hue family'),
  49: ('color', ['color'], 'chocolate-brown, caramel-brown and cream ingredient regions remain separately bounded on the declared food surface'),
  50: ('color', ['color'], 'cobalt-blue belongs to the declared cup surface while espresso-brown beverage and light cream retain their separate ingredient regions'),
  51: ('color', ['color'], 'tomato-red, basil-green and mozzarella-white retain separate ingredient boundaries on the declared food surface'),
  57: ('texture', ['color','appearance'], 'black orthogonal lines separate unequal red, blue and yellow rectangular regions on the same light carrier'),
  65: ('color', ['color'], 'a warm orange garment region remains separate from the cooler teal background across their declared boundary'),
  66: ('lighting', ['lighting','color'], 'blue and amber illumination arrive from distinct directions; their receiving footprints follow local surface orientation and occlusion'),
  67: ('color_grading', ['color'], 'a restrained green bias recurs across the declared dark, middle and light tonal scope while relative shading and material distinctions remain readable'),
  72: ('color_grading', ['color'], 'the declared image scope retains achromatic black, white and gray shading except for one bounded red owner whose color stays inside its own outline'),
  73: ('lighting', ['lighting','color'], 'cyan and magenta illumination form separate directional receiving footprints in the dark scene; each footprint follows surface form and occlusion'),
  75: ('color', ['color'], 'a small lime-colored trim remains bounded against a larger electric-blue field and a separate charcoal ground'),
  76: ('lighting', ['lighting','color','material'], 'green luminous marks originate on the declared dark display surface; nearby receiving surfaces show separate weaker spill following their geometry'),
  77: ('lighting', ['lighting','color','material'], 'yellow painted structural regions retain matte local color while cyan light originates on a separate display surface and illuminates only its receiving surroundings'),
  78: ('surface_material', ['color','material'], 'silver-colored metal retains localized reflected highlights while separate ice-blue translucent plastic retains visible light transmission against a white field'),
  79: ('color', ['color'], 'lavender, blue and coral connect in that positional order along one continuous declared background surface, retaining the surface shading beneath the spatial gradient'),
  81: ('color', ['color'], 'black, oxblood-red and pale bone local colors remain on their three separately declared owners; the oxblood region stays readable within the darker field'),
  85: ('surface_material', ['color','material'], 'rust-colored and dirty-cream surface regions follow their existing bounded deposit pattern against a separate dark ground'),
  88: ('lighting', ['lighting','color'], 'a deep-red directional receiving footprint remains spatially separate from the cooler navy and violet light field'),
  91: ('surface_material', ['color','material'], 'pale celadon-green glaze follows the curved ceramic body with continuous highlight shading while a bounded darker motif remains on that same body'),
  92: ('surface_material', ['color','material'], 'bounded cobalt-blue motif regions remain on the same white glazed ceramic body; continuous ceramic shading connects the white body across the motif boundaries'),
}

# Full descriptions can deterministically activate. Names, brands, partial
# components and paraphrases are discovery only. Each opted-in profile promotes
# ALL components, evidence and native-pixel gates, never just the matching color.
PROFILE_SPECS = [
 ('neutral_cobalt_owner', [8], ['color'], [
  'one small cobalt-blue owner is bounded inside a larger off-white and graphite neutral field',
  'the cobalt color remains confined to that owner while the neutral field retains readable shading'], ['a global blue wash','a cobalt background dominating the frame']),
 ('bounded_metal_trim', [9,10,11,12,14,15,20,24], ['color','material'], [
  'the declared metallic trim has bounded colored reflections separate from the larger local-color field',
  'highlight variation follows the trim surface while neighboring matte regions retain their own color'], ['flat yellow paint substituted for reflective trim','colored light used as proof of metallic composition']),
 ('reflective_translucent_owners', [78], ['color','material'], [
  'localized reflected highlights belong to the declared metal owner',
  'visible light transmission belongs to a separate translucent owner',
  'the two material owners retain separate readable boundaries'], ['one opaque gray surface replaces both materials','a smooth pale surface alone proves translucency']),
 ('crossing_lines_same_carrier', [18], ['color','appearance','material'], [
  'distinct colored line families cross on one continuous declared carrier',
  'their unequal widths and spacing remain separately readable through the intersections'], ['solid colored blocks replace crossing lines','separate objects substitute for the same carrier pattern']),
 ('bands_same_carrier', [17,19], ['color','appearance','material'], [
  'the declared colored bands share the same continuous fabric or ribbon carrier',
  'band boundaries remain readable while each declared color stays confined to its assigned band'], ['different objects substitute for bands on one carrier','band colors spread over the whole carrier']),
 ('food_container_color_owners', [50], ['color'], [
  'the declared container surface retains its own bounded local color',
  'the beverage or food regions retain their separate ingredient colors inside that container',
  'the container color does not spread across the ingredient boundaries'], ['blue liquid substitutes for a blue cup','a uniformly recolored food surface replaces distinct ingredients']),
 ('primary_rectangles_orthogonal', [57], ['color','appearance'], [
  'black orthogonal lines divide unequal red blue and yellow rectangles on one light carrier',
  'all three primary-color regions and their shared line topology remain visible on that same carrier'], ['three separate primary-color objects','diagonal curves substitute for orthogonal line topology']),
 ('painted_emissive_owners', [76,77], ['lighting','color','material'], [
  'the declared painted region keeps a bounded nonemissive local color',
  'colored illumination originates on a separate declared luminous surface',
  'weaker spill follows receiving surface geometry rather than recoloring the whole frame'], ['painted green marks substitute for display emission','a global cyan wash obscures painted local color']),
 ('local_color_under_separate_lights', [66,70,73,88], ['lighting','color'], [
  'two differently colored directional light contributions form separate receiving footprints on the declared surfaces',
  'each light footprint follows surface orientation and occlusion while bounded base material regions remain distinguishable',
  'the colored illumination stays attributable to those footprints rather than a uniform image tint'], ['colored paint alone substitutes for received light','a global two-color grade substitutes for directional footprints']),
 ('ordered_background_gradient', [36,74,79], ['color'], [
  'the declared color stops connect in the stated positional order along one continuous background surface',
  'surface shading remains readable through the spatial color transition'], ['tonal mapping across unrelated screen positions','separate disconnected blocks substitute for the continuous gradient']),
 ('dark_oxblood_bone_owners', [81], ['color'], [
  'black oxblood-red and pale bone local colors retain three separately declared owners',
  'the oxblood region remains readable inside the darker field around the bounded pale detail'], ['gold added from an adjacent palette','dark red replaced by a global black wash']),
 ('celadon_glaze_same_body', [91], ['color','material'], [
  'pale green glaze follows the declared curved ceramic body with continuous highlight shading',
  'a bounded darker motif remains on that same ceramic body'], ['flat green paint substitutes for curved glazed shading','a separate dark object substitutes for the motif']),
 ('blue_motif_white_ceramic', [92], ['color','material'], [
  'bounded cobalt-blue motifs remain on the same white glazed ceramic body',
  'continuous ceramic shading connects the white body across the blue motif boundaries'], ['a separate blue object beside a white vessel','a blue-lit white vessel substitutes for bounded blue motifs']),
]

def effects(dimensions, mechanism='object_palette'):
    paths={
      'color':['surface.local_color','wardrobe.color','background.local_color'],
      'material':['surface.material','wardrobe.material','surface.reflectance','surface.transmission'],
      'appearance':['wardrobe.pattern','surface.pattern'],
      'lighting':['lighting.color','lighting.direction','surface.illumination'],
    }
    if mechanism in {'global_grade','selective_grade'}:
        paths['color']=['image.color_grading']
    elif mechanism=='spatial_gradient':
        paths['color']=['surface.local_color','surface.spatial_gradient','background.local_color','background.spatial_gradient']
    elif mechanism=='colored_lighting':
        paths['color']=['lighting.color','surface.illumination.color']
    elif mechanism in {'emissive_surface','mixed_surface_light'}:
        paths['color']=['surface.emission.color','surface.local_color','surface.illumination.color']
        paths['material']=['surface.emission','surface.reflectance']
    elif mechanism=='food_palette':
        paths['color']=['surface.local_color','container.surface.local_color','ingredients.local_color']
    return [{'dimension':d,'target':'*','property':p} for d in dimensions for p in paths[d]]

def build():
    cards = read(RESEARCH/'SEMANTIC-CARDS.json')['cards']
    drafts = {d['semantic_id']:d for d in read(RESEARCH/'CANDIDATE-DRAFTS.json')['drafts']}
    mappings = {m['semantic_id']:m for m in read(RESEARCH/'RUNTIME-MAPPING.json')['mappings']}
    data = pg.load_json(ASSETS/'photo_prompt_tags.json')
    slots, updates, profiles, bundles, adoption = {}, {}, [], [], []
    held = {68,89,90,93,94,95,96,97,98,99,100}
    for card in cards:
        sid=card['seed_id']; semantic_id=card['semantic_id']; mapping=mappings[semantic_id]
        row={'semantic_id':semantic_id,'label_ko':card['label_ko'], 'research_priority':mapping['priority'],
             'source_refs':card.get('source_refs',[]), 'new_profile_ids':[], 'binding_policy':'bind_generic_targets_to_actual_frozen_scene_owners_after_freeze; preserve the same canonical carrier property paths across dimensions'}
        if sid in held:
            row.update(decision='hold_specific_claim', reason='Specific film/cultural/function/data semantics require context evidence beyond a color list; adjacent visible generic relations remain available.', runtime_candidates=[])
        elif sid in APPLICATIONS:
            slot, dimensions, english=APPLICATIONS[sid]
            proposal=drafts[semantic_id]['entry_proposal']; cid=proposal['id'].replace('pal_','pal_app_',1)
            entry={'id':cid,'ko':card['label_ko']+'의 지정 영역 응용','en':english,
                   'weight':0.35,'tags':['palette_application',slot],
                   'aliases':[card['label_ko']],
                   'keywords':[card['label_ko'],english],
                   'concept_units':english.split('; '),
                   'relations':[{'id':'declared_palette_owners','type':'retains_bounded_colors_on','subject':'the declared existing color carriers','object':'their separately declared surface or light regions'}],
                   'affected_dimensions':dimensions,'affected_properties':effects(dimensions,card['mechanism']),
                   'embedding_text':english}
            if sid in {49,50,51}: entry['for_any']=['food','drink','still_life','object']; entry['tags'].append('food')
            slots.setdefault(slot,[]).append(entry)
            row.update(decision='new_narrow_application',runtime_candidates=[{'slot':slot,'id':cid,'source_file':'photo_prompt_palette_applications_extension.json','effects':effects(dimensions,card['mechanism'])}])
            if sid==81:row['rejected_adjacent_candidate']='obsidian_antique_gold_oxblood_palette (adds gold)'
        else:
            # Context is not a synonym, an equivalent palette, a query term or
            # an instruction. It helps a composer bind the existing broad relation.
            refs=mapping['existing_candidate_sources']
            accepted=[]
            for ref in refs:
                if ref['id'].startswith('cr_'):
                    slot=ref['slot'];cid=ref['id']
                    if not any(r['id']==cid for r in data['slots'].get(slot,[])): raise ValueError(cid)
                    context={'id':'palette_'+semantic_id.lower(),'definition':'A possible context for the existing relation, not a palette synonym.',
                             'observable_interpretation':card['visual_relation_en'],
                             'claim_limits':['Use only if these owners already fit the frozen scene. Palette colors, example objects, material and hierarchy are separate authorial choices. This context cannot impose them or establish cultural provenance.'],
                             'activation_authority':'interpretation_only_not_a_required_visual_recipe'}
                    updates.setdefault(slot,{}).setdefault(cid,{'contexts':[]})['contexts'].append(context)
                    accepted.append(ref)
            row.update(decision='compose_existing_relation_with_optional_context',runtime_candidates=accepted)
            if not accepted:raise ValueError('Unmapped palette '+semantic_id)
        adoption.append(row)

    for slug,seeds,dimensions,components,confounds in PROFILE_SPECS:
        pid='pa_'+slug; definition='; '.join(components)
        related=[c for c in cards if c['seed_id'] in seeds]
        mechanism={'local_color_under_separate_lights':'colored_lighting','painted_emissive_owners':'mixed_surface_light',
                   'ordered_background_gradient':'spatial_gradient','food_container_color_owners':'food_palette'}.get(slug,'object_palette')
        profile={'id':pid,'category':'owner_bound_palette_application',
                 'activation':{'exact_terms':[definition], 'requires_adult_character':False,'semantic_discovery_requires_component_evidence':False},
                 'semantics':{'definition':definition,
                              'paraphrase_examples':[c['visual_relation_en'] for c in related],
                              'contrast_examples':confounds, 'visual_components':components,
                              'claim_limits':['Palette and style names alone do not activate this relation.', 'Colors and owners follow the requester or an explicit compatible selection; no brand, chemical composition, historical authenticity, emotion, safety function or numerical mapping is established.', 'All components are mandatory only after legitimate exact activation or explicit post-core opt-in.']},
                 'concept_candidate':{'concept_terms':components+[c['label_ko'] for c in related], 'affected_dimensions':dimensions,'affected_properties':effects(dimensions,mechanism)},
                 'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
                 'reject_substitutes':confounds,
                 'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':[
                    {'id':'component_'+str(i),'match_terms':[phrase], 'evidence_field':'component_'+str(i)+'_phrase',
                     'evidence_terms':[phrase],'min_content_words':3,'instruction':'Make this selected owner relation visible: '+phrase,
                     'render_gate':{'id':'vo_'+pid+'_'+str(i),'review_scale':'both',
                                    'description':phrase+'. Inspect the assigned owners in saved native pixels and the whole frame; an absent, occluded, merged, reversed or unclear component fails.'}}
                    for i,phrase in enumerate(components,1)]}}
        profiles.append(profile)
        members=[r for r in adoption if int(r['semantic_id'][1:]) in seeds and r['decision']=='new_narrow_application']
        for row in members: row['new_profile_ids'].append(pid)
        # One self-contained candidate association at a time; approximate discovery
        # or palette-name exposure never activates this profile automatically.
        for row in members:
            ref=row['runtime_candidates'][0]
            bundles.append({'id':'palette_relation_'+ref['id'], 'primary_visual_proposition':definition,
                            'hard_profile_ids':[pid], 'component_groups':[{'id':'component_'+str(i),'visible_evidence':[phrase]} for i,phrase in enumerate(components,1)],
                            'candidate_ids':[ref['id']],'candidate_slots':{ref['id']:ref['slot']},'confusion_boundaries':confounds,
                            'source_keywords':[ref['id']], 'candidate_only':True,'activation_mode':'component_complete_exact_only'})

    extension={'schema_version':'photo-prompt-research-extension/v1','slots':slots,
               'existing_slot_context_extensions':updates,'visual_semantics':bundles}
    record={'contract_version':'photo-extension-maintenance/v1','record_id':'photo_prompt_palette_applications_extension-20261006',
            'source_filename':'photo_prompt_palette_applications_extension.json','authored_source_sha256':digest(extension),
            'runtime_keys':['slots','existing_slot_context_extensions','visual_semantics'],
            'maintenance_only':{'research_path':str(RESEARCH.relative_to(ROOT)),
               'source_ledger_sha256':hashlib.sha256((RESEARCH/'SOURCES.json').read_bytes()).hexdigest(),
               'adoption':adoption,
               'owner_policy':'Reusable targets use the supported wildcard, never fabricated research owner IDs. Explicit surface, wardrobe, background, ingredient, light and grade paths retain parent/cross-dimension lock checks. Adopted run evidence names actual frozen scene owners; a declaration is not an automatic semantic proof.',
               'hex_policy':'HEX values are research sRGB approximations and are not exact photographic pixel promises.',
               'held_claims':[row['semantic_id'] for row in adoption if row['decision']=='hold_specific_claim']},
            'adoption_scope':'Optional existing-owner applications; palette names are advisory; no pre-core, runtime code or generic profile edits.'}
    record_file=ROOT/'docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_palette_applications_extension-20261006.json'
    write(record_file,record)
    extension['maintenance_ref']={'contract_version':'photo-extension-maintenance-ref/v1','record_id':record['record_id'],'sha256':digest(record)}
    write(ASSETS/'photo_prompt_palette_applications_extension.json',extension)
    write(ASSETS/'photo_prompt_visual_obligations_palette_applications.json',{'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','description':'Narrow owner-bound palette applications. Names remain advisory; all selected components retain native-pixel gates.','profiles':profiles})
    manifest=read(ASSETS/'photo_prompt_source_manifest.json')
    for kind,name in [('candidate','photo_prompt_palette_applications_extension.json'),('visual_profile','photo_prompt_visual_obligations_palette_applications.json')]:
        if not any(r['file']==name for r in manifest['sources']):
            manifest['sources'].append({'file':name,'kind':kind,'required':True,'load_order':sum(r['kind']==kind for r in manifest['sources'])})
    write(ASSETS/'photo_prompt_source_manifest.json',manifest)
    counts={decision:sum(r['decision']==decision for r in adoption) for decision in sorted({r['decision'] for r in adoption})}
    report={'schema_version':'color-palette-adoption/v1','cards_reviewed':len(cards),'decisions':counts,
            'new_candidates':sum(len(rs) for rs in slots.values()),'new_profiles':len(profiles),
            'context_records':sum(len(v['contexts']) for rs in updates.values() for v in rs.values()),
            'existing_candidates_with_context':sum(len(rs) for rs in updates.values()),
            'compiled_native_gates':sum(len(p['authored_components']['components']) for p in profiles),
            'rows':adoption}
    write(EVIDENCE/'ADOPTION-MANIFEST.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='rows'},ensure_ascii=False,indent=2))

if __name__=='__main__': build()
