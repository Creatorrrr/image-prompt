"""Named-free maintenance probes; these are not blind human holdouts."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as g
from build_visual_profile_index import load_project_env
load_project_env();assets=ROOT/'skills/photo-prompt-image-generator/assets'
registry=g.load_visual_obligation_registry(assets/'photo_prompt_visual_obligations.json')
index=g.load_visual_profile_index(assets/'photo_prompt_visual_profile_index.json',registry)
cases=[
('thumb_index_cross','sf_profile_051_base','한 손의 엄지와 검지 끝이 서로 엇갈려 작은 교차를 만들고 나머지 세 손가락은 손바닥으로 접힌다. 손목부터 그 교차 끝까지 같은 인물의 손으로 이어지는 초상 사진.'),
('shaka_digits','sf_profile_050_base','한 인물이 엄지와 새끼손가락만 양옆으로 펴고 가운데 세 손가락을 손바닥에 굽힌다. 두 펴진 손가락과 손목이 같은 손의 양끝으로 이어지는 셀프포트레이트.'),
('mirror_chin_clear','sf_profile_094_base','물리 거울 반사 안에서 인물이 촬영 폰을 가슴 윗부분에 쥔다. 폰 윗변이 턱보다 아래라 눈과 코와 입이 모두 그 위에 드러나며 손목과 쥔 폰이 같은 반사된 방 안에 연결된다.'),
('surface_shadow_bands','sf_profile_177_base','창의 블라인드를 통과한 빛이 얼굴과 어깨에 평행한 어두운 띠를 만든다. 띠는 코와 볼의 굴곡을 따라 휘어지며 광원을 가리는 블라인드 간격과 같은 방향으로 이어지는 인물 사진.'),
]
results=[]
for name,expected,text in cases:
    vector=g.embed_texts_with_gemini([text],model=index['embedding_model'],dimensions=index['embedding_dimensions'])[0]
    resolution=g.resolve_visual_profile_hits(registry,[{'source':'authorial_core_baseline','text':text,'polarity':'advisory'}],visual_profile_index=index,query_text=text,query_vector=vector,adult_context=True)
    hits=[{'profile_id':h['profile_id'],'match_basis':h.get('match_basis'),'hard_eligible':h.get('hard_eligible')}for h in resolution['hits']]
    observed=next((h for h in hits if h['profile_id']==expected),None)
    results.append({'id':name,'query':text,'expected_profile':expected,'expected_profile_exposed':bool(observed),'expected_optional_only':bool(observed and not observed['hard_eligible']),'hits':hits})
negative=['a V-shaped radio antenna on an empty roof','a glass rectangle beside a phone screen photograph','a political Gen Z stare discussed in a newspaper','a portrait of one person without any physical mirror']
negative_results=[]
for text in negative:
    r=g.resolve_visual_profile_hits(registry,[{'source':'user_requirement','text':text,'polarity':'required'}],visual_profile_index=index,adult_context=False)
    hard=[h['profile_id']for h in r['hits']if h.get('hard_eligible')and h['profile_id'].startswith('sf_profile_')]
    negative_results.append({'query':text,'new_hard_profiles':hard,'pass':not hard})
report={'proof_scope':'Real Gemini query vectors and current full visual index; diagnostic optional exposure and exact negatives. Research-author maintenance probes, not independent holdout, final adoption or pixel evidence.','positive_probes':results,'hard_negative_probes':negative_results,'positive_expected_exposed':sum(x['expected_profile_exposed']for x in results),'negative_passes':sum(x['pass']for x in negative_results)}
(OUT/'semantic-probes.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'positive_expected_exposed':report['positive_expected_exposed'],'positive_total':len(results),'negative_passes':report['negative_passes'],'negative_total':len(negative_results)},ensure_ascii=False))
