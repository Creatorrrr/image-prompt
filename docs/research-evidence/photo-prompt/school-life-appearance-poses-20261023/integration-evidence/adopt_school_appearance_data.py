"""Register reviewed complete school-life alternatives; preserve existing payloads."""
import copy,csv,hashlib,json,pathlib,sys,uuid
ROOT=pathlib.Path('/Users/chasoik/Projects/image-prompt')
S=ROOT/'skills/photo-prompt-image-generator';A=S/'assets';O=pathlib.Path(__file__).resolve().parent;Q=O.parent
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as c
from photo_runtime_sources import source_update

def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

APP=('One complete optional authored school-life realization. Retain the complete English and Korean '
     'propositions, stated owners, object and person counts, garment layers, physical supports, directed '
     'connections and depicted-media boundaries together. Apply only within independently frozen requester '
     'meaning and allowed changes. Research graphs and citations are review metadata, not native facts, '
     'owner selections, qualification or effect permission. Student roles and school clothing do not establish '
     'age, identity, nationality, consent, personality, popularity, academic ability, repetition, causation, '
     'diagnosis, sound or temporal history. Selected distinguishing components and both relation endpoints '
     'must be observable together; partial or hidden required evidence cannot pass the full relation.')

def footprint(key):
    sec=next((r['section'] for r in read(Q/'semantic-cards.json')['cards'] if r['id']==key),0)
    dims={'appearance','composition','material','count'}
    if sec in [1,2,3,5,6,9,15]:dims.update({'style','subject','role'})
    if sec in [7,8]:dims.update({'subject','style'})
    if sec in [9,10,11,12,13,14]:dims.update({'subject','pose','action','relationship','role','setting'})
    if sec==16:dims.update({'subject','pose','relationship','setting'})
    if sec==4 or key in ['V02','V03','V04','T05','T06','T08','I03','I04','I05']:dims.add('color')
    if key in ['H14','E03']:dims.update({'format','style'})
    return sorted(dims)

