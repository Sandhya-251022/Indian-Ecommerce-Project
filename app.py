import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Indian E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PROFESSIONAL CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ---------- Main Background ---------- */

.stApp {
    background-color: #F5F7FB;
}

/* ---------- Main Content ---------- */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* ---------- Title ---------- */

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #14213D;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 16px;
    color: #64748B;
    margin-bottom: 25px;
}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"] {
    background-color: #14213D;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {
    background-color: #1F3154;
    border-radius: 8px;
}

section[data-testid="stSidebar"] input {
    color: #14213D !important;
}

/* ---------- KPI Cards ---------- */

.kpi-card {
    background: white;
    padding: 20px 22px;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.06);
    min-height: 125px;
}

.kpi-title {
    font-size: 14px;
    font-weight: 600;
    color: #64748B;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 27px;
    font-weight: 800;
    color: #14213D;
}

.kpi-icon {
    font-size: 25px;
    margin-bottom: 5px;
}

/* ---------- Section Headers ---------- */

.section-title {
    font-size: 22px;
    font-weight: 750;
    color: #14213D;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* ---------- Insight Cards ---------- */

.insight-card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border-left: 5px solid #2563EB;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
    min-height: 90px;
}

.insight-title {
    font-size: 13px;
    color: #64748B;
    font-weight: 600;
}

.insight-value {
    font-size: 18px;
    color: #14213D;
    font-weight: 750;
    margin-top: 5px;
}

/* ---------- Footer ---------- */

.footer {
    text-align: center;
    color: #64748B;
    font-size: 13px;
    padding: 20px;
}

/* ---------- Dataframe ---------- */

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #E2E8F0;
}

/* ---------- Buttons ---------- */

.stButton > button {
    border-radius: 8px;
    border: none;
    background-color: #2563EB;
    color: white;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    data = pd.read_csv(
        Path(__file__).parent / "Indian_Ecommerce_Sales_Analysis_Dataset.csv"
    )

    data["Order_Date"] = pd.to_datetime(data["Order_Date"])

    return data


df = load_data()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🛒 Indian E-Commerce Sales Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive analysis of sales, profit, products, customers and regional performance'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.markdown(
    "## 🔎 Dashboard Filters"
)

st.sidebar.markdown("---")

