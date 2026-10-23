"""Integrate reviewed optional literals; leave unreviewed mechanisms deferred."""
from pathlib import Path
import copy, hashlib, json, uuid

R = Path(__file__).resolve().parents[5]
O = Path(__file__).resolve().parent
P = O.parent
A = R / 'skills/photo-prompt-image-generator/assets'

def read(p): return json.loads(p.read_bytes())
def write(p, v): p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ident(prefix, value): return prefix + uuid.uuid5(uuid.NAMESPACE_URL, 'image-prompt/flintlock-fantasy-20261023/' + value).hex

# Direct whole-literal review. These are deliberately conservative mutation
# scopes, NOT unions of the proposed slot descriptors. Internal object geometry
# is appearance; adding a separate actor or a visible interaction declares it.
SCOPES = {
 'A01':'appearance material','A02':'appearance material lighting','A06':'appearance setting',
 'A07':'appearance setting','B01':'appearance material','B02':'appearance material',
 'B04':'appearance','B05':'appearance material composition setting count',
 'B06':'appearance','B07':'appearance atmosphere composition',
 'B08':'appearance material composition count',
 'C01':'subject role count appearance pose composition',
 'C02':'subject role count appearance pose composition',
 'C03':'subject role count appearance pose composition setting',
 'C04':'subject role count appearance pose composition setting',
 'C05':'subject role count appearance action pose relationship',
 'C06':'subject role age count appearance pose relationship material',
 'D02':'appearance material count setting composition',
 'D03':'appearance material setting text','D04':'appearance count',
 'D07':'setting composition camera','E01':'setting appearance material composition',
 'E02':'setting appearance material','E03':'setting appearance atmosphere camera composition',
 'E06':'appearance count text setting composition',
 'E07':'subject age count setting appearance material pose relationship',
 'F01':'appearance material composition','F02':'setting appearance material composition',
 'F03':'subject role age count action pose relationship appearance material',
 'F04':'subject role age count action pose relationship appearance',
 'F06':'setting appearance count composition',
 'F07':'appearance material setting','F08':'appearance material count setting',
 'G01':'appearance material color','G02':'appearance count text setting composition',
 'G03':'subject role age count appearance relationship',
 'G04':'appearance text composition setting',
 'G05':'subject age count pose relationship appearance setting',
 'G06':'appearance setting','G07':'subject appearance composition camera',
 'G08':'appearance subject setting composition','G09':'subject appearance camera',
 'H01':'subject role age action pose appearance lighting atmosphere',
 'H02':'subject role age count appearance setting composition',
 'H04':'appearance count lighting composition',
 'H05':'subject role age count action pose relationship appearance lighting',
 'H06':'subject count species appearance pose','H08':'subject role age count action pose appearance material',
 'J03':'appearance material color','J05':'appearance material count',
 'J12':'subject role age appearance','J16':'appearance material text composition setting',
}
HUMAN = set('C01 C02 C03 C04 C05 C06 F03 F04 G03 G05 H01 H02 H05 H08 J12'.split())
ADULT = set('C06 E07 F03 F04 G03 G05 H01 H02 H05 H08 J12'.split())
REFINE = {
 'cand_42d2b29291fe52db93a6bf09617d266e': ('D05 D06', '각진 돌출 능보들이 주 성벽에 이어져 있고, 해자 건너에는 출입구 앞을 가리는 별도의 쐐기 모양 라블랭이 놓인다.'),
 'cand_9c0d3821b9ae5cc49781a59f278b4f29': ('D01', '방어 흉벽 뒤의 넓은 포좌에 설치된 대포들이 각각 대응하는 개구부를 통하여 바깥을 향한다.'),
 'cand_e55f66332e315f20bf90ddbb61f8d36b': ('C08', '장식 견장들이 재킷 어깨 위에 놓이고 부착 밑판들이 보인다.'),
 'cand_f25347e368185c8780231631bf099418': ('J06', '코트 안쪽에 앞이 열린 조끼가 보인다.'),
 'cand_fc38c2780414540280a85f200fec999e': ('J11', '드레스 치마가 가슴 바로 아래에서 몸판에 이어지고, 치마는 그 높인 몸판 이음선으로부터 아래로 내려온다.'),
}

