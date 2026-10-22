"""Build research-only JSON/Markdown/TSV. No runtime, model, index, or image calls."""
import collections,csv,hashlib,html,json,pathlib,re,sys
sys.dont_write_bytecode=True
from research_cards import CARDS
from research_sources import NOTES
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def dump(name,value): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def tsv(name,fields,rows):
    with (HERE/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
def source_key(url):return ('ko:' if 'scpko.' in url else '')+url.rsplit('/',1)[-1]

def build():
    access=json.loads((HERE/'SOURCE-ACCESS.json').read_text())
    sources=[]
    for i,a in enumerate(sorted(access,key=lambda x:x['url']),1):
        key=source_key(a['url']);note=NOTES.get(key)
        author=a.get('licensebox_author')
        sources.append(dict(source_id=f'S{i:03}',source_key=key,url=a['url'],title=html.unescape(a.get('title','')),
          retrieved_on='2026-10-22',access_status=a['access_status'],http_status=a.get('http_status'),
          text_sha256=a.get('text_sha256'),text_chars=a.get('text_chars'),revision_html=a.get('revision_html'),
          review_status='targeted_passages_reviewed' if note else 'collected_not_substantively_reviewed',
          read_scope=note[0] if note else 'HTML body downloaded; not used as fact support in this package',
          finding=note[1] if note else '',limit=note[2] if note else 'Do not cite as independently verified support.',
          detected_licensebox_author=author,author_status='parsed_from_licensebox_recheck_before_publication' if author else 'not_resolved',
          text_license='SCP Wiki default CC BY-SA 3.0; page-specific exceptions require review',
          media_reuse='none; individual images have separate provenance and licenses'))
    bykey={s['source_key']:s for s in sources}
    catalog_raw=(ASSETS/'photo_candidate_slot_catalog.json').read_bytes();catalog=json.loads(catalog_raw)['slot_catalog']
    cards=[]
    for c in CARDS:
        c=dict(c);c['source_ids']=[bykey[k]['source_id'] for k in c['source_slugs']]
        c['review_gates']=[{'gate_id':f"{c['card_id']}-R{i}",'required_visible_relation':r,'pixel_status':'NOT_RUN','partial_is_fail':True,'unobservable_is_pass':False} for i,r in enumerate(c['directed_relations'],1)]
        c['source_claim_scope']='Source supports term/context; geometry and photographic realization are authored proposals unless explicitly marked versioned.'
        c['regression_near_miss']=dict(input=c['nearest_confusion'],expected='reject_equivalence_or_leave_unobservable',execution='NOT_RUN')
        cards.append(c)
    dump('semantic-cards.json',{'schema':'scp-research-semantics/v1','date':'2026-10-22','catalog_sha256':sha(catalog_raw),'catalog_slot_count':len(catalog),'runtime_registration':'none','cards':cards})
    defaults={1:['I14','I13'],2:['I09','I08'],3:['I10','I13'],4:['I10'],5:['I12','I10','I14'],6:['M05'],7:['C04','C06'],8:['R08'],9:['R09','T06'],10:['T06','T05'],11:['N01','N03'],12:['G01'],13:['F05','F07'],14:['G11','F10'],15:['K01'],16:['A01'],17:['B05','B06','B07','B09'],18:['N06'],19:['E01'],20:['N05']}
    reference=json.loads((HERE/'reference-glossary.json').read_text());routes=[]
    for table in reference['tables']:
        section=int(table['section'].split('.')[0])
        for rawrow in table['rows']:
            term=rawrow[1] if section==4 else rawrow[0]
            matched=[c['card_id'] for c in cards if any(t and t.casefold() in term.casefold() for t in c['seed_terms'])]
            selected=list(dict.fromkeys(matched or defaults[section]))
            selected_cards=[c for c in cards if c['card_id'] in selected]
            routes.append({'seed_id':f'K{len(routes)+1:03}','section':section,'section_title':table['section'],'term':term,'original_row':rawrow,
              'input_status':'assistant_glossary_seed_untrusted_not_authority','definition_verification':'family_and_selected_primary_passages_not_every_individual_definition',
              'card_ids':selected,'optional_visual_card_ids':[c['card_id'] for c in selected_cards if c['observability'] in ('still','proxy','versioned')],
              'automatic_hard_obligation':False,'route_policy':'Resolve request meaning independently; preserve negation and selected source/version. Do not activate all linked realizations.',
              'source_ids':sorted({s for c in selected_cards for s in c['source_ids']})})
    dump('keyword-routes.json',{'schema':'scp-research-keyword-routes/v1','table_entry_count':len(routes),'section_count':20,'supplemental_non_table_boundary':'110-Montauk is covered by F07/B07; it is not counted as a 269th table entry.','routes':routes})
    drafts=[]
    for c in cards:
        if c['observability'] not in ('still','proxy','versioned'):continue
        drafts.append({'draft_id':'DR-'+c['card_id'],'card_id':c['card_id'],'proposal_ko':c['proposal_ko'],'proposal_en':c['proposal_en'],
          'owners':c['owners'],'directed_relations':c['directed_relations'],'proposed_slots':c['proposed_slots'],
          'dimensions_to_review':sorted({d for s in c['proposed_slots'] for d in catalog[s].get('dimensions',[])}),
          'conditions_to_author':'Actual requester-grounded owners, prerequisites, scope and applicable selected branch must be authored before native admission.',
          'effects_status':'UNKNOWN_PENDING_FULL_SOURCE_REVIEW','obligation_status':'Complete positive-source-unit and owner/endpoint obligations must be reviewed; card gates are not native proof.',
          'source_ids':c['source_ids'],'observability':c['observability'],'semantic_label_is_not_embedding_fact':True,
          'native_approval':False,'runtime_schema_compatible':False,'registration_status':'not_in_operating_manifest','evaluation_status':'NOT_RUN'})
    dump('candidate-drafts.json',{'schema':'scp-research-candidate-drafts/v1','draft_count':len(drafts),'runtime_import_allowed':False,'count_note':'Drafts are a subset of semantic cards, not additional independent research units.','drafts':drafts})
    dump('sources.json',sources)
    tsv('SOURCES.tsv',['source_id','source_key','url','review_status','read_scope','finding','limit','detected_licensebox_author'],[{k:s[k] for k in ['source_id','source_key','url','review_status','read_scope','finding','limit','detected_licensebox_author']} for s in sources])
    atlas=['# 참조 키워드 전체 경로','',f'20개 분야의 표 항목 {len(routes)}개. 정의 원문은 reference-glossary.json에 보존한다. 카드 연결은 선택 가능성을 나타내며 정의 검증·동의어 병합·의무 활성화가 아니다.','']
    for sec in range(1,21):
        rows=[r for r in routes if r['section']==sec];atlas+=['## '+rows[0]['section_title'],'','| ID | 키워드 | 조사 카드 | 선택 가능한 가시 실현 |','|---|---|---|---|']
        for r in rows:atlas.append(f"| {r['seed_id']} | {r['term'].replace('|','/')} | {', '.join(r['card_ids'])} | {', '.join(r['optional_visual_card_ids']) or '문맥/시간 검증으로 유지'} |")
        atlas.append('')
    (HERE/'KEYWORD-ATLAS.md').write_text('\n'.join(atlas)+'\n')
    visual=['# 시각 의미 카드','', '가시 제안은 원전 설정을 단일 정본으로 바꾸지 않는다. context/sequence 카드는 양성 시각 후보 초안으로 내보내지 않는다. 모든 native/검색/이미지 평가는 NOT_RUN이다.','']
    for c in cards:
        visual += [f"## {c['card_id']} {c['title']} [{c['observability']}]",'',c['proposal_ko'],'',c['proposal_en'],'']
        if c['owners']:
            visual+=['소유자·성분: '+'; '.join(f'{k}: {v}' for k,v in c['owners'].items()),'', '검토할 방향 관계: '+'; '.join(f"{r['from']} → {r['relation']} → {r['to']}" for r in c['directed_relations']),'']
        visual+=['가장 가까운 오인: '+c['nearest_confusion'],'','주장 한계: '+c['claim_limit'],'','역할 제안: '+', '.join(c['proposed_slots'])+' (catalog 존재 확인과 의미/native 승인은 별개)','', '근거: '+', '.join(f"[{bykey[k]['title']}]({bykey[k]['url']})" for k in c['source_slugs']),'']
    (HERE/'VISUAL-CARDS.md').write_text('\n'.join(visual)+'\n')
    selected_positive=['I01','I02','I03','I04','I06','I08','I11','M01','M02','M03','M04','C01','C02','C03','C05','R01','R02','R03','R04','R05','R06','T01','T04','G02','G07','F02','F03','F04','F08','K03','K08','K09','B01','B02','E02','E03','E06','E08']
    evals=[];byid={c['card_id']:c for c in cards}
    for cid in selected_positive:
        c=byid[cid];evals.append(dict(case_id='DEV-'+cid,cohort='development_positive',card_ids=cid,query_ko=c['proposal_ko'],query_en=c['proposal_en'],expected='Find compatible complete source if present; selected relation remains optional unless independently requested.',status='NOT_RUN'))
    boundary_en={
      'I08':'A decorative black page border, an empty blank and a physical hole are different from bars covering printed text.',
      'I10':'Safe is not harmless; Keter is not strength; personnel class and clearance are separate classifications.',
      'I11':'An orange coverall does not establish a criminal history, death-row status or consent to experimentation.',
      'M05':'A task-force name does not imply heavy weapons or fetish clothing; distinguish repeated unit numbers by nickname.',
      'C01':'A spiral or fractal on a panel does not prove a cognitohazard, memetic effect or lethal function.',
      'C04':'Antimemetics, invisibility, censorship, memory erasure and counter-memes are different concepts.',
      'C05':'The color of a glass vial does not identify an amnestic or mnestic drug or prove its efficacy.',
      'C07':'A single frozen hand gesture does not establish the full order, timing or effect of a kinetoglyph.',
      'R03':'A landscape photograph, mirror or screen on a wall is not necessarily a traversable doorway.',
      'R04':'An occluded stair, compressed perspective or lens distortion does not establish impossible topology.',
      'R09':'Type Green does not require green skin; Type Gray does not mean gray paint; Type Red does not require red light.',
      'T04':'False-color imagery inside a display is different from a naked-eye aura or measured Aspect Radiation.',
      'F05':'Do not assign every Nälkä community cannibalism, sexual cult practices, Yaldabaoth worship or an identical moral character.',
      'F07':'Do not combine every Scarlet King proposal or invent a specific sexual act for the redacted 110-Montauk procedure.',
      'F08':'A generic masked ball does not establish Alagadda; a black star graphic is not necessarily an astronomical object.',
      'K03':'The Alleys is a web-community name; a physical narrow street does not establish that organization.',
      'K05':'The name Seocheon Country Club alone does not establish a golf course, its operators or resurrection powers.',
      'B01':'Overlapping bodies, a cord or a hidden endpoint do not establish a continuous two-body tissue bridge.',
      'E02':'The former SCP-173 photograph has a different rights status from the article text; a still sculpture does not prove its movement rule.',
      'E08':'Deep furniture-store rows do not prove infinity; a blurred face differs from an explicitly featureless face.'}
    for cid,en in boundary_en.items():
        c=byid[cid];evals.append(dict(case_id='BOUNDARY-'+cid,cohort='boundary',card_ids=cid,query_ko=c['nearest_confusion'],query_en=en,expected='Reject the stated equivalence; do not infer nonvisual claims or activate genre-only obligations.',status='NOT_RUN'))
    ordinary=[('제품 사진 속 투명 유리 화병','A transparent glass flower vase in a product photograph'),('병원 복도 관찰창','A hospital corridor observation window'),('공항의 이중 보안문','Two successive airport security doors'),('주황색 공장 작업복','An orange factory coverall'),('일반 청력 보호 귀덮개','Ordinary hearing-protection earmuffs'),('빈티지 기계식 완구','A vintage mechanical toy'),('박물관의 콘크리트 조각','A concrete sculpture in a museum'),('서점 안의 긴 진열대','Long display shelves inside a bookshop'),('도시의 겨울 안개','Winter fog in a city'),('가정용 게임과 블록 장난감','A home video game beside toy blocks'),('의료 연구용 시료병','Specimen vessels for ordinary medical research'),('방패 모양 미술 문양','A shield-shaped decorative art pattern')]
    for i,(ko,en) in enumerate(ordinary,1):evals.append(dict(case_id=f'CTRL-{i:02}',cohort='ordinary_control',card_ids='',query_ko=ko,query_en=en,expected='No unrequested SCP identity, hazard, faction, mutation, drug effect, violence or reproductive context.',status='NOT_RUN'))
    nonvisual=[('초록 피부가 아닌 녹색 유형','A Type Green with no green skin'),('모두가 잊어버리는 존재','An entity whose information cannot be retained'),('기억을 없앤 약','A drug declared to erase memories'),('정확한 행위를 밝히지 않은 110-몽토크','110-Montauk without specifying its redacted actions'),('현실을 지키는 장치라는 설정','An apparatus declared to stabilize reality'),('죽을 수 없지만 늙는 세계','A world without death but with continued aging'),('주홍왕의 특정 제안을 아직 선택하지 않음','No specific Scarlet King proposal has been chosen'),('성적 강압의 과거를 외모로 단정하지 않음','Do not infer a history of sexual coercion from appearance')]
    for i,(ko,en) in enumerate(nonvisual,1):evals.append(dict(case_id=f'NONVIS-{i:02}',cohort='nonvisual_control',card_ids='',query_ko=ko,query_en=en,expected='Preserve declared context; no still-image PASS for mechanism, consent, cause, identity or history.',status='NOT_RUN'))
    tsv('EVALUATION-CASES.tsv',['case_id','cohort','card_ids','query_ko','query_en','expected','status'],evals)
    tsv('REALIZATIONS.tsv',['draft_id','card_id','observability','proposed_slots','proposal_ko','proposal_en'],[{**{k:d[k] for k in ['draft_id','card_id','observability','proposal_ko','proposal_en']},'proposed_slots':','.join(d['proposed_slots'])} for d in drafts])
    dump('PACKAGE-COUNTS.json',dict(reference_table_entries=len(routes),sections=20,cards=len(cards),card_modes=dict(collections.Counter(c['observability'] for c in cards)),priorities=dict(collections.Counter(c['priority'] for c in cards)),drafts=len(drafts),sources_accessed=len(sources),targeted_sources=sum(s['review_status']=='targeted_passages_reviewed' for s in sources),evaluation_cases=len(evals),evaluation_queries=len(evals)*2,cohorts=dict(collections.Counter(e['cohort'] for e in evals)),evaluation_query_limit='Authored development/engineering controls, not independent natural-query holdout; retrieval not run.'))
    print((HERE/'PACKAGE-COUNTS.json').read_text())
if __name__=='__main__':build()
