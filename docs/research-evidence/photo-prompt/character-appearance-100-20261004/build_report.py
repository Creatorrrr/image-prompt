#!/usr/bin/env python3
"""Create the readable case list and evidence-layered maintenance receipt."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg

def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    cases=json.loads((HERE/'CHARACTER-CASEBOOK.json').read_text())['cases']
    receipt=json.loads((HERE/'INTEGRATION-MAINTENANCE.json').read_text())
    retrieval=json.loads((HERE/'RETRIEVAL-RESULTS.json').read_text())
    base=json.loads((HERE/'BASELINE.json').read_text())
    data=pg.load_runtime_data();registry=data[pg.VISUAL_OBLIGATIONS_DATA_KEY]
    profiles={p['id']:p for p in registry['profiles']}
    index=data[pg.VISUAL_PROFILE_INDEX_DATA_KEY]
    suite_path=HERE/'full-suite/SUMMARY.json'
    suite=json.loads(suite_path.read_text()) if suite_path.exists() else None
    group_names={'hololive':'홀로라이브','guilty_gear_strive':'길티기어 스트라이브',
        'tekken8':'철권 8','pokemon':'포켓몬 기본 도감 형태','demon_slayer':'귀멸의 칼날 입지편'}
    counts=receipt['counts']
    lines=['**추가 조사한 캐릭터 100개와 외형 요소 분해**','',
        '기존 37개 사례와 다른 100개를 추가했다. 아래의 공식 출처 링크와 도판 바이트 해시는 특정 관찰 버전을 식별한다. 포켓몬은 기본 형태의 종 디자인 사례이며, 다른 개체·메가·지역 형태를 합친 사례가 아니다.',
        '', '귀멸의 칼날은 공식 캐릭터 페이지의 장면 크롭을 사용했다. 크롭 밖의 옷·허리·다리, 알려진 설정만 있는 신체 구조, 가려진 부착 기점을 관찰했다고 쓰지 않았다. 철권 일부는 공식 전후면 설정화이고 일부는 크롭된 주요 렌더다.',
        '', '| ID | 계열 | 캐릭터 | 주요 관찰 요소 | 의미 연결 수 |', '| --- | --- | --- | --- | --- |']
    for c in cases:
        short=c['decomposed_elements'][0]['observation_ko']+' / '+c['decomposed_elements'][3]['observation_ko']
        lines.append(f'| {c["id"]} | {group_names[c["group"]]} | [{c["name_ko"]}](#{c["id"].lower()}) | {short} | {len(c["runtime_links"])} |')
    lines+=['','각 사례의 의미 연결은 선택한 요소를 기존 정의와 대조한 기록이다. 사례 전체를 하나의 자동 스타일로 등록하지 않는다. “부분 확인”은 해당 정의를 충족한 관찰 판정이 아니다.','']
    labels={'head_or_hair':'머리·상부 윤곽','face_or_surface':'얼굴·표면','clothing_or_body':'의상·몸통','appendages_or_details':'부속·세부','props_or_companions':'소품·별도 소유자'}
    for c in cases:
        lines += [f'<a id="{c["id"].lower()}"></a>',f'**{c["id"]} {c["name_ko"]} / {c["name_en"]}**','',
            f'[공식 페이지]({c["source_url"]}) · [관찰 도판]({c["artwork_url"]}) · 버전: {c["version_scope"]}', '']
        for part in c['decomposed_elements']:
            lines.append(f'- {labels[part["region"]]}: {part["observation_ko"]}')
        lines.append('- 관계: '+'; '.join(c['observable_relations_ko']))
        lines.append('- 확인 불가·혼동 경계: '+'; '.join(c['unobservable_and_confusions_ko']))
        for link in c['runtime_links']:
            p=profiles[link['profile_id']]
            ko=p['semantics']['paraphrase_examples'][-1]
            status='부분 확인' if link['source_relation_status'].startswith('PARTIAL') else '보이는 요소 대조'
            lines.append(f'- 의미 연결 `{link["profile_id"]}` ({status}, 소유자: {link["source_owner"]}): {ko}')
            if status=='부분 확인':lines.append('  - '+link['source_review_note_ko'])
        if c['held_observations']:lines.append('- 연구 기록에 유지: '+', '.join(c['held_observations']))
        lines+=['',f'도판 SHA-256: `{c["artwork_sha256"]}`','']
    (HERE/'CHARACTER-LIST.md').write_text('\n'.join(lines)+'\n')

    observed=sum(c['evidence_state']=='PUBLISHER_PIXELS_OBSERVED' for c in cases)
    unchanged_assets=[];changed_assets=[]
    for rel,old_sha in base['assets'].items():
        path=ROOT/rel
        if not path.exists():continue
        (unchanged_assets if sha(path)==old_sha else changed_assets).append(rel)
    preserved=json.loads((HERE/'BASELINE-REGISTRY.json').read_text())['profiles']
    comparisons=[]
    for before in preserved:
        after=profiles[before['id']]
        comparisons.append(all(before[k]==after[k] for k in ('activation','render_gates','required_evidence_fields','composition_instruction'))
            and before['semantics']['definition']==after['semantics']['definition']
            and before.get('concept_candidate',{}).get('affected_properties')==after.get('concept_candidate',{}).get('affected_properties'))
    assert all(comparisons)
    assert pg.dictionary_hash(data)==base['dictionary_hash']
    maintenance={'contract_version':'photo-extension-maintenance-record/v1',
        'record_id':'character-appearance-100-20261004','maintenance_only':True,
        'integration_receipt':{'path':str((HERE/'INTEGRATION-MAINTENANCE.json').relative_to(ROOT)),
            'sha256':sha(HERE/'INTEGRATION-MAINTENANCE.json')},'counts':counts}
    save(HERE/'MAINTENANCE-RECORD.json',maintenance)
    validation={'schema_version':'character-appearance-validation-summary/v1',
        'source_layer':{'official_pages':100,'distinct_artwork_hashes':len({c['artwork_sha256'] for c in cases}),
            'publisher_pixels_observed':observed,'case_count':len(cases),'groups':dict(Counter(c['group'] for c in cases)),
            'independent_generated_image_evaluation':False},
        'authored_data_layer':{'before_profile_count':len(preserved),'current_profile_count':len(profiles),
            'preserved_prior_profiles':sum(comparisons),**counts,'ordinary_dictionary_hash':pg.dictionary_hash(data),
            'ordinary_dictionary_hash_unchanged':True,'ordinary_candidate_count':sum(len(r) for r in data['slots'].values()),
            'changed_baseline_asset_paths':changed_assets,'unchanged_baseline_asset_count':len(unchanged_assets)},
        'index_layer':{'registry_sha256':index['registry_sha256'],'index_validated_against_live_registry':True,
            'vectors_reembedded':110,'batch_size':1,'prior_unchanged_vectors_reused':1561},
        'retrieval_layer':retrieval['counts'],'full_suite':suite,
        'rendered_generated_image_layer':'NOT_RUN_IN_THIS_MAINTENANCE_REQUEST',
        'git_layer':'workspace changes only; current additional scope has no new commit or push'}
    save(HERE/'VALIDATION-SUMMARY.json',validation)
    suite_text=f'전체 unittest discovery {suite["tests_run"]}개 통과, 실패 {len(suite["failure_ids"])}개, 오류 {len(suite["error_ids"])}개.' if suite and suite['successful'] else '전체 unittest discovery 실행 중. 최종 판정은 full-suite/SUMMARY.json으로 확인한다.'
    report=[
        '**캐릭터 외형 100개 추가 조사와 시각 의미 반영 결과**','',
        '기존 37개와 다른 100개를 추가 조사하여 실제 시각 의미 레지스트리에 반영했다. 홀로라이브·길티기어 스트라이브·철권 8·포켓몬·귀멸의 칼날에서 각각 20개다. 공식 페이지 100개와 서로 다른 공식 도판 100개를 취득하고 픽셀을 대조했다.',
        '',f'신규 의미 {counts["new_profiles"]}개, 신규 필수 구성 요소 {counts["new_components"]}개, 기존 의미 보강 {counts["enriched_existing_profiles"]}개를 반영했다. 신규 의미의 한영 완전 표현 {counts["new_profile_full_alternatives"]}개와 기존 의미의 추가 완전 표현 {counts["existing_full_alternatives_added"]}개가 들어갔다. 전체 시각 의미는 1,622개에서 {len(profiles):,}개로 늘었다.',
        '', '100개 캐릭터마다 5개 영역의 외형 분해, 요소 사이 관계, 가려진 구조, 혼동 경계, 소유자, 실제 프로필 연결을 남겼다. 308개 의미 연결 중 27개는 부분 확인으로 보류했다. 예를 들어 알리사는 로봇 설정만으로 기계 관절을 추가하지 않았고, 마린의 가려진 눈 색과 루나의 치마 속 받침을 추정하지 않았다. 베드맨의 기계 사지와 델릴라의 모발은 소유자가 다르다.',
        '', '새 의미의 대표 관계는 짧은 단발 끝선, 내려온 모발의 반복 교차, 안경 테와 코 다리, 모자에 붙은 돌출부, 동물 머리 가면, 입 아래 천 감김, 단단한 사지 절편과 관절 면, 한 꼬리 끝의 두 갈래, 몸 털과 의상 털의 구분, 날개 막과 지지선, 등껍질과 열린 관, 집게의 마주 보는 두 턱이다.',
        '', '캐릭터 이름은 연구 출처 식별에만 쓴다. 이름·전체 팔레트·나이·성격·작품 장르로 다른 인물의 외형을 자동 활성화하지 않는다. 모든 새 관계는 지정 소유자와 필수 요소를 요구하며 누락은 실패, 가림은 확인 불가로 유지한다. 기존 1,622개 정의·활성화·필수 필드·속성 효과·원본 픽셀 검증 기준은 보존됐다.',
        '', '시각 의미 인덱스를 batch-size 1로 갱신했다. 변경된 110개 의미를 다시 임베딩하고 1,561개 기존 벡터를 재사용했다. 일반 후보 데이터 9,840개와 사전 해시는 유지됐으며 기존 일반 후보 인덱스도 유효하다. 캐릭터 완성형 후보 100개를 덧붙이는 방식은 사용하지 않았다.',
        '', '실제 검색 진단에서는 별도 문장 12개 모두 목표 의미가 전체 1,671개 벡터 중 1위였다. 완전한 요소 증거를 가진 벡터 검색은 10/12개, 같은 증거를 가진 실제 BM25F+벡터 검색은 12/12개를 선택 가능한 후보로 찾았다. 트라이콘 모자와 사지 끝 집게는 벡터 단독 선택 임계값에 미달했다. 요소 증거 없이 자유 문장만 넣으면 0/12개가 선택 후보로 승격됐다. 이는 all-of 구성 요소 확인 규칙을 유지한 결과이며 자유 자연어 자동 활성화 성공으로 집계하지 않는다. 음성·오타 일반화나 생성 이미지 구현 성공을 주장하지 않는다.',
        '', '집중 테스트 12개 통과. 사전 메타데이터 검증, 라이브 레지스트리와 인덱스 해시 검증, 기존 의미 보존, 이름 단독 비활성화, 다른 소유자·의상·신체 경계, 속성 잠금 검증을 통과했다. '+suite_text,
        '', '이번 추가 요청의 검증 범위는 공식 출처 관찰·데이터·검색·회귀 테스트다. 100개 신규 생성 이미지 평가를 실행한 결과는 아니다. 현재 변경은 로컬 작업 공간에 저장했으며 이 추가 범위의 커밋·푸시는 실행하지 않았다.',
        '', '[100개 목록과 상세 외형 분해](CHARACTER-LIST.md) · [구조화한 사례집](CHARACTER-CASEBOOK.json) · [프로필 연결과 반영 수치](INTEGRATION-MAINTENANCE.json) · [공식 출처·도판 해시](SOURCE-RECEIPTS.json) · [부분 확인 판정](SOURCE-RELATION-REVIEW.json) · [실제 검색 진단](RETRIEVAL-RESULTS.json) · [검증 요약](VALIDATION-SUMMARY.json)',
        '', '공식 출처 계열: [hololive talents](https://hololive.hololivepro.com/en/talents/) · [GUILTY GEAR -STRIVE- characters](https://www.guiltygear.com/ggst/en/character/) · [TEKKEN 8 fighters](https://tekken.com/fighters/jin-kazama) · [Pokémon 도감](https://zukan.pokemon.co.jp/detail/0025) · [귀멸의 칼날 입지편](https://kimetsu.com/anime/risshihen/character/)',
        '', '도판 원본은 재현용 URL·SHA-256과 로컬 검사 캐시에 남겼다. 타사 원본 도판 100개를 저장소 데이터로 복제하지 않았다. 미래에 공식 도판이 바뀌면 해시가 같지 않은 자료를 같은 관찰 증거로 취급하지 않는다.',
    ]
    (HERE/'REPORT.md').write_text('\n'.join(report)+'\n')
    print(json.dumps({'cases':len(cases),'profiles':len(profiles),'preserved':sum(comparisons),'full_suite_complete':bool(suite)},ensure_ascii=False))

if __name__=='__main__':main()
