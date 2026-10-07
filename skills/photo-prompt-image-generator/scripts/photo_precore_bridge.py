"""Load shared neutral modules without importing candidate-aware code."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


def load(name):
    key = "photo_precore_" + name
    if key not in sys.modules:
        directory = str(Path(__file__).resolve().parents[1] / "precore")
        spec = spec_from_file_location(key, Path(directory) / (name + ".py"))
        module = module_from_spec(spec)
        sys.modules[key] = module
        added = directory not in sys.path
        if added:
            sys.path.insert(0, directory)
        try:
            spec.loader.exec_module(module)
        except BaseException:
            sys.modules.pop(key, None)
            raise
        finally:
            if added:
                sys.path.remove(directory)
    return sys.modules[key]
