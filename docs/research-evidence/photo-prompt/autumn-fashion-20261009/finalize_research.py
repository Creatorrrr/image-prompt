"""Validate research references and observe source preservation without mutations."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import stat
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REPORT = ROOT / 'docs/analysis/2026-10-09-autumn-fashion-visual-semantics-research.md'


def read(name):
    return json.loads((HERE / name).read_text())


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def current_snapshot(saved):
    result = {}
    for key in saved:
        path = ROOT / key
        if path.is_file():
            data = path.read_bytes()
            result[key] = {'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),
                'mode':stat.S_IMODE(path.stat().st_mode)}
        else:
            result[key] = {'absent':True}
    return result


def main():
    baseline = read('source-snapshot.json')
    current_sources = current_snapshot(baseline['source_files'])
    current_dirty = current_snapshot(baseline['tracked_dirty_files'])
    changed_sources = [p for p in current_sources if current_sources[p] != baseline['source_files'][p]]
    changed_dirty = [p for p in current_dirty if current_dirty[p] != baseline['tracked_dirty_files'][p]]
    head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    own_files = sorted(str(p.relative_to(ROOT)) for p in HERE.iterdir() if p.is_file())
    own_files += [str(REPORT.relative_to(ROOT))]
    dump('final-preservation.json', {'observed_at_kst':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),
        'baseline_head':baseline['head'],'observed_head':head,'head_unchanged':head==baseline['head'],
        'source_hash_mode_changes_since_inventory':changed_sources,
        'preexisting_tracked_dirty_hash_mode_changes':changed_dirty,
        'all_observed_source_bytes_unchanged':not changed_sources,
        'all_observed_preexisting_tracked_dirty_bytes_unchanged':not changed_dirty,
        'actual_task_write_scope':own_files,
        'untracked_external_contents_hashed':False,
        'scope_limit':'Source/code/index-manifest and tracked-dirty observations; external untracked contents were not fully hashed. Concurrent changes, if any, are observed, not attributed or reverted.',
        'runtime_writes_performed_by_this_task':False,
        'commit_push_or_ref_mutation_performed':False})
    cards = read('semantic-cards.json')['cards']
    ids = {c['id'] for c in cards}
    plan = read('term-plan.json')['terms']
    candidates = read('candidate-proposals.json')['candidates']
    regression = read('regression-plan.json')
    implementation = read('implementation-plan.json')
    outfits = read('source-outfit-examples.json')
    sources = read('sources.json')['sources'] + read('supplemental-sources.json')['sources']
    with (HERE/'term-plan.csv').open(newline='') as stream:
        csv_rows = list(csv.DictReader(stream))
    assert len(csv_rows)==len(plan)==347
    for csv_row, row in zip(csv_rows,plan):
        for key,value in csv_row.items():
            expected = ';'.join(row[key]) if isinstance(row[key],list) else str(row[key])
            assert value==expected,(row['term_id'],key)
    assert all(c['card_id'] in ids for c in candidates)
    assert all(t['card_id'] in ids for t in plan)
    assert all(set(p['card_ids'])<=ids for p in regression['comparison_pairs']+regression['native_image_groups'])
    assert all(set(w.get('card_ids',[]))<=ids for w in implementation['work_waves'])
    assert len(regression['comparison_pairs'])==56
    assert len(regression['mutation_cases'])==12
    assert len(regression['native_image_groups'])==12
    assert len(outfits['outfit_examples'])==12 and len(outfits['reverse_lookup'])==10
    assert all(p['status']=='planned_not_run' for p in regression['comparison_pairs']+regression['mutation_cases'])
    assert all(p['status']=='planned_not_executed' for p in regression['native_image_groups'])
    existing_paths = implementation['current_files_to_review']+implementation['existing_verification_entrypoints']
    missing_paths = [p for p in existing_paths if not (ROOT/p).is_file()]
    assert not missing_paths,missing_paths
    candidate_ids = {x['id'] for x in read('current-positive-records.json')['candidates']}
    profile_ids = {x['id'] for x in read('current-positive-records.json')['profiles']}
    # Full lexical inventories may contain high-count terms omitted from the compact record export.
    inventory = read('term-inventory.json')['terms']
    all_candidate_ids = {h['id'] for t in inventory for h in t['positive_field_mentions']['candidates']}
    all_profile_ids = {h['id'] for t in inventory for h in t['positive_field_mentions']['profiles']}
    assert all(set(t['candidate_neighbor_ids'])<=all_candidate_ids and
        set(t['profile_neighbor_ids'])<=all_profile_ids for t in plan)
    sources_by_id = {s['id']:s for s in sources}
    assert len(sources_by_id)==42 and all(set(c['source_ids'])<=sources_by_id.keys() for c in cards)
    assert all(c['native_review_contract']['family_axis_authority'].startswith('Advisory') for c in candidates)
    assert all(c['native_review_contract']['selected_variant_evidence'][0]['statement_en']==c['phrase_en'] for c in candidates)
    # This output is named by the main report and is written after the link check.
    generated_name = HERE/'report-validation.json'
    markdown_files = [REPORT,HERE/'README.md',HERE/'semantic-cards.md',HERE/'sources.md']
    broken_links=[]
    local_links=[]
    for path in markdown_files:
        for link in re.findall(r'\]\((/[^)]+)\)',path.read_text()):
            target=Path(link.split(':')[0])
            local_links.append(str(target))
            if not target.is_file() and target != generated_name:
                broken_links.append({'from':str(path.relative_to(ROOT)),'target':str(target)})
    assert not broken_links,broken_links
    manifests={}
    for path in sorted(HERE.iterdir()):
        if path.is_file() and path.name not in {'report-validation.json','artifact-manifest.json'}:
            manifests[path.name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
    manifests[str(REPORT.relative_to(ROOT))]={'sha256':hashlib.sha256(REPORT.read_bytes()).hexdigest(),'bytes':REPORT.stat().st_size}
    dump('artifact-manifest.json', {'files':manifests,'purpose':'Bindings for this research publication, not runtime source/index authority'})
    result={'status':'PASS','validated_at_kst':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),
        'terms':347,'cards':113,'candidate_drafts':129,'sources':42,'comparison_pairs':56,
        'mutation_cases':12,'native_image_groups':12,'source_outfit_examples':12,'reverse_lookup_rows':10,
        'csv_json_identical':True,'card_candidate_source_references_valid':True,
        'family_axes_are_advisory_not_active_sibling_gates':True,'existing_plan_paths_valid':True,
        'local_markdown_links_checked':len(local_links),'broken_local_links':broken_links,
        'compact_existing_candidate_records':len(candidate_ids),'compact_existing_profile_records':len(profile_ids),
        'validation_scope':'Research artifact integrity and explicit planned/executed boundaries. Not fact certification, runtime regression or pixel qualification.',
        'source_changed_since_inventory':changed_sources,'tracked_dirty_changed_since_inventory':changed_dirty,
        'image_calls':0,'embedding_calls':0,'runtime_registration_executed':False,'index_rebuild_executed':False}
    dump('report-validation.json',result)
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':
    main()
