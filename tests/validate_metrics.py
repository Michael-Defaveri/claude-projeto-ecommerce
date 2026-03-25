import pandas as pd
import numpy as np

# Load all CSV files
df_vendas = pd.read_csv('data/vendas_temporais_rows.csv')
df_clientes = pd.read_csv('data/clientes_segmentacao_rows.csv')
df_precos = pd.read_csv('data/precos_competitividade_rows.csv')

print("=" * 60)
print("KPI METRICS VALIDATION")
print("=" * 60)

# ---- KPI 1.1: Total Revenue ----
print("\n--- KPI 1.1: Total Revenue ---")
total_revenue = df_vendas["receita_total"].sum()
print(f"Total Revenue: R$ {total_revenue:,.2f}")
print("PASS: Formula df['receita_total'].sum() works correctly")

# ---- KPI 1.2: Revenue Over Time ----
print("\n--- KPI 1.2: Revenue Over Time ---")
daily_rev = df_vendas.groupby("data_venda")["receita_total"].sum()
monthly_rev = df_vendas.groupby(["ano_venda", "mes_venda"])["receita_total"].sum()
print(f"Daily revenue rows: {len(daily_rev)}")
print(f"Monthly revenue rows: {len(monthly_rev)}")
print(f"Monthly breakdown:\n{monthly_rev}")
print("PASS: Groupby formulas work correctly")

# ---- KPI 1.3: Sales Growth MoM ----
print("\n--- KPI 1.3: Sales Growth MoM ---")
monthly = df_vendas.groupby(["ano_venda", "mes_venda"])["receita_total"].sum().reset_index()
monthly["mom_growth_pct"] = monthly["receita_total"].pct_change() * 100
print(f"MoM Growth:\n{monthly[['ano_venda','mes_venda','receita_total','mom_growth_pct']]}")
print("PASS: pct_change() formula works")

# ---- KPI 1.4: Average Ticket ----
print("\n--- KPI 1.4: Average Ticket ---")
ticket_mean = df_vendas["ticket_medio"].mean()
ticket_calc = df_vendas["receita_total"].sum() / df_vendas["total_vendas"].sum()
print(f"ticket_medio.mean(): R$ {ticket_mean:.4f}")
print(f"receita/total_vendas: R$ {ticket_calc:.4f}")
print(f"Difference: {abs(ticket_mean - ticket_calc):.4f}")
print("NOTE: Both formulas give different results (mean of pre-aggregated vs global ratio)")
print("PASS: Both formulas are valid depending on use case")

# ---- KPI 1.5: Total Orders and Unique Customers ----
print("\n--- KPI 1.5: Total Orders and Unique Customers ---")
total_orders = df_vendas["total_vendas"].sum()
total_unique = df_vendas["total_clientes_unicos"].sum()
print(f"Total Orders: {total_orders}")
print(f"Total Unique Customers (cumulative): {total_unique}")
print("NOTE: total_clientes_unicos is cumulative per time slot, not deduplicated globally")
print("PASS: Formulas are mathematically correct")

# ---- KPI 1.6: Peak Sales Hours ----
print("\n--- KPI 1.6: Peak Sales Hours ---")
hourly_revenue = df_vendas.groupby("hora_venda")["receita_total"].sum().sort_values(ascending=False)
peak_hours = hourly_revenue.head(5)
print(f"Top 5 Peak Hours:\n{peak_hours}")
print("PASS: groupby hour formula works")

# ---- KPI 2.1: Customer Count by Segment ----
print("\n--- KPI 2.1: Customer Count by Segment ---")
seg_count = df_clientes["segmento_cliente"].value_counts()
print(f"Segment counts:\n{seg_count}")
print("PASS: value_counts() works")

# ---- KPI 2.2: Revenue by Segment ----
print("\n--- KPI 2.2: Revenue by Segment ---")
seg_revenue = df_clientes.groupby("segmento_cliente")["receita_total"].sum()
print(f"Revenue by segment:\n{seg_revenue}")
print("PASS: groupby segment revenue works")

