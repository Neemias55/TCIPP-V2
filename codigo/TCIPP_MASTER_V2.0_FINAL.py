"""
Autor: Neemias da Silva Ferreira
ORCID: 0009-0005-1552-6018
Data: 23 de setembro de 2026
Maceió-Alagoas
"""


import numpy as np
import re
import unicodedata
from collections import Counter
from datetime import datetime
from copy import deepcopy
from numbers import Integral

# =============================================================================
# CONFIGURAÇÕES DO TCIPP
# =============================================================================

class ConfigTCIPP:
    """Configuração central do TCIPP"""
    VERSAO = "TCIPP_MASTER_V2.0_FINAL"
    AUTOR = "Neemias da Silva Ferreira"
    ORCID = "0009-0005-1552-6018"
    DATA = "2026-09-23"
    
    # 5 dimensões do TCIPP
    DIMENSOES = [
        "Inovação",
        "Processos",
        "Estabilidade",
        "Adaptabilidade",
        "Integração"
    ]
    
    # 6 arquétipos de referência
    REFERENCIAS = {
        'IDEAL':      {'perfil': [5, 5, 5, 5, 5], 'icone': '🏆', 'descricao': 'Perfeição absoluta'},
        'NEUTRO':     {'perfil': [3, 3, 3, 3, 3], 'icone': '⚖️', 'descricao': 'Equilíbrio genérico'},
        'ESTAVEL':    {'perfil': [4, 4, 4, 4, 4], 'icone': '🛡️', 'descricao': 'Foco em processos'},
        'INOVADOR':   {'perfil': [5, 3, 5, 3, 5], 'icone': '🚀', 'descricao': 'Foco em inovação'},
        'PROCESSUAL': {'perfil': [3, 5, 3, 5, 3], 'icone': '⚙️', 'descricao': 'Foco em disciplina'},
        'CAOTICO':    {'perfil': [1, 5, 2, 4, 3], 'icone': '💀', 'descricao': 'Referência negativa'}
    }
    
    # 5 níveis de maturidade
    NIVEIS = {
        1: {'nome': 'Inicial', 'icone': '🟥', 'descricao': 'Predomínio de caos ou rigidez'},
        2: {'nome': 'Reconhecimento', 'icone': '🟧', 'descricao': 'Separação entre projeto e rotina'},
        3: {'nome': 'Estruturação', 'icone': '🟨', 'descricao': 'Alternância controlada'},
        4: {'nome': 'Coexistência', 'icone': '🟩', 'descricao': 'Projetos e processos se alimentam'},
        5: {'nome': 'Maturidade Espiral', 'icone': '🟦', 'descricao': 'Aprendizado contínuo'}
    }
    
    # Recomendações por nível
    RECOMENDACOES = {
        1: "Focar em estabilização básica e definição de processos",
        2: "Separar claramente projetos de operação",
        3: "Alternar ciclos de inovação e estabilização",
        4: "Integrar projetos e processos em fluxo contínuo",
        5: "Manter aprendizado contínuo e adaptação"
    }
    
    # ==========================================================================
    # CONFIGURAÇÃO MATEMÁTICA OFICIAL — TCIPP V2.0 FINAL
    # ==========================================================================
    # Função de score: S(x) = média(x) - BETA * max(0, 3 - min(x))
    # Limiares: [t_N1_N2, t_N2_N3, t_N3_N4, t_N4_N5]
    # Regra de fronteira: o limiar pertence ao nível superior (≥)
    # Scores negativos: permitidos
    # ==========================================================================
    BETA = 0.70
    LIMIARES = [1.25, 2.5, 3.5, 4.5]


# =============================================================================
# CLASSE PRINCIPAL DO TCIPP
# =============================================================================

