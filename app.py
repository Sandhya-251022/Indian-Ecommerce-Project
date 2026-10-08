import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================
# PROFESSIONAL PURPLE THEME
# =========================

st.markdown("""
<style>

/* ---------- MAIN PAGE ---------- */
.stApp {
    background: #F7F5FC;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #24113F 0%,
        #3B176D 50%,
        #4C1D95 100%
    );
}

section[data-testid="stSidebar"] > div {
    background: transparent;
}

/* Sidebar normal text */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: #FFFFFF !important;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

/* ---------- DATE INPUT ---------- */
section[data-testid="stSidebar"] input {
    color: #24113F !important;
    background-color: #FFFFFF !important;
    border-radius: 10px !important;
}

/* ---------- MULTISELECT / SELECT BOX ---------- */
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #24113F !important;
}

/* Selected filter tags */
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background-color: #7C3AED !important;
    color: white !important;
}

section[data-testid="stSidebar"] span[data-baseweb="tag"] span {
    color: white !important;
}

/* ---------- DATASET PERIOD BOX ---------- */
.dataset-period {
    background: linear-gradient(
        135deg,
        #7C3AED,
        #A855F7
    );
    color: #FFFFFF;
    padding: 14px;
    border-radius: 12px;
    margin-top: 10px;
    font-size: 0.85rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.25);
}

.dataset-period-title {
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 6px;
}

.dataset-period-date {
    color: #FFFFFF;
    font-weight: 500;
    line-height: 1.6;
}

/* ---------- MAIN HEADER ---------- */
.dashboard-header {
    background: linear-gradient(
        135deg,
        #24113F,
        #5B21B6,
        #7C3AED
    );
    color: white;
    padding: 32px;
    border-radius: 0 0 22px 22px;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(76,29,149,0.25);
}

.dashboard-header h1 {
    color: white !important;
    font-size: 2.4rem;
    margin-bottom: 8px;
}

.dashboard-header p {
    color: #EDE9FE !important;
    font-size: 1.05rem;
}

/* ---------- KPI CARDS ---------- */
.kpi-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 22px;
    border: 1px solid #E9D5FF;
    box-shadow: 0 5px 18px rgba(76,29,149,0.10);
    min-height: 135px;
}

.kpi-title {
    color: #6B21A8;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.kpi-value {
    color: #24113F;
    font-size: 1.75rem;
    font-weight: 800;
    margin-top: 10px;
}

.kpi-description {
    color: #7C6F8D;
    font-size: 0.78rem;
    margin-top: 6px;
}

/* ---------- SECTION HEADINGS ---------- */
h1, h2, h3 {
    color: #24113F !important;
}

.section-title {
    color: #5B21B6;
    font-size: 1.35rem;
    font-weight: 800;
    margin-top: 20px;
}

/* ---------- TABS ---------- */
button[data-baseweb="tab"] {
    color: #5B21B6 !important;
    font-weight: 600 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #7C3AED !important;
    border-bottom-color: #7C3AED !important;
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    background: linear-gradient(
        135deg,
        #6D28D9,
        #8B5CF6
    ) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background: #5B21B6 !important;
    color: white !important;
}

/* ---------- INFO BOX ---------- */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* ---------- DATAFRAME ---------- */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    border: 1px solid #E9D5FF;
}

/* ---------- SCROLLBAR ---------- */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #F3E8FF;
}

::-webkit-scrollbar-thumb {
    background: #7C3AED;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #5B21B6;
}

</style>
""", unsafe_allow_html=True)


st.sidebar.markdown(
    f"""
    <div class="dataset-period">
        <div class="dataset-period-title">
            📊 Dataset Period
        </div>

        <div class="dataset-period-date">
            {dataset_start.strftime("%d %B %Y")}
            &nbsp; → &nbsp;
            {dataset_end.strftime("%d %B %Y")}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <h3 style="color:white !important;">
        📅 Date Range
    </h3>
    """,
    unsafe_allow_html=True
)
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
