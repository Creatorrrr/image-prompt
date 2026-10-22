"""Saved-query regression: descriptive sensory limits must not empty discovery."""
from pathlib import Path
import os,sys,unittest

SKILL=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PHOTO_CAPABILITY_TEST_ROOT',SKILL))/'scripts'))
if not (SKILL/'scripts/photo_recall_first.py').exists():
    from photo_installed_h_f2 import release,default_store,read,CONFIG
    native,_,_=release(default_store(),read(SKILL/CONFIG)['generation_id'])
    sys.path.append(str(native/'scripts'))
import photo_h_f2_query_scope as q
from photo_h_f2_search import present_material
from photo_h_f2_event_phase import RECIPE

class CapabilityClause(unittest.TestCase):
    def material(self,text):
        _,trace=q.order_focus([{'id':'ordinary'}],text,{})
        rows,projection=present_material([{'id':'ordinary'}],{'schema':RECIPE},focus=trace)
        return rows,trace,projection

    def test_actual_science_query_keeps_discovery(self):
        text=('Photographic role: A sealed brainlike specimen in an unfamiliar scientific vessel surrounded by instruments that seem adapted to senses a human observer does not possess.\n'
              'Scene context: A fictional woman observes this apparatus through a laboratory inspection window in an uneasy photographic encounter.')
        rows,trace,_=self.material(text)
        self.assertEqual(rows,[{'id':'ordinary'}])
        self.assertNotIn('unmodeled_restricted_change',(trace.get('request') or {}).get('strict_nonpositive_roles',[]))

    def test_relative_clause_variants_do_not_create_permission_or_native_approval(self):
        for phrase in ['senses that humans do not possess','senses a human operator does not have','senses which a human observer did not possess']:
            with self.subTest(phrase=phrase):
                rows,_,_=self.material('Photographic role: A sealed instrument adapted to '+phrase+'.\nScene context: An observer studies the instrument.')
                self.assertEqual(rows,[{'id':'ordinary'}])

    def test_real_restrictions_still_empty_unproved_material(self):
        for phrase in ['Do not infer its unprovided maker.', 'A human observer does not have an arm.',
                       'Senses a human observer does not possess; do not change the vessel.',
                       'Keep the iris color unspecified; do not change it.',
                       'A creature without eyes.', 'A human observer must not possess the instrument.']:
            with self.subTest(phrase=phrase):
                rows,_,_=self.material('Photographic role: '+phrase+'\nScene context: An existing observer and instrument.')
                self.assertEqual(rows,[])

if __name__=='__main__':unittest.main()
