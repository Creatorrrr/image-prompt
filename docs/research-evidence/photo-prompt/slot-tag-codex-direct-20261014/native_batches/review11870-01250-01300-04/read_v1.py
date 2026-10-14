import json,gzip,pathlib,hashlib,sys
R=pathlib.Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');D=R/'native-inputs/prepared/review11870-01250-01300-04';P=json.loads((D/'PREPARED-PACKET.json').read_text());I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(pathlib.Path(I['current_snapshot']['file']).read_bytes()));C=json.loads(pathlib.Path('docs/research-evidence/photo-prompt/slot-retrieval-stage05-20261012/CONTROLLED-FINAL-SOURCE.json').read_text());cb=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
a,b=map(int,sys.argv[1:3]);assert 1250<=a<b<=1300 and b-a<=5
for o in range(a,b):
 cid=P['ids'][o-1250];print('ORDINAL',o,cid)
 for k in ['original_records','current_records','historical_compiled_rows','references','reference_bindings']:print(k,json.dumps(P[k][cid],ensure_ascii=False,indent=2))
 print('complete_own_bindings',json.dumps({k:v for k,v in S['slot_bindings'].items()if v['candidate_id']==cid},ensure_ascii=False,indent=2));print('revision',json.dumps(I['required_revisions'][cid],ensure_ascii=False,indent=2))
 for ref in P['original_records'][cid]['provenance']:
  _,slot,id=ref['source'].split(':');entry=next(x for x in C['slots'][slot]if x['id']==id);h=hashlib.sha256(cb(entry)).hexdigest();print('origin_equality',h==ref['sha256'],h)
  if h==ref['sha256']:print('whole_sha_equal_origin',json.dumps(entry,ensure_ascii=False,indent=2))
