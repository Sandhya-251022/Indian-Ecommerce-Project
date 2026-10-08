import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Indian E-Commerce Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PROFESSIONAL THEME
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       MAIN PAGE
       ========================= */

    .stApp {
        background: whitesmoke;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background: navy;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: gray;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: lightgray !important;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] {
        background: darkslategray;
        border: 1px solid gray;
        border-radius: 10px;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] span {
        color: white !important;
    }

    section[data-testid="stSidebar"]
    input {
        background: darkslategray !important;
        color: white !important;
        border: 1px solid gray !important;
        border-radius: 8px;
    }


    /* =========================
       HEADER
       ========================= */

    .dashboard-header {
        background: linear-gradient(
            135deg,
            navy 0%,
            darkblue 50%,
            indigo 100%
        );

        padding: 32px 36px;
        border-radius: 22px;
        margin-bottom: 25px;

        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.18);
    }

    .dashboard-header h1 {
        color: white;
        font-size: 2.35rem;
        margin: 0;
        font-weight: 800;
    }

    .dashboard-header p {
        color: lightblue;
        margin: 9px 0 0 0;
        font-size: 1rem;
    }

    .dashboard-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.10);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: lightblue;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        margin-bottom: 12px;
        font-weight: 600;
    }


    /* =========================
       SECTION TITLES
       ========================= */

    .section-title {
        color: navy;
        font-size: 1.25rem;
        font-weight: 800;
        margin: 28px 0 14px 0;
    }

    .section-subtitle {
        color: dimgray;
        font-size: 0.88rem;
        margin-top: -8px;
        margin-bottom: 15px;
    }


    /* =========================
       KPI CARDS
       ========================= */

    .kpi-card {
        background: white;
        border-radius: 18px;

        padding: 20px 21px;

        border: 1px solid lightgray;

        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.07);

        min-height: 125px;
    }

    .kpi-card::after {
        content: "";
        display: block;

        width: 100%;
        height: 4px;

        margin-top: 12px;

        background: linear-gradient(
            90deg,
            blue,
            cyan
        );

        border-radius: 5px;
    }

    .kpi-label {
        color: dimgray;
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .kpi-value {
        color: navy;
        font-size: 1.7rem;
        font-weight: 800;
        margin-top: 8px;
    }

    .kpi-note {
        color: gray;
        font-size: 0.76rem;
        margin-top: 4px;
    }


    /* =========================
       INSIGHT CARDS
       ========================= */

    .insight-card {
        background: white;

        border: 1px solid lightgray;
        border-left: 5px solid blue;

        border-radius: 14px;

        padding: 17px 18px;
        margin-bottom: 12px;

        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
    }

    .insight-title {
        color: navy;
        font-weight: 700;
        margin-bottom: 5px;
        font-size: 0.95rem;
    }

    .insight-text {
        color: dimgray;
        font-size: 0.88rem;
        line-height: 1.5;
    }


    /* =========================
       MANAGEMENT SUMMARY
       ========================= */

    .summary-box {
        background: aliceblue;

        border: 1px solid lightblue;
        border-radius: 16px;

        padding: 20px 22px;

        color: navy;

        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
    }


    /* =========================
       TABS
       ========================= */

    button[data-baseweb="tab"] {
        font-weight: 700;
        font-size: 0.92rem;
        color: dimgray;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: blue !important;
    }

    div[data-baseweb="tab-highlight"] {
        background-color: blue !important;
    }


    /* =========================
       DATAFRAME
       ========================= */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid lightgray;

        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.05);
    }


    /* =========================
       FOOTER
       ========================= */

    .footer {
        text-align: center;
        color: gray;

        font-size: 0.78rem;

        padding: 30px 0 8px 0;

        border-top: 1px solid lightgray;

        margin-top: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


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
# HEADER
# =========================================================

st.markdown(
    """
    <div class="dashboard-header">

        <div class="dashboard-badge">
            BUSINESS INTELLIGENCE • DATA ANALYTICS
        </div>

        <h1>
            🛍️ Indian E-Commerce Analytics
        </h1>

        <p>
            Interactive analysis of sales, profit,
            customer orders and regional performance
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    "## 🎛️ Dashboard Controls"
)

st.sidebar.caption(
    "Use the filters below to explore the dataset."
)

st.sidebar.markdown("---")


states = sorted(
    df["State"]
    .dropna()
    .unique()
    .tolist()
)

categories = sorted(
    df["Category"]
    .dropna()
    .unique()
    .tolist()
)

statuses = sorted(
    df["Order_Status"]
    .dropna()
    .unique()
    .tolist()
)


selected_states = st.sidebar.multiselect(
    "📍 State",
    states,
    default=states,
    help="Select one or more states."
)


selected_categories = st.sidebar.multiselect(
    "📦 Category",
    categories,
    default=categories,
    help="Select one or more product categories."
)


selected_statuses = st.sidebar.multiselect(
    "🚚 Order Status",
    statuses,
    default=statuses,
    help="Select order status."
)


min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()


date_range = st.sidebar.date_input(
    "📅 Order Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


if isinstance(date_range, (tuple, list)) and len(date_range) == 2:

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
# EMPTY DATA CHECK
# =========================================================

if filtered.empty:

    st.warning(
        "No records match the selected filters. "
        "Please broaden your filters."
    )

    st.stop()


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

delivered_pct = (
    filtered["Order_Status"]
    .eq("Delivered")
    .mean() * 100
)


# =========================================================
# KPI SECTION
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📈 Key Performance Indicators'
    '</div>',
    unsafe_allow_html=True
)


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


for col, (label, value, note) in zip(kpi_cols, kpis):

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


st.markdown("<br>", unsafe_allow_html=True)


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
# PLOTLY FORMATTING FUNCTION
# =========================================================

def polish(fig, height=360):

    fig.update_layout(
        height=height,
        template="plotly_white",

        font=dict(
            family="Arial",
            color="dimgray"
        ),

        margin=dict(
            l=40,
            r=25,
            t=60,
            b=40
        ),

        title_font=dict(
            size=17,
            color="navy"
        ),

        title_x=0.02,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.update_xaxes(
        showgrid=False
    )

    fig.update_yaxes(
        gridcolor="lightgray",
        zeroline=False
    )

    return fig


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Overview",
        "📦 Products & Orders",
        "💡 Business Insights"
    ]
)


# =========================================================
# TAB 1 - OVERVIEW
# =========================================================

with tab1:

    st.markdown(
        '<div class="section-title">'
        'Performance Overview'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Monitor revenue, category performance and regional sales.'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # -----------------------------------------------------
    # MONTHLY SALES
    # -----------------------------------------------------

    with col1:

        fig_month = px.line(
            monthly,
            x="Month",
            y="Sales_INR",
            markers=True,
            title="Monthly Sales Trend"
        )

        fig_month.update_traces(
            line=dict(
                color="blue",
                width=3
            ),
            marker=dict(
                size=8
            )
        )

        st.plotly_chart(
            polish(fig_month),
            use_container_width=True
        )


    # -----------------------------------------------------
    # CATEGORY SALES
    # -----------------------------------------------------

    with col2:

        fig_category = px.bar(
            category_sales,
            x="Category",
            y="Sales_INR",
            text_auto=".2s",
            title="Sales by Category",
            color_discrete_sequence=["blue"]
        )

        fig_category.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            polish(fig_category),
            use_container_width=True
        )


    col1, col2 = st.columns(2)


    # -----------------------------------------------------
    # STATE SALES
    # -----------------------------------------------------

    with col1:

        fig_state = px.bar(
            state_sales.head(10),
            x="Sales_INR",
            y="State",
            orientation="h",
            text_auto=".2s",
            title="Top 10 States by Sales",
            color_discrete_sequence=["teal"]
        )

        fig_state.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            }
        )

        st.plotly_chart(
            polish(fig_state),
            use_container_width=True
        )


    # -----------------------------------------------------
    # CATEGORY PROFIT
    # -----------------------------------------------------

    with col2:

        fig_profit = px.bar(
            category_profit,
            x="Category",
            y="Profit_INR",
            text_auto=".2s",
            title="Profit by Category",
            color_discrete_sequence=["green"]
        )

        fig_profit.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            polish(fig_profit),
            use_container_width=True
        )


# =========================================================
# TAB 2 - PRODUCTS & ORDERS
# =========================================================

with tab2:

    st.markdown(
        '<div class="section-title">'
        'Products & Order Behaviour'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Understand payment preferences, order status '
        'and product-level performance.'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # -----------------------------------------------------
    # PAYMENT METHOD
    # -----------------------------------------------------

    with col1:

        fig_payment = px.pie(
            payment,
            names="Payment_Mode",
            values="Count",
            hole=0.58,
            title="Payment Method Distribution"
        )

        fig_payment.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            polish(fig_payment),
            use_container_width=True
        )


    # -----------------------------------------------------
    # ORDER STATUS
    # -----------------------------------------------------

    with col2:

        fig_status = px.pie(
            status,
            names="Order_Status",
            values="Count",
            hole=0.58,
            title="Order Status Distribution"
        )

        fig_status.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            polish(fig_status),
            use_container_width=True
        )


    # -----------------------------------------------------
    # QUANTITY VS SALES
    # -----------------------------------------------------

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
        title="Quantity vs Sales"
    )

    fig_scatter.update_traces(
        marker=dict(
            size=9,
            opacity=0.72
        )
    )

    st.plotly_chart(
        polish(
            fig_scatter,
            height=420
        ),
        use_container_width=True
    )


    # -----------------------------------------------------
    # TOP PRODUCTS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Top 10 Product Segments'
        '</div>',
        unsafe_allow_html=True
    )


    display_products = top_products.copy()


    display_products["Sales_INR"] = (
        display_products["Sales_INR"]
        .map(
            lambda x: f"₹{x:,.0f}"
        )
    )


    display_products["Profit_INR"] = (
        display_products["Profit_INR"]
        .map(
            lambda x: f"₹{x:,.0f}"
        )
    )


    st.dataframe(
        display_products,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 3 - BUSINESS INSIGHTS
# =====================================
