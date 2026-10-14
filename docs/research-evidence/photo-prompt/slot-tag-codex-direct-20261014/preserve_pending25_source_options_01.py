"""Freeze directly read source alternatives and their unresolved semantic scope.

No alternative is applied, no native status is updated, and no operating record
or tag is approved. Existing-only application choices are not universal source
replacements merely because their literal structure validates.
"""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FILES = [
    'authored/root_pending13_source_proposals_native_v1.json',
    'authored/root_pending13_source_proposals_native_v1.literal.py',
    'authored/root_pending13_source_proposals_native_v2.json',
    'authored/root_pending13_source_proposals_native_v2.literal.py',
    'worker-notes/native-source-root-pending13-proposals-20261015.md',
    'worker-notes/native-source-root-pending13-proposals-20261015.json',
    'worker-notes/native-07250-root-pending13-independent-20261015.json',
    'worker-notes/native-07250-root-pending13-independent-20261015.json.sha256',
    'worker-notes/native-07250-root-pending13-independent-20261015.files.sha256',
    'worker-notes/native-07250-root-pending13-independent-20261015.author.py',
    'worker-notes/native-07250-root-pending13-independent-20261015.read.py',
    'authored/native_remaining12_owner_scope_revision_01.json',
    'authored/native_remaining12_owner_scope_revision_01.literal.py',
    'authored/native_remaining12_owner_scope_revision_02.json',
    'authored/native_remaining12_owner_scope_revision_02.literal.py',
    'authored/native_remaining12_owner_scope_revision_03.json',
    'authored/native_remaining12_owner_scope_revision_03.literal.py',
    'worker-notes/native-source-remaining12-owner-scope-revision-01-20261015.md',
    'worker-notes/native-source-remaining12-owner-scope-revision-02-20261015.md',
    'worker-notes/native-source-remaining12-owner-scope-revision-03-20261015.md']


def read(name):
    return json.loads((HERE / name).read_bytes())


expected = {
    'authored/root_pending13_source_proposals_native_v2.json': 'f329b02bc5bf9a3bb6e16789fea6fdb58086c48f7902dcf43d2c2c0fe9c13a63',
    'authored/native_remaining12_owner_scope_revision_01.json': 'f91f8464a76f7999679cd892e9d7b6331f0580eb6da1f34c50187a7206fb4c0d',
    'authored/native_remaining12_owner_scope_revision_02.json': '4380afa92bf9259ad455c43c88bee28bd632cddd8ce702abcde427862af8447d',
    'authored/native_remaining12_owner_scope_revision_03.json': '97e72c778cf53f45460e820ba2fe9e53461bbc75bf7b83dee4153c5b4c420818',
    'worker-notes/native-07250-root-pending13-independent-20261015.json': '2548394b3f39f374d0c7738b8fccc04b62dd04dd3b82feb2ba208c27427c85a8'}
pins = {}
for name in FILES + [Path(__file__).name]:
    path = HERE / name
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert name not in expected or sha == expected[name], name
    if path.suffix == '.json':
        json.loads(raw)
    elif path.suffix == '.py':
        ast.parse(raw, filename=str(path))
    pins[str(path.relative_to(ROOT))] = sha

root13 = read('authored/root_pending13_source_proposals_native_v2.json')
assert [row['ordinal'] for row in root13['records']] == [0, 1, 2, 6, 7, 8, 10, 11, 12, 13, 14, 15, 19]
remaining = [read(f'authored/native_remaining12_owner_scope_revision_{n:02d}.json') for n in [1, 2, 3]]
assert sorted(row['ordinal'] for document in remaining for row in document['records']) == [1253, 1255, 1256, 1258, 1264, 1267, 1273, 1284, 1285, 1287, 1295, 1299]

