import streamlit as st
import pandas as pd
import numpy as np
import io

# ============================================================
# DATA CLEANING PIPELINE - STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Data Cleaning Workbench",
    page_icon="🧹",
    layout="wide"
)

# ============================================================
# CHANGEABLE COLORS
# ============================================================

PRIMARY = "#2563EB"
SUCCESS = "#16A34A"
DANGER = "#DC2626"
WARNING = "#D97706"
TEXT = "#0F172A"
MUTED = "#64748B"
CARD = "#F8FAFC"
BORDER = "#E2E8F0"

st.markdown(
    f"""
    <style>
    .main-title {{
        font-size: 42px;
        font-weight: 800;
        color: {CARD};
        margin-bottom: 0;
    }}

    .subtitle {{
        color: {MUTED};
        font-size: 17px;
        margin-bottom: 25px;
    }}

    .metric-card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 18px;
        min-height: 105px;
    }}

    .metric-label {{
        color: {MUTED};
        font-size: 14px;
    }}

    .metric-value {{
        color: {TEXT};
        font-size: 28px;
        font-weight: 750;
        margin-top: 6px;
    }}

    .stButton > button {{
        border-radius: 8px;
        font-weight: 600;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SESSION STATE
# ============================================================

if "raw_df" not in st.session_state:
    st.session_state.raw_df = None

if "clean_df" not in st.session_state:
    st.session_state.clean_df = None

if "pipeline_log" not in st.session_state:
    st.session_state.pipeline_log = []

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def missing_report(df):
    report = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": df.isna().sum().values,
        "Missing %": (df.isna().mean().values * 100).round(2),
        "Data Type": df.dtypes.astype(str).values,
        "Unique Values": [df[c].nunique(dropna=True) for c in df.columns]
    })
    return report.sort_values("Missing Count", ascending=False)


def quality_metrics(df):
    return {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing": int(df.isna().sum().sum()),
        "Duplicates": int(df.duplicated().sum())
    }


def add_log(message):
    st.session_state.pipeline_log.append(message)


def read_uploaded_file(uploaded_file):
    name = uploaded_file.name.lower()

    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)

    return None


def dataframe_to_excel(df):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Cleaned_Data")

    return output.getvalue()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🧹 Cleaning Workbench")

page = st.sidebar.radio(
    "Pipeline",
    [
        "📁 Upload & Overview",
        "🔎 Data Quality",
        "🧹 Cleaning",
        "📊 Before vs After",
        "📤 Export"
    ]
)

st.sidebar.divider()

if st.session_state.clean_df is not None:
    st.sidebar.success("Dataset loaded")
else:
    st.sidebar.info("Upload a dataset to begin.")

st.sidebar.divider()

st.sidebar.caption(
    "Tip: Keep the raw dataset unchanged and apply cleaning operations to the working copy."
)

# ============================================================
# UPLOAD & OVERVIEW
# ============================================================

if page == "📁 Upload & Overview":

    st.markdown(
        '<div class="main-title">🧹 Data Cleaning Workbench</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Upload, profile, clean, validate and export your dataset.</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:

        try:
            new_df = read_uploaded_file(uploaded_file)

            if new_df is None:
                st.error("Unsupported file format.")
            elif new_df.empty:
                st.error("The uploaded dataset is empty.")
            else:
                # Load only when a new file is selected.
                if (
                    st.session_state.clean_df is None
                    or st.session_state.source_name != uploaded_file.name
                ):
                    st.session_state.raw_df = new_df.copy()
                    st.session_state.clean_df = new_df.copy()
                    st.session_state.pipeline_log = [
                        f"Loaded dataset: {uploaded_file.name}"
                    ]
                    st.session_state.source_name = uploaded_file.name

                df = st.session_state.clean_df
                metrics = quality_metrics(df)

                c1, c2, c3, c4 = st.columns(4)

                values = [
                    ("Rows", f"{metrics['Rows']:,}"),
                    ("Columns", f"{metrics['Columns']:,}"),
                    ("Missing Values", f"{metrics['Missing']:,}"),
                    ("Duplicates", f"{metrics['Duplicates']:,}")
                ]

                for col, (label, value) in zip([c1, c2, c3, c4], values):
                    with col:
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">{label}</div>
                                <div class="metric-value">{value}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                st.write("")
                st.subheader("👀 Dataset Preview")

                st.dataframe(
                    df.head(100),
                    use_container_width=True,
                    hide_index=True
                )

                st.subheader("📋 Column Information")

                info = pd.DataFrame({
                    "Column": df.columns,
                    "Data Type": df.dtypes.astype(str).values,
                    "Non-Null": df.notna().sum().values,
                    "Null": df.isna().sum().values,
                    "Unique": [df[c].nunique(dropna=True) for c in df.columns]
                })

                st.dataframe(
                    info,
                    use_container_width=True,
                    hide_index=True
                )

        except Exception as e:
            st.error(f"Could not read the file: {e}")

# ============================================================
# DATA QUALITY
# ============================================================

elif page == "🔎 Data Quality":

    st.title("🔎 Data Quality Report")

    if st.session_state.clean_df is None:
        st.warning("Please upload a dataset first.")
        st.stop()

    df = st.session_state.clean_df

    metrics = quality_metrics(df)

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("Rows", metrics["Rows"]),
        ("Columns", metrics["Columns"]),
        ("Missing Values", metrics["Missing"]),
        ("Duplicate Rows", metrics["Duplicates"])
    ]

    for col, (label, value) in zip([c1, c2, c3, c4], cards):
        with col:
            st.metric(label, value)

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "❓ Missing Values",
            "♻️ Duplicates",
            "🔤 Data Types",
            "📈 Statistics"
        ]
    )

    with tab1:
        report = missing_report(df)

        st.dataframe(
            report,
            use_container_width=True,
            hide_index=True
        )

        missing_only = report[report["Missing Count"] > 0]

        if missing_only.empty:
            st.success("✅ No missing values found.")
        else:
            st.warning(
                f"{len(missing_only)} column(s) contain missing values."
            )

    with tab2:
        duplicate_count = int(df.duplicated().sum())

        if duplicate_count == 0:
            st.success("✅ No duplicate rows found.")
        else:
            st.warning(
                f"Found {duplicate_count:,} duplicate row(s)."
            )

            st.dataframe(
                df[df.duplicated(keep=False)].head(100),
                use_container_width=True,
                hide_index=True
            )

    with tab3:
        dtype_report = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Example": [
                df[c].dropna().iloc[0] if df[c].notna().any() else "No value"
                for c in df.columns
            ]
        })

        st.dataframe(
            dtype_report,
            use_container_width=True,
            hide_index=True
        )

    with tab4:
        numeric = df.select_dtypes(include=np.number)

        if numeric.empty:
            st.info("No numeric columns found.")
        else:
            st.dataframe(
                numeric.describe().T,
                use_container_width=True
            )

# ============================================================
# CLEANING
# ============================================================

elif page == "🧹 Cleaning":

    st.title("🧹 Cleaning Pipeline")

    if st.session_state.clean_df is None:
        st.warning("Please upload a dataset first.")
        st.stop()

    df = st.session_state.clean_df

    operation = st.selectbox(
        "Choose a cleaning operation",
        [
            "Remove Duplicate Rows",
            "Handle Missing Values",
            "Clean Text Columns",
            "Convert Data Type",
            "Rename Column",
            "Remove Columns",
            "Handle Outliers (IQR)",
            "Remove Constant Columns"
        ]
    )

    st.divider()

    # --------------------------------------------------------
    # DUPLICATES
    # --------------------------------------------------------

    if operation == "Remove Duplicate Rows":

        count = int(df.duplicated().sum())

        st.write(f"Duplicate rows found: **{count:,}**")

        if st.button("♻️ Remove Duplicates"):

            if count == 0:
                st.info("No duplicate rows to remove.")
            else:
                before = len(df)
                st.session_state.clean_df = (
                    df.drop_duplicates()
                    .reset_index(drop=True)
                )
                removed = before - len(st.session_state.clean_df)

                add_log(f"Removed {removed:,} duplicate rows.")

                st.success(
                    f"✅ Removed {removed:,} duplicate rows."
                )
                st.rerun()

    # --------------------------------------------------------
    # MISSING VALUES
    # --------------------------------------------------------

    elif operation == "Handle Missing Values":

        columns_with_missing = [
            c for c in df.columns if df[c].isna().any()
        ]

        if not columns_with_missing:
            st.success("✅ No missing values found.")
        else:

            col = st.selectbox(
                "Select column",
                columns_with_missing
            )

            strategy = st.selectbox(
                "Choose strategy",
                [
                    "Drop rows",
                    "Fill with Mean",
                    "Fill with Median",
                    "Fill with Mode",
                    "Fill with Custom Value"
                ]
            )

            custom_value = None

            if strategy == "Fill with Custom Value":
                custom_value = st.text_input(
                    "Custom value"
                )

            if st.button("🧹 Apply Missing Value Treatment"):

                work = df.copy()

                if strategy == "Drop rows":
                    work = work.dropna(subset=[col])

                elif strategy == "Fill with Mean":

                    if not pd.api.types.is_numeric_dtype(work[col]):
                        st.error("Mean can only be used with numeric columns.")
                        st.stop()

                    work[col] = work[col].fillna(work[col].mean())

                elif strategy == "Fill with Median":

                    if not pd.api.types.is_numeric_dtype(work[col]):
                        st.error("Median can only be used with numeric columns.")
                        st.stop()

                    work[col] = work[col].fillna(work[col].median())

                elif strategy == "Fill with Mode":

                    mode = work[col].mode()

                    if mode.empty:
                        st.error("No mode available for this column.")
                        st.stop()

                    work[col] = work[col].fillna(mode.iloc[0])

                elif strategy == "Fill with Custom Value":

                    if custom_value == "":
                        st.error("Enter a custom value.")
                        st.stop()

                    work[col] = work[col].fillna(custom_value)

                st.session_state.clean_df = work

                add_log(
                    f"Missing values handled in '{col}' using '{strategy}'."
                )

                st.success(
                    f"✅ Applied '{strategy}' to '{col}'."
                )
                st.rerun()

    # --------------------------------------------------------
    # TEXT CLEANING
    # --------------------------------------------------------

    elif operation == "Clean Text Columns":

        text_columns = df.select_dtypes(
            include=["object", "string"]
        ).columns.tolist()

        if not text_columns:
            st.info("No text columns found.")
        else:

            col = st.selectbox(
                "Select text column",
                text_columns
            )

            actions = st.multiselect(
                "Select cleaning actions",
                [
                    "Strip Whitespace",
                    "Convert to Lowercase",
                    "Convert to Uppercase"
                ],
                default=["Strip Whitespace"]
            )

            if st.button("✨ Clean Text"):

                work = df.copy()

                series = work[col].astype("string")

                if "Strip Whitespace" in actions:
                    series = series.str.strip()

                if "Convert to Lowercase" in actions:
                    series = series.str.lower()

                if "Convert to Uppercase" in actions:
                    series = series.str.upper()

                work[col] = series

                st.session_state.clean_df = work

                add_log(
                    f"Text cleaned in '{col}': {', '.join(actions)}."
                )

                st.success("✅ Text cleaning applied.")
                st.rerun()

    # --------------------------------------------------------
    # DATA TYPE
    # --------------------------------------------------------

    elif operation == "Convert Data Type":

        col = st.selectbox(
            "Select column",
            df.columns
        )

        target = st.selectbox(
            "Convert to",
            [
                "string",
                "integer",
                "float",
                "datetime"
            ]
        )

        if st.button("🔄 Convert Data Type"):

            work = df.copy()

            try:
                if target == "string":
                    work[col] = work[col].astype("string")

                elif target == "integer":
                    work[col] = pd.to_numeric(
                        work[col],
                        errors="coerce"
                    ).astype("Int64")

                elif target == "float":
                    work[col] = pd.to_numeric(
                        work[col],
                        errors="coerce"
                    )

                elif target == "datetime":
                    work[col] = pd.to_datetime(
                        work[col],
                        errors="coerce"
                    )

                st.session_state.clean_df = work

                add_log(
                    f"Converted '{col}' to {target}."
                )

                st.success(
                    f"✅ '{col}' converted to {target}."
                )
                st.rerun()

            except Exception as e:
                st.error(f"Conversion failed: {e}")

    # --------------------------------------------------------
    # RENAME COLUMN
    # --------------------------------------------------------

    elif operation == "Rename Column":

        col = st.selectbox(
            "Column to rename",
            df.columns
        )

        new_name = st.text_input(
            "New column name"
        )

        if st.button("✏️ Rename Column"):

            new_name = new_name.strip()

            if not new_name:
                st.error("Enter a new column name.")
            elif new_name in df.columns:
                st.error("A column with this name already exists.")
            else:
                work = df.copy()
                work.rename(
                    columns={col: new_name},
                    inplace=True
                )

                st.session_state.clean_df = work

                add_log(
                    f"Renamed column '{col}' to '{new_name}'."
                )

                st.success("✅ Column renamed.")
                st.rerun()

    # --------------------------------------------------------
    # REMOVE COLUMNS
    # --------------------------------------------------------

    elif operation == "Remove Columns":

        selected = st.multiselect(
            "Select columns to remove",
            df.columns
        )

        if st.button("🗑️ Remove Selected Columns"):

            if not selected:
                st.error("Select at least one column.")
            elif len(selected) >= len(df.columns):
                st.error("You cannot remove all columns.")
            else:
                work = df.drop(columns=selected)

                st.session_state.clean_df = work

                add_log(
                    f"Removed columns: {', '.join(selected)}."
                )

                st.success(
                    f"✅ Removed {len(selected)} column(s)."
                )
                st.rerun()

    # --------------------------------------------------------
    # IQR OUTLIERS
    # --------------------------------------------------------

    elif operation == "Handle Outliers (IQR)":

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns.tolist()

        if not numeric_columns:
            st.info("No numeric columns found.")
        else:

            col = st.selectbox(
                "Numeric column",
                numeric_columns
            )

            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outlier_mask = (
                (df[col] < lower)
                | (df[col] > upper)
            )

            outliers = int(outlier_mask.sum())

            st.write(
                f"Lower bound: **{lower:.2f}**"
            )
            st.write(
                f"Upper bound: **{upper:.2f}**"
            )
            st.write(
                f"Potential outliers: **{outliers:,}**"
            )

            strategy = st.radio(
                "Treatment",
                [
                    "Remove outlier rows",
                    "Cap values to IQR limits"
                ]
            )

            if st.button("📌 Apply Outlier Treatment"):

                work = df.copy()

                if strategy == "Remove outlier rows":
                    work = work.loc[
                        ~outlier_mask
                    ].reset_index(drop=True)

                else:
                    work[col] = work[col].clip(
                        lower=lower,
                        upper=upper
                    )

                st.session_state.clean_df = work

                add_log(
                    f"Applied IQR outlier treatment to '{col}': {strategy}."
                )

                st.success("✅ Outlier treatment applied.")
                st.rerun()

    # --------------------------------------------------------
    # CONSTANT COLUMNS
    # --------------------------------------------------------

    elif operation == "Remove Constant Columns":

        constant_columns = [
            c for c in df.columns
            if df[c].nunique(dropna=False) <= 1
        ]

        if not constant_columns:
            st.success("✅ No constant columns found.")
        else:

            st.write(
                "Constant columns detected:"
            )
            st.write(constant_columns)

            selected = st.multiselect(
                "Select columns to remove",
                constant_columns,
                default=constant_columns
            )

            if st.button("🗑️ Remove Constant Columns"):

                if not selected:
                    st.info("No columns selected.")
                elif len(selected) >= len(df.columns):
                    st.error("Cannot remove all columns.")
                else:
                    st.session_state.clean_df = df.drop(
                        columns=selected
                    )

                    add_log(
                        f"Removed constant columns: {', '.join(selected)}."
                    )

                    st.success("✅ Constant columns removed.")
                    st.rerun()

# ============================================================
# BEFORE VS AFTER
# ============================================================

elif page == "📊 Before vs After":

    st.title("📊 Before vs After")

    if st.session_state.raw_df is None:
        st.warning("Please upload a dataset first.")
        st.stop()

    raw = st.session_state.raw_df
    clean = st.session_state.clean_df

    raw_metrics = quality_metrics(raw)
    clean_metrics = quality_metrics(clean)

    c1, c2, c3, c4 = st.columns(4)

    comparisons = [
        (
            "Rows",
            raw_metrics["Rows"],
            clean_metrics["Rows"]
        ),
        (
            "Columns",
            raw_metrics["Columns"],
            clean_metrics["Columns"]
        ),
        (
            "Missing Values",
            raw_metrics["Missing"],
            clean_metrics["Missing"]
        ),
        (
            "Duplicates",
            raw_metrics["Duplicates"],
            clean_metrics["Duplicates"]
        )
    ]

    for col, (label, before, after) in zip(
        [c1, c2, c3, c4],
        comparisons
    ):
        with col:
            st.metric(
                label,
                after,
                delta=after - before
            )

    st.divider()

    comparison_df = pd.DataFrame({
        "Metric": [
            "Rows",
            "Columns",
            "Missing Values",
            "Duplicate Rows"
        ],
        "Before": [
            raw_metrics["Rows"],
            raw_metrics["Columns"],
            raw_metrics["Missing"],
            raw_metrics["Duplicates"]
        ],
        "After": [
            clean_metrics["Rows"],
            clean_metrics["Columns"],
            clean_metrics["Missing"],
            clean_metrics["Duplicates"]
        ]
    })

    st.subheader("📋 Cleaning Summary")

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📝 Pipeline Log")

    if st.session_state.pipeline_log:
        for item in st.session_state.pipeline_log:
            st.write("•", item)
    else:
        st.info("No cleaning operations recorded.")

    st.subheader("👀 Cleaned Dataset Preview")

    st.dataframe(
        clean.head(100),
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# EXPORT
# ============================================================

elif page == "📤 Export":

    st.title("📤 Export Clean Dataset")

    if st.session_state.clean_df is None:
        st.warning("Please upload a dataset first.")
        st.stop()

    clean = st.session_state.clean_df

    st.success(
        f"Your cleaned dataset contains {len(clean):,} rows "
        f"and {len(clean.columns):,} columns."
    )

    csv_data = clean.to_csv(index=False).encode("utf-8")

    excel_data = dataframe_to_excel(clean)

    c1, c2 = st.columns(2)

    with c1:
        st.download_button(
            "⬇️ Download CSV",
            data=csv_data,
            file_name="cleaned_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

    with c2:
        st.download_button(
            "⬇️ Download Excel",
            data=excel_data,
            file_name="cleaned_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.divider()

    st.subheader("📋 Cleaning Report")

    report = missing_report(clean)

    st.dataframe(
        report,
        use_container_width=True,
        hide_index=True
    )

    report_csv = report.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📄 Download Data Quality Report",
        data=report_csv,
        file_name="data_quality_report.csv",
        mime="text/csv"
    )

    st.subheader("📝 Pipeline Log")

    if st.session_state.pipeline_log:
        log_df = pd.DataFrame({
            "Step": range(1, len(st.session_state.pipeline_log) + 1),
            "Operation": st.session_state.pipeline_log
        })

        st.dataframe(
            log_df,
            use_container_width=True,
            hide_index=True
        )

st.divider()
st.caption(
    "🧹 Data Cleaning Workbench | Python + Pandas + Streamlit + Plotly"
)
