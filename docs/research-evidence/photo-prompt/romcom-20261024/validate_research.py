"""Check cross-file integrity and source-snapshot drift; never qualifies runtime."""
import collections
import hashlib
import json
import pathlib

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'

def read(name):
    return json.loads((HERE/name).read_text())

def main():
    source=read('reference-browser.json')
    semantics=read('semantic-cards.json')
    cards=semantics['visual_cards']
    contexts=semantics['context_cards']
    routes=read('keyword-routes.json')['terms']
    drafts=read('candidate-drafts.json')['drafts']
    sources=read('sources.json')
    boundaries=read('boundary-cases.json')
    development=read('development-cases.json')
    card_ids={c['id'] for c in cards}
    context_ids={c['id'] for c in contexts}
    source_ids={s['id'] for s in sources}
    assert len(card_ids)==len(cards) and len(context_ids)==len(contexts)
    expected={f'T{t:02d}-R{r:02d}':cells for t,table in enumerate(source['content']['tables'][:22],1) for r,cells in enumerate(table[1:],1)}
    assert len(routes)==len(expected)==317
    assert {k['id'] for k in routes}==set(expected)
    for k in routes:
        assert [k['original_label'],k['original_definition']]==expected[k['id']]
        assert k['context_card_id'] in context_ids
        assert set(k['visual_card_ids']) <= card_ids
        assert set(k['lexical_source_ids']) <= source_ids
        assert k['runtime_hard_activation'] is False
    assert len(read('keyword-routes.json')['scene_examples'])==7
    slots=set(json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_bytes())['slot_catalog'])
    for c in cards:
        assert c['positive_en'].strip() and c['positive_ko'].strip()
        assert set(c['term_refs']) <= set(expected)
        assert set(c['suggested_slots']) <= slots, c['id']
        assert set(c['source_ids']) <= source_ids
        assert c['observable_gate'] and c['confusion_boundary']
        assert c['native_approval'] is False and c['automatic_hard_activation'] is False
        assert c['pixel_status']=='NOT_RUN' and c['runtime_registration']=='NOT_APPLIED'
        nodes={e[k] for e in c['research_relations'] for k in ('from','to')}
        assert nodes==set(c['owner_nodes']) and len(nodes)>1
    for c in contexts:
        assert c['positive_en'] is None and c['runtime_visual_binding'] is False
        assert c['native_approval'] is False
        assert set(c['optional_card_ids']) <= card_ids
        assert set(c['source_ids']) <= source_ids
    assert len(drafts)==len(cards)
    assert {d['semantic_card_id'] for d in drafts}==card_ids
    for d in drafts:
        assert d['native_approval'] is False and d['indexed'] is False and d['bindings_created'] is False
        assert d['status']=='research_draft_not_native_source'
    for b in boundaries:
        assert set(b['card_ids']) <= card_ids
        assert b['status']=='DESIGNED_NOT_EXECUTED'
    assert len(development)==len(cards)*2+len(boundaries)*2
    assert all(x['evaluation_status']=='NOT_RUN' for x in development)
    # Sensitive reference sections are complete, not just the first 20k characters.
    assert [sum(k['table']==t for k in routes) for t in (19,20,21)]==[15,19,14]
    snapshot=read('corpus-snapshot.json')
    changed=[]
    for mod in snapshot['modules']:
        p=ASSETS/mod['file']
        current=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
        if current!=mod['sha256']:
            changed.append(mod['file'])
    manifest=hashlib.sha256((ASSETS/'photo_candidate_corpus_manifest.json').read_bytes()).hexdigest()
    if manifest != snapshot['manifest_sha256']:
        changed.append('photo_candidate_corpus_manifest.json')
    for rel,original in snapshot['script_sha256'].items():
        p=ROOT/rel
        current=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
        if current!=original:
            changed.append(rel)
    result=dict(schema='romcom-research-validation/v1',research_structure='PASS',counts=read('BUILD-SUMMARY.json'),source_snapshot_comparison='UNCHANGED' if not changed else 'DRIFT_REQUIRES_REBASELINE_BEFORE_INTEGRATION',changed_protected_sources=changed,protected_scope='105 manifest modules, manifest and four named maintenance scripts; not a whole-workspace concurrent-change attribution.',claim_limit='Cross-file consistency and hash comparison only. No natural-language truth, native qualification, retrieval, image or acceptance proof.',semantic_review='Sequential author self-review; no independent reviewer or holdout.',runtime_integration='NOT_APPLIED',retrieval='NOT_RUN',image_generation='NOT_RUN')
    (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    main()
