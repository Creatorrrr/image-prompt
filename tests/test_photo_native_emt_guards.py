from __future__ import annotations
import copy,unittest
from tests import photo_native_authoring as fixtures
import prompt_generator as g
import photo_global_retrieval as global_search
BASELINE_TAIL = 'The foreground carrier remains clearly distinct from separate background pictures and objects. Continuous body contours, garment surfaces and near-object contact remain readable within the frame. Soft available light describes the local surfaces without hiding their spatial relationships. A steady viewpoint keeps the main actor or physical carrier and its immediate setting readable together.'


OPEN_DIMENSIONS = ['framing', 'composition', 'lighting', 'camera', 'color', 'material', 'atmosphere', 'relationship']


SCENES = [{'name': 'clinical-indoor-care',
  'expected_action': True,
  'requests': {'EN': 'Photograph an adult clinical emergency medical technician in a high-visibility transport '
                     'uniform assessing one adult patient and securing stretcher restraints and a transport '
                     'monitor in an indoor ambulance loading bay.',
               'KO': '실내 구급차 적재 구역에서 고시인성 이송 근무복을 입은 성인 응급구조사가 성인 환자 한 명을 평가하고 들것 고정 장치와 이송 모니터를 연결하는 임상 이송 장면을 '
                     '촬영해줘.'},
  'fields': {'subject': 'one adult clinical emergency medical technician in a high-visibility transport uniform',
             'setting': 'an indoor ambulance loading bay',
             'event': 'the technician assesses one adult patient and secures the stretcher restraints and '
                      'transport monitor',
             'interpreted_intent': 'A photograph preserving the declared primary carrier and foreground action. '
                                   'Requester duties are the declared adult uniformed foreground actor, '
                                   'indoor/outdoor loading location, one adult patient assessment, and the '
                                   'specified restraint/monitor operation. Any before/for-loading wording '
                                   'retained in the EN baseline is an open timing choice, not a requester duty.',
             'baseline_event': 'the technician assesses one adult patient and secures the stretcher restraints '
                               'and transport monitor before ambulance loading',
             'category': 'human',
             'primary_phrase': 'one adult clinical emergency medical technician in a high-visibility transport '
                               'uniform',
             'open_dimensions': ['framing',
                                 'composition',
                                 'lighting',
                                 'camera',
                                 'color',
                                 'material',
                                 'atmosphere',
                                 'relationship',
                                 'timing']},
  'ko_overrides': {'event': 'the technician assesses one adult patient and connects the stretcher restraints and '
                            'transport monitor'},
  'ko_remove': ['baseline_event']},
 {'name': 'clinical-outdoor-care',
  'expected_action': True,
  'requests': {'EN': 'Photograph an adult clinical emergency medical technician in a high-visibility transport '
                     'uniform assessing one adult patient and securing stretcher restraints and a transport '
                     'monitor in an outdoor ambulance loading area.',
               'KO': '야외 구급차 적재 구역에서 고시인성 이송 근무복을 입은 성인 응급구조사가 성인 환자 한 명을 평가하고 들것 고정 장치와 이송 모니터를 연결하는 임상 이송 장면을 '
                     '촬영해줘.'},
  'fields': {'subject': 'one adult clinical emergency medical technician in a high-visibility transport uniform',
             'setting': 'an outdoor ambulance loading area',
             'event': 'the technician assesses one adult patient and secures the stretcher restraints and '
                      'transport monitor',
             'interpreted_intent': 'A photograph preserving the declared primary carrier and foreground action. '
                                   'Requester duties are the declared adult uniformed foreground actor, '
                                   'indoor/outdoor loading location, one adult patient assessment, and the '
                                   'specified restraint/monitor operation. Any before/for-loading wording '
                                   'retained in the EN baseline is an open timing choice, not a requester duty.',
             'baseline_event': 'the technician assesses one adult patient and secures the stretcher restraints '
                               'and transport monitor before ambulance loading',
             'category': 'human',
             'primary_phrase': 'one adult clinical emergency medical technician in a high-visibility transport '
                               'uniform',
             'open_dimensions': ['framing',
                                 'composition',
                                 'lighting',
                                 'camera',
                                 'color',
                                 'material',
                                 'atmosphere',
                                 'relationship',
                                 'timing']},
  'ko_overrides': {'event': 'the technician assesses one adult patient and connects the stretcher restraints and '
                            'transport monitor'},
  'ko_remove': ['baseline_event']},
 {'name': 'plain-indoor-paramedic',
  'expected_action': True,
  'requests': {'EN': 'Photograph an adult paramedic in a high-visibility EMT transport uniform assessing one '
                     'adult patient and securing stretcher restraints and a transport monitor inside an ambulance '
                     'loading bay.',
               'KO': '실내 구급차 적재 구역에서 고시인성 응급구조사 이송 근무복을 입은 성인 구급대원이 성인 환자 한 명을 평가하고 들것 고정 장치와 이송 모니터를 연결하는 모습을 '
                     '촬영해줘.'},
  'fields': {'subject': 'one adult paramedic in a high-visibility EMT transport uniform',
             'setting': 'an indoor ambulance loading bay',
             'event': 'the paramedic assesses one adult patient and secures stretcher restraints and a transport '
                      'monitor',
             'interpreted_intent': 'A photograph preserving the declared primary carrier and foreground action. '
                                   'Requester duties are the declared adult uniformed foreground actor, '
                                   'indoor/outdoor loading location, one adult patient assessment, and the '
                                   'specified restraint/monitor operation. Any before/for-loading wording '
                                   'retained in the EN baseline is an open timing choice, not a requester duty.',
             'baseline_event': 'the paramedic assesses one adult patient and secures stretcher restraints and a '
                               'transport monitor for ambulance loading',
             'category': 'human',
             'primary_phrase': 'one adult paramedic in a high-visibility EMT transport uniform',
             'open_dimensions': ['framing',
                                 'composition',
                                 'lighting',
                                 'camera',
                                 'color',
                                 'material',
                                 'atmosphere',
                                 'relationship',
                                 'timing']},
  'ko_overrides': {'event': 'the paramedic assesses one adult patient and connects stretcher restraints and a '
                            'transport monitor'},
  'ko_remove': ['baseline_event']},
 {'name': 'uniform-wearer-without-care',
  'expected_action': False,
  'requests': {'EN': 'Photograph an adult fashion model displaying a high-visibility EMT transport uniform in a '
                     'studio without performing patient care.',
               'KO': '성인 패션 모델이 실내 스튜디오에서 고시인성 응급구조사 이송 근무복을 보여주는 모습을 촬영해줘. 환자 돌봄 작업은 하지 않아.'},
  'fields': {'subject': 'one adult fashion model wearing a high-visibility EMT transport uniform',
             'setting': 'a plain indoor photography studio',
             'event': 'the model displays the uniform without performing patient care',
             'interpreted_intent': 'A photograph preserving the declared primary carrier and foreground action. '
                                   'The source requires the adult fashion model displaying the named uniform in a '
                                   'studio and excludes that model performing patient care. KO explicitly '
                                   'prescribes an indoor studio. Wearing in the baseline and a plain studio '
                                   'treatment are editable author staging. The care exclusion stays mandatory and '
                                   'actor-scoped; user_exclusions remains unchanged.',
             'category': 'human',
             'primary_phrase': 'one adult fashion model',
             'subject_anchor': 'high-visibility EMT transport uniform',
             'extra_anchors': [{'anchor_id': 'requested_studio',
                                'source_text': 'in a studio',
                                'dimension': 'setting',
                                'target': 'scene',
                                'property': 'location.type',
                                'prompt_evidence': 'photography studio'}],
             'open_dimensions': ['framing',
                                 'composition',
                                 'lighting',
                                 'camera',
                                 'color',
                                 'material',
                                 'atmosphere',
                                 'relationship',
                                 'pose',
                                 'setting']},
  'ko_overrides': {'extra_anchors': [{'anchor_id': 'requested_studio',
                                      'source_text': '실내 스튜디오',
                                      'dimension': 'setting',
                                      'target': 'scene',
                                      'property': 'location.type',
                                      'prompt_evidence': 'indoor photography studio'}]},
  'ko_remove': []},
 {'name': 'printed-clinical-card',
  'expected_action': False,
  'requests': {'EN': 'Photograph a flat paper card carrying a printed clinical EMT patient-transfer picture; the '
                     'physical paper card itself is the subject.',
               'KO': '응급구조사 환자 이송 장면이 인쇄된 평평한 종이 카드를 촬영해줘. 실제 주 피사체는 종이 카드 자체야.'},
  'fields': {'subject': 'one flat paper card displaying a printed clinical EMT patient-transfer picture',
             'setting': 'a plain indoor photography studio',
             'event': 'the paper card carries the printed clinical EMT patient-transfer picture',
             'interpreted_intent': 'A photograph preserving the declared primary carrier and foreground action. '
                                   'The physical flat paper card is the primary photographed subject. Clinical '
                                   'figures and care inside its printed picture do not become primary live actors '
                                   'or live-care duties. The print need not itself be a photograph. Placement, '
                                   'paper-edge cues and the selected studio are editable author staging.',
             'category': 'object',
             'primary_phrase': 'one flat paper card',
             'visual_priorities': ['one paper card',
                                   'the paper card carries the printed clinical EMT patient-transfer picture'],
             'open_dimensions': ['framing',
                                 'composition',
                                 'lighting',
                                 'camera',
                                 'color',
                                 'material',
                                 'atmosphere',
                                 'relationship',
                                 'setting',
                                 'pose']},
  'ko_overrides': {},
  'ko_remove': []},
 {'name': 'background-emt-poster',
  'expected_action': False,
  'requests': {'EN': 'Photograph an adult fashion model in an ordinary sweater in an outdoor courtyard beside a '
                     'separate printed clinical EMT patient-transfer poster. The poster is background, and the '
                     'model stands still.',
               'KO': '별도로 인쇄된 응급구조사 임상 환자 이송 포스터 옆 야외 안뜰에서 평범한 스웨터를 입은 성인 패션 모델이 가만히 서 있는 모습을 촬영해줘. 의료 장면은 배경 포스터 '
                     '안에만 있어.'},
  'fields': {'subject': 'one adult fashion model in an ordinary sweater',
             'setting': 'an outdoor courtyard beside a separate printed clinical EMT patient-transfer poster',
             'event': 'the fashion model stands still',
             'interpreted_intent': 'A photograph preserving the declared primary carrier and foreground action. '
                                   'The adult fashion model in an ordinary sweater is the primary actor, standing '
                                   'still in the outdoor courtyard. The separate printed clinical poster is '
                                   "background, not the model's uniform or live action. Hand position is open. KO "
                                   'explicitly confines the medical scene to that printed poster; no new blanket '
                                   'care ban is inferred for EN.',
             'baseline_tail': ' The separate printed clinical EMT patient-transfer poster remains in the '
                              'background.',
             'category': 'human',
             'primary_phrase': 'one adult fashion model in an ordinary sweater',
             'extra_anchors': [{'anchor_id': 'requested_poster_background',
                                'source_text': 'The poster is background',
                                'dimension': 'relationship',
                                'target': 'poster',
                                'property': 'spatial.layer',
                                'prompt_evidence': 'The separate printed clinical EMT patient-transfer poster '
                                                   'remains in the background'}],
             'open_dimensions': ['framing',
                                 'composition',
                                 'lighting',
                                 'camera',
                                 'color',
                                 'material',
                                 'atmosphere',
                                 'relationship',
                                 'pose']},
  'ko_overrides': {'baseline_tail': ' The separate printed clinical EMT patient-transfer poster remains in the '
                                    'background. Its clinical patient-transfer scene appears only within the '
                                    'printed poster.',
                   'extra_anchors': [{'anchor_id': 'requested_poster_background',
                                      'source_text': '배경 포스터',
                                      'dimension': 'relationship',
                                      'target': 'poster',
                                      'property': 'spatial.layer',
                                      'prompt_evidence': 'The separate printed clinical EMT patient-transfer '
                                                         'poster remains in the background'},
                                     {'anchor_id': 'requested_printed_clinical_scope',
                                      'source_text': '의료 장면은 배경 포스터 안에만 있어.',
                                      'dimension': 'relationship',
                                      'target': 'clinical_scene',
                                      'property': 'representation.carrier',
                                      'prompt_evidence': 'Its clinical patient-transfer scene appears only within '
                                                         'the printed poster'}]},
  'ko_remove': []},
 {'name': 'clinical-nurse-transport-control',
  'expected_action': True,
  'requests': {'EN': 'Photograph an adult clinical nurse in ordinary nursing scrubs assessing one adult patient '
                     'and securing stretcher restraints and a transport monitor for ambulance handover outdoors.',
               'KO': '일반 간호 근무복을 입은 성인 임상 간호사가 야외 구급차 인계 구역에서 성인 환자 한 명을 평가하고 들것 고정 장치와 이송 모니터를 연결하는 모습을 촬영해줘.'},
  'fields': {'subject': 'one adult clinical nurse in ordinary nursing scrubs',
             'setting': 'an outdoor ambulance handover area',
             'event': 'the nurse assesses one adult patient and secures stretcher restraints and a transport '
                      'monitor for ambulance handover',
             'interpreted_intent': 'A photograph preserving the declared primary carrier and foreground action',
             'category': 'human',
             'primary_phrase': 'one adult clinical nurse in ordinary nursing scrubs'},
  'ko_overrides': {'subject': 'one adult clinical nurse in ordinary nursing uniform',
                   'event': 'the nurse assesses one adult patient and connects stretcher restraints and a '
                            'transport monitor',
                   'interpreted_intent': 'A photograph preserving the declared primary carrier and foreground '
                                         'action. Requester duties are the adult clinical nurse, ordinary nursing '
                                         'uniform, the outdoor handover location, one adult patient assessment '
                                         'and connecting the restraints/monitor. No EMT role, high-visibility '
                                         'garment, scrubs-only subtype or numerical apparatus recipe is inferred.',
                   'primary_phrase': 'one adult clinical nurse in ordinary nursing uniform',
                   'open_dimensions': ['framing',
                                       'composition',
                                       'lighting',
                                       'camera',
                                       'color',
                                       'material',
                                       'atmosphere',
                                       'relationship',
                                       'timing']},
  'ko_remove': []}]