def main():
    cards = read(P/'semantic-cards.json')['cards']
    drafts = {d['card_id']: d for d in read(P/'candidate-drafts.json')['drafts']}
    sources = {s['source_id']: s for s in read(P/'sources.json')['sources']}
    catalog = read(A/'photo_candidate_slot_catalog.json')['slot_catalog']
    fresh, bindings, decisions = {}, {}, []
    research_sha = sha(P/'semantic-cards.json')
    for original in cards:
        card = copy.deepcopy(original); key = card['card_id']
        if key in drafts and drafts[key]['proposed_disposition'] == 'defer':
            decisions.append({'card_id':key, 'status':'deferred_source_plate_review', 'candidate_id':None})
            continue
        if key in drafts and drafts[key]['proposed_disposition'] != 'new':
            target = next((cid for cid,(ids,_) in REFINE.items() if key in ids.split()), 'cand_613c117d227555dca27eef2bc0b5b0be')
            decisions.append({'card_id':key,'status':'refine_existing_translation' if key!='J13' else 'reuse_complete_existing_source','candidate_id':target})
            continue
        diagnostic = card.get('kind') == 'context_only'
        cid = ident('cand_', key)
        card.update(candidate_id=cid, registration_status='diagnostic_only' if diagnostic else 'optional_authored_visual_source',
                    native_approval=False, native_qualification='not_qualified', source_image_review='NOT_RUN',
                    translation_review='paired full literals directly reviewed by integrating agent; independent translator not run')
        if diagnostic:
            en = ('Context-only distinction: ' + '; '.join(card['terms']) + '. These names alone establish no visible actor, event, status, consent, identity, diagnosis, chronology or mandatory prop. Resolve the actual requester meaning independently; this diagnostic is never positive image content.')
            ko = card['claim_limit_ko']
        else:
            en, ko = card['proposal_en'], card['proposal_ko']
            assert key in SCOPES, key
        card['source_refs'] = [sources[s] for s in card['source_ids']]
        content = {'en':en, 'ko':ko, 'definition':en,
                   'aliases':([card['title_ko']] + card.get('terms',[]) if diagnostic else [card['title_ko']]),
                   'research_semantics':card}
        conditions = {'for_any':['human']} if key in HUMAN else {}
        if key in ADULT: conditions['requires_adult_context'] = True
        effects = {'dimensions':[] if diagnostic else sorted(SCOPES[key].split()), 'properties':[]}
        fresh[cid] = {'id':cid,'record_kind':'diagnostic' if diagnostic else 'visual_option',
                      'content':content,'conditions':conditions,'effects':effects,
                      'provenance':[{'source':f'authored literal {P.relative_to(R)}/semantic-cards.json#{key}; contextual source {sources[s]["url"]}; digest is research file, not webpage bytes','sha256':research_sha} for s in card['source_ids']]}
        if not diagnostic:
            for slot in card['proposed_slots']:
                assert slot in catalog
                bid=ident('bind_',key+'/'+slot)
                bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional',
                               'semantic_role':catalog[slot]['semantic_role'],
                               'conditions':{'subject_applicability':{}},'weight':2}
        decisions.append({'card_id':key,'status':'registered_diagnostic' if diagnostic else 'registered_optional_visual','candidate_id':cid})
    assert len([r for r in fresh.values() if r['record_kind']=='visual_option']) == 52
    assert len([r for r in fresh.values() if r['record_kind']=='diagnostic']) == 21
    write(O/'new-native-records.json', fresh)
    module='photo_candidate_flintlock_fantasy_20261023.json'
    binding_module='photo_candidate_flintlock_fantasy_bindings_20261023.json'
    write(A/module, {'schema':'photo-candidate-module/v3','candidates':fresh})
    write(A/binding_module, {'schema':'photo-candidate-slot-bindings/v3','slot_bindings':bindings})
    manifest=read(A/'photo_candidate_corpus_manifest.json'); changed={}; before={}; changes=[]
    for m in manifest['modules']:
        if m['kind']!='candidates': continue
        p=A/m['file']; body=read(p); owned=set(body['candidates']) & set(REFINE)
        if not owned: continue
        for cid in owned:
            old=copy.deepcopy(body['candidates'][cid]); new=copy.deepcopy(old)
            new['content']['ko']=REFINE[cid][1]
            new['content']['embedding_text']=old['content'].get('embedding_text',old['content']['en'])+' | '+REFINE[cid][1]
            assert all(old[k]==new[k] for k in ('conditions','effects','provenance'))
            before[cid]=old;changed[cid]=new;body['candidates'][cid]=new
            changes.append({'candidate_id':cid,'module':m['file'],'card_ids':REFINE[cid][0].split(),
                            'fields':['content.ko','content.embedding_text'],
                            'review':'Complete original EN preserved. KO restores the original endpoints and plurality; no new source fact, owner or effect authority.'})
        write(p,body)
    assert len(changed)==5
    for name,kind in [(module,'candidates'),(binding_module,'slot_bindings')]:
        assert name not in [m['file'] for m in manifest['modules']]
        manifest['modules'].append({'file':name,'kind':kind})
    write(A/'photo_candidate_corpus_manifest.json',manifest)
    write(O/'changed-source-before.json',before);write(O/'changed-native-records.json',changed)
    write(O/'data-integration.json',{'new_visual_candidates':52,'new_diagnostics':21,'new_bindings':len(bindings),
                                   'refined_CIDs':5,'refined_cards':6,'reused_CIDs':1,'deferred_cards':22,
                                   'decisions':decisions,'existing_changes':changes,
                                   'effects_review':'Direct whole bilingual literal review, not slot descriptor unions. Conservative whole mutation dimensions; no invented scalar facts or owner permissions.',
                                   'native_approval':False,'pixel_status':'NOT_RUN'})
    write(A/'photo_flintlock_fantasy_semantics_20261023.json',{
        'schema':'photo-flintlock-fantasy-visual-semantics/v1','cards':cards,'keyword_routes':read(P/'keyword-routes.json'),
        'source_refs':list(sources.values()),'decisions':decisions,'native_approval':False,
        'authority':'Maintenance sidecar only; no hard activation, native source facts, owner selection or pixel approval.',
        'research_spec_sha256':research_sha})
    print(json.dumps({'new_visual':52,'new_diagnostic':21,'bindings':len(bindings),'refined_CIDs':len(changed),'deferred':22}))

if __name__=='__main__': main()
