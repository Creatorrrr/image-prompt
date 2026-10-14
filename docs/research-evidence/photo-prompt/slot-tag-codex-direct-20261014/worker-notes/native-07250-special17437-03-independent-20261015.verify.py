"""Offline hash/quote/path/ID bookkeeping; no semantic approval or status changes."""
import pathlib,json,gzip,hashlib,collections,sys
R=pathlib.Path(__file__).resolve().parents[1];P=R/'native_batches/review08250-17437-03/BATCH.json';B=json.loads(P.read_text());Z=B['records'][0];S=Z['source_after'];Q=Z['proof'];F=Q['facts'];ID={f['id']:f for f in F};C=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest();H=lambda b:hashlib.sha256(b).hexdigest()
assert H(P.read_bytes())=='f40f34eb95482240139d0986e989ec6ff0c657ff776c830c88da110768763716';assert C(B)=='ec9c490f374da25e3859cbdfc0411122ed6229229edd2701bca0395a8e34840d'
def at(p):
 v=S
 for k in p.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
for f in F:
 assert f['quote'] in at(f['pointer'])
 if '/realization_content/' in f['pointer']:assert f['pointer'].split('/')[3]==f['realization_id']
 for key in f['requires']:assert key in ID and ID[key]['realization_id']==f['realization_id'] and ID[key]['mode'] in ['prerequisite','preservation']
seen=set();active=set()
def visit(i):
 if i in seen:return
 assert i not in active;active.add(i)
 for k in ID[i]['requires']:visit(k)
 active.remove(i);seen.add(i)
for i in ID:visit(i)
covered=set()
for u in Q['source_units']:
 assert u['quote']==at(u['pointer'])
 for i in u['fact_refs']:assert ID[i]['realization_id']==u['realization_id'] and ID[i]['pointer']==u['pointer'];covered.add(i)
 assert (u['disposition']=='semantic' and u['fact_refs']) or (u['disposition']=='nonsemantic' and not u['fact_refs'])
assert covered==set(ID)
for rid,e in Q['effect_sets'].items():
 keys={(f['dimension'],f['target'],f['property']) for f in F if f['realization_id']==rid and f['mode']=='effect'}
 assert keys=={(p['dimension'],p['target'],p['property']) for p in e['properties']}
 assert {k[0] for k in keys}==set(e['dimensions'])
root=json.loads(gzip.decompress((R/'SOURCE.json.gz').read_bytes()));current=json.loads(gzip.decompress((R/'native-inputs/08250-special-quote-color-plan-03/CURRENT-PROPOSAL.json.gz').read_bytes()));cid=Z['candidate_id'];assert current['candidates'][cid]==S;assert root['candidates'][cid]==Z['source_before']
assert {k:v for k,v in root['slot_bindings'].items() if v.get('candidate_id')==cid}=={};assert {k:v for k,v in current['slot_bindings'].items() if v.get('candidate_id')==cid}=={}
original=json.loads((R/'decisions/review_08250_09250_17250_17500.json').read_text())['decisions'][187];assert C(original)=='5589091c1c3a1fb7cd17f66c32f9bf171b2900b426643e3675faa40ca6a6d92c'
catalog=json.loads((R/'CATALOG-FINAL-144-V4.json').read_text());assert C(catalog)==Q['catalog_sha256']
for slot,role in Q['roles'].items():assert C(catalog[slot])==role['spec_sha256'];assert all(i in ID for i in role['fact_refs'])
groups=json.loads((R/'worker-notes/native-07250-special17437-03-independent-20261015.exact-payload-groups.json').read_text())['groups'];classidx={i:g['group'] for g in groups for i in g['actual_fact_indices']};fidgroup={F[i]['id']:classidx[i] for i in range(len(F))}
units=collections.defaultdict(list)
for i,u in enumerate(Q['source_units']):
 rel=u['pointer'].replace('/realization_content/'+u['realization_id']+'/','/realization_content/{RID}/')
 key=(rel,u['quote'],u['disposition'],tuple(sorted({fidgroup[f] for f in u['fact_refs']})))
 units[key].append(i)
U=[{'group':i,'relative_pointer':k[0],'whole_quote':k[1],'disposition':k[2],'fact_payload_group_ids':list(k[3]),'actual_unit_indices':v,'rids':dict(collections.Counter(Q['source_units'][j]['realization_id'] for j in v))} for i,(k,v) in enumerate(units.items())]
out=R/'worker-notes/native-07250-special17437-03-independent-20261015.bookkeeping.json'
if not out.exists():out.write_text(json.dumps({'semantic_approval':False,'batch_raw_sha256':H(P.read_bytes()),'facts_mechanically_bound':len(F),'source_units_mechanically_bound':len(Q['source_units']),'actual_assignment_payload_classes':len(groups),'unit_groups':U,'all_quote_containment_and_unit_reference_checks':True,'all_same_rid_requires_and_acyclic_checks':True,'effect_property_sets_matched':18,'actual_original_current_source_and_item188_hashes_matched':True,'original_and_current_own_bindings':{},'production_or_runtime_validation_claimed':False},ensure_ascii=False,indent=2)+'\n')
print('unitgroups',len(U))
for u in U:
 print(json.dumps({k:v for k,v in u.items() if k not in ['actual_unit_indices','whole_quote']}|{'count':len(u['actual_unit_indices']),'quote':u['whole_quote'] if len(u['whole_quote'])<150 else {'whole_exact_source_field':Q['source_units'][u['actual_unit_indices'][0]]['pointer'],'sha256':H(u['whole_quote'].encode()),'characters':len(u['whole_quote'])}},ensure_ascii=False))
