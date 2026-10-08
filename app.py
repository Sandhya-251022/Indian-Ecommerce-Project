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
# PROFESSIONAL CSS
# =========================================================

st.markdown("""
<style>

/* =====================================================
   MAIN PAGE
===================================================== */

.stApp {
    background-color: #F5F7FB;
}

.block-container {
    padding-top: 1.3rem;
    padding-bottom: 0.8rem;
    max-width: 1500px;
}


/* =====================================================
   SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {
    background-color: #14213D;
}

/* Only text elements - DO NOT style every sidebar element */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: white !important;
}

/* Sidebar header */

.sidebar-title {
    color: white;
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 15px;
}

/* Sidebar filter spacing */

section[data-testid="stSidebar"] .stMultiSelect {
    margin-bottom: 5px;
}

section[data-testid="stSidebar"] .stDateInput {
    margin-top: 3px;
    margin-bottom: 5px;
}


/* =====================================================
   MAIN TITLE
===================================================== */

.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #14213D;
    margin-bottom: 2px;
    line-height: 1.2;
}

.subtitle {
    font-size: 15px;
    color: #64748B;
    margin-bottom: 14px;
}


/* =====================================================
   SECTION TITLE
===================================================== */

.section-title {
    font-size: 20px;
    font-weight: 750;
    color: #14213D;
    margin-top: 12px;
    margin-bottom: 7px;
}


/* =====================================================
   KPI CARDS
===================================================== */

.kpi-card {
    background: #FFFFFF;
    padding: 14px 17px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.06);
    min-height: 100px;
}

.kpi-icon {
    font-size: 22px;
    margin-bottom: 2px;
}

.kpi-title {
    font-size: 11px;
    font-weight: 700;
    color: #64748B;
    margin-bottom: 4px;
    letter-spacing: 0.4px;
}

.kpi-value {
    font-size: 22px;
    font-weight: 800;
    color: #14213D;
}


/* =====================================================
   CHART SPACING
===================================================== */

div[data-testid="stPlotlyChart"] {
    margin-top: -4px;
    margin-bottom: -7px;
}


/* =====================================================
   DATAFRAME
===================================================== */

[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #E2E8F0;
}


/* =====================================================
   INSIGHT CARDS
===================================================== */

.insight-card {
    background: #FFFFFF;
    padding: 13px;
    border-radius: 10px;
    border-left: 4px solid #2563EB;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    min-height: 72px;
}

.insight-title {
    font-size: 11px;
    color: #64748B;
    font-weight: 700;
}

.insight-value {
    font-size: 16px;
    color: #14213D;
    font-weight: 750;
    margin-top: 4px;
}


/* =====================================================
   FOOTER
===================================================== */

.footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    padding: 8px;
}


/* =====================================================
   DIVIDER
===================================================== */

hr {
    margin-top: 8px;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    data = pd.read_csv(
        Path(__file__).parent /
        "Indian_Ecommerce_Sales_Analysis_Dataset.csv"
    )

    data["Order_Date"] = pd.to_datetime(
        data["Order_Date"],
        errors="coerce"
    )

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
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    '<div class="sidebar-title">🔎 Dashboard Filters</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown("---")


# -----------------------------
# STATE
# -----------------------------

selected_states = st.sidebar.multiselect(
    "📍 State",
    options=sorted(df["State"].dropna().unique()),
    default=sorted(df["State"].dropna().unique())
)


# -----------------------------
# CATEGORY
# -----------------------------

selected_categories = st.sidebar.multiselect(
    "🛍️ Category",
    options=sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)


# -----------------------------
# ORDER STATUS
# -----------------------------

selected_statuses = st.sidebar.multiselect(
    "📦 Order Status",
    options=sorted(df["Order_Status"].dropna().unique()),
    default=sorted(df["Order_Status"].dropna().unique())
)


# -----------------------------
# DATE
# -----------------------------

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "📅 Order Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    format="DD/MM/YYYY"
)

if isinstance(date_range, tuple) and len(date_range) == 2:

    start_date = date_range[0]
    end_date = date_range[1]

else:

    start_date = min_date
    end_date = max_date


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
    if total_orders > 0
    else 0
)

profit_margin = (
    total_profit / total_sales * 100
    if total_sales > 0
    else 0
)


# =========================================================
# BUSINESS OVERVIEW
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


# =========================================================
# PROFESSIONAL COLOR PALETTE
# =========================================================

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
    .groupby(
        filtered["Order_Date"].dt.to_period("M")
    )["Sales_INR"]
    .sum()
    .reset_index()
)

monthly["Month"] = (
    monthly["Order_Date"]
    .dt.strftime("%b %Y")
)


fig_month = px.line(
    monthly,
    x="Month",
    y="Sales_INR",
    markers=True,
    title="📈 Monthly Sales Trend"
)

fig_month.update_traces(
    line=dict(
        color="#2563EB",
        width=3
    ),
    marker=dict(
        size=8
    )
)

fig_month.update_layout(
    template="plotly_white",
    title_font=dict(
        size=18,
        color="#14213D"
    ),
    xaxis_title="Month",
    yaxis_title="Sales (₹)",
    hovermode="x unified",
    margin=dict(
        l=20,
        r=20,
        t=55,
        b=20
    )
)


# =========================================================
# CATEGORY SALES
# =========================================================

category_sales = (
    filtered
    .groupby(
        "Category",
        as_index=False
    )["Sales_INR"]
    .sum()
    .sort_values(
        "Sales_INR",
        ascending=False
    )
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
    template="plotly_white",
    title_font=dict(
        size=18,
        color="#14213D"
    ),
    showlegend=False,
    margin=dict(
        l=20,
        r=20,
        t=55,
        b=20
    )
)


# =========================================================
# SALES CHARTS
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
    .sort_values(
        "Sales_INR",
        ascending=False
    )
)


fig_state = px.bar(
    state_sales.head(10),
    x="Sales_INR",
    y="State",
    orientation="h",
    title="🏆 Top 10 States by Sales",
    text_auto=".2s"
)

fig_state.update_traces(
    marker_color="#2563EB"
)

fig_state.update_layout(
    template="plotly_white",
    title_font=dict(
        size=18,
        color="#14213D"
    ),
    yaxis={
        "categoryorder": "total ascending"
    },
    margin=dict(
        l=20,
        r=20,
        t=55,
        b=20
    )
)


# =========================================================
# CATEGORY PROFIT
# =========================================================

category_profit = (
    filtered
    .groupby(
        "Category",
        as_index=False
    )["Profit_INR"]
    .sum()
    .sort_values(
        "Profit_INR",
        ascending=False
    )
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
    template="plotly_white",
    title_font=dict(
        size=18,
        color="#14213D"
    ),
    showlegend=False,
    margin=dict(
        l=20,
        r=20,
        t=55,
        b=20
    )
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
# PAYMENT MODE
# =========================================================

payment = (
    filtered["Payment_Mode"]
    .value_counts()
    .reset_index()
)

payment.columns = [
    "Payment_Mode",
    "Count"
]


payment_fig = px.pie(
    payment,
    names="Payment_Mode",
    values="Count",
    hole=0.5,
    title="💳 Payment Method Distribution",
    color_discrete_sequence=professional_colors
)

payment_fig.update_layout(
    template="plotly_white",
    title_font=dict(
        size=18,
        color="#14213D"
    ),
    margin=dict(
        l=20,
        r=20,
        t=55,
        b=20
    )
)


# =========================================================
# ORDER STATUS
# =========================================================

status = (
    filtered["Order_Status"]
    .value_counts()
    .reset_index()
)

status.columns = [
    "Order_Status",
    "Count"
]


status_fig = px.pie(
    status,
    names="Order_Status",
    values="Count",
    hole=0.5,
    title="📦 Order Status Distribution",
    color_discrete_sequence=professional_colors
)

status_fig.update_layout(
    template="plotly_white",
    title_font=dict(
        size=18,
        color="#14213D"
    ),
    margin=dict(
        l=20,
        r=20,
        t=55,
        b=20
    )
)


# =========================================================
# PAYMENT + STATUS
# =========================================================

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
    template="plotly_white",
    title_font=dict(
        size=18,
        color="#14213D"
    ),
    margin=dict(
        l=20,
        r=20,
        t=55,
        b=20
    )
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# =========================================================
# TOP 10 PRODUCTS
# =========================================================

top_products = (
    filtered
    .groupby(
        "Sub_Category",
        as_index=False
    )
    .agg(
        Sales_INR=("Sales_INR", "sum"),
        Profit_INR=("Profit_INR", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values(
        "Sales_INR",
        ascending=False
    )
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
        filtered["Order_Status"]
        .eq("Delivered")
        .mean()
    ) * 100

    cancelled_pct = (
        filtered["Order_Status"]
        .eq("Cancelled")
        .mean()
    ) * 100


    # -----------------------------------------------------
    # INSIGHT CARDS
    # -----------------------------------------------------

    a, b, c, d = st.columns(4)


    with a:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    TOP CATEGORY
                </div>
                <div class="insight-value">
                    🛍️ {best_category}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with b:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    TOP STATE
                </div>
                <div class="insight-value">
                    📍 {best_state}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    TOP PRODUCT
                </div>
                <div class="insight-value">
                    ⭐ {best_product}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with d:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    DELIVERED ORDERS
                </div>
                <div class="insight-value">
                    📦 {delivered_pct:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # DETAILED INSIGHTS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.info(
            f"💰 **Total Sales:** ₹{total_sales:,.0f}\n\n"
            f"📈 **Total Profit:** ₹{total_profit:,.0f}\n\n"
            f"🧾 **Average Order Value:** ₹{avg_order_value:,.0f}"
        )


    with col2:

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
        Python • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_h=True
)
