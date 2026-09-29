# Chapter 06 Materials

## Purpose

Chapter 06 introduces Matplotlib for explicit control over Python visualizations.

## Active Source Notebooks

- `0600-matplotlib.ipynb` - Landing: Chapter orientation, video, learning goals, flow, glossary, and slides.
- `0601-mpl.ipynb` - Matplotlib Basics: Matplotlib introduction, installation, syntax styles, stateful pyplot commands, first plots, labels, titles, legends, and `plt.subplot()` layouts.
- `0602-figures-axes.ipynb` - Figures and Axes: Object-oriented figures and axes with `plt.subplots()`, multiple axes, `fig.suptitle()` and `sharey`; manual placement and insets with `fig.add_axes()`; figure size, DPI, and saving figures with `dpi=`.
- `0603-controls-plot-types.ipynb` - Styling and Plot Types: Style sheets and `rcParams`, legends, axis ranges, colors and line and marker styles; common plot types (scatter, bar, histogram, boxplot), each with a one-sentence business takeaway; six exercises; a closing Quick Reference table.

## Student Assignments

- `assignments/index.ipynb` - assignment landing page.
- `assignments/preview.ipynb` - server-graded preview quiz: ten glossary questions (figure, stateful interface, `plt.subplots()`, figure title, shared axis, inset axes, DPI, alpha, format string, boxplot); consistency test in `tests/grader/test_ch06_preview.py`.
- `assignments/lab.ipynb` - Chapter 06 server-graded lab (`ch06-lab`) with five plotting questions set in one small retailer: revenue trend line, actual vs forecast lines with legend, a two-panel bar and histogram dashboard with `suptitle`, an ad spend vs sales scatter with axis limits, and a report figure saved with `savefig` at a set dpi. Graded by the `matplotlib` runner profile with `plot_checks` in `_html_extra/api/lib/quiz-app.php`; regression test in `tests/grader/test_ch06_lab.py`.
- `assignments/homework.ipynb` - Chapter 06 server-graded homework (`ch06-homework`) with five true/false questions and five plotting questions that extend the lab: sales vs target with line width and markers, two overlapping histograms with `alpha`, a full-year chart with a Q4 `add_axes()` inset, a three-region `sharey=True` comparison built in a `zip()` loop, and a `df.plot(ax=ax)` chart finished with Matplotlib. Coding questions are graded by the `matplotlib` runner profile with `plot_checks`; regression test in `tests/grader/test_ch06_homework.py`.

## Figures And Media

- `0602-figures-axes.ipynb` saves an example figure to `../../_build/generated/monthly_revenue.png`.
- The Q5 lab solution writes `regional_margin_q2.png` next to `lab.ipynb`, and the `0602` Saving Figures exercise solution writes `quarterly_revenue.png` next to the notebook, when executed; both files are ignored in `.gitignore`.
- Chapter overview video embedded in `0600-matplotlib.ipynb`.

## Supporting Code And Data

- No external project datasets. Section examples and assignments use one small retailer's data, defined inline in each cell so it runs on its own in Live Code: monthly and quarterly revenue, regions (North, South, East, West), stores, products, ad spend, daily sales with a promotion week, order values, and warehouse delivery times. Random data uses a fixed seed (`np.random.default_rng(...)`).
- The `Line and marker styles` gallery in `0603` keeps simple `x` values on purpose: it is a side-by-side catalog of styles.
- Setup cells after each section title are tagged `hide-input`, `thebe-init`, and `runnable`, so Live Code runs the imports automatically.

## Slide Deck

- Source: `_html_extra/chapters/06-matplotlib/overview.md`.
- Rendered HTML: `_html_extra/chapters/06-matplotlib/overview.html`.
- Status: rewritten 2026-09-29 (24 slides) from the current sections: roadmap, goals, one divider per section, code taken from the notebooks' business examples, plot-type chooser, vocabulary, and practice. Every slide was rendered to an image and checked for overflow.
- Regenerate after edits (from the repo root): `npx @marp-team/marp-cli --no-stdin --html _html_extra/chapters/06-matplotlib/overview.md -o _html_extra/chapters/06-matplotlib/overview.html`. `--no-stdin` matters when running from a script or non-interactive shell; without it marp-cli waits for input on stdin.
- The front matter is ch03's, plus the template's `.cols`, `pre`, and callout-variant rules for the two-column slides.

## Archived Or Unlisted Material

- No archived or unlisted notebooks for this chapter.

## Maintenance Notes

- Active content section count: 3.
- No unlisted active notebooks remain in `chapters/06-matplotlib/`.
