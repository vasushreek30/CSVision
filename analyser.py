import pandas as pd



def is_identifier_column(df, column):

    column_name = (
        column.lower()
        .replace("_", " ")
        .replace("-", " ")
    )

    identifier_keywords = [
        "id",
        "name",
        "email",
        "phone",
        "address",
        "roll",
        "registration",
        "reg no",
        "student number",
    ]

    for keyword in identifier_keywords:

        if keyword == column_name:
            return True

    return False




def classify_columns(df):

    column_types = {}

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    for column in df.columns:

        if is_identifier_column(df, column):

            column_types[column] = "identifier"

        elif column in numeric_columns:

            column_types[column] = "numerical"

        else:

            column_types[column] = "categorical"

    return column_types



def analyze_data_quality(df):

    missing_values = df.isnull().sum()

    total_cells = df.shape[0] * df.shape[1]

    total_missing = missing_values.sum()

    if total_cells > 0:

        completeness = (
            (total_cells - total_missing)
            / total_cells
        ) * 100

    else:

        completeness = 0

    duplicate_rows = df.duplicated().sum()

    columns_with_missing = (
        missing_values > 0
    ).sum()

    rows_with_missing = (
        df.isnull().any(axis=1)
    ).sum()

    return {
        "missing_values": missing_values,
        "total_missing": int(total_missing),
        "completeness": completeness,
        "duplicate_rows": int(duplicate_rows),
        "columns_with_missing": int(columns_with_missing),
        "rows_with_missing": int(rows_with_missing)
    }



def detect_outliers(df, column):

    Q1 = df[column].quantile(0.25)

    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR

    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_bound)
        |
        (df[column] > upper_bound)
    ]

    return outliers



def detect_date_columns(df):

    date_columns = []

    for column in df.columns:

        # Skip numerical columns
        if pd.api.types.is_numeric_dtype(
            df[column]
        ):
            continue

        converted = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        valid_dates = converted.notna().sum()

        if len(df) > 0:

            valid_ratio = (
                valid_dates / len(df)
            )

            if valid_ratio >= 0.8:

                date_columns.append(column)

    return date_columns