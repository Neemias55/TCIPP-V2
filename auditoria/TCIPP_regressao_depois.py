#!/usr/bin/env python3
"""
TCIPP_regressao_depois.py — Captura o comportamento do R10 V2 APÓS a substituição

Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026

OBJETIVO:
Capturar o nível de maturidade calculado pelo R10 V2 para todos os 3125 vetores.
Comparar com o baseline do R10 original.
"""

import itertools
import pandas as pd
import numpy as np
from datetime import datetime

# =============================================================================
# IMPORTAR O R10 V2
# =============================================================================

from TCIPP_MASTER_R10_V2 import TCIPP

# =============================================================================
# CAPTURA DE BASELINE
# =============================================================================

def capturar_baseline_v2():
    """Captura o nível de maturidade para todos os 3125 vetores."""
    tcipp = TCIPP()
    
    all_vectors = list(itertools.product([1, 2, 3, 4, 5], repeat=5))
    
    resultados = []
    
    for v in all_vectors:
        resultado = tcipp.auditar(list(v))
        if 'erro' in resultado:
            print(f"Erro no vetor {v}: {resultado['erro']}")
            continue
        
        resultados.append({
            'vector': v,
            'nivel': resultado['nivel'],
            'nivel_nome': resultado['nivel_nome'],
            'melhor_referencia': resultado['melhor_referencia'],
        })
    
    df = pd.DataFrame(resultados)
    return df

def comparar_baselines(df_r10, df_v2):
    """Compara os baselines do R10 original e do R10 V2."""
    print("\n📊 COMPARAÇÃO DE BASELINES")
    print("=" * 80)
    
    # Merge
    df = df_r10[['vector', 'nivel']].rename(
        columns={'nivel': 'nivel_r10'}
    ).merge(
        df_v2[['vector', 'nivel']].rename(
            columns={'nivel': 'nivel_v2'}
        ),
        on='vector'
    )
    
    df['delta'] = df['nivel_v2'] - df['nivel_r10']
    
    # Distribuição R10
    print("\n   R10 Original:")
    dist_r10 = df['nivel_r10'].value_counts().sort_index()
    for nivel, freq in dist_r10.items():
        pct = freq / len(df) * 100
        print(f"      Nível {nivel}: {freq} vetores ({pct:.1f}%)")
    
    # Distribuição V2
    print("\n   R10 V2:")
    dist_v2 = df['nivel_v2'].value_counts().sort_index()
    for nivel, freq in dist_v2.items():
        pct = freq / len(df) * 100
        print(f"      Nível {nivel}: {freq} vetores ({pct:.1f}%)")
    
    # Mudanças
    print("\n   Mudanças de nível:")
    mudancas = df[df['delta'] != 0]
    print(f"      Total de vetores: {len(df)}")
    print(f"      Vetores que mudaram: {len(mudancas)} ({len(mudancas)/len(df)*100:.1f}%)")
    print(f"      Vetores que permaneceram: {len(df) - len(mudancas)} ({(len(df)-len(mudancas))/len(df)*100:.1f}%)")
    
    print("\n   Distribuição das mudanças:")
    for delta in sorted(df['delta'].unique()):
        count = len(df[df['delta'] == delta])
        if delta == 0:
            print(f"      Permaneceu: {count} vetores ({count/len(df)*100:.1f}%)")
        elif delta > 0:
            print(f"      Subiu {delta} nível(is): {count} vetores ({count/len(df)*100:.1f}%)")
        else:
            print(f"      Desceu {abs(delta)} nível(is): {count} vetores ({count/len(df)*100:.1f}%)")
    
    # Casos críticos
    print("\n   Casos críticos:")
    casos = {
        "[1,1,1,1,1]": (1,1,1,1,1),
        "[1,5,1,5,1]": (1,5,1,5,1),
        "[2,2,2,2,2]": (2,2,2,2,2),
        "[3,3,3,3,3]": (3,3,3,3,3),
        "[4,4,4,4,4]": (4,4,4,4,4),
        "[5,5,5,5,5]": (5,5,5,5,5),
    }
    
    print(f"\n      {'Caso':<20} {'R10':<8} {'V2':<8} {'Delta':<8}")
    print(f"      {'-'*20} {'-'*8} {'-'*8} {'-'*8}")
    
    for nome, v in casos.items():
        row = df[df['vector'] == v].iloc[0]
        delta = row['delta']
        delta_str = f"+{delta}" if delta > 0 else str(delta)
        print(f"      {nome:<20} {row['nivel_r10']:<8} {row['nivel_v2']:<8} {delta_str:<8}")
    
    return df

def main():
    print("=" * 80)
    print("🔬 TCIPP — CAPTURA DE BASELINE (R10 V2)")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Autor: Neemias da Silva Ferreira")
    print(f"📋 ORCID: 0009-0005-1552-6018")
    print("=" * 80)
    
    # Carregar baseline do R10 original
    print("\n📂 Carregando baseline do R10 original...")
    df_r10 = pd.read_csv(r"C:\V54\resultados\tcipp_baseline_r10.csv")
    df_r10['vector'] = df_r10['vector'].apply(eval)  # Converter string para tupla
    
    # Capturar baseline do R10 V2
    print("📊 Capturando baseline do R10 V2...")
    df_v2 = capturar_baseline_v2()
    
    # Comparar
    df_comparacao = comparar_baselines(df_r10, df_v2)
    
    # Salvar
    caminho = r"C:\V54\resultados\tcipp_comparacao_r10_v2.csv"
    df_comparacao.to_csv(caminho, index=False)
    print(f"\n📁 Comparação salva em: {caminho}")
    
    print("\n" + "=" * 80)
    print("🏆 COMPARAÇÃO CONCLUÍDA")
    print("=" * 80)

if __name__ == "__main__":
    main()