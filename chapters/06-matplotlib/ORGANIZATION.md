# Chapter 06 Organization

## Chapter Role

Chapter 06 teaches Matplotlib as the lower-level plotting tool students can use when pandas plotting is not enough.

## Learning Goals

Students should be able to:

1. Distinguish a figure from its axes and build single- and multi-chart figures with `plt.subplots()`.
2. Create line, bar, scatter, histogram, and box plots that match a management question about trend, comparison, relationship, or distribution.
3. Label and style charts with titles, axis labels, legends, colors, line styles, markers, transparency, and axis ranges.
4. Arrange charts for comparison with subplots, shared axes, figure titles, and `add_axes()` insets.
5. Set figure size and resolution, save figures for reports, and finish pandas plots with Matplotlib methods.

These match the Learning Goals on `0600-matplotlib.ipynb`.

## Sequence

1. `0600-matplotlib.ipynb` - Landing
   - Chapter orientation, video, learning goals, flow, glossary, and slides.
2. `0601-mpl.ipynb` - Matplotlib Basics
   - Matplotlib introduction, installation, syntax styles, stateful pyplot commands, first plots, labels, titles, legends, and `plt.subplot()` layouts.
3. `0602-figures-axes.ipynb` - Figures and Axes
   - Object-oriented figures and axes with `plt.subplots()`, multiple axes, `fig.suptitle()` and `sharey`; manual placement and insets with `fig.add_axes()`; figure size, DPI, and saving figures with `dpi=`.
4. `0603-controls-plot-types.ipynb` - Styling and Plot Types
   - Figure and axes control tables, `rcParams` styling, legends, axis ranges, colors and line settings, and common plot types.
5. `assignments/index.ipynb` - Assignments
   - Preview
   - Lab
   - Homework

## Topic Coverage Review

- Coverage status: aligned with the current notebooks and `_toc.yml`.
- Landing page is limited to orientation, video, learning goals, chapter flow, glossary, and slide link.
- Detailed teaching content lives in the content section notebooks.

## Section Organization Review

- Active content section count: 3.
- Organization status: passes the preferred 2-5 section range.

## Exercise And Assignment Plan

- Preview: introduce the chapter vocabulary and core terms before class.
- Lab: server-graded plotting practice on one retailer's data: line plot with markers and labels (0601/0602), styled lines with a legend (0603), a 1x2 bar and histogram dashboard with `suptitle` (0602/0603), a scatter plot with axis limits (0603), and a saved report figure with `figsize` and `dpi` (0602 Figure Size, Resolution, and Saving). The grader checks chart properties, so pyplot and object-oriented solutions both pass.
- Homework: server-graded reinforcement with five true/false concept checks and five plotting questions that extend the lab rather than repeat it: line width and marker shape (0603), overlapping histograms with `alpha` (0603), an `add_axes()` inset (0602), a shared-y comparison with an axes loop (0602/0603), and pandas plotting finished with Matplotlib (links ch05 and learning goal 4).

## Maintenance Notes

- Chapter overview slides are present and linked from the landing page.
- Media and data references are recorded in `MATERIALS.md`.
- Archived material, if any, is outside the active chapter folder.
