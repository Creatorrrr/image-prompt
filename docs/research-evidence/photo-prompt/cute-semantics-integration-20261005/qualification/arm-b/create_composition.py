import copy
import datetime
import hashlib
import json
from pathlib import Path

B = Path(__file__).parent
pack = json.loads((B / 'candidate_pack.json').read_text())[0]
core = pack['authorial_core']
lock = core['intent_lock']
prompt = core['baseline_prompt_en']
envelope = json.loads((B / 'request_envelope.json').read_text())

clarification_reasons = {
    'aircraft_pilot_operation': 'There is no cockpit, flight control or aircraft operation in the festival scene.',
    'composite_overwhelmed_expression': 'The chosen wink and smile have neither upward pupils nor a tongue crossing the lips; this compound meaning would change the fixed facial test.',
    'contained_affect_self_presentation': 'An open celebratory smile and playful paws do not establish controlled presentation plus an interrupted self-regulation action; pooled tears alone are insufficient.',
    'embodied_corruption_transition': 'No unfinished body-darkening boundary or former identity transition belongs to the ordinary festival scene.',
    'hands_free_supported_drink_load': 'The background kettle is not a cup balanced against the subject torso; the required load would change the chosen hand and body moment.',
    'kuudere_composed_warmth_relation': 'There is no trusted counterpart, practical support action or same-target helpful consequence, and the expression is openly celebratory.',
    'rectangle_silhouette_relation': 'A body-width classification does not contribute to the face, hand and cuff moment or the frozen keyword test.',
    'uncanny_coherence_mismatch': 'Adding a local realism mismatch would undermine the ordinary scene and its articulation and expression test.',
}
clarifications = []
for row in pack['semantic_clarification']['candidates']:
    required = row['applicability']['status'] == 'required'
    decision = {
        'clarification_id': row['id'],
        'decision': 'applied' if required else 'rejected',
        'rationale': 'Preserve the frozen broad photograph, reference-guided fictional adult, visible moment and authorized face/hair reference scope; agent-owned keyword staging remains an external testcase.' if required else clarification_reasons[row['profile_id']],
    }
    if required:
        decision['prompt_evidence'] = 'One complex photographic scene presents a reference-guided fictional adult woman in a single visible moment'
    clarifications.append(decision)

creative_reasons = {
    'augmentation:adult_appeal:sensual:face_shape_relation:u_rounded_lower_face_relation': 'Broadening the lower jaw would redesign the authorized reference-guided tapered face rather than improve the celebration photograph.',
    'slot:shot_scale:pr_camera_distance_subject_scale_candidate': 'The independent baseline already supplies a coherent conversational mid-thigh crop and festival margin; a transformed framing detail would add nothing useful.',
    'slot:hand_pose:pv_prayer_palms': 'Palm-to-palm contact and extended fingers compete with the separately drooping curled paws and would erase the frozen gesture test.',
    'slot:eye_makeup_line:sff_pro_m09': 'A lower-lash color bridge could compete with the pooled-tear boundary and adds no useful festival relation.',
    'slot:expression:ae_squinch': 'Both eyes remaining open contradicts the frozen one-closed-eye wink.',
}
creative = [{'candidate_id': row['id'], 'decision': 'rejected', 'rationale': creative_reasons[row['id']]} for row in pack['creative_augmentation']['candidates']]

context = [
    {
        'candidate_id': 'augmentation:adult_appeal:sensual:expression:ae_smolder_attraction',
        'reading': 'potential',
        'reason': 'An explicitly flirtatious open-eye target can add supporting adult attraction, but gaze duration cannot be inferred from a still.',
        'proposed_application': 'Retain the wink, wet open lower lid and smile while the open eye addresses the conversational camera as a quiet flirting cue.',
        'requirement_evidence': [],
    },
    {
        'candidate_id': 'augmentation:adult_appeal:sensual:garment_detail:pfe_one_shoulder_candidate',
        'reading': 'potential',
        'reason': 'One asymmetrical knit shoulder support can express subtle attraction while retaining both long cuffs.',
        'proposed_application': 'Let the rust knit rest on one shoulder and slope below the other through one continuous diagonal edge, keeping cuffs at the finger bases.',
        'requirement_evidence': [],
    },
    {
        'candidate_id': 'augmentation:adult_appeal:sensual:wardrobe_style:athletic_unitard_continuous_one_piece',
        'reading': 'irrelevant',
        'reason': 'A sports one-piece can carry supporting adult appeal, but it contributes less scene-specific material interest than the ribbed knit cuffs in this ordinary neighborhood celebration.',
        'proposed_application': 'Decline the sports one-piece direction in this photograph.',
        'requirement_evidence': [],
    },
    {
        'candidate_id': 'augmentation:adult_appeal:sensual:face_shape_relation:u_rounded_lower_face_relation',
        'reading': 'conflicting',
        'reason': 'A broader rounded jaw changes the observed tapered facial proportions and weakens the authorized reference use.',
        'proposed_application': 'Preserve the visible reference-guided jaw shape.',
        'requirement_evidence': [],
    },
]

