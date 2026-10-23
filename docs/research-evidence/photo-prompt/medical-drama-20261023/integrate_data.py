"""Register bounded authored medical data without altering unrelated records."""
from pathlib import Path
import collections,copy,hashlib,json,os,sys,uuid

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SKILL=ROOT/'skills/photo-prompt-image-generator'
ASSETS=SKILL/'assets'
OUT=HERE/'integration-evidence'
sys.path.insert(0,str(SKILL/'scripts'))
import photo_candidate_corpus as corpus
from photo_runtime_sources import source_update

NS=uuid.UUID('9e3a82f5-16de-4cb5-94ae-89372e39104b')
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(prefix,key):return prefix+uuid.uuid5(NS,'medical-drama-20261023:'+key).hex
def write(p,value):
    raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
    tmp=p.with_name(p.name+'.medical-drama.tmp')
    tmp.write_bytes(raw);os.replace(tmp,p)

CONTRACT=(
 'One complete optional authored medical-scene visual realization, not a diagnosis, treatment instruction or genre definition. '
 'Retain every English and Korean positive clause, actual actor, body part, garment layer, instrument, count, support, '
 'attachment, directed contact, connection endpoint, display boundary and explicit model, illustrative or staged mode. '
 'Review the entire proposition and all effects against independently frozen requester meaning and actual open dimensions/properties; '
 'a keyword, genre label, role tag or research graph creates no owner, prerequisite, permission or native qualification. '
 'Do not transfer a hand, tube, support or depicted image to another owner or combine mutually exclusive alternatives. '
 'All adopted distinguishing components and their complete required connections must be visible together at useful scale. '
 'UNOBSERVABLE_NOT_PASS; partial_is_fail. '
 'A still image does not establish real identity, credentials, age beyond declared fictional context, consent, coercion, '
 'sexual intent, romance, pain, diagnosis, consciousness, anesthesia depth, sterility, certification, internal tube placement, '
 'physiological measurements, functioning, treatment success, healing, history, chronology, sound or legal conclusions. '
 'A monitor, document or diagram depicts a claim within its own boundary rather than proving that claim of the actual person. '
 'Sources support bounded definitions and confusion boundaries; scene geometry is authored, not an observed clinical photograph.'
)

# Conservative complete-proposition footprints are authored separately from slot tags.
GROUP_EFFECTS={
 'A':{'setting','count','pose','action','appearance','composition','relationship'},
 'B':{'appearance'},
 'C':{'pose','body_geometry','setting','relationship'},
 'D':{'action','pose','body_geometry','appearance','relationship','setting'},
 'E':{'pose','body_geometry','appearance','relationship','setting'},
 'F':{'setting','appearance','composition','relationship'},
 'G':{'setting','appearance','composition','relationship'},
}
EXTRA={
 'A03':{'subject','age','body_geometry'},'A14':{'count','action','pose'},
 'B16':{'style','color','material'},
 'B17':{'style','material'},'B18':{'style','color','material'},'B21':{'subject','age','style','sexual_tone'},
 'C09':{'age'},'C12':{'subject','age','style'},'C13':{'subject','age','style'},
 'D01':{'count'},'D02':{'count'},'D03':{'count'},'D04':{'count'},'D05':{'count','lighting'},
 'D08':{'body_geometry'},'D14':{'subject','age','style','count'},'D15':{'style','count'},'D16':{'count'},'D18':{'count'},
 'E07':{'age','subject','body_geometry'},'E11':{'count','action'},'E12':{'color','lighting'},'E13':{'color','lighting'},'E14':{'color','lighting'},'E15':{'material'},
 'F01':{'count','pose','action','body_geometry'},'F02':{'subject','pose','body_geometry'},'F03':{'subject','pose','body_geometry'},
 'F04':{'text'},'F05':{'text'},'F06':{'style','text','body_geometry'},'F07':{'style','text','body_geometry'},
 'F08':{'camera','framing','count','pose'},'F09':{'camera','pose','body_geometry'},'F10':{'count'},'F11':{'count','framing'},'F12':{'lighting','color'},
 'G01':{'subject','style','body_geometry'},'G02':{'subject','style','body_geometry','count'},'G03':{'subject','style','body_geometry','color'},
 'G04':{'text'},'G05':{'count','pose','action'},
}

