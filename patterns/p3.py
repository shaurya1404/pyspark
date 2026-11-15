# Anti-Join: Customers Without Orders (Easy)
# 'customers with no orders, 'users with no events', 'files that never arrived'

# Problem
# The marketing team wants to re-engage customers who registered but have never placed a single order. 
# From the customers and orders tables, return every customer who does not appear as the buyer on any order. 
# For each such customer, report their customer_id, customer_name, and signup_date. List each qualifying customer once, ordered by customer_id ascending.

# Input columns: customers -> ; orders ->
# Output columns: customer_id, customer_name, signup_date

# Order the result by customer_id

from pyspark.sql import functions as F

def cust_no_orders(customers, orders):
    return(
        customers.join(orders, customers.customer_id == orders.customer_id, 'anti').select('customer_id', 'customer_name', 'signup_date') \
        .orderBy(F.col('customer_id'))
    )

# **Note: left vs. semi vs. anti join**

# All three keep rows from the LEFT table; they differ in what they return:

# | Join   | Keeps                                  | Columns returned | Can duplicate left rows? |
# |--------|----------------------------------------|------------------|------------------------|
# | `left` | All left rows (nulls where no match)   | Left + right     | Yes, one row per match |
# | `semi` | Left rows WITH a match                 | Left only        | No |
# | `anti` | Left rows WITHOUT a match              | Left only        | No |

# semi + anti together = the whole left table, with no overlap.