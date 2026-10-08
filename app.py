import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Indian E-Commerce Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# PROFESSIONAL THEME
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Main page */
    .stApp {
        background: #f5f7fb;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: #f9fafb !important;
    }

    section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {
        background: #1f2937;
    }

    /* Header */
    .dashboard-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
        padding: 28px 32px;
        border-radius: 18px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
    }

    .dashboard-header h1 {
        color: white;
        font-size: 2.15rem;
        margin: 0;
        font-weight: 750;
    }

    .dashboard-header p {
        color: #dbeafe;
        margin: 8px 0 0 0;
        font-size: 1rem;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 18px 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
        min-height: 115px;
    }

    .kpi-label {
        color: #64748b;
        font-size: 0.82rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .kpi-value {
        color: #0f172a;
        font-size: 1.75rem;
        font-weight: 750;
        margin-top: 7px;
    }

    .kpi-note {
        color: #64748b;
        font-size: 0.78rem;
        margin-top: 4px;
    }

    /* Section titles */
    .section-title {
        color: #0f172a;
        font-size: 1.2rem;
        font-weight: 750;
        margin: 24px 0 10px 0;
    }

    /* Insight cards */
    .insight-card {
        background: white;
        border-left: 4px solid #2563eb;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
    }

    .insight-title {
        color: #0f172a;
        font-weight: 700;
        margin-bottom: 3px;
    }

    .insight-text {
        color: #475569;
        font-size: 0.9rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.8rem;
        padding: 25px 0 5px 0;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-weight: 650;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "Indian_Ecommerce_Sales_Analysis_Dataset.csv"
    data = pd.read_csv(file_path)
    data["Order_Date"] = pd.to_datetime(data["Order_Date"], errors="coerce")
    return data.dropna(subset=["Order_Date"]).copy()

df = load_data()

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown("""
<div class="dashboard-header">
    <h1>🛍️ Indian E-Commerce Analytics</h1>
    <p>Sales, profit, customer orders and regional performance — interactive business intelligence dashboard</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.markdown("## 🎛️ Dashboard Controls")
st.sidebar.caption("Use the filters below to explore the dataset.")

states = sorted(df["State"].dropna().unique().tolist())
categories = sorted(df["Category"].dropna().unique().tolist())
statuses = sorted(df["Order_Status"].dropna().unique().tolist())

selected_states = st.sidebar.multiselect(
    "State",
    states,
    default=states,
    help="Select one or more states."
)

selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories,
    help="Select one or more product categories."
)

selected_statuses = st.sidebar.multiselect(
    "Order Status",
    statuses,
    default=statuses,
    help="Filter by delivery/order status."
)

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# ---------------------------------------------------------
# FILTER DATA
# ---------------------------------------------------------
filtered = df[
    df["State"].isin(selected_states)
    & df["Category"].isin(selected_categories)
    & df["Order_Status"].isin(selected_statuses)
    & (df["Order_Date"].dt.date >= start_date)
    & (df["Order_Date"].dt.date <= end_date)
].copy()

# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------
total_sales = filtered["Sales_INR"].sum()
total_profit = filtered["Profit_INR"].sum()
total_orders = filtered["Order_ID"].nunique()
total_quantity = filtered["Quantity"].sum()
avg_order_value = total_sales / total_orders if total_orders else 0
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

delivered_pct = filtered["Order_Status"].eq("Delivered").mean() * 100 if len(filtered) else 0

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
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
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

if filtered.empty:
    st.warning("No records match the selected filters. Please broaden your filters.")
    st.stop()

# ---------------------------------------------------------
# PREPARE DATA
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# PLOTLY THEME
# ---------------------------------------------------------
plot_bg = "rgba(0,0,0,0)"
paper_bg = "rgba(0,0,0,0)"

def polish(fig, height=360):
    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(family="Arial", color="#334155"),
        margin=dict(l=35, r=20, t=55, b=35),
        title_font=dict(size=17, color="#0f172a"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#e2e8f0")
    return fig

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📦 Products & Orders", "💡 Business Insights"])

with tab1:
    st.markdown('<div class="section-title">Performance Overview</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_month = px.line(
            monthly,
            x="Month",
            y="Sales_INR",
            markers=True,
            title="Monthly Sales Trend"
        )
        fig_month.update_traces(line_width=3, marker_size=8)
        st.plotly_chart(polish(fig_month), use_container_width=True)

    with col2:
        fig_category = px.bar(
            category_sales,
            x="Category",
            y="Sales_INR",
            text_auto=".2s",
            title="Sales by Category"
        )
        fig_category.update_traces(textposition="outside")
        st.plotly_chart(polish(fig_category), use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_state = px.bar(
            state_sales.head(10),
            x="Sales_INR",
            y="State",
            orientation="h",
            text_auto=".2s",
            title="Top 10 States by Sales"
        )
        fig_state.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(polish(fig_state), use_container_width=True)

    with col2:
        fig_profit = px.bar(
            category_profit,
            x="Category",
            y="Profit_INR",
            text_auto=".2s",
            title="Profit by Category"
        )
        fig_profit.update_traces(textposition="outside")
        st.plotly_chart(polish(fig_profit), use_container_width=True)

with tab2:
    st.markdown('<div class="section-title">Products & Order Behaviour</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_payment = px.pie(
            payment,
            names="Payment_Mode",
            values="Count",
            hole=0.58,
            title="Payment Method Distribution"
        )
        fig_payment.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(polish(fig_payment), use_container_width=True)

    with col2:
        fig_status = px.pie(
            status,
            names="Order_Status",
            values="Count",
            hole=0.58,
            title="Order Status Distribution"
        )
        fig_status.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(polish(fig_status), use_container_width=True)

    fig_scatter = px.scatter(
        filtered,
        x="Quantity",
        y="Sales_INR",
        color="Category",
        hover_data=["Sub_Category", "State", "Order_Status"],
        title="Quantity vs Sales"
    )
    fig_scatter.update_traces(marker=dict(size=9, opacity=0.72))
    st.plotly_chart(polish(fig_scatter, height=400), use_container_width=True)

    st.markdown('<div class="section-title">Top 10 Product Segments</div>', unsafe_allow_html=True)
    display_products = top_products.copy()
    display_products["Sales_INR"] = display_products["Sales_INR"].map(lambda x: f"₹{x:,.0f}")
    display_products["Profit_INR"] = display_products["Profit_INR"].map(lambda x: f"₹{x:,.0f}")
    st.dataframe(
        display_products,
        use_container_width=True,
        hide_index=True
    )

with tab3:
    st.markdown('<div class="section-title">Key Business Insights</div>', unsafe_allow_html=True)

    best_category = category_sales.iloc[0]["Category"]
    best_state = state_sales.iloc[0]["State"]
    best_product = top_products.iloc[0]["Sub_Category"]
    cancelled_pct = filtered["Order_Status"].eq("Cancelled").mean() * 100

    insight_cols = st.columns(2)

    insights = [
        ("🏆 Leading Category", f"{best_category} generates the highest sales in the selected data."),
        ("📍 Leading State", f"{best_state} is the strongest state by sales."),
        ("⭐ Top Product Segment", f"{best_product} is the highest-selling product segment."),
        ("🚚 Delivery Performance", f"{delivered_pct:.1f}% of filtered orders are delivered."),
        ("💰 Average Order Value", f"The average order value is ₹{avg_order_value:,.0f}."),
        ("📉 Cancellation Rate", f"{cancelled_pct:.1f}% of filtered orders are cancelled.")
    ]

    for i, (title, text_value) in enumerate(insights):
        with insight_cols[i % 2]:
            st.markdown(
                f"""
                <div class="insight-card">
                    <div class="insight-title">{title}</div>
                    <div class="insight-text">{text_value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-title">Management Summary</div>', unsafe_allow_html=True)
    st.info(
        f"Sales of ₹{total_sales:,.0f} generated profit of ₹{total_profit:,.0f}, "
        f"with a profit margin of {profit_margin:.2f}%. "
        f"The analysis covers {total_orders:,} orders and {total_quantity:,} units."
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        Indian E-Commerce Sales & Profit Analysis • Python • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
