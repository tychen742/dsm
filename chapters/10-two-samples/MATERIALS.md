# Chapter 10 Materials

## Purpose

Chapter 10 extends inference to comparisons between two groups, including A/B testing, a case study, and causality.

## Active Source Notebooks

- `1000-two-samples.ipynb` - Landing: Chapter orientation, video, learning goals, flow, glossary, and slides.
- `1001-ab-testing.ipynb` - A/B Testing: Random Sampling Prelude; smokers and nonsmokers, hypotheses, test statistic, null prediction, permutation tests, p-values, and conclusions.
- `1002-deflategate.ipynb` - Deflategate: Applied case study using hypotheses, test statistics, null prediction, permutation testing, and evidence interpretation.
- `1003-causality.ipynb` - Causality: Randomized controlled trial, potential outcomes, causal hypotheses, permutation testing, and meta-analysis.

## Student Assignments

- `assignments/index.ipynb` - assignment landing page.
- `assignments/preview.ipynb` - server-graded preview quiz covering glossary and core terms.
- `assignments/lab.ipynb` - Chapter 10 server-graded lab (`ch10-lab`) with five pandas tasks: group means and the observed difference with groupby, conversion rates, the difference under one given shuffle of the labels, a one-sided permutation-test p-value and decision from given simulated differences, and classifying studies as causal evidence, association only, or no evidence.
- `assignments/homework.ipynb` - Chapter 10 server-graded homework (`ch10-homework`) with five scenario-based true/false checks (opt-in comparisons, what shuffling simulates, one-sided statistics, randomized trials, small randomized studies) and five pandas coding questions: basket size by segment, churn by plan, a two-sided permutation p-value and decision, relative lift, and a randomized controlled trial.

## Figures And Media

- `../../figures/causality1.png` and `../../figures/causality2.png` in `1003-causality.ipynb`.
- Chapter overview video embedded in `1000-two-samples.ipynb`.

## Supporting Code And Data

- `actors.csv`, `baby.csv`, `deflategate.csv`, `bta.csv`, and `observed_outcomes.csv` from `data/`.

## Slide Deck

- Source: `_html_extra/chapters/10-two-samples/overview.md`.
- Rendered HTML: `_html_extra/chapters/10-two-samples/overview.html`.
- Status: legacy one-per-chapter overview deck, still linked from the landing page until per-section lecture decks (`XXNN-slides.md`/`.html`) replace it.

## Archived Or Unlisted Material

- No archived or unlisted notebooks for this chapter.

## Maintenance Notes

- Active content section count: 3.
- No unlisted active notebooks remain in `chapters/10-two-samples/`.
- Active content sections now include paired `thebe-interactive` exercise cells with adjacent `hide-input` solution cells.
