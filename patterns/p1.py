# Conditional Column Creation (EASY)

# Problem
# An operations team triages incoming orders. For each order, classify its size, flag whether it ships express, and compute a priority score used to rank the queue.

# The order size is "small" when the amount is below 50, "medium" when the amount is between 50 and 200 inclusive, and "large" when the amount is above 200. The express flag is 1 when the shipping type is express and 0 otherwise. The priority score equals the amount divided by 100, plus an extra 10 points when the order ships express, rounded to 2 decimals. Return every order ordered from the highest priority score to the lowest.

# Input columns: order_id, customer_id, amount, shipping_type
# Output columns: order_id, customer_id, amount, shipping_type, order_size, is_express, priority_score

from pyspark.sql import functions as F

def etl(orders):
    return (
        orders.withColumn('order_size', F.when(F.col('amount') > 200, 'large').when(F.col('amount') >= 50, 'medium').otherwise('small')) \
        .withColumn('is_express', F.when(F.col('shipping_type') == 'express', 1).otherwise(0)) \
        .withColumn('priority_score', F.round((F.col('amount') / 100.0) + (10 * F.col('is_express')), 2)) \
        .orderBy(F.col('priority_score').desc())
    )