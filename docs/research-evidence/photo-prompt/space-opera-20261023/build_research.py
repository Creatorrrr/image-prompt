#!/usr/bin/env python3
"""Generate research artifacts only. No embeddings, registration or runtime writes."""
import collections,csv,hashlib,json,re
from pathlib import Path
from keywords_data import CONTINUATION,route
from research_cards import DATA
from research_context import DATA as CONTEXT_DATA
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def dump(n,x): (HERE/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def md(n,s): (HERE/n).write_text(s.strip()+'\n')
def escaped(s):return str(s).replace('|',' / ').replace('\n',' ')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+'|'.join('---' for _ in headers)+'|\n'+'\n'.join('| '+' | '.join(map(escaped,r))+' |' for r in rows)+'\n'

MAIN_SOURCES=[
('M01','ILM: The Force Awakens Portfolio','https://www.ilm.com/art-department/the-force-awakens-portfolio/','Introduction, used-universe discussion and Rick Carter design account; image gallery not pixel-reviewed','body','Used-universe and iterative visual storytelling are explicit production approaches.','Does not prescribe a universal palette, exact wear geometry or a kitbashing history for an arbitrary model.'),
('M02','Art Directors Guild: Michael and Denise Okuda','https://assets.adg.org/media/press/2018-05-04_21-57-49/Star_Trek_Icons_Michael_Denise_Okuda_.pdf','Two-page release; Michael Okuda display/LCARS credits on page 2','body','LCARS is a named fictional interface with a specific production origin.','No inference that all floating displays are LCARS or that depicted systems function in reality.'),
('M03','ion studio: 25th Century LCARS','https://ion.studio/25th-century-lcars','Season One, palette, desk holo and Season Two production account','body','A participating designer describes palette choices, diegetic displays and the move to 3D holographic representations.','Production account only; palette and design are version-dependent; no gallery pixels inspected.'),
('M04','NASA: Environmental Control and Life Support Systems','https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/','Overview and Water Recovery, Air Revitalization, Oxygen Generation sections','body','Water recovery, cabin-air cleaning/CO2 removal and oxygen generation have distinct functions and material flows.','No new recovery-rate/current-mission claim; apparatus geometry and failure scenes are authored, not measured.'),
('M05','NASA: 11.0 Spacesuits','https://www.nasa.gov/reference/11-0-spacesuits-vol-2/','LEA/EVA definitions; interfaces; 11.1.8 depressurization protection; 11.2.1 suited functions','body','Pressure protection and independent EVA life support differ from ordinary flight clothing; mobility and suit interfaces matter.','Selected sections only; no certification or medical diagnosis, no claim that appearance proves pressure integrity.'),
('M06','NASA: What is a light-year?','https://science.nasa.gov/exoplanets/what-is-a-light-year/','Opening definition and star/galaxy scale discussion','body','Light-year is a distance unit; star systems and galaxies are different scales.','Dated exoplanet counts and numerical mission/cosmology headlines are excluded.'),
('M07','Partridge et al.: An extra-uterine system to physiologically support the extreme premature lamb','https://www.nature.com/articles/ncomms15112','Article open redirected to inaccessible authorization endpoint; PMC mirror showed browser check','failed','No article-body scientific claim adopted.','Not a read full paper; do not use as proof of current human complete ectogenesis.'),
('M08','CHOP: A Unique Womb-Like Device Could Reduce Mortality and Disability for Extremely Premature Babies','https://www.chop.edu/news/unique-womb-device-could-reduce-mortality-and-disability-extremely-premature-babies','Search excerpt of 2017 release; body returned 403','search_excerpt','Indexed release describes a fluid-filled animal-study support environment.','Provisional source lead only; re-open body/primary paper before scientific adoption; no current human treatment claim.'),
('M09','Office of Naval Research: Electromagnetic Railgun Prototype Launcher','https://www.onr.navy.mil/media-center/news-releases/bang-navy-begins-tests-electromagnetic-railgun-prototype-launcher','2012 historical release, mechanism paragraph','body','Electromagnetic acceleration acts on a sliding armature between two rails.','Historical mechanism only; no current program status, performance numbers or coilgun engineering adopted.'),
('M10','Niven-hosted Known Space Concordance: Ringworld Appendix','https://news.larryniven.net/concordance/content.asp?ovr=t&page=Ringworld+Appendix','Search excerpt only; body returned 502','search_excerpt','Indexed concordance uses a star and ribbon-world distinction.','Concordance is not the novel text or a verified author-authored design; novel/design evidence remains required.')]

THEMES={'ships':['T11','T14','C01'],'propulsion':['T01','T02','T04','M06'],'habitats':['T05','T06','T08','T15'],'life_support':['M04','M05','T03'],'ftl':['T13','C05'],'weapons':['T11','T12','M09'],'alien':['T09','T10','C03'],'identity':['C07','C09','C10','C11','C16'],'politics':['C02','C04','C06','C08','C14'],'trade':['C08','C13','C11'],'contact':['C03','C05'],'religion':['C20','C08'],'autonomy':['C19','C17','M08'],'family':['C15','C03','C13'],'costume':['M05','C01'],'used':['M01'],'interface':['M02','M03'],'atrocity':['C18','T12'],'versioned':['C08','C11','C17','C18']}
THEMES['war']=['C13','C14','C15','C18']
ROUTE_NOTES={
'still':'選択した現形の構造を判定する。語だけで色・数量・勢力を固定しない。',
'proxy':'현재 형상·관계는 표현할 수 있으나 제목의 제도·원인·의식·의도는 별도 문맥이다.',
'sequence':'변화·순서·인과·동일성은 연속 증거 또는 명시 서사가 필요하다. 정지 도상은 정황이다.',
'context':'장르·사회·서사·해석의 문맥으로 보존한다. 자동 시각 의무와 효과 권한을 부여하지 않는다.',
'nonvisual':'단일 사진으로 값·정의·의식·권리를 판정하지 않는다. 표시된 텍스트는 극중 주장이다.',
'versioned':'작품·판본·출처 범위를 유지한다. 고유어를 일반 개념이나 고정 외형으로 자동 확장하지 않는다.'}
ROUTE_NOTES['still']='선택한 현재 형태의 구조를 판정한다. 용어만으로 색·개수·세력을 고정하지 않는다.'

def seeds():
    p=json.loads((HERE/'reference-preview.json').read_text())
    text=p['turns'][0]['items'][1]['text'];rows=[];section=''
    for line in text.splitlines():
        if line.startswith('## '):section=line[3:]
        m=re.match(r'^\| \*\*(.*?) — (.*?)\*\* \|',line)
        if m:rows.append(dict(en=m[1],ko=m[2],section=section,provenance='connector_body'))
    assert len(rows)==171
    for line in CONTINUATION.splitlines():
        if not line.strip():continue
        if line.startswith('## '):section=line[3:];continue
        en,ko=line.split('|');rows.append(dict(en=en,ko=ko,section=section,provenance='browser_rendered_table_recovered'))
    assert len(rows)==291 and len({r['en'] for r in rows})==291
    for i,r in enumerate(rows,1):r.update(seed_id=f'K{i:03}',route=route(r['en'],r['section']),handling=ROUTE_NOTES[route(r['en'],r['section'])],individually_source_verified=False)
    return rows

def main():
    source=[]
    for f in ['space-sources-agent.json','civilization-sources-agent.json']:source+=json.loads((HERE/f).read_text())['sources']
    source += [dict(zip(['id','title','url','read_scope','access','supports','limits'],r)) for r in MAIN_SOURCES]
    for r in source:r.update(retrieved_on='2026-10-23',scene_authority='bounded_concept_support_only; geometry is authored; no source-pixel review')
    dump('sources.json',source)
    with (HERE/'SOURCES.tsv').open('w') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['id','title','url','access','read_scope','supports','limits'])
        for r in source:w.writerow([r[k] if isinstance(r[k],str) else '; '.join(r[k]) for k in ['id','title','url','access','read_scope','supports','limits']])
    ks=seeds();cards=[];contexts=[]
    for line in filter(str.strip,CONTEXT_DATA.splitlines()):
        did,section,distinction,visible,limits,src=line.split('|')
        contexts.append(dict(context_id=did,seed_ids=[k['seed_id'] for k in ks if k['section'].startswith(section+'.')],distinction=distinction,visible_support=visible,not_established=limits,source_ids=src.split(','),semantic_authority='context_only',native_approval=False))
    dump('context-records.json',contexts)
    md('CONTEXT-DISTINCTIONS.md','# 문맥과 비가시 의미의 구분\n\n선정적·폭력적 항목도 원문 목록에 유지한다. 아래 기록은 개별 법률·의학 판정이나 시각 도상 처방이 아니다. 같은 주제의 문맥 기록들이 함께 적용되며 자동 시각 효과를 부여하지 않는다.\n\n'+'\n\n'.join(f"## {d['context_id']}\n\n{d['distinction']}\n\n가시 지지: {d['visible_support']}\n\n주장 한계: {d['not_established']}\n\n출처: {', '.join(d['source_ids'])}. 정확한 읽은 범위는 [출처 기록](SOURCE-LEDGER.md)에 있다." for d in contexts))
    catalog=json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    remap={'body_geometry':'body_form','relationship':'relational_action','wardrobe':'wardrobe_style'}
    gaps={21:'Ringworld 원전/공식 디자인의 띠·벽·항성 관계를 본문으로 확인해야 한다. M10은 발췌인 hosted concordance다.',25:'M09는 레일건만 지지한다. 코일건 원전 공학 자료를 확보하기 전 두 구조 비교 채택을 보류한다.',31:'지표 유리화의 작품별 피해 범위와 원인을 공식 원전에서 확인해야 한다. C18은 Exterminatus 명령이지 glassing 기전이 아니다.',42:'M07 본문 접근 실패·M08 발췌만 확보. 동물의 부분 발생 지원과 인간 완전 체외 임신을 구분한 원전 재검토가 필요하다.'}
    for i,line in enumerate(filter(str.strip,DATA.splitlines()),1):
        title,seedfr,en,ko,ow,ed,conf,limit,theme,sl,action=line.split('|')
        owners=dict(x.split(':',1) for x in ow.split(';'))
        edges=[dict(zip(['from','relation','to'],x.split('>'))) for x in ed.split(';')]
        ids=[]
        for fragment in seedfr.split(';'):
            matches=[k['seed_id'] for k in ks if fragment.casefold() in k['en'].casefold()]
            assert matches,(i,fragment)
            ids.extend(matches)
        slots=list(dict.fromkeys(remap.get(x,x) for x in sl.split(',')))
        assert all(s in catalog for s in slots)
        src=THEMES[theme].copy()
        if i==12:src=['T01','T02']
        if i==13:src=['T04']
        if i==14:src=['T03','M04']
        if i==16:src=['T13']
        if i==21:src=['T06','M10']
        if i==22:src=['T08']
        if i==25:src=['M09']
        if i==42:src=['M07','M08','C19']
        if i==10:action='refine'
        if i==72:action='reuse'
        if i in gaps:action='defer'
        c=dict(card_id=f'V{i:02}',title=title,seed_ids=sorted(set(ids)),proposal_en=en,proposal_ko=ko,components=[dict(owner=k,description=v) for k,v in owners.items()],owners=owners,directed_relations=edges,nearest_confusion=conf,claim_limit=limit,source_ids=src,source_claim_scope='sources support bounded definitions, constraints or work context; this exact geometry is authored, not a sourced design',theme=theme,proposed_slots=slots,proposed_action=action,additional_research=gaps.get(i),native_approval=False,registration_status='research_only',observability='context_support_only' if action=='context' else 'authored_still_or_proxy',review_gates=[dict(gate_id=f'V{i:02}-R{n}',required_visible_relation=e,status='NOT_RUN',partial_is_fail=True,unobservable_is_pass=False) for n,e in enumerate(edges,1)])
        cards.append(c)
    assert len(cards)==72
    for k in ks:
        k['card_ids']=[c['card_id'] for c in cards if k['seed_id'] in c['seed_ids']]
        k['context_record_ids']=[d['context_id'] for d in contexts if k['seed_id'] in d['seed_ids']]
    dump('keyword-routes.json',ks);dump('semantic-cards.json',cards)
    drafts=[dict(draft_id='D'+c['card_id'][1:],card_id=c['card_id'],en=c['proposal_en'],ko=c['proposal_ko'],slots=c['proposed_slots'],owners=c['owners'],relations=c['directed_relations'],source_ids=c['source_ids'],application_contract='Optional complete scene proposition. Preserve every stated owner, count, attachment and relationship together. Compare with frozen requester anchors and all effects before selection. Sources, titles and graphs grant no native facts or permissions.',intrinsic_conditions='NOT_AUTHORED: inspect selected full source and requester compatibility before registration',intrinsic_effects='NOT_AUTHORED: do not use empty effects to bypass frozen dimensions',native_source_review='NOT_RUN',runtime_id=None) for c in cards if c['proposed_action'] not in ['context','defer']]
    dump('candidate-drafts.json',drafts)
    md('KEYWORD-ATLAS.md','# 키워드 전체 경로\n\n참조 대화 291개 원 항목. `/`로 묶인 표제는 원문 한 행을 한 항목으로 유지했다. 아래 경로는 연구자의 처리 판단이며 각 용어 정의 전체의 독립 검증을 뜻하지 않는다.\n\n'+table(['ID','원 주제','English','한국어','경로','카드'],[[k['seed_id'],k['section'],k['en'],k['ko'],k['route'],', '.join(k['card_ids']) or '문맥/원전 조사'] for k in ks]))
    paragraphs=['# 시각 의미 카드 72개','모든 장면은 선택형 저술안이다. sources.json의 출처는 정의·제약·작품 맥락만 지지하며, 구성·재료·상태·표시값의 정확한 픽셀 사실을 승인하지 않는다. `NOT_RUN`, `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`를 유지한다.']
    for c in cards:
        links='; '.join(f'[{x}](sources.json)' for x in c['source_ids'])
        paragraphs.append(f"## {c['card_id']} · {c['title']}\n\n{c['proposal_ko']}\n\n{c['proposal_en']}\n\n- 소유자/성분: "+'; '.join(f'{k}: {v}' for k,v in c['owners'].items())+'\n- 방향 관계: '+'; '.join(f"{e['from']} → {e['relation']} → {e['to']}" for e in c['directed_relations'])+f"\n- 혼동: {c['nearest_confusion']}\n- 주장 한계: {c['claim_limit']}\n- 제안 슬롯: {', '.join(c['proposed_slots'])}; 잠정 판단: {c['proposed_action']}\n- 출처: {links}. 위 정확한 장면은 저술안.\n- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가."+(f"\n- 채택 전 공백: {c['additional_research']}" if c['additional_research'] else ''))
    md('VISUAL-CARDS.md','\n\n'.join(paragraphs))
    md('SOURCE-LEDGER.md','# 출처와 실제 확인 범위\n\n본문 접근은 전체 원전 독파나 이미지 픽셀 검토를 뜻하지 않는다. 검색 발췌·실패 기록은 승인 근거에서 제외한다.\n\n'+'\n\n'.join(f"## {s['id']} · [{s['title']}]({s['url']})\n\n접근: {s['access']}. 확인: {s['read_scope']}\n\n지지: "+('; '.join(s['supports']) if isinstance(s['supports'],list) else s['supports'])+'\n\n한계: '+('; '.join(s['limits']) if isinstance(s['limits'],list) else s['limits']) for s in source))
    # Candidate neighbors are source observations, never retrieval rankings.
    snaps=json.loads((HERE/'existing-source-snapshots.json').read_text());audit=json.loads((HERE/'CORPUS-AUDIT.json').read_text())
    allc={};allb={};mods={}
    for m in json.loads((ASSETS/'photo_candidate_corpus_manifest.json').read_text())['modules']:
        j=json.loads((ASSETS/m['file']).read_text())
        allc.update(j.get('candidates',{}));allb.update(j.get('slot_bindings',{}))
        for cid in j.get('candidates',{}):mods[cid]=m['file']
    fixed={5:'cand_e3a169af62dc52b08d248c262e7140e1',6:'cand_1fb8cbe7a3515a028ee63ae7f2877291',8:'cand_190e6d55275459aa9918a04695be8300',10:'cand_7b74028598cd503abdcd5256886084e5',11:'cand_6002ff059dd85912ad9037019ee3299f',14:'cand_437476164ca957b29be8f79121d9d23d',36:'cand_610afa98d8c8552a99d827ad83f47f01',72:'cand_0331b45fc2e85e2bbb4611167d7187a0'}
    selected=[];matrix=[]
    for i,c in enumerate(cards,1):
        cid=fixed.get(i);near=[]
        if cid in allc:
            near=[cid];r=allc[cid]
            selected.append(dict(card_id=c['card_id'],cid=cid,module=mods[cid],record=r,bindings={k:b for k,b in allb.items() if b.get('candidate_id')==cid},canonical_sha256=hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()))
        matrix.append(dict(card_id=c['card_id'],action=c['proposed_action'],existing_neighbor_ids=near,neighbor_equivalence='not_approved; compare complete positive fields, native facts, branch, conditions, effects and role guards',rationale=('기존 장면의 전체 명제와 조건/효과를 먼저 비교한다. 소유자·연결·맥락 차이가 있으면 successor/refine으로 분리한다.' if near else '고정 필드 진단만으로 의미 부재를 판정하지 않는다. 전체 코퍼스 의미 검토 후에만 신규 여부를 확정한다.'),additional_research=c['additional_research'],native_qualification='NOT_RUN',retrieval='NOT_RUN',pixels='NOT_RUN'))
    dump('adoption-matrix.json',matrix);dump('topology-neighbors.json',selected)
    # One positive case per draft plus hard contrast cases and independent general controls.
    cases=[dict(case_id=f'E{n:03}',group='development',query_en=d['en'],query_ko=d['ko'],expected_card_ids=[d['card_id']],expected_behavior='expose complete compatible proposition; never require adoption or title-based fact',status='NOT_RUN') for n,d in enumerate(drafts,1)]
    contrasts=[('postal carrier','우편 배달원','No spacecraft-carrier import'),('revolver cylinder','리볼버 실린더','No rotating habitat import'),('scuba cylinder and hose','스쿠버 실린더와 호스','No orbital habitat or EVA suit substitution'),('holographic nail polish','홀로그래픽 네일 광택','No floating display import'),('a cassette album archive','카세트 음반 기록고','No compulsory spacecraft or horror'),('a smiling adult beside restraints','구속구 옆 미소 짓는 성인','No consent/coercion conclusion'),('two similar people','닮은 두 사람','No cloning, kinship or mind-continuity conclusion'),('a barren planet surface','불모 행성 표면','No sterilization or genocide conclusion'),('fictional Pon Farr context','허구의 폰 파르 문맥','Keep work-specific biological premise separate from consent'),('an order named Exterminatus','엑스테르미나투스라는 명령','No automatic exploding planet'),('an alien diplomat without tentacles','촉수가 없는 외계 사절','Do not add tentacles or hive mind'),('no weapons; shipboard shared meal','무기 없이 선내 공동 식사','No automatic fleet battle'),('an ordinary pressure suit','일반 압력복','No sexual costume import'),('space opera without FTL','초광속 없는 스페이스 오페라','No compulsory warp or gate'),('a shared server with separate users','별도 사용자의 공용 서버','No shared consciousness conclusion'),('a clear-sided research vessel','투명 측면 연구 용기','No gestation, life or parenthood conclusion'),('an ordinary library genealogy book','일반 도서관 족보 책','Preserve human-only condition; no dynastic marriage assumption'),('a sealed gate in a medieval castle','중세 성의 닫힌 문','No star gate import'),('a bright blue nebula photograph','밝고 푸른 성운 사진','Keep filter mapping and local sky appearance distinct'),('a damaged hull with a free tether end','자유 끝이 있는 안전줄과 손상 선체','Do not mark the detached end as attached')]
    for en,ko,expect in contrasts:cases.append(dict(case_id=f'E{len(cases)+1:03}',group='boundary',query_en=en,query_ko=ko,expected_card_ids=[],expected_behavior=expect,status='NOT_RUN'))
    controls=[('studio portrait of an adult in a wool coat','울 코트를 입은 성인 스튜디오 인물 사진'),('ordinary library reading table','일반 도서관 독서 탁자'),('product photo of a ceramic cup','도자기 컵 제품 사진'),('wildlife bird on a branch','나뭇가지의 야생 새'),('a diver holding a regulator','레귤레이터를 잡은 다이버'),('daylight city street','낮의 도시 거리'),('a chef preparing soup','수프를 만드는 요리사'),('a mechanic repairing a bicycle','자전거 수리 정비사'),('a family sharing a meal at home','집에서 식사하는 가족'),('a night sky with no ships','함선 없는 밤하늘'),('ordinary medical corridor','일반 의료 복도'),('a non-sci-fi wedding invitation','SF가 아닌 결혼 초대장')]
    for en,ko in controls:cases.append(dict(case_id=f'E{len(cases)+1:03}',group='general_control',query_en=en,query_ko=ko,expected_card_ids=[],expected_behavior='no forced space-opera, sexual, horror or political additions; preserve baseline compatible behavior',status='NOT_RUN'))
    dump('evaluation-cases.json',cases)
    with (HERE/'EVALUATION-CASES.tsv').open('w') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['id','group','query_en','query_ko','expected','status'])
        for r in cases:w.writerow([r['case_id'],r['group'],r['query_en'],r['query_ko'],r['expected_behavior'],r['status']])
    stats=dict(keywords=len(ks),routes=dict(collections.Counter(k['route'] for k in ks)),cards=len(cards),drafts=len(drafts),sources=len(source),access=dict(collections.Counter(s['access'] for s in source)),relations=sum(len(c['directed_relations']) for c in cards),adoption=dict(collections.Counter(c['proposed_action'] for c in cards)),evaluation_cases=len(cases),bilingual_queries=len(cases)*2,candidates=audit['candidates'],bindings=audit['bindings'],modules=audit['modules'])
    dump('COUNTS.json',stats);print(json.dumps(stats,ensure_ascii=False))

if __name__=='__main__':main()
