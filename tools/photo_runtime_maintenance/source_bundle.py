"""Export the installed code from its exact existing Git commit, without activation."""
from pathlib import Path
import hashlib
import subprocess
import tempfile

from state import ROOT, EVIDENCE, read, write, sha, git
from bundles import pack, restore


def main():
    baseline = read(EVIDENCE/'BASELINE.json.gz')
    installed = baseline['installed']
    native = Path(installed['native'])
    manifest = read(native/'manifest.json')
    wt = next(Path(p) for p in baseline['repositories'] if p != str(ROOT))
    commit = baseline['repositories'][str(wt)]['head']
    destination = ROOT/'docs/research-archives/photo-prompt/h-f2-operating-source.zip'
    lockpath = destination.with_name('SOURCE-LOCK.json')
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        members = {}
        origins = {}
        for relative, expected in manifest['source']['code'].items():
            source = 'skills/photo-prompt-image-generator/'+relative
            raw = git(wt, 'show', commit+':'+source)
            if hashlib.sha256(raw).hexdigest() != expected or sha(native/relative) != expected:
                raise ValueError('Git/source/installed mismatch: '+relative)
            p = temp/'code'/relative
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
            members[relative] = p
            origins[relative] = {'commit': commit, 'path': source, 'sha256': expected}
        for name, p in [('native-manifest.json',native/'manifest.json'),
                        ('h-f2-manifest.json',Path(installed['hroot'])/'manifest.json'),
                        ('embedding-runtime.lock.json',native/'embedding-runtime.lock.json'),
                        ('retrieval-runtime.json',ROOT/'skills/photo-prompt-image-generator/retrieval-runtime.json')]:
            members['release-inputs/'+name] = p
        seal = pack(destination, members)
        seal.update(schema='photo-operating-source-bundle/v1', code=manifest['source']['code'],
                    origins=origins, installed=installed['config'],
                    dependencies={'native_generation':installed['native'], 'h_generation':installed['hroot'],
                                  'model':'skill-owned installation and copied package preserved',
                                  'runtime':'embedding-runtime.lock.json'},
                    executable_authority=False, source_only=True)
        write(lockpath, seal)
        restored = restore(destination, seal, temp/'restored')
        actual = {str(p.relative_to(restored)):sha(p) for d in ('scripts','precore') for p in (restored/d).glob('*.py')}
        if actual != manifest['source']['code']:
            raise ValueError('restored operating code differs')
    write(EVIDENCE/'STAGE02.json', {'status':'PASS', 'source_commit':commit,
          'code_files_verified':len(origins), 'bundle':str(destination.relative_to(ROOT)),
          'bundle_sha256':sha(destination), 'restored_code_matches_installed':True,
          'operating_selection_changed':False, 'CURRENT_writes':0, 'Gemini_calls':0,
          'restoration_does_not_read_worktree':True,
          'data_dependencies_preserved':installed})
    print('operating source bundle PASS:', len(origins), 'code files')


if __name__ == '__main__':
    main()
