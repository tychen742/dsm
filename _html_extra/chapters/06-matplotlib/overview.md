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
  pre { background: #f6f8fa !important; border: 1px solid #d0e8d4; border-radius: 6px; margin: 8px 0; font-size: 0.68em; line-height: 1.35; }
  pre code { color: inherit; background: none; border: none; padding: 10px 12px; }
  .cols { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; align-items: start; }
  .cols.r64 { grid-template-columns: 6fr 4fr; }
  .callout.warn { background: #fff8e1; border-color: #b8860b; }
  .callout.rule { background: #f0f4ff; border-color: #5577cc; }
---

<!-- _class: title -->

# Chapter 6: Matplotlib

Explicit control over figures, axes, and chart styling

*Sections: Matplotlib basics · Figures and axes · Styling and plot types*

*Use arrow keys or Space to navigate · Press F for fullscreen*

---

## Chapter Roadmap

| Part | Main Question | Core Vocabulary |
|---|---|---|
| Matplotlib basics | How do I draw and label a first chart? | pyplot, stateful interface, line plot, legend |
| Figures and axes | How do I build and arrange charts on purpose? | figure, axes, `plt.subplots()`, inset, DPI |
| Styling and plot types | How do I style a chart and pick the right type? | rcParams, axis range, alpha, histogram, boxplot |

<div class="callout">

pandas plotting (Chapter 5) is built on Matplotlib. This chapter shows the layer underneath, for when a business chart needs more control.

</div>

---

## Chapter Goals

By the end of this chapter, you will be able to:

1. Distinguish a figure from its axes and build single- and multi-chart figures with `plt.subplots()`.
2. Create line, bar, scatter, histogram, and box plots that match a management question about trend, comparison, relationship, or distribution.
3. Label and style charts with titles, axis labels, legends, colors, line styles, markers, transparency, and axis ranges.
4. Arrange charts for comparison with subplots, shared axes, figure titles, and `add_axes()` insets.
5. Set figure size and resolution, save figures for reports, and finish pandas plots with Matplotlib methods.

---

<!-- _class: section -->

## Matplotlib Basics

First plots, labels, and the pyplot interface

---

## Two Ways to Use Matplotlib

| | Stateful (pyplot) | Object-oriented |
|---|---|---|
| Looks like | `plt.plot()`, `plt.title()` | `fig, ax = plt.subplots()`, `ax.set_title()` |
| Acts on | The current figure and axes | The figure and axes you name |
| Best for | Quick, one-off exploration | Most real charts, especially several at once |

```python
import matplotlib.pyplot as plt   # the plotting module, always imported as plt
```

<div class="callout">

"Stateful" means pyplot quietly tracks a current figure and axes; each `plt.*` call changes whatever is current.

</div>

---

## A First Line Plot

<div class="cols">
<div>

```python
month = np.arange(1, 7)
revenue = np.array([110, 104, 118,
                    121, 125, 119])

plt.figure(figsize=(4, 3))
plt.plot(month, revenue, c='red',
         label='Revenue')
plt.xlabel('Month')
plt.ylabel('Revenue ($K)')
plt.title('Monthly Revenue')
plt.legend()
```

</div>
<div>

- `plt.figure(figsize=...)` sets the canvas size in inches.
- `plt.plot(x, y)` draws a line: good for a **trend**.
- `label=` names the line; `plt.legend()` shows it.
- Every chart needs a title and axis labels with units.

<div class="callout rule">

pandas does the same in one call: `df.plot(x='month', y='revenue', title='Monthly Revenue')`.

</div>

</div>
</div>

---

## Scatter Plots and `plt.subplot()`

<div class="cols">
<div>

**Relationship between two measures**

```python
ad_spend = np.array([5, 10, 15, 20, 25, 30])
sales = np.array([60, 85, 110, 120, 150, 165])

plt.scatter(ad_spend, sales)
```

</div>
<div>

**Two charts in a grid, stateful style**

```python
plt.figure(figsize=(8, 3))
plt.subplot(1, 2, 1)     # 1 row, 2 cols, chart 1
plt.plot(month, revenue, 'r--')
plt.subplot(1, 2, 2)     # chart 2
plt.plot(month, units, 'g*-')
```

</div>
</div>

<div class="callout warn">

`plt.subplot()` (singular) is the older way. For new code, use `plt.subplots()` (plural), next section.

</div>

---

<!-- _class: section -->

## Figures and Axes

Building, arranging, sizing, and saving charts

---

## Figure vs Axes

<div class="cols r64">
<div>

| | Figure | Axes |
|---|---|---|
| What it is | The whole canvas | One chart on the canvas |
| Contains | One or more axes | Data, ticks, labels, title, legend |
| Made by | `plt.figure()`, `plt.subplots()` | `plt.subplots()`, `fig.add_axes()` |

Most formatting is done with **axes methods**: `ax.set_title()`, `ax.set_xlabel()`, `ax.set_ylabel()`, `ax.legend()`.

</div>
<div>

```text
Figure
└── Axes (one chart)
    ├── XAxis
    ├── YAxis
    ├── Title
    ├── Lines / Bars
    └── Legend
```

</div>
</div>

---

## `plt.subplots()`: The Everyday Workflow

<div class="cols">
<div>

**One chart**

```python
fig, ax = plt.subplots(figsize=(4, 3))
ax.plot(month, revenue, 'g--')
ax.set_xlabel('Month')
ax.set_ylabel('Revenue ($K)')
ax.set_title('Monthly Revenue')
```

</div>
<div>

**Several charts: `axes` is an array**

```python
fig, axes = plt.subplots(1, 2, figsize=(6, 2))
axes[0].plot(month, store_a, 'r--')
axes[0].set_title('Store A')
axes[1].plot(month, store_b, 'g*-')
axes[1].set_title('Store B')
```

</div>
</div>

<div class="callout">

`plt.subplots()` returns the figure and its axes together; unpack them with `fig, ax = ...` or `fig, axes = ...`.

</div>

---

## Loop, Tidy, and Title the Figure

<div class="cols">
<div>

```python
fig, axes = plt.subplots(1, 2, figsize=(6, 2))
for ax, sales, name in zip(axes,
                           [store_a, store_b],
                           ['Store A', 'Store B']):
    ax.plot(month, sales)
    ax.set_xlabel('Month')
    ax.set_ylabel('Sales ($K)')
    ax.set_title(name)
plt.tight_layout()
```

</div>
<div>

```python
fig, axes = plt.subplots(1, 2, figsize=(8, 3),
                         sharey=True)
axes[0].plot(quarters, north, marker='o')
axes[1].plot(quarters, south, marker='o')
fig.suptitle('Quarterly Revenue by Region ($K)')
```

- `zip()` pairs each axes with its data and title.
- `tight_layout()` fixes overlapping labels.
- `sharey=True`: same scale, **fair comparison**.
- `fig.suptitle()` titles the whole figure.

</div>
</div>

---

## Insets with `add_axes()`

<div class="cols">
<div>

```python
fig = plt.figure(figsize=(4, 3))
main = fig.add_axes([0.1, 0.1, 0.8, 0.8])
inset = fig.add_axes([0.2, 0.5, 0.25, 0.3])

main.plot(day, daily_sales)
main.set_title('Daily Sales in June')

inset.plot(day[14:21], daily_sales[14:21], 'r')
inset.set_title('Promotion Week')
```

</div>
<div>

`[left, bottom, width, height]` are **fractions of the figure**:

| Value | Meaning |
|---|---|
| `0.1, 0.1` | Start 10% from the left and bottom |
| `0.8, 0.8` | Take 80% of the width and height |

<div class="callout rule">

Use `plt.subplots()` for grids; use `add_axes()` only when you need exact placement, such as a zoomed inset.

</div>

</div>
</div>

---

## Size, Resolution, and Saving

<div class="cols">
<div>

```python
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(quarters, revenue, marker='o')
ax.set_title('Quarterly Revenue')

fig.savefig('quarterly_revenue.png', dpi=150)
```

</div>
<div>

| Setting | Controls | Typical value |
|---|---|---|
| `figsize=(w, h)` | Size in inches | `(6, 3)` for a slide |
| `dpi=` | Dots per inch | 100 screen, 200–300 print |
| File extension | Format | `.png`, `.pdf`, `.svg` |

</div>
</div>

<div class="callout warn">

A chart that looks sharp on screen can print blurry. Save report figures with `dpi=` of 200 or more.

</div>

---

<!-- _class: section -->

## Styling and Plot Types

Styling charts and matching the chart to the question

---

## Figure Methods vs Axes Methods

<div class="cols">
<div>

**Figure: the whole canvas**

| Method | Sets |
|---|---|
| `fig.suptitle()` | Title over all charts |
| `fig.tight_layout()` | Spacing |
| `fig.savefig()` | Saved file |
| `fig.set_size_inches()` | Size |

</div>
<div>

**Axes: one chart**

| Method | Sets |
|---|---|
| `ax.set_title()` | Chart title |
| `ax.set_xlabel()`, `ax.set_ylabel()` | Axis labels |
| `ax.set_xlim()`, `ax.set_ylim()` | Axis ranges |
| `ax.legend()`, `ax.grid()` | Legend, grid |

</div>
</div>

---

## Defaults, Legends, and Axis Ranges

<div class="cols">
<div>

**Change defaults for every later chart**

```python
plt.style.use('ggplot')             # a style sheet
plt.rcParams['figure.dpi'] = 150    # one setting
```

**Label each series, then place the legend**

```python
ax.plot(month, laptops, label='Laptops')
ax.plot(month, phones, label='Phones')
ax.legend(loc='lower right')
```

</div>
<div>

**Zoom in on the promotion week**

```python
ax.plot(day, daily_sales)
ax.set_xlim(14, 22)
ax.set_ylim(30, 80)
```

<div class="callout">

Axis ranges change what the reader sees, not the data. Starting a bar chart's y-axis above zero can exaggerate small differences.

</div>

</div>
</div>

---

## Colors, Line Styles, and Markers

<div class="cols">
<div>

```python
ax.plot(month, actual, 'b.-')     # format string
ax.plot(month, budget, color='green',
        ls='--', lw=1, marker='s')
ax.plot(month, north, color='#8B008B',
        alpha=0.5)                # hex color, half transparent
```

</div>
<div>

| Parameter | Short form | Example |
|---|---|---|
| `color` | `c` | `'red'`, `'#FF8C00'` |
| `linestyle` | `ls` | `'-'`, `'--'`, `':'` |
| `linewidth` | `lw` | `2.5` |
| `marker` | | `'o'`, `'s'`, `'^'` |
| `alpha` | | `0.5` (0 to 1) |

</div>
</div>

<div class="callout rule">

A format string such as `'r--'` sets color, line style, and marker in one argument.

</div>

---

## Choosing a Plot Type

| Management question | Plot type | Matplotlib |
|---|---|---|
| How did revenue change over the year? (**trend**) | Line plot | `ax.plot(x, y)` |
| Which department sold the most? (**comparison**) | Bar plot | `ax.bar(categories, values)` |
| Does a higher price mean fewer units sold? (**relationship**) | Scatter plot | `ax.scatter(x, y)` |
| What order values are typical? (**distribution**) | Histogram | `ax.hist(values, bins=10)` |
| Which warehouse delivers most consistently? (**distribution by group**) | Boxplot | `ax.boxplot([a, b, c])` |

<div class="callout">

Start from the question, then pick the chart. The same data can answer different questions with different charts.

</div>

---

## Plot Types in Code

<div class="cols">
<div>

```python
fig, ax = plt.subplots()
ax.bar(['Apparel', 'Electronics', 'Home', 'Toys'],
       [240, 410, 185, 120])
ax.set_title('Sales by Department ($K)')
```

```python
fig, ax = plt.subplots()
ax.hist(order_values, bins=10)
ax.set_xlabel('Order Value ($)')
```

</div>
<div>

```python
fig, ax = plt.subplots()
ax.boxplot(delivery_days)
ax.set_xticks([1, 2, 3],
              ['Warehouse A', 'Warehouse B',
               'Warehouse C'])
ax.set_ylabel('Delivery Time (days)')
```

A boxplot shows the median (line), the middle 50% (box), the typical range (whiskers), and **outliers** (circles).

</div>
</div>

---

## Three Workflows

| Workflow | Use it when | Start with |
|---|---|---|
| Stateful pyplot | Quick, one-off exploration | `plt.plot(x, y)` |
| `plt.subplots()` | Most charts, one or many | `fig, ax = plt.subplots()` |
| `fig.add_axes()` | Exact placement or an inset | `fig.add_axes([l, b, w, h])` |

<div class="callout rule">

Default to `plt.subplots()`. Every chart then has a named `ax` you can format, and every figure a named `fig` you can save.

</div>

---

## Chapter 6 Vocabulary

| # | Term | Short Meaning |
|---:|---|---|
| 1 | Figure | The whole canvas that holds one or more axes. |
| 2 | Axes | One chart inside a figure. |
| 3 | Stateful interface | pyplot functions that act on the current figure and axes. |
| 4 | Object-oriented interface | Figure and axes stored in variables; methods called on them. |
| 5 | Figure title | One title above all subplots (`fig.suptitle()`). |
| 6 | Shared axis | One axis range for every subplot (`sharey=True`). |
| 7 | Inset axes | A small chart placed on a larger one (`fig.add_axes()`). |
| 8 | DPI | Dots per inch: the resolution of a drawn or saved figure. |
| 9 | Alpha | Transparency from 0 (invisible) to 1 (opaque). |
| 10 | Boxplot | Median, quartiles, whiskers, and outliers of a distribution. |

---

## Practice

| Assignment | What it checks |
|---|---|
| Preview | Chapter vocabulary, before class |
| Lab | Five charts for one retailer: trend, actual vs forecast, dashboard, scatter, saved report figure |
| Homework | Scenario true/false questions and five charts: targets, overlapping histograms, an inset, shared axes, pandas plus Matplotlib |

<div class="callout">

The lab and homework are graded on the chart itself (axes, titles, labels, styles, saved files), so either plotting style earns credit.

</div>

---

## What To Carry Forward

After this chapter, students should be ready to:

- Build any chart with `fig, ax = plt.subplots()` and finish it with axes methods.
- Choose a chart type from the business question it has to answer.
- Arrange charts so comparisons are fair and the message is clear.
- Save report-ready figures, and fine-tune pandas and Seaborn charts through their Matplotlib axes.

---

<!-- _class: title -->

# End of Chapter 6

*Next: Chapter 7: Seaborn*
