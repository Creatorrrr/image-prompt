from pathlib import Path
import copy,re,sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from photo_h_f2_query_scope import analyze
from photo_h_f2_event_phase import compile_contract,compile_contracts,order_phase,present_material,primary_units,request
T=lambda s:re.findall(r'[^\W_]+',s.casefold(),re.UNICODE)
GENERIC='Post-event residue across its owned surface'
CANDLE='꺼진 촛불의 심지와 연기'
DOG='After a dog has finished crossing a floor, muddy pawprints remain on that floor.'
BREAD='Bread crumbs remain on a cutting board after slicing one loaf has finished.'
PARCEL='Once a paper-wrapped parcel has been fully opened, torn wrapping remains on the table.'

def record(primary,lookup=''):
    return {'id':'fixture','meaning':{'primary':{'base':{'/content/ko':'ko','/content/en':'en'}},'literals':{'ko':primary,'en':'A physical component.','lookup':lookup},'search':{'fields':{'aliases':['lookup']}}}}

class GapSourceTests(unittest.TestCase):
    def project(self,q,texts):
        rows=[{'id':str(i),'bm25':10-i,'cosine':.8-i/100,'rrf':.2-i/100} for i in range(len(texts))];old=copy.deepcopy(rows)
        c=compile_contracts({str(i):x for i,x in enumerate(texts)},T,source_units=lambda key:primary_units(record(texts[int(key)]),'base','a'*64))
        full,phase=order_phase(rows,q,analyze(q,T),c,T);out,p=present_material(full,phase)
        self.assertEqual(rows,old);self.assertEqual({r['id']:r for r in full},{r['id']:r for r in old});self.assertFalse(p['native_approval'])
        return out,p,phase
    def test_korean_explicit_termination_is_material_not_a_safety_claim(self):
        c=compile_contract(CANDLE,T);self.assertEqual(c['phase'],'post_event_residue')
        for key in ('phase_witnesses','material_witnesses','relation_witnesses'):
            for w in c[key]:self.assertEqual(CANDLE[w['start']:w['end']],w['quote'])
    def test_actual_later_primary_is_discovered_after_component_first_D(self):
        r=record(CANDLE);d='A dark wick above a visible candle\n'+CANDLE
        c=compile_contracts({'x':d},T,source_units=lambda _:primary_units(r,'base','a'*64))['x']
        self.assertEqual(c['phase'],'post_event_residue');self.assertEqual(c['source_profile']['scene_family'],'candle')
        self.assertEqual(c['primary_phase_evidence'][0]['pointer'],'/content/ko')
    def test_lookup_only_korean_termination_cannot_supply_source_evidence(self):
        r=record('A candle flame is burning.',lookup=CANDLE)
        self.assertNotIn('x',compile_contracts({'x':'A candle flame\n'+CANDLE},T,source_units=lambda _:primary_units(r,'base','a'*64)))
    def test_negated_quoted_or_active_korean_source_is_not_post_event(self):
        for text in [CANDLE+'는 없다.','"'+CANDLE+'"',CANDLE+' 대신 진행 중인 동작']:
            with self.subTest(text=text):self.assertIsNone(compile_contract(text,T))
    def test_plain_candle_recovers_material_without_permitting_symbolism(self):
        out,p,_=self.project('Show ordinary physical smoke after a candle is snuffed, without magic residue or vanitas symbolism.',[GENERIC,CANDLE,'A just-extinguished candle with smoke supporting vanitas meaning'])
        self.assertEqual([r['id'] for r in out],['1']);self.assertEqual(p['query_context_permissions'],{})
    def test_optional_symbolism_allows_neutral_and_symbolic_sources(self):
        out,p,_=self.project('Show physical smoke after a candle is snuffed; vanitas symbolism may be included optionally.',[CANDLE,'A just-extinguished candle with smoke supporting vanitas meaning'])
        self.assertEqual([r['id'] for r in out],['0','1']);self.assertEqual(p['query_context_permissions'],{'mortality_symbolism':'optional'})
    def test_generic_request_keeps_plain_material_without_undeclared_owned_events(self):
        out,_,_=self.project('Show physical residue of a completed event.',[CANDLE,DOG,BREAD,PARCEL,GENERIC]);self.assertEqual([r['id'] for r in out],['0','4'])
    def test_matching_owned_traces_in_english_and_korean(self):
        cases=[('dog_pawprints','Show muddy pawprints left on the floor after a dog has finished crossing it.','개가 바닥을 가로지르는 동작이 끝난 뒤 남은 진흙 발자국이라는 물리적 사후 흔적을 보여줘.',DOG),('bread_crumbs','Show crumbs on the cutting board after cutting a loaf of bread has finished.','빵을 자르는 동작이 끝난 뒤 도마에 남은 부스러기라는 물리적 사후 흔적을 보여줘.',BREAD),('parcel_wrapping','Show torn wrapping left on the table after a parcel has been fully opened.','소포를 완전히 연 뒤 테이블에 남은 찢어진 포장지라는 물리적 사후 흔적을 보여줘.',PARCEL)]
        for family,en,ko,source in cases:
            for q in (en,ko):
                with self.subTest(family=family,q=q):
                    out,p,phase=self.project(q,[GENERIC,DOG,BREAD,PARCEL]);self.assertEqual([r['id'] for r in out],[str([GENERIC,DOG,BREAD,PARCEL].index(source))]);self.assertEqual(p['query_scene_family'],family)
                    for w in phase['request']['scene_witnesses']:self.assertEqual(q[w['start']:w['end']],w['quote'])
    def test_support_and_material_are_needed_with_the_named_owner(self):
        for q in ['Show physical residue after a dog has finished grooming.','Show bread remnants after a completed event.','Show physical residue after a parcel has been fully opened.']:
            with self.subTest(q=q):self.assertEqual(request(q,analyze(q,T),T)['scene_family'],'unproven_owner')
    def test_boot_prints_cannot_supply_dog_owner(self):
        out,_,_=self.project('Show muddy pawprints on a floor after a dog has finished crossing it.',['Post-event boot prints remain on a floor.',DOG]);self.assertEqual([r['id'] for r in out],['1'])
    def test_soil_crumbs_cannot_supply_bread(self):
        out,_,_=self.project('Show crumbs on a cutting board after cutting bread has finished.',['Post-event soil crumbs remain on a cutting board.',BREAD]);self.assertEqual([r['id'] for r in out],['1'])
    def test_ongoing_parcel_opening_cannot_supply_completed_material(self):
        out,_,_=self.project('Show torn wrapping on the table after a parcel has been fully opened.',['An ongoing action opens a parcel with torn wrapping on a table.',PARCEL]);self.assertEqual([r['id'] for r in out],['1'])
    def test_negated_owner_is_not_restored_by_masked_text(self):
        q='Show physical residue of a completed event. Dog is not present; pawprints remain on a floor.'
        self.assertNotEqual(request(q,analyze(q,T),T)['scene_family'],'dog_pawprints')
    def test_wrong_surface_cannot_borrow_the_owned_trace_contract(self):
        out,_,_=self.project('Show crumbs on a plate after cutting bread has finished.',[BREAD]);self.assertFalse(out)
    def test_failed_recipe_cannot_supply_is_a_rejected_substitute(self):
        source=BREAD+' A failed recipe cannot supply this relation.'
        out,_,phase=self.project('Show crumbs on a cutting board after cutting bread has finished.',[source]);self.assertEqual([r['id'] for r in out],['0']);self.assertFalse(phase['positive']['0']['context_requirements'])
    def test_magic_residue_cannot_substitute_is_not_a_required_context(self):
        source=CANDLE+'. Magic residue cannot substitute for the physical trace.'
        out,_,phase=self.project('Show physical smoke after a candle is snuffed.',[source]);self.assertEqual([r['id'] for r in out],['0']);self.assertFalse(phase['positive']['0']['context_requirements'])
    def test_context_that_cannot_be_omitted_still_remains_required(self):
        source='Failed recipe aftermath with harmless kitchen mess. A failed recipe cannot be omitted.'
        out,_,phase=self.project('Show physical aftermath after a failed recipe attempt has ended with kitchen mess.',[source]);self.assertEqual([r['id'] for r in out],['0']);self.assertTrue(phase['positive']['0']['context_requirements'])
    def test_claim_limit_does_not_erase_a_symbolic_context(self):
        source=CANDLE+'. Mortality symbolism cannot prove an actual death event.'
        out,p,phase=self.project('Show physical smoke after a candle is snuffed.',[source]);self.assertFalse(out);self.assertTrue(phase['context_qualified']['0']['context_requirements'])
    def test_english_ongoing_action_rejects_completed_counterpart(self):
        q='Show someone washing a floor in an ongoing action, not the physical aftermath of a completed event.'
        out,p,phase=self.project(q,[DOG,'An ongoing action washes a floor.',CANDLE]);self.assertEqual([r['id'] for r in out],['1']);self.assertNotIn('request',phase);self.assertEqual(p['mode'],'explicit_phase_exclusion')
    def test_korean_ongoing_action_rejects_completed_counterpart(self):
        q='완료된 사건의 사후 흔적이 아니라 바닥을 닦는 진행 중인 동작을 보여줘.'
        out,p,phase=self.project(q,[DOG,'An ongoing action washes a floor.']);self.assertEqual([r['id'] for r in out],['1'])
        for w in phase['excluded_phase']['positive_ongoing_witnesses']+phase['excluded_phase']['excluded_post_event_witnesses']:self.assertEqual(q[w['start']:w['end']],w['quote'])
    def test_quoted_phase_label_does_not_supply_a_physical_exclusion(self):
        q='Show an ongoing action beside a sign reading "not physical aftermath of a completed event".'
        out,p,phase=self.project(q,[DOG,'An ongoing action washes a floor.']);self.assertNotIn('excluded_phase',phase);self.assertEqual([r['id'] for r in out],['0','1'])
    def test_ongoing_without_an_excluded_counterpart_keeps_ordinary_discovery(self):
        out,p,phase=self.project('Show an ongoing action washing a floor.',[DOG,'An ongoing action washes a floor.']);self.assertNotIn('excluded_phase',phase);self.assertEqual(len(out),2)
    def test_negated_ongoing_does_not_invert_a_positive_aftermath_request(self):
        out,p,phase=self.project('Show physical residue of a completed event, not an ongoing action.',[GENERIC,'An ongoing action washes a floor.']);self.assertEqual([r['id'] for r in out],['0']);self.assertNotIn('excluded_phase',phase)
    def test_an_explicitly_rejected_phase_is_never_padding(self):
        out,p,phase=self.project('Show an ongoing action, not physical aftermath of a completed event.',[GENERIC,CANDLE]);self.assertFalse(out);self.assertEqual(p['available'],0);self.assertEqual(p['unfilled'],8)

if __name__=='__main__':unittest.main()
