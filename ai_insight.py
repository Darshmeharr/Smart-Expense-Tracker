class AIInsights:

    @staticmethod
    def generate(df):

        if df.empty:
            return [
                "No transactions available."
            ]

        insights = []

        income = (
            df[df["Type"] == "Income"]
            ["Amount"]
            .sum()
        )

        expenses = (
            df[df["Type"] == "Expense"]
            ["Amount"]
            .sum()
        )

        if income > 0:

            savings_rate = (
                (income - expenses)
                / income
            ) * 100

            if savings_rate >= 40:
                insights.append(
                    "Excellent savings habit. Keep it up."
                )

            elif savings_rate >= 20:
                insights.append(
                    "Good savings rate, but there is room for improvement."
                )

            else:
                insights.append(
                    "Your savings rate is low. Consider reducing discretionary spending."
                )

        expense_df = df[
            df["Type"] == "Expense"
        ]

        if not expense_df.empty:

            category_spending = (
                expense_df.groupby("Category")
                ["Amount"]
                .sum()
                .sort_values(ascending=False)
            )

            top_category = category_spending.index[0]
            top_amount = category_spending.iloc[0]

            insights.append(
                f"Highest spending category: {top_category} (₹{top_amount:.2f})"
            )

            total_expense = category_spending.sum()

            percentage = (
                top_amount / total_expense
            ) * 100

            if percentage > 40:
                insights.append(
                    f"You spend {percentage:.1f}% of your expenses on {top_category}. Consider setting a budget."
                )

        if expenses > income:
            insights.append(
                "Warning: Expenses exceed income."
            )

        if income > expenses:
            insights.append(
                "You are operating at a positive cash flow."
            )

        return insights
