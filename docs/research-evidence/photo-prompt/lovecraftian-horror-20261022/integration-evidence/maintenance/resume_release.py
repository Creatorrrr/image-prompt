"""Resume after the verified native index; preserve every publication check.

Python 3.14 cyclic-GC scans dominated large acyclic JSON decoding in the first
attempt. Disabling cyclic GC changes allocation scheduling, not source/index,
native, H-F2, hash, local-execution, vector, or field-statistics validation.
"""
import gc
gc.disable()
from pathlib import Path
import runpy, textwrap, time, json, hashlib

O = Path(__file__).resolve().parent
source = O / 'build_release.py'
ns = runpy.run_path(str(source))
report = ns['read'](O / 'native-index-build.json')
layout = ns['read'](ns['STAGE'] / 'assets/photo_candidate_search.json')
assert report['verification']['verified'] is True
assert layout['layout_id'] == report['layout_id']
assert ns['read'](O / 'canonical-source-validation.json')['status'] == 'pass'
ns.update(new=ns['collect'](), fresh=ns['read'](O / 'new-native-records.json'),
          changed=ns['read'](O / 'changed-native-records.json'), t=time.monotonic())
audit = {'status': 'resume_verified_index_with_all_publication_checks',
         'python_cyclic_gc_enabled': gc.isenabled(),
         'builder_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
         'native_layout_id': report['layout_id'],
         'validation_bypassed': False, 'kernel_code_changed': False,
         'interrupted_pid': 90831,
         'reason': 'sample showed repeated cyclic GC during JSON decode; no runtime code change'}
(O / 'resume-execution.json').write_text(json.dumps(audit, indent=2)+'\n')
publication = ns['read'](O / 'native-staged.json')
sealed = ns['STORE'] / 'generations' / publication['generation_id']
verified = ns['SnapshotPublisher']._verify_generation(sealed, publication['generation_id'], full=True)
assert verified['source_fingerprint'] == publication['source_fingerprint']
assert verified['search_layout']['layout_id'] == report['layout_id']
for relative, member in verified['members'].items():
    assert ns['file_sha'](ns['STAGE'] / relative) == member['sha256'], relative
ns['publication'] = publication
audit['reused_completed_native_publication'] = publication['generation_id']
audit['all_published_members_reverified_by_hash'] = True
audit['stage_identical_to_published_members'] = True
audit['interrupted_resume_pid'] = 46795
(O / 'resume-execution.json').write_text(json.dumps(audit, indent=2)+'\n')
tail = source.read_text().split(' publication=SnapshotPublisher(STAGE,STORE).stage();write(O/\'native-staged.json\',publication)', 1)[1]
tail = tail.split("if __name__=='__main__':main()", 1)[0]
exec(compile(textwrap.dedent(tail), str(source)+':resume-publication', 'exec'), ns)
