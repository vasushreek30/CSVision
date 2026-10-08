import pandas as pd


def generate_numerical_insights(df, numerical_columns):

    insights = []

    for column in numerical_columns:

        data = df[column].dropna()

        if data.empty:
            continue

        average = data.mean()
        maximum = data.max()
        minimum = data.min()

        insights.append({
            "column": column,
            "average": average,
            "maximum": maximum,
            "minimum": minimum
        })

    return insights