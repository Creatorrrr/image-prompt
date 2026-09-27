"""Project research tables without treating a boundary as a confusion negative."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    rows, section, headers = [], "", []
    for line in (HERE / "RESEARCH.md").read_text().splitlines():
        if line.startswith("## "):
            section, headers = line, []
        if not section.startswith(tuple(f"## {n}." for n in range(3, 8))):
            continue
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not headers:
            headers = cells
            continue
        if all(set(cell) <= set("-:") for cell in cells):
            continue
        if len(cells) != len(headers):
            raise ValueError(f"Mismatched table columns: {line}")
        number = int(section.split(".", 1)[0].split()[-1])
        rows.append({
            "id": f"keyword_relation_{len(rows) + 1:02}",
            "section": section,
            "term_group": cells[0],
            "terms": [term.strip() for term in cells[0].split(" / ")],
            "source_columns": dict(zip(headers, cells)),
            "observable_target_or_relation": cells[1],
            "boundary_relation": cells[2] if number == 4 else None,
            "confusion_or_independent_axes": cells[2] if number != 4 else None,
            "limits_or_implementation": cells[3] if len(cells) == 4 else None,
            "evidence_level": "source_informed_or_authored_visual_analysis",
            "authority": "research_only; see proposals and runtime profiles for actual exact activation",
        })
    payload = {
        "schema_version": "portrait-fashion-exposure-keyword-catalog/v1",
        "scope": "Research tables only; different source columns retain their own meanings. Not runtime discovery input.",
        "group_count": len(rows),
        "term_form_count": sum(len(row["terms"]) for row in rows),
        "rows": rows,
    }
    (HERE / "keyword_catalog.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {payload['group_count']} concept groups and {payload['term_form_count']} term forms")


if __name__ == "__main__":
    main()
