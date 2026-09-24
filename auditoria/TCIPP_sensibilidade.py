#!/usr/bin/env python3
"""
TCIPP_sensibilidade.py — Auditoria de Sensibilidade

Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026

OBJETIVO:
Medir como alterações unitárias em cada dimensão afetam o score e o nível.
"""

import itertools
import pandas as pd
import numpy as np
from datetime import datetime

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
    """Score = média - beta * gargalo"""
    media = sum(v) / len(v)
    gargalo = max(0, 3 - min(v))
    return media - BETA * gargalo

def classificar(score):
    """Classifica o score em níveis 1-5."""
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
# ANÁLISE DE SENSIBILIDADE
# =============================================================================

def analisar_sensibilidade():
    """
    Para cada vetor e cada dimensão, mede:
    - Mudança no score ao aumentar a dimensão em 1
    - Mudança no nível ao aumentar a dimensão em 1
    - Mudança no score ao diminuir a dimensão em 1
    - Mudança no nível ao diminuir a dimensão em 1
    """
    all_vectors = list(itertools.product(DIMENSOES, repeat=5))
    
    resultados = []
    
    for v in all_vectors:
        score_atual = calcular_score(v)
        nivel_atual = classificar(score_atual)
        
        for i in range(5):
            # Aumentar dimensão i em 1 (se possível)
            if v[i] < 5:
                v_mais = list(v)
                v_mais[i] += 1
                v_mais = tuple(v_mais)
                score_mais = calcular_score(v_mais)
                nivel_mais = classificar(score_mais)
                delta_score_mais = score_mais - score_atual
                delta_nivel_mais = nivel_mais - nivel_atual
            else:
                delta_score_mais = None
                delta_nivel_mais = None
            
            # Diminuir dimensão i em 1 (se possível)
            if v[i] > 1:
                v_menos = list(v)
                v_menos[i] -= 1
                v_menos = tuple(v_menos)
                score_menos = calcular_score(v_menos)
                nivel_menos = classificar(score_menos)
                delta_score_menos = score_menos - score_atual
                delta_nivel_menos = nivel_menos - nivel_atual
            else:
                delta_score_menos = None
                delta_nivel_menos = None
            
            resultados.append({
                'vector': v,
                'dimensao': i+1,
                'score_atual': score_atual,
                'nivel_atual': nivel_atual,
                'delta_score_mais': delta_score_mais,
                'delta_nivel_mais': delta_nivel_mais,
                'delta_score_menos': delta_score_menos,
                'delta_nivel_menos': delta_nivel_menos,
            })
    
    return pd.DataFrame(resultados)

def analisar_por_dimensao(df):
    """Agrega os resultados por dimensão."""
    print("\n📊 SENSIBILIDADE POR DIMENSÃO")
    print("=" * 80)
    
    for dim in range(1, 6):
        subset = df[df['dimensao'] == dim]
        
        # Delta score ao aumentar
        deltas_mais = subset['delta_score_mais'].dropna()
        deltas_menos = subset['delta_score_menos'].dropna()
        
        print(f"\n   Dimensão {dim}:")
        print(f"      Aumentar +1:")
        print(f"         Delta score médio: {deltas_mais.mean():.4f}")
        print(f"         Delta score mínimo: {deltas_mais.min():.4f}")
        print(f"         Delta score máximo: {deltas_mais.max():.4f}")
        print(f"         Muda nível: {sum(subset['delta_nivel_mais'].dropna() != 0)} casos")
        
        print(f"      Diminuir -1:")
        print(f"         Delta score médio: {deltas_menos.mean():.4f}")
        print(f"         Delta score mínimo: {deltas_menos.min():.4f}")
        print(f"         Delta score máximo: {deltas_menos.max():.4f}")
        print(f"         Muda nível: {sum(subset['delta_nivel_menos'].dropna() != 0)} casos")

