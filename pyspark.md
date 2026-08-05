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
