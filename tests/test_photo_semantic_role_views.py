"""Synthetic structural bindings; no candidate/source semantic approval."""
import copy
from dataclasses import FrozenInstanceError
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

PATH = Path(__file__).resolve().parents[1] / 'skills/photo-prompt-image-generator/scripts/photo_semantic_role_views.py'
SPEC = importlib.util.spec_from_file_location('isolated_photo_semantic_role_views', PATH)
v = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = v
SPEC.loader.exec_module(v)


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                   separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def fixture(*, mode='effect', role_kind='direct'):
    cid = 'cand_' + '1' * 32
    text = 'Existing actor and existing gavel. The actor announces while holding the gavel. Holding elsewhere is unrelated.'
    facts = [dict(id='actorP', realization_id='base', pointer='/content/en', quote='Existing actor',
                  dimension='subject', target='actor', property='entity.presence', mode='prerequisite',
                  value={'type': 'entity.presence/v1', 'value': 'present'}, requires=[]),
             dict(id='gavelP', realization_id='base', pointer='/content/en', quote='existing gavel',
                  dimension='subject', target='gavel', property='entity.presence', mode='prerequisite',
                  value={'type': 'entity.presence/v1', 'value': 'present'}, requires=[]),
             dict(id='announce', realization_id='base', pointer='/content/en',
                  quote='announces while holding the gavel', dimension='action', target='actor',
                  property='action.announcing', mode=mode,
                  value={'type': 'action.announcing/v1', 'value': 'announcing_while_holding_same_gavel'},
                  requires=['actorP', 'gavelP'])]
    if mode == 'effect':
        facts[-1].update(operation='set_value', receivers=['gavel'])
    unit = dict(realization_id='base', pointer='/content/en', quote=text,
                fact_refs=['actorP', 'gavelP', 'announce'], disposition='semantic')
    spec = dict(id='relational_action', semantic_role=role_kind,
                description='Concrete performed interaction with actual endpoints.',
                dimensions=['relationship'], property_prefixes=['interaction.'],
                includes=['Retain original owners.'], excludes=['Role label alone.'])
    context = dict(candidate_id=cid, actual_realization_ids=['base'], meaning_sha256='2' * 64,
                   catalog_by_id={'relational_action': spec}, facts=facts, source_units=[unit],
                   positive_fields=[dict(realization_id='base', pointer='/content/en', text=text)],
                   closure_snapshot=dict(owner_maps={'base': {'actor': 'independent actor', 'gavel': 'independent gavel'}},
                        effect_sets={'base': {'full_effect': copy.deepcopy(facts[-1])}},
                        guard_sets={'base': {'opaque': ['whole source condition', 'actual owner relation']}},
                        dependencies={'base': []}, profile_contracts={'base': None}, reference_sha256={}))
    facet = 'holding the gavel'
    start = text.index(facet)
    view = dict(schema=v.SCHEMA, id='manual_holding_facet', candidate_id=cid, realization_id='base',
                role_id='relational_action', spec_sha256=digest(spec),
                canonical_fact_refs=[dict(fact_id='announce', fact_sha256=digest(facts[-1]), mode=mode)],
                normal_anchors=[dict(fact_id='announce', pointer='/content/en', source_unit_sha256=digest(unit),
                    full_field_sha256=digest(text), facet_quote=facet, start=start, stop=start + len(facet))],
                endpoint_refs=[dict(fact_id='announce', position='target')], requires_refs=['actorP', 'gavelP'],
                whole_closure_sha256=digest(context['closure_snapshot']),
                manual_semantic_facet='Only holding supports interaction; announcing alone does not.',
                whole_value_retained='Retain the entire announcing/holding value and all permissions.',
                manual_boundary_rationale='No strike, new hand or announcement directed at gavel inferred.')
    if mode == 'effect':
        view['endpoint_refs'].append(dict(fact_id='announce', position='receiver', index=0))
    return context, [view]


