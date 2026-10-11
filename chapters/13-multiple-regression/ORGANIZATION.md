# Chapter 13 Organization

## Chapter Role

Chapter 13 builds from simple regression toward predictive modeling with more than one input variable, using machine-learning framing where it clarifies training, testing, and evaluation.

## Learning Goals

Students should be able to:

1. Explain why multiple predictors may improve a prediction model.
2. Describe the role of training, validation, and testing data in predictive modeling.
3. Fit a multiple regression model.
4. Interpret coefficients while holding other variables constant.
5. Evaluate prediction quality in a management context.

## Sequence

1. `1300-multiple-regression.ipynb` - Landing
   - Chapter orientation, video, learning goals, flow, glossary, and slides.
2. `1301-linear-regression.ipynb` - Linear Regression
   - Machine-learning framing, validation and evaluation, data types, multiple regression orientation, simple linear model review, exploratory data analysis, train/test split, model training, evaluation, and prediction.
3. `1302-multiple-regression.ipynb` - Multiple Regression
   - Home prices, multiple linear regression, train/test split, least squares, coefficient interpretation, and nearest neighbors for regression.
4. `assignments/index.ipynb` - Assignments
   - Preview
   - Lab
   - Homework

## Topic Coverage Review

- Coverage status: aligned with the current notebooks and `_toc.yml`.
- Landing page is limited to orientation, video, learning goals, chapter flow, glossary, and slide link.
- Detailed teaching content lives in the content section notebooks.
- The old machine-learning landing material has been merged into `1301-linear-regression.ipynb` as an active prelude rather than remaining only as archived planning content.

## Section Organization Review

- Active content section count: 2.
- Organization status: passes the preferred 2-5 section range.

## Exercise And Assignment Plan

- Preview: introduce the chapter vocabulary and core terms before class.
- Section notebooks: each active content section includes at least one paired `thebe-interactive` exercise and adjacent `hide-input` solution cell.
- Lab: server-graded scikit-learn tasks (`sklearn` runner profile): fit a LinearRegression and read its intercept and coefficients, the effect of one more room holding other features fixed, the most correlated predictor pair (multicollinearity), test RMSE of a simple vs. multiple model after train_test_split, and test-set R-squared with r2_score.
- Homework: five scenario-based true/false checks (reading a coefficient, correlated predictors, training error, more predictors and overfitting, R-squared) and five coding questions: pricing listings with a fitted model, test residuals and RMSE, nearest-neighbor regression, checking two predictors for multicollinearity, and choosing a model by test RMSE.

## Maintenance Notes

- Chapter overview slides are present and linked from the landing page.
- Media and data references are recorded in `MATERIALS.md`.
- The archived `1300-machine-learning.ipynb` source is retained under `authoring/archived-notebooks/13-multiple-regression/` for provenance after its usable content was merged.
