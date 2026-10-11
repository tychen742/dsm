"""Grader test for the Chapter 10 lab (ch10-lab).

Runs every lab question through the server-side runner (pandas profile) with
the expected outputs defined in _html_extra/api/lib/quiz-app.php:

- the reference solution (lab-answer cell) must pass,
- a student submission (question cell with the solution filled in) must pass,
- the unedited question cell must fail,
- common wrong answers must fail with a hint.

Run with:  .venv/bin/python tests/grader/test_ch10_lab.py   (or pytest)
"""

import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

LAB = ROOT / "chapters" / "10-two-samples" / "assignments" / "lab.ipynb"
LAB_ID = "ch10-lab"

SETUP = "import numpy as np\nimport pandas as pd\n"

WRONG_ANSWERS = {
    "q1": {
        "A minus B": SETUP + "ab = pd.DataFrame({'version': ['A', 'B'] * 6, 'order_value': [42, 46, 38, 50, 45, 49, 40, 45, 44, 52, 41, 47]})\nm = ab.groupby('version')['order_value'].mean().round(2)\nprint('Mean A:', m['A'])\nprint('Mean B:', m['B'])\nprint('Observed difference:', round(m['A'] - m['B'], 2))",
    },
    "q2": {
        "count instead of rate": SETUP + "v = pd.DataFrame({'version': ['A'] * 10 + ['B'] * 10, 'converted': [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]})\nr = v.groupby('version')['converted'].sum()\nprint('Rate A:', r['A'])\nprint('Rate B:', r['B'])\nprint('Difference:', r['B'] - r['A'])",
    },
    "q3": {
        "real labels instead of shuffled": SETUP + "ab = pd.DataFrame({'version': ['A', 'B'] * 6, 'order_value': [42, 46, 38, 50, 45, 49, 40, 45, 44, 52, 41, 47]})\nm = ab.groupby('version')['order_value'].mean()\nprint('Shuffled difference:', round(m['B'] - m['A'], 2))",
    },
    "q4": {
        "two-sided p-value": SETUP + "s = pd.Series([1.83, -0.5, 1.17, -0.17, -2.83, -0.83, 2.17, -2.17, -1.17, 2.5, 2.17, 4.83, -1.83, -0.17, -5.17, 2.83, -1.17, -4.83, 4.5, 0.5])\np = (s.abs() >= 4.5).mean()\nprint('P-value:', p)\nprint('Decision:', 'do not reject the null')",
    },
    "q5": {
        "p-value only": SETUP + "for name, p in zip(['Coupon email', 'Loyalty members', 'New layout'], [0.01, 0.002, 0.34]):\n    if p < 0.05:\n        print(name + ':', 'evidence of a causal effect')\n    else:\n        print(name + ':', 'no evidence of a difference')",
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


def test_ch10_lab():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
