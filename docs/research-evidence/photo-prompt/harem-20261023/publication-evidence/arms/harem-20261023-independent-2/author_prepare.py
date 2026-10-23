import json, pathlib, hashlib, shutil

r = pathlib.Path(__file__).parent
e = json.loads((r / 'revisions/984406fcb394433ab80130db93b26736/request_envelope_input.json').read_text())
c = json.loads((r / 'revisions/5c14df485714451c8b05a35055ce5952/creative_controls.json').read_text())
cat = pathlib.Path('skills/photo-prompt-image-generator/precore/visual_feature_catalog.json')

b = '''Create a cinematic photographic still of four fictional adults at a sheltered electric-ferry pier in a near-future coastal city, moments after their repair shift has ended. The central character is a woman; the other three are men. The attached portrait guides the central character's face and hair: a short straight dark bob with fine wispy parted fringe, large brown eyes, a softly tapered face, a small nose and natural rosy lips. Her identity and life belong to this fictional scene. She wears an indigo utility jacket unzipped over a simple cream top, carrying her closed tool case at her side. Several suitors show romantic interest in the same recipient, the shared recipient of competing romantic invitations. On her left, a man in a faded ochre overshirt holds a single small flower toward her at chest level, his absorbed gaze meeting her eyes and a hopeful half-smile escaping his composure. On her right, a man in a charcoal work jacket has turned his whole torso toward her, offering a pair of ferry excursion tickets in his open palm, with one ticket clearly intended for himself and the other for her; he watches her with an intimate, anticipatory smile. A third man beside the pier bench has made room next to himself, holding one warm drink for her, then catching sight of the flower with a rueful affectionate smile while still keeping his attention on her. Their invitations converge on her rather than on each other. The overlapping offers make her pause between them: her empty hand hovers halfway toward the flower as she glances toward the ticket holder, cheeks gently warm and a surprised smile suggesting she understands their interest but has not chosen. The flower and tickets remain separate and readable on either side of her torso, with each man's forearm visibly connected to his own hand. The tool case hangs from her other hand clear of the offers. A quiet autonomous ferry waits at the berth behind them, its curved battery housing and narrow cyan docking lights setting the time slightly ahead of the present. Damp decking, a closed maintenance hatch and their tired work clothes make the interruption feel earned after shared work. Frame from mid-thigh upward at conversational eye level, slightly oblique to the pier, keeping all four faces and the two leading offers clearly visible in one plane. Soft amber shelter light catches skin against cool blue dusk and harbor reflections. Let the shared target, contrasting ways of asking, and her suspended response carry a warm romantic-comedy tension, with believable skin, lived-in fabric and restrained cinematic color.'''
b = ' '.join(b.split())
(r / 'baseline_prompt_en.txt').write_text(b + '\n')

