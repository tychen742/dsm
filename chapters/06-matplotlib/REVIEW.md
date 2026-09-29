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

- [x] Replace all five questions in `assignments/lab.ipynb`. Code done 2026-09-28; goes live after the server steps below.

Current questions are print/string/arithmetic drills (Q3 multiplies rows by columns; Q5 builds a filename string). None creates a figure or axes.

Fix notes:

- Questions should build real plots: line chart with labels, `plt.subplots()` grid, legend, axis limits, plot-type choice on business data.
- The grader must check plot state rather than stdout, e.g. `ax.get_title()`, `len(fig.axes)`, `ax.get_xlim()`, `len(ax.lines)`, `ax.get_legend()`.
- Confirm the server grader venv has `matplotlib` installed and uses a non-interactive backend (`Agg`).
- Update the `ch06-lab` entry in `_html_extra/api/lib/quiz-app.php` to match.
- Re-execute solution cells and commit their outputs.

Grader findings (2026-09-28):

- Flow: page JS sends the first five `thebe-interactive` cells' code to `v1/lab-attempts.php` → `dsm_grade_lab_code_attempt()` → `dsm_run_lab_code_cell()` pipes JSON to `lib/python_lab_runner.py` → normalized stdout is compared exactly against `code_outputs` in `dsm_lab_definition()` / `dsm_homework_definition()`.
- The runner has two profiles only: `plain_python` (AST allowlist, a few builtins and methods, run with `-I -S`) and `pandas` (adds `pandas`/`numpy` imports and skips the method allowlist).
- Matplotlib cannot be graded today. Tested locally: `import matplotlib.pyplot as plt` is rejected ("Only pandas and numpy imports are allowed"). This likely explains why ch05–ch07 labs are print drills.
- List comprehensions are rejected in every profile (`ListComp is not allowed`), though `0603` teaches one.
- Cold Matplotlib start with an empty config dir took 10.1 s locally (font-cache build) against the 3 s timeout. Warm start was 0.42 s. The grader needs a persistent, writable `MPLCONFIGDIR`, or every submission will time out.
- `_html_extra/api/README.md` installs only `numpy pandas` in the production grader venv; `matplotlib` must be added there (not verified on the server).
- Security, out of scope for ch06: the `pandas` profile can read arbitrary server files (`pd.read_csv("/etc/hosts")` succeeded). Spun off as a separate task.

Proposed grader change:

1. Add a `matplotlib` runner profile: allow `numpy`, `pandas`, `matplotlib`, `matplotlib.pyplot` imports; call `matplotlib.use("Agg")` before import; set `MPLCONFIGDIR` from config; make `plt.show()` a no-op; replace `savefig` with a recorder so no files are written; allow `ListComp`/`comprehension`.
2. After running the code, the runner extracts a plot summary from every open figure (axes count, title, x/y labels, limits, line count with colors and styles, bar and patch counts, scatter point counts, legend labels, `suptitle`, figure size, DPI, recorded `savefig` calls).
3. Grade with property checks instead of exact stdout: each question in the definition lists only the properties it requires (e.g. `{"axes": 4, "ax[0].title": "North"}`), and the runner returns pass/fail per check with a short hint. Keep `code_outputs` stdout matching available for mixed questions.
4. Add `matplotlib` to `lab_grader` in `dsm_run_lab_code_cell()`'s profile allowlist, add `mplconfig_dir` to config, update the README install line.
5. Test script: run every reference solution plus common wrong answers through the runner and assert the scores.

Grader status (2026-09-28): items 1–4 built, not deployed. Details and the `plot_checks` path reference are in `_html_extra/api/README.md` ("Runner Profiles"). Verified: runner tests locally (Matplotlib 3.11.2) for pass/fail checks, blocked file access, bar/hist/scatter/pandas summaries, and the old profiles; PHP lint and an end-to-end grading harness in Docker (PHP 8.4, Matplotlib 3.10) including ch02/ch04 regression. Item 5 waits for the new ch06 questions.

Before the new lab goes live on the server:

- [x] `pip install matplotlib` in the grader venv (3.10.9).
- [x] `/var/www/dsm_private/mplconfig` (tychen:www-data, 2770) set as `mplconfig_dir` in the live config; font cache warmed.
- [x] `timeout_seconds` raised to 5; runner on the server Python takes 0.8–1.0 s.
- [-] Merge with the pandas-hardening task: that task's work was discarded 2026-09-29 (it was uncommitted and based on an old `main`). The underlying issue is recorded in `authoring/PROGRESS.md` Project TODOs.