class TCIPP:
    """
    Tool for Continuous Improvement and Process Performance
    
    VERSÃO 2.0 FINAL — Configuração oficial
    """
    
    def __init__(self):
        self.config = ConfigTCIPP()
        for atributo in ("DIMENSOES", "REFERENCIAS", "NIVEIS", "RECOMENDACOES"):
            setattr(self.config, atributo, deepcopy(getattr(ConfigTCIPP, atributo)))
        self.historico = []
    
    # -------------------------------------------------------------------------
    # 1. AUDITORIA DE ORGANIZAÇÃO (5 RESPOSTAS)
    # -------------------------------------------------------------------------

    def _validar_configuracao(self):
        """Valida a integridade mínima da configuração antes de usá-la."""
        if not isinstance(self.config.VERSAO, str) or not self.config.VERSAO.strip():
            return "VERSAO deve ser um texto não vazio"
        if not isinstance(self.config.AUTOR, str) or not self.config.AUTOR.strip():
            return "AUTOR deve ser um texto não vazio"
        if not isinstance(self.config.ORCID, str) or not self.config.ORCID.strip():
            return "ORCID deve ser um texto não vazio"
        orcid = self.config.ORCID.strip()
        if not re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", orcid):
            return "ORCID deve seguir o formato XXXX-XXXX-XXXX-XXXX"
        compact = orcid.replace("-", "")
        total = 0
        for char in compact[:15]:
            total = (total + int(char)) * 2
        remainder = (12 - (total % 11)) % 11
        check_digit = "X" if remainder == 10 else str(remainder)
        if compact[-1] != check_digit:
            return "ORCID inválido: dígito verificador não confere"
        if not isinstance(self.config.DATA, str):
            return "DATA deve ser um texto no formato ISO 8601"
        try:
            datetime.fromisoformat(self.config.DATA)
        except (TypeError, ValueError):
            return "DATA deve ser uma data ISO 8601 válida"
        if not isinstance(self.config.DIMENSOES, (list, tuple)) or len(self.config.DIMENSOES) != 5:
            return "DIMENSOES deve conter exatamente 5 itens"
        if not all(isinstance(x, str) and x.strip() for x in self.config.DIMENSOES):
            return "DIMENSOES deve conter apenas nomes textuais não vazios"
        if len(set(x.strip().casefold() for x in self.config.DIMENSOES)) != 5:
            return "DIMENSOES deve conter 5 nomes únicos (sem duplicatas)"
        referencias_esperadas = {'IDEAL', 'NEUTRO', 'ESTAVEL', 'INOVADOR', 'PROCESSUAL', 'CAOTICO'}
        if not isinstance(self.config.REFERENCIAS, dict) or set(self.config.REFERENCIAS) != referencias_esperadas:
            return "REFERENCIAS deve conter exatamente: IDEAL, NEUTRO, ESTAVEL, INOVADOR, PROCESSUAL e CAOTICO"
        for nome, ref in self.config.REFERENCIAS.items():
            if not isinstance(nome, str) or not nome or not isinstance(ref, dict):
                return "Cada referência deve ter nome e configuração válidos"
            perfil = ref.get('perfil')
            if not isinstance(perfil, (list, tuple)) or len(perfil) != 5 or not all(
                isinstance(v, Integral) and not isinstance(v, bool) and 1 <= v <= 5 for v in perfil
            ):
                return f"Perfil inválido na referência {nome!r}: são necessários 5 inteiros entre 1 e 5"
            if (not isinstance(ref.get('icone'), str) or not ref.get('icone').strip() or
                    not isinstance(ref.get('descricao'), str) or not ref.get('descricao').strip()):
                return f"Ícone ou descrição inválidos/vazios na referência {nome!r}"
        if (not isinstance(self.config.NIVEIS, dict) or
                set(self.config.NIVEIS) != {1, 2, 3, 4, 5} or
                any(type(nivel) is not int for nivel in self.config.NIVEIS)):
            return "NIVEIS deve definir exatamente os níveis inteiros 1 a 5 (sem booleanos)"
        for nivel, cfg in self.config.NIVEIS.items():
            if (not isinstance(cfg, dict) or
                    not all(isinstance(cfg.get(k), str) and cfg.get(k).strip()
                            for k in ('nome', 'icone', 'descricao'))):
                return f"Configuração inválida ou incompleta para o nível {nivel}"
        if not isinstance(self.config.RECOMENDACOES, dict):
            return "RECOMENDACOES deve ser um dicionário"
        if (set(self.config.RECOMENDACOES) != {1, 2, 3, 4, 5} or
                any(type(nivel) is not int for nivel in self.config.RECOMENDACOES)):
            return "RECOMENDACOES deve definir exatamente os níveis inteiros 1 a 5 (sem booleanos)"
        if not all(isinstance(texto, str) and texto.strip()
                   for texto in self.config.RECOMENDACOES.values()):
            return "RECOMENDACOES deve conter textos não vazios para todos os níveis"
        # Validar parâmetros da função de score
        if not isinstance(self.config.BETA, (int, float)) or isinstance(self.config.BETA, bool):
            return "BETA deve ser um número real"
        if self.config.BETA < 0:
            return "BETA deve ser não negativo"
        if not isinstance(self.config.LIMIARES, (list, tuple)) or len(self.config.LIMIARES) != 4:
            return "LIMIARES deve conter exatamente 4 valores"
        if not all(isinstance(l, (int, float)) and not isinstance(l, bool) for l in self.config.LIMIARES):
            return "LIMIARES deve conter apenas números reais"
        if not all(self.config.LIMIARES[i] < self.config.LIMIARES[i+1] for i in range(3)):
            return "LIMIARES deve estar em ordem crescente"
        return None

    def auditar(self, respostas):
        """
        Audita uma organização com base em 5 respostas (escala 1 a 5).
        """
        erro_config = self._validar_configuracao()
        if erro_config:
            return {'erro': f'Configuração TCIPP inválida: {erro_config}'}
        if not isinstance(respostas, (list, tuple)):
            return {'erro': 'As respostas devem ser uma lista ou tupla com exatamente 5 inteiros'}
        if len(respostas) != 5:
            return {'erro': 'São necessárias exatamente 5 respostas'}

        for i, r in enumerate(respostas):
            if isinstance(r, bool) or not isinstance(r, Integral) or not 1 <= r <= 5:
                return {'erro': f'Resposta {i+1} inválida: {r}. Use um inteiro entre 1 e 5.'}
        respostas = [int(r) for r in respostas]
        
        distancias = self._calcular_distancias(respostas)
        
        ordem_refs = ('IDEAL', 'NEUTRO', 'ESTAVEL', 'INOVADOR', 'PROCESSUAL', 'CAOTICO')
        melhor_ref = min(ordem_refs, key=lambda nome: (distancias[nome], ordem_refs.index(nome)))
        
        nivel = self._calcular_nivel(respostas)
        
        alertas = self._gerar_alertas(respostas)
        recomendacoes = self._gerar_recomendacoes(nivel, alertas)
        perfil = self._gerar_perfil(distancias)
        
        resultado = {
            'versao': self.config.VERSAO,
            'data': datetime.now().isoformat(),
            'respostas': respostas,
            'nivel': nivel,
            'nivel_nome': self.config.NIVEIS[nivel]['nome'],
            'nivel_icone': self.config.NIVEIS[nivel]['icone'],
            'nivel_descricao': self.config.NIVEIS[nivel]['descricao'],
            'melhor_referencia': melhor_ref,
            'melhor_referencia_icone': self.config.REFERENCIAS[melhor_ref]['icone'],
            'distancias': distancias,
            'perfil': perfil,
            'alertas': alertas,
            'recomendacoes': recomendacoes,
            'aprovado': nivel >= 3
        }
        
        self.historico.append(deepcopy(resultado))
        return resultado
    
    def _calcular_distancias(self, respostas):
        """Calcula distância para cada arquétipo de referência"""
        distancias = {}
        for nome, ref in self.config.REFERENCIAS.items():
            dist = np.mean([abs(respostas[i] - ref['perfil'][i]) for i in range(5)])
            distancias[nome] = float(dist)
        return distancias
    
    def _calcular_nivel(self, respostas):
        """
        Calcula o nível de maturidade (1 a 5) usando a função oficial:
        S(x) = média(x) - BETA * max(0, 3 - min(x))
        
        Limiares: [1.25, 2.5, 3.5, 4.5]
        Regra de fronteira: o limiar pertence ao nível superior (≥)
        """
        media = sum(respostas) / len(respostas)
        gargalo = max(0, 3 - min(respostas))
        score = media - self.config.BETA * gargalo
        
        limiares = self.config.LIMIARES
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
    
    def _gerar_alertas(self, respostas):
        """Gera alertas baseados nas respostas"""
        alertas = []
        nomes = self.config.DIMENSOES
        
        for i, r in enumerate(respostas):
            if r < 3:
                alertas.append(f"⚠️ {nomes[i]} baixa ({r}/5) — requer atenção")
            elif r >= 4:
                alertas.append(f"✅ {nomes[i]} alta ({r}/5) — ponto forte")
        
        return alertas
    
    def _gerar_recomendacoes(self, nivel, alertas):
        """Gera recomendações baseadas no nível e alertas"""
        recomendacoes = [self.config.RECOMENDACOES.get(nivel, 'Continuar evoluindo')]
        
        recomendacoes_dimensao = (
            "→ Investir em P&D e cultura de inovação",
            "→ Mapear e documentar processos críticos",
            "→ Criar rituais de estabilização e previsibilidade",
            "→ Desenvolver capacidade de resposta a mudanças",
            "→ Quebrar silos e promover colaboração",
        )
        for indice, nome in enumerate(self.config.DIMENSOES):
            if any(a.startswith(f"⚠️ {nome} baixa (") for a in alertas):
                recomendacoes.append(recomendacoes_dimensao[indice])
        
        return recomendacoes
    
    def _gerar_perfil(self, distancias):
        """Gera perfil de distâncias para cada arquétipo"""
        perfil = []
        ordem_refs = ('IDEAL', 'NEUTRO', 'ESTAVEL', 'INOVADOR', 'PROCESSUAL', 'CAOTICO')
        for nome, dist in sorted(distancias.items(), key=lambda x: (x[1], ordem_refs.index(x[0]))):
            perfil.append({
                'referencia': nome,
                'icone': self.config.REFERENCIAS[nome]['icone'],
                'distancia': dist,
                'descricao': self.config.REFERENCIAS[nome]['descricao']
            })
        return perfil
    
    # -------------------------------------------------------------------------
    # 2. RELATÓRIO FORMATADO
    # -------------------------------------------------------------------------
    
    def gerar_relatorio(self, resultado):
        """Gera relatório formatado em texto"""
        erro_config = self._validar_configuracao()
        if erro_config:
            return f"❌ ERRO: Configuração TCIPP inválida: {erro_config}"
        if not isinstance(resultado, dict):
            return "❌ ERRO: resultado deve ser um dicionário"
        if 'erro' in resultado:
            return f"❌ ERRO: {resultado['erro']}"
        campos_obrigatorios = (
            'versao', 'data', 'respostas', 'nivel', 'nivel_nome', 'distancias',
            'nivel_icone', 'nivel_descricao', 'melhor_referencia',
            'melhor_referencia_icone', 'perfil', 'alertas',
            'recomendacoes', 'aprovado'
        )
        ausentes = [campo for campo in campos_obrigatorios if campo not in resultado]
        if ausentes:
            return "❌ ERRO: resultado incompleto; campos ausentes: " + ", ".join(ausentes)

        # Validações básicas (resumidas para brevidade)
        linhas = []
        linhas.append("=" * 70)
        linhas.append(f"📊 RELATÓRIO TCIPP — {resultado['versao']}")
        linhas.append("=" * 70)
        linhas.append(f"Data: {resultado['data']}")
        linhas.append("")
        
        linhas.append("📋 RESPOSTAS:")
        for i, (dim, resp) in enumerate(zip(self.config.DIMENSOES, resultado['respostas'])):
            linhas.append(f"   {i+1}. {dim}: {resp}/5")
        linhas.append("")
        
        linhas.append(f"🏆 NÍVEL DE MATURIDADE: {resultado['nivel_icone']} {resultado['nivel']} — {resultado['nivel_nome']}")
        linhas.append(f"   {resultado['nivel_descricao']}")
        linhas.append("")
        
        linhas.append(f"🎯 MELHOR REFERÊNCIA: {resultado['melhor_referencia_icone']} {resultado['melhor_referencia']}")
        linhas.append("")
        
        linhas.append("📊 PERFIL DE DISTÂNCIAS:")
        for p in resultado['perfil']:
            linhas.append(f"   {p['icone']} {p['referencia']:12s} — distância: {p['distancia']:.4f}")
        linhas.append("")
        
        if resultado['alertas']:
            linhas.append("⚠️ ALERTAS:")
            for a in resultado['alertas']:
                linhas.append(f"   {a}")
            linhas.append("")
        
        if resultado['recomendacoes']:
            linhas.append("💡 RECOMENDAÇÕES:")
            for r in resultado['recomendacoes']:
                linhas.append(f"   {r}")
            linhas.append("")
        
        veredito = "✅ APROVADO" if resultado['aprovado'] else "❌ REPROVADO"
        linhas.append(f"📌 VEREDITO: {veredito}")
        linhas.append("=" * 70)
        
        return "\n".join(linhas)
    
    # -------------------------------------------------------------------------
    # 3. AUDITORIA DE CORPORA (mantida)
    # -------------------------------------------------------------------------
    
    def auditar_corpus(self, nome_corpus, resultado_v54):
        """Audita um corpus usando os resultados do V54."""
        if not isinstance(nome_corpus, str) or not nome_corpus.strip():
            raise ValueError("nome_corpus deve ser um texto não vazio")
        nome_normalizado = nome_corpus.strip()
        if any(unicodedata.category(ch) in {"Cc", "Cf"} for ch in nome_normalizado):
            raise ValueError("nome_corpus não pode conter caracteres de controle ou formatação invisível")
        if not isinstance(resultado_v54, dict):
            raise TypeError("resultado_v54 deve ser um dicionário")

        phi_raw = resultado_v54.get('phi_log')
        macro_z = resultado_v54.get('macro_z')
        micro_z = resultado_v54.get('micro_z')

        def numero_finito(valor):
            if isinstance(valor, (bool, np.bool_)) or not isinstance(valor, (int, float, np.number)):
                return None
            try:
                convertido = float(valor)
            except (TypeError, ValueError, OverflowError):
                return None
            return convertido if np.isfinite(convertido) else None

        phi = numero_finito(phi_raw)
        macro_num = numero_finito(macro_z)
        micro_num = numero_finito(micro_z)
        if macro_num is None or micro_num is None:
            classificacao = "Indeterminado"
        elif macro_num > 3 and micro_num < 0:
            classificacao = "Cifra de Bloco / Nomenclador"
        elif macro_num < -3 and micro_num > 3:
            classificacao = "Língua Natural Plena"
        elif -1 < macro_num < 1 and micro_num > 3:
            classificacao = "Sílaba Rígida / Monossilábica"
        elif abs(macro_num) < 1 and abs(micro_num) < 1:
            classificacao = "Ruído / Texto Plano"
        else:
            classificacao = "Indeterminado"
        
        return {
            'corpus': nome_normalizado,
            'phi_log': phi,
            'macro_z': macro_num,
            'micro_z': micro_num,
            'classificacao': classificacao,
            'data': datetime.now().isoformat()
        }
    
    # -------------------------------------------------------------------------
    # 4. API PÚBLICA
    # -------------------------------------------------------------------------
    
    def api_auditar(self, respostas):
        """API pública para auditoria"""
        return self.auditar(respostas)
    
    def api_relatorio(self, respostas):
        """API pública para relatório formatado"""
        resultado = self.auditar(respostas)
        return self.gerar_relatorio(resultado)


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🏢 TCIPP — Tool for Continuous Improvement and Process Performance")
    print("=" * 70)
    print(f"Versão: {ConfigTCIPP.VERSAO}")
    print(f"Autor: {ConfigTCIPP.AUTOR}")
    print(f"ORCID: {ConfigTCIPP.ORCID}")
    print(f"Beta: {ConfigTCIPP.BETA}")
    print(f"Limiares: {ConfigTCIPP.LIMIARES}")
    print("=" * 70)
    
    tcipp = TCIPP()
    
    # Testes
    print("\n📌 TESTE 1: Empresa Excelente [5,4,5,4,5]")
    print("-" * 70)
    resultado1 = tcipp.auditar([5, 4, 5, 4, 5])
    print(tcipp.gerar_relatorio(resultado1))
    
    print("\n📌 TESTE 2: Empresa em Crise [1,2,1,3,2]")
    print("-" * 70)
    resultado2 = tcipp.auditar([1, 2, 1, 3, 2])
    print(tcipp.gerar_relatorio(resultado2))
    
    print("\n📌 TESTE 3: Empresa Equilibrada [4,4,4,4,4]")
    print("-" * 70)
    resultado3 = tcipp.auditar([4, 4, 4, 4, 4])
    print(tcipp.gerar_relatorio(resultado3))
    
    print("\n📌 TESTE 4: Caso Caótico [1,5,1,5,1]")
    print("-" * 70)
    resultado4 = tcipp.auditar([1, 5, 1, 5, 1])
    print(tcipp.gerar_relatorio(resultado4))
    
    print("\n📌 TESTE 5: Caso Ruim Uniforme [2,2,2,2,2]")
    print("-" * 70)
    resultado5 = tcipp.auditar([2, 2, 2, 2, 2])
    print(tcipp.gerar_relatorio(resultado5))
    
    print("\n" + "=" * 70)
    print("📋 RESUMO DOS TESTES")
    print("=" * 70)
    print(f"Teste 1 (Excelente):     Nível {resultado1['nivel']} — {resultado1['nivel_nome']}")
    print(f"Teste 2 (Crise):         Nível {resultado2['nivel']} — {resultado2['nivel_nome']}")
    print(f"Teste 3 (Equilibrada):   Nível {resultado3['nivel']} — {resultado3['nivel_nome']}")
    print(f"Teste 4 (Caótico):       Nível {resultado4['nivel']} — {resultado4['nivel_nome']}")
    print(f"Teste 5 (Ruim Uniforme): Nível {resultado5['nivel']} — {resultado5['nivel_nome']}")
    print("=" * 70)