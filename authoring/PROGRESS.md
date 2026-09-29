# Progress Tracker

Status values: `Draft` · `In Progress` · `Needs Review` · `Complete`

## Project TODOs

- Keep runnable helper code outside `chapters/`. Reusable notebook helpers live in `shared/`, and shared data files live in `data/`.
- **After midterm (Fall 2026): protect answer keys and solutions.** The repo is public, so answer keys and solutions are readable on GitHub even though students cannot see them on thinkdsm.org:
  - `_html_extra/api/lib/quiz-app.php` holds every preview key, homework true/false key, and lab/homework `plot_checks` / `code_outputs`.
  - Lab and homework solution cells are in the notebook source, and locked answers are hidden only by page JavaScript/CSS, so the code is in the page HTML.
  - After midterm: store all answer keys in DSM's current database (the PHP API's production database), not in the repo. Add an answer-key table keyed by assignment ID (`chNN-preview`, `chNN-lab`, `chNN-homework`) holding preview answers, homework true/false answers, and lab/homework `plot_checks` / `code_outputs`. `quiz-app.php` keeps only non-secret metadata (chapter, slug, max score, Canvas column, runner profile) and reads keys from the DB; grading fails with a clear "answer key not configured" error if a key is missing. Manage keys in the admin area with an audit record of each change; seed the table once from the current `quiz-app.php` values, then delete the keys from the code.
  - Keep the grader tests working: read keys from the DB (or an exported copy kept outside the repo), not from the repo.
  - Later: move DSM onto the ThinkPress platform (`~/workspace/press`, Django + PostgreSQL, `learn.thinkpress.org`), which is built for several books and owns assignment records, submissions, and grades. ThinkPress starts with other books first because DSM and py are in production. When DSM moves: add a ThinkDSM `catalog.Book` row and DSM assignments, add a private grading-spec field to press (it has no answer-key field yet) that the learner API never returns, keep code grading as a separate DSM service (press does not run code; `python_lab_runner.py` becomes that service), and carry over accounts, login events, attempts and best scores, Canvas sync, and the admin reports and exports. Shape the answer-key table above so it maps cleanly onto press later.
  - Rotate the preview keys after the move, since git history keeps the old ones.
  - Longer term: make the repo private once cells can run without Live Code (mybinder.org requires a public repo).
  - Serving locked answer cells only after unlock is a separate change.
- **Harden the grader's `pandas` runner profile.** Code graded under `runner_profile => 'pandas'` (ch04 lab and some homework) can read files readable by the web server user; `pd.read_csv("/etc/hosts")` succeeds, and `to_csv`, `np.load`, and `pd.read_pickle` are reachable. The `matplotlib` profile already blocks these by attribute name (`MATPLOTLIB_BLOCKED_ATTRIBUTES` in `_html_extra/api/lib/python_lab_runner.py`); apply the same blocklist to `pandas`, run the runner with `-I`, and check every pandas-profile reference solution still passes. An earlier attempt (2026-09-28) was discarded unfinished.

## Part I — Fundamentals

| Chapter | Title | Sections | Assignments | Status | Notes |
|---------|-------|----------|-------------|--------|-------|
| 01 | Intro to Data Science | 0101, 0102 | No | In Progress | |
| 02 | Python Basics | 0201–0208 | No | In Progress | |

## Part II — Working with Data

| Chapter | Title | Sections | Assignments | Status | Notes |
|---------|-------|----------|-------------|--------|-------|
| 03 | NumPy | 0301–0303 | No | In Progress | |
| 04 | Pandas | 0401–0405 | No | In Progress | |

## Part III — Data Visualization

| Chapter | Title | Sections | Assignments | Status | Notes |
|---------|-------|----------|-------------|--------|-------|
| 05 | Visualization Overview | 0501 | No | In Progress | |
| 06 | Matplotlib | 0601 | No | In Progress | |
| 07 | Seaborn | 0701 | No | In Progress | |

## Part IV — Inferential Statistics

| Chapter | Title | Sections | Assignments | Status | Notes |
|---------|-------|----------|-------------|--------|-------|
| 08 | Probability & Stats | 0801, 0802 | No | In Progress | |
| 09 | Hypothesis Testing | 0901–0903 | No | In Progress | |
| 10 | Two Samples | 1001–1003 | No | In Progress | |
| 11 | Estimation | 1101–1103 | No | In Progress | |
| 12 | Regression | 1201–1204 | No | In Progress | |

## Part V — Machine Learning

| Chapter | Title | Sections | Assignments | Status | Notes |
|---------|-------|----------|-------------|--------|-------|
| 13 | Multiple Regression | 1301, 1302 | No | In Progress | |
| 14 | Classification | 1402–1406 | No | In Progress | |
| 15 | Clustering | 1501 | No | In Progress | |

## Appendices

| Item | Title | Status | Notes |
|------|-------|--------|-------|
| — | Tooling | In Progress | |
| — | Cheatsheets | In Progress | |
| — | Jupyter Setup | In Progress | |
| — | Bibliography | In Progress | |
