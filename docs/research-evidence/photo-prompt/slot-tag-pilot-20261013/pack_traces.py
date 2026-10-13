"""Pack only this task's completed traces, removing identical label copies."""
import hashlib
import json
from sample import HERE
from trace_io import read_trace, write_trace


def main():
    changes = []
    for suffix in ("contexts.json", "retrieval.json"):
        old = HERE / ("human-en-" + suffix)
        corrected = HERE / ("linen-en-" + suffix)
        assert old.read_bytes() == corrected.read_bytes()
        changes.append({"duplicate_removed": old.name, "identical_survivor": corrected.name,
            "before_sha256": hashlib.sha256(old.read_bytes()).hexdigest()})
        old.unlink()
    for name in ("linen-en", "linen-ko", "object-en", "adult-human-en", "adult-human-ko"):
        path = HERE / (name + "-retrieval.json")
        value = json.loads(path.read_bytes())
        target = path.with_suffix(".json.gz")
        assert not target.exists()
        write_trace(target, value)
        assert read_trace(target) == value
        changes.append({"packed": path.name, "retained": target.name, "json_values_equal": True,
            "before_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "after_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "before_bytes": path.stat().st_size, "after_bytes": target.stat().st_size})
        path.unlink()
    (HERE / "TRACE-PACKING.json").write_text(json.dumps({"verified": True, "changes": changes,
        "scope": "Only traces created by this pilot; no source, historical evidence or user files touched."}, indent=2) + "\n")
    print(json.dumps({"verified": True, "packed_traces": 5, "removed_identical_mislabelled_copies": 2}))


if __name__ == "__main__":
    main()
