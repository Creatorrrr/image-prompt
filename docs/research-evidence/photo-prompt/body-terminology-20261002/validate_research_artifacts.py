"""Validate research consistency and source preservation; no runtime or image test."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(name):
    return json.loads((OUT / name).read_text())

def unique(entries, name):
    ids = [x['id'] for x in entries]
    require(len(ids) == len(set(ids)), name + ' duplicate IDs')
    return set(ids)

audit = read('CURRENT-DATA-AUDIT.json')
sources = read('SOURCES.json')['sources']
source_ids = unique(sources, 'sources')
require(all(s['url'].startswith('https://') for s in sources), 'non-https source')
semantics = read('SEMANTIC-PROPOSALS.json')
proposals = semantics['proposals']
proposal_ids = unique(proposals, 'proposals')
candidates = read('CANDIDATE-PROPOSALS.json')['candidates']
unique(candidates, 'candidates')
require(len(candidates) == len(proposals) == 91, 'proposal count mismatch')
require(len(semantics['knowledge_and_context_records']) == 11, 'context count mismatch')
profiles = {p['id'] for p in audit['selected_profiles']}
for p in proposals:
    require(p['status'] == 'research_proposal_not_implemented' and p['export_allowed'] is False,
            p['id'] + ' has runtime/export claim')
    require(set(p['source_refs']) <= source_ids, p['id'] + ' unknown source')
    require(set(p['existing_profile_ids']) <= profiles, p['id'] + ' unknown existing owner')
    groups = unique(p['component_groups'], p['id'] + ' components')
    require(len(groups) >= 3, p['id'] + ' missing concrete component groups')
    require(groups == {g['id'] for g in p['proposed_render_gates']}, p['id'] + ' incomplete gates')
    require(bool(p['closest_counterexample'] and p['required_view_state']), p['id'] + ' missing boundary')
for c in candidates:
    require(c['semantic_proposal_id'] in proposal_ids, c['id'] + ' unknown semantic proposal')
    require(c['export_allowed'] is False, c['id'] + ' export enabled')
    effects = {p['dimension'] for p in c['affected_properties']}
    require(effects == set(c['complete_effect_dimensions']), c['id'] + ' incomplete dimensions')
    compatible = effects <= set(c['slot_declared_dimensions'])
    require(compatible or c['admission_status'] == 'ownership_split_required', c['id'] + ' hidden ownership conflict')
    text = json.dumps(c['positive_candidate_text'], ensure_ascii=False)
    require('http://' not in text and 'https://' not in text, c['id'] + ' source URL in positive text')
    require(len(c['positive_candidate_text']['concept_units']) >= 3, c['id'] + ' empty semantic units')

terms = read('TERM-INVENTORY.json')['terms']
term_ids = unique(terms, 'inventory')
coverage = read('COVERAGE-MAP.json')['terms']
require(len(terms) == len(coverage) == 415, 'inventory/coverage count mismatch')
require(term_ids == {c['term_id'] for c in coverage}, 'coverage IDs mismatch')
require({t['section'] for t in terms} == set(range(1, 20)), 'missing chapter')
for c in coverage:
    require(set(c['related_axis_proposal_ids']) <= proposal_ids, c['term_id'] + ' bad axis reference')
    require(c['runtime_alias_authorized'] is False, c['term_id'] + ' implied exact alias')
cases = [json.loads(line) for line in (OUT / 'REGRESSION-CASES.jsonl').read_text().splitlines() if line]
unique(cases, 'regression cases')
require(len(cases) == 70, 'case count mismatch')
for case in cases:
    require(case['status'] == 'proposed_not_run', case['id'] + ' false test pass claim')
    require(set(case['proposal_ids']) <= proposal_ids, case['id'] + ' bad proposal reference')

matches = []
for source in audit['source_files']:
    path = ROOT / source['path']
    match = path.is_file() and sha(path) == source['sha256']
    matches.append(dict(path=source['path'], unchanged=match))
    require(match, 'baseline source changed: ' + source['path'])
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
require(head == audit['head'], 'HEAD changed since baseline')

owners = read('EXISTING-OWNER-MAP.json')
require(len(owners) == len({x['profile_id'] for x in owners}) == 15, 'existing-owner mapping count')
for owner in owners:
    entries = json.loads((ROOT / owner['path']).read_text()).get('profiles', [])
    require(any(p['id'] == owner['profile_id'] for p in entries), 'owner not in current source: ' + owner['profile_id'])

artifact_receipts = []
for path in sorted(OUT.iterdir()):
    if not path.is_file() or path.name == 'VALIDATION.json':
        continue
    content = path.read_text()
    if path.suffix == '.json':
        json.loads(content)
    if path.suffix == '.md':
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if ':' in target or target.startswith('#'):
                continue
            require(target == 'VALIDATION.json' or (path.parent / target).exists(), path.name + ' broken local link: ' + target)
    for number, line in enumerate(content.splitlines(), 1):
        require(line == line.rstrip(), path.name + ':' + str(number) + ' trailing whitespace')
    artifact_receipts.append(dict(path=path.name, bytes=path.stat().st_size, sha256=sha(path)))

diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, text=True, capture_output=True)
require(diff.returncode == 0, 'git diff --check failed: ' + diff.stdout + diff.stderr)
result = dict(schema_version='body-research-artifact-validation/v1', checked_on='2026-10-02',
    status='PASS' if not errors else 'FAIL', errors=errors, head=head,
    source_files_checked=len(matches), source_files_unchanged=sum(m['unchanged'] for m in matches),
    source_checks=matches, json_references_valid=not errors,
    counts=dict(sources=len(sources), proposals=len(proposals), candidates=len(candidates),
        context_records=len(semantics['knowledge_and_context_records']), terms=len(terms),
        regression_cases=len(cases), existing_profile_owners=len(owners)),
    ownership_splits_required=[c['id'] for c in candidates if c['admission_status'] == 'ownership_split_required'],
    artifacts=artifact_receipts,
    validation_scope=['research artifact syntax and referential consistency',
        'proposal component/gate completeness', 'explicit symbolic ownership and blocked export',
        'baseline source hash preservation', 'tracked diff and local documentation whitespace'],
    not_run=['runtime data implementation', 'dictionary validator and unit regression tests',
        'embedding/index build', 'frozen-core retrieval comparison', 'prompt/runtime generation audit',
        'image render and pixel review', 'user acceptance'])
(OUT / 'VALIDATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k:result[k] for k in ('status', 'errors', 'source_files_checked', 'source_files_unchanged', 'counts')}, ensure_ascii=False))
raise SystemExit(1 if errors else 0)
