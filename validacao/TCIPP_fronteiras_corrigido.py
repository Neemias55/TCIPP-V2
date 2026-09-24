#!/usr/bin/env python3
"""
TCIPP_fronteiras_corrigido.py — Auditoria de Fronteiras Corrigida

Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026

OBJETIVO:
Corrigir a auditoria de fronteiras das 4 combinações válidas.
"""

import itertools
import pandas as pd
import numpy as np
from datetime import datetime

DIMENSOES = [1, 2, 3, 4, 5]
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

def auditar_fronteiras(beta, t):
    """Auditoria de fronteiras corrigida."""
    all_v = list(itertools.product(DIMENSOES, repeat=5))
    scores = [calcular_score(v, beta) for v in all_v]
    
    # 1. Vetores exatamente no limiar
    exatamente = [v for v, s in zip(all_v, scores) if abs(s - t) < 1e-9]
    
    # 2. Vetores próximos abaixo (diferença < 0.01)
    proximos_abaixo = [v for v, s in zip(all_v, scores) if 0 < t - s < 0.01]
    
    # 3. Vetores próximos acima (diferença < 0.01)
    proximos_acima = [v for v, s in zip(all_v, scores) if 0 < s - t < 0.01]
    
    # 4. Total abaixo
    total_abaixo = [v for v, s in zip(all_v, scores) if s < t]
    
    # 5. Total acima
    total_acima = [v for v, s in zip(all_v, scores) if s > t]
    
    # 6. Verificar se todos os "exatamente" têm o mesmo nível
    niveis_exatamente = set(classificar(calcular_score(v, beta), t) for v in exatamente)
    niveis_abaixo = set(classificar(calcular_score(v, beta), t) for v in proximos_abaixo)
    niveis_acima = set(classificar(calcular_score(v, beta), t) for v in proximos_acima)
    
    return {
        'exatamente': (len(exatamente), niveis_exatamente),
        'proximos_abaixo': (len(proximos_abaixo), niveis_abaixo),
        'proximos_acima': (len(proximos_acima), niveis_acima),
        'total_abaixo': len(total_abaixo),
        'total_acima': len(total_acima),
    }

def main():
    print("=" * 80)
    print("🔬 TCIPP — AUDITORIA DE FRONTEIRAS CORRIGIDA")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Autor: Neemias da Silva Ferreira")
    print(f"📋 ORCID: 0009-0005-1552-6018")
    print("=" * 80)
    
    combinacoes = [
        (0.65, 1.35),
        (0.70, 1.25),
        (0.70, 1.30),
        (0.75, 1.25),
    ]
    
    for beta, t in combinacoes:
        print(f"\n{'='*80}")
        print(f"📊 COMBINAÇÃO β={beta}, t={t}")
        print(f"{'='*80}")
        
        r = auditar_fronteiras(beta, t)
        
        print(f"\n   Vetores exatamente no limiar (score = {t}):")
        print(f"      Total: {r['exatamente'][0]}")
        print(f"      Níveis: {r['exatamente'][1]}")
        
        print(f"\n   Vetores próximos abaixo (0 < {t} - score < 0.01):")
        print(f"      Total: {r['proximos_abaixo'][0]}")
        print(f"      Níveis: {r['proximos_abaixo'][1]}")
        
        print(f"\n   Vetores próximos acima (0 < score - {t} < 0.01):")
        print(f"      Total: {r['proximos_acima'][0]}")
        print(f"      Níveis: {r['proximos_acima'][1]}")
        
        print(f"\n   Total abaixo do limiar (score < {t}): {r['total_abaixo']}")
        print(f"   Total acima do limiar (score > {t}): {r['total_acima']}")
        print(f"   Soma: {r['total_abaixo'] + r['exatamente'][0] + r['total_acima']}")
    
    # Resumo
    print(f"\n{'='*80}")
    print(f"🏆 RESUMO DA AUDITORIA DE FRONTEIRAS")
    print(f"{'='*80}")
    
    print(f"\n   {'Combinação':<20} {'No limiar':<12} {'Próx. abaixo':<15} {'Próx. acima':<15}")
    print(f"   {'-'*20} {'-'*12} {'-'*15} {'-'*15}")
    
    for beta, t in combinacoes:
        r = auditar_fronteiras(beta, t)
        nome = f"β={beta}, t={t}"
        print(f"   {nome:<20} {r['exatamente'][0]:<12} {r['proximos_abaixo'][0]:<15} {r['proximos_acima'][0]:<15}")

if __name__ == "__main__":
    main()