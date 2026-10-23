from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
DECISIONS = [
('cand_5273e2e9e22652348ea5981e42f63d1f','scope_refine','세 명 이상과 성인 조건을 유지하는 특정 대안. 하렘 일반의 정의나 모든 요청의 강제 인원수로 재사용하지 않는다.'),
('cand_e599382b585b546a911e97403b4b2d51','reuse_only_selected_rivalry','동일한 제한 선택을 두고 세 후보 이상이 경쟁한다는 전체 조건이 맞는 경우에만 심사. 비경쟁·삼각관계 요청에는 부적합.'),
('cand_ba4dbcec79cf5424b734e7e5b3f4a049','effects_and_endpoints_review','같은 수신자와 세 소품을 도입한다. 효과 배열이 비어 있어도 물건·개수·제안 방향이 생긴다는 사실을 검토해야 한다. 선물만으로 romantic을 증명하지 않는다.'),
('cand_3830eb2f0276579d918ce1d61414971a','reuse_only_selected_rivalry','mutually incompatible와 same time/place/opportunity를 보존해야 한다. 새 일반 하렘 후보의 기본값으로 복사하지 않는다.'),
('cand_4efc43a5c88a5a7588af8be91ed81a73','role_review','현재의 겹친 손·보류 동작과 aftermath_trace의 과거 사건 흔적 요건이 맞는지 검토. binding의 allow-domain 조건을 우회하지 않는다.'),
('cand_ed1be097a436570a8a9227ff0392db76','role_and_tone_review','현재 진행 중인 동시 제안과 aftermath_trace 구분. sensual 태그가 단독으로 관능을 추가하지 않게 확인. 빈 effects는 보존 증거가 아니다.'),
('cand_40f82b875ed154adb1dae24bb19a5405','medium_scope_review','비중첩 사건 배경·세 route figure 이상을 쓰는 키아트 대안. 물리적 같은 방·동시 교제에 재사용하지 않는다.'),
('cand_865a5df45ea355d9a23dfedf859dab5a','role_review','선택되지 않은 경로의 병렬 제시와 실제 사건 뒤 흔적은 다르다. no pair finalized는 결말의 증명이 아니다.'),
('cand_1b4b2fd9a03a58dcad9e2978f7925027','reuse_only_explicit_restage','19세기 유럽 오리엔탈리즘 회화의 비판적 성인 재연이라는 문맥을 보존. 실제 역사 하렘·현대 로맨스와 합치지 않는다.'),
('cand_7a5dc50e968f592188aa5372876695e4','context_plus_visible_alternative','worry masked as irritation은 내면·숨김을 포함한다. 직접 표정 증거와 문맥 분리; 단순 홍조로 성격을 확정하지 않는다.'),
('cand_a514fac63aeb5377a6f4a32985db090a','context_preserve','불평으로 위장한 도움은 문맥/의도. 말의 청각 증거와 숨긴 의도를 정지 사진의 직접 사실로 승격하지 않는다.'),
('cand_bad4cd47f48c5b0ba848b8829bbeaff2','temporal_refine','도와준 직후는 전 사건과 순서를 전제. 이미 도움을 마친 관계가 core에서 주어졌는지 확인하거나 현재 공존하는 제스처 대안으로 분리한다.'),
('cand_522c907a6a97547886a2d207a4138b03','bilingual_refine','영문 handkerchief OR charm, 한글 손수건 AND 참으로 대안/개수 불일치. held out 동작도 한글에 없다. 선택지별 완결 한영 대안으로 정밀화한다.'),
('cand_d2834908636b578489498652230bafd9','owner_scope_no_direct_reuse','paraphrases와 contextual_usage는 같은 사람의 두 손을 가리킨다. H07 두 사람 깍지에 그대로 재사용하면 소유자가 바뀐다. 같은 사람 손깍지는 유지하고 다른 owner 대안을 별도 심사. 한글 두 손가락 표현도 교정 검토.'),
('cand_ae856dfccef0599eb2db1c6ba565e112','reuse_or_bilingual_refine','영문은 허리 지지부·끈·아래 클립·같은 스타킹 윗단·별도 경계를 담고 한글은 짧다. 원래 primary/adult 조건 전체를 유지하며 W17의 2끈 대안과 개수 차이를 심사한다.'),
('cand_909113fba8195d4d8ab1d2b14060ec8d','reuse_review','컵 경계→같은 긴 몸판의 연결과 기존 의복 주인·appearance 효과를 보존할 때 재사용 우선. W13의 짧은 몸판과 동일한 전체 대안인지는 별도 판단.'),
('cand_66191177f598566baa5e3cecce76422c','non_equivalent_variant','가터가 뷔스티에에 붙은 대안은 독립 허리벨트에 붙은 W17과 소유 의복·연결점이 다르다. 가터벨트의 동의어로 병합하지 않는다.'),
('cand_f7a9fcedc7de5792ba4ae6940a0f64d7','reuse_component_review','세로 보강 채널만으로 busk·뒤 끈·별도 속옷·강한 압박을 추가하지 않는다. W12 전체 실현과 일치하려면 나머지 구조의 직접 근거가 필요하다.'),
]

