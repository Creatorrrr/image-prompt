import json,pathlib
r=pathlib.Path('generated/photo-runs/mecha-20261024-arm-a');w=json.loads((r/'workflow.json').read_text());m=json.loads(pathlib.Path(w['artifacts']['h_f2_material']['path']).read_text())
def decode(v,l):
 if isinstance(v,dict):
  if set(v)=={'$literal'}:return l[v['$literal']]
  return {k:decode(x,l) for k,x in v.items()}
 if isinstance(v,list):return [decode(x,l) for x in v]
 return v
out=[]
for cid,s in m['sources'].items():
 out.append({'cid':cid,'conditions':s['conditions'],'effects':s['effects'],'native_contract':s['meaning'].get('native_contract'),'meaning_graphs':s['meaning'].get('graphs'),'native':decode(s['native'],s['meaning']['literals']),'all_source_literals':s['meaning']['literals'],'provenance':s['provenance'],'record_kind':s['record_kind']})
(r/'material-full-source-decoded.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
for i,s in enumerate(out):
 print(i,s['cid'],str(s['provenance']),json.dumps(s['native'].get('tree',{}).get('semantics',s['native'].get('tree',{}).get('label','')),ensure_ascii=False)[:260])
