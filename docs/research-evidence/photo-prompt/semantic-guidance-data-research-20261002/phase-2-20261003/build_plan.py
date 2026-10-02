"""Build reviewable research artifacts. Never write production data or call models."""
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
PREVIOUS = OUT.parent / "phase-1"

def sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def read(name):
    return json.loads((OUT / name).read_text())

def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def at(value, path):
    for key in path.split("."):
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value

def set_at(value, path, replacement):
    parts = path.split(".")
    parent = value
    for key in parts[:-1]:
        if isinstance(parent, list): parent = parent[int(key)]
        else: parent = parent.setdefault(key, {})
    if isinstance(parent, list): parent[int(parts[-1])] = replacement
    else: parent[parts[-1]] = replacement

def draft_after(raw, operations):
    """Apply review operations only to an in-memory copy, with before-value guards."""
    result = copy.deepcopy(raw)
    for op in operations:
        try: before = at(result, op["path"])
        except KeyError: before = None
        assert before == op["before"], op["path"]
        if op["operation"] == "append_unique":
            after = copy.deepcopy(before or [])
            for item in op["values"]:
                if item not in after: after.append(copy.deepcopy(item))
        else:
            assert op["operation"] == "replace"
            after = copy.deepcopy(op["after"])
        set_at(result, op["path"], after)
    return result

def add_op(raw, ops, path, *, values=None, after=None):
    interim = draft_after(raw, ops)
    try: before = copy.deepcopy(at(interim, path))
    except KeyError: before = None
    op = {"operation": "append_unique" if values is not None else "replace", "path": path, "before": before}
    if values is not None: op["values"] = values
    else: op["after"] = after
    ops.append(op)

