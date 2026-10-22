"""Copy only named run evidence; preserve exact bytes and source locators."""
from pathlib import Path
import hashlib
import json
import shutil

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
RUNS = {
    'archive': ROOT / 'generated/photo-runs/lovecraftian-retest-archive-20261022-a53714ff',
    'science': ROOT / 'generated/photo-runs/lovecraftian-retest-science-20261022-c66e9276',
    'encounter': ROOT / 'generated/photo-runs/lovecraftian-retest-encounter-20261022-ad803291-v2',
}
EXTRA = (
    'source-free-concepts.json', 'source-free-concept-choice.json',
    'random-concept-selection.json', 'source-free-note.md',
    'source-contribution.json', 'source-reviews.json', 'complete-source-reviews.json',
    'composition-comparison.md', 'final-prompt.txt', 'composed.json',
    'compose-audit-result.json', 'prepare-render-result.json',
    'pinned-neutral-launcher.json', 'authorization-scope.json',
    'validation-input-field-diff.json', 'input-recovery-provenance.json',
    'run_manifest.json', 'execution-summary.json', 'test-report.json',
    'run-summary.json', 'run-report.json', 'run-report.md',
    'run-summary.md', 'provenance-correction.json',
    'pixel-review.json', 'render-review.json', 'pixel-audit.json',
    'source-pixel-review.json', 'visual-review.json', 'artistic-review.json',
    'artistic-pixel-review.json', 'review-audit-result.json',
    'review-audit-output.json', 'pixel-audit-output.json',
    'compose-audit-output.json', 'runtime-audit-output.json',
    'image_runs.ndjson', 'ledger.ndjson', 'ledger-corrected.ndjson',
    'run_manifest.corrected.json', 'recorder-provenance-correction.md',
    'supplemental-pixel-review.json', 'proof-index.json',
    'native-tool-error-1.json', 'native-tool-error-2.json',
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect():
    copies = []
    for arm, run in RUNS.items():
        state = json.loads((run / 'workflow.json').read_bytes())
        sources = [(run / 'workflow.json', 'workflow.json')]
        for name, item in state['artifacts'].items():
            path = Path(item['path'])
            sources.append((path, 'artifacts/' + name + path.suffix))
        sources.extend((run / name, name) for name in EXTRA if (run / name).is_file())
        for source, relative in sources:
            destination = OUT / 'arms' / arm / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            actual = digest(destination)
            assert actual == digest(source)
            copies.append({'arm': arm, 'source': str(source),
                           'copy': str(destination.relative_to(OUT)), 'sha256': actual})
    (OUT / 'EVIDENCE-COPIES.json').write_text(
        json.dumps({'status': 'pass', 'byte_exact_copies': copies}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'copied': len(copies)}))


if __name__ == '__main__':
    collect()
