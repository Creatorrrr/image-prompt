"""One fixed document-arm comparison; no recipe/threshold tuning."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4];E=Path(__file__).parent
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
from photo_candidate_authoring import read,write

if __name__=='__main__':
    a=read(E/'RESULT-D1.json')['metrics'];b=read(E/'RESULT-D1b.json')['metrics']
    eligible=b['retrieved_positive_pairs']>=a['retrieved_positive_pairs'] and b['goals_with_positive_at_k']>=28
    better=(b['retrieved_positive_pairs'],b['goals_with_positive_at_k'])>(a['retrieved_positive_pairs'],a['goals_with_positive_at_k'])
    selected='D1b' if eligible and better else 'D1'
    winner=a if selected=='D1' else b
    result={'selected':selected,'D1b_eligible':eligible,'D1b_strictly_better':better,
            'FIT8':winner['retrieved_positive_pairs'],'goals8':winner['goals_with_positive_at_k'],
            'run_Q1':winner['retrieved_positive_pairs']<62 or winner['goals_with_positive_at_k']<28,
            'rule':'FIT8, goals8, simplicity; reject D1b below D1 FIT or A28 goals; one recipe only'}
    write(E/'SELECTED-DOCUMENTS.json',result);print(result)