def main():
    OUT.mkdir(exist_ok=True)
    if (OUT/'data-integration.json').exists():raise SystemExit('Already integrated; preserve recorded evidence.')
    cards=read(HERE/'semantic-cards.json')['cards'];sources=read(HERE/'sources.json')['sources']
    routes=read(HERE/'keyword-routes.json')['routes'];oldmap=read(HERE/'existing-source-mapping.json')['selected']
    manifest_path=ASSETS/corpus.MANIFEST_NAME
    before=corpus.load(ASSETS)
    manifest_before=read(manifest_path)
    protected={str(p.relative_to(ROOT)):sha(p) for p in [SKILL/'SKILL.md',SKILL/'retrieval-runtime.json',*ASSETS.glob('*.json'),*(SKILL/'precore').glob('*.py'),*(SKILL/'scripts').glob('*.py')]}
    write(OUT/'integration-baseline.json',{'protected':protected,'manifest':manifest_before,
        'candidate_sha256':{k:canonical(v) for k,v in before['candidates'].items()},
        'binding_sha256':{k:canonical(v) for k,v in before['slot_bindings'].items()},
        'candidate_count':len(before['candidates']),'binding_count':len(before['slot_bindings']),
        'catalog_sha256':canonical(before['slot_catalog']),'policies_sha256':canonical(before['policies'])})
    byold={x['id']:x for x in oldmap};mapping={};records={};bindings={};decisions=[];source_drift=[]
    exact={(x.get('content',{}).get('en'),x.get('content',{}).get('ko')):cid for cid,x in before['candidates'].items() if x['record_kind']!='diagnostic'}
    for card in cards:
        key=card['id']
        if key.startswith('R'):
            old=byold[key];cid=old['candidate_id'];assert cid in before['candidates'],cid
            current=before['candidates'][cid]
            if canonical(current)!=old['source_record_sha256']:source_drift.append({'card_id':key,'candidate_id':cid,'research_sha':old['source_record_sha256'],'current_sha':canonical(current)})
            assert current['content']['en']==card['positive_en'] and current['content']['ko']==card['positive_ko'],('reused literal drift',key)
            mapping[key]=cid;decisions.append({'card_id':key,'candidate_id':cid,'status':'existing_complete_source_reused','native_approval':False});continue
        cid=ident('cand_',key);mapping[key]=cid
        held=card['mode']=='held_reference_needed' or key=='G06'
        positive=card['mode']=='authored_visual_option' and not held
        meta={**copy.deepcopy(card),'candidate_id':cid,'runtime_registration':True,'runtime_importable':True,
            'registration_status':'authored_optional_visual' if positive else 'held_diagnostic' if held else 'context_diagnostic',
            'native_approval':False,'native_qualification':'not_qualified','graph_scope':'review metadata only; not typed native facts or eligibility evidence'}
        if positive:
            assert (card['positive_en'],card['positive_ko']) not in exact,('exact existing source must be reused',key)
            dims=GROUP_EFFECTS[key[0]]|EXTRA.get(key,set())
            # Bounded garment forms affect wardrobe, not the reference face or hair.
            effects={'dimensions':sorted(dims),'properties':[{'dimension':'appearance','target':'main_subject','property':'wardrobe'}]} if dims=={'appearance'} else {'dimensions':sorted(dims),'properties':[]}
            content={'en':card['positive_en'],'ko':card['positive_ko'],'definition':card['positive_en'],
                'aliases':[card['title_ko']],'application_contract':CONTRACT,'research_semantics':meta}
            cond={'for_any':['human']} if key[0] in 'BCDE' and key not in ['C12','C13','D14'] else {}
            if 'adult' in card['positive_en'].lower():cond['requires_adult_context']=True
            slots=card['suggested_slots']
        else:
            if key=='G06':meta['hold_reason']='Near-overlapping staged-set variant requires separate usefulness review; do not relabel the different complete R20 source as equivalent.'
            content={'definition':('Held reference/usefulness diagnostic excluded from positive visual retrieval: ' if held else 'Context diagnostic excluded from positive visual retrieval: ')+card['title_ko']+'. '+card['claim_limit'],'research_semantics':meta}
            effects={'dimensions':[],'properties':[]};cond={};slots=[]
        records[cid]={'id':cid,'record_kind':'visual_option' if positive else 'diagnostic','content':content,
            'conditions':cond,'effects':effects,'provenance':[{'source':'authored research docs/research-evidence/photo-prompt/medical-drama-20261023/semantic-cards.json#'+key,'sha256':sha(HERE/'semantic-cards.json')}]}
        for slot in slots:
            assert slot in before['slot_catalog'];bid=ident('bind_',cid+':'+slot)
            bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':before['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':1}
        decisions.append({'card_id':key,'candidate_id':cid,'status':meta['registration_status'],'positive':positive,'slots':slots,'native_approval':False})
    assert set(records).isdisjoint(before['candidates']) and set(bindings).isdisjoint(before['slot_bindings'])
    cm='photo_candidate_medical_drama_20261023.json';bm='photo_candidate_medical_drama_bindings_20261023.json';sm='photo_medical_drama_semantics_20261023.json'
    for name in [cm,bm,sm]:assert not (ASSETS/name).exists(),name
    registry={'schema':'photo-medical-drama-visual-semantics/v1','cards':[{**copy.deepcopy(c),'candidate_id':mapping[c['id']],'native_approval':False,'registration_status':next(x['status'] for x in decisions if x['card_id']==c['id'])} for c in cards],
        'keyword_routes':[{**copy.deepcopy(x),'optional_candidate_ids':[mapping[y] for y in x['optional_visual_card_ids'] if y!='G06'],'context_candidate_ids':[mapping[y] for y in x['context_card_ids']],'held_candidate_ids':[mapping[y] for y in x['held_card_ids']+(['G06'] if 'G06' in x['optional_visual_card_ids'] else [])],'automatic_hard_activation':False} for x in routes],
        'sources':sources,'native_approval':False,'automatic_activation':False,'research_sha256':sha(HERE/'semantic-cards.json')}
    proposed=OUT/'proposed-assets';proposed.mkdir(exist_ok=True)
    write(proposed/cm,{'schema':corpus.MODULE_SCHEMAS['candidates'],'candidates':records})
    write(proposed/bm,{'schema':corpus.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings})
    write(proposed/sm,registry)
    write(OUT/'card-candidate-map.json',mapping);write(OUT/'new-native-records.json',records)
    write(OUT/'changed-native-records.json',{})
    if '--prepare-only' in sys.argv:
        print(json.dumps({'status':'prepared_only','new_records':len(records),'positive':sum(x['record_kind']=='visual_option' for x in records.values()),'bindings':len(bindings)}));return
    with source_update(SKILL):
        assert sha(manifest_path)==protected[str(manifest_path.relative_to(ROOT))],'Concurrent manifest change before adoption'
        write(ASSETS/cm,{'schema':corpus.MODULE_SCHEMAS['candidates'],'candidates':records})
        write(ASSETS/bm,{'schema':corpus.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings})
        write(ASSETS/sm,registry)
        manifest=read(manifest_path)
        for name,kind in [(cm,'candidates'),(bm,'slot_bindings')]:manifest['modules'].append({'file':name,'kind':kind})
        write(manifest_path,manifest)
    after=corpus.load(ASSETS)
    assert all(after['candidates'][k]==v for k,v in before['candidates'].items())
    assert all(after['slot_bindings'][k]==v for k,v in before['slot_bindings'].items())
    assert all(after[k]==before[k] for k in ['slot_catalog','policies'])
    allow=[str((ASSETS/n).relative_to(ROOT)) for n in [cm,bm,sm,corpus.MANIFEST_NAME]]
    write(OUT/'card-candidate-map.json',mapping);write(OUT/'new-native-records.json',records)
    write(OUT/'changed-native-records.json',{})
    result={'status':'authored_source_data_integrated','new_positive':sum(x['record_kind']=='visual_option' for x in records.values()),
        'new_diagnostics':sum(x['record_kind']=='diagnostic' for x in records.values()),'new_bindings':len(bindings),
        'new_records':len(records),'reused_complete_CIDs':len(byold),'keyword_routes':len(routes),'semantic_cards':len(cards),
        'before_candidates':len(before['candidates']),'after_candidates':len(after['candidates']),
        'before_bindings':len(before['slot_bindings']),'after_bindings':len(after['slot_bindings']),
        'all_existing_candidates_bindings_catalog_policies_preserved':True,'native_approval':False,
        'research_to_current_source_drift':source_drift,'authored_file_allowlist':allow,'decisions':decisions,
        'index_status':'NOT_RUN','image_status':'NOT_RUN'}
    write(OUT/'data-integration.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='decisions'},ensure_ascii=False))

if __name__=='__main__':main()
