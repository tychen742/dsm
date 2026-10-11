# Chapter 10 Organization

## Chapter Role

Chapter 10 teaches students how to compare two groups and reason about experimental evidence in business and public examples.

## Learning Objectives

Students should be able to:

1. Frame a two-sample comparison as a testable management question.
2. Interpret A/B test results using observed differences and simulated comparisons.
3. Use a case study to connect data, assumptions, and evidence.
4. Distinguish association, experimental comparison, and causal inference.

## Sequence

1. `1000-two-samples.ipynb` - Landing
   - Chapter orientation, video, learning goals, flow, glossary, and slides.
2. `1001-ab-testing.ipynb` - A/B Testing
   - Random Sampling Prelude; smokers and nonsmokers, hypotheses, test statistic, null prediction, permutation tests, p-values, and conclusions.
3. `1002-deflategate.ipynb` - Deflategate
   - Applied case study using hypotheses, test statistics, null prediction, permutation testing, and evidence interpretation.
4. `1003-causality.ipynb` - Causality
   - Randomized controlled trial, potential outcomes, causal hypotheses, permutation testing, and meta-analysis.
5. `assignments/index.ipynb` - Assignments
   - Preview
   - Lab
   - Homework

## Topic Coverage Review

- Coverage status: aligned with the current notebooks and `_toc.yml`.
- Landing page is limited to orientation, video, learning goals, chapter flow, glossary, and slide link.
- Detailed teaching content lives in the content section notebooks.
- Planning reflects the moved landing content: the random sampling setup now belongs to `1001-ab-testing.ipynb` as the Random Sampling Prelude.

## Section Organization Review

- Active content section count: 3.
- Organization status: passes the preferred 2-5 section range.

## Exercise And Assignment Plan

- Preview: introduce the chapter vocabulary and core terms before class.
- Section notebooks: each active content section includes at least one paired `thebe-interactive` exercise and adjacent `hide-input` solution cell.
- Lab: server-graded pandas tasks (`pandas` runner profile): group means and the observed difference with groupby, conversion rates, the difference under one given shuffle of the labels, a one-sided permutation-test p-value and decision from given simulated differences, and classifying studies as causal evidence, association only, or no evidence.
- Homework: five scenario-based true/false checks (opt-in comparisons, what shuffling simulates, one-sided statistics, randomized trials, small randomized studies) and five pandas coding questions: basket size by segment, churn by plan, a two-sided permutation p-value and decision, relative lift, and a randomized controlled trial.

## Maintenance Notes

- Slides: the landing page links the legacy one-per-chapter overview deck (`overview.html`). Per-section lecture decks (`XXNN-slides.md`/`.html`, one per content section) will replace it; switch the landing page to a Lecture Slides list once all of this chapter's decks exist.
- Media and data references are recorded in `MATERIALS.md`.
- Archived material, if any, is outside the active chapter folder.
