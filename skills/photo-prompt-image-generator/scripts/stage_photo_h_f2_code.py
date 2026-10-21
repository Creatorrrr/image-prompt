"""Stage query/workflow code on a sealed H-F2 release; keep its data and CURRENT.

By default only the two maintained H-F2 query/workflow modules are replaced.
An explicit member allowlist and reviewed overlay can carry a wider code fix
without publishing unrelated dirty work. Data and old generations stay intact.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from photo_installed_h_f2 import (
    CONFIG, SKILL_ROOT, default_store, digest, file_sha, read, release,
    require, runtime_python,
)

MODULES = ('photo_h_f2_queries.py', 'photo_h_f2_workflow.py')


def stage(destination, *, source_store=None, generation_id=None, skill_root=SKILL_ROOT,
          members=None, overlay_root=None):
    destination = Path(destination).resolve()
    source_store = Path(source_store or default_store()).resolve()
    config = read(Path(skill_root) / CONFIG)
    generation_id = generation_id or config['generation_id']
    native, manifest, native_manifest = release(source_store, generation_id, full=True)
    selected = list(members) if members is not None else ['scripts/' + n for n in MODULES]
    require(bool(selected) and len(set(selected)) == len(selected), 'nonempty distinct code member allowlist required')
    source_root = Path(overlay_root or skill_root).resolve()
    for relative in selected:
        path = Path(relative)
        require(not path.is_absolute() and len(path.parts) == 2 and path.parts[0] in ('scripts','precore')
                and path.suffix == '.py', 'not an explicit Python code member')
        source = source_root / relative
        require(source.is_file() and not source.is_symlink() and source_root in source.resolve().parents, 'unsafe overlay code member')
    python = runtime_python(skill_root, manifest)
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.code-release-', dir=destination) as temporary:
        staged = Path(temporary) / 'native'
        members = {}
        for relative, row in native_manifest['members'].items():
            target = staged / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(native / relative, target)
        for relative in selected:
            source = source_root / relative
            compile(source.read_bytes(), str(source), 'exec')
            shutil.copyfile(source, staged / relative)
        program = """import json,sys;sys.path.insert(0,sys.argv[1])
import prompt_generator as g
import photo_runtime_sources as r
print(json.dumps({'code':r.LOADED_CODE,'environment':r.LOADED_ENVIRONMENT,
                  'algorithm_sha256':r.algorithm_hash(g)}))
"""
        env = dict(os.environ, HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', PYTHONNOUSERSITE='1')
        env.pop('PYTHONPATH', None)
        result = subprocess.run([str(python), '-I', '-c', program, str(staged / 'scripts')],
                                env=env, text=True, capture_output=True, check=True)
        implementation = json.loads(result.stdout)
        expected = dict(native_manifest['source']['code'])
        expected.update({relative: file_sha(staged / relative) for relative in selected})
        require(implementation['code'] == expected, 'unexpected code change in staged release')
        require(implementation['environment'] == native_manifest['source']['environment'], 'runtime environment changed')
        updated = copy.deepcopy(native_manifest)
        updated['source']['code'] = expected
        updated['source_fingerprint'] = digest(updated['source'])
        updated['algorithm_sha256'] = implementation['algorithm_sha256']
        for relative in sorted(set(native_manifest['members']) | set(selected)):
            path = staged / relative
            st = path.stat()
            members[relative] = {'bytes': st.st_size, 'sha256': file_sha(path),
                                 'identity': [st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns]}
        updated['members'] = members
        native_id = digest(updated)
        (staged / 'manifest.json').write_text(json.dumps(updated, ensure_ascii=False, sort_keys=True, separators=(',', ':')))
        target = destination / 'generations' / native_id
        target.parent.mkdir(parents=True, exist_ok=True)
        require(not target.exists(), 'staged native generation already exists')
        os.rename(staged, target)

        h_manifest = copy.deepcopy(manifest)
        h_manifest['native_generation_id'] = native_id
        h_manifest['code'] = {p.name: file_sha(p) for p in sorted((target / 'scripts').glob('photo_h_f2*.py'))}
        h_id = digest(h_manifest)
        h_staged = Path(temporary) / 'h-f2'
        h_staged.mkdir()
        for relative, sha in manifest['files'].items():
            source = source_store / 'h-f2-generations' / generation_id / relative
            output = h_staged / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, output)
            require(file_sha(output) == sha, 'H-F2 data changed during copy')
        (h_staged / 'manifest.json').write_text(json.dumps(h_manifest, ensure_ascii=False, sort_keys=True, separators=(',', ':')))
        h_target = destination / 'h-f2-generations' / h_id
        h_target.parent.mkdir(parents=True, exist_ok=True)
        require(not h_target.exists(), 'staged H-F2 generation already exists')
        os.rename(h_staged, h_target)
        release(destination, h_id, full=True)
    return {'status': 'pass', 'store': str(destination), 'generation_id': h_id,
            'native_generation_id': native_id, 'parent_generation_id': generation_id,
            'candidate_data_changed': False, 'CURRENT_writes': 0, 'code_members_replaced': selected}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--source-store', type=Path)
    parser.add_argument('--generation-id')
    parser.add_argument('--member', action='append', help='exact existing or new scripts/*.py or precore/*.py member; repeatable')
    parser.add_argument('--overlay-root', type=Path, help='reviewed member files; copied into the sealed release, never a runtime dependency')
    args = parser.parse_args()
    print(json.dumps(stage(args.destination, source_store=args.source_store,
                           generation_id=args.generation_id, members=args.member,
                           overlay_root=args.overlay_root), indent=2))
