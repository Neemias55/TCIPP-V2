#!/usr/bin/env python3
"""
TCIPP_regressao_antes.py — Captura o comportamento do R10 ANTES da substituição

Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026

OBJETIVO:
Capturar o nível de maturidade calculado pelo R10 original para todos os 3125 vetores.
Isso servirá como baseline para os testes de regressão após a substituição.
"""

import itertools
import pandas as pd
import numpy as np
from datetime import datetime

# =============================================================================
# IMPORTAR O R10 (já renomeado para TCIPP_MASTER_R10.py)
# =============================================================================

from TCIPP_MASTER_R10 import TCIPP

# =============================================================================
# CAPTURA DE BASELINE
# =============================================================================

def capturar_baseline():
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

def analisar_baseline(df):
    """Analisa o baseline."""
    print("\n📊 BASELINE — R10 ORIGINAL")
    print("=" * 80)
    
    # Distribuição
    print("\n   Distribuição dos níveis:")
    dist = df['nivel'].value_counts().sort_index()
    for nivel, freq in dist.items():
        pct = freq / len(df) * 100
        print(f"      Nível {nivel}: {freq} vetores ({pct:.1f}%)")
    
    # Casos críticos
    print("\n   Casos críticos:")
    casos = {
        "[1,1,1,1,1]": (1,1,1,1,1),
        "[1,5,1,5,1]": (1,5,1,5,1),
        "[2,2,2,2,2]": (2,2,2,2,2),
        "[3,3,3,3,3]": (3,3,3,3,3),
        "[4,4,4,4,4]": (4,4,4,4,4),
        "[5,5,5,5,5]": (5,5,5,5,5),
        "[5,4,5,4,5]": (5,4,5,4,5),
        "[1,2,1,3,2]": (1,2,1,3,2),
    }
    for nome, v in casos.items():
        row = df[df['vector'] == v]
        if len(row) > 0:
            nivel = row.iloc[0]['nivel']
            melhor_ref = row.iloc[0]['melhor_referencia']
            print(f"      {nome}: Nível {nivel} — Melhor ref: {melhor_ref}")

def main():
    print("=" * 80)
    print("🔬 TCIPP — CAPTURA DE BASELINE (R10 ORIGINAL)")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Autor: Neemias da Silva Ferreira")
    print(f"📋 ORCID: 0009-0005-1552-6018")
    print("=" * 80)
    
    print("\n📊 Capturando baseline para todos os 3125 vetores...")
    df = capturar_baseline()
    
    analisar_baseline(df)
    
    # Salvar
    caminho = r"C:\V54\resultados\tcipp_baseline_r10.csv"
    df.to_csv(caminho, index=False)
    print(f"\n📁 Baseline salvo em: {caminho}")
    
    print("\n" + "=" * 80)
    print("🏆 BASELINE CAPTURADO")
    print("=" * 80)

if __name__ == "__main__":
    main()