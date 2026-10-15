"""Partial research consumer validation in a full corpus; never native adoption.

No publication or production write API is used. The full-production adoption
gate remains 18,250/pending0. Only already accepted exact proofs are attached.
"""
from __future__ import annotations
import argparse, copy, gzip, hashlib, importlib, json, os, shutil, sys, time
from pathlib import Path

OUT = Path(__file__).resolve().parent
R = OUT.parent
ROOT = R.parents[3]
G = Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.path[:0] = [str(G/'scripts'), str(G/'precore'), str(R)]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
import photo_global_index as documents
import direct_review as dr
# direct_review has a historical working-tree path insertion. Consumer modules
# must resolve from the exact frozen generation, even while other work proceeds.
sys.path[:0] = [str(G/'scripts'), str(G/'precore')]
import native_reviews as reviews

def save(name,value):
    path=OUT/name
    if path.exists():
        if path.read_bytes()==c.canonical_bytes(value)+b'\n':return
        raise ValueError('preserve previous evidence: '+str(path))
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(c.canonical_bytes(value)+b'\n')

def source():
    inventory=c.decode((R/'ROOT-CURRENT149-APPROVAL-INVENTORY-01.json').read_bytes())
    current=reviews.artifact(ROOT,inventory['current_source'])
    assert len(current['candidates'])==18250 and len(current['slot_catalog'])==149
    assert c.digest(current)=='39ab970ec8a42550f6afb41163ae6e2e76c1403f60f76cb9e5a962e3197dd65c'
    assert c.digest(current['slot_catalog'])==inventory['catalog_sha256']=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
    selected={v['candidate_id']:v for v in inventory['records']}
    assert len(selected)==77
    accepted={};history=[]
    for entry in inventory['accepted_history']:
        for key in ('assignment','batch','acceptance'): reviews.artifact(ROOT,entry[key])
        batch_path=ROOT/entry['batch']['file'];note=batch_path.parent/'NOTE.json'
        checked=reviews.verify_batch(entry['assignment']['file'],entry['batch']['file'],str(note),root=ROOT,here=R)
        reviews.verify_acceptance(ROOT,entry['acceptance'],checked)
        history.append({k:checked[k] for k in ('assignment_sha256','batch_sha256','note_sha256','statuses')})
        for cid,row in checked['records'].items():
            if cid not in selected or selected[cid]['batch']!=entry['batch']: continue
            assert row['status']=='approved' and c.digest(row['proof'])==selected[cid]['proof_sha256']
            assert reviews.exact(row['source_after'],current['candidates'][cid])
            hashes=native.referenced_records(current['candidates'][cid],current)
            refs={k:current['candidates'][k] for k in hashes if c.ID.fullmatch(k)}
            bindings={k:current['slot_bindings'][k] for k in hashes if c.BINDING_ID.fullmatch(k)}
            assert set(row['dependency_records'])==set(refs)
            assert reviews.exact(row['reference_bindings'],bindings)
            for child,dep in row['dependency_records'].items():
                plain=copy.deepcopy(dep);plain['content'].pop('role_evidence',None)
                assert reviews.exact(plain,refs[child])
            accepted[cid]=row
    assert set(accepted)==set(selected)
    proposed=copy.deepcopy(current)
    for cid,row in accepted.items(): proposed['candidates'][cid]['content']['role_evidence']=copy.deepcopy(row['proof'])
    for cid,row in accepted.items():
        for child,dep in row['dependency_records'].items():
            assert child in accepted and reviews.exact(dep['content']['role_evidence'],accepted[child]['proof'])
        native.validate(proposed['candidates'][cid],proposed['slot_catalog'],corpus=proposed)
    c.validate(proposed)
    assert proposed['slot_bindings']==current['slot_bindings'] and proposed['policies']==current['policies']
    assert set(proposed['candidates'])==set(current['candidates'])
    tags=[]
    by_pair={(b['candidate_id'],b['slot_id']):b for b in current['slot_bindings'].values()}
    for cid,row in sorted(accepted.items()):
        for tag,role in sorted(row['proof']['roles'].items()):
            tags.append({'candidate_id':cid,'slot_id':tag,'semantic_role':current['slot_catalog'][tag]['semantic_role'],
                'scope':role['scope'],'realization_ids':role['realization_ids'],'proof_sha256':c.digest(row['proof']),
                'existing_binding':by_pair.get((cid,tag)),'persistent_binding_added':False})
    return current,proposed,accepted,tags,history

