#!/usr/bin/env python3
"""Integrate separately reviewed semantic units; never route from case names.

The PSV files are explicit authoring input, not heuristic extraction from names,
publisher biographies, or image captions. Baseline copies make the procedure
repeatable without appending duplicate phrases or overwriting unrelated assets.
"""
from __future__ import annotations
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rows(name, width):
    result=[]
    for n, line in enumerate((HERE/name).read_text().splitlines(),1):
        if not line or line.startswith('#'): continue
        fields=line.split('|')
        assert len(fields)==width, (name,n,len(fields))
        result.append(fields)
    return result

def unique(values):
    result=[];seen=set()
    for value in values:
        key=value.casefold()
        if key not in seen:result.append(value);seen.add(key)
    return result

CARRIERS={
    'hair':['hair','hairstyle','wig','모발','머리','헤어','가발'],
    'eyewear':['glasses','spectacles','eyewear','안경','아이웨어'],
    'headwear':['hat','cap','headband','headwear','모자','캡','머리띠'],
    'garment':['garment','clothing','cloth','costume','armor','glove','옷','의상','의복','천','갑주','장갑'],
    'skin':['skin','body surface','face surface','피부','몸 표면','얼굴 표면'],
    'mask':['mask','face covering','wrap','mouth object','가면','얼굴 덮개','얼굴 천','입 앞'],
    'mouth':['mouth','teeth','dental','입','치아','치관','치열'],
    'cover':['cover','covering','덮개','몸 덮개'],
    'nonhuman':['nonhuman','creature','robot','machine','animal design','비인간','생물','로봇','기계','동물 디자인'],
}