#### New Lab (swapped in 2026-09-28)

Five plotting questions set in one small retailer, now in `assignments/lab.ipynb` with executed solution output:

| # | Title | Skills | Section source |
|---|---|---|---|
| 1 | Revenue Trend | `plt.subplots()`, line plot with markers, title, axis labels | 0601, 0602, 0603 markers |
| 2 | Actual vs Forecast | two lines, line style, color, labels, legend | 0601, 0603 |
| 3 | Regional Dashboard | 1x2 subplots, `figsize`, bar chart, histogram bins, `suptitle` | 0602, 0603 |
| 4 | Ad Spend and Sales | scatter plot, axis labels, `set_xlim`/`set_ylim` | 0601, 0603 |
| 5 | Report-Ready Figure | `figsize`, bar chart, `savefig` with filename and dpi | 0602, 0603 |

- [x] Questions and solutions in `lab.ipynb`; solution cells executed with outputs committed. Cell tags unchanged (`thebe-interactive`; `hide-input` + `lab-answer`).
- [x] `ch06-lab` in `quiz-app.php` switched from `code_outputs` to `runner_profile => 'matplotlib'` with `plot_checks`.
- [x] Test: `tests/grader/test_ch06_lab.py` reads questions and solutions from `lab.ipynb` and checks from `quiz-app.php` (via PHP or the php Docker image), then verifies solutions and filled-in submissions pass, unedited questions fail, and common wrong answers fail with a hint. Result: 27 passed, 0 failed. Run with `.venv/bin/python tests/grader/test_ch06_lab.py`.
- [x] `.gitignore`: `chapters/06-matplotlib/assignments/regional_margin_q2.png`, which the Q5 solution writes when the notebook executes.
- [x] Section alignment in `0602`: new `fig.suptitle()` example (two regional revenue panels plotted against quarter labels), and the `savefig` example now uses `dpi=200` with a sentence on screen vs print resolution. Outputs copied from an executed run; saved file verified at 200 dpi.
- The `data-lab-answers-release-at="2026-10-13..."` marker on the lab page is only a fallback when the settings API is unreachable; answer visibility follows the admin setting at `/api/admin/assignments.php`.
- Existing ch06-lab attempts keep the scores they were given under the old questions.
- Deployed 2026-09-28 (`4cb3cf1`, Build and Deploy run 36518745869). Live Q1 submission scored 2/2.

### M2. Homework coding questions do not use Matplotlib

- [x] Replace Q6–Q10 in `assignments/homework.ipynb`. Done 2026-09-28 on branch `ch06-homework`: five plotting questions (sales vs target, two stores with `alpha`, Q4 `add_axes()` inset, `sharey` regional comparison, `df.plot(ax=ax)` polish), solutions executed, `ch06-homework` switched to `plot_checks`, test `tests/grader/test_ch06_homework.py` (29 passed). Grader summary gained `alpha`, axes `position`, and figure `sharex`/`sharey`. `0602` now explains `sharey=True`.

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

Done 2026-09-28. Scope decided with the author: fix defects book-wide, keep the book's house style for the rest.

- [x] Remove the empty `<h2>Overview</h2>` heading (ch06 only; on ch03–ch05 the heading introduces real text and was kept).
- [x] Add 3–5 overview bullets in `- **Concept Term**: Short description.` format (ch06: five bullets from the section content).
- [x] Remove the `{contents}` block: removed from all nine landing pages. It rendered nothing, since landing headings are raw `<h2>`.
- [-] Rename "Learning Goals" to "Learning Objectives": kept "Learning Goals", the heading on all nine landing pages.
- [-] Standard video credit: kept the book's `video-credit` box, used on all nine landing pages.
- [x] Slides link color: added to ch05–ch09 (ch01–ch04 already had it).

### M5. Homework true/false questions restate definitions

- [x] Rewrite Q1–Q5 in `assignments/homework.ipynb` as short management or workplace scenarios that require applying the concept. Done 2026-09-28: dashboard title vs `suptitle`, object-oriented vs stateful plotting, plot type for a distribution, shared y-axis, and `savefig` dpi for print.
- [x] Keep a 3:2 or 2:3 True/False balance: now F, T, F, T, T (was T, T, F, T, F). The homework test checks the key against the solution cells and the balance.

Q4 ("saving a figure is useful for a report") is true on its face and tests nothing.

## Should Fix

### S6. Section balance and structure

Done 2026-09-28 on branch `ch06-sections` (outline approved by the author).

