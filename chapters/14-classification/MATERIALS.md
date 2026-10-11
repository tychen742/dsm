# Chapter 14 Materials

## Purpose

Chapter 14 introduces classification, nearest neighbors, training and testing, implementation, and classifier accuracy.

## Active Source Notebooks

- `1400-classification.ipynb` - Landing: Chapter orientation, video, learning goals, flow, glossary, and slides.
- `1401-classification.ipynb` - Classification: Classification tasks and how supervised learning differs from regression and clustering.
- `1402-nearest-neighbors.ipynb` - Nearest Neighbors: Chronic kidney disease example, nearest-neighbor classifier, decision boundaries, and k-nearest neighbors.
- `1403-training-testing-accuracy.ipynb` - Training, Testing, and Accuracy: Train/test workflow, overly optimistic testing, test set generation, classifier accuracy, wine classification, and breast cancer diagnosis.
- `1404-rows-of-tables.ipynb` - Rows of Tables: Rows as observations, arrays from rows, distances with two attributes, row-wise apply, and nearest-neighbor lookup.
- `1405-implementing-the-classifier.ipynb` - Implementing the Classifier: Banknote authentication, multiple attributes, distance in multiple dimensions, classifier plan, and implementation steps.

## Student Assignments

- `assignments/index.ipynb` - assignment landing page.
- `assignments/preview.ipynb` - server-graded preview quiz covering glossary and core terms.
- `assignments/lab.ipynb` - Chapter 14 server-graded lab (`ch14-lab`) with five pandas tasks: the nearest neighbor and its distance, a 5-nearest-neighbor majority vote (k changes the prediction), standardizing a new case with training statistics, a classify() function applied to a test set, and test accuracy compared with an always-the-common-class baseline.
- `assignments/homework.ipynb` - Chapter 14 server-graded homework (`ch14-homework`) with five scenario-based true/false checks (testing on training data, scaling, scaling with the test set, k = 1, accuracy with rare classes) and five pandas coding questions: distance between two rows, a 3-nearest-neighbor prediction, scaling a test set with training statistics, accuracy vs. baseline and fraud caught, and choosing k by test accuracy.

## Figures And Media

- External Brittany Wenger image in the archived source content now merged into `1403-training-testing-accuracy.ipynb`.
- Chapter overview video embedded in `1400-classification.ipynb`.

## Supporting Code And Data

- `ckd.csv`, `banknote.csv`, `wine.csv`, and `breast-cancer.csv` from `data/`.

## Slide Deck

- Source: `_html_extra/chapters/14-classification/overview.md`.
- Rendered HTML: `_html_extra/chapters/14-classification/overview.html`.
- Status: verified during the landing-page alignment pass.

## Archived Or Unlisted Material

- Archived old standalone accuracy notebook under `authoring/archived-notebooks/14-classification/`.

## Maintenance Notes

- Active content section count: 5, consolidated from the old six-section shape by merging classifier accuracy into `1403-training-testing-accuracy.ipynb`.
- No unlisted active notebooks remain in `chapters/14-classification/`.
- Active content sections now include paired `thebe-interactive` exercise cells with adjacent `hide-input` solution cells.
