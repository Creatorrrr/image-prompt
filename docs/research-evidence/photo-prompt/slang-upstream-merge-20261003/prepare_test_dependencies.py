"""Copy existing ignored frozen test artifacts by exact SHA, without regenerating."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ORIGINAL = Path('/Users/chasoik/Projects/image-prompt')


def main():
    receipt_path = HERE / 'IGNORED-TEST-DEPENDENCIES.json'
    previous = json.loads(receipt_path.read_text())
    files = {row['path']: row for row in previous['files']}
    missing_sources = []

    def copy(name, expected=None):
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or not str(path).startswith(('artifacts/photo-runs/', 'generated_images/')):
            return
        source, target = ORIGINAL / path, ROOT / path
        if target.exists():
            return
        if not source.is_file():
            missing_sources.append(str(path))
            return
        raw = source.read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        if expected is not None:
            assert actual == expected, path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        files[str(path)] = {'path': str(path), 'sha256': actual, 'bytes': len(raw),
                            'copied_from_existing_hash_bound_local_artifact': expected is not None,
                            'existing_local_source_bytes_preserved': True}

    def visit(node):
        if isinstance(node, list):
            for child in node:
                visit(child)
        elif isinstance(node, dict):
            for key, value in node.items():
                if key.endswith('_path') and isinstance(value, str):
                    prefix = key[:-5]
                    expected = node.get(prefix + '_file_sha256') or node.get(prefix + '_sha256')
                    if isinstance(expected, str) and len(expected) == 64:
                        copy(value, expected)
                elif isinstance(value, (dict, list)):
                    visit(value)

    for fixture in (ROOT / 'tests/fixtures/photo_prompt').glob('*.jsonl'):
        for line in fixture.read_text().splitlines():
            if line.strip():
                visit(json.loads(line))
    makeup = Path('artifacts/photo-runs/20260831-makeup-reference-five-arm-v1')
    copy(str(makeup / 'shared/source_observation.json'))
    for source in sorted((ORIGINAL / makeup / 'arms').glob('arm-*/authorial_core.json')):
        copy(str(source.relative_to(ORIGINAL)))
    assert len(list((ROOT / makeup / 'arms').glob('arm-*/authorial_core.json'))) == 5
    result = {'reason': 'Fresh worktree omitted ignored historical artifacts required by unchanged frozen tests. Copied existing exact bytes, verified frozen SHA where declared; no source, test, fixture, outcome or image regeneration.',
              'files': [files[name] for name in sorted(files)], 'unavailable_other_fixture_references': sorted(set(missing_sources)),
              'image_generation_calls': 0}
    receipt_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'copied_artifacts': len(files), 'total_bytes': sum(row['bytes'] for row in files.values()),
                      'unavailable_other_fixture_references': len(set(missing_sources)), 'source_or_fixture_changes': 0}))


if __name__ == '__main__':
    main()
