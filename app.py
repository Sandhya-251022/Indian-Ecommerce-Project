import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Indian E-Commerce Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PROFESSIONAL PURPLE THEME
# ============================================================

st.markdown("""
<style>

    /* Main page */
    .stApp {
        background: #F7F5FC;
        color: #241B35;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #24113F 0%, #35165C 50%, #472078 100%);
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] label {
        font-weight: 600 !important;
    }

    /* Sidebar date input */
    section[data-testid="stSidebar"] input {
        background-color: #FFFFFF !important;
        color: #241B35 !important;
        border-radius: 10px !important;
        border: 1px solid #D8B4FE !important;
        font-weight: 600 !important;
    }

    /* Sidebar select boxes */
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #241B35 !important;
    }

    /* Header */
    .dashboard-header {
        background: linear-gradient(
            135deg,
            #32145F 0%,
            #5B21B6 50%,
            #7C3AED 100%
        );
        padding: 35px 40px;
        border-radius: 0 0 25px 25px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(91, 33, 182, 0.25);
    }

    .dashboard-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .dashboard-subtitle {
        font-size: 16px;
        color: #E9D5FF;
    }

    /* KPI Cards */
    .kpi-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #E9D5FF;
        box-shadow: 0 5px 18px rgba(76, 29, 149, 0.10);
        min-height: 135px;
        transition: 0.2s;
    }

    .kpi-card:hover {
        box-shadow: 0 8px 25px rgba(76, 29, 149, 0.18);
    }

    .kpi-title {
        color: #6B5B7A;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    .kpi-value {
        color: #32145F;
        font-size: 28px;
        font-weight: 800;
        margin-top: 8px;
    }

    .kpi-description {
        color: #8B7D99;
        font-size: 12px;
        margin-top: 5px;
    }

    /* Section headings */
    .section-title {
        color: #32145F;
        font-size: 24px;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Dataset period box */
    .dataset-period {
        background: linear-gradient(
            135deg,
            #EDE9FE,
            #DDD6FE
        );
        color: #4C1D95 !important;
        padding: 14px 16px;
        border-radius: 12px;
        margin-top: 12px;
        border: 1px solid #C4B5FD;
        font-size: 13px;
        line-height: 1.6;
    }

    .dataset-period b {
        color: #32145F !important;
    }

    /* Insight box */
    .insight-box {
        background: white;
        border-left: 5px solid #7C3AED;
        padding: 18px;
        margin: 10px 0;
        border-radius: 10px;
        box-shadow: 0 3px 12px rgba(76, 29, 149, 0.08);
        color: #33263D;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: #EDE9FE;
        padding: 8px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #4C1D95;
        font-weight: 700;
        border-radius: 8px;
        padding: 10px 18px;
    }

    .stTabs [aria-selected="true"] {
        background: #7C3AED !important;
        color: white !important;
    }

    /* Buttons */
    .stButton > button {
        background: #7C3AED;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: 700;
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

</style>
""", unsafe_allow_html=True)



# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    file_path = (
        Path(__file__).parent
        / "Indian_Ecommerce_Sales_Analysis_Dataset.csv"
    )

    data = pd.read_csv(file_path)

    data["Order_Date"] = pd.to_datetime(
        data["Order_Date"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["Order_Date"]
    ).copy()

    return data


df = load_data()


# =========================================================
# DATASET DATE RANGE
# =========================================================

dataset_start = df["Order_Date"].min().date()
dataset_end = df["Order_Date"].max().date()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    "## 🛒 E-Commerce Dashboard"
)

st.sidebar.caption(
    "Filter the business data to explore performance."
)

st.sidebar.markdown("---")


# =========================================================
# STATE
# =========================================================

states = sorted(
    df["State"].dropna().unique()
)

selected_states = st.sidebar.multiselect(
    "📍 State",
    options=states,
    default=states
)


# =========================================================
# CATEGORY
# =========================================================

categories = sorted(
    df["Category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "🛍️ Category",
    options=categories,
    default=categories
)


# =========================================================
# ORDER STATUS
# =========================================================

statuses = sorted(
    df["Order_Status"].dropna().unique()
)

selected_statuses = st.sidebar.multiselect(
    "🚚 Order Status",
    options=statuses,
    default=statuses
)


# =========================================================
# DATE RANGE
# =========================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### 📅 Date Range"
)

# START DATE
start_date = st.sidebar.date_input(
    "Start date",
    value=dataset_start,
    min_value=dataset_start,
    max_value=dataset_end,
    format="DD/MM/YYYY"
)

# END DATE
end_date = st.sidebar.date_input(
    "End date",
    value=dataset_end,
    min_value=dataset_start,
    max_value=dataset_end,
    format="DD/MM/YYYY"
)


# =========================================================
# DATE VALIDATION
# =========================================================

if start_date > end_date:

    st.sidebar.error(
        "Start date must be before End date."
    )

    st.stop()


# =========================================================
# SHOW DATASET PERIOD
# =========================================================

