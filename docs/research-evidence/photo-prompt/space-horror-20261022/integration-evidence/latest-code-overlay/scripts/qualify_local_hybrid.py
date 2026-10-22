#!/usr/bin/env python3
"""Replay frozen real-core positive/exclusion/printed-context slot cases."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import photo_candidate_corpus as c  # noqa: F401 - preserve native qualifier module loading order
import prompt_generator as g
import photo_slot_queries as queries
import audit_global_retrieval as audit
from photo_search_reader import SearchReader,LazyRuntimeData
from photo_embedding_provider import atomic,load_env


def run(a):
    cases=json.loads(a.cases.read_bytes());a.output.mkdir(parents=True,exist_ok=True)
    reader=SearchReader(a.assets);data=LazyRuntimeData(reader);results=[]
    if reader.manifest['space']['provider']=='gemini':
        if not a.allow_gemini:raise ValueError('explicit --allow-gemini required for baseline provider/cache use')
        if len(cases)>80:raise ValueError('qualification baseline query budget exceeded')
        load_env(Path(__file__).resolve().parents[3]/'.env')
    try:
        for case in cases:
            root=Path(case['directory'])
            for name,sha in case['files'].items():
                if hashlib.sha256((root/name).read_bytes()).hexdigest()!=sha:raise ValueError('frozen hybrid input changed')
            controls=json.loads((root/'creative-controls.json').read_bytes())
            core=g.load_authorial_core_arg(root/'authorial-core.json',request_envelope=g.load_request_envelope_arg(root/'request-envelope.json'),creative_control_snapshot=controls)
            embodiment=json.loads((root/'embodiment-review.json').read_bytes())
            start=time.monotonic()
            context=queries.prepare(core,controls,data['slot_catalog'],[case['slot']],a.output/'query-cache',language=case['language'],space=reader.manifest['space'])
            pack=g.generate_candidate_pack(data,core,controls,embodiment,query_context=context,requested_slots=[case['slot']],query_language=case['language'],seed=17)
            issues=audit.audit(pack,data,context)
            if issues:raise ValueError('hybrid audit failed: '+str(issues)[:500])
            directory=a.output/case['key'];directory.mkdir(exist_ok=True)
            atomic(directory/'pack.json',pack);atomic(directory/'query-context.json',context)
            hit=case['target'] in pack['global_retrieval']['selected_candidate_ids']
            result={'key':case['key'],'mode':case['mode'],'language':case['language'],'target':case['target'],'hit':hit,
                    'forbidden_adoption':hit if case['mode']!='positive' else False,'audit_pass':True,'seconds':time.monotonic()-start,
                    'selected_ids':pack['global_retrieval']['selected_candidate_ids']}
            results.append(result);print(json.dumps(result),flush=True)
    finally:reader.close()
    summary={'schema':'photo-local-hybrid-qualification/v1','space':reader.manifest['space'],'corpus_sha256':reader.manifest['corpus_sha256'],
             'cases_sha256':hashlib.sha256(a.cases.read_bytes()).hexdigest(),'cases':len(results),
             'forbidden_adoptions':sum(r['forbidden_adoption'] for r in results),'audit_pass':True,
             'languages':{lang:{'positive_cases':sum(r['mode']=='positive' and r['language']==lang for r in results),
                 'positive_hits':sum(r['hit'] and r['mode']=='positive' and r['language']==lang for r in results)} for lang in ('ko','en')},'results':results}
    atomic(a.output/'hybrid-summary.json',summary);return summary


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--assets',type=Path,required=True)
    p.add_argument('--cases',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--allow-gemini',action='store_true');a=p.parse_args();print(json.dumps(run(a)))


if __name__=='__main__':main()