def prepare():
    before,after,accepted,tags,history=source()
    save('APPROVED-ROLE-RELATIONS.json',tags)
    compressed=gzip.compress(c.canonical_bytes(after),mtime=0)
    target=OUT/'PARTIAL-RESEARCH-CORPUS.json.gz'
    with target.open('xb') as stream:stream.write(compressed)
    save('SOURCE-VERIFICATION.json',dict(schema='photo-full-context-partial-native-validation/v1',
        source_sha256=c.digest(before),research_container_sha256=c.digest(after),candidate_count=18250,catalog_count=149,
        approved_proof_count=len(accepted),role_relations=len(tags),full_source_approval_count=77,
        records_without_current_equal_root_approval=18173,persistent_bindings_preserved=len(after['slot_bindings']),
        persistent_bindings_added=0,policies_preserved=True,unapproved_records_unchanged=True,
        exact_accepted_batches=history,full_corpus_structure_validated=True,
        operating_changes=0,operating_native_qualified_count=0,production_adoption_gate_bypassed=False,
        runtime_activated=False,stage05_complete=False,stage06_complete=False,semantic_accuracy_certified=False,
        frozen_generation=str(G),gemini_calls=0))
    print(json.dumps({'accepted':len(accepted),'relations':len(tags),'full_candidate_count':len(after['candidates'])}),flush=True)

def local_installation():
    """Frozen inference code, separately pinned existing installation address.

    Generations deliberately do not include the 1GB installed model package.
    No new installation, download or alternate model/space is permitted.
    """
    import photo_local_embedding as local
    installation=ROOT/'skills/photo-prompt-image-generator'
    assert (G/'embedding-runtime.lock.json').read_bytes()==(installation/'embedding-runtime.lock.json').read_bytes()
    original_lock=local.runtime_lock
    worker=installation/'scripts/photo_local_embedding.py'
    assert worker.read_bytes()==(G/'scripts/photo_local_embedding.py').read_bytes()
    local.ROOT=installation
    # The installed child starts from the same exact pinned code bytes, with
    # its package beside the lock. No model package exists inside generations.
    local.__file__=str(worker)
    local.runtime_lock=lambda root=installation,verify=True:original_lock(root,verify=verify)
    local.space=lambda root=installation:dict(local.runtime_lock(root)['space'])
    original_binding=local.installed_binding
    local.installed_binding=lambda root=installation:original_binding(root)
    import photo_embedding_provider as provider
    space=provider.default_space()
    assert space['provider']=='embeddinggemma2-local' and space['dimensions']==768
    return provider,space

