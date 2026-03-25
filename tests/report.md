# QA Validation Report — E-Commerce Dashboard

**Date:** 2026-03-25
**Validated by:** QA Engineer (qa-engineer)
**Scope:** Data Quality, KPI Metrics, App Code Review, Edge Cases

---

## Summary

| Area | Status | Notes |
|------|--------|-------|
| Data Quality | PASS (with observations) | All files load; no nulls, no duplicates; one data anomaly in Tenis category |
| KPI Validation | PASS | All 14 KPIs validated; formulas are mathematically correct |
| App Review | PASS (with observations) | All KPIs implemented; minor UX and edge-case notes |
| Edge Cases | PASS (with observations) | Handled gracefully; one notable segment imbalance |

**Overall Status: PASS** — The dashboard is production-ready. Minor observations documented below do not block deployment.

---

## 1. Data Quality

### 1.1 File Loading

| File | Status | Shape | Notes |
|------|--------|-------|-------|
| `vendas_temporais_rows.csv` | PASS | 507 rows × 11 cols | Loads correctly |
| `clientes_segmentacao_rows.csv` | PASS | 50 rows × 10 cols | Loads correctly |
| `precos_competitividade_rows.csv` | PASS | 215 rows × 14 cols | Loads correctly |

### 1.2 Column Name Verification

**vendas_temporais_rows.csv**

Expected (per `.llm/database.md`): `receita_total`, `quantidade_total`, `total_vendas`, `total_clientes_unicos`, `ticket_medio`, `data_venda`, `hora_venda`

Actual columns: `data_venda`, `ano_venda`, `mes_venda`, `dia_venda`, `dia_semana_nome`, `hora_venda`, `receita_total`, `quantidade_total`, `total_vendas`, `total_clientes_unicos`, `ticket_medio`

Status: **PASS** — All documented fields present; additional derived columns (`ano_venda`, `mes_venda`, `dia_venda`, `dia_semana_nome`) are valid additions.

**clientes_segmentacao_rows.csv**

Expected: `cliente_id`, `receita_total`, `total_compras`, `ticket_medio`, `segmento_cliente`, `primeira_compra`, `ultima_compra`

Actual: `cliente_id`, `nome_cliente`, `estado`, `receita_total`, `total_compras`, `ticket_medio`, `primeira_compra`, `ultima_compra`, `segmento_cliente`, `ranking_receita`

Status: **PASS** — All documented fields present; additional columns (`nome_cliente`, `estado`, `ranking_receita`) are valid enrichment.

**precos_competitividade_rows.csv**

Expected: `produto_id`, `nome_produto`, `categoria`, `classificacao_preco`, `nosso_preco`, `preco_medio_concorrentes`, `diferenca_percentual_vs_media`

Actual: `produto_id`, `nome_produto`, `categoria`, `marca`, `nosso_preco`, `preco_medio_concorrentes`, `preco_minimo_concorrentes`, `preco_maximo_concorrentes`, `total_concorrentes`, `diferenca_percentual_vs_media`, `diferenca_percentual_vs_minimo`, `classificacao_preco`, `receita_total`, `quantidade_total`

Status: **PASS** — All documented fields present; additional columns are valid.

### 1.3 Data Types

| Field | Expected | Actual | Status |
|-------|----------|--------|--------|
| `data_venda` | date | object (string) | OBSERVATION — loaded as string; app correctly converts with `pd.to_datetime()` |
| `receita_total` (vendas) | float | float64 | PASS |
| `hora_venda` | int (0–23) | int64 | PASS |
| `ticket_medio` (vendas) | float | float64 | PASS |
| `cliente_id` | string | object | PASS |
| `primeira_compra`, `ultima_compra` | date | object (string) | OBSERVATION — app correctly converts with `pd.to_datetime()` |
| `nosso_preco` | float | float64 | PASS |
| `diferenca_percentual_vs_media` | float (%) | float64 | PASS |

### 1.4 Missing Values

| File | Missing Values | Status |
|------|---------------|--------|
| `vendas_temporais_rows.csv` | 0 nulls in all 11 columns | PASS |
| `clientes_segmentacao_rows.csv` | 0 nulls in all 10 columns | PASS |
| `precos_competitividade_rows.csv` | 0 nulls in all 14 columns | PASS |

### 1.5 Duplicate Rows

| File | Full-Row Duplicates | Key Duplicates | Status |
|------|-------------------|----------------|--------|
| `vendas_temporais_rows.csv` | 0 | N/A | PASS |
| `clientes_segmentacao_rows.csv` | 0 | 0 duplicate `cliente_id` | PASS |
| `precos_competitividade_rows.csv` | 0 | 0 duplicate `produto_id` | PASS |

### 1.6 Value Integrity

