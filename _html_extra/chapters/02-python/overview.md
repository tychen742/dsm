---
marp: true
theme: default
paginate: true
style: |
  section {
    font-family: 'Segoe UI', system-ui, sans-serif;
    font-size: 21px;
    color: #1a1a1a;
    padding: 34px 48px 58px 48px;
    background: white;
  }
  h1 {
    color: #2a6b37;
    font-size: 1.82em;
    border-bottom: 3px solid #b8860b;
    padding-bottom: 8px;
    margin-bottom: 14px;
  }
  h2 {
    color: #2a6b37;
    font-size: 1.3em;
    margin-bottom: 10px;
  }
  h3 {
    color: #2a6b37;
    font-size: 1.03em;
    margin: 10px 0 6px 0;
  }
  ul, ol { margin-left: 1.1em; }
  li { margin-bottom: 5px; line-height: 1.32; }
  p { line-height: 1.35; }
  section.title,
  section.section {
    background: #2a6b37;
    color: white;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  section.title h1,
  section.section h2 {
    color: white;
    border: none;
  }
  section.title h1 { font-size: 2.16em; }
  section.title p,
  section.section p {
    color: #d7ecd9;
    font-size: 0.95em;
  }
  .callout {
    background: #e8f5eb;
    border-left: 4px solid #2a6b37;
    border-radius: 4px;
    padding: 8px 12px;
    margin: 8px 0;
    font-size: 0.84em;
    line-height: 1.35;
  }
  table {
    display: table;
    font-size: 0.78em;
    border-collapse: collapse;
    width: 100%;
  }
  th {
    background: #2a6b37;
    color: white;
    padding: 6px 8px;
    text-align: left;
  }
  td {
    padding: 6px 8px;
    border-bottom: 1px solid #e0e0e0;
    vertical-align: top;
  }
  tr:nth-child(even) td { background: #f7faf7; }
  code {
    color: #c7254e;
    background: #f6f8fa;
    border: 1px solid #e0e0e0;
    border-radius: 3px;
    padding: 1px 4px;
  }
  pre {
    font-size: 0.72em;
    line-height: 1.28;
  }
---

<!-- _class: title -->

# Chapter 2: Python Basics

Practical programming foundations for data science and management

*Syntax · Control structures · Lists · Dictionaries · Functions*

*Use arrow keys or Space to navigate · Press F for fullscreen*

---

## Chapter Roadmap

| Section | Main Question | Core Vocabulary |
|---|---|---|
| Syntax | How do you write valid Python statements? | value, variable, type, operator |
| Control structures | How do programs choose and repeat actions? | Boolean, conditional, loop |
| Lists | How do you work with ordered values? | list, index, slice, method |
| Dictionaries | How do you map keys to values? | dictionary, key, value, counter |
| Functions | How do you package reusable work? | parameter, argument, return, scope |

<div class="callout">

The goal is practical fluency: enough Python to read, write, debug, and adapt data analysis code.

</div>

---

## Chapter Goals

By the end of this chapter, you will be able to:

1. Write and run simple Python statements with correct syntax, variables, objects, types, and operators.
2. Use conditionals and Boolean expressions to represent business rules.
3. Use `while` and `for` loops to repeat work over counts, conditions, and collections.
4. Work with lists and dictionaries to organize, access, modify, and count data values.
5. Define, call, and debug functions with parameters, return values, docstrings, scope, and tracebacks.

---

<!-- _class: section -->

## Python Syntax

Values, variables, types, operators, data structures, and modules

---

## Statements, Values, And Output

Python programs are built from statements that operate on values.

```python
department = "Marketing"
sales = 1250
cost = 875
profit = sales - cost

print(f"{department} profit: ${profit}")
```

- `print()` displays output.
- F-strings combine text with computed values.
- Comments explain intent without changing what Python runs.

---

## Variables And Names

Variables attach useful names to objects.

```python
customer_count = 42
average_order_value = 38.50
monthly_revenue = customer_count * average_order_value
```

Good names help you read the calculation:

- Use lowercase words separated by underscores.
- Choose names that explain the business meaning.
- Update variables when a later statement should replace the stored value.

---

## Built-In Data Types

| Type | Example | Common Use |
|---|---:|---|
| `int` | `42` | Counts, units, whole-number IDs |
| `float` | `38.50` | Prices, rates, measurements |
| `str` | `"East"` | Names, labels, categories |
| `bool` | `True` | Conditions and flags |

```python
price_text = "19.99"
price = float(price_text)
```

Imported data often arrives as text, so type conversion is a routine data-cleaning step.

---

## Operators And Precedence

Python operators combine values into expressions.

| Operator | Meaning | Example |
|---|---|---|
| `+`, `-`, `*`, `/` | Arithmetic | `revenue - cost` |
| `//` | Integer division | `17 // 5` gives `3` |
| `%` | Remainder | `17 % 5` gives `2` |
| `**` | Power | `growth ** 2` |

```python
profit_margin = (revenue - cost) / revenue
```

Parentheses make the order of operations visible.

---

## Objects, References, And Mutability

Python variables refer to objects. Some objects can change in place.

```python
sales = [340, 280, 410]
same_sales = sales
same_sales.append(390)
```

- Numbers and strings are immutable.
- Lists and dictionaries are mutable.
- Two variables can refer to the same mutable object.

<div class="callout">

Aliasing matters because changing a list through one name can affect code that uses another name for the same list.

</div>

---

## Modules And Packages

Modules and packages add tools beyond core Python.

```python
import math

discounted_price = math.floor(19.99 * 0.85)
```

- A module is a file of reusable Python code.
- A package is a collection of modules.
- Later chapters use packages such as NumPy, pandas, matplotlib, and seaborn.

---

<!-- _class: section -->

## Control Structures

Boolean expressions, conditionals, while loops, for loops, and loop control

---

## Boolean Expressions

A Boolean expression evaluates to `True` or `False`.

```python
order_total = 64
is_loyal_customer = True

qualifies = order_total >= 50 and is_loyal_customer
```

| Operator | Meaning |
|---|---|
| `==`, `!=` | Equal to, not equal to |
| `<`, `<=`, `>`, `>=` | Compare ordered values |
| `and`, `or`, `not` | Combine logical tests |

---

## Conditional Execution

Conditionals let code represent business rules.

```python
inventory = 18

if inventory == 0:
    status = "out of stock"
elif inventory < 20:
    status = "reorder soon"
else:
    status = "available"
```

- `if` runs a block only when its condition is true.
- `elif` checks another condition.
- `else` handles the remaining cases.

---

## Nested Decisions

Nested conditionals handle decisions inside decisions.

```python
segment = "enterprise"
contract_value = 85000

if segment == "enterprise":
    if contract_value >= 75000:
        priority = "strategic"
    else:
        priority = "standard enterprise"
else:
    priority = "standard"
```

Use nesting when the inner decision only makes sense after the outer decision is true.

---

## `while` Loops

A `while` loop repeats while a condition remains true.

```python
balance = 500
month = 0

while balance > 0:
    balance = balance - 125
    month = month + 1
```

Common patterns:

- Condition-controlled loops stop when a condition changes.
- Count-controlled loops repeat a known number of times.
- Sentinel-controlled loops stop when a special input value appears.

---

## `for` Loops

A `for` loop repeats once for each item in a sequence.

```python
sales = [340, 280, 410]
total = 0

for amount in sales:
    total = total + amount
```

Use `for` when the collection or range controls how many times the loop runs.

```python
for month in range(1, 13):
    print(month)
```

---

## Looping With Position

`enumerate()` gives both the position and the value.

```python
regions = ["East", "West", "South"]

for index, region in enumerate(regions):
    print(index, region)
```

Nested loops repeat one loop inside another.

```python
for region in regions:
    for quarter in range(1, 5):
        print(region, quarter)
```

---

## Loop Control

`break` and `continue` change a loop's normal flow.

```python
for score in satisfaction_scores:
    if score is None:
        continue
    if score < 2:
        break
    reviewed = reviewed + 1
```

| Statement | Effect |
|---|---|
| `break` | Exit the loop now |
| `continue` | Skip to the next iteration |

Use them sparingly and make the condition clear.

---

<!-- _class: section -->

## Lists

Ordered collections, indexes, slices, methods, strings, files, and aliasing

---

## Creating And Indexing Lists

Lists store ordered collections of values.

```python
sales = [340, 280, 410, 390]

first_sale = sales[0]
last_sale = sales[-1]
middle_sales = sales[1:3]
```

- Indexes start at `0`.
- Negative indexes count from the end.
- Slices create a new list from part of a list.

---

## Modifying Lists

Lists are mutable, so methods can change them in place.

```python
sales.append(420)
sales.extend([395, 430])
removed = sales.pop()
sales.sort()
```

| Method | Common Use |
|---|---|
| `append()` | Add one item |
| `extend()` | Add several items |
| `pop()` | Remove and return by position |
| `remove()` | Remove by value |
| `sort()` | Reorder in place |

---

## List Functions And Operations

Built-in functions summarize lists.

```python
scores = [4, 5, 3, 5, 4]

count = len(scores)
best = max(scores)
worst = min(scores)
total = sum(scores)
average = total / count
```

List operations also create and combine lists:

```python
repeated = [0] * 4
combined = ["East"] + ["West"]
```

---

## Lists And Strings

Strings and lists are both sequences, but they behave differently.

```python
region = "North"
letters = list(region)
words = "North Region".split()
label = "-".join(words)
```

- You can loop over a string one character at a time.
- `split()` turns a string into a list.
- `join()` turns a list of strings into one string.

---

## Files And Word Lists

File examples show how lists can collect data from outside Python code.

```python
words = []

with open("data/words.txt") as source:
    for line in source:
        words.append(line.strip())
```

After the list exists, you can search, count, slice, sort, and filter it.

<div class="callout">

This pattern previews later work with datasets: read values, store them in a collection, then analyze the collection.

</div>

---

## Aliasing With Lists

Two names can point to the same list.

```python
original = ["East", "West"]
alias = original
copy = original[:]

alias.append("South")
```

- `alias` and `original` refer to the same object.
- `copy` refers to a different list with the same starting values.
- This distinction matters when functions receive lists as arguments.

---

<!-- _class: section -->

## Dictionaries

Mappings, keys, membership, counters, iteration, and accumulation

---

## Dictionaries As Mappings

A dictionary maps keys to values.

```python
prices = {
    "basic": 19,
    "pro": 49,
    "enterprise": 199
}

pro_price = prices["pro"]
```

Use dictionaries when lookup by label matters more than position.

---

## Creating And Querying Dictionaries

```python
inventory = {}
inventory["laptop"] = 12
inventory["monitor"] = 18

if "laptop" in inventory:
    inventory["laptop"] = inventory["laptop"] - 1
```

- Keys must be unique.
- Membership with `in` checks keys.
- Updating an existing key replaces its value.

---

## Counters

Dictionaries are useful for counting categories.

```python
departments = ["Sales", "Ops", "Sales", "HR", "Ops"]
counts = {}

for department in departments:
    if department not in counts:
        counts[department] = 0
    counts[department] = counts[department] + 1
```

This pattern appears in data cleaning, survey analysis, transaction summaries, and text analysis.

---

## Looping Through Dictionaries

```python
counts = {"Sales": 2, "Ops": 2, "HR": 1}

for department in counts:
    print(department, counts[department])

for department, count in counts.items():
    print(department, count)
```

| Pattern | Gives You |
|---|---|
| `for key in d` | Each key |
| `d.keys()` | Dictionary keys |
| `d.values()` | Dictionary values |
| `d.items()` | Key-value pairs |

---

## Lists And Dictionaries Together

Real data often needs nested collections.

```python
employees = [
    {"name": "Asha", "department": "Sales", "sales": 14},
    {"name": "Ben", "department": "Ops", "sales": 7},
    {"name": "Caro", "department": "Sales", "sales": 10},
]
```

- A list of dictionaries can represent records.
- A dictionary of lists can group values by category.
- Accumulation builds summaries one row at a time.

---

<!-- _class: section -->

## Functions

Built-ins, user-defined functions, composition, docstrings, scope, stack diagrams, and tracebacks

---

## Built-In Functions

Python includes reusable functions for common work.

```python
scores = [4, 5, 3, 5, 4]

len(scores)
sum(scores)
round(sum(scores) / len(scores), 2)
```

Before writing a new function, check whether Python already provides the operation you need.

---

## Defining And Calling Functions

Functions package a reusable calculation.

```python
def profit_margin(revenue, cost):
    profit = revenue - cost
    return profit / revenue

margin = profit_margin(1250, 875)
```

- Parameters name the inputs inside the function.
- Arguments are the actual values passed during a call.
- `return` sends a result back to the caller.

---

## Function Composition

Function calls can be combined.

```python
def total(values):
    return sum(values)

def average(values):
    return total(values) / len(values)

rounded_average = round(average([4, 5, 3]), 2)
```

Composition helps you build larger calculations from smaller pieces that are easier to test.

---

## Docstrings And Repetition

Docstrings explain what a function expects and returns.

```python
def reorder_needed(inventory, threshold):
    """Return True when inventory is below the threshold."""
    return inventory < threshold
```

Functions reduce repetition when the same rule appears in multiple places.

```python
for quantity in [12, 4, 19]:
    print(reorder_needed(quantity, 10))
```

---

## List Arguments

Lists passed to functions can be modified in place.

```python
def add_tax_amount(amounts, tax):
    amounts.append(tax)

charges = [20, 35]
add_tax_amount(charges, 4)
```

If a function should not change the original list, make a copy or return a new list.

```python
def with_tax_amount(amounts, tax):
    return amounts + [tax]
```

---

## Scope

Scope controls where names can be used.

```python
def discount(price):
    rate = 0.10
    return price * (1 - rate)

sale_price = discount(50)
```

- `rate` is local to the function.
- `sale_price` is assigned outside the function.
- Clear parameters are better than relying on outside variables.

---

## Stack Diagrams

A stack diagram tracks function calls and local variables.

```python
def add_fee(price):
    fee = 3
    return price + fee

def final_price(price):
    return add_fee(price) * 1.08

total = final_price(20)
```

Each active function call has its own frame. Frames help explain why local variables do not exist everywhere.

---

## Tracebacks

Tracebacks show where Python found an error.

```python
def average(values):
    return sum(values) / len(values)

average([])
```

Read from the bottom up:

1. Identify the exception type.
2. Read the message.
3. Find the line that caused the error.
4. Inspect the values used on that line.

---

## Common Error Signals

| Error Signal | What To Check |
|---|---|
| `NameError` | Was the variable assigned before it was used? |
| `TypeError` | Did the operation receive the wrong kind of value? |
| `IndexError` | Did the code ask for a list position that does not exist? |
| `KeyError` | Did the dictionary contain the requested key? |
| `ZeroDivisionError` | Could the denominator be zero? |

Debugging is part of analysis: read the traceback, inspect the relevant values, and test a smaller example.

---

## How The Pieces Fit Together

```python
orders = [
    {"region": "East", "total": 64},
    {"region": "West", "total": 42},
    {"region": "East", "total": 91},
]

def summarize_by_region(rows):
    totals = {}
    for row in rows:
        region = row["region"]
        totals[region] = totals.get(region, 0) + row["total"]
    return totals
```

This combines dictionaries, lists, loops, accumulation, and a function with a clear return value.

---

## What To Practice

- Trace variable values through short examples.
- Explain whether code uses a list, dictionary, loop, or function, and why.
- Convert business rules into Boolean expressions and conditionals.
- Build counters and totals from a list of values or records.
- Read tracebacks carefully before changing code.

<div class="callout">

Chapter 03 assumes these basics so NumPy arrays and pandas objects feel like extensions of ideas you already know.

</div>
