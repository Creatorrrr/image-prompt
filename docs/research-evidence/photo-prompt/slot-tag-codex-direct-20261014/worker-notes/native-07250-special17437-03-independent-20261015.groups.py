"""Exact JSON payload equality projection only. No inferred modes, values or approvals."""
import pathlib,json,hashlib,collections,sys
R=pathlib.Path(__file__).resolve().parents[1];P=R/'native_batches/review08250-17437-03/BATCH.json';B=json.loads(P.read_text())['records'][0];F=B['proof']['facts'];ID={f['id']:f for f in F}
C=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def payload(f):return {k:v for k,v in f.items() if k not in ['id','realization_id','pointer','quote','requires']}
groups=collections.defaultdict(list)
for i,f in enumerate(F):groups[C(payload(f))].append((i,f))
G=[]
for ix,(key,occ) in enumerate(groups.items()):
 qr=collections.defaultdict(list);rq=collections.defaultdict(list)
 for i,f in occ:
  p=f['pointer'];rid=f['realization_id'];rel=p.replace('/realization_content/'+rid+'/','/realization_content/{RID}/')
  qr[C({'relative_pointer':rel,'quote':f['quote']})].append(i)
  rq[C([payload(ID[k]) for k in f['requires']])].append(i)
 G.append({'group':ix,'payload':json.loads(key),'count':len(occ),'rids':dict(collections.Counter(f['realization_id'] for _,f in occ)),'actual_fact_indices':[i for i,_ in occ],'quote_and_relative_field_groups':[dict(json.loads(k),indices=v) for k,v in qr.items()],'requires_exact_payload_variants':[{'required_payloads':json.loads(k),'indices':v} for k,v in rq.items()]})
if len(sys.argv)>1:
 for g in G[int(sys.argv[1]):int(sys.argv[2])]:
  # Full occurrence indices stay in immutable machine file; output counts plus exact payload/quotes/req variants.
  out={k:v for k,v in g.items() if k!='actual_fact_indices'}
  for q in out['quote_and_relative_field_groups']:q['occurrence_count']=len(q.pop('indices'))
  for q in out['requires_exact_payload_variants']:
   q['occurrence_count']=len(q.pop('indices'));q['required_payload_group_ids']=[next(g2['group'] for g2 in G if g2['payload']==v) for v in q.pop('required_payloads')]
  print(json.dumps(out,ensure_ascii=False))
else:
 out=R/'worker-notes/native-07250-special17437-03-independent-20261015.exact-payload-groups.json';assert not out.exists();out.write_text(json.dumps({'batch_raw_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'raw_occurrences':len(F),'groups':G,'preparation_is_not_direct_read_attestation':True},ensure_ascii=False,indent=2)+'\n');print({'groups':len(G),'occurrences':len(F),'unique_unit_quotes':len({u['quote'] for u in B['proof']['source_units']}),'unit_dispositions':dict(collections.Counter(u['disposition'] for u in B['proof']['source_units']))})