NEW_SOURCES = [
    {"id": "nikl-one-piece", "title": "한국어기초사전 원피스, 표제어 26721", "publisher": "국립국어원", "url": "https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=26721", "language": "ko", "access": "official_entry_read_in_browser", "locator": "표제어 정의, 원피스 수영복 용례, 투피스 참고어", "supports": ["기본 표제어는 윗옷과 치마가 연결된 의복이다.", "동일 항목에도 원피스 수영복이라는 복합어 용례가 있다."], "limits": ["영어 one-piece의 전체 의미나 작품명 의미를 이 항목만으로 확정하지 않는다.", "사전의 성별 용법을 착용자 성별에 관한 시각적 필수 조건으로 옮기지 않는다."], "access_note": "웹 추출 도구 접근 실패 후 사전 검색 UI에서 원문 확인. 세션 URL은 보관하지 않음."},
    {"id": "togashi-kuudere-pdf", "title": "ツンデレ属性と言語表現の関係", "publisher": "冨樫純一, author-hosted handout", "url": "https://www2.ic.daito.ac.jp/jtogashi/articles/togashi2009a.pdf", "language": "ja", "access": "pdf_download_text_and_page_render_read", "locator": "PDF p.2 본문 도식과 각주 3", "supports": ["바깥 표현과 안쪽 특별한 감정을 구분하는 관계 도식이다.", "각주에서 외면의 츤츤을 쿨로 바꾸어 쿨데레에 적용한다."], "limits": ["실용적 도움, 젖은 소매, 도구 전달은 원문의 필수 정의가 아니다.", "모든 현대 용례나 외모·성별·연령의 보편 기준을 확정하지 않는다."], "pdf_id": "togashi2009a"},
    {"id": "flight-kuudere-pdf", "title": "ときドキ時計 CVシリーズ official release", "publisher": "FLIGHT", "url": "https://www.flight.co.jp/uploaded_files/c_news/106_detail.pdf", "language": "ja", "access": "pdf_download_page_render_read", "locator": "PDF p.2 캐릭터 설명, p.3 각주 1", "supports": ["차분한 겉모습과 특정 상대에게 드러나는 친근함을 함께 기술한다.", "시간에 따라 마음을 열어가는 표현도 한 용례로 제시한다."], "limits": ["작품 캐릭터의 머리색·의상·학교 맥락은 성인 사진 데이터에 상속하지 않는다.", "해당 상품의 여성·남성 관계 설명을 모든 쿨데레의 정의로 일반화하지 않는다."], "pdf_id": "flight106"},
    {"id": "vogue-busk-instructions", "title": "Vogue Patterns V1876 English/Français instructions", "publisher": "Vogue Patterns / Sewdirect", "url": "https://s3.eu-west-1.wasabisys.com/sewdirect/V1876_francais_english_ins.pdf", "language": "en/fr", "access": "pdf_download_text_and_page_render_read", "locator": "PDF p.3, Front and Back Closures, steps 19–26", "supports": ["고리 부분과 돌기 부분을 서로 맞는 앞판 가장자리에 배치한다.", "두 앞판 경계의 결합과 고리·돌기의 대응 위치가 제작 도면에 보인다."], "limits": ["모든 코르셋이 이 잠금 형식을 가지는 것은 아니다.", "특정 상품의 훅 수, 좌우 배치, 컵·언더와이어·봉제 순서는 일반 시각 조건으로 확장하지 않는다."], "pdf_id": "vogue1876"},
    {"id": "simplicity-one-shoulder", "title": "Simplicity S3165 one-shoulder dress", "publisher": "Simplicity / Sewdirect", "url": "https://www.sewdirect.com/product/simplicity-s3165/", "language": "en", "access": "product_text_and_browser_line_art_read", "locator": "About this product; Line art views A/B/C, front/back", "supports": ["한쪽 어깨를 잇는 의복 경계가 앞뒤 도식에 나타난다.", "장식 리본이 있는 버전과 없는 버전, 여러 길이를 함께 제시한다."], "limits": ["리본·바이어스 재단·사이드 지퍼·기장은 해당 상품의 변형이며 원숄더 전체의 필수 조건이 아니다.", "일반 사진의 드레이프만으로 바이어스 재단을 증명하지 않는다."]},
    {"id": "heathcoat-tulle-variants", "title": "Flare Free looking bright!", "publisher": "Heathcoat Fabrics", "url": "https://www.heathcoat.co.uk/new-colours-for-flare-free-tulle/", "language": "en", "access": "primary_article_text_read_earlier_in_turn", "locator": "English tulle/dress nets range; construction, weights, handle, sparkle/matte options", "supports": ["제조사 제품군에 조직·무게·촉감·표면 마감의 변형이 존재한다."], "limits": ["모든 튤을 육각형·흰색·같은 굵기나 소재로 고정하는 근거가 아니다.", "직물의 안전성 규정이나 섬유 조성을 이미지로 판단하는 근거로 사용하지 않는다."], "access_note": "첫 본문/색인 읽기는 성공했으나 뒤이은 재열기는 시간 초과. 형태 도식은 별도로 관찰하지 않음."},
    {"id": "schneider-diopter-types", "title": "Diopters: Full, Split, Spot", "publisher": "Schneider-Kreuznach", "url": "https://schneiderkreuznach.com/en/cine-optics/filters/cine-filters/diopters", "language": "en", "access": "primary_article_text_read", "locator": "Diopter Split/Spot descriptions and Filters in Use captions", "supports": ["스플릿 방식은 앞뒤 두 영역을 동시에 초점에 두는 관계이다.", "스폿 방식의 중앙 선명·가장자리 흐림과 구분한다."], "limits": ["흐린 경계가 모든 스플릿 사진에서 반드시 드러난다고 말하지 않는다.", "캡션을 읽었으며 이 단계에서 해당 예제 픽셀을 직접 검토하지 않았다.", "생성 이미지의 두 초점 영역만으로 실제 광학 장비나 제작 방법을 증명하지 않는다."]},
    {"id": "dehancer-halation", "title": "Halation tool documentation", "publisher": "Dehancer", "url": "https://www.dehancer.com/learn/article/halation", "language": "en", "access": "primary_tool_documentation_read", "locator": "Local Diffusion, Global Diffusion, Hue, Halation + Bloom", "supports": ["이 디지털 시뮬레이션은 국소 후광과 2차 확산, 색상 변형을 구분한다.", "개발사는 할레이션과 블룸을 함께 사용하는 시뮬레이션도 설명한다."], "limits": ["디지털 제품 설명을 모든 실제 필름의 물리적 정의로 일반화하지 않는다.", "전역 번짐만 있는 장면을 국소 경계 후광의 증거로 인정하는 근거가 아니다."]},
    {"id": "profoto-face-light-detail", "title": "John Russo reveals his character portrait lighting secrets", "publisher": "Profoto", "url": "https://www.profoto.com/lv/en/still-photography/profoto-stories/character-portraits-with-john-russo-and-profoto-d2", "language": "en", "access": "primary_article_text_read", "locator": "Patterns of light / Classic covers: Short light, Broad light", "supports": ["카메라 가까운 얼굴 면이 더 어두우면 쇼트, 더 밝으면 브로드라는 관계를 설명한다.", "조명을 그대로 두고 인물을 움직여 조명 패턴을 바꾼 사례를 제시한다."], "limits": ["고정된 화면 왼쪽·오른쪽 또는 특정 얼굴형의 아름다움을 보편 조건으로 삼지 않는다.", "예시 사진 픽셀을 이 단계에서 별도로 검사하지 않았다."]},
]