def analisar_mudancas_nivel(df):
    """Analisa com que frequência o nível muda."""
    print("\n📊 MUDANÇAS DE NÍVEL")
    print("=" * 80)
    
    # Aumentar
    subset_mais = df[df['delta_nivel_mais'].notna()]
    mudancas_mais = subset_mais[subset_mais['delta_nivel_mais'] != 0]
    print(f"\n   Aumentar +1:")
    print(f"      Total de testes: {len(subset_mais)}")
    print(f"      Mudanças de nível: {len(mudancas_mais)} ({len(mudancas_mais)/len(subset_mais)*100:.2f}%)")
    if len(mudancas_mais) > 0:
        print(f"      Delta nível médio: {mudancas_mais['delta_nivel_mais'].mean():.4f}")
        print(f"      Delta nível mínimo: {mudancas_mais['delta_nivel_mais'].min()}")
        print(f"      Delta nível máximo: {mudancas_mais['delta_nivel_mais'].max()}")
    
    # Diminuir
    subset_menos = df[df['delta_nivel_menos'].notna()]
    mudancas_menos = subset_menos[subset_menos['delta_nivel_menos'] != 0]
    print(f"\n   Diminuir -1:")
    print(f"      Total de testes: {len(subset_menos)}")
    print(f"      Mudanças de nível: {len(mudancas_menos)} ({len(mudancas_menos)/len(subset_menos)*100:.2f}%)")
    if len(mudancas_menos) > 0:
        print(f"      Delta nível médio: {mudancas_menos['delta_nivel_menos'].mean():.4f}")
        print(f"      Delta nível mínimo: {mudancas_menos['delta_nivel_menos'].min()}")
        print(f"      Delta nível máximo: {mudancas_menos['delta_nivel_menos'].max()}")

def analisar_gargalo_vs_outros(df):
    """Compara a sensibilidade do gargalo vs outras dimensões."""
    print("\n📊 GARGALO VS OUTRAS DIMENSÕES")
    print("=" * 80)
    
    # Identificar quando a dimensão é o gargalo
    df['eh_gargalo'] = df.apply(
        lambda row: row['vector'][row['dimensao']-1] == min(row['vector']),
        axis=1
    )
    
    # Sensibilidade quando é gargalo
    gargalo = df[df['eh_gargalo']]
    nao_gargalo = df[~df['eh_gargalo']]
    
    print(f"\n   Quando a dimensão É o gargalo:")
    print(f"      Delta score médio (aumentar): {gargalo['delta_score_mais'].dropna().mean():.4f}")
    print(f"      Muda nível: {sum(gargalo['delta_nivel_mais'].dropna() != 0)} casos")
    
    print(f"\n   Quando a dimensão NÃO é o gargalo:")
    print(f"      Delta score médio (aumentar): {nao_gargalo['delta_score_mais'].dropna().mean():.4f}")
    print(f"      Muda nível: {sum(nao_gargalo['delta_nivel_mais'].dropna() != 0)} casos")

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("🔬 TCIPP — AUDITORIA DE SENSIBILIDADE")
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
    
    # 1. Analisar sensibilidade
    print("\n📊 Calculando sensibilidade para todos os 3125 vetores...")
    df = analisar_sensibilidade()
    
    # 2. Sensibilidade por dimensão
    analisar_por_dimensao(df)
    
    # 3. Mudanças de nível
    analisar_mudancas_nivel(df)
    
    # 4. Gargalo vs outras dimensões
    analisar_gargalo_vs_outros(df)
    
    # 5. Salvar CSV
    caminho = r"C:\V54\resultados\tcipp_sensibilidade.csv"
    df.to_csv(caminho, index=False)
    print(f"\n📁 Resultados salvos em: {caminho}")
    
    # 6. Veredicto parcial
    print("\n" + "=" * 80)
    print("🏆 VEREDICTO PARCIAL — SENSIBILIDADE")
    print("=" * 80)
    print("   ✅ Análise concluída. Ver resultados acima.")
    print("=" * 80)

if __name__ == "__main__":
    main()