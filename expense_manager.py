from database import (
    insert_transaction,
    fetch_transactions,
    delete_transaction
)

import pandas as pd


class ExpenseManager:

    @staticmethod
    def add_income(date, description, amount):
        insert_transaction(
            date=date,
            category="Income",
            description=description,
            amount=amount,
            transaction_type="Income"
        )

    @staticmethod
    def add_expense(date, category, description, amount):
        insert_transaction(
            date=date,
            category=category,
            description=description,
            amount=amount,
            transaction_type="Expense"
        )

    @staticmethod
    def get_dataframe():
        data = fetch_transactions()

        df = pd.DataFrame(
            data,
            columns=[
                "ID",
                "Date",
                "Category",
                "Description",
                "Amount",
                "Type"
            ]
        )

        return df

    @staticmethod
    def get_total_income():
        df = ExpenseManager.get_dataframe()

        if df.empty:
            return 0

        income = df[df["Type"] == "Income"]

        return income["Amount"].sum()

    @staticmethod
    def get_total_expenses():
        df = ExpenseManager.get_dataframe()

        if df.empty:
            return 0

        expenses = df[df["Type"] == "Expense"]

        return expenses["Amount"].sum()

    @staticmethod
    def get_savings():
        return (
            ExpenseManager.get_total_income()
            - ExpenseManager.get_total_expenses()
        )

    @staticmethod
    def get_category_expenses():
        df = ExpenseManager.get_dataframe()

        if df.empty:
            return pd.DataFrame()

        expenses = df[df["Type"] == "Expense"]

        grouped = (
            expenses.groupby("Category")["Amount"]
            .sum()
            .reset_index()
        )

        return grouped

    @staticmethod
    def remove_transaction(transaction_id):
        delete_transaction(transaction_id)

    @staticmethod
    def get_financial_health_score():

        income = ExpenseManager.get_total_income()
        expenses = ExpenseManager.get_total_expenses()

        if income == 0:
            return 0

        savings_rate = ((income - expenses) / income) * 100

        if savings_rate >= 40:
            return 100
        elif savings_rate >= 30:
            return 85
        elif savings_rate >= 20:
            return 70
        elif savings_rate >= 10:
            return 55
        else:
            return 40
