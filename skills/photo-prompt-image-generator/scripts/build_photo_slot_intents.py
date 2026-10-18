"""Bind directly authored slot rows to an existing managed authoring material.

Input is {overall_intent: string, slots: object}. This tool writes hashes and
validates the neutral contract; it never writes expression goals or queries.
"""
import argparse
import json
from pathlib import Path
import subprocess

from photo_installed_h_f2 import (CONFIG, SKILL_ROOT, default_store, read, release,
                                runtime_python)
from photo_workflow_state import load_state, value, verify_freeze


def build(run, authored, output):
    state = load_state(run)
    verify_freeze(state)
    material = value(state, "slot_intent_material")
    config = read(SKILL_ROOT / CONFIG)
    native, manifest, _ = release(default_store(), config["generation_id"])
    program = """import sys,json;sys.path.insert(0,sys.argv[1])
import photo_slot_expression as e
data=json.load(sys.stdin);m=data['material'];a=data['authored']
if set(a)!={'overall_intent','slots'}:raise ValueError('authored overall_intent and slots required')
p=e.create(m['core'],m['controls'],m['catalog'],a['slots'],a['overall_intent'])
e.validate(p,m['core'],m['controls'],m['catalog'],m['requested_slot_ids'])
print(json.dumps(p,ensure_ascii=False,indent=2))
"""
    result = subprocess.run([str(runtime_python(SKILL_ROOT, manifest)), "-I", "-c", program,
                             str(native / "scripts")], input=json.dumps({"material": material,
                             "authored": read(authored)}, ensure_ascii=False), text=True, capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr)
    Path(output).write_text(result.stdout)
    return {"status": "pass", "output": str(Path(output).resolve()), "authored_semantics_unchanged": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--authored", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.run, args.authored, args.output), ensure_ascii=False))
