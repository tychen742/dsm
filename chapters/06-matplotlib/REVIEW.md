---
orphan: true
---

# Chapter 06 Quality Review

Review date: 2026-09-28. Scope: landing page, `0601`–`0603`, assignments, planning docs, slides, and the preview answer key.

Verification: `0601`–`0603` executed with the project `.venv` (Matplotlib 3.11.2). No errors; one deprecation warning (`boxplot(vert=...)`).

Status legend: `[ ]` open, `[x]` done, `[-]` skipped/deferred (note why).

## Suggested Fix Order

1. Remove visible duplicate solutions (M3).
2. Rewrite lab and homework coding questions as real plotting tasks with a plot-checking grader (M1, M2, M5).
3. Align the landing page and rebuild the glossary from section content (M4, S7).
4. Restructure sections: move `add_axes()` to `0602`, fix the `0601` opening, add index tags and closing sections (S6, S8, S10).
5. Add business-context examples (S9).
6. Rebuild slides, update `MATERIALS.md` and `ORGANIZATION.md`, run the book build (S12).

## Must Fix

### M1. Lab does not use Matplotlib

- [ ] Replace all five questions in `assignments/lab.ipynb`.

Current questions are print/string/arithmetic drills (Q3 multiplies rows by columns; Q5 builds a filename string). None creates a figure or axes.

Fix notes:

- Questions should build real plots: line chart with labels, `plt.subplots()` grid, legend, axis limits, plot-type choice on business data.
- The grader must check plot state rather than stdout, e.g. `ax.get_title()`, `len(fig.axes)`, `ax.get_xlim()`, `len(ax.lines)`, `ax.get_legend()`.
- Confirm the server grader venv has `matplotlib` installed and uses a non-interactive backend (`Agg`).
- Update the `ch06-lab` entry in `_html_extra/api/lib/quiz-app.php` to match.
- Re-execute solution cells and commit their outputs.

### M2. Homework coding questions do not use Matplotlib

- [ ] Replace Q6–Q10 in `assignments/homework.ipynb`.

Current questions compute figure area, inches times DPI, and similar. Q7 and Q10 are the same append-in-a-loop task with different labels.

Fix notes:

- Extend the lab rather than repeat it (e.g. `fig.suptitle`, `sharex`, `savefig` with DPI, line styles for actual vs forecast, histogram bins).
- Same grader approach as M1; update the `ch06-homework` entry.

### M3. Nine exercise answers are visible without clicking

- [x] Delete the untagged duplicate `### Solution` cells that follow each hidden solution:
  - [x] `0601-mpl.ipynb` cell 27
  - [x] `0602-figures-axes.ipynb` cell 20
  - [x] `0603-controls-plot-types.ipynb` cells 28, 35, 41, 47, 59, 67, 74

Done 2026-09-28. Kept the tagged `hide-input` solutions (which carry committed output) and removed the visible duplicates. Verified: notebooks validate with `nbformat`; all 10 exercises are still followed by a hidden solution cell with output; no visible `### Solution` cells remain.

### M4. Landing page does not follow the standard layout

File: `0600-matplotlib.ipynb`

- [ ] Remove the empty `<h2>Overview</h2>` heading.
- [ ] Add 3–5 overview bullets in `- **Concept Term**: Short description.` format.
- [ ] Remove the `{contents}` block (landing pages do not use it).
- [ ] Rename "Learning Goals" to "Learning Objectives".
- [ ] Use the standard video credit: linked `Title (M:SS)` plus "Hosted on YouTube; property of its original creator, embedded here for educational reference only." Keep the existing video (UO98lJQ3QGI).
- [ ] Add the link color style to the slides heading: `style="color: var(--pst-color-link, #176de8);"`.

### M5. Homework true/false questions restate definitions

- [ ] Rewrite Q1–Q5 in `assignments/homework.ipynb` as short management or workplace scenarios that require applying the concept.
- [ ] Keep a 3:2 or 2:3 True/False balance (currently 3 True, 2 False).

Q4 ("saving a figure is useful for a report") is true on its face and tests nothing.

## Should Fix

### S6. Section balance and structure

- [ ] Move `## OO with add_axes()` (and its DPI subsection, or relocate DPI to Figure-Level Controls) from `0603` to `0602`.
  - `0603` is 76 cells and 1.5 MB; `0602` has only one `##` heading.
  - `0602` cell 5 already promises `add_axes()`, and the section title "Figures and Axes" fits it.