def build():
    import build_shared_candidate_index as builder
    import photo_search_layout as layout
    from photo_search_reader import SearchReader
    provider,space=local_installation()
    proposed=c.decode(gzip.decompress((OUT/'PARTIAL-RESEARCH-CORPUS.json.gz').read_bytes()))
    source_report=c.decode((OUT/'SOURCE-VERIFICATION.json').read_bytes())
    assert c.digest(proposed)==source_report['research_container_sha256']
    old=SearchReader(G/'assets');assert old.manifest['space']==space
    positive={cid for cid,r in proposed['candidates'].items() if r['record_kind'] in documents.POSITIVE_KINDS}
    changed=[]
    for cid in sorted(positive):
        recipe,text=documents.text(proposed['candidates'][cid]);previous=old.meta['vector_recipes'].get(cid)
        if previous is None or previous['recipe']!=recipe or previous['text_sha256']!=hashlib.sha256(text.encode()).hexdigest():changed.append(cid)
    save('BUILD-PREFLIGHT.json',{'positive_documents':len(positive),'changed_document_ids':changed,
        'changed_document_count':len(changed),'expected_exact_vector_reuse':len(positive)-len(changed),
        'source_sha256':c.digest(proposed),'space':space,'generation':str(G),
        'operating_source_writes':0,'production_publication_calls':0,'gemini_allowed':False,
        'new_downloads_allowed':False,'network_denied_by_os':True})
    vectors=builder.offline_vector_map(old,proposed);old.close()
    entries=vectors['entries'];assert set(entries)==positive-set(changed)
    executions=[]
    for offset in range(0,len(changed),16):
        batch=changed[offset:offset+16];projected=[documents.text(proposed['candidates'][cid]) for cid in batch]
        rows=provider.embed_many([x[1] for x in projected],[{'candidate_id':cid,'recipe':x[0]} for cid,x in zip(batch,projected,strict=True)],OUT/'local-document-cache',space=space,kind='document')
        for cid,(recipe,text),row in zip(batch,projected,rows,strict=True):
            provider.validate_execution(row['execution'],space,text,row['vector'],'document')
            entries[cid]={'id':cid,'recipe':recipe,'text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),
                'vector':row['vector'],'embedding_execution':row['execution']}
            executions.append({'candidate_id':cid,'cache_hit':row['cache_hit'],'execution':row['execution'],'vector_sha256':row['vector_sha256']})
        print(json.dumps({'local_documents_complete':len(executions),'total_changed':len(changed)}),flush=True)
    save('DOCUMENT-EXECUTIONS.json',executions)
    documents.validate(vectors,proposed)
    assets=OUT/'assets';assets.mkdir(exist_ok=False)
    modules=[]
    for field in ('candidates','slot_catalog','slot_bindings','policies'):
        name=field+'.json';(assets/name).write_bytes(c.canonical_bytes({'schema':c.MODULE_SCHEMAS[field],field:proposed[field]}))
        modules.append({'file':name,'kind':field})
    (assets/c.MANIFEST_NAME).write_bytes(c.canonical_bytes({'schema':c.MANIFEST_SCHEMA,'modules':modules}))
    staged=layout.build(assets,proposed,vectors,activate=True)
    verified=layout.verify(assets,proposed,staged,vectors)
    save('BUILD-VERIFICATION.json',{'research_layout_id':staged['layout_id'],'source_sha256':c.digest(proposed),
        'positive_documents':len(positive),'vector_reuse':len(positive)-len(changed),
        'local_document_inputs':sum(not r['cache_hit'] for r in executions),'local_document_cache_hits':sum(r['cache_hit'] for r in executions),
        'changed_document_count':len(changed),'verification':verified,'gemini_calls':0,
        'production_runtime_published':False,'production_pointer_changed':False,
        'full_corpus_semantic_review_complete':False,'partial_native_proof_count':77})
    print(json.dumps({'layout':staged['layout_id'],'changed_documents':len(changed),'reused':len(positive)-len(changed)}),flush=True)

def composition(pack):
    """The complete archived blue-cup baseline is read and kept verbatim.

    The cup, kitchen counter, window light and glaze are consistent as prose.
    No articulated body appears. All optional additions remain declined.
    """
    core=pack['authorial_core'];lock=core['intent_lock'];prompt=core['baseline_prompt_en']
    review=copy.deepcopy(pack['embodiment_preflight']['baseline_review'])
    review.update(provenance='agent_postcomposition',prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest())
    result={'pack_id':pack['pack_id'],'composer':'agent','prompt_en':prompt,'negative_en':pack['negative_en'],
        'chosen_candidate_ids':[],'chosen_visual_concept_ids':[],'candidate_interpretations':[],
        'global_retrieval_sha256':pack['global_retrieval']['canonical_sha256'],
        'embodiment_review':{'source_contract_sha256':pack['embodiment_preflight']['canonical_sha256'],'review':review},
        'authorial_core_binding':{'source_authorial_core_sha256':core['canonical_sha256'],
            'source_intent_lock_sha256':lock['canonical_sha256'],
            'preserved_anchor_ids':[r['anchor_id'] for r in lock['semantic_anchors']],
            'preserved_evidence':[],'authorial_decisions':[]},
        'semantic_clarification_decisions':[{'clarification_id':r['id'],
            'decision':'applied' if r.get('required_in_final_prompt') else 'rejected',
            'rationale':'Preserve the frozen cup scene and decline optional interpretation.',
            'prompt_evidence':lock['semantic_anchors'][0]['prompt_evidence']} for r in pack.get('semantic_clarification',{}).get('candidates',[])],
        'creative_augmentation_brief':{'decisions':[{'candidate_id':r['id'],'decision':'rejected',
            'rationale':'Keep the frozen baseline visual hierarchy.'} for r in pack.get('creative_augmentation',{}).get('candidates',[])]}}
    obligations=pack.get('semantic_assertion_obligations') or {}
    if obligations.get('enabled'):
        result['semantic_assertion_evidence']={'source_contract_sha256':obligations['canonical_sha256'],
            'evidence':{r['assertion_id']:copy.deepcopy(r['frozen_evidence']) for r in obligations['obligations']}}
    return result