# These reasons are root-authored after direct reading. File iteration above
# validates identities only; it does not derive a semantic verdict from labels.
reasons = {
    '0/2/6/7/12': 'A declared existing source actually contributing illumination can be a valid bounded use. Freezing its exact source class or physical receiving surface adds application restrictions absent from the bare noun. Preserve the broader source-type choice as unresolved; no universal replacement selected.',
    '1': 'Both lab and LED remain positive. Laboratory-use equipment and an actual laboratory setting are separate possible senses; neither is silently selected. A light-to-laboratory relation does not establish the receiver-to-laboratory relation.',
    '8/10/13/15/19': 'Actual photographic conventions apply to the image with the stated subject matter. The genre role does not generally require a new abstract photo.topic node. Existing-topic-only applications are bounded proposals, not mandatory graph enrichment.',
    '11': 'Reject the proposed timing-only application as the sole meaning-preserving replacement. Golden-hour illumination intent must remain explicitly represented. Actual day phase, simulated illumination and an existing source are distinct choices; no hue, softness, sun angle or time value is invented.',
    '14': 'The full EN/KO phrase supports a holistic dieselpunk visual sensibility. Prefer that reading over automatically splitting the word mood into a second independent atmosphere effect. This is a semantic preference pending an exact selected source revision, not a tag or native approval.',
    '1253': 'The physical counter separating two actual participants is a plausible explicit reading. Preserve spatial-between, separation and formal social impression as distinct meaning; no occupation, access right, count or numerical distance is inferred. No final source choice yet.',
    '1255': 'Same existing holder and object, actual holding, near-self placement and neutral presentation are preserved. The phrase as specified below lacks an in-source antecedent and must become explicit receiver prose before a selected input.',
    '1256': 'Blank badge and access card remain actual alternatives. Absence of badge lettering is an explicit text effect, not a role-name shortcut. Gaze endpoints and actual eyes remain independently declared; no workplace, authority or head pose is created.',
    '1258': 'Actual safe voltage checking remains an effect with the exact tester and measurement target. The safe qualifier is neither certification nor a prerequisite that silently removes selected action. No wire, probe, PPE, result or target topology is invented.',
    '1264': 'Chair-seat-part is one interpretation of the Korean seat wording. Do not silently force a separate place or seat scope to be part_of the chair. Current state, disturbed seat and recent trace must remain; this interpretation stays pending.',
    '1267': 'Projected grid, lantern array and spatial grid illumination are competing readings, not original OR branches. Prefer no mechanism without direct source support. No projected surface, extra emitter, array cardinality or volumetric particles are invented; the exact application remains pending.',
    '1273': 'Existing action figure OR doll identity, actual smallness and scene-prop role survive separately. Keep the original human applicability condition as a condition; it does not make the toy human or create a new person.',
    '1284': 'Eye-focused album appearance applies to an explicitly selected actual face and image. Face/eyes require atomic evidence on the same actual carrier; no automatic primary_face or invented eye node. Preserve kpop OR album conditions.',
    '1285': 'Counterpart-chair association and propped-against-chair state are positive. The proposed participant interpretation is not yet a final reading of partner chair. It must not add two participants or move an actual selected association into a fabricated prerequisite.',
    '1287': 'Keep actual colleague role, off-frame relation and image coverage as bounded effects on the same independently declared colleague and other person. The other person need not become visible, and no workplace or new colleague is introduced.',
    '1295': 'Aged-looking and young-looking skin are two region-local selections with appearance and age permission projections, not four independent aging actions. The exact regions and their real owners remain separate; no baby, family or chronological age. Catalog local-region/nonhuman applicability remains under explicit V5 review.',
    '1299': 'No complete source-after or owner/receiver contract was authored. Actual exchange, hands-only scope and macro composition must remain pending together. Do not infer two people, a hand count, transferred object or completed transfer, and do not drop action to force approval.'}
report = {'schema': 'photo-root-source-alternative-review-checkpoint/v1', 'actor': '/root',
    'research_only': True, 'files': pins, 'raw_sha256_and_json_python_ast_checks': True,
    'root_direct_read_scope': {
        'root13_complete_original_current_5B_ownbindings': 'Read in this continuous task before this checkpoint; not inferred from this serializer.',
        'root13_complete_fifteen_source_after_guards_maps_effects_and_independent_semantic_reasons': True,
        'remaining12_complete_current_and_all_authored_after_options_owner_plans_effects': True,
        'remaining12_all_exact_old5B_fresh_root_read_claimed': False,
        'fresh_root_all49_or51_fullspec_read_claimed': False,
        'independent13_source_and_all_options_review': 'Pinned separate07250 direct review; its51 fullspec reads are its own attestation, not root reads.'},
    'root_semantic_findings': reasons,
    'proposals_selected_into_a_new_input': 0, 'source_records_changed': 0,
    'native_proofs_statuses_acceptances_changed': 0, 'slot_tags_changed': 0,
    'operational_native_qualification': 0, 'gemini_calls': 0, 'network_calls': 0,
    'historical_v1_boundary': 'Wrong frozen_entity_relation value_type in root13v1 is preserved; only v2 uses the actual entity.owner_id/v1 protocol. Shape correction grants no meaning approval.'}
output = HERE / 'ROOT-PENDING25-SOURCE-OPTIONS-REVIEW-01.json'
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip()
with output.open('x') as stream:
    json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
planned = set(pins) | {str(output.relative_to(ROOT))}
subprocess.run(['git', 'add', '--', *sorted(planned)], cwd=ROOT, check=True)
checked = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, capture_output=True, text=True)
assert checked.returncode == 0, checked.stdout
actual = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert actual <= planned
for name in planned:
    assert subprocess.check_output(['git', 'show', ':' + name], cwd=ROOT) == (ROOT / name).read_bytes(), name
print(json.dumps({'pinned_files': len(pins), 'unique_proposed_records': 25, 'native_or_operational_approvals': 0, 'staged': True}))
