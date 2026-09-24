#!/usr/bin/env python3
"""
TCIPP_comparar_beta.py — Comparação de β

Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026

OBJETIVO:
Comparar o comportamento do TCIPP com diferentes valores de β.
"""

import itertools
import pandas as pd
import numpy as np
from datetime import datetime

DIMENSOES = [1, 2, 3, 4, 5]
LIMIARES = [1.5, 2.5, 3.5, 4.5]

def calcular_score(v, beta):
    media = sum(v) / len(v)
    gargalo = max(0, 3 - min(v))
    return media - beta * gargalo

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

def analisar_beta(beta):
    all_v = list(itertools.product(DIMENSOES, repeat=5))
    scores = [calcular_score(v, beta) for v in all_v]
    
    df = pd.DataFrame({'vector': all_v, 'score': scores})
    df['level'] = df['score'].apply(classificar)
    
    return df

def comparar_betas(betas):
    print("=" * 80)
    print("🔬 COMPARAÇÃO DE β")
    print("=" * 80)
    
    all_v = list(itertools.product(DIMENSOES, repeat=5))
    
    # Calcular para cada β
    resultados = {}
    for beta in betas:
        resultados[beta] = analisar_beta(beta)
    
    # Casos críticos
    casos = {
        '[1,1,1,1,1]': (1,1,1,1,1),
        '[1,5,1,5,1]': (1,5,1,5,1),
        '[2,2,2,2,2]': (2,2,2,2,2),
        '[3,3,3,3,3]': (3,3,3,3,3),
        '[4,4,4,4,4]': (4,4,4,4,4),
        '[5,5,5,5,5]': (5,5,5,5,5),
    }
    
    print("\n📊 CASOS CRÍTICOS")
    print(f"\n   {'Caso':<15} {'Média':<8} {'Gargalo':<8}", end="")
    for beta in betas:
        print(f" {'β='+str(beta):<10}", end="")
    print()
    print("   " + "-" * (31 + 10*len(betas)))
    
    for nome, v in casos.items():
        media = sum(v) / len(v)
        gargalo = max(0, 3 - min(v))
        print(f"   {nome:<15} {media:<8.2f} {gargalo:<8.2f}", end="")
        for beta in betas:
            score = calcular_score(v, beta)
            nivel = classificar(score)
            print(f" {score:.2f}→N{nivel:<5}", end="")
        print()
    
    print("\n📊 DISTRIBUIÇÃO")
    for beta in betas:
        df = resultados[beta]
        print(f"\n   β = {beta}:")
        dist = df['level'].value_counts().sort_index()
        for nivel, freq in dist.items():
            pct = freq / len(df) * 100
            print(f"      Nível {nivel}: {freq} vetores ({pct:.1f}%)")
    
    print("\n📊 MUDANÇAS ENTRE β=0.5 E β=0.7")
    df_05 = resultados[0.5]
    df_07 = resultados[0.7]
    
    merged = df_05[['vector', 'level']].rename(columns={'level': 'level_05'}).merge(
        df_07[['vector', 'level']].rename(columns={'level': 'level_07'}),
        on='vector'
    )
    merged['delta'] = merged['level_07'] - merged['level_05']
    
    mudancas = merged[merged['delta'] != 0]
    print(f"\n   Total de vetores: {len(merged)}")
    print(f"   Vetores que mudaram: {len(mudancas)} ({len(mudancas)/len(merged)*100:.1f}%)")
    
    print("\n   Distribuição das mudanças:")
    for delta in sorted(merged['delta'].unique()):
        count = len(merged[merged['delta'] == delta])
        if delta == 0:
            print(f"      Permaneceu: {count} vetores ({count/len(merged)*100:.1f}%)")
        elif delta > 0:
            print(f"      Subiu {delta} nível(is): {count} vetores ({count/len(merged)*100:.1f}%)")
        else:
            print(f"      Desceu {abs(delta)} nível(is): {count} vetores ({count/len(merged)*100:.1f}%)")

if __name__ == "__main__":
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Autor: Neemias da Silva Ferreira")
    print(f"📋 ORCID: 0009-0005-1552-6018")
    
    comparar_betas([0.5, 0.6, 0.7])