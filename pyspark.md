# PySpark

## What is Spark? Why does it exist?

- Up until now, SQL operations were performed on a single system in order to transform, clean, and load data. However, a single system in and of itself will have resource constraints - say 16GB RAM with 8 cores.

- So, as data increases, resources have a ceiling limit to perform the operations. When handling big data such as terabytes or petabytes of data, things will really start to slow down.

- Now, the trivial solution is to vertically scale - improve the resources of the single-system. However, this isn't scalable nor cost-effective as that too will hit a limit aftter a certain point and would also lead to wasted resources when data scales down to use lesser sizes.

- Hence, the more optial solution is Horizontal Scaling - Use 20 not-so-fancy systems in order to process the data by partitioning it into subsets of data. This is exaclty what Spark does.

- Spark is a distributed compute engine which allows processing of big data much more manageable and scalable. It processes data across multiple machines. It does NOT store data at any point; It's stateless. You point it at files sitting in S3 or a Delta/Iceberg table, it reads them, computes, writes results back out, and forgets everything.

This delineation between storage and processing is what makes it extremely powerful. It means your storage layer (cheap, durable, always-on) and your compute layer (expensive, elastic, spun up on demand) scale independently.