def main():
    assert not (O/'source-preservation.json').exists(),'Completed source registration already recorded'
    old=c.load(A);original_manifest=read(A/c.MANIFEST_NAME)
    old_hash={m['file']:sha(A/m['file']) for m in original_manifest['modules']}
    write(O/'working-source-before.json',{'corpus_sha256':c.digest(old),'candidates':len(old['candidates']),
        'bindings':len(old['slot_bindings']),'modules':old_hash,'manifest_sha256':sha(A/c.MANIFEST_NAME)})
    cards=read(Q/'semantic-cards.json')['cards'];routes=read(Q/'keyword-routes.json')['routes'];sources={r['id']:r for r in read(Q/'sources.json')['sources']}
    drafts={r['card_id']:r for r in read(Q/'candidate-drafts.json')['drafts']}
    context={r['id']:r for r in read(Q/'contexts-development.json')['rows']}
    candidates={};bindings={};registry=[];lookup={}
    for card in cards:
        key=card['id'];positive=key in drafts
        cid='cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/school-life-appearance-poses/20261023/'+key).hex
        assert cid not in old['candidates'];lookup[key]=cid
        if positive:
            en=drafts[key]['prompt_fragment_en'];ko=drafts[key]['prompt_fragment_ko']
            assert en==card['positive_en'] and ko==card['positive_ko']
        else:
            en=context[key]['query_en'];ko=card['name_ko']+'。'+card['handling']
        meta={**copy.deepcopy(card),'schema':'photo-school-life-visual-semantics/v1','card_id':key,
              'candidate_id':cid,'registration_status':'authored_optional_source' if positive else 'context_diagnostic',
              'runtime_importable':True,'native_approval':False,'native_qualification':'not_qualified',
              'source_details':[sources[s] for s in card['source_ids']],
              'provenance_boundary':'Research-file SHA, not remote webpage content hash. Scene geometry is authored proposal.',
              'graph_scope':'Review metadata only. No typed native facts, owner choices, guards or effect permissions.',
              'bilingual_review':'Complete English and Korean propositions reviewed with same owners and endpoints; no substitution from short label.'}
        registry.append(meta)
        candidates[cid]={'id':cid,'record_kind':'visual_option' if positive else 'diagnostic',
            'content':{'en':en,'ko':ko,'definition':('Complete optional school-life visual realization: '+en) if positive else 'Nonvisual school-life distinction; excluded from positive material retrieval.',
                       'aliases':[card['name_ko']],
                       'application_contract':APP if positive else 'Context and proof limits only; no automatic still-image recipe or native authority.',
                       'research_semantics':meta},
            'conditions':{},'effects':{'dimensions':footprint(key) if positive else [],'properties':[]},
            'provenance':[{'source':sources[s]['url'],'sha256':sha(Q/'visual-authored.tsv') if positive else sha(Q/'contexts-authored.tsv')} for s in card['source_ids']]}
        if positive:
            for slot in card['suggested_slots']:
                assert slot in old['slot_catalog'];bid='bind_'+uuid.uuid5(uuid.NAMESPACE_URL,cid+'/'+slot).hex
                bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional',
                    'semantic_role':old['slot_catalog'][slot]['semantic_role'],
                    'conditions':{'subject_applicability':{}},'weight':1.0}
    assert len(candidates)==168 and sum(r['record_kind']=='visual_option' for r in candidates.values())==140
    proposed=copy.deepcopy(old);proposed['candidates'].update(candidates);proposed['slot_bindings'].update(bindings);c.validate(proposed)
    cm='photo_candidate_school_appearance_poses_20261023.json';bm='photo_candidate_school_appearance_poses_bindings_20261023.json'
    result={'schema':'photo-school-life-semantic-registry/v1','cards':registry,
        'keyword_routes':[{**r,'candidate_ids':[lookup[k] for k in r['optional_visual_card_ids']+r['context_card_ids']]} for r in routes],
        'existing_source_triage':read(Q/'existing-source-triage.json'),
        'counts':{'cards':len(cards),'keyword_routes':len(routes),'visual_options':140,'context_diagnostics':28,'bindings':len(bindings)},
        'native_approval':False,'pixel_qualification':'NOT_RUN','research_source_sha256':{p.name:sha(p) for p in Q.iterdir() if p.is_file()}}
    with source_update(S):
        current=c.load(A)
        if c.digest(current)!=c.digest(old):
            write(O/'source-rebase.json',{'prior_sha256':c.digest(old),'latest_sha256':c.digest(current),'reason':'Concurrent source additions preserved under source_update lock'})
        old=current
        manifest=read(A/c.MANIFEST_NAME)
        old_hash={m['file']:sha(A/m['file']) for m in manifest['modules']}
        assert not any(m['file'] in {cm,bm} for m in manifest['modules'])
        assert set(candidates).isdisjoint(old['candidates']) and set(bindings).isdisjoint(old['slot_bindings'])
        assert all(b['semantic_role']==old['slot_catalog'][b['slot_id']]['semantic_role'] for b in bindings.values())
        proposed=copy.deepcopy(old);proposed['candidates'].update(candidates);proposed['slot_bindings'].update(bindings);c.validate(proposed)
        write(O/'working-source-before-locked.json',{'corpus_sha256':c.digest(old),'candidates':len(old['candidates']),'bindings':len(old['slot_bindings']),'modules':old_hash,'manifest_sha256':sha(A/c.MANIFEST_NAME)})
        write(A/cm,{'schema':c.MODULE_SCHEMAS['candidates'],'candidates':candidates})
        write(A/bm,{'schema':c.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings})
        manifest['modules'] += [{'file':cm,'kind':'candidates'},{'file':bm,'kind':'slot_bindings'}]
        write(A/c.MANIFEST_NAME,manifest);write(A/'photo_school_appearance_poses_semantics_20261023.json',result)
        actual=c.load(A);assert actual==proposed
    assert all(actual['candidates'][k]==v for k,v in old['candidates'].items())
    assert all(actual['slot_bindings'][k]==v for k,v in old['slot_bindings'].items())
    assert all(actual[k]==old[k] for k in ['slot_catalog','policies'])
    preservation={'status':'pass','old_candidates_preserved':len(old['candidates']),
        'old_bindings_preserved':len(old['slot_bindings']),'old_module_bytes_preserved':all(sha(A/k)==h for k,h in old_hash.items()),
        'total_candidates':len(actual['candidates']),'total_bindings':len(actual['slot_bindings']),**result['counts']}
    write(O/'data-integration.json',result);write(O/'new-native-records.json',candidates);write(O/'changed-native-records.json',{})
    write(O/'source-preservation.json',preservation);print(json.dumps(preservation,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
