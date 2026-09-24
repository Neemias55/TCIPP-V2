#!/usr/bin/env python3
"""
TCIPP_matriz_transicao.py — Matriz de Transição entre Versões

Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026

OBJETIVO:
Construir a matriz de transição completa entre a versão OWA + Quantis
e a versão Média - Gargalo + Limiares Naturais.
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
# MATRIZ DE TRANSIÇÃO
# =============================================================================

def construir_matriz():
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
    df = df_owa[['vector', 'level']].rename(
        columns={'level': 'level_owa'}
    ).merge(
        df_gargalo[['vector', 'level']].rename(
            columns={'level': 'level_gargalo'}
        ),
        on='vector'
    )
    
    # Matriz de transição
    matriz = pd.crosstab(
        df['level_owa'],
        df['level_gargalo'],
        rownames=['Nível OWA'],
        colnames=['Nível Gargalo']
    )
    
    return df, matriz

def analisar_matriz(matriz):
    print("\n📊 MATRIZ DE TRANSIÇÃO")
    print("=" * 80)
    print("\n   Linhas: Nível na versão OWA + Quantis")
    print("   Colunas: Nível na versão Média - Gargalo + Limiares Naturais")
    print()
    print(matriz.to_string())
    
    print("\n📊 ANÁLISE DAS TRANSIÇÕES")
    print("=" * 80)
    
    for nivel_owa in range(1, 6):
        if nivel_owa not in matriz.index:
            continue
        
        print(f"\n   Vetores que eram Nível {nivel_owa} na versão OWA:")
        
        total = matriz.loc[nivel_owa].sum()
        print(f"      Total: {total} vetores")
        
        for nivel_gargalo in range(1, 6):
            if nivel_gargalo not in matriz.columns:
                continue
            
            count = matriz.loc[nivel_owa, nivel_gargalo]
            if count > 0:
                pct = count / total * 100
                delta = nivel_gargalo - nivel_owa
                
                if delta == 0:
                    direcao = "permaneceu"
                elif delta > 0:
                    direcao = f"subiu {delta} nível(is)"
                else:
                    direcao = f"desceu {abs(delta)} nível(is)"
                
                print(f"      → Nível {nivel_gargalo}: {count} vetores ({pct:.1f}%) — {direcao}")

def verificar_consistencia(df):
    print("\n📊 VERIFICAÇÃO DE CONSISTÊNCIA")
    print("=" * 80)
    
    # Contar mudanças
    df['delta'] = df['level_gargalo'] - df['level_owa']
    
    print(f"\n   Total de vetores: {len(df)}")
    print(f"   Vetores que permaneceram: {len(df[df['delta'] == 0])}")
    print(f"   Vetores que mudaram: {len(df[df['delta'] != 0])}")
    
    print("\n   Distribuição das mudanças:")
    for delta in sorted(df['delta'].unique()):
        count = len(df[df['delta'] == delta])
        if delta == 0:
            print(f"      Permaneceu: {count} vetores ({count/len(df)*100:.1f}%)")
        elif delta > 0:
            print(f"      Subiu {delta} nível(is): {count} vetores ({count/len(df)*100:.1f}%)")
        else:
            print(f"      Desceu {abs(delta)} nível(is): {count} vetores ({count/len(df)*100:.1f}%)")

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("🔬 TCIPP — MATRIZ DE TRANSIÇÃO")
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
    
    # Construir matriz
    print("\n📊 Construindo matriz de transição...")
    df, matriz = construir_matriz()
    
    # Analisar
    analisar_matriz(matriz)
    verificar_consistencia(df)
    
    # Salvar
    caminho = r"C:\V54\resultados\tcipp_matriz_transicao.csv"
    df.to_csv(caminho, index=False)
    print(f"\n📁 Resultados salvos em: {caminho}")
    
    # Veredicto
    print("\n" + "=" * 80)
    print("🏆 VEREDICTO PARCIAL — MATRIZ DE TRANSIÇÃO")
    print("=" * 80)
    print("   ✅ Matriz construída. Ver resultados acima.")
    print("=" * 80)

if __name__ == "__main__":
    main()