- [x] Move `## OO with add_axes()` (and its DPI subsection, or relocate DPI to Figure-Level Controls) from `0603` to `0602`. Now `0602` has `## Manual Placement with add_axes()` and `## Figure Size, Resolution, and Saving` (`figsize=` moved from `0603`, DPI, Saving Figures). Cell counts: `0602` 25 → 44, `0603` 70 → 54.
  - `0603` is 76 cells and 1.5 MB; `0602` has only one `##` heading.
  - `0602` cell 5 already promises `add_axes()`, and the section title "Figures and Axes" fits it.
- [x] Fix the `0601` opening: one hidden setup cell, `{contents}` right after it, Introduction/Installation/Two Styles grouped under `## Introduction`, and `## Multiple Plots with plt.subplot()` promoted, giving three `##` headings. The "usual headers" text now shows the imports as a code block.
  - Merge import cells 1 and 6 into one `hide-input` cell right after the title.
  - Move `{contents}` directly after the imports cell.
  - Turn Introduction/Installation into regular content after the contents block.
  - Promote or re-home "Two Styles of Matplotlib Syntax" (currently an orphan `###` under Introduction).
  - Reach at least three `##` headings.
- [x] Add an exercise for "Saving Figures" in `0602`: save a quarterly revenue chart as `quarterly_revenue.png` at `dpi=150` (file ignored in `.gitignore`).
- [x] Reconcile the save path: `MATERIALS.md` now records `../../_build/generated/filename.png`.

### S7. Glossary and learning objectives drift from content

Done 2026-09-29 on branch `ch06-glossary`.

- [x] Remove or teach glossary terms with no real coverage: removed Artist; kept Style sheet (`plt.style.use` in 0603 rcParams) and Tick (0602 figure/axes table, 0603 rcParams), with explanations tied to that content.
- [x] Add terms that are taught (glossary now 34 terms, each checked against the section text): `plt.subplots()`, `savefig`, DPI, `tight_layout`, rcParams, format string, alpha, inset axes, boxplot, stateful (pyplot) interface.
- [x] Revise objectives with no matching content (rewritten; five goals now map to 0601–0603 and the lab/homework): #1 (artists), #3 ("scales"), #5 (customization layer under pandas and Seaborn). Either add content or reword.
- [x] Align `ORGANIZATION.md` Learning Goals with the landing page (same five goals).
- [x] Regenerate the preview questions from the revised glossary: ten new questions; test `tests/grader/test_ch06_preview.py` (23 passed).

### S8. No index entries

- [x] Add `{index}` directives near each substantive `##` and `###` heading in `0601`–`0603`. Done 2026-09-29: 33 blocks (0601: 8, 0602: 7, 0603: 18) in the book's existing fenced style; Recap skipped as structural.

### S9. Weak business context

Done 2026-09-29 on branch `ch06-business-examples`.

- [x] Replace most `sin(x)` / `x**2` / A–D examples with business data: 51 cells across 0601–0603 now use one small retailer's data, defined inline per cell. Demos avoid reproducing assignment tasks (e.g. the `add_axes()` demo zooms on a promotion week, not Q4). The style gallery in 0603 stays abstract on purpose. Setup cells now hold imports only.
- [x] Reuse datasets already introduced in earlier chapters where possible: same style as ch04's inline tables (regions, quarters, months), and the same retailer as the ch06 lab and homework.

Only the sales/visits exercise in `0603` is currently a business case.

### S10. Missing closing sections

Done 2026-09-29 on branch `ch06-closing-sections`.

- [x] Add Summary and Further Reading (and References if sources are cited) to `0601` and `0602`. The one outside source, the Matplotlib paper, is cited in the 0601 introduction as {cite}`Hunter_2007` and added to `references.bib`, so it appears on the book's Bibliography page.
- [x] Expand the `0603` Recap into a Summary (keeps the workflow advice); add Further Reading.
- [x] Delete the trailing empty cell at the end of `0603`.

### S11. Preview answer key is a fixed pattern

- [x] Shuffle the correct-answer positions for `ch06-preview`: key is now C, A, D, B, D, A, B, C, D, A (done with S7). The preview test fails if the key returns to a fixed cycle.
- [x] Book-wide follow-up: the cycle was actually in 11 chapters (ch03, ch05, ch07–ch15), not just ch07 and ch08. All fixed 2026-09-29 by moving each correct choice to a new position; correct terms unchanged. `tests/grader/test_preview_keys.py` checks every chapter.

### S12. Slides are still the template

Done 2026-09-29 on branch `ch06-slides`.

