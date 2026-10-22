"""Preserve only concrete image paths explicitly returned by this arm's tool."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct

ROOT = Path('/Users/chasoik/Projects/image-prompt')
ARM = ROOT / 'docs/research-evidence/photo-prompt/clockpunk-20261023/image-tests/arm-b'
RUN = ROOT / 'generated/photo-runs/clockpunk-20261023-independent-b'
OUTPUT = ROOT / 'generated/images/clockpunk-20261023-independent-b'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--paths-json', required=True)
    args = parser.parse_args()
    state = json.loads((RUN / 'workflow.json').read_text())
    plan = json.loads(Path(state['artifacts']['native_plan']['path']).read_text())
    paths = json.loads(args.paths_json)
    verified = []
    seen = set()
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute() or not path.is_file():
            continue
        header = path.read_bytes()[:24]
        if header[:8] != b'\x89PNG\r\n\x1a\n' or header[12:16] != b'IHDR':
            continue
        size, fmt = list(struct.unpack('>II', header[16:24])), 'PNG'
        sha = digest(path)
        if sha in seen:
            continue
        seen.add(sha)
        suffix = {'PNG': '.png', 'JPEG': '.jpeg', 'WEBP': '.webp'}.get(fmt)
        if suffix is None:
            continue
        OUTPUT.mkdir(parents=True, exist_ok=True)
        target = OUTPUT / ('original' + (f'-{len(verified)+1}' if verified else '') + suffix)
        if target.exists() and digest(target) != sha:
            raise RuntimeError('Refusing to replace an existing different result')
        if not target.exists():
            shutil.copy2(path, target)
        if digest(target) != sha:
            raise RuntimeError('Original-to-workspace copy hash mismatch')
        verified.append({'tool_returned_path': str(path), 'workspace_path': str(target),
                         'sha256': sha, 'size': size, 'format': fmt})
    observation = {'operation_id': plan['operation_id'],
                   'outcome': 'returned' if verified else 'preview_only'}
    if verified:
        observation['image_path'] = verified[0]['workspace_path']
    (ARM / 'native-observation.json').write_text(json.dumps(observation, indent=2) + '\n')
    (ARM / 'image-persistence.json').write_text(json.dumps({
        'schema': 'clockpunk-arm-returned-image-persistence/v1',
        'operation_id': plan['operation_id'],
        'source': 'exact local paths returned by image_gen tool; no cache scan or reconstruction',
        'images': verified,
        'outcome': observation['outcome']}, indent=2) + '\n')
    print(json.dumps(observation))


if __name__ == '__main__':
    main()
