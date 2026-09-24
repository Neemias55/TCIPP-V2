#!/usr/bin/env python3
"""
TCIPP_monotonicidade_final.py — Teste de Monotonicidade Final

Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026

OBJETIVO:
Testar monotonicidade para a combinação escolhida (β=0.70, t=1.25)
após a correção da auditoria de fronteiras.
"""

import itertools
import pandas as pd
import numpy as np
from datetime import datetime

DIMENSOES = [1, 2, 3, 4, 5]
LIMIARES_FIXOS = [2.5, 3.5, 4.5]
BETA = 0.70
T = 1.25

def calcular_score(v, beta=BETA):
    media = sum(v) / len(v)
    gargalo = max(0, 3 - min(v))
    return media - beta * gargalo

def classificar(score, t=T):
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

def validar_monotonicidade():
    all_v = list(itertools.product(DIMENSOES, repeat=5))
    vector_to_level = {v: classificar(calcular_score(v)) for v in all_v}
    
    violations = 0
    exemplos = []
    
    for vA in all_v:
        lvlA = vector_to_level[vA]
        for i in range(5):
            if vA[i] < 5:
                vB = list(vA)
                vB[i] += 1
                vB = tuple(vB)
                lvlB = vector_to_level[vB]
                if lvlB < lvlA:
                    violations += 1
                    if len(exemplos) < 5:
                        exemplos.append((vA, vB, lvlA, lvlB))
    
    return violations, exemplos

def main():
    print("=" * 80)
    print("🔬 TCIPP — TESTE DE MONOTONICIDADE FINAL")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Autor: Neemias da Silva Ferreira")
    print(f"📋 ORCID: 0009-0005-1552-6018")
    print("=" * 80)
    
    print(f"""
    CONFIGURAÇÃO:
    β = {BETA}
    t = {T}
    Limiares fixos: {LIMIARES_FIXOS}
    """)
    
    print("\n📊 Testando monotonicidade em todos os 3125 vetores...")
    violations, exemplos = validar_monotonicidade()
    
    print(f"\n   Total de violações: {violations}")
    
    if violations == 0:
        print("   ✅ ZERO VIOLAÇÕES DE MONOTONICIDADE!")
    else:
        print("   ❌ VIOLAÇÕES ENCONTRADAS:")
        for vA, vB, lA, lB in exemplos:
            print(f"      {vA} (N{lA}) → {vB} (N{lB})")
    
    print("\n" + "=" * 80)
    print("🏆 VEREDICTO")
    print("=" * 80)
    if violations == 0:
        print("   ✅ MONOTONICIDADE APROVADA")
    else:
        print(f"   ❌ MONOTONICIDADE REPROVADA: {violations} violações")
    print("=" * 80)

if __name__ == "__main__":
    main()