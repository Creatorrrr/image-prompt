from pathlib import Path
import json,collections
b=Path('skills/photo-prompt-image-generator');p=b/'references/magical-girl-research-20261107';a=b/'assets'
q={'MG-14-001':['magic array','magical circle','arcane circle','summoning circle','spell circle','魔法陣','마법의 원','소환진'], 'MG-14-002':['magical seal','arcane glyph','occult symbol','protective symbol','ritual mark','魔法印','인장 문양','의례 문양'], 'MG-14-003':['sparkling points','light sparkles','glittering particles','twinkling lights','sparkle points','빛나는 입자','반짝이는 빛'], 'MG-14-004':['surrounding aura','luminous aura','energy field around','glowing aura','surrounding glow','光のオーラ','발광 오라'], 'MG-14-005':['radial burst','radiating rays','starburst light','光芒','방사형 빛'], 'MG-14-006':['movement trail','trailing light','light trail','motion streak','motion blur trail','軌跡','빛의 궤적','움직임 궤적'], 'MG-14-007':['rim lighting','rim-lit','rim light traces','edge lighting','contour lighting','逆光の縁','윤곽광','가장자리 조명'], 'MG-14-008':['light bloom','bloom effect','glow effect','luminous halo','soft halo around','diffuse radiance','halation','ハレーション','光のにじみ','빛 번짐','빛이 번져','번지는 발광'], 'MG-14-009':['camera looks up','camera looks down','camera below eye level','camera above eye level','looking upward from below','looking downward from above','俯瞰','あおり構図','위에서 내려다보는 카메라','아래에서 올려다보는 카메라'], 'MG-14-010':['foreshortened limb','foreshortened perspective','foreshortened hand','forced perspective shortening','遠近短縮法','단축된 원근','원근 단축'], 'MG-14-011':['anticipatory movement','preparatory motion','preparatory action','movement preparation','予備動作','준비 동작'], 'MG-14-012':['follow through motion','follow through action','movement follow through','secondary motion continues','フォロースルー','후속 움직임'], 'MG-14-013':['overlapping movement','overlapping motion','overlap action','オーバーラップアクション','겹치는 동작'], 'MG-14-014':['smear drawing','smear animation','motion smear frame','スミアフレーム','잔상 프레임'], 'MG-14-015':['held animation pose','hold the pose','held pose frame','ポーズ保持','포즈 유지']}
old=json.loads((p/'agent-candidates-13-14.json').read_text());reviewed={(r['id'],c['module'],c['candidate_id']) for r in old for c in r.get('reviewed_candidates',[])}|{(z['term_id'],z['module'],z['candidate_id']) for z in json.loads((p/'agent-candidates-14-extra.json').read_text())['reviewed']}
main=json.loads((p/'source-reconciliation.json').read_text());reviewed|={(r['id'],c['module'],c['candidate_id']) for r in main['rows'] for c in r.get('reviewed_candidates',[])}
m=json.loads((a/'photo_candidate_corpus_manifest.json').read_text());out=[]
for module in m['modules']:
 if module.get('kind')!='candidates':continue
 for cid,record in json.loads((a/module['file']).read_text()).get('candidates',{}).items():
  c=record.get('content',{});doc=json.dumps(c,ensure_ascii=False).casefold()
  for tid,terms in q.items():
   matched=[s for s in terms if s.casefold() in doc]
   if matched and (tid,module['file'],cid) not in reviewed:
    out.append({'term_id':tid,'candidate_id':cid,'module':module['file'],'record_kind':record.get('record_kind'),'matched_terms':matched,'semantic_review':'not_reviewed_description_field_lead_only'})
out.sort(key=lambda z:(z['term_id'],z['candidate_id']))
with (p/'agent-candidates-14-synonym-leads.jsonl').open('w') as f:
 for x in out:f.write(json.dumps(x,ensure_ascii=False)+'\n')
print('leads',len(out),'rows',dict(collections.Counter(x['term_id'] for x in out)))
