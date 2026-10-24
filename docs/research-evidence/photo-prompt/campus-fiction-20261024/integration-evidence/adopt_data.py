"""Adopt complete reviewed campus realizations; preserve all pre-existing records."""
import copy, gc, hashlib, json, pathlib, subprocess, sys, uuid
gc.disable()
ROOT=pathlib.Path('/Users/chasoik/Projects/image-prompt')
S=ROOT/'skills/photo-prompt-image-generator';A=S/'assets';O=pathlib.Path(__file__).resolve().parent;Q=O.parent
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as c
from photo_runtime_sources import source_update
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
CM='photo_candidate_campus_life_20261024.json';BM='photo_candidate_campus_life_bindings_20261024.json';SM='photo_campus_life_semantics_20261024.json'
APP=('One complete optional authored campus-life realization. Preserve the complete English/Korean propositions, '
     'stated owners and counts, garment layers, support paths, directed connections, contact versus air gaps, '
     'and depicted-media boundaries together. Apply only within independently frozen requester meaning and '
     'open dimensions. Research graphs/citations are review metadata, not native facts, permission or source '
     'qualification. Campus, clothes, props and poses do not establish identity, enrollment, age, consent, '
     'relationship history, power, contribution, crime, diagnosis, cause, sound or temporal history. '
     'Both endpoints and every adopted distinguishing component must be observable. Hidden required evidence '
     'is UNOBSERVABLE_NOT_PASS; partial contract success is partial_is_fail.')
def footprint(card):
    # Conservative complete-source footprint, never a slot-derived permission waiver.
    key=card['id'];dims={'composition'}
    if key.startswith('S'):dims|={'setting','count','relationship'}
    if key.startswith('W'):dims|={'appearance','material','style','count','relationship','subject'}
    if key.startswith('P'):dims|={'appearance','count','relationship','subject'}
    if key.startswith('A'):dims|={'subject','action','pose','count','relationship','setting'}
    if key.startswith('F'):dims|={'framing','setting'}
    if key in {'S02','S03','S04','S05','S07','S10','S13','S14'}:dims|={'subject','action','pose'}
    if key in {'W02','W25','P01','P03','P07','S13','A04','A13','A14','A15','A16','A17','A18','A19','A20','F04','F06'}:dims.add('text')
    if key in {'W01','W02','W10','W15','W16','W25','P03','P09','A42'}:dims.add('color')
    if key=='P07':dims|={'format','framing'}
    if key in {'A09','A10','A11','A12','A20','A21','A22','A23','A24','A25','A26','A27','A28','A29','A30','A31','A32','A33','A34','A35','A36','A37','A38','A39','A40','A41','A42'}:dims.add('appearance')
    if key in {'F01','F02','F03','F05'}:dims|={'subject','count','pose','relationship'}
    if key in {'F04','F06'}:dims|={'lighting','subject','count','appearance'}
    return sorted(dims)
