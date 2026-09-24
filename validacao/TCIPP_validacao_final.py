#!/usr/bin/env python3
"""
TCIPP_validacao_final.py — Validação Final das 4 Combinações

Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026

OBJETIVO:
Testar as 4 combinações válidas de (β, t) contra o conjunto completo
de requisitos do TCIPP:
1. Seis casos críticos
2. Distribuição dos 3125 vetores
3. Monotonicidade (0 violações)
4. Invariância de ordem
5. Fronteiras (scores próximos de t)
6. Intervalo do score (negativos permitidos?)
7. Integração R10 V2
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

# =============================================================================
# VERIFICAÇÃO 1 — SEIS CASOS CRÍTICOS
# =============================================================================

def verificar_casos_criticos(beta, t):
    casos = {
        '[1,1,1,1,1] Degenerado': ((1,1,1,1,1), 1),
        '[1,5,1,5,1] Caótico':    ((1,5,1,5,1), 1),
        '[2,2,2,2,2] Ruim':       ((2,2,2,2,2), 2),
        '[3,3,3,3,3] Médio':      ((3,3,3,3,3), 3),
        '[4,4,4,4,4] Bom':        ((4,4,4,4,4), 4),
        '[5,5,5,5,5] Excelente':  ((5,5,5,5,5), 5),
    }
    
    resultados = {}
    todos_ok = True
    for nome, (v, esperado) in casos.items():
        score = calcular_score(v, beta)
        nivel = classificar(score, t)
        ok = (nivel == esperado)
        if not ok:
            todos_ok = False
        resultados[nome] = (score, nivel, esperado, ok)
    
    return todos_ok, resultados

# =============================================================================
# VERIFICAÇÃO 2 — DISTRIBUIÇÃO DOS 3125 VETORES
# =============================================================================

def verificar_distribuicao(beta, t):
    all_v = list(itertools.product(DIMENSOES, repeat=5))
    niveis = [classificar(calcular_score(v, beta), t) for v in all_v]
    dist = pd.Series(niveis).value_counts().sort_index().to_dict()
    return dist, all_v, niveis

# =============================================================================
# VERIFICAÇÃO 3 — MONOTONICIDADE
# =============================================================================

def verificar_monotonicidade(beta, t):
    all_v = list(itertools.product(DIMENSOES, repeat=5))
    vector_to_level = {v: classificar(calcular_score(v, beta), t) for v in all_v}
    
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
                    if len(exemplos) < 3:
                        exemplos.append((vA, vB, lvlA, lvlB))
    
    return violations, exemplos

# =============================================================================
# VERIFICAÇÃO 4 — INVARIÂNCIA DE ORDEM
# =============================================================================

def verificar_invariancia_ordem(beta):
    all_v = list(itertools.product(DIMENSOES, repeat=5))
    inconsistencias = 0
    for v in all_v:
        score_original = calcular_score(v, beta)
        v_invertido = tuple(reversed(v))
        score_invertido = calcular_score(v_invertido, beta)
        if abs(score_original - score_invertido) > 1e-9:
            inconsistencias += 1
    return inconsistencias

# =============================================================================
# VERIFICAÇÃO 5 — FRONTEIRAS
# =============================================================================

def verificar_fronteiras(beta, t):
    """Testa vetores cujos scores estão próximos do limiar t."""
    all_v = list(itertools.product(DIMENSOES, repeat=5))
    
    # Vetores com score exatamente igual a t
    exatamente = [v for v in all_v if abs(calcular_score(v, beta) - t) < 1e-9]
    
    # Vetores com score logo abaixo de t
    abaixo = [v for v in all_v if 0 < t - calcular_score(v, beta) < 0.01]
    
    # Vetores com score logo acima de t
    acima = [v for v in all_v if 0 < calcular_score(v, beta) - t < 0.01]
    
    # Verificar consistência
    niveis_exatamente = [classificar(calcular_score(v, beta), t) for v in exatamente]
    niveis_abaixo = [classificar(calcular_score(v, beta), t) for v in abaixo]
    niveis_acima = [classificar(calcular_score(v, beta), t) for v in acima]
    
    return {
        'exatamente': (len(exatamente), set(niveis_exatamente)),
        'abaixo': (len(abaixo), set(niveis_abaixo)),
        'acima': (len(acima), set(niveis_acima)),
    }

# =============================================================================
# VERIFICAÇÃO 6 — INTERVALO DO SCORE
# =============================================================================

def verificar_intervalo(beta):
    all_v = list(itertools.product(DIMENSOES, repeat=5))
    scores = [calcular_score(v, beta) for v in all_v]
    
    negativos = [s for s in scores if s < 0]
    acima_5 = [s for s in scores if s > 5]
    
    return {
        'min': min(scores),
        'max': max(scores),
        'negativos': len(negativos),
        'acima_5': len(acima_5),
        'menor_negativo': min(negativos) if negativos else None,
    }

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("🔬 TCIPP — VALIDAÇÃO FINAL DAS 4 COMBINAÇÕES")
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
    
    resultados_finais = {}
    
    for beta, t in combinacoes:
        print(f"\n{'='*80}")
        print(f"📊 COMBINAÇÃO β={beta}, t={t}")
        print(f"{'='*80}")
        
        # 1. Casos críticos
        print(f"\n1️⃣ CASOS CRÍTICOS")
        ok, casos = verificar_casos_criticos(beta, t)
        for nome, (score, nivel, esperado, ok_caso) in casos.items():
            status = "✅" if ok_caso else "❌"
            print(f"   {status} {nome}: score={score:.4f}, nível={nivel} (esperado={esperado})")
        
        # 2. Distribuição
        print(f"\n2️⃣ DISTRIBUIÇÃO")
        dist, all_v, niveis = verificar_distribuicao(beta, t)
        for nivel in sorted(dist.keys()):
            freq = dist[nivel]
            pct = freq / 3125 * 100
            print(f"   Nível {nivel}: {freq} vetores ({pct:.1f}%)")
        
        # 3. Monotonicidade
        print(f"\n3️⃣ MONOTONICIDADE")
        viol, exemplos = verificar_monotonicidade(beta, t)
        if viol == 0:
            print(f"   ✅ 0 violações")
        else:
            print(f"   ❌ {viol} violações")
            for vA, vB, lA, lB in exemplos:
                print(f"      {vA} (N{lA}) → {vB} (N{lB})")
        
        # 4. Invariância de ordem
        print(f"\n4️⃣ INVARIÂNCIA DE ORDEM")
        inv = verificar_invariancia_ordem(beta)
        if inv == 0:
            print(f"   ✅ 0 inconsistências")
        else:
            print(f"   ❌ {inv} inconsistências")
        
        # 5. Fronteiras
        print(f"\n5️⃣ FRONTEIRAS")
        front = verificar_fronteiras(beta, t)
        print(f"   Score = {t}: {front['exatamente'][0]} vetores, níveis: {front['exatamente'][1]}")
        print(f"   Score < {t}: {front['abaixo'][0]} vetores, níveis: {front['abaixo'][1]}")
        print(f"   Score > {t}: {front['acima'][0]} vetores, níveis: {front['acima'][1]}")
        
        # 6. Intervalo
        print(f"\n6️⃣ INTERVALO DO SCORE")
        intervalo = verificar_intervalo(beta)
        print(f"   Mínimo: {intervalo['min']:.4f}")
        print(f"   Máximo: {intervalo['max']:.4f}")
        print(f"   Negativos: {intervalo['negativos']}")
        if intervalo['negativos'] > 0:
            print(f"   Menor negativo: {intervalo['menor_negativo']:.4f}")
        
        # Armazenar resultados
        resultados_finais[(beta, t)] = {
            'casos_ok': ok,
            'dist': dist,
            'violacoes': viol,
            'inv_ordem': inv,
            'fronteiras': front,
            'intervalo': intervalo,
        }
    
    # Resumo final
    print(f"\n{'='*80}")
    print(f"🏆 RESUMO COMPARATIVO")
    print(f"{'='*80}")
    
    print(f"\n   {'Combinação':<20} {'Casos':<10} {'Monot.':<10} {'Inv.Ordem':<12} {'Neg.':<8}")
    print(f"   {'-'*20} {'-'*10} {'-'*10} {'-'*12} {'-'*8}")
    
    for (beta, t), r in resultados_finais.items():
        casos_status = "✅" if r['casos_ok'] else "❌"
        monot_status = "✅" if r['violacoes'] == 0 else "❌"
        inv_status = "✅" if r['inv_ordem'] == 0 else "❌"
        neg_status = f"{r['intervalo']['negativos']}"
        
        nome = f"β={beta}, t={t}"
        print(f"   {nome:<20} {casos_status:<10} {monot_status:<10} {inv_status:<12} {neg_status:<8}")
    
    # Recomendação
    print(f"\n{'='*80}")
    print(f"📋 RECOMENDAÇÃO")
    print(f"{'='*80}")
    
    validas = [(bt, r) for bt, r in resultados_finais.items() 
               if r['casos_ok'] and r['violacoes'] == 0 and r['inv_ordem'] == 0]
    
    if len(validas) == 4:
        print("\n   ✅ Todas as 4 combinações são válidas.")
        print("\n   Critérios para escolha:")
        print("   - Parcimônia: menor β")
        print("   - Robustez: maior margem entre caótico e uniforme")
        print("   - Fronteiras: comportamento consistente")
    else:
        print(f"\n   ⚠️ Apenas {len(validas)} de 4 combinações são válidas.")

if __name__ == "__main__":
    main()