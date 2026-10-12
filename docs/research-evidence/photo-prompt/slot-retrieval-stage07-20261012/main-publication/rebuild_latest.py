"""Bind the late upstream food classification to a canonical current generation."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/.codex/worktrees/slot-retrieval-stage07-integration/image-prompt')
SKILL = ROOT/'skills/photo-prompt-image-generator'
PYTHON = Path('/Users/chasoik/Projects/image-prompt/.venv/bin/python')
sys.path.insert(0, str(SKILL/'scripts'))
import prompt_generator as g
from photo_runtime_sources import source_update, SnapshotPublisher


def save(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def main():
    old = json.loads((OUT/'REPAIRED-RUNTIME.json').read_text())
    store = OUT/'latest-runtime-store'
    command = [str(PYTHON), str(OUT/'rebuild_publish.py'), '--root', str(ROOT),
               '--phase', 'latest', '--external-update', '--no-publication', '--require-cached',
               '--visual-cache-index', str(SKILL/'assets/photo_prompt_visual_profile_index.json')]
    if '--resume-publication' not in sys.argv and '--verify-only' not in sys.argv:
        with source_update(SKILL, store):
            subprocess.run(command, cwd=ROOT, check=True)
    if '--verify-only' in sys.argv:
        pointer = json.loads((OUT/'LATEST-PUBLICATION.json').read_text())
    else:
        pointer = SnapshotPublisher(SKILL, store).publish()
        save('LATEST-PUBLICATION.json', pointer)
        subprocess.run([str(PYTHON), str(SKILL/'scripts/publish_photo_runtime_snapshot.py'),
                        '--source-root', str(SKILL), '--complete-update'], cwd=ROOT, check=True,
                       stdout=subprocess.DEVNULL)
    root = store/'generations'/pointer['generation_id']
    manifest = json.loads((root/'manifest.json').read_text())
    meta = dict(generation_id=pointer['generation_id'], source_fingerprint=pointer['source_fingerprint'],
                store=str(store), sealed_root=str(root), code_sha256=old['code_sha256'])
    save('LATEST-RUNTIME.json', meta)
    indexes = []
    for filename in ('photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json'):
        load = g.load_semantic_index_payload if filename == 'photo_prompt_semantic_index.json' else g.load_visual_profile_index_payload
        before = load(Path(old['sealed_root'])/'assets'/filename)
        after = load(root/'assets'/filename)
        assert before['entries'] == after['entries'], filename
        for key in ('bm25f', 'entry_order', 'provider', 'semantic_text_recipe', 'embedding_model', 'embedding_dimensions'):
            assert before.get(key) == after.get(key), (filename, key)
        indexes.append(dict(index=filename, entries=len(after['entries']),
                            positive_documents_vectors_and_query_metadata_identical=True))
    for path in (Path(old['sealed_root'])/'scripts').rglob('*'):
        if path.is_file() and path.suffix == '.py':
            assert path.read_bytes() == (root/'scripts'/path.relative_to(Path(old['sealed_root'])/'scripts')).read_bytes(), path.name
    save('LATEST-RETRIEVAL-INVARIANCE.json', dict(previous=old, current=meta, indexes=indexes,
        all_python_script_bytes_identical=True, source_change='fire_f116 coarse subject category object -> food',
        embedding_api_calls=0, exact_sweep_reused=40380))
    print(json.dumps(meta), flush=True)


if __name__ == '__main__':
    main()
