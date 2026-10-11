# Chapter 12 Materials

## Purpose

Chapter 12 introduces regression for prediction and relationship analysis.

## Active Source Notebooks

- `1200-regression.ipynb` - Landing: Chapter orientation, video, learning goals, flow, glossary, and slides.
- `1201-correlation.ipynb` - Correlation: Scatterplots, correlation coefficient, properties of correlation, association versus causation, outliers, ecological correlations, and interpretation.
- `1202-regression-line.ipynb` - Regression Line: Prediction prelude, standard units, regression line equation, regression effect, fitted values, slope units, and examples.
- `1203-least-squares.ipynb` - Least Squares: Prediction errors, root mean squared error, numerical optimization, and the least-squares line.
- `1204-visual-diag-residual.ipynb` - Visual Diagnostics: Regression diagnostics, nonlinearity, heteroscedasticity, and residual-based model checks.

## Student Assignments

- `assignments/index.ipynb` - assignment landing page.
- `assignments/preview.ipynb` - server-graded preview quiz covering glossary and core terms.
- `assignments/lab.ipynb` - Chapter 12 server-graded lab (`ch12-lab`) with five pandas tasks: r from standard units, the regression line's slope and intercept, a prediction and a residual, RMSE of the least squares line vs. a rule of thumb, and mean residuals by price range to detect a curved pattern.
- `assignments/homework.ipynb` - Chapter 12 server-graded homework (`ch12-homework`) with five scenario-based true/false checks (correlation vs. causation, r and units, the regression effect, least squares, fan-shaped residuals) and five pandas coding questions: a negative correlation, slope/intercept/prediction, predicting in standard units, RMSE, and residual spread (heteroscedasticity).

## Figures And Media

- `../../figures/regline.png` in `1202-regression-line.ipynb`; `../../figures/chocoNobel.png` in `1201-correlation.ipynb`; external dugong image in `1204-visual-diag-residual.ipynb`.
- Chapter overview video embedded in `1200-regression.ipynb`.

## Supporting Code And Data

- `hybrid.csv`, `sat2014.csv`, `family_heights.csv`, `galton.csv`, `baby.csv`, `little_women.csv`, and `dugongs.csv` from `data/`.

## Slide Deck

- Source: `_html_extra/chapters/12-regression/overview.md`.
- Rendered HTML: `_html_extra/chapters/12-regression/overview.html`.
- Status: verified during the landing-page alignment pass.

## Archived Or Unlisted Material

- No archived or unlisted notebooks for this chapter.

## Maintenance Notes

- Active content section count: 4.
- No unlisted active notebooks remain in `chapters/12-regression/`.
- Terminology uses "Least Squares" consistently for the method and section title.
- Active content sections now include paired `thebe-interactive` exercise cells with adjacent `hide-input` solution cells.
