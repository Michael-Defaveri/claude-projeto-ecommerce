# KPI Metrics Reference

> This document defines the key business KPIs for the e-commerce dashboard, organized by domain.
> Data is sourced from three Gold layer CSV files in `data/`.

---

## Data Sources

| Dataset | File | Granularity | Domain |
|---------|------|-------------|--------|
| Sales over time | `data/vendas_temporais_rows.csv` | 1 row per `data_venda + hora_venda` | Revenue & Sales |
| Customer segmentation | `data/clientes_segmentacao_rows.csv` | 1 row per `cliente_id` | Customer |
| Price competitiveness | `data/precos_competitividade_rows.csv` | 1 row per `produto_id` | Pricing |

---

## Domain 1: Revenue & Sales KPIs

### KPI 1.1 — Total Revenue

**Business definition:** The sum of all revenue generated across all sales transactions in the selected period. This is the primary top-line metric reflecting the overall financial health of the business.

**Formula:**
```python
df["receita_total"].sum()
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `receita_total` | float | `vendas_temporais_rows.csv` |

---

### KPI 1.2 — Revenue Over Time (Daily / Monthly Trends)

**Business definition:** Revenue aggregated by day or month to reveal growth trends, seasonality, and demand fluctuations over time. Essential for identifying peak periods and planning inventory or promotions.

**Formula:**
```python
# Daily revenue
df.groupby("data_venda")["receita_total"].sum()

# Monthly revenue
df.groupby(["ano_venda", "mes_venda"])["receita_total"].sum()
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `data_venda` | date | `vendas_temporais_rows.csv` |
| `ano_venda` | int | `vendas_temporais_rows.csv` |
| `mes_venda` | int | `vendas_temporais_rows.csv` |
| `receita_total` | float | `vendas_temporais_rows.csv` |

---

### KPI 1.3 — Sales Growth (Month-over-Month)

**Business definition:** The percentage change in revenue from one month to the next. A positive MoM growth indicates business expansion; negative growth is an early warning signal requiring investigation.

**Formula:**
```python
monthly = df.groupby(["ano_venda", "mes_venda"])["receita_total"].sum().reset_index()
monthly["mom_growth_pct"] = monthly["receita_total"].pct_change() * 100
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `ano_venda` | int | `vendas_temporais_rows.csv` |
| `mes_venda` | int | `vendas_temporais_rows.csv` |
| `receita_total` | float | `vendas_temporais_rows.csv` |

---

### KPI 1.4 — Average Ticket (Ticket Médio)

**Business definition:** The average revenue generated per order. Reflects purchasing power of customers and the effectiveness of upselling strategies. A higher ticket médio typically indicates premium product mix or successful cross-selling.

**Formula:**
```python
# Pre-aggregated in dataset (weighted average across time slots)
df["ticket_medio"].mean()

# Or recalculated from totals
df["receita_total"].sum() / df["total_vendas"].sum()
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `ticket_medio` | float | `vendas_temporais_rows.csv` |
| `receita_total` | float | `vendas_temporais_rows.csv` |
| `total_vendas` | int | `vendas_temporais_rows.csv` |

---

### KPI 1.5 — Total Orders and Total Unique Customers

**Business definition:** Total orders measures the volume of completed transactions. Total unique customers counts distinct buyers. Together they indicate market reach, repeat purchase behavior, and conversion efficiency.

**Formula:**
```python
# Total orders
total_orders = df["total_vendas"].sum()

# Total unique customers (cumulative, note: same customer may appear in multiple time slots)
total_unique_customers = df["total_clientes_unicos"].sum()
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `total_vendas` | int | `vendas_temporais_rows.csv` |
| `total_clientes_unicos` | int | `vendas_temporais_rows.csv` |

---

### KPI 1.6 — Peak Sales Hours

**Business definition:** The hours of the day that generate the highest revenue or order volume. Identifies optimal windows for marketing campaigns, flash sales, staffing, and infrastructure scaling.

**Formula:**
```python
# Revenue by hour
hourly_revenue = df.groupby("hora_venda")["receita_total"].sum().sort_values(ascending=False)

# Top peak hours
peak_hours = hourly_revenue.head(5)
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `hora_venda` | int (0–23) | `vendas_temporais_rows.csv` |
| `receita_total` | float | `vendas_temporais_rows.csv` |
| `total_vendas` | int | `vendas_temporais_rows.csv` |

---

## Domain 2: Customer Segmentation KPIs

Customers are classified into three segments based on total lifetime revenue:

| Segment | Rule | Portuguese label |
|---------|------|-----------------|
| VIP | `receita_total >= 10,000` | VIP |
| TOP_TIER | `5,000 <= receita_total < 10,000` | TOP_TIER |
| REGULAR | `receita_total < 5,000` | REGULAR |

