#!/usr/bin/env python3
"""
gerar_painel.py — Gera apenas o painel consolidado do TCIPP
"""

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

DIMENSOES = [1, 2, 3, 4, 5]
BETA = 0.70
LIMIARES = [1.25, 2.5, 3.5, 4.5]

CORES = {1: '#E74C3C', 2: '#E67E22', 3: '#F1C40F', 4: '#2ECC71', 5: '#3498DB'}

def calcular_score(v, beta=BETA):
    media = sum(v) / len(v)
    gargalo = max(0, 3 - min(v))
    return media - beta * gargalo

def classificar(score, limiares=LIMIARES):
    if score < limiares[0]:
        return 1
    elif score < limiares[1]:
        return 2
    elif score < limiares[2]:
        return 3
    elif score < limiares[3]:
        return 4
    else:
        return 5

def calcular_distribuicao():
    all_v = list(itertools.product(DIMENSOES, repeat=5))
    niveis = [classificar(calcular_score(v)) for v in all_v]
    dist = pd.Series(niveis).value_counts().sort_index().to_dict()
    return dist

def gerar_painel():
    print("Iniciando geração do painel...")
    
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    dist = calcular_distribuicao()
    niveis = list(dist.keys())
    freq = list(dist.values())
    cores = [CORES[n] for n in niveis]
    
    # Subplot 1: Distribuição
    ax1 = fig.add_subplot(gs[0, 0])
    bars = ax1.bar([f'N{n}' for n in niveis], freq, color=cores, edgecolor='black')
    for bar, f in zip(bars, freq):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
                 f'{f}', ha='center', fontsize=9, fontweight='bold')
    ax1.set_title('Distribuição dos Níveis', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Vetores')
    ax1.grid(axis='y', alpha=0.3)
    print("  Subplot 1 OK")
    
    # Subplot 2: Função de Score
    ax2 = fig.add_subplot(gs[0, 1])
    medias = np.linspace(1, 5, 100)
    for minimo, cor in [(1, '#E74C3C'), (2, '#E67E22'), (3, '#F1C40F'), (5, '#3498DB')]:
        scores = [m - BETA * max(0, 3 - minimo) if m >= minimo else np.nan for m in medias]
        ax2.plot(medias, scores, color=cor, linewidth=2, label=f'min={minimo}')
    for limiar in LIMIARES:
        ax2.axhline(y=limiar, color='gray', linestyle='--', alpha=0.5)
    ax2.set_title('Função de Score', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Média')
    ax2.set_ylabel('Score')
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3)
    print("  Subplot 2 OK")
    
    # Subplot 3: Casos Críticos
    ax3 = fig.add_subplot(gs[1, 0])
    casos = {
        'Deg.': (1,1,1,1,1),
        'Caót.': (1,5,1,5,1),
        'Ruim': (2,2,2,2,2),
        'Médio': (3,3,3,3,3),
        'Bom': (4,4,4,4,4),
        'Excel.': (5,5,5,5,5),
    }
    nomes = list(casos.keys())
    scores = [calcular_score(v) for v in casos.values()]
    niveis_casos = [classificar(s) for s in scores]
    cores_casos = [CORES[n] for n in niveis_casos]
    ax3.bar(nomes, scores, color=cores_casos, edgecolor='black')
    for limiar in LIMIARES:
        ax3.axhline(y=limiar, color='gray', linestyle='--', alpha=0.5)
    ax3.axhline(y=0, color='black', linewidth=1)
    ax3.set_title('Casos Críticos', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Score')
    ax3.grid(axis='y', alpha=0.3)
    print("  Subplot 3 OK")
    
    # Subplot 4: Pizza
    ax4 = fig.add_subplot(gs[1, 1])
    labels = [f'N{n}' for n in niveis]
    ax4.pie(freq, labels=labels, colors=cores, autopct='%1.1f%%', startangle=90,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1})
    ax4.set_title('Distribuição Percentual', fontsize=12, fontweight='bold')
    print("  Subplot 4 OK")
    
    fig.suptitle('TCIPP V2.0 FINAL — Painel Consolidado\nβ=0.70, t=1.25, Limiares=[1.25, 2.5, 3.5, 4.5]',
                 fontsize=16, fontweight='bold')
    
    print("  Salvando...")
    plt.savefig(r'C:\TCIPP\grafico\07_painel_consolidado.png', dpi=150, bbox_inches='tight')
    print("  ✅ 07_painel_consolidado.png")
    plt.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Gerando painel consolidado...")
    print("=" * 60)
    gerar_painel()
    print("=" * 60)
    print("Concluído.")
    print("=" * 60)