"""Focused regressions using the installed expression/projection implementation."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import sys
import unittest

SKILL = Path(__file__).resolve().parents[1]
config = json.loads((SKILL / 'retrieval-runtime.json').read_text())
store = Path(os.environ.get('PHOTO_RUNTIME_STORE') or Path(os.environ.get('XDG_CACHE_HOME', str(Path.home() / '.cache'))) / 'image-prompt/photo-shared-runtime') / 'h-f2-installed'
native = Path(os.environ.get('PHOTO_H_F2_TEST_NATIVE', store / 'generations' / config['native_generation_id']))
sys.path.insert(0, str(native / 'scripts'))
spec = importlib.util.spec_from_file_location('photo_h_f2_queries', SKILL / 'scripts/photo_h_f2_queries.py')
queries = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = queries
spec.loader.exec_module(queries)
import photo_slot_expression as expression
import photo_slot_queries as slot_queries


def fixture():
    topic = 'A glass lighthouse above a frozen lake'
    setting = 'surreal=0'
    raw = topic + '\n' + setting + '\nFor a second image, a red bus. Save both files.'
    core = {'contract_version': 'photo-authorial-core/v3', 'canonical_sha256': 'a' * 64,
            'source_request': raw, 'subject': 'a glass lighthouse', 'user_exclusions': [],
            'baseline_prompt_en': 'A glass lighthouse rises above a frozen lake, its illuminated glass walls reflected across pale ice. At dusk the warm interior light reveals the spiral staircase and the cool blue horizon remains visible through the transparent tower. The tower occupies the left third of a wide photographic frame, with the ice extending toward a distant ridge.',
            'request_binding': {'active_spans': [
                {'span_id': 'topic', 'start': 0, 'end': len(topic), 'text': topic},
                {'span_id': 'settings', 'start': len(topic) + 1, 'end': len(topic) + 1 + len(setting), 'text': setting}]}}
    controls = {'canonical_sha256': 'b' * 64}
    catalog = json.loads((native / 'assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    row = {'status': 'search', 'reason': 'Develop the dusk illumination.',
           'expressive_goal': 'Warm light through the glass tower at dusk.',
           'observable_targets': ['glass tower'], 'owner_relations': [],
           'required_constraints': [], 'preserved_choices': [], 'open_scope': ['lighting'],
           'unknowns': [], 'role_focus': 'warm transmitted light inside a glass lighthouse',
           'scene_context': 'a tower above a frozen lake at dusk', 'language': 'en',
           'grounds': [expression.source_span(core, '/subject', 0, len(core['subject']))],
           'review': {'author': 'Codex', 'rationale': 'Develop light while preserving the frozen subject.'}}
    plan = expression.create(core, controls, catalog, {'lighting': row}, 'An illuminated glass tower above ice.')
    return core, controls, catalog, plan


class WholeSceneQueries(unittest.TestCase):
    def test_slot_text_and_binding_remain_identical(self):
        core, controls, catalog, plan = fixture()
        expected, _, binding = slot_queries.inputs(core, controls, catalog, 'lighting', 'en', expression_plan=plan, recipe=queries.RECIPE)
        result = queries.prepare(core, controls, catalog, plan)
        self.assertEqual(result['slots']['lighting']['text'], expected)
        self.assertEqual(result['slots']['lighting']['binding'], binding)
        self.assertEqual(result['query_scopes'], {'lighting': 'slot', queries.REQUEST_TOPIC: 'request_topic', queries.BASELINE_PROMPT: 'baseline_prompt'})

    def test_topic_uses_only_active_arm_and_removes_settings(self):
        core, controls, catalog, plan = fixture()
        result = queries.prepare(core, controls, catalog, plan)
        self.assertEqual(result['slots'][queries.REQUEST_TOPIC]['text'], core['request_binding']['active_spans'][0]['text'])
        self.assertNotIn('surreal', result['slots'][queries.REQUEST_TOPIC]['text'])
        self.assertNotIn('red bus', result['slots'][queries.REQUEST_TOPIC]['text'])
        self.assertNotIn('Save both', result['slots'][queries.REQUEST_TOPIC]['text'])

    def test_baseline_is_separate_and_complete(self):
        core, controls, catalog, plan = fixture()
        result = queries.prepare(core, controls, catalog, plan)
        self.assertEqual(result['slots'][queries.BASELINE_PROMPT]['text'], core['baseline_prompt_en'])
        self.assertNotEqual(result['slots'][queries.REQUEST_TOPIC]['text'], result['slots'][queries.BASELINE_PROMPT]['text'])

    def test_whole_searches_run_with_zero_searched_slots(self):
        core, controls, catalog, plan = fixture()
        for status in ('not_applicable', 'unresolved'):
            row = copy.deepcopy(plan['slots']['lighting'])
            row.update(status=status, role_focus='', scene_context='', unknowns=['undecided'] if status == 'unresolved' else [])
            alternative = expression.create(core, controls, catalog, {'lighting': row}, plan['overall_intent'])
            self.assertEqual(set(queries.prepare(core, controls, catalog, alternative)['slots']), queries.WHOLE_QUERY_IDS)
        empty = expression.create(core, controls, catalog, {}, plan['overall_intent'])
        self.assertEqual(set(queries.prepare(core, controls, catalog, empty)['slots']), queries.WHOLE_QUERY_IDS)

    def test_exclusions_never_become_positive_search_terms(self):
        core, controls, _, plan = fixture()
        core['user_exclusions'] = ['lighthouse']
        result = queries.whole_scene(core, controls, plan)
        for row in result.values():
            self.assertNotIn('lighthouse', row['text'])
            self.assertFalse(row['binding']['projection']['exclusions_used_as_positive_query'])

    def test_source_changes_refresh_query_binding(self):
        core, controls, _, plan = fixture()
        before = queries.whole_scene(core, controls, plan)
        changed = copy.deepcopy(core)
        changed['baseline_prompt_en'] += ' Thin frost catches the light.'
        after = queries.whole_scene(changed, controls, plan)
        self.assertNotEqual(before[queries.BASELINE_PROMPT]['text_sha256'], after[queries.BASELINE_PROMPT]['text_sha256'])
        self.assertNotEqual(before[queries.REQUEST_TOPIC]['binding'], after[queries.REQUEST_TOPIC]['binding'])

    def test_missing_active_scope_fails_instead_of_searching_other_arms(self):
        core, controls, _, plan = fixture()
        del core['request_binding']
        with self.assertRaisesRegex(ValueError, 'active requester spans'):
            queries.whole_scene(core, controls, plan)

    def test_empty_positive_query_fails_explicitly(self):
        core, controls, _, plan = fixture()
        core['baseline_prompt_en'] = ''
        with self.assertRaisesRegex(ValueError, 'baseline_prompt'):
            queries.whole_scene(core, controls, plan)


if __name__ == '__main__':
    unittest.main()
