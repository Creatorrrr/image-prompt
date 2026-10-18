"""Build a source-verified separate-lane generation; never activates it."""
from pathlib import Path
import argparse
import resource
import sys
import time

ROOT=Path(__file__).resolve().parents[4];E=Path(__file__).parent
S=ROOT/'skills/photo-prompt-image-generator';OLD=E.parent/'candidate-semantic-renewal-20261018'
CACHE=Path.home()/'.cache/image-prompt/candidate-recall-followup-20261019'
sys.path.insert(0,str(S/'scripts'))
from photo_candidate_authoring import read, write, file_sha
from photo_candidate_lane_generation import baseline, stage, Generation


def verify_freeze():
    for name in ['FREEZE.json','BUILDER-FREEZE.json']:
        for path,sha in read(E/name)['files'].items():
            if file_sha(ROOT/path)!=sha:raise ValueError('frozen input or implementation changed: '+path)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('arm',choices=['D1','D1b'])
    args=parser.parse_args();verify_freeze()
    path=E/('BUILD-'+args.arm+'.json')
    if path.exists():raise ValueError('preserve completed build; no repeat inference')
    started=time.monotonic()
    base,native,native_manifest=baseline(S)
    approval=read(OLD/'REVIEW-ACCEPTANCE.json')
    reviews={}
    for p in sorted((OLD/'reviews').glob('luna-*/*.json')):
        row=read(p)
        if row['decision']=='enrich':reviews[row['candidate_id']]=row
    if len(reviews)!=41:raise ValueError('fixed source-only enrichment scope changed')
    result=stage(CACHE/'store',base,native,native_manifest,reviews,approval,arm=args.arm,
                 skill_root=S,embedding_cache=CACHE/'document-embeddings')
    result['elapsed_seconds']=time.monotonic()-started
    result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':result['peak_rss_bytes']*=1024
    if result['elapsed_seconds']>28800 or result['peak_rss_bytes']>8589934592:
        raise ValueError('frozen workstation resource ceiling exceeded')
    write(path,result)
    print(result,flush=True)
