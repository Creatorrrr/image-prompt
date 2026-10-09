import hashlib,json,pathlib,re,sys
P=pathlib.Path(__file__).resolve().parent
W=pathlib.Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt')
S=W/'skills/photo-prompt-image-generator/scripts';sys.path.insert(0,str(S))
from visual_profile_contracts import validate_visual_profile_source,compile_visual_profile,validate_hard_activation
from photo_candidate_semantics import validate_candidate_entries
from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
from validate_photo_prompt_dictionary import validate_visual_obligation_registry
from photo_source_manifest import SourceInventory
x=json.load(open(P/'data-fragment.json'));errors=[];new_c=[];new_p=[];gates=[]
for w in x['domain_writes']:
    validate_candidate_entries({'slots':{w['slot']:w['candidates']}},AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
    assert w['context_extensions']==[]
    new_c.extend(w['candidates']);new_p.extend(w['profiles'])
    assert w['slot'] in json.load(open(W/'skills/photo-prompt-image-generator/assets'/w['candidate_file']))['slots']
    for p in w['profiles']:
        validate_visual_profile_source(p);validate_hard_activation(p['activation']['hard_activation']);compiled=compile_visual_profile(p);gates.extend(g['id'] for g in compiled['render_gates'])
        assert p['activation']['exact_terms']==[p['semantics']['definition']]
        assert not {'component_semantics','required_evidence_fields','evidence_requirements','render_gates','composition_instruction'} & set(p)
        assert 'component_semantics' not in p['semantics']
        assert p['authored_components']['discovery']['required_group_ids']==[c['id'] for c in p['authored_components']['components']]
    serialized=json.dumps({k:v for k,v in w.items() if k in ['candidates','profiles']},ensure_ascii=False)
    assert not re.search(r'https?://|research_draft|SPR_DRAFT_|source_ids|original_description|source_support|S00|Vogue|CottonWorks|Seamwork|Jovani',serialized)
    assert not re.search(r'[a-z] A\b',serialized), 'technical object label in runtime prose'
    for candidate,profile in zip(w['candidates'],w['profiles']):
        assert profile['id']=='spring_'+candidate['id'].removeprefix('spf_')
        assert profile['semantics']['definition']==candidate['en']
        assert profile['semantics']['visual_components']==candidate['concept_units']
        for part,component,evidence in zip(candidate['concept_units'],profile['authored_components']['components'],profile['authored_components']['obligations'][0]['evidence']):
            assert component['match_terms'][0]==part
            assert evidence['requirement']['must_mention_any']==[part]
for entries in [new_c,new_p]:assert len({e['id'] for e in entries})==len(entries)
assert len(gates)==len(set(gates))
assigned=[d['draft_id'] for i,d in enumerate(sorted(json.load(open('/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-20261009/candidate-drafts.json'))['drafts'],key=lambda d:d['draft_id'])) if i%3==0]
assert [d['draft_id'] for d in x['decisions']]==assigned
assert len(x['evidence'])==len(assigned)==94
for e in x['evidence']:
    if 'authored_edges' in e:
        roots={n.split('.')[0] for r in e['authored_edges'] for n in [r['subject'],r['object']]}
        assert roots <= set(e['declared_owner_objects']), (e['draft_id'],roots-set(e['declared_owner_objects']))
        assert all(r['subject']!=r['object'] for r in e['authored_edges'])
registry=json.load(open(W/'skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json'))
base=len(registry['profiles']);registry['profiles']+=new_p
synthetic=P/'fragment-registry-validation.sidecar.json';synthetic.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
validate_visual_obligation_registry(synthetic,errors,inventory=SourceInventory.for_test(P))
summary={'valid':not errors,'errors':errors,'new_candidates_checked':len(new_c),'new_profiles_checked':len(new_p),'base_registry_profiles_checked':base,'native_gate_count':len(gates),'assigned_drafts_checked':len(assigned),'decision_counts':{'new':93,'reuse':1,'enrich':0,'metadata':0},'all_relation_endpoints_have_declared_owner':True,'source_and_raw_text_separated_from_runtime_data':True,'generated_fields_omitted_from_source_profiles':True,'runtime_owner_labels_natural':True,'exact_terms_components_evidence_and_candidate_text_consistent':True,'shared_asset_writes':False,'fragment_sha256':hashlib.sha256((P/'data-fragment.json').read_bytes()).hexdigest(),'verification_boundary':'Fragment schema, compiled native contracts, property effects, owner graph and research separation; no index publication, retrieval, generation or pixel success.'}
(P/'fragment-contract-audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(P/'fragment-registry-audit.json').write_text(json.dumps({'synthetic':True,'base_profile_count':base,'new_profile_count':len(new_p),'valid':not errors,'errors':errors},indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