def consume():
    provider,space=local_installation()
    import prompt_generator as g
    import photo_runtime_sources as runtime
    import photo_slot_queries as queries
    import audit_composed_prompt as audit
    for directory in ('scripts','precore'):
        target=OUT/directory
        if target.exists():
            for path in (G/directory).glob('*'):
                if path.is_file(): assert (target/path.name).read_bytes()==path.read_bytes()
        else:shutil.copytree(G/directory,target,ignore=shutil.ignore_patterns('__pycache__'))
    for name in ('embedding-default.json','embedding-runtime.lock.json','requirements-local-embeddings.txt'):
        shutil.copyfile(G/name,OUT/name)
    research_scope={'mode':'local_research_only','partial_native_proofs':77,'whole_source_count':18250,
        'catalog_count':149,'production_qualified_count':0,'production_adoption_gate':'18250/pending0 unchanged',
        'persistent_binding_additions':0,'semantic_accuracy_certified':False}
    store=OUT/'research-runtime-store'
    runtime_provider=runtime.RuntimeSnapshotProvider(OUT,store)
    prior=OUT/'RESEARCH-GENERATION-MANIFEST.json'
    published=(c.decode(prior.read_bytes())['publication'] if prior.exists()
        else runtime_provider.publisher.publish(observation=research_scope))
    snapshot=runtime_provider.acquire()
    assert published['generation_id']==snapshot.generation_id
    from dataclasses import replace
    snapshot=replace(snapshot,observation=runtime.freeze(research_scope))
    save('RESEARCH-GENERATION-MANIFEST.json',{'schema':'photo-partial-research-generation-wrapper/v1',
        'research_scope':research_scope,'publication':published,
        'standard_generation_manifest_file':str(snapshot.root/'manifest.json'),
        'standard_generation_manifest_sha256':hashlib.sha256((snapshot.root/'manifest.json').read_bytes()).hexdigest()})
    fixture=ROOT/'docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs/dev-02-blue-cup-en'
    controls=c.decode((fixture/'creative-controls.json').read_bytes())
    core=g.load_authorial_core_arg(fixture/'authorial-core.json',request_envelope=g.load_request_envelope_arg(fixture/'request-envelope.json'),creative_control_snapshot=controls)
    embodiment=c.decode((fixture/'embodiment-review.json').read_bytes())
    import photo_global_retrieval as intrinsic
    import photo_role_proposals as roles
    relations=c.decode((OUT/'APPROVED-ROLE-RELATIONS.json').read_bytes())
    request_data=snapshot.data.for_core(core)
    allowed,source_roles,_=intrinsic.eligible(request_data,core,controls)
    relation_checks=[]
    for relation in relations:
        cid,tag=relation['candidate_id'],relation['slot_id']
        p=roles.propose(request_data,tag,cid,source_roles.get(cid,[]),realization_ids=relation['realization_ids'])
        assert p['native_qualification']=='qualified' and p['semantic_role']==relation['semantic_role']
        assert not p['persistent_tag_write'] and p['scope']=='request'
        relation_checks.append({'candidate_id':cid,'slot_id':tag,'proposal':p,
            'request_intrinsic_eligible':cid in allowed,'source_guards_execution_required_for_adoption':True})
    plain=c.decode(gzip.decompress((OUT/'PARTIAL-RESEARCH-CORPUS.json.gz').read_bytes()))
    original_inventory=c.decode((R/'ROOT-CURRENT149-APPROVAL-INVENTORY-01.json').read_bytes())
    before=reviews.artifact(ROOT,original_inventory['current_source'])
    assert documents.documents(plain)==documents.documents(before)
    assert len(snapshot.data.reader.meta['positive_ids'])==len(set(snapshot.data.reader.meta['positive_ids']))==18198
    assert len(snapshot.data.reader.meta['record_sha256'])==18250
    save('REQUEST-ROLE-VERIFICATION.json',{'approved_role_relation_checks':relation_checks,
        'relation_count':len(relation_checks),'same_positive_documents_before_after_native_metadata':True,
        'one_positive_document_per_cid':True,'positive_documents':18198,'all_source_ids_preserved':18250,
        'persistent_binding_additions':0,'tag_rank_votes_added':0,
        'boundary':'Per-proof roles pass the existing request-local proposal constructor. A proposal alone grants no intrinsic admission, owner choice, effect permission, final adoption or semantic accuracy.'})
    slots=sorted(snapshot.data['slot_catalog'])
    assert len(slots)==149
    existing_context=OUT/'QUERY-CONTEXT.json'
    context=(c.decode(existing_context.read_bytes()) if existing_context.exists()
        else queries.prepare(core,controls,snapshot.data['slot_catalog'],slots,OUT/'local-query-cache',space=space))
    queries.validate_set(context,core,controls,snapshot.data['slot_catalog'],slots,space=space)
    save('QUERY-CONTEXT.json',context)
    print(json.dumps({'query_vectors':len(context['slots']),'local_queries_ready':True}),flush=True)
    pack=g.generate_candidate_pack(snapshot.data,core,controls,embodiment,query_context=context,requested_slots=slots)
    save('CANDIDATE-PACK.json',pack)
    receipt=runtime_provider.receipt(snapshot,pack);save('ISSUED-RECEIPT.json',receipt)
    replayed=runtime_provider.from_receipt(pack,receipt)
    assert replayed.generation_id==snapshot.generation_id
    composed=composition(pack);save('COMPOSED.json',composed)
    report=audit.audit_composed_prompt(pack,composed,runtime_receipt=receipt,runtime_store=store)
    save('COMPOSE-AUDIT.json',report)
    modules={}
    for name,module in sorted(sys.modules.items()):
        path=getattr(module,'__file__',None)
        if path and (name.startswith('photo_') or name in {'prompt_generator','audit_composed_prompt','bm25f_retrieval'}):
            path=Path(path).resolve()
            assert path.is_relative_to(G) or name=='photo_local_embedding'
            modules[name]={'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    accepted={r['candidate_id'] for r in c.decode((OUT/'APPROVED-ROLE-RELATIONS.json').read_bytes())}
    retrieved=pack['global_retrieval'];chosen=set(retrieved['selected_candidate_ids'])
    save('CONSUMER-VERIFICATION.json',{'schema':'photo-full-context-partial-native-consumers/v1',
        'research_scope':research_scope,'generation_id':snapshot.generation_id,
        'requested_slots':len(slots),'executed_slot_searches':len(retrieved['slot_searches']),
        'whole_positive_pool_eligible_count':retrieved['eligible_candidates'],
        'all_slots_search_whole_shared_positive_corpus':all(r['search_scope']=='whole_shared_positive_corpus' and not r['tag_admission_filter'] for r in retrieved['slot_searches'].values()),
        'reader_io_metrics_after_pack_receipt_replay_and_compose':dict(snapshot.data.reader.metrics),
        'whole_pool_positive_document_count':len(snapshot.data.reader.meta['positive_ids']),
        'global_record_count':len(snapshot.data.reader.meta['record_sha256']),
        'public_unique_candidates':len(chosen),'public_approved77_candidates':sorted(chosen&accepted),
        'issued_receipt_replayed':True,'compose_status':report['status'],'compose_failures':report['failures'],
        'composed_optional_adoptions':0,'semantic_precision_measured':False,'render_or_pixels_verified':False,
        'local_query_inputs':sum(not r['cache_hit'] for r in context['slots'].values()),
        'local_query_cache_hits':sum(r['cache_hit'] for r in context['slots'].values()),
        'production_runtime_writes':0,'production_native_qualified_count':0,'gemini_calls':0,
        'consumer_module_pins':modules})
    assert report['status']=='pass',report
    print(json.dumps({'issued_receipt_replayed':True,'compose':report['status'],'searches':len(retrieved['slot_searches'])}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','build','consume']);a=p.parse_args()
    {'prepare':prepare,'build':build,'consume':consume}[a.action]()
