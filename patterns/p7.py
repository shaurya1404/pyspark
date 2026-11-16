# Deduplication with Latest Record Priority (Medium)

# Problem
# Customer records are ingested repeatedly, so the same customer can appear multiple times with different versions of their contact details. Collapse the table down to one row per customer, keeping only that customer's latest version as determined by updated_at.

# For every customer, return their most recent email, phone, and updated_at. The updated_at value must be returned as text in the format YYYY-MM-DD HH24:MI:SS (e.g. 2024-01-15 14:30:00).

# Input columns: record_id, customer_id, email, phone, updated_at
# Output columns: customer_id, email, phone, updated_at

# Sort the results by customer_id ascending.

from pyspark.sql import functions as F
from pyspark.sql.window import Window

def deduped(customers):
    w = Window.partitionBy('customer_id').orderBy(F.col('updated_at').desc())
    return (
        customers.withColumn('latest', F.row_number().over(w)).filter(F.col('latest') == 1).drop('record_id', 'latest') \
            .withColumn('updated_at', F.date_format(F.col('updated_at'), 'yyyy-MM-dd HH:mm:ss')) \
            .orderBy('customer_id')
    )

# Note: If 'updated_at' is in text format, convert it to Timestamp via F.to_timestamp() before creating the ranking column
# In date_format(), 'HH' -> 24 hours and 'hh' -> 12 hours