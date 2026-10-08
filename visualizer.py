import pandas as pd
import matplotlib.pyplot as plt


# Colors for our graphs
COLORS = [
    "#6366F1",
    "#14B8A6",
    "#F59E0B",
    "#EC4899",
    "#3B82F6",
    "#8B5CF6"
]


# --------------------------------------------------
# HISTOGRAM
# --------------------------------------------------

def create_histogram(df, column, color):

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(
        df[column].dropna(),
        bins=10,
        color=color,
        edgecolor="white",
        alpha=0.85
    )

    ax.set_title(
        f"Distribution of {column}",
        fontsize=18,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel(
        column,
        fontsize=12
    )

    ax.set_ylabel(
        "Frequency",
        fontsize=12
    )

    ax.tick_params(
        axis="both",
        labelsize=10
    )

    ax.grid(
        linestyle="--",
        alpha=0.25
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    return fig


# --------------------------------------------------
# BAR CHART
# --------------------------------------------------

def create_bar_chart(df, column, color):

    fig, ax = plt.subplots(figsize=(10, 6))

    value_counts = df[column].value_counts()

    ax.bar(
        value_counts.index.astype(str),
        value_counts.values,
        color=color,
        alpha=0.85
    )

    ax.set_title(
        f"Distribution of {column}",
        fontsize=18,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel(
        column,
        fontsize=12
    )

    ax.set_ylabel(
        "Count",
        fontsize=12
    )

    ax.tick_params(
        axis="both",
        labelsize=10
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.xticks(rotation=30)

    plt.tight_layout()

    return fig


# --------------------------------------------------
# SCATTER PLOT
# --------------------------------------------------

def create_scatter_plot(df, x_column, y_column):

    fig, ax = plt.subplots(figsize=(10, 6))

    data = df[
        [x_column, y_column]
    ].dropna()

    ax.scatter(
        data[x_column],
        data[y_column],
        s=100,
        alpha=0.8
    )

    # Add labels if Name column exists
    if "Name" in df.columns:

        for index in data.index:

            ax.annotate(
                df.loc[index, "Name"],
                (
                    df.loc[index, x_column],
                    df.loc[index, y_column]
                ),
                xytext=(6, 6),
                textcoords="offset points",
                fontsize=9
            )

    # Add trend line
    if len(data) >= 2:

        import numpy as np

        x = data[x_column]
        y = data[y_column]

        slope, intercept = np.polyfit(
            x,
            y,
            1
        )

        trend_line = (
            slope * x + intercept
        )

        ax.plot(
            x,
            trend_line,
            linestyle="--",
            linewidth=2
        )

    ax.set_title(
        f"{y_column} vs {x_column}",
        fontsize=18,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel(
        x_column,
        fontsize=12
    )

    ax.set_ylabel(
        y_column,
        fontsize=12
    )

    ax.tick_params(
        axis="both",
        labelsize=10
    )

    ax.grid(
        linestyle="--",
        alpha=0.25
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    return fig


# --------------------------------------------------
# LINE CHART
# --------------------------------------------------

def create_line_chart(df, date_column, value_column):

    fig, ax = plt.subplots(figsize=(10, 6))

    data = df[
        [date_column, value_column]
    ].copy()

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce"
    )

    data = data.dropna()

    data = data.sort_values(
        date_column
    )

    ax.plot(
        data[date_column],
        data[value_column],
        marker="o",
        linewidth=2
    )

    ax.set_title(
        f"{value_column} Over Time",
        fontsize=18,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel(
        date_column,
        fontsize=12
    )

    ax.set_ylabel(
        value_column,
        fontsize=12
    )

    ax.tick_params(
        axis="both",
        labelsize=10
    )

    ax.grid(
        linestyle="--",
        alpha=0.25
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    return fig