embodiment = copy.deepcopy(json.loads((B / 'embodiment_review.json').read_text()))
embodiment['provenance'] = 'agent_postcomposition'
embodiment['summary'] = 'Re-reviewed the complete unchanged final photograph after candidate review. The selected wink bundle confirms the independently authored eye states. Both arms remain free for paws, cuffs preserve decisive fingertips, the step supports the subject, and hands do not cover the wet open lower lid. No extra positive runtime prose is added.'
embodiment['prompt_sha256'] = hashlib.sha256(prompt.encode()).hexdigest()

wink_phrase = 'She gives a soft, unmistakable smile, her right eye visibly winking closed while her left eye remains open'
composed = {
    'contract_version': 'photo-composed-prompt/v1',
    'pack_id': pack['pack_id'],
    'composer': 'agent',
    'prompt_en': prompt,
    'negative_en': pack['negative_en'],
    'core_retrieval_sha256': pack['core_retrieval']['canonical_sha256'],
    'chosen_candidate_ids': ['bundle:cv_bundle_wink'],
    'chosen_visual_concept_ids': [],
    'coverage_assertions': {
        row['prompt_evidence']: row['prompt_evidence'] for row in lock['semantic_anchors']
    },
    'candidate_interpretations': [{
        'candidate_id': 'bundle:cv_bundle_wink',
        'artistic_interpretation': 'One closed and one open eye coexist on the same smiling fictional adult; the complete wink meaning leaves the independent wet-eye and paw scene intact.',
        'transformation': 'Retain actor-right closed lid and actor-left open wet eye in the celebration state; independently authored subject-side wording makes ownership explicit.',
        'prompt_evidence': wink_phrase,
        'component_evidence': {'component_1': 'her right eye visibly winking closed', 'component_2': 'her left eye remains open'},
        'relation_evidence': {'owner_scope': wink_phrase},
    }],
    'semantic_clarification_decisions': clarifications,
    'creative_augmentation_brief': {'decisions': creative},
    'semantic_assertion_evidence': {
        'source_contract_sha256': pack['semantic_assertion_obligations']['canonical_sha256'],
        'evidence': {row['assertion_id']: row['frozen_evidence'] for row in pack['semantic_assertion_obligations']['obligations']},
    },
    'authorial_core_binding': {
        'source_authorial_core_sha256': core['canonical_sha256'],
        'source_intent_lock_sha256': lock['canonical_sha256'],
        'preserved_anchor_ids': [row['anchor_id'] for row in lock['semantic_anchors']],
        'preserved_evidence': [],
        'authorial_decisions': [],
    },
    'embodiment_review': {'source_contract_sha256': pack['embodiment_preflight']['canonical_sha256'], 'review': embodiment},
    'adult_appeal_brief': {
        'adult_subject_phrase': 'a reference-guided fictional adult woman',
        'agency_phrase': 'She gives a soft, unmistakable smile',
        'axes': {
            'sensual': {
                'intensity': 1, 'realization': 'baseline', 'affected_dimensions': [],
                'artistic_interpretation': 'The close viewer relationship, voluntarily playful gaze, relaxed scoop neckline and knit texture give supporting human attraction while the celebration and tested forms remain focal. This retains the initial direction.',
                'prompt_evidence': 'meeting the viewer with a playful, intimate presence',
            },
            'fetish': {
                'intensity': 0, 'realization': 'baseline', 'affected_dimensions': [],
                'artistic_interpretation': 'No added fetish direction is selected; the cuffs remain the independently tested garment form.',
                'prompt_evidence': '',
            },
        },
        'blend': {'emphasis': 'sensual_led'},
        'contextual_review': context,
        'contextual_comparison': 'At sensual 1, both the baseline and an asymmetrically supported knit garment can carry subtle human attraction with the cuffs retained. The diagonal exposure becomes another competitor beside tears, fingertips and sleeve boundaries. Quiet flirting can preserve the eye states, but explicit flirting shifts the celebration toward an attraction performance. The athletic one-piece provides less local material interest, and jaw reshaping weakens reference scope. Retain the complete baseline for the most coherent festival moment; none of these adult candidates is adopted.',
    },
}

(B / 'composed_prompt.json').write_text(json.dumps(composed, ensure_ascii=False, indent=2) + '\n')
(B / 'final_prompt.txt').write_text(prompt + '\n')
(B / 'semantic_self_review.json').write_text(json.dumps({
    'contract_version': 'bounded-semantic-self-review/v1',
    'reviewed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'prompt_sha256': embodiment['prompt_sha256'],
    'required_contradictions': [],
    'testcase_keywords_preserved': ['보케', '고양이 앞발', '윙크', '눈물 고임과 미소', '모에소데'],
    'candidate_review': 'Complete compatible wink bundle retained; unrelated compounds and conflicting hand/eye choices rejected.',
    'remaining_native_questions': 'All five forms still require native pixels, especially liquid tears versus catchlight and long cuff coverage versus readable hand curls.',
    'user_acceptance': 'pending',
}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'pack_id': pack['pack_id'], 'chosen_candidate_ids': composed['chosen_candidate_ids'], 'prompt_sha256': embodiment['prompt_sha256']}))
