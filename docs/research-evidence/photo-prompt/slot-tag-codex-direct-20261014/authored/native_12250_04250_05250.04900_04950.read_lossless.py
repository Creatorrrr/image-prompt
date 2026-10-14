import sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=json.loads((R/'authored/native_12250_04250_05250.04900_04950.input.json').read_text());seen={}
def enc(v,path):
 s=json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
 if s in seen:
  ref={'EXACT_AS':seen[s]}
  if len(json.dumps(ref,separators=(',',':')))<len(s):return ref
 seen[s]=path
 if isinstance(v,dict):return {k:enc(x,path+'/'+k) for k,x in v.items()}
 if isinstance(v,list):return [enc(x,path+'/'+str(i)) for i,x in enumerate(v)]
 return v
prior=json.loads((R/'authored/native_12250_04250_05250.04250_04300.input.json').read_text())
for old in prior['records']:enc(old,'R'+str(old['ordinal']))
prior2=json.loads((R/'authored/native_12250_04250_05250.04300_04350.input.json').read_text())
for old in prior2['records']:enc(old,'R'+str(old['ordinal']))
prior3=json.loads((R/'authored/native_12250_04250_05250.04350_04400.input.json').read_text())
for old in prior3['records']:enc(old,'R'+str(old['ordinal']))
prior4=json.loads((R/'authored/native_12250_04250_05250.04400_04450.input.json').read_text())
for old in prior4['records']:enc(old,'R'+str(old['ordinal']))
prior5=json.loads((R/'authored/native_12250_04250_05250.04450_04500.input.json').read_text())
for old in prior5['records']:enc(old,'R'+str(old['ordinal']))
prior6=json.loads((R/'authored/native_12250_04250_05250.04500_04550.input.json').read_text())
for old in prior6['records']:enc(old,'R'+str(old['ordinal']))
prior7=json.loads((R/'authored/native_12250_04250_05250.04550_04600.input.json').read_text())
for old in prior7['records']:enc(old,'R'+str(old['ordinal']))
prior8=json.loads((R/'authored/native_12250_04250_05250.04600_04650.input.json').read_text())
for old in prior8['records']:enc(old,'R'+str(old['ordinal']))
prior9=json.loads((R/'authored/native_12250_04250_05250.04650_04700.input.json').read_text())
for old in prior9['records']:enc(old,'R'+str(old['ordinal']))
prior10=json.loads((R/'authored/native_12250_04250_05250.04700_04750.input.json').read_text())
for old in prior10['records']:enc(old,'R'+str(old['ordinal']))
prior11=json.loads((R/'authored/native_12250_04250_05250.04750_04800.input.json').read_text())
for old in prior11['records']:enc(old,'R'+str(old['ordinal']))
prior12=json.loads((R/'authored/native_12250_04250_05250.04800_04850.input.json').read_text())
for old in prior12['records']:enc(old,'R'+str(old['ordinal']))
prior13=json.loads((R/'authored/native_12250_04250_05250.04850_04900.input.json').read_text())
for old in prior13['records']:enc(old,'R'+str(old['ordinal']))
start,stop=map(int,sys.argv[1:]);assert 4900<=start<stop<=4950
# Earlier rows here must actually have been completely read. The caller controls start/stop.
for row in p['records']:
 n=row['ordinal']
 if n>=stop:break
 v=enc(row,'R'+str(n))
 if n>=start:print(n,json.dumps(v,ensure_ascii=False,separators=(',',':')))
