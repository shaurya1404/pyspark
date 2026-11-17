# SCD Type 2 Historical Table (Hard)

# Problem
# A customer table stores one row every time a customer's status changes, stamped with the modified_date of that change.
# Build the Slowly Changing Dimension (SCD) Type 2 history: one row per status version per customer, showing the window during which that status was in effect.

# For each version, valid_from is the modified_date when the status took effect, and valid_to is the modified_date of that customer's next status change.
# The most recent version of each customer has no next change, so its valid_to is NULL and its is_current flag is 'Y'; every earlier version has is_current set to 'N'.

# Input columns: id, name, status, modified_date
# Output columns: id, name, status, valid_from, valid_to, is_current

# Sort output by id, then valid_from ascending

from pyspark.sql import functions as F
from pyspark.sql.window import Window

def scd_t2(customers):
    w = Window.partitionBy('id').orderBy('valid_from')
    return (
        customers.withColumnRenamed('modified_date', 'valid_from').withColumn('valid_to', F.lead('valid_from').over(w)) \
            .withColumn('is_current', F.when(F.col('valid_to').isNull(), 'Y').otherwise('N'))
            .orderBy('id', 'valid_from')
    )