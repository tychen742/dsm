"""Grader test for the Chapter 14 lab (ch14-lab).

Runs every lab question through the server-side runner (pandas profile) with
the expected outputs defined in _html_extra/api/lib/quiz-app.php:

- the reference solution (lab-answer cell) must pass,
- a student submission (question cell with the solution filled in) must pass,
- the unedited question cell must fail,
- common wrong answers must fail with a hint.

Run with:  .venv/bin/python tests/grader/test_ch14_lab.py   (or pytest)
"""

import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

LAB = ROOT / "chapters" / "14-classification" / "assignments" / "lab.ipynb"
LAB_ID = "ch14-lab"

SETUP = "import numpy as np\nimport pandas as pd\n"

L = "loans = pd.DataFrame({'income_su': [1.2, 0.8, -0.3, -1.1, 0.4, -0.9, 1.5, -0.2, 0.1, -1.4], 'debt_su': [-0.9, -0.4, 0.6, 1.3, -0.1, 0.9, -1.2, 1.0, 0.3, 0.2], 'outcome': ['repaid', 'repaid', 'default', 'default', 'repaid', 'default', 'repaid', 'default', 'repaid', 'default']})\n"

WRONG_ANSWERS = {
    "q1": {
        "farthest instead of nearest": SETUP + L + "a = np.array([0.0, 0.4])\nloans['d'] = np.sqrt(((loans[['income_su', 'debt_su']] - a) ** 2).sum(axis=1))\nn = loans.sort_values('d', ascending=False)\nprint('Nearest distance:', round(n['d'].iloc[0], 3))\nprint('1-NN prediction:', n['outcome'].iloc[0])",
    },
    "q2": {
        "first five rows, not nearest": SETUP + L + "v = loans.head(5)['outcome'].value_counts()\nprint('Default votes:', v['default'])\nprint('Repaid votes:', v['repaid'])\nprint('5-NN prediction:', v.idxmax())",
    },
    "q3": {
        "sample SD (ddof=1)": SETUP + "t = pd.DataFrame({'income': [42, 55, 61, 38, 70, 48], 'balance': [1200, 300, 800, 2500, 150, 1900]})\nn = pd.Series({'income': 50, 'balance': 1000})\ns = (n - t.mean()) / t.std()\nprint('Income in standard units:', round(s['income'], 2))\nprint('Balance in standard units:', round(s['balance'], 2))",
    },
    "q4": {
        "k = 1": SETUP + L + "t = pd.DataFrame({'income_su': [0.9, -0.8, 0.0, -0.5, 0.6], 'debt_su': [-0.6, 0.8, 0.5, 0.1, 0.4]})\np = []\nfor i, d in zip(t['income_su'], t['debt_su']):\n    dist = np.sqrt(((loans[['income_su', 'debt_su']] - np.array([i, d])) ** 2).sum(axis=1))\n    p.append(loans.assign(dist=dist).sort_values('dist')['outcome'].iloc[0])\nprint('Predictions:', p)",
    },
    "q5": {
        "count instead of proportion": SETUP + "print('Classifier accuracy:', 3)\nprint('Baseline accuracy:', 3)",
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
        ("definition", "runner profile", definition.get("runner_profile") == "pandas", ""),
        ("definition", "output ids are question ids", set(outputs) <= set(ids), ""),
    ]
    return results + check_questions(ids, questions, solutions, checks, WRONG_ANSWERS, "pandas", outputs)


def test_ch14_lab():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
