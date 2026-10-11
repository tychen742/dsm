"""Grader test for the Chapter 12 lab (ch12-lab).

Runs every lab question through the server-side runner (pandas profile) with
the expected outputs defined in _html_extra/api/lib/quiz-app.php:

- the reference solution (lab-answer cell) must pass,
- a student submission (question cell with the solution filled in) must pass,
- the unedited question cell must fail,
- common wrong answers must fail with a hint.

Run with:  .venv/bin/python tests/grader/test_ch12_lab.py   (or pytest)
"""

import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

LAB = ROOT / "chapters" / "12-regression" / "assignments" / "lab.ipynb"
LAB_ID = "ch12-lab"

SETUP = "import numpy as np\nimport pandas as pd\n"

WRONG_ANSWERS = {
    "q1": {
        "sample SD (ddof=1)": SETUP + "ads = pd.DataFrame({'ad_spend': [2, 3, 4, 5, 6, 7, 8, 9], 'sales': [60, 72, 70, 85, 88, 98, 95, 110]})\nx = ads['ad_spend']\ny = ads['sales']\nzx = (x - x.mean()) / x.std()\nzy = (y - y.mean()) / y.std()\nprint('r:', round(np.mean(zx * zy), 3))",
    },
    "q2": {
        "SDs inverted": SETUP + "ads = pd.DataFrame({'ad_spend': [2, 3, 4, 5, 6, 7, 8, 9], 'sales': [60, 72, 70, 85, 88, 98, 95, 110]})\nx = ads['ad_spend']\ny = ads['sales']\nr = np.mean(((x - np.mean(x)) / np.std(x)) * ((y - np.mean(y)) / np.std(y)))\na = r * np.std(x) / np.std(y)\nprint('Slope:', round(a, 2))\nprint('Intercept:', round(np.mean(y) - a * np.mean(x), 2))",
    },
    "q3": {
        "residual sign flipped": SETUP + "print('Predicted sales at 6.5:', 91.32)\nprint('Residual at 5:', -3.54)",
    },
    "q4": {
        "MSE instead of RMSE": SETUP + "print('Regression RMSE:', round(3.67 ** 2, 2))\nprint('Rule of thumb RMSE:', round(4.27 ** 2, 2))",
    },
    "q5": {
        "pattern without residuals": SETUP + "print('Low prices:', 71.7)\nprint('Middle prices:', 38.0)\nprint('High prices:', 30.3)\nprint('Pattern:', 'no clear pattern')",
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


def test_ch12_lab():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
