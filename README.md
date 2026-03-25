# E-Commerce Analytics Dashboard

Dashboard interativo de Business Intelligence para análise de dados de e-commerce, construído com Streamlit e Plotly. Cobre três domínios de negócio: **Receita & Vendas**, **Segmentação de Clientes** e **Competitividade de Preços**.

> Projeto desenvolvido com **Claude Code Agent Teams** — um time de 4 agentes de IA coordenados em paralelo (analista de dados, desenvolvedor full-stack, engenheiro de QA e tech lead).

---

## Funcionalidades

- **Receita & Vendas** — tendência diária/mensal, ticket médio, horários de pico, crescimento MoM
- **Segmentação de Clientes** — distribuição por segmento (VIP / TOP_TIER / REGULAR), receita por segmento, CLV
- **Competitividade de Preços** — comparativo com média de mercado por categoria, distribuição de classificação de preços
- Filtros interativos na sidebar com atualização reativa dos gráficos
- 14 KPIs rastreados com fórmulas documentadas em [`docs/metrics.md`](docs/metrics.md)
- Dados validados com 0 nulos e 0 duplicatas — veja o [relatório de QA](tests/report.md)

---

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | Python 3.13 |
| Dashboard | Streamlit |
| Visualização | Plotly Express / Graph Objects |
| Dados | Pandas + CSV (camada Gold) |
| Gerenciador de pacotes | uv |
| Desenvolvimento | Claude Code Agent Teams |

---

## Arquitetura de Dados

O projeto consome **data marts em camada Gold** (arquitetura medallion), sem necessidade de banco de dados:

```
data/
├── vendas_temporais_rows.csv        # 507 linhas — receita por data + hora
├── clientes_segmentacao_rows.csv    #  50 linhas — CLV e segmento por cliente
└── precos_competitividade_rows.csv  # 215 linhas — preço próprio vs. concorrência por produto
```

Documentação completa do schema em [`.llm/database.md`](.llm/database.md).

---

## Instalação e Execução

**Pré-requisitos:** Python 3.13+ e [`uv`](https://github.com/astral-sh/uv)

```bash
# Clone o repositório
git clone https://github.com/<seu-usuario>/claude-projeto-ecommerce.git
cd claude-projeto-ecommerce

# Instale as dependências
uv sync

# Execute o dashboard
uv run streamlit run app.py
```

Acesse em `http://localhost:8501`.

**Sem `uv`:**
```bash
pip install streamlit pandas plotly
streamlit run app.py
```

---

## Validação de Dados e KPIs

Scripts de validação disponíveis em [`tests/`](tests/):

```bash
# Validar qualidade dos dados (nulos, duplicatas, tipos, regras de negócio)
uv run python tests/validate_data.py

# Validar fórmulas dos 14 KPIs
uv run python tests/validate_metrics.py
```

Resultado atual: **todos os testes passam** — veja o relatório completo em [`tests/report.md`](tests/report.md).

---

## Estrutura do Projeto

```
claude-projeto-ecommerce/
├── app.py                        # Aplicação Streamlit principal (467 linhas)
├── main.py                       # Entry point
├── pyproject.toml                # Configuração do projeto e dependências
├── data/                         # Data marts Gold (CSV)
├── docs/
│   ├── metrics.md                # Definição técnica dos 14 KPIs
│   ├── build-summary.md          # Resumo do build e estrutura do time de agentes
│   └── agent-teams-reference.md  # Guia de uso do Claude Agent Teams
├── tests/
│   ├── validate_data.py          # Validação de qualidade dos dados
│   ├── validate_metrics.py       # Validação das fórmulas de KPI
│   └── report.md                 # Relatório de QA
└── .llm/
    └── database.md               # Catálogo de dados e schemas
```

---

## Desenvolvimento com Claude Agent Teams

Este projeto foi construído experimentalmente com o recurso **Agent Teams** do Claude Code, onde 4 agentes trabalharam em paralelo com papéis definidos:

| Agente | Modelo | Responsabilidade |
|--------|--------|-----------------|
| `team-lead` | Opus | Coordenação, revisão e `build-summary.md` |
| `data-analyst` | Sonnet | Definição de KPIs e `docs/metrics.md` |
| `fullstack-dev` | Sonnet | `app.py` e toda a camada de visualização |
| `qa-engineer` | Sonnet | Scripts de validação e `tests/report.md` |

Fluxo: `data-analyst` → `fullstack-dev` → `qa-engineer` → `team-lead`

Referência completa em [`docs/agent-teams-reference.md`](docs/agent-teams-reference.md).

---

## KPIs Monitorados

**Receita & Vendas (6):** Total de Receita, Receita por Dia, Receita Mensal, Crescimento MoM, Ticket Médio, Horários de Pico

**Clientes (4):** Distribuição por Segmento, Receita por Segmento, Ticket Médio por Segmento, Indicadores de CLV

**Preços (4):** Distribuição de Classificação de Preço, Diferença de Preço vs. Concorrência por Categoria, Receita por Classificação, Produtos Acima/Abaixo da Média

Definições completas e fórmulas em [`docs/metrics.md`](docs/metrics.md).

---

## Licença

MIT
