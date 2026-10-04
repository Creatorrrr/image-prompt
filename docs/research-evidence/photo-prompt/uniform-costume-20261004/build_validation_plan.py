"""Save future acceptance cases and isolated illustrative runtime drafts."""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Positive request | nearby negative request | what must stay different
CASES = r"""
U01|황색 몸판과 진동부터 붉은 소매가 이어진 동다리|소매도 몸판과 같은 단색 긴 코트|몸판과 소매의 부착 경계가 없으면 배색 관계를 충족하지 않음
U02|긴 민소매 전복을 붉은 긴 소매 옷 위에 입었다|접시 위의 전복 요리|의복 문맥과 식재료 동음이의어를 분리
U03|철릭의 상의와 주름 하의가 허리 접합선에서 이어진다|긴 코트 아래 별도의 플리츠 치마|한 의복의 허리 연결과 두 의복의 겹침을 분리
U04|확인된 유물 버전의 철릭 소매 탈착 경계|일반 철릭 전신 사진|특수 소매 버전을 일반 철릭에 자동 활성화하지 않음
U06|펠리스를 한쪽 어깨에 걸쳐 빈 소매가 내려온다|모피 재킷의 양팔 소매에 팔을 끼운다|빈 소매와 실제 착용 소매를 구분
U07|네 모서리 윗판과 아래 챙이 있는 차프카|둥근 원통 샤코|윗판의 각진 외곽과 별도 챙이 모두 보여야 함
U09|1863~66 Keystone Zouaves 재킷의 가짜 조끼 앞판|열린 재킷 속에 독립된 조끼를 입었다|붙은 패널과 독립 의복의 소유/층을 구분
U11|Scots Guards 버전의 적색 튜닉과 베어스킨|다른 근위 연대의 의장복|모든 연대에 세 단추 묶음 또는 깃털 없음 강제 금지
U14|박물관 사례에 맞춘 역사 SS 표식의 부착 위치|표식 없는 검정 패션 재킷|색만으로 조직 hard match 금지; 명시 역사 표식을 임의 문양으로 바꾸지 않음
U15|녹색 코트·탠 셔츠·토프 바지의 AGSU 구성|청색 코트와 흰 셔츠의 ASU|부품별 배색과 버전 ID 혼합 금지
U16|확인한 계급의 ASU 바지 장식|계급이 지정되지 않은 ASU 제복|금색 브레이드를 모든 계급의 필수로 만들지 않음
U17|앞 여밈 옆에 실제 주머니가 붙은 전투복|카모 무늬만 프린트된 평범한 셔츠|무늬로 주머니·여밈 증거를 대체하지 않음
U18|M42 가을면 스모크를 선택했다|M42 봄면 스모크를 선택했다|한 화면의 외피에 두 계절 면을 동시에 required로 넣지 않음
U19|성인 모델이 세일러 칼라가 있는 무대 의복을 입었다|미성년 학생이 일반 학교 교복을 입었다|같은 칼라의 재사용이 연령·역할·성적 맥락의 전이를 허용하지 않음
U20|1859 청색 프록의 청색 깃과 커프스|1841형 흰 덧깃·커프스 프록|시대 차이를 보존; 가린 커프스는 PASS가 아닌 UNOBSERVABLE
U22|노퍽 코트·벨트·긴 스커트의 Yeoman (F) 연구 버전|짧은 세일러 원피스|노퍽 주름과 벨트의 부착 관계를 미니 의복으로 대체하지 않음
U23|청색 직물 NASA 훈련복|헬멧·바이저가 목 연결부에 붙은 청색 압력복|색상 동일성으로 구조와 용도를 합치지 않음
U24|항공사가 지정되지 않은 조종사 셔츠|항공사·계급·견장 줄 수가 명시된 조종사복|전자의 네 줄 견장·흰 모자·윙 배지 자동 부과 금지
U26|스위스 일반 삼색 갈라복|황흑 배색의 고수 버전|군악 배색과 일반 배색은 대안
U27|흉갑과 러프를 추가한 스위스 대례복|청색 훈련복|직물 훈련 버전에 흉갑·러프·모리온 자동 추가 금지
U29|궁정 일상복으로 지정된 검정 코트·적색 조끼|확인된 대례복 배색|미확인 일상 배색을 대례 근거로 승인하지 않음
U31|1829 톱햇·테일코트의 런던 경찰 연구 버전|1863 이후 헬멧·튜닉 버전|시대 혼합 금지
U32|RCMP 의례용 레드서지|RCMP의 일상 근무복|역할이 같아도 의례 외피를 일상 기본값으로 강제하지 않음
U33|경찰 제복을 입은 정적인 성인 인물|교통을 통제하는 성인 경찰관|직업명만 있을 때 public-safety 동작 profile이 hard 활성화되지 않음
U34|재킷에 봉제된 반사 띠가 조명에 반응한다|평평한 노란 장식띠|기능 재질이나 인증을 추론하지 않고 관찰되는 광학 반응만 검증
U35|소방서 내 근무복을 입은 성인|공기호흡기를 점검하고 호스를 연결하는 성인 소방관|서내 복장만으로 PPE·진압 동작 profile 추가 금지
U38|회색 스웨트셔츠·바지의 교정복 사례|주황 일체형 촬영 소품|유물·촬영 소품과 실제 규정의 출처 종류를 보존
U39|합성 전시 구성으로 기록된 역사 간호복|한 벌의 원본 유물이라고 요청된 착장|합성 전시를 원본으로 확정하지 않음
U40|스크럽을 입은 성인 모델의 초상|환자 식별·활력 징후 확인을 수행하는 성인 간호사|의복만으로 임상 동작 profile 활성화 금지
U42|직물 후드와 얼굴 개구부가 있는 커버올|봉인된 헬멧 압력복|모양과 보호 성능을 분리; 소재·규격 없는 방호 인증 주장 금지
U43|머리의 수술모와 얼굴의 마스크|눈 부분의 검정 눈가리개|cap/mask/blindfold의 소유 부위와 경계를 구분
U44|JAL 1996 일반복 단일 앞섶|JAL 1996 책임자복 이중 앞섶|직급 대안을 한 재킷에 합치지 않음
U45|JAL 1970~77의 적색 벨트와 뒤지퍼|금색 앞단추 재킷을 입는 다른 시대|보이지 않는 뒤지퍼를 추론 PASS로 판정하지 않음
U46|머리 전체가 보이는 JAL 1996 모자 없는 버전|머리 윗부분이 크롭 밖인 동일 버전|후자의 모자 없음 gate는 UNOBSERVABLE이며 PASS가 아님
U47|목 스카프와 별도 머리 장식의 대한항공 2005 계열|하나의 목 장식이 머리까지 연결된 장식|소품 위치·귀속을 분리
U50|동일 재킷에 바지를 선택한 대한항공 버전|동일 재킷에 스커트를 선택한 버전|하의 대안을 한 착용자에게 모두 required로 만들지 않음
U49|SQ의 네 색 중 선택한 케바야|출처 확인 없는 색-직급 이름 대응표|색 존재와 직급 매핑 근거의 수준을 구분
U52|흰 앞치마를 겹친 무대 메이드복|실크 앞치마를 패션 액세서리로 착용|앞치마로 실제 가사/접객 행위를 추가하지 않음
U54|버니 레오타드와 인공 귀 머리 장식|실제 토끼 종 캐릭터|인공 귀가 종·신체 귀·성적 행동의 변경 권한을 만들지 않음
U55|c1925 무릎 길이 실제 maid 유물|긴 치마·앞치마만 가능한 메이드 고정 조합|실제 변이 사례를 허용하고 보편적 앞치마 필수 금지
U57|선 개수가 지정되지 않은 학교 세일러 칼라|학교별 선 수가 지정된 세일러 칼라|모든 학교에 세 줄을 강제하지 않음
U59|초란의 긴 재킷|탄란과 본탄의 짧은 재킷·넓은 바지|대안 재단과 품행/폭력 성격 추론을 분리
U60|학위·기관이 명시된 가운과 선택 모자|기관이 지정되지 않은 academic gown|사각모·탐모·후드를 동시에 넣지 않음
U62|수련자의 매듭 없는 허리끈|서원 후 세 매듭 사례|회색/갈색·수련/서원 축을 분리
U64|테두리 안의 직사각 가사 패치워크|무작위 직사각 프린트 코트|봉제 패치·테두리와 표면 프린트의 연결 증거를 구분
U65|흰 상의·붉은 하카마의 기본 미코복|치하야가 추가된 춤 버전|기본 버전에 겉옷·춤 동작 자동 추가 금지
U68|후기 DS9 회색 어깨·검은 몸판·부서색 목층|초기 DS9의 부서색 어깨·회색 목층|부품의 위치와 판본 색을 반대로 대체하지 않음
U69|공식 허가 복제품의 Wrath of Khan 코트|원 촬영복의 정확한 소재를 요구한 경우|복제품 설명을 원본 소재 증거로 바꾸지 않음
U71|흰 장갑판 아래 검은 보디글러브|검은 관절층이 없는 흰 로봇 몸체|원래 종·몸을 유지하고 판 사이 별도 층의 native gate 검증
U72|스노트루퍼 후드·벨트 아래 케이프|스카우트 또는 일반 스톰트루퍼|임무·판본별 장비를 모두 한 병사에 합치지 않음
U73|공식 Phase I 헬멧 도판이 확보된 요청|판본이 없는 clone trooper 요청|전자는 도판대로; 후자는 미확인 판본을 exact hard profile로 확정하지 않음
U74|공식 애니 2B 상체 크롭에서 관찰한 의복|게임판 9S·사령관·오퍼레이터 전신|크롭·캐릭터·매체 사이의 증거 전이 금지
U75|Half-Blood Prince 훈련 트랙수트|경기용 팔꿈치·무릎 보호대·헬멧|훈련과 경기의 추가 장비를 분리
U77|인터뷰 색인에서 확인한 의상 주제|전후면 디테일이 검증된 촬영복|색인·영상·실제 도판의 증거 수준을 구분
U78|명시적으로 선택한 성인 코르셋 장교 모티프|단순 군복이라는 요청|선택 전 코르셋·노출·성적 스타일 자동 부과 금지
U80|광택 제복의 하이라이트|발광 패널 경계의 자체 광원|반사와 발광을 서로 증거로 대체하지 않음
U81|군복 밑단의 국소 헤짐과 봉제 수선|같은 사람의 피부 상처|의복 손상을 신체 손상으로 전이하지 않음
U82|선택된 패널 가장자리만 발광하는 제복|사이버 보안요원이라는 이름만 있는 요청|이름에서 전신 네온·로봇 몸·침입/경비 동작 추론 금지
U83|손에 든 무기를 명시한 무장 수도회 코스튬|갈색 수도복 초상|소품·손-그립 관계는 명시된 경우에만 선택
"""