| Check | Result | Status |
|-------|--------|--------|
| Negative `receita_total` in vendas | 0 rows | PASS |
| Negative `quantidade_total` in vendas | 0 rows | PASS |
| `hora_venda` range 0–23 | Min=0, Max=23 | PASS |
| Negative `receita_total` in clientes | 0 rows | PASS |
| Negative `receita_total` in precos | 0 rows | PASS |
| Negative `quantidade_total` in precos | 0 rows | PASS |
| `nosso_preco` range plausible | R$ 31.90 to R$ 1,428.99 | PASS |
| Date range sensible | 2025-12-13 to 2026-01-11 (30 days) | PASS |

### 1.7 Segmentation Rules

| Segment | Rule (per docs) | Verified | Status |
|---------|----------------|----------|--------|
| VIP | `receita_total >= 10,000` | 49/49 rows comply | PASS |
| TOP_TIER | `receita_total >= 5,000` | 1/1 rows comply | PASS |
| REGULAR | `receita_total < 5,000` | 0 rows in dataset | OBSERVATION — no REGULAR customers in the 50-customer dataset |

### 1.8 Data Anomaly — Tenis Category

**OBSERVATION (not a data error, but notable):**

All 15 products in the `Tenis` category have `nosso_preco` = exactly 2x `preco_medio_concorrentes`, resulting in `diferenca_percentual_vs_media ≈ 100%` for all Tenis products. This appears to be a synthetic data generation artifact rather than a real pricing scenario.

**Impact:** The category-level KPI 3.2 shows Tenis at ~100% price differential, skewing the overall average.

**Recommendation:** Investigate data pipeline for the Tenis category; flag in dashboard with a tooltip or note.

---

## 2. KPI Validation

All KPI formulas from `docs/metrics.md` were validated by executing the exact formulas against the CSV data.

### Domain 1: Revenue & Sales

| KPI | Formula Validated | Result | Status |
|-----|------------------|--------|--------|
| 1.1 Total Revenue | `df["receita_total"].sum()` | R$ 974,077.28 | PASS |
| 1.2 Revenue Over Time | `groupby("data_venda")` / `groupby(["ano_venda","mes_venda"])` | 30 daily points, 2 monthly points | PASS |
| 1.3 Sales Growth MoM | `pct_change() * 100` | Dec 2025: R$ 622,809 → Jan 2026: R$ 351,268 (−43.6%) | PASS |
| 1.4 Average Ticket | `receita_total.sum() / total_vendas.sum()` | R$ 322.54 (global ratio) | PASS |
| 1.5 Total Orders & Unique Customers | `total_vendas.sum()` / `total_clientes_unicos.sum()` | 3,020 orders / 2,838 customer-slots | PASS |
| 1.6 Peak Sales Hours | `groupby("hora_venda").sort_values()` | Top hour: 15h (R$ 77,175) | PASS |

**Note on KPI 1.4:** metrics.md documents two valid formulas for ticket médio:
- `df["ticket_medio"].mean()` → R$ 328.09 (mean of pre-aggregated per-slot averages)
- `df["receita_total"].sum() / df["total_vendas"].sum()` → R$ 322.54 (global ratio)

Both are mathematically valid but produce different results. The app uses the global ratio formula (R$ 322.54), which is the more accurate business metric.

**Note on KPI 1.5:** `total_clientes_unicos` is summed across time slots (not deduplicated globally). The same customer can appear in multiple time slots, so this is a cumulative count, not a true unique count. The app uses `clientes_df["cliente_id"].nunique()` for the KPI card, which provides the accurate deduplicated count (50).

### Domain 2: Customer Segmentation

| KPI | Formula Validated | Result | Status |
|-----|------------------|--------|--------|
| 2.1 Customer Count by Segment | `value_counts()` | VIP: 49, TOP_TIER: 1, REGULAR: 0 | PASS |
| 2.2 Revenue by Segment | `groupby("segmento_cliente")["receita_total"].sum()` | VIP: R$ 964,412, TOP_TIER: R$ 9,665 | PASS |
| 2.3 Avg Ticket by Segment | `groupby("segmento_cliente")["ticket_medio"].mean()` | VIP: R$ 326.72, TOP_TIER: R$ 178.99 | PASS |
| 2.4 CLV Indicators | `tenure_days`, `purchase_frequency` calculated correctly | Avg tenure: VIP 28.7d, TOP_TIER 26d | PASS |

**Note on KPI 2.4:** The `replace(0, 1)` in the `purchase_frequency` formula correctly handles zero-tenure edge cases. No customers with `tenure_days = 0` exist in the current dataset, but the safeguard is appropriate.

### Domain 3: Price Competitiveness