core = {
    'contract_version': 'photo-authorial-core/v3',
    'provenance': 'agent_prepack',
    'source_request': e['request_text'],
    'creative_controls_sha256': c['canonical_sha256'],
    'interpreted_intent': 'Requester asks for a randomized image test of the just-discussed harem topic using the attached image. Context resolves the topic as an ensemble with several romantic interests directed at one shared recipient; this is a genre relationship rather than an isolated character personality archetype. I independently chose a reverse-harem configuration with four fictional adults, a late electric ferry after a maintenance shift, and competing personal invitations. Compare a formal celebratory group portrait with an interrupted departure: the latter gives the shared romantic direction, distinct invitations and recipient response a visible cause and consequence. Subtle sensual attraction supports the warmth; fetish=0 and surreal=0 add no extra treatment; creativity=1 keeps the staging close and permits restrained later alternatives. Reference use is my face/hair-only scope choice and supplies neither real identity nor age. Number, gender, adulthood, work roles, gestures, props and near-future setting are replaceable authorial choices. The prior topic link is discovery evidence only, not new requester text or permission.',
    'subject': 'A fictional adult woman and three fictional adult male suitors, using the portrait only for the central face and hair.',
    'setting': 'Sheltered electric-ferry pier in a near-future coastal city at blue dusk.',
    'event': 'End of a repair shift interrupted by competing romantic invitations.',
    'visual_priorities': [
        'Several distinct romantic offers converge on one recipient, rather than general group sociability.',
        'The recipient notices more than one offer and pauses visibly, keeping the choice unresolved.',
        'Separate readable hands, flower and tickets preserve the topology of the interaction.',
        'The quiet waiting ferry and work traces make departure the immediate stake.'
    ],
    'baseline_prompt_en': b,
    'user_definitions': [],
    'interpretation_provenance': [
        {'term': '이번에 반영한 주제', 'source_text': '이번에 반영한 주제', 'basis': 'request_context', 'resolution': 'The elliptical topic is resolved through the actual prior human topic link as harem: multiple romantic interests directed at a shared recipient. No particular count, gender, pose, age, attire or biology is a requester requirement.', 'sources': []},
        {'term': '랜덤한 컨셉', 'source_text': '랜덤한 컨셉', 'basis': 'agent_general_knowledge', 'resolution': 'Select a reproducible random scenario within the assigned broad domain, then independently author its visual relation and preregister pixel criteria.', 'sources': []},
        {'term': '첨부한 이미지를 활용하여', 'source_text': '첨부한 이미지를 활용하여', 'basis': 'request_context', 'resolution': 'Use the supplied portrait as visible appearance reference, choosing a face-and-hair-only scope while authoring a separate fictional scene.', 'sources': []}
    ],
    'unresolved_ambiguities': [],
    'user_exclusions': [],
    'runtime_forbidden_labels': [],
    'intent_lock': {
        'contract_version': 'photo-intent-lock/v2',
        'priority': 'requesting_user',
        'semantic_anchors': [
            {'anchor_id': 'core_concept', 'source_text': '이번에 반영한 주제', 'dimension': 'concept', 'prompt_evidence': 'Several suitors show romantic interest in the same recipient'},
            {'anchor_id': 'core_subject', 'source_text': '주제가 이미지에 실제로 반영되는지', 'dimension': 'subject', 'prompt_evidence': 'the shared recipient of competing romantic invitations'},
            {'anchor_id': 'core_event', 'source_text': '주제가 이미지에 실제로 반영되는지', 'dimension': 'event', 'prompt_evidence': 'The overlapping offers make her pause between them'},
            {'anchor_id': 'reference_used', 'source_text': '첨부한 이미지를 활용하여', 'dimension': 'reference_use', 'prompt_evidence': "The attached portrait guides the central character's face and hair"}
        ],
        'locked_dimensions': ['concept', 'subject', 'event', 'reference_use'],
        'open_dimensions': ['identity', 'count', 'age', 'role', 'species', 'appearance', 'pose', 'body_geometry', 'expression', 'action', 'setting', 'relationship', 'sexual_tone', 'style', 'viewer_outcome', 'text', 'format', 'framing', 'composition', 'lighting', 'camera', 'color', 'material', 'timing', 'atmosphere', 'character_response']
    },
    'semantic_assertions': [
        {'assertion_id': 'camera_axes', 'dimension': 'camera', 'polarity': 'advisory', 'source_span_ids': ['test_request'], 'affected_dimensions': ['camera'], 'axes': {'camera_axis_review': 'camera_axis_review_v1', 'capture_owner': 'unprescribed', 'direction_requirement': 'open', 'height_requirement': 'open'}, 'evidence': {}}
    ],
    'request_lineage': None,
    'style': {'domain': 'cinematic location photography', 'family': 'near-future romantic comedy still', 'evidence': ['warm shelter light against cool harbor dusk', 'believable wet decking and workwear']},
    'variation_key': 'seed-202610230202-ferry'
}
(r / 'authorial_core.input.json').write_text(json.dumps(core, ensure_ascii=False, indent=2) + '\n')

selected = [
    ('feature.situation', 'request_derived', 'The overlapping offers make her pause between them', 'The test needs a romantic interruption that becomes visible at one shutter rather than a group label.', 'The current topic is realized through simultaneous invitations and a recipient pause.'),
    ('feature.interaction', 'request_derived', 'Several suitors show romantic interest in the same recipient', 'The defining relation requires several distinct sources of interest and one common recipient.', 'The current topic calls for a shared romantic recipient; exact gestures remain my staging.'),
    ('feature.subject', 'agent_visual_choice', 'The central character is a woman; the other three are men.', 'An independently chosen reverse-harem cast gives a clear shared recipient without treating gender or count as the request.', None),
    ('feature.action', 'agent_visual_choice', 'holds a single small flower toward her at chest level', 'A personal flower invitation gives one suitor a readily readable romantic vector.', None),
    ('feature.facial_expression', 'agent_visual_choice', 'a rueful affectionate smile', 'The third reaction makes reciprocal awareness and gentle rivalry visible without adding conflict.', None),
    ('feature.location', 'agent_visual_choice', 'at a sheltered electric-ferry pier in a near-future coastal city', 'A departure point gives each invitation urgency and a common reason to remain together.', None),
    ('feature.environmental_details', 'agent_visual_choice', 'its curved battery housing and narrow cyan docking lights', 'One restrained future technology cue anchors the allocated domain while preserving ordinary human interaction.', None),
    ('feature.composition', 'agent_visual_choice', 'keeping all four faces and the two leading offers clearly visible in one plane', 'The projected placement allows target-directed offers and recipient reaction to be judged together.', None)
]
rows = []
for cid, basis, ev, why, der in selected:
    rows.append({'category_id': cid, 'basis': basis, 'source_span_ids': ['test_request'] if basis == 'request_derived' else [], 'source_text': None, 'derivation': der, 'reason': why, 'baseline_evidence': ev})
