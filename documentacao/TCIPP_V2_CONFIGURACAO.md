# TCIPP V2.0 FINAL — Configuração Oficial


**Autor:** Neemias da Silva Ferreira  
**ORCID:** [0009-0005-1552-6018](https://orcid.org/0009-0005-1552-6018)  
**Data:** 23 de setembro de 2026  
**Local:** Maceió-Alagoas, Brasil

## Parâmetros Matemáticos

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| β | 0.70 | Coeficiente de penalização do gargalo |
| t | 1.25 | Limiar entre Nível 1 e Nível 2 |
| Limiares | [1.25, 2.5, 3.5, 4.5] | Limiares de classificação |
| Scores negativos | Permitidos | Não limitar a [0, 5] |
| Regra de fronteira | ≥ | O limiar pertence ao nível superior |

## Função de Score

S(x) = média(x) - 0.70 * max(0, 3 - min(x))

## Classificação

M(x) = 1, se S(x) < 1.25
M(x) = 2, se 1.25 <= S(x) < 2.5
M(x) = 3, se 2.5 <= S(x) < 3.5
M(x) = 4, se 3.5 <= S(x) < 4.5
M(x) = 5, se S(x) >= 4.5

## Regra de Fronteira

Em todos os limiares, o valor exato pertence ao nível superior:
- S(x) = 1.25 → Nível 2
- S(x) = 2.5 → Nível 3
- S(x) = 3.5 → Nível 4
- S(x) = 4.5 → Nível 5

## Scores Negativos

Permitidos. Eles resultam da aplicação da penalização por gargalo e são
classificados no Nível 1. O valor negativo não representa uma dimensão
abaixo do mínimo nem, isoladamente, comprova degeneração organizacional.

## Justificativa da Escolha de β = 0.70 e t = 1.25

| Critério | β=0.65 | β=0.70, t=1.25 | β=0.75 |
|----------|--------|----------------|--------|
| Parcimônia | 1º | 2º | 4º |
| Robustez | 4º | 2º | 1º |
| Fronteiras | ⚠️ | ✅ | ⚠️ |
| Negativos | 6 | 6 | 21 |

Vencedor: β=0.70, t=1.25

Vantagens:
- Fronteira limpa (nenhum vetor no limiar)
- Margem de 0.10 (robusta)
- Apenas 6 scores negativos
- Distribuição equilibrada