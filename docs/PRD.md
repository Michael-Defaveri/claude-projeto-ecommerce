# PRD — E-Commerce Analytics Dashboard

**Versão:** 1.0
**Data:** 2026-03-25
**Status:** Entregue
**Autor:** Michael (Jornada de Dados)

---

## 1. Visão Geral

### 1.1 Problema

Times de negócio em e-commerce enfrentam dificuldade para consolidar dados dispersos de vendas, clientes e preços em uma visão única e acionável. Sem um painel centralizado, decisões sobre estratégia de preços, priorização de segmentos e identificação de tendências dependem de planilhas manuais e análises ad-hoc lentas.

### 1.2 Solução

Um dashboard interativo de Business Intelligence que consolida três domínios críticos — **Receita & Vendas**, **Segmentação de Clientes** e **Competitividade de Preços** — em uma única interface web, alimentada por data marts em camada Gold e com KPIs validados matematicamente.

### 1.3 Objetivo Primário

Permitir que analistas e gestores identifiquem padrões de receita, entendam o perfil dos clientes e tomem decisões de precificação baseadas em dados competitivos, sem depender de engenharia para cada consulta.

---

## 2. Usuários-Alvo

| Perfil | Necessidade Principal |
|--------|-----------------------|
| Analista de Dados | Validar KPIs, explorar tendências temporais, exportar insights |
| Gestor Comercial | Monitorar receita, crescimento MoM e horários de pico |
| Gestor de Marketing | Entender segmentos de clientes e CLV para campanhas |
| Gestor de Pricing | Comparar preços próprios vs. concorrência por categoria |

---

## 3. Escopo do Produto (v1.0)

### 3.1 Dentro do Escopo

- Dashboard web interativo com Streamlit
- 14 KPIs distribuídos em 3 domínios de negócio
- Filtros interativos na sidebar (data, segmento, categoria, classificação de preço)
- Gráficos interativos com Plotly (linha, barra, pizza, scatter, tabela)
- Consumo de data marts CSV em camada Gold
- Validação automatizada de dados e fórmulas de KPIs
- Documentação técnica completa (catálogo de dados, métricas, relatório de QA)

### 3.2 Fora do Escopo (v1.0)

- Conexão direta a banco de dados ou data warehouse
- Autenticação e controle de acesso por usuário
- Exportação de relatórios em PDF ou Excel
- Atualização em tempo real dos dados (streaming)
- Deploy em cloud (Streamlit Cloud, AWS, etc.)
- Histórico de dados além de 30 dias

---

## 4. Requisitos Funcionais

### 4.1 Domínio 1 — Receita & Vendas

| ID | Requisito | Prioridade |
|----|-----------|-----------|
| RF-01 | Exibir total de receita no período selecionado | Alta |
| RF-02 | Exibir ticket médio no período selecionado | Alta |
| RF-03 | Gráfico de linha com receita diária | Alta |
| RF-04 | Gráfico de barras com receita mensal + crescimento MoM | Alta |
| RF-05 | Gráfico de barras com volume de vendas por hora do dia | Média |
| RF-06 | Filtro de período por data (início / fim) | Alta |

### 4.2 Domínio 2 — Segmentação de Clientes

| ID | Requisito | Prioridade |
|----|-----------|-----------|
| RF-07 | Gráfico de pizza com distribuição de clientes por segmento | Alta |
| RF-08 | Gráfico de barras com receita por segmento | Alta |
| RF-09 | Gráfico de barras com ticket médio por segmento | Alta |
| RF-10 | Tabela com indicadores de CLV (tenure, frequência, receita total) | Média |
| RF-11 | Filtro por segmento (VIP, TOP_TIER, REGULAR) | Alta |

### 4.3 Domínio 3 — Competitividade de Preços

| ID | Requisito | Prioridade |
|----|-----------|-----------|
| RF-12 | Gráfico de barras com distribuição de classificação de preço | Alta |
| RF-13 | Gráfico de barras divergente com diferença de preço vs. média por categoria | Alta |
| RF-14 | Gráfico de barras com receita por classificação de preço | Alta |
| RF-15 | Tabela resumo + scatter plot de produtos acima/abaixo da média | Média |
| RF-16 | Filtro por categoria de produto e classificação de preço | Alta |

### 4.4 Requisitos Gerais

| ID | Requisito | Prioridade |
|----|-----------|-----------|
| RF-17 | Sidebar com todos os filtros interativos | Alta |
| RF-18 | Atualização reativa dos gráficos ao aplicar filtros | Alta |
| RF-19 | Layout responsivo em modo wide | Média |
| RF-20 | Cache de dados para evitar recarregamentos desnecessários | Média |

---

## 5. Requisitos Não Funcionais

| ID | Requisito | Critério de Aceite |
|----|-----------|-------------------|
| RNF-01 | Performance | Dashboard carrega em < 3s com dados locais |
| RNF-02 | Qualidade dos dados | 0 valores nulos, 0 duplicatas nos data marts |
| RNF-03 | Cobertura de KPIs | 100% dos 14 KPIs implementados e validados |
| RNF-04 | Reprodutibilidade | `uv sync` + `streamlit run app.py` suficientes para rodar |
| RNF-05 | Documentação | Catálogo de dados, definição de KPIs e relatório de QA presentes |
| RNF-06 | Tratamento de erros | Divisões por zero e datasets vazios tratados graciosamente |

---

## 6. Arquitetura Técnica

### 6.1 Arquitetura de Dados (Medallion)

