"""Project only reviewed, task-scoped evidence into the native Sources receipt."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
RELPATH = "docs/research-evidence/photo-prompt/semantic-guidance-data-research-20261002/phase-2-20261003"

def load(name): return json.loads((OUT / name).read_text())

snapshot = load("current-snapshot.json")
validation = load("validation-results.json")
plans = load("profile-change-plan.json")["plans"]

count_method = f'''import json
from pathlib import Path
snapshot = json.loads(Path("{RELPATH}/current-snapshot.json").read_text())
print(snapshot["loaded_profile_count"])
print(len(snapshot["selected_profiles"]))'''
check_method = f'''import json
from pathlib import Path
result = json.loads(Path("{RELPATH}/validation-results.json").read_text())
print(len(result["local_anchor_fixtures"]))
print(result["preserved_profile_gates"])
print(result["changed_protected_files"])
print(result["image_generation_calls"])'''
# Execute the exact evidence-display methods locally; no model or source mutation.
exec(compile(count_method, "count-method", "exec"))
exec(compile(check_method, "check-method", "exec"))
payload = {"schemaVersion": 1, "items": [
    {"id": "current-profile-population", "title": "현재 1496개 프로필과 15개 심층 조사 대상", "queries": [{"id": "loaded-profile-snapshot", "source": {"label": "현재 시각 의미 데이터", "files": [{"label": "current-snapshot.json"}, {"label": "current-distribution.json"}], "metricDefinitions": [{"label": "프로필 수", "definition": "현재 프로필 수는 실제 로더가 읽은 시각 프로필의 수이며, 심층 조사 대상은 두 목표에 맞춰 선택한 기존 프로필이다."}], "filters": ["심층 표본은 기존 12개 개념군의 15개 프로필이다."], "caveats": ["프로필 수는 서로 다른 의미 수나 사용자 수요 비중이 아니다.", "심층 표본은 무작위가 아니므로 전체 데이터의 결함률을 추정하지 않는다."]}, "capturedAt": snapshot["captured_at"], "columns": [{"field": "population", "label": "대상"}, {"field": "count", "label": "프로필 수"}], "rows": [{"population": "현재 로더 전체", "count": snapshot["loaded_profile_count"]}, {"population": "심층 조사", "count": len(snapshot["selected_profiles"])}], "methods": [{"language": "python", "code": count_method}]}]},
    {"id": "neutral-anchor-contract", "title": "중립 구조 문장 5개의 증거 조건 비교", "queries": [{"id": "binding-fixtures", "source": {"label": "현재 조건과 데이터 초안", "files": [{"label": "validation-results.json"}, {"label": "verify_plan.py"}, {"label": "profile-change-plan.json"}], "metricDefinitions": [{"label": "증거 문장 검사", "definition": "증거 문장 검사는 카울·메시·앞판 잠금과 원단 투과의 5개 문장을 기존 문자열 앵커 및 변경 초안과 대조한다."}], "caveats": ["메모리 안의 초안 검사이며 실제 데이터에는 반영하지 않았다.", "현재 조건은 5개 문장을 거절했고 초안은 받아들였지만 검색·LLM·이미지의 성공률을 측정하지 않았다."]}, "capturedAt": validation["checked_at"], "columns": [{"field": "profile", "label": "프로필"}, {"field": "field", "label": "증거 필드"}, {"field": "before", "label": "현재 조건"}, {"field": "draft", "label": "데이터 초안"}], "rows": [{"profile": r["profile_id"], "field": r["field"], "before": "앵커 부족으로 거절", "draft": "로컬 증거 조건 수용"} for r in validation["local_anchor_fixtures"]], "methods": [{"language": "python", "code": check_method}]}]},
    {"id": "staged-data-integration", "title": "의미 범위·구조 조건·캐릭터 범위의 반영 순서", "queries": [{"id": "unapplied-stage-plan", "source": {"label": "데이터 반영 계획", "files": [{"label": "INTEGRATION-PLAN.md"}, {"label": "profile-change-plan.json"}, {"label": "character-scope-plan.json"}, {"label": "source-evidence.json"}], "links": [{"label": "원어 의미 도식", "href": "https://www2.ic.daito.ac.jp/jtogashi/articles/togashi2009a.pdf"}, {"label": "앞판 잠금 제작 도면", "href": "https://s3.eu-west-1.wasabisys.com/sewdirect/V1876_francais_english_ins.pdf"}], "metricDefinitions": [{"label": "반영 순서", "definition": "반영 순서는 10개 프로필의 의미·예문, 4개 프로필의 중립 구조·증거 조건, 쿨데레 프로필과 의미 그래프의 범위 정렬을 나누어 검토하는 계획이다."}], "caveats": ["반영 계획은 데이터·인덱스 갱신과 독립 검증을 포함하지만 스킬 로직 변경은 포함하지 않는다.", "용어 없는 표현은 안전성 통과를 보장하지 않으며 형상·차단·사용자 판단은 별도로 평가해야 한다."]}, "summary": "프로필 ID와 기존 필수 관계를 유지하면서 문맥 범위와 구조 문장의 대응을 보강하는 미적용 계획이다."}]}], "schemaVersion": 1}
(OUT / "sources-receipt-input.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
print("Reviewed Sources input saved")
