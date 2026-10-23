"""Read-only diagnostics for this task's own staging process; no source/guard edits."""
def _school_capture_build_stack():
    import sys,json,traceback,time
    from pathlib import Path
    frames=[]
    f=sys._getframe().f_back
    while f is not None:
        variables={}
        for key,value in f.f_locals.items():
            if isinstance(value,(dict,list,tuple,str,bytes)):
                variables[key]={'type':type(value).__name__,'len':len(value)}
        frames.append({'file':f.f_code.co_filename,'function':f.f_code.co_name,'line':f.f_lineno,'container_lengths':variables})
        f=f.f_back
    p=Path('/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/school-life-20261023/integration-evidence/build-stack-snapshot.json')
    p.write_text(json.dumps({'timestamp':time.time(),'stack':traceback.format_stack(),'frames':frames,'mutation':'none; lengths and traceback only'},indent=2)+'\n')
_school_capture_build_stack()
del _school_capture_build_stack