```
Bronze (transacional) → Silver (limpo) → Gold (agregado, CSV)
                                                    ↓
                                           Dashboard (Streamlit)
```

O projeto consome exclusivamente a camada **Gold**, composta por três data marts pré-agregados:

| Data Mart | Arquivo | Granularidade | Linhas |
|-----------|---------|---------------|--------|
| Vendas Temporais | `vendas_temporais_rows.csv` | Data + Hora | 507 |
| Segmentação de Clientes | `clientes_segmentacao_rows.csv` | Cliente | 50 |
| Preços e Competitividade | `precos_competitividade_rows.csv` | Produto | 215 |

### 6.2 Stack Tecnológico

- **Runtime:** Python 3.13
- **UI:** Streamlit (modo wide, sidebar de filtros)
- **Visualização:** Plotly Express + Plotly Graph Objects
- **Processamento:** Pandas
- **Empacotamento:** uv + pyproject.toml

### 6.3 Padrões de Design

- **Separação de responsabilidades:** carregamento → filtragem → renderização
- **KPI-first:** cada visualização mapeada a um KPI de negócio documentado
- **Cache declarativo:** `@st.cache_data` no carregamento de dados
- **Funções de renderização isoladas** por domínio de negócio

---

## 7. KPIs e Definições de Negócio

### 7.1 Segmentos de Clientes

| Segmento | Critério (Receita Total) |
|----------|--------------------------|
| VIP | ≥ R$ 10.000 |
| TOP_TIER | ≥ R$ 5.000 e < R$ 10.000 |
| REGULAR | < R$ 5.000 |

### 7.2 Classificações de Preço

| Classificação | Significado |
|---------------|-------------|
| MAIS_CARO_QUE_TODOS | Acima de todos os concorrentes |
| ACIMA_DA_MEDIA | Acima da média, mas não o mais caro |
| NA_MEDIA | Na média de mercado |
| ABAIXO_DA_MEDIA | Abaixo da média, mas não o mais barato |
| MAIS_BARATO_QUE_TODOS | Abaixo de todos os concorrentes |

Definições completas e fórmulas em [`docs/metrics.md`](docs/metrics.md).

---

## 8. Critérios de Aceite

### 8.1 Entrega Técnica

- [x] Dashboard executável com `streamlit run app.py`
- [x] Todos os 14 KPIs renderizados e visíveis
- [x] Filtros funcionando e atualizando gráficos reativamente
- [x] `tests/validate_data.py` — todos os testes passam
- [x] `tests/validate_metrics.py` — todas as fórmulas validadas

### 8.2 Qualidade de Dados

- [x] 0 valores nulos nos três data marts
- [x] 0 linhas duplicadas
- [x] Tipos de dados corretos (datas, numéricos, strings)
- [x] Regras de segmentação aplicadas corretamente

### 8.3 Documentação

- [x] `README.md` com instruções de instalação e execução
- [x] `docs/metrics.md` com definição de todos os KPIs
- [x] `.llm/database.md` com catálogo de dados completo
- [x] `tests/report.md` com relatório de QA

---

## 9. Observações e Anomalias Conhecidas

Identificadas durante QA — não bloqueiam o uso, mas são relevantes para análise de negócio:

| Observação | Impacto | Ação Recomendada |
|------------|---------|-----------------|
| Categoria "Tenis": todos os 15 produtos com preço ~2x a média concorrente | Pode indicar erro de precificação ou mercado de nicho | Revisão com time comercial |
| 98% dos clientes classificados como VIP | Pode indicar critério de segmentação muito permissivo para a base atual | Recalibrar limiares de segmentação |
| 25 produtos com receita zero | Produtos listados mas sem vendas no período | Investigar disponibilidade ou visibilidade |
| Dados cobrem apenas 30 dias (2025-12-13 a 2026-01-11) | Tendências de longo prazo não disponíveis | Ampliar janela histórica em próxima versão |

---

## 10. Processo de Desenvolvimento

Este projeto foi desenvolvido com **Claude Code Agent Teams** (v1.0 experimental), com 4 agentes especializados operando em paralelo:

| Agente | Modelo | Entregável |
|--------|--------|-----------|
| `team-lead` | Claude Opus | Coordenação geral e `docs/build-summary.md` |
| `data-analyst` | Claude Sonnet | `docs/metrics.md` — definição dos 14 KPIs |
| `fullstack-dev` | Claude Sonnet | `app.py` — dashboard completo |
| `qa-engineer` | Claude Sonnet | `tests/` — validação e relatório de QA |

**Workflow de dependências:**
```
data-analyst ──► fullstack-dev ──► qa-engineer ──► team-lead
```

A abordagem demonstrou que fluxos de dados analíticos podem ser construídos end-to-end com agentes especializados, mantendo qualidade de entrega verificável por testes automatizados.

---

## 11. Roadmap (Pós v1.0)

| Versão | Feature | Prioridade |
|--------|---------|-----------|
| v1.1 | Conexão a banco de dados (SQLite ou DuckDB) | Alta |
| v1.1 | Exportação de relatório em Excel/PDF | Média |
| v1.2 | Deploy no Streamlit Cloud com CI/CD | Alta |
| v1.2 | Autenticação básica por senha | Média |
| v2.0 | Atualização automática dos dados (pipeline de ingestão) | Alta |
| v2.0 | Alertas de KPI (ex.: queda de receita > 20% MoM) | Média |
| v2.0 | Análise preditiva de CLV com scikit-learn | Baixa |
