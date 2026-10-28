import numpy as np
import pandas as pd

FILE_PATH = None
DATE_COLUMN = "order_date"
GROUP_COLUMN = "region"
TARGET_COLUMN = "sales"

# --------------------------------------------------
# STEP 1: CREATE SAMPLE DATA
# --------------------------------------------------
def make_sample_data(n=600, seed=42):
    rng = np.random.default_rng(seed)

    dates = pd.date_range(
        "2023-01-01",
        periods=n,
        freq="D"
    )

    sales = (
        np.linspace(100, 200, n)
        + 15 * np.sin(np.arange(n) / 30)
        + rng.normal(0, 12, n)
    )

    # Add some outliers
    sales[rng.choice(n, 6, replace=False)] *= 2.5

    data = pd.DataFrame({
        "order_date": dates,
        "sales": sales,
        "units": rng.poisson(25, n),
        "price": rng.normal(50, 7, n),
        "region": rng.choice(
            ["North", "South", "East", "West"],
            n,
            p=[0.35, 0.25, 0.25, 0.15]
        )
    })

    # Add missing values
    data.loc[
        rng.choice(n, 25, replace=False),
        "price"
    ] = np.nan

    return data


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
if FILE_PATH is None:
    df = make_sample_data()
elif FILE_PATH.lower().endswith((".xlsx", ".xls")):
    df = pd.read_excel(FILE_PATH)
else:
    df = pd.read_csv(FILE_PATH)

# Convert date column
if DATE_COLUMN and DATE_COLUMN in df.columns:
    df[DATE_COLUMN] = pd.to_datetime(
        df[DATE_COLUMN],
        errors="coerce"
    )


# --------------------------------------------------
# STEP 2: FIRST LOOK AT DATA
# --------------------------------------------------
print("\n===== STEP 2: FIRST LOOK AT THE DATA =====")
print("Shape (rows, columns):", df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

num_cols = df.select_dtypes(
    include="number"
).columns.tolist()

cat_cols = [
    c for c in df.columns
    if c not in num_cols
    and not pd.api.types.is_datetime64_any_dtype(df[c])
]

print("\nNumeric columns:", num_cols)
print("Categorical columns:", cat_cols)


# --------------------------------------------------
# STEP 3: DATA QUALITY
# --------------------------------------------------
print("\n===== STEP 3: DATA QUALITY =====")

missing = df.isnull().sum()

print("\nMissing values:")
if missing.sum() > 0:
    print(missing[missing > 0])
else:
    print("No missing values")

print("\nDuplicate rows:", df.duplicated().sum())


# --------------------------------------------------
# STEP 4: DESCRIPTIVE STATISTICS
# --------------------------------------------------
print("\n===== STEP 4: DESCRIPTIVE STATISTICS =====")

summary = df[num_cols].describe().T
summary["median"] = df[num_cols].median()
summary["variance"] = df[num_cols].var()
summary["IQR"] = summary["75%"] - summary["25%"]
summary["skewness"] = df[num_cols].skew()

print(summary.round(2))

# Identify distribution shape
for col in num_cols:
    sk = summary.loc[col, "skewness"]

    if sk > 0.5:
        shape = "right-skewed"
    elif sk < -0.5:
        shape = "left-skewed"
    else:
        shape = "roughly symmetric"

    print(f"{col}: {shape}")

# Frequency counts for categorical columns
for col in cat_cols:
    print(f"\nCounts for '{col}':")
    print(df[col].value_counts())
    
# --------------------------------------------------
# STEP 5: DISTRIBUTIONS
# --------------------------------------------------
print("\n===== STEP 5: DISTRIBUTIONS =====")

print("\nSales Mean:", df[TARGET_COLUMN].mean())
print("Sales Median:", df[TARGET_COLUMN].median())
print("Sales Minimum:", df[TARGET_COLUMN].min())
print("Sales Maximum:", df[TARGET_COLUMN].max())

print("\nSales Distribution:")
print(df[TARGET_COLUMN].describe())


# --------------------------------------------------
# STEP 6: OUTLIERS
# --------------------------------------------------
print("\n===== STEP 6: OUTLIERS =====")

for col in num_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1

    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr

    count = (
        (df[col] < low) |
        (df[col] > high)
    ).sum()

    print(
        f"{col:>10}: "
        f"normal range = [{low:.2f}, {high:.2f}] "
        f"-> outliers = {count}"
    )

q1 = df[TARGET_COLUMN].quantile(0.25)
q3 = df[TARGET_COLUMN].quantile(0.75)
iqr = q3 - q1

outliers = df[
    (df[TARGET_COLUMN] < q1 - 1.5 * iqr) |
    (df[TARGET_COLUMN] > q3 + 1.5 * iqr)
]

print(f"\nOutlier rows in '{TARGET_COLUMN}':")
print(outliers.head(10))


# --------------------------------------------------
# STEP 7: CORRELATION
# --------------------------------------------------
print("\n===== STEP 7: CORRELATION =====")

corr = df[num_cols].corr()
print(corr.round(2))


# --------------------------------------------------
# STEP 8: GROUP ANALYSIS
# --------------------------------------------------
if GROUP_COLUMN and GROUP_COLUMN in df.columns:
    print(
        f"\n===== STEP 8: "
        f"{TARGET_COLUMN} BY {GROUP_COLUMN} ====="
    )

    group_summary = (
        df.groupby(GROUP_COLUMN)[TARGET_COLUMN]
        .agg([
            "count",
            "mean",
            "median",
            "std",
            "min",
            "max"
        ])
        .round(2)
    )

    print(group_summary)


# --------------------------------------------------
# STEP 9: TIME TREND
# --------------------------------------------------
if DATE_COLUMN and DATE_COLUMN in df.columns:
    print(
        f"\n===== STEP 9: TREND OF "
        f"{TARGET_COLUMN} OVER TIME ====="
    )

    ts = (
        df.dropna(subset=[DATE_COLUMN])
        .set_index(DATE_COLUMN)[TARGET_COLUMN]
    )

    monthly = ts.resample("ME").mean()
    monthly = monthly.dropna()

    rolling = monthly.rolling(
        window=3,
        min_periods=1
    ).mean()

    if len(monthly) >= 2:
        x = np.arange(len(monthly))

        slope, intercept = np.polyfit(
            x,
            monthly.values,
            1
        )

        r_squared = np.corrcoef(
            x,
            monthly.values
        )[0, 1] ** 2

        if slope > 0:
            direction = "UPWARD"
        elif slope < 0:
            direction = "DOWNWARD"
        else:
            direction = "FLAT"

        print("Trend direction:", direction)
        print(f"Slope: {slope:.2f} per month")
        print(f"R-squared: {r_squared:.2f}")

    print("\nMonthly Average:")
    print(monthly)

    print("\n3-Month Rolling Average:")
    print(rolling)

print("\n==== EDA COMPLETED SUCCESSFULLY ====")
