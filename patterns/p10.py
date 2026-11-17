# Pivot Table Reshaping (Medium)

# Problem
# You are a data analyst at Google building a regional sales dashboard.
# Sales arrive one row per transaction, but the dashboard needs a wide layout with one row per region and each product's revenue in its own column.

# For every region, report the total amount for Product_A, Product_B, and Product_C as three separate columns, using 0 when the region had no sales of that product.
# Also report grand_total, the total amount across all products in the region.
# Round every total to 2 decimal places and list regions in ascending alphabetical order.

# Input columns: sale_id, region, product, sale_date, amount
# Output columns: region, Product_A_total, Product_B_total, Product_C_total, grand_total

from pyspark.sql import functions as F

def pivot(sales):
    products = ['Product_A', 'Product_B', 'Product_C']
    wide = sales.groupBy('region').pivot('product', products).agg(F.round(F.sum('amount'), 2)).fillna(0)
    totals = sales.groupBy('region').agg(F.round((F.sum('amount')), 2).alias('grand_total'))

    return (
        wide.join(totals, 'region').select('region', *[F.col(p).alias(f'{p}_total') for p in products], 'grand_total').orderBy('region')
    )

# Note: Prefer always providing an explicit list for the row values of the Pivoted column since otherwise, the engine has to perform a Full-Table-Scan
# Note: Joining via 'wide.region == totals.region' results in two of the same columns in the dataframe. So, prefer passing the common column simply as a string

# Note: With a single aggregation, Spark ignores the alias inside .agg() and names the columns directly as the pivoted values ('Pivoted_A').
# The alias only applies when you pass two or more aggregations. Each column is then named {pivot value}_{alias}