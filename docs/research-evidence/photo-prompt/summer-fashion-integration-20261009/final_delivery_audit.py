"""Read-only delivery integrity audit; does not infer pixel or user acceptance."""
import hashlib
import json
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/chasoik/Projects/image-prompt')
WORKTREE = Path('/Users/chasoik/.codex/worktrees/summer-fashion-integration-20261009/image-prompt')
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/summer-fashion-integration-20261009'
CAMPAIGN = ROOT / 'runs/summer-fashion-qualification-20261009'
SKILL = ROOT / 'skills/photo-prompt-image-generator'
REFERENCE = Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
sys.path.insert(0, str(SKILL / 'scripts'))
from photo_runtime_sources import capture_sources, default_store, json_digest, _pointer_directory, _read_current


def read(path):
    return json.loads(path.read_text())


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def signature(path):
    if not path.is_file():
        return None
    return dict(sha256=sha(path), mode=stat.S_IMODE(path.stat().st_mode), bytes=path.stat().st_size)


def latest(arm, basename):
    paths = sorted((CAMPAIGN / arm / 'revisions').glob('*/' + basename), key=lambda p: p.stat().st_mtime)
    return paths[-1]


def main():
    failures = []

    def require(value, label):
        if not value:
            failures.append(label)

    ready = read(EVIDENCE / 'data-ready.json')
    expected = ready['data_ready_generation']
    source, _ = capture_sources(SKILL)
    directory = _pointer_directory(default_store(), SKILL, 'local_current')
    pointer = _read_current(directory)
    revision = read(directory / 'SOURCE.json')
    require(pointer['source_fingerprint'] == json_digest(source), 'current primary pointer/source mismatch')
    require(not revision.get('editing'), 'unfinished source revision')
    require(sha(SKILL / 'SKILL.md') == ready['canonical_skill_sha256'], 'canonical skill drift')
    require(sha(ROOT / '.agents/skills/photo-prompt-image-generator/SKILL.md') == ready['mirror_skill_sha256'], 'mirror skill drift')

    baseline = read(EVIDENCE / 'primary-application-baseline.json')
    owned_derived = {str(Path('skills/photo-prompt-image-generator/assets') / name) for name in (
        'photo_prompt_source_manifest.json', 'photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json')}
    protected = {name: value for name, value in baseline.items() if name not in owned_derived}
    drift = [name for name, value in protected.items() if signature(ROOT / name) != value]
    applied = read(EVIDENCE / 'primary-application-receipt.json')['applied_files']
    applied_drift = [name for name in applied if sha(ROOT / name) != sha(WORKTREE / name)]
    owned_non_derived_drift = [name for name in applied_drift if name not in owned_derived]
    require(not owned_non_derived_drift, 'reviewed owned source/test/provenance bytes drift')
    require(not (set(drift) & set(applied)), 'protected drift overlaps owned changes')
    require(all((ROOT / name).is_file() and (ROOT / name).stat().st_size > 0 for name in drift), 'preexisting file missing/empty')
    application = read(EVIDENCE / 'primary-application-receipt.json')
    require(application['status'] == 'pass' and not application['protected_drift'], 'application-time preservation failed')
    current_checks = read(EVIDENCE / 'current-source-checks.json')
    require(current_checks['status'] == 'pass', 'current source checks failed')
    require(current_checks['source_binding_at_completion']['source_fingerprint'] == pointer['source_fingerprint'], 'current checks source binding drift')

    reference_sha = sha(REFERENCE)
    request_sha = sha(CAMPAIGN / 'shared-request.txt')
    cases = []
    freeze_revisions = {
        'case_a': '891c7297b2c841dbb5bcc59c1b9a3cb7',
        'case_b': '01fc939d63b945b9b22fe4bfd834fa07',
        'case_c': '356cdd2ed6df4fec8e640a56f057ff10',
    }
    for arm, frozen_revision in freeze_revisions.items():
        home = CAMPAIGN / arm
        summary = read(home / 'case-summary.json')
        source_binding = summary.get('source_binding') or summary['source']
        ledger = [json.loads(line) for line in (home / 'image_runs.ndjson').read_text().splitlines() if line.strip()]
        manifest = read(home / 'run_manifest.json')
        require(len(ledger) == 1, arm + ': expected one actual ledger row')
        row = ledger[0]
        require(row['image_call_count'] == manifest['image_call_count'] == 1, arm + ': call count mismatch')
        require(row.get('retry_of') is None, arm + ': unexpected retry')
        require(manifest['ledger_run_id'] == row['run_id'], arm + ': ledger binding mismatch')
        require(manifest['cross_arm_inputs_used'] is False, arm + ': cross-arm declaration invalid')
        require(manifest['skill_sha256'] == ready['canonical_skill_sha256'], arm + ': skill binding mismatch')
        require(source_binding['generation_id'] == expected['generation_id'], arm + ': generation binding mismatch')
        require(source_binding['source_fingerprint'] == expected['source_fingerprint'], arm + ': fingerprint binding mismatch')
        require(manifest['reference_sha256'] == row['reference_sha256'] == [reference_sha], arm + ': reference drift')
        for key in ('pack_id', 'authorial_core_sha256', 'intent_lock_sha256', 'runtime_prompt_sha256', 'effective_visual_contract_sha256', 'status', 'image_paths'):
            require(manifest[key] == row[key], arm + ': manifest mismatch ' + key)
        frozen = home / 'revisions' / frozen_revision
        freeze = read(frozen / 'freeze_receipt.json')
        require(freeze['contracts']['core'] == row['authorial_core_sha256'], arm + ': frozen core contract mismatch')
        require(freeze['contracts']['intent_lock'] == row['intent_lock_sha256'], arm + ': frozen intent mismatch')
        require(freeze['files']['request_raw'] == request_sha, arm + ': shared human request mismatch')
        for role in ('authorial_core_input', 'authorial_core_normalized', 'embodiment_review', 'feature_selection'):
            require(sha(frozen / (role + '.json')) == freeze['files'][role], arm + ': frozen file changed ' + role)
        composed = latest(arm, 'composed_audit.json')
        runtime = latest(arm, 'runtime_audit.json')
        for path in (composed, runtime):
            audit = read(path)
            require(audit['status'] == 'pass' and not audit['failures'], arm + ': pipeline audit failed ' + path.name)
            require(audit['effective_visual_contract_sha256'] == row['effective_visual_contract_sha256'], arm + ': audited visual contract drift')
        images = row.get('image_hashes', [])
        for image in images:
            require(sha(Path(image['path'])) == image['sha256'], arm + ': saved image hash mismatch')
        if row['status'] == 'success':
            require(len(images) == len(row['image_paths']) == 1, arm + ': expected one saved image')
            review = read(home / 'visual-review.json')
            require(review['result_sha256'] == images[0]['sha256'], arm + ': review image mismatch')
            audit_path = latest(arm, 'review_audit.json')
            visual_audit = read(audit_path)['visual']
            require(not visual_audit['schema_failures'], arm + ': invalid review record')
            require(visual_audit['effective_visual_contract_sha256'] == row['effective_visual_contract_sha256'], arm + ': review contract mismatch')
            counts = {status: sum(g['status'] == status for g in review['hard_gates'].values()) for status in ('pass', 'fail')}
            pixel = dict(required=len(review['hard_gates']), **counts, status=visual_audit['qualification_status'], representative_eligible=visual_audit['representative_eligible'])
        else:
            require(row['status'] == 'safety_block' and not row['image_paths'], arm + ': unexpected outcome')
            require(sha(Path(row['attempt_evidence_path'])) == row['attempt_evidence_sha256'], arm + ': blocked evidence drift')
            pixel = dict(required=summary['all_of_native_gates']['total'], assessed=0, not_run=summary['all_of_native_gates']['not_run'], status='NOT_RUN_NOT_PASS')
        cases.append(dict(arm_id=arm, ledger_rows=len(ledger), actual_calls=row['image_call_count'], native_status=row['status'],
                          run_id=row['run_id'], source_binding=source_binding, frozen_core_sha256=row['authorial_core_sha256'],
                          reference_sha256=reference_sha, images=images, pixel=pixel,
                          summary=str(home / 'case-summary.json'), composed_audit=str(composed), runtime_audit=str(runtime)))

    result = dict(schema_version='summer-fashion-delivery-integrity/v1', checked_at=datetime.now(timezone.utc).isoformat(),
                  status=('pass_with_observed_out_of_scope_advancement' if drift or pointer['generation_id'] != expected['generation_id'] else 'pass') if not failures else 'fail', failures=failures,
                  protected_files_checked=len(protected), protected_drift=drift, applied_files_checked=len(applied), applied_drift=applied_drift,
                  owned_non_derived_files_checked=len([name for name in applied if name not in owned_derived]), owned_non_derived_drift=owned_non_derived_drift,
                  preservation_scope='Application-time 9118-file preservation passed. Later out-of-scope changes remain untouched and are explicitly listed; this is not a claim that all concurrent bytes still equal the older baseline.',
                  application_time_receipt=str(EVIDENCE / 'primary-application-receipt.json'),
                  source_advancement=dict(frozen_campaign_generation_id=expected['generation_id'], frozen_campaign_source_fingerprint=expected['source_fingerprint'],
                                          current_generation_id=pointer['generation_id'], current_source_fingerprint=pointer['source_fingerprint'],
                                          initial_drift_evidence=str(EVIDENCE / 'final-delivery-initial-current-drift.json')),
                  current_source_checks=str(EVIDENCE / 'current-source-checks.json'),
                  generation_id=pointer['generation_id'], source_fingerprint=pointer['source_fingerprint'], cases=cases,
                  totals=dict(actual_calls=sum(c['actual_calls'] for c in cases), returned_images=sum(len(c['images']) for c in cases),
                              safety_blocked=sum(c['native_status'] == 'safety_block' for c in cases), retries=0),
                  boundary='Validates actual source, frozen inputs, audits, ledger and saved bytes; pixel truth is recorded separately by native inspection. User acceptance remains pending.')
    (EVIDENCE / 'final-delivery-integrity.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'failures', 'protected_files_checked', 'owned_non_derived_files_checked', 'owned_non_derived_drift', 'totals')}, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == '__main__':
    raise SystemExit(main())
