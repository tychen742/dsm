"""Grader test for the Chapter 08 lab (ch08-lab).

Runs every lab question through the server-side runner (pandas profile) with
the expected outputs defined in _html_extra/api/lib/quiz-app.php:

- the reference solution (lab-answer cell) must pass,
- a student submission (question cell with the solution filled in) must pass,
- the unedited question cell must fail,
- common wrong answers must fail with a hint.

Run with:  .venv/bin/python tests/grader/test_ch08_lab.py   (or pytest)
"""

import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

LAB = ROOT / "chapters" / "08-prob-stats" / "assignments" / "lab.ipynb"
LAB_ID = "ch08-lab"

SETUP = "import numpy as np\nimport pandas as pd\n"

WRONG_ANSWERS = {
    "q1": {
        "no rounding": SETUP + "tickets = pd.DataFrame({'outcome': ['same day', 'next day', '2+ days'], 'probability': [0.55, 0.30, 0.15]})\nprint('Total probability:', round(tickets['probability'].sum(), 2))\nprint('P(not same day):', 1 - 0.55)",
        "same day instead of complement": SETUP + "print('Total probability:', 1.0)\nprint('P(not same day):', 0.55)",
    },
    "q2": {
        "average price instead of expected value": SETUP + "plans = pd.DataFrame({'price': [10, 25, 60], 'probability': [0.5, 0.3, 0.2]})\nper = round(plans['price'].mean(), 2)\nprint('Expected revenue per subscriber:', per)\nprint('Expected revenue from', 2000, 'subscribers:', per * 2000)",
    },
    "q3": {
        "reports mean": SETUP + "d = pd.Series([3, 4, 4, 3, 5, 4, 22, 3, 6, 11])\nprint('Mean:', d.mean())\nprint('Median:', d.median())\nprint('Typical value:', 'mean')",
    },
    "q4": {
        "range instead of IQR": SETUP + "s = pd.Series([1000, 1200, 1100, 1500, 1300, 1400, 1600, 1300, 1500, 1100])\nq25 = np.percentile(s, 25)\nq75 = np.percentile(s, 75)\nprint('25th percentile:', q25)\nprint('75th percentile:', q75)\nprint('IQR:', s.max() - s.min())\nprint('Standard deviation:', round(np.std(s), 1))",
        "sample SD (ddof=1)": SETUP + "s = pd.Series([1000, 1200, 1100, 1500, 1300, 1400, 1600, 1300, 1500, 1100])\nq25 = np.percentile(s, 25)\nq75 = np.percentile(s, 75)\nprint('25th percentile:', q25)\nprint('75th percentile:', q75)\nprint('IQR:', q75 - q25)\nprint('Standard deviation:', round(s.std(), 1))",
    },
    "q5": {
        "SE quartered": SETUP + "print('SE with n=100:', 0.04)\nprint('SE with n=400:', 0.01)",
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


def test_ch08_lab():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
