#!/usr/bin/env python3
"""Validate research integrity, without claiming retrieval or pixel success."""
from pathlib import Path
from collections import Counter
import datetime
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def read(name):
    return json.loads((HERE / name).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def main():
    tables, routes = read('conversation-tables.json'), read('keyword-routes.json')
    cards, drafts = read('semantic-cards.json'), read('candidate-drafts.json')
    sources, evals = read('sources.json'), read('evaluation-cases.json')
    comparisons, baseline = read('existing-source-mapping.json'), read('BASELINE.json')
    assert len(tables)==23 and sum(len(t)-1 for t in tables)==247
    assert len(routes)==247 and len({r['id'] for r in routes})==247
    assert [r['term'] for r in routes]==[r[0] for t in tables for r in t[1:]]
    assert [r['original_definition'] for r in routes]==[' | '.join(r[1:]) for t in tables for r in t[1:]]
    assert all(r['hard_activation'] is False and r['automatic_bundle'] is False for r in routes)
    assert sum(r['classification']=='sensitive_context_diagnostic' for r in routes)==30
    card_ids = {c['id'] for c in cards}
    assert len(card_ids)==len(cards)==96
    source_ids = {s['id'] for s in sources}
    slot_catalog = json.loads((ROOT / 'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    for c in cards:
        assert set(c['source_ids'])<=source_ids
        assert set(c['planned_slots'])<=set(slot_catalog), c['id']
        assert c['runtime_registered'] is False and c['native_pixel_status']=='NOT_RUN'
        assert len(c['components'])==3 and all(g['required'] and g['en'] and g['ko'] and g['render_gate'] for g in c['components'])
        assert len({g['id'] for g in c['components']})==3
        assert len(set(c['seed_terms']))==len(c['seed_terms'])
        assert set(c['seed_terms'])<={r['term'] for r in routes}
        owners = {n['id'] for n in c['owners']}
        assert len(owners)==len(c['owners']) and owners and c['relations']
        assert all(e['subject'] in owners and e['object'] in owners for e in c['relations']), c['id']
    assert all(set(r['optional_realization_ids'])<=card_ids for r in routes)
    assert len(drafts)==90 and len({d['draft_id'] for d in drafts})==90
    assert all(d['research_card_id'] in card_ids and d['runtime_registered'] is False and d['native_qualification']=='NOT_RUN' and d['registration_status']=='not_in_operating_manifest' for d in drafts)
    assert not any(d['mode']=='sequence' or d['research_card_id'] in {'V064','V074'} for d in drafts)
    assert len(evals)==40 and all(e['query_ko'] and e['query_en'] and e['execution_status']=='NOT_RUN' and e['results'] is None for e in evals)
    assert all(e['expected_card']=='NONE' or e['expected_card'] in card_ids for e in evals)
    assert len(comparisons)==15
    assert all(m['decision'] in {'reuse','refine','new','context','defer'} and m['card_id'] in card_ids and m['existing_record']['id']==m['existing_id'] for m in comparisons)
    for m in comparisons:
        actual = hashlib.sha256(json.dumps(m['existing_record'], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        assert actual==m['record_sha256']
        assert all(b['candidate_id']==m['existing_id'] for b in m['existing_bindings'])
    counts = read('PACKAGE-COUNTS.json')
    assert counts['card_modes']==dict(Counter(c['mode'] for c in cards))
    assert counts['route_classes']==dict(Counter(r['classification'] for r in routes))
    own_prefix = str(HERE.relative_to(ROOT))+'/'
    raw_status = subprocess.check_output(['git','status','--porcelain=v1','-z'], cwd=ROOT)
    dirty = [x.decode() for x in raw_status.split(b'\0') if x]
    head = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    drift = [{'path':name,'before':old,'after':digest(ROOT/name)} for name,old in baseline['protected_hashes'].items() if digest(ROOT/name)!=old]
    manifest = json.loads((ROOT / 'skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json').read_text())
    assert all('marine_literature' not in m['file'] for m in manifest['modules'])
    (HERE / 'SOURCE-OBSERVATIONS.json').write_text(json.dumps({
        'baseline_head':baseline['head'],'current_head':head,
        'baseline_dirty_entries':baseline['dirty_entry_count'],'current_dirty_entries':len(dirty),
        'protected_file_count':len(baseline['protected_hashes']),'protected_file_drift':drift,
        'research_path':own_prefix,'own_git_status':[s for s in dirty if own_prefix in s],
        'qualification':'Hashes describe observed bytes; concurrent drift is preserved, not reverted. No source/index/runtime publication was invoked. CURRENT was not captured at turn start, so whole-turn installed-runtime invariance is not asserted.'
    },ensure_ascii=False,indent=2)+'\n')
    report = {
        'status':'RESEARCH_STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE' if drift or head!=baseline['head'] else 'RESEARCH_STRUCTURE_PASS',
        'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'coverage':{'tables':23,'keyword_rows':247,'semantic_cards':96,'required_bilingual_component_groups':288,
                    'candidate_drafts':90,'sources':20,'full_existing_record_comparisons':15,'evaluation_cases_not_executed':40,'bilingual_queries_not_executed':80},
        'checks':['full table row and definition preservation','unique research identities','declared relation endpoints',
                  'bilingual required groups','source references and planned slot existence','sensitive context retention',
                  'no automatic hard activation or bundles','sequence and diagnostic proxy exclusions from candidate drafts',
                  'full existing-record canonical hashes and binding ownership','current manifest has no proposed research module'],
        'protected_file_drift_count':len(drift),'head_drift':head!=baseline['head'],
        'not_established':['independent truth of every seed definition','full fanart pixel review','exhaustive semantic deduplication',
                           'native source compilation','embedding execution','actual candidate retrieval','image generation','native pixel qualification','installed runtime change','user acceptance'],
        'writes':'research directory only as authored task output; no authored operating source changes, index builds, publication, commit or push',
    }
    (HERE / 'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))


if __name__ == '__main__':
    main()
