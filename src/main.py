"entrypoint of repo"

import pandas as pd

from services.df_services import (
    compute_expenses,
    convert_amount,
    convert_type_to_investment,
    extract_column,
    month_analysis,
    plot_pie_chart,
)
from services.label_services import classify


def main(df: pd.DataFrame):
    """main entrypoint"""

    df = convert_type_to_investment(df=df)
    expenses = extract_column(df=df, col_names=["Type", "Amount"])
    expenses.loc[:, "Amount"] = expenses["Amount"].apply(convert_amount)
    total_credit_amount, total_debit_amount, total_investment_amount = compute_expenses(
        df=expenses
    )
    plot_pie_chart(
        total_credit_amount=total_credit_amount,
        total_debit_amount=total_debit_amount,
        total_investment_amount=total_investment_amount,
    )
    month_analysis(df=df)


if __name__ == "__main__":
    df = pd.read_csv("data/mutations20240108202828.csv")

    # classify(df=df)
    main(df=df)
    input("press any key to exit: ")
