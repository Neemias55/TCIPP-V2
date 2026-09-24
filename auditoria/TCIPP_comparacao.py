#!/usr/bin/env python3
"""
TCIPP_comparacao.py — Comparação entre Versões

Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026

OBJETIVO:
Comparar a versão anterior (OWA + Quantis) com a versão atual (Média - Gargalo + Limiares Naturais).
"""

import itertools
import pandas as pd
import numpy as np
from datetime import datetime

# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

DIMENSOES = [1, 2, 3, 4, 5]

# Versão anterior (OWA + Quantis)
PESOS_OWA = [0.40, 0.25, 0.15, 0.12, 0.08]

# Versão atual (Média - Gargalo + Limiares Naturais)
BETA = 0.5
LIMIARES = [1.5, 2.5, 3.5, 4.5]

# =============================================================================
# FUNÇÕES — VERSÃO ANTERIOR
# =============================================================================

def score_owa(v):
    v_ord = sorted(v)
    return sum(w * x for w, x in zip(PESOS_OWA, v_ord))

def classificar_owa(df_scores):
    """Classifica por quantis (625 por nível)."""
    df = df_scores.sort_values('score').reset_index(drop=True)
    df['level'] = (df.index // 625) + 1
    return df

# =============================================================================
# FUNÇÕES — VERSÃO ATUAL
# =============================================================================

def score_gargalo(v):
    media = sum(v) / len(v)
    gargalo = max(0, 3 - min(v))
    return media - BETA * gargalo

def classificar_gargalo(score):
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
# COMPARAÇÃO
# =============================================================================

def comparar():
    all_vectors = list(itertools.product(DIMENSOES, repeat=5))
    
    # Versão OWA
    df_owa = pd.DataFrame({
        'vector': all_vectors,
        'score': [score_owa(v) for v in all_vectors]
    })
    df_owa = classificar_owa(df_owa)
    
    # Versão Gargalo
    df_gargalo = pd.DataFrame({
        'vector': all_vectors,
        'score': [score_gargalo(v) for v in all_vectors]
    })
    df_gargalo['level'] = df_gargalo['score'].apply(classificar_gargalo)
    
    # Merge
    df = df_owa[['vector', 'score', 'level']].rename(
        columns={'score': 'score_owa', 'level': 'level_owa'}
    ).merge(
        df_gargalo[['vector', 'score', 'level']].rename(
            columns={'score': 'score_gargalo', 'level': 'level_gargalo'}
        ),
        on='vector'
    )
    
    # Calcular diferenças
    df['delta_level'] = df['level_gargalo'] - df['level_owa']
    
    return df

def analisar_comparacao(df):
    print("\n📊 DISTRIBUIÇÃO COMPARATIVA")
    print("=" * 80)
    
    print("\n   Versão OWA + Quantis:")
    dist_owa = df['level_owa'].value_counts().sort_index()
    for nivel, freq in dist_owa.items():
        print(f"      Nível {nivel}: {freq} vetores ({freq/len(df)*100:.1f}%)")
    
    print("\n   Versão Média - Gargalo + Limiares Naturais:")
    dist_gargalo = df['level_gargalo'].value_counts().sort_index()
    for nivel, freq in dist_gargalo.items():
        print(f"      Nível {nivel}: {freq} vetores ({freq/len(df)*100:.1f}%)")
    
    print("\n📊 MUDANÇAS DE NÍVEL")
    print("=" * 80)
    
    mudancas = df[df['delta_level'] != 0]
    print(f"\n   Total de vetores: {len(df)}")
    print(f"   Vetores que mudaram de nível: {len(mudancas)} ({len(mudancas)/len(df)*100:.1f}%)")
    print(f"   Vetores que permaneceram: {len(df) - len(mudancas)} ({(len(df)-len(mudancas))/len(df)*100:.1f}%)")
    
    print("\n   Distribuição das mudanças:")
    delta_counts = df['delta_level'].value_counts().sort_index()
    for delta, count in delta_counts.items():
        if delta != 0:
            direcao = "subiu" if delta > 0 else "desceu"
            print(f"      {direcao} {abs(delta)} nível(is): {count} vetores ({count/len(df)*100:.1f}%)")
    
    print("\n📊 CASOS CRÍTICOS")
    print("=" * 80)
    
    casos = {
        "[1,1,1,1,1] Degenerado": (1,1,1,1,1),
        "[1,5,1,5,1] Caótico": (1,5,1,5,1),
        "[2,2,2,2,2] Ruim": (2,2,2,2,2),
        "[3,3,3,3,3] Médio": (3,3,3,3,3),
        "[4,4,4,4,4] Bom": (4,4,4,4,4),
        "[5,5,5,5,5] Excelente": (5,5,5,5,5),
    }
    
    print(f"\n   {'Caso':<30} {'OWA':<10} {'Gargalo':<10} {'Delta':<10}")
    print(f"   {'-'*30} {'-'*10} {'-'*10} {'-'*10}")
    
    for nome, v in casos.items():
        row = df[df['vector'] == v].iloc[0]
        delta = row['delta_level']
        delta_str = f"+{delta}" if delta > 0 else str(delta)
        print(f"   {nome:<30} {row['level_owa']:<10} {row['level_gargalo']:<10} {delta_str:<10}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("🔬 TCIPP — COMPARAÇÃO ENTRE VERSÕES")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Autor: Neemias da Silva Ferreira")
    print(f"📋 ORCID: 0009-0005-1552-6018")
    print("=" * 80)
    
    print(f"""
    VERSÃO ANTERIOR:
    S(x) = OWA com pesos {PESOS_OWA}
    Corte por quantis (625 por nível)
    
    VERSÃO ATUAL:
    S(x) = média(x) - {BETA} * max(0, 3 - min(x))
    Limiares: {LIMIARES}
    """)
    
    # Comparar
    print("\n📊 Comparando versões...")
    df = comparar()
    
    # Analisar
    analisar_comparacao(df)
    
    # Salvar
    caminho = r"C:\V54\resultados\tcipp_comparacao.csv"
    df.to_csv(caminho, index=False)
    print(f"\n📁 Resultados salvos em: {caminho}")
    
    # Veredicto
    print("\n" + "=" * 80)
    print("🏆 VEREDICTO PARCIAL — COMPARAÇÃO")
    print("=" * 80)
    print("   ✅ Comparação concluída. Ver resultados acima.")
    print("=" * 80)

if __name__ == "__main__":
    main()