def freeze_inputs(scene, language):
    fields = copy.deepcopy(scene["fields"])
    if language == "KO":
        fields.update(copy.deepcopy(scene["ko_overrides"]))
        for name in scene["ko_remove"]:
            fields.pop(name)
    request = scene["requests"][language]
    baseline = (f'A natural photograph shows {fields["subject"]} in {fields["setting"]}. '
        f'In the visible scene, {fields.get("baseline_event", fields["event"])}. '
        + BASELINE_TAIL + fields.get("baseline_tail", ""))
    raw = fixtures.core(request, subject=fields["subject"], setting=fields["setting"], event=fields["event"],
        interpreted_intent=fields["interpreted_intent"],
        visual_priorities=fields.get("visual_priorities", [fields["subject"], fields["event"]]),
        baseline_prompt_en=baseline)
    raw["interpretation_provenance"][0]["resolution"] = "A photograph preserving the declared primary carrier and foreground action"
    raw["semantic_assertions"] = [{"assertion_id": "primary_subject", "dimension": "subject",
        "polarity": "required", "source_span_ids": ["scope_1"], "affected_dimensions": ["subject"],
        "axes": {"subject_category": fields["category"]},
        "evidence": {"subject_phrase": fields["primary_phrase"]}}]
    raw["intent_lock"]["semantic_anchors"] = [
        {"anchor_id": "anchor_concept", "source_text": request, "dimension": "concept",
         "prompt_evidence": "photograph shows"},
        {"anchor_id": "anchor_subject", "source_text": request, "dimension": "subject",
         "prompt_evidence": fields.get("subject_anchor", fields["subject"])},
        {"anchor_id": "anchor_event", "source_text": request, "dimension": "event",
         "prompt_evidence": fields["event"]},
        *copy.deepcopy(fields.get("extra_anchors", [])),
    ]
    raw["intent_lock"]["open_dimensions"] = fields.get("open_dimensions", OPEN_DIMENSIONS)
    controls = g.creative_controls.resolve(request,
        context={"subject_category": "human" if fields["category"] == "human" else "nonhuman"},
        overrides={"sensual": 0, "fetish": 0, "surreal": 0, "creativity": 1}, seed=47)
    raw["creative_controls_sha256"] = controls["canonical_sha256"]
    envelope_raw = fixtures.envelope(request)
    core = g.normalize_authorial_core(raw, request_envelope=g.normalize_request_envelope(envelope_raw),
        creative_control_snapshot=controls)
    return {"raw": raw, "envelope_raw": envelope_raw, "controls": controls, "core": core}


TARGET='cand_466638d1cf1259de8b5fd3cfabbdfb0f'
class NativeEMTGuardTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=g.load_runtime_data()
 def test_clinical_industrial_stillness_and_background_scopes(self):
  for scene in SCENES:
   for language in ('EN','KO'):
    with self.subTest(scene=scene['name'],language=language):
     inputs=freeze_inputs(scene,language)
     allowed,_,_=global_search.eligible(self.data,inputs['core'],inputs['controls'])
     self.assertEqual(TARGET in allowed,scene['expected_action'])