def rebound(context, views):
    """Only exact synthetic hash upkeep; not a source/proof semantic converter."""
    facts = {f['id']: f for f in context['facts']}
    for view in views:
        view['spec_sha256'] = digest(context['catalog_by_id'][view['role_id']])
        view['whole_closure_sha256'] = digest(context['closure_snapshot'])
        for ref in view['canonical_fact_refs']:
            ref['fact_sha256'] = digest(facts[ref['fact_id']])
        for anchor in view['normal_anchors']:
            unit = next(u for u in context['source_units'] if u.get('disposition') == 'semantic'
                        and u['pointer'] == anchor['pointer'])
            anchor['source_unit_sha256'] = digest(unit)
            anchor['full_field_sha256'] = digest(unit['quote'])


class ManualRoleViewTests(unittest.TestCase):
    def validate(self, c, views):
        return v.validate_full_views(views, context=c)

    def rejected(self, c, views):
        with self.assertRaises(ValueError):
            self.validate(c, views)

    def test_full_compact_lookup_immutable_inputs_and_original_effect(self):
        c, views = fixture(); before = copy.deepcopy((c, views))
        result = self.validate(c, views)
        receipt = v.compact_views(result, authoritative_contract_sha256=digest(c))
        expected = copy.deepcopy(receipt)  # Independent retained full-validation artifact.
        for source in [result, receipt]:
            support = v.selected_support(source, expected_binding=expected,
                role_id='relational_action', realization_id='base', fact_id='announce')
            self.assertEqual(support['support_kind'], 'manual_semantic_role_view')
            actual = support['fact']
            self.assertEqual(actual['property'], 'action.announcing')
            self.assertEqual(actual['dimension'], 'action')
            self.assertEqual(actual['value'], c['facts'][-1]['value'])
            self.assertEqual(actual['receivers'], ['gavel'])
            self.assertNotIn('eligible', support); self.assertNotIn('qualified', support)
            actual['value']['value'] = 'mutated returned copy'
        self.assertEqual((c, views), before)
        with self.assertRaises(FrozenInstanceError):
            result._payload = b'changed'
        views[0]['manual_semantic_facet'] = 'changed input'
        c['facts'][-1]['value']['value'] = 'changed input'
        self.assertEqual(receipt, v.compact_views(result, authoritative_contract_sha256=result.source_contract_sha256))

    def test_direct_catalog_mismatch_is_explicit_view_not_property_alias(self):
        c, views = fixture()
        self.assertNotIn(c['facts'][-1]['dimension'], c['catalog_by_id']['relational_action']['dimensions'])
        result = self.validate(c, views)
        self.assertEqual(json.loads(result._payload)['bindings'][0]['fact']['property'], 'action.announcing')

    def test_same_mode_actual_p_preservation_context(self):
        for mode, kind in [('prerequisite', 'direct'), ('preservation', 'direct'), ('context', 'contextual')]:
            with self.subTest(mode=mode):
                c, views = fixture(mode=mode, role_kind=kind)
                result = self.validate(c, views)
                self.assertEqual(json.loads(result._payload)['bindings'][0]['fact']['mode'], mode)
        c, views = fixture(mode='context')
        self.rejected(c, views)
        c, views = fixture(mode='preservation')
        c['facts'][-1]['value'] = {'type': 'frozen_property_reference/v1', 'value': 'same'}
        rebound(c, views); self.rejected(c, views)

    def test_mode_value_operation_receivers_pointer_and_fullfact_pins(self):
        mutations = [('value', {'type':'other/v1','value':'different'}), ('mode','context'),
                     ('operation','relocate'), ('target','other'), ('receivers',[]),
                     ('pointer','/content/ko'), ('quote','holding the gavel'), ('requires',[])]
        for key, value in mutations:
            with self.subTest(key=key):
                c, views = fixture(); c['facts'][-1][key] = value
                self.rejected(c, views)

    def test_changed_whole_spec_and_every_closure_section(self):
        c, views = fixture(); c['catalog_by_id']['relational_action']['excludes'].append('new boundary')
        self.rejected(c, views)
        for key in v.CLOSURE_FIELDS:
            with self.subTest(key=key):
                c, views = fixture()
                if key == 'reference_sha256':c['closure_snapshot'][key]['cand_other'] = '4'*64
                else:c['closure_snapshot'][key]['base'] = {'changed':True}
                self.rejected(c, views)

    def test_wrong_cid_rid_fact_digest_or_mode_rejected(self):
        for key, value in [('candidate_id','cand_'+'3'*32), ('realization_id','sibling'), ('spec_sha256','0'*64)]:
            with self.subTest(key=key):
                c, views = fixture(); views[0][key] = value; self.rejected(c, views)
        for key, value in [('fact_id','absent'), ('fact_sha256','0'*64), ('mode','prerequisite')]:
            with self.subTest(key=key):
                c, views = fixture(); views[0]['canonical_fact_refs'][0][key] = value; self.rejected(c, views)

    def test_sibling_fact_even_if_ref_digest_updated(self):
        c, views = fixture(); c['actual_realization_ids'].append('sibling')
        for key in v.CLOSURE_FIELDS - {'reference_sha256'}:c['closure_snapshot'][key]['sibling'] = None
        c['facts'][-1]['realization_id'] = 'sibling'; rebound(c, views)
        self.rejected(c, views)

    def test_facet_cannot_borrow_another_sentence_or_canonical_occurrence(self):
        c, views = fixture(); a = views[0]['normal_anchors'][0]
        a.update(facet_quote='Holding elsewhere', start=c['positive_fields'][0]['text'].index('Holding elsewhere'))
        a['stop'] = a['start'] + len(a['facet_quote']); self.rejected(c, views)
        c, views = fixture(); text = c['positive_fields'][0]['text'] + ' Also holding the gavel.'
        c['positive_fields'][0]['text'] = text; c['source_units'][0]['quote'] = text
        a=views[0]['normal_anchors'][0]; a['start']=text.rindex('holding the gavel');a['stop']=a['start']+len(a['facet_quote'])
        rebound(c, views); self.rejected(c, views)

    def test_exact_anchor_field_unit_offset_and_quote(self):
        for key, value in [('source_unit_sha256','0'*64), ('full_field_sha256','0'*64),
                           ('start',True), ('start',-1), ('stop',9999), ('pointer','/content/ko'),
                           ('facet_quote','unmentioned contact')]:
            with self.subTest(key=key,value=value):
                c, views = fixture(); views[0]['normal_anchors'][0][key]=value; self.rejected(c, views)
        c, views = fixture(); c['source_units'][0]['quote']='holding the gavel'; rebound(c, views)
        self.rejected(c, views)

    def test_reference_nonsemantic_or_missing_directfact_cannot_anchor(self):
        for kind in ['semantic_reference','nonsemantic']:
            with self.subTest(kind=kind):
                c, views = fixture(); c['source_units'][0]['disposition']=kind; self.rejected(c, views)
        c, views = fixture(); c['source_units'][0]['fact_refs'].remove('announce'); rebound(c, views)
        self.rejected(c, views)
        c, views = fixture(); c['positive_fields']=[]; self.rejected(c, views)

    def test_guard_refs_coexist_without_becoming_scalar_fact_support(self):
        c, views = fixture(); c['source_units'][0]['guard_refs']=['actual_relation_guard']; rebound(c, views)
        self.validate(c, views)
        views[0]['canonical_fact_refs'][0]['fact_id']='actual_relation_guard'; self.rejected(c, views)

    def test_whole_requires_closure_and_cycles(self):
        c, views = fixture(); views[0]['requires_refs'].remove('gavelP'); self.rejected(c, views)
        c, views = fixture(); c['facts'][0]['requires']=['gavelP']; rebound(c, views); self.validate(c, views)
        c['facts'][1]['requires']=['actorP']; rebound(c, views); self.rejected(c, views)
        c, views = fixture(); c['facts'][0]['requires']=['absent']; rebound(c, views); self.rejected(c, views)

    def test_all_actual_receivers_required_no_endpoint_override_or_newowner(self):
        c, views = fixture(); views[0]['endpoint_refs'].pop(); self.rejected(c, views)
        c, views = fixture(); views[0]['endpoint_refs'][1]['index']=1; self.rejected(c, views)
        c, views = fixture(); views[0]['endpoint_refs'][0]['target']='invented camera'; self.rejected(c, views)
        c, views = fixture(); views[0]['endpoint_refs'].append(dict(fact_id='actorP',position='target'));self.validate(c, views)
        c, views = fixture(); views[0]['endpoint_refs'].append(dict(fact_id='absent',position='target'));self.rejected(c, views)

    def test_multiple_actual_receivers_cannot_drop_or_reorder(self):
        c, views = fixture(); c['facts'][-1]['receivers'].append('coordinating_other'); rebound(c, views)
        self.rejected(c, views)
        views[0]['endpoint_refs'].append(dict(fact_id='announce',position='receiver',index=1))
        result=self.validate(c, views); receipt=v.compact_views(result,authoritative_contract_sha256=digest(c))
        c['facts'][-1]['receivers'].reverse(); rebound(c, views)
        new=v.compact_views(self.validate(c,views),authoritative_contract_sha256=digest(c))
        with self.assertRaises(ValueError):v.selected_support(new,expected_binding=receipt,role_id='relational_action',realization_id='base',fact_id='announce')

    def test_explicit_caps_and_duplicates(self):
        for field, limit in [('canonical_fact_refs',8),('normal_anchors',8),('endpoint_refs',32)]:
            with self.subTest(field=field):
                c, views = fixture(); views[0][field] *= limit+1; self.rejected(c, views)
        c, views=fixture(); self.rejected(c, views*129)
        c, views=fixture(); self.rejected(c, views*2)
        c, views=fixture(); views[0]['normal_anchors']*=2; self.rejected(c,views)
        c, views=fixture(); views[0]['endpoint_refs']*=2; self.rejected(c,views)
        c, views=fixture(); views[0]['canonical_fact_refs']*=2; self.rejected(c,views)

    def test_exact_accepted_caps_not_silent_truncation(self):
        c, views = fixture()
        many = [dict(copy.deepcopy(views[0]), id='view_' + str(i)) for i in range(128)]
        result = self.validate(c, many)
        self.assertEqual(len(json.loads(result._payload)['bindings']), 128)
        # Eight explicitly anchored canonical refs remain eight unchanged facts.
        c, views = fixture(); base_fact = copy.deepcopy(c['facts'][-1])
        base_ref = copy.deepcopy(views[0]['canonical_fact_refs'][0])
        base_anchor = copy.deepcopy(views[0]['normal_anchors'][0])
        for i in range(1, 8):
            fid = 'effect_' + str(i); fact = dict(copy.deepcopy(base_fact), id=fid)
            c['facts'].append(fact); c['source_units'][0]['fact_refs'].append(fid)
            views[0]['canonical_fact_refs'].append(dict(base_ref, fact_id=fid))
            views[0]['normal_anchors'].append(dict(base_anchor, fact_id=fid))
            views[0]['endpoint_refs'].extend([dict(fact_id=fid, position='target'),
                dict(fact_id=fid, position='receiver', index=0)])
        rebound(c, views)
        self.assertEqual(len(json.loads(self.validate(c, views)._payload)['bindings']), 8)
        c, views = fixture(); c['facts'][-1]['receivers'] = ['receiver_' + str(i) for i in range(31)]
        views[0]['endpoint_refs'] = [dict(fact_id='announce', position='target')] + [
            dict(fact_id='announce', position='receiver', index=i) for i in range(31)]
        rebound(c, views)
        self.assertEqual(len(json.loads(self.validate(c, views)._payload)['bindings'][0]['endpoint_refs']), 32)

    def test_malformed_nested_json_fails_closed(self):
        for path in ['view_rid', 'fact_ref', 'endpoint', 'anchor', 'typed_empty', 'typed_number']:
            with self.subTest(path=path):
                c, views = fixture()
                if path == 'view_rid': views[0]['realization_id'] = []
                elif path == 'fact_ref': views[0]['canonical_fact_refs'][0]['fact_id'] = []
                elif path == 'endpoint': views[0]['endpoint_refs'][0]['fact_id'] = []
                elif path == 'anchor': views[0]['normal_anchors'][0]['pointer'] = []
                elif path == 'typed_empty': c['facts'][-1]['value']['value'] = []
                else: c['facts'][-1]['value']['value'] = 7
                self.rejected(c, views)

    def test_empty_views_do_not_certify_a_role(self):
        c,_=fixture(); result=self.validate(c,[]);receipt=v.compact_views(result,authoritative_contract_sha256=digest(c))
        self.assertIsNone(v.selected_support(result,expected_binding=receipt,role_id='relational_action',realization_id='base',fact_id='announce'))

    def test_compact_without_external_authority_or_recomputed_selfhash_rejected(self):
        c, views=fixture(); result=self.validate(c,views)
        with self.assertRaises(TypeError):v.compact_views(result)
        with self.assertRaises(ValueError):v.compact_views(result,authoritative_contract_sha256='0'*64)
        with self.assertRaises(ValueError):v.compact_views({},authoritative_contract_sha256=digest(c))
        receipt=v.compact_views(result,authoritative_contract_sha256=digest(c));expected=copy.deepcopy(receipt)
        with self.assertRaises(TypeError):v.selected_support(receipt,role_id='r',realization_id='base',fact_id='announce')
        with self.assertRaises(ValueError):v.selected_support(receipt,expected_binding={},role_id='r',realization_id='base',fact_id='announce')
        receipt['bindings'][0]['fact']['value']['value']='forged'
        receipt['receipt_sha256']=digest({k:val for k,val in receipt.items() if k!='receipt_sha256'})
        with self.assertRaises(ValueError):v.selected_support(receipt,expected_binding=expected,role_id='relational_action',realization_id='base',fact_id='announce')

    def test_context_flag_cannot_replace_actual_source_data(self):
        c, views=fixture();c['source_qualified']=True;self.rejected(c,views)
        c, views=fixture();del c['source_units'];self.rejected(c,views)
        c, views=fixture();views[0]['manual_semantic_facet']=' ';self.rejected(c,views)
        c, views=fixture();c['facts'][-1]['value']['value']=float('nan');self.rejected(c,views)

    def test_lookup_scope_exact_and_external_binding_stale(self):
        c, views=fixture();result=self.validate(c,views);receipt=v.compact_views(result,authoritative_contract_sha256=digest(c))
        for role,rid,factid in [('absent','base','announce'),('relational_action','sibling','announce'),('relational_action','base','absent')]:
            self.assertIsNone(v.selected_support(receipt,expected_binding=receipt,role_id=role,realization_id=rid,fact_id=factid))
        expected=copy.deepcopy(receipt);expected['views_sha256']='0'*64
        expected['receipt_sha256']=digest({k:val for k,val in expected.items() if k!='receipt_sha256'})
        with self.assertRaises(ValueError):v.selected_support(receipt,expected_binding=expected,role_id='relational_action',realization_id='base',fact_id='announce')

    def test_structural_manual_assertion_is_not_machine_entailment(self):
        c, views=fixture();views[0]['manual_semantic_facet']='False human assertion: announcing is physical striking.'
        result=self.validate(c,views)
        self.assertIsInstance(result,v.ValidatedViewBindings)
        self.assertNotIn('qualified',json.loads(result._payload))
        # A reviewer must HOLD this false NL assertion. The helper never claims
        # to infer the role from the substring or determine semantic truth.


if __name__ == '__main__':unittest.main()
