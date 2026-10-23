"""Verify recorded artifacts; pixel judgments remain separately authored observations."""
from pathlib import Path
import hashlib, json, struct, zlib

O = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/Projects/image-prompt')
PIN = '265a75945bda1a1aea3b26ca88e13ab0dcb3139d22ae85197ed2d478ee3f2978'
REFERENCE = Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
REF_SHA = '06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7'
SKILL_SHA = 'f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089'

def read(p): return json.loads(Path(p).read_bytes())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def textsha(s): return hashlib.sha256(s.encode()).hexdigest()
def png(p):
    b = Path(p).read_bytes()
    assert b[:8] == b'\x89PNG\r\n\x1a\n'
    i = 8; dims = None; last = None; chunks = 0
    while i < len(b):
        size = struct.unpack('>I', b[i:i+4])[0]
        kind = b[i+4:i+8]; content = b[i+8:i+8+size]
        assert zlib.crc32(kind+content) & 0xffffffff == struct.unpack('>I', b[i+8+size:i+12+size])[0]
        if kind == b'IHDR': dims = list(struct.unpack('>II', content[:8]))
        last = kind; i += 12+size; chunks += 1
    assert i == len(b) and last == b'IEND' and dims
    return dict(dimensions=dims, chunks=chunks, all_chunk_crc_valid=True)

assert sha(REFERENCE) == REF_SHA
assert sha(ROOT/'skills/photo-prompt-image-generator/SKILL.md') == SKILL_SHA
new_cids = set(read(O/'new-native-records.json'))
freezes = read(O/'pre-data-arm-freezes.json')
rows = []
(O/'prompts').mkdir(exist_ok=True)
for freeze in freezes:
    arm = freeze['arm']; p = Path(freeze['run']); w = read(p/'workflow.json')
    assert w['phase'] == 'review_record_validated'
    assert w['h_f2_binding']['generation_id'] == PIN
    bindings = w['artifacts']
    for name, entry in bindings.items():
        assert sha(entry['path']) == entry['sha256'], (arm, name)
    assert sha(bindings['authorial_core_normalized']['path']) == freeze['core_file_sha256']
    assert sha(bindings['baseline']['path']) == freeze['baseline_file_sha256']
    co = read(bindings['composed']['path']); rr = read(bindings['render_request']['path'])
    plan = read(bindings['native_plan']['path']); mat = read(bindings['h_f2_material']['path'])
    audit = read(bindings['review_audit']['path'])['visual']
    assert audit['technical_qualified'] is True and audit['failed_hard_gates'] == [] and audit['schema_failures'] == []
    assert audit['required_hard_gate_count'] == 5 and audit['user_judgment']['genuinely_moe'] == 'pending'
    assert co['chosen_candidate_ids'] == co['chosen_visual_concept_ids'] == []
    assert mat['native_approval'] is False
    assert set(mat['sources']).isdisjoint(new_cids)
    assert all(d['use'] == 'skip' for d in co['h_f2_material_decisions'])
    ledger = [json.loads(line) for line in (p/'image_runs.ndjson').read_text().splitlines() if line.strip()]
    assert len(ledger) == 1
    l = ledger[0]
    assert l['status'] == 'success' and l['image_call_count'] == 1 and l['attempt'] == 1 and l['retry_of'] is None
    assert l['reference_sha256'] == [REF_SHA]
    assert l['chosen_candidate_ids'] == l['chosen_visual_concept_ids'] == []
    prompt = l['prompt_en']
    assert prompt == co['prompt_en'] == rr['runtime_prompt_en'] == plan['payload']['prompt']
    assert textsha(prompt) == l['runtime_prompt_sha256']
    assert plan['payload']['referenced_image_paths'] == [str(REFERENCE)]
    assert rr['referenced_image_paths'] == [str(REFERENCE)]
    assert plan['payload']['transparent_background'] is False
    images = l['image_hashes']; assert len(images) == 1
    image = Path(images[0]['path']); assert sha(image) == images[0]['sha256']
    obs = read(O/'parent-pixel-reviews'/f'{arm}.json')
    image_meta = png(image)
    assert obs['image_sha256'] == sha(image) and obs['dimensions'] == image_meta['dimensions']
    manifest_bound = 0
    extra = p/'artifact-file-manifest.json'
    if extra.exists():
        for x in read(extra)['files']:
            assert sha(x['path']) == x['file_sha256'], (arm, x['path'])
            manifest_bound += 1
    # Preserve actual runtime text byte-for-byte as a convenient prompt artifact.
    out = O/'prompts'/f'{arm}.txt'; out.write_bytes(prompt.encode())
    rows.append(dict(arm=arm, run=str(p), workflow_phase=w['phase'], workflow_bound_files=len(bindings),
        additional_manifest_bound_files=manifest_bound, core_and_baseline_predata_hashes_unchanged=True,
        prompt=str(out), prompt_sha256=textsha(prompt), reference_sha256=REF_SHA,
        image=str(image), image_sha256=sha(image), **image_meta, actual_calls=1, retries=0,
        observed_model=None, requested_model=w['transport']['model'], ledger_run_id=l['run_id'],
        h_f2_generation_id=PIN, native_chosen_arrays=[[],[]], native_approval=False,
        natural_new_module_exposure_count=0, generic_hard_gates_passed=5,
        source_card=obs['source_card'], source_gate_count=len(obs['gates']),
        source_gates_passed=sum(g['pass'] for g in obs['gates']),
        source_verdict=obs['complete_source_verdict'],
        complete_authored_scene='NOT_FULLY_QUALIFIED' if arm=='A' else 'FAIL' if arm=='B' else 'PARTIAL_NOT_PASS',
        full_historical_ensemble='NOT_ESTABLISHED', user_acceptance='pending',
        independence_limit='Earlier-arm summaries unintentionally exposed after predata core/baseline/slot freeze; no full postcore nonexposure claim.' if arm=='B' else None))
result = dict(schema='court-r2-image-evidence-verification/v1', status='pass', arms=rows,
    total_actual_calls=3, total_retries=0, source_structure_passed=2, source_structure_total=3,
    complete_authored_scene_passed=0, generic_structure_passed=3,
    natural_new_module_exposure_arms=0, total_arms=3, paired_before_after=False,
    boundary='File/hash/audit consistency is verified here. Pixel observations are separately recorded by the agents and parent; user acceptance and historical authenticity are not inferred.')
(O/'image-evidence-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='arms'},ensure_ascii=False))
