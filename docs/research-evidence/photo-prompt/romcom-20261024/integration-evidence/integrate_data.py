"""Register scoped romcom options; preserve every existing candidate and binding."""
from pathlib import Path
import copy, hashlib, json, sys, uuid

O=Path(__file__).resolve().parent;Q=O.parent;R=O.parents[4];S=R/'skills/photo-prompt-image-generator';A=S/'assets'
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as corpus

def read(p):return json.loads(p.read_bytes())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
NS=uuid.UUID('b0efc34e-4f2d-5896-9d3b-74e37785d428')
def ident(prefix,text):return prefix+uuid.uuid5(NS,text).hex

CONTRACT=('One optional complete authored visual realization. Preserve the whole bilingual proposition, its stated counts, each owner and contact endpoint, support, gap, garment layer, object connection, gaze direction and depicted-medium boundary together. '
 'Use only within independently frozen requester meaning, established owner/object prerequisites and permitted whole effects. A romcom genre, route, citation or research graph creates no person, event, age, consent or permission. '
 'All distinguishing components and connections must be observable together; partial evidence is not full compliance. Still pixels do not establish romantic feeling, personality, history, intention, accident, prior object use, consent, coercion, identity, kinship, profession, relationship agreement, temporal order, sound, an ending, or fiber composition. '
 'Research metadata and index exposure are not native semantic qualification or requester acceptance.')

def main():
    assert not (O/'data-integration.json').exists(),'Do not overwrite an existing integration.'
    before=corpus.load(A);manifest=read(A/corpus.MANIFEST_NAME);manifest_sha=sha(A/corpus.MANIFEST_NAME)
    research=read(Q/'semantic-cards.json');routes=read(Q/'keyword-routes.json');sources=read(Q/'sources.json');source_by_id={s['id']:s for s in sources}
    fresh={};bindings={};registry=[];decisions=[]
    existing_pairs={}
    for cid,rec in before['candidates'].items():existing_pairs.setdefault((rec['content'].get('en'),rec['content'].get('ko')),[]).append(cid)
    comparisons=read(Q/'existing-source-decisions.json')
    for card in research['visual_cards']+research['context_cards']:
        visual=card['mode']=='optional_visual_realization';key=card['id'];meta=copy.deepcopy(card)
        meta.update(registration_status='authored_optional_source' if visual else 'context_diagnostic',native_approval=False,native_qualification='not_qualified',automatic_hard_activation=False,source_details=[source_by_id[s] for s in card['source_ids']])
        cid=ident('cand_','romcom:'+key);assert cid not in before['candidates']
        if visual:
            en=card['positive_en'];ko=card['positive_ko'];pair=(en,ko)
            assert not existing_pairs.get(pair),'Exact bilingual duplicate requires a reuse decision'
            content={'en':en,'ko':ko,'definition':'Complete optional authored visual realization: '+en,'aliases':[card['label_ko']],'application_contract':CONTRACT,'research_semantics':meta}
            # Conservative complete-source effect envelope. Role qualification is separate.
            dimensions=['subject','count','appearance','pose','body_geometry','action','composition','setting']
            if key.startswith(('E','F','S','C')):dimensions+=['expression','camera','lighting']
            if key.startswith('M'):dimensions+=['style','format','color']
            if key=='S09':dimensions+=['text']
            conditions={'for_any':['human']}
            if key.startswith('M'):conditions['requires_any_tags']=['illustration','comic','manga']
        else:
            content={'definition':'Context-only diagnostic, excluded from positive visual retrieval: '+card['distinction_ko']+' Required additional evidence: '+card['required_evidence'],'research_semantics':meta}
            dimensions=[];conditions={}
        record={'id':cid,'record_kind':'visual_option' if visual else 'diagnostic','content':content,'conditions':conditions,'effects':{'dimensions':sorted(set(dimensions)),'properties':[]},'provenance':[{'source':str((Q/'semantic-cards.json').relative_to(R))+'#'+key,'sha256':sha(Q/'semantic-cards.json')}]}
        fresh[cid]=record
        if visual:
            for slot in card['suggested_slots']:
                assert slot in before['slot_catalog']
                bid=ident('bind_',cid+':'+slot)
                bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':before['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':1.0}
        meta['candidate_id']=cid;meta['actual_slot_suggestions']=card.get('suggested_slots',[]) if visual else []
        registry.append(meta)
        neighbours=[d for d in comparisons if d['card_id']==key and d.get('candidate_id')]
        decisions.append({'card_id':key,'candidate_id':cid,'decision':'new_complete_scoped_alternative' if visual else 'diagnostic','related_existing_candidate_ids':[d['candidate_id'] for d in neighbours],'reason':'Preserve every exact authored qualifier as a separate optional proposition; related existing alternatives remain byte-exact and are not declared equivalent.' if visual else 'Nonvisual distinction retained outside positive visual retrieval.','effects_review':record['effects'],'native_approval':False})
    mapping={c['id']:c['candidate_id'] for c in registry}
    for route in routes['terms']:
        route['candidate_ids']=[mapping[x] for x in route['visual_card_ids']]
        route['context_candidate_id']=mapping[route['context_card_id']]
        route.update(discovery_only=True,automatic_hard_activation=False,route_semantics='Optional/adjacent research realization, not an exact synonym, native source proof or genre recipe.')
    candidate_name='photo_candidate_romcom_20261024.json';binding_name='photo_candidate_romcom_bindings_20261024.json';semantic_name='photo_romcom_semantics_20261024.json'
    for filename in (candidate_name,binding_name,semantic_name):assert not (A/filename).exists()
    assert sha(A/corpus.MANIFEST_NAME)==manifest_sha,'Concurrent manifest update requires rebaseline'
    write(A/candidate_name,{'schema':corpus.MODULE_SCHEMAS['candidates'],'candidates':fresh})
    write(A/binding_name,{'schema':corpus.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings})
    manifest['modules'] += [{'file':candidate_name,'kind':'candidates'},{'file':binding_name,'kind':'slot_bindings'}]
    write(A/corpus.MANIFEST_NAME,manifest)
    write(A/semantic_name,{'schema':'photo-romcom-visual-semantics/v1','cards':registry,'keyword_routes':routes['terms'],'scene_examples':routes['scene_examples'],'sources':sources,'native_approval':False,'automatic_hard_activation':False,'research_sha256':sha(Q/'semantic-cards.json'),'scope':'317 original reference terms; 99 optional authored visual propositions, 19 context diagnostics. Specific independent lexical corroboration covers 41 terms, not all definitions.'})
    after=corpus.load(A)
    assert all(after['candidates'][cid]==r for cid,r in before['candidates'].items())
    assert all(after['slot_bindings'][bid]==b for bid,b in before['slot_bindings'].items())
    assert all(after[k]==before[k] for k in ('slot_catalog','policies'))
    write(O/'new-native-records.json',fresh);write(O/'changed-native-records.json',{});write(O/'adoption-review.json',decisions)
    summary={'status':'source_registered','visual_sources':len(research['visual_cards']),'context_diagnostics':len(research['context_cards']),'new_bindings':len(bindings),'keyword_routes':len(routes['terms']),'before_CIDs':len(before['candidates']),'after_CIDs':len(after['candidates']),'all_existing_candidates_bindings_catalog_policies_preserved':True,'native_approval':False,'index_status':'NOT_RUN','allowed_source_files':[candidate_name,binding_name,semantic_name,corpus.MANIFEST_NAME]}
    write(O/'data-integration.json',summary);print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
