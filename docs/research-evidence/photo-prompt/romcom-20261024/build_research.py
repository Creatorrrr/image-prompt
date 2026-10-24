"""Build review-only research artifacts. Never imports or writes runtime data."""
import collections
import csv
import hashlib
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT/'skills/photo-prompt-image-generator/assets'

def read(name):
    return json.loads((HERE/name).read_text())

def write(name, value):
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def rows(name):
    with (HERE/name).open() as f:
        return list(csv.DictReader(f, delimiter='|'))

def refs(text):
    return [f'T{int(t):02d}-R{int(r):02d}' for t,r in (s.split(':') for s in text.split(','))]

def md(text):
    return text.replace('|', '\\|').replace('\n',' ')

SOURCES = [
 ('R00','참조 대화 전체','ChatGPT conversation supplied by requester','https://chatgpt.com/c/6adb7078-3e30-83ee-a7e7-d068606052dc','Chrome rendered DOM, 2026-10-24','317 original term rows and 7 authored scene examples; source vocabulary, not an independent authority.','Definitions and examples are retained as reference material. No instruction or generation authorization is inherited.'),
 ('R01','Guide to Contemporary Romance; Romance Tropes in Books','Harlequin','https://harlequin.com/pages/guide-to-contemporary-romance','web open and publisher search result','Publisher usage of rom-com, friends/enemies to lovers, fake dating and second chance.','Publishing usage does not define visible geometry, sexual explicitness, or universal film endings.'),
 ('R02','Glossary of Genres and Tropes','University of Texas at Austin Libraries','https://guides.lib.utexas.edu/c.php?g=1382248&p=11369014','web open','Distinguishes relationship tropes including forced proximity, friends to lovers, love triangle, opposites, second chance and slow burn.','A reading guide is evidence of trope usage, not a still-image diagnostic or exhaustive cross-cultural taxonomy.'),
 ('R03','Flirting with screwball','BFI','https://www.bfi.org.uk/features/flirting-screwball','web open, paragraphs about the mismatched couple and antagonistic courtship','Screwball combines mismatched partners, social contrast, verbal conflict and chaotic plotting.','Historical film analysis; a noisy pose or bright light alone cannot establish screwball.'),
 ('R04','つんでれ','Shogakukan Digital Daijisen via Kotobank','https://kotobank.jp/word/つんでれ-573086','web open, definition','Documents contrast between an aloof manner and affectionate behavior in particular settings.','The entry uses gendered examples. This source alone does not verify every dere subtype or impose a gender requirement.'),
 ('R05','Ship: Words We Are Watching','Merriam-Webster','https://www.merriam-webster.com/wordplay/ship-words-were-watching','web open','Documents shipping as audience support for a relationship and related fan vocabulary.','Does not make a preferred pairing canon or verify every fandom term.'),
 ('R06','相合傘','Shogakukan dictionaries via Kotobank','https://kotobank.jp/word/相合傘-420912','web open, senses 1 and 2','Separates sharing a physical umbrella from a drawn umbrella with names.','The historical gendered wording is source scope, not a condition on modern subjects.'),
 ('R07','萌え袖','Shogakukan Digital Daijisen via Kotobank','https://kotobank.jp/word/萌え袖-2627057','web open, definition','Long cuffs cover part of the hands rather than leaving the hands fully outside.','Neither age nor relationship nor hoodie ownership follows from the sleeve geometry.'),
 ('R08','壁ドン','Shueisha imidas','https://imidas.jp/ryuko/detail/N-101-2151.html','web open, 2014/08 entry','Separates noise-protest wall banging from the later romance gesture with a hand against a wall near another person.','The source describes cultural staging; it does not prove consent, force or a particular emotion in an image.'),
 ('R09','女性の恋愛と肌に関する意識調査','Mandom','https://www.mandom.co.jp/release/pdf/2015112701.pdf','web PDF, printed page 2 footnote, extracted line 103','A 2015 corporate release uses agokui for raising another person’s chin to orient the face.','Limited primary usage, not a dictionary or normative consent claim. Survey distances and preferences are not generalized here.'),
 ('R10','Exposed: A History of Lingerie','The Museum at FIT','https://exhibitions.fitnyc.edu/exposed-lingerie-history/','web open, introductory classification and collection captions','Distinguishes structured support garments from unstructured lingerie and documents changing inner/outerwear uses.','Supports garment history and structure; individual authored seams, strap counts and fiber chemistry need separate evidence.'),
 ('R11','Manzai: A Uniquely Japanese Style of Comedy','Japan Up Close','https://japanupclose.web-japan.org/techculture/c20231013_1.html','web open, Japanese Manzai Style','Explains the funny boke role and corrective tsukkomi role in a pair’s comic exchange.','Does not equate tsukkomi with violence or permit inference of spoken content from a pose.'),
 ('R12','What is the shot-reverse shot?','Adobe','https://www.adobe.com/creativecloud/video/production/cinematography/camera-shots-and-angles/reverse-shot.html','web open, continuity editing explanation','Defines an alternating sequence of angles linking a character, the viewed subject and a reaction.','A still OTS frame or split-screen does not establish the whole editing sequence; other authored camera choices are not sourced definitions.'),
 ('R13','What is slapstick comedy?','BBC Maestro','https://www.bbcmaestro.com/blog/what-is-slapstick-comedy','web open, physical comedy and structural elements','Discusses exaggerated physical action, falls, chases, repetition, inversion and anticipation.','Not a universal injury model and not evidence that an isolated pictured state is funny.'),
 ('R14','Yukata (Light Japanese Robe)','Japan Search / National Diet Library gallery','https://jpsearch.go.jp/en/gallery/ndl-q4zQoa0BBXw','web open, introductory text','Documents a summer unlined cotton kimono and historical bathing, everyday and festival uses.','Appearance alone cannot prove fiber composition, date or exact garment classification.'),
 ('R15','ラブコメディ作品における「戦わない男性」表象','Myu Sakai, Annual Review of Cultural Studies 11 (2023), pp.141-162','https://www.jstage.jst.go.jp/article/arcs/11/0/11_141/_pdf','web PDF, printed p.150 / zero-based PDF p.9','The To LOVE-Ru analysis discusses accidental sexual contact and narrative attribution of responsibility.','A case study of particular manga; not a universal account, a consent finding, or a visual generation recipe.'),
]
SOURCES += [
 ('R16','banter','Merriam-Webster','https://www.merriam-webster.com/dictionary/banter','web definition','Witty, friendly teasing in speech.','Not a visible facial diagnosis or evidence of affection.'),
 ('R17','deadpan','Merriam-Webster','https://www.merriam-webster.com/dictionary/deadpan','web definition','An impassive expression or matter-of-fact delivery.','A blank face alone does not establish comic speech or timing.'),
 ('R18','double entendre','Merriam-Webster','https://www.merriam-webster.com/dictionary/double%20entendre','web definition','An expression admitting two interpretations, often including a sexually suggestive one.','Requires language and context; a suggestive-looking prop does not prove a specific utterance.'),
 ('R19','camisole','Merriam-Webster','https://www.merriam-webster.com/dictionary/camisole','web definition','A short sleeveless garment; also has a historical jacket sense.','Strap thickness, transparency and inner/outer use require particular design evidence.'),
 ('R20','bustier','Merriam-Webster','https://www.merriam-webster.com/dictionary/bustier','web definition','A close-fitting top, often strapless, used as underwear or outerwear.','Often is not always; boning, exact length and fastening are design variants.'),
 ('R21','negligee','Merriam-Webster','https://www.merriam-webster.com/dictionary/negligee','web definition','Includes a long flowing dressing gown, usually sheer, and a broader informal-attire sense.','This corrects the overly broad one-shape reading; usually sheer does not mandate transparency in every scene.'),
 ('R22','pratfall','Merriam-Webster','https://www.merriam-webster.com/dictionary/pratfall','web definition','A fall onto the buttocks, with a figurative sense of humiliating blunder.','The fall is an event, not every seated floor pose.'),
 ('R23','double take','Merriam-Webster','https://www.merriam-webster.com/dictionary/double%20take','web definition','A delayed reaction following initial failure to notice an unusual situation.','Do not reduce this temporal relation to one generic surprised face.'),
 ('R24','fan service','Dictionary.com','https://www.dictionary.com/browse/fan-service','web definition','Audience-appealing additions to fiction, with sexual material a prominent but nonexclusive use.','Audience intention and reception remain separate from visible appearance.'),
 ('R25','ecchi','Dictionary.com','https://www.dictionary.com/browse/ecchi','web definition','Documents a subculture category involving light sexual themes and imagery.','English borrowing scope does not define all Japanese everyday usage or a standardized age rating.'),
 ('R26','Fanfic/Fandom terms and abbreviations','More Than That fan community','https://mtt.just-once.net/fanfiction/viewpage.php?page=glossary','web community-authored glossary','Separates canon, fanon, headcanon and a fan’s preferred OTP; also distinguishes canon pairings.','Primary evidence of usage within this community, not an exhaustive or universal fandom standard.'),
]

