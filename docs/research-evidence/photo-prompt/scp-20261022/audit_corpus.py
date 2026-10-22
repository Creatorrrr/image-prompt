"""Snapshot lexical evidence and selected full neighbors, without runtime imports."""
import hashlib,json,pathlib,re,collections
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def sha(b):return hashlib.sha256(b).hexdigest()
def text(v):return v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,sort_keys=True)
def main():
    manifest_bytes=(ASSETS/'photo_candidate_corpus_manifest.json').read_bytes()
    manifest=json.loads(manifest_bytes); rows=[];bindings=[];module_hashes={}
    for m in manifest['modules']:
        raw=(ASSETS/m['file']).read_bytes();module_hashes[m['file']]=sha(raw);d=json.loads(raw)
        if m['kind']=='candidates':
            items=d['candidates']; items=items.items() if isinstance(items,dict) else ((x['id'],x) for x in items)
            for cid,c in items:rows.append((cid,c,m['file']))
        elif m['kind']=='slot_bindings':
            seq=d['slot_bindings']; seq=seq.values() if isinstance(seq,dict) else seq
            bindings.extend(dict(b,source_module=m['file']) for b in seq)
    patterns={
      'scp_literal':r'\bSCP\b','containment':r'containment|격리','airlock':r'airlock|에어록',
      'observation_window':r'observation window|관찰창','hazmat':r'hazmat|방호복',
      'glove_port':r'glove.?port|장갑.?포트','cognitive_context':r'cognitohazard|인식재해',
      'antimeme_context':r'antimem|항밈','reality_anchor':r'reality anchor|현실성 닻|스크랜턴',
      'redaction':r'redact|검열|가림','non_euclidean':r'non.euclidean|비유클리드',
      'specimen':r'specimen|시료|표본','surveillance':r'surveillance|감시',
      'ritual':r'ritual|의식 도형','vial':r'\bvial|앰풀','corrosion':r'corrosion|부식',
      'tissue_machine_join':r'biomechanical|tissue.*conduit|생체.*접합',
      'reflection_mismatch':r'reflection.*mismatch|반사.*불일치',
      'threshold_space':r'non-Euclidean space folding|threshold|문턱',
      'numbered_coverall':r'numbered.*(?:jumpsuit|coverall)|번호.*작업복',
      'false_color_display':r'false.colou?r|의사색',
      'korean_named':r'무진|국가초상|서천컨트리|삼대천|세을가|플러그소프트|NPES|Mujin|Seocheon',
    }
    results={}
    for name,pat in patterns.items():
        matches=[]
        for cid,c,f in rows:
            content=c['content']; parts={k:text(content[k]) for k in ('en','ko','additional_details') if k in content}
            hits={k:re.findall(pat,v,re.I) for k,v in parts.items() if re.search(pat,v,re.I)}
            if hits:matches.append({'candidate_id':cid,'source_module':f,'matched_fields':list(hits),'en':content.get('en'),'record_kind':c['record_kind']})
        results[name]={'pattern':pat,'count':len(matches),'matches':matches}
    binding_by_id=collections.defaultdict(list)
    for b in bindings:binding_by_id[b['candidate_id']].append(b)
    # Exact reviewed neighbors; these are not retrieval output or automatically approved reuse.
    selected={
      'cand_8a3f213b6dbc5cb0bc823f5782e6ca1c':('reuse_first','I01','glazed barrier, room door, viewing window and access point already share the same boundary; preserve full owner/conditions/effects'),
      'cand_c7591cee5fb55aba87ba657862b2a9da':('refine_or_reuse','I01,I06','existing limiter/output path is not a sealed room or viewing window'),
      'cand_ae81ae6d5f9450d0bba77c0ba07d7f59':('context_reuse','I12,G01','modern investigation/containment situation; no barrier topology'),
      'cand_3bcf055a0fc65bc086785a701bedfa28':('reuse_first','I08','page/lines/occluding bars already explicit; preserve all source conditions and obligations'),
      'cand_a7f1e74071375d87a59a7181fe761301':('context_reuse','C01,C04,C06','context-only information hazards; never promote to a visible hazardous pattern'),
      'cand_5d9b5604b9405b90b3b119b99954d247':('context_reuse','R04','keeps mathematical/SCP/metaphorical meanings separate'),
      'cand_2e98a153e36f57cca7a9733d296aed72':('refine_review','R03,R04','short space-folding source; inspect full source before adding endpoints or guarantees'),
      'cand_9f862c77561e56a99671ffa3103563f1':('context_reuse','R04','liminal non-Euclidean context must remain distinct from selected topology'),
      'cand_a747319a8c415515a409692400479d8b':('reuse_neighbor','F02,F04,B01','tissue/conduit interface; not two-body fusion or every prosthesis'),
      'cand_cd64e64632545afa870ebf36324ce112':('reuse_neighbor','F02,F04,B01','continuous tissue-to-conduit taper; preserve owner and branch'),
      'cand_22fce7248cc35990b2b431cbbeb8cac0':('reuse_first','T01','adult gesture and bounded ritual center already exist; magic efficacy remains context'),
      'cand_d200a9be7ad457e2a8c0b8e65e68d35d':('near_miss','C05','storm-glass crystals are not a medicine ampoule; no drug efficacy'),
      'cand_72301a3a73cc5b0dbfb253e4ad3618eb':('near_miss','C05','herbs/blank vials lack sealed neck and capped syringe topology'),
      'cand_9f1cf92a74fc5cefba13dd6720b2f0ca':('near_miss','R01,R02','marine manifold is not a Kant counter/SRA'),
      'cand_313088e0690a56688ea5e89ee2577058':('do_not_borrow_context','F04,B01','sexualized form context cannot be imported from anatomical resemblance'),
    }
    snapshots=[];missing=[]
    for cid,(decision,cards,reason) in selected.items():
        found=next(((c,f) for x,c,f in rows if x==cid),None)
        if not found:missing.append(cid);continue
        c,f=found;snapshots.append({'candidate_id':cid,'source_module':f,'source_sha256':sha(json.dumps(c,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()),'module_sha256':module_hashes[f],'record':c,'bindings':binding_by_id[cid],'suggested_disposition':decision,'related_cards':cards.split(','),'review_reason':reason,'native_adoption':'not_run'})
    post_drift=[f for f,h in module_hashes.items() if not (ASSETS/f).exists() or sha((ASSETS/f).read_bytes())!=h]
    if sha((ASSETS/'photo_candidate_corpus_manifest.json').read_bytes())!=sha(manifest_bytes):post_drift.append('photo_candidate_corpus_manifest.json')
    report={'schema':'scp-research-lexical-audit/v1','captured_on':'2026-10-22','candidate_count':len(rows),'record_kinds':dict(collections.Counter(c['record_kind'] for _,c,_ in rows)),'module_count':len(manifest['modules']),'source_module_sha256':module_hashes,'manifest_sha256':sha(manifest_bytes),'snapshot_changed_during_read':post_drift,'bindings':len(bindings),'primary_fields':['content.en','content.ko','content.additional_details'],'exclusions':'tags, metadata, conditions, obligations, and native proof are not used as lexical match evidence','meaning_limit':'Exact pattern matches only. Zero does not establish semantic absence; count is not rank, eligibility, exposure, adoption or quality.','patterns':results,'selected_missing_ids':missing}
    (HERE/'CORPUS-LEXICAL-AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (HERE/'existing-source-mapping.json').write_text(json.dumps(snapshots,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'candidates':len(rows),'kinds':report['record_kinds'],'mappings':len(snapshots),'missing':missing,'counts':{k:v['count'] for k,v in results.items()}},ensure_ascii=False))
if __name__=='__main__':main()
