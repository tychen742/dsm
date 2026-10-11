# Chapter 07 Organization

## Chapter Role

Chapter 07 extends visualization from manual chart construction to concise statistical graphics that help students compare groups and relationships.

## Learning Objectives

Students should be able to:

1. Create common Seaborn plots from pandas DataFrames.
2. Use plot aesthetics to compare business groups.
3. Interpret distributions and relationships shown in statistical graphics.
4. Choose between pandas, Matplotlib, and Seaborn for common visualization tasks.

## Sequence

1. `0700-seaborn.ipynb` - Landing
   - Chapter orientation, video, learning goals, flow, glossary, and slides.
2. `0701-seaborn.ipynb` - Seaborn Foundations
   - Seaborn overview, library comparison, tidy/wide/nested data, semantic mappings, and figure-level versus axes-level APIs.
3. `0702-plot-families.ipynb` - Seaborn Plot Families
   - Distribution, relational, and categorical plot families with group comparisons from DataFrames.
4. `0703-faceting-style.ipynb` - Faceting, Multivariate Views, and Style
   - Figure-level wrappers, `FacetGrid`, pair plots, joint plots, heatmaps, themes, overlays, and KDE styling.
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
- Lab: server-graded Seaborn plotting tasks (`seaborn` runner profile with plot checks): histogram, scatter plot with `hue`, wide-to-tidy `melt()` with a grouped bar plot, box plot with a median comparison, and a faceted `relplot()`.
- Homework: five scenario-based true/false checks (tidy data, hue, figure- vs axes-level functions, box plots, themes) and five Seaborn plotting questions graded by plot checks: count plot, KDE by group, line plot by group, correlation heatmap, and a faceted `displot()`.

## Maintenance Notes

- Slides: the landing page links the legacy one-per-chapter overview deck (`overview.html`). Per-section lecture decks (`XXNN-slides.md`/`.html`, one per content section) will replace it; switch the landing page to a Lecture Slides list once all of this chapter's decks exist.
- Media and data references are recorded in `MATERIALS.md`.
- Archived material, if any, is outside the active chapter folder.
