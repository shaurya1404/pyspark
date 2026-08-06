# PySpark

## What is Spark? Why does it exist?

- Up until now,I was pewrforming SQL operations on a single system in order to transform, clean, and load data. However, a single system in and of itself will have resource constraints - say 16GB RAM with 8 cores.

- So, as data increases, resources have a ceiling limit to perform the operations. When handling big data such as terabytes or petabytes of data, things will really start to slow down.

- Now, the trivial solution is to vertically scale - improve the resources of the single-system. However, this isn't scalable nor cost-effective as that too will hit a limit aftter a certain point and would also lead to wasted resources when data scales down to use lesser sizes.

- Hence, the more optimal solution is Horizontal Scaling - Use 20 not-so-fancy systems in order to process the data by partitioning it into subsets of data. This is exaclty what Spark does.

- Spark is a distributed compute engine which allows processing of big data in a much more manageable and scalable manner. It processes data across multiple machines. It does NOT store data at any point; It's stateless. You point it at files sitting in S3 or a Delta/Iceberg table, it reads them, computes, writes results back out, and forgets everything.

This delineation between storage and processing is what makes it extremely powerful. It means your storage layer (cheap, durable, always-on) and your compute layer (expensive, elastic, spun up on demand) scale independently.

PySpark is a reference to the Python API that Spark exposes which allows one to write Python in order to use Spark

## Spark Architecture

There are essentially three 'roles' that are running in a Spark application:

1) Driver: It schedules the work. It holds the SparkSession, builds the execution plan, and runs the complete Python script. It exists because you started a job, and it dies when that job finishes.

2) Cluster Manager: It schedule the infrastructure. It is a machine that was running even before the job was created and will continue to run after it's been completed. It has no idea what Spark is. It's a landlord with a pool of machines a portion of which it provides to the Driver based on how much it needs and whether it has the permission to access them.

3) Executors: The individual worker nodes that are spun up by the Clsuter Manager and given to the Driver to delegate tasks to. The Driver is the Orchestrator. The executor nodes are the ones that actually perform the tasks.

- The relationship between the Driver and Executors is known as a Master-Slave architecture.

***Note***: Machines are called Nodes in Spark parlance

- The Cluster Manager: "Who needs how many CPUs and how much RAM, and are they allowed to have it?"
- The Driver: "I need 20 containers, 4 cores and 16 GB each."
- The Cluster Manager: Checks capacity and quotas, finds space on physical machines, and launches executor nodes. Exits the loop.

## Lazy Evaluation

Operations in Spark can be split into two types: 1. Transformations (select, filter, join, groupBy, withColumn) are LAZY. None of these are executed immediately when they're read. They are all added in the Logical Plan. 2. Actions (show, count, collect, write, take) are EAGER. They force the entire Logtical Plan made up until their line of call to execute.

Spark's Lazy architecture is a feature, not a bug; it allows Spark to create an optimised logical plan of all the Transformations and executes them as effectively as possible only when the script calls an Action. The logical plan allows ther Optimizer to look at the entire pipeline collectively and rewrite it before running any of it.

## DataFrame Reader API

`spark.read` gives access to the DataFrameReader - a configurable object whose purpose is to turn external files into a DataFrame

spark.read.format('csv').option('header', True).option('inferSchema', True).load(path)
#     └──────┬────────┘ └──────────────────────┬──────────────────────────┘ └───┬───┘
#      get the reader                   configure the reader                execute

1) `.format(str)` - The data source: csv, json, parquet, delta, text. Defaults to `parquet` if not mentioned.

2) `.option(key, value)` - Configure the reader object by accessing its properties

3) `.schema(structType)` - Supply the column names and data types instead of letting Spark infer them

4) `.load(path)` — Execute. Returns the DataFrame.

***Note***: options belong to a format, and the reader silently ignores any that don't apply. `header` and `inferSchema` are CSV options; passing them to a JSON file format read does nothing but also raises no error. Same for a typo'd key.

- `df.display()` is a Databricks function, not PySpark. It displays the DataFrame as a sorted grid. 
- `df.show(n, truncate=False)` is a PySpark function, which prints ASCII. 
- n (optional): No. of rows to show - default = 20; truncate (optional): Truncate strings longer than 20 chars. Default = False

## DDL and StructType

1) DDL

DDL can be used to define the Schema explicitly instead of letting Spark infer via the inferSchema option od the DataFrameReader.
The following structType definition (similar to SQL queries) can be passed into `.schema(structType)` to define the Schema of a DF via DDL

```python
my_ddl_schema = '''
    item_identifier STRING,
    item_weight STRING,
    item_fat_content STRING,
    item_visibility DOUBLE,
    item_type STRING,
    item_mrp DOUBLE,
    outlet_identifier STRING,
    outlet_establishment_year INTEGER,
    outlet_size STRING,
    outlet_location_type STRING,
    outlet_type STRING,
    item_outlet_sales DOUBLE
'''
```

- `df.printSchema()` displays the schema of a PySpark DataFrame. It lists every column name, its data type, and whether it allows null values.

2) StructType() Schema

StructType is the second way of defining the Schema of your DataFrame.

- `StructField` - Defines a single columns: a name, a datatype, and whether NULLs are allowed
- `StructType` - An ordered list of StructFields (columns).

