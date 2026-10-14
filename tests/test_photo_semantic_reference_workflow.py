"""Reference-unit evidence survives actual lazy packs and fresh runtime audit."""
import copy
import unittest
from unittest import mock

import tests.test_photo_native_joint_assignments as joint
from tests.test_photo_semantic_evidence import reattest


class SemanticReferenceWorkflowTests(unittest.TestCase):
    def check_reference_pack(self, required):
        original_pair = joint.pair

        def with_reference(**kwargs):
            data = original_pair(**kwargs)
            parent = data['candidates'][joint.P]
            before = copy.deepcopy(parent['content']['role_evidence']['effect_sets'])
            text = 'Keep this selected cracked texture readable on the same existing surface.'
            parent['content']['render_gates'] = [text]
            joint.seal(data, {'texture': ['cracks']}, cid=joint.P)
            proof = parent['content']['role_evidence']
            proof['source_units'] = [unit for unit in proof['source_units']
                                     if unit['pointer'] != '/content/render_gates/0']
            proof['source_units'].append({
                'realization_id': 'base', 'pointer': '/content/render_gates/0', 'quote': text,
                'fact_refs': ['cracks'], 'disposition': 'semantic_reference',
                'reference_relation': 'selected_output_constraint',
                'retained_constraint_rationale': 'The selected texture must remain readable on the same surface. '
                    'Its complete cracked value is independently grounded in the direct EN unit; '
                    'this local reference adds no effect or permission.'})
            reattest(data, cid=joint.P)
            joint.c.validate(data)
            self.assertEqual(len([unit for unit in proof['source_units']
                                  if unit['disposition'] == 'semantic_reference']), 1)
            self.assertEqual(before, parent['content']['role_evidence']['effect_sets'])
            return data

        # The existing complete harness constructs a real sharded/lazy runtime,
        # retrieves a sealed public pack with synthetic fixed vectors, checks
        # conflicting and disjoint mappings, and audits fresh render requests.
        # This is code-path evidence, not real corpus/model or pixel evidence.
        case = joint.JointPublicPackTests()
        try:
            with mock.patch.object(joint, 'pair', side_effect=with_reference):
                case.check_pack(required)
        finally:
            case.doCleanups()

    def test_independent_reference_source_public_pack_and_fresh_runtime(self):
        self.check_reference_pack(False)

    def test_reference_parent_required_child_public_pack_and_fresh_runtime(self):
        self.check_reference_pack(True)


if __name__ == '__main__':
    unittest.main()
