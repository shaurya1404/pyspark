# PySpark Window Functions for Running Totals and Ranking (Medium)

# Problem
# A sales dashboard tracks each product's sales over time.
# Return every sale with running_total, the cumulative amount for that product through sale_date
# Also return sale_rank, its descending amount position where equal amounts share a position and subsequent distinct amounts receive consecutive positions
# Order by product and date.

# Input columns: sale_id, product_id, sale_date, amount
# Output columns: product_id, sale_date, amount, running_total, sale_rank

# Order the result by product_id, sale_date.

from pyspark.sql import functions as F
from pyspark.sql.window import Window

def dashboard(sales):
    w = Window.partitionBy('product_id').orderBy('sale_date').rowsBetween(Window.unboundedPreceding, Window.currentRow)
    return(
        sales.withColumn('running_total', F.sum(F.col('amount')).over(w)) \
            .withColumn('sale_rank', F.dense_rank().over(Window.partitionBy('product_id').orderBy(F.col('amount').desc()))) \
            .orderBy('product_id', 'sale_date')
    )