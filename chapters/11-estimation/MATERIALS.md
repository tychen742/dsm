# Chapter 11 Materials

## Purpose

Chapter 11 introduces estimation, percentiles, bootstrap methods, and confidence intervals.

## Active Source Notebooks

- `1100-estimation.ipynb` - Landing: Chapter orientation, video, learning goals, flow, glossary, and slides.
- `1101-percentiles.ipynb` - Percentiles: Estimation prelude, numerical examples, percentile function, general definition, and quartiles.
- `1102-bootstrap.ipynb` - The Bootstrap: Employee compensation data, population and parameter, random sample and estimate, resampling, bootstrap medians, and bootstrap distributions.
- `1103-confidence-intervals.ipynb` - Confidence Intervals: Bootstrap confidence intervals for medians, means, proportions, and care in using the percentile method.

## Student Assignments

- `assignments/index.ipynb` - assignment landing page.
- `assignments/preview.ipynb` - server-graded preview quiz covering glossary and core terms.
- `assignments/lab.ipynb` - Chapter 11 server-graded lab (`ch11-lab`) with five pandas tasks: delivery percentiles with method='nearest', a sample median and one given bootstrap resample, a 95% bootstrap confidence interval from given bootstrap medians, 95% vs. 80% interval widths, and a bootstrap interval for a proportion used to judge a majority claim.
- `assignments/homework.ipynb` - Chapter 11 server-graded homework (`ch11-homework`) with five scenario-based true/false checks (resampling with replacement, intervals for a mean vs. individual values, the meaning of 95% confidence, lower confidence levels, the bootstrap and extremes) and five pandas coding questions: quartiles, one bootstrap resample, a 95% interval for a mean, sample size and interval width, and checking a supplier's claim against an interval.

## Figures And Media

- `../../figures/bootstrap_pic.png` in `1102-bootstrap.ipynb`.
- Chapter overview video embedded in `1100-estimation.ipynb`.

## Supporting Code And Data

- `scores_by_section.csv`, `san_francisco_2019.csv`, and `baby.csv` from `data/`.

## Slide Deck

- Source: `_html_extra/chapters/11-estimation/overview.md`.
- Rendered HTML: `_html_extra/chapters/11-estimation/overview.html`.
- Status: verified during the landing-page alignment pass.

## Archived Or Unlisted Material

- No archived or unlisted notebooks for this chapter.

## Maintenance Notes

- Active content section count: 3.
- No unlisted active notebooks remain in `chapters/11-estimation/`.
- Active content sections now include paired `thebe-interactive` exercise cells with adjacent `hide-input` solution cells.
