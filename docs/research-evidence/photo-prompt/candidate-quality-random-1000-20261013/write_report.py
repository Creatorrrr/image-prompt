"""Write a source-linked report from the completed, explicit audit."""
from pathlib import Path
import json

R = Path(__file__).resolve().parent
summary = json.loads((R / "RESULTS.json").read_text())
manifest = json.loads((R / "SAMPLE-MANIFEST.json").read_text())
samples = {row["sample_number"]: row for row in map(json.loads, (R / "samples.jsonl").read_text().splitlines())}
reviews = {row["sample_number"]: row for row in map(json.loads, (R / "reviews.jsonl").read_text().splitlines())}


def link(name, label=None):
    return f"[{label or name}]({R / name})"


def sample_link(number):
    return f"[#{number}]({R / 'samples.jsonl'}:{number})"


def escape(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


meaning_notes = {
    83: "브라 뒷밴드의 훅앤아이 여밈을 정의하면서 재표현에는 bra strap detail, 변경 속성에는 bra_strap_adjust가 들어 있다. 등 밴드 여밈과 어깨끈 조절의 부품이 섞였다.",
    123: "블랙홀 강착원반 시각화의 정의가 위·아래로 휘는 원반과 좌우 밝기 비대칭을 모두 requires로 요구한다. 관측 시점에 따른 특정 변형으로 범위를 한정해야 한다.",
    154: "한글의 일반적인 유능함·취약성 성인 주체와 영어의 숙련 제작자 및 성인 동료가 같은 aliases에 들어 있다. 직업과 다른 성인 행위자가 추가돼 의미 범위가 일치하지 않는다. 원래 작성자가 구체 변형을 의도했을 가능성과 이관 과정의 손상 여부는 별도다.",
    278: "선택된 캄보디아 아르다나리슈바라의 시바 측 필수 요소를 영어 beard로 기록했다. 대응하는 Met 문서는 mustache로 기술한다. 한글 수염을 영어에서 다른 얼굴 부위로 좁힌 원전 대비 차이다.",
    503: "정의와 한글은 유연한 EL 와이어인데 aliases에는 Gas-discharge tube와 Violet glow in glass tubes가 들어 있다. 형광체 코팅 와이어와 기체 방전 유리관은 같은 발광체 방식이 아니다.",
}
tag_notes = {
    40: "봉인이 걸친 닫힌 이음과 그 위치의 파열은 물건 상태·배치 관계다. prop_direction에 필요한 방향을 정하지 않는다.",
    132: "보케 광원은 초점 밖 광학 모습이다. ambient_particle에 등록돼 입자와 광학 원반을 혼동할 수 있다.",
    234: "허구 자료를 제시하는 인터뷰 구도를 caption_context에 넣었다. 캡션 내용·표시 조건이 아니라 촬영/구도 관계다.",
    302: "TikTok 브이로그 감성을 world 및 setting 변경으로 등록했다. 플랫폼·미디어의 표현 감성과 세계의 설정을 구분해야 한다.",
    396: "나뭇잎을 통과한 얼룩빛은 빛의 패턴이다. light_direction에 필요한 광원 방향을 정하지 않는다.",
    428: "리본·천이 중력 방향으로 안정되게 매달린 관계를 ambient_particle에 넣었다. 공기 운동·천의 변형 조건이며 입자 후보가 아니다.",
    451: "저채도 90년대 그런지 에디토리얼 무드를 world 및 setting 변경으로 등록했다. 스타일·색보정·무드가 더 직접적인 역할이다.",
    642: "맨다리에 그린 장미 바디페인트를 garment_detail로 등록하고 효과도 wardrobe로 지정했다. 실제 소유자는 피부이며 의복 프린트와 명시적으로 구분하는 원본이다.",
    643: "몸과 다른 동작을 하는 투영 그림자 관계를 reflection_logic에 등록했다. 효과에도 reflected_subject.gesture와 reflection이 남아 있다. 그림자와 거울상을 구분해야 한다.",
}
weak_notes = {
    20: "borderline 성적 암시의 경계를 정의할 기준이나 구체 단서가 없다. 성인 맥락 태그 자체는 적합하다.",
    22: "시각 단위에 소유자 일치만 기록이라는 작성 지시가 들어 있고 허리 밴드가 두 번 반복된다. 구체 부품은 존재한다.",
    115: "한글은 좁은 소매를 요구하지만 영어 controlled sleeve width에는 좁다는 값이 없다.",
    193: "진공 포장은 구체적이지만 concept object가 실제 주체 종류를 정하지 않는다.",
    230: "wrong reflection을 catching한다는 말에 반사가 어떻게 어긋나는지, 어떻게 접촉하는지 없다.",
    260: "자유로운 아티스트 외형은 구체 스타일 단서 없이 직업·성격의 인상에 기대고 있다.",
    315: "인지하고 자리를 내주는 행동은 미모에 특이적인 반응이 아니다. 평판을 쓰려면 추가 서사 맥락이 필요하다.",
    331: "ritual goddess drape는 구체 드레이프나 선택된 문화/창작 변형을 정하지 않는다. ko도 영어다.",
    484: "주요 시각 단위가 하의 끈과 상단 컵 부재만 기록이라는 작성 지시다. 부품 의미와 지시를 분리해야 한다.",
    546: "지연된 반사에 시간 또는 실물과 반사의 상태 차이가 없다. ko도 영어다.",
    675: "피사체로 당겨지는 모니터 빛에 광선 경로·형상·변형 범위가 없다.",
    924: "주요 시각 단위가 컵 범위·받침·중앙 브리지만 기록이라는 지시다. 나머지 부품은 구체적이다.",
    983: "숨을 멈춘 집중이라는 표정에 읽을 수 있는 얼굴 단서가 없고 ko도 영어다.",
    998: "차가운 얼굴과 따뜻한 손이 온도인지 무표정과 돌봄 행동의 비유인지 정해져 있지 않다.",
}

detail = [
    "**후보 데이터 의미 품질 감사: 상세 발견 — 2026-10-13**\n",
    "샘플 번호는 추출 순서다. 각 번호 링크에서 완전한 원본과 binding을 확인할 수 있다. 아래는 이번 감사의 판정이며 태그 대안은 수정 방향의 제안이다. 기존 데이터에는 적용하지 않았다.\n",
    "의미 불일치·정의 범위 문제 5개는 다음과 같다.\n",
    "| 샘플 | canonical ID | 원본 필드와 판정 |\n|---|---|---|",
]
for number in summary["confirmed_meaning_inconsistency_samples"]:
    detail.append(f"| {sample_link(number)} | `{reviews[number]['candidate_id']}` | {meaning_notes[number]} |")
detail.extend([
    "\n#123의 시점 의존성은 [NASA 강착원반 시각화](https://svs.gsfc.nasa.gov/13326)의 설명으로 확인했다. NASA는 원반 바로 위·아래 시점에서는 Doppler 밝기 비대칭이 사라짐을 설명한다. 특정 시점의 시각 정의를 보편 조건으로 확장한 것이 문제다.\n",
    "#278의 기준은 [Met의 해당 캄보디아 작품 설명](https://www.metmuseum.org/art/collection/search/39198)이다. 문서의 콧수염과 데이터의 beard 차이를 기록했다. 다른 아르다나리슈바라 변형 전체의 얼굴 특징을 판정한 것은 아니다.\n",
    "#503의 EL 와이어 방식은 [Adafruit 제조사 기술 문서](https://learn.adafruit.com/el-wire/)가 설명하는 형광체 코팅과 외피 구조로 확인했다. 기체 방전관을 별칭으로 유지하면 물체의 발광 방식과 형태가 다른 검색어를 같은 후보로 연결하게 된다.\n",
    "부적합 슬롯으로 판정한 9개는 다음과 같다. 슬롯 이름만으로 판정하지 않고 영어 의미·관계·효과 대상과 함께 비교했다. 역할 경계는 질적 판단이므로 독립적인 정답 라벨로 보장되지는 않는다.\n",
    "| 샘플 | 현재 슬롯 | 관련 역할 제안 | 판정 근거 |\n|---|---|---|---|",
])
for number in summary["wrong_slot_samples"]:
    row = reviews[number]
    detail.append(f"| {sample_link(number)} | `{','.join(row['assigned_slots'])}` | `{','.join(row['suggested_semantic_slots'])}` | {tag_notes[number]} |")
detail.extend([
    "\n범위가 넓지만 관련 있는 30개를 위 9개와 합쳐 오류로 계산하지 않았다. 예를 들어 #135의 낮은 카메라 시점은 구도에도 영향을 주므로 composition 태그를 넓은 관련으로 인정했다. 다만 선언 효과에 camera 방향·높이가 빠지고 aliases가 worms / eye / view로 쪼개진 것은 보강 대상이다.\n",
    "내용을 더 구체화할 필요가 있는 14개는 다음과 같다. 작성 지시가 섞인 번들도 실제 부품 자체가 전부 무의미하다는 판정은 아니다.\n",
    "| 샘플 | 종류 | 보강할 내용 |\n|---|---|---|",
])
for number in summary["weak_meaning_samples"]:
    detail.append(f"| {sample_link(number)} | `{reviews[number]['record_kind']}` | {weak_notes[number]} |")
detail.extend([
    f"\n{sample_link(263)}의 prix seam은 전문 표현의 세부를 보류했다. [Dents 원전](https://row.dentsgloves.com/pages/dents-guide-to-buying-gloves)은 노출된 바깥 봉제를 뒷받침한다. 데이터가 추가한 맞댄 경계까지는 그 문서로 확인하지 못했다. 노출 봉제의 핵심 의미를 틀렸다고 확정하지 않았다.\n",
    "적용 조건의 충돌은 슬롯 태그의 단어와 별개로 확인했다. 아래 12개는 의복을 입은 사람의 소재를 설명하거나 for_any에 human을 선언하지만 binding의 subject_categories 기본 목록에는 human이 없다.\n",
    "| 샘플 | 한글 의미 | 인물·패션 조건 | 인물·CJK 세계관 조건 |\n|---|---|---|---|",
])
for number in summary["human_material_guard_conflict_samples"]:
    label = samples[number]["candidate"]["content"].get("ko", "")
    detail.append(f"| {sample_link(number)} | {escape(label)} | 거부 | 허용 |")
detail.extend([
    f"\n현재 `photo_global_retrieval.guard_policy`를 subject_category=human, domains=[fashion] 및 domains=[cjk_narrative_world]로 직접 호출해 비교했다. 각 후보는 유일한 persistent binding에서 첫 조건을 거부하고 두 번째 조건을 허용했다. 그러므로 항상 검색 불가라는 결론은 아니다. 일반 인물·패션 용도에서의 의미/정책 범위 충돌은 재현됐다. 계약 입력과 반환값은 {link('GUARD-PROBES.json')}에 보존했다.\n",
    f"{sample_link(995)}는 영어 embedding_text가 명시적으로 macro product photography를 설명하지만 binding은 product를 거부한다. object/product 계약에서 거부됨을 같은 함수로 확인했다. #388의 documentary 조건도 별도로 거부된다. 전체 검색과 순위/회수율은 이번 감사에서 실행하지 않았다.\n",
    "한영 내용·범위 차이 23개는 다음과 같다. 제목과 구체 변형을 한 쌍으로 저장한 의도적인 경우가 포함될 수 있으므로 23개를 모두 오역 또는 이관 손상으로 확정하지 않는다. 특히 배우 수·동작·색·길이처럼 선택 결과를 달리할 요소는 명시적으로 분리할 필요가 있다.\n",
    "| 샘플 | ko | en |\n|---|---|---|",
])
for number, row in reviews.items():
    if row["translation"] == "mismatch":
        content = samples[number]["candidate"]["content"]
        detail.append(f"| {sample_link(number)} | {escape(content.get('ko',''))} | {escape(content.get('en',''))} |")
detail.extend([
    "\nko에 한국어 설명이 없고 영어가 그대로 있는 45개의 번호는 " + ", ".join(sample_link(n) for n, row in reviews.items() if row["translation"] == "missing_ko") + "다. 문장 의미가 없는 경우와 구분해서 집계했다.\n",
    "원본 의미가 명료해도 보강할 메타데이터가 남는다. #440에는 머리와 귀걸이의 배치를 함께 정의하면서 효과는 jewelry만 지정한 범위 차이가 있다. #382의 소매를 걷는 동작에는 appearance만 선언돼 있다. #588의 혼동 경계에는 중복을 검토하라는 내부 정비 지시가 남아 있다. #687의 팔짱 자세에는 tripod/timer/remote 같은 촬영 운용 태그가 요구된다. 이들은 데이터 정합성 검토 항목이며 실제 요청이나 생성 결과의 오류를 재현했다고 주장하지 않는다.\n",
    "역사·행동 의도·동의·소유권·재료 정체·소리·시계열은 텍스트 맥락에서 유효할 수 있다. 단일 사진으로 증명되지 않는다는 이유만으로 그 의미를 데이터 오류로 계산하지 않았다. informational flags는 이 제한을 기록한다. 모든 flag를 오류 수로 더하면 잘못된 집계가 된다.\n",
])
(R / "FINDINGS.ko.md").write_text("\n".join(detail) + "\n")

report = f"""**후보 데이터 무작위 1,000개 의미 품질 감사 — 2026-10-13**

대부분의 후보는 실제 사물·형태·관계 또는 유효한 촬영/서사 맥락을 담고 있다. 다만 의미가 다른 부품·별칭의 혼합, 특정 과학 변형의 과도한 일반화, 잘못된 슬롯과 효과 대상, 후보 의미와 맞지 않는 적용 조건이 확인됐다. 데이터 품질을 충분히 정리된 상태로 보기는 어렵다. 아래의 98%는 내용의 중심 의미가 명료하다는 이번 정성 판정이며, 데이터 전체의 정확도나 검색·생성 성공률은 아니다.

| 검토 축 | 결과 | 분모와 해석 |
|---|---:|---|
| 중심 의미가 명료하고 일관됨 | 980개 / 98.0% | 무작위 표본 1,000개 |
| 의미/시각 단서 보강 필요 | 14개 / 1.4% | 추상적 단서, 모호한 비유, 의미 필드에 섞인 작성 지시 |
| 의미 불일치·정의 범위 문제 | 5개 / 0.5% | 부품·별칭·원전·한영 주체 범위 불일치 |
| 전문 표현 세부 확인 보류 | 1개 / 0.1% | prix seam의 추가적인 맞댄 경계 설명 |
| 기존 슬롯 태그 적합 | 653개 / 94.4% | persistent binding이 있는 692개 |
| 범위가 넓지만 관련 있는 태그 | 30개 / 4.3% | 위 692개; 자동 오류로 계산하지 않음 |
| 기존 슬롯 태그 부적합 | 9개 / 1.3% | 위 692개 |
| persistent binding 없음 | 308개 | 프로필 196, 번들 106, 관계 메커니즘 6; 허용된 구조 |
| ko 필드의 한국어 설명 누락 | 45개 | 영어가 그대로 들어 있는 옵션; 의미 부재와 다름 |
| ko/en 내용·범위 차이 | 23개 | 의도적인 제목/구체 변형 차이도 가능 |

검토 축은 겹친다. 태그가 맞고 문장 의미가 명료한 후보도 적용 조건에 막힐 수 있으므로 각 행을 더해 전체 오류 수로 사용하면 안 된다. 슬롯이 없는 308개를 모두 태그 누락 오류로 처리하지도 않았다. 공통 풀의 profile/bundle/mechanism은 현재 binding 없이 존재할 수 있다. 관련 역할 제안은 판정표에 기록했으며 새 태그를 적용하지 않았다.

실질적인 문제를 대표하는 원본은 다음과 같다.

| 원본 | 문제 | 필요한 정리 |
|---|---|---|
| {sample_link(83)} | 뒷밴드 훅앤아이 여밈이 재표현·속성에서는 브라 어깨끈 조절로 바뀜 | 실제 부품의 소유자와 변경 속성을 일치시키기 |
| {sample_link(503)} | EL 와이어에 가스 방전 유리관이 aliases로 붙어 있음 | 다른 방식의 물체를 별칭으로 연결하지 않기 |
| {sample_link(123)} | 강착원반 시각화에 시점 의존적인 밝기 비대칭을 보편 조건으로 요구 | 선택된 관측 시점을 명시하기 |
| {sample_link(642)} | 피부의 바디페인트가 garment_detail이고 효과 대상도 wardrobe | body_marking 및 피부 소유자로 정리하기 |
| {sample_link(396)} | 나뭇잎의 얼룩빛이 light_direction에 들어 있음 | 패턴과 방향을 분리하기 |
| {sample_link(302)} | TikTok 표현 감성이 world/setting 변경으로 등록됨 | 플랫폼·스타일의 역할을 구분하기 |

EL 와이어의 형광체 코팅 구조는 [Adafruit 기술 문서](https://learn.adafruit.com/el-wire/)로 확인했다. 원반 밝기 비대칭의 시점 의존성은 [NASA 시각화 설명](https://svs.gsfc.nasa.gov/13326)으로 확인했다. 나머지 의미 불일치 2개와 슬롯 부적합 9개 전체, 보강 대상 14개 및 한영 차이 23개는 {link('FINDINGS.ko.md','상세 발견 목록')}에 원본 링크와 함께 기록했다.

적용 조건에서는 의복 소재 후보 12개가 사람을 설명하면서 기본 subject_categories에서는 human을 제외하고 있었다. 현재 정책 함수를 인물·패션 계약으로 호출했을 때 12개 모두 거부됐으며, CJK 세계관 도메인의 override 조건에서는 허용됐다. 따라서 후보가 항상 검색 불가한 것은 아니지만 일반 패션 용도와 적용 범위가 충돌한다. 상품 매크로 촬영 후보 #995도 object/product 계약에서 거부됐다. {link('GUARD-PROBES.json','조건별 함수 입력과 반환값')}은 실제 함수로 재현한 근거다. 이 검사는 합성 계약의 정책 판정이며 전체 검색 순위·회수율 검사는 아니다.

중복 검사는 표본 안에서 identity/provenance를 제외한 content+effects 완전 일치 0그룹, 실제 양성 인덱스 recipe+text 완전 일치 0그룹이었다. 핵심 의미 문장이 겹치는 것은 17그룹, 34개 후보였다. 전부 서로 다른 종류의 옵션·프로필·번들 사이의 반복이며 각자의 사용 계약이 다르다. 이를 무조건 같은 canonical ID로 합치면 활성화·증거·구성 계약을 잃을 수 있다. 이번 결과로 전 데이터의 의미 중복이 없거나 검색 순위에 반복 편향이 없다고 판단할 수는 없다. 비교 방식과 그룹은 {link('REPETITION-CHECKS.json')}에 보존했다.

정상적인 좁은 변형도 구분했다. 크리놀렛의 평평한 앞과 뒤쪽 구조는 [V&A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)가 뒷받침한다. 선택된 헤바즈라의 손·컵·배우자 특징은 [Himalayan Art의 해당 작품](https://www.himalayanart.org/items/90531), 테필린의 머리·위팔 착용은 [Chabad의 구성 설명](https://www.chabad.org/library/article_cdo/aid/1921512/jewish/Purchasing-Tefillin-A-Buyers-Guide.htm)과 대조했다. 혜성 꼬리의 넓은 의미에서의 태양 반대 방향은 [NASA 설명](https://spaceplace.nasa.gov/comets/en/)에 맞아 초기 의심을 해제했다. 장르·의도·신화·문화의 선택된 표현을 그 전체의 유일한 정의로 취급하지 않았다.

표본은 canonical 후보 18,250개 전체에서 단순 무작위 비복원으로 1,000개를 추출한 것이다. 종류·슬롯 quota와 재추출은 없었다. 난수 seed는 `{manifest['seed_decimal']}`이고, 정렬된 전체 ID 목록에 Python Random.sample을 적용했다. 표본 종류는 옵션 692, 프로필 196, 번들 106, 관계 메커니즘 6개이며 112개 catalog 슬롯 중 88개가 기존 binding으로 나타났다. diagnostic 및 relationship_concept는 이번 난수 표본에 없었다. 희소 종류나 모든 슬롯의 의미 품질을 별도로 보장하는 검사 결과는 아니다.

모든 표본의 핵심 의미·한영 표현·관계·효과·binding을 중복 문구를 줄인 카드로 개별 읽고, 의심 사례는 원본 필드와 공통 적용 조건 및 제한을 추가 대조했다. 단순 문자열 규칙이나 schema 통과로 의미 판정을 자동 생성하지 않았다. 처음 판정과 재확인 후 변경은 {link('ADJUDICATIONS.json')}에 남겼다. 한글 설명과 영어 구체 변형의 차이가 최초 작성 의도인지 이관 오류인지까지는 이 감사만으로 확정하지 않는다. 문화·과학 전문 항목도 선택된 근거를 대조한 범위이며 모든 세부의 전문가 인증은 아니다.

검증에서는 고정 seed로 동일한 1,000개와 동일 순서를 재현했고, 모든 판정의 ID·원본 SHA·binding을 대조했다. 후보·정책·catalog·manifest를 포함한 원본 파일 35개의 SHA가 일치했고 참조 후보 224개도 현재 원본과 일치했다. native 구조 검사는 18,250개 후보와 12,020개 binding에서 통과했다. HEAD `{manifest['head']}`, runtime generation `{manifest['generation_id']}`, source fingerprint가 유지됐다. 기존 수정 중인 문서 2개도 바뀌지 않았다. {link('VERIFICATION.json','검증 기록')}에 비교값과 결과를 저장했다.

우선 수정 방향은 다음과 같다.

1. 실제 부품·장치 의미가 바뀌는 정의·별칭·원전 차이 5개와 피부/의복/그림자처럼 효과 대상이 다른 항목을 정리한다.
2. 소재 및 촬영 후보의 적용 조건을 실제 용도와 맞춘다. 사람·패션과 오브젝트·상품의 대표 계약을 함께 검증한다.
3. 부적합 태그 9개를 바로잡고 넓은 관련 태그 30개에는 필요한 추가 역할을 검토한다. binding 없는 프로필·번들은 역할 계약을 고려해 태그를 보강한다.
4. ko/en을 제목과 구체 변형으로 명시적으로 구분하고, 영어가 그대로 있는 ko 45개와 내용·범위 차이 23개를 정리한다. 작성 지시를 시각 의미 필드에서 분리한다.
5. 데이터 수정 뒤에는 그 변경의 영향을 받는 검색 텍스트·임베딩을 갱신하고 소유자·방향·부품 경계 검색을 검증한다. 이번 감사는 기존 벡터의 의미 품질이나 이미지 결과를 검증한 작업이 아니다.

전체 결과는 {link('SAMPLE-RESULTS.csv','1,000행 판정표')}, {link('reviews.jsonl','개별 판정 JSONL')}, {link('RESULTS.json','집계 JSON')}에서 확인할 수 있다. 완전한 원본은 {link('samples.jsonl')}, 추출 및 원본 고정값은 {link('SAMPLE-MANIFEST.json')}, 평가 기준은 {link('METHOD.ko.md')}에 있다.

이번 작업은 감사 자료만 새로 저장했다. 후보 데이터·binding·임베딩·runtime는 수정하지 않았고 이미지 또는 임베딩 API 호출, 커밋, 푸시는 하지 않았다. Codex의 정성적 텍스트 판정이며 독립 전문가 합의·실서비스 요청·생성 이미지 및 실제 픽셀 검증을 대체하지 않는다.
"""
(R / "REPORT.ko.md").write_text(report)
print({"report": str(R / "REPORT.ko.md"), "report_characters": len(report), "details_characters": sum(map(len, detail))})
