# Chapter 12 Organization

## Chapter Role

Chapter 12 teaches simple linear regression as a practical tool for prediction and relationship analysis before multiple regression.

## Learning Objectives

Students should be able to:

1. Interpret correlation as the direction and strength of a linear relationship.
2. Fit and interpret a simple regression line.
3. Explain least squares as a criterion for choosing a line.
4. Use residuals to evaluate prediction errors.
5. Diagnose common limitations of linear regression using visual checks.

## Sequence

1. `1200-regression.ipynb` - Landing
   - Chapter orientation, video, learning goals, flow, glossary, and slides.
2. `1201-correlation.ipynb` - Correlation
   - Scatterplots, correlation coefficient, properties of correlation, association versus causation, outliers, ecological correlations, and interpretation.
3. `1202-regression-line.ipynb` - Regression Line
   - Prediction prelude, standard units, regression line equation, regression effect, fitted values, slope units, and examples.
4. `1203-least-squares.ipynb` - Least Squares
   - Prediction errors, root mean squared error, numerical optimization, and the least-squares line.
5. `1204-visual-diag-residual.ipynb` - Visual Diagnostics
   - Regression diagnostics, nonlinearity, heteroscedasticity, and residual-based model checks.
6. `assignments/index.ipynb` - Assignments
   - Preview
   - Lab
   - Homework

## Topic Coverage Review

- Coverage status: aligned with the current notebooks and `_toc.yml`.
- Landing page is limited to orientation, video, learning goals, chapter flow, glossary, and slide link.
- Detailed teaching content lives in the content section notebooks.

## Section Organization Review

- Active content section count: 4.
- Organization status: passes the preferred 2-5 section range.

## Exercise And Assignment Plan

- Preview: introduce the chapter vocabulary and core terms before class.
- Section notebooks: each active content section includes at least one paired `thebe-interactive` exercise and adjacent `hide-input` solution cell.
- Lab: server-graded pandas tasks (`pandas` runner profile): r from standard units, the regression line's slope and intercept, a prediction and a residual, RMSE of the least squares line vs. a rule of thumb, and mean residuals by price range to detect a curved pattern.
- Homework: five scenario-based true/false checks (correlation vs. causation, r and units, the regression effect, least squares, fan-shaped residuals) and five pandas coding questions: a negative correlation, slope/intercept/prediction, predicting in standard units, RMSE, and residual spread (heteroscedasticity).

## Maintenance Notes

- Slides: the landing page links the legacy one-per-chapter overview deck (`overview.html`). Per-section lecture decks (`XXNN-slides.md`/`.html`, one per content section) will replace it; switch the landing page to a Lecture Slides list once all of this chapter's decks exist.
- Media and data references are recorded in `MATERIALS.md`.
- Archived material, if any, is outside the active chapter folder.
- Terminology uses "Least Squares" consistently for the section title and method.
