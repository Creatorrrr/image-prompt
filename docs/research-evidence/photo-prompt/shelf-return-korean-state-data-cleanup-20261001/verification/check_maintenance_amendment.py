from pathlib import Path
import sys,json,subprocess,copy,hashlib,socket,urllib.request
R=Path('/workspace/scratch/ce8f20680f5a/image-prompt');E=R/'docs/research-evidence/photo-prompt/shelf-return-korean-state-data-cleanup-20261001';O=E/'preparation-revisions/pre-maintenance-binding';sys.path.insert(0,str(E))
def deny(*a,**k):raise AssertionError('API/network/write forbidden')
socket.create_connection=deny;socket.socket.connect=deny;urllib.request.urlopen=deny;urllib.request.build_opener=deny
import cycle_common as c
c.write_json=deny;c.g.embed_texts_with_gemini=deny;c.g.get_gemini_api_key=deny;c.g.cached_gemini_client=deny
f=c.load_freeze();old=c.read_json(O/'frozen-inventory-queries.json');rev=c.read_json(E/'maintenance-binding-revision.json');assert c.sha((E/'frozen-inventory-queries.json').read_bytes())=='9874c3e2ffc0ca109809123415936af0500ef6712db4d946f3f8c77c3d91842e';assert c.sha((O/'frozen-inventory-queries.json').read_bytes())==rev['original_freeze_sha256']=='562ca3a65499c35305169cac656c413293bc793ba72bd90f5387ce0a96eaed20'
changed=[k for k in set(f)|set(old)if f.get(k)!=old.get(k)];assert set(changed)==set(rev['allowed_freeze_changes']);assert f['maintenance_revision']==rev
for name,h in old['artifact_sha256'].items():
 p=O/name if (O/name).exists()else E/name
 assert c.sha(p.read_bytes())==h,(name,'original frozen artifact differs')
oldrec=c.read_json(R/rev['old_record_file']);newrec=c.read_json(R/rev['new_record_file']);assert (R/rev['old_record_file']).read_bytes()==subprocess.check_output(['git','show',f['baseline_commit']+':'+rev['old_record_file']],cwd=R)
assert {k:v for k,v in oldrec.items()if k not in['record_id','authored_source_sha256']}=={k:v for k,v in newrec.items()if k not in['record_id','authored_source_sha256']}
for which in ['old','new']:assert c.sha((R/rev[which+'_record_file']).read_bytes())==rev[which+'_record_file_sha256'];assert c.objsha(c.read_json(R/rev[which+'_record_file']))==rev[which+'_reference']['sha256']
base=c.read_json(E/'baseline-raw-extension.json');expected=copy.deepcopy(base);target=next(x for x in expected['slots']['aftermath_trace']if x['id']==c.TARGET.split(':')[-1]);target['ko']=c.PROPOSED_KO;measured=c.read_json(O/'measured-ko-only-proposal.json');assert expected==measured;assert c.sha((O/'measured-ko-only-proposal.json').read_bytes())==rev['original_proposed_raw_source_sha256'];expected['maintenance_ref']=rev['new_reference'];assert c.read_json(R/f['source_file'])==expected;assert (R/f['source_file']).read_bytes()==c.raw_proposal(f);assert c.objsha({k:v for k,v in expected.items()if k!='maintenance_ref'})==newrec['authored_source_sha256']==rev['new_authored_source_sha256']
for name,h in rev['unchanged_measured_artifact_sha256'].items():assert c.sha((E/name).read_bytes())==h
assert c.sha((c.A/'photo_prompt_semantic_index.json').read_bytes())==rev['unchanged_index_manifest_sha256']
states=c.states_from_freeze(f);assert states==c.states_from_freeze(old);assert c.g.load_json(c.A/'photo_prompt_tags.json')==states['proposal'];assert c.g.dictionary_hash(states['proposal'])==rev['unchanged_dictionary_hash']
print('PASS exact metadata-only amendment: old freeze/artifacts preserved; old record byte-identical to baseline; new record differs in only record_id/authored_source_sha256; raw ko proposal plus maintenance_ref only; all merged data/query/input/ranking/cache/index invariants unchanged. Freeze changed keys:',sorted(changed))
print('New artifact binding keys:',sorted(set(f['artifact_sha256'])-set(old['artifact_sha256'])))
