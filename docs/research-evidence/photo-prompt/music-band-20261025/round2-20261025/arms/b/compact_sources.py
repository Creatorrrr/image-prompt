import json,pathlib,sys
p=pathlib.Path('docs/research-evidence/photo-prompt/music-band-20261025/round2-20261025/arms/b');w=json.loads(pathlib.Path('generated/photo-runs/music-band-20261025-r2-b/workflow.json').read_text());m=json.loads(pathlib.Path(w['artifacts']['h_f2_material']['path']).read_text())
def resolve(v,lit):
 if isinstance(v,dict):
  if set(v)=={'$literal'}:return lit[v['$literal']]
  return {k:resolve(x,lit) for k,x in v.items()}
 if isinstance(v,list):return [resolve(x,lit) for x in v]
 return v
sources=[]
for cid,s in m['sources'].items():
 t=resolve(s['native']['tree'],s['meaning']['literals']); r=t.get('research_semantics');
 if isinstance(r,dict): t['research_semantics']={k:v for k,v in r.items() if k in ('observable_components','owner_contract','pixel_gate','confusion_boundary_ko','source_support','source_conditions_and_effects_are_separate_from_research_metadata')}
 sources.append({'id':cid,'conditions':s['conditions'],'effects':s['effects'],'native':t})
(p/'source-review-readable.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
a=int(sys.argv[1]) if len(sys.argv)>1 else 0;b=int(sys.argv[2]) if len(sys.argv)>2 else len(sources)
for i,s in enumerate(sources[a:b],a):print(i,json.dumps(s,ensure_ascii=False,separators=(',',':')))
