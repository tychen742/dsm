"""Grader test for the Chapter 11 lab (ch11-lab).

Runs every lab question through the server-side runner (pandas profile) with
the expected outputs defined in _html_extra/api/lib/quiz-app.php:

- the reference solution (lab-answer cell) must pass,
- a student submission (question cell with the solution filled in) must pass,
- the unedited question cell must fail,
- common wrong answers must fail with a hint.

Run with:  .venv/bin/python tests/grader/test_ch11_lab.py   (or pytest)
"""

import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

LAB = ROOT / "chapters" / "11-estimation" / "assignments" / "lab.ipynb"
LAB_ID = "ch11-lab"

SETUP = "import numpy as np\nimport pandas as pd\n"

WRONG_ANSWERS = {
    "q1": {
        "default linear method": SETUP + "d = pd.Series([2, 3, 3, 4, 4, 5, 5, 6, 8, 12])\nprint('75th percentile:', np.percentile(d, 75))\nprint('90th percentile:', np.percentile(d, 90))",
    },
    "q2": {
        "means instead of medians": SETUP + "s = pd.Series([62, 58, 75, 81, 66, 93, 70, 59, 88, 64, 120, 72])\nr = pd.Series([120, 88, 64, 81, 88, 88, 62, 93, 81, 120, 72, 64])\nprint('Sample median:', s.mean())\nprint('Resample median:', r.mean())",
    },
    "q3": {
        "5th to 95th percentile": SETUP + "m = pd.Series([63.0, 68.0, 73.5, 72.0, 72.0, 78.0, 75.0, 88.0, 68.0, 73.5, 73.5, 71.0, 81.0, 72.0, 71.0, 78.0, 70.0, 65.0, 68.0, 66.0, 62.0, 66.0, 68.0, 65.0, 64.0, 68.0, 66.0, 70.0, 67.0, 64.0, 81.5, 73.5, 84.5, 70.0, 68.0, 72.5, 71.0, 73.5, 75.5, 68.0])\nprint('95% CI:', np.percentile(m, 5, method='nearest'), 'to', np.percentile(m, 95, method='nearest'))",
    },
    "q4": {
        "80% from 20th to 80th": SETUP + "m = pd.Series([63.0, 68.0, 73.5, 72.0, 72.0, 78.0, 75.0, 88.0, 68.0, 73.5, 73.5, 71.0, 81.0, 72.0, 71.0, 78.0, 70.0, 65.0, 68.0, 66.0, 62.0, 66.0, 68.0, 65.0, 64.0, 68.0, 66.0, 70.0, 67.0, 64.0, 81.5, 73.5, 84.5, 70.0, 68.0, 72.5, 71.0, 73.5, 75.5, 68.0])\nprint('95% width:', np.percentile(m, 97.5, method='nearest') - np.percentile(m, 2.5, method='nearest'))\nprint('80% width:', np.percentile(m, 80, method='nearest') - np.percentile(m, 20, method='nearest'))",
    },
    "q5": {
        "checks the estimate, not the interval": SETUP + "print('95% CI:', 0.52, 'to', 0.625)\nprint('Whole interval above 0.5:', 0.58 > 0.5 and 0.5 > 0.52)",
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


def test_ch11_lab():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
