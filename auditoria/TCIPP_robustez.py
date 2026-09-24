#!/usr/bin/env python3
"""
TCIPP_robustez.py — Auditoria de Robustez

Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026

OBJETIVO:
Testar casos extremos, empates, fronteiras, simetria e invariância.
"""

import itertools
import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter

# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

DIMENSOES = [1, 2, 3, 4, 5]
BETA = 0.5
LIMIARES = [1.5, 2.5, 3.5, 4.5]

# =============================================================================
# FUNÇÕES
# =============================================================================

def calcular_score(v):
    media = sum(v) / len(v)
    gargalo = max(0, 3 - min(v))
    return media - BETA * gargalo

def classificar(score):
    if score < LIMIARES[0]:
        return 1
    elif score < LIMIARES[1]:
        return 2
    elif score < LIMIARES[2]:
        return 3
    elif score < LIMIARES[3]:
        return 4
    else:
        return 5

# =============================================================================
# TESTES DE ROBUSTEZ
# =============================================================================

def testar_casos_extremos():
    """Testa casos extremos."""
    print("\n📊 CASOS EXTREMOS")
    print("=" * 80)
    
    casos = {
        "[1,1,1,1,1] (Degenerado)": (1,1,1,1,1),
        "[5,5,5,5,5] (Excelente)": (5,5,5,5,5),
        "[1,5,1,5,1] (Caótico)": (1,5,1,5,1),
        "[5,1,5,1,5] (Caótico invertido)": (5,1,5,1,5),
        "[1,1,1,1,5] (Gargalo extremo)": (1,1,1,1,5),
        "[5,5,5,5,1] (Gargalo isolado)": (5,5,5,5,1),
        "[2,2,2,2,2] (Ruim uniforme)": (2,2,2,2,2),
        "[3,3,3,3,3] (Médio uniforme)": (3,3,3,3,3),
        "[4,4,4,4,4] (Bom uniforme)": (4,4,4,4,4),
    }
    
    for nome, v in casos.items():
        score = calcular_score(v)
        nivel = classificar(score)
        print(f"   {nome}: score={score:.4f}, nível={nivel}")

def testar_empates():
    """Testa vetores com o mesmo score."""
    print("\n📊 EMPATES")
    print("=" * 80)
    
    all_vectors = list(itertools.product(DIMENSOES, repeat=5))
    scores = [calcular_score(v) for v in all_vectors]
    
    # Contar frequência de cada score
    score_counts = Counter([round(s, 4) for s in scores])
    
    # Encontrar scores com mais empates
    mais_empates = sorted(score_counts.items(), key=lambda x: -x[1])[:5]
    
    print("\n   Top 5 scores com mais empates:")
    for score, count in mais_empates:
        print(f"      Score {score:.4f}: {count} vetores")
    
    # Verificar se vetores com mesmo score têm mesmo nível
    df = pd.DataFrame({'vector': all_vectors, 'score': scores})
    df['score_round'] = df['score'].round(4)
    df['level'] = df['score'].apply(classificar)
    
    inconsistencias = 0
    for score, group in df.groupby('score_round'):
        if len(group['level'].unique()) > 1:
            inconsistencias += 1
    
    print(f"\n   Scores com níveis inconsistentes: {inconsistencias}")
    if inconsistencias == 0:
        print("   ✅ Todos os vetores com mesmo score têm mesmo nível!")

def testar_fronteiras():
    """Testa vetores exatamente nos limiares."""
    print("\n📊 FRONTEIRAS")
    print("=" * 80)
    
    all_vectors = list(itertools.product(DIMENSOES, repeat=5))
    
    for limiar in LIMIARES:
        vetores_limiar = [v for v in all_vectors if abs(calcular_score(v) - limiar) < 0.0001]
        if vetores_limiar:
            print(f"\n   Limiar {limiar}: {len(vetores_limiar)} vetores")
            for v in vetores_limiar[:3]:
                score = calcular_score(v)
                nivel = classificar(score)
                print(f"      {v}: score={score:.4f}, nível={nivel}")
        else:
            print(f"\n   Limiar {limiar}: Nenhum vetor exatamente no limiar")

