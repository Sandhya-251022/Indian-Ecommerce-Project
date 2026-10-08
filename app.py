import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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


# ============================================================
# LOAD DATASET
# ============================================================

DATA_FILE = Path(__file__).parent / "Indian_Ecommerce_Sales_Analysis_Dataset.csv"

try:
    df = pd.read_csv(DATA_FILE)
except Exception as e:
    st.error("Unable to load the dataset.")
    st.write(e)
    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

df = df.dropna(subset=["Order_Date"])

dataset_start = df["Order_Date"].min().date()
dataset_end = df["Order_Date"].max().date()

# Numeric columns
numeric_columns = [
    "Quantity",
    "Unit_Price_INR",
    "Discount_Percent",
    "Sales_INR",
    "Profit_INR",
    "Profit_Margin_Percent"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
df["Month_Number"] = df["Order_Date"].dt.month


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:25px;
        font-weight:800;
        margin-bottom:5px;">
        📊 Dashboard Controls
    </div>

    <div style="
        color:#E9D5FF;
        font-size:13px;
        margin-bottom:25px;">
        Use the filters below to explore the dataset.
    </div>
    """,
    unsafe_allow_html=True
)


# State filter
st.sidebar.markdown("### 📍 State")

states = sorted(df["State"].dropna().unique())

selected_states = st.sidebar.multiselect(
    "Select State",
    states,
    default=states,
    label_visibility="collapsed"
)


# Category filter
st.sidebar.markdown("### 🛍️ Category")

categories = sorted(df["Category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories,
    label_visibility="collapsed"
)


# Order status filter
st.sidebar.markdown("### 📦 Order Status")

statuses = sorted(df["Order_Status"].dropna().unique())

selected_status = st.sidebar.multiselect(
    "Select Order Status",
    statuses,
    default=statuses,
    label_visibility="collapsed"
)


# ============================================================
# DATE RANGE
# ============================================================

st.sidebar.markdown("### 📅 Date Range")

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


# Purple dataset period box
st.sidebar.markdown(
    f"""
    <div class="dataset-period">
        <b>📅 Dataset Period</b><br>
        <span style="color:#5B21B6;">
        {dataset_start.strftime("%d %B %Y")}
        →
        {dataset_end.strftime("%d %B %Y")}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    (df["State"].isin(selected_states)) &
    (df["Category"].isin(selected_categories)) &
    (df["Order_Status"].isin(selected_status)) &
    (df["Order_Date"].dt.date >= start_date) &
    (df["Order_Date"].dt.date <= end_date)
].copy()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="dashboard-header">

        <div class="dashboard-title">
            🛍️ Indian E-Commerce Analytics
        </div>

        <div class="dashboard-subtitle">
            Interactive business intelligence dashboard for
            sales, profit, orders and regional performance
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["Sales_INR"].sum()
total_profit = filtered_df["Profit_INR"].sum()
total_orders = filtered_df["Order_ID"].nunique()
quantity_sold = filtered_df["Quantity"].sum()

if total_sales > 0:
    profit_margin = (total_profit / total_sales) * 100
else:
    profit_margin = 0


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Sales</div>
            <div class="kpi-value">₹{total_sales:,.0f}</div>
            <div class="kpi-description">Revenue generated</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Profit</div>
            <div class="kpi-value">₹{total_profit:,.0f}</div>
            <div class="kpi-description">Net profit</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-description">Unique orders</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Quantity Sold</div>
            <div class="kpi-value">{quantity_sold:,}</div>
            <div class="kpi-description">Units sold</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Profit Margin</div>
            <div class="kpi-value">{profit_margin:.2f}%</div>
            <div class="kpi-description">Profit / sales</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Overview",
        "📦 Products & Orders",
        "💡 Business Insights"
    ]
)


# ============================================================
# TAB 1 - OVERVIEW
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-title">Performance Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # ---------------- Monthly Sales ----------------

    with col1:

        monthly_sales = (
            filtered_df
            .groupby(["Month_Number", "Month_Name"], as_index=False)
            ["Sales_INR"]
            .sum()
            .sort_values("Month_Number")
        )

        fig_month = px.line(
            monthly_sales,
            x="Month_Name",
            y="Sales_INR",
            markers=True,
            title="Monthly Sales Trend"
        )

        fig_month.update_traces(
            line=dict(color="#7C3AED", width=4),
            marker=dict(size=9)
        )

        fig_month.update_layout(
            template="plotly_white",
            height=400,
            xaxis_title="Month",
            yaxis_title="Sales (INR)",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_month,
            use_container_width=True
        )


    # ---------------- Sales by Category ----------------

    with col2:

        category_sales = (
            filtered_df
            .groupby("Category", as_index=False)
            ["Sales_INR"]
            .sum()
            .sort_values("Sales_INR", ascending=False)
        )

        fig_category = px.bar(
            category_sales,
            x="Category",
            y="Sales_INR",
            title="Sales by Category",
            text_auto=".2s"
        )

        fig_category.update_traces(
            marker_color="#8B5CF6"
        )

        fig_category.update_layout(
            template="plotly_white",
            height=400,
            xaxis_title="Category",
            yaxis_title="Sales (INR)"
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )


    # ---------------- State Sales ----------------

    st.markdown(
        '<div class="section-title">Regional Performance</div>',
        unsafe_allow_html=True
    )

    state_sales = (
        filtered_df
        .groupby("State", as_index=False)
        ["Sales_INR"]
        .sum()
        .sort_values("Sales_INR", ascending=False)
        .head(10)
    )

    fig_state = px.bar(
        state_sales.sort_values("Sales_INR"),
        x="Sales_INR",
        y="State",
        orientation="h",
        title="Top 10 States by Sales",
        text_auto=".2s"
    )

    fig_state.update_traces(
        marker_color="#6D28D9"
    )

    fig_state.update_layout(
        template="plotly_white",
        height=450,
        xaxis_title="Sales (INR)",
        yaxis_title="State"
    )

    st.plotly_chart(
        fig_state,
        use_container_width=True
    )


    # ---------------- Profit by Category ----------------

    col3, col4 = st.columns(2)

    with col3:

        profit_category = (
            filtered_df
            .groupby("Category", as_index=False)
            ["Profit_INR"]
            .sum()
            .sort_values("Profit_INR", ascending=False)
        )

        fig_profit = px.bar(
            profit_category,
            x="Category",
            y="Profit_INR",
            title="Profit by Category",
            text_auto=".2s"
        )

        fig_profit.update_traces(
            marker_color="#A855F7"
        )

        fig_profit.update_layout(
            template="plotly_white",
            height=400,
            xaxis_title="Category",
            yaxis_title="Profit (INR)"
        )

        st.plotly_chart(
            fig_profit,
            use_container_width=True
        )


    # ---------------- Payment Mode ----------------

    with col4:

        payment_data = (
            filtered_df
            .groupby("Payment_Mode")
            .size()
            .reset_index(name="Orders")
        )

        fig_payment = px.pie(
            payment_data,
            names="Payment_Mode",
            values="Orders",
            title="Payment Method Distribution",
            hole=0.45
        )

        fig_payment.update_layout(
            height=400,
            template="plotly_white"
        )

        st.plotly_chart(
            fig_payment,
            use_container_width=True
        )


