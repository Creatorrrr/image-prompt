"""Serialize root-authored scope corrections after the independent 144 audit.

All changes below are explicit normative slot decisions. This helper neither
classifies candidates nor copies old approvals to a new catalog. Preserve R01.
"""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def read(name):
    raw = (HERE / name).read_bytes()
    return json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def save(name, value):
    path = HERE / name
    with path.open('xb') as stream:
        stream.write(canonical(value) + b'\n')
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': sha(value)}


before = read('CATALOG-FINAL-142-V2.json')
previous = read('CATALOG-PROPOSED-144-V3.json')
after = copy.deepcopy(previous)
after['surface_moisture']['property_prefixes'].extend(['skin.state.dry', 'garment.state.dry', 'wardrobe.state.dry'])
after['body_pose'].update({
    'description': 'Explicit whole-body posture, support or articulation of an identified biological, mechanical or represented body, without inferring unmentioned anatomy.',
    'description_ko': '생물·기계·묘사된 몸의 명시적 전신 자세·지지·관절 배치. 실제 대상과 몸의 범위를 확인하며 언급하지 않은 신체 부위나 지지 접촉을 추론하지 않는다.',
    'owners': ['entity'], 'applicability': {},
    'includes': ['Explicit standing, sitting, lying or other whole-body posture of a declared human, animal, robot or represented body.',
                 'Preserve the actual support and articulated connections when declared. Standing alone does not supply feet, legs, a supporting ground contact or a human body.',
                 'Decide effect versus a required existing posture from the whole source; source-specific category and domain conditions remain cumulative.'],
    'excludes': ['A rigid object shape, a camera viewpoint or an activity word alone does not establish a whole-body pose.',
                 'Relative rotation of body axes, hand articulation, concrete action and rendered motion have separate roles when supported.',
                 'Do not turn an unavailable body or limb into a new entity to satisfy a pose.'],
})
after['body_orientation'].update({
    'description': 'Explicit orientation of an identified body or relative rotation of its declared connected regions, including biological, mechanical and represented bodies.',
    'description_ko': '생물·기계·묘사된 몸과 명시적으로 연결된 부위의 축 방향·상대 회전. 카메라 방향·전신 지지 자세·눈의 시선과 구별한다.',
    'owners': ['entity'], 'applicability': {},
    'includes': ['A declared body axis orientation or relative rotation of connected regions, with the actual regions, relation and reference basis stated.',
                 'A nonhuman or represented body can qualify on the same literal contract. Actual source conditions and available owner regions still apply.'],
    'excludes': ['Camera position, body support pose, eye-gaze direction and a scene object facing the frame are not interchangeable.',
                 'Standing or an activity alone does not supply a rotation, connected region, angle, axis or reference basis.',
                 'Do not infer eyes, a nose, joints or a human torso from the role name or a mechanical subject.'],
})
after['light_shape'].update({
    'description': 'Explicit spatial geometry of illumination, highlights or shadow boundaries on an identified receiving surface or within a declared illuminated spatial region.',
    'description_ko': '특정 수광 표면 또는 명시된 공간 영역에 나타나는 빛·하이라이트·그림자 경계의 공간 형태. 표면 무늬와 명시적 입체 광선 분포를 실제 범위에 맞게 구별한다.',
    'includes': ['A source-declared light pattern or shadow boundary on its actual receiving surface.',
                 'Explicit volumetric rays or other spatial light geometry can use their declared spatial region; a physical receiving surface is not compulsory for that meaning.',
                 'Preserve the source geometry, carrier and actual light/receiver relation. The source may require additional independently grounded owners.'],
    'excludes': ['A ray shape does not itself identify a lamp, camera, fog, smoke, dust particles or the physical scattering mechanism.',
                 'Spatial shape alone does not supply incident direction, light intensity, color temperature or the type of source.',
                 'Sacred/revelatory wording does not create a deity, religious event or an otherwise unmentioned world fact.'],
})
after['relational_action'].update({
    'description': 'Concrete interaction with explicitly declared action endpoints, including biological, mechanical or represented participants and their objects.',
    'description_ko': '명시된 행위 주체와 상대·물체 사이의 구체적 상호 동작. 인간·동물·기계·묘사된 대상을 포함하며 실제 행위와 소유·접촉 관계를 구별한다.',
    'applicability': {},
    'includes': ['The source explicitly describes the participants or a participant and an object interacting; each endpoint must be independently supported.',
                 'Self-directed interaction can address an explicitly owned part or object while retaining its actual part/whole relationship.',
                 'A human participant is not compulsory. Intrinsic source conditions, distinctness or part ownership, and actual performed action remain mandatory.'],
    'excludes': ['A role label, co-presence, proximity or an isolated hand pose does not supply a performed interaction.',
                 'Do not add a counterpart, helper, contact, tool or action endpoint from a verb category alone.',
                 'Do not split one actual self-owned body into two people or merge explicitly distinct participants.'],
})
after['companion_animal'].update({
    'description': 'A separately declared animal participant explicitly accompanying an identified primary subject, with the companion relation, count and ownership grounded.',
    'description_ko': '명시된 주 대상에 실제로 동반하는 별도 동물 참여자. 주 대상과 동물의 동반 관계·수·소유자를 각각 확인하며 주 대상을 인간으로 한정하지 않는다.',
    'applicability': {},
    'includes': ['An explicit animal companion relation to the declared primary subject; the primary subject can be human or nonhuman.',
                 'Keep animal identity/count, independent owners and any required contact or placement conditions exactly as supported.'],
    'excludes': ['A lone animal, an animal name, another animal in the background or a generic peaceful mood alone does not establish companionship.',
                 'Do not infer pet ownership, species, domestication, affection, physical contact or a new primary subject from the tag.',
                 'An animal-only source with no accompanying relation must use its actual subject/action roles instead.'],
})
after['garment_detail'].update({
    'description': 'Construction, topology, trim or local form of an identified garment, whether worn, displayed, standalone or represented, distinct from anatomy and material identity.',
    'description_ko': '착용·전시·단독·묘사된 의복 자체의 구조·연결·트림·국소 형태. 실제 의복 소유자를 확인하며 인체 구조·피부 표식·재질 정체와 구별한다.',
    'applicability': {},
    'includes': ['An actual garment-owned seam, cuff, hem, sleeve, trim or construction relation; an independently declared human wearer is not compulsory.',
                 'If a wearer, layering relation, support or attachment is required by the source, preserve that specific condition rather than deriving it from the slot.',
                 'Separately supported material, texture, fit, layering or state can have their own roles without duplicating the garment.'],
    'excludes': ['Cloth material or an unowned edge alone is not a garment construction detail.',
                 'A garment detail does not establish a wearer, anatomy, exposure, fit, material identity or clothing ensemble.',
                 'Do not remove any intrinsic source-specific human, adult or domain restriction.'],
})
after['hair_style'].update({
    'description': 'Explicit shape, length, arrangement or strand topology of an identified hair region or wig, separate from its color and material identity.',
    'description_ko': '실제 모발 영역이나 가발의 명시적 형태·길이·배치·가닥 연결. 색·재질과 분리하며 자연 모발·가발·묘사된 머리의 실제 소유자를 구별한다.',
    'owners': ['entity'], 'applicability': {},
    'includes': ['An explicitly declared hair or wig arrangement with its actual owned region and strand continuity.',
                 'A standalone wig or represented hair can qualify without inventing a human wearer or biological follicles.',
                 'Source-specific wearer/category conditions and existing-region prerequisites remain mandatory.'],
    'excludes': ['A synthetic fiber sheen alone does not supply a hairstyle or a living hair root.',
                 'General animal fur, a braided rope, a body-hair region and a hair-color word are not automatically a head-hair arrangement.',
                 'Do not introduce a wearer, head, scalp, follicles, hair identity or a new physical strand connection from a style name.'],
})
after['hair_color'].update({
    'description': 'Explicit color and color placement bounded to an identified hair region, wig or represented hair, distinct from scene grading and material identity.',
    'description_ko': '실제 모발 영역·가발·묘사된 머리에 한정된 명시적 색과 배치. 장면 색 보정·빛의 색·의복 색·재질 정체와 구별한다.',
    'owners': ['entity'], 'applicability': {},
    'includes': ['A declared hair or wig color on its actual bounded region; a human wearer or natural living hair is not compulsory.',
                 'Keep the exact source color, placement, intrinsic subject restrictions and independently required region ownership.'],
    'excludes': ['Illumination color, global image grading, general fur, a colored fiber object or an unowned color word alone is not hair-region color.',
                 'Do not infer dye chemistry, natural pigmentation, a wearer, follicles, hairstyle or another body region from the color.',
                 'A broader slot contract does not waive an intrinsic source-specific human or adult condition.'],
})
assert len(after) == 144 and set(after) == set(previous)
changed = [key for key in sorted(after) if before.get(key) != after[key]]
assert len(changed) == 12
proposal = save('CATALOG-PROPOSED-144-V3-R02.json', after)

