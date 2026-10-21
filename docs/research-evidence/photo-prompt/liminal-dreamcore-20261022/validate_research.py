"""Research integrity checks only; never claim native, retrieval, or pixel success."""
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit
import csv
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'


def read_json(name):
    return json.loads((HERE / name).read_text())


def read_tsv(name):
    with (HERE / name).open() as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    assert all(None not in r and all(v is not None and v != '' for v in r.values()) for r in rows), name
    return rows


def digest_record(record):
    raw = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()


def main():
    seeds, specs, sources = read_tsv('SEEDS.tsv'), read_tsv('SEMANTIC-SPEC.tsv'), read_tsv('SOURCES.tsv')
    assert len(seeds) == len(specs) == 200
    assert [int(r['id']) for r in seeds] == [int(r['id']) for r in specs] == list(range(1, 201))
    source_ids = {r['id'] for r in sources}
    assert len(source_ids) == len(sources) == 41
    assert all(urlsplit(s['url']).scheme == 'https' and urlsplit(s['url']).netloc for s in sources)
    cards = read_json('semantic-cards.json')['cards']
    drafts = read_json('candidate-drafts.json')['drafts']
    by_card = {c['id']: c for c in cards}
    assert len(by_card) == len(cards) == 200
    catalog = json.loads((ASSETS / 'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    all_gates = []
    for c in cards:
        assert set(c['source_ids']) <= source_ids, c['id']
        assert c['confusion_boundaries_ko'] and c['claim_limit_ko']
        assert set(c['planned_slots']) <= set(catalog), c['id']
        owner_ids = {o['id'] for o in c['owners']}
        assert len(owner_ids) == len(c['owners'])
        for r in c['relations']:
            assert {r['subject'], r['object']} <= owner_ids, (c['id'], r)
        has_draft = c['evidence_mode'] in {'still', 'proxy', 'versioned'}
        assert bool(c['still_candidate_draft']) == has_draft
        assert bool(c['owners']) == has_draft
        assert len(c['render_gate_proposals']) == len(c['owners']) + len(c['relations'])
        all_gates.extend(g['id'] for g in c['render_gate_proposals'])
    assert len(set(all_gates)) == len(all_gates)
    assert len(drafts) == 128
    for d in drafts:
        c = by_card[d['semantic_card_id']]
        assert c['still_candidate_draft'] == d['draft_id']
        assert d['registration_status'] == 'not_in_operating_manifest'
        assert d['runtime_importable'] is False
        assert d['owner_graph']['relations'] == c['relations']
        assert d['native_evidence'] is d['embedding'] is d['retrieval_receipt'] is d['pixel_review'] is None
        assert 'claim_limit' not in d['positive_projection_en']
        assert d['positive_projection_en'] and d['relation_projection_for_authoring']
    realizations = read_tsv('REALIZATIONS.tsv')
    assert len(realizations) == len({r['id'] for r in realizations}) == 32
    for r in realizations:
        assert all(1 <= int(n) <= 200 for n in r['seed_ids'].split(','))
        assert re.search('[가-힣]', r['phrase_ko']) and re.search('[A-Za-z]', r['phrase_en'])
    cases = read_tsv('EVALUATION-CASES.tsv')
    assert len(cases) == len({r['id'] for r in cases}) == 48
    assert Counter(c['cohort'] for c in cases) == {'development': 32, 'ordinary_control': 12, 'nonvisual_control': 4}
    assert all(set(c['target_cards'].split(',')) <= set(by_card) for c in cases)
    assert read_json('evaluation-cases.json')['execution_status'] == 'NOT_RUN'
    mappings = read_json('existing-source-mapping.json')['rows']
    assert len(mappings) == 23
    corpus = {}
    for module in json.loads((ASSETS / 'photo_candidate_corpus_manifest.json').read_text())['modules']:
        data = json.loads((ASSETS / module['file']).read_text())
        corpus.update(data.get('candidates', {}))
    assert not any(d['draft_id'] in corpus for d in drafts)
    mapped_source_drift = []
    for m in mappings:
        assert m['candidate_id'] == m['full_source_record']['id']
        assert digest_record(m['full_source_record']) == m['source_sha256']
        if m['candidate_id'] not in corpus or digest_record(corpus[m['candidate_id']]) != m['source_sha256']:
            mapped_source_drift.append(m['candidate_id'])
        assert all(b['candidate_id'] == m['candidate_id'] for b in m['full_bindings'])
    missing_links = []
    for f in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', f.read_text()):
            if '://' not in target and not target.startswith('#') and not (HERE / target.split('#')[0]).exists():
                missing_links.append({'file': f.name, 'target': target})
    assert not missing_links, missing_links
    baseline = read_json('BASELINE.json')
    tracked_drift = []
    for name, old_hash in baseline['tracked_sha256'].items():
        f = ROOT / name
        if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != old_hash:
            tracked_drift.append(name)
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
    source_drift = bool(tracked_drift or mapped_source_drift or head != baseline['head'])
    result = {
        'schema': 'liminal-research-validation/v1',
        'status': 'STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE' if source_drift else 'STRUCTURE_PASS_PROTECTED_TRACKED_SOURCES_UNCHANGED',
        'counts': read_json('PACKAGE.json')['counts'],
        'evidence_modes': dict(Counter(c['evidence_mode'] for c in cards)),
        'owner_component_count': sum(len(c['owners']) for c in cards),
        'directed_relation_count': sum(len(c['relations']) for c in cards),
        'planned_gate_count': len(all_gates),
        'relative_markdown_links': 'pass',
        'source_refs_owner_endpoints_slots': 'pass',
        'source_mapping_hashes': 'pass_internal_snapshot',
        'head_before': baseline['head'], 'head_after': head,
        'protected_tracked_files': len(baseline['tracked_sha256']),
        'tracked_source_drift': tracked_drift,
        'mapped_source_drift': mapped_source_drift,
        'preexisting_untracked_files': 'not fully hash baselined; none are mutation targets of these scripts',
        'proof_boundary': 'structural integrity only; natural-language truth and research completeness are not certified by this script',
        'runtime_candidate_registration': 'NOT_RUN', 'native_qualification': 'NOT_RUN',
        'embedding_inference': 'NOT_RUN', 'retrieval_evaluation': 'NOT_RUN',
        'index_build_publication_activation': 'NOT_RUN', 'image_generation_pixel_review': 'NOT_RUN',
        'independent_holdout': 'NOT_RUN', 'requester_acceptance': 'PENDING',
        'commit_push': 'NOT_RUN',
    }
    (HERE / 'VALIDATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    checksum_lines = []
    for f in sorted(HERE.iterdir()):
        if f.is_file() and f.name != 'SHA256SUMS':
            checksum_lines.append(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}')
    (HERE / 'SHA256SUMS').write_text('\n'.join(checksum_lines) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
