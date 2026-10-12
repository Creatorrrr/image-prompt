"""Prove the source-only evidence amendment preserves retrieval inputs."""
import hashlib
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/.codex/worktrees/slot-retrieval-stage07-integration/image-prompt')
sys.path.insert(0, str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as g


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def indexes(root, name):
    assets = root/'assets'
    meta = json.loads((assets/name).read_text())
    entries = {}
    shards = []
    for row in meta['shards']:
        path = assets/row['path']
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == row['sha256'], path
        payload = json.loads(path.read_text())['entries']
        assert not (entries.keys() & payload.keys()), path
        entries.update(payload)
        shards.append(dict(path=row['path'], sha256=actual, size=path.stat().st_size))
    assert len(entries) == meta['entry_count']
    return meta, entries, shards


def main():
    old = json.loads((OUT/'runtime-acquisition.json').read_text())
    new = json.loads((OUT/'QUALIFIED-RUNTIME.json').read_text())
    before, after = (Path(row['sealed_root']) for row in (old, new))
    a, b = (g.load_runtime_data(root/'assets/photo_prompt_tags.json') for root in (before, after))
    code_a = {str(p.relative_to(before)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (before/'scripts').rglob('*.py')}
    code_b = {str(p.relative_to(after)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (after/'scripts').rglob('*.py')}
    assert code_a == code_b
    assert a['slots'] == b['slots']
    index_results = {}
    active = []
    for name in ('photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json'):
        ma, ea, sa = indexes(before, name)
        mb, eb, sb = indexes(after, name)
        differences = sorted(k for k in ea.keys() | eb.keys() if ea.get(k) != eb.get(k))
        assert not differences, (name, differences)
        for key in ('provider', 'semantic_text_recipe', 'embedding_model', 'embedding_dimensions'):
            assert ma.get(key) == mb.get(key), key
        # Only fingerprint metadata may change; BM25F documents themselves are in entries.
        index_results[name] = dict(entries=len(eb), entries_identical=True,
            entries_sha256=digest(eb), changed_entry_ids=differences,
            embedding_identity={k:mb.get(k) for k in ('provider','semantic_text_recipe','embedding_model','embedding_dimensions')},
            old_shards=sa, new_shards=sb)
        for key in ('bm25f', 'exact_lookup', 'retrieval_policy', 'entry_order'):
            assert ma.get(key) == mb.get(key), (name, key)
            index_results[name][key+'_identical'] = True
        active.extend(dict(index=name, **row) for row in sb)
    raw = [json.loads((r/'assets/photo_prompt_visual_obligations.json').read_text()) for r in (before, after)]
    profiles = [{p['id']:p for p in row['profiles']} for row in raw]
    changed = sorted(k for k in profiles[0] if profiles[0][k] != profiles[1][k])
    assert changed == ['golem_constructed_material_agency']
    for key in profiles[0]:
        assert g.visual_profile_semantic_text(profiles[0][key]) == g.visual_profile_semantic_text(profiles[1][key])
        assert g.visual_profile_bm25f_fields(profiles[0][key]) == g.visual_profile_bm25f_fields(profiles[1][key])
    result = dict(baseline_generation=old['generation_id'], qualified_generation=new['generation_id'],
        old_source_fingerprint=old['source_fingerprint'], new_source_fingerprint=new['source_fingerprint'],
        all_script_bytes_identical=True, script_files=len(code_a), code_binding=new['code_sha256'],
        slot_corpus_identical=True, slot_corpus_sha256=digest(b['slots']), slots=len(b['slots']),
        ordinary_candidates=sum(len(rows) for rows in b['slots'].values()),
        source_manifest_identical=(before/'assets/photo_prompt_source_manifest.json').read_bytes()==(after/'assets/photo_prompt_source_manifest.json').read_bytes(),
        changed_profile_ids=changed, all_main_profile_positive_text_and_bm25f_fields_identical=True,
        indexes=index_results, active_shards=active,
        exact_and_role_probe_reuse='Same complete ordinary corpus, queries, index documents, ranker and code. Baseline full exact sweep and source-derived route probe results remain valid; qualified public packs and compositions are separately rerun.',
        embedding_api_calls=0, image_calls=0)
    (OUT/'RETRIEVAL-INVARIANCE.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('slots','ordinary_candidates','slot_corpus_identical','all_script_bytes_identical','changed_profile_ids')}))


if __name__ == '__main__':
    main()
