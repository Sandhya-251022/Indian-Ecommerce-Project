import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Indian E-Commerce Business Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM PROFESSIONAL DESIGN
# =========================================================

st.markdown("""
<style>

/* =========================================================
   MAIN PAGE
========================================================= */

.stApp {
    background: #f3f7f6;
}

.block-container {
    max-width: 1500px;
    padding: 1.2rem 2rem 1.5rem 2rem;
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #102a2e 0%,
        #164e52 100%
    );
}

/* Sidebar headings */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

/* Sidebar labels */

section[data-testid="stSidebar"] label {
    color: #f4fffd !important;
    font-weight: 600 !important;
}

/* Sidebar normal text */

section[data-testid="stSidebar"] p {
    color: #d7efec !important;
}

/* =========================================================
   MULTISELECT
========================================================= */

section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}

/* Selected values inside multiselect */

section[data-testid="stSidebar"]
div[data-baseweb="select"]
div[data-baseweb="tag"] {
    background-color: #e05f59 !important;
    border-radius: 7px !important;
}

section[data-testid="stSidebar"]
div[data-baseweb="select"]
div[data-baseweb="tag"] span {
    color: #ffffff !important;
}

/* Multiselect input text */

section[data-testid="stSidebar"]
div[data-baseweb="select"]
input {
    color: #17383b !important;
    -webkit-text-fill-color: #17383b !important;
}

/* Dropdown text */

section[data-testid="stSidebar"]
div[role="listbox"] {
    background-color: #ffffff !important;
}

section[data-testid="stSidebar"]
div[role="option"] {
    color: #17383b !important;
}


/* =========================================================
   DATE INPUT
========================================================= */

/* Date input box */

section[data-testid="stSidebar"]
div[data-testid="stDateInput"]
div[data-baseweb="input"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #d5e3e1 !important;
}

/* Date text */

section[data-testid="stSidebar"]
div[data-testid="stDateInput"]
input {
    background-color: #ffffff !important;
    color: #17383b !important;
    -webkit-text-fill-color: #17383b !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

/* Date placeholder */

section[data-testid="stSidebar"]
div[data-testid="stDateInput"]
input::placeholder {
    color: #607779 !important;
    -webkit-text-fill-color: #607779 !important;
    opacity: 1 !important;
}

/* Calendar icon */

section[data-testid="stSidebar"]
div[data-testid="stDateInput"]
svg {
    color: #17383b !important;
    fill: #17383b !important;
}

/* Date input button */

section[data-testid="stSidebar"]
div[data-testid="stDateInput"]
button {
    color: #17383b !important;
}


/* =========================================================
   DATE CALENDAR POPUP
========================================================= */

div[data-baseweb="calendar"] {
    background-color: #ffffff !important;
}

div[data-baseweb="calendar"] * {
    color: #17383b;
}

div[data-baseweb="calendar"] button {
    color: #17383b !important;
}


/* =========================================================
   DATE RANGE HEADING
========================================================= */

.date-heading {
    color: #ffffff !important;
    font-size: 1.05rem;
    font-weight: 800;
    margin-top: 14px;
    margin-bottom: 8px;
}


/* =========================================================
   DATASET PERIOD BOX
========================================================= */

.dataset-period {
    background: #e8f7f4;
    color: #164e52;
    padding: 10px 12px;
    border-radius: 10px;
    margin-top: 8px;
    font-size: 0.80rem;
    line-height: 1.5;
}


/* =========================================================
   HERO HEADER
========================================================= */

.hero {
    background: linear-gradient(
        115deg,
        #0f3d3e 0%,
        #147d78 58%,
        #20a39e 100%
    );

    border-radius: 22px;

    padding: 28px 32px;

    margin-bottom: 16px;

    box-shadow:
        0 12px 30px
        rgba(15, 61, 62, 0.20);
}

.hero h1 {
    color: white;

    margin: 0;

    font-size: 2.2rem;

    font-weight: 800;
}

.hero p {
    color: #d9fffa;

    margin: 7px 0 0;

    font-size: 1rem;
}


/* =========================================================
   INFORMATION STRIP
========================================================= */

.info-strip {
    background: #e6f5f2;

    border: 1px solid #b9dfd9;

    color: #174e4d;

    border-radius: 12px;

    padding: 10px 15px;

    margin-bottom: 16px;

    font-size: 0.88rem;
}


/* =========================================================
   KPI CARDS
========================================================= */

.kpi {
    background: #ffffff;

    border-radius: 16px;

    padding: 17px 19px;

    border: 1px solid #dce9e7;

    border-top: 5px solid #159a91;

    box-shadow:
        0 7px 22px
        rgba(22, 78, 82, 0.08);

    min-height: 115px;
}

.kpi-label {
    color: #607779;

    font-size: 0.74rem;

    font-weight: 750;

    letter-spacing: 0.06em;

    text-transform: uppercase;
}

.kpi-value {
    color: #17383b;

    font-size: 1.55rem;

    font-weight: 800;

    margin-top: 7px;
}

.kpi-note {
    color: #7b8f91;

    font-size: 0.76rem;

    margin-top: 3px;
}


/* =========================================================
   SECTION TITLES
========================================================= */

.section {
    color: #17383b;

    font-size: 1.18rem;

    font-weight: 800;

    margin: 18px 0 8px;
}


/* =========================================================
   CHARTS
========================================================= */

div[data-testid="stPlotlyChart"] {
    margin-top: -4px;
    margin-bottom: -5px;
}


/* =========================================================
   INSIGHT CARDS
========================================================= */

.insight {
    background: #ffffff;

    border-radius: 14px;

    border-left: 5px solid #159a91;

    padding: 14px 16px;

    margin-bottom: 10px;

    box-shadow:
        0 5px 16px
        rgba(22, 78, 82, 0.06);
}

.insight b {
    color: #17383b;
}

.insight span {
    color: #607779;

    font-size: 0.88rem;
}


/* =========================================================
   DATAFRAME
========================================================= */

[data-testid="stDataFrame"] {
    border-radius: 12px;

    overflow: hidden;

    border: 1px solid #dce9e7;
}


/* =========================================================
   FOOTER
========================================================= */

.footer {
    text-align: center;

    color: #789092;

    padding: 20px 0 4px;

    font-size: 0.78rem;
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
# STATE FILTER
# =========================================================

states = sorted(
    df["State"]
    .dropna()
    .unique()
)

selected_states = st.sidebar.multiselect(
    "📍 State",
    options=states,
    default=states
)


# =========================================================
# CATEGORY FILTER
# =========================================================

categories = sorted(
    df["Category"]
    .dropna()
    .unique()
)

selected_categories = st.sidebar.multiselect(
    "🛍️ Category",
    options=categories,
    default=categories
)


# =========================================================
# ORDER STATUS FILTER
# =========================================================

statuses = sorted(
    df["Order_Status"]
    .dropna()
    .unique()
)

selected_statuses = st.sidebar.multiselect(
    "🚚 Order Status",
    options=statuses,
    default=statuses
)


# =========================================================
# DATE RANGE
# =========================================================

st.sidebar.markdown(
    '<div class="date-heading">📅 Date Range</div>',
    unsafe_allow_html=True
)


# START DATE

start_date = st.sidebar.date_input(
    "Start date",

    value=dataset_start,

    min_value=dataset_start,

    max_value=dataset_end,

    format="DD/MM/YYYY",

    key="start_date"
)


# END DATE

end_date = st.sidebar.date_input(
    "End date",

    value=dataset_end,

    min_value=dataset_start,

    max_value=dataset_end,

    format="DD/MM/YYYY",

    key="end_date"
)


# =========================================================
# VALIDATE DATES
# =========================================================

if start_date > end_date:

    st.sidebar.error(
        "Start date must be before End date."
    )

    st.stop()


# =========================================================
# SHOW DATASET DATE RANGE
# =========================================================

st.sidebar.markdown(
    f"""
    <div class="dataset-period">
        <b>📊 Dataset Period</b><br>
        {dataset_start.strftime("%d %B %Y")}
        →
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

    & df["Category"].isin(selected_categories)

    & df["Order_Status"].isin(selected_statuses)

    & (
        df["Order_Date"].dt.date
        >= start_date
    )

    & (
        df["Order_Date"].dt.date
        <= end_date
    )
].copy()