```python
from pyspark.sql.types import *

my_struct_schema = StructType([
    StructField('item_identifier', StringType(), True),
    StructField('item_weight', StringType(), True),
    StructField('item_fat_content', StringType(), True),
    StructField('item_visibility', DoubleType(), True),
    StructField('item_type', StringType(), True),
    StructField('item_mrp', DoubleType(), True),
    StructField('outlet_identifier', StringType(), True),
    StructField('outlet_establishment_year', IntegerType(), True),
    StructField('outlet_size', StringType(), True),
    StructField('outlet_location_type', StringType(), True),
    StructField('outlet_type', StringType(), True),
    StructField('item_outlet_sales', DoubleType(), True)
])
```

## SELECT Statement

Straight Forward way of performing SQL Select

Select first 3 columns of the table only:
1) `df.select('item_identifier', 'item_weight', 'item_fat_content').display()`
2) `df.select(col('item_identifier'), col('item_weight'), col('item_fat_content')).display()` 

***Note***: 2nd syntax is the standardized approach since it's required while writing aliases and/or agg. It also requires SQL function import

### Alias

Straight forward way of changing column name in the result set.

```python
from pyspark.sql.functions import *

df.select(col('item_identifier').alias('item_ID'))
```

## Filter

### Scenario 1

Filter out only those rows which consist of Item Fat Content as 'Regular'

```python
df.filter(col('Item_Fat_Content') == 'Regular').display()
```

### Scenario 2

Filter out rows that have Item_Type as 'Soft Drinks' and Item_Weight < 10

```python
df.filter((col('Item_Type') == 'Soft Drinks') & (col(Item_Weight) <> 10)).display()
```

### Scenario 3

Filter out rows that are either in Tier 1 or Tier 2 and have an Outlet Size of NULL

```python
df.filter((col('Outlet_Location_Type').isin('Tier 1', 'Tier 2') & col('Outlet_Size').isNull())).display()
```

## withColumnRenamed

Allows us to rename the column directly in the DataFrame

```python
df.withColumnRenamed('item_weight', 'Item_Wt').display()
```

## withColumn

Allows us to add a new column or modify an existing one

### Scenario 1 - Add a new column 'flag' which has a constant value 'new' for each row

```python
df = df.withColumn('flag', lit('new'))
df.display()
```

`lit()` allows converion of a Python value into a Column. It is needed when the value is being passed where a Column is required.
In the above, `lit()` was necessary to store a constant value for each row since 2nd param of 'withColumn' expects the final relsut to be a Column

### Scenario 2 - Add a new column 'multiply' which stores the multiplied values of 'Item_Weight' and 'Item_MRP' for each row

```python
df = df.withColumn('multiply', col('Item_Weight')*col('Item_MRP'))
df.display()
```

### Scenario 3 - Change the 'Low Fat' to 'LF" and the 'Regular' to 'Reg' in the Item_Fat_Content Column

```python
df = df.withColumn('Item_Fat_Content', regexp_replace('Item_Fat_Content', 'Regular', 'Reg'))\
    .withColumn('Item_Fat_Content', regexp_replace('Item_Fat_Content', 'Low Fat', 'LF'))
```
***Note***: If column name already exists in the table (Scenrio 3), we modify a column, otherwise, create a new one

`regexp_replace(column, pattern, replacement)` finds every match of a regex in a string column and swaps it out — applied row by row, returning a new Column.
It returns a Column, not a DataFrame. It's an expression, so it only means anything inside select(), withColumn(), filter(), etc.
Nothing is mutated — df is unchanged unless you reassign.

## Type Casting

Change or clarify a columns data type

`.cast()` is a Column method, not a DataFrame method. It takes one column expression and returns a new column expression whose values are converted to a different data type. `.astype()` and `.cast()` are identical.

`df.item_weight.cast(StringType())` is just an expression - it won't mutate anything unless:

```python
df = df.withColumn('Item_Weight', col('Item_Weight').cast(StringType()))
```

***Note***: StringType is a class; StringType() is an instance of that class - cast() requires an instance of the type you want converted to since it allows passing paramters, if needed, into the type we want such as `DecimalType(10, 2)`

## Sort/Order By

Analogous to ORDER BY in SQL Queries. `.sort()` and `.orderBy()` are identical methods.

1) Scenario 1 - Order by according to Item Weight in descending order

```python
df.orderBy(col("Item_Weight").desc()).display()
```

***Note***: Use .asc() in the same manner

2) Scenario 2 - Order by on the basis of (Item_Weight, Item_Visibility) - first in desc and second in asc

```python
df.orderBy(col("Item_Weight").desc(), col("Item_Visibility").asc()).display()
```

***Note***: `orderBy` returns a new DataFrame. It doesn't directly mutate the original one unless we re-assign `df = df.orderBy(...)`

## Limit

Analogous to LIMIT in SQL.

```python
df.limit(10).display()
```

## Drop

Allows us to drop column(s) in the Data Frame

```python
df.drop('Item_Visibility', 'Item_Type').display()
```

## Drop Duplicates

Allows us to get ride of duplicate rows in the DataFrame. Also known as 'dedup-ing' the DataFrame

### Scenario 1 - Drop duplicates based on all columns
```
df.dropDuplicates().display()
```
OR
```
df.distinct().display()
```
`.distinct()` vs `.dropDuplicates()` — distinct() deduplicates across all columns. dropDuplicates() does the same when called bare, but accepts a subset: df.dropDuplicates(["email"]) keeps one row per email while retaining all the other columns. distinct() can't do that. Which row survives is non-deterministic unless you order first.

### Scenario 2 - Dro Duplicates based on a subset of columns

```
df.dropDuplicates(['])

