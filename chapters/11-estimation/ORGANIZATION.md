# Chapter 11 Organization

## Chapter Role

Chapter 11 shifts from testing claims to estimating unknown quantities and communicating uncertainty.

## Learning Goals

Students should be able to:

1. Use percentiles to describe distributions and benchmarks.
2. Explain estimation as using sample data to approximate an unknown population value.
3. Generate bootstrap samples.
4. Build and interpret bootstrap confidence intervals.
5. Communicate interval estimates for management decisions.

## Sequence

1. `1100-estimation.ipynb` - Landing
   - Chapter orientation, video, learning goals, flow, glossary, and slides.
2. `1101-percentiles.ipynb` - Percentiles
   - Estimation prelude, numerical examples, percentile function, general definition, and quartiles.
3. `1102-bootstrap.ipynb` - The Bootstrap
   - Employee compensation data, population and parameter, random sample and estimate, resampling, bootstrap medians, and bootstrap distributions.
4. `1103-confidence-intervals.ipynb` - Confidence Intervals
   - Bootstrap confidence intervals for medians, means, proportions, and care in using the percentile method.
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
- Lab: server-graded pandas tasks (`pandas` runner profile): delivery percentiles with method='nearest', a sample median and one given bootstrap resample, a 95% bootstrap confidence interval from given bootstrap medians, 95% vs. 80% interval widths, and a bootstrap interval for a proportion used to judge a majority claim.
- Homework: five scenario-based true/false checks (resampling with replacement, intervals for a mean vs. individual values, the meaning of 95% confidence, lower confidence levels, the bootstrap and extremes) and five pandas coding questions: quartiles, one bootstrap resample, a 95% interval for a mean, sample size and interval width, and checking a supplier's claim against an interval.

## Maintenance Notes

- Chapter overview slides are present and linked from the landing page.
- Media and data references are recorded in `MATERIALS.md`.
- Archived material, if any, is outside the active chapter folder.
