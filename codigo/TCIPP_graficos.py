#!/usr/bin/env python3
"""
TCIPP_graficos.py — Geração de Gráficos do TCIPP V2.0 FINAL

Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026
Maceió-Alagoas

OBJETIVO:
Gerar gráficos visuais do TCIPP V2.0 FINAL para documentação.
"""

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from datetime import datetime
import os

# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

DIMENSOES = [1, 2, 3, 4, 5]
BETA = 0.70
LIMIARES = [1.25, 2.5, 3.5, 4.5]

# Cores dos níveis
CORES = {
    1: '#E74C3C',  # Vermelho
    2: '#E67E22',  # Laranja
    3: '#F1C40F',  # Amarelo
    4: '#2ECC71',  # Verde
    5: '#3498DB',  # Azul
}

NOMES = {
    1: 'Inicial',
    2: 'Reconhecimento',
    3: 'Estruturação',
    4: 'Coexistência',
    5: 'Maturidade Espiral',
}

# =============================================================================
# FUNÇÕES
# =============================================================================

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

# =============================================================================
# GRÁFICO 1 — DISTRIBUIÇÃO DOS NÍVEIS
# =============================================================================

def grafico_distribuicao(salvar=True):
    dist = calcular_distribuicao()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    niveis = list(dist.keys())
    freq = list(dist.values())
    cores = [CORES[n] for n in niveis]
    labels = [f"Nível {n}\n{NOMES[n]}" for n in niveis]
    
    bars = ax.bar(labels, freq, color=cores, edgecolor='black', linewidth=1.5)
    
    # Adicionar valores nas barras
    for bar, f in zip(bars, freq):
        height = bar.get_height()
        pct = f / 3125 * 100
        ax.text(bar.get_x() + bar.get_width()/2., height + 20,
                f'{f}\n({pct:.1f}%)',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_title('TCIPP V2.0 FINAL — Distribuição dos Níveis\n(3125 vetores)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Nível de Maturidade', fontsize=12)
    ax.set_ylabel('Número de Vetores', fontsize=12)
    ax.set_ylim(0, max(freq) * 1.2)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    if salvar:
        plt.savefig(r'C:\TCIPP\grafico\01_distribuicao_niveis.png', dpi=150, bbox_inches='tight')
        print("   ✅ 01_distribuicao_niveis.png")
    plt.show()

# =============================================================================
# GRÁFICO 2 — FUNÇÃO DE SCORE
# =============================================================================

def grafico_funcao_score(salvar=True):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Média variando de 1 a 5
    medias = np.linspace(1, 5, 100)
    
    # Diferentes valores de mínimo
    for minimo, cor, label in [(1, '#E74C3C', 'min=1 (gargalo extremo)'),
                                (2, '#E67E22', 'min=2 (gargalo)'),
                                (3, '#F1C40F', 'min=3 (sem gargalo)'),
                                (4, '#2ECC71', 'min=4 (sem gargalo)'),
                                (5, '#3498DB', 'min=5 (sem gargalo)')]:
        scores = []
        for m in medias:
            if m < minimo:
                scores.append(np.nan)
            else:
                gargalo = max(0, 3 - minimo)
                score = m - BETA * gargalo
                scores.append(score)
        ax.plot(medias, scores, color=cor, linewidth=2.5, label=label)
    
    # Linhas dos limiares
    for i, limiar in enumerate(LIMIARES):
        ax.axhline(y=limiar, color='gray', linestyle='--', alpha=0.5, linewidth=1)
        ax.text(5.05, limiar, f'  t={limiar}', va='center', fontsize=9, color='gray')
    
    # Sombrear regiões dos níveis
    ax.axhspan(-1, 1.25, alpha=0.1, color=CORES[1])
    ax.axhspan(1.25, 2.5, alpha=0.1, color=CORES[2])
    ax.axhspan(2.5, 3.5, alpha=0.1, color=CORES[3])
    ax.axhspan(3.5, 4.5, alpha=0.1, color=CORES[4])
    ax.axhspan(4.5, 6, alpha=0.1, color=CORES[5])
    
    ax.set_title('TCIPP V2.0 FINAL — Função de Score\nS(x) = média(x) - 0.70 × max(0, 3 - min(x))',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Média das 5 Dimensões', fontsize=12)
    ax.set_ylabel('Score S(x)', fontsize=12)
    ax.set_xlim(1, 5)
    ax.set_ylim(-0.5, 5.5)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    if salvar:
        plt.savefig(r'C:\TCIPP\grafico\02_funcao_score.png', dpi=150, bbox_inches='tight')
        print("   ✅ 02_funcao_score.png")
    plt.show()

# =============================================================================
# GRÁFICO 3 — CASOS CRÍTICOS
# =============================================================================

def grafico_casos_criticos(salvar=True):
    casos = {
        '[1,1,1,1,1]\nDegenerado': (1,1,1,1,1),
        '[1,5,1,5,1]\nCaótico': (1,5,1,5,1),
        '[2,2,2,2,2]\nRuim': (2,2,2,2,2),
        '[3,3,3,3,3]\nMédio': (3,3,3,3,3),
        '[4,4,4,4,4]\nBom': (4,4,4,4,4),
        '[5,5,5,5,5]\nExcelente': (5,5,5,5,5),
    }
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    nomes = list(casos.keys())
    scores = [calcular_score(v) for v in casos.values()]
    niveis = [classificar(s) for s in scores]
    cores = [CORES[n] for n in niveis]
    
    bars = ax.bar(nomes, scores, color=cores, edgecolor='black', linewidth=1.5)
    
    # Adicionar valores nas barras
    for bar, score, nivel in zip(bars, scores, niveis):
        height = bar.get_height()
        offset = 0.1 if height >= 0 else -0.3
        ax.text(bar.get_x() + bar.get_width()/2., height + offset,
                f'S={score:.2f}\nNível {nivel}',
                ha='center', va='bottom' if height >= 0 else 'top',
                fontsize=10, fontweight='bold')
    
    # Linhas dos limiares
    for limiar in LIMIARES:
        ax.axhline(y=limiar, color='gray', linestyle='--', alpha=0.5, linewidth=1)
        ax.text(5.5, limiar, f't={limiar}', va='center', fontsize=9, color='gray')
    
    ax.axhline(y=0, color='black', linewidth=1)
    
    ax.set_title('TCIPP V2.0 FINAL — Casos Críticos\n(6 vetores âncora)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylabel('Score S(x)', fontsize=12)
    ax.set_ylim(-0.8, 5.5)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.xticks(rotation=0, fontsize=10)
    plt.tight_layout()
    if salvar:
        plt.savefig(r'C:\TCIPP\grafico\03_casos_criticos.png', dpi=150, bbox_inches='tight')
        print("   ✅ 03_casos_criticos.png")
    plt.show()

# =============================================================================
# GRÁFICO 4 — MAPA DE CALOR
# =============================================================================

def grafico_mapa_calor(salvar=True):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Grid de médias e mínimos
    medias = np.linspace(1, 5, 50)
    minimos = np.linspace(1, 5, 50)
    
    M, Min = np.meshgrid(medias, minimos)
    scores = M - BETA * np.maximum(0, 3 - Min)
    
    # Mapa de calor
    im = ax.contourf(M, Min, scores, levels=20, cmap='RdYlGn_r', alpha=0.8)
    
    # Linhas dos limiares
    contour = ax.contour(M, Min, scores, levels=LIMIARES, colors='black', linewidths=2)
    ax.clabel(contour, inline=True, fontsize=10, fmt='t=%.2f')
    
    # Casos críticos
    casos = {
        'Degenerado': (1, 1),
        'Caótico': (2.6, 1),
        'Ruim': (2, 2),
        'Médio': (3, 3),
        'Bom': (4, 4),
        'Excelente': (5, 5),
    }
    
    for nome, (media, minimo) in casos.items():
        ax.plot(media, minimo, 'ko', markersize=10, markeredgecolor='white', markeredgewidth=2)
        ax.annotate(nome, (media, minimo), textcoords="offset points",
                    xytext=(10, 10), fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    plt.colorbar(im, ax=ax, label='Score S(x)')
    
    ax.set_title('TCIPP V2.0 FINAL — Mapa de Calor do Score\n(média vs mínimo)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Média das 5 Dimensões', fontsize=12)
    ax.set_ylabel('Mínimo das 5 Dimensões', fontsize=12)
    
    plt.tight_layout()
    if salvar:
        plt.savefig(r'C:\TCIPP\grafico\04_mapa_calor.png', dpi=150, bbox_inches='tight')
        print("   ✅ 04_mapa_calor.png")
    plt.show()

# =============================================================================
# GRÁFICO 5 — COMPARAÇÃO DE β
# =============================================================================

def grafico_comparacao_beta(salvar=True):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Casos para comparar
    casos = {
        '[1,1,1,1,1]': (1,1,1,1,1),
        '[1,5,1,5,1]': (1,5,1,5,1),
        '[2,2,2,2,2]': (2,2,2,2,2),
        '[3,3,3,3,3]': (3,3,3,3,3),
        '[4,4,4,4,4]': (4,4,4,4,4),
        '[5,5,5,5,5]': (5,5,5,5,5),
    }
    
    betas = [0.5, 0.6, 0.7, 0.75]
    cores_beta = ['#3498DB', '#9B59B6', '#E74C3C', '#E67E22']
    
    x = np.arange(len(casos))
    width = 0.2
    
    for i, (beta, cor) in enumerate(zip(betas, cores_beta)):
        scores = [calcular_score(v, beta) for v in casos.values()]
        offset = (i - 1.5) * width
        bars = ax.bar(x + offset, scores, width, label=f'β={beta}', color=cor, edgecolor='black')
    
    # Linhas dos limiares (para β=0.70)
    for limiar in LIMIARES:
        ax.axhline(y=limiar, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    
    ax.set_title('TCIPP V2.0 FINAL — Comparação de β\n(efeito do coeficiente de gargalo)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(casos.keys(), fontsize=10)
    ax.set_ylabel('Score S(x)', fontsize=12)
    ax.set_ylim(-0.8, 5.5)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    if salvar:
        plt.savefig(r'C:\TCIPP\grafico\05_comparacao_beta.png', dpi=150, bbox_inches='tight')
        print("   ✅ 05_comparacao_beta.png")
    plt.show()

# =============================================================================
# GRÁFICO 6 — PIZZA DOS NÍVEIS
# =============================================================================

def grafico_pizza(salvar=True):
    dist = calcular_distribuicao()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    niveis = list(dist.keys())
    freq = list(dist.values())
    cores = [CORES[n] for n in niveis]
    labels = [f"Nível {n}\n{NOMES[n]}\n{f} ({f/3125*100:.1f}%)" for n, f in zip(niveis, freq)]
    
    wedges, texts, autotexts = ax.pie(freq, labels=labels, colors=cores,
                                        autopct='%1.1f%%', startangle=90,
                                        textprops={'fontsize': 10, 'fontweight': 'bold'},
                                        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
    
    ax.set_title('TCIPP V2.0 FINAL — Distribuição Percentual dos Níveis\n(3125 vetores)',
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    if salvar:
        plt.savefig(r'C:\TCIPP\grafico\06_pizza_niveis.png', dpi=150, bbox_inches='tight')
        print("   ✅ 06_pizza_niveis.png")
    plt.show()

# =============================================================================
# GRÁFICO 7 — PAINEL CONSOLIDADO
# =============================================================================

def grafico_painel(salvar=True):
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # --- Subplot 1: Distribuição ---
    ax1 = fig.add_subplot(gs[0, 0])
    dist = calcular_distribuicao()
    niveis = list(dist.keys())
    freq = list(dist.values())
    cores = [CORES[n] for n in niveis]
    bars = ax1.bar([f'N{n}' for n in niveis], freq, color=cores, edgecolor='black')
    for bar, f in zip(bars, freq):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
                 f'{f}', ha='center', fontsize=9, fontweight='bold')
    ax1.set_title('Distribuição dos Níveis', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Vetores')
    ax1.grid(axis='y', alpha=0.3)
    
    # --- Subplot 2: Função de Score ---
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
    
    # --- Subplot 3: Casos Críticos ---
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
    niveis = [classificar(s) for s in scores]
    cores = [CORES[n] for n in niveis]
    bars = ax3.bar(nomes, scores, color=cores, edgecolor='black')
    for limiar in LIMIARES:
        ax3.axhline(y=limiar, color='gray', linestyle='--', alpha=0.5)
    ax3.axhline(y=0, color='black', linewidth=1)
    ax3.set_title('Casos Críticos', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Score')
    ax3.grid(axis='y', alpha=0.3)
    
    # --- Subplot 4: Pizza ---
    ax4 = fig.add_subplot(gs[1, 1])
    labels = [f'N{n}' for n in niveis]
    wedges, texts, autotexts = ax4.pie(freq, labels=labels, colors=cores,
                                        autopct='%1.1f%%', startangle=90,
                                        wedgeprops={'edgecolor': 'black', 'linewidth': 1})
    ax4.set_title('Distribuição Percentual', fontsize=12, fontweight='bold')
    
    fig.suptitle('TCIPP V2.0 FINAL — Painel Consolidado\nβ=0.70, t=1.25, Limiares=[1.25, 2.5, 3.5, 4.5]',
                 fontsize=16, fontweight='bold')
    
    if salvar:
        plt.savefig(r'C:\TCIPP\grafico\07_painel_consolidado.png', dpi=150, bbox_inches='tight')
        print("   ✅ 07_painel_consolidado.png")
    plt.show()

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("📊 TCIPP — GERAÇÃO DE GRÁFICOS")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Autor: Neemias da Silva Ferreira")
    print(f"📋 ORCID: 0009-0005-1552-6018")
    print("=" * 80)
    
    # Criar pasta se não existir
    pasta = r'C:\TCIPP\grafico'
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f"\n📁 Pasta criada: {pasta}")
    else:
        print(f"\n📁 Pasta existente: {pasta}")
    
    print("\n📊 Gerando gráficos...")
    print()
    
    grafico_distribuicao()
    grafico_funcao_score()
    grafico_casos_criticos()
    grafico_mapa_calor()
    grafico_comparacao_beta()
    grafico_pizza()
    grafico_painel()
    
    print()
    print("=" * 80)
    print("🏆 GRÁFICOS GERADOS COM SUCESSO")
    print("=" * 80)
    print(f"\n📁 Localização: {pasta}")
    print("\n   Arquivos:")
    print("   1. 01_distribuicao_niveis.png")
    print("   2. 02_funcao_score.png")
    print("   3. 03_casos_criticos.png")
    print("   4. 04_mapa_calor.png")
    print("   5. 05_comparacao_beta.png")
    print("   6. 06_pizza_niveis.png")
    print("   7. 07_painel_consolidado.png")
    print("=" * 80)

if __name__ == "__main__":
    main()