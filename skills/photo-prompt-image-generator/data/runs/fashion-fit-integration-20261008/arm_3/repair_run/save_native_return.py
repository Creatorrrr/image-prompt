from pathlib import Path
import hashlib,json,shutil,struct,sys
source=Path(sys.argv[1]); dest=Path(sys.argv[2]); run=Path(sys.argv[3]); hint=sys.argv[4]
arm=run.parent.resolve()
if not dest.resolve().is_relative_to(arm) or not run.resolve().is_relative_to(arm):
    raise ValueError("save outside own arm")
if not source.is_file(): raise ValueError("actual tool-returned path unavailable")
if dest.exists(): raise ValueError("native attempt destination exists; preserve previous bytes")
dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copyfile(source,dest)
raw=dest.read_bytes(); original=source.read_bytes()
if raw!=original: raise ValueError("saved native copy changed bytes")
width=height=None
if raw.startswith(b"\x89PNG\r\n\x1a\n"):
    width,height=struct.unpack(">II",raw[16:24])
sha=hashlib.sha256(raw).hexdigest()
metadata={"schema":"actual-native-output/v1","attempt":2,"source_image_path":str(source),"source_image_sha256":sha,"saved_image_path":str(dest.resolve()),"saved_image_sha256":sha,"saved_bytes":len(raw),"native_width":width,"native_height":height,"output_hint":hint,"copy_keeps_source":True,"pixels_modified":False}
(run/"native_tool_output_metadata.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(metadata,ensure_ascii=False))
