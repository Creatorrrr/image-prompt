"""Regression checks for source-bound display-only identifier projection."""
import copy
import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
workflow=types.ModuleType('photo_h_f2_workflow')
workflow.RESEARCH_MEANING_FIELDS={'owners','directed_relations','component_gates'}
with patch.dict(sys.modules,{'photo_h_f2_workflow':workflow}):
    import photo_h_f2_v4_extra_projection as projection

class DisplayIdentifiers(unittest.TestCase):
    def setUp(self):
        self.research={'owners':{'adult1':'first person','adult2':'second person'},
                       'directed_relations':[{'from':'adult1','to':'adult2'}],
                       'component_gates':[{'gate_id':'gate-adult1','owner':'adult1'}]}
        self.record={'id':'cand_example','content':{'research_semantics':self.research},'conditions':{}}
        self.material={'candidate_id':'cand_example','conditions':{},'meaning':'Two people.\n'+projection.MARK+json.dumps(self.research)}
        self.spec={'sha256':projection.digest(self.record),'identifiers':{'adult1':'owner','adult2':'owner','gate-adult1':'gate'},
                   'occurrences':[{'path':['owners','adult1'],'kind':'key','value':'adult1'},
                                  {'path':['owners','adult2'],'kind':'key','value':'adult2'},
                                  {'path':['directed_relations','0','from'],'kind':'value','value':'adult1'},
                                  {'path':['directed_relations','0','to'],'kind':'value','value':'adult2'},
                                  {'path':['component_gates','0','gate_id'],'kind':'value','value':'gate-adult1'},
                                  {'path':['component_gates','0','owner'],'kind':'value','value':'adult1'}]}
    def test_distinct_references_without_changing_source(self):
        before=copy.deepcopy(self.record)
        with patch.dict(projection.MANIFEST,{'cand_example':self.spec}):
            result,evidence=projection.project(self.material,self.record)
        self.assertNotIn('adult1',result['meaning']);self.assertNotIn('adult2',result['meaning'])
        self.assertEqual(self.record,before);self.assertEqual(result['conditions'],{})
        self.assertEqual(set(evidence['reverse_aliases'].values())&{'adult1','adult2'},{'adult1','adult2'})
    def test_source_and_conditions_must_match(self):
        with patch.dict(projection.MANIFEST,{'cand_example':self.spec}):
            bad=copy.deepcopy(self.record);bad['content']['extra']='changed'
            with self.assertRaises(ValueError):projection.project(self.material,bad)
            bad=copy.deepcopy(self.material);bad['conditions']={'requires_adult_context':True}
            with self.assertRaises(ValueError):projection.project(bad,self.record)

if __name__=='__main__':unittest.main()