def run():
    cases = []
    for n, line in enumerate(CASES.strip().splitlines(), 1):
        aid, positive, negative, boundary = line.split("|")
        cases.append({"id": f"UV{n:03d}", "atom_ids": [aid],
            "request_pair": {"a": positive, "b": negative}, "expected_distinction_ko": boundary,
            "future_layers": ["retrieval_rank_and_eligibility", "exact_vs_advisory_activation", "selected_candidate_adoption", "prompt_component_evidence", "native_pixel_gate"],
            "request_locks_to_preserve": ["subject_count", "identity", "species", "age", "pose", "camera", "explicit_appearance_properties"],
            "status": "planned_not_executed", "partial_is_fail": True, "occluded": "UNOBSERVABLE"})
    (HERE / "validation-cases.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cases))
    ko = "민소매 전복의 진동에서 별도 안쪽 옷 소매가 나옴"
    en = "the inner sleeves emerge through the open armholes of a separate sleeveless outer robe on the same wearer"
    candidate = {
        "id": "uniform_draft_sleeveless_robe_over_inner_sleeves", "ko": ko, "en": en, "weight": 0.45,
        "for_any": ["human"], "aliases": [ko], "keywords": [ko, "민소매 겉옷과 별도 안쪽 소매의 겹침"],
        "embedding_text": en + " | " + ko, "concept_units": [en],
        "relations": [{"id": "draft_sleeveless_robe_owner", "type": "declared_owner_scope", "subject": "the sleeveless outer robe", "object": "the request-supported costume wearer"},
            {"id": "draft_sleeveless_robe_layer", "type": "layered_over", "subject": "the sleeveless outer robe", "object": "the independent inner long-sleeved garment"}],
        "tags": ["human", "costume", "cosplay"], "affected_dimensions": ["appearance"],
    }
    phrases = ["the separate sleeveless outer robe has open armholes", "the inner sleeves emerge through those outer armholes on the same wearer"]
    profile = {
        "id": "uniform_draft_sleeveless_robe_over_inner_sleeves", "category": "costume_cosplay_visible_relation",
        "activation": {"exact_terms": [en, ko], "requires_adult_character": False,
            "semantic_discovery_requires_component_evidence": True,
            "hard_activation": {"contract_version": "photo-visual-hard-activation/v1", "required_any_groups": [{"id": "selected_relation", "any_terms": [en, ko]}]}},
        "semantics": {"definition": en, "paraphrase_examples": ["open outer armholes reveal independently owned inner sleeves"],
            "contrast_examples": ["a sleeved outer coat", "abalone food on a plate"],
            "claim_limits": ["One selected garment relation, not a full historical date or rank definition.", "No role, action, age or body change follows from this garment."]},
        "concept_candidate": {"concept_terms": [ko, "민소매 겉옷과 별도 안쪽 소매의 겹침"]},
        "runtime_expression": {"default_mode": "definition_with_optional_label", "prompt_label_terms": [], "forbidden_prompt_terms": [], "runtime_forbidden_labels": []},
        "reject_substitutes": ["outer sleeves mistaken for inner sleeves", "one unlayered robe"],
        "authored_components": {"contract_version": "photo-authored-visual-components/v1", "components": [
            {"id": f"component_{i}", "match_terms": [en, ko], "evidence_field": f"component_{i}_phrase", "evidence_terms": [p], "min_content_words": 3,
                "instruction": "Preserve this selected owner relation: " + p,
                "render_gate": {"id": f"vo_uniform_draft_robe_{i}", "review_scale": "native", "description": p + ". A partial, misplaced or occluded relation does not pass."}}
            for i, p in enumerate(phrases, 1)]},
    }
    draft = {"schema": "uniform-costume-runtime-example-research/v1", "runtime_ready": False,
        "research_source_ids": ["S02"], "research_atom_id": "U02", "candidate_slot_proposal": "garment_detail",
        "limits_ko": ["현행 구조를 따라 작성한 검토용 예제다. 배포 검증기·속성 충돌·회귀 테스트는 실행하지 않았다.",
            "for_any human은 이 인간 착용자 예제에만 적용한다. 다른 종/기계 캐릭터에 그대로 복사하지 않는다.",
            "전복이라는 단어만으로 exact hard activation을 만들지 않는다. 의복 문맥의 형태 관계를 요구한다.",
            "affected_properties는 실제 appearance 소유·속성 경로 확인 뒤 추가한다. 연구의 임시 property 키를 복사하지 않는다."],
        "candidate": candidate, "profile": profile}
    (HERE / "runtime-example-drafts.json").write_text(json.dumps(draft, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"planned_request_pairs": len(cases), "illustrative_runtime_drafts": 1}))

if __name__ == "__main__":
    run()
