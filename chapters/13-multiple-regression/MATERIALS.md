# Chapter 13 Materials

## Purpose

Chapter 13 extends regression to multiple predictors and introduces machine-learning framing where it supports prediction.

## Active Source Notebooks

- `1300-multiple-regression.ipynb` - Landing: Chapter orientation, video, learning goals, flow, glossary, and slides.
- `1301-linear-regression.ipynb` - Linear Regression: Machine-learning framing, validation and evaluation, data types, multiple regression orientation, simple linear model review, exploratory data analysis, train/test split, model training, evaluation, and prediction.
- `1302-multiple-regression.ipynb` - Multiple Regression: Home prices, multiple linear regression, train/test split, least squares, coefficient interpretation, and nearest neighbors for regression.

## Student Assignments

- `assignments/index.ipynb` - assignment landing page.
- `assignments/preview.ipynb` - server-graded preview quiz covering glossary and core terms.
- `assignments/lab.ipynb` - Chapter 13 server-graded lab (`ch13-lab`) with five scikit-learn tasks (`sklearn` runner profile): fit a LinearRegression and read its intercept and coefficients, the effect of one more room holding other features fixed, the most correlated predictor pair (multicollinearity), test RMSE of a simple vs. multiple model after train_test_split, and test-set R-squared with r2_score.
- `assignments/homework.ipynb` - Chapter 13 server-graded homework (`ch13-homework`) with five scenario-based true/false checks (reading a coefficient, correlated predictors, training error, more predictors and overfitting, R-squared) and five coding questions: pricing listings with a fitted model, test residuals and RMSE, nearest-neighbor regression, checking two predictors for multicollinearity, and choosing a model by test RMSE.

## Figures And Media

- `../../figures/ml-types-of-learning.png`, `../../figures/ml-how-much-data.png`, and `../../figures/ml-data-types-in-ds.png` in `1301-linear-regression.ipynb`.
- Chapter overview video embedded in `1300-multiple-regression.ipynb`.

## Supporting Code And Data

- `USA_Housing.csv` and `house.csv` from `data/`.

## Slide Deck

- Source: `_html_extra/chapters/13-multiple-regression/overview.md`.
- Rendered HTML: `_html_extra/chapters/13-multiple-regression/overview.html`.
- Status: verified during the landing-page alignment pass.

## Archived Or Unlisted Material

- The old `1300-machine-learning.ipynb` notebook was moved to `authoring/archived-notebooks/13-multiple-regression/` in the prior cleanup. Its substantive planning content has now been merged into `1301-linear-regression.ipynb` as a cleaned machine-learning prelude.

## Maintenance Notes

- Active content section count: 2.
- No unlisted active notebooks remain in `chapters/13-multiple-regression/`.
- Active content sections now include paired `thebe-interactive` exercise cells with adjacent `hide-input` solution cells.
