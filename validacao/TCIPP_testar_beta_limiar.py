#!/usr/bin/env python3
"""
TCIPP_testar_beta_limiar.py — Teste de Combinações β e Limiar

Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026

OBJETIVO:
Testar combinações de β e primeiro limiar t que satisfaçam:
- [1,5,1,5,1] → Nível 1
- [2,2,2,2,2] → Nível 2
- Monotonicidade preservada
- Distribuição saudável
"""

import itertools
import pandas as pd
import numpy as np
from datetime import datetime

DIMENSOES = [1, 2, 3, 4, 5]
# Limiares fixos: N2/N3, N3/N4, N4/N5
LIMIARES_FIXOS = [2.5, 3.5, 4.5]

def calcular_score(v, beta):
    media = sum(v) / len(v)
    gargalo = max(0, 3 - min(v))
    return media - beta * gargalo

def classificar(score, t):
    if score < t:
        return 1
    elif score < LIMIARES_FIXOS[0]:
        return 2
    elif score < LIMIARES_FIXOS[1]:
        return 3
    elif score < LIMIARES_FIXOS[2]:
        return 4
    else:
        return 5

def validar_monotonicidade(vector_to_level, all_vectors):
    violations = 0
    for vA in all_vectors:
        lvlA = vector_to_level[vA]
        for i in range(5):
            if vA[i] < 5:
                vB = list(vA)
                vB[i] += 1
                vB = tuple(vB)
                lvlB = vector_to_level[vB]
                if lvlB < lvlA:
                    violations += 1
    return violations

def testar_combinacao(beta, t):
    """Testa uma combinação de β e t."""
    all_vectors = list(itertools.product(DIMENSOES, repeat=5))
    
    df = pd.DataFrame({
        'vector': all_vectors,
        'score': [calcular_score(v, beta) for v in all_vectors]
    })
    df['level'] = df['score'].apply(lambda s: classificar(s, t))
    
    vector_to_level = dict(zip(df['vector'], df['level']))
    
    # Verificar casos âncora
    caso_caotico = vector_to_level[(1,5,1,5,1)]
    caso_uniforme = vector_to_level[(2,2,2,2,2)]
    
    # Validar monotonicidade
    violations = validar_monotonicidade(vector_to_level, all_vectors)
    
    # Distribuição
    dist = df['level'].value_counts().sort_index().to_dict()
    
    return {
        'beta': beta,
        't': t,
        'caotico': caso_caotico,
        'uniforme': caso_uniforme,
        'violations': violations,
        'dist': dist,
        'df': df
    }

def main():
    print("=" * 80)
    print("🔬 TCIPP — TESTE DE COMBINAÇÕES β E LIMIAR")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Autor: Neemias da Silva Ferreira")
    print(f"📋 ORCID: 0009-0005-1552-6018")
    print("=" * 80)
    
    print("""
    OBJETIVO:
    Encontrar combinações de β e t que satisfaçam:
    - [1,5,1,5,1] → Nível 1
    - [2,2,2,2,2] → Nível 2
    - Monotonicidade preservada
    """)
    
    # Testar combinações
    combinacoes = []
    
    for beta in [0.65, 0.70, 0.75, 0.80, 0.85, 0.90]:
        for t in [1.25, 1.30, 1.35, 1.40, 1.45, 1.50]:
            resultado = testar_combinacao(beta, t)
            combinacoes.append(resultado)
    
    # Filtrar combinações válidas
    validas = [c for c in combinacoes 
               if c['caotico'] == 1 
               and c['uniforme'] == 2 
               and c['violations'] == 0]
    
    print(f"\n📊 COMBINAÇÕES TESTADAS: {len(combinacoes)}")
    print(f"📊 COMBINAÇÕES VÁLIDAS: {len(validas)}")
    
    if validas:
        print("\n📊 COMBINAÇÕES QUE SATISFAZEM OS REQUISITOS:")
        print(f"\n   {'β':<8} {'t':<8} {'Caótico':<10} {'Uniforme':<10} {'Violações':<12}")
        print(f"   {'-'*8} {'-'*8} {'-'*10} {'-'*10} {'-'*12}")
        
        for c in validas:
            print(f"   {c['beta']:<8.2f} {c['t']:<8.2f} {c['caotico']:<10} {c['uniforme']:<10} {c['violations']:<12}")
        
        # Mostrar distribuição da primeira combinação válida
        print("\n📊 DISTRIBUIÇÃO DA PRIMEIRA COMBINAÇÃO VÁLIDA:")
        c = validas[0]
        print(f"\n   β = {c['beta']}, t = {c['t']}")
        for nivel in sorted(c['dist'].keys()):
            freq = c['dist'][nivel]
            pct = freq / 3125 * 100
            print(f"   Nível {nivel}: {freq} vetores ({pct:.1f}%)")
    else:
        print("\n❌ NENHUMA COMBINAÇÃO VÁLIDA ENCONTRADA")
        print("\n   Vamos analisar por que:")
        for c in combinacoes[:10]:
            print(f"   β={c['beta']}, t={c['t']}: caótico=N{c['caotico']}, uniforme=N{c['uniforme']}, violações={c['violations']}")

if __name__ == "__main__":
    main()