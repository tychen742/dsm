# Chapter 15 Organization

## Chapter Role

Chapter 15 completes the introductory machine-learning sequence by showing how clustering can find groups when labels are not provided.

## Learning Goals

Students should be able to:

1. Distinguish supervised and unsupervised learning.
2. Choose features and scaling decisions that match a clustering question.
3. Describe and run the basic k-means workflow.
4. Use elbow and silhouette checks to compare values of `k`.
5. Interpret clusters in a management context while identifying limitations.

## Sequence

1. `1500-clustering.ipynb` - Landing
   - Chapter orientation, video, learning goals, flow, glossary, and slides.
2. `1501-clustering-concepts.ipynb` - Clustering Concepts
   - Unsupervised learning, management use cases, similarity, feature choice, scale, common clustering methods, and practical interpretation cautions.
3. `1502-k-means-workflow.ipynb` - K-Means Workflow
   - K-means algorithm, synthetic data with known labels, visualization, fitting clusters with `n_init` and `random_state`, centers, labels, and comparison to known generated labels.
4. `1503-interpreting-clusters.ipynb` - Interpreting Clusters
   - Customer segmentation example (synthetic `customer_segments.csv`): raw vs. scaled features, choosing `k` with elbow and silhouette checks, cluster profiles in original units, segment names and possible actions, practical tips, and the arbitrariness of cluster labels.
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
- Organization status: expanded from the old single-section k-means workflow into the preferred three-part sequence: concepts, workflow, and interpretation.

## Exercise And Assignment Plan

- Preview: introduce the chapter vocabulary and core terms before class.
- Section notebooks: each active content section includes at least one paired `thebe-interactive` exercise and adjacent `hide-input` solution cell.
- Lab: server-graded scikit-learn tasks (`sklearn` runner profile): one k-means assignment step and one update step by hand, KMeans on raw vs. standardized features (sorted cluster sizes), choosing k with silhouette scores, and cluster profiles in original units sorted by spend. Expected outputs avoid cluster numbers, which can differ between scikit-learn versions.
- Homework: five scenario-based true/false checks (unlabeled data, scaling, smallest inertia, silhouette scores, arbitrary cluster numbers) and five coding questions: an assignment step on one feature, inertia by hand, KMeans cluster sizes, choosing k by silhouette score, and profiling a segment with groupby.

## Maintenance Notes

- Chapter overview slides are present and linked from the landing page.
- Media and data references are recorded in `MATERIALS.md`.
- Archived material, if any, is outside the active chapter folder.