| KPI | Formula Validated | Result | Status |
|-----|------------------|--------|--------|
| 3.1 Price Classification Distribution | `value_counts()` | ACIMA_DA_MEDIA: 92 (42.8%), ABAIXO_DA_MEDIA: 76 (35.3%) | PASS |
| 3.2 Avg Price Diff vs Competitors | `diferenca_percentual_vs_media.mean()` | Overall: +7.35% (skewed by Tenis category anomaly) | PASS |
| 3.3 Revenue by Price Classification | `groupby("classificacao_preco")["receita_total"].sum()` | ABAIXO_DA_MEDIA leads: R$ 456,277 | PASS |
| 3.4 Products Above/Below Market | Count by tier | 127 above (59.1%), 82 below (38.1%), 6 at market | PASS |

**Note on KPI 3.2 (important):** The `diferenca_percentual_vs_media` column is pre-computed in the CSV and matches the formula `(nosso_preco - preco_medio_concorrentes) / preco_medio_concorrentes * 100` exactly (max deviation: 0.000000). However, the Tenis category anomaly (all products at ~100%) inflates the overall average from ~0.5% to 7.35%. A filter excluding this category would produce a more representative result.

---

## 3. App Review (app.py)

### 3.1 Data Loading

| Check | Status | Notes |
|-------|--------|-------|
| All 3 CSV files loaded | PASS | Lines 20, 25, 37 |
| `data_venda` converted to datetime | PASS | Line 21 |
| Date fields in clientes converted | PASS | Lines 26–27 |
| `tenure_days` computed at load time | PASS | Lines 30–32 |
| `purchase_frequency` computed at load time | PASS | Lines 33–35 |
| `@st.cache_data` decorator used | PASS | Line 18 — prevents reloading on every interaction |

### 3.2 KPI Coverage

| KPI from metrics.md | Implemented in app.py | Chart Type | Status |
|--------------------|----------------------|------------|--------|
| 1.1 Total Revenue | Yes — KPI card (line 99) | Metric card | PASS |
| 1.2 Revenue Over Time (daily) | Yes — line chart (lines 126–138) | Line chart | PASS |
| 1.2 Revenue Over Time (monthly) | Yes — bar chart (lines 144–165) | Bar chart | PASS |
| 1.3 Sales Growth MoM | Yes — computed in monthly bar (line 154) | (in data; not shown as separate chart) | PASS |
| 1.4 Average Ticket | Yes — KPI card (lines 102–106) | Metric card | PASS |
| 1.5 Total Orders | Yes — KPI card (line 100) | Metric card | PASS |
| 1.5 Unique Customers | Yes — KPI card (line 101) with `nunique()` | Metric card | PASS |
| 1.6 Peak Sales Hours | Yes — hourly bar (lines 193–209) | Bar chart | PASS |
| 2.1 Customer Count by Segment | Yes — pie chart (lines 225–236) | Pie chart | PASS |
| 2.2 Revenue by Segment | Yes — bar chart (lines 240–255) | Bar chart | PASS |
| 2.3 Avg Ticket by Segment | Yes — bar chart (lines 261–276) | Bar chart | PASS |
| 2.4 CLV Indicators | Yes — dataframe table (lines 280–292) | Table | PASS |
| 3.1 Price Classification Distribution | Yes — bar chart (lines 342–358) | Bar chart | PASS |
| 3.2 Avg Price Diff by Category | Yes — bar chart (lines 382–402) | Bar chart | PASS |
| 3.3 Revenue by Price Classification | Yes — bar chart (lines 361–379) | Bar chart | PASS |
| 3.4 Products Above/Below Market | Yes — summary table + scatter (lines 406–460) | Table + Scatter | PASS |

**All 14 KPIs from metrics.md are implemented.** Coverage: 100%.

### 3.3 Chart Appropriateness

| Chart | Verdict |
|-------|---------|
| Daily Revenue — Line chart | PASS — correct for time-series trends |
| Monthly Revenue — Bar chart | PASS — correct for discrete monthly comparison |
| Revenue by Day of Week — Bar chart | PASS — correct for categorical comparison |
| Peak Hours — Bar chart | PASS — correct for 24-hour categorical distribution |
| Customer Count by Segment — Pie chart | PASS — appropriate for part-to-whole composition |
| Revenue by Segment — Bar chart | PASS — correct for categorical comparison |
| Avg Ticket by Segment — Bar chart | PASS — correct |
| CLV Indicators — Dataframe table | PASS — appropriate for multi-metric comparison |
| Price Classification Distribution — Bar chart | PASS — correct for categorical counts |
| Avg Price Diff by Category — Bar chart with hline | PASS — diverging bar is effective for +/− values |
| Revenue by Price Class — Bar chart | PASS — correct |
| Price Positioning vs Revenue — Scatter with size | PASS — ideal for two continuous variables + size dimension |

