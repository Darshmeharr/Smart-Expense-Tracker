import pandas as pd
import matplotlib.pyplot as plt


class Analytics:

    @staticmethod
    def category_summary(df):

        if df.empty:
            return pd.DataFrame()

        expenses = df[df["Type"] == "Expense"]

        if expenses.empty:
            return pd.DataFrame()

        summary = (
            expenses.groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        return summary

    @staticmethod
    def monthly_summary(df):

        if df.empty:
            return pd.DataFrame()

        df["Date"] = pd.to_datetime(df["Date"])

        expenses = df[df["Type"] == "Expense"]

        if expenses.empty:
            return pd.DataFrame()

        expenses["Month"] = expenses["Date"].dt.strftime("%Y-%m")

        monthly = (
            expenses.groupby("Month")["Amount"]
            .sum()
            .reset_index()
        )

        return monthly

    @staticmethod
    def highest_expense_category(df):

        summary = Analytics.category_summary(df)

        if summary.empty:
            return None, 0

        category = summary.iloc[0]["Category"]
        amount = summary.iloc[0]["Amount"]

        return category, amount

    @staticmethod
    def create_pie_chart(df):

        summary = Analytics.category_summary(df)

        if summary.empty:
            return None

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.pie(
            summary["Amount"],
            labels=summary["Category"],
            autopct="%1.1f%%"
        )

        ax.set_title("Category Wise Spending")

        return fig

    @staticmethod
    def create_monthly_chart(df):

        monthly = Analytics.monthly_summary(df)

        if monthly.empty:
            return None

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.plot(
            monthly["Month"],
            monthly["Amount"],
            marker="o"
        )

        ax.set_title("Monthly Expense Trend")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount")

        plt.xticks(rotation=45)

        return fig
