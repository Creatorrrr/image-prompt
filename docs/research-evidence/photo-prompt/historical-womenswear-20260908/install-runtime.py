import copy, hashlib, json
from pathlib import Path
R=Path.cwd(); A=R/'skills/photo-prompt-image-generator/assets'
P=R/'docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned'
def digest(d):return hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
candidates={c['id']:c for c in json.loads((P/'candidate-drafts.v2.json').read_text())['candidate_drafts']}
ext=json.loads((P/'optional-extension.proposed.json').read_text())
ext.pop('maintenance_ref');ext['schema_version']='photo-prompt-research-extension/v1'
korean=[
'가운 등목선에서 시작한 깊은 상자주름이 허리를 지나 치마까지 자유롭게 내려온다',
'가운 등판이 허리에 맞춰지고 그 아래에서 치마가 펼쳐진다',
'겉치마가 세 구획으로 걷어 올려지고 그 아래 별도 페티코트가 보인다',
'가운 치마가 허리 좌우로 넓게 퍼지고 앞뒤 깊이는 좌우 폭보다 작다',
'가운 몸판 앞 열림의 양 가장자리가 아래로 좁아지는 별도 스토머커 앞판을 둘러싼다',
'가벼운 슈미즈 가운의 몸판과 치마에 부드러운 주름이 생기고 새시가 자연 허리에서 천을 모은다',
'가운 몸판이 가슴 바로 아래에서 끝나고 긴 치마가 그 높은 이음선에서 내려온다',
'가운 치마가 허리 바로 아래에서 뒤로 돌출하고 뒤 치마가 그 높은 돌출부에서 떨어진다',
'긴 티펫 천이 가운 위팔 소매 뒤에 부착되어 팔을 들어도 소매와 연결되어 늘어진다',
'넓은 윔플 천이 턱 아래를 받치고 같은 천이 얼굴 아래 목까지 감싼다',
'좁은 바베트 띠가 양 관자놀이 사이에서 턱 아래를 지나고 목 앞면은 드러난다',
'긴 흰 면 외출 드레스의 몸판과 소매를 레이스 인서션이 연결하고 맞춘 허리 아래로 모인 긴 치마가 이어진다',
'넉넉한 드레스 몸판 아래 허리 솔기가 자연 허리보다 낮은 골반 부근에 놓인다',
'머리에 밀착한 종 모양 클로슈의 짧은 챙이 이마와 관자놀이 가까이 내려온다',
'소매가 달린 포 형태의 장옷을 머리에 걸쳐 앞자락이 얼굴을 감싸고 양옆에 소매와 앞 고름이 구별된다',
'치마형 쓰개치마가 머리 위 모인 띠에서 양옆으로 내려오고 띠의 두 끈이 턱 아래에서 만난다',
'긴 둥근 당의 앞뒤 자락이 치마 위에서 옆트임으로 나뉘고 좁은 소매 끝에 밝은 거들지가 이어진다',
'고소데의 큰 늘어진 소매 패널 안에 작은 손목 입구가 있고 그 패널이 곧은 몸판과 구별된다',
'긴 장포에 넓고 곧은 소매가 이어지고 목선 소매끝 밑단 테두리와 천 위 반복 나비 자수가 보인다',
'넉넉한 발목 길이 치파오의 몸판 아래가 완만히 넓어지고 넓은 긴 소매와 대각선 앞 여밈이 있다',
'좁은 레이스 띠가 가운 몸판 내부의 두 천 패널을 연결한다',
'옷의 바탕 천 위에 꽃 문양 브로케이딩이 직조되어 도톰한 문양을 이룬다',
'같은 색 천의 다마스크 문양 안에서 무광 부분과 광택 부분이 교대로 나타난다',
'가운 허리에 고정한 샤틀렌 고리에서 짧은 체인으로 작은 도구통이 매달린다'
]
profiles=[]
for b,ko in zip(ext['visual_semantics'],korean):
    c=candidates[b['id']];phrases=[x['visible_evidence'][0] for x in b['component_groups']]
    b['hard_profile_ids']=[b['id']];b['activation_mode']='component_complete_exact_only'
    b['source_keywords']=c['search_terms']
    components=[]
    for i,g in enumerate(b['component_groups'],1):
        phrase=g['visible_evidence'][0]
        components.append({'id':g['id'],'match_terms':[phrase],'evidence_field':g['id']+'_phrase','evidence_terms':[phrase],'min_content_words':3,'instruction':'Keep the selected garment relation visible: '+phrase,'render_gate':{'id':f"vo_{b['id']}_{i}",'review_scale':'native','description':'The saved image visibly shows '+phrase+'. Occlusion or a substituted garment relation does not pass.'}})
    profiles.append({'id':b['id'],'category':'historical_womenswear_visible_relation','activation':{'exact_terms':['; '.join(phrases),ko],'requires_adult_character':False,'semantic_discovery_requires_component_evidence':True},'semantics':{'definition':c['label_en']+' as a selected visible variant: '+'; '.join(phrases)+'.','paraphrase_examples':[c['label_en']+' with '+' and '.join(phrases),*c['search_terms']],'contrast_examples':c['confusion_boundaries_ko'],'claim_limits':c['claim_limits_ko']+['This selected garment form does not establish the wearer identity, ethnicity, social status or the photograph capture date.']},'concept_candidate':{'concept_terms':[c['label_en'],c['label_ko'],*phrases]},'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},'reject_substitutes':c['confusion_boundaries_ko'],'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':components}})
for profile in profiles:
    if profile['id']=='hw_qipao_1920_loose':
        # A family name remains searchable without establishing a particular variant.
        family_labels=['qipao','cheongsam','치파오','창파오']
        profile['semantics']['paraphrase_examples']=[
            phrase for phrase in profile['semantics']['paraphrase_examples']
            if phrase not in family_labels
        ]+['loose cheongsam','loose qipao','roomy cheongsam','넉넉한 치파오','1920년대 치파오']
        profile['concept_candidate']['concept_terms']=list(dict.fromkeys(
            profile['concept_candidate']['concept_terms']+family_labels))
for slot,rows in ext['slots'].items():
    for e in rows:
        cid=e['id'].rsplit('_',1)[0];c=candidates[cid]
        e['weight']=0.55;e['tags']=['historical_womenswear_visual_semantics',slot]
        e['keywords']=list(dict.fromkeys([c['label_ko'],c['label_en'],*c['search_terms'],e['en']]))
        e['embedding_text']=c['label_en']+': '+e['en']
record={'contract_version':'photo-extension-maintenance/v1','record_id':'photo_prompt_historical_womenswear_extension','source_filename':'photo_prompt_historical_womenswear_extension.json','authored_source_sha256':digest(ext),'runtime_keys':['slots','visual_semantics'],'maintenance_only':{'research_path':str(P.relative_to(R)),'candidate_drafts_sha256':hashlib.sha256((P/'candidate-drafts.v2.json').read_bytes()).hexdigest(),'source_ledger_sha256':hashlib.sha256((P/'source-ledger.json').read_bytes()).hexdigest(),'profile_scope':{b['id']:{'evidence_ids':candidates[b['id']]['source_ids'],'limits':candidates[b['id']]['claim_limits_ko'],'source_row_ids':candidates[b['id']]['source_row_ids']} for b in ext['visual_semantics']},'adoption_scope':'24 evidence-scoped optional variants; other research drafts remain unregistered; no claim of complete era classification'}}
write(R/'docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_historical_womenswear_extension.json',record)
ext['maintenance_ref']={'contract_version':'photo-extension-maintenance-ref/v1','record_id':record['record_id'],'sha256':digest(record)}
write(A/'photo_prompt_historical_womenswear_extension.json',ext)
write(A/'photo_prompt_visual_obligations_historical_womenswear.json',{'schema_version':'photo-visual-obligation-registry-extension/v1','relation_contract_version':'photo-visual-relation/v1','description':'Selected visible garment topology, layered clothing and textile surface relations.','profiles':profiles})
tags_path=A/'photo_prompt_tags.json'
tags_text=tags_path.read_text()
if 'photo_prompt_historical_womenswear_extension.json' not in tags_text:
    marker='      "photo_prompt_opening_era_extension.json"'+chr(10)
    assert tags_text.count(marker)==1
    tags_text=tags_text.replace(marker,'      "photo_prompt_opening_era_extension.json",'+chr(10)+'      "photo_prompt_historical_womenswear_extension.json"'+chr(10),1)
    tags_path.write_text(tags_text)
print('Authored',len(profiles),'profiles,',sum(len(p['authored_components']['components']) for p in profiles),'gates and 24 optional bundles')
