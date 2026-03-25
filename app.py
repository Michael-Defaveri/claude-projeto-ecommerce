import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide",
)

# ──────────────────────────────────────────────
# Data loading
# ──────────────────────────────────────────────
@st.cache_data
def load_data():
    vendas = pd.read_csv("data/vendas_temporais_rows.csv")
    vendas["data_venda"] = pd.to_datetime(vendas["data_venda"])
    vendas["receita_total"] = vendas["receita_total"].astype(float)
    vendas["ticket_medio"] = vendas["ticket_medio"].astype(float)

    clientes = pd.read_csv("data/clientes_segmentacao_rows.csv")
    clientes["primeira_compra"] = pd.to_datetime(clientes["primeira_compra"])
    clientes["ultima_compra"] = pd.to_datetime(clientes["ultima_compra"])
    clientes["receita_total"] = clientes["receita_total"].astype(float)
    clientes["ticket_medio"] = clientes["ticket_medio"].astype(float)
    clientes["tenure_days"] = (
        clientes["ultima_compra"] - clientes["primeira_compra"]
    ).dt.days
    clientes["purchase_frequency"] = clientes["total_compras"] / clientes[
        "tenure_days"
    ].replace(0, 1)

    precos = pd.read_csv("data/precos_competitividade_rows.csv")
    precos["receita_total"] = precos["receita_total"].astype(float)
    precos["diferenca_percentual_vs_media"] = precos[
        "diferenca_percentual_vs_media"
    ].astype(float)

    return vendas, clientes, precos


vendas, clientes, precos = load_data()

# ──────────────────────────────────────────────
# Sidebar filters
# ──────────────────────────────────────────────
st.sidebar.header("Filters")

date_min = vendas["data_venda"].min().date()
date_max = vendas["data_venda"].max().date()
date_range = st.sidebar.date_input(
    "Date range",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max,
)

segments = st.sidebar.multiselect(
    "Customer segments",
    options=sorted(clientes["segmento_cliente"].unique()),
    default=sorted(clientes["segmento_cliente"].unique()),
)

categories = st.sidebar.multiselect(
    "Product categories",
    options=sorted(precos["categoria"].dropna().unique()),
    default=sorted(precos["categoria"].dropna().unique()),
)

# Apply date filter
if len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_date, end_date = vendas["data_venda"].min(), vendas["data_venda"].max()

vendas_f = vendas[
    (vendas["data_venda"] >= start_date) & (vendas["data_venda"] <= end_date)
]
clientes_f = clientes[clientes["segmento_cliente"].isin(segments)]
precos_f = precos[precos["categoria"].isin(categories)]

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.title("E-Commerce Dashboard")
st.caption(
    "Gold layer analytics — Revenue & Sales | Customer Segmentation | Price Competitiveness"
)
st.divider()

# ──────────────────────────────────────────────
# Section 1: KPI cards
# ──────────────────────────────────────────────
def render_kpi_cards(vendas_df, clientes_df):
    total_revenue = vendas_df["receita_total"].sum()
    total_orders = vendas_df["total_vendas"].sum()
    total_unique_customers = clientes_df["cliente_id"].nunique()
    avg_ticket = (
        vendas_df["receita_total"].sum() / vendas_df["total_vendas"].sum()
        if vendas_df["total_vendas"].sum() > 0
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"R$ {total_revenue:,.2f}")
    c2.metric("Total Orders", f"{int(total_orders):,}")
    c3.metric("Unique Customers", f"{total_unique_customers:,}")
    c4.metric("Average Ticket", f"R$ {avg_ticket:,.2f}")


st.subheader("Key Metrics")
render_kpi_cards(vendas_f, clientes_f)
st.divider()

