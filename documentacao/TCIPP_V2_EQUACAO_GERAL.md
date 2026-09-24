# TCIPP V2.0 FINAL — Equação Geral


**Autor:** Neemias da Silva Ferreira  
**ORCID:** [0009-0005-1552-6018](https://orcid.org/0009-0005-1552-6018)  
**Data:** 23 de setembro de 2026  
**Local:** Maceió-Alagoas, Brasil

## Configuração Oficial

| Parâmetro | Valor |
|-----------|-------|
| β | 0.70 |
| t | 1.25 |
| Limiares | [1.25, 2.5, 3.5, 4.5] |
| Scores negativos | Permitidos |
| Regra de fronteira | ≥ |

## Função de Score

S(x) = média(x) - 0.70 * max(0, 3 - min(x))

Onde:
- média(x) = (x1 + x2 + x3 + x4 + x5) / 5
- min(x) = menor valor entre x1, x2, x3, x4, x5

## Classificação

M(x) = 1, se S(x) < 1.25
M(x) = 2, se 1.25 <= S(x) < 2.5
M(x) = 3, se 2.5 <= S(x) < 3.5
M(x) = 4, se 3.5 <= S(x) < 4.5
M(x) = 5, se S(x) >= 4.5

## Casos Críticos Verificados

| Vetor | Score | Nível |
|-------|-------|-------|
| [1,1,1,1,1] | -0.40 | 1 |
| [1,5,1,5,1] | 1.20 | 1 |
| [2,2,2,2,2] | 1.30 | 2 |
| [3,3,3,3,3] | 3.00 | 3 |
| [4,4,4,4,4] | 4.00 | 4 |
| [5,5,5,5,5] | 5.00 | 5 |

## Propriedades Matemáticas

- Monotonicidade: 0 violações
- Invariância de ordem: 0 inconsistências
- Intervalo do score: [-0.40, 5.00]
- Scores negativos: Permitidos (6 vetores)

## Distribuição

| Nível | Vetores | Percentual |
|-------|---------|------------|
| 1 | 951 | 30.4% |
| 2 | 1346 | 43.1% |
| 3 | 581 | 18.6% |
| 4 | 226 | 7.2% |
| 5 | 21 | 0.7% |

## Equação Geral Consolidada

TCIPP(x) = ( d(x), r*(x), M(x), A(x), R(x), Q(x) )

Onde:
- d_r(x) = (1/5) * soma(|xi - p_ri|)
- r*(x) = argmin d_r(x)
- S(x) = média(x) - 0.70 * max(0, 3 - min(x))
- M(x) = classificação por limiares
- A_i(xi) = alerta dimensional
- Q(x) = 1 se M(x) >= 3, 0 caso contrário