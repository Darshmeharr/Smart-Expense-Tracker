from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np


class ExpensePredictor:

    @staticmethod
    def predict_next_month(df):

        if df.empty:
            return None

        expenses = df[df["Type"] == "Expense"]

        if len(expenses) < 3:
            return None

        expenses["Date"] = pd.to_datetime(expenses["Date"])

        expenses["Month"] = (
            expenses["Date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly = (
            expenses.groupby("Month")["Amount"]
            .sum()
            .reset_index()
        )

        if len(monthly) < 3:
            return None

        X = np.arange(len(monthly)).reshape(-1, 1)

        y = monthly["Amount"]

        model = LinearRegression()

        model.fit(X, y)

        next_month = model.predict(
            [[len(monthly)]]
        )[0]

        return round(next_month, 2)
