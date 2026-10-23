"""Research integrity and preservation checks. No native approval or API calls."""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]

def pairs(rows):
    result={}
    for key,value in rows:
        assert key not in result, f'duplicate JSON key {key}'
        result[key]=value
    return result

def read(name):
    return json.loads((HERE/name).read_text(),object_pairs_hook=pairs)

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None

def main():
    checks={};all_json={p.name:read(p.name) for p in HERE.glob('*.json')}
    checks['duplicate_json_keys']='PASS'
    cards=read('semantic-cards.json')['cards'];drafts=read('candidate-drafts.json')['drafts']
    sources=read('sources.json')['sources'];routes=read('keyword-routes.json')['routes']
    summary=read('PACKAGE-SUMMARY.json');baseline=read('BASELINE.json')
    ids={c['id'] for c in cards};source_ids={s['id'] for s in sources}
    assert len(ids)==len(cards)==113
    assert len(source_ids)==len(sources)==44
    assert len({d['draft_id'] for d in drafts})==len(drafts)==79
    assert Counter(c['evidence_mode'] for c in cards)==Counter({'still':29,'proxy':50,'context':34})
    checks['counts_and_unique_ids']='PASS'
    catalog=json.loads((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    for card in cards:
        assert card['source_ids'] and set(card['source_ids'])<=source_ids
        assert set(card['proposed_current_slots'])<=set(catalog)
        assert not card['native_approval'] and not card['automatic_hard_activation']
        assert card['claim_limit_ko'] and card['confusion_boundaries'] and card['review_before_adoption']
        owners={o['id'] for o in card['owners']}
        assert len(owners)==len(card['owners'])
        for rel in card['relations']:
            assert rel['subject'] in owners and rel['object'] in owners and rel['subject']!=rel['object']
            assert rel['predicate']
        if card['evidence_mode']=='context':
            assert not card['phrase_en'] and not card['phrase_ko'] and not card['owners'] and not card['relations'] and not card['gates']
        else:
            assert card['phrase_en'] and card['phrase_ko'] and owners and card['relations'] and card['gates']
            assert len(card['gates'])==len(card['owners'])+len(card['relations'])
        for gate in card['gates']:
            assert gate['pixel_status']=='NOT_RUN' and gate['partial_is_fail']
            assert gate['unobservable_status']=='UNOBSERVABLE_NOT_PASS'
            if gate['kind']=='relation':assert gate['both_endpoints_required'] and gate['owner_continuity_required']
    checks['cards_graph_endpoints_context_separation_and_pixel_limits']='PASS'
    card_map={c['id']:c for c in cards}
    assert {d['card_id'] for d in drafts}=={c['id'] for c in cards if c['evidence_mode']!='context'}
    for d in drafts:
        assert not d['native_approval'] and not d['runtime_importable']
        assert 'candidate_id' not in d and 'realization_id' not in d
        assert d['positive_en']==card_map[d['card_id']]['phrase_en']
        assert d['positive_ko']==card_map[d['card_id']]['phrase_ko']
        for b in d['proposed_bindings']:assert b['source_semantic_role']==catalog[b['slot_id']]['semantic_role'] and b['status']=='role_fit_review_required'
    checks['drafts_are_research_only_and_current_slot_roles']='PASS'
    assert len(routes)==217 and [r['id'] for r in routes]==[f'K{i:03d}' for i in range(1,218)]
    assert Counter(r['row_kind'] for r in routes)==Counter({'term':191,'authored_worldbuilding':10,'work_reference':9,'authored_combination':7})
    for row in routes:
        assert row['source_label'] and row['source_definition_excerpt'] and row['route_card_ids']
        assert set(row['route_card_ids'])<=ids
    browser=read('reference-browser-access.json')
    assert browser['recovered_table_rows']==len(routes) and browser['complete_visible_table_coverage']
    assert {str(s):n for s,n in Counter(r['section'] for r in routes).items()}==browser['rows_by_section']
    for c in cards:assert c['reference_keyword_ids']==[r['id'] for r in routes if c['id'] in r['route_card_ids']]
    checks['complete_chrome_217_table_row_coverage_and_reference_links']='PASS'
    # Semantic boundaries intentionally reviewed rather than inferred from a universal token route.
    route_map={r['source_label'].split(' — ',1)[0]:r['route_card_ids'] for r in routes}
    assert route_map['Construct']==['G87']
    assert route_map['Dress Reform']==['G01','G25']
    assert 'G91' in route_map['Fetishism'] and 'G92' in route_map['Sadomasochistic Motifs / BDSM']
    assert 'G96' in route_map['Resurrectionist / Body-snatcher']
    checks['reviewed_critical_route_boundaries']='PASS'
    for s in sources:assert s['url'].startswith('https://') and s['access'] and s['locator'] and s['supported_scope_and_limit_ko']
    checks['source_provenance_and_access_limits']='PASS'
    snapshots=read('existing-source-mapping.json')['records'];audit=read('CORPUS-LEXICAL-AUDIT.json')
    assert len(snapshots)==30 and len(audit['results'])==27
    for cid,row in snapshots.items():
        assert row['record']['id']==cid
        assert hashlib.sha256(canonical(row['record'])).hexdigest()==row['canonical_sha256']
        assert all(b['candidate_id']==cid for b in row['bindings'].values())
    for d in read('adoption-decisions.json')['decisions']:
        assert d['card_id'] in ids and d['status']=='PLAN_NOT_APPLIED'
        assert set(d['inspected_snapshot_ids'])<=set(snapshots)
    checks['existing_source_and_binding_snapshots']='PASS'
    with (HERE/'EVALUATION-CASES.tsv').open() as f:cases=list(csv.DictReader(f,delimiter='\t'))
    assert len(cases)==151 and len({c['case_id'] for c in cases})==151
    for c in cases:
        assert c['query_en'] and c['query_ko'] and c['search_status']=='NOT_RUN'
        for field in ['relevant_research_card_ids','wrong_substitution_card_ids']:
            assert set(filter(None,c[field].split('|')))<=ids
        if c['split']=='nonvisual':assert c['limit_or_expected_result']=='BLOCKED_UNSCORED'
    assert len(cases)*2==summary['bilingual_queries']==302
    checks['bilingual_evaluation_probes_and_nonvisual_limits']='PASS'
    for name in ['native_qualification','index_embedding','runtime_retrieval','image_generation','pixel_review','install_publish_commit_push']:
        assert summary[name]=='NOT_RUN'
    assert not summary['operational_source_changed_by_this_task']
    checks['operational_status_not_inflated']='PASS'
    # Report drift; never restore another task's changes or replace the original baseline.
    drift=[]
    for relative,old in baseline['protected_hashes'].items():
        now=digest(ROOT/relative)
        if old!=now:drift.append({'path':relative,'baseline_sha256':old,'current_sha256':now})
    current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    module_drift=[{'file':name,'baseline_sha256':sha,'current_sha256':digest(ROOT/'skills/photo-prompt-image-generator/assets'/name)} for name,sha in audit['module_hashes'].items() if digest(ROOT/'skills/photo-prompt-image-generator/assets'/name)!=sha]
    # Only verify local relative links, not external website contents or image pixels.
    for p in HERE.glob('*.md'):
        if p.name=='reference-excerpt.md':continue
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if re.match(r'^[a-zA-Z]+:',target) or target.startswith('#'):continue
            path=target.split('#',1)[0]
            if path in {'VALIDATION.json','SHA256SUMS'}:continue
            assert (p.parent/path).exists(),f'{p.name}: broken local link {target}'
    checks['local_document_links']='PASS'
    checksum_lines=[]
    for path in sorted(HERE.rglob('*')):
        if path.is_file() and path.name not in {'SHA256SUMS','VALIDATION.json'}:
            assert '__pycache__' not in path.parts
            checksum_lines.append(f'{digest(path)}  {path.relative_to(HERE)}')
    (HERE/'SHA256SUMS').write_text('\n'.join(checksum_lines)+'\n')
    result={'schema':'gaslamp-research-validation/v1','research_integrity':'PASS','checks':checks,'counts':summary,
        'protected_files_compared':len(baseline['protected_hashes']),'protected_file_drift':drift,'source_module_drift_since_audit':module_drift,
        'baseline_head':baseline['head'],'current_head':current_head,'head_changed':current_head!=baseline['head'],
        'workspace_preservation_status':'MATCH_AT_CHECK' if not drift and not module_drift else 'DRIFT_OBSERVED_DO_NOT_REVERT',
        'checksum_files':len(checksum_lines),'checksums_are':'byte integrity only; not factual accuracy or native/render qualification',
        'task_write_scope':'Only this new gaslamp research folder. Concurrent workspace changes, if any, are not attributed or reverted.',
        'external_source_fact_check':'LIMITED_TO_RECORDED_READ_SCOPES','native_retrieval_pixels':'NOT_RUN'}
    (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['research_integrity','checks','protected_files_compared','protected_file_drift','source_module_drift_since_audit','head_changed','workspace_preservation_status','checksum_files','native_retrieval_pixels']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