- [x] Rewrite `_html_extra/chapters/06-matplotlib/overview.md` with real section content and key code patterns: 24 slides following 0601–0603, in ch03's slide style.
- [x] Regenerate `overview.html` with `npx @marp-team/marp-cli --no-stdin --html ...`; all slides rendered to images and checked for overflow.
- [x] Correct the "verified" status line in `MATERIALS.md`.
- Other chapters: ch05 and ch07–ch15 still have the six-slide placeholder deck.

## Could Defer

- [x] Suppress stray return-value output: 17 cells remained after S9 (0601: 4, 0602: 6, 0603: 7); each now ends with `plt.show()`, outputs refreshed. Done 2026-09-29.
- [x] Replace deprecated `ax.boxplot(..., vert=True)`: removed (vertical is the default); done with S9.
- [x] Fix typos in `0603` (done 2026-09-29):
  - [x] "aviaible" → "available styles"
  - [x] `pt.rcParams` → `plt.rcParams`
  - [x] unclosed backtick in "`axes[2]" (fixed when S9 rewrote that paragraph)
  - [x] "insert axes" → "inset axes" (fixed when S9 rewrote that demo, now in `0602`)
  - [x] curly quotes in the linestyle comment; the list also showed an en dash where `'-'` belongs
  - [x] `matplotlib.style.use` → `plt.style.use` for consistency; also "matplotlib offers" → "Matplotlib offers"
- [x] Seed random data: histogram, boxplot, and the sales exercise prompt use `np.random.default_rng(seed)`; done with S9.
- [x] Fix the inset exercise prompt (now in `0602`): it now says only that `x` is already defined.
- [ ] Confirm whether the AGENTS.md "Spring 2026: chapters 1–8 are frozen" note is still in effect for Fall 2026.

## Completion Checklist

- [ ] Notebook JSON validates for every changed file.
- [ ] `0601`–`0603` and assignment solution cells re-executed; outputs committed.
- [ ] Grader updated and tested for `ch06-lab` and `ch06-homework`.
- [ ] `MATERIALS.md` and `ORGANIZATION.md` updated.
- [ ] Slides regenerated.
- [ ] Book build passes with no new warnings for ch06.

## Follow-up Review of 0603 (2026-09-29)

Pass A (in-page fixes, no heading moves), done on branch `ch06-0603-pass-a`:

- [x] Boxplot text: whiskers stop at 1.5 × IQR; they reach the minimum and maximum only when there are no outliers.
- [x] Style sheets and rcParams: two charts compare the `default` and `ggplot` styles with `plt.style.context()`, and one uses `plt.rc_context()`, so nothing changes globally. Removed `%config`, the tiny chart, and the reset cell.
- [x] Every multi-series chart and exercise now labels its series and shows a legend; the color demo's legend sits outside the plot (`bbox_to_anchor`).
- [x] Plot range: the identical "tight axes" panel became "y-axis from zero", with a sentence on how truncated axes exaggerate differences.
- [x] Alpha: a new 300-order scatter shows why transparency helps when marks overlap.
- [x] Plot types: one sentence per chart on what it tells a manager; a new bins comparison (5, 15, 60); a note on sorting bars.
- [x] Polish: Title Case for the #### headings, the Oxford comma in "Colors, Line Width, and Style", `plt.show()` instead of `;`, `figsize=(4, 3)` spacing, no stray `dpi=100`, `plt.subplots()` in the legend demo, and no red/green pair in the style exercise (budget is gray), plus a sentence on color-blind readers.

Pass B (restructure; outline approved by the author), done 2026-09-29:

- [x] Replace the four opening reference tables: cut what 0602 already teaches, trim to one short Quick Reference, and move it to the end. The page now opens with Styling in Practice; "`rcParams`" is now "Style Sheets and `rcParams`".
- [x] Rebalance exercises: the three line-styling exercises became one ("Style a Revenue Chart"); new exercises for legends, a scatter plot, and a boxplot; the bar-and-histogram exercise moved under Histogram. Five exercises became six.
- [x] Split the 16-line style gallery into three labeled panels (line widths, line styles, markers); dropped `line.set_dashes()` and the marker `'1'`.
- Author's direction (2026-09-29): keep styling first, and use it when teaching plot types. Done: the scatter highlights the current price with a legend, the bar chart is sorted with only the leader colored and a takeaway title, the histogram has white bin edges and a median line, and the boxplot has filled boxes, a title, and a y-axis from zero. The section intro says the examples reuse the styling tools.

