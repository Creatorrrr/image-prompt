"""Validate the applied contract batch; never calls a text/image provider."""
from pathlib import Path
import collections,hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SKILL=ROOT/'skills/photo-prompt-image-generator';sys.path.insert(0,str(SKILL/'scripts'))
import photo_candidate_corpus as c
import photo_global_index as index
import photo_search_layout as layout
import photo_runtime_sources as runtime

def main():
 data=c.load(SKILL/'assets');manifest=json.loads((SKILL/'assets'/c.MANIFEST_NAME).read_text());baseline=json.loads((HERE/'BASELINE.json').read_text());before={'candidates':{},'slot_bindings':{},'slot_catalog':{},'policies':{}}
 for module in manifest['modules']:
  raw=subprocess.check_output(['git','show',baseline['head']+':'+str((SKILL/'assets'/module['file']).relative_to(ROOT))]);before[module['kind']].update(json.loads(raw)[module['kind']])
 assert set(before['candidates'])==set(data['candidates'])
 assert data['slot_bindings']==before['slot_bindings'];assert data['slot_catalog']==before['slot_catalog'];assert data['policies']==before['policies']
 changed={cid:row for cid,row in data['candidates'].items() if row!=before['candidates'][cid]}
 assert len(changed)==13
 for cid,row in data['candidates'].items():
  old=before['candidates'][cid];assert row['conditions']==old['conditions'];assert row['provenance']==old['provenance']
 owners=collections.Counter(cid for m in manifest['modules'] if m['kind']=='candidates' for cid in json.load(open(SKILL/'assets'/m['file']))['candidates']);assert set(owners)==set(data['candidates']) and set(owners.values())=={1}
 pairs=[(b['candidate_id'],b['slot_id']) for b in data['slot_bindings'].values()];assert len(pairs)==len(set(pairs))
 old_positive={cid for cid,row in before['candidates'].items() if row['record_kind'] in index.POSITIVE_KINDS};new_positive=set(index.documents(data));removed=old_positive-new_positive;assert len(removed)==6 and not new_positive-old_positive
 for cid in removed:assert data['candidates'][cid]['record_kind']=='diagnostic'
 search_manifest=c.decode((SKILL/'assets'/layout.MANIFEST).read_bytes());verification=layout.verify(SKILL/'assets',data,search_manifest)
 snapshot=runtime.RuntimeSnapshotProvider(SKILL).acquire();assert snapshot.manifest['search_layout']['corpus_sha256']==c.digest(data);snapshot.data.reader.close()
 protected={path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in baseline['protected']};assert protected==baseline['protected']
 active=[search_manifest['metadata']['path']]+[m['path'] for m in search_manifest['shards']]
 assert len(active)==len(set(active));assert all((SKILL/'assets'/path).is_file() for path in active)
 report={'schema':'photo-stage05-contract-batch-verification/v1','verified':True,'source_schema':c.SCHEMA,'pack_schema':'photo-candidate-pack/v10','retrieval_schema':'photo-slot-retrieval/v4','role_proposal_schema':'photo-request-role-proposal/v3','bundle_schema':'photo-candidate-bundles/v2','canonical_candidates':len(data['candidates']),'source_sha256':c.digest(data),'positive_candidates':len(new_positive),'diagnostic_candidates':len(data['candidates'])-len(new_positive),'slots':len(data['slot_catalog']),'bindings':len(data['slot_bindings']),'changed_records':sorted(changed),'removed_positive_ids':sorted(removed),'changed_positive_text_ids':sorted(cid for cid in new_positive if index.text(before['candidates'][cid])!=index.text(data['candidates'][cid])),'original_conditions_and_provenance_preserved':True,'candidate_ids_preserved':True,'native_tags_written':False,'duplicate_relationships':0,'single_payload_owner':True,'layout':verification,'layout_id':search_manifest['layout_id'],'generation_id':snapshot.generation_id,'source_fingerprint':snapshot.manifest['source_fingerprint'],'active_closure':active,'protected_dirty_files':protected,'semantic_stage05_complete':False,'stages06_08_complete':False}
 (HERE/'NATIVE-VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in report.items() if k not in ['active_closure','changed_records','removed_positive_ids','protected_dirty_files']})
if __name__=='__main__':main()
