"""Separate-process original-main/full-payload equivalence and timing evidence."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import tarfile
import time


def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def worker(args):
    sys.path.insert(0,str(args.skill / "scripts"))
    import prompt_generator as pg
    start=time.perf_counter()
    if args.arm=="baseline":
        data=pg.load_runtime_data()
        pg._core_slot_index(canonical(data["slots"]).decode())
        generation=None
        cache=None
    else:
        from photo_runtime_sources import RuntimeSnapshotProvider
        provider=RuntimeSnapshotProvider(args.skill,args.store)
        snapshot=provider.acquire()
        data=snapshot.data
        generation=snapshot.generation_id
        cache=snapshot.cache_status
    preparation=time.perf_counter()-start
    index=data.slot_index(canonical(data["slots"]).decode()) if hasattr(data,"slot_index") else pg._core_slot_index(canonical(data["slots"]).decode())
    result={"arm":args.arm,"preparation_seconds":preparation,"generation_id":generation,"cache_status":cache,
            "slot_corpus_sha256":sha(data["slots"]),"full_slot_index_sha256":sha(index),
            "document_count":len(index["documents"]),"cases":[]}
    if args.arm=="runtime":
        before=time.perf_counter()
        repeated=provider.acquire()
        result["warm_acquire_seconds"]=time.perf_counter()-before
        assert repeated.data is snapshot.data
    if args.archive:
        with tarfile.open(args.archive) as archive:
            names=sorted(row.name for row in archive.getmembers() if row.name.endswith("/authorial-core.json"))
            for name in names:
                prefix=name.removesuffix("/authorial-core.json")
                controls=json.load(archive.extractfile(prefix+"/creative-controls.json"))
                envelope=pg.normalize_request_envelope(json.load(archive.extractfile(prefix+"/request-envelope.json")))
                core=pg.normalize_authorial_core(json.load(archive.extractfile(name)),request_envelope=envelope,creative_control_snapshot=controls)
                before=sha(core)
                slots=pg.retrieve_core_slots(data,core,controls)
                review={"contract_version":"photo-embodiment-review/v1","provenance":"agent_prepack",
                        "prompt_sha256":hashlib.sha256(core["baseline_prompt_en"].encode()).hexdigest(),
                        "scope":"not_applicable","summary":"Retrieval-only controlled replay; no pixel or physical qualification.","checks":{}}
                pack=pg.generate_candidate_pack(data,core,controls,review,seed=91)
                assert sha(core)==before
                result["cases"].append({"id":prefix,"core_sha256":before,"retrieval_sha256":sha(slots),
                    "pack_sha256":sha(pack),"visual_sha256":{key:sha(pack.get(key)) for key in
                        ("visual_obligations","visual_concept_candidates","semantic_clarification")},
                    "candidate_count":sum(len(row["candidates"]) for row in slots[0].values())})
    Path(args.result).write_text(json.dumps(result,indent=2)+"\n")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--worker",action="store_true")
    parser.add_argument("--skill",type=Path)
    parser.add_argument("--baseline",type=Path)
    parser.add_argument("--archive",type=Path)
    parser.add_argument("--store",type=Path,required=True)
    parser.add_argument("--result",type=Path,required=True)
    parser.add_argument("--arm",choices=("baseline","runtime"))
    parser.add_argument("--repeats",type=int,default=3)
    args=parser.parse_args()
    if args.worker:
        worker(args)
        return
    samples=[]
    for repeat in range(args.repeats):
        for arm in (("baseline","runtime") if repeat%2==0 else ("runtime","baseline")):
            result=args.result.with_name(f"{arm}-{repeat+1}.json")
            command=[sys.executable,str(Path(__file__).resolve()),"--worker","--arm",arm,"--skill",
                str(args.baseline if arm=="baseline" else args.skill),"--store",str(args.store),"--result",str(result)]
            if repeat==0 and args.archive:
                command.extend(["--archive",str(args.archive)])
            subprocess.run(command,check=True,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"})
            samples.append(json.loads(result.read_text()))
            print(f"{arm} preparation {samples[-1]['preparation_seconds']:.3f}s",flush=True)
    baseline=next(row for row in samples if row["arm"]=="baseline")
    runtime=next(row for row in samples if row["arm"]=="runtime")
    for key in ("slot_corpus_sha256","full_slot_index_sha256","document_count","cases"):
        assert baseline[key]==runtime[key],key
    record={"schema":"photo-runtime-freshness-equivalence/v1","source_pin":"cb496c1db984f9fe5d632fa764aae4d3f6aedf63",
            "full_index_exact":True,"frozen_query_and_public_pack_case_count":len(baseline["cases"]),
            "frozen_cases_exact":True,"samples":samples,
            "preparation_median_seconds":{arm:statistics.median(row["preparation_seconds"] for row in samples if row["arm"]==arm) for arm in ("baseline","runtime")},
            "proof_boundary":"Preparation plus controlled frozen retrieval/full public-pack equality. OS file caches not cleared; no image/embedding APIs or native pixels. Bootstrap cost is reported in the first runtime sample."}
    args.result.write_text(json.dumps(record,indent=2)+"\n")


if __name__=="__main__":
    main()
