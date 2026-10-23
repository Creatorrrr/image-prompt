"""Same frozen full-pool probes, one immutable generation per process.

Orchestration only: no kernel, query, vector, source or ranking changes.
"""
from pathlib import Path
import argparse, collections, gc, hashlib, json, sys
gc.disable()
O = Path(__file__).resolve().parent


def read(p):
    return json.loads(p.read_bytes())


def write(p, value):
    tmp = p.with_suffix(p.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(p)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['after', 'before', 'summary'])
    phase = parser.parse_args().phase
    B, S, I = (read(O / n) for n in ('before.json', 'successor.json', 'install.json'))
    assert I['status'] == 'pass'
    cases = read(O / 'frozen-query-cases.json')
    encoded = read(O / 'query-embeddings.json')
    assert [(r['id'], r['query']) for r in cases] == [(r['id'], r['query']) for r in encoded['rows']]
    frozen_sha = hashlib.sha256((O / 'frozen-query-cases.json').read_bytes()).hexdigest()
    assert encoded['case_sha256'] == frozen_sha
    registry = read(O.parent / 'data-integration.json')
    lookup = {r['card_id']: r['candidate_id'] for r in registry['adoptions'] if r['decision'] in ('new', 'reuse')}
    fresh = read(O / 'new-native-records.json')
    new_visual = {cid for cid, r in fresh.items() if r['record_kind'] == 'visual_option'}
    diagnostics = set(fresh) - new_visual
    checkpoint = O / ('probe-' + phase + '.json')
    if phase != 'summary':
        store = Path(I['store']) if phase == 'after' else Path(B['store'])
        gid = S['generation_id'] if phase == 'after' else B['config']['generation_id']
        sys.path.insert(0, str(Path(I['store']) / 'generations' / S['native_generation_id'] / 'scripts'))
        from photo_h_f2_generation import Generation
        import photo_canonical_source as canonical
        print('loading', phase, gid, flush=True)
        generation = Generation(store, gid, full=True)
        assert generation.binding == encoded['binding']
        print('sealed generation verified', phase, flush=True)
        if phase == 'after':
            assert diagnostics.isdisjoint({r['cid'] for r in generation.metadata})
            for cid in sorted(new_visual):
                assert canonical.native_snapshot(generation.body.record(cid)) == fresh[cid]
            print('72 visual source snapshots exact; 35 diagnostics excluded', flush=True)
        index = generation.index()
        print('unchanged production full-pool index initialized', phase, flush=True)
        state = read(checkpoint) if checkpoint.exists() else {
            'generation_id': gid, 'frozen_query_sha256': frozen_sha,
            'production_kernel': S['native_generation_id'], 'rows': []}
        assert state['generation_id'] == gid and state['frozen_query_sha256'] == frozen_sha
        assert state['production_kernel'] == S['native_generation_id']
        done = {r['id'] for r in state['rows']}
        for row, ev in zip(cases, encoded['rows'], strict=True):
            if row['id'] in done or (phase == 'before' and row['cohort'] in ('development', 'new_scene_phrasing')):
                continue
            result = index.search(row['query'], ev['embedding'], generation.binding)
            assert result['lane_calls'] == {'BM25F': 1, 'local_cosine': 1}
            out = {'id': row['id'], 'top8': result['order'][:8]}
            if phase == 'after':
                targets = {lookup[k] for k in row['expected_cards'] if k in lookup}
                out.update({
                    'rank': next((i + 1 for i, r in enumerate(result['order']) if r['cid'] in targets), None),
                    'registered_expected_CIDs': sorted(targets),
                    'population': result['considered_CIDs'], 'query_scope': result['query_scope'],
                    'new_at8': [r['cid'] for r in result['order'][:8] if r['cid'] in new_visual]})
            state['rows'].append(out)
            if len(state['rows']) % 16 == 0:
                write(checkpoint, state)
                print('searched', phase, len(state['rows']), flush=True)
        state['complete'] = True
        state['population'] = generation.manifest['CID_count']
        write(checkpoint, state)
        print('complete', phase, len(state['rows']), flush=True)
        return
    after, before = read(O / 'probe-after.json'), read(O / 'probe-before.json')
    assert after['complete'] and before['complete']
    assert after['frozen_query_sha256'] == before['frozen_query_sha256'] == frozen_sha
    arows, brows = ({r['id']: r for r in state['rows']} for state in (after, before))
    assert len(arows) == len(cases) == 326
    results = []
    for row in cases:
        a = arows[row['id']]
        out = {**row, 'registered_expected_CIDs': a['registered_expected_CIDs'],
               'after': {k: a[k] for k in ('rank', 'top8', 'population', 'query_scope')},
               'new_at8': a['new_at8'],
               'route': 'full_pool_probe_before_managed_random_sampling; no slot or adoption approval'}
        if row['id'] in brows:
            b = brows[row['id']]
            out['before_top8'] = b['top8']
            out['old_top8_overlap'] = len({r['cid'] for r in b['top8']} & {r['cid'] for r in a['top8']})
        results.append(out)
    groups = {}
    for cohort in sorted({r['cohort'] for r in results}):
        rows = [r for r in results if r['cohort'] == cohort]
        graded = [r for r in rows if r['registered_expected_CIDs']]
        groups[cohort] = {
            'queries': len(rows), 'registered_targets': len(graded),
            'target_at8': sum(r['after']['rank'] is not None and r['after']['rank'] <= 8 for r in graded),
            'target_at32': sum(r['after']['rank'] is not None and r['after']['rank'] <= 32 for r in graded),
            'new_sources_at8': sum(bool(r['new_at8']) for r in rows)}
    summary = {
        'status': 'source_and_retrieval_probes_complete', 'queries': len(results),
        'before_control_queries': len(brows), 'groups': groups,
        'new_CIDs_exact_at_install': len(fresh), 'runtime_visual_sources_exact': len(new_visual),
        'diagnostics_excluded_from_positive_search': len(diagnostics),
        'before_positive_CIDs': before['population'], 'after_positive_CIDs': after['population'],
        'native_approval': False, 'pixel_status': 'SEPARATE',
        'execution': 'one generation per process; identical frozen cases, vectors and production kernel',
        'limits': 'Source-derived development and reviewed new phrasing, not blind holdout. Rank/exposure does not prove source compatibility, native adoption or causal image improvement.'}
    write(O / 'retrieval-qualification.json', {'summary': summary, 'cases': results})
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
