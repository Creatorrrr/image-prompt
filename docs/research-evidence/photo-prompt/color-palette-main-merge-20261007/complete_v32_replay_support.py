"""Include authenticated archived backing paths needed by V32's V31 checks."""
from pathlib import Path
import hashlib
import json

E=Path(__file__).resolve().parent
W=E.parents[3]
I=Path('skills/subculture-illustration-image-generator')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

helper=W/'tests/photo_palette_history.py';text=helper.read_text()
needle='        f._v24_empty_destination(directory);staged.replace(directory)\n'
addition='''        # V32 validates V31's original backing paths as well as logical files.
        # Their mapping and payload identity are already sealed by V32's proof.
        _, original_v31 = f._v32_transition(source_root)
        for row in original_v31['members']:
            if row['source_path'] == row['path']:
                continue
            raw = f._v24_verified_payload(source_root, row)
            target = staged / f._v17_safe_path(row['source_path'])
            if target.exists():
                if target.read_bytes() != raw or target.stat().st_mode & 0o7777 != int(row['mode'][-3:], 8):
                    raise AssertionError('Frozen V32 archived backing collision: ' + row['source_path'])
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if link_verified:
                try:
                    os.link(f._v24_regular_path(source_root, row['source_path']), target)
                except OSError as exc:
                    if exc.errno != errno.EXDEV:
                        raise
                    target.write_bytes(raw); target.chmod(int(row['mode'][-3:], 8))
            else:
                target.write_bytes(raw); target.chmod(int(row['mode'][-3:], 8))
'''
assert text.count(needle)==1;helper.write_text(text.replace(needle,addition+needle))
implementation=json.loads((E/'BOUNDARY-IMPLEMENTATION.json').read_text());old=implementation['support_sha256'];new=sha(helper)
for p in [W/'tests/photo_prompt_fixtures.py',W/I/'scripts/validate_illustration_assets.py']:
    text=p.read_text();assert text.count(old)==1;p.write_text(text.replace(old,new))
descriptor=W/I/'assets/universal_scene_baseline_v2.json'
original=(E/'v32-parent-source-files'/I/'assets/universal_scene_baseline_v2.json').read_bytes()
oldv=json.loads((E/'V33-PALETTE-DATA-PROOF.json').read_text())['previous_validator_sha256'].encode()
assert original.count(oldv)==1
descriptor.write_bytes(original.replace(oldv,sha(W/I/'scripts/validate_illustration_assets.py').encode(),1))
implementation.update(support_sha256=new,validator_sha256=sha(W/I/'scripts/validate_illustration_assets.py'),fixtures_sha256=sha(W/'tests/photo_prompt_fixtures.py'),universal_descriptor_sha256=sha(descriptor),replay_support='V32 materialization also retains V31 manifest-authenticated original source_path backings; no proof or historical assertion is weakened.')
(E/'BOUNDARY-IMPLEMENTATION.json').write_text(json.dumps(implementation,indent=2)+'\n')
print(json.dumps(implementation))
