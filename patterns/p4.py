# Get Top N Records per Group (Medium)

# Problem
# A regional sales team wants products in the three highest revenue levels within each region.
# Sum revenue by region and product, assign equal totals the same region_rank, and keep ranks 1 through 3. 
# Return region, product name, total revenue, and rank ordered by region and rank.

# Input Columns: sale_id, region, product_name, sale_date, revenue
# Output columns: region, product_name, total_revenue, region_rank

# region_rank is the tie-preserving revenue position within the region.

from pyspark.sql import functions as F
from pyspark.sql.window import Window

def top_three(sales):
    w = Window.partitionBy(F.col('region')).orderBy(F.col('total_revenue').desc())
    return (
        sales.groupBy('region', 'product_name').agg(F.sum('revenue').alias('total_revenue')).withColumn('region_rank', F.dense_rank().over(w)) \
            .filter(F.col('region_rank') <= 3) \
            .orderBy('region', 'region_rank')
    )