# ============================================================
# TAB 2 - PRODUCTS & ORDERS
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">Products & Order Analysis</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # ---------------- Order Status ----------------

    with col1:

        status_data = (
            filtered_df
            .groupby("Order_Status")
            .size()
            .reset_index(name="Orders")
        )

        fig_status = px.pie(
            status_data,
            names="Order_Status",
            values="Orders",
            title="Order Status Distribution",
            hole=0.45
        )

        fig_status.update_layout(
            height=400,
            template="plotly_white"
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True
        )


    # ---------------- Quantity vs Sales ----------------

    with col2:

        fig_scatter = px.scatter(
            filtered_df,
            x="Quantity",
            y="Sales_INR",
            color="Category",
            hover_data=[
                "Product_Name",
                "State"
            ] if "Product_Name" in filtered_df.columns else ["State"],
            title="Quantity vs Sales"
        )

        fig_scatter.update_layout(
            template="plotly_white",
            height=400
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )


    # ---------------- Top Products ----------------

    st.markdown(
        '<div class="section-title">Top Products</div>',
        unsafe_allow_html=True
    )

    if "Product_Name" in filtered_df.columns:

        top_products = (
            filtered_df
            .groupby("Product_Name", as_index=False)
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

        st.dataframe(
            top_products,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Product_Name column is not available in the dataset.")


# ============================================================
# TAB 3 - BUSINESS INSIGHTS
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-title">Business Insights</div>',
        unsafe_allow_html=True
    )

    if len(filtered_df) > 0:

        # Top category
        top_category = (
            filtered_df.groupby("Category")["Sales_INR"]
            .sum()
            .idxmax()
        )

        top_category_sales = (
            filtered_df.groupby("Category")["Sales_INR"]
            .sum()
            .max()
        )

        # Top state
        top_state = (
            filtered_df.groupby("State")["Sales_INR"]
            .sum()
            .idxmax()
        )

        top_state_sales = (
            filtered_df.groupby("State")["Sales_INR"]
            .sum()
            .max()
        )

        # Average order value
        average_order_value = (
            total_sales / total_orders
            if total_orders > 0 else 0
        )

        # Delivered percentage
        delivered_count = (
            (filtered_df["Order_Status"] == "Delivered").sum()
        )

        delivered_percentage = (
            delivered_count / len(filtered_df) * 100
            if len(filtered_df) > 0 else 0
        )

        # Cancelled percentage
        cancelled_count = (
            (filtered_df["Order_Status"] == "Cancelled").sum()
        )

        cancelled_percentage = (
            cancelled_count / len(filtered_df) * 100
            if len(filtered_df) > 0 else 0
        )


        # Insight cards

        st.markdown(
            f"""
            <div class="insight-box">
                🏆 <b>Top Performing Category</b><br>
                {top_category} generated
                <b>₹{top_category_sales:,.0f}</b> in sales.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="insight-box">
                📍 <b>Top Performing State</b><br>
                {top_state} generated
                <b>₹{top_state_sales:,.0f}</b> in sales.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="insight-box">
                💰 <b>Average Order Value</b><br>
                Each order generated approximately
                <b>₹{average_order_value:,.0f}</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="insight-box">
                🚚 <b>Delivered Orders</b><br>
                Approximately
                <b>{delivered_percentage:.2f}%</b>
                of filtered orders were delivered.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="insight-box">
                ⚠️ <b>Cancelled Orders</b><br>
                Approximately
                <b>{cancelled_percentage:.2f}%</b>
                of filtered orders were cancelled.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="insight-box">
                📈 <b>Overall Profitability</b><br>
                The selected data produced
                <b>₹{total_profit:,.0f}</b>
                profit with a margin of
                <b>{profit_margin:.2f}%</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.warning(
            "No data available for the selected filters."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br>
    <hr>
    <div style="
        text-align:center;
        color:#7C6F8A;
        font-size:13px;
        padding:15px;">
        Indian E-Commerce Sales & Profit Analysis
        | Data Analysis & Visualization using Python
    </div>
    """,
    unsafe_allow_html=True
)