source = read('SOURCE.json.gz')
order = read('ORDER.json')
meanings = {
    2507: 'Explicit volumetric god rays and a threshold relation support a spatial light geometry; no fog/device/deity is inferred.',
    4503: 'Explicit robot standing in command standby exposes the old human-only pose gate; no unmentioned limbs, support contact or rotation is supplied.',
    4125: 'The robot performs self-repair on its own explicitly open panel; retain the self-owned endpoint rather than adding a human or a second person.',
    1371: 'Synthetic wig-fiber detail demonstrates a nonbiological carrier, but its sheen alone is a negative control for actual hairstyle arrangement.',
    1466: 'Pale-blue cosplay wig color is explicitly local color; its intrinsic for_any human restriction is retained even though the slot itself is generic.',
    7761: 'An explicit gathered wig braid, repeated crossing sections and separate tied end support owned strand topology; no biological follicle is inferred.',
    8296: 'Long costume braid continuously joins the gathered wig at the back of the head. Preserve the actual source-supported continuity and wearer condition.',
    3671: 'A dove passing through the frame has no stated companionship. Historical companion provenance is not a positive companion-role witness.',
}
evidence = save('CATALOG-PROPOSED-144-V3-R02-SOURCE-EVIDENCE.json', {
    'schema': 'photo-root-catalog-source-evidence/v1', 'actor': '/root',
    'status': 'proposal_pending_independent_whole_catalog_review',
    'source_sha256': sha(source),
    'root_direct_full_source_reads': [{'ordinal': n, 'candidate_id': order[n],
        'whole_original_record': source['candidates'][order[n]], 'root_meaning': reason}
        for n, reason in meanings.items()],
    'root_direct_full_prior_specs_reread': {key: before[key] for key in [
        'body_pose', 'body_orientation', 'light_shape', 'relational_action',
        'companion_animal', 'garment_detail', 'hair_style', 'hair_color']},
    'prior_four_change_source_evidence': 'CATALOG-PROPOSED-144-V3-SOURCE-EVIDENCE.json',
    'independent_prior_whole144_review': {
        'file': 'worker-notes/native-evidence-whole144-taxonomy-review-20261014.json',
        'raw_sha256': 'fd0b8cd7ddf7300135023f09dcd6703936ef33473ced0b171bbcd21ba9b2a414'},
    'normative_scope_choices_without_claiming_a_positive_corpus_example': [
        'body_orientation explicitly keeps the generic body-axis definition; standing alone is not an orientation witness.',
        'companion_animal keeps an actual accompanying relation without a compulsory human primary; the lone dove is expressly negative.',
        'garment_detail remains garment-owned construction without a compulsory wearer; cloth alone is expressly negative.'],
    'candidate_tags_assigned': 0, 'native_proofs_resigned': 0,
    'canonical_catalog_changed': False, 'source_corrections_applied': False, 'gemini_calls': 0,
})
reasons = {
    'thermal_state': 'Preserve explicit physical temperature meanings separately from color, emotional warmth, sensory proxies and inferred thermal causes.',
    'surface_moisture': 'Preserve actual surface moisture and bound skin/garment wet, damp and dry facts without including unrelated skin/garment state.',
    'participant_role': 'Remove accidental primary/secondary viewpoint restriction while preserving the actual carrier, independently needed endpoints and intrinsic human/adult/domain conditions.',
    'narrative_phase': 'Explicit event phases do not require a human; retain actual event relation and original source guards.',
    'body_pose': 'The whole-body definition must include explicitly standing animals/robots without inventing anatomy or inferring posture from an activity.',
    'body_orientation': 'The generic body-axis contract applies to an explicitly declared body regardless of biology; no rotation is inferred from pose.',
    'light_shape': 'Actual volumetric geometry needs its declared spatial region rather than an invented receiving surface or scattering medium.',
    'relational_action': 'The already stated human/animal/object interaction meaning must not be restricted to human subjects; actual endpoints and self/other ownership remain explicit.',
    'companion_animal': 'An accompanying animal requires an actual relation, while a human primary is not inherent to that relation. Lone animals remain negative.',
    'garment_detail': 'A garment-owned construction role must not invent a human wearer for a standalone/represented garment.',
    'hair_style': 'Explicit wig topology and represented hair need their actual carrier rather than invented living hair or a wearer; fiber sheen alone remains negative.',
    'hair_color': 'Explicit bounded wig color is local appearance, without dye/pigment biology or a compulsory human owner. Intrinsic source restrictions still apply.',
}
delta = save('CATALOG-PROPOSED-144-V3-R02-DELTA.json', {
    'schema': 'photo-root-catalog-proposal/v1', 'actor': '/root', 'status': 'proposal_only',
    'before_count': 142, 'after_count': 144, 'before_sha256': sha(before), 'after_sha256': sha(after),
    'previous_proposal_sha256': sha(previous),
    'changes': [{'pointer': '/' + key, 'before_exists': key in before, 'before': before.get(key),
                 'after_exists': True, 'after': after[key], 'reason': reasons[key]} for key in changed],
    'revision_changes': [{'pointer': '/' + key, 'before': previous[key], 'after': after[key]}
                         for key in sorted(after) if previous[key] != after[key]],
    'source_evidence': evidence, 'whole144_independent_review_complete': False,
    'root_acceptance_written': False, 'canonical_changed': False,
    'source_or_proof_automatic_conversion': False,
})
print(json.dumps({'proposal': proposal, 'source_evidence': evidence, 'delta': delta}))