# ──────────────────────────────────────────────
# Section 2: Sales Trends
# ──────────────────────────────────────────────
def render_sales_trends(vendas_df):
    st.subheader("Sales Trends")

    # KPI 1.2 — Daily revenue line chart
    daily = (
        vendas_df.groupby("data_venda")["receita_total"].sum().reset_index()
    )
    daily.columns = ["Date", "Revenue"]
    fig_daily = px.line(
        daily,
        x="Date",
        y="Revenue",
        title="Daily Revenue",
        labels={"Revenue": "Revenue (R$)"},
    )
    fig_daily.update_traces(line_color="#1f77b4")
    st.plotly_chart(fig_daily, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # KPI 1.2 / 1.3 — Monthly revenue bar + MoM growth
        monthly = (
            vendas_df.groupby(["ano_venda", "mes_venda"])["receita_total"]
            .sum()
            .reset_index()
        )
        monthly["period"] = (
            monthly["ano_venda"].astype(str)
            + "-"
            + monthly["mes_venda"].astype(str).str.zfill(2)
        )
        monthly["mom_growth_pct"] = monthly["receita_total"].pct_change() * 100
        fig_monthly = px.bar(
            monthly,
            x="period",
            y="receita_total",
            title="Monthly Revenue",
            labels={"period": "Month", "receita_total": "Revenue (R$)"},
            color="receita_total",
            color_continuous_scale="Blues",
        )
        fig_monthly.update_coloraxes(showscale=False)
        st.plotly_chart(fig_monthly, use_container_width=True)

    with col_b:
        # KPI 1.6 — Sales by day of week
        dow_order = [
            "Segunda", "Terca", "Quarta", "Quinta",
            "Sexta", "Sabado", "Domingo",
        ]
        dow = (
            vendas_df.groupby("dia_semana_nome")["receita_total"]
            .sum()
            .reindex(dow_order, fill_value=0)
            .reset_index()
        )
        dow.columns = ["Day", "Revenue"]
        fig_dow = px.bar(
            dow,
            x="Day",
            y="Revenue",
            title="Revenue by Day of Week",
            labels={"Revenue": "Revenue (R$)"},
            color="Revenue",
            color_continuous_scale="Greens",
        )
        fig_dow.update_coloraxes(showscale=False)
        st.plotly_chart(fig_dow, use_container_width=True)

    # KPI 1.6 — Peak hours heatmap-style bar
    hourly = (
        vendas_df.groupby("hora_venda")["receita_total"].sum().reset_index()
    )
    hourly.columns = ["Hour", "Revenue"]
    hourly = hourly.sort_values("Hour")
    fig_hourly = px.bar(
        hourly,
        x="Hour",
        y="Revenue",
        title="Revenue by Hour of Day (Peak Hours Analysis)",
        labels={"Hour": "Hour (0–23)", "Revenue": "Revenue (R$)"},
        color="Revenue",
        color_continuous_scale="Oranges",
    )
    fig_hourly.update_coloraxes(showscale=False)
    fig_hourly.update_xaxes(dtick=1)
    st.plotly_chart(fig_hourly, use_container_width=True)


render_sales_trends(vendas_f)
st.divider()

# ──────────────────────────────────────────────
# Section 3: Customer Segmentation
# ──────────────────────────────────────────────
def render_customer_segmentation(clientes_df):
    st.subheader("Customer Segmentation")

    col_a, col_b = st.columns(2)

    with col_a:
        # KPI 2.1 — Segment distribution pie chart
        seg_counts = clientes_df["segmento_cliente"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        color_map = {"VIP": "#FFD700", "TOP_TIER": "#C0C0C0", "REGULAR": "#CD7F32"}
        fig_pie = px.pie(
            seg_counts,
            names="Segment",
            values="Count",
            title="Customer Count by Segment",
            color="Segment",
            color_discrete_map=color_map,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        # KPI 2.2 — Revenue by segment
        seg_rev = (
            clientes_df.groupby("segmento_cliente")["receita_total"]
            .sum()
            .reset_index()
        )
        seg_rev.columns = ["Segment", "Revenue"]
        fig_seg_rev = px.bar(
            seg_rev,
            x="Segment",
            y="Revenue",
            title="Revenue by Segment",
            labels={"Revenue": "Revenue (R$)"},
            color="Segment",
            color_discrete_map=color_map,
        )
        st.plotly_chart(fig_seg_rev, use_container_width=True)

    # KPI 2.3 — Average ticket by segment + KPI 2.4 CLV indicators
    col_c, col_d = st.columns(2)

    with col_c:
        seg_ticket = (
            clientes_df.groupby("segmento_cliente")["ticket_medio"]
            .mean()
            .reset_index()
        )
        seg_ticket.columns = ["Segment", "Avg Ticket"]
        fig_ticket = px.bar(
            seg_ticket,
            x="Segment",
            y="Avg Ticket",
            title="Average Ticket by Segment",
            labels={"Avg Ticket": "Avg Ticket (R$)"},
            color="Segment",
            color_discrete_map=color_map,
        )
        st.plotly_chart(fig_ticket, use_container_width=True)

    with col_d:
        # KPI 2.4 — CLV indicators table
        clv = clientes_df.groupby("segmento_cliente").agg(
            avg_receita=("receita_total", "mean"),
            avg_compras=("total_compras", "mean"),
            avg_tenure_days=("tenure_days", "mean"),
            avg_frequency=("purchase_frequency", "mean"),
        ).reset_index()
        clv.columns = ["Segment", "Avg Revenue", "Avg Orders", "Avg Tenure (days)", "Avg Freq (orders/day)"]
        clv["Avg Revenue"] = clv["Avg Revenue"].map("R$ {:,.2f}".format)
        clv["Avg Orders"] = clv["Avg Orders"].map("{:.1f}".format)
        clv["Avg Tenure (days)"] = clv["Avg Tenure (days)"].map("{:.0f}".format)
        clv["Avg Freq (orders/day)"] = clv["Avg Freq (orders/day)"].map("{:.3f}".format)
        st.markdown("**Customer Lifetime Value Indicators by Segment**")
        st.dataframe(clv, use_container_width=True, hide_index=True)

    # Top customers table
    st.markdown("**Top 10 Customers by Revenue**")
    top_customers = (
        clientes_df.sort_values("receita_total", ascending=False)
        .head(10)[
            [
                "ranking_receita",
                "nome_cliente",
                "estado",
                "segmento_cliente",
                "receita_total",
                "total_compras",
                "ticket_medio",
            ]
        ]
        .copy()
    )
    top_customers.columns = [
        "Rank", "Customer", "State", "Segment", "Revenue (R$)", "Orders", "Avg Ticket (R$)"
    ]
    top_customers["Revenue (R$)"] = top_customers["Revenue (R$)"].map("{:,.2f}".format)
    top_customers["Avg Ticket (R$)"] = top_customers["Avg Ticket (R$)"].map("{:,.2f}".format)
    st.dataframe(top_customers, use_container_width=True, hide_index=True)


render_customer_segmentation(clientes_f)
st.divider()

# ──────────────────────────────────────────────
# Section 4: Price Competitiveness
# ──────────────────────────────────────────────
def render_price_competitiveness(precos_df):
    st.subheader("Price Competitiveness")

    classification_order = [
        "MAIS_BARATO_QUE_TODOS",
        "ABAIXO_DA_MEDIA",
        "NA_MEDIA",
        "ACIMA_DA_MEDIA",
        "MAIS_CARO_QUE_TODOS",
    ]
    color_seq = ["#2ecc71", "#82e0aa", "#f7dc6f", "#e59866", "#e74c3c"]
    color_map_price = dict(zip(classification_order, color_seq))

    col_a, col_b = st.columns(2)

    with col_a:
        # KPI 3.1 — Price classification distribution
        price_dist = (
            precos_df["classificacao_preco"]
            .value_counts()
            .reindex(classification_order, fill_value=0)
            .reset_index()
        )
        price_dist.columns = ["Classification", "Count"]
        fig_price_dist = px.bar(
            price_dist,
            x="Classification",
            y="Count",
            title="Price Classification Distribution",
            color="Classification",
            color_discrete_map=color_map_price,
        )
        fig_price_dist.update_layout(showlegend=False)
        st.plotly_chart(fig_price_dist, use_container_width=True)

    with col_b:
        # KPI 3.3 — Revenue by price classification
        rev_by_class = (
            precos_df.groupby("classificacao_preco")["receita_total"]
            .sum()
            .reindex(classification_order, fill_value=0)
            .reset_index()
        )
        rev_by_class.columns = ["Classification", "Revenue"]
        fig_rev_class = px.bar(
            rev_by_class,
            x="Classification",
            y="Revenue",
            title="Revenue by Price Classification",
            labels={"Revenue": "Revenue (R$)"},
            color="Classification",
            color_discrete_map=color_map_price,
        )
        fig_rev_class.update_layout(showlegend=False)
        st.plotly_chart(fig_rev_class, use_container_width=True)

    # KPI 3.2 — Average price difference vs competitors by category
    avg_diff_cat = (
        precos_df.groupby("categoria")["diferenca_percentual_vs_media"]
        .mean()
        .reset_index()
        .sort_values("diferenca_percentual_vs_media", ascending=False)
    )
    avg_diff_cat.columns = ["Category", "Avg Price Diff (%)"]
    avg_diff_cat["color"] = avg_diff_cat["Avg Price Diff (%)"].apply(
        lambda x: "Above Market" if x > 0 else "Below Market"
    )
    fig_diff = px.bar(
        avg_diff_cat,
        x="Category",
        y="Avg Price Diff (%)",
        title="Avg Price Difference vs Competitors by Category (%)",
        color="color",
        color_discrete_map={"Above Market": "#e74c3c", "Below Market": "#2ecc71"},
        labels={"color": "Position"},
    )
    fig_diff.add_hline(y=0, line_dash="dash", line_color="gray")
    st.plotly_chart(fig_diff, use_container_width=True)

    # KPI 3.4 — Products above/below market summary + scatter
    col_c, col_d = st.columns([1, 2])

    with col_c:
        above = precos_df[
            precos_df["classificacao_preco"].isin(
                ["ACIMA_DA_MEDIA", "MAIS_CARO_QUE_TODOS"]
            )
        ]
        below = precos_df[
            precos_df["classificacao_preco"].isin(
                ["ABAIXO_DA_MEDIA", "MAIS_BARATO_QUE_TODOS"]
            )
        ]
        at_avg = precos_df[precos_df["classificacao_preco"] == "NA_MEDIA"]
        total = len(precos_df)

        summary_data = {
            "Position": ["Above Market", "At Market", "Below Market"],
            "Products": [len(above), len(at_avg), len(below)],
            "% of Catalog": [
                f"{len(above)/total*100:.1f}%",
                f"{len(at_avg)/total*100:.1f}%",
                f"{len(below)/total*100:.1f}%",
            ],
        }
        st.markdown("**Products vs Market Average (KPI 3.4)**")
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

        avg_overall = precos_df["diferenca_percentual_vs_media"].mean()
        st.metric(
            "Overall Avg Price Diff vs Market",
            f"{avg_overall:+.2f}%",
            help="Positive = we are pricier than average competitor",
        )

    with col_d:
        # Scatter: price diff vs revenue (only products with revenue > 0)
        precos_with_rev = precos_df[precos_df["receita_total"] > 0].copy()
        fig_scatter = px.scatter(
            precos_with_rev,
            x="diferenca_percentual_vs_media",
            y="receita_total",
            color="classificacao_preco",
            size="quantidade_total",
            hover_name="nome_produto",
            hover_data=["categoria", "nosso_preco"],
            title="Price Positioning vs Revenue (products with sales)",
            labels={
                "diferenca_percentual_vs_media": "Price Diff vs Avg Competitor (%)",
                "receita_total": "Revenue (R$)",
                "classificacao_preco": "Price Class",
            },
            color_discrete_map=color_map_price,
        )
        fig_scatter.add_vline(x=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_scatter, use_container_width=True)


render_price_competitiveness(precos_f)

st.divider()
st.caption("Data source: Gold layer CSVs — data/ | Built with Streamlit + Plotly")
