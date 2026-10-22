# Sales Data Analysis System

A beginner-friendly Python + Pandas project that cleans sales records and creates summary reports.

## Features
- Loads sales records from CSV
- Converts dates and numeric columns
- Removes exact duplicates and rows missing essential values
- Filters non-positive quantities
- Recalculates revenue as quantity × unit price
- Reports total revenue, unique orders, average revenue per order, highest-revenue month, top product, and top city
- Exports cleaned data and three summary CSV reports

## Tech stack
- Python 3.12+
- Pandas

## Dataset
`data/sales.csv` contains 250 **synthetic sample records** created for this project. It is not real company data.

## Setup
1. Install Python.
2. Open this project folder in VS Code.
3. Open VS Code Terminal (**Terminal → New Terminal**).
4. Install dependency:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Run:

   ```bash
   python src/analysis.py
   ```

If `python` is not recognized on your system, try `py src/analysis.py`.

## Outputs
After running, the `output/` folder will contain:
- `cleaned_sales.csv`
- `monthly_sales.csv`
- `product_summary.csv`
- `city_summary.csv`

## Data quality notes
This is a learning project. The current cleaning rules are simple and explicit; in real datasets, investigate suspicious records instead of deleting data automatically. `order_id` is treated as an order identifier, and the demo data uses one row per order.

## Future improvements
- Add data-quality checks and a cleaning log
- Create visualizations with Matplotlib
- Add unit tests
- Load data into a SQL database
- Automate the pipeline
