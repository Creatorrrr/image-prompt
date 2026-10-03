"""Build and inspect the exact publication scope, excluding unrelated work."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
EVIDENCE = HERE.parent
INDEX = Path('/tmp/image-prompt-slang-merge-20261003-otvpg0ba/publication.index')


def main():
    preservation = json.loads((HERE / 'PRESERVATION.json').read_text())
    indexes = json.loads((HERE / 'INDEX-RECONCILIATION.json').read_text())
    paths = set(preservation['exclusive_local_files'])
    paths.update((
        'skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json',
        'skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json',
        'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json',
    ))
    paths.update(indexes['semantic_shards'])
    source_paths = set(paths)
    directories = [str((EVIDENCE / name).relative_to(ROOT)) for name in (
        'slang-visual-semantics-20261003', 'slang-integration-20261003',
        'slang-merge-20261003',
    )]
    listed = subprocess.check_output([
        'git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z', '--',
        *directories,
    ], cwd=ROOT)
    paths.update(p.decode() for p in listed.split(b'\0') if p)
    # The scope receipt itself is tracked, without a circular self-hash.
    receipt = str((HERE / 'PUBLICATION-SCOPE.json').relative_to(ROOT))
    paths.discard(receipt)
    assert not any(path in preservation['protected_unrelated_files'] for path in paths)
    assert not any(path.endswith('/native-data-snapshot.tar.gz') for path in paths)
    assert all((ROOT / path).is_file() for path in paths)
    assert not subprocess.check_output(['git', 'ls-files', '--unmerged'], cwd=ROOT)
    patterns = {
        'openai_token': rb'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}',
        'google_token': rb'\bAIza[0-9A-Za-z_-]{35}',
        'private_key': rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        'aws_access_key': rb'\bAKIA[0-9A-Z]{16}',
    }
    matches = []
    rows = {}
    for name in sorted(paths):
        data = (subprocess.check_output(['git', 'show', f':{name}'], cwd=ROOT,
                env={**os.environ, 'GIT_INDEX_FILE': str(INDEX)})
                if name in source_paths else (ROOT / name).read_bytes())
        rows[name] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
        if b'\0' not in data and name.rsplit('.', 1)[-1].lower() not in {'png', 'jpg', 'jpeg', 'gz'}:
            for kind, pattern in patterns.items():
                count = len(re.findall(pattern, data))
                if count:
                    matches.append({'file': name, 'kind': kind, 'count': count})
    assert not matches, matches
    assert all(row['bytes'] < 50_000_000 for row in rows.values())
    result = {
        'schema_version': 'photo-slang-publication-scope/v1',
        'files_without_receipt': len(rows), 'total_bytes_without_receipt': sum(r['bytes'] for r in rows.values()),
        'all_files_below_50MB': True, 'credential_pattern_matches': matches,
        'protected_unrelated_files_excluded': True, 'native_archive_excluded': True,
        'source_receipts_bind_tested_publication_index': True,
        'current_semantic_shards_included': indexes['semantic_shards'],
        'files': rows,
    }
    (HERE / 'PUBLICATION-SCOPE.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    paths.add(receipt)
    pathspec = Path('/tmp/image-prompt-slang-merge-20261003-publication-paths.nul')
    pathspec.write_bytes(b'\0'.join(p.encode() for p in sorted(paths)) + b'\0')
    print(json.dumps({
        'files_to_stage': len(paths), 'bytes_without_receipt': result['total_bytes_without_receipt'],
        'credential_pattern_matches': matches, 'pathspec': str(pathspec),
        'largest_files': sorted(
            [{'path': name, 'bytes': row['bytes']} for name, row in rows.items()],
            key=lambda row: row['bytes'], reverse=True,
        )[:8],
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
