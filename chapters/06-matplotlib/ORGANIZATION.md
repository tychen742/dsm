# Chapter 06 Organization

## Chapter Role

Chapter 06 teaches Matplotlib as the lower-level plotting tool students can use when pandas plotting is not enough.

## Learning Goals

Students should be able to:

1. Create basic Matplotlib figures and axes.
2. Plot common chart types with explicit labels and titles.
3. Customize chart appearance to support clear communication.
4. Use Matplotlib when a business chart needs more control than pandas plotting provides.

## Sequence

1. `0600-matplotlib.ipynb` - Landing
   - Chapter orientation, video, learning goals, flow, glossary, and slides.
2. `0601-mpl.ipynb` - Matplotlib Basics and Stateful Plotting
   - Matplotlib introduction, syntax styles, stateful pyplot commands, first plots, labels, titles, legends, and subplots.
3. `0602-figures-axes.ipynb` - Matplotlib Figures and Axes
   - Object-oriented figures and axes, `plt.subplots()`, multiple axes, `fig.suptitle()`, and saving figures with `dpi=`.
4. `0603-controls-plot-types.ipynb` - Matplotlib Controls and Common Plot Types
   - Figure and axes controls, styles, colors, line settings, common plot types, `add_axes()`, and DPI.
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
- Lab: server-graded plotting practice on one retailer's data: line plot with markers and labels (0601/0602), styled lines with a legend (0603), a 1x2 bar and histogram dashboard with `suptitle` (0602/0603), a scatter plot with axis limits (0603), and a saved report figure with `figsize` and `dpi` (0602). The grader checks chart properties, so pyplot and object-oriented solutions both pass.
- Homework: server-graded reinforcement with five scenario-based true/false concept checks and five coding questions covering the chapter's main technical practice.

## Maintenance Notes

- Chapter overview slides are present and linked from the landing page.
- Media and data references are recorded in `MATERIALS.md`.
- Archived material, if any, is outside the active chapter folder.
