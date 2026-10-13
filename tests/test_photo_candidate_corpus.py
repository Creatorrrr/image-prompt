from __future__ import annotations
import copy,json,sys,tempfile,unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
from tests.photo_native_schema import slot

A='cand_'+'a'*32
B='cand_'+'b'*32
X='bind_'+'a'*32
Y='bind_'+'b'*32
E={'dimensions':['style'],'properties':[]}


def fixture():
    return {'schema':c.SCHEMA,'candidates':{A:{'id':A,'record_kind':'visual_option',
        'content':{'en':'a glossy fabric surface'},'conditions':{},'effects':copy.deepcopy(E),
        'provenance':[{'source':'authored test','sha256':'a'*64}]}},
        'slot_catalog':{tag:slot(tag,['style'])
                        for tag in ['wardrobe_style','garment_detail']},
        'slot_bindings':{X:{'id':X,'candidate_id':A,'slot_id':'wardrobe_style',
            'role':'optional','semantic_role':'direct','conditions':{'subject_applicability':{}},'weight':1}},'policies':{}}


class SharedCorpusTests(unittest.TestCase):
    def test_one_source_many_roles_and_many_sources_one_role(self):
        d=fixture();d['slot_bindings'][Y]={**copy.deepcopy(d['slot_bindings'][X]),'id':Y,'slot_id':'garment_detail'}
        d['candidates'][B]={**copy.deepcopy(d['candidates'][A]),'id':B}
        z='bind_'+'c'*32
        d['slot_bindings'][z]={**copy.deepcopy(d['slot_bindings'][X]),'id':z,'candidate_id':B}
        c.validate(d)
        self.assertEqual(len(list(c.all_entries(d))),2)
        self.assertEqual(len(list(c.role_entries(d,'wardrobe_style'))),2)
        self.assertEqual(list(c.role_entries(d,'garment_detail'))[0]['id'],A)

    def test_untagged_candidate_remains_in_global_corpus(self):
        d=fixture();d['slot_bindings'].clear();c.validate(d)
        self.assertEqual(list(c.all_entries(d))[0]['id'],A)

    def test_retag_does_not_change_candidate_identity_or_content(self):
        d=fixture();before=c.digest(d['candidates'])
        d['slot_bindings'][X]['slot_id']='garment_detail';c.validate(d)
        self.assertEqual(c.digest(d['candidates']),before)

    def test_dangling_candidate_and_tag_are_rejected(self):
        for field,value in [('candidate_id',B),('slot_id','missing')]:
            d=fixture();d['slot_bindings'][X][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):c.validate(d)

    def test_duplicate_role_relationship_is_rejected(self):
        d=fixture();d['slot_bindings'][Y]={**d['slot_bindings'][X],'id':Y}
        with self.assertRaises(ValueError):c.validate(d)

    def test_mismatched_global_identity_is_rejected(self):
        d=fixture();d['candidates'][A]['id']=B
        with self.assertRaises(ValueError):c.validate(d)

    def test_double_effect_ownership_and_invalid_properties_are_rejected(self):
        d=fixture();d['candidates'][A]['content']['affected_dimensions']=['style']
        with self.assertRaises(ValueError):c.validate(d)
        d=fixture();d['candidates'][A]['effects']['properties']=[{'dimension':'pose','target':'main_subject','property':'face'}]
        with self.assertRaises(ValueError):c.validate(d)

    def test_role_condition_isolation_and_foreign_role_rejection(self):
        d=fixture();d['slot_bindings'][X]['conditions']={'subject_applicability':{'deny_domains':['studio']}}
        self.assertNotIn('_role_conditions',c.entry(d,A))
        self.assertEqual(c.entry(d,A,X)['_role_conditions']['subject_applicability']['deny_domains'],['studio'])
        d['candidates'][B]={**copy.deepcopy(d['candidates'][A]),'id':B}
        with self.assertRaises(ValueError):c.entry(d,B,X)

    def test_duplicate_json_key_and_nonfinite_values_are_rejected(self):
        for raw in ['{"a":1,"a":2}','{"a":NaN}']:
            with self.subTest(raw=raw),self.assertRaises(ValueError):c.decode(raw)
        d=fixture();d['policies']['bad']=float('inf')
        with self.assertRaises(ValueError):c.validate(d)

    def test_old_tree_contract_is_rejected(self):
        with self.assertRaises(ValueError):c.validate({'slots':{'wardrobe_style':[]}})

    def test_explicit_dangling_reference_is_rejected(self):
        d=fixture();d['policies']['bundle']={'candidate_refs':[B]}
        with self.assertRaises(ValueError):c.validate(d)

    def test_cycle_and_unknown_effect_dimension_are_rejected(self):
        d=fixture();d['candidates'][A]['content']['canonical_candidate_ref']=A
        with self.assertRaises(ValueError):c.validate(d)
        d=fixture();d['candidates'][A]['effects']['dimensions']=['unknown_axis']
        with self.assertRaises(ValueError):c.validate(d)

    def test_conditions_cannot_overwrite_identity_or_effects(self):
        for field,value in [('id',B),('affected_dimensions',['pose'])]:
            d=fixture();d['slot_bindings'][X]['conditions'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):c.validate(d)

    def test_native_loader_rejects_duplicate_source_owner_and_path_escape(self):
        d=fixture()
        with tempfile.TemporaryDirectory() as name:
            p=Path(name);modules=[]
            for field,schema in c.MODULE_SCHEMAS.items():
                file=field+'.json';(p/file).write_text(json.dumps({'schema':schema,field:d[field]}))
                modules.append({'file':file,'kind':field})
            manifest={'schema':c.MANIFEST_SCHEMA,'modules':modules}
            path=p/c.MANIFEST_NAME;path.write_text(json.dumps(manifest))
            self.assertEqual(c.load(p),d)
            manifest['modules'].append({'file':'candidates.json','kind':'candidates'})
            path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):c.load(p)
            manifest['modules']=[{'file':'../escape.json','kind':'candidates'}]
            path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):c.load(p)


if __name__=='__main__':unittest.main()