### 3.4 Potential Runtime Issues

| Issue | Severity | Location | Notes |
|-------|----------|----------|-------|
| Day-of-week reindex with `fill_value=0` | LOW | Lines 176–178 | Gracefully handles missing days; no error risk |
| Empty filtered dataset (e.g., no segment selected) | LOW | Lines 83–84 | If `segments=[]`, all charts will render with empty data — Plotly renders empty charts without crashing |
| Division in avg_ticket with `total_vendas.sum() > 0` guard | PASS | Lines 102–106 | Correctly guards against division by zero |
| `precos_with_rev` filter for scatter plot | PASS | Line 442 | Correctly excludes zero-revenue products from scatter |
| MoM growth `pct_change()` on single-month filtered data | LOW | Line 154 | If date filter produces only one month, `pct_change()` returns NaN for that single row — no crash, but no growth visible |

### 3.5 Sidebar Filter Behavior

| Filter | Implementation | Status |
|--------|---------------|--------|
| Date range filter | Applied to `vendas_f` only | OBSERVATION — date filter does not cross-filter `clientes_f` or `precos_f`; this is by design since those datasets have no direct date dimension at the mart level |
| Segment filter | Applied to `clientes_f` | PASS |
| Category filter | Applied to `precos_f` | PASS |

---

## 4. Edge Cases

### 4.1 Missing Values

No missing values exist in any of the 3 CSV files. All 0-null checks passed. No defensive null-handling is required beyond what the app already implements.

### 4.2 Zero Quantities / Zero Revenue

| Dataset | Zero-revenue products | Handling |
|---------|-----------------------|---------|
| `precos_competitividade_rows.csv` | 25 products with `receita_total = 0` (by tier: MAIS_CARO_QUE_TODOS: 16, ACIMA_DA_MEDIA: 9, ABAIXO_DA_MEDIA: 5) | App scatter chart correctly filters these out (line 442) |

**Observation:** 16 out of 35 products classified as `MAIS_CARO_QUE_TODOS` (45.7%) have zero revenue, suggesting overpricing may be suppressing conversions. This is a valid business insight surfaced by KPI 3.4.

### 4.3 Segment Imbalance

The customer dataset is heavily skewed: 49 VIP customers (98%) and only 1 TOP_TIER customer (2%). There are **no REGULAR customers** in the dataset. This means:

- KPI 2.1 pie chart will only show 2 slices (VIP, TOP_TIER)
- The `color_map` in the app defines a color for `REGULAR` that will never render
- All CLV averages are VIP-dominated

This is a data characteristic (likely a high-value customer dataset), not a bug. No code error is produced.

### 4.4 Tenis Category Pricing Anomaly

As noted in section 1.8, all Tenis products show `nosso_preco ≈ 2x preco_medio_concorrentes`. This inflates:
- KPI 3.2 overall average from ~0.5% to 7.35%
- The category-level bar chart will show Tenis at ~100% differential, dwarfing all other categories visually

The app renders this correctly (no code error), but the chart may be misleading to end users.

### 4.5 Single-Month Date Filter

If a user filters to a single month using the sidebar date picker:
- KPI 1.3 (MoM growth) will show `NaN` for the `mom_growth_pct` column — no crash, but no growth metric visible
- This is acceptable behavior for a single-month view

---

## 5. Recommendations

| Priority | Recommendation |
|----------|---------------|
| MEDIUM | **Tenis category anomaly:** Add a data quality warning note in the dashboard for the Tenis price differential chart, or investigate the data source for that category |
| LOW | **MoM Growth as explicit KPI card:** The MoM growth is calculated in the monthly dataframe but not surfaced as a visible metric card — consider adding a `st.metric()` for it |
| LOW | **REGULAR segment:** The dataset has no REGULAR customers; consider noting this in the dashboard or using the full customer population if available |
| LOW | **Zero-revenue products insight:** The 16 `MAIS_CARO_QUE_TODOS` products with zero revenue is a strong pricing insight — consider highlighting it as a KPI card (e.g., "Products with overpricing risk") |
| INFO | **`total_clientes_unicos` in KPI 1.5:** The app correctly uses `cliente_id.nunique()` from the segmentation dataset for the Unique Customers card, which is more accurate than summing the time-slot column from vendas |

---

## Appendix: Validation Scripts

The following scripts were used for validation and are available in `tests/`:

- `tests/validate_data.py` — Data quality checks (shapes, dtypes, nulls, duplicates, segmentation rules)
- `tests/validate_metrics.py` — KPI formula execution and cross-validation against CSV data

---

*Report generated: 2026-03-25 | QA Engineer — ecommerce-dashboard team*
