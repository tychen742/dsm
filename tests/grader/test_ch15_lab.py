"""Grader test for the Chapter 15 lab (ch15-lab).

Runs every lab question through the server-side runner (sklearn profile) with
the expected outputs defined in _html_extra/api/lib/quiz-app.php:

- the reference solution (lab-answer cell) must pass,
- a student submission (question cell with the solution filled in) must pass,
- the unedited question cell must fail,
- common wrong answers must fail with a hint.

Run with:  .venv/bin/python tests/grader/test_ch15_lab.py   (or pytest)
"""

import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

LAB = ROOT / "chapters" / "15-clustering" / "assignments" / "lab.ipynb"
LAB_ID = "ch15-lab"

SETUP = "import numpy as np\nimport pandas as pd\n"

C = "customers = pd.DataFrame({'spend': [300, 650, 450, 800, 500, 900, 700, 1100, 2000, 2500, 2900, 2300, 2100, 2700, 3000, 2400], 'orders': [3, 2, 4, 3, 24, 22, 26, 25, 5, 4, 6, 5, 28, 26, 30, 27]})\nscaled = (customers - customers.mean()) / customers.std(ddof=0)\n"
K = "from sklearn.cluster import KMeans\nfrom sklearn.metrics import silhouette_score\n"
ST = "stores = pd.DataFrame({'traffic_su': [-1.2, -1.0, -1.3, -0.9, 0.1, 0.3, 0.0, 0.2, 1.3, 1.1, 1.4, 1.2], 'basket_su': [1.1, 0.9, 1.2, 1.0, -1.0, -1.2, -0.9, -1.1, 0.2, 0.0, 0.3, 0.1]})\n"

WRONG_ANSWERS = {
    "q1": {
        "farther center": SETUP + "print('Assignments:', [1, 1, 0, 0, 1, 0])\nprint('Cluster sizes:', [3, 3])",
    },
    "q2": {
        "sum instead of mean": SETUP + "p = pd.DataFrame({'a': [-1.0, -0.8, 1.1, 0.9, -1.2, 1.3], 'b': [-0.5, -0.9, 0.8, 1.2, -0.7, 0.6], 'cluster': [0, 0, 1, 1, 0, 1]})\nc = p.groupby('cluster').sum().round(2)\nprint('Center 0:', c.loc[0].tolist())\nprint('Center 1:', c.loc[1].tolist())",
    },
    "q3": {
        "scaled both times": SETUP + K + C + "l = KMeans(n_clusters=4, n_init=10, random_state=0).fit_predict(scaled)\nprint('Raw sizes:', sorted(pd.Series(l).value_counts().tolist()))\nprint('Scaled sizes:', sorted(pd.Series(l).value_counts().tolist()))",
    },
    "q4": {
        "silhouette on raw features": SETUP + K + C + "b, bs = None, -1\nfor k in [2, 3, 4, 5]:\n    l = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(customers)\n    s = round(silhouette_score(customers, l), 3)\n    print('k=' + str(k) + ':', s)\n    if s > bs:\n        b, bs = k, s\nprint('Best k:', b)",
    },
    "q5": {
        "profile in standard units": SETUP + K + C + "scaled['cluster'] = KMeans(n_clusters=4, n_init=10, random_state=0).fit_predict(scaled)\np = scaled.groupby('cluster')[['spend', 'orders']].mean().sort_values('spend')\nfor s, o in zip(p['spend'], p['orders']):\n    print('Spend ' + str(round(s, 2)) + ', orders ' + str(round(o, 2)))",
    },
}


def collect_results():
    definition = assignment_definition("dsm_lab_definition", LAB_ID)
    checks = {}
    outputs = definition["code_outputs"]
    questions, solutions = notebook_code_cells(LAB, "lab-answer")
    ids = [f"q{n}" for n in range(1, len(questions) + 1)]
    results = [
        ("definition", "question ids match notebook", sorted(outputs) == ids, ""),
        ("definition", "runner profile", definition.get("runner_profile") == "sklearn", ""),
        ("definition", "output ids are question ids", set(outputs) <= set(ids), ""),
    ]
    return results + check_questions(ids, questions, solutions, checks, WRONG_ANSWERS, "sklearn", outputs)


def test_ch15_lab():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
