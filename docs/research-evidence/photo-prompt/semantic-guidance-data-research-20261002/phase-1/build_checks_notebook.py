"""Save the exact scoped checks as a portable notebook with observed outputs.

Cells execute with standard-library Python in this process. This environment
does not provide a Jupyter kernel; the execution method is explicitly recorded.
"""
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
import json

OUT = Path(__file__).resolve().parent

INTRO = """# 첫 조사 묶음의 구조·출처·보존 확인

분석 단위는 연구 카드 1개, 문맥 사례 쌍 1개, 기존 프로필 1개다.
이 검사는 의미 등가성·모델 지식·생성 여부·검열 통과율·픽셀 성과를 측정하지 않는다.
모든 예문과 변형은 작성용 초안이며 독립 평가용 홀드아웃이 아니다.

아래 셀은 표준 라이브러리 Python으로 실제 실행한 출력이다. 이 환경에는
Jupyter 커널이 없어, 노트북 셀을 동일 프로세스에서 순서대로 실행해 저장했다.
"""

SETUP = """from pathlib import Path
import json
import runpy

relative = Path('docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-1')
folder = next((p if (p / 'verify_research.py').is_file() else p / relative)
              for p in (Path.cwd(), *Path.cwd().parents)
              if (p / 'verify_research.py').is_file() or (p / relative / 'verify_research.py').is_file())
checks = runpy.run_path(str(folder / 'verify_research.py'))
report = checks['validate']()
print(json.dumps({key: report[key] for key in (
    'structural_status', 'source_file_protection_status',
    'baseline_loaded_profiles', 'observed_loaded_profiles',
    'protected_skill_files', 'changed_skill_files',
    'changed_selected_profiles', 'counts')}, ensure_ascii=False, indent=2))
"""

COVERAGE = """print(json.dumps({
    'source_access_counts': report['source_access_counts'],
    'context_relation_counts': report['context_relation_counts'],
    'not_run': report['not_run'],
}, ensure_ascii=False, indent=2))
"""


def main():
    cells = [{"cell_type": "markdown", "id": "scope", "metadata": {}, "source": INTRO.splitlines(True)}]
    context = {}
    for i, code in enumerate((SETUP, COVERAGE), 1):
        stream = StringIO()
        with redirect_stdout(stream):
            exec(compile(code, f"research-checks-cell-{i}", "exec"), context)
        cells.append({"cell_type": "code", "id": f"checks-{i}", "metadata": {},
                      "source": code.splitlines(True), "execution_count": i,
                      "outputs": [{"output_type": "stream", "name": "stdout", "text": stream.getvalue().splitlines(True)}]})
    notebook = dict(cells=cells, nbformat=4, nbformat_minor=5,
                    metadata={"language_info": {"name": "python", "version": "3"},
                              "research_execution": {"method": "sequential stdlib Python execution; no Jupyter kernel",
                                                     "checked_at_kst": context["report"]["checked_at_kst"]}})
    (OUT / "research-checks.ipynb").write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"executed_code_cells": 2, "errors": 0, "method": "stdlib Python, not Jupyter kernel"}))


if __name__ == "__main__":
    main()
