#!/usr/bin/env python3
"""Retrieve independent frozen inputs with the installed H-F2 release.

The output is an H-F2 material bundle, not a legacy candidate pack. The
authored slot plan is required: search queries cannot be inferred from a
candidate or silently manufactured from the request.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

import photo_installed_h_f2 as installed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ('request-envelope-json', 'authorial-core-json', 'creative-controls-json',
                 'embodiment-review-json', 'slot-expression-plan-json', 'output-directory'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--query-cache', type=Path)
    parser.add_argument('--require-camera-evidence', action='append',
                        choices=('direction', 'height'), default=[])
    parser.add_argument('--new-author-camera-evidence', action='store_true')
    args = parser.parse_args(argv)
    skill = Path(__file__).resolve().parents[1]
    config = installed.read(skill / installed.CONFIG)
    installed.require(config.get('schema') == installed.SCHEMA and
        config.get('policy') == 'photo-h-f2/v1' and
        config.get('store_subdirectory') == 'h-f2-installed', 'invalid installed search configuration')
    store = installed.default_store().resolve()
    native, manifest, native_manifest = installed.release(store, config['generation_id'], full=True)
    installed.require(manifest['native_generation_id'] == config['native_generation_id'] and
        installed.digest(native_manifest['source']['code']) == config['code_sha256'],
        'installed release binding changed')
    python = installed.runtime_python(skill, manifest)
    worker = Path(__file__).with_name('photo_h_f2_standalone.py').resolve()
    env = dict(os.environ, HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
               HF_HUB_DISABLE_TELEMETRY='1', PYTHONNOUSERSITE='1')
    for key in ('PYTHONPATH', 'OPENAI_API_KEY', 'GEMINI_API_KEY', 'GOOGLE_API_KEY', 'ANTHROPIC_API_KEY'):
        env.pop(key, None)
    launcher = ('import sys,runpy;from pathlib import Path;'
                'native=sys.argv.pop(1);entry=sys.argv.pop(1);'
                'sys.path.insert(0,str(Path(native)/"scripts"));'
                'runpy.run_path(entry,run_name="__main__")')
    forwarded = list(sys.argv[1:] if argv is None else argv)
    return subprocess.run([str(python), '-I', '-c', launcher, str(native), str(worker),
                           '--installed-store', str(store), '--installed-generation', config['generation_id'],
                           '--installed-skill', str(skill), *forwarded], env=env).returncode


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError, TypeError) as exc:
        print('Error: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
