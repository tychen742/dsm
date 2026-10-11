"""Grader test for the Chapter 09 lab (ch09-lab).

Runs every lab question through the server-side runner (pandas profile) with
the expected outputs defined in _html_extra/api/lib/quiz-app.php:

- the reference solution (lab-answer cell) must pass,
- a student submission (question cell with the solution filled in) must pass,
- the unedited question cell must fail,
- common wrong answers must fail with a hint.

Run with:  .venv/bin/python tests/grader/test_ch09_lab.py   (or pytest)
"""

import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

LAB = ROOT / "chapters" / "09-test-hypothesis" / "assignments" / "lab.ipynb"
LAB_ID = "ch09-lab"

SETUP = "import numpy as np\nimport pandas as pd\n"

WRONG_ANSWERS = {
    "q1": {
        "signed difference": SETUP + "print('Observed percent:', 24.5)\nprint('Test statistic:', round(20 - 24.5, 2))",
    },
    "q2": {
        "not halved": SETUP + "a = pd.Series([0.40, 0.35, 0.25])\nb = pd.Series([0.30, 0.40, 0.30])\nprint('TVD:', round((b - a).abs().sum(), 2))",
        "signed sum": SETUP + "a = pd.Series([0.40, 0.35, 0.25])\nb = pd.Series([0.30, 0.40, 0.30])\nprint('TVD:', round((b - a).sum() / 2, 2))",
    },
    "q3": {
        "strictly greater": SETUP + "s = pd.Series([0.04, 0.07, 0.01, 0.08, 0.09, 0.05, 0.07, 0.07, 0.05, 0.03, 0.00, 0.10, 0.06, 0.14, 0.08, 0.07, 0.04, 0.10, 0.04, 0.11])\nn = (s > 0.10).sum()\nprint('At least as large:', n)\nprint('P-value:', n / len(s))",
    },
    "q4": {
        "only the 5% rule": SETUP + "for name, p in zip(['Free shipping', 'Loyalty email', 'New layout'], [0.003, 0.04, 0.21]):\n    if p < 0.05:\n        print(name + ':', 'significant')\n    else:\n        print(name + ':', 'not significant')",
    },
    "q5": {
        "count only": SETUP + "print('False alarms:', 1)\nprint('False-alarm rate:', 1)",
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


def test_ch09_lab():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