NEUTRAL = {
    "clothing_ct037_v1": {
        "en": "the garment opening at the neck hangs in loose folds of the same continuous fabric",
        "ko": "같은 의복의 목 둘레 개구부가 연속된 천의 느슨한 접힘으로 늘어진다",
        "source": "met-cowl",
    },
    "clothing_ct090_v2": {
        "en": "fine threads form an evenly spaced network of actual open cells in the garment fabric",
        "ko": "의복의 가는 실들이 일정한 간격을 유지하며 실제로 열린 셀 조직을 이룬다",
        "source": "cotton-mesh",
    },
    "clothing_ct023_v2": {
        "en": "a fitted paneled bodice has two center-front edges joined by a vertical row of metal loops engaging matching studs",
        "ko": "몸에 맞춘 패널 상의의 중앙 앞판 양쪽 가장자리가 세로로 대응하는 금속 고리와 돌기의 맞물림으로 연결된다",
        "source": "vogue-busk-instructions",
    },
}

EXTRA_SOURCES = {
    "one_piece_dress_construction": ["nikl-one-piece", "simplicity-one-shoulder"],
    "kuudere_composed_warmth_relation": ["togashi-kuudere-pdf", "flight-kuudere-pdf"],
    "clothing_ct023_v2": ["vogue-busk-instructions"],
    "clothing_ct090_v2": ["heathcoat-tulle-variants"],
    "pfe_one_shoulder": ["simplicity-one-shoulder"],
    "split_diopter_dual_focus_planes": ["schneider-diopter-types"],
    "film_halation_highlight_edge_relation": ["dehancer-halation"],
    "broad_face_light_orientation_relation": ["profoto-face-light-detail"],
    "short_face_light_orientation_relation": ["profoto-face-light-detail"],
}

