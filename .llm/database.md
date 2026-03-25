# Gold Layer - Catálogo de Dados (Data Marts via CSV)

> Documento técnico para analistas de dados, dashboards (Streamlit) e agentes de IA (Claude Code).
> Os dados são consumidos diretamente de arquivos `.csv` na pasta `data/`.
> Mantém o mesmo schema da camada Gold.

---

## Visão Geral

| Propriedade                 | Valor                             |
| --------------------------- | --------------------------------- |
| **Fonte de Dados**          | Arquivos CSV (`/data`)            |
| **Arquitetura**             | Medalhão (Bronze → Silver → Gold) |
| **Ferramenta de Modelagem** | dbt (lógica reaproveitada)        |
| **Materialização Gold**     | CSV                               |
| **Total de Data Marts**     | 3                                 |

### Arquivos disponíveis

| # | Arquivo CSV                       | Equivalente (Tabela Gold) | Domínio          | Objetivo                     |
| - | --------------------------------- | ------------------------- | ---------------- | ---------------------------- |
| 1 | `vendas_temporais_rows.csv`       | `vendas_temporais`        | Vendas           | Métricas de vendas agregadas |
| 2 | `clientes_segmentacao_rows.csv`   | `clientes_segmentacao`    | Customer Success | Segmentação de clientes      |
| 3 | `precos_competitividade_rows.csv` | `precos_competitividade`  | Pricing          | Competitividade de preços    |

📁 Estrutura esperada:

```
/data
  ├── vendas_temporais_rows.csv
  ├── clientes_segmentacao_rows.csv
  └── precos_competitividade_rows.csv
```

---

## Fluxo de dados (conceitual)

```
RAW → BRONZE → SILVER → GOLD (CSV final)

Agora você consome diretamente:
CSV (Gold pronto para análise)
```

---

# Data Mart 1: `vendas_temporais`

## Objetivo

Analisar performance de vendas ao longo do tempo (dia, hora, sazonalidade).

## Arquivo

`data/vendas_temporais_rows.csv`

## Granularidade

1 linha por `data_venda + hora_venda`

## Principais métricas

* `receita_total`
* `quantidade_total`
* `total_vendas`
* `total_clientes_unicos`
* `ticket_medio`

## Uso típico (Python + Pandas)

```python
import pandas as pd

df = pd.read_csv("data/vendas_temporais_rows.csv")

# Receita por mês
df.groupby(["ano_venda", "mes_venda"])["receita_total"].sum()

# Horário de pico
df.groupby("hora_venda")["receita_total"].sum().sort_values(ascending=False)
```

---

# Data Mart 2: `clientes_segmentacao`

## Objetivo

Segmentar clientes por valor (VIP, TOP_TIER, REGULAR)

## Arquivo

`data/clientes_segmentacao_rows.csv`

## Granularidade

1 linha por cliente

## Segmentação

| Segmento | Regra             |
| -------- | ----------------- |
| VIP      | receita >= 10.000 |
| TOP_TIER | receita >= 5.000  |
| REGULAR  | receita < 5.000   |

## Uso típico

```python
df = pd.read_csv("data/clientes_segmentacao_rows.csv")

# Clientes por segmento
df["segmento_cliente"].value_counts()

# Receita por segmento
df.groupby("segmento_cliente")["receita_total"].sum()

# Top 10 clientes
df.sort_values("receita_total", ascending=False).head(10)
```

---

# Data Mart 3: `precos_competitividade`

## Objetivo

Comparar preços com concorrentes e analisar impacto nas vendas

## Arquivo

`data/precos_competitividade_rows.csv`

## Granularidade

1 linha por produto

## Classificações

* `MAIS_CARO_QUE_TODOS`
* `ACIMA_DA_MEDIA`
* `NA_MEDIA`
* `ABAIXO_DA_MEDIA`
* `MAIS_BARATO_QUE_TODOS`

## Uso típico

```python
df = pd.read_csv("data/precos_competitividade_rows.csv")

# Distribuição de preços
df["classificacao_preco"].value_counts()

# Produtos mais caros
df.sort_values("diferenca_percentual_vs_media", ascending=False).head(10)

# Relação preço vs vendas
df[["diferenca_percentual_vs_media", "quantidade_total"]].corr()
```

---

# Relacionamentos (conceitual)

Mesmo sem banco, você pode cruzar os dados via Python:

* `cliente_id` → clientes ↔ vendas
* `produto_id` → preços ↔ vendas

Exemplo:

```python
df_clientes = pd.read_csv("data/clientes_segmentacao_rows.csv")
df_precos = pd.read_csv("data/precos_competitividade_rows.csv")

# Exemplo simples: análise por segmento
df_clientes.groupby("segmento_cliente")["receita_total"].sum()
```

---

# Uso com Streamlit (Full Stack simples)

```python
import streamlit as st
import pandas as pd

df_vendas = pd.read_csv("data/vendas_temporais_rows.csv")

st.title("Dashboard de Vendas")

st.line_chart(
    df_vendas.groupby("data_venda")["receita_total"].sum()
)
```

---

# Categorias conhecidas

### Categorias

Eletrônicos, Casa, Moda, Games, Cozinha, Beleza, Acessórios

### Segmentos

VIP, TOP_TIER, REGULAR

### Concorrentes

Mercado Livre, Amazon, Shopee, Magalu
