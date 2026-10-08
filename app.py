import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt

from analyser import (
    classify_columns,
    analyze_data_quality,
    detect_date_columns,
    detect_outliers
)

from insights import generate_numerical_insights

from visualizer import (
    create_histogram,
    create_bar_chart,
    create_scatter_plot,
    create_line_chart,
    COLORS
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CSV Insight Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# BACKGROUND IMAGE
# =========================================================

with open("assets/background.png", "rb") as image_file:

    encoded_image = base64.b64encode(
        image_file.read()
    ).decode()


# =========================================================
# CUSTOM CSS
# =========================================================

st.html(f"""
<style>

.stApp {{
    background-image:
        linear-gradient(
            rgba(5, 10, 20, 0.78),
            rgba(5, 10, 20, 0.78)
        ),
        url("data:image/png;base64,{encoded_image}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
}}

header {{
    visibility: hidden;
}}

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

.block-container {{
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}}


/* =====================================================
   HERO
   ===================================================== */

.hero {{
    text-align: center;
    padding: 55px 20px 45px;
}}

.hero-badge {{
    display: inline-block;
    padding: 8px 16px;
    border-radius: 999px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(129, 140, 248, 0.3);
    color: #c4b5fd;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 20px;
}}

.hero-icon {{
    width: 64px;
    height: 64px;
    margin: 0 auto 20px;

    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 5px;

    padding: 12px;

    border-radius: 16px;

    background: rgba(15, 23, 42, 0.75);

    border: 1px solid rgba(96, 165, 250, 0.35);

    box-shadow:
        0 0 25px rgba(59, 130, 246, 0.15);

    backdrop-filter: blur(10px);
}}

.bar {{
    width: 8px;
    border-radius: 4px 4px 2px 2px;
}}

.bar-1 {{
    height: 18px;
    background: #60a5fa;
}}

.bar-2 {{
    height: 28px;
    background: #38bdf8;
}}

.bar-3 {{
    height: 22px;
    background: #f59e0b;
}}

.bar-4 {{
    height: 36px;
    background: #fb923c;
}}

.hero-title {{
    font-size: 58px;
    font-weight: 800;
    letter-spacing: -2px;
    margin: 0;

    background: linear-gradient(
        90deg,
        #f8fafc,
        #60a5fa,
        #f59e0b
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.hero-subtitle {{
    max-width: 700px;
    margin: 20px auto 0;
    color: #e2e8f0;
}}


/* =====================================================
   FEATURE CARDS
   ===================================================== */

.feature-card {{
    height: 100%;
    min-height: 175px;
    padding: 28px;

    border-radius: 20px;

    background: rgba(15, 23, 42, 0.55);

    border: 1px solid rgba(255, 255, 255, 0.12);

    box-shadow:
        0 20px 50px rgba(0, 0, 0, 0.25);

    backdrop-filter: blur(15px);
}}

.feature-icon {{
    font-size: 32px;
    margin-bottom: 18px;
}}

.feature-title {{
    color: #f8fafc;
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 8px;
}}

.feature-text {{
    color: #cbd5e1;
    font-size: 14px;
    line-height: 1.6;
}}


/* =====================================================
   SECTIONS
   ===================================================== */

.section-heading {{
    color: #f8fafc;
    font-size: 27px;
    font-weight: 750;
    margin-top: 55px;
    margin-bottom: 8px;
}}

.section-description {{
    color: #94a3b8;
    font-size: 15px;
    margin-bottom: 20px;
}}


/* =====================================================
   FILE UPLOADER
   ===================================================== */

div[data-testid="stFileUploader"] {{
    background: rgba(15, 23, 42, 0.60);

    border: 1px dashed rgba(129, 140, 248, 0.6);

    border-radius: 22px;

    padding: 25px;

    backdrop-filter: blur(15px);

    transition: 0.2s ease;
}}

div[data-testid="stFileUploader"]:hover {{
    border-color: rgba(167, 139, 250, 0.9);

    background: rgba(30, 27, 75, 0.65);
}}

div[data-testid="stFileUploader"] label {{
    color: #e2e8f0 !important;
}}


/* =====================================================
   STATISTICS
   ===================================================== */

.stat-card {{
    padding: 24px;

    border-radius: 18px;

    background: rgba(15, 23, 42, 0.60);

    border: 1px solid rgba(255, 255, 255, 0.1);

    backdrop-filter: blur(15px);
}}

.stat-label {{
    color: #94a3b8;
    font-size: 13px;
    margin-bottom: 8px;
}}

.stat-value {{
    color: #f8fafc;
    font-size: 30px;
    font-weight: 750;
}}


/* =====================================================
   SUCCESS MESSAGE
   ===================================================== */

.success-box {{
    padding: 15px 20px;

    margin-top: 20px;

    border-radius: 14px;

    background: rgba(34, 197, 94, 0.10);

    border: 1px solid rgba(34, 197, 94, 0.25);

    color: #86efac;

    font-weight: 600;
}}


/* =====================================================
   DATAFRAME
   ===================================================== */

div[data-testid="stDataFrame"] {{
    border-radius: 15px;
    overflow: hidden;
}}

</style>
""")


# =========================================================
# HERO SECTION
# =========================================================

st.html("""
<div class="hero">

    <div class="hero-icon">
        <span class="bar bar-1"></span>
        <span class="bar bar-2"></span>
        <span class="bar bar-3"></span>
        <span class="bar bar-4"></span>
    </div>

    <div class="hero-title">
        CSVision
    </div>

    <div class="hero-subtitle">
        Turn raw CSV data into meaningful insights,
        powerful visualizations, and intelligent analysis —
        automatically.
    </div>

</div>
""")


# =========================================================
# FEATURE CARDS
# =========================================================

col1, col2, col3 = st.columns(
    3,
    gap="large"
)


with col1:

    st.html("""
    <div class="feature-card">

        <div class="feature-icon">
            🔍
        </div>

        <div class="feature-title">
            Automatic Analysis
        </div>

        <div class="feature-text">
            Detect numerical, categorical, date,
            and identifier columns automatically.
        </div>

    </div>
    """)


with col2:

    st.html("""
    <div class="feature-card">

        <div class="feature-icon">
            📈
        </div>

        <div class="feature-title">
            Smart Visualizations
        </div>

        <div class="feature-text">
            Generate meaningful charts based on
            the structure and relationships in your data.
        </div>

    </div>
    """)


with col3:

    st.html("""
    <div class="feature-card">

        <div class="feature-icon">
            🧠
        </div>

        <div class="feature-title">
            Intelligent Insights
        </div>

        <div class="feature-text">
            Discover trends, correlations,
            outliers, and important patterns.
        </div>

    </div>
    """)


# =========================================================
# UPLOAD SECTION
# =========================================================

st.html("""
<div class="section-heading">
    🚀 Start Exploring Your Data
</div>

<div class="section-description">
    Upload a CSV file and let the analyzer do the work.
</div>
""")


uploaded_file = st.file_uploader(
    "Drop your CSV file here or click Browse files",
    type=["csv"],
    help="CSV files only"
)


# =========================================================
# DATA ANALYSIS
# =========================================================

if uploaded_file is not None:

    try:

        # =================================================
        # LOAD DATA
        # =================================================

        df = pd.read_csv(uploaded_file)


        # =================================================
        # ANALYZE DATA
        # =================================================

        column_types = classify_columns(df)

        data_quality = analyze_data_quality(df)

        date_columns = detect_date_columns(df)


        # =================================================
        # GET NUMERICAL COLUMNS
        # =================================================

        numerical_columns = [
            column
            for column, column_type in column_types.items()
            if column_type == "numerical"
        ]


        # =================================================
        # AUTOMATIC VISUALIZATIONS
        # =================================================

        st.html("""
        <div class="section-heading">
            📊 Automatic Visualizations
        </div>

        <div class="section-description">
            Automatically generated charts based on the
            structure of your dataset.
        </div>
        """)


        charts = []

        color_index = 0


        # -------------------------------------------------
        # GENERATE ALL AUTOMATIC VISUALIZATIONS
        # -------------------------------------------------

        for column, column_type in column_types.items():

            # ---------------------------------------------
            # NUMERICAL COLUMN
            # ---------------------------------------------

            if column_type == "numerical":

                color = COLORS[
                    color_index % len(COLORS)
                ]

                fig = create_histogram(
                    df,
                    column,
                    color
                )

                charts.append(fig)

                color_index += 1


            # ---------------------------------------------
            # CATEGORICAL COLUMN
            # ---------------------------------------------

            elif column_type == "categorical":

                color = COLORS[
                    color_index % len(COLORS)
                ]

                fig = create_bar_chart(
                    df,
                    column,
                    color
                )

                charts.append(fig)

                color_index += 1


        # -------------------------------------------------
        # DISPLAY TWO AUTOMATIC CHARTS PER ROW
        # -------------------------------------------------

        for i in range(
            0,
            len(charts),
            2
        ):

            chart_columns = st.columns(
                2,
                gap="large"
            )


            # First chart
            with chart_columns[0]:

                st.pyplot(
                    charts[i],
                    width="stretch"
                )


            # Second chart
            if i + 1 < len(charts):

                with chart_columns[1]:

                    st.pyplot(
                        charts[i + 1],
                        width="stretch"
                    )


        # -------------------------------------------------
        # CLOSE AUTOMATIC CHARTS
        # -------------------------------------------------

        for fig in charts:

            plt.close(fig)


        # =================================================
        # RELATIONSHIP ANALYSIS
        # =================================================

        if len(numerical_columns) >= 2:

            st.html("""
            <div class="section-heading">
                🔗 Relationship Analysis
            </div>

            <div class="section-description">
                Explore relationships between numerical
                variables in your dataset.
            </div>
            """)


            relationship_charts = []


            # -------------------------------------------------
            # GENERATE ALL RELATIONSHIP CHARTS
            # -------------------------------------------------

            for i in range(
                len(numerical_columns)
            ):

                for j in range(
                    i + 1,
                    len(numerical_columns)
                ):

                    x_column = numerical_columns[i]

                    y_column = numerical_columns[j]

                    fig = create_scatter_plot(
                        df,
                        x_column,
                        y_column
                    )

                    relationship_charts.append(
                        fig
                    )


            # -------------------------------------------------
            # DISPLAY TWO RELATIONSHIP CHARTS PER ROW
            # -------------------------------------------------

            for i in range(
                0,
                len(relationship_charts),
                2
            ):

                chart_columns = st.columns(
                    2,
                    gap="large"
                )


                # First relationship chart
                with chart_columns[0]:

                    st.pyplot(
                        relationship_charts[i],
                        width="stretch"
                    )


                # Second relationship chart
                if i + 1 < len(relationship_charts):

                    with chart_columns[1]:

                        st.pyplot(
                            relationship_charts[i + 1],
                            width="stretch"
                        )


            # -------------------------------------------------
            # CLOSE RELATIONSHIP CHARTS
            # -------------------------------------------------

            for fig in relationship_charts:

                plt.close(fig)


        # =================================================
        # DATE / TIME VISUALIZATIONS
        # =================================================

        if date_columns and numerical_columns:

            st.html("""
            <div class="section-heading">
                📅 Trends Over Time
            </div>

            <div class="section-description">
                Visualize how numerical values change over time.
            </div>
            """)


            time_charts = []


            # -------------------------------------------------
            # GENERATE ALL TIME CHARTS
            # -------------------------------------------------

            for date_column in date_columns:

                for numerical_column in numerical_columns:

                    fig = create_line_chart(
                        df,
                        date_column,
                        numerical_column
                    )

                    time_charts.append(
                        fig
                    )


            # -------------------------------------------------
            # DISPLAY TWO TIME CHARTS PER ROW
            # -------------------------------------------------

            for i in range(
                0,
                len(time_charts),
                2
            ):

                chart_columns = st.columns(
                    2,
                    gap="large"
                )


                # First time chart
                with chart_columns[0]:

                    st.pyplot(
                        time_charts[i],
                        width="stretch"
                    )


                # Second time chart
                if i + 1 < len(time_charts):

                    with chart_columns[1]:

                        st.pyplot(
                            time_charts[i + 1],
                            width="stretch"
                        )


            # -------------------------------------------------
            # CLOSE TIME CHARTS
            # -------------------------------------------------

            for fig in time_charts:

                plt.close(fig)


        # =================================================
        # COLUMN ANALYSIS
        # =================================================

        st.html("""
        <div class="section-heading">
            🔍 Column Analysis
        </div>

        <div class="section-description">
            Automatically detected the type of each column
            in your dataset.
        </div>
        """)


        for column, column_type in column_types.items():

            if column_type == "numerical":

                icon = "🔢"
                label = "Numerical"

            elif column_type == "categorical":

                icon = "🏷️"
                label = "Categorical"

            elif column_type == "identifier":

                icon = "🆔"
                label = "Identifier"

            else:

                icon = "📌"
                label = column_type.title()


            st.html(f"""
            <div class="stat-card" style="margin-bottom: 10px;">

                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">

                    <div style="
                        color: #f8fafc;
                        font-size: 16px;
                        font-weight: 600;
                    ">
                        {column}
                    </div>

                    <div style="
                        color: #cbd5e1;
                        font-size: 14px;
                    ">
                        {icon} {label}
                    </div>

                </div>

            </div>
            """)


        # =================================================
        # DATA QUALITY
        # =================================================

        st.html("""
        <div class="section-heading">
            🧹 Data Quality
        </div>

        <div class="section-description">
            Check the overall quality and completeness
            of your dataset.
        </div>
        """)


        quality1, quality2, quality3, quality4 = st.columns(
            4,
            gap="medium"
        )


        with quality1:

            st.html(f"""
            <div class="stat-card">

                <div class="stat-label">
                    COMPLETENESS
                </div>

                <div class="stat-value">
                    {data_quality["completeness"]:.1f}%
                </div>

            </div>
            """)


        with quality2:

            st.html(f"""
            <div class="stat-card">

                <div class="stat-label">
                    MISSING VALUES
                </div>

                <div class="stat-value">
                    {data_quality["total_missing"]}
                </div>

            </div>
            """)


        with quality3:

            st.html(f"""
            <div class="stat-card">

                <div class="stat-label">
                    DUPLICATE ROWS
                </div>

                <div class="stat-value">
                    {data_quality["duplicate_rows"]}
                </div>

            </div>
            """)


        with quality4:

            st.html(f"""
            <div class="stat-card">

                <div class="stat-label">
                    ROWS WITH MISSING
                </div>

                <div class="stat-value">
                    {data_quality["rows_with_missing"]}
                </div>

            </div>
            """)


        # =================================================
        # OUTLIER ANALYSIS
        # =================================================

        st.html("""
        <div class="section-heading">
            ⚠️ Outlier Analysis
        </div>

        <div class="section-description">
            Detect unusual values in numerical columns using
            the Interquartile Range (IQR) method.
        </div>
        """)


        if numerical_columns:

            outlier_found = False


            for column in numerical_columns:

                outliers = detect_outliers(
                    df,
                    column
                )


                if not outliers.empty:

                    outlier_found = True

                    st.warning(
                        f"⚠️ {column}: "
                        f"{len(outliers)} potential "
                        f"outlier(s) detected."
                    )


                    st.dataframe(
                        outliers,
                        use_container_width=True,
                        hide_index=True
                    )


            if not outlier_found:

                st.success(
                    "✓ No potential outliers detected "
                    "in the numerical columns."
                )


        else:

            st.info(
                "No numerical columns are available "
                "for outlier analysis."
            )


        # =================================================
        # INSIGHTS
        # =================================================

        st.html("""
        <div class="section-heading">
            🧠 Data Insights
        </div>

        <div class="section-description">
            Key statistical insights automatically generated
            from the numerical columns in your dataset.
        </div>
        """)


        insights = generate_numerical_insights(
            df,
            numerical_columns
        )


        if insights:

            for insight in insights:

                st.html(f"""
                <div class="stat-card" style="margin-bottom: 12px;">

                    <div style="
                        color: #f8fafc;
                        font-size: 17px;
                        font-weight: 700;
                        margin-bottom: 12px;
                    ">
                        {insight["column"]}
                    </div>

                    <div style="
                        color: #cbd5e1;
                        font-size: 14px;
                        line-height: 1.8;
                    ">

                        Average:

                        <strong style="color:#60a5fa;">
                            {insight["average"]:.2f}
                        </strong>

                        &nbsp;&nbsp;&nbsp;

                        Maximum:

                        <strong style="color:#f59e0b;">
                            {insight["maximum"]:.2f}
                        </strong>

                        &nbsp;&nbsp;&nbsp;

                        Minimum:

                        <strong style="color:#38bdf8;">
                            {insight["minimum"]:.2f}
                        </strong>

                    </div>

                </div>
                """)


        else:

            st.info(
                "No numerical insights are available "
                "for this dataset."
            )


        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        st.html("""
        <div class="success-box">
            ✓ Dataset loaded successfully
        </div>
        """)


        # =================================================
        # DATASET OVERVIEW
        # =================================================

        st.html("""
        <div class="section-heading">
            📊 Dataset Overview
        </div>

        <div class="section-description">
            A quick look at the structure of your dataset.
        </div>
        """)


        rows = df.shape[0]

        columns = df.shape[1]

        numerical_count = len(
            numerical_columns
        )

        categorical_count = sum(
            1
            for column_type in column_types.values()
            if column_type == "categorical"
        )


        stat1, stat2, stat3, stat4 = st.columns(
            4,
            gap="medium"
        )


        with stat1:

            st.html(f"""
            <div class="stat-card">

                <div class="stat-label">
                    ROWS
                </div>

                <div class="stat-value">
                    {rows}
                </div>

            </div>
            """)


        with stat2:

            st.html(f"""
            <div class="stat-card">

                <div class="stat-label">
                    COLUMNS
                </div>

                <div class="stat-value">
                    {columns}
                </div>

            </div>
            """)


        with stat3:

            st.html(f"""
            <div class="stat-card">

                <div class="stat-label">
                    NUMERICAL
                </div>

                <div class="stat-value">
                    {numerical_count}
                </div>

            </div>
            """)


        with stat4:

            st.html(f"""
            <div class="stat-card">

                <div class="stat-label">
                    CATEGORICAL
                </div>

                <div class="stat-value">
                    {categorical_count}
                </div>

            </div>
            """)


        # =================================================
        # DATASET PREVIEW
        # =================================================

        st.html("""
        <div class="section-heading">
            📋 Dataset Preview
        </div>
        """)


        st.dataframe(
            df,
            use_container_width=True,
            height=350
        )


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        st.error(
            f"Unable to read this CSV file: {e}"
        )