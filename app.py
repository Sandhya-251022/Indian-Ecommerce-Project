import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Indian E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

/* =====================================================
   MAIN DASHBOARD BACKGROUND
   ===================================================== */

       st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(
        135deg,
        #071A2B 0%,
        #0B2D4D 45%,
        #123E63 100%
    ) !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        135deg,
        #071A2B 0%,
        #0B2D4D 45%,
        #123E63 100%
    ) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}


/* =====================================================
   MAIN CONTENT
   ===================================================== */

.main {
    background: transparent !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}


/* =====================================================
   TITLE
   ===================================================== */

h1 {
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 42px !important;
}

h2, h3 {
    color: #FFFFFF !important;
}

.stCaption {
    color: #D5E5F5 !important;
}


/* =====================================================
   NORMAL TEXT
   ===================================================== */

.stMarkdown,
.stText,
p,
label {
    color: #EAF4FF;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #061522 0%,
        #0A2740 50%,
        #0D3557 100%
    ) !important;
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #FFFFFF !important;
}


/* =====================================================
   SIDEBAR SELECT BOXES
   ===================================================== */

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #F1F6FA !important;
    color: #111111 !important;
    border-radius: 8px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #111111 !important;
}


/* =====================================================
   DATE INPUT
   ===================================================== */

section[data-testid="stSidebar"] div[data-baseweb="input"] {
    background-color: #F1F6FA !important;
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="input"] input {
    color: #111111 !important;
    background-color: #F1F6FA !important;
}

section[data-testid="stSidebar"] div[data-baseweb="input"] input::placeholder {
    color: #555555 !important;
}

section[data-testid="stSidebar"] div[data-baseweb="input"] svg {
    fill: #222222 !important;
}


/* =====================================================
   KPI CARDS - LIGHT BLUE
   ===================================================== */

div[data-testid="metric-container"] {
    background: #EAF3F8 !important;
    border-radius: 16px !important;
    padding: 18px !important;
    border: 1px solid #C8DCE8 !important;
    box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.25) !important;
}

div[data-testid="metric-container"] label {
    color: #234E70 !important;
    font-weight: 600 !important;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0B2D4D !important;
    font-weight: 700 !important;
}

div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #234E70 !important;
}


/* =====================================================
   CHART CARDS - LIGHT BLUE
   ===================================================== */

div[data-testid="stPlotlyChart"] {
    background: #EAF3F8 !important;
    border-radius: 18px !important;
    padding: 10px !important;
    box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.25) !important;
    border: 1px solid #C8DCE8 !important;
}


/* =====================================================
   DATAFRAME - LIGHT BLUE
   ===================================================== */

div[data-testid="stDataFrame"] {
    background: #EAF3F8 !important;
    border-radius: 15px !important;
    padding: 8px !important;
    box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.25) !important;
    border: 1px solid #C8DCE8 !important;
}


/* =====================================================
   INFO BOXES
   ===================================================== */

div[data-testid="stAlert"] {
    border-radius: 12px !important;
}


/* =====================================================
   DIVIDER
   ===================================================== */

hr {
    border-color: rgba(255, 255, 255, 0.25) !important;
}


/* =====================================================
   BUTTONS
   ===================================================== */

button {
    border-radius: 8px !important;
}


/* =====================================================
   FOOTER
   ===================================================== */

footer {
    visibility: hidden;
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
# TITLE
# =========================================================

st.title("🛒 Indian E-Commerce Sales & Profit Dashboard")

st.caption(
    "Interactive analysis of sales, profit, products, customers and regional performance"
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Dashboard Filters")

selected_states = st.sidebar.multiselect(
    "State",
    sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

selected_categories = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

selected_statuses = st.sidebar.multiselect(
    "Order Status",
    sorted(df["Order_Status"].unique()),
    default=sorted(df["Order_Status"].unique())
)


min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date",
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

avg_order_value = total_sales / total_orders if total_orders else 0

profit_margin = (
    total_profit / total_sales * 100
    if total_sales
    else 0
)


# =========================================================
# KPI CARDS
# =========================================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Sales",
    f"₹{total_sales:,.0f}"
)

c2.metric(
    "Total Profit",
    f"₹{total_profit:,.0f}"
)

c3.metric(
    "Total Orders",
    f"{total_orders:,}"
)

c4.metric(
    "Quantity Sold",
    f"{total_quantity:,}"
)

c5.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)


st.divider()


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
    text_auto=".2s"
)


# =========================================================
# FIRST CHART ROW
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
    yaxis={"categoryorder": "total ascending"}
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
    text_auto=".2s"
)


# =========================================================
# SECOND CHART ROW
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

payment = filtered["Payment_Mode"].value_counts().reset_index()

payment.columns = [
    "Payment_Mode",
    "Count"
]


# =========================================================
# ORDER STATUS
# =========================================================

status = filtered["Order_Status"].value_counts().reset_index()

status.columns = [
    "Order_Status",
    "Count"
]


# =========================================================
# PIE CHARTS
# =========================================================

left, right = st.columns(2)

with left:

    st.plotly_chart(
        px.pie(
            payment,
            names="Payment_Mode",
            values="Count",
            hole=0.45,
            title="💳 Payment Method Distribution"
        ),
        use_container_width=True
    )

with right:

    st.plotly_chart(
        px.pie(
            status,
            names="Order_Status",
            values="Count",
            hole=0.45,
            title="📦 Order Status Distribution"
        ),
        use_container_width=True
    )


# =========================================================
# QUANTITY VS SALES
# =========================================================

st.plotly_chart(
    px.scatter(
        filtered,
        x="Quantity",
        y="Sales_INR",
        color="Category",
        hover_data=[
            "Sub_Category",
            "State",
            "Order_Status"
        ],
        title="📊 Quantity vs Sales"
    ),
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
    .sort_values(
        "Sales_INR",
        ascending=False
    )
    .head(10)
)


st.subheader("⭐ Top 10 Products")

st.dataframe(
    top_products,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# KEY INSIGHTS
# =========================================================

st.subheader("💡 Key Insights")

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


    a, b, c, d = st.columns(4)

    a.info(
        f"Top category: {best_category}"
    )

    b.info(
        f"Top state: {best_state}"
    )

    c.info(
        f"Top product: {best_product}"
    )

    d.info(
        f"Delivered orders: {delivered_pct:.1f}%"
    )


    st.write(
        f"- Total sales: ₹{total_sales:,.0f}"
    )

    st.write(
        f"- Total profit: ₹{total_profit:,.0f}"
    )

    st.write(
        f"- Average order value: ₹{avg_order_value:,.0f}"
    )

    st.write(
        f"- Overall profit margin: {profit_margin:.2f}%"
    )

    st.write(
        f"- Cancelled orders: {cancelled_pct:.1f}%"
    )

else:

    st.warning(
        "No records match the selected filters."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Indian E-Commerce Sales & Profit Analysis | Python + Pandas + Plotly + Streamlit"
)
