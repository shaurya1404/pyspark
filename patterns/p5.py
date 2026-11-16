# Lead and Lag Functions (Medium)

# Problem
# You are a data engineer on the market-data team at a trading analytics platform. 
# Portfolio managers want each day's closing price shown next to the previous and next trading day's closes for the same stock, so they can scan momentum at a glance, plus a daily percentage change that quantifies each move.

# Return every row of stock_prices with three derived columns.
# prev_price is the closing price on the same symbol's immediately earlier trading day, or 0 when there is no earlier day.
# next_price is the closing price on the same symbol's immediately later trading day, or 0 when there is no later day.
# daily_change_pct is the percentage change versus the previous close, computed as (closing_price - previous_close) / previous_close * 100 and rounded to 2 decimal places.
# note the asymmetry on a symbol's first trading day: prev_price is reported as 0, but daily_change_pct must be NULL (not 0) because there is no prior close to compare against.

# Input columns: trade_date, stock_symbol, closing_price
# Output columns: trade_date, stock_symbol, closing_price, prev_price, next_price, daily_change_pct

# Order the result by stock_symbol ascending, then trade_date ascending.

from pyspark.sql import functions as F
from pyspark.sql.window import Window

def stock_change(stock_prices):
    w = Window.partitionBy('stock_symbol').orderBy('trade_date')
    stock_prices = stock_prices.withColumn('trade_date', F.to_date('trade_date')) # converting 'trade_date' type from string to date via to_date()
    return (
        stock_prices.withColumn('prev_price', F.coalesce(F.lag('closing_price').over(w), F.lit(0))) \
            .withColumn('next_price', F.coalesce(F.lead('closing_price').over(w), F.lit(0))) \
            .withColumn('daily_change_pct', F.round(((F.col('closing_price') - F.col('prev_price')) * 100.0) / F.nullif(F.col('prev_price'), 0), 2)) \
            .orderBy('stock_symbol', 'trade_date')
    )

# Note: lag() and lead() both allow additional arguments, so we could've skipped coalesce entirely
# F.lag('closing_price', 1, 0).over(w) - 2nd argument is the offset, 3rd argument is the default when there's no earlier row