st.sidebar.markdown(
    f"""
    <div style="
        background:#e5f5f2;
        border-radius:9px;
        padding:10px;
        margin-top:8px;
        color:#164e52;
        font-size:0.78rem;
        line-height:1.5;
    ">
        <b>📊 Dataset Available</b><br>
        {dataset_start.strftime("%d %B %Y")}
        <br>
        to
        <br>
        {dataset_end.strftime("%d %B %Y")}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FILTER DATA
# =========================================================

filtered = df[
    df["State"].isin(selected_states)
    &
    df["Category"].isin(selected_categories)
    &
    df["Order_Status"].isin(selected_statuses)
    &
    (df["Order_Date"].dt.date >= start_date)
    &
    (df["Order_Date"].dt.date <= end_date)
].copy()


# =========================================================
# EMPTY DATA
# =========================================================

if filtered.empty:

    st.warning(
        "⚠️ No records match the selected filters. "
        "Please change the filters."
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero-box">

        <div class="hero-title">
            🛒 Indian E-Commerce Business Dashboard
        </div>

        <div class="hero-subtitle">
            Interactive analysis of sales, profitability,
            orders, products and regional performance
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SELECTED PERIOD
# =========================================================

st.markdown(
    f"""
    <div class="period-box">

        <div class="period-title">
            📅 SELECTED ANALYSIS PERIOD
        </div>

        <div class="period-value">
            {start_date.strftime("%d %B %Y")}
            &nbsp; → &nbsp;
            {end_date.strftime("%d %B %Y")}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered["Sales_INR"].sum()

total_profit = filtered["Profit_INR"].sum()

total_orders = filtered["Order_ID"].nunique()

total_quantity = filtered["Quantity"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

avg_order_value = (
    total_sales / total_orders
    if total_orders != 0
    else 0
)


# =========================================================
# KPI CARDS
# =========================================================

kpi_cols = st.columns(5)

kpis = [
    (
        "Total Sales",
        f"₹{total_sales:,.0f}",
        "Revenue generated"
    ),

    (
        "Total Profit",
        f"₹{total_profit:,.0f}",
        "Net profit"
    ),

    (
        "Total Orders",
        f"{total_orders:,}",
        "Unique orders"
    ),

    (
        "Quantity Sold",
        f"{total_quantity:,}",
        "Units sold"
    ),

    (
        "Profit Margin",
        f"{profit_margin:.2f}%",
        "Profit / Sales"
    )
]

for col, (label, value, note) in zip(
    kpi_cols,
    kpis
):

    with col:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    {label}
                </div>

                <div class="kpi-value">
                    {value}
                </div>

                <div class="kpi-note">
                    {note}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# PREPARE DATA
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


state_sales = (
    filtered
    .groupby(
        "State",
        as_index=False
    )
    .agg(
        Sales_INR=("Sales_INR", "sum"),
        Profit_INR=("Profit_INR", "sum")
    )
    .sort_values(
        "Sales_INR",
        ascending=False
    )
)


payment = (
    filtered["Payment_Mode"]
    .value_counts()
    .reset_index()
)

payment.columns = [
    "Payment_Mode",
    "Count"
]


status = (
    filtered["Order_Status"]
    .value_counts()
    .reset_index()
)

status.columns = [
    "Order_Status",
    "Count"
]


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


# =========================================================
# CHART STYLE
# =========================================================

def chart_style(fig, height=330):

    fig.update_layout(

        height=height,

        template="plotly_white",

        paper_bgcolor="white",

        plot_bgcolor="white",

        font=dict(
            family="Arial",
            color="#35575a"
        ),

        margin=dict(
            l=40,
            r=20,
            t=55,
            b=40
        ),

        title_font=dict(
            size=16,
            color="#17383b"
        ),

        hoverlabel=dict(
            bgcolor="white",
            font_size=12
        )
    )

    fig.update_xaxes(
        showgrid=False
    )

    fig.update_yaxes(
        gridcolor="#e5eeee"
    )

    return fig


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Executive Overview",
        "📦 Products & Orders",
        "💡 Business Insights"
    ]
)


# =========================================================
# TAB 1
# =========================================================

