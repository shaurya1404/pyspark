# Index

An Index is a Data Structure that speeds up data read operations on a table at the cost of extra storage and slower writes.

## Data Files and Pages

Data is not stored as rows and coluns in a Database. Data Files are the OS-level files that store the database in the disk. Data Files are comprised of Data Pages

**Data Page**: The fundamental unit of storage in a database. Data Pages are 8KB in size.

### Structure of A Data Page

| Page Header (96 bytes) | Row data (~8060 bytes usable) | Row offset array |

**Page Header**: Contains Metadata such as page number, file number, available free space, etc.
**Row Data**: Consists of the actual rows stacked sequentially. Number of rows in one page is contingent on how much data a single row holds.
**Row offset array**: An array that stores pointers to where each row starts.

## Why Index?

Without an index, data is stored as a heap structure, i.e, data is inserted in chronological order with no sorting. Since no sorting is involved, data writes are extremely fast. Searching is extremely slow as a Full Table Scan is done since there's no logical sorting of the data. Time complexity is `O(n)`.

## B-Tree

A Balanced Tree is a Hierarchical structure that stores data at the leaf nodes. It starts at the root nodes and passes through level(s) of Index Pages. The Index Pages are known as intermediary nodes. The search complexit becomes `O(log(n))`

The Index Page stores key-value pairs wherein the Key describes which range of the sorted data is stored in the subsequent page while the Value contains the pointer to the subsequent page (either data or index).

Reading an Index Page is much faster than reading a Data Page.

## Clustered Index

The Clustered Index determines the physical order rows are stored on disk. The rows are stored within the actual disk in the order of the column that the Clustered Index is defined upon. A table can only have one since there's only one way to physically arrange data (usually the primary key).

The leaf nodes of the B-Tree of a Clustered Index containes the Data Pages themselves.

## Non-clsutered Index

A Non-Clustered Index doesn't physically re-arrange or affect the rows in the Data Page. Unlike Clustered Indexes, the leaf nodes are not data Pages but instead Index Pages called Row-Locator Pages that consist of 1:1 pointers to the Data File, Data Page, and the offset to the exact row we're looking for.

With the exception of the leaf nodes being Row-Locator pages instead of actual data pages at the leaf node, the intermediate nodes and root node work the same in Clustered & Non-Clustered indexes - an index page pointing to another index page which stores the location of a group of rows.

Searching via a Non-Clustered index requires one extra layer of index page lookup, i.e, the Row-Locator Page lookup to find the exact data page location and offset of the row that we're looking for.