def main():
    assert not (O/'source-preservation.json').exists(),'Registration already completed; do not overwrite evidence'
    cards=read(Q/'semantic-cards.json')['cards'];routes=read(Q/'keyword-routes.json')['routes'];sources={s['id']:s for s in read(Q/'sources.json')}
    research_sha=sha(Q/'cards-authored.psv');new={};bindings={};lookup={};registry=[]
    reuse={'A25':'cand_e88cd98b3bce5a3f938e3043f720708e'}
    with source_update(S):
        old=c.load(A);manifest=read(A/c.MANIFEST_NAME);old_hash={m['file']:sha(A/m['file']) for m in manifest['modules']}
        write(O/'working-source-before.json',{'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'corpus_sha256':c.digest(old),'candidates':len(old['candidates']),'bindings':len(old['slot_bindings']),'modules':old_hash,'manifest_sha256':sha(A/c.MANIFEST_NAME),'skill_sha256':sha(S/'SKILL.md')})
        assert not any(m['file'] in {CM,BM} for m in manifest['modules'])
        for card in cards:
            key=card['id'];positive=card['mode'] in {'observable','staged_proxy'}
            cid=reuse.get(key,'cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/campus-life/20261024/'+key).hex);lookup[key]=cid
            meta={**copy.deepcopy(card),'schema':'photo-campus-life-visual-semantics/v1','card_id':key,'candidate_id':cid,'registration_status':'reused_existing_complete_hand_geometry' if key in reuse else ('authored_optional_source' if positive else 'context_diagnostic'),'native_approval':False,'native_qualification':'not_qualified','source_details':[sources[s] for s in card['source_ids']],'provenance_boundary':'Research-authored file SHA, not remote-page-byte SHA. Specimen geometry is an authored proposal, not a documented occurrence. Related terms are not synonyms.','graph_scope':'Research owner graph is review metadata only; no typed native permission or guard inferred.'}
            # Keep original research runtime_importable=False; this field refers to the draft only.
            meta['native_registration_present']=True;registry.append(meta)
            if key in reuse:
                original=old['candidates'][cid]
                assert 'alternating fingers' in original['content']['en'] and 'thumbs and wrists' in original['content']['en']
                # Adult eligibility remains requester/core context; original source is byte-for-byte retained.
            else:
                en=card['positive_en'] if positive else card['context_en'];ko=card['positive_ko'] if positive else card['context_ko']
                new[cid]={'id':cid,'record_kind':'visual_option' if positive else 'diagnostic','content':{'en':en,'ko':ko,'definition':('Complete optional campus-life visual realization: '+en) if positive else 'Nonvisual campus distinction; excluded from positive image material retrieval. '+en,'aliases':card['related_terms'],'application_contract':APP if positive else 'Context and proof limits only. No positive still-image prescription or native authority.','research_semantics':meta},'conditions':{},'effects':{'dimensions':footprint(card) if positive else [],'properties':[]},'provenance':[{'source':str((Q/'semantic-cards.json').relative_to(ROOT))+'#'+key,'sha256':research_sha}]}
            if positive:
                existing_slots={b['slot_id'] for b in old['slot_bindings'].values() if b['candidate_id']==cid}
                for slot in card['suggested_slots']:
                    assert slot in old['slot_catalog']
                    if slot in existing_slots:continue
                    bid='bind_'+uuid.uuid5(uuid.NAMESPACE_URL,cid+'/'+slot).hex
                    bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':old['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':1.0}
        assert len(new)==123 and sum(v['record_kind']=='visual_option' for v in new.values())==100
        assert set(new).isdisjoint(old['candidates']) and set(bindings).isdisjoint(old['slot_bindings'])
        proposed=copy.deepcopy(old);proposed['candidates'].update(new);proposed['slot_bindings'].update(bindings);c.validate(proposed)
        write(A/CM,{'schema':c.MODULE_SCHEMAS['candidates'],'candidates':new});write(A/BM,{'schema':c.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings})
        manifest['modules'] += [{'file':CM,'kind':'candidates'},{'file':BM,'kind':'slot_bindings'}];write(A/c.MANIFEST_NAME,manifest)
        result={'schema':'photo-campus-life-semantic-registry/v1','cards':registry,'keyword_routes':[{**r,'candidate_ids':list(dict.fromkeys(lookup[k] for k in r['card_ids']))} for r in routes],'existing_source_triage':read(Q/'existing-source-triage.json'),'counts':{'cards':len(cards),'keyword_routes':len(routes),'new_visual_options':100,'new_context_diagnostics':23,'reused_existing_candidates':1,'new_bindings':len(bindings)},'native_approval':False,'pixel_qualification':'NOT_RUN','research_source_sha256':{p.name:sha(p) for p in Q.iterdir() if p.is_file()}}
        write(A/SM,result);actual=c.load(A);assert actual==proposed
        assert all(actual['candidates'][k]==v for k,v in old['candidates'].items())
        assert all(actual['slot_bindings'][k]==v for k,v in old['slot_bindings'].items())
        assert all(actual[k]==old[k] for k in ['slot_catalog','policies'])
        assert all(sha(A/k)==h for k,h in old_hash.items())
    write(O/'data-integration.json',result);write(O/'new-native-records.json',new);write(O/'changed-native-records.json',{});write(O/'card-candidate-map.json',lookup)
    report={'status':'pass','old_candidates_preserved':len(old['candidates']),'old_bindings_preserved':len(old['slot_bindings']),'old_module_bytes_preserved':True,'new_CIDs':len(new),'new_visual_options':100,'new_diagnostics':23,'reused_CIDs':reuse,'new_bindings':len(bindings),'total_CIDs':len(actual['candidates']),'total_bindings':len(actual['slot_bindings']),'research_graph_is_native_qualification':False}
    write(O/'source-preservation.json',report);print(json.dumps(report,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
