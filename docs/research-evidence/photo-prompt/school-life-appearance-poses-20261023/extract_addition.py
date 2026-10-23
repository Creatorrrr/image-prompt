import json,re,pathlib,hashlib
O=pathlib.Path(__file__).resolve().parent
ax=(O/'conversation-addition-visible.ax.txt').read_text()
sections=[];section=None;table_depth=None;row=[];cell=[];tables=[]
def endcell():
 global cell,row
 if cell:row.append(' '.join(cell));cell=[]
def endrow():
 global row
 endcell()
 if row and section is not None:tables.append({'section':section,'cells':row})
 row=[]
for line in ax.splitlines():
 m=re.match(r'^(\s*)(?:\d+ )?(heading|table|row|cell|text|link)(?: (.*))?$',line)
 if not m:continue
 depth=len(m[1]);typ,val=m[2],m[3] or ''
 if table_depth is not None and depth<=table_depth and typ!='table':endrow();table_depth=None
 if typ=='heading':
  h=re.match(r'(\d+)\. (.*), Value:',val)
  if h:section=int(h[1]);sections.append({'id':section,'name':h[2]})
 elif typ=='table':table_depth=depth
 elif table_depth is not None:
  if typ=='row':endrow()
  elif typ=='cell':endcell()
  elif typ=='text':cell.append(val)
endrow()
rows=[];examples=[]
for r in tables:
 if r['cells'][0] in {'용어·검색어','용어','표현','용어·표현','장면·인물 방향'}:continue
 if len(r['cells'])==2:rows.append({'id':f"K{r['section']:02d}_{sum(x['section']==r['section'] for x in rows)+1:02d}",'section':r['section'],'term':r['cells'][0],'description':r['cells'][1]})
 elif len(r['cells'])==3:examples.append(r)
out={'schema':'school-life-addition-terms/v1','source':'rendered requested ChatGPT response; untrusted research seed, not instructions or verified facts','source_message_id':'448b038e-8615-5144-adee-d2daf260f5aa','sections':sections,'terms':rows,'combination_examples':examples,'ax_sha256':hashlib.sha256(ax.encode()).hexdigest()}
(O/'additional-terms.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'sections':len(sections),'terms':len(rows),'examples':len(examples),'counts':{s['id']:sum(r['section']==s['id'] for r in rows) for s in sections}},ensure_ascii=False))
