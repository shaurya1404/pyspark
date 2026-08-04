# Pandas

## Why Pandas?

- Basic data structures in Python such as Lists and Dicts allow one to store data, however, they have no notion of what a 'column' or a 'table' is and no way to perform group operations on the data without writing loops and logic from scratch.

- Pandas reconciles these missing data concepts by inbtroducing two objects: Series and DataFrame

## Series And DataFrame

**Series**: Analogous to a single column. A 1D array with an index attached to it

```python
import pandas as pd
data1 = [100.1, 104.2, 205]
data2 = ("cats", "dogs", "mice")
data3 = {"name": "ichigo", "power": "getsuga"} # dicts - keys are implicitly set as indices

series1 = pd.Series(data1) # Calling the constructor for the class Series (not a method, that's why 'Series')
series2 = pd.Series(data2, index=["a", "b", "c"]) # Optional parameter - Allows us to define the index instead of default 0-base 
series3 = pd.Series(data3)

print(series1)
print(series2)
print(series3)

series2.loc["a"] = "rabits"

print(series1.loc[1], '\n')
print(series2.loc["a"], '\n') # loc - label lookup
print(series3.iloc[0], '\n') #  iloc - positional lookup

print(series1[series1 > 200])
```

**DataFrame**: Analgous to a table (rows AND columns). A 2D dictionary of Series sharing one index

```python
import pandas as pd

data = { # Defining DF column-wise
    "Name": ["Urahara", "Aizen", "Kenpachi"],
    "Strength": ["Intellect", "Spiritual Pressure", "Combat"]
}

df = pd.DataFrame(data) # Constructor to define new object
 
print(df, '\n')
print(df.loc[1], '\n')

# Add a new column
df["Power Rating"] = [8.6, 9.4, 9.2]

# Add new rows
new_rows = pd.DataFrame([ # Defining DF row-wise
                            {"Name": "Ichigo", "Strength": "Potential", "Power Rating": 9.6},
                            {"Name": "Yhwach", "Strength": "Quincy King", "Power Rating": 9.8}
                        ], index = ["OptIndex", "AnotherOne"])

df = pd.concat([df, new_rows])
print(df, '\n')
```