"""B1 synthetic address-resolution tests, not source/native/consumer approval."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0,str(SCRIPTS))
import photo_native_owner_resolution as r
n=r.witnesses


def assertion(aid,kind,**axes):
    return {'assertion_id':aid,'dimension':'subject','polarity':'required','source_span_ids':['scope'],
        'axes':{'native_schema':n.SCHEMA,'kind':kind,**axes},'evidence':{'owners':'All named owners are independently present'},
        'affected_dimensions':['subject']}


def reseal(core):
    core.pop('canonical_sha256',None);core.pop('core_id',None)
    core['canonical_sha256']=r.digest(core);core['core_id']=core['canonical_sha256'][:16]
    return core


def core(*,exact=True,scoped=True,members=('coat_A','glove_A'),additional=()):
    owners=list(dict.fromkeys([*members,'holder_A','image_A','scene_A',*additional]))
    text='All named owners are independently present: '+', '.join(owners)+'. The complete local collection consists of '+', '.join(members)+'.'
    sha=hashlib.sha256(text.encode()).hexdigest()
    inputs={'schema':n.INPUT_SCHEMA,'complete':True,'items':[{'id':'request','kind':'request_text','sha256':sha},
        {'id':'independent_image','kind':'reference_image','sha256':hashlib.sha256(b'explicit isolated fixture image bytes').hexdigest()}]}
    binding={'request_sha256':sha,'request_envelope_sha256':'e'*64,
        'active_spans':[{'span_id':'scope','text':text,'start':0,'end':len(text)}]}
    if scoped:binding['input_inventory']=inputs
    rows=[]
    for i,owner in enumerate(owners):
        rows += [assertion('owner_'+str(i),'owner',owner=owner,owner_kind='independently_declared_entity'),
            assertion('presence_'+str(i),'fact',owner=owner,property='entity.presence',value_type='entity.presence/v1',value='present')]
    for role,owner in [('main_subject','holder_A'),('image','image_A'),('scene','scene_A')]:
        rows.append(assertion('role_'+role,'role',role=role,owner=owner))
    if scoped:
        inventory={'schema':n.MEMBER_SCOPE_SCHEMA,'complete':True,'state':'known_present','input_binding':n.input_binding(binding),
            'reviewed_input_ids':[item['id'] for item in inputs['items']],
            'members':[{'owner_id':owner,'source_span_ids':['scope'],'source_input_ids':['request']} for owner in members]}
        rows.append(assertion('collection','existing_member_scope',scope_id='local_members',inventory=n.canonical(inventory)))
    result={'contract_version':'photo-authorial-core/v3','source_request':text,'baseline_prompt_en':text,
        'semantic_assertions':rows,'request_binding':binding,
        'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['concept','subject','identity','age','event'],
                       'open_dimensions':['material','appearance','role','composition','camera'],'semantic_anchors':[]}}
    return reseal(result) if exact else result


def frozen(value):
    return n.read(value['semantic_assertions'],value['request_binding']['active_spans'],value['baseline_prompt_en'],
        intent_lock=value['intent_lock'],request_binding=value['request_binding'])


def fixed(target='point',role='main_subject'):
    return {'target':target,'origin':'existing','selection':{'kind':'fixed_role','role':role}}


def selected(target='point',owner='coat_A'):
    return {'target':target,'origin':'existing','selection':{'kind':'selected_existing_owner','owner_id':owner}}


def scope_binding(value,target='members',sid='local_members'):
    scope=next(item for item in frozen(value)['member_scopes'] if item['scope_id']==sid)
    return {'target':target,'origin':'existing','selection':{'kind':'existing_member_scope','scope_id':sid,
        'scope_sha256':r.digest(scope),'target_semantics':'each_member','receiver_semantics':'all_members'}}


def fact(fid='gloss',target='members',*,mode='effect',value='glossy',prop='surface.optical_response',
         dim='material',operation='set_value',receivers=(),requires=()):
    row={'id':fid,'realization_id':'base','mode':mode,'dimension':dim,'target':target,'property':prop,
         'value':{'type':prop+'/v1','value':value},'requires':list(requires)}
    if mode=='effect':row.update(operation=operation,receivers=list(receivers))
    return row


def node(bindings,facts,*,cid='source_A',guards=(),children=()):
    row={'candidate_id':cid,'realization_id':'base','meaning_sha256':hashlib.sha256((cid+' meaning').encode()).hexdigest(),
        'qualification_sha256':hashlib.sha256((cid+' manually prechecked fixture projection').encode()).hexdigest(),
        'bindings':copy.deepcopy(bindings),'guard_only_targets':list(guards),'facts':copy.deepcopy(facts),
        'selected_children':copy.deepcopy(list(children))}
    return seal_node(row)


def seal_node(row):
    row['projection_sha256']=r.node_digest(row);return row


def edge(child,selection='required'):
    return {key:child[key] for key in ('candidate_id','realization_id','meaning_sha256','qualification_sha256','projection_sha256')}|{'selection':selection}


def projection(value,nodes,*,roots=None,kind=None):
    fr=frozen(value);kind=kind or (r.EXACT_CONTEXT if 'canonical_sha256' in value else r.FIXED_CONTEXT)
    result={'schema':r.SCHEMA,'context_kind':kind,'owner_graph_sha256':r.digest(fr['graph']),
        'roots':roots or [{key:nodes[0][key] for key in ('candidate_id','realization_id')}],'nodes':copy.deepcopy(nodes)}
    if kind==r.EXACT_CONTEXT:result['core_sha256']=value.get('canonical_sha256')
    if any(b['selection']['kind']=='existing_member_scope' for item in nodes for b in item['bindings']):
        result['member_scopes_sha256']=r.digest(fr.get('member_scopes',[]))
    return result


def resolve(value,nodes,**kw):return r.resolve_selected_contracts(value,projection(value,nodes,**kw))


class NativeMemberScopeResolutionTests(unittest.TestCase):
    def test_each_member_p_pr_context_e_share_one_complete_view(self):
        c=core();facts=[fact('old',mode='prerequisite',value='matte'),
            fact('preserved',mode='preservation',value='same'),fact('context',mode='context',value='displayed'),
            fact('new',value='glossy',requires=['old','preserved'])]
        facts[1]['value']={'type':'frozen_property_reference/v1','value':'same'}
        result=resolve(c,[node([scope_binding(c)],facts)])
        expanded=result['nodes'][0]['expanded_facts']
        self.assertEqual(len(expanded),8)
        for fid in ['old','preserved','context','new']:
            actual=[item for item in expanded if item['fact_id']==fid]
            self.assertEqual([item['target']['owner_id'] for item in actual],['coat_A','glove_A'])
        self.assertEqual(len(result['effect_assignments']),2)
        self.assertEqual({item['value']['value'] for item in result['effect_assignments']},{'glossy'})
        self.assertEqual(result['permission_scope']['dimensions'],['material'])
        self.assertNotIn('allowed',result);self.assertNotIn('qualified',result)
        # P/PR values are preserved for B2 to match, not mechanically approved here.
        self.assertEqual(expanded[0]['value']['value'],'matte')
        self.assertEqual(expanded[2]['value']['type'],'frozen_property_reference/v1')

    def test_collective_point_assignment_uses_all_receivers_without_copying_value(self):
        c=core();row=node([fixed('wearer'),scope_binding(c)],
            [fact(target='wearer',prop='outfit.styling',dim='appearance',value='coordinated',receivers=['members'])])
        result=resolve(c,[row]);facts=result['nodes'][0]['expanded_facts']
        self.assertEqual(len(facts),1);self.assertEqual(facts[0]['target']['owner_id'],'holder_A')
        self.assertEqual(facts[0]['canonical_receivers'],['coat_A','glove_A'])
        self.assertEqual([x['target'] for x in result['effect_assignments']],['holder_A'])
        self.assertEqual({x['target'] for x in result['permission_scope']['properties']},{'holder_A','coat_A','glove_A'})

    def test_receiver_literal_order_and_scope_provenance_are_preserved(self):
        c=core();row=node([fixed('image','image'),selected('single','coat_A'),scope_binding(c)],
            [fact(target='image',receivers=['single','members'])])
        result=resolve(c,[row]);f=result['nodes'][0]['expanded_facts'][0]
        self.assertEqual(f['source_receivers'],['single','members'])
        self.assertEqual([x['source_target'] for x in f['receiver_expansions']],['single','members'])
        self.assertEqual([m['owner_id'] for x in f['receiver_expansions'] for m in x['members']],['coat_A','coat_A','glove_A'])
        self.assertEqual(f['canonical_receivers'],['coat_A','glove_A'])
        self.assertEqual(f['receiver_expansions'][1]['members'][1]['scope_provenance']['member_index'],1)
        self.assertEqual(f['receiver_expansions'][1]['members'][1]['scope_provenance']['source_input_ids'],['request'])

    def test_joint_scope_intersection_conflicts_even_across_different_source_targets(self):
        c=core();a=node([scope_binding(c)],[fact(value='glossy')])
        b=node([selected('other','glove_A')],[fact(target='other',value='matte')],cid='source_B')
        roots=[{'candidate_id':x['candidate_id'],'realization_id':'base'} for x in [a,b]]
        with self.assertRaisesRegex(ValueError,'joint actual-owner'):resolve(c,[a,b],roots=roots)
        b['facts'][0]['value']['value']='glossy';seal_node(b)
        result=resolve(c,[a,b],roots=roots)
        self.assertEqual(len(result['effect_assignments']),2)
        self.assertEqual(len(next(x for x in result['effect_assignments'] if x['target']=='glove_A')['sources']),2)

    def test_actual_alias_joint_value_type_operation_receiver_controls(self):
        c=core(additional=['coat_alias','receiver_alias'])
        c['semantic_assertions']=[x for x in c['semantic_assertions'] if not (x['axes']['kind']=='fact' and x['axes']['owner'] in {'coat_alias','receiver_alias'})]
        c['semantic_assertions'] += [assertion('same_coat','equivalent',left='coat_A',right='coat_alias'),
            assertion('same_receiver','equivalent',left='holder_A',right='receiver_alias')]
        reseal(c)
        a=node([selected('a','coat_A'),selected('ra','holder_A')],[fact(target='a',receivers=['ra'])])
        b=node([selected('b','coat_alias'),selected('rb','receiver_alias')],[fact(target='b',receivers=['rb'])],cid='source_B')
        roots=[{'candidate_id':x['candidate_id'],'realization_id':'base'} for x in [a,b]]
        good=resolve(c,[a,b],roots=roots)
        self.assertEqual(len(good['effect_assignments']),1)
        for defect in ['value','type','operation','receiver']:
            bad=copy.deepcopy(b)
            if defect=='value':bad['facts'][0]['value']['value']='matte'
            elif defect=='type':bad['facts'][0]['value']['type']='different/value-v1'
            elif defect=='operation':bad['facts'][0]['operation']='relocate'
            else:bad['facts'][0]['receivers']=[];bad['bindings'].pop()
            seal_node(bad)
            with self.subTest(defect=defect):
                with self.assertRaisesRegex(ValueError,'joint actual-owner'):resolve(c,[a,bad],roots=roots)

    def test_disjoint_owners_different_values_and_distinct_properties_are_preserved(self):
        c=core();c['semantic_assertions'].append(assertion('separate','disjoint',left='coat_A',right='glove_A'));reseal(c)
        a=node([selected('a','coat_A')],[fact(target='a',value='glossy')])
        b=node([selected('b','glove_A')],[fact(target='b',value='matte'),fact('rough',target='b',prop='surface.texture',value='rough')],cid='source_B')
        result=resolve(c,[a,b],roots=[{'candidate_id':x['candidate_id'],'realization_id':'base'} for x in [a,b]])
        self.assertEqual(len(result['effect_assignments']),3)

    def test_same_source_distinct_targets_actual_alias_conflict_and_local_strictness(self):
        c=core();a=node([selected('a','coat_A'),selected('b','coat_A')],
            [fact('one',target='a'),fact('two',target='b',value='matte')])
        with self.assertRaisesRegex(ValueError,'joint actual-owner'):resolve(c,[a])
        # Source-local receiver equality is kept stricter than actual aliases.
        a=node([selected('a','coat_A'),selected('r1','holder_A'),selected('r2','holder_A')],
            [fact('one',target='a',receivers=['r1']),fact('two',target='a',receivers=['r2'])])
        with self.assertRaisesRegex(ValueError,'source-local'):resolve(c,[a])

    def test_explicit_part_of_members_are_not_merged_or_given_parent_presence(self):
        c=core();c['semantic_assertions'].append(assertion('part','part_of',left='glove_A',right='coat_A'));reseal(c)
        result=resolve(c,[node([scope_binding(c)],[fact()])])
        self.assertEqual({x['target'] for x in result['effect_assignments']},{'coat_A','glove_A'})
        bad=copy.deepcopy(c);bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if not (x['axes']['kind']=='fact' and x['axes']['owner']=='glove_A')];reseal(bad)
        with self.assertRaisesRegex(ValueError,'independent exact atomic presence'):frozen(bad)

    def test_scope_alias_duplicate_is_rejected_not_deduplicated(self):
        c=core(additional=['coat_alias']);c['semantic_assertions']=[x for x in c['semantic_assertions'] if not (x['axes']['kind']=='fact' and x['axes']['owner']=='coat_alias')]
        c['semantic_assertions'].append(assertion('same','equivalent',left='coat_A',right='coat_alias'))
        scope=c['semantic_assertions'][-2] if c['semantic_assertions'][-2]['axes']['kind']=='existing_member_scope' else next(x for x in c['semantic_assertions'] if x['axes']['kind']=='existing_member_scope')
        inv=json.loads(scope['axes']['inventory']);inv['members'][1]['owner_id']='coat_alias';scope['axes']['inventory']=n.canonical(inv);reseal(c)
        with self.assertRaisesRegex(ValueError,'duplicate canonical member'):frozen(c)

    def test_hash_absent_fixed_point_context_is_distinct_and_no_presence_is_invented(self):
        c=core(exact=False,scoped=False)
        c['semantic_assertions']=[x for x in c['semantic_assertions'] if x['axes']['kind']!='fact']
        row=node([fixed()],[fact(target='point')])
        result=resolve(c,[row]);self.assertEqual(result['context']['kind'],r.FIXED_CONTEXT)
        self.assertNotIn('core_sha256',result['context']);self.assertNotIn('member_scopes_sha256',result['context'])
        self.assertEqual(result['nodes'][0]['bindings'][0]['members'],[{'owner_id':'holder_A','canonical_owner_id':'holder_A'}])
        # A hash appearing anywhere in the fixed tag cannot be silently ignored.
        for defect in ['core_hash','core_id','projection_hash']:
            bad=copy.deepcopy(c);p=projection(c,[row])
            if defect=='core_hash':bad['canonical_sha256']='0'*64
            elif defect=='core_id':bad['core_id']='ignored'
            else:p['core_sha256']='0'*64
            with self.subTest(defect=defect):
                with self.assertRaises(ValueError):r.resolve_selected_contracts(bad,p)

    def test_selected_points_and_scopes_never_use_hash_absent_context(self):
        for scoped in [False,True]:
            c=core(exact=False,scoped=scoped);row=node([scope_binding(c) if scoped else selected('point')],[fact(target='members' if scoped else 'point')])
            with self.subTest(scoped=scoped):
                with self.assertRaises(ValueError):resolve(c,[row])

    def test_exact_core_graph_scope_source_and_node_hashes_cannot_fallback(self):
        c=core();row=node([scope_binding(c)],[fact()]);p=projection(c,[row])
        for defect in ['core_hash','core_id','core_body','projection_core','graph','table','scope','meaning','qualification','node','input_hash']:
            bad=copy.deepcopy(c);q=copy.deepcopy(p)
            if defect=='core_hash':bad['canonical_sha256']='0'*64
            elif defect=='core_id':bad['core_id']='0'*16
            elif defect=='core_body':bad['baseline_prompt_en']+=' changed'
            elif defect=='projection_core':q['core_sha256']='0'*64
            elif defect=='graph':q['owner_graph_sha256']='0'*64
            elif defect=='table':q['member_scopes_sha256']='0'*64
            elif defect=='scope':q['nodes'][0]['bindings'][0]['selection']['scope_sha256']='0'*64;seal_node(q['nodes'][0])
            elif defect=='meaning':q['nodes'][0]['meaning_sha256']='0'*64
            elif defect=='qualification':q['nodes'][0]['qualification_sha256']='0'*64
            elif defect=='node':q['nodes'][0]['projection_sha256']='0'*64
            else:
                scope=next(x for x in bad['semantic_assertions'] if x['axes']['kind']=='existing_member_scope');inv=json.loads(scope['axes']['inventory']);inv['input_binding']['input_inventory_sha256']='0'*64;scope['axes']['inventory']=n.canonical(inv);reseal(bad);q['core_sha256']=bad['canonical_sha256']
            with self.subTest(defect=defect):
                with self.assertRaises(ValueError):r.resolve_selected_contracts(bad,q)

    def test_invalid_inventory_or_single_presence_cannot_be_repaired_by_new_hashes(self):
        c=core();row=node([scope_binding(c)],[fact()]);original=projection(c,[row])
        for defect in ['unknown','incomplete','empty','input_incomplete','missing_presence','advisory','foreign_span','foreign_input']:
            bad=copy.deepcopy(c);scope=next(x for x in bad['semantic_assertions'] if x['axes']['kind']=='existing_member_scope');inv=json.loads(scope['axes']['inventory'])
            if defect=='unknown':inv['state']='unknown'
            elif defect=='incomplete':inv['complete']=False
            elif defect=='empty':inv['members']=[]
            elif defect=='input_incomplete':bad['request_binding']['input_inventory']['complete']=False
            elif defect=='missing_presence':bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if not (x['axes']['kind']=='fact' and x['axes']['owner']=='glove_A')]
            elif defect=='advisory':scope['polarity']='advisory'
            elif defect=='foreign_span':inv['members'][0]['source_span_ids']=['missing']
            else:inv['members'][0]['source_input_ids']=['invented']
            scope['axes']['inventory']=n.canonical(inv);reseal(bad);p=copy.deepcopy(original);p['core_sha256']=bad['canonical_sha256']
            with self.subTest(defect=defect):
                with self.assertRaises(ValueError):r.resolve_selected_contracts(bad,p)

    def test_binding_inventory_and_expansion_tags_have_no_defaults_or_subset_selection(self):
        c=core();row=node([scope_binding(c)],[fact()])
        for defect in ['missing','extra','duplicate','point_array','scope_missing','scope_foreign','subset','target_tag','receiver_tag','unknown_tag','wrong_origin','map_field']:
            bad=copy.deepcopy(row);binding=bad['bindings'][0]
            if defect=='missing':bad['bindings']=[]
            elif defect=='extra':bad['bindings'].append(selected('unused','coat_A'))
            elif defect=='duplicate':bad['bindings'].append(copy.deepcopy(binding))
            elif defect=='point_array':binding['selection']={'kind':'selected_existing_owner','owner_id':['coat_A','glove_A']}
            elif defect=='scope_missing':binding['selection'].pop('scope_id')
            elif defect=='scope_foreign':binding['selection']['scope_id']='unknown'
            elif defect=='subset':binding['selection']['members']=['coat_A']
            elif defect=='target_tag':binding['selection']['target_semantics']='first_member'
            elif defect=='receiver_tag':binding['selection']['receiver_semantics']='first_member'
            elif defect=='unknown_tag':binding['selection']['kind']='unknown'
            elif defect=='wrong_origin':binding['origin']='introduced'
            else:binding['legacy_fallback']='main_subject'
            seal_node(bad)
            with self.subTest(defect=defect):
                with self.assertRaises(ValueError):resolve(c,[bad])

    def test_selected_point_presence_is_exact_and_existing_creation_is_rejected(self):
        c=core(scoped=False);row=node([selected()],[fact(target='point')])
        self.assertEqual(resolve(c,[row])['nodes'][0]['bindings'][0]['members'][0]['owner_id'],'coat_A')
        for defect in ['absent','wrong_type','anatomy_only','missing_owner','creation']:
            bad=copy.deepcopy(c);a=copy.deepcopy(row)
            presence=next(x for x in bad['semantic_assertions'] if x['axes']['kind']=='fact' and x['axes']['owner']=='coat_A')
            if defect=='absent':presence['axes']['value']='absent'
            elif defect=='wrong_type':presence['axes']['value_type']='face.presence/v1'
            elif defect=='anatomy_only':presence['axes']['property']='anatomy.face.presence';presence['axes']['value_type']='anatomy.face.presence/v1'
            elif defect=='missing_owner':a['bindings'][0]['selection']['owner_id']='missing'
            else:a['facts'][0]['operation']='add_entity'
            reseal(bad);seal_node(a)
            with self.subTest(defect=defect):
                with self.assertRaises(ValueError):resolve(bad,[a])

    def test_introduced_point_is_preserved_and_never_frozen_scope_or_guard_witness(self):
        c=core(exact=False,scoped=False)
        binding={'target':'new','origin':'introduced','selection':{'kind':'introduced_point','role':'secondary_prop','introduced_by':'create'}}
        a=node([binding],[fact('create',target='new',prop='entity.presence',dim='subject',value='present',operation='add_entity')])
        owner=resolve(c,[a])['nodes'][0]['bindings'][0]['members'][0]['owner_id']
        self.assertEqual(owner,'native-introduced:'+a['meaning_sha256']+':base:new')
        for defect in ['missing_creator','occupied_role','prerequisite','guard_only','scope_add','scope_remove']:
            bad=copy.deepcopy(a);value=copy.deepcopy(c)
            if defect=='missing_creator':bad['bindings'][0]['selection']['introduced_by']='missing'
            elif defect=='occupied_role':bad['bindings'][0]['selection']['role']='main_subject'
            elif defect=='prerequisite':bad['facts'].append(fact('old',target='new',mode='prerequisite'))
            elif defect=='guard_only':bad['bindings'].append({'target':'guard','origin':'introduced','selection':{'kind':'introduced_point','role':'secondary_hair','introduced_by':'missing'}});bad['guard_only_targets']=['guard']
            else:
                value=core();bad=node([scope_binding(value)],[fact(operation='add_entity' if defect=='scope_add' else 'remove_entity')])
            seal_node(bad)
            with self.subTest(defect=defect):
                with self.assertRaises(ValueError):resolve(value,[bad])

    def test_guard_only_bindings_are_explicit_addresses_without_guard_parsing(self):
        c=core();a=node([scope_binding(c),selected('guard_owner','holder_A')],[fact()],guards=['guard_owner'])
        result=resolve(c,[a]);self.assertEqual(len(result['nodes'][0]['bindings']),2)
        self.assertEqual(len(result['nodes'][0]['expanded_facts']),2)
        self.assertNotIn('guard_owner',{x['source_target'] for x in result['nodes'][0]['expanded_facts']})
        # Authentic own-sealed namespace is B2's responsibility; no guard pass flag.
        self.assertNotIn('guards_verified',result)
        a['guard_only_targets']=['members'];seal_node(a)
        with self.assertRaisesRegex(ValueError,'guard-only'):resolve(c,[a])

    def test_actual_selected_required_optional_and_shared_child_closure(self):
        c=core();child=node([selected('object','coat_A')],[fact(target='object')],cid='child')
        a=node([fixed('image','image')],[fact(target='image',prop='image.finish',value='clean')],children=[edge(child)])
        b=node([],[],cid='source_B',children=[edge(child,'explicit_optional')])
        roots=[{'candidate_id':x['candidate_id'],'realization_id':'base'} for x in [a,b,child]]
        result=resolve(c,[a,b,child],roots=roots)
        actual=next(x for x in result['nodes'] if x['candidate_id']=='child')
        self.assertEqual(len(actual['incoming']),2);self.assertEqual(len(actual['expanded_facts']),1)
        self.assertEqual(len(result['effect_assignments']),2)
        # An unselected optional definition is NOT an active input node/edge.
        a['selected_children']=[];seal_node(a)
        result=resolve(c,[a]);self.assertEqual([x['candidate_id'] for x in result['nodes']],['source_A'])
        with self.assertRaisesRegex(ValueError,'unused'):resolve(c,[a,child])

    def test_missing_stale_conflicting_cyclic_foreign_or_unused_closure_is_rejected(self):
        c=core();child=node([],[],cid='child');a=node([],[],children=[edge(child)])
        for defect in ['missing','wrong_child_rid','wrong_child_proof','wrong_edge_projection','duplicate_edge','duplicate_node','conflicting_rid','root_rid','unused']:
            parent=copy.deepcopy(a);other=copy.deepcopy(child);nodes=[parent,other];roots=None
            if defect=='missing':nodes.pop()
            elif defect=='wrong_child_rid':parent['selected_children'][0]['realization_id']='foreign'
            elif defect=='wrong_child_proof':parent['selected_children'][0]['qualification_sha256']='0'*64
            elif defect=='wrong_edge_projection':parent['selected_children'][0]['projection_sha256']='0'*64
            elif defect=='duplicate_edge':parent['selected_children']*=2
            elif defect=='duplicate_node':nodes.append(copy.deepcopy(child))
            elif defect=='conflicting_rid':other['realization_id']='foreign';seal_node(other)
            elif defect=='root_rid':roots=[{'candidate_id':'source_A','realization_id':'foreign'}]
            else:nodes.append(node([],[],cid='unused'))
            seal_node(parent)
            with self.subTest(defect=defect):
                with self.assertRaises(ValueError):resolve(c,nodes,roots=roots)
        # Cycles cannot have recursively self-consistent node digests; malformed
        # cyclic attempts are rejected at edge seals before any recursion.
        child['selected_children']=[edge(a)];seal_node(child);a['selected_children']=[edge(child)];seal_node(a)
        with self.assertRaises(ValueError):resolve(c,[a,child])

    def test_source_fact_mode_requires_shape_and_same_rid_are_exact(self):
        c=core();base=node([scope_binding(c)],[fact('old',mode='prerequisite',value='matte'),fact('new',requires=['old'])])
        for defect in ['duplicate_fact','foreign_rid','unknown_mode','bad_typed_value','bad_operation','foreign_requires','effect_requires','self_requires','extra_quote','receiver_missing','receiver_duplicate','cycle']:
            a=copy.deepcopy(base);f=a['facts'][1]
            if defect=='duplicate_fact':a['facts'].append(copy.deepcopy(f))
            elif defect=='foreign_rid':f['realization_id']='foreign'
            elif defect=='unknown_mode':f['mode']='no_effect'
            elif defect=='bad_typed_value':f['value']={'type':'surface.optical_response/v1','value':True}
            elif defect=='bad_operation':f['operation']='guess'
            elif defect=='foreign_requires':f['requires']=['missing']
            elif defect=='effect_requires':a['facts'][0]['requires']=['new']
            elif defect=='self_requires':f['requires']=['new']
            elif defect=='extra_quote':f['quote']='a source clause B1 does not parse'
            elif defect=='receiver_missing':f['receivers']=['missing']
            elif defect=='receiver_duplicate':f['receivers']=['members','members']
            else:
                a['facts']=[fact('p',mode='prerequisite',requires=['q']),fact('q',mode='preservation',requires=['p'])]
            seal_node(a)
            with self.subTest(defect=defect):
                with self.assertRaises(ValueError):resolve(c,[a])

    def test_property_lock_api_receives_every_actual_target_and_receiver(self):
        from photo_contracts import property_effects_allowed
        c=core();a=node([scope_binding(c),fixed('image','image')],
            [fact(receivers=['image'])]);result=resolve(c,[a]);scope=result['permission_scope']
        self.assertEqual({x['target'] for x in scope['properties']},{'coat_A','glove_A','image_A'})
        lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'material','target':'glove_A','property':'surface.optical_response'}]}
        self.assertFalse(property_effects_allowed(lock,scope['dimensions'],scope['properties'],owner_graph=scope['owner_graph']))
        same=node([selected('one','glove_A')],[fact(target='one',value='glossy')]);q=resolve(c,[same])['permission_scope']
        self.assertFalse(property_effects_allowed(lock,q['dimensions'],q['properties'],owner_graph=q['owner_graph']))
        # Introduce no anatomy/entailments: unrelated property stays allowed.
        other=node([selected('one','glove_A')],[fact(target='one',prop='surface.pattern',value='striped')]);q=resolve(c,[other])['permission_scope']
        self.assertTrue(property_effects_allowed(lock,q['dimensions'],q['properties'],owner_graph=q['owner_graph']))

    def test_receiver_and_parent_overlap_unknown_and_disjoint_lock_controls(self):
        from photo_contracts import property_effects_allowed
        for relation,expected in [('part_of',False),('disjoint',True),(None,False)]:
            c=core()
            if relation:c['semantic_assertions'].append(assertion('relation',relation,left='glove_A',right='coat_A'));reseal(c)
            a=node([selected('surface','glove_A')],[fact(target='surface')]);scope=resolve(c,[a])['permission_scope']
            lock={'semantic_anchors':[{'dimension':'material','target':'coat_A','property':'surface.optical_response'}]}
            with self.subTest(relation=relation):
                self.assertEqual(property_effects_allowed(lock,scope['dimensions'],scope['properties'],owner_graph=scope['owner_graph']),expected)

    def test_caps_bindings_facts_selected_nodes_edges_and_depth(self):
        c=core(scoped=False)
        # Exactly64 selected-owner nodes allowed; fixed-only nodes are not
        # incorrectly capped by the caller-selection-entry limit.
        selected_nodes=[node([selected('point','coat_A')],[fact(target='point')],cid='source_'+str(i)) for i in range(65)]
        roots=lambda nodes:[{'candidate_id':x['candidate_id'],'realization_id':'base'} for x in nodes]
        self.assertEqual(len(resolve(c,selected_nodes[:64],roots=roots(selected_nodes[:64]))['nodes']),64)
        with self.assertRaisesRegex(ValueError,'caller-selected'):resolve(c,selected_nodes,roots=roots(selected_nodes))
        fixed_nodes=[node([fixed()],[fact(target='point')],cid='fixed_'+str(i)) for i in range(65)]
        self.assertEqual(len(resolve(c,fixed_nodes,roots=roots(fixed_nodes))['nodes']),65)
        a=node([fixed('p'+str(i)) for i in range(32)],[],guards=['p'+str(i) for i in range(32)])
        self.assertEqual(len(resolve(c,[a])['nodes'][0]['bindings']),32)
        a['bindings'].append(fixed('overflow'));seal_node(a)
        with self.assertRaises(ValueError):resolve(c,[a])
        a=node([fixed()],[fact('f'+str(i),target='point') for i in range(4096)])
        self.assertEqual(len(resolve(c,[a])['nodes'][0]['expanded_facts']),4096)
        a['facts'].append(fact('overflow',target='point'));seal_node(a)
        with self.assertRaises(ValueError):resolve(c,[a])
        children=[node([],[],cid='child_'+str(i)) for i in range(9)]
        a=node([],[],children=[edge(x) for x in children[:8]])
        self.assertEqual(len(resolve(c,[a,*children[:8]])['nodes']),9)
        a['selected_children'].append(edge(children[8]));seal_node(a)
        with self.assertRaises(ValueError):resolve(c,[a,*children])
        chain=[node([],[],cid='depth_0')]
        for i in range(1,10):chain.insert(0,node([],[],cid='depth_'+str(i),children=[edge(chain[0])]))
        self.assertEqual(len(resolve(c,chain[1:])['nodes']),9)
        with self.assertRaises(ValueError):resolve(c,chain)

    def test_scope_and_core_caps_remain_neutral_not_compressed(self):
        c=core();a=node([scope_binding(c)],[fact()]);p=projection(c,[a])
        for defect in ['rows65','scope9','members33','owners33','oversize_utf8']:
            bad=copy.deepcopy(c)
            if defect=='rows65':
                bad['semantic_assertions'] += [{'axes':{'ordinary':'advisory'}} for _ in range(65-len(bad['semantic_assertions']))]
            elif defect=='scope9':
                original=next(x for x in bad['semantic_assertions'] if x['axes']['kind']=='existing_member_scope')
                for i in range(8):
                    extra=copy.deepcopy(original);extra['assertion_id']='scope_'+str(i);extra['axes']['scope_id']='scope_'+str(i);bad['semantic_assertions'].append(extra)
            elif defect=='owners33':
                for i in range(33):bad['semantic_assertions'].append(assertion('more_'+str(i),'owner',owner='extra_'+str(i),owner_kind='entity'))
            else:
                scope=next(x for x in bad['semantic_assertions'] if x['axes']['kind']=='existing_member_scope');inv=json.loads(scope['axes']['inventory'])
                if defect=='members33':inv['members']=[copy.deepcopy(inv['members'][0]) for _ in range(33)]
                else:inv['padding']='한'*22000
                scope['axes']['inventory']=n.canonical(inv)
            reseal(bad);q=copy.deepcopy(p);q['core_sha256']=bad['canonical_sha256']
            with self.subTest(defect=defect):
                with self.assertRaises(ValueError):r.resolve_selected_contracts(bad,q)
        self.assertEqual((n.MAX_ROWS,n.MAX_OWNERS,n.MAX_MEMBERS,n.MAX_MEMBER_SCOPES,n.MAX_MEMBER_INVENTORY_BYTES),(64,32,32,8,65536))

    def test_pure_repeat_serialized_projection_parity_and_input_no_mutation(self):
        c=core();a=node([scope_binding(c)],[fact()]);p=projection(c,[a]);before=copy.deepcopy((c,p))
        one=r.resolve_selected_contracts(c,p);two=r.resolve_selected_contracts(json.loads(json.dumps(c)),json.loads(json.dumps(p)))
        self.assertEqual(n.canonical(one),n.canonical(two));self.assertEqual((c,p),before)
        self.assertEqual(one['canonical_sha256'],r.digest({k:v for k,v in one.items() if k!='canonical_sha256'}))
        # The normalized fact projection is identical whether B2 originally read
        # full positive source or its sealed compact form. This tests that exact
        # private projection boundary, not an unimplemented consumer adapter.
        self.assertEqual(r.resolve_selected_contracts(c,copy.deepcopy(p)),one)

    def test_actual_authoring_wire_frozen_scope_enters_exact_context(self):
        wire=__import__('photo_precore_bridge').load('photo_authoring_wire')
        f=ROOT/'tests/fixtures/photo_prompt/camera_authoring_path_v1/en_open'
        raw=json.loads((f/'authorial-core.json').read_text());request=json.loads((f/'request-envelope.json').read_text())
        statement='All named owners are independently present: coat_A and glove_A. The complete local collection consists of coat_A and glove_A.'
        text=request['request_text']+' '+statement;sha=hashlib.sha256(text.encode()).hexdigest()
        request.update(request_text=text,request_sha256=sha,input_inventory={'schema':n.INPUT_SCHEMA,'complete':True,
            'items':[{'id':'request','kind':'request_text','sha256':sha}]})
        request['active_spans'][0].update(end=len(text),text=text);env=wire.normalize_request_envelope(request)
        raw['source_request']=text;raw['baseline_prompt_en']+=' '+statement
        rows=[]
        for i,owner in enumerate(['coat_A','glove_A']):
            rows += [assertion('owner_'+str(i),'owner',owner=owner,owner_kind='independently_declared_entity'),
                assertion('presence_'+str(i),'fact',owner=owner,property='entity.presence',value_type='entity.presence/v1',value='present')]
        inv={'schema':n.MEMBER_SCOPE_SCHEMA,'complete':True,'state':'known_present','input_binding':n.input_binding(env),
             'reviewed_input_ids':['request'],'members':[{'owner_id':x,'source_span_ids':['topic'],'source_input_ids':['request']} for x in ['coat_A','glove_A']]}
        rows.append(assertion('members','existing_member_scope',scope_id='local_members',inventory=n.canonical(inv)))
        for item in rows:item['source_span_ids']=['topic'];item['evidence']={'owners':statement}
        raw['semantic_assertions']+=rows
        full=wire.normalize_authorial_core(raw,request_envelope=env)
        result=resolve(full,[node([scope_binding(full)],[fact()])])
        self.assertEqual(result['context']['core_sha256'],full['canonical_sha256'])
        self.assertEqual(result['context']['input_binding'],n.input_binding(env))
        self.assertEqual({x['target'] for x in result['effect_assignments']},{'coat_A','glove_A'})

    def test_pure_module_never_imports_native_guard_qualification_or_provider(self):
        c=core();p=projection(c,[node([scope_binding(c)],[fact()])]);code=r'''
import sys,json,pathlib
sys.path.insert(0,sys.argv[1])
def audit(event,args):
 if event in {'socket.connect','socket.getaddrinfo'}:raise AssertionError('network')
 if event=='open' and isinstance(args[0],(str,bytes)):
  path=pathlib.Path(args[0]).resolve()
  if any(x in {'assets','references','generations'} for x in path.parts):raise AssertionError('candidate/runtime read')
sys.addaudithook(audit)
import photo_native_owner_resolution as r
v=json.load(sys.stdin);a=r.resolve_selected_contracts(v['core'],v['projection'])
assert len(a['effect_assignments'])==2
assert not any(x in sys.modules for x in ['photo_semantic_evidence','photo_candidate_corpus','prompt_generator','photo_embedding_provider'])
'''
        process=subprocess.run([sys.executable,'-c',code,str(SCRIPTS)],input=json.dumps({'core':c,'projection':p}),text=True,capture_output=True)
        self.assertEqual(process.returncode,0,process.stderr)


if __name__=='__main__':unittest.main()
