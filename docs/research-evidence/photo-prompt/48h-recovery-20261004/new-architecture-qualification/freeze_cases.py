"""Author/freeze new source-exposed synthetic cases; no runtime imports/calls."""
import hashlib,json
from pathlib import Path
O=Path(__file__).resolve().parent
P=json.loads((O/'proposal.json').read_text())
E={e['profile_id']:e for e in P['edits']}
CP='pf_rib_vault_chapel'; VP='pf_venetian_arcade'
components={p:E[p]['unchanged_english_exact'].split('; ') for p in E}
# Each extra phrase is source-owned only where the Korean request states it.
wall='those supports stand along the chapel walls'
rhythm='the upper openings have a rhythm distinct from those of the lower arcade'
rows=[]
def add(pid,role,language,request,facts,contradicts=None):
    baseline=('An architectural photograph studies this arrangement: '+'; '.join(facts)+'. '
              'A measured oblique view keeps the connected spaces legible within a single frame. '
              'Soft daylight describes the edges and surfaces, and restrained tonal separation gives the principal architectural relationships visual priority. '
              'The surrounding details remain subordinate to the structure.')
    rows.append({'id':pid+'_'+role,'profile_id':pid,'cohort':'source_guided','role':role,'language':language,
                 'source_exposed':True,'blind_data':False,'request':request,'baseline_prompt_en':baseline,
                 'request_facts':facts,'target_components':components[pid],'contradicts_target_component':contradicts,
                 'ownership_note':'Only request_facts plus the request for an architectural photograph are requester-owned; all view/light/tonal staging remains agent-owned.',
                 'expected':{'before_hard':None if role=='canonical_ko' else role in ('exact_en','old_complete_ko') or role.endswith('_ko'),
                             'after_hard':role in ('canonical_ko','exact_en'),
                             'before_audit':'fail' if role.startswith('incompatible_') and language=='ko' else 'pass','after_audit':'pass'}})
for pid in E:
    facts=components[pid]+([wall] if pid==CP else [rhythm])
    add(pid,'canonical_ko','ko','건축 사진을 만들어 주세요: '+E[pid]['new_value']+'.',facts)
    add(pid,'exact_en','en','Make an architectural photograph: '+E[pid]['unchanged_english_exact']+'.',components[pid])
old_extra={CP:'이곳은 예배당이고 교차하는 리브 전체가 돌로 되어 있다. 리브와 이어지는 벽측 지지부 옆 개구부들의 상단은 뾰족하며, 예배 영역은 이 예배당의 끝에 있다.',
           VP:'아래 아케이드는 물가를 향한다. 바로 그 위층 갤러리는 아래 아케이드보다 섬세한 투각형이며, 그 위에 지지되는 상부 벽체는 넓은 벽 덩어리를 이룬다.'}
for pid in E:
    add(pid,'old_complete_ko','ko','건축 사진을 만들어 주세요: '+E[pid]['old_value']+'. '+old_extra[pid],components[pid]+([wall] if pid==CP else [rhythm]))
negatives=[
(CP,'timber',0,'timber ribs intersect across the chapel ceiling','이곳은 예배당이며 교차하는 천장 리브 전체가 나무로 되어 있다. 리브는 상단이 뾰족한 개구부 옆 벽측 지지부와 연결되고 예배 영역은 예배당 끝에 있다.'),
(CP,'round_openings',1,'the ribs continue toward supports beside round-headed openings','이곳은 예배당이고 천장 리브는 돌로 되어 있다. 리브와 이어지는 벽측 지지부 옆 개구부의 상단은 모두 둥근 반원형이다. 예배 영역은 예배당 끝에 있다.'),
(VP,'inland',0,'an open lower arcade faces a dry inland plaza','아래 아케이드는 건조한 내륙 광장을 향한다. 바로 위에는 아래 아케이드보다 섬세한 투각형 갤러리가 있고, 넓은 상부 벽체가 그 갤러리 위에 지지된다.'),
(VP,'solid_gallery',1,'a solid-walled enclosed gallery occupies the level above the lower arcade','아래 아케이드는 물가를 향한다. 바로 위층 갤러리는 불투명한 연속 벽으로 둘러싸인 폐쇄형이고, 넓은 상부 벽체가 그 갤러리 위에 지지된다.'),
(VP,'narrow_parapet',2,'a narrow low parapet rests above the gallery','아래 아케이드는 물가를 향한다. 바로 위층에는 아래 아케이드보다 섬세한 투각형 갤러리가 있다. 갤러리 위에 지지되는 상부 벽체는 폭이 좁고 높이가 낮은 난간벽이다.')]
for pid,name,ix,replacement,ko in negatives:
    facts=list(components[pid]);facts[ix]=replacement;facts.append(wall if pid==CP else rhythm)
    add(pid,'incompatible_'+name+'_ko','ko','건축 사진을 만들어 주세요: '+E[pid]['old_value']+'. '+ko,facts,ix+1)
    add(pid,'incompatible_'+name+'_en','en','Make an architectural photograph: '+'; '.join(facts)+'.',facts,ix+1)
