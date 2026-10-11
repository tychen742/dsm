# Chapter 14 Organization

## Chapter Role

Chapter 14 introduces supervised machine learning through classification and nearest-neighbor methods.

## Learning Objectives

Students should be able to:

1. Distinguish classification from regression.
2. Explain nearest-neighbor classification at a conceptual level.
3. Split data into training and testing sets.
4. Represent observations as rows with features and labels.
5. Implement and evaluate a simple classifier.

## Sequence

1. `1400-classification.ipynb` - Landing
   - Chapter orientation, video, learning goals, flow, glossary, and slides.
2. `1401-classification.ipynb` - Classification
   - Classification tasks and how supervised learning differs from regression and clustering.
3. `1402-nearest-neighbors.ipynb` - Nearest Neighbors
   - Chronic kidney disease example, nearest-neighbor classifier, decision boundaries, and k-nearest neighbors.
4. `1403-training-testing-accuracy.ipynb` - Training, Testing, and Accuracy
   - Train/test workflow, overly optimistic testing, test set generation, classifier accuracy, wine classification, and breast cancer diagnosis.
5. `1404-rows-of-tables.ipynb` - Rows of Tables
   - Rows as observations, arrays from rows, distances with two attributes, row-wise apply, and nearest-neighbor lookup.
6. `1405-implementing-the-classifier.ipynb` - Implementing the Classifier
   - Banknote authentication, multiple attributes, distance in multiple dimensions, classifier plan, and implementation steps.
7. `assignments/index.ipynb` - Assignments
   - Preview
   - Lab
   - Homework

## Topic Coverage Review

- Coverage status: aligned with the current notebooks and `_toc.yml`.
- Landing page is limited to orientation, video, learning goals, chapter flow, glossary, and slide link.
- Detailed teaching content lives in the content section notebooks.

## Section Organization Review

- Active content section count: 5.
- Organization status: consolidated to the allowed 4-5 section range for this larger chapter, with the old standalone accuracy section merged into training/testing.

## Exercise And Assignment Plan

- Preview: introduce the chapter vocabulary and core terms before class.
- Section notebooks: each active content section includes at least one paired `thebe-interactive` exercise and adjacent `hide-input` solution cell.
- Lab: server-graded pandas tasks (`pandas` runner profile): the nearest neighbor and its distance, a 5-nearest-neighbor majority vote (k changes the prediction), standardizing a new case with training statistics, a classify() function applied to a test set, and test accuracy compared with an always-the-common-class baseline.
- Homework: five scenario-based true/false checks (testing on training data, scaling, scaling with the test set, k = 1, accuracy with rare classes) and five pandas coding questions: distance between two rows, a 3-nearest-neighbor prediction, scaling a test set with training statistics, accuracy vs. baseline and fraud caught, and choosing k by test accuracy.

## Maintenance Notes

- Slides: the landing page links the legacy one-per-chapter overview deck (`overview.html`). Per-section lecture decks (`XXNN-slides.md`/`.html`, one per content section) will replace it; switch the landing page to a Lecture Slides list once all of this chapter's decks exist.
- Media and data references are recorded in `MATERIALS.md`.
- Archived material, if any, is outside the active chapter folder.
