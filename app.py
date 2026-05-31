import streamlit as st
import pandas as pd
from datetime import date

from database import create_tables
from expense_manager import ExpenseManager
from analytics import Analytics
from predictor import ExpensePredictor
from ai_insights import AIInsights

# ----------------------------
# Initial Setup
# ----------------------------

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide"
)

create_tables()

st.title("💰 Smart Expense Tracker")
st.markdown("Track expenses, analyze spending, and predict future expenses.")

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.header("Add Transaction")

transaction_type = st.sidebar.selectbox(
    "Transaction Type",
    ["Expense", "Income"]
)

transaction_date = st.sidebar.date_input(
    "Date",
    value=date.today()
)

description = st.sidebar.text_input(
    "Description"
)

amount = st.sidebar.number_input(
    "Amount",
    min_value=0.0,
    step=1.0
)

if transaction_type == "Expense":

    category = st.sidebar.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Entertainment",
            "Bills",
            "Education",
            "Healthcare",
            "Other"
        ]
    )

else:
    category = "Income"

if st.sidebar.button("Save Transaction"):

    if amount > 0:

        if transaction_type == "Expense":

            ExpenseManager.add_expense(
                str(transaction_date),
                category,
                description,
                amount
            )

        else:

            ExpenseManager.add_income(
                str(transaction_date),
                description,
                amount
            )

        st.sidebar.success("Transaction Added Successfully")

    else:
        st.sidebar.error("Enter Valid Amount")

# ----------------------------
# Load Data
# ----------------------------

df = ExpenseManager.get_dataframe()

# ----------------------------
# Dashboard Cards
# ----------------------------

income = ExpenseManager.get_total_income()
expenses = ExpenseManager.get_total_expenses()
savings = ExpenseManager.get_savings()
health_score = ExpenseManager.get_financial_health_score()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Income", f"₹{income:,.2f}")

with col2:
    st.metric("Expenses", f"₹{expenses:,.2f}")

with col3:
    st.metric("Savings", f"₹{savings:,.2f}")

with col4:
    st.metric("Health Score", f"{health_score}/100")

st.divider()

# ----------------------------
# Transaction History
# ----------------------------

st.subheader("Transaction History")

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No Transactions Available")

st.divider()

# ----------------------------
# Charts
# ----------------------------

left, right = st.columns(2)

with left:

    st.subheader("Category Distribution")

    pie_chart = Analytics.create_pie_chart(df)

    if pie_chart:
        st.pyplot(pie_chart)
    else:
        st.info("Not enough data.")

with right:

    st.subheader("Monthly Trend")

    line_chart = Analytics.create_monthly_chart(df)

    if line_chart:
        st.pyplot(line_chart)
    else:
        st.info("Not enough data.")

st.divider()

# ----------------------------
# Category Summary
# ----------------------------

st.subheader("Category Summary")

summary = Analytics.category_summary(df)

if not summary.empty:
    st.dataframe(summary, use_container_width=True)

    category, amount = Analytics.highest_expense_category(df)

    st.success(
        f"Highest Spending Category: {category} (₹{amount:,.2f})"
    )

else:
    st.info("No expense data available.")

st.divider()

# ----------------------------
# Expense Prediction
# ----------------------------

st.subheader("Expense Prediction")

prediction = ExpensePredictor.predict_next_month(df)

if prediction:
    st.info(
        f"Predicted Next Month Expense: ₹{prediction:,.2f}"
    )
else:
    st.warning(
        "At least 3 months of expense data required."
    )

st.divider()

# ----------------------------
# AI Insights
# ----------------------------

st.subheader("AI Spending Insights")

insights = AIInsights.generate(df)

for insight in insights:
    st.write("•", insight)

st.divider()

# ----------------------------
# Delete Transactions
# ----------------------------

st.subheader("Delete Transaction")

if not df.empty:

    transaction_ids = df["ID"].tolist()

    selected_id = st.selectbox(
        "Select Transaction ID",
        transaction_ids
    )

    if st.button("Delete Selected Transaction"):

        ExpenseManager.remove_transaction(
            selected_id
        )

        st.success(
            "Transaction Deleted Successfully"
        )

        st.rerun()