def build():
 s=json.loads((HERE/'corpus-snapshot.json').read_text()); rows={x['candidate_id']:x for x in s['matches']}
 out=[]
 for cid,decision,reason in DECISIONS:
  assert cid in rows,cid
  out.append(dict(**rows[cid],research_decision=decision,reason=reason,runtime_change_performed=False,native_status='NOT_RUN'))
 (HERE/'existing-source-decisions.json').write_text(json.dumps(dict(schema='harem-existing-source-decisions/v1',decisions=out),ensure_ascii=False,indent=2)+'\n')
 md=['# 기존 데이터 진단','',f"Manifest {len(s['modules'])}모듈, 후보 {s['candidate_count']:,}개, binding {s['binding_count']:,}개, slot {s['slot_count']}개를 읽었다. 지정 flat content 어휘의 일치 레코드 {s['match_count']}개를 전체 원문/조건/효과/binding과 함께 보존했다.",'',
  '어휘 건수는 의미 coverage나 실제 검색 성능이 아니다. 특히 contact 2건은 지정한 영어·한국어 일부 문자열의 결과이며 다른 표현의 포즈가 없다는 뜻이 아니다. nested research/embedding만의 일치는 제외했다.','',
  '|ID|영문 원문|현재 role|판정|이유|','|---|---|---|---|---|']
 for r in out:
  en=r['record']['content'].get('en','').replace('|','/');roles=', '.join(b['slot_id'] for b in r['bindings'])
  md.append(f"|{r['candidate_id']}|{en}|{roles}|{r['research_decision']}|{r['reason']}|")
 md += ['', '## 일러스트레이션 경로','',f"두 의미 자산에서 넓은 지정 어휘에 걸린 이웃 {len(s['illustration_neighbors'])}개를 보존했다. 이 수는 하렘 직접 후보 수가 아니다. 기존 moe_ntr_relationship_displacement, moe_yandere_obsession을 확인했으며 해당 정의·기존 alias typing·v5/v7 의미 binding을 별도 심사한다.",'',
  'photo의 flat CID/binding을 illustration grammar에 그대로 이식하지 않는다. 불변 v1 의미를 변경할 이유가 생기면 호환 확장/마이그레이션으로 설계한다. 현재 이웃 읽기는 실제 v7 실행이나 NTR/얀데레의 완전 검증이 아니다.','',
  '## 후속 심사 범위','', '각 레코드의 완전 JSON은 existing-source-decisions.json에 있다. 스냅샷 이후 동시 작업의 변경은 최종 VALIDATION에 기록하며 구현 직전 현재 source를 다시 읽는다. 단순한 기존 CID 존재·태그·빈 effects를 승인으로 취급하지 않는다.']
 (HERE/'CORPUS-FINDINGS.md').write_text('\n'.join(md)+'\n')

if __name__=='__main__': build()
