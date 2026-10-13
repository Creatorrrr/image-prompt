#!/usr/bin/env python3
"""Validate the sole native shared source and its shared generated index."""
from pathlib import Path
import argparse,json
import photo_candidate_corpus as c
import photo_shared_views as views
import photo_global_index as index
import photo_search_layout as layout
from photo_candidate_context import primary_context_alternatives

def validate_source_corpus(root,data,inventory=None):
    errors=[]
    try:
        source=views.source(data);c.validate(source)
        if inventory:inventory.validate()
        for cid,record in source['candidates'].items():
            content=record['content'];primary_context_alternatives(content.get('primary_context_alternatives'))
            for key in ('for_any','for_all','exclude_for_any','requires_primary_any_tags','requires_any_tags','requires_all_tags','exclude_any_tags'):
                if key in content:c.strings(content[key],cid+'.'+key)
            if 'relations' in content:
                from photo_candidate_semantics import validate_relations
                validate_relations(content['relations'],cid)
        if '_global_index' in data:  # Explicit offline fixture vector map only.
            index.validate(data['_global_index'],source)
        elif (Path(root)/'assets'/layout.MANIFEST).is_file():
            assets=Path(root)/'assets'
            layout.verify(assets,source,c.decode((assets/layout.MANIFEST).read_bytes()))
        else:raise ValueError('native lazy search manifest required')
    except (ValueError,KeyError,TypeError) as error:errors.append(str(error))
    return errors

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--assets',type=Path,default=Path(__file__).resolve().parents[1]/'assets');a=p.parse_args();data=c.load(a.assets);errors=validate_source_corpus(a.assets.parent,data)
    print(json.dumps({'native_candidates':len(data['candidates']),'bindings':len(data['slot_bindings']),'errors':errors},ensure_ascii=False));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
