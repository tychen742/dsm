---
marp: true
theme: default
paginate: true
style: |
  section {
    font-family: 'Segoe UI', system-ui, sans-serif;
    font-size: 22px;
    color: #1a1a1a;
    padding: 34px 48px 58px 48px;
    background: white;
  }
  h1 { color: #2a6b37; font-size: 1.8em; border-bottom: 3px solid #b8860b; padding-bottom: 8px; margin-bottom: 14px; }
  h2 { color: #2a6b37; font-size: 1.28em; margin-bottom: 10px; }
  ul, ol { margin-left: 1.15em; }
  li { margin-bottom: 6px; line-height: 1.35; }
  p { line-height: 1.35; }
  section.title {
    background: #2a6b37;
    color: white;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  section.title h1 { color: white; border: none; font-size: 2.15em; }
  section.title p { color: #d7ecd9; font-size: 0.95em; }
  section.section {
    background: #2a6b37;
    color: white;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  section.section h2 { color: white; border: none; font-size: 1.9em; }
  section.section p { color: #d7ecd9; font-size: 0.95em; }
  .callout { background: #e8f5eb; border-left: 4px solid #2a6b37; border-radius: 4px; padding: 8px 12px; margin: 8px 0; font-size: 0.84em; line-height: 1.35; }
  table { display: table; font-size: 0.78em; border-collapse: collapse; width: 100%; }
  th { background: #2a6b37; color: white; padding: 6px 8px; text-align: left; }
  td { padding: 6px 8px; border-bottom: 1px solid #e0e0e0; vertical-align: top; }
  tr:nth-child(even) td { background: #f7faf7; }
  code { color: #c7254e; background: #f6f8fa; border: 1px solid #e0e0e0; border-radius: 3px; padding: 1px 4px; }
---

<!-- _class: title -->

# Chapter 3: NumPy Arrays

Numerical arrays for efficient data science work

*Sections: Array basics · Array computation · Random number generation*

*Use arrow keys or Space to navigate · Press F for fullscreen*

---

## Chapter Roadmap

| Part | Main Question | Core Vocabulary |
|---|---|---|
| Array basics | How does NumPy store numerical collections? | array, ndarray, shape, dtype |
| Array computation | How do arrays compute without manual loops? | vectorized operation, ufunc, aggregation |
| Random generation | How can arrays model uncertainty? | generator, seed, sampling, simulation |

<div class="callout">

This chapter bridges basic Python and table-oriented data work by making numerical collections faster and easier to compute with.

</div>

---

## Chapter Goals

By the end of this chapter, you will be able to:

1. Create NumPy arrays and inspect their shape, size, dimension, and data type.
2. Select and reshape array values with indexing, slicing, masks, and shape methods.
3. Apply vectorized operations and universal functions across arrays.
4. Summarize and compare arrays with aggregation, axes, broadcasting, sorting, and fancy indexing.
5. Use random generators for reproducible samples and simple simulations.

---

<!-- _class: section -->

## Array Basics

Creating, inspecting, indexing, and reshaping arrays

---

## Why Arrays?

NumPy arrays are compact numerical collections.

| Python Lists | NumPy Arrays |
|---|---|
| Flexible containers for general objects | Homogeneous containers for numerical work |
| Often require explicit loops | Support whole-array operations |
| Good for mixed small collections | Better for large numerical datasets |

```python
sales = np.array([340, 280, 410])
sales.shape
```

---

## Lists vs Arrays

Python lists are flexible. NumPy arrays are specialized.

```python
prices_list = [9.99, 12.50, 7.25]
prices_array = np.array(prices_list)
```

| Question | List Habit | Array Habit |
|---|---|---|
| What can it hold? | Mixed objects | One main dtype |
| How does it compute? | Usually loop by loop | Whole collection at once |
| What is it best for? | General Python data | Numeric analysis |

---

## Creating Arrays

Most NumPy work starts by creating an `ndarray`.

```python
np.array([10, 20, 30])
np.arange(0, 12, 3)
np.linspace(0, 1, 5)
np.zeros(4)
np.ones((2, 3))
```

Choose the constructor that matches the business question: observed values, regular ranges, evenly spaced values, or placeholder arrays.

---

## Shape Is Structure

The `shape` tells you how the values are arranged.

```python
sales = np.array([[120, 135, 142],
                  [98, 105, 111]])

sales.shape
```

| Shape | Meaning |
|---|---|
| `(3,)` | One-dimensional array with 3 values |
| `(2, 3)` | Two rows and three columns |
| `(4, 2, 3)` | Three-dimensional structure |

---

## Data Types Matter

The `dtype` controls how values are stored and computed.

```python
np.array([1, 2, 3]).dtype
np.array([1, 2, 3.5]).dtype
np.array(["A", "B", "C"]).dtype
```

- Numeric dtypes support mathematical operations.
- Mixed inputs may be converted to a common dtype.
- String arrays have fixed-width string storage.

---

## Indexing And Slicing

Indexing selects one value. Slicing selects a range.

```python
sales = np.array([120, 135, 142, 130])

sales[0]
sales[1:3]
sales[-1]
```

For management data, this is how you select specific periods, product positions, or subsets of a numerical record.

---

## Two-Dimensional Selection

A two-dimensional array uses row and column positions.

```python
sales = np.array([[120, 135, 142],
                  [98, 105, 111]])

sales[0, 2]   # first row, third column
sales[:, 1]   # every row, second column
sales[1, :]   # second row, every column
```

Think: first choose rows, then choose columns.

---

## Reshaping Arrays

`reshape()` changes the arrangement without changing the values.

```python
monthly = np.arange(1, 13)
quarter_table = monthly.reshape(4, 3)
```

Use reshaping when the same values need a more useful layout, such as months into quarters or daily values into weeks.

---

<!-- _class: section -->

## Array Computation

Vectorized operations, ufuncs, aggregation, and broadcasting

---

## Computing With Whole Arrays

Vectorized operations move repetitive work into NumPy's optimized layer.

```python
prices = np.array([10, 12, 15])
quantities = np.array([4, 3, 2])
revenue = prices * quantities
```

- Element-wise operations apply to corresponding values.
- Universal functions provide fast reusable operations.
- Aggregations summarize arrays into totals, averages, or extrema.
- Broadcasting combines compatible shapes without manual repetition.

---

## Iteration vs Vectorization

Loops describe each step. Vectorized code describes the calculation.

```python
costs = np.array([80, 95, 110])
markup = 1.25

prices = costs * markup
```

Vectorized operations are usually:

- Shorter to read
- Less error-prone
- Faster for large arrays

---

## Universal Functions

Universal functions, or ufuncs, apply fast element-wise calculations.

```python
values = np.array([4, 9, 16])

np.sqrt(values)
np.log(values)
np.round(values / 3, 2)
```

Use ufuncs when every value should receive the same mathematical treatment.

---

## Aggregations

Aggregations turn many values into summaries.

```python
sales = np.array([120, 135, 142, 130])

sales.sum()
sales.mean()
sales.min()
sales.max()
```

These are the array version of common management questions: total revenue, average demand, best result, worst result.

---

## Axis Support

The `axis` argument controls the direction of a summary.

```python
sales = np.array([[120, 135, 142],
                  [98, 105, 111]])

sales.sum(axis=0)  # column totals
sales.sum(axis=1)  # row totals
```

| Axis | Plain Meaning |
|---|---|
| `axis=0` | Summarize down rows for each column |
| `axis=1` | Summarize across columns for each row |

---

## Broadcasting

Broadcasting lets compatible shapes work together.

```python
prices = np.array([10, 12, 15])
discount = 0.90

sale_prices = prices * discount
```

NumPy treats the scalar discount as if it matched the array shape. This avoids manual repetition.

---

## Boolean Masks

A Boolean mask marks which values meet a condition.

```python
sales = np.array([120, 85, 142, 97])

high_sales = sales >= 100
sales[high_sales]
```

Masks are the foundation for filtering data before pandas.

---

## Modifying With Masks

Masks can also update selected values.

```python
scores = np.array([88, 74, 91, 69])
scores[scores < 70] = 70
```

This pattern is useful for caps, floors, flags, recoding, and threshold-based decisions.

---

## Fancy Indexing And Sorting

Fancy indexing selects positions from an index array.

```python
sales = np.array([120, 85, 142, 97])
positions = np.array([2, 0])

sales[positions]
np.sort(sales)
np.argsort(sales)
```

Sorting and index arrays support ranking workflows such as top stores, lowest costs, or best-performing periods.

---

<!-- _class: section -->

## Random Number Generation

Sampling and simulation with reproducible random values

---

## Modeling Uncertainty

Random generators help analysts explore possible outcomes.

```python
rng = np.random.default_rng(42)
daily_demand = rng.normal(120, 15, size=30)
daily_demand.mean()
```

| Concept | Why It Matters |
|---|---|
| Seed | Makes a random sequence reproducible. |
| Generator | Keeps random state explicit and local. |
| Sampling | Draws values from data or a distribution. |
| Simulation | Repeats random draws to study uncertainty. |

---

## Modern Random API

Use a generator instead of relying on global random state.

```python
rng = np.random.default_rng(42)

rng.random(5)
rng.integers(1, 7, size=10)
rng.normal(100, 12, size=30)
```

The seed makes examples reproducible for teaching, testing, and debugging.

---

## Sampling From Values

`choice()` draws from a set of possible values.

```python
rng = np.random.default_rng(42)
stores = np.array(["A", "B", "C", "D"])

rng.choice(stores, size=6)
```

Sampling can model customer arrivals, store selection, product demand categories, or experimental assignment.

---

## Simulation Workflow

A simulation repeats a random process and summarizes the outcomes.

```python
rng = np.random.default_rng(42)
demand = rng.normal(120, 15, size=1000)

(demand > 150).mean()
```

Simulation turns uncertain business questions into estimated probabilities or expected outcomes.

---

## Randomness Checklist

Before using random numbers, ask:

1. What random process am I modeling?
2. What distribution or sample values make sense?
3. How many draws do I need?
4. Should I set a seed for reproducibility?
5. What summary answers the business question?

---

## Chapter 3 Vocabulary

| # | Term | Short Meaning |
|---:|---|---|
| 1 | ndarray | NumPy's N-dimensional array object. |
| 2 | Shape | Length along each array axis. |
| 3 | dtype | Data type used to store array values. |
| 4 | Vectorized operation | Whole-array computation without explicit Python loops. |
| 5 | Universal function | Fast NumPy function applied element by element. |
| 6 | Broadcasting | Combining compatible arrays with different shapes. |
| 7 | Boolean mask | True/False array used to filter another array. |
| 8 | Aggregation | Summary calculation over many values. |
| 9 | Seed | Starting value for reproducible random output. |
| 10 | Simulation | Random modeling of possible outcomes. |

---

## What To Carry Forward

After this chapter, students should be ready to:

- Recognize when numerical data should become an array.
- Replace simple Python loops with vectorized array operations.
- Use random samples to reason about uncertainty.
- Bring NumPy habits into pandas, visualization, and statistics chapters.

---

## Carry Forward

- Use the section practice exercises to check runnable code skills.