selected_states = st.sidebar.multiselect(
    "📍 State",
    sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

selected_categories = st.sidebar.multiselect(
    "🛍️ Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

selected_statuses = st.sidebar.multiselect(
    "📦 Order Status",
    sorted(df["Order_Status"].unique()),
    default=sorted(df["Order_Status"].unique())
)

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "📅 Order Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

start_date, end_date = (
    date_range
    if isinstance(date_range, tuple) and len(date_range) == 2
    else (min_date, max_date)
)


# =========================================================
# FILTER DATA
# =========================================================

filtered = df[
    df["State"].isin(selected_states)
    & df["Category"].isin(selected_categories)
    & df["Order_Status"].isin(selected_statuses)
    & (df["Order_Date"].dt.date >= start_date)
    & (df["Order_Date"].dt.date <= end_date)
].copy()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered["Sales_INR"].sum()
total_profit = filtered["Profit_INR"].sum()
total_orders = filtered["Order_ID"].nunique()
total_quantity = filtered["Quantity"].sum()

avg_order_value = (
    total_sales / total_orders
    if total_orders
    else 0
)

profit_margin = (
    total_profit / total_sales * 100
    if total_sales
    else 0
)


# =========================================================
# KPI CARDS
# =========================================================

st.markdown(
    '<div class="section-title">📊 Business Overview</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-title">TOTAL SALES</div>
            <div class="kpi-value">₹{total_sales:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">📈</div>
            <div class="kpi-title">TOTAL PROFIT</div>
            <div class="kpi-value">₹{total_profit:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🧾</div>
            <div class="kpi-title">TOTAL ORDERS</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">📦</div>
            <div class="kpi-title">QUANTITY SOLD</div>
            <div class="kpi-value">{total_quantity:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🎯</div>
            <div class="kpi-title">PROFIT MARGIN</div>
            <div class="kpi-value">{profit_margin:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# COMMON PLOTLY DESIGN
# =========================================================

plot_template = "plotly_white"

professional_colors = [
    "#2563EB",
    "#14B8A6",
    "#F59E0B",
    "#8B5CF6",
    "#EF4444",
    "#06B6D4",
    "#84CC16",
    "#F97316"
]


# =========================================================
# MONTHLY SALES
# =========================================================

monthly = (
    filtered
    .groupby(filtered["Order_Date"].dt.to_period("M"))["Sales_INR"]
    .sum()
    .reset_index()
)

monthly["Month"] = monthly["Order_Date"].dt.strftime("%b %Y")

fig_month = px.line(
    monthly,
    x="Month",
    y="Sales_INR",
    markers=True,
    title="📈 Monthly Sales Trend"
)

fig_month.update_traces(
    line=dict(width=3),
    marker=dict(size=8)
)

fig_month.update_layout(
    template=plot_template,
    title_font=dict(size=18, color="#14213D"),
    xaxis_title="Month",
    yaxis_title="Sales (₹)",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=60, b=20)
)


# =========================================================
# CATEGORY SALES
# =========================================================

category_sales = (
    filtered
    .groupby("Category", as_index=False)["Sales_INR"]
    .sum()
    .sort_values("Sales_INR", ascending=False)
)

fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales_INR",
    title="🛍️ Sales by Category",
    text_auto=".2s",
    color="Category",
    color_discrete_sequence=professional_colors
)

fig_category.update_layout(
    template=plot_template,
    title_font=dict(size=18, color="#14213D"),
    showlegend=False,
    margin=dict(l=20, r=20, t=60, b=20)
)


# =========================================================
# SALES TREND + CATEGORY
# =========================================================

left, right = st.columns(2)

with left:
    st.plotly_chart(
        fig_month,
        use_container_width=True
    )

with right:
    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# =========================================================
# STATE SALES
# =========================================================

state_sales = (
    filtered
    .groupby("State", as_index=False)
    .agg(
        Sales_INR=("Sales_INR", "sum"),
        Profit_INR=("Profit_INR", "sum")
    )
    .sort_values("Sales_INR", ascending=False)
)

fig_state = px.bar(
    state_sales.head(10),
    x="Sales_INR",
    y="State",
    orientation="h",
    title="🏆 Top 10 States by Sales",
    text_auto=".2s"
)

fig_state.update_layout(
    template=plot_template,
    title_font=dict(size=18, color="#14213D"),
    yaxis={"categoryorder": "total ascending"},
    margin=dict(l=20, r=20, t=60, b=20)
)


# =========================================================
# CATEGORY PROFIT
# =========================================================

category_profit = (
    filtered
    .groupby("Category", as_index=False)["Profit_INR"]
    .sum()
    .sort_values("Profit_INR", ascending=False)
)

fig_profit = px.bar(
    category_profit,
    x="Category",
    y="Profit_INR",
    title="💰 Profit by Category",
    text_auto=".2s",
    color="Category",
    color_discrete_sequence=professional_colors
)

fig_profit.update_layout(
    template=plot_template,
    title_font=dict(size=18, color="#14213D"),
    showlegend=False,
    margin=dict(l=20, r=20, t=60, b=20)
)


# =========================================================
# STATE + PROFIT
# =========================================================

left, right = st.columns(2)

with left:
    st.plotly_chart(
        fig_state,
        use_container_width=True
    )

with right:
    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )


# =========================================================
# PAYMENT & STATUS
# =========================================================

payment = filtered["Payment_Mode"].value_counts().reset_index()
payment.columns = ["Payment_Mode", "Count"]

status = filtered["Order_Status"].value_counts().reset_index()
status.columns = ["Order_Status", "Count"]


payment_fig = px.pie(
    payment,
    names="Payment_Mode",
    values="Count",
    hole=0.5,
    title="💳 Payment Method Distribution",
    color_discrete_sequence=professional_colors
)

payment_fig.update_layout(
    template=plot_template,
    title_font=dict(size=18, color="#14213D"),
    margin=dict(l=20, r=20, t=60, b=20)
)


status_fig = px.pie(
    status,
    names="Order_Status",
    values="Count",
    hole=0.5,
    title="📦 Order Status Distribution",
    color_discrete_sequence=professional_colors
)

status_fig.update_layout(
    template=plot_template,
    title_font=dict(size=18, color="#14213D"),
    margin=dict(l=20, r=20, t=60, b=20)
)


left, right = st.columns(2)

with left:
    st.plotly_chart(
        payment_fig,
        use_container_width=True
    )

with right:
    st.plotly_chart(
        status_fig,
        use_container_width=True
    )


# =========================================================
# QUANTITY VS SALES
# =========================================================

fig_scatter = px.scatter(
    filtered,
    x="Quantity",
    y="Sales_INR",
    color="Category",
    hover_data=[
        "Sub_Category",
        "State",
        "Order_Status"
    ],
    title="📊 Quantity vs Sales",
    color_discrete_sequence=professional_colors
)

fig_scatter.update_layout(
    template=plot_template,
    title_font=dict(size=18, color="#14213D"),
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# =========================================================
# TOP PRODUCTS
# =========================================================

top_products = (
    filtered
    .groupby("Sub_Category", as_index=False)
    .agg(
        Sales_INR=("Sales_INR", "sum"),
        Profit_INR=("Profit_INR", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values("Sales_INR", ascending=False)
    .head(10)
)

st.markdown(
    '<div class="section-title">⭐ Top 10 Products</div>',
    unsafe_allow_html=True
)

st.dataframe(
    top_products,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# KEY INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">💡 Key Business Insights</div>',
    unsafe_allow_html=True
)

if not filtered.empty:

    best_category = category_sales.iloc[0]["Category"]
    best_state = state_sales.iloc[0]["State"]
    best_product = top_products.iloc[0]["Sub_Category"]

    delivered_pct = (
        filtered["Order_Status"].eq("Delivered").mean()
    ) * 100

    cancelled_pct = (
        filtered["Order_Status"].eq("Cancelled").mean()
    ) * 100

    a, b, c, d = st.columns(4)

    with a:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">TOP CATEGORY</div>
                <div class="insight-value">🛍️ {best_category}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with b:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">TOP STATE</div>
                <div class="insight-value">📍 {best_state}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">TOP PRODUCT</div>
                <div class="insight-value">⭐ {best_product}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with d:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">DELIVERED ORDERS</div>
                <div class="insight-value">📦 {delivered_pct:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:

        st.info(
            f"💰 **Total Sales:** ₹{total_sales:,.0f}\n\n"
            f"📈 **Total Profit:** ₹{total_profit:,.0f}\n\n"
            f"🧾 **Average Order Value:** ₹{avg_order_value:,.0f}"
        )

    with insight_col2:

        st.info(
            f"🎯 **Overall Profit Margin:** {profit_margin:.2f}%\n\n"
            f"📦 **Delivered Orders:** {delivered_pct:.1f}%\n\n"
            f"❌ **Cancelled Orders:** {cancelled_pct:.1f}%"
        )

else:

    st.warning(
        "⚠️ No records match the selected filters."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        🛒 <b>Indian E-Commerce Sales & Profit Analysis</b>
        <br>
        Built with Python • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
