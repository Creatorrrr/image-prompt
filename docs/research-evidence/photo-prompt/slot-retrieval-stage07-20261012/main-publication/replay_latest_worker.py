"""Recreate all frozen cases through the production pack API and real runtime receipts."""
import copy
import json
from pathlib import Path
import shutil
import sys

OUT = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/.codex/worktrees/slot-retrieval-stage07-integration/image-prompt')
sys.path.insert(0, str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as g
import audit_composed_prompt as audit
from photo_runtime_sources import RuntimeSnapshotProvider

meta = json.loads((OUT/'LATEST-RUNTIME.json').read_text())
provider = RuntimeSnapshotProvider(ROOT/'skills/photo-prompt-image-generator', Path(meta['store']))
snapshot = provider.acquire()
assert snapshot.generation_id == meta['generation_id']
shard = int(sys.argv[1])
checkpoint = OUT/('LATEST-API-CASES-'+str(shard)+'.json')
results = json.loads(checkpoint.read_text())['cases'] if checkpoint.exists() else []
assert all(r['generation_id'] == snapshot.generation_id for r in results)
completed = {r['case'] for r in results}
ordinal = 0
for old_lane, lane in [('repaired-public-natural', 'latest-api-natural'),
                       ('repaired-public-native', 'latest-api-native')]:
    for path in sorted((OUT/old_lane).glob('*/candidate-pack.json')):
        take = ordinal % 4 == shard
        ordinal += 1
        if not take:
            continue
        if path.parent.name in completed:
            saved = OUT/lane/path.parent.name/'candidate-pack.json'
            assert saved.exists() and Path(str(saved)+'.runtime-receipt.json').exists()
            continue
        previous = json.loads(path.read_text())[0]
        folder = OUT/lane/path.parent.name
        folder.mkdir(parents=True, exist_ok=True)
        argv = json.loads((path.parent/'generate-command.json').read_text())
        options = {argv[i]: argv[i+1] for i in range(len(argv)-1) if argv[i].startswith('--')
                   and not argv[i+1].startswith('--')}
        for filename in ('request-envelope.json', 'authorial-core.json', 'creative-controls.json', 'embodiment-review.json'):
            shutil.copy2(path.parent/filename, folder/filename)
        embodiment = json.loads(Path(options['--embodiment-review-json']).read_text())
        visual = g.load_visual_intent_arg(options.get('--visual-intent-json'),
            snapshot.data[g.VISUAL_OBLIGATIONS_DATA_KEY], snapshot.data[g.VISUAL_PROFILE_INDEX_DATA_KEY])
        pack = g.generate_candidate_pack(snapshot.data, previous['authorial_core'], previous['creative_controls'],
                                        embodiment, seed=int(options['--seed']), visual_intent=visual)
        (folder/'candidate-pack-diagnostic.json').write_text(json.dumps([pack], ensure_ascii=False, indent=2)+'\n')
        if pack['slots'] != previous['slots']:
            changed_slots = [s for s in set(pack['slots']) | set(previous['slots']) if pack['slots'].get(s) != previous['slots'].get(s)]
            (folder/'DIFFERENCE.json').write_text(json.dumps(dict(changed_slots=changed_slots,
                old={s: previous['slots'].get(s) for s in changed_slots},
                new={s: pack['slots'].get(s) for s in changed_slots}), ensure_ascii=False, indent=2)+'\n')
        comparable_new = copy.deepcopy(pack['slots'])
        comparable_old = copy.deepcopy(previous['slots'])
        count_change = None
        if 'subject' in comparable_new and 'subject' in comparable_old:
            old_count = comparable_old['subject'].pop('candidate_count')
            new_count = comparable_new['subject'].pop('candidate_count')
            if old_count != new_count:
                assert g.frozen_core_context(snapshot.data, pack['authorial_core'], pack['creative_controls'])[0]['subject_category'] == 'object'
                assert new_count == old_count - 1
                count_change = dict(old=old_count, new=new_count,
                    reason='fire_f116 is now food, so the object subject eligibility pool has one fewer source row; emitted candidate objects are unchanged.')
        assert comparable_new == comparable_old, (path.parent.name, 'emitted ordinary candidate payload changed')
        for key in ('authorial_core', 'creative_controls', 'negative_en', 'visual_concept_candidates',
                    'semantic_assertion_obligations', 'embodiment_preflight', 'candidate_bundles'):
            assert pack[key] == previous[key], (path.parent.name, key)
        target = folder/'candidate-pack.json'
        target.write_text(json.dumps([pack], ensure_ascii=False, indent=2)+'\n')
        receipt = provider.receipt(snapshot, pack)
        Path(str(target)+'.runtime-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
        assert not audit.audit_core_retrieval(pack, snapshot.data), path.parent.name
        damaged = copy.deepcopy(pack)
        slot = next(iter(damaged['slots']))
        damaged['slots'][slot]['candidates'].pop()
        assert audit.audit_core_retrieval(damaged, snapshot.data), path.parent.name
        results.append(dict(case=path.parent.name, lane=lane, generation_id=snapshot.generation_id,
                            production_pack_api=True, receipt_written=True, source_recomputation_errors=[],
                            candidate_payloads_core_controls_negative_and_bundles_unchanged=True,
                            eligible_subject_count_change=count_change, omission_detected=True))
        (OUT/('LATEST-API-CASES-'+str(shard)+'.json')).write_text(json.dumps(dict(cases=results,
            generation_id=snapshot.generation_id, execution='Production generate_candidate_pack on a verified snapshot; actual production receipt; source recomputation; no mocks. This lane is the API, not the CLI argument parser.'),
            ensure_ascii=False, indent=2)+'\n')
        print(json.dumps(dict(case=path.parent.name, api='pass', payload_unchanged=True)), flush=True)
assert len(results) == 10
