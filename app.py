import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Indian E-Commerce Sales Dashboard", page_icon="🛒", layout="wide")

@st.cache_data
def load_data():
    data = pd.read_csv(Path(__file__).parent / "Indian_Ecommerce_Sales_Analysis_Dataset.csv")
    data["Order_Date"] = pd.to_datetime(data["Order_Date"])
    return data

df = load_data()

st.title("🛒 Indian E-Commerce Sales & Profit Dashboard")
st.caption("Interactive analysis of sales, profit, products, customers and regional performance")

st.sidebar.header("🔎 Dashboard Filters")
selected_states = st.sidebar.multiselect("State", sorted(df["State"].unique()), default=sorted(df["State"].unique()))
selected_categories = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
selected_statuses = st.sidebar.multiselect("Order Status", sorted(df["Order_Status"].unique()), default=sorted(df["Order_Status"].unique()))

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()
date_range = st.sidebar.date_input("Order Date", value=(min_date, max_date), min_value=min_date, max_value=max_date)
start_date, end_date = date_range if isinstance(date_range, tuple) and len(date_range) == 2 else (min_date, max_date)

filtered = df[
    df["State"].isin(selected_states)
    & df["Category"].isin(selected_categories)
    & df["Order_Status"].isin(selected_statuses)
    & (df["Order_Date"].dt.date >= start_date)
    & (df["Order_Date"].dt.date <= end_date)
].copy()

total_sales = filtered["Sales_INR"].sum()
total_profit = filtered["Profit_INR"].sum()
total_orders = filtered["Order_ID"].nunique()
total_quantity = filtered["Quantity"].sum()
avg_order_value = total_sales / total_orders if total_orders else 0
profit_margin = total_profit / total_sales * 100 if total_sales else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Sales", f"₹{total_sales:,.0f}")
c2.metric("Total Profit", f"₹{total_profit:,.0f}")
c3.metric("Total Orders", f"{total_orders:,}")
c4.metric("Quantity Sold", f"{total_quantity:,}")
c5.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

monthly = filtered.groupby(filtered["Order_Date"].dt.to_period("M"))["Sales_INR"].sum().reset_index()
monthly["Month"] = monthly["Order_Date"].dt.strftime("%b %Y")
fig_month = px.line(monthly, x="Month", y="Sales_INR", markers=True, title="📈 Monthly Sales Trend")

category_sales = filtered.groupby("Category", as_index=False)["Sales_INR"].sum().sort_values("Sales_INR", ascending=False)
fig_category = px.bar(category_sales, x="Category", y="Sales_INR", title="🛍️ Sales by Category", text_auto=".2s")

left, right = st.columns(2)
with left:
    st.plotly_chart(fig_month, use_container_width=True)
with right:
    st.plotly_chart(fig_category, use_container_width=True)

state_sales = filtered.groupby("State", as_index=False).agg(Sales_INR=("Sales_INR", "sum"), Profit_INR=("Profit_INR", "sum")).sort_values("Sales_INR", ascending=False)
fig_state = px.bar(state_sales.head(10), x="Sales_INR", y="State", orientation="h", title="🏆 Top 10 States by Sales", text_auto=".2s")
fig_state.update_layout(yaxis={"categoryorder": "total ascending"})

category_profit = filtered.groupby("Category", as_index=False)["Profit_INR"].sum().sort_values("Profit_INR", ascending=False)
fig_profit = px.bar(category_profit, x="Category", y="Profit_INR", title="💰 Profit by Category", text_auto=".2s")

left, right = st.columns(2)
with left:
    st.plotly_chart(fig_state, use_container_width=True)
with right:
    st.plotly_chart(fig_profit, use_container_width=True)

payment = filtered["Payment_Mode"].value_counts().reset_index()
payment.columns = ["Payment_Mode", "Count"]
status = filtered["Order_Status"].value_counts().reset_index()
status.columns = ["Order_Status", "Count"]

left, right = st.columns(2)
with left:
    st.plotly_chart(px.pie(payment, names="Payment_Mode", values="Count", hole=0.45, title="💳 Payment Method Distribution"), use_container_width=True)
with right:
    st.plotly_chart(px.pie(status, names="Order_Status", values="Count", hole=0.45, title="📦 Order Status Distribution"), use_container_width=True)

st.plotly_chart(
    px.scatter(filtered, x="Quantity", y="Sales_INR", color="Category",
               hover_data=["Sub_Category", "State", "Order_Status"],
               title="📊 Quantity vs Sales"),
    use_container_width=True
)

top_products = filtered.groupby("Sub_Category", as_index=False).agg(
    Sales_INR=("Sales_INR", "sum"),
    Profit_INR=("Profit_INR", "sum"),
    Quantity=("Quantity", "sum")
).sort_values("Sales_INR", ascending=False).head(10)

st.subheader("⭐ Top 10 Products")
st.dataframe(top_products, use_container_width=True, hide_index=True)

st.subheader("💡 Key Insights")
if not filtered.empty:
    best_category = category_sales.iloc[0]["Category"]
    best_state = state_sales.iloc[0]["State"]
    best_product = top_products.iloc[0]["Sub_Category"]
    delivered_pct = (filtered["Order_Status"].eq("Delivered").mean()) * 100
    cancelled_pct = (filtered["Order_Status"].eq("Cancelled").mean()) * 100

    a, b, c, d = st.columns(4)
    a.info(f"Top category: {best_category}")
    b.info(f"Top state: {best_state}")
    c.info(f"Top product: {best_product}")
    d.info(f"Delivered orders: {delivered_pct:.1f}%")

    st.write(f"- Total sales: ₹{total_sales:,.0f}")
    st.write(f"- Total profit: ₹{total_profit:,.0f}")
    st.write(f"- Average order value: ₹{avg_order_value:,.0f}")
    st.write(f"- Overall profit margin: {profit_margin:.2f}%")
    st.write(f"- Cancelled orders: {cancelled_pct:.1f}%")
else:
    st.warning("No records match the selected filters.")

st.divider()
st.caption("Indian E-Commerce Sales & Profit Analysis | Python + Pandas + Plotly + Streamlit")
