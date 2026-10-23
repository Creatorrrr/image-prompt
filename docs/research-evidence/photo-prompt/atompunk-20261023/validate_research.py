"""Validate research references and ownership; this is not a semantic or pixel evaluator."""
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from research_context import HERE, ROOT, ASSETS


def read(name):
    return json.loads((HERE / name).read_text())


def rows(name):
    with (HERE / name).open() as f:
        return list(csv.DictReader(f, delimiter='\t'))


def canonical(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def main():
    errors, checks = [], []

    def check(condition, label):
        (checks if condition else errors).append(label)

    cards = read('semantic-cards.json')['cards']
    drafts = read('candidate-drafts.json')['drafts']
    routes = read('keyword-routes.json')['routes']
    sources = rows('SOURCES.tsv')
    ids = {c['id'] for c in cards}
    sid = {s['id'] for s in sources}
    seed_ids = {r['id'] for r in routes}
    catalog = read('catalog-snapshot.json')
    check(len(ids) == len(cards) == 101, '101 unique semantic cards')
    check(len(seed_ids) == len(routes) == 191, '191 original vocabulary rows routed')
    check(len(sid) == len(sources) == 53, '53 source ledger entries, including access failure')
    check(len({d['draft_id'] for d in drafts}) == len(drafts) == 88, '88 unique non-importable structural drafts')
    for c in cards:
        check(set(c['seed_ids']) <= seed_ids, f'{c["id"]} valid seed references')
        check(set(c['source_ids']) <= sid, f'{c["id"]} valid source references')
        check(set(c['planned_slots']) <= set(catalog), f'{c["id"]} proposed slots exist; meaning approval separate')
        owners = {o['id'] for o in c['owners']}
        check(len(owners) == len(c['owners']), f'{c["id"]} unique owner nodes')
        for r in c['relations']:
            check({r['subject'], r['object']} <= owners, f'{c["id"]} declared relation endpoints: {r}')
        visible = c['mode'] in {'still', 'proxy', 'versioned'}
        check(bool(c['owners']) == visible, f'{c["id"]} context-only cards have no positive owner projection')
        check(c['confusion_boundaries_ko'] and c['claim_limit_ko'], f'{c["id"]} confusion and claim limit')
    for r in routes:
        check(bool(r['card_ids']) and set(r['card_ids']) <= ids, f'{r["id"]} complete route')
    for d in drafts:
        check(d['semantic_card_id'] in ids and not d['runtime_importable'], f'{d["draft_id"]} research only')
        check(all(d[k] is None for k in ['native_source_proof', 'retrieval_receipt', 'image', 'pixel_review', 'requester_acceptance']),
              f'{d["draft_id"]} no fabricated execution or qualification')
    cases = rows('EVALUATION-CASES.tsv')
    check(len(cases) == len({r['id'] for r in cases}) == 60, '60 unique evaluation cases')
    check(Counter(r['cohort'] for r in cases) == {'development': 24, 'boundary': 16, 'ordinary_control': 12, 'nonvisual_control': 8},
          'evaluation cohort counts')
    for r in cases:
        check(bool(r['query_en'] and r['query_ko']) and r['status'] == 'NOT_RUN', f'{r["id"]} bilingual and not executed')
        check(set(filter(None, r['expected_cards'].split(','))) <= ids, f'{r["id"]} valid expected cards')
    scenes = rows('REALIZATIONS.tsv')
    check(len(scenes) == len({r['id'] for r in scenes}) == 18, '18 bilingual authored scene combinations')
    for r in scenes:
        check(set(r['cards'].split(',')) <= ids, f'{r["id"]} scene card references')
        check(all(r[k] for k in r), f'{r["id"]} bilingual text, prerequisites, effect and claim review')
    mapping = read('existing-source-mapping.json')
    mapped = {r['candidate_id'] for r in mapping['records']}
    decisions = rows('EXISTING-DECISIONS.tsv')
    check(len(decisions) == 23 and all(r['candidate_id'] in mapped for r in decisions), '23 existing-source triage records captured')
    for r in mapping['records']:
        check(canonical(r['full_source_record']) == r['source_sha256'], f'{r["candidate_id"]} full source hash')
        check(canonical(r['full_bindings']) == r['binding_set_sha256'], f'{r["candidate_id"]} full binding hash')
    # Markdown local links only; external availability is separately documented in the source ledger.
    for path in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if ':' not in target and not target.startswith('#'):
                target = target.split('#')[0]
                check(target in {'VALIDATION.json', 'SHA256SUMS'} or (path.parent / target).exists(),
                      f'{path.name} local link: {target}')
    baseline = read('BASELINE.json')
    drift = []
    for name, sha in baseline['tracked_sha256'].items():
        path = ROOT / name
        current = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        if current != sha:
            drift.append({'path': name, 'baseline': sha, 'current': current})
    # Concurrent changes are reported; never repaired or attributed to this research writer.
    snapshot = read('CORPUS-SNAPSHOT.json')
    source_drift = [name for name, sha in snapshot['module_sha256'].items()
                    if hashlib.sha256((ASSETS / name).read_bytes()).hexdigest() != sha]
    result = {'schema': 'atompunk-research-validation/v1',
              'status': 'PASS' if not errors else 'FAIL', 'checks_passed': len(checks), 'errors': errors,
              'counts': {'seeds': len(routes), 'cards': len(cards), 'drafts': len(drafts),
                         'source_entries': len(sources), 'realizations': len(scenes),
                         'evaluation_cases': len(cases), 'bilingual_queries': len(cases) * 2,
                         'reviewed_existing_records': len(decisions)},
              'tracked_file_comparison': {'count': len(baseline['tracked_sha256']), 'drift': drift},
              'corpus_module_drift_since_snapshot': source_drift,
              'current_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
              'not_validated': ['semantic truth', 'native source qualification', 'retrieval exposure or rank',
                                'installed runtime', 'image generation', 'native pixels', 'user acceptance'],
              'write_scope': 'this research directory only; no source/index/installed modifications'}
    (HERE / 'VALIDATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    checksums = []
    for path in sorted(HERE.rglob('*')):
        if path.is_file() and path.name != 'SHA256SUMS' and '__pycache__' not in path.parts:
            checksums.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(HERE)}')
    (HERE / 'SHA256SUMS').write_text('\n'.join(checksums) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'checks_passed', 'errors', 'counts']}, ensure_ascii=False))
    print(json.dumps({'tracked_file_drift': len(drift), 'corpus_module_drift': source_drift}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
