"""Validate this research delivery and record, without repairing, workspace drift."""
from pathlib import Path
import collections
import csv
import datetime
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
REPORT = ROOT / 'docs/analysis/2026-10-09-spring-fashion-visual-semantics-research.md'
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'


def read(name):
    return json.loads((OUT / name).read_text())


def write(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def digest(path):
    hasher = hashlib.sha256()
    with path.open('rb') as handle:
        for part in iter(lambda: handle.read(1024 * 1024), b''):
            hasher.update(part)
    return hasher.hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8')


counts = read('validation.json')['counts']
cards = read('semantic-cards.json')['cards']
drafts = read('candidate-drafts.json')['drafts']
terms = read('term-plan.json')['terms']
sources = read('sources.json')['sources']
regression = read('regression-plan.json')
plan = read('implementation-plan.json')
original = read('thread-rows.json')
before = read('workspace-before.json')
snapshot = read('current-inventory.json')
checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


check('289 original keyword rows, 15 combinations and 8 outfits',
      collections.Counter(row['section'] for row in original)
      == dict(enumerate([20, 18, 15, 17, 24, 16, 18, 16, 15, 25, 21, 24, 24, 24, 12, 15, 8], 1)))
check('118 cards, 281 drafts, 289 mapped terms',
      (len(cards), len(drafts), len(terms)) == (118, 281, 289))
check('40 external sources with 37 direct and 3 search-only entries',
      len(sources) == 41 and counts['sources_page_or_collection_verified'] == 37
      and counts['sources_search_only'] == 3)
check('14 conversation-seed-only cards are explicitly distinguished',
      sum(c['evidence_level'] == 'conversation_seed_only' for c in cards) == 14)
hidden = {'SPT10-01', 'SPT10-02', 'SPT10-03', 'SPT10-04', 'SPT10-23', 'SPT15-06'}
check('Six hidden specification terms deliberately have no direct drafts',
      {t['term_id'] for t in terms if not t['direct_draft_ids']} == hidden
      and all('no still-image hard proof' in t['handling'] for t in terms if t['term_id'] in hidden))
check('Visible-bra row is not mislabeled as hidden absence',
      all(t['direct_draft_ids'] and 'no still-image hard proof' not in t['handling']
          for t in terms if t['term_id'] == 'SPT15-05'))
check('32 P0 cards and 86 P1 cards',
      collections.Counter(c['priority'] for c in cards) == {'P0': 32, 'P1': 86})
check('66 comparison pairs, 14 mutations and 12 planned pixel arms',
      (len(regression['comparisons']), len(regression['mutations']),
       len(regression['native_pixel_arms'])) == (66, 14, 12))
original_outfits = {r['term_id']: r for r in original if r['section'] == 17}
check('Eight image arms preserve the exact original outfit and emphasis',
      all(arm['request_seed'] == original_outfits[arm['original_outfit_id']]['original_description']
          and arm['original_emphasis'] == original_outfits[arm['original_outfit_id']]['outfit_emphasis']
          for arm in regression['native_pixel_arms'][:8]))
check('Twelve planned arm IDs are unique and all referenced cards exist',
      {a['arm_id'] for a in regression['native_pixel_arms']} == {f'P{i:02d}' for i in range(1, 13)}
      and all(set(a['card_ids']) <= {c['id'] for c in cards} for a in regression['native_pixel_arms']))
check('Main report retains all eight original outfit clauses',
      all(r['original_description'] in REPORT.read_text() for r in original_outfits.values()))
check('All card, draft and term rows remain disabled research proposals',
      all(row['runtime_ready'] is False for row in [*cards, *drafts, *terms]))
check('Variant graphs and property paths are explicitly pending runtime binding',
      all('Not yet bound' in d['graph_binding_status'] for d in drafts)
      and all('proposals' in c['property_path_status'] for c in cards))
check('Planned regression scenarios are not execution claims',
      regression['execution_status'] == 'not_run'
      and all(c['run_status'] == 'planned_not_executed' for c in regression['comparisons'])
      and all(c['run_status'] == 'planned_not_executed' for c in regression['native_pixel_arms']))
check('Implementation phases 0 through 8 and disabled runtime status',
      [w['phase'] for w in plan['work_packages']] == list(range(9))
      and plan['runtime_ready'] is False)
with (OUT / 'term-plan.csv').open(encoding='utf-8-sig', newline='') as handle:
    csv_rows = list(csv.DictReader(handle))
check('CSV and JSON retain the same term identities in order',
      [r['term_id'] for r in csv_rows] == [r['term_id'] for r in terms])
detail = (OUT / 'semantic-cards.md').read_text()
check('Readable cards contain all 118 headings and 281 draft IDs',
      len(re.findall(r'^## SF\d{3} ', detail, flags=re.M)) == 118
      and set(re.findall(r'SPR_DRAFT_SF\d{3}_\d{2}', detail))
      == {d['draft_id'] for d in drafts})

changed, missing, unchanged = [], [], 0
for relative, prior_sha in before['tracked_file_hashes'].items():
    path = ROOT / relative
    if not path.is_file():
        missing.append(relative)
        continue
    current_sha = digest(path)
    if current_sha == prior_sha:
        unchanged += 1
    else:
        changed.append({'path': relative, 'before_sha256': prior_sha, 'after_sha256': current_sha})
head_after = git('rev-parse', 'HEAD').strip()
status_after = git('status', '--porcelain=v1', '-z', '--untracked-files=all')
baseline_untracked = [entry[3:] for entry in before['status_porcelain'].split('\0')
                      if entry.startswith('?? ')]
missing_untracked = [name for name in baseline_untracked
                     if not (ROOT / name).exists() and not (ROOT / name).is_symlink()]
source_changes = []
for name, prior_sha in snapshot['source_sha256'].items():
    path = ASSETS / name
    current_sha = digest(path) if path.is_file() else None
    if current_sha != prior_sha:
        source_changes.append({'file': name, 'snapshot_sha256': prior_sha, 'final_sha256': current_sha})
manifest_sha = digest(ASSETS / 'photo_prompt_source_manifest.json')
snapshot_manifest_changed = manifest_sha != snapshot['source_manifest_sha256']
own_paths = sorted([str(REPORT.relative_to(ROOT)),
                    *(str(p.relative_to(ROOT)) for p in OUT.rglob('*') if p.is_file()
                      and '__pycache__' not in p.parts)])
preservation = {
    'schema_version': 'spring-fashion-preservation/v1',
    'observed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'baseline_observed_at_utc': before['observed_at_utc'],
    'head_before': before['head'], 'head_after': head_after,
    'head_unchanged': before['head'] == head_after,
    'tracked_baseline_files': len(before['tracked_file_hashes']),
    'tracked_unchanged': unchanged, 'tracked_changed': changed, 'tracked_missing': missing,
    'untracked_baseline_paths': len(baseline_untracked),
    'untracked_missing_paths': missing_untracked,
    'status_before': before['status_porcelain'], 'status_after': status_after,
    'research_authored_scope': own_paths,
    'scope_note': 'This research writes only its new research folder and analysis report. Byte differences outside that scope are observations, not attribution; nothing is restored or staged.',
    'untracked_evidence_limit': 'Untracked presence is recorded in Git status; all untracked bytes were not captured by the baseline. Research did not edit pre-existing untracked files.',
    'preservation_status': 'EXISTING_TRACKED_BYTES_UNCHANGED' if not changed and not missing
                           else 'WORKSPACE_DRIFT_RECORDED_WITHOUT_REPAIR',
    'snapshot_source_changes_at_finish': source_changes,
    'snapshot_manifest_changed_at_finish': snapshot_manifest_changed,
    'snapshot_manifest_final_sha256': manifest_sha,
    'snapshot_currentness': 'SOURCE_HASHES_UNCHANGED' if not source_changes and not snapshot_manifest_changed
                           else 'DATED_SNAPSHOT_ONLY_RECHECK_BEFORE_INTEGRATION',
    'execution': {'asset_edits_by_research': False, 'git_stage_commit_push_pr': False,
                  'restores_resets': False, 'embedding_calls': 0, 'image_calls': 0}
}
write('final-preservation.json', preservation)

# These two files are created by this check. Verify their planned local links
# and then write the manifest after every other artifact has been finalized.
virtual_outputs = {OUT / 'report-validation.json', OUT / 'artifact-manifest.json'}
local_links = []
for doc in [REPORT, *sorted(OUT.glob('*.md'))]:
    check(f'Markdown has nonempty content: {doc.name}', bool(doc.read_text().strip()))
    for target in re.findall(r'\[[^\]\n]*\]\(([^\)\n]+)\)', doc.read_text()):
        if target.startswith('/'):
            path = Path(unquote(target).split('#', 1)[0])
            check(f'Local Markdown target exists: {path}', path.is_file() or path in virtual_outputs)
            local_links.append({'document': str(doc.relative_to(ROOT)), 'target': str(path)})
check('Main report accurately includes required scope and status counts',
      all(fragment in REPORT.read_text() for fragment in
          ['289', '118개', '281개', '66쌍', '14개', '12묶음', '37개', '3개', '미실행', 'runtime_ready=false']))
json_paths = sorted(p for p in OUT.glob('*.json') if p.name not in
                    {'report-validation.json', 'artifact-manifest.json'})
for path in json_paths:
    json.loads(path.read_text())
check('All saved research JSON inputs and outputs parse', bool(json_paths))
write('report-validation.json', {
    'schema_version': 'spring-fashion-report-validation/v1', 'status': 'PASS',
    'scope': 'Research integrity, document links, count/status agreement and preservation observations only. No runtime, retrieval or pixel qualification.',
    'observed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'checks': checks, 'local_links': local_links, 'counts': counts,
    'preservation_status': preservation['preservation_status'],
    'snapshot_currentness': preservation['snapshot_currentness'],
    'execution': read('validation.json')['execution']
})
files = [REPORT, *sorted(p for p in OUT.rglob('*') if p.is_file()
                       and p.name != 'artifact-manifest.json' and '__pycache__' not in p.parts)]
write('artifact-manifest.json', {
    'schema_version': 'spring-fashion-artifact-manifest/v1',
    'observed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'self_hash_excluded': True,
    'files': [{'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
               'sha256': digest(p)} for p in files]
})
print(json.dumps({'status': 'PASS', 'counts': counts, 'checks': len(checks),
                  'local_links': len(local_links), 'tracked_unchanged': unchanged,
                  'tracked_changed_count': len(changed), 'tracked_missing_count': len(missing),
                  'untracked_missing_count': len(missing_untracked),
                  'head_unchanged': preservation['head_unchanged'],
                  'snapshot_currentness': preservation['snapshot_currentness'],
                  'scope': 'Research/document integrity only; no execution-data or image qualification'},
                 ensure_ascii=False, indent=2))
