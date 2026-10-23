"""Research integrity validation, not source qualification or image quality."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[3]
def read(name):
    return json.loads((ROOT/name).read_text())
errors=[]
checks={}
def check(name, condition):
    checks[name]=bool(condition)
    if not condition: errors.append(name)

tables=read('conversation-tables.json')
atlas=read('keyword-atlas.json')
cards=read('semantic-cards.json')
contexts=read('context-distinctions.json')
sources=read('sources.json')
cases=read('evaluation-cases.json')
queries=read('evaluation-queries.json')
gaps=read('remaining-research.json')
slots=json.loads((PROJECT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
check('table_and_row_counts',len(tables)==24 and len(atlas)==393)
expected=[(t['table'],i,row) for t in tables for i,row in enumerate(t['rows'][1:],1)]
check('all_original_cells_and_order',[(x['table_index'],x['row_index'],x['source_cells']) for x in atlas]==expected)
for name,items in [('atlas',atlas),('cards',cards),('contexts',contexts),('sources',sources),('cases',cases),('queries',queries)]:
    check(name+'_unique_ids',len({x['id'] for x in items})==len(items))
cids={x['id'] for x in cards};sids={x['id'] for x in sources};ctxids={x['id'] for x in contexts}
check('expected_card_context_source_counts',len(cards)==104 and len(contexts)==52 and len(sources)==40)
check('keyword_card_links',all(set(x['component_card_ids'])<=cids for x in atlas))
check('keyword_context_links',all(set(x['section_context_ids'])<=ctxids for x in atlas))
check('source_links',all(set(x['source_ids'])<=sids for x in atlas+cards+contexts))
check('bilingual_visual_propositions',all(x['positive_ko'].strip() and len(x['positive_en'].split())>=12 for x in cards))
check('explicit_graphs_and_checks',all(x['owner_nodes'] and len(x['relations'])>=1 and len(x['observable_gates'])>=3 for x in cards))
check('graph_endpoint_owners',all(all(r['from'] in x['owner_nodes'] and r['to'] in x['owner_nodes'] for r in x['relations']) for x in cards))
check('existing_slot_names_only',all(set(x['suggested_slots'])<=slots.keys() for x in cards))
check('no_runtime_or_native_approval',all(x['runtime_importable'] is False and x['native_approval'] is False for x in atlas+cards+contexts))
check('all_deferred_terms_retained', {x['id'] for x in atlas if x['mode']=='defer_specific_visual'}=={x['keyword_id'] for x in gaps})
check('evaluation_card_links',all(set(x['target_research_cards'])<=cids for x in cases+queries))
check('evaluation_counts',len(cases)==24 and len(queries)==256)
check('no_false_holdout_or_execution',all(x['holdout'] is False for x in cases+queries) and all(x['execution_status']=='not_run' for x in cases))
check('source_access_scope_present',all(x['url'].startswith('https://') and x['access'] and x['limitations_ko'] for x in sources))
missing_links=[]
for f in ROOT.glob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',f.read_text()):
        if '://' in link or link.startswith('#'): continue
        target=(f.parent/link.split('#',1)[0])
        # These files are emitted after the validation stage.
        if target.name in ['validation.json','provenance.json']: continue
        if not target.exists(): missing_links.append({'file':f.name,'target':link})
check('local_markdown_targets_exist',not missing_links)
report={'status':'pass' if not errors else 'fail','checks':checks,'errors':errors,'missing_links':missing_links,
        'limits':['Checks structure, literal preservation and internal links only.',
                  'Does not establish source factual completeness, native approval, retrieval quality, saved-pixel quality or user acceptance.'],
        'image_calls':0,'retrieval_calls':0,'embedding_calls':0,'runtime_source_writes':0}
(ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
