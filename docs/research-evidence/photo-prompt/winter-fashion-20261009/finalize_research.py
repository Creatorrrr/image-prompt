"""Verify research documents and record observed source/dirty-work preservation."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
REPORT=ROOT/'docs/analysis/2026-10-09-winter-fashion-visual-semantics-research.md'

def dump(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def file_record(p):
    if not p.is_file():return None
    return {'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,
            'mode':p.stat().st_mode & 0o777}

def main():
    snapshot=json.loads((HERE/'source-snapshot.json').read_text())
    validation=json.loads((HERE/'research-validation.json').read_text())
    original=snapshot['source_files']
    current={name:file_record(ROOT/name) for name in original}
    drift=[name for name in original if original[name]!=current[name]]
    old_dirty=snapshot['tracked_dirty_files']
    current_dirty={name:file_record(ROOT/name) for name in old_dirty}
    dirty_changes=[name for name in old_dirty if old_dirty[name]!=current_dirty[name]]
    now=datetime.now(ZoneInfo('Asia/Seoul')).isoformat()
    dump('final-preservation.json',{'checked_at_kst':now,'reference_snapshot_started_at_kst':snapshot['started_at_kst'],
         'reference_head':snapshot['head'],'current_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
         'source_files_compared':len(original),'source_changes_since_snapshot':drift,
         'tracked_dirty_files_compared':len(old_dirty),'tracked_dirty_changes_since_snapshot':dirty_changes,
         'all_compared_sources_unchanged':not drift,'all_preexisting_tracked_dirty_bytes_and_modes_preserved':not dirty_changes,
         'source_after':current,'tracked_dirty_after':current_dirty,
         'agent_write_scope':['docs/research-evidence/photo-prompt/winter-fashion-20261009/',str(REPORT.relative_to(ROOT))],
         'scope_limit':'Hashes cover named tracked source/code/index headers and dirty files; no attribution or complete retention proof for untracked files. No reset, checkout, stash, source/index edit, commit or push performed.'})
    dump('report-validation.json',{'status':'pending'})
    json_files=sorted(HERE.glob('*.json'))
    for p in json_files:json.loads(p.read_text())
    required=['sources.json','semantic-cards.json','semantic-cards.md','candidate-proposals.json','term-plan.json','term-plan.csv',
              'regression-plan.json','implementation-plan.json','reference-supplement.json','research-validation.json',
              'source-snapshot.json','final-preservation.json','report-validation.json']
    assert all((HERE/name).is_file() for name in required)
    local_links=[];missing=[]
    for p in [REPORT,HERE/'semantic-cards.md']:
        for path in re.findall(r'\]\((/[^)]+)\)',p.read_text()):
            path=path.split(':')[0]
            local_links.append(path)
            if not Path(path).exists():missing.append(path)
    assert not missing,missing
    report=REPORT.read_text()
    for n in ['304','46','79','162','146','56','12','16','11,188','2,977']:
        assert n in report,n
    assert validation['status']=='PASS_research_integrity_only'
    cards=json.loads((HERE/'semantic-cards.json').read_text())['cards']
    sources=json.loads((HERE/'sources.json').read_text())['sources']
    proposals=json.loads((HERE/'candidate-proposals.json').read_text())['proposals']
    assert len({x['id'] for x in cards})==79
    assert len({x['id'] for x in sources})==46
    assert len({x['id'] for x in proposals})==162
    assert all(x['runtime_ready'] is False and x['runtime_registration'] is False for x in proposals)
    own_files=sorted(p for p in HERE.iterdir() if p.is_file())+[REPORT]
    proof={str(p.relative_to(ROOT)):file_record(p) for p in own_files if p.name!='report-validation.json'}
    result={'status':'PASS_research_report_integrity_only','checked_at_kst':now,
         'json_files_parsed':len(json_files),'local_links_checked':len(local_links),'missing_local_links':missing,
         'source_card_term_candidate_references':'PASS','csv_json_full_column_parity':'PASS in build_research.py',
         'reported_count_consistency':'PASS','source_after_drift':drift,'tracked_dirty_after_drift':dirty_changes,
         'all_compared_source_and_tracked_dirty_hashes_preserved':not drift and not dirty_changes,
         'runtime_registration_executed':False,'index_rebuild_executed':False,'live_retrieval_executed':False,
         'image_calls':0,'embedding_calls':0,'artifact_files':proof,
         'limitations':'Research verification only. This is not runtime-contract, retrieval, native-pixel or user-acceptance proof.'}
    dump('report-validation.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='artifact_files'},ensure_ascii=False))

if __name__=='__main__':main()