# =========================================================
# EMPTY DATA CHECK
# =========================================================

if filtered.empty:

    st.warning(
        "⚠️ No records match the selected filters. "
        "Please broaden the filters."
    )

    st.stop()


# =========================================================
# HERO HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">

        <h1>
            🛒 Indian E-Commerce Business Dashboard
        </h1>

        <p>
            Interactive analysis of sales, profitability,
            orders, products and regional performance
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SELECTED DATE INFORMATION
# =========================================================

st.markdown(
    f"""
    <div class="info-strip">

        📅 <b>Selected Period:</b>
        {start_date.strftime("%d %B %Y")}
        →
        {end_date.strftime("%d %B %Y")}

        &nbsp;&nbsp; | &nbsp;&nbsp;

        📊 <b>Records Analysed:</b>
        {len(filtered):,}

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
    if total_sales
    else 0
)

avg_order_value = (
    total_sales / total_orders
    if total_orders
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
            <div class="kpi">

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
# PREPARE CHART DATA
# =========================================================

monthly = (
    filtered
    .groupby(
        filtered["Order_Date"]
        .dt.to_period("M")
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
# CHART STYLE FUNCTION
# =========================================================

def chart_style(
    fig,
    height=350
):

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
            l=35,
            r=20,
            t=60,
            b=40
        ),

        title_font=dict(
            size=17,
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
        gridcolor="#e4eeee"
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
# TAB 1 - EXECUTIVE OVERVIEW
# =========================================================

with tab1:

    st.markdown(
        '<div class="section">'
        '📈 Sales & Profit Performance'
        '</div>',
        unsafe_allow_html=True
    )


    c1, c2 = st.columns(2)


    # -----------------------------------------------------
    # MONTHLY SALES
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # CATEGORY SALES
    # -----------------------------------------------------

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


    c1, c2 = st.columns(2)


    # -----------------------------------------------------
    # TOP STATES
    # -----------------------------------------------------

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
                "categoryorder":
                "total ascending"
            }
        )

        st.plotly_chart(
            chart_style(fig),
            use_container_width=True
        )


    # -----------------------------------------------------
    # CATEGORY PROFIT
    # -----------------------------------------------------

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
# TAB 2 - PRODUCTS & ORDERS
# =========================================================
with tab2:

    st.markdown(
        '<div class="section">'
        '📦 Product & Order Behaviour'
        '</div>',
        unsafe_allow_html=True
    )


    c1, c2 = st.columns(2)


    # -----------------------------------------------------
    # PAYMENT
    # -----------------------------------------------------

    with c1:

        fig = px.pie(
            payment,

            names="Payment_Mode",

            values="Count",

            hole=0.58,

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


    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    with c2:

        fig = px.pie(
            status,

            names="Order_Status",

            values="Count",

            hole=0.58,

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
        marker_size=9,

        opacity=0.72
    )

    st.plotly_chart(
        chart_style(
            fig,
            390
        ),
        use_container_width=True
    )


    # -----------------------------------------------------
    # TOP PRODUCTS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section">'
        '🏆 Top 10 Product Segments'
        '</div>',
        unsafe_allow_html=True
    )


    table = top_products.copy()


    table["Sales_INR"] = table[
        "Sales_INR"
    ].map(
        lambda x: f"₹{x:,.0f}"
    )


    table["Profit_INR"] = table[
        "Profit_INR"
    ].map(
        lambda x: f"₹{x:,.0f}"
    )


    st.dataframe(
        table,

        use_container_width=True,

        hide_index=True
    )

# =========================================================
# TAB 3 - BUSINESS INSIGHTS
# =========================================================

with tab3:

    st.markdown(
        '<div class="section">'
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

            f"{best_category} has "
            "the highest sales."
        ),

        (
            "📍 Leading State",

            f"{best_state} is "
            "the strongest state by sales."
        ),

        (
            "⭐ Top Product Segment",

            f"{best_product} is "
            "the top-selling product segment."
        ),

        (
            "🚚 Delivery Performance",

            f"{delivered_pct:.1f}% "
            "of orders are delivered."
        ),

        (
            "💰 Average Order Value",

            f"Average order value is "
            f"₹{avg_order_value:,.0f}."
        ),

        (
            "📉 Cancellation Rate",

            f"{cancelled_pct:.1f}% "
            "of orders are cancelled."
        )
    ]


    left, right = st.columns(2)


    for i, (title, message) in enumerate(
        insights
    ):

        target = (
            left
            if i % 2 == 0
            else right
        )


        with target:

            st.markdown(
                f"""
                <div class="insight">

                    <b>{title}</b>

                    <br>

                    <span>{message}</span>

                </div>
                """,
                unsafe_allow_html=True
            )


    # -----------------------------------------------------
    # MANAGEMENT SUMMARY
    # -----------------------------------------------------

    st.markdown(
        '<div class="section">'
        '📋 Management Summary'
        '</div>',
        unsafe_allow_html=True
    )


    st.success(
        f"During the selected period, the business generated "
        f"₹{total_sales:,.0f} in sales and "
        f"₹{total_profit:,.0f} in profit from "
        f"{total_orders:,} orders. "
        f"The overall profit margin is "
        f"{profit_margin:.2f}%."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        🛒 <b>Indian E-Commerce Business Analytics</b>

        <br>

        Python • Pandas • Plotly • Streamlit

    </div>
    """,
    unsafe_allow_html=True
)
