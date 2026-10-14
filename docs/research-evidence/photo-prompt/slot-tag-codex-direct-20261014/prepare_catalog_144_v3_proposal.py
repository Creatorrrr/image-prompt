"""Serialize root's four explicit taxonomy proposals and read source witnesses.

No candidate role or mode is inferred; no canonical corpus/index is changed.
This is a proposal, not the final catalog review/acceptance. All source witnesses
below were fully displayed and directly read by root before this serialization.
"""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def save(name, value):
    path = HERE / name
    with path.open('xb') as stream:
        stream.write(canonical(value) + b'\n')
    return {'file': str(path.relative_to(ROOT)),
            'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'sha256': hashlib.sha256(canonical(value)).hexdigest()}


before = read(HERE / 'CATALOG-FINAL-142-V2.json')
after = copy.deepcopy(before)
after['thermal_state'] = {
    'id': 'thermal_state',
    'description': 'Explicit physical temperature state or temperature change of an identified carrier, separate from illumination color temperature, emotional warmth and a sensory proxy.',
    'description_ko': '소유자가 명시된 대상의 직접 선언된 물리 온도 상태 또는 온도 변화. 빛의 색온도, 정서적 온기, 열감을 연상시키는 단서와 구별한다.',
    'dimensions': ['material'], 'owners': ['entity'],
    'property_prefixes': ['thermal.state', 'thermal.temperature', 'thermal.process',
                          'material.thermal', 'object.temperature', 'surface.temperature'],
    'semantic_role': 'direct', 'priority': 'support',
    'core_fields': ['subject', 'event', 'setting', 'visual_priorities'],
    'applicability': {},
    'evidence_terms': ['warm', 'hot', 'cold', 'temperature', 'cooling', 'heating', '온도', '식어가는'],
    'includes': [
        'An explicitly warm cup, hot metal or cold surface; its actual carrier must be identified.',
        'Explicit cooling or heating preserves the actual temperature-change meaning, without inventing its mechanism, rate, endpoint or elapsed sequence.',
        'Preserve a stated number and unit literally when both exist in the source; do not infer measurement certification or convert units.',
        'A selected thermal state is an effect; a separately required existing thermal state is a prerequisite; an explicit preservation instruction keeps that same state. Decide each mode from the whole source.',
    ],
    'excludes': [
        'Lighting warm/cool or Kelvin color temperature, emotional warmth/coldness, and skin warm-color cues alone.',
        'Steam, a red appearance, gloss or a sensory proxy alone does not establish actual temperature or a heating cause.',
        'Naming temperature as a measurement variable without a declared state, value or change does not supply a thermal-state fact.',
        'Do not add heaters, flames, particles, melting, burns, chemical identity, a numeric value or a heat-transfer mechanism from a thermal state alone.',
        'Cooling alone does not establish a phase change. Explicit melting/solidification or a selected transformation stage requires its own source-supported fact.',
    ],
    'neighbors': ['surface_material', 'surface_moisture', 'sensory_cue', 'light_color',
                  'prop_state', 'physical_motion', 'transformation_stage', 'atmospheric_medium'],
}
after['surface_moisture'] = {
    'id': 'surface_moisture',
    'description': 'Explicit wetness, dampness, dryness or bounded moisture state of an identified physical surface, distinct from surface material, texture and optical sheen.',
    'description_ko': '소유자가 명시된 물리 표면의 젖음·축축함·건조함 또는 한정된 수분 상태. 재질 정체, 표면 조직, 광택과 구별한다.',
    'dimensions': ['material', 'appearance'], 'owners': ['surface'],
    'property_prefixes': ['surface.moisture', 'surface.wetness', 'material.moisture',
                          'skin.state.wet', 'skin.state.damp', 'garment.state.wet', 'garment.state.damp',
                          'wardrobe.state.wet', 'wardrobe.state.damp'],
    'semantic_role': 'direct', 'priority': 'support',
    'core_fields': ['subject', 'setting', 'visual_priorities'],
    'applicability': {},
    'evidence_terms': ['wet', 'damp', 'dry', 'moisture', '젖은', '축축한', '건조한'],
    'includes': [
        'Explicit wet rock, wet fur or a damp forest floor, with an actual surface carrier and scope.',
        'Actual skin or garment moisture can also support an appropriate skin/garment state role when the complete source independently satisfies that role. Share the supported fact; do not create duplicate owners or effects to obtain another tag.',
        'A dry-to-wet boundary preserves its stated spatial scope. Droplet shape, free-liquid geometry and a condensation process need their separately supported facts.',
        'Choose effect, prerequisite or preservation directly from the whole source; the slot name does not supply the mode.',
    ],
    'excludes': [
        'Gloss, reflectivity, color, roughness or texture alone does not prove moisture; moisture alone does not require gloss.',
        'Air humidity, haze and airborne droplets are not surface wetness without an explicit surface relation.',
        'Do not infer rain, sweat-gland activity, immersion, chemical composition, illness, temperature or a wetting cause from wetness alone.',
        'Do not infer garment transparency, cling, a body region, new anatomy or exposure from damp clothing.',
        'Dry humor, dry color treatment and emotional descriptions do not establish physical dryness.',
    ],
    'neighbors': ['surface_material', 'texture', 'skin_condition', 'garment_state',
                  'environment_detail', 'space_condition', 'liquid_inclusion',
                  'atmospheric_medium', 'thermal_state'],
}
role = after['participant_role']
role.update({
    'description': 'Explicit participation or relational role of a declared participant, whether primary or secondary, without inferring identity, occupation or a new counterpart from appearance.',
    'description_ko': '주·보조 구분 없이 이미 명시된 참여자의 참여상·관계상 역할. 외모에서 정체·직업·관계를 추론하거나 역할 이름만으로 상대역을 추가하지 않는다.',
    'includes': ['A declared participant role can belong to either the primary or another existing participant. The source must identify the actual role carrier and any independently required relation endpoints.'],
    'excludes': ['Off-frame placement, a back view and person count belong to their independently supported framing/count roles.',
                 'A rival/partner label does not itself create another participant or establish actual identity, occupation, disposition or a performed interaction.',
                 'Role truth and tag fit remain separate from effect permission; a prerequisite role cannot authorize a new role or relationship.'],
})
phase = after['narrative_phase']
phase.update({
    'description': 'Selected instant or phase within an explicitly declared human, natural, mechanical or other event, distinct from clock time, a named occasion and inferred chronology.',
    'description_ko': '명시된 인간·자연·기계 등 사건 안에서 선택한 순간이나 단계. 하루 시각·행사 명목과 구별하며 사건의 원인·완료·연속 경과를 추론하지 않는다.',
    'applicability': {},
    'includes': ['Explicit before/after/during relations and selected natural-event phases, including an already declared loading event, rainfall or tide.',
                 'Human participation is not required. Existing source conditions and actual event/carrier identity remain mandatory.',
                 'A procedure operation or material transformation can additionally have its own role; a selected event phase alone does not supply the operation or transformation.'],
    'excludes': ['Clock time, season, historical era and the name of an occasion alone.',
                 'An inferred preceding cause, unmentioned event, completed outcome or elapsed sequence.',
                 'Do not infer rainfall from wetness or a clock time from low tide; a phase requires its explicit source event relation.'],
})
assert len(after) == 144 and set(before) <= set(after)
proposal = save('CATALOG-PROPOSED-144-V3.json', after)
source = read(HERE / 'SOURCE.json.gz')
order = read(HERE / 'ORDER.json')
meanings = {
    368: 'Warm steam has unresolved physical-temperature versus evocation scope; retain as a negative control, not an automatically approved thermal example.',
    439: 'Hot metal is explicit; the action and existing thermal prerequisite/effect choice require individual source review. No red glow or heater is inferred.',
    455: 'A warm thermos cup directly names qualitative thermal state; care tags do not add care actions or contents.',
    1296: 'Warm mug and two-hand holding are distinct actual meanings; no warmth-as-emotion or preexisting-warmth waiver.',
    3519: 'Cold surface and a bounded dry-to-condensed boundary are explicit; original condensation_process condition stays.',
    3628: 'Cooling wax is an actual thermal change; molten state and relief are separate explicit meanings, not a temperature value or mechanism.',
    4353: 'Unfurling after rain explicitly supplies a natural-event temporal relation; droplets in embedding text and growth remain separate clauses.',
    4431: 'Immediately before loading names a selected relation to an actual loading event. Measuring a temperature does not supply a numerical result or a thermal-state value.',
    4441: 'Low tide is an explicit natural-event phase and wet stone is explicit in embedding_text. No clock hour or optical sheen is inferred.',
    4442: 'Wet fur is explicit in embedding_text; animal identity and foraging do not themselves prove wetness, sheen or an earlier immersion event.',
    4452: 'A damp forest floor is explicit, although the original Korean omits damp. No invented sheen or rain cause.',
}
evidence = save('CATALOG-PROPOSED-144-V3-SOURCE-EVIDENCE.json', {
    'schema': 'photo-root-catalog-source-evidence/v1', 'actor': '/root',
    'status': 'proposal_pending_independent_whole_catalog_review',
    'source_sha256': hashlib.sha256(canonical(source)).hexdigest(),
    'root_direct_full_source_reads': [{'ordinal': ordinal, 'candidate_id': order[ordinal],
        'whole_original_record': source['candidates'][order[ordinal]], 'root_meaning': reason}
        for ordinal, reason in meanings.items()],
    'root_direct_full_neighbor_specs_read': {key: before[key] for key in [
        'surface_material', 'texture', 'prop_state', 'sensory_cue', 'light_color',
        'space_condition', 'environment_detail', 'atmospheric_medium', 'skin_condition',
        'garment_state', 'participant_role', 'narrative_phase', 'transformation_stage']},
    'root_participant_role_boundary': 'The142V2 description/includes explicitly restrict another participant. Main actor peer-rival prerequisites in17437 do not fit by generic prefix alone. A deliberately explicit catalog expansion, with no source counterpart invention, requires separate whole-catalog approval.',
    'proposal': proposal,
    'source_corrections_applied': False, 'candidate_tags_assigned': 0,
    'native_proofs_resigned': 0, 'canonical_catalog_changed': False,
    'gemini_calls': 0,
})
deltas = []
reasons = {
    'thermal_state': 'Actual source temperature and cooling meanings lack a physical-state role; do not replace them with color temperature, prop use state or sensory evocation.',
    'surface_moisture': 'Actual wet rock/fur/forest-floor moisture is not material identity, a required optical sheen or surface organization.',
    'participant_role': 'Make participation-role tagging independent of primary/secondary viewpoint while preserving exact carrier/endpoints and every intrinsic adult/domain condition.',
    'narrative_phase': 'Remove unsupported human-only/domain limits from an explicit event-phase definition; retain event identity, original source guards and no inferred chronology.',
}
for key in ['thermal_state', 'surface_moisture', 'participant_role', 'narrative_phase']:
    deltas.append({'pointer': '/' + key, 'before_exists': key in before,
                   'before': before.get(key), 'after_exists': True,
                   'after': after[key], 'reason': reasons[key]})
delta_ref = save('CATALOG-PROPOSED-144-V3-DELTA.json', {
    'schema': 'photo-root-catalog-proposal/v1', 'actor': '/root',
    'status': 'proposal_only', 'before_count': 142, 'after_count': 144,
    'before_sha256': hashlib.sha256(canonical(before)).hexdigest(),
    'after_sha256': hashlib.sha256(canonical(after)).hexdigest(),
    'changes': deltas, 'source_evidence': evidence,
    'whole144_independent_review_complete': False,
    'root_acceptance_written': False, 'canonical_changed': False,
    'source_or_proof_automatic_conversion': False,
})
print(json.dumps({'proposal': proposal, 'evidence': evidence, 'deltas': delta_ref}, ensure_ascii=False))