- [ ] Fix the `0601` opening:
  - Merge import cells 1 and 6 into one `hide-input` cell right after the title.
  - Move `{contents}` directly after the imports cell.
  - Turn Introduction/Installation into regular content after the contents block.
  - Promote or re-home "Two Styles of Matplotlib Syntax" (currently an orphan `###` under Introduction).
  - Reach at least three `##` headings.
- [ ] Add an exercise for "Saving Figures" in `0602`.
- [ ] Reconcile the save path: code writes to `../../_build/generated`; `MATERIALS.md` says `../../figures/`.

### S7. Glossary and learning objectives drift from content

- [ ] Remove or teach glossary terms with no real coverage: Artist (never taught), Style sheet, Tick.
- [ ] Add terms that are taught: `plt.subplots()`, `savefig`, DPI, `tight_layout`, rcParams, format string, alpha, inset axes, boxplot, stateful (pyplot) interface.
- [ ] Revise objectives with no matching content: #1 (artists), #3 ("scales"), #5 (customization layer under pandas and Seaborn). Either add content or reword.
- [ ] Align `ORGANIZATION.md` Learning Goals (4 items) with the landing page (5 items).
- [ ] Regenerate the preview questions from the revised glossary.

### S8. No index entries

- [ ] Add `{index}` directives near each substantive `##` and `###` heading in `0601`–`0603`.

### S9. Weak business context

- [ ] Replace most `sin(x)` / `x**2` / A–D examples with business data (quarterly revenue, regional sales, forecast vs actual, customer visits).
- [ ] Reuse datasets already introduced in earlier chapters where possible.

Only the sales/visits exercise in `0603` is currently a business case.

### S10. Missing closing sections

- [ ] Add Summary and Further Reading (and References if sources are cited) to `0601` and `0602`.
- [ ] Expand the `0603` Recap into a Summary; add Further Reading.
- [ ] Delete the trailing empty cell at the end of `0603`.

### S11. Preview answer key is a fixed pattern

- [ ] Shuffle the correct-answer positions for `ch06-preview` in `_html_extra/api/lib/quiz-app.php` and in `preview.ipynb`.
- [ ] Book-wide follow-up: ch07 and ch08 use the same A-B-C-D-A-B… key. Decide whether to fix all chapters.

### S12. Slides are still the template

- [ ] Rewrite `_html_extra/chapters/06-matplotlib/overview.md` with real section content and key code patterns.
- [ ] Regenerate `overview.html` with `npx @marp-team/marp-cli --html ...`.
- [ ] Correct the "verified" status line in `MATERIALS.md`.

## Could Defer

- [ ] Suppress stray return-value output in 22 cells (`Text(0.5, 1.0, ...)`, `[<matplotlib.lines.Line2D ...>]`): end cells with `;` or `plt.show()`, then re-execute. Counts: `0601` 5, `0602` 2, `0603` 15.
- [ ] Replace deprecated `ax.boxplot(..., vert=True)` with `orientation='vertical'` (deprecated in 3.11, removed in 3.13).
- [ ] Fix typos in `0603`:
  - [ ] "aviaible"
  - [ ] `pt.rcParams`
  - [ ] unclosed backtick in "`axes[2]"
  - [ ] "insert axes" → "inset axes"
  - [ ] curly quotes in the linestyle comment
  - [ ] `matplotlib.style.use` → `plt.style.use` for consistency
- [ ] Seed random data (histogram `random.sample`, boxplot `np.random.normal`, sales exercise `np.random.normal`) so outputs are stable.
- [ ] Fix the `0603` inset exercise prompt (cell 65): it says `x = np.linspace(0, 5, 50)` is defined, but the setup cell defines `np.linspace(0, 10, 50)`.
- [ ] Confirm whether the AGENTS.md "Spring 2026: chapters 1–8 are frozen" note is still in effect for Fall 2026.

## Completion Checklist

- [ ] Notebook JSON validates for every changed file.
- [ ] `0601`–`0603` and assignment solution cells re-executed; outputs committed.
- [ ] Grader updated and tested for `ch06-lab` and `ch06-homework`.
- [ ] `MATERIALS.md` and `ORGANIZATION.md` updated.
- [ ] Slides regenerated.
- [ ] Book build passes with no new warnings for ch06.