DEFAULT_CONTEXT = {1:'X01',2:'X02',3:'X03',4:'X04',5:'X05',6:'X06',7:'X07',8:'X08',9:'X09',10:'X07',11:'X10',12:'X10',13:'X11',14:'X12',15:'X12',16:'X12',17:'X13',18:'X14',19:'X15',20:'X16',21:'X17',22:'X19'}
# Only these exact reference terms receive independent lexical corroboration.
LEXICAL = {
 'R01':['1:1','2:3','2:5','2:7','2:10'],
 'R02':['2:3','2:5','2:7','2:8','2:14','3:1','4:12'],
 'R03':['1:3'], 'R04':['6:1'], 'R05':['22:2','22:3'],
 'R06':['11:7'], 'R07':['14:6'], 'R08':['12:11'], 'R09':['12:12'],
 'R10':['15:9','15:12'], 'R11':['8:3','8:4'], 'R12':['17:4'],
 'R13':['9:1','9:2','9:9'], 'R14':['16:6'], 'R15':['20:7'],
 'R16':['8:1'], 'R17':['8:5'], 'R18':['19:6'], 'R19':['15:8'],
 'R20':['15:13'], 'R21':['15:10'], 'R22':['9:2'], 'R23':['9:4'],
 'R24':['19:4'], 'R25':['19:3'], 'R26':['22:1','22:4','22:5','22:6','22:7'],
}
# Cross-topic neighbors are reviewed from full current source, not inferred from lexical hit counts.
HAREM_NEIGHBORS = {
 'R02':'H06','R03':'H07','R04':'H08','R05':'H05','R06':'H11','R09':'H10',
 'R11':'H13','R12':'H21','R15':'H15','R17':'H14','R19':'H12','R20':'H20',
 'R22':'H18','R26':'H16','R27':'H17','S06':'H22','S08':'H04',
 'E05':'A10','E04':'P04','W04':'W03','W08':'W06','W12':'W09','W13':'W19',
 'W14':'W14','W15':'W15','W16':'W16','W17':'W12','W18':'W13',
 'W19':'W17','W20':'W18','F01':'C03','F02':'C04','F03':'C08',
}