sel = {'contract_version': 'photo-precore-feature-selection/v1', 'request_id': e['request_id'], 'active_span_ids': ['test_request'], 'catalog_path': str(cat), 'catalog_schema_version': 'photo-precore-feature-catalog/v2', 'catalog_sha256': hashlib.sha256(cat.read_bytes()).hexdigest(), 'request_sha256': e['request_sha256'], 'baseline_prompt_sha256': hashlib.sha256(b.encode()).hexdigest(), 'selected': rows}
(r / 'precore_feature_selection.input.json').write_text(json.dumps(sel, ensure_ascii=False, indent=2) + '\n')
checks = {
    'body_ownership': ("Each visible offer is assigned to one separate suitor; the woman's tool case uses her other hand.", ["with each man's forearm visibly connected to his own hand", 'The tool case hangs from her other hand clear of the offers']),
    'joint_chain_and_reach': ('Chest-level flower and open-palm tickets sit within ordinary flexed forearm reach, with the central free hand between them.', ['holds a single small flower toward her at chest level', 'her empty hand hovers halfway toward the flower']),
    'support_and_balance': ("They stand on the pier while the third is beside a supported bench; no one bears another person's weight.", ['Damp decking, a closed maintenance hatch and their tired work clothes']),
    'contact_and_space': ('Offers are separated on opposite sides, the tool case is lowered, and hands do not need to occupy the same space.', ['The flower and tickets remain separate and readable on either side of her torso', 'The tool case hangs from her other hand clear of the offers']),
    'visibility_and_projection': ('A mid-thigh ensemble view keeps both leading hands and all faces together at comparable depth; the far bench invitation is secondary.', ['Frame from mid-thigh upward at conversational eye level', 'keeping all four faces and the two leading offers clearly visible in one plane'])
}
review = {'contract_version': 'photo-embodiment-review/v1', 'provenance': 'agent_prepack', 'prompt_sha256': hashlib.sha256(b.encode()).hexdigest(), 'scope': 'body_action', 'summary': 'Ordinary adult human bodies on a stable pier; each personal offer has its own owner and target-directed forearm, while the recipient has one free responding hand and one tool-case hand.', 'checks': {k: {'status': 'supported', 'reason': v[0], 'prompt_evidence': v[1]} for k, v in checks.items()}}
(r / 'embodiment_review.input.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
shutil.copyfile(cat, r / 'visual_feature_catalog.snapshot.json')
test = {'schema': 'independent-harem-image-test/v1', 'arm': 2, 'frozen_before_candidate_access': True, 'seed': 202610230202, 'topic_meaning': 'Multiple romantic interest vectors converge on the same identifiable recipient; a group alone is insufficient.', 'hard_topic_gates': [
    {'id': 'shared_target', 'criterion': 'At least two separately identifiable suitors direct personal romantic attention or invitations toward the same identifiable recipient in the actual pixels.'},
    {'id': 'romantic_specificity', 'criterion': 'At least two vectors have mutually reinforcing relational cues such as personal invitation, absorbed gaze, tender expression or affiliative proximity; a generic group smile or service offer alone is insufficient.'},
    {'id': 'recipient_response', 'criterion': 'The shared recipient visibly registers more than one converging offer through directed attention, suspended reach or reaction; the narrative cannot be supplied only by prose.'},
    {'id': 'single_frame_topology', 'criterion': 'The suitors, shared target and carrying offer/attention connections remain visible together in one frame.'}
], 'authorial_checks': [
    {'id': 'near_future_ferry', 'criterion': 'A plausible ferry departure setting with a readable restrained future cue remains visible.'},
    {'id': 'reference_face_hair', 'criterion': 'The recipient visibly resembles the portrait in short dark bob/fringe and facial impression at the available scale; exact identity is neither claimed nor tested.'},
    {'id': 'embodiment', 'criterion': 'Offer hands trace to their owners and separate objects; hands and faces remain inspectable.'}
], 'interpretation_rules': 'Full pass requires every topic gate visible and supported. Partial evidence or author-imagined motive cannot pass a multi-component gate. Authorial checks are reported separately from topic meaning. Candidate exposure, permitted adoption, exact transport, pixels and user acceptance are separate outcomes. Pending user acceptance is not acceptance.', 'controls': {k: v['value'] for k, v in c['controls'].items()}}
(r / 'test-case.frozen.json').write_text(json.dumps(test, ensure_ascii=False, indent=2) + '\n')
print('baseline_words', len(b.split()))
print('baseline_sha256', hashlib.sha256(b.encode()).hexdigest())
print('test_case_sha256', hashlib.sha256((r / 'test-case.frozen.json').read_bytes()).hexdigest())
