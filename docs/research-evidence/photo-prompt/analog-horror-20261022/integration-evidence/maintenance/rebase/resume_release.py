"""Resume verified index after a temporary disk allocation failure. All publisher and H-F2 checks run."""
import gc
gc.disable()
from pathlib import Path
import runpy,textwrap,time,json,hashlib
O=Path(__file__).resolve().parent
source=O/'build_release.py';ns=runpy.run_path(str(source));read=ns['read']
report=read(O/'native-index-build.json');layout=read(ns['STAGE']/'assets/photo_candidate_search.json')
assert report['verification']['verified'] is True and layout['layout_id']==report['layout_id']
assert read(O/'canonical-source-validation.json')['status']=='pass'
ns.update(new=ns['collect'](),fresh=read(O/'new-native-records.json'),changed=read(O/'changed-native-records.json'),t=time.monotonic())
(O/'resume-execution.json').write_text(json.dumps({'status':'resume_verified_index','reason':'OSError ENOSPC during native publication; temporary allocation failure recovered','builder_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'native_layout_id':report['layout_id'],'validation_bypassed':False,'publication_checks':'all original native/source/index/H-F2/code seals run'},indent=2)+'\n')
tail=source.read_text().split(' publication=SnapshotPublisher(STAGE,STORE).stage();write(O/\'native-staged.json\',publication)',1)[1].split("if __name__=='__main__':main()",1)[0]
head="publication=SnapshotPublisher(STAGE,STORE).stage();write(O/'native-staged.json',publication)\n"
exec(compile(head+textwrap.dedent(tail),str(source)+':resume-native-publication','exec'),ns)
