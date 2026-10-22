from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "sales.csv"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_data(path: Path) -> pd.DataFrame:
    """Load sales data from a CSV file."""
    return pd.read_csv(path)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply basic, transparent cleaning rules."""
    df = df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for col in ["quantity", "unit_price", "revenue"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove exact duplicate rows, then rows missing essential fields.
    df = df.drop_duplicates()
    df = df.dropna(subset=[
        "order_id", "order_date", "city", "product",
        "quantity", "unit_price", "revenue"
    ])
    # Keep plausible positive sales records.
    df = df[(df["quantity"] > 0) & (df["unit_price"] >= 0)]
    # Recalculate revenue so inconsistent source values don't persist.
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df

def create_reports(df: pd.DataFrame) -> None:
    """Print insights and save useful CSV summaries."""
    df = df.copy()
    df["month"] = df["order_date"].dt.to_period("M").astype(str)

    total_revenue = df["revenue"].sum()
    total_orders = df["order_id"].nunique()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    print("\n=== SALES SUMMARY ===")
    print(f"Rows analyzed: {len(df)}")
    print(f"Unique orders: {total_orders}")
    print(f"Total revenue: ₹{total_revenue:,.2f}")
    print(f"Average revenue per order: ₹{avg_order_value:,.2f}")

    monthly = df.groupby("month", as_index=False)["revenue"].sum()
    monthly = monthly.sort_values("month")
    by_product = df.groupby("product", as_index=False).agg(
        units_sold=("quantity", "sum"),
        revenue=("revenue", "sum")
    ).sort_values("revenue", ascending=False)
    by_city = df.groupby("city", as_index=False)["revenue"].sum()
    by_city = by_city.sort_values("revenue", ascending=False)

    monthly.to_csv(OUTPUT_DIR / "monthly_sales.csv", index=False)
    by_product.to_csv(OUTPUT_DIR / "product_summary.csv", index=False)
    by_city.to_csv(OUTPUT_DIR / "city_summary.csv", index=False)
    df.to_csv(OUTPUT_DIR / "cleaned_sales.csv", index=False)

    if not monthly.empty:
        peak = monthly.loc[monthly["revenue"].idxmax()]
        print(f"Highest-revenue month: {peak['month']} (₹{peak['revenue']:,.2f})")
    if not by_product.empty:
        top = by_product.iloc[0]
        print(f"Top product by revenue: {top['product']} (₹{top['revenue']:,.2f})")
    if not by_city.empty:
        top_city = by_city.iloc[0]
        print(f"Top city by revenue: {top_city['city']} (₹{top_city['revenue']:,.2f})")

    print(f"\nReports saved in: {OUTPUT_DIR}")

def main():
    raw = load_data(INPUT_FILE)
    print(f"Loaded {len(raw)} rows.")
    clean = clean_data(raw)
    print(f"After cleaning: {len(clean)} rows.")
    create_reports(clean)

if __name__ == "__main__":
    main()