with tab1:

    st.markdown(
        '<div class="section-title">'
        '📈 Sales & Profit Performance'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # ROW 1
    # -----------------------------------------------------

    c1, c2 = st.columns(2)

    # MONTHLY SALES

    with c1:

        fig = px.line(
            monthly,
            x="Month",
            y="Sales_INR",
            markers=True,
            title="Monthly Sales Trend"
        )

        fig.update_traces(
            line=dict(
                color="#159a91",
                width=3
            ),
            marker=dict(
                size=8
            )
        )

        st.plotly_chart(
            chart_style(fig),
            use_container_width=True
        )

    # CATEGORY SALES

    with c2:

        fig = px.bar(
            category_sales,
            x="Category",
            y="Sales_INR",
            text_auto=".2s",
            title="Sales by Category"
        )

        fig.update_traces(
            marker_color="#20a39e",
            textposition="outside"
        )

        st.plotly_chart(
            chart_style(fig),
            use_container_width=True
        )

    # -----------------------------------------------------
    # ROW 2
    # -----------------------------------------------------

    c1, c2 = st.columns(2)

    # TOP STATES

    with c1:

        fig = px.bar(
            state_sales.head(10),
            x="Sales_INR",
            y="State",
            orientation="h",
            text_auto=".2s",
            title="Top 10 States by Sales"
        )

        fig.update_traces(
            marker_color="#4776c8"
        )

        fig.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            }
        )

        st.plotly_chart(
            chart_style(fig),
            use_container_width=True
        )

    # CATEGORY PROFIT

    with c2:

        fig = px.bar(
            category_profit,
            x="Category",
            y="Profit_INR",
            text_auto=".2s",
            title="Profit by Category"
        )

        fig.update_traces(
            marker_color="#e3a72f",
            textposition="outside"
        )

        st.plotly_chart(
            chart_style(fig),
            use_container_width=True
        )


# =========================================================
# TAB 2
# =========================================================

with tab2:

    st.markdown(
        '<div class="section-title">'
        '📦 Product & Order Behaviour'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # PAYMENT + STATUS
    # -----------------------------------------------------

    c1, c2 = st.columns(2)

    # PAYMENT

    with c1:

        fig = px.pie(
            payment,
            names="Payment_Mode",
            values="Count",
            hole=0.55,
            title="Payment Method Distribution"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            chart_style(fig),
            use_container_width=True
        )

    # ORDER STATUS

    with c2:

        fig = px.pie(
            status,
            names="Order_Status",
            values="Count",
            hole=0.55,
            title="Order Status Distribution"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            chart_style(fig),
            use_container_width=True
        )

    # -----------------------------------------------------
    # QUANTITY VS SALES
    # -----------------------------------------------------

    fig = px.scatter(
        filtered,
        x="Quantity",
        y="Sales_INR",
        color="Category",
        hover_data=[
            "Sub_Category",
            "State",
            "Order_Status"
        ],
        title="Quantity vs Sales"
    )

    fig.update_traces(
        marker_size=8,
        opacity=0.75
    )

    st.plotly_chart(
        chart_style(fig, 380),
        use_container_width=True
    )

    # -----------------------------------------------------
    # TOP PRODUCTS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🏆 Top 10 Product Segments'
        '</div>',
        unsafe_allow_html=True
    )

    display_products = top_products.copy()

    display_products["Sales_INR"] = (
        display_products["Sales_INR"]
        .map(lambda x: f"₹{x:,.0f}")
    )

    display_products["Profit_INR"] = (
        display_products["Profit_INR"]
        .map(lambda x: f"₹{x:,.0f}")
    )

    st.dataframe(
        display_products,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 3
# =========================================================

with tab3:

    st.markdown(
        '<div class="section-title">'
        '💡 Key Business Insights'
        '</div>',
        unsafe_allow_html=True
    )

    best_category = (
        category_sales.iloc[0]["Category"]
    )

    best_state = (
        state_sales.iloc[0]["State"]
    )

    best_product = (
        top_products.iloc[0]["Sub_Category"]
    )

    delivered_pct = (
        filtered["Order_Status"]
        .eq("Delivered")
        .mean()
        * 100
    )

    cancelled_pct = (
        filtered["Order_Status"]
        .eq("Cancelled")
        .mean()
        * 100
    )


    insights = [

        (
            "🏆 Leading Category",
            f"{best_category} has the highest sales."
        ),

        (
            "📍 Leading State",
            f"{best_state} is the strongest state by sales."
        ),

        (
            "⭐ Top Product Segment",
            f"{best_product} is the top-selling product segment."
        ),

        (
            "🚚 Delivery Performance",
            f"{delivered_pct:.1f}% of orders are delivered."
        ),

        (
            "💰 Average Order Value",
            f"Average order value is ₹{avg_order_value:,.0f}."
        ),

        (
            "📉 Cancellation Rate",
            f"{cancelled_pct:.1f}% of orders are cancelled."
        )
    ]


    left, right = st.columns(2)


    for i, (title, message) in enumerate(insights):

        target = (
            left
            if i % 2 == 0
            else right
        )

        with target:

            st.markdown(
                f"""
                <div class="insight-card">

                    <div class="insight-title">
                        {title}
                    </div>

                    <div class="insight-text">
                        {message}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # -----------------------------------------------------
    # MANAGEMENT SUMMARY
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📋 Management Summary'
        '</div>',
        unsafe_allow_html=True
    )

    st.success(
        f"""
        During the selected period, the business generated
        ₹{total_sales:,.0f} in sales and
        ₹{total_profit:,.0f} in profit from
        {total_orders:,} orders.

        The overall profit margin is
        {profit_margin:.2f}%.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Indian E-Commerce Business Analytics
        • Python • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
