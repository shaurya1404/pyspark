# DataFrame GroupBy with Aggregation (MEDIUM)

# Problem
# You are a data analyst on a retail analytics team at Amazon, and the category manager wants to know which products actually drive revenue. From the raw sales transactions, produce one summary row per product.

# - For each product, report total_sales as the revenue it generated (the sum of price * quantity across its transactions) rounded to 2 decimal places, avg_price as the average price across its transactions rounded to 2 decimal places, and transaction_count as how many transactions it appeared in.
# - Rank the products from highest revenue to lowest.

# Input columns: sale_id, product_id, price, quantity, sale_date
# Output columns: product_id, total_sales, avg_price, transaction_count

from pyspark.sql import functions as F

def summary(products):
    return(
        products.groupBy('product_id').agg(F.round(F.sum(F.col('price') * F.col('quantity')), 2).alias('total_sales'), 
                                           F.round(F.avg(F.col('price')), 2).alias('avg_price'),
                                           F.count('*').alias('transaction_count')).orderBy(F.col('total_sales').desc(), 'product_id')
    )

# Note: The groupBy() in .groupBy().agg() is a Shuffle Operation - grouped by column(s) distinct values in one VM
# Note: No need to .drop() at the end since .groupBy().agg() result only contains the grouped by and aggregated columns