---

### KPI 2.1 — Customer Count by Segment

**Business definition:** The number of customers in each segment (VIP, TOP_TIER, REGULAR). Shows the distribution of your customer base and highlights how concentrated or diversified your revenue sources are.

**Formula:**
```python
df["segmento_cliente"].value_counts()
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `cliente_id` | string | `clientes_segmentacao_rows.csv` |
| `segmento_cliente` | string (VIP/TOP_TIER/REGULAR) | `clientes_segmentacao_rows.csv` |

---

### KPI 2.2 — Revenue by Segment

**Business definition:** Total revenue contributed by each customer segment. Helps understand which segment drives the majority of income and where retention efforts should be prioritized.

**Formula:**
```python
df.groupby("segmento_cliente")["receita_total"].sum()
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `segmento_cliente` | string | `clientes_segmentacao_rows.csv` |
| `receita_total` | float | `clientes_segmentacao_rows.csv` |

---

### KPI 2.3 — Average Ticket by Segment

**Business definition:** The mean order value for customers within each segment. VIP customers are expected to have higher average tickets. Deviations from this pattern may signal pricing or assortment issues.

**Formula:**
```python
df.groupby("segmento_cliente")["ticket_medio"].mean()
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `segmento_cliente` | string | `clientes_segmentacao_rows.csv` |
| `ticket_medio` | float | `clientes_segmentacao_rows.csv` |

---

### KPI 2.4 — Customer Lifetime Value Indicators

**Business definition:** Proxy metrics that estimate customer value over their relationship with the business. Combines total spend, purchase frequency, and tenure (days between first and last purchase) to identify high-value and at-risk customers.

**Formula:**
```python
import pandas as pd

df["primeira_compra"] = pd.to_datetime(df["primeira_compra"])
df["ultima_compra"] = pd.to_datetime(df["ultima_compra"])

# Tenure in days
df["tenure_days"] = (df["ultima_compra"] - df["primeira_compra"]).dt.days

# Purchase frequency (orders per day active)
df["purchase_frequency"] = df["total_compras"] / df["tenure_days"].replace(0, 1)

# Summary by segment
df.groupby("segmento_cliente").agg(
    avg_receita=("receita_total", "mean"),
    avg_compras=("total_compras", "mean"),
    avg_tenure_days=("tenure_days", "mean"),
    avg_frequency=("purchase_frequency", "mean")
)
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `cliente_id` | string | `clientes_segmentacao_rows.csv` |
| `segmento_cliente` | string | `clientes_segmentacao_rows.csv` |
| `receita_total` | float | `clientes_segmentacao_rows.csv` |
| `total_compras` | int | `clientes_segmentacao_rows.csv` |
| `ticket_medio` | float | `clientes_segmentacao_rows.csv` |
| `primeira_compra` | date | `clientes_segmentacao_rows.csv` |
| `ultima_compra` | date | `clientes_segmentacao_rows.csv` |
| `ranking_receita` | int | `clientes_segmentacao_rows.csv` |

---

## Domain 3: Price Competitiveness KPIs

Products are classified into five price tiers relative to competitor prices:

| Classification | Meaning |
|---------------|---------|
| `MAIS_CARO_QUE_TODOS` | Our price is higher than all competitors |
| `ACIMA_DA_MEDIA` | Our price is above the competitor average |
| `NA_MEDIA` | Our price equals the competitor average |
| `ABAIXO_DA_MEDIA` | Our price is below the competitor average |
| `MAIS_BARATO_QUE_TODOS` | Our price is lower than all competitors |

---

### KPI 3.1 — Price Classification Distribution

**Business definition:** The count and percentage of products in each price tier. Provides a snapshot of competitive positioning. A high concentration in `MAIS_CARO_QUE_TODOS` may indicate pricing pressure risks; being predominantly `ABAIXO_DA_MEDIA` may erode margins.

**Formula:**
```python
# Count
df["classificacao_preco"].value_counts()

# Percentage
df["classificacao_preco"].value_counts(normalize=True) * 100
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `produto_id` | string | `precos_competitividade_rows.csv` |
| `classificacao_preco` | string | `precos_competitividade_rows.csv` |

---

### KPI 3.2 — Average Price Difference vs Competitors

**Business definition:** The mean percentage difference between our price and the average competitor price across all products. Positive values indicate we are priced above the market; negative values indicate we are below. This is the primary pricing health metric.

**Formula:**
```python
# Overall average
df["diferenca_percentual_vs_media"].mean()

# By category
df.groupby("categoria")["diferenca_percentual_vs_media"].mean()

# By classification
df.groupby("classificacao_preco")["diferenca_percentual_vs_media"].mean()
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `diferenca_percentual_vs_media` | float (%) | `precos_competitividade_rows.csv` |
| `classificacao_preco` | string | `precos_competitividade_rows.csv` |
| `categoria` | string | `precos_competitividade_rows.csv` |