def testar_simetria():
    """Testa se permutações do vetor têm o mesmo score."""
    print("\n📊 SIMETRIA (PERMUTAÇÕES)")
    print("=" * 80)
    
    all_vectors = list(itertools.product(DIMENSOES, repeat=5))
    
    inconsistencias = 0
    exemplos = []
    
    for v in all_vectors:
        score_v = calcular_score(v)
        # Testar permutações
        for perm in set(itertools.permutations(v)):
            score_perm = calcular_score(perm)
            if abs(score_v - score_perm) > 0.0001:
                inconsistencias += 1
                if len(exemplos) < 3:
                    exemplos.append((v, perm, score_v, score_perm))
    
    print(f"\n   Inconsistências de simetria: {inconsistencias}")
    if inconsistencias == 0:
        print("   ✅ Todas as permutações têm o mesmo score!")
    else:
        for v, perm, sv, sp in exemplos:
            print(f"      {v} (score {sv:.4f}) vs {perm} (score {sp:.4f})")

def testar_invariancia_ordem():
    """Testa se o score depende da ordem das dimensões."""
    print("\n📊 INVARIÂNCIA DE ORDEM")
    print("=" * 80)
    
    # O score usa média e min, que são invariantes à ordem
    # Vamos confirmar
    all_vectors = list(itertools.product(DIMENSOES, repeat=5))
    
    inconsistencias = 0
    for v in all_vectors:
        score_original = calcular_score(v)
        v_invertido = tuple(reversed(v))
        score_invertido = calcular_score(v_invertido)
        if abs(score_original - score_invertido) > 0.0001:
            inconsistencias += 1
    
    print(f"\n   Inconsistências de ordem: {inconsistencias}")
    if inconsistencias == 0:
        print("   ✅ O score não depende da ordem das dimensões!")

def testar_intervalo_score():
    """Testa se o score está no intervalo esperado."""
    print("\n📊 INTERVALO DE SCORE")
    print("=" * 80)
    
    all_vectors = list(itertools.product(DIMENSOES, repeat=5))
    scores = [calcular_score(v) for v in all_vectors]
    
    print(f"\n   Score mínimo: {min(scores):.4f}")
    print(f"   Score máximo: {max(scores):.4f}")
    print(f"   Score médio: {np.mean(scores):.4f}")
    print(f"   Score mediano: {np.median(scores):.4f}")
    
    # Verificar se todos os scores estão no intervalo [0, 5]
    fora_intervalo = [s for s in scores if s < 0 or s > 5]
    print(f"\n   Scores fora do intervalo [0, 5]: {len(fora_intervalo)}")
    if len(fora_intervalo) == 0:
        print("   ✅ Todos os scores estão no intervalo [0, 5]!")

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("🔬 TCIPP — AUDITORIA DE ROBUSTEZ")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Autor: Neemias da Silva Ferreira")
    print(f"📋 ORCID: 0009-0005-1552-6018")
    print("=" * 80)
    
    print(f"""
    FUNÇÃO DE SCORE:
    S(x) = média(x) - {BETA} * max(0, 3 - min(x))
    
    LIMIARES: {LIMIARES}
    """)
    
    # Executar testes
    testar_casos_extremos()
    testar_empates()
    testar_fronteiras()
    testar_simetria()
    testar_invariancia_ordem()
    testar_intervalo_score()
    
    # Veredicto parcial
    print("\n" + "=" * 80)
    print("🏆 VEREDICTO PARCIAL — ROBUSTEZ")
    print("=" * 80)
    print("   ✅ Análise concluída. Ver resultados acima.")
    print("=" * 80)

if __name__ == "__main__":
    main()