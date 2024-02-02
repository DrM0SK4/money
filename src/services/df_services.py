"services for pandas dataframe"
from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd

INVESTMENT = "Investment"


def extract_column(df: pd.DataFrame, col_names: List[str]) -> pd.Series:
    """Extract a list of columns from a dataframe.

    Args:
        df (pd.DataFrame): _description_
        col_names (List[str]): _description_

    Returns:
        pd.Series: _description_
    """
    return df[col_names]


def convert_type_to_investment(df: pd.DataFrame) -> pd.DataFrame:
    """Convert certain transactions type to investment.

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    # return df[df["Description"] != "E. Mosca"]
    investment_transactions_description = [
        "E. Mosca",
        "Flatex Bank AG",
        "Degiro Enrico Mosca",
    ]
    for itd in investment_transactions_description:
        df.loc[df["Description"] == itd, "Type"] = INVESTMENT
    investment_transaction_name = ["1097726"]
    for itn in investment_transaction_name:
        df.loc[df["Name"].str.contains(itn, case=False, na=False), "Type"] = INVESTMENT

    return df


def convert_amount(amount: str) -> float:
    """Convert a string like 23,89 into a float like 23.89

    Args:
        amount (str): _description_

    Returns:
        float: _description_
    """
    return float(amount.replace(".", "").replace(",", "."))


def compute_expenses(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Given a datarame with two columns Type and Amount:
        -> sum together all the Amount for Type == Debet
        -> sum together all the Amount for Type == Credit
        -> sum together all the Amount for Type == Investment

    Args:
        df (pd.DataFrame): _description_

    Returns:
        Tuple[float,float, float]: total_credit_amount,total_debit_amount,total_investment_amount
    """

    total_credit_amount: float = df.loc[df["Type"] == "Credit", "Amount"].sum()
    total_debit_amount: float = df.loc[df["Type"] == "Debet", "Amount"].sum()
    total_investment_amount: float = df.loc[df["Type"] == INVESTMENT, "Amount"].sum()

    return (total_credit_amount, total_debit_amount, total_investment_amount)


def plot_pie_chart(
    total_credit_amount: float,
    total_debit_amount: float,
    total_investment_amount: float,
) -> None:
    """Plot the total credit, total debit and total investment as a pie chart.

    Args:
        total_credit_amount (float): _description_
        total_debit_amount (float): _description_
        total_investment_amount (float): _description_
    """

    # Create a DataFrame for plotting
    plot_data = pd.DataFrame(
        {"Amount": [total_credit_amount, total_debit_amount, total_investment_amount]},
        index=["Credit", "Debit", INVESTMENT],
    )

    # Plot a pie chart
    ax = plot_data.plot.pie(y="Amount", autopct="%1.1f%%", startangle=90, labels=None)

    # Display numeric values as annotations
    for index, value in enumerate(plot_data["Amount"]):
        ax.text(index, 0, f"{value:.2f}", ha="center", va="center")

    ax.text(
        len(plot_data["Amount"]) + 1,
        0,
        f"{(total_credit_amount-total_debit_amount):.2f}",
        ha="center",
        va="center",
    )
    plt.title("Credit, Debit and Investment Amounts")
    plt.show()


def month_analysis(df: pd.DataFrame) -> None:
    """_summary_

    Args:
        df (pd.DataFrame): _description_
    """
    # Convert the 'Date' column to datetime format
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

    # Extract the month from the 'Date' column
    df["Month"] = df["Date"].dt.month
    df = extract_column(df=df, col_names=["Type", "Amount", "Month", "Date"])
    df.loc[:, "Amount"] = df["Amount"].apply(convert_amount)

    pivot_table = df.pivot_table(
        index="Month", columns="Type", values="Amount", aggfunc="sum", fill_value=0
    )

    # Plot stacked bar chart
    pivot_table.plot(kind="bar", stacked=True, colormap="tab20c")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.title("Credit and Debit Amounts by Month")
    plt.legend(title="Type", loc="upper right")
    plt.show()
