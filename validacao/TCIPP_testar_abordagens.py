#!/usr/bin/env python3
"""
TCIPP_testar_abordagens.py — Teste de Abordagens de Score
"""

import itertools
import pandas as pd
import numpy as np

DIMENSOES = [1, 2, 3, 4, 5]

def score_owa(v, pesos):
    v_ord = sorted(v)
    return sum(w * x for w, x in zip(pesos, v_ord))

def score_media(v):
    return sum(v) / len(v)

def score_hibrido(v, alpha):
    return alpha * min(v) + (1 - alpha) * score_media(v)

def analisar(nome, score_func):
    all_v = list(itertools.product(DIMENSOES, repeat=5))
    scores = [score_func(v) for v in all_v]
    
    df = pd.DataFrame({'vector': all_v, 'score': scores})
    df = df.sort_values('score').reset_index(drop=True)
    df['level'] = (df.index // 625) + 1
    
    print(f"\n{'='*80}")
    print(f"📊 {nome}")
    print(f"{'='*80}")
    print(f"Score: min={min(scores):.4f}, max={max(scores):.4f}, média={np.mean(scores):.4f}")
    print(f"Score ≤ 3.00: {sum(1 for s in scores if s <= 3.00)} vetores")
    print(f"Score ≤ 3.84: {sum(1 for s in scores if s <= 3.84)} vetores")
    
    print("\nLimiares:")
    for i in range(5):
        inicio = i * 625
        fim = (i+1) * 625 - 1
        print(f"  Nível {i+1}: [{df.iloc[inicio]['score']:.4f}, {df.iloc[fim]['score']:.4f}]")
    
    print("\nCasos críticos:")
    casos = {
        '[1,1,1,1,1]': (1,1,1,1,1),
        '[1,5,1,5,1]': (1,5,1,5,1),
        '[2,2,2,2,2]': (2,2,2,2,2),
        '[3,3,3,3,3]': (3,3,3,3,3),
        '[4,4,4,4,4]': (4,4,4,4,4),
        '[5,5,5,5,5]': (5,5,5,5,5),
    }
    for nome_caso, v in casos.items():
        row = df[df['vector'] == v]
        if len(row) > 0:
            level = row.iloc[0]['level']
            score = row.iloc[0]['score']
            print(f"  {nome_caso}: score={score:.4f}, nível={level}")

analisar("OWA [0.40, 0.25, 0.15, 0.12, 0.08]", lambda v: score_owa(v, [0.40, 0.25, 0.15, 0.12, 0.08]))
analisar("OWA [0.25, 0.22, 0.20, 0.18, 0.15]", lambda v: score_owa(v, [0.25, 0.22, 0.20, 0.18, 0.15]))
analisar("Média aritmética", score_media)
analisar("Híbrido α=0.3", lambda v: score_hibrido(v, 0.3))
analisar("Híbrido α=0.5", lambda v: score_hibrido(v, 0.5))