import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================================================
# PAGE
# =========================================================
st.set_page_config(
    page_title="Indian E-Commerce Business Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM DESIGN
# =========================================================
st.markdown("""
<style>
/* ---------- Overall ---------- */
.stApp {
    background: #f3f7f6;
}

.block-container {
    max-width: 1500px;
    padding: 1.2rem 2rem 2rem 2rem;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102a2e 0%, #164e52 100%);
}

section[data-testid="stSidebar"] * {
    color: #f4fffd !important;
}

section[data-testid="stSidebar"] .stCaption {
    color: #c6e5e1 !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background: #ffffff !important;
    border-radius: 10px;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #16383b !important;
}

/* ---------- Header ---------- */
.hero {
    background: linear-gradient(115deg, #0f3d3e 0%, #147d78 58%, #20a39e 100%);
    border-radius: 22px;
    padding: 30px 34px;
    margin-bottom: 20px;
    box-shadow: 0 12px 30px rgba(15, 61, 62, 0.20);
}

.hero h1 {
    color: white;
    margin: 0;
    font-size: 2.25rem;
    font-weight: 800;
}

.hero p {
    color: #d9fffa;
    margin: 8px 0 0;
    font-size: 1rem;
}

/* ---------- Info strip ---------- */
.info-strip {
    background: #e6f5f2;
    border: 1px solid #b9dfd9;
    color: #174e4d;
    border-radius: 12px;
    padding: 10px 15px;
    margin-bottom: 18px;
    font-size: 0.9rem;
}

/* ---------- KPI cards ---------- */
.kpi {
    background: white;
    border-radius: 16px;
    padding: 18px 20px;
    border: 1px solid #dce9e7;
    border-top: 5px solid #159a91;
    box-shadow: 0 7px 22px rgba(22, 78, 82, 0.08);
    min-height: 120px;
}

.kpi:nth-child(2) { border-top-color: #e3a72f; }
.kpi:nth-child(3) { border-top-color: #4776c8; }
.kpi:nth-child(4) { border-top-color: #8c63c7; }
.kpi:nth-child(5) { border-top-color: #e06b75; }

.kpi-label {
    color: #607779;
    font-size: 0.76rem;
    font-weight: 750;
    letter-spacing: .06em;
    text-transform: uppercase;
}

.kpi-value {
    color: #17383b;
    font-size: 1.65rem;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-note {
    color: #7b8f91;
    font-size: .78rem;
    margin-top: 4px;
}

/* ---------- Section headers ---------- */
.section {
    color: #17383b;
    font-size: 1.18rem;
    font-weight: 800;
    margin: 24px 0 10px;
}

/* ---------- Cards around charts ---------- */
.chart-card {
    background: white;
    border: 1px solid #e0ebe9;
    border-radius: 16px;
    padding: 8px 10px 4px;
    box-shadow: 0 5px 18px rgba(22, 78, 82, 0.06);
}

/* ---------- Insight cards ---------- */
.insight {
    background: white;
    border-radius: 14px;
    border-left: 5px solid #159a91;
    padding: 15px 17px;
    margin-bottom: 12px;
    box-shadow: 0 5px 16px rgba(22, 78, 82, 0.06);
}

.insight b {
    color: #17383b;
}

.insight span {
    color: #607779;
    font-size: .9rem;
}

/* ---------- Footer ---------- */
.footer {
    text-align: center;
    color: #789092;
    padding: 28px 0 5px;
    font-size: .78rem;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "Indian_Ecommerce_Sales_Analysis_Dataset.csv"
    data = pd.read_csv(file_path)
    data["Order_Date"] = pd.to_datetime(data["Order_Date"], errors="coerce")
    return data.dropna(subset=["Order_Date"]).copy()

df = load_data()

dataset_start = df["Order_Date"].min().date()
dataset_end = df["Order_Date"].max().date()

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("## 🛒 E-Commerce Dashboard")
st.sidebar.caption("Filter the business data to explore performance.")

states = sorted(df["State"].dropna().unique())
categories = sorted(df["Category"].dropna().unique())
statuses = sorted(df["Order_Status"].dropna().unique())

selected_states = st.sidebar.multiselect(
    "📍 State",
    states,
    default=states
)

selected_categories = st.sidebar.multiselect(
    "🛍️ Category",
    categories,
    default=categories
)

selected_statuses = st.sidebar.multiselect(
    "🚚 Order Status",
    statuses,
    default=statuses
)

st.sidebar.markdown("### 📅 Date Range")

# Two separate date boxes so the complete date is always visible.
start_date = st.sidebar.date_input(
    "Start date",
    value=dataset_start,
    min_value=dataset_start,
    max_value=dataset_end,
    format="DD/MM/YYYY"
)

end_date = st.sidebar.date_input(
    "End date",
    value=dataset_end,
    min_value=dataset_start,
    max_value=dataset_end,
    format="DD/MM/YYYY"
)

if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")
    st.stop()

st.sidebar.markdown(
    f"""
    <div style="
        background:#e8f7f4;
        color:#164e52;
        padding:10px;
        border-radius:10px;
        margin-top:8px;
        font-size:0.82rem;">
        <b>Dataset period</b><br>
        {dataset_start.strftime("%d %B %Y")} → {dataset_end.strftime("%d %B %Y")}
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FILTER
# =========================================================
filtered = df[
    df["State"].isin(selected_states)
    & df["Category"].isin(selected_categories)
    & df["Order_Status"].isin(selected_statuses)
    & (df["Order_Date"].dt.date >= start_date)
    & (df["Order_Date"].dt.date <= end_date)
].copy()

if filtered.empty:
    st.warning("No records match the selected filters. Please broaden the filters.")
    st.stop()

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <h1>🛒 Indian E-Commerce Business Dashboard</h1>
    <p>Interactive analysis of sales, profitability, orders, products and regional performance</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="info-strip">
        📅 <b>Selected period:</b>
        {start_date.strftime("%d %B %Y")} → {end_date.strftime("%d %B %Y")}
        &nbsp;&nbsp; | &nbsp;&nbsp;
        📊 <b>Records analysed:</b> {len(filtered):,}
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# KPI
# =========================================================
total_sales = filtered["Sales_INR"].sum()
total_profit = filtered["Profit_INR"].sum()
total_orders = filtered["Order_ID"].nunique()
total_quantity = filtered["Quantity"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

kpi_cols = st.columns(5)

kpis = [
    ("Total Sales", f"₹{total_sales:,.0f}", "Revenue generated"),
    ("Total Profit", f"₹{total_profit:,.0f}", "Net profit"),
    ("Total Orders", f"{total_orders:,}", "Unique orders"),
    ("Quantity Sold", f"{total_quantity:,}", "Units sold"),
    ("Profit Margin", f"{profit_margin:.2f}%", "Profit / sales")
]

for col, (label, value, note) in zip(kpi_cols, kpis):
    with col:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# PREP DATA
# =========================================================
monthly = (
    filtered.groupby(filtered["Order_Date"].dt.to_period("M"))["Sales_INR"]
    .sum()
    .reset_index()
)
monthly["Month"] = monthly["Order_Date"].dt.strftime("%b %Y")

category_sales = (
    filtered.groupby("Category", as_index=False)["Sales_INR"]
    .sum()
    .sort_values("Sales_INR", ascending=False)
)

category_profit = (
    filtered.groupby("Category", as_index=False)["Profit_INR"]
    .sum()
    .sort_values("Profit_INR", ascending=False)
)

state_sales = (
    filtered.groupby("State", as_index=False)
    .agg(Sales_INR=("Sales_INR", "sum"), Profit_INR=("Profit_INR", "sum"))
    .sort_values("Sales_INR", ascending=False)
)

payment = filtered["Payment_Mode"].value_counts().reset_index()
payment.columns = ["Payment_Mode", "Count"]

status = filtered["Order_Status"].value_counts().reset_index()
status.columns = ["Order_Status", "Count"]

top_products = (
    filtered.groupby("Sub_Category", as_index=False)
    .agg(
        Sales_INR=("Sales_INR", "sum"),
        Profit_INR=("Profit_INR", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values("Sales_INR", ascending=False)
    .head(10)
)

# =========================================================
# CHART STYLE
# =========================================================
def chart_style(fig, height=350):
    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Arial", color="#35575a"),
        margin=dict(l=35, r=20, t=60, b=40),
        title_font=dict(size=17, color="#17383b"),
        hoverlabel=dict(bgcolor="white", font_size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#e4eeee")
    return fig

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3 = st.tabs([
    "📊 Executive Overview",
    "📦 Products & Orders",
    "💡 Business Insights"
])

# =========================================================
# TAB 1
# =========================================================
with tab1:
    st.markdown('<div class="section">📈 Sales & Profit Performance</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.line(
            monthly,
            x="Month",
            y="Sales_INR",
            markers=True,
            title="Monthly Sales Trend"
        )
        fig.update_traces(line_width=3, marker_size=8)
        st.plotly_chart(chart_style(fig), use_container_width=True)

    with c2:
        fig = px.bar(
            category_sales,
            x="Category",
            y="Sales_INR",
            text_auto=".2s",
            title="Sales by Category"
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(chart_style(fig), use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            state_sales.head(10),
            x="Sales_INR",
            y="State",
            orientation="h",
            text_auto=".2s",
            title="Top 10 States by Sales"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(chart_style(fig), use_container_width=True)

    with c2:
        fig = px.bar(
            category_profit,
            x="Category",
            y="Profit_INR",
            text_auto=".2s",
            title="Profit by Category"
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(chart_style(fig), use_container_width=True)

# =========================================================
# TAB 2
# =========================================================
with tab2:
    st.markdown('<div class="section">📦 Product & Order Behaviour</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.pie(
            payment,
            names="Payment_Mode",
            values="Count",
            hole=0.58,
            title="Payment Method Distribution"
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(chart_style(fig), use_container_width=True)

    with c2:
        fig = px.pie(
            status,
            names="Order_Status",
            values="Count",
            hole=0.58,
            title="Order Status Distribution"
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(chart_style(fig), use_container_width=True)

    fig = px.scatter(
        filtered,
        x="Quantity",
        y="Sales_INR",
        color="Category",
        hover_data=["Sub_Category", "State", "Order_Status"],
        title="Quantity vs Sales"
    )
    fig.update_traces(marker_size=9, opacity=0.72)
    st.plotly_chart(chart_style(fig, 390), use_container_width=True)

    st.markdown('<div class="section">🏆 Top 10 Product Segments</div>', unsafe_allow_html=True)

    table = top_products.copy()
    table["Sales_INR"] = table["Sales_INR"].map(lambda x: f"₹{x:,.0f}")
    table["Profit_INR"] = table["Profit_INR"].map(lambda x: f"₹{x:,.0f}")

    st.dataframe(table, use_container_width=True, hide_index=True)

# =========================================================
# TAB 3
# =========================================================
with tab3:
    st.markdown('<div class="section">💡 Key Business Insights</div>', unsafe_allow_html=True)

    best_category = category_sales.iloc[0]["Category"]
    best_state = state_sales.iloc[0]["State"]
    best_product = top_products.iloc[0]["Sub_Category"]

    delivered_pct = filtered["Order_Status"].eq("Delivered").mean() * 100
    cancelled_pct = filtered["Order_Status"].eq("Cancelled").mean() * 100
    avg_order_value = total_sales / total_orders if total_orders else 0

    insights = [
        ("🏆 Leading Category", f"{best_category} has the highest sales."),
        ("📍 Leading State", f"{best_state} is the strongest state by sales."),
        ("⭐ Top Product Segment", f"{best_product} is the top-selling product segment."),
        ("🚚 Delivery Performance", f"{delivered_pct:.1f}% of orders are delivered."),
        ("💰 Average Order Value", f"Average order value is ₹{avg_order_value:,.0f}."),
        ("📉 Cancellation Rate", f"{cancelled_pct:.1f}% of orders are cancelled.")
    ]

    left, right = st.columns(2)

    for i, (title, message) in enumerate(insights):
        target = left if i % 2 == 0 else right
        with target:
            st.markdown(
                f"""
                <div class="insight">
                    <b>{title}</b><br>
                    <span>{message}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown('<div class="section">📋 Management Summary</div>', unsafe_allow_html=True)

    st.success(
        f"During the selected period, the business generated ₹{total_sales:,.0f} "
        f"in sales and ₹{total_profit:,.0f} in profit from {total_orders:,} orders. "
        f"The overall profit margin is {profit_margin:.2f}%."
    )

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
    Indian E-Commerce Business Analytics • Python • Pandas • Plotly • Streamlit
</div>
""", unsafe_allow_html=True)