def main():
    baseline=json.loads((HERE/'BASELINE-REGISTRY.json').read_text())
    original={p['id']:p for p in baseline['profiles']}
    source_payloads={};owner={}
    for path in (HERE/'input-snapshot').glob('photo_prompt_visual_obligations*.json'):
        payload=json.loads(path.read_text());source_payloads[path.name]=payload
        for p in payload.get('profiles',[]):owner[p['id']]=(path.name,p)
    receipt={'schema_version':'character-appearance-semantic-integration/v1',
             'source_case_count':100,'new_relations':[],'existing_owner_enrichments':[],
             'held_units':[], 'ordinary_candidate_change':'NONE',
             'proper_names_runtime_activation':False}
    changed=set()
    for pid, raw_en, raw_ko in rows('EXISTING-ALTERNATIVES.psv',3):
        before=original[pid];filename,p=owner[pid]
        en=raw_en.split(';');ko=raw_ko.split(';')
        groups=before['semantics']['component_semantics']['groups']
        assert len(en)==len(ko)==len(groups),(pid,len(en),len(groups))
        phrases=['; '.join(en),'; '.join(ko)]
        p['semantics']['paraphrase_examples']=unique(p['semantics'].get('paraphrase_examples',[])+phrases)
        candidate=p.setdefault('concept_candidate',{})
        candidate['concept_terms']=unique(candidate.get('concept_terms',[])+phrases)
        authored=p.get('authored_components')
        if authored:
            for comp, e, k in zip(authored['components'],en,ko):
                comp['match_terms']=unique(comp['match_terms']+[e,k])
                comp['evidence_terms']=unique(comp['evidence_terms']+[e,k])
            for field in ('composition_instruction','required_evidence_fields','evidence_requirements','render_gates'):
                p.pop(field,None)
            p['semantics'].pop('component_semantics',None)
        else:
            for group,e,k,field in zip(p['semantics']['component_semantics']['groups'],en,ko,p['required_evidence_fields']):
                group['any_terms']=unique(group['any_terms']+[e,k])
                requirement=p['evidence_requirements'][field]
                requirement['must_mention_any']=unique(requirement['must_mention_any']+[e,k])
        changed.add(filename)
        receipt['existing_owner_enrichments'].append({
            'profile_id':pid,'source_file':filename,'decision':'REUSE_EQUIVALENT',
            'new_full_paraphrases':phrases,'component_alternatives_en':en,'component_alternatives_ko':ko})

    registry={'schema_version':'photo-visual-obligation-registry-extension/v1',
              'relation_contract_version':'photo-visual-relation/v1','profiles':[]}
    new_units={}
    for pid,dim,prop,carrier,exact_en,exact_ko,raw,raw_en,raw_ko,rejects in rows('NEW-RELATIONS.psv',10):
        primary=raw.split(';');en=raw_en.split(';');ko=raw_ko.split(';');confusions=rejects.split(';')
        assert pid not in original and len(primary)==len(en)==len(ko),(pid,len(primary),len(en))
        phrases=unique(['; '.join(primary),'; '.join(en),'; '.join(ko)])
        components=[]
        for n,(p,e,k) in enumerate(zip(primary,en,ko),1):
            variants=unique([p,e,k])
            components.append({'id':f'component_{n}', 'match_terms':variants,
                'evidence_field':f'component_{n}_phrase','evidence_terms':variants,'min_content_words':3,
                'instruction':f'Keep the selected carrier and owner explicit: {p}.',
                'render_gate':{'id':f'vo_{pid}_{n}','review_scale':'native',
                   'description':f'{p}. Inspect the selected same owner in original pixels. Every component is required; partial evidence fails and hidden components are unobservable.'}})
        limits=['Preserve the declared subject, owner, medium, age, count and all dimension and property locks.',
                'Character names are research provenance and do not activate this relation.',
                'This profile describes a selected visible relation; color, material, function and narrative cause require independent selection.',
                'Every component is required on the same declared carrier; missing parts fail and hidden parts are unobservable.']
        if carrier=='nonhuman':
            limits+=['Use only an already declared nonhuman creature or machine design. Do not convert a referenced human into this carrier.',
                     'Hidden attachment roots do not prove biological origin, a costume fastener, a residual limb socket or a material type.']
        if carrier=='skin':
            limits+=['Visible surface marks do not establish injury history, disease, diagnosis or biological cause.']
        profile={'id':pid,'category':'selected_character_appearance_relation',
            'activation':{'exact_terms':[exact_en,exact_ko],'requires_adult_character':False,
                'semantic_discovery_requires_component_evidence':True,
                'hard_activation':{'contract_version':'photo-visual-hard-activation/v1',
                    'required_any_groups':[{'id':'declared_carrier','any_terms':CARRIERS[carrier]}]}},
            'semantics':{'definition':'; '.join(primary),'paraphrase_examples':phrases,
                'visual_components':primary,'contrast_examples':confusions,'claim_limits':limits},
            'concept_candidate':{'concept_terms':unique([exact_en,exact_ko]+phrases),
                'core_assertion_discovery':True,'affected_dimensions':[dim],
                'affected_properties':[{'dimension':dim,'target':'main_subject','property':prop}]},
            'runtime_expression':{'default_mode':'definition_with_optional_label',
                'prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
            'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':components},
            'reject_substitutes':confusions}
        registry['profiles'].append(profile);new_units[pid]=profile
        receipt['new_relations'].append({'profile_id':pid,'decision':'NEW_SELECTED_RELATION',
            'carrier':carrier,'components':primary,'effects':profile['concept_candidate']['affected_properties']})
    registry_filename='photo_prompt_visual_obligations_character_appearance.json'
    save(ASSETS/registry_filename,registry)
    for filename in sorted(changed):save(ASSETS/filename,source_payloads[filename])
    # Registration, not a character-name router or specialized scene branch.
    generator=SKILL/'scripts/prompt_generator.py'
    code=generator.read_text()
    if f'    "{registry_filename}",' not in code:
        anchor='    "photo_prompt_visual_obligations_subculture_appearance.json",\n'
        assert code.count(anchor)==1
        generator.write_text(code.replace(anchor,anchor+f'    "{registry_filename}",\n'))

    # Those two proposals reuse existing meaning or remain research-only.
    redirect={'ca_layered_skirt_hem':'y2kr_visible_layers'}
    held={'ca_fan_ribs':'The observed handheld fan is documented as a separate prop. No new automatic prop candidate is created without a current owner-scoped prop selection contract.'}
    receipt['held_units']=[{'unit_id':pid,'decision':'RESEARCH_ONLY','reason':reason} for pid,reason in held.items()]
    receipt['reuse_decisions']=[{'proposed_id':p,'profile_id':r,'reason':'Independent layer edges already belong to the existing multi-layer garment relation.'} for p,r in redirect.items()]
    observations=rows('OBSERVATIONS.psv',10)
    sources={r['id']:r for r in json.loads((HERE/'SOURCE-RECEIPTS.json').read_text())['rows']}
    cases=[]
    reviews=json.loads((HERE/'SOURCE-REVIEW-OVERRIDES.json').read_text())
    reviewed_links=[]
    for fields in observations:
        cid,*_=fields;src=sources[cid]
        existing=[p for p in fields[8].split(',') if p]
        # A machine's intrinsic luminous panel is not a costume-panel owner.
        existing=[p for p in existing if not(cid=='C056' and p=='costume_ccx_cc35_01')]
        added=[p for p in fields[9].split(',') if p]
        existing+= [redirect[p] for p in added if p in redirect]
        added=[p for p in added if p not in redirect and p not in held]
        existing=unique(existing);assert all(p in original for p in existing),(cid,existing)
        assert all(p in new_units for p in added),(cid,added)
        assert existing or added,cid
        case={k:src[k] for k in ('id','group','name_ko','name_en','version_scope','source_url','source_page_title','source_page_sha256','artwork_url','artwork_label','artwork_sha256','artwork_dimensions')}
        case.update({'evidence_state':'PUBLISHER_PIXELS_OBSERVED',
            'observation_scope':'This exact artwork snapshot. Cropped or hidden regions are not reconstructed from biography or other costumes.',
            'decomposed_elements':[
                {'id':'upper_form','region':'head_or_hair','observation_ko':fields[1]},
                {'id':'face_surface','region':'face_or_surface','observation_ko':fields[2]},
                {'id':'clothing_body','region':'clothing_or_body','observation_ko':fields[3]},
                {'id':'appendages_details','region':'appendages_or_details','observation_ko':fields[4]},
                {'id':'separate_owners','region':'props_or_companions','observation_ko':fields[5]},
            ],'observable_relations_ko':fields[6].split(';'),
            'unobservable_and_confusions_ko':fields[7].split(';'),
            'existing_profile_ids':existing,'new_profile_ids':added,
            'runtime_links':[{'profile_id':p,'decision':'EXISTING_PARAPHRASE_ENRICHMENT' if p in original else 'NEW_SELECTED_RELATION',
                             'source_relation_status':'VISIBLE_RELATION_CANDIDATE_REQUIRES_ALL_COMPONENT_REVIEW',
                             'scope':'Same selected feature owner only; source observation is not proof of generated-image compliance.'} for p in existing+added],
            'held_observations':[p for p in fields[9].split(',') if p in held],
            'named_character_routing':False})
        for link in case['runtime_links']:
            key=cid+':'+link['profile_id']
            partial=reviews['partial'].get(key)
            link['source_relation_status']='PARTIAL_UNOBSERVABLE_IS_NOT_PASS' if partial else 'VISIBLE_COMPONENTS_OBSERVED'
            link['source_review_note_ko']=partial or '선택한 보이는 요소의 외곽·연결·소유 관계를 해당 정의와 대조했다. 가려진 뿌리나 원인은 이 판정에 포함하지 않는다.'
            link.update(reviews['owners'].get(key,{'source_owner':src['name_ko'],'owner_role':'primary_character'}))
            link['runtime_target_rule']='Apply only after this feature owner is independently selected as main_subject; do not transfer companion features to the primary character.'
            if cid in reviews['carrier_notes']:link['carrier_note_ko']=reviews['carrier_notes'][cid]
            reviewed_links.append({'case_id':cid,**link})
        assert any(x['source_relation_status']=='VISIBLE_COMPONENTS_OBSERVED' for x in case['runtime_links']),cid
        cases.append(case)
    assert len(cases)==len(set(c['id'] for c in cases))==100
    assert len(set((c['group'],c['name_en']) for c in cases))==100
    used={p for c in cases for p in c['new_profile_ids']}
    assert used==set(new_units),('unreferenced',set(new_units)-used)
    for row in receipt['new_relations']+receipt['existing_owner_enrichments']:
        row['case_ids']=[c['id'] for c in cases if row['profile_id'] in c['existing_profile_ids']+c['new_profile_ids']]
        assert row['case_ids'],row['profile_id']
    receipt['counts']={'new_profiles':len(registry['profiles']),
        'enriched_existing_profiles':len(receipt['existing_owner_enrichments']),
        'new_components':sum(len(p['authored_components']['components']) for p in registry['profiles']),
        'new_profile_full_alternatives':sum(len(p['semantics']['paraphrase_examples']) for p in registry['profiles']),
        'existing_full_alternatives_added':sum(len(x['new_full_paraphrases']) for x in receipt['existing_owner_enrichments']),
        'case_count':len(cases),'profile_links':sum(len(c['runtime_links']) for c in cases),
        'source_observed_links':sum(x['source_relation_status']=='VISIBLE_COMPONENTS_OBSERVED' for x in reviewed_links),
        'source_partial_links':sum(x['source_relation_status']=='PARTIAL_UNOBSERVABLE_IS_NOT_PASS' for x in reviewed_links)}
    # Each new relation needs at least one source whose required components are
    # actually visible. Partial source evidence never becomes a passing case.
    assert set(new_units)<={x['profile_id'] for x in reviewed_links if x['source_relation_status']=='VISIBLE_COMPONENTS_OBSERVED'}
    save(HERE/'SOURCE-RELATION-REVIEW.json',{'schema_version':'character-appearance-source-relation-review/v1',
        'qualification_scope':'acquired publisher source pixels; not generated-image qualification',
        'links':reviewed_links})
    save(HERE/'CHARACTER-CASEBOOK.json',{'schema_version':'research-character-appearance-casebook/v2','cases':cases})
    save(HERE/'INTEGRATION-MAINTENANCE.json',receipt)
    print(json.dumps(receipt['counts'],ensure_ascii=False))

if __name__=='__main__':main()
