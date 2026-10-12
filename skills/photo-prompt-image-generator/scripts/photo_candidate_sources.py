"""The only runtime source inventory: native shared corpus modules."""
from dataclasses import dataclass
from pathlib import Path
import photo_candidate_corpus as c

@dataclass(frozen=True)
class SourceInventory:
    assets:Path
    rows:tuple
    @classmethod
    def load(cls,assets):
        assets=Path(assets).resolve();manifest=c.decode((assets/c.MANIFEST_NAME).read_bytes())
        if manifest.get('schema')!=c.MANIFEST_SCHEMA or set(manifest)!={'schema','modules'}:raise ValueError('native shared source manifest required')
        rows=[];seen=set()
        for row in manifest['modules']:
            name=row['file'];path=assets/name
            if row['kind'] not in c.MODULE_SCHEMAS or path.parent!=assets or path.is_symlink() or name in seen:raise ValueError('invalid native source owner')
            seen.add(name);rows.append((name,row['kind']))
        return cls(assets,tuple(rows))
    def validate(self):
        c.load(self.assets)
    def check_root(self,path):
        if Path(path).parent.resolve()!=self.assets:raise ValueError('source inventory root mismatch')
