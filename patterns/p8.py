# Gap and Island Detection (Hard)

# Problem
# An activity log records the dates on which each user generated an event.
# Split each user's activity into islands of strictly consecutive calendar dates: any missing date starts a new island.
# For each island, return its global island_id, first and last dates, and number of active dates, ordered by user_id and start_date; island_id follows that same order starting at 1.

# Input columns: event_id, user_id, event_date
# Output columns: user_id, island_id, start_date, end_date, consecutive_days

from pyspark.sql import functions as F
from pyspark.sql.window import Window

def gaps_and_islands(events):
    w = Window.partitionBy('user_id').orderBy('event_date')
    surr_key = Window.orderBy('user_id', 'start_date')
    return (
        events.dropDuplicates(['user_id', 'event_date']).withColumn('enumerated', F.row_number().over(w)) # dropDuplicates on user_id, not event_id
            .withColumn('grouped', F.col('event_date') - F.col('enumerated')) \
            .groupBy('user_id', 'grouped').agg(F.min('event_date').alias('start_date'), F.max('event_date').alias('end_date'), F.count('*').alias('consecutive_days')) \
            .withColumn('island_id', F.row_number().over(surr_key)) \
            .select('user_id', 'island_id', 'start_date', 'end_date', 'consecutive_days') \
            .orderBy('user_id', 'start_date')
    )

# Note: island_id is to be implemented as a surrogate key to uniquely identify each new island after aggreagtion
# Note: Used .select() in the end to filter out unnecessary columns AND re-order the final columns
# Note: F.expr("date_sub(event_date, enumerated)") works too - F.expr() turns a SQL expression into a Column (spark.sql() is used for an entire query and returns an entire Dataframe)