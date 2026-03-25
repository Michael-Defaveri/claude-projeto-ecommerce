# Build Summary — E-Commerce Dashboard

**Date:** 2026-03-25
**Team:** ecommerce-dashboard (3 Sonnet teammates + Opus team lead)

---

## What Was Built

An interactive Streamlit dashboard for e-commerce data analytics, built on top of three Gold-layer CSV datasets. The dashboard covers 14 KPIs across 3 business domains.

### Deliverables

| # | File | Description |
|---|------|-------------|
| 1 | `app.py` | Streamlit dashboard — main application |
| 2 | `docs/metrics.md` | KPI definitions (14 metrics, 3 domains) |
| 3 | `tests/report.md` | QA validation report |
| 4 | `tests/validate_data.py` | Data quality validation script |
| 5 | `tests/validate_metrics.py` | KPI formula validation script |
| 6 | `docs/build-summary.md` | This file |

### Data Sources

| File | Rows | Domain |
|------|------|--------|
| `data/vendas_temporais_rows.csv` | 507 | Revenue & Sales |
| `data/clientes_segmentacao_rows.csv` | 50 | Customer Segmentation |
| `data/precos_competitividade_rows.csv` | 215 | Price Competitiveness |

---

## How to Run

```bash
streamlit run app.py
```

### Requirements

- Python 3.8+
- `streamlit`
- `pandas`
- `plotly`

Install dependencies:

```bash
pip install streamlit pandas plotly
```

---

## KPIs Implemented

### Domain 1: Revenue & Sales (6 KPIs)

| KPI | Visualization |
|-----|--------------|
| 1.1 Total Revenue | Metric card |
| 1.2 Revenue Over Time (daily/monthly) | Line chart + Bar chart |
| 1.3 Sales Growth MoM | Computed in monthly data |
| 1.4 Average Ticket | Metric card |
| 1.5 Total Orders & Unique Customers | Metric cards |
| 1.6 Peak Sales Hours | Bar chart (hourly) |

### Domain 2: Customer Segmentation (4 KPIs)

| KPI | Visualization |
|-----|--------------|
| 2.1 Customer Count by Segment | Pie chart |
| 2.2 Revenue by Segment | Bar chart |
| 2.3 Average Ticket by Segment | Bar chart |
| 2.4 Customer Lifetime Value Indicators | Data table |

### Domain 3: Price Competitiveness (4 KPIs)

| KPI | Visualization |
|-----|--------------|
| 3.1 Price Classification Distribution | Bar chart |
| 3.2 Avg Price Difference vs Competitors | Bar chart by category |
| 3.3 Revenue by Price Classification | Bar chart |
| 3.4 Products Above/Below Market Average | Summary table + Scatter plot |

### Dashboard Features

- **Sidebar filters**: Date range, Customer segments, Product categories
- **Interactive charts**: Built with Plotly Express (hover, zoom, pan)
- **Responsive layout**: Wide mode with multi-column layouts
- **Data caching**: `@st.cache_data` for performance
- **Top 10 customers table** with ranking, state, segment, and revenue

---

## QA Results

**Overall Status: PASS**

| Area | Status |
|------|--------|
| Data Quality | PASS — 0 nulls, 0 duplicates, all columns verified |
| KPI Validation | PASS — All 14 formulas mathematically verified |
| App Code Review | PASS — 100% KPI coverage, proper error handling |
| Edge Cases | PASS — Graceful handling of edge cases |

### Notable Observations (non-blocking)

1. **Tenis category anomaly**: All 15 products priced at ~2x competitor average — inflates overall price differential
2. **No REGULAR customers**: Dataset contains only VIP (49) and TOP_TIER (1) customers
3. **25 zero-revenue products**: 16 of 35 `MAIS_CARO_QUE_TODOS` products have zero revenue — potential overpricing insight

---

## Team Structure

| Role | Agent | Model | Task |
|------|-------|-------|------|
| Team Lead | team-lead | Opus | Coordination + build-summary.md |
| Data Analyst | data-analyst | Sonnet | KPI definitions (docs/metrics.md) |
| Fullstack Dev | fullstack-dev | Sonnet | Dashboard app (app.py) |
| QA Engineer | qa-engineer | Sonnet | Validation (tests/report.md) |

### Workflow

```
data-analyst (#1) → fullstack-dev (#2) → qa-engineer (#3) → team-lead (#4)
```

Each task was completed sequentially with dependency-based unblocking. The data-analyst defined KPIs first, the fullstack-dev built the app based on those definitions, and the QA engineer validated everything end-to-end.
