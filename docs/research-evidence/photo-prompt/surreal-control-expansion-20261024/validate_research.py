#!/usr/bin/env python3
"""Check research integrity and unchanged operating source; performs no image/API calls."""
import collections
import hashlib
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'


def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def main():
    checks=[]
    def check(name,condition,detail=None):
        checks.append({'check':name,'pass':bool(condition),'detail':detail})
    expected={'pro-candidate-draft.json':'7f2011db2b3071a4463a33ba29c0c0448b29e982f6afde5866aa7ac409b938aa',
              'pro-research-report.ko.md':'707f0495b3f75d7e47e09518eee67c64358b2f08f9f4305bc3e32ea6dd59b568'}
    check('original_downloads_unchanged',all(sha(HERE/'input'/n)==s for n,s in expected.items()))
    sources=read(HERE/'sources.json')['sources'];source_ids={s['source_id'] for s in sources}
    check('unique_sources',len(source_ids)==len(sources)==25)
    cards=read(HERE/'candidate-proposals.json')['cards'];ids={c['research_id']for c in cards}
    check('unique_cards',len(ids)==len(cards)==26)
    check('explicit_research_status',all(c['native_approval'] is False and c['pixel_status']=='NOT_RUN' and c['intrinsic_surreal_level'] is None for c in cards))
    check('card_completeness',all(c['proposal_en'].strip() and c['proposal_ko'].strip() and c['same_frame_evidence'] and c['confounds'] and c['claim_limits'] and c['relation_record'] for c in cards))
    check('source_reference_closure',all(set(c['source_ids'])<=source_ids for c in cards))
    state=read(HERE/'evidence/corpus-state.json');records={}
    for m in read(ASSETS/'photo_candidate_corpus_manifest.json')['modules']:
        if m['kind']=='candidates':records.update(read(ASSETS/m['file'])['candidates'])
    check('operating_module_bytes_preserved',all(sha(ASSETS/m['file'])==m['sha256']for m in state['modules']))
    check('operating_manifest_preserved',sha(ASSETS/'photo_candidate_corpus_manifest.json')==state['manifest_sha256'])
    check('installed_config_preserved',read(ROOT/'skills/photo-prompt-image-generator/retrieval-runtime.json')==state['runtime_config'])
    check('all_source_record_digests_preserved',read(HERE/'evidence/source-record-digests.json')=={cid:digest(c)for cid,c in records.items()})
    check('neighbor_reference_and_hash_closure',all(n['candidate_id']in records and n['source_sha256']==digest(records[n['candidate_id']])for c in cards for n in c['neighbor_sources']))
    reused=[c for c in cards if c['decision']=='reuse_same_source']
    check('reuse_whole_en_ko_unchanged',all(c['proposal_en']==records[c['reuse_candidate_id']]['content']['en'] and c['proposal_ko']==records[c['reuse_candidate_id']]['content']['ko'] and c['existing_source_sha256']==digest(records[c['reuse_candidate_id']])for c in reused))
    check('reuse_known_card_identity',next(c for c in cards if c['research_id']=='R22')['reuse_candidate_id']=='cand_4f9aa7915bdd53f5b9a974059bebf7d7' and next(c for c in cards if c['research_id']=='R26')['reuse_candidate_id']=='cand_7b3f6740821d5f839db30de43420e00e')
    c4=next(c for c in cards if c['research_id']=='C04')
    check('cup_unobservable_global_absence_removed',all('손잡이가 없' not in str(v) and '다른 손잡이가 없다'not in str(v)for v in [c4['proposal_ko'],c4['same_frame_evidence'],c4['relation_record']]))
    mechanisms=read(HERE/'mechanism-coverage.json')['mechanisms'];mids={m['mechanism_id']for m in mechanisms}
    check('mechanism_reference_closure',len(mids)==12 and all(c['mechanism_id']in mids for c in cards)and all(set(m['witness_candidate_ids'])<=set(records)for m in mechanisms))
    diagnostics=read(HERE/'diagnostics.json')['records']
    check('diagnostics_separate_from_positive_pool',len(diagnostics)==16 and len({d['diagnostic_id']for d in diagnostics})==16 and all(d['positive_retrieval']is False for d in diagnostics))
    cal=read(HERE/'calibration-plan.json');groups=cal['groups']
    check('calibration_shape',len(groups)==8 and sum(len(g['levels'])for g in groups)==32 and all({x['level']for x in g['levels']}=={0,1,2,3}for g in groups))
    check('no_calibration_image_claim',cal['generation_calls_executed']==0 and all(g['is_tested']is False and g['execution_status']=='NOT_RUN'for g in groups))
    check('calibration_reference_closure',all(g.get('candidate_ref')in ids|set(records)for g in groups if 'candidate_ref'in g))
    routes=read(HERE/'discovery-routes.json')['routes']
    check('discovery_route_closure',len(routes)==26 and all(r['research_card_id']in ids and r['mechanism_id']in mids for r in routes))
    check('held_record_not_positive_route',next(r for r in routes if r['research_card_id']=='C07')['positive_material_target']is False)
    ev=read(HERE/'retrieval-evaluation-plan.json')
    check('retrieval_evaluation_shape',ev['case_count']==40 and ev['bilingual_query_count']==80 and len(ev['cases'])==40 and collections.Counter(c['kind']for c in ev['cases'])['intended_relation']==20)
    check('development_not_holdout_or_executed',ev['independent_holdout']is False and ev['status']=='NOT_RUN')
    check('explicit_fantasy_zero_control_exists',any(c.get('preserve_explicit_fantasy')and 'surreal=0'in c['en']for c in ev['cases']))
    for name in ['REPORT.ko.md','IMPLEMENTATION-PLAN.ko.md']:
        text=(HERE/name).read_text()
        missing=[]
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if '://'not in target and not target.startswith('#'):
                clean=target.split('#',1)[0]
                if clean!='VALIDATION.json' and not (HERE/clean).exists():missing.append(clean)
        check('local_links_'+name,not missing,missing)
    result={'schema':'surreal-control-research-validation/v1','status':'pass'if all(c['pass']for c in checks)else'fail',
            'checks':checks,'source_count':len(sources),'card_count':len(cards),
            'decision_counts':dict(collections.Counter(c['decision']for c in cards)),
            'image_calls':0,'operating_source_writes':0,
            'limits':['structural consistency does not prove semantic novelty','no production retrieval qualification','no image or user acceptance claim']}
    (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'checks':len(checks),'failed':[c['check']for c in checks if not c['pass']]},ensure_ascii=False))
    raise SystemExit(0 if result['status']=='pass' else 1)


if __name__=='__main__':main()
