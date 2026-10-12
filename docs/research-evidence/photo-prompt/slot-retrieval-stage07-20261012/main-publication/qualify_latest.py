"""Close the additional upstream delta without relabeling historical CLI evidence."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/.codex/worktrees/slot-retrieval-stage07-integration/image-prompt')
REL = 'docs/research-evidence/photo-prompt/slot-retrieval-stage07-20261012/main-publication'
ASSETS = 'skills/photo-prompt-image-generator/assets'


def read(name):
    return json.loads((OUT/name).read_text())


def save(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    meta = read('LATEST-RUNTIME.json')
    cases = [row for i in range(4) for row in read('LATEST-API-CASES-'+str(i)+'.json')['cases']]
    assert len(cases) == len({r['case'] for r in cases}) == 40
    assert all(r['generation_id'] == meta['generation_id'] and not r['source_recomputation_errors']
               and r['candidate_payloads_core_controls_negative_and_bundles_unchanged']
               and r['omission_detected'] for r in cases)
    smoke = read('LATEST-PUBLIC-CLI-SMOKE.json')
    assert smoke['cli_exit'] == smoke['view_exit'] == 0 and smoke['actual_receipt_verified']
    assert smoke['generation_id'] == meta['generation_id'] and not smoke['source_recomputation_errors']
    api_file = OUT/'latest-api-natural/dev-02-blue-cup-en/candidate-pack.json'
    public_file = OUT/'latest-public-cli/dev-02-blue-cup-en/candidate-pack.json'
    assert json.loads(api_file.read_text()) == json.loads(public_file.read_text())
    save('LATEST-PUBLIC-API-PARITY.json', dict(case=smoke['case'], pack_objects_identical=True,
        api_sha256=hashlib.sha256(api_file.read_bytes()).hexdigest(),
        public_sha256=hashlib.sha256(public_file.read_bytes()).hexdigest(),
        observation='The earlier public smoke ran before its API case file existed; compare both saved actual outputs now.'))
    audits = read('LATEST-COMPOSITION-VALIDATION.json')
    assert len(audits) == 9 and all(r['actual_receipt_verified'] and r['generation_id'] == meta['generation_id']
        and r['composed_audit']['status'] == r['runtime_audit']['status'] == 'pass'
        and not r['embodiment_failures'] for r in audits)
    old = {(r['case'], r['variant']): r for r in read('REPAIRED-COMPOSITION-ALL-INPUTS.json')['cases']}
    authored = read('LATEST-COMPOSITION-ALL-INPUTS.json')['cases']
    assert len(authored) == 48
    for row in authored:
        now = json.loads(Path(row['inputs']['composed']['path']).read_text())
        before = json.loads(Path(old[(row['case'], row['variant'])]['inputs']['composed']['path']).read_text())
        for key in ('prompt_en', 'negative_en', 'chosen_candidate_ids'):
            assert now[key] == before[key], (row['case'], key)
    selectors = set()
    for lane in ('merge-focused', 'repaired-animal-context', 'repaired-bird-negative-recheck', 'latest-food-context'):
        selectors.update(re.findall(r'\((tests\.[^)]+)\)', (OUT/(lane+'-tests.log')).read_text()))
    assert read('latest-food-context-tests.json')['successful']
    inventory = read('latest-inventory/inventory.json')
    for key in ('duplicate_source_ids', 'raw_not_loaded', 'loaded_not_raw', 'source_labels_changed',
                'lexical_missing', 'lexical_extra', 'semantic_missing', 'semantic_extra'):
        assert not inventory[key], key
    assert inventory['raw_count'] == inventory['loaded_count'] == 11977
    upstream = '747f1da4751f7498e85c6cd3213ee772ce3cd59d'
    remote_preserved = [ASSETS+'/photo_prompt_tags.json', 'tests/test_photo_food_carrier_retrieval.py',
                        'tests/test_photo_subject_context_retrieval.py']
    for name in remote_preserved:
        assert (ROOT/name).read_bytes() == git('show', upstream+':'+name), name
    tags = json.loads((ROOT/ASSETS/'photo_prompt_tags.json').read_text())
    previous_tags = json.loads(git('show', '1ce59a91ec8b74d6f0e997fb9d1c7af8ca0902ca:'+ASSETS+'/photo_prompt_tags.json'))
    # Exactly the one upstream coarse category addition; the authored corpus is unchanged.
    assert tags['slot_applicability']['subject_category_overrides'].pop('fire_f116') == 'food'
    assert tags == previous_tags
    result = dict(runtime=meta, latest_upstream=upstream, upstream_delta_files_preserved=remote_preserved,
        current_production_api_cases=40, current_source_recomputation_errors=0,
        current_candidate_omission_checks=40, current_public_cli_and_view_smokes=1,
        earlier_public_cli_and_view_cases=40, earlier_cli_generation=read('REPAIRED-RUNTIME.json')['generation_id'],
        current_full_composed_runtime_audits=9, all_current_critical_audits_pass=True,
        final_prose_negative_and_choices_unchanged=48, native_positive_hits=10, native_false_hits=0,
        required_target_exposures=13, adoption_eligible_targets=12,
        emitted_candidate_payloads_core_controls_negative_bundles_and_subject_meaning_unchanged=True,
        expected_eligibility_pool_metadata_changes=[dict(case=r['case'], **r['eligible_subject_count_change'])
            for r in cases if r.get('eligible_subject_count_change')],
        focused_tests_unique=len(selectors), latest_delta_tests_pass=19, all_latest_selectors_pass=True,
        inventory=dict(slots=inventory['slot_count'], candidates=inventory['loaded_count'], errors=0,
                       semantic_non_slot_documents=inventory['semantic_non_slot_documents']),
        exact=read('FINAL-MERGE-VALIDATION.json')['exact'], exact_reuse=read('LATEST-RETRIEVAL-INVARIANCE.json'),
        embedding_api_calls=0, image_calls=0, whole_suite='Not rerun.',
        proof_boundary='40 final API packs and source audits, 9 final receipt-bound composed/runtime audits, 1 final real CLI/view, plus unchanged CLI code and 40 earlier CLI/view cases. No claim of 40 final CLI replays or 48 final full audits.')
    save('LATEST-VALIDATION.json', result)
    manifest_name = ASSETS+'/photo_prompt_semantic_index.json'
    manifest = json.loads((ROOT/manifest_name).read_text())
    active = []
    for row in manifest['shards']:
        name = ASSETS+'/'+row['path']
        raw = (ROOT/name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row['sha256'], name
        active.append(dict(path=name, sha256=row['sha256'], size=len(raw)))
    save('LATEST-MERGE-INTENT.json', dict(integrated_commits=[
        '47d535d12ab80f1ae99c2f443af3f2846a891b6e',
        '0b33ae2c18a26060b918436c38d6d77eb2385306', upstream],
        first_merge='1ce59a91ec8b74d6f0e997fb9d1c7af8ca0902ca',
        second_merge=git('rev-parse', 'HEAD').decode().strip(),
        active_semantic_shards=active, runtime=meta,
        latest_upstream_source_and_tests_preserved=True,
        previous_three_animal_source_prerequisites_retained=True))
    files = ['LATEST-VALIDATION.json', 'LATEST-MERGE-INTENT.json', 'LATEST-RUNTIME.json',
        'LATEST-PUBLICATION.json', 'LATEST-RETRIEVAL-INVARIANCE.json', 'LATEST-PUBLIC-CLI-SMOKE.json', 'LATEST-PUBLIC-API-PARITY.json',
        'LATEST-COMPOSITION-VALIDATION.json', 'LATEST-COMPOSITION-INPUTS.json',
        'LATEST-COMPOSITION-ALL-INPUTS.json', 'latest-food-context-tests.json', 'latest-food-context-tests.log',
        'latest-index-summary.json', 'latest-semantic-build.log', 'latest-dictionary.log', 'latest-visual-check.log',
        'latest-visual-vector-preflight.json', 'latest-inventory/runtime-acquisition.json',
        'rebuild_latest.py', 'replay_latest_worker.py', 'verify_latest_compositions.py',
        'latest_public_smoke.py', 'qualify_latest.py', 'LATEST-SOURCE-INTENT-PREFLIGHT.json'] + ['LATEST-API-CASES-'+str(i)+'.json' for i in range(4)]
    previous_report = (OUT/'REPORT.md').read_text()
    paragraph = '''
## 검증 도중 추가된 최신 main 반영

추가 원격 커밋 `747f1da4751f7498e85c6cd3213ee772ce3cd59d`의 누룽지 food 분류와 음식·용기 경계 테스트를 그대로 통합했다. 최종 generation은 `43dac5d6856375e2495bdb38463cb3d54e8749592e69344c2e5666ea6d4be64a`다. 112개 슬롯의 source·loader·lexical/semantic index 11,977개 ID 및 라벨 불일치가 0이다.

최종 generation에서 production API pack 40개와 source 재계산·누락 변조 검사를 반복했다. 실제로 반환된 후보 객체·주체 의미·core·controls·negative·bundle은 이전 검증본과 동일하다. 일부 object 장면의 candidate_count만 food로 옮긴 누룽지 원본 1개만큼 감소했으며 이를 별도로 기록했다. 실제 공개 CLI·view 1건과 최종 receipt를 사용한 composed/runtime 감사 9건도 통과했다. 이전 공개 CLI·view 40건은 이전 generation 증거로 보존하며 최종 generation의 CLI 40건을 반복했다는 뜻은 아니다. 프롬프트·negative·선택 ID 48건은 계속 동일하다.

최신 변경의 음식·용기·동물 테스트 19건이 통과해 관련 고유 selector 총 62개의 마지막 실행이 통과했다. positive 검색 문서·벡터·metadata·Python 코드는 그대로라 exact 전수 결과를 재사용했다. 새 임베딩 및 이미지 호출은 없다. main FF·푸시·원본 작업 보존의 최종 결과는 DELIVERY 기록에서 확인한다.
'''
    if '## 검증 도중 추가된 최신 main 반영' not in previous_report:
        (OUT/'REPORT.md').write_text(previous_report+paragraph)
    files.append('REPORT.md')
    staged_files = []
    for filename in files:
        source = OUT/filename
        target = ROOT/REL/filename
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix == '.log':
            target.write_text('\n'.join(line.rstrip() for line in source.read_text().splitlines())+'\n')
        else:
            shutil.copy2(source, target)
        staged_files.append(REL+'/'+filename)
    paths = [manifest_name, *[r['path'] for r in active], *staged_files]
    subprocess.run(['git', 'add', '--', *paths], cwd=ROOT, check=True)
    subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, check=True)
    assert not git('ls-files', '-u').strip()
    assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(paths)
    print(json.dumps(dict(production_api_cases=40, final_full_audits=9, focused_tests_unique=len(selectors),
                         candidates=inventory['loaded_count'], active_shards=len(active),
                         eligibility_count_changes=len(result['expected_eligibility_pool_metadata_changes']))))


if __name__ == '__main__':
    main()
