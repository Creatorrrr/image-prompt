"""Bounded authored-data regressions, not rendered-image quality claims."""
from pathlib import Path
import hashlib
import json
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as generator
EVIDENCE=ROOT/'docs/research-evidence/photo-prompt/scene-data-cleanup-20261001'

class DataCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=generator.load_json(ROOT/'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')
    def row(self,slot,eid):
        return next(x for x in self.data['slots'][slot] if x['id']==eid)

class SceneLocationCleanupTests(DataCase):
    def test_physical_location_captions_keep_authored_specialized_associations(self):
        e=self.row('location','mountain_valley_stream_spring')
        self.assertIn('Korean mountain valley stream in spring',e['embedding_text'])
        self.assertIn('pine trees',e['embedding_text'])
        self.assertNotIn('full-body',e['embedding_text'])
        self.assertIn('hanbok',e['tags'])
        e=self.row('location','pure_black_flash_backdrop')
        self.assertIn('harsh direct flash falloff',e['embedding_text'])
        self.assertNotIn('close portrait',e['embedding_text'])
        self.assertIn('gothic',e['tags'])
    def test_floral_room_indexes_positive_room_evidence(self):
        e=self.row('location','sunlit_floral_room')
        self.assertIn('flowers',e['embedding_text'])
        self.assertIn('soft daylight',e['embedding_text'])
        self.assertNotIn('church',generator.semantic_text_for_entry(e,'location'))
        self.assertNotIn('priest',generator.semantic_text_for_entry(e,'location'))
        self.assertIn('bridal',e['tags'])
    def test_switchboard_keeps_real_connections_and_half_plugged_state(self):
        e=self.row('location','switchboard_room')
        self.assertEqual(e['ko'],'구식 전화 교환실')
        self.assertIn('half-plugged',e['embedding_text'])
        self.assertNotIn('magic',e['embedding_text'])
    def test_welding_korean_fields_preserve_sparks_without_human_guard(self):
        e=self.row('location','welding_workshop_pit')
        self.assertEqual(e['ko'],'불꽃이 튀는 용접 작업장 피트')
        self.assertEqual(e['phrase_ko'],'불꽃이 튀는 용접 작업장 피트에서')
        self.assertEqual(e['en'],'a welding workshop pit with sparks')
        self.assertNotIn('for_any',e)

class ScenePropCleanupTests(DataCase):
    def test_coffee_gesture_is_preserved_in_both_languages(self):
        e=self.row('prop','two_coffee_cups_prop')
        self.assertIn('관객에게 건네는',e['ko'])
        self.assertEqual(e['en'],'two coffee cups, one offered to the viewer')
        self.assertEqual(e['embedding_text'],e['en'])
        self.assertIn('gift',e['tags'])
    def test_shared_umbrella_keeps_two_people_and_transparency(self):
        e=self.row('prop','shared_umbrella_two_prop')
        self.assertEqual(e['en'],'a transparent umbrella shared by two people')
        self.assertEqual(e['embedding_text'],e['en'])
        self.assertEqual(e['ko'],'둘이 쓰는 투명 우산')
        self.assertNotIn('viewer',generator.semantic_text_for_entry(e,'prop'))
    def test_genealogy_records_content_not_proof_of_subject_identity(self):
        e=self.row('prop','dynastic_genealogy_book_prop')
        self.assertIn('recording royal lineage',e['embedding_text'])
        self.assertNotIn('proving',e['embedding_text'])
        self.assertIn('royal',e['tags'])
    def test_diary_preserves_blank_or_marked_alternatives(self):
        e=self.row('prop','unreadable_diary_prop')
        self.assertIn('blank pages or non-legible notes',e['en'])
        self.assertIn('blank or bear non-legible',e['embedding_text'])
        self.assertIn('blank diary',e['aliases'])
        self.assertIn('no_text_required',e['tags'])
        self.assertIn('no readable text',e['embedding_text'])
    def test_cafe_and_laundry_owner_state_relations_remain(self):
        e=self.row('action','ed_cafe_pickup_wait_candidate')
        self.assertIn("service side, apart from the customer's hands",e['embedding_text'])
        self.assertIn('route for handoff is open',e['concept_units'])
        e=self.row('action','ed_laundromat_transfer_candidate')
        self.assertIn('cloth, hand and basket follow one reachable transfer path',e['embedding_text'])
        self.assertIn('basket sits stably near the machine',e['embedding_text'])