SCOPE_LIMITS = {
    "aircraft_pilot_operation": "항공기 운항 관계를 보이는 선택 프로필이다. 휴식 중인 조종사 인물 사진이나 조종사라는 직업 전체를 같은 필수 관계로 평가하지 않는다.",
    "one_piece_dress_construction": "한국어 원피스 기본 표제어의 드레스 구조를 다룬다. 원피스 수영복, 영어 one-piece 일반 의복, 작품명은 문맥이 다른 뜻으로 분리한다.",
    "embodied_corruption_transition": "몸 위에서 진행 중인 상태 경계는 이 프로필의 선택 연출이다. 윤리적 타락, 진영 변경, 어두운 분위기 전체의 보편 정의가 아니다.",
    "kuudere_composed_warmth_relation": "원어의 차분한 외면과 선택적 친근함을 한 성인 장면으로 표현하는 데이터다. 실용적 도움과 같은 상대의 가시 결과는 이 프로필의 연출 조건이며 모든 쿨데레의 어휘 정의가 아니다.",
    "pfe_cowl": "이 항목에서 제외한 두꺼운 니트 카울이나 후드는 다른 카울 용례이다. 그 자체가 잘못된 의복이라는 뜻은 아니다.",
    "clothing_ct037_v1": "같은 의복의 목 개구부에 연결된 느슨한 접힘을 선택한 프로필이다. 별도 스카프, 후드, 세워진 두꺼운 칼라와 구별한다.",
    "pfe_one_shoulder": "연결되는 어깨 수를 평가한다. 끈의 조각 수, 장식 리본 유무, 앞뒤 도식의 화면 좌우는 같은 개념의 필수 기준이 아니다.",
    "pfe_ruching": "국소적인 천 모임과 그 소유 경계를 보인다. 사진의 모든 주름을 동일한 봉제 방법의 증거로 보지 않으며 셔링·스모킹의 시각적 유사성을 인정한다.",
    "clothing_ct090_v2": "가는 실과 실제 열린 셀의 규칙적 간격을 선택한 프로필이다. 셀의 육각형 모양, 흰색, 꽃무늬, 섬유 조성이나 뒤쪽 신체 노출을 자동으로 추가하지 않는다.",
    "clothing_ct023_v2": "고리와 돌기가 맞물리는 중앙 앞판 잠금 변형이다. 모든 코르셋이 이런 잠금이 있는 것은 아니며 체형의 잘록함을 잠금 구조의 증거로 쓰지 않는다.",
    "split_diopter_dual_focus_planes": "이 프로필의 완충 흐림 영역은 선택한 장면 조건이다. 스플릿 광학 장비 전체의 필수 가시 결함으로 일반화하지 않는다.",
    "film_halation_highlight_edge_relation": "이 프로필은 따뜻한 국소 경계 후광을 선택한다. 블룸과 동시에 존재할 수 있으나 블룸만으로 국소 경계 후광 조건을 충족하지 않는다.",
    "broad_face_light_orientation_relation": "카메라·얼굴 회전·밝은 면의 상대 관계를 평가한다. 화면을 좌우 반전해도 관계는 보존될 수 있으며 특정 성별이나 얼굴형의 미적 우열을 뜻하지 않는다.",
    "short_face_light_orientation_relation": "카메라·얼굴 회전·그늘 면의 상대 관계를 평가한다. 조명의 화면 왼쪽·오른쪽만으로 이 패턴을 결정하지 않는다.",
    "sheer_garment_optical_layering": "원단 섬유층과 요청한 아래 표면의 투과 관계를 함께 유지한다. 신체, 아래 의복, 배경 중 실제 요청된 대상을 유지하고 임의의 불투명 덮개를 추가하지 않는다. 적용 가능한 성인·콘텐츠 제약과 요청한 피복 범위는 별도로 유지한다.",
}

