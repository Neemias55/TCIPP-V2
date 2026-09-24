# TCIPP — Tool for Continuous Improvement and Process Performance

**Autor:** Neemias da Silva Ferreira  
**ORCID:** [0009-0005-1552-6018](https://orcid.org/0009-0005-1552-6018)  
**Data:** 23 de setembro de 2026  
**Local:** Maceió, Alagoas, Brasil

---

## Sobre o TCIPP

O **TCIPP** é uma ferramenta de diagnóstico organizacional que transforma cinco respostas, registradas em escala de 1 a 5, em um nível de maturidade de 1 a 5.

### As cinco dimensões

1. Inovação
2. Processos
3. Estabilidade
4. Adaptabilidade
5. Integração

### Os cinco níveis

| Nível | Nome | Descrição |
|---|---|---|
| 1 | Inicial | Predomínio de caos ou rigidez |
| 2 | Reconhecimento | Separação entre projeto e rotina |
| 3 | Estruturação | Alternância controlada |
| 4 | Coexistência | Projetos e processos se alimentam |
| 5 | Maturidade Espiral | Aprendizado contínuo |

## Equação oficial — V2.0 FINAL

### TESTE DE RENDERIZAÇÃO

$$
S(x) = \text{média}(x) - 0{,}70 \times \max(0, 3 - \min(x))
$$

Em que `x` representa o conjunto das cinco respostas.

### Classificação

| Condição do score | Nível |
|---|---:|
| S(x) < 1,25 | 1 |
| 1,25 ≤ S(x) < 2,5 | 2 |
| 2,5 ≤ S(x) < 3,5 | 3 |
| 3,5 ≤ S(x) < 4,5 | 4 |
| S(x) ≥ 4,5 | 5 |

### Parâmetros congelados

| Parâmetro | Valor |
|---|---|
| β | 0,70 |
| t | 1,25 |
| Limiares | [1,25; 2,5; 3,5; 4,5] |

## Scripts principais

| Script | Finalidade |
|---|---|
| `codigo/TCIPP_MASTER_V2.0_FINAL.py` | Implementação indicada como versão oficial |
| `codigo/TCIPP_graficos.py` | Geração de gráficos |
| `codigo/gerar_painel.py` | Gerador de painel consolidado, caso esteja presente no pacote |

> Antes da publicação, confirme que todos os arquivos citados estão incluídos e que os exemplos de execução correspondem às interfaces reais dos scripts.

## Estrutura do repositório

```text
TCIPP/
├── README.md
├── codigo/
│   ├── TCIPP_MASTER_V2.0_FINAL.py
│   ├── TCIPP_graficos.py
│   └── gerar_painel.py
├── validacao/
├── auditoria/
├── documentacao/
├── grafico/
└── resultado/
```

## Requisitos e execução

O ambiente e as dependências exatas devem ser conferidos nos scripts da versão publicada. Caso os scripts utilizem as bibliotecas abaixo, instale-as com:

```bash
pip install numpy pandas matplotlib
```

Execute a partir da pasta do projeto, após confirmar os argumentos e caminhos esperados pelo script:

```bash
python codigo/TCIPP_MASTER_V2.0_FINAL.py
```

Os nomes de classes, métodos e formatos de retorno devem ser consultados diretamente na implementação oficial. O nome do arquivo contém pontos (`V2.0`), portanto não deve ser presumido como um módulo importável com um `from ... import ...` convencional.

## Documentação

- [Guia detalhado](documentacao/TCIPP_V2_README.md)
- [Equação geral](documentacao/TCIPP_V2_EQUACAO_GERAL.md)
- [Configuração](documentacao/TCIPP_V2_CONFIGURACAO.md)
- [Auditoria](documentacao/TCIPP_V2_AUDITORIA.md)

## Contato

- **ORCID:** [0009-0005-1552-6018](https://orcid.org/0009-0005-1552-6018)
- **Local:** Maceió, Alagoas, Brasil
