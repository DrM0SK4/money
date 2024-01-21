from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd


def extract_column(df: pd.DataFrame, col_names: List[str]) -> pd.Series:
    """Extract a list of columns from a dataframe.

    Args:
        df (pd.DataFrame): _description_
        col_names (List[str]): _description_

    Returns:
        pd.Series: _description_
    """
    return df[col_names]


def convert_amount(amount: str) -> float:
    """Convert a string like 23,89 into a float like 23.89

    Args:
        amount (str): _description_

    Returns:
        float: _description_
    """
    return float(amount.replace(".", "").replace(",", "."))


def compute_expenses(df: pd.DataFrame) -> Tuple[float, float]:
    """Given a datarame with two columns Type and Amount:
        -> sum together all the Amount for Type == Debet
        -> sum together all the Amount for Type == Credit

    Args:
        df (pd.DataFrame): _description_

    Returns:
        Tuple[float,float]: total_credit_amount,total_debit_amount
    """

    total_credit_amount: float = df.loc[df["Type"] == "Credit", "Amount"].sum()
    total_debit_amount: float = df.loc[df["Type"] == "Debet", "Amount"].sum()

    return (total_credit_amount, total_debit_amount)


def plot_pie_chart(total_credit_amount: float, total_debit_amount: float) -> None:
    """Plot the total credit and total debit as a pie chart.

    Args:
        total_credit_amount (float): _description_
        total_debit_amount (float): _description_
    """

    # Create a DataFrame for plotting
    plot_data = pd.DataFrame(
        {"Amount": [total_credit_amount, total_debit_amount]}, index=["Credit", "Debit"]
    )

    # Plot a pie chart
    ax = plot_data.plot.pie(y="Amount", autopct="%1.1f%%", startangle=90, labels=None)

    # Display numeric values as annotations
    for index, value in enumerate(plot_data["Amount"]):
        ax.text(index, 0, f"{value:.2f}", ha="center", va="center")

    ax.text(
        index + 1,
        0,
        f"{(total_credit_amount-total_debit_amount):.2f}",
        ha="center",
        va="center",
    )
    plt.title("Credit and Debit Amounts")
    plt.show()


def month_analysis(df: pd.DataFrame) -> None:
    # Convert the 'Date' column to datetime format
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

    # Extract the month from the 'Date' column
    df["Month"] = df["Date"].dt.month
    df = extract_column(df=df, col_names=["Type", "Amount", "Month", "Date"])
    df.loc[:, "Amount"] = df["Amount"].apply(convert_amount)
    # Group the DataFrame by month
    # grouped_by_month = df.groupby("Month").size()

    # # Plot a histogram
    # grouped_by_month.plot(kind="bar", color="skyblue")
    # plt.xlabel("Month")
    # plt.ylabel("Frequency")
    # plt.title("Histogram of Dates by Month")
    # plt.show()
    pivot_table = df.pivot_table(
        index="Month", columns="Type", values="Amount", aggfunc="sum", fill_value=0
    )

    # Plot stacked bar chart
    ax = pivot_table.plot(kind="bar", stacked=True, colormap="tab20c")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.title("Credit and Debit Amounts by Month")
    plt.legend(title="Type", loc="upper right")
    plt.show()


def main():
    df = pd.read_csv("mutations20240108202828.csv")

    expenses = extract_column(df=df, col_names=["Type", "Amount"])
    expenses.loc[:, "Amount"] = expenses["Amount"].apply(convert_amount)
    total_credit_amount, total_debit_amount = compute_expenses(df=expenses)
    # plot_pie_chart(
    #     total_credit_amount=total_credit_amount, total_debit_amount=total_debit_amount
    # )
    month_analysis(df=df)


if __name__ == "__main__":
    main()
    input("press any key to exit: ")
