# AGENTS.md — thinkdsm.org (Data Science & Management)

## Base

Skill: `book-authoring` (from ai_shared)
Style: `guidelines/STYLE_GUIDE.md` in ai_shared

## Project Context

- College-level introductory textbook for data science and management students
- Audience: students with no assumed programming or data science background
- Application context: business and management; CS concepts are secondary
- Published at thinkdsm.org as a Jupyter Book

## Read First

1. `README.md` for repository structure
2. `authoring/BOOK_PLAN.md` for audience, scope, and chapter sequence
3. `_toc.yml` for the current notebook order
4. The target chapter's `MATERIALS.md` and `ORGANIZATION.md` before editing that chapter

## Shared Book Rules

Follow `book-authoring` for shared Jupyter Book conventions: landing page format, content notebook structure, glossary/index rules, assignment order, standard assignment descriptions, preview/lab/homework formats, submit panel behavior, student portal links, and chapter overview slides.

## Working Rules

### Content

- Business and management cases are the primary context for examples.
- Prefer simple datasets (fruits, names, nums) when the topic does not require real data.
- Reuse the same datasets across chapters for consistency.
- Always show diffs when proposing changes to existing content.

### Landing Pages

- Landing pages (first notebook in each chapter) are named `NNNN-TOPIC.ipynb` without "intro" suffix
  - Example: `0100-data-science.ipynb`, `0200-python.ipynb`, `0300-numpy.ipynb`
  - Landing pages introduce chapter scope and learning outcomes only
  - Landing pages do not contain exercises

### Sidebar Navigation

- Menu expand/collapse arrows must sit on the same visual baseline as the corresponding menu entry text. Do not leave arrows on a separate lower line or vertically offset from the entry they control.

### Deployment

- This repo follows the default book-authoring deployment model: "deploy" means commit and push the current changes to GitHub.
- Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds the Jupyter Book and deploys the built HTML/API files to the production VM.
- Exception: a local `./deploy` wrapper exists for direct VM deployment, but do not run it unless explicitly requested.

### Assignment UI

- Homework question blocks should use the same simple bordered-card treatment as preview questions. Avoid busy, nested, or competing borders around the question content.
- Section `Interactive Exercise` labels should render in the same red used by lab interactive-exercise labels.

### Assignment Naming

- Assignment IDs, API IDs, Canvas gradebook column names, Canvas CSV score headers, and Canvas CSV filenames use the same hyphenated `chNN-type` convention: `ch01-preview`, `ch01-lab`, `ch01-homework`.
- Do not use assignment-first or underscore forms such as `preview_ch01`, `lab_ch01`, `homework_ch01`, `preview01`, `lab01`, or `homework01` for new assignment records or Canvas exports.
- Score reports and Canvas-ready CSV exports filtered to one assignment in best-score mode must include every active student except explicitly excluded admin/test accounts. Students without a submission show/export score `0`, attempts `0`, and blank `Last Submitted`.

### Chapter Planning

- Every numbered chapter directory must contain `MATERIALS.md` and `ORGANIZATION.md`.
- Review both planning files before editing chapter content or chapter assignments. If either file is missing, create or restore it as part of the chapter edit.

### Exercises

- Create one exercise per `###` section that has substantial content.
- Short or non-essential `###` sections do not require an exercise.
- Place each exercise at the end of its `###` section.
- Two code cells per exercise: question cell (`thebe-interactive`), solution cell (`hide-input`).
- Thebe must not convert hidden solution cells. Keep `thebe_config.selector` excluding `.tag_hide-input` so solution toggles remain visible after Live Code is activated.
- Content-section exercise answers are not blocked. Assignment `thebe-interactive` questions and answer cells may be blocked, locked, or released by the admin/date-gate logic.

### DSM Assignment Overrides

- Auto-graded assignment IDs must use `chNN-preview`, `chNN-lab`, and `chNN-homework`, where `NN` is the two-digit chapter number.
- Starting with Chapter 02 labs, answer cells should be tagged `hide-input` and `lab-answer`; include answers in the notebook source, but reveal the "Show code cell source" toggle only after the due date by setting a page-level `data-lab-answers-release-at` timestamp.
- Auto-graded assignment feedback must not reveal correct answers before the due date. Before the due date, students may see their submission status, score, and retry guidance. After the due date, student review may show submitted answers and correct answers together.
- Authentication events are research data for later research projects. Keep historical login timestamps for each user in a login-event table; do not rely only on an overwritten `last_login_at` field.

## Semester Constraints

Update each semester.

- Fall 2026: all chapters are in scope. Do not restructure existing chapter headings without discussion.
- During breaks, major restructuring will happen.
- Why: agents have at times made aggressive changes without consulting the author. During the semester, fix issues within a chapter, and consult the author before structural or large changes (moving or renaming sections, rewriting many examples, book-wide edits): propose the plan, wait for approval, then make the change.
