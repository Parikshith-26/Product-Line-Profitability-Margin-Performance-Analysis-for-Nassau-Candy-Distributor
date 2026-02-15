import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(layout="wide")

px.defaults.template = "plotly_dark"

st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }
    .stMetric {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("nassau_clean.xlsx")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.title("📊 Product Line Profitability Dashboard")

# -----------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------
st.sidebar.header("Filters")

min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

division = st.sidebar.multiselect(
    "Select Division",
    df["Division"].unique(),
    default=df["Division"].unique()
)

margin_threshold = st.sidebar.slider(
    "Margin Threshold (%)",
    0.0, 100.0, 10.0
)

product_search = st.sidebar.text_input("Search Product")

# -----------------------------------------------------
# APPLY FILTERS
# -----------------------------------------------------
filtered_df = df.copy()

filtered_df = filtered_df[
    (filtered_df["Date"] >= pd.to_datetime(date_range[0])) &
    (filtered_df["Date"] <= pd.to_datetime(date_range[1]))
]

filtered_df = filtered_df[
    filtered_df["Division"].isin(division)
]

if product_search:
    filtered_df = filtered_df[
        filtered_df["Product Name"].str.contains(product_search, case=False)
    ]

# -----------------------------------------------------
# KPI CALCULATIONS
# -----------------------------------------------------
filtered_df["Gross Profit"] = filtered_df["Sales"] - filtered_df["Cost"]

filtered_df["Gross Margin (%)"] = (
    filtered_df["Gross Profit"] / filtered_df["Sales"]
) * 100

filtered_df["Profit per Unit"] = (
    filtered_df["Gross Profit"] / filtered_df["Units"]
)

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()

filtered_df["Revenue Contribution (%)"] = (
    filtered_df["Sales"] / total_sales
) * 100

filtered_df["Profit Contribution (%)"] = (
    filtered_df["Gross Profit"] / total_profit
) * 100

# Risk Level
filtered_df["Risk Level"] = filtered_df["Gross Margin (%)"].apply(
    lambda x: "High Risk" if x < margin_threshold else "Safe"
)

# -----------------------------------------------------
# KPI CARDS
# -----------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Total Profit", f"{total_profit:,.0f}")
col3.metric(
    "Average Margin (%)",
    f"{filtered_df['Gross Margin (%)'].mean():.2f}"
)

# -----------------------------------------------------
# AUTOMATED INSIGHTS
# -----------------------------------------------------
st.markdown("## 🤖 Automated Insights")

if not filtered_df.empty:

    best_division = (
        filtered_df.groupby("Division")["Gross Profit"]
        .sum()
        .idxmax()
    )

    worst_margin_product = (
        filtered_df.groupby("Product Name")["Gross Margin (%)"]
        .mean()
        .idxmin()
    )

    high_risk_count = (
        filtered_df[filtered_df["Risk Level"] == "High Risk"]
        ["Product Name"].nunique()
    )

    profit_summary = (
        filtered_df.groupby("Product Name")["Gross Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    top_20_count = max(1, int(len(profit_summary) * 0.2))

    dependency_ratio = (
        profit_summary.head(top_20_count).sum()
        / profit_summary.sum()
    ) * 100

    avg_volatility = (
        filtered_df.groupby("Product Name")["Gross Margin (%)"]
        .std()
        .mean()
    )

    insight_text = f"""
• 📌 Highest Profit Division: **{best_division}**
• ⚠️ Lowest Margin Product: **{worst_margin_product}**
• 🔴 High Risk Products (< {margin_threshold}% margin): **{high_risk_count}**
• 📊 Top 20% Products Contribute **{dependency_ratio:.2f}%** of Total Profit
• 📈 Average Margin Volatility: **{avg_volatility:.2f}**
"""

    if dependency_ratio > 70:
        insight_text += "\n\n⚠️ High Profit Concentration Risk Detected"

    if avg_volatility > filtered_df["Gross Margin (%)"].std():
        insight_text += "\n\n⚠️ Margin Instability Detected"

    st.info(insight_text)

else:
    st.warning("No data available for selected filters.")

# -----------------------------------------------------
# EXPORT BUTTON
# -----------------------------------------------------
st.markdown("### 📥 Export Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_profitability_data.csv",
    mime="text/csv"
)

st.markdown("---")

# -----------------------------------------------------
# TABS
# -----------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Product Overview",
    "🏢 Division Performance",
    "⚠️ Cost Diagnostics",
    "📈 Profit Concentration"
])

# -----------------------------------------------------
# TAB 1 — PRODUCT OVERVIEW
# -----------------------------------------------------
with tab1:

    product_summary = (
        filtered_df.groupby("Product Name")
        .agg({
            "Sales": "sum",
            "Gross Profit": "sum",
            "Gross Margin (%)": "mean"
        })
        .reset_index()
    )

    product_summary["Profit Contribution (%)"] = (
        product_summary["Gross Profit"]
        / product_summary["Gross Profit"].sum()
    ) * 100

    volatility = (
        filtered_df.groupby("Product Name")["Gross Margin (%)"]
        .std()
        .reset_index()
        .rename(columns={"Gross Margin (%)": "Margin Volatility"})
    )

    product_summary = product_summary.merge(
        volatility,
        on="Product Name",
        how="left"
    )

    median_vol = product_summary["Margin Volatility"].median()

    product_summary["Volatility Risk"] = product_summary[
        "Margin Volatility"
    ].apply(lambda x: "High Volatility" if x > median_vol else "Stable")

    st.dataframe(
        product_summary.sort_values(
            "Gross Margin (%)", ascending=False
        ).style.background_gradient(
            subset=["Margin Volatility"],
            cmap="Reds"
        )
    )

    fig_pc = px.bar(
        product_summary.sort_values(
            "Profit Contribution (%)", ascending=False
        ).head(15),
        x="Product Name",
        y="Profit Contribution (%)",
        color="Profit Contribution (%)"
    )

    st.plotly_chart(fig_pc, use_container_width=True)

# -----------------------------------------------------
# TAB 2 — DIVISION PERFORMANCE
# -----------------------------------------------------
with tab2:

    division_summary = (
        filtered_df.groupby("Division")
        .agg({
            "Sales": "sum",
            "Gross Profit": "sum",
            "Gross Margin (%)": "mean"
        })
        .reset_index()
    )

    colA, colB = st.columns(2)

    fig_rev = px.bar(
        division_summary,
        x="Division",
        y=["Sales", "Gross Profit"],
        barmode="group"
    )

    colA.plotly_chart(fig_rev, use_container_width=True)

    fig_margin = px.box(
        filtered_df,
        x="Division",
        y="Gross Margin (%)"
    )

    colB.plotly_chart(fig_margin, use_container_width=True)

# -----------------------------------------------------
# TAB 3 — COST DIAGNOSTICS
# -----------------------------------------------------
with tab3:

    fig_cs = px.scatter(
        filtered_df,
        x="Cost",
        y="Sales",
        color="Risk Level",
        size="Gross Profit",
        hover_name="Product Name"
    )

    st.plotly_chart(fig_cs, use_container_width=True)

# -----------------------------------------------------
# TAB 4 — PROFIT CONCENTRATION
# -----------------------------------------------------
with tab4:

    pareto = (
        filtered_df.groupby("Product Name")["Gross Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    pareto["Cumulative Profit"] = pareto["Gross Profit"].cumsum()
    pareto["Cumulative %"] = (
        pareto["Cumulative Profit"]
        / pareto["Gross Profit"].sum()
    ) * 100

    top_20_count = int(len(pareto) * 0.2)
    top_20_profit_share = (
        pareto.head(top_20_count)["Gross Profit"].sum()
        / pareto["Gross Profit"].sum()
    ) * 100

    st.metric(
        "Top 20% Product Profit Share",
        f"{top_20_profit_share:.2f}%"
    )

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=pareto["Product Name"],
        y=pareto["Gross Profit"],
        name="Gross Profit"
    ))

    fig.add_trace(go.Scatter(
        x=pareto["Product Name"],
        y=pareto["Cumulative %"],
        name="Cumulative %",
        yaxis="y2",
        mode="lines+markers"
    ))

    fig.update_layout(
        yaxis=dict(title="Gross Profit"),
        yaxis2=dict(
            title="Cumulative %",
            overlaying="y",
            side="right"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