---

### KPI 3.3 — Revenue by Price Classification

**Business definition:** Total revenue generated by products in each price tier. Shows whether competitively priced products drive more sales volume. Useful for deciding pricing strategy (e.g., if `ABAIXO_DA_MEDIA` products generate disproportionately high revenue, aggressive pricing may be justified).

**Formula:**
```python
df.groupby("classificacao_preco")["receita_total"].sum().sort_values(ascending=False)
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `classificacao_preco` | string | `precos_competitividade_rows.csv` |
| `receita_total` | float | `precos_competitividade_rows.csv` |

---

### KPI 3.4 — Products Above / Below Market Average

**Business definition:** Count of products priced above vs. below the market average. A simple competitive score. Useful for executive reporting and pricing team OKRs. Products with zero revenue in each tier also reveal whether overpricing is suppressing conversions.

**Formula:**
```python
# Products above market average (ACIMA_DA_MEDIA + MAIS_CARO_QUE_TODOS)
above = df[df["classificacao_preco"].isin(["ACIMA_DA_MEDIA", "MAIS_CARO_QUE_TODOS"])]
below = df[df["classificacao_preco"].isin(["ABAIXO_DA_MEDIA", "MAIS_BARATO_QUE_TODOS"])]
at_avg = df[df["classificacao_preco"] == "NA_MEDIA"]

summary = {
    "above_market": len(above),
    "below_market": len(below),
    "at_market": len(at_avg),
    "above_pct": len(above) / len(df) * 100,
    "below_pct": len(below) / len(df) * 100,
}

# Revenue impact: zero-revenue products by tier
df[df["receita_total"] == 0].groupby("classificacao_preco").size()
```

**Required fields:**
| Field | Type | Source CSV |
|-------|------|------------|
| `produto_id` | string | `precos_competitividade_rows.csv` |
| `classificacao_preco` | string | `precos_competitividade_rows.csv` |
| `nosso_preco` | float | `precos_competitividade_rows.csv` |
| `preco_medio_concorrentes` | float | `precos_competitividade_rows.csv` |
| `preco_minimo_concorrentes` | float | `precos_competitividade_rows.csv` |
| `preco_maximo_concorrentes` | float | `precos_competitividade_rows.csv` |
| `receita_total` | float | `precos_competitividade_rows.csv` |
| `quantidade_total` | int | `precos_competitividade_rows.csv` |

---

## Summary Table

| # | KPI | Domain | Primary Field(s) | Source CSV |
|---|-----|--------|-----------------|------------|
| 1.1 | Total Revenue | Revenue & Sales | `receita_total` | `vendas_temporais_rows.csv` |
| 1.2 | Revenue Over Time | Revenue & Sales | `data_venda`, `receita_total` | `vendas_temporais_rows.csv` |
| 1.3 | Sales Growth MoM | Revenue & Sales | `ano_venda`, `mes_venda`, `receita_total` | `vendas_temporais_rows.csv` |
| 1.4 | Average Ticket | Revenue & Sales | `ticket_medio`, `total_vendas` | `vendas_temporais_rows.csv` |
| 1.5 | Total Orders & Unique Customers | Revenue & Sales | `total_vendas`, `total_clientes_unicos` | `vendas_temporais_rows.csv` |
| 1.6 | Peak Sales Hours | Revenue & Sales | `hora_venda`, `receita_total` | `vendas_temporais_rows.csv` |
| 2.1 | Customer Count by Segment | Customer | `segmento_cliente` | `clientes_segmentacao_rows.csv` |
| 2.2 | Revenue by Segment | Customer | `segmento_cliente`, `receita_total` | `clientes_segmentacao_rows.csv` |
| 2.3 | Average Ticket by Segment | Customer | `segmento_cliente`, `ticket_medio` | `clientes_segmentacao_rows.csv` |
| 2.4 | Customer Lifetime Value Indicators | Customer | `receita_total`, `total_compras`, `primeira_compra`, `ultima_compra` | `clientes_segmentacao_rows.csv` |
| 3.1 | Price Classification Distribution | Pricing | `classificacao_preco` | `precos_competitividade_rows.csv` |
| 3.2 | Avg Price Difference vs Competitors | Pricing | `diferenca_percentual_vs_media` | `precos_competitividade_rows.csv` |
| 3.3 | Revenue by Price Classification | Pricing | `classificacao_preco`, `receita_total` | `precos_competitividade_rows.csv` |
| 3.4 | Products Above/Below Market Average | Pricing | `classificacao_preco`, `nosso_preco`, `preco_medio_concorrentes` | `precos_competitividade_rows.csv` |
