# Chapter 15 Materials

## Purpose

Chapter 15 introduces clustering as an unsupervised machine-learning technique, with emphasis on k-means.

## Active Source Notebooks

- `1500-clustering.ipynb` - Landing: Chapter orientation, video, learning goals, flow, glossary, and slides.
- `1501-clustering-concepts.ipynb` - Clustering Concepts: Unsupervised learning, management use cases, similarity, feature choice, scale, common clustering methods, and practical interpretation cautions.
- `1502-k-means-workflow.ipynb` - K-Means Workflow: K-means algorithm, synthetic `make_blobs` data with known labels, visualization, fitting clusters (`n_init`, `random_state`), centers, labels, and comparison to known generated labels.
- `1503-interpreting-clusters.ipynb` - Interpreting Clusters: customer segmentation example, raw vs. scaled features, choosing `k` with elbow and silhouette checks, cluster profiles in original units, segment names and actions, practical tips, and the arbitrariness of cluster labels.

## Student Assignments

- `assignments/index.ipynb` - assignment landing page.
- `assignments/preview.ipynb` - server-graded preview quiz covering glossary and core terms.
- `assignments/lab.ipynb` - Chapter 15 server-graded lab (`ch15-lab`) with five coding questions on center distances, cluster assignment, center updates, elbow comparison, and cluster summaries.
- `assignments/homework.ipynb` - Chapter 15 server-graded homework (`ch15-homework`) with five scenario-based true/false questions and five coding questions on cluster counts, nearest centers, scaled features, cluster averages, and silhouette choices.

## Figures And Media

- Chapter overview video embedded in `1500-clustering.ipynb`.

## Supporting Code And Data

- `1502`: generated synthetic data from `sklearn.datasets.make_blobs` (`random_state=101`).
- `1503`: `data/customer_segments.csv`, a synthetic data set of 240 online-store customers (`customer_id`, `annual_spend` in dollars, `orders_per_year`) generated for this book with `numpy.random.default_rng(15)` from four customer types: occasional (90; spend ~$400, ~3 orders), frequent small-basket (60; ~$900, ~24), big-ticket (50; ~$2,200, ~5), and loyal high-value (40; ~$2,600, ~28). Disclosed as synthetic in the notebook.
- K-means examples use `sklearn.cluster.KMeans`; cluster evaluation uses `sklearn.metrics.silhouette_score`.

## Slide Deck

- Source: `_html_extra/chapters/15-clustering/overview.md`.
- Rendered HTML: `_html_extra/chapters/15-clustering/overview.html`.
- Status: verified during the landing-page alignment pass.

## Archived Or Unlisted Material

- No archived or unlisted notebooks for this chapter.

## Maintenance Notes

- Active content section count: 3, expanded from the old single-section k-means workflow into concepts, workflow, and interpretation.
- No unlisted active notebooks remain in `chapters/15-clustering/`.
- Active content sections now include paired `thebe-interactive` exercise cells with adjacent `hide-input` solution cells.
