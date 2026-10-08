"""Validate research references and preservation; no runtime/test/image execution."""
import collections
import csv
import hashlib
import json
import re
import stat
import subprocess
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]


def read(name):return json.loads((OUT/name).read_text())


def main():
    errors=[]; warnings=[]; checks=[]
    def check(condition,label):
        checks.append(dict(check=label,passed=bool(condition)))
        if not condition:errors.append(label)

    receipt=read('reference/SOURCE-RECEIPT.json');raw=(OUT/'reference/keyword-inventory.tsv').read_bytes()
    inventory=list(csv.DictReader(raw.decode().splitlines(),delimiter='\t'))
    ids={r['id']:r for r in inventory}
    check([r['id'] for r in inventory]==[f'H{i:03d}' for i in range(1,455)],'all 454 original H IDs in order')
    check(dict(collections.Counter(r['category'] for r in inventory))==receipt['category_counts'],'all 20 category counts')
    expected=next(q for q in receipt['retrieval'] if q.get('artifact')=='keyword-inventory.tsv')
    check(hashlib.sha256(raw).hexdigest()==expected['local_sha256'],'transcribed inventory SHA256')
    combos=list(csv.DictReader((OUT/'reference/character-combinations.tsv').open(),delimiter='\t'))
    check([r['id'] for r in combos]==[f'R{i:02d}' for i in range(1,49)],'48 original creative combination IDs')

    import assemble_research as assembly
    cards=[];sources=[]
    for prefix in assembly.PREFIXES:
        d=read(prefix+'-cards.json');cards.extend(d['cards']);sources.extend(read(prefix+'-sources.json')['sources'])
        for c in d['cards']:
            check(bool(c.get('namespace')) and bool(c.get('domain')),'card scope '+c['id'])
            check(bool(c.get('minimum_visible_signature',c.get('minimum_signature',c.get('minimum_visual_signature')))),'card signature '+c['id'])
            for hid in assembly.keyword_ids(c):check(hid in ids,'card original ID '+c['id']+':'+hid)
            for field in ['reference_keywords','input_keywords']:
                for q in c.get(field,[]):
                    if not isinstance(q,dict):continue
                    hid=q['id'];check(q.get('ko_original',q.get('ko'))==ids[hid]['ko'],'original Korean '+c['id']+':'+hid)
                    check(q.get('en_original',q.get('en'))==ids[hid]['en'],'original English '+c['id']+':'+hid)
    bycard={c['id']:c for c in cards};bysource={s['id']:s for s in sources}
    check(len(bycard)==len(cards),'unique research card IDs')
    check(len(bysource)==len(sources),'unique source record IDs')
    for c in cards:
        for sid in assembly.source_ids(c):check(sid in bysource,'source reference '+c['id']+':'+str(sid))

    rows=read('RESEARCH-CROSSWALK.json')['rows']
    check([r['id'] for r in rows]==list(ids),'all H rows routed')
    for r in rows:
        check(r['runtime_adoption']=='not_performed','no adoption claim '+r['id'])
        for cid in r['semantic_card_refs']:check(cid in bycard,'crosswalk card ref '+r['id']+':'+cid)

    drafts=read('CANDIDATE-DRAFTS.json')['drafts'];allowed={'id','ko','en','concept_units','relations','affected_dimensions','affected_properties'}
    runtime_ids=[]
    for d in drafts:
        e=d['runtime_entry_draft'];runtime_ids.append((d['proposed_slot'],e['id']))
        check(set(e)<=allowed,'draft runtime key shape '+e['id'])
        check(d['semantic_card_ref'] in bycard,'draft semantic ref '+e['id'])
        check(all(i in ids for i in d['reference_keyword_ids']),'draft glossary IDs '+e['id'])
        for q in e['relations']:check(set(q)=={'id','type','subject','object'} and all(q.values()),'draft relation shape '+e['id'])
        for q in e['affected_properties']:check(set(q)=={'dimension','target','property'} and q['dimension']=='appearance' and q['target']=='main_subject','draft effect shape '+e['id'])
        check(d['status']=='proposal_not_inserted','draft has no adoption claim '+e['id'])
    check(len(set(runtime_ids))==len(runtime_ids),'unique candidate draft slot/IDs')
    families=read('PROFILE-AND-BUNDLE-PLAN.json')['families']
    for b in families:
        check(all(i in bycard for i in b['semantic_card_refs']),'family card refs '+b['id'])
        check(b['activation']=='association_does_not_create_hard_activation','family activation boundary '+b['id'])
    cases=[json.loads(q) for q in (OUT/'VALIDATION-CASES.jsonl').read_text().splitlines() if q]
    check(len({q['id'] for q in cases})==len(cases),'unique proposed case IDs')
    check(all(q['status']=='proposed_not_run' for q in cases),'all cases unexecuted')
    for q in cases:
        for hid in q.get('glossary_ids',[]):check(hid in ids,'boundary case input ID '+q['id'])

    snapshot=read('runtime-inquiry-snapshot.json');changed=[];missing=[]
    for q in snapshot['files']:
        p=ROOT/q['path']
        if not p.is_file():missing.append(q['path']);continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=q['sha256'] or stat.S_IMODE(p.stat().st_mode)!=q['mode']:changed.append(q['path'])
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    check(not missing,'inquiry snapshot files were not removed')
    source_drift=[]
    for q in read('CURRENT-DATA-AUDIT.json')['source_hashes']:
        p=ROOT/'skills/photo-prompt-image-generator/assets'/q['file']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=q['sha256']:source_drift.append(q['file'])
    check(not source_drift,'authored sources used for the audit retain their bytes')
    # Shared checkout updates are observations, never silently restored or ignored.
    intervening=[]; descendant=None
    if head!=snapshot['head']:
        descendant=subprocess.run(['git','merge-base','--is-ancestor',snapshot['head'],head],cwd=ROOT,capture_output=True).returncode==0
        intervening=subprocess.check_output(['git','log','--format=%h %s',snapshot['head']+'..'+head],cwd=ROOT,text=True).splitlines()
        warnings.append('HEAD advanced during research; the observed commit(s) are recorded. This research did not create a commit.')
    if changed:warnings.append('Two or more scoped snapshot files changed concurrently; see preservation paths. No restoration was attempted.')
    summary=read('ASSEMBLY-SUMMARY.json')
    check(summary['semantic_cards']==len(cards) and summary['candidate_drafts']==len(drafts) and summary['case_count']==len(cases),'final assembly counts')
    check(all(s['normalized_read_status']!='unknown' for s in read('SOURCE-CATALOG.json')['sources']),'source read statuses are explicit')

    # Structural linking alone cannot certify definition quality or image quality.
    warnings.extend(['454 input routes are not 454 independent primary definitions.',
        'Research card geometry and runtime-shaped drafts remain author proposals.',
        'Source-photo pixels, live activation, ranker, final selected prompt, native pixels and acceptance are not run.',
        'Preservation snapshot starts after research-folder creation; it is not an initial whole-workspace backup.'])
    result=dict(status=('passed_with_concurrent_workspace_changes' if changed or head!=snapshot['head'] else 'passed') if not errors else 'failed',checks=len(checks),passed=sum(c['passed'] for c in checks),
        errors=errors,warnings=warnings,counts=summary,
        preservation=dict(captured_at=snapshot['captured_at'],file_count=len(snapshot['files']),unchanged_count=len(snapshot['files'])-len(changed)-len(missing),changed=changed,missing=missing,authored_source_drift=source_drift,head_before=snapshot['head'],head_after=head,head_is_descendant=descendant,intervening_commits=intervening,assessment='observed_shared_checkout_drift_not_overwritten' if changed or intervening else 'snapshot_unchanged'),
        proof_boundary='Research structure/provenance/reference and scoped preservation only; no production loader or quality test execution.')
    (OUT/'RESEARCH-VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))
    if errors:raise SystemExit(1)

    report=ROOT/'docs/researches/2026-10-08-character-hair-visual-semantics.md'
    s=report.read_text();counts=summary['source_counts']
    content=(f"最終 집계: **의미 카드 {len(cards)}개**, 전체 **454개 처리 경로**, 그중 {summary['terms_with_detailed_card_links']}개 입력에 상세 카드 연결, "
             f"**후보 초안 {len(drafts)}개**, **프로필·번들 설계 {len(families)}개**, "
             f"**대조 설계 {summary['controlled_minimal_pairs']}개 + 경계 사례 {summary['additional_boundary_cases']}개**다. 모두 연구 산출물이며 production 채택 수가 아니다.\n\n"
             f"출처 레코드는 {counts['source_records']}개이며 직접 본문/API {counts['current_direct_body_or_api_records']}개와 "
             f"검색·접근 제한 {counts['limited_or_search_only_records']}개를 구분했다. 중복을 정규화한 URL 문자열은 {counts['unique_url_strings']}개다. "
             "플랫폼 위키의 여러 문서를 묶은 레코드가 있어 레코드 수와 페이지 수가 다르다. 이 숫자는 독립 기관 수나 모든 명칭의 검증 수가 아니다.")
    content=content.replace('最終','최종')
    s=re.sub(r'(?s)(<!-- ASSEMBLY-STATS:START -->).*?(<!-- ASSEMBLY-STATS:END -->)',lambda m:m[1]+'\n'+content+'\n'+m[2],s)
    report.write_text(s)


if __name__=='__main__':main()
