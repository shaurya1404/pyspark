# Session Timeout Detection (30-min Inactivity) (Medium)

# Problem
# Detect session timeouts by identifying gaps of more than 30 minutes between consecutive user activities. 
# A session ends when inactivity exceeds the threshold, and a new session begins on the user's next activity.

# Group each user's events into sessions: a new session starts at the user's first event, or whenever more than 30 minutes (1800 seconds) have passed since that user's previous event. 
# Session IDs are zero-based per user (the first session is 0), assigned in chronological order.

# For every (user, session) report:
# session_start — timestamp of the first event in the session, returned as text in the format YYYY-MM-DD HH24:MI:SS (e.g. 2024-01-15 08:00:00).
# session_end — timestamp of the last event in the session, returned as text in the same format.
# event_count — number of events in the session.

# Input columns: event_id, user_id, event_timestamp, event_type
# Output columns: user_id, session_id, session_start, session_end, event_count

# session_id identifies the user's chronological session; session_start is the first event timestamp

from pyspark.sql import functions as F
from pyspark.sql.types import LongType
from pyspark.sql.window import Window

def sessionization(events):
    w = Window.partitionBy('user_id').orderBy('event_timestamp')
    w_running = w.rowsBetween(Window.unboundedPreceding, Window.currentRow) # always explicitly state the frame for a running sum
    with_sessions = events.withColumn('prev_ts', F.lag('event_timestamp').over(w)) \
            .withColumn('new_sess_flag', F.when((F.col('event_timestamp').cast(LongType()) - F.col('prev_ts').cast(LongType()) > 1800), F.lit(1)) \
                        .otherwise(F.lit(0))) \
            .withColumn('session_id', F.sum('new_sess_flag').over(w_running))
    return (
        with_sessions.groupBy('user_id', 'session_id') \
            .agg(F.min('event_timestamp').alias('session_start'), F.max('event_timestamp').alias('session_end'), F.count('*').alias('event_count')) \
            .select('user_id', 'session_id', F.date_format(F.col('session_start'), 'yyyy-MM-dd HH:mm:ss').alias('session_start'),
                    F.date_format(F.col('session_end'), 'yyyy-MM-dd HH:mm:ss').alias('session_end'), 'event_count')
    )

# Note: In PySpark, Timestamp casted to Long converts the Timestamp to the number of SECONDS since 1970