# Each row is one project-authored development minimal pair, not a tested retrieval result.
PAIRS = [
    ("pilot-aircraft", "항공기 조종석에서 체크리스트와 계기를 확인하며 비행 단계에 맞게 조작하는 성인", "파일럿이 공항 카페에서 쉬는 인물 사진", "An adult at an aircraft control station checks a checklist and instruments consistent with the flight phase.", "A pilot rests in an airport cafe in a portrait.", "운항 장면과 직업 인물 사진"),
    ("dress-one-unit", "의복 윗부분과 치마가 허리 연결을 통해 한 벌을 이루는 성인의 드레스", "성인이 착용한 원피스 수영복", "An adult's dress has a bodice joined to a skirt in one continuous garment.", "An adult wears a one-piece swimsuit.", "복합어가 기본 드레스 의미를 바꿈"),
    ("character-transition", "성인 허구 인물의 옛 표식이 남아 있고 손목에서 몸으로 번지는 경계와 진행 중인 선택이 보인다", "성인 허구 인물이 신념을 바꾸었으나 신체와 복장은 그대로다", "An adult fictional character retains an old emblem while an unfinished boundary spreads from the wrist with a visible choice.", "An adult fictional character changes allegiance while the body and clothing remain unchanged.", "일반 서사 개념과 선택한 신체 경계 연출"),
    ("reserved-help", "담담한 성인이 같은 성인 동료에게 필요한 도구를 건네고 그 동료가 안도할 때 눈가만 조금 풀린다", "담담한 성인이 특정 성인 동료를 떠올리며 작은 미소를 짓지만 도움 행동은 없다", "A composed adult gives a needed tool to the same adult coworker and the eyes soften slightly as the coworker visibly relaxes.", "A composed adult gives a small smile while thinking of one adult coworker, with no helpful action.", "두 장면 모두 일반 친근함 용례가 될 수 있으나 현 프로필은 도움 관계를 선택함"),
    ("cowl-draped-opening", "의복 목선에 연결된 같은 천이 느슨하게 내려와 접힘을 만든다", "의복 목선 위에 별도 스카프를 얹는다", "The garment's own neckline fabric hangs in loose connected folds.", "A separate scarf rests over the garment's neckline.", "같은 천의 부착과 별도 물건의 소유권"),
    ("single-shoulder-support", "앞뒤 패널이 같은 한쪽 어깨를 지나 연결되며 반대 어깨는 의복 연결에서 열린다", "한 끈이 두 갈래로 갈라져 양쪽 어깨를 각각 지난다", "Front and back panels connect over the same single shoulder; the other shoulder stays open in the garment structure.", "One strap divides into two branches that cross two different shoulders.", "끈 수가 아닌 연결되는 어깨 수"),
    ("local-gathered-folds", "같은 천이 의복의 옆 솔기에서 조밀하게 모이고 주변 패널로 접힘이 이어진다", "매끈한 천에 조밀한 주름처럼 보이는 선무늬가 인쇄되어 있다", "The same garment fabric gathers tightly at a side seam and its folds continue into the adjoining panel.", "Lines resembling tight folds are printed on otherwise smooth cloth.", "입체 천 모임과 인쇄 표면"),
    ("textile-transmission", "보이는 섬유층 뒤의 성인 신체 윤곽이 같은 원단을 통해 부분적으로 겹쳐 읽힌다", "불투명 의복은 그대로인데 성인 신체가 유리처럼 투명해 보인다", "The requested adult body's contours are partly readable beneath a visible transmitting garment fiber layer.", "The garment remains opaque while the adult body appears transparent like glass.", "원단 투과의 소유자와 투명 신체 오류"),
    ("fine-open-cells", "가는 실들 사이의 열린 공간을 통해 뒤쪽 표면이 보이는 일정한 셀 조직", "불투명 천 위에 그물 무늬가 인쇄되어 있다", "A regular cell network has actual openings between fine threads through which the background surface is visible.", "A grid pattern is printed on opaque cloth.", "실제 열린 셀과 도안"),
    ("paired-front-fastening", "패널 상의의 중앙 앞판 양쪽에 있는 고리와 돌기가 세로로 맞물려 두 경계를 닫는다", "패널 상의 앞판 한쪽에 금속 돌기 장식만 늘어서 있다", "Metal loops and matching studs engage vertically across the paneled bodice's two center-front edges.", "Decorative metal studs line only one front panel of the bodice.", "맞물림과 장식"),
    ("separated-focus-zones", "앞의 손과 뒤의 인물이 서로 떨어진 깊이에서 또렷하며 그 사이의 깊이는 부드럽게 흐리다", "한 장면 전체가 같은 정도로 선명한 심도 깊은 사진", "A foreground hand and distant person occupy distinct sharp zones with a softer intervening depth.", "Every depth in the scene is equally sharp in a deep-focus photograph.", "선택한 두 초점 영역과 장면 전체 선명"),
    ("warm-highlight-halo", "밝은 창틀과 어두운 벽의 경계를 따라 얇은 따뜻한 후광이 있고 장면 전체에는 약한 블룸도 있다", "경계 후광 없이 장면 전체에 균일한 블룸만 있다", "A thin warm halo follows the bright window edge against a dark wall while mild bloom also fills the scene.", "Uniform scene-wide bloom appears with no local edge halo.", "효과 공존과 대체"),
    ("broad-cheek-lit", "돌아선 얼굴에서 카메라에 넓게 보이는 볼 면이 더 밝고 좁게 보이는 볼 면이 그늘에 있다", "화면 왼쪽 조명만 밝고 얼굴은 완전히 정면이라 두 볼의 보이는 폭이 같다", "On a turned face, the wider camera-facing cheek plane is brighter and the narrower plane is shaded.", "A screen-left lamp is bright but the face is frontal and both cheek planes show equal width.", "상대 기하와 고정 좌우 규칙"),
    ("short-cheek-lit", "돌아선 얼굴에서 카메라에 넓게 보이는 볼은 그늘이고 반대의 좁게 보이는 볼이 더 밝다", "카메라에 넓게 보이는 볼이 밝고 좁게 보이는 볼은 그늘에 있다", "On a turned face, the wider camera-facing cheek is shaded and the narrower far cheek is brighter.", "The wider camera-facing cheek is brighter and the narrower far cheek is shaded.", "쇼트와 브로드의 관계 역전"),
]

def main():
    snapshot = read("current-snapshot.json")
    previous = json.loads((PREVIOUS / "profile-data-proposals.json").read_text())
    cards = json.loads((PREVIOUS / "concept-cards.json").read_text())["cards"]
    if (OUT / "source-evidence.json").exists():
        # Rebuilding drafts is not a fresh source read. Preserve original access evidence.
        sources = read("source-evidence.json")["items"]
    else:
        receipts = json.loads((ROOT / "tmp/pdfs/semantic-data-research-20261003/download-receipt.json").read_text())
        downloads = {x["id"]: x for x in receipts}
        sources = copy.deepcopy(NEW_SOURCES)
        for row in sources:
            row["checked_at"] = datetime.now(timezone.utc).isoformat()
            row["source_type"] = "primary"
            row["reuse"] = "Store own paraphrase, URL, locator and access evidence; do not redistribute full source PDFs or product images."
            if row.get("pdf_id"): row["download_evidence"] = downloads[row["pdf_id"]]
        write("source-evidence.json", {"schema_version": 1, "items": sources, "previous_sources": "../phase-1/sources.json", "source_counts_are_not_model_validation": True})

    plans = []
    for earlier in previous["proposals"]:
        pid = earlier["profile_id"]
        raw = snapshot["raw_owners"][pid]["raw_profile"]
        ops = []
        for op in earlier["operations"]:
            assert op["operation"] == "append_unique"
            add_op(raw, ops, op["path"], values=op["values"])
        add_op(raw, ops, "semantics.claim_limits", values=[SCOPE_LIMITS[pid]])
        stage = "A_scope_and_examples"
        if pid in NEUTRAL:
            stage = "B_neutral_structural_contracts"
            neutral = NEUTRAL[pid]
            add_op(raw, ops, "semantics.definition", after=neutral["en"])
            add_op(raw, ops, "semantics.paraphrase_examples", values=[neutral["ko"], neutral["en"]])
            add_op(raw, ops, "semantics.visual_components", values=[neutral["en"]])
            add_op(raw, ops, "authored_components.components.0.match_terms", values=[neutral["en"], neutral["ko"]])
            add_op(raw, ops, "authored_components.components.0.evidence_terms", values=[neutral["en"]])
            add_op(raw, ops, "authored_components.components.0.instruction", after="Realize this selected visible structure on the requested garment: " + neutral["en"] + ". Preserve its stated owner and connection.")
            add_op(raw, ops, "authored_components.components.0.render_gate.description", after=neutral["en"] + ". Inspect this same garment, its real boundaries and connections at native resolution. A nearby object, printed imitation, missing connection or occluded required detail fails.")
        elif pid == "sheer_garment_optical_layering":
            stage = "B_neutral_structural_contracts"
            add_op(raw, ops, "semantics.definition", after="A garment textile remains visibly present through fibers or open-cell structure, seams, edges, folds and surface diffusion while light and the requested underlying surface are partly transmitted through the same cloth; folds, stretch, viewing angle and illumination change transmission coherently.")
            add_op(raw, ops, "composition_instruction", after="Make the garment textile visibly present through its fibers or open-cell structure, seams, edges and folds. Let light reveal the requested underlying body, lower garment or background through that same textile, preserving the requested coverage and actual layer owner. Choose one material and one lighting relationship; retain coherent transmission and visible material boundaries.")
            add_op(raw, ops, "evidence_requirements.translucent_textile_phrase.must_mention_any", values=["a garment textile layer that partially transmits the view behind it"])
            add_op(raw, ops, "evidence_requirements.layer_contrast_phrase.must_mention_any", values=["underlying body contours remain partly visible beneath the readable garment fibers", "the requested lower garment remains partly visible beneath the transmitting textile", "the background remains partly visible through the same garment panel"])
            gate = copy.deepcopy(raw["render_gates"])
            gate[2]["description"] = "Light and the requested underlying body, lower garment or background are partly transmitted through the same visible garment textile in a coherent direction. The transmitting layer and underlying owner must remain distinct; an unrequested opaque covering cannot replace the intended lower surface."
            add_op(raw, ops, "render_gates", after=gate)
            add_op(raw, ops, "activation.context_disambiguation.any_terms", values=["underlying body visible through garment fibers", "의복 섬유층을 통해 부분적으로 보이는 아래 신체"])
        elif pid == "kuudere_composed_warmth_relation":
            stage = "C_character_scope_alignment"
            add_op(raw, ops, "semantics.definition", after="General contextual meaning combines a composed, restrained outward surface with selective positive affiliation toward a particular counterpart. This profile selects one adult fictional still-image realization: stable composure, a localized warmth cue, a quiet practical action and an already-visible helpful consequence for that same trusted adult counterpart. The selected action is an operational cue rather than a universal definition of the archetype; appearance alone is insufficient evidence.")
        after = draft_after(raw, ops)
        plans.append({
            "profile_id": pid, "card_id": earlier["card_id"], "stage": stage,
            "status": "NOT_APPLIED_DATA_ONLY_REVIEW_DRAFT",
            "source_file": snapshot["raw_owners"][pid]["path"],
            "source_file_sha256": snapshot["protected_file_sha256"][snapshot["raw_owners"][pid]["path"]],
            "before_raw_profile_sha256": sha(raw), "after_raw_profile_sha256": sha(after),
            "source_ids": list(dict.fromkeys(earlier["source_ids"] + EXTRA_SOURCES.get(pid, []))),
            "operations": ops,
            "preserved_contracts": ["profile ID", "gate IDs and review scales", "required evidence field names", "component group count and IDs", "minimum content-word thresholds", "runtime expression mode", "exact terms and hard activation groups"],
            "activation_note": "Only the sheer profile adds two specific context-disambiguation phrases. No draft synonym is promoted into exact/hard activation.",
            "validation_boundary": "Before/after binding and compilation checks are local contract checks. Semantic correctness, retrieval performance, LLM behavior and pixels need separate evaluation.",
        })
    write("profile-change-plan.json", {"schema_version": 1, "baseline_head": snapshot["git_head"], "baseline_capture": snapshot["captured_at"], "status": "NOT_APPLIED", "production_apply_script": False, "plans": plans})

    graph_path = "skills/photo-prompt-image-generator/assets/photo_prompt_character_moe_extension.json"
    graph = json.loads((ROOT / graph_path).read_text())
    old = next(x for x in graph["character_mechanism_graph"]["concept_profiles"] if x["id"] == "kuudere")
    graph_ops = []
    for path, replacement in {
        "definition": "General contextual meaning is a composed outward surface coexisting with selective positive affiliation toward a particular counterpart. This dataset selects one operational realization of that relation: stable emotional reserve, one localized warmth cue and a quiet target-directed supportive act with a visible consequence for the same counterpart. The support action and consequence are the selected cue scheme, not universal lexical requirements; hair, eyes, wardrobe, gender, occupation and attractiveness do not establish the concept.",
        "en": "selective relational warmth beneath a composed low-expression surface; this dataset selects quiet same-target support and a visible response",
        "ko": "침착한 외면과 특정 상대를 향한 친근함이 공존하는 개념; 이 데이터는 같은 상대를 위한 조용한 도움과 가시 반응의 연출을 선택한다",
        "ja": "平静な外面と特定の相手への親しさが同居する概念。このデータでは同じ相手への静かな支援と可視の反応で表す一つの実現形を扱う",
    }.items(): add_op(old, graph_ops, path, after=replacement)
    write("character-scope-plan.json", {"status": "NOT_APPLIED", "source_file": graph_path, "source_file_sha256": snapshot["protected_file_sha256"][graph_path], "record_path": "character_mechanism_graph.concept_profiles[id=kuudere]", "before_sha256": sha(old), "after_sha256": sha(draft_after(old, graph_ops)), "operations": graph_ops, "preserved": ["aliases", "axis requirements/exclusions", "required relations", "evidence roles", "optional runtime nodes", "applicability"], "limit": "This clarifies common meaning versus the selected cue scheme. It does not make all possible kuudere scenes satisfy the existing runtime contract. Alternate realization records require a separate data design and independent examples."})

    case_rows = []
    by_card = {c["id"]: c for c in cards}
    for cid, pos_ko, neg_ko, pos_en, neg_en, rationale in PAIRS:
        card = by_card[cid]
        source_ids = list(dict.fromkeys(card["source_ids"] + [s for pid in card["profile_ids"] for s in EXTRA_SOURCES.get(pid, [])]))
        case_rows.append({"id": cid + "-minimal-pair-01", "card_id": cid, "profile_ids": card["profile_ids"], "positive": {"ko": pos_ko, "en": pos_en}, "contrast": {"ko": neg_ko, "en": neg_en}, "expected_scope": {"positive": "matches_selected_visual_scope", "contrast": "outside_selected_scope_not_necessarily_wrong_dictionary_meaning"}, "rationale_ko": rationale, "source_ids": source_ids, "status": "PROJECT_AUTHORED_DEVELOPMENT_PAIR_NOT_MODEL_EVALUATED"})
    (OUT / "semantic-minimal-pairs.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in case_rows) + "\n")
    write("reference-observations.json", {"scope": "Own textual observations only; no source images or full PDFs redistributed.", "items": [
        {"source_id": "vogue-busk-instructions", "method": "PDF p.3 rendered with pdftoppm, viewed at 1600px", "observation": "Steps 19/26 place the matching hook and stud sections on two center-front edges; diagrams show paired engagement and separate front/back closures.", "not_inferred": ["universal hook count or side", "wearer body shape", "real load-bearing function in an image"]},
        {"source_id": "simplicity-one-shoulder", "method": "Ordinary in-page browser view of Line art front/back A/B/C", "observation": "Each view connects front/back over one corresponding shoulder. A/B add a bow; C omits it. Front/back screen sides differ because view direction changes.", "not_inferred": ["mandatory bow or length", "bias-cut evidence from arbitrary photos", "number of all textile strips equals shoulder count"]},
        {"source_id": "togashi-kuudere-pdf", "method": "PDF p.2 text extraction and rendered page inspection", "observation": "Body diagram separates outward expression and inward affiliation; footnote 3 applies a cool outward component to kuudere.", "not_inferred": ["mandatory help action", "gender", "fixed physical appearance"]},
        {"source_id": "flight-kuudere-pdf", "method": "PDF pp.2/3 rendered page inspection after unusable text extraction", "observation": "Footnote 1 discusses cool outward presentation with special warmth toward a particular counterpart; the specific character illustration is not reused in adult photographic data.", "not_inferred": ["universal hairstyle", "school context as adult data", "universal practical-help scene"]},
    ], "previous": "../phase-1/reference-observations.json"})

    baseline = json.loads((PREVIOUS / "source-snapshot.json").read_text())
    differences = []
    for row in baseline["profiles"]:
        old = row["profile"]; now = snapshot["selected_profiles"][old["id"]]
        if old != now:
            changed = []
            def walk(a, b, path=""):
                if isinstance(a, dict) and isinstance(b, dict):
                    for key in sorted(set(a) | set(b)): walk(a.get(key), b.get(key), path + "." + key)
                elif a != b: changed.append({"path": path.lstrip("."), "before": a, "current": b})
            walk(old, now)
            differences.append({"profile_id": old["id"], "changes": changed})
    write("baseline-drift.json", {"previous_loaded_profile_count": baseline["loaded_profile_count"], "current_loaded_profile_count": snapshot["loaded_profile_count"], "net_change": snapshot["loaded_profile_count"] - baseline["loaded_profile_count"], "selected_profile_differences": differences, "policy": "Rebase proposals on current raw profile and protected source hashes. Never restore phase-1 whole files over unrelated edits."})
    print(json.dumps({"profile_plans": len(plans), "graph_plans": 1, "source_receipts": len(sources), "minimal_pairs": len(case_rows), "language_utterances": len(case_rows) * 4, "stages": {s: sum(r["stage"] == s for r in plans) for s in sorted({r["stage"] for r in plans})}, "selected_drift": len(differences)}))

if __name__ == "__main__": main()
