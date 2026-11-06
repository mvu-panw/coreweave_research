# Table

Source: https://docs.coreweave.com/products/wandb/ref/python/data-types/table

# Table

[View source](https://github.com/wandb/wandb/blob/main/wandb/sdk/data_types/table.py#L211)

## Class wandb.Table

The Table class used to display and analyze tabular data.

Unlike traditional spreadsheets, Tables support numerous types of data:
scalar values, strings, numpy arrays, and most subclasses of `wandb.data_types.Media`.
This means you can embed `Images`, `Video`, `Audio`, and other sorts of rich, annotated media
directly in Tables, alongside other traditional scalar values.

This class is the primary class used to generate W\&B Tables
[https://docs.wandb.ai/models/tables](https://docs.wandb.ai/models/tables)

```python theme={"system"}
columns: 'list[ColumnKey] | None' = None,
data: 'list[InputRow] | np.ndarray | pd.DataFrame | None' = None,
rows: 'list[InputRow] | None' = None,
dataframe: 'pd.DataFrame | None' = None,
dtype: 'Any' = None,
optional: 'bool | list[bool]' = True,
allow_mixed_types: 'bool' = False,
log_mode: 'LogMode | None' = 'IMMUTABLE'
```

## Args

**columns** `list[ColumnKey] | None`

Names of the columns in the table. Defaults to \["Input", "Output", "Expected"].

**data** `list[InputRow] | np.ndarray | pd.DataFrame | None`

2D row-oriented array of values, NumPy array, or pandas DataFrame.

**rows** `list[InputRow] | None`

2D row-oriented array of values.

**dataframe** `pd.DataFrame | None`

pandas DataFrame object used to create the table. When set, `data` and `columns` arguments are ignored.

**dtype** `Any`

The expected type for the column values, used to validate the
data. If not set, types are inferred from the data. It can be:

* a single type
  * a Python built-in type such as `int`, `str`, `bool`, list, dict, or
    datetime.
  * a W\&B Media type like `wandb.Image` declared under wandb.data\_types
  * a const value
* a list of any of the above to assign a different type to each
  column (should be the same length as `columns`)

**optional** `bool | list[bool]`

Determines if `None` values are allowed. Defaults to True.

* If a singular bool value, then the optionality is enforced for all
  columns specified at construction time
* If a list of bool values, then the optionality is applied to each
  column - should be the same length as `columns`
  applies to all columns. A list of bool values applies to each respective column.

**allow\_mixed\_types** `bool`

Determines if columns are allowed to have mixed types (disables type validation). Defaults to False

**log\_mode** `LogMode | None`

Controls how the Table is logged when mutations occur.
Options:

* "IMMUTABLE" (default): Table can only be logged once; subsequent
  logging attempts after the table has been mutated will be no-ops.
* "MUTABLE": Table can be re-logged after mutations, creating
  a new artifact version each time it's logged.
* "INCREMENTAL": Table data is logged incrementally, with each log creating
  a new artifact entry containing the new data since the last log.

## Methods

### method Table.add\_column()

```python theme={"system"}
self,
name: 'str',
data: 'list[Any] | np.ndarray',
optional: 'bool' = False
```

Adds a column of data to the table.

##### Arguments

**name** `str`

The unique name of the column.

**data** `list[Any] | np.ndarray`

A column of homogeneous data.

**optional** `bool`

If null-like values are permitted.

### method Table.add\_computed\_columns()

```python theme={"system"}
self,
fn: 'Callable[[int, dict[ColumnKey, Any]], dict[str, Any]]'
```

Adds one or more computed columns based on existing data.

##### Arguments

**fn** `Callable[[int, dict[ColumnKey, Any]], dict[str, Any]]`

A function which accepts an index and row dict, and returns a dict representing new columns for that row, keyed by the new column names.

##### Examples

In the callback:

* `ndx` is an integer representing the index of the row.
* `row` is a dictionary keyed by existing columns.

```python theme={"system"}
import wandb

table = wandb.Table(columns=["x", "y"], data=[[3, 1], [4, 6]])
table.add_computed_columns(lambda ndx, row: {"diff": row["x"] - row["y"]})
```

### method Table.add\_data()

```python theme={"system"}
self, *data: 'Any'
```

Adds a new row of data to the table.

The maximum amount ofrows in a table is determined by
`wandb.Table.MAX_ARTIFACT_ROWS`.

The length of the data should match the length of the table column.

##### Arguments

**data** `Any`

No description provided.

### method Table.add\_row()

```python theme={"system"}
self, *row: 'Any'
```

Deprecated. Use `Table.add_data` method instead.

##### Arguments

**row** `Any`

No description provided.

### method Table.cast()

```python theme={"system"}
self,
col_name: 'ColumnKey',
dtype: 'Any',
optional: 'bool' = False
```

Casts a column to a specific data type.

This can be one of the normal python classes, an internal W\&B type,
or an example object, like an instance of wandb.Image or
wandb.Classes.

##### Arguments

**col\_name** `ColumnKey`

The name of the column to cast.

**dtype** `Any`

The target dtype.

**optional** `bool`

If the column should allow Nones.

### method Table.get\_column()

```python theme={"system"}
self,
name: 'ColumnKey',
convert_to: "Literal['numpy'] | None" = None
```

Retrieves a column from the table and optionally converts it to a NumPy object.

##### Arguments

**name** `ColumnKey`

The name of the column.

**convert\_to** `Literal['numpy'] | None`

"numpy" will convert the underlying data to a NumPy object.

### method Table.get\_dataframe()

```python theme={"system"}
self
```

Returns a `pandas.DataFrame` of the table.

### method Table.get\_index()

```python theme={"system"}
(self)
```

Returns an array of row indexes for use in other tables to create links.
