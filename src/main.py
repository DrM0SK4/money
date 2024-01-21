"entrypoint of repo"

import pandas as pd

from services.df_services import (
    compute_expenses,
    convert_amount,
    extract_column,
    month_analysis,
    plot_pie_chart,
)


def main():
    """main entrypoint"""
    df = pd.read_csv("data/mutations20240108202828.csv")

    expenses = extract_column(df=df, col_names=["Type", "Amount"])
    expenses.loc[:, "Amount"] = expenses["Amount"].apply(convert_amount)
    total_credit_amount, total_debit_amount = compute_expenses(df=expenses)
    plot_pie_chart(
        total_credit_amount=total_credit_amount, total_debit_amount=total_debit_amount
    )
    month_analysis(df=df)


if __name__ == "__main__":
    main()
    input("press any key to exit: ")
