"""Copy only a concrete local image path explicitly returned by the native tool."""
import hashlib
import json
import pathlib
import shutil
import struct
import sys

run = pathlib.Path(sys.argv[1]).resolve()
metadata = json.loads(sys.argv[2])
if len(sys.argv) > 3:
    request = json.loads(sys.argv[3])
    (run / "native_tool_request_actual.json").write_text(
        json.dumps(request, ensure_ascii=False, indent=2) + "\n"
    )
paths = [pathlib.Path(p) for p in metadata.get("reported_paths", [])]
paths = [p for p in paths if p.is_absolute() and p.is_file()]
(run / "native_tool_return_metadata.json").write_text(
    json.dumps(metadata, ensure_ascii=False, indent=2) + "\n"
)
if not paths:
    print(json.dumps({"outcome": "preview_only"}))
    raise SystemExit(0)

source = paths[0]
dest = run / "generated_images" / "letterpress-fit-repair-1.png"
dest.parent.mkdir(parents=True, exist_ok=True)
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest() != source_hash:
    raise RuntimeError("existing_output_conflict")
if not dest.exists():
    shutil.copyfile(source, dest)
image_hash = hashlib.sha256(dest.read_bytes()).hexdigest()
if image_hash != source_hash:
    raise RuntimeError("returned_image_copy_hash_mismatch")
header = dest.read_bytes()[:24]
size = list(struct.unpack(">II", header[16:24])) if header[:8] == b"\x89PNG\r\n\x1a\n" else None
proof = {
    "source_path_explicitly_returned": str(source),
    "source_sha256": source_hash,
    "local_image_path": str(dest),
    "local_image_sha256": image_hash,
    "size": size,
    "copy_method": "byte-for-byte local copy; no pixel editing",
    "returned_path_rule": "Only paths present in the actual native tool result were considered.",
}
(run / "native_result_copy.json").write_text(
    json.dumps(proof, ensure_ascii=False, indent=2) + "\n"
)
print(json.dumps({"outcome": "returned", "image_path": str(dest)}))
