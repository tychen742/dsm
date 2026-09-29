# Chapter 06 Materials

## Purpose

Chapter 06 introduces Matplotlib for explicit control over Python visualizations.

## Active Source Notebooks

- `0600-matplotlib.ipynb` - Landing: Chapter orientation, video, learning goals, flow, glossary, and slides.
- `0601-mpl.ipynb` - Matplotlib Basics and Stateful Plotting: Matplotlib introduction, syntax styles, stateful pyplot commands, first plots, labels, titles, legends, and subplots.
- `0602-figures-axes.ipynb` - Matplotlib Figures and Axes: Object-oriented figures and axes, `plt.subplots()`, multiple axes, `fig.suptitle()`, and saving figures with `dpi=`.
- `0603-controls-plot-types.ipynb` - Matplotlib Controls and Common Plot Types: Figure and axes controls, styles, colors, line settings, common plot types, `add_axes()`, and DPI.

## Student Assignments

- `assignments/index.ipynb` - assignment landing page.
- `assignments/preview.ipynb` - server-graded preview quiz covering glossary and core terms.
- `assignments/lab.ipynb` - Chapter 06 server-graded lab (`ch06-lab`) with five plotting questions set in one small retailer: revenue trend line, actual vs forecast lines with legend, a two-panel bar and histogram dashboard with `suptitle`, an ad spend vs sales scatter with axis limits, and a report figure saved with `savefig` at a set dpi. Graded by the `matplotlib` runner profile with `plot_checks` in `_html_extra/api/lib/quiz-app.php`; regression test in `tests/grader/test_ch06_lab.py`.
- `assignments/homework.ipynb` - Chapter 06 server-graded homework (`ch06-homework`) with five true/false questions and five plotting questions that extend the lab: sales vs target with line width and markers, two overlapping histograms with `alpha`, a full-year chart with a Q4 `add_axes()` inset, a three-region `sharey=True` comparison built in a `zip()` loop, and a `df.plot(ax=ax)` chart finished with Matplotlib. Coding questions are graded by the `matplotlib` runner profile with `plot_checks`; regression test in `tests/grader/test_ch06_homework.py`.

## Figures And Media

- `0602-figures-axes.ipynb` saves an example figure to `../../_build/generated/filename.png`.
- The Q5 lab solution writes `regional_margin_q2.png` next to `lab.ipynb` when executed; the file is ignored in `.gitignore`.
- Chapter overview video embedded in `0600-matplotlib.ipynb`.

## Supporting Code And Data

- No external project datasets; examples use generated arrays and in-notebook values.

## Slide Deck

- Source: `_html_extra/chapters/06-matplotlib/overview.md`.
- Rendered HTML: `_html_extra/chapters/06-matplotlib/overview.html`.
- Status: verified during the landing-page alignment pass.

## Archived Or Unlisted Material

- No archived or unlisted notebooks for this chapter.

## Maintenance Notes

- Active content section count: 3.
- No unlisted active notebooks remain in `chapters/06-matplotlib/`.
