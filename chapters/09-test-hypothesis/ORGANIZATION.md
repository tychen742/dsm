# Chapter 09 Organization

## Chapter Role

Chapter 09 moves from describing variability to testing whether observed outcomes are plausible under a proposed model.

## Learning Goals

Students should be able to:

1. State null and alternative hypotheses for a management question.
2. Choose an appropriate test statistic for a simple hypothesis test.
3. Simulate a null distribution.
4. Interpret a p-value as evidence against a model.
5. Connect statistical evidence to business decisions while acknowledging uncertainty.

## Sequence

1. `0900-hypothesis-testing.ipynb` - Landing
   - Chapter orientation, video, learning goals, flow, glossary, and slides.
2. `0901-assess-model-1.ipynb` - Assessing Model 1: Swain vs. Alabama
   - Model assessment, test statistics, simulated comparisons, prediction under a model, and statistical bias.
3. `0902-assess-model-2.ipynb` - Assessing Model 2: Alameda County Jury Panels
   - Distance between distributions, simulated model assessment, evidence against a model, and data quality.
4. `0903-decisions-uncertainty.ipynb` - Hypotheses and p-Value
   - Mendel case, hypotheses, test statistic, null distribution, p-values, cutoffs, and decisions under uncertainty.
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
- Section notebooks: each active content section includes at least one paired `thebe-interactive` exercise and adjacent `hide-input` solution cell.
- Lab: server-graded pandas tasks (`pandas` runner profile) using given simulation results: an absolute-distance test statistic, total variation distance, a p-value from simulated statistics, the conventional significance labels, and the false-alarm (Type I error) rate of A/A tests.
- Homework: five scenario-based true/false checks (stating the null, reading a p-value, choosing a statistic, not rejecting is not proof, many tests and false alarms) and five pandas coding questions: a defect-rate statistic, a channel-mix TVD, a p-value from simulations, decisions at two cutoffs, and the 95th-percentile cutoff for a statistic.

## Maintenance Notes

- Chapter overview slides are present and linked from the landing page.
- Media and data references are recorded in `MATERIALS.md`.
- Archived material, if any, is outside the active chapter folder.