def main():
    capture=read('reference-browser.json')
    source_rows=[]
    for sid,title,publisher,url,access,support,limit in SOURCES:
        source_rows.append(dict(id=sid,title=title,publisher=publisher,url=url,accessed_date_kst='2026-10-24',access_method=access,supported_claim=support,claim_limit=limit))
    write('sources.json',source_rows)
    source_md=['# 출처와 주장 범위','', '2026-10-24 KST. 외부 문서 26개와 원 대화다. 출처가 지원하는 어휘/문맥과 연구자가 저작한 기하를 구별한다. 원 대화는 독립 검증 출처가 아니다.','']
    for s in source_rows:
        source_md += [f"## {s['id']} {s['title']}",'',f"[{s['publisher']}]({s['url']})",'',f"- 확인: {s['access_method']}",f"- 지원하는 주장: {s['supported_claim']}",f"- 한계: {s['claim_limit']}",'']
    (HERE/'SOURCES.md').write_text('\n'.join(source_md)+'\n')
    lexical=collections.defaultdict(list)
    for sid, rr in LEXICAL.items():
        for ref in rr:
            lexical[refs(ref)[0]].append(sid)
    contexts=[]
    for row in rows('contexts-authored.tsv'):
        contexts.append(dict(id=row['id'],label_ko=row['label_ko'],mode='context_only',tables=[int(x) for x in row['tables'].split(',')],source_ids=row['sources'].split(','),distinction_ko=row['distinction_ko'],required_evidence=row['required_evidence'],optional_card_ids=row['optional_cards'].split(',') if row['optional_cards'] else [],positive_en=None,runtime_visual_binding=False,native_approval=False))
    cards=[]
    for row in rows('cards-authored.tsv'):
        edges=[dict(zip(('from','relation','to'),e.split('>'))) for e in row['relations'].split(';')]
        cards.append(dict(id=row['id'],label_ko=row['label_ko'],mode='optional_visual_realization',term_refs=refs(row['term_refs']),suggested_slots=row['slots'].split(','),source_ids=row['sources'].split(','),positive_en=row['positive_en'],positive_ko=row['positive_ko'],owner_nodes=sorted({e[k] for e in edges for k in ('from','to')}),research_relations=edges,observable_gate=row['observable_gate'],confusion_boundary=row['confusion_boundary'],provenance='agent_authored_research_option',source_relation='Sources support their listed claims only. Geometry is an optional authored realization, not a sourced universal definition.',activation='Only after independent requester meaning, owner prerequisites and permitted effects are established; no genre-triggered insertion.',native_approval=False,automatic_hard_activation=False,pixel_status='NOT_RUN',runtime_registration='NOT_APPLIED',graph_scope='Research review metadata only; not source qualification, a frozen fact or effect permission.'))
    write('semantic-cards.json',dict(schema='romcom-research-semantics/v1',visual_cards=cards,context_cards=contexts))
    routes=[]
    for t,table in enumerate(capture['content']['tables'][:22],1):
        for r, cells in enumerate(table[1:],1):
            kid=f'T{t:02d}-R{r:02d}'
            cx=DEFAULT_CONTEXT[t]
            if t==21 and r in (10,11,12,13): cx='X18'
            linked=[c['id'] for c in cards if kid in c['term_refs']]
            corroborated=lexical.get(kid,[])
            routes.append(dict(id=kid,table=t,row=r,original_label=cells[0],original_definition=cells[1],context_card_id=cx,visual_card_ids=linked,visual_relation='optional_or_adjacent_example_not_complete_definition' if linked else 'context_or_further_form_development',lexical_evidence_status='specific_claim_corroborated' if corroborated else 'reference_definition_preserved_independent_term_check_pending',lexical_source_ids=['R00']+corroborated,source_scope_note='Corroboration covers only sources.json supported_claim, not all clauses of the original definition.',routing_decision='review_optional_realization' if linked else 'retain_context_and_schedule_missing_form_review',runtime_hard_activation=False))
    write('keyword-routes.json',dict(schema='romcom-keyword-routes/v1',terms=routes,scene_examples=[dict(id=f'EX{i:02d}',label=r[0],original_combination=r[1]) for i,r in enumerate(capture['content']['tables'][22][1:],1)]))
    old=json.loads((ASSETS/'photo_candidate_harem_20261023.json').read_text())
    by_sid={r['content'].get('research_semantics',{}).get('id'):(cid,r) for cid,r in old['candidates'].items()}
    binding_data=json.loads((ASSETS/'photo_candidate_harem_bindings_20261023.json').read_text())['slot_bindings']
    decisions=[]
    for card in cards:
        sid=HAREM_NEIGHBORS.get(card['id'])
        if sid:
            cid,record=by_sid[sid]
            decisions.append(dict(card_id=card['id'],decision='reuse_or_refine_after_whole_source_review',candidate_id=cid,source_module='photo_candidate_harem_20261023.json',source_card_id=sid,source_record=record,source_bindings=[b for b in binding_data.values() if b['candidate_id']==cid],reason='Full source is a concrete neighbor. Compare changed support, count, owner, garment layers and bilingual meaning before reuse. New wording is not automatically a new CID.',remaining_checks=['complete selected-branch en/ko meaning','intrinsic conditions and whole effects','exact slot spec and current native qualification','request-local owner prerequisites','all introduced details and omitted constraints']))
        else:
            decisions.append(dict(card_id=card['id'],decision='new_or_existing_neighbor_pending_full_corpus_review',candidate_id=None,reason='Lexical absence or a different label does not prove novelty. Search full meaning in all source modules before allocating an ID.'))
    # Existing umbrella fragments and temporal labels warrant precise refinement.
    for cid,reason in [
        ('cand_67d7910889fa5a1cb3fef1300f76eb71','Shared-umbrella close frame lacks an explicit common canopy and two head endpoints; review as a composition option, not full R07 evidence.'),
        ('cand_5e2823261de459b0abf2319b458db382','Hands sharing a handle does not itself establish one canopy covering both people; do not over-upgrade the fragment.'),
        ('cand_972acf2f94535c50a0d0b1767483530f','Double-take label needs temporal context; one frozen surprised expression cannot establish a second look.'),
        ('cand_773305f14cd45e549ad49bb4d17844c4','Existing slow-burn context should remain contextual, without an invented compulsory pose.')]:
        audit=read('corpus-snapshot.json')
        found=next(m for m in audit['matches'] if m['candidate_id']==cid)
        decisions.append(dict(card_id='R07' if 'umbrella' in reason.lower() or 'handle' in reason.lower() else 'X09' if 'Double-take' in reason else 'X04',decision='refine_or_retain_context',candidate_id=cid,source_record=found['record'],source_module=found['module'],source_bindings=found['bindings'],reason=reason))
    write('existing-source-decisions.json',decisions)
    drafts=[]
    for card in cards:
        decision=next(d for d in decisions if d['card_id']==card['id'])
        drafts.append(dict(draft_id='DRAFT-ROM-'+card['id'],semantic_card_id=card['id'],status='research_draft_not_native_source',record_kind_proposal='visual_option',proposed_content_en=card['positive_en'],proposed_content_ko=card['positive_ko'],slot_proposals=card['suggested_slots'],source_decision=decision['decision'],existing_candidate_id=decision.get('candidate_id'),required_review=['independently existing owners and needed objects','whole bilingual meaning and branch selection','count, garment, support, gaze, pose and medium effects','current field-local source evidence and role qualification'],native_approval=False,bindings_created=False,indexed=False))
    write('candidate-drafts.json',dict(schema='romcom-candidate-drafts/v1',drafts=drafts))
    boundary=[]
    for row in rows('boundary-cases.tsv'):
        boundary.append(dict(id=row['id'],positive_request_ko=row['positive_request'],confusable_request_ko=row['confusable_request'],expected_distinction=row['expected_distinction'],card_ids=row['cards'].split(','),status='DESIGNED_NOT_EXECUTED'))
    write('boundary-cases.json',boundary)
    development=[]
    for c in cards:
        for lang in ('en','ko'):
            development.append(dict(id=c['id']+'-'+lang,kind='author_exposed_development',query=c['positive_'+lang],language=lang,expected_card_id=c['id'],expected_relation=c['observable_gate'],evaluation_status='NOT_RUN',independence='Not holdout; wording overlaps authored data.'))
    for b in boundary:
        for side in ('positive','confusable'):
            development.append(dict(id=b['id']+'-'+side,kind='boundary_development',query=b[side+'_request_ko'],language='ko',expected_distinction=b['expected_distinction'],evaluation_status='NOT_RUN'))
    write('development-cases.json',development)
    atlas=['# 원 대화 용어 317개와 반영 경로','', '317개 항목 보존은 전 항목의 독립 사전 검증·형태 확장 완료를 뜻하지 않는다. 구체 실현은 선택적 또는 인접 대안이며 원뜻의 단일 정의가 아니다. 미확인 세부 정의는 명시적으로 pending이다.','']
    for t,group in __import__('itertools').groupby(routes,key=lambda x:x['table']):
        atlas += [f'## 표 {t}','', '|ID|원 표제|원 설명|문맥|시각 카드|독립 용어 근거|','|---|---|---|---|---|---|']
        for k in group:
            atlas.append('|'+ '|'.join(md(str(v)) for v in [k['id'],k['original_label'],k['original_definition'],k['context_card_id'],','.join(k['visual_card_ids']) or '추가 형태 검토/문맥',','.join(k['lexical_source_ids'][1:]) or 'pending'])+'|')
        atlas.append('')
    (HERE/'KEYWORD-ATLAS.md').write_text('\n'.join(atlas)+'\n')
    visual=['# 관찰 가능한 관계 카드와 문맥 경계','', '아래 영어·한국어는 독립적으로 작성한 연구 대안이다. 출처는 지정한 어휘·문맥만 지원하며 모든 기하를 보증하지 않는다. 각 카드의 전체 접점과 소유자를 함께 확인한다.','']
    for c in cards:
        visual += [f"## {c['id']} {c['label_ko']}",'',c['positive_en'],'',c['positive_ko'],'',f"- 원 용어: {', '.join(c['term_refs'])}",f"- 판정: {c['observable_gate']}",f"- 혼동/주장 한계: {c['confusion_boundary']}",f"- 제안 slot: {', '.join(c['suggested_slots'])}",f"- 근거 범위 참조: {', '.join(c['source_ids'])}",'- 상태: 연구 초안, 자동 hard 활성화 없음, native 미검증, 픽셀 미실행','']
    for c in contexts:
        visual += [f"## {c['id']} {c['label_ko']}",'',c['distinction_ko'],'',f"필요한 별도 근거: {c['required_evidence']}",'']
    (HERE/'VISUAL-CARDS.md').write_text('\n'.join(visual)+'\n')
    summary=dict(original_terms=len(routes),scene_examples=7,visual_cards=len(cards),context_cards=len(contexts),candidate_drafts=len(drafts),boundary_pairs=len(boundary),development_queries=len(development),terms_with_specific_visual_neighbor=sum(bool(k['visual_card_ids']) for k in routes),terms_with_specific_independent_lexical_corroboration=sum(len(k['lexical_source_ids'])>1 for k in routes),external_sources=len(source_rows)-1,concrete_source_comparisons=sum('source_record' in d for d in decisions),runtime_integration='NOT_APPLIED',retrieval='NOT_RUN',pixels='NOT_RUN',holdout='NOT_CREATED')
    write('BUILD-SUMMARY.json',summary)
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':
    main()
