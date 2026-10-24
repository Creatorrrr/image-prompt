"""Bilingual authored-source retrieval probes; exposure is not semantic adoption."""
import collections,csv,gc,json,sys,hashlib
from pathlib import Path
gc.disable()
ROOT=Path('/Users/chasoik/Projects/image-prompt');S=ROOT/'skills/photo-prompt-image-generator';O=Path(__file__).resolve().parent;Q=O.parent
def read(p):return json.loads(p.read_bytes())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
    rel=read(O/'successor.json');sys.path.insert(0,str(Path(rel['store'])/'generations'/rel['native_generation_id']/'scripts'))
    from photo_h_f2_generation import Generation
    from photo_h_f2_encoder import LocalEncoder
    import photo_recall_first as rf
    lookup=read(O/'card-candidate-map.json');fresh=read(O/'new-native-records.json');diagnostic={cid for cid,v in fresh.items() if v['record_kind']=='diagnostic'}
    g=Generation(rel['store'],rel['generation_id'],full=True);cases=[]
    for d in read(Q/'candidate-drafts.json')['drafts']:
        for language in ('en','ko'):cases.append({'id':d['card_id']+'_'+language,'set':'source_description_development','language':language,'query':d['positive_'+language],'expected_CIDs':[lookup[d['card_id']]]})
    with (Q/'BOUNDARY-CASES.tsv').open() as f:
        for row in csv.DictReader(f,delimiter='\t'):
            for language in ('en','ko'):cases.append({'id':row['id']+'_'+language,'set':'boundary_development','language':language,'query':row['query_'+language],'expected_CIDs':[lookup[k] for k in row['card_ids'].split(',') if lookup[k] not in diagnostic],'expected_boundary':row['expected'],'forbidden_claim':row['forbidden']})
    write(O/'retrieval-cases.json',cases)
    probe=O/'query-embedding-evidence.json'
    if probe.exists():
        encoded=read(probe);assert encoded['queries_sha256']==hashlib.sha256((O/'retrieval-cases.json').read_bytes()).hexdigest();assert encoded['binding']==g.binding
    else:
        encoded={'queries_sha256':hashlib.sha256((O/'retrieval-cases.json').read_bytes()).hexdigest(),'binding':g.binding,'rows':[]}
        with LocalEncoder(S) as e:
            assert e.binding==g.binding
            for start in range(0,len(cases),12):
                batch=cases[start:start+12];vectors=e.encode([r['query'] for r in batch],'query')
                for case,ev in zip(batch,vectors,strict=True):
                    rf.check_embedding(ev,g.binding,case['query'],'query');encoded['rows'].append({'id':case['id'],'embedding':ev})
                print('encoded',len(encoded['rows']),flush=True)
        write(probe,encoded)
    index=g.index();rows=[]
    for case,ev in zip(cases,encoded['rows'],strict=True):
        assert case['id']==ev['id'];result=index.search(case['query'],ev['embedding'],g.binding);order=result['order']
        assert not any(r['cid'] in diagnostic for r in order),'Diagnostic positive leak'
        rank=next((i+1 for i,r in enumerate(order) if r['cid'] in case['expected_CIDs']),None)
        rows.append({**case,'rank':rank,'top8':order[:8],'population':result['considered_CIDs'],'lane_calls':result['lane_calls'],'semantic_adoption':'NOT_TESTED'})
        if len(rows)%20==0:print('searched',len(rows),flush=True)
    positive=[r for r in rows if r['set']=='source_description_development']
    summary={'status':'complete','generation_id':g.id,'queries':len(rows),'positive_description_queries':len(positive),'boundary_queries':len(rows)-len(positive),'diagnostic_positive_leaks':0,'positive_target_at8':sum(r['rank'] is not None and r['rank']<=8 for r in positive),'positive_target_at32':sum(r['rank'] is not None and r['rank']<=32 for r in positive),'positive_target_at96':sum(r['rank'] is not None and r['rank']<=96 for r in positive),'population':rows[0]['population'],'limit':'Authored development descriptions/boundary probes, not independent holdout. No claim of boundary-compliant adoption, baseline improvement, native semantic qualification or pixels.'}
    write(O/'retrieval-qualification.json',{'summary':summary,'cases':rows});print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