class SceneContextCleanupTests(DataCase):
    def test_after_sunset_blue_hour_is_dusk_not_dawn(self):
        e=self.row('time_of_day','time_blue_hour')
        self.assertEqual(e['facets']['time_of_day'],['dusk'])
        self.assertIn('after sunset',e['en'])
        self.assertNotIn('blue',e['aliases'])
        self.assertIn('blue hour after sunset',e['aliases'])
        self.assertEqual(self.row('time_of_day','civil_twilight')['facets']['time_of_day'],['dawn','dusk'])
    def test_event_phase_does_not_fabricate_clock_time(self):
        for eid in ['pre_open_setup_hour','post_event_empty_hour']:
            self.assertNotIn('time_of_day',self.row('time_of_day',eid).get('facets',{}))
        self.assertIn('before visitors arrive',self.row('time_of_day','pre_open_setup_hour')['en'])
        self.assertIn('after people have left',self.row('time_of_day','post_event_empty_hour')['en'])
    def test_storm_caption_retains_weather_and_existing_context_guard(self):
        e=self.row('weather','storm_window_rain')
        self.assertEqual(e['embedding_text'],'storm rain beating against a window')
        self.assertIn('horror',e['tags'])
        self.assertTrue(e['requires_any_tags'])
    def test_empty_surroundings_do_not_require_or_forbid_a_primary_person(self):
        e=self.row('crowd_density','empty_deserted_space')
        self.assertEqual(e['ko'],'군중 없이 텅 빈 주변 공간')
        self.assertEqual(e['phrase_ko'],'주변 공간이 텅 비어 군중이 보이지 않는 배열로')
        self.assertNotIn('for_any',e)
    def test_depth_and_occlusion_relations_remain(self):
        e=self.row('composition','three_plane_depth_chain')
        self.assertIn('one continuous space',e['embedding_text'])
        self.assertIn('coherent occlusion and scale change',e['embedding_text'])
        e=self.row('composition','occlusion_continuity_lock')
        self.assertIn('hidden and revealed subject edges remain physically consistent',e['embedding_text'])

class ScenePreservationTests(DataCase):
    def test_prior_twenty_three_edited_rows_are_byte_semantically_preserved(self):
        evidence=json.loads((EVIDENCE/'baseline-preservation.json').read_text())
        self.assertEqual(len(evidence['prior_23_rows']),23)
        # Pose and its later acting overlay add equivalent reviewed context.
        # Keep the historical source hash and separately protect its live meaning.
        filenames=tuple(name for name in generator.RESEARCH_EXTENSION_FILENAMES
                        if name not in {'photo_prompt_pose_vocabulary_extension.json',
                                        'photo_prompt_acting_expression_extension.json',
                                        'photo_prompt_neutral_expression_extension.json'})
        with patch.object(generator,'RESEARCH_EXTENSION_FILENAMES',filenames):
            source=generator.load_json(ROOT/'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')
        for record in evidence['prior_23_rows']:
            row=next(item for item in source['slots'][record['slot']] if item['id']==record['id'])
            actual=hashlib.sha256(json.dumps(row,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
            self.assertEqual(actual,record['sha256'],record['id'])
            current=self.row(record['slot'],record['id'])
            additive_fields={'paraphrases','contextual_usage'}
            self.assertEqual({k:v for k,v in current.items() if k not in additive_fields},
                             {k:v for k,v in row.items() if k not in additive_fields},record['id'])
            self.assertTrue(set(row.get('paraphrases',[])) <= set(current.get('paraphrases',[])))
    def test_frozen_inventory_and_queries_remain_bound(self):
        source=(EVIDENCE/'frozen-inventory-queries.json').read_bytes()
        self.assertEqual(hashlib.sha256(source).hexdigest(),(EVIDENCE/'frozen-sha256.txt').read_text().split()[0])
        f=json.loads(source)
        self.assertEqual(len(f['inventory']),32)
        self.assertEqual(len(f['queries']),42)
        self.assertEqual(f['incremental_baseline_hash'],'c464aca9b1547ca965e91a0063082234d9df2ad0216f87409b65058060632f4b')

if __name__=='__main__':unittest.main()
