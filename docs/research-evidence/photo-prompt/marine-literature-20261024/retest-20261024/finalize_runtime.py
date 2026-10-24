"""Seal exact latest producer AND independent auditor scope compatibility."""
from pathlib import Path
import gc;gc.disable()
import ast,hashlib,json,shutil,sys
T=Path(__file__).resolve().parent;R=T.parents[4];S=R/'skills/photo-prompt-image-generator';STAGE=T/'successor-skill'
read=lambda p:json.loads(Path(p).read_bytes())
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def fn(path,name):
 text=path.read_text();lines=text.splitlines(keepends=True);node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name==name);return node,lines
def port_function(rel,name):
 node,lines=fn(STAGE/rel,name);fresh,newlines=fn(S/rel,name)
 (STAGE/rel).write_text(''.join(lines[:node.lineno-1]+newlines[fresh.lineno-1:fresh.end_lineno]+lines[node.end_lineno:]))

def main():
 initial=read(T/'successor.json');write(T/'successor.initial-seal.json',initial)
 # A concurrent, validated selector advanced only code, with an identical corpus.
 # Prefer that complete installed kernel over maintaining a private backport.
 current=read(T/'current-compatible-base.json');latest=Path(current['native'])
 assert current['source_corpus_equals_original_release_base'] and current['H_F2_code_equals_staged']
 prior_base=read(T/'release-base.json');oldN=Path(prior_base['native'])
 modules=read(oldN/'assets/photo_candidate_corpus_manifest.json')['modules']
 assert modules==read(latest/'assets/photo_candidate_corpus_manifest.json')['modules']
 assert all((oldN/'assets'/m['file']).read_bytes()==(latest/'assets'/m['file']).read_bytes() for m in modules)
 latest_manifest=read(latest/'manifest.json')
 for rel,row in latest_manifest['members'].items():
  if rel.startswith(('scripts/','precore/')):
   dst=STAGE/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(latest/rel,dst)
   assert hashlib.sha256(dst.read_bytes()).hexdigest()==row['sha256']
 if not (T/'release-base.original.json').exists():write(T/'release-base.original.json',prior_base)
 write(T/'release-base.json',{**prior_base,**current,'captured_after_code_only_selector_advance':True})
 port=read(T/'runtime-compatibility-port.json')
 names=list(dict.fromkeys([*port['ported_files'],'scripts/audit_composed_prompt.py']))
 port['ported_files']={p:hashlib.sha256((STAGE/p).read_bytes()).hexdigest() for p in names}
 port['independent_auditor_scope_projection_ported']=True
 base=read(T/'release-base.json');manifest=read(Path(base['native'])/'manifest.json')
 port['all_other_original_members_unchanged']=all(hashlib.sha256((STAGE/p).read_bytes()).hexdigest()==row['sha256'] for p,row in manifest['members'].items() if p.endswith('.py') and p.startswith(('scripts/','precore/')))
 port['final_strategy']='Exact complete current installed kernel reused; private compatibility port superseded.'
 port['installed_kernel_code_sha256']=current['config']['code_sha256']
 assert port['all_other_original_members_unchanged']
 write(T/'runtime-compatibility-port.json',port)
 runtime=STAGE/'.runtime'
 if runtime.is_symlink():runtime.unlink()
 runtime.mkdir(exist_ok=True)
 env=runtime/'embedding-python'
 if not env.exists():env.symlink_to(S/'.runtime/embedding-python',target_is_directory=True)
 lock=read(STAGE/'embedding-runtime.lock.json')
 for name,row in lock['files'].items():
  src=S/lock['package']/name;dst=STAGE/lock['package']/name;dst.parent.mkdir(parents=True,exist_ok=True)
  if not dst.is_file() or hashlib.sha256(dst.read_bytes()).hexdigest()!=row['sha256']:shutil.copyfile(src,dst)
  assert not dst.is_symlink() and hashlib.sha256(dst.read_bytes()).hexdigest()==row['sha256']
 sys.path.insert(0,str(STAGE/'scripts'))
 from photo_runtime_sources import SnapshotPublisher
 from photo_h_f2_generation import stage,Generation
 from photo_recall_generation import read as read_any
 pub=SnapshotPublisher(STAGE,T/'successor-store').stage();write(T/'native-staged.final.json',pub)
 H=Path(initial['store'])/'h-f2-generations'/initial['generation_id'];m=read(H/'manifest.json')
 inputs={'generation':str(H),'documents':str(H/'documents.json.gz'),'field_documents':str(H/'field-documents.json.gz'),'fields':str(H/'fields.json.gz'),'proofs':str(H/'document-proofs.json.gz'),'vectors':str(H/'vectors.f64'),'binding':m['binding'],'native_generation_id':pub['generation_id']}
 gid=stage(T/'successor-store',inputs);Generation(T/'successor-store',gid,full=True)
 result={**initial,'generation_id':gid,'native_generation_id':pub['generation_id'],'kernel_changes':'Exact complete current installed kernel reused; private compatibility port superseded. No scoring or sampling changes.','kernel_code_unchanged_vs_selected_base':True,'independent_auditor_query_scope':True,'scope_tests_pending':True}
 write(T/'successor.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':main()
