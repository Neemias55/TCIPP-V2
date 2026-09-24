# TCIPP V2.0 — Guia de Uso e Referência

**Autor:** Neemias da Silva Ferreira  
**ORCID:** [0009-0005-1552-6018](https://orcid.org/0009-0005-1552-6018)  
**Versão documentada:** TCIPP V2.0 FINAL  
**Data:** 23 de setembro de 2026

> **Nota de integridade documental:** este guia consolida os parâmetros e conceitos fornecidos para a V2.0. Detalhes de API, nomes de funções, mensagens de retorno, resultados empíricos e referências bibliográficas não foram presumidos. Antes da publicação, confronte-os com `codigo/TCIPP_MASTER_V2.0_FINAL.py`, os arquivos de auditoria e os resultados reproduzíveis.

---

## 1. Finalidade

O TCIPP (Tool for Continuous Improvement and Process Performance) é apresentado como uma ferramenta de diagnóstico organizacional. A entrada é composta por cinco respostas em escala de 1 a 5; a saída central é um nível de maturidade entre 1 e 5.

O nível é uma classificação diagnóstica produzida pela regra matemática da versão. Não deve ser interpretado, sem validação adicional, como certificação, previsão de desempenho ou avaliação universal de uma organização.

## 2. Dimensões avaliadas

1. Inovação
2. Processos
3. Estabilidade
4. Adaptabilidade
5. Integração

Cada resposta deve respeitar a escala definida pela implementação. Verifique no script oficial se há validação de tipo, tratamento de valores ausentes e rejeição de entradas fora do intervalo.

## 3. Níveis de maturidade

| Nível | Nome | Descrição |
|---|---|---|
| 1 | Inicial | Predomínio de caos ou rigidez |
| 2 | Reconhecimento | Separação entre projeto e rotina |
| 3 | Estruturação | Alternância controlada |
| 4 | Coexistência | Projetos e processos se alimentam |
| 5 | Maturidade Espiral | Aprendizado contínuo |

Esses rótulos descrevem a escala conceitual do TCIPP. A interpretação de um resultado deve considerar o contexto e as limitações do instrumento.

## 4. Equação e parâmetros congelados

A função de score informada para a V2.0 FINAL é:

\[
S(x) = \operatorname{média}(x) - 0{,}70 \times \max(0, 3 - \min(x))
\]

Parâmetros:

| Parâmetro | Valor |
|---|---|
| β | 0,70 |
| t | 1,25 |
| Limiares | [1,25; 2,5; 3,5; 4,5] |

Classificação por intervalos:

| Condição | Nível |
|---|---:|
| S(x) < 1,25 | 1 |
| 1,25 ≤ S(x) < 2,5 | 2 |
| 2,5 ≤ S(x) < 3,5 | 3 |
| 3,5 ≤ S(x) < 4,5 | 4 |
| S(x) ≥ 4,5 | 5 |

A fronteira é inclusiva no nível superior: um score exatamente igual a um limiar pertence ao nível que começa naquele limiar. Scores negativos são permitidos pela configuração congelada; não se deve aplicar truncamento em zero sem alterar formalmente a versão.

## 5. Fluxo de uso

1. Registre cinco respostas válidas, uma por dimensão.
2. Encaminhe o vetor à implementação oficial.
3. Obtenha o score e o nível calculados pelo programa.
4. Registre a versão do código e os parâmetros utilizados.
5. Interprete o resultado junto ao contexto do diagnóstico.

### Exemplo de entrada

```python
respostas = [5, 4, 5, 4, 5]
```

Este exemplo mostra apenas o formato do vetor. A chamada executável depende da API efetivamente definida no script oficial. Não presuma nomes de classe, método ou chaves de retorno sem conferir o código.

## 6. API e contrato de retorno

A API pública deve ser documentada diretamente a partir de `TCIPP_MASTER_V2.0_FINAL.py`. Antes de publicar exemplos de importação, registre:

- nome real da classe ou função de entrada;
- parâmetros obrigatórios e opcionais;
- validações aplicadas ao vetor;
- estrutura exata do retorno;
- tratamento de erros e entradas inválidas;
- dependências e versão mínima do Python.

**Não publique como contrato confirmado** uma chamada ilustrativa que ainda não tenha sido executada contra o arquivo oficial.

## 7. Casos críticos e testes de fronteira

A validação da V2.0 deve incluir, no mínimo, os seguintes grupos. Os resultados esperados precisam ser reproduzidos pela implementação antes de serem apresentados como evidência:

1. Vetores uniformes nos extremos da escala.
2. Vetores uniformes nos pontos intermediários.
3. Vetores com uma resposta baixa e as demais altas.
4. Vetores com uma resposta alta e as demais baixas.
5. Scores exatamente nos limiares 1,25; 2,5; 3,5 e 4,5.
6. Entradas inválidas: quantidade diferente de cinco, valores fora da escala, tipos incompatíveis e valores ausentes.

Registre entrada, score, nível esperado, nível observado e resultado do teste. Não atribua resultados numéricos a esses casos sem executar a versão congelada.

## 8. Distribuição e resultados experimentais

Distribuições de níveis, frequências, empates, reduções de nível e comparações entre versões devem ser acompanhadas do arquivo de resultados, do número de vetores avaliados, dos parâmetros e do script que produziu a tabela.

Não há, neste documento, uma distribuição numérica declarada como resultado oficial. Inclua-a somente após confirmar a correspondência entre os dados, o código V2.0 FINAL e o log de execução.

## 9. Gráficos e painel

O projeto lista `TCIPP_graficos.py` como gerador de gráficos. Um gerador de painel consolidado (`gerar_painel.py`) também foi mencionado no planejamento do repositório; confirme sua presença e compatibilidade antes de incluí-lo como script oficial.

Documente, para cada artefato visual:

- script gerador;
- arquivo de entrada utilizado;
- data e versão da execução;
- significado dos eixos e categorias;
- diretório de saída.

## 10. Reprodutibilidade e auditoria

Para permitir reprodução independente:

- mantenha a versão oficial identificada e sem alterações silenciosas;
- preserve os parâmetros congelados;
- registre o comando executado e o ambiente;
- associe cada resultado ao CSV/log correspondente;
- diferencie testes de validação, análises exploratórias e resultados finais;
- não misture saídas de versões distintas sem identificá-las.

## 11. Limitações de interpretação

O TCIPP produz uma classificação segundo uma regra matemática e uma escala conceitual. A validade externa, a confiabilidade, a sensibilidade a diferentes contextos e a relação com resultados organizacionais precisam ser sustentadas por estudos e evidências apropriados. Um nível isolado não substitui análise contextual nem deve ser apresentado como garantia de desempenho.

## 12. Documentos relacionados

- `TCIPP_V2_EQUACAO_GERAL.md`
- `TCIPP_V2_CONFIGURACAO.md`
- `TCIPP_V2_AUDITORIA.md`
- `tcipp_run_log.txt`
- arquivos de validação e resultados correspondentes

Confira se esses arquivos acompanham a versão publicada e se seus conteúdos se referem especificamente à V2.0 FINAL.

## 13. Checklist antes da publicação

- [ ] A equação e os limiares coincidem com o script oficial.
- [ ] Os testes de fronteira foram executados e registrados.
- [ ] A API documentada foi conferida no código.
- [ ] Os exemplos foram executados em ambiente limpo.
- [ ] Todos os scripts citados existem no repositório.
- [ ] Gráficos e CSVs têm origem e versão identificadas.
- [ ] Resultados numéricos têm logs reproduzíveis.
- [ ] O README da raiz aponta para este guia.
