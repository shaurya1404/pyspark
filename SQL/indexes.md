# Structural Index

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

A Balanced Tree is a Hierarchical structure that stores data at the leaf nodes. It starts at the root nodes and passes through level(s) of Index Pages. The Index Pages are known as intermediary nodes. The search complexity becomes `O(log(n))`

The Index Page stores key-value pairs wherein the Key describes which range of the sorted data is stored in the subsequent page while the Value contains the pointer to that page (either data or index).

Reading an Index Page is much faster than reading a Data Page.

## Clustered Index

A Clustered Index determines the physical order rows are stored on disk. The rows are stored within the actual disk in the order of the column that the Clustered Index is defined upon. A table can only have one since there's only one way to physically arrange data (usually the primary key).

The leaf nodes of the B-Tree of a Clustered Index containes the Data Pages themselves.

## Non-clsutered Index

A Non-Clustered Index doesn't physically re-arrange or affect the rows in the Data Pages. Unlike Clustered Indexes, the leaf nodes are not data Pages but instead Index Pages that consist of row-locator rows having a 1:1 mapping to the actual rows in the Data Pages.

The intermediate nodes and root node work the same in Clustered & Non-Clustered indexes - an index page pointing to another index page which stores the location of a group of rows.

If the table's structure is Heap (no clustered index) - row locators store actual physical addresses of the rows
If the table has a clustered index - row locators contain clustered key values, i.e, a second lookup in the clustered B-tree

## Clustered vs Non-Clustered (Use Preview)

Searching via a Non-Clustered index requires one extra layer of looking up, i.e, the leaf Index Page lookup to find the pointer to the actual row we're looking for.

| Aspect                 | Clustered Index                                      | Non-Clustered Index                                    |
|------------------------|------------------------------------------------------|--------------------------------------------------------------------------------|
| **Definition**         | Physically sorts and stores rows                     | Separate structure with pointers to the data                                      |
| **Number of Indexes**  | **One** index per table                                                                  | **Multiple** indexes are allowed                                                  |
| **Read Performance**   | Faster                                                                                    | Slower                                                                             |
| **Write Performance**  | Slower, due to potential data row reordering                                             | Faster, since physical data order is unaffected                                   |
| **Storage Efficiency** | More storage-efficient                                                                    | Requires additional storage space                                                 |
| **Use Case**           | - Unique column<br>- Not frequently modified column<br>- Better range query performance, since physical sorting ensures contiguous memory for ranges | - Columns frequently used in search conditions and joins<br>- Better exact match query performance, since each row must be looked up sequentially |

## Syntax for Indexes

`CREATE CLUSTERED INDEX index_name ON table_name (col1, col2, ...)`
`CREATE NONCLUSTERED INDEX index_name ON table_name (col1, col2, ...)`

## Composite Index

Creating an index based on more than one column.

**Leftmost Prefix Rule**: The index works ONLY if the query filter starts from the leftmost column in the index and follows its order. The index cannot be used of the query doesn't filter from the leftmost column and resorts to a Full Table Scan.

`CREATE NONCLUSTERED INDEX index_name ON table_name (A, B, C)`
**Index used**: (A), (A, B), (A, B, C)
**Index NOT used**: (B), (A, C), (B, C)

# Storage Indexes

## Rowstore Index

The default index. Data is indexed and stored row-by-row. Every column of the row sits together physically.

**Structure**: B-tree

**Clustered**:     The leaf level is the actual table data, physically sorted by the key. Only one per table.
**Nonclustered**:  A separate structure with leaf nodes containing key + pointer back to the row. Many allowed per table.

## Columnstore Index

Data is stored column by column - all values from one column stored and compressed in Lob Pages

### Columnstore Structure

No B-tree structure here, but instead:

1) Rowgroups: Data is first divided into one or more row groups (~1M rows per group) which ensures that the groups are large enough to compress but still manageable in the memory.

2) Column Segments: Rows within each row group are sliced on the basis of columns. So a rowgroup from a 10-column table produces 10 separate segments

3) Data Compression: Each column segment is then compressed individually. Unlike Rowstore indexes, data can be compressed upto 5-10x since all values in a column have the same data type and are repetitive. A common compression technique is using Dictionaries - Store the data using a smaller data type and storing the mapping to the actual values in a seperate dictionary.

4) Lob Pages: The data is stored in LOB pages instead of the traditional ~8KB data pages. In addition to the Header and Body that data pages have, LoB pages have an additional Segment Header section which stores important metadata about the column segment in this page such as the Segment ID, Rowgroup ID, and the Dictionary ID. No offset array here since data is not stored as seperate rows.

**Clustered Columnstore Index**: Replaces the table's strage on-disk entirely. The data itself will no longer be stored row-by-row in data pages but rather column-by-column in LOB pages. All the columns are madatorily included in the index.

**Nonclustered Columnstore Index**: The original rowstore table (heap or clustered index) stays untouched. An additional structure is created with a replica of the data and stored in LOB pages that co-exists with the original data. Since the original data co-exists, we can selectively choose some/all columns to make the columnstore index using.

## Advantages of Columnstore Index

1) Data Compresion: Since columnstore groups same-type, high-repetitive values together, compression is a lot more efficient.

2) Efficient I/O: A query like `SELECT SUM(Amount) WHERE Region='West'` will pull all 20 columns just to access the 2 columns in the query. In columnstore, only the pages containng the relevent segments will be accessed.

## OLTP vs OLAP

**OLTP**: Rowstore index is best for Online Transaction Processing (OLTP) systems which frequently insert, update, and delete single records such as Banking and Healthcare management systems.
**OLAP**: Columnstore index is best for Online Analytical Processing (OLAP) systems which perform aggregate operations and big data analytics frequently such as Business Intelligence systems.

## Syntax 

**Rowstore Index**
`CREATE NONCLUSTERED INDEX index_name ON table_name (Country)`
`CREATE CLUSTERED INDEX index_name ON table_name (ID)`

**Columnstore Index**
`CREATE NONCLUSTERED COLUMNSTORE INDEX index_name ON table_name (Country)`
`CREATE CLUSTERED COLUMNSTORE INDEX index_name ON table_name`

The table can have only 1 Clustered Index - either rowstore or columnstore. Clustered columnstore doesn't take any columns as params since it's created only on all columns.
The table can have multiple Nonclustered Rowstore indexes but only 1 Columnstore Index.