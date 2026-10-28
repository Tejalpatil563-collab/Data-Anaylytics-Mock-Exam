
import numpy as np
import pandas as pd

# --------------------------------------------------
# 1. DATA LAYER
# --------------------------------------------------
rng = np.random.default_rng(42)
n = 5000

df = pd.DataFrame({
    "date": (
        pd.to_datetime("2025-01-01")
        + pd.to_timedelta(
            rng.integers(0, 365, n),
            unit="D"
        )
    ),
    "region": rng.choice(
        ["North", "South", "East", "West"], n
    ),
    "category": rng.choice(
        ["Electronics", "Clothing", "Home", "Sports"], n
    ),
    "units": rng.integers(1, 10, n),
    "unit_price": rng.uniform(10, 200, n).round(2)
})

df["revenue"] = df["units"] * df["unit_price"]

# --------------------------------------------------
# 2. SALES PERFORMANCE DASHBOARD
# --------------------------------------------------
print("=" * 55)
print("          SALES PERFORMANCE DASHBOARD")
print("=" * 55)

# --------------------------------------------------
# 3. FILTERS
# --------------------------------------------------
print("\nAvailable Regions:")
print(", ".join(sorted(df["region"].unique())))

print("\nAvailable Categories:")
print(", ".join(sorted(df["category"].unique())))

region_input = input(
    "\nEnter regions separated by comma (or ALL): "
).strip()

category_input = input(
    "Enter categories separated by comma (or ALL): "
).strip()

start_input = input(
    "Enter start date (YYYY-MM-DD or ENTER for all): "
).strip()

end_input = input(
    "Enter end date (YYYY-MM-DD or ENTER for all): "
).strip()

# Apply region filter
if region_input and region_input.upper() != "ALL":
    selected_regions = [
        x.strip().title()
        for x in region_input.split(",")
    ]
    df = df[df["region"].isin(selected_regions)]

# Apply category filter
if category_input and category_input.upper() != "ALL":
    selected_categories = [
        x.strip().title()
        for x in category_input.split(",")
    ]
    df = df[df["category"].isin(selected_categories)]

# Apply date filter
if start_input:
    df = df[df["date"] >= pd.to_datetime(start_input)]

if end_input:
    df = df[
        df["date"] <= (
            pd.to_datetime(end_input) + pd.Timedelta(days=1)
            - pd.Timedelta(seconds=1)
        )
    ]

# --------------------------------------------------
# 4. KPI CARDS
# --------------------------------------------------
print("\n" + "=" * 55)
print("                    KPI SUMMARY")
print("=" * 55)

if df.empty:
    print("No data available for the selected filters.")

else:
    total_revenue = df["revenue"].sum()
    total_orders = len(df)
    avg_order_value = df["revenue"].mean()
    total_units = df["units"].sum()

    print(f"Total Revenue   : ${total_revenue:,.2f}")
    print(f"Orders          : {total_orders:,}")
    print(f"Avg Order Value : ${avg_order_value:,.2f}")
    print(f"Units Sold      : {total_units:,}")

    # --------------------------------------------------
    # 5. MONTHLY REVENUE TREND
    # --------------------------------------------------
    print("\n" + "=" * 55)
    print("             MONTHLY REVENUE TREND")
    print("=" * 55)

    monthly = (
        df.set_index("date")
        .resample("MS")["revenue"]
        .sum()
    )

    print(monthly.round(2).to_string())

    # --------------------------------------------------
    # 6. REVENUE BY CATEGORY
    # --------------------------------------------------
    print("\n" + "=" * 55)
    print("              REVENUE BY CATEGORY")
    print("=" * 55)

    category_summary = (
        df.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    print(category_summary.round(2).to_string())

    # --------------------------------------------------
    # 7. REVENUE BY REGION
    # --------------------------------------------------
    print("\n" + "=" * 55)
    print("               REVENUE BY REGION")
    print("=" * 55)

    region_summary = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    print(region_summary.round(2).to_string())

    # --------------------------------------------------
    # 8. FINAL SUMMARY
    # --------------------------------------------------
    print("\n" + "=" * 55)
    print("                 FINAL SUMMARY")
    print("=" * 55)

    print("Highest Revenue Category:", category_summary.idxmax())
    print("Highest Revenue Region  :", region_summary.idxmax())
    print("Total Records Analyzed  :", len(df))

print("\n==== SALES ANALYSIS COMPLETED SUCCESSFULLY ====")
