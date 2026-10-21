from pathlib import Path
import copy
import re
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from photo_h_f2_query_scope import analyze
from photo_h_f2_event_phase import request, compile_contract, compile_contracts, order_phase
T = lambda s: re.findall(r'[^\W_]+', s.casefold(), re.UNICODE)
Q = 'Photographic role: Show physical traces of a completed operation, rather than an ongoing action.'
POST = 'Post-event residue across a workshop floor'
SETTLING = 'Settling aftereffect phase with a visible residual trace and diminishing motion'
SMOKE = 'A smoke column rising from a just-extinguished candle'
ACTIVE = 'Active tool contact that shows an ongoing process and one immediate visible result'
PEAK = 'The photograph freezes an unstable mid-action instant before the event settles'

class EventPhaseTests(unittest.TestCase):
    def req(self, q):return request(q, analyze(q, T), T)
    def contract(self, text):return compile_contract(text,T)
    def test_prior_residue_with_active_exclusion(self):
        r=self.req(Q);self.assertEqual(r['phase'],'post_event_residue')
        for w in r['positive_witnesses']:self.assertEqual(Q[w['start']:w['end']],w['quote'])
    def test_paraphrase_not_specific_query(self):
        self.assertIsNotNone(self.req('Owned remnants of an earlier action, distinct from an unfinished operation.'))
    def test_explicit_physical_prior_event_needs_no_negative_boilerplate(self):
        self.assertIsNotNone(self.req('Show residue of a completed event.'))
        for q in ['Show a completed action, rather than an ongoing process.', 'Show an ongoing process, rather than physical traces of an earlier action.']:
            self.assertIsNone(self.req(q))
    def test_specific_scene_requires_source_scene_witnesses(self):
        for q in [Q+' Scene context: A kitchen.', Q.replace('physical traces','physical traces on a kitchen table')]:
            req=self.req(q);self.assertEqual(req['owner_scope'],'source_scene_required');self.assertEqual(req['scene_family'],'recipe')
    def test_quoted_or_negated_phase_is_not_a_positive_request(self):
        for q in ['Do not '+Q, 'Discuss "'+Q+'"', Q.replace('Show physical','Show no physical')]:self.assertIsNone(self.req(q))
    def test_mixed_positive_phases_do_not_trigger(self):self.assertIsNone(self.req(Q.replace('traces of','traces and an ongoing process of')))
    def test_post_event_owned_material(self):self.assertEqual(self.contract(POST)['phase'],'post_event_residue')
    def test_settling_and_rising_motion_are_not_initiating_action(self):
        for text in (SETTLING,SMOKE):self.assertEqual(self.contract(text)['phase'],'post_event_residue')
    def test_active_cause_and_unfinished_action(self):
        for text in (ACTIVE,PEAK,'One primary action is visibly underway','An unfinished slow action links the actor to the table'):
            self.assertEqual(self.contract(text)['phase'],'ongoing_action')
    def test_negated_quoted_or_conditional_source_is_not_evidence(self):
        for text in ['Not '+POST,'No '+POST,POST+' is absent',POST+' is missing','Without '+POST,'"'+POST+'"','If '+POST]:self.assertIsNone(self.contract(text))
    def test_comparison_does_not_supply_positive_phase(self):
        self.assertIsNone(self.contract('A tabletop, rather than post-event residue across its surface'))
    def test_negative_aftermath_in_active_source_stays_active(self):
        self.assertEqual(self.contract(PEAK+', rather than post-event residue')['phase'],'ongoing_action')
    def test_labels_cannot_override_primary_meaning(self):
        for d in ['A tabletop photograph\n'+POST,'An actor works at the table. '+POST]:self.assertIsNone(self.contract(d))
    def test_arbitrary_surface_state_is_not_prior_event_evidence(self):
        for text in ['A burned tabletop with physical residue','A preserved irregular surface texture','Before-and-after material residue across a working process']:
            self.assertIsNone(self.contract(text))
    def test_mixed_assertion_is_ambiguous(self):self.assertIsNone(self.contract(POST+' with an unfinished slow action'))
    def test_stable_partition_retains_every_score_and_row(self):
        texts=[ACTIVE,'A tabletop photograph',SETTLING,PEAK,POST,SMOKE]
        rows=[{'id':str(i),'bm25':12-i,'cosine':.8-i/100,'rrf':.1-i/1000} for i in range(len(texts))];old=copy.deepcopy(rows)
        out,trace=order_phase(rows,Q,analyze(Q,T),compile_contracts(dict(zip(map(str,range(len(texts))),texts)),T,source_units=lambda key:[{'pointer':'/content/en','text':texts[int(key)]}]),T)
        self.assertEqual([r['id'] for r in out],['2','4','5','1','0','3']);self.assertTrue(trace['applied']);self.assertEqual(rows,old)
        self.assertEqual({r['id']:r for r in out},{r['id']:r for r in old})
        for cid,c in {**trace['positive'],**trace['conflicting']}.items():
            for key in ('phase_witnesses','material_witnesses','relation_witnesses'):
                for w in c.get(key,[]):self.assertEqual(texts[int(cid)][w['start']:w['end']],w['quote'])
    def test_without_positive_source_retains_original_order(self):
        rows=[{'id':'a'},{'id':'b'}];out,t=order_phase(rows,Q,analyze(Q,T),compile_contracts({'a':ACTIVE,'b':'A tabletop'},T,source_units=lambda key:[{'pointer':'/content/en','text':{'a':ACTIVE,'b':'A tabletop'}[key]}]),T)
        self.assertEqual(out,rows);self.assertFalse(t['applied'])
    def test_unrelated_request_does_not_change_order(self):
        rows=[{'id':'a'},{'id':'b'}];q='A workshop portrait';out,t=order_phase(rows,q,analyze(q,T),compile_contracts({'a':ACTIVE,'b':POST},T,source_units=lambda key:[{'pointer':'/content/en','text':{'a':ACTIVE,'b':POST}[key]}]),T)
        self.assertEqual(out,rows);self.assertFalse(t['applied'])
    def test_already_conforming_keeps_order(self):
        rows=[{'id':'a'},{'id':'b'}];out,t=order_phase(rows,Q,analyze(Q,T),compile_contracts({'a':POST,'b':ACTIVE},T,source_units=lambda key:[{'pointer':'/content/en','text':{'a':POST,'b':ACTIVE}[key]}]),T)
        self.assertFalse(t['applied']);self.assertEqual(out,rows)

if __name__=='__main__':unittest.main()