assert len(rows)==16 and len({c['id'] for c in rows})==16
for c in rows:
    c['request_sha256']=hashlib.sha256(c['request'].encode()).hexdigest()
    c['baseline_sha256']=hashlib.sha256(c['baseline_prompt_en'].encode()).hexdigest()
    c['contains_old_exact']=E[c['profile_id']]['old_value'] in c['request']
    c['contains_new_exact']=E[c['profile_id']]['new_value'] in c['request']
    assert len(c['baseline_prompt_en'].split())>=48
    assert all(f in c['baseline_prompt_en'] for f in c['request_facts'])
    if c['role']=='old_complete_ko':assert c['contains_old_exact'] and not c['contains_new_exact']
    if c['role']=='canonical_ko':assert c['contains_new_exact'] and not c['contains_old_exact']
    if c['role'].startswith('incompatible_'):assert E[c['profile_id']]['unchanged_english_exact'] not in c['request']
mutations=[]
def mutation(pid,name,index,new,kind='replace_content'):
    mutations.append({'id':pid+'_'+name,'source_case_id':pid+'_old_complete_ko','profile_id':pid,'kind':kind,
                      'old':components[pid][index],'new':new,'affected_anchor_ids':['relation_'+str(index+1)],
                      'expected_content_failure':kind=='replace_content','purpose':'Alter the actual prompt while preserving immutable request/core/pack bindings and truthfully updating mutable evidence.'})
mutation(CP,'stone_to_timber',0,'timber ribs intersect across the chapel ceiling')
mutation(CP,'pointed_to_round',1,'the ribs continue toward supports beside round-headed openings')
mutation(CP,'end_to_middle',2,'a distinct worship area occupies the middle of the chapel')
mutation(VP,'water_to_inland',0,'an open lower arcade faces a dry inland plaza')
mutation(VP,'openwork_to_solid',1,'a solid-walled enclosed gallery occupies the level above the lower arcade')
mutation(VP,'broad_to_narrow',2,'a narrow low parapet rests above the gallery')
mutation(CP,'support_owner_transfer',1,'the ribs stop above a detached screen, while supports beside pointed openings belong to a separate neighboring bay')
mutation(VP,'gallery_owner_transfer',1,'a finer openwork gallery occupies the level above an adjacent building')
for pid,sentence in [(CP,'The very same ceiling ribs are made entirely of timber.'),(VP,'The very same lower arcade faces a dry inland plaza far from any water.')]:
    mutations.append({'id':pid+'_append_contradiction','source_case_id':pid+'_old_complete_ko','profile_id':pid,
                      'kind':'append_contradiction','append':sentence,'affected_anchor_ids':[],
                      'expected_content_failure':None,'purpose':'Diagnostic only: original literal anchors remain; a pass demonstrates a semantic limitation, not successful semantic protection.'})
case_payload={'schema_version':'architecture-frozen-cases/v1','source_commit':P['source_commit'],'seed':20261004,'source_guided_case_count':16,'new_unique_profile_coverage':0,'cases':rows}
for name,data in [('cases.json',case_payload),('mutations.json',{'schema_version':'architecture-content-mutations/v1','mutation_count':10,'cases':mutations})]:
    path=O/name
    if path.exists():raise SystemExit('Refuse to overwrite frozen '+str(path))
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('New cases frozen: 16 source-guided requests and 10 separate mutation controls; no runtime execution')