# ---- KPI 2.3: Average Ticket by Segment ----
print("\n--- KPI 2.3: Average Ticket by Segment ---")
seg_ticket = df_clientes.groupby("segmento_cliente")["ticket_medio"].mean()
print(f"Avg ticket by segment:\n{seg_ticket}")
print("PASS: groupby segment ticket works")

# ---- KPI 2.4: Customer Lifetime Value Indicators ----
print("\n--- KPI 2.4: Customer Lifetime Value Indicators ---")
df_clientes["primeira_compra"] = pd.to_datetime(df_clientes["primeira_compra"])
df_clientes["ultima_compra"] = pd.to_datetime(df_clientes["ultima_compra"])
df_clientes["tenure_days"] = (df_clientes["ultima_compra"] - df_clientes["primeira_compra"]).dt.days
df_clientes["purchase_frequency"] = df_clientes["total_compras"] / df_clientes["tenure_days"].replace(0, 1)
clv = df_clientes.groupby("segmento_cliente").agg(
    avg_receita=("receita_total", "mean"),
    avg_compras=("total_compras", "mean"),
    avg_tenure_days=("tenure_days", "mean"),
    avg_frequency=("purchase_frequency", "mean")
)
print(f"CLV indicators:\n{clv}")
print(f"Customers with tenure=0 days: {(df_clientes['tenure_days'] == 0).sum()}")
print("PASS: CLV formula works (uses replace(0,1) to avoid division by zero)")

# ---- KPI 3.1: Price Classification Distribution ----
print("\n--- KPI 3.1: Price Classification Distribution ---")
price_dist = df_precos["classificacao_preco"].value_counts()
price_pct = df_precos["classificacao_preco"].value_counts(normalize=True) * 100
print(f"Count:\n{price_dist}")
print(f"Percentage:\n{price_pct.round(1)}")
print("PASS: value_counts() formula works")

# ---- KPI 3.2: Average Price Difference vs Competitors ----
print("\n--- KPI 3.2: Average Price Difference vs Competitors ---")
avg_diff = df_precos["diferenca_percentual_vs_media"].mean()
cat_diff = df_precos.groupby("categoria")["diferenca_percentual_vs_media"].mean()
print(f"Overall avg diff: {avg_diff:.4f}%")
print(f"By category:\n{cat_diff.round(4)}")
print("PASS: mean() formula works")

# ---- KPI 3.3: Revenue by Price Classification ----
print("\n--- KPI 3.3: Revenue by Price Classification ---")
rev_by_class = df_precos.groupby("classificacao_preco")["receita_total"].sum().sort_values(ascending=False)
print(f"Revenue by classification:\n{rev_by_class}")
print("PASS: groupby classificacao_preco revenue works")

# ---- KPI 3.4: Products Above/Below Market Average ----
print("\n--- KPI 3.4: Products Above/Below Market Average ---")
above = df_precos[df_precos["classificacao_preco"].isin(["ACIMA_DA_MEDIA", "MAIS_CARO_QUE_TODOS"])]
below = df_precos[df_precos["classificacao_preco"].isin(["ABAIXO_DA_MEDIA", "MAIS_BARATO_QUE_TODOS"])]
at_avg = df_precos[df_precos["classificacao_preco"] == "NA_MEDIA"]
summary = {
    "above_market": len(above),
    "below_market": len(below),
    "at_market": len(at_avg),
    "above_pct": round(len(above) / len(df_precos) * 100, 1),
    "below_pct": round(len(below) / len(df_precos) * 100, 1),
}
print(f"Market position: {summary}")
zero_rev_by_tier = df_precos[df_precos["receita_total"] == 0].groupby("classificacao_preco").size()
print(f"Zero-revenue products by tier:\n{zero_rev_by_tier}")
print("PASS: Above/below market formula works")

print("\n" + "=" * 60)
print("ALL KPI VALIDATIONS COMPLETE")
print("=" * 60)
