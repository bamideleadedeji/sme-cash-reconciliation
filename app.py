import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="SME Daily Cash & Sales Reconciliation",
    page_icon="📊",
    layout="wide",
)

# App Header
st.title(" SME Daily Cash & Sales Reconciliation Suite")
st.caption(
    "Interactive Demo | Built for Retail, POS Operators, and Micro-Enterprises"
)

# Sidebar Call-to-Action
st.sidebar.header(" Get the Full Master Suite")
st.sidebar.info(
    "Need the offline Excel & live Google Sheets master template with automated"
    " formulas?"
)
st.sidebar.markdown(
    "[👉 Buy on Gumroad ($15)](https://bamidele38.gumroad.com/l/xjgee)"
)
st.sidebar.markdown(
    "[🇳🇬 Local Bank Transfer (₦5,000)](https://flutterwave.com)"
)

# Initialize Session State Data
if "df_log" not in st.session_state:
  st.session_state.df_log = pd.DataFrame({
      "Txn ID": ["TXN-001", "TXN-002", "TXN-003", "TXN-004"],
      "Category": ["Retail Sales", "Retail Sales", "Retail Sales", "Supplies"],
      "Payment Mode": ["Cash", "POS", "Bank Transfer", "Cash"],
      "Description": [
          "Store Over-the-counter",
          "Card POS Terminal",
          "Direct Bank Transfer",
          "Inventory Restock",
      ],
      "Cash In": [25000.0, 18500.0, 42000.0, 0.0],
      "Cash Out": [0.0, 0.0, 0.0, 12000.0],
  })

# 1. Interactive Ledger Table
st.subheader("1. Daily Transaction Ledger")
st.write("Edit values directly in the table to test live reconciliation:")

edited_df = st.data_editor(
    st.session_state.df_log, num_rows="dynamic", use_container_width=True
)

# 2. Real-time Till Reconciliation Engine
st.markdown("---")
st.subheader("2. Till Reconciliation & Cash Count")

cash_in_total = edited_df[edited_df["Payment Mode"] == "Cash"]["Cash In"].sum()
cash_out_total = edited_df[edited_df["Payment Mode"] == "Cash"][
    "Cash Out"
].sum()
expected_cash = cash_in_total - cash_out_total

col1, col2, col3 = st.columns(3)

with col1:
  st.metric(
      "Expected Cash in Till",
      f"₦{expected_cash:,.2f}",
      help="Calculated as Cash In minus Cash Out",
  )

with col2:
  actual_cash = st.number_input(
      "Actual Physical Cash Counted (₦)",
      value=float(expected_cash),
      step=1000.0,
  )

variance = actual_cash - expected_cash

with col3:
  if variance == 0:
    st.success("✅ TILL BALANCED (Zero Discrepancy)")
  elif variance < 0:
    st.error(f"⚠️ SHORTAGE DETECTED: ₦{abs(variance):,.2f}")
  else:
    st.warning(f"ℹ️ SURPLUS DETECTED: ₦{variance:,.2f}")

# 3. Channel Breakdown Chart
st.markdown("---")
st.subheader("3. Payment Mode Inflow Analysis")

inflow_by_mode = (
    edited_df.groupby("Payment Mode")["Cash In"].sum().reset_index()
)
fig = px.pie(
    inflow_by_mode,
    values="Cash In",
    names="Payment Mode",
    hole=0.4,
    title="Inflows by Payment Channel",
)
st.plotly_chart(fig, use_container_width=True)
