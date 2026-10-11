"""Grader test for the Chapter 09 homework (ch09-homework).

Checks the five coding questions (q6-q10) the same way as the lab test:
reference solutions and filled-in submissions pass (pandas profile), unedited questions fail,
and common wrong answers fail with a hint. Also checks that the true/false
answer key covers the notebook's radio-button questions, matches the
solution cells, and keeps a 3:2 or 2:3 balance.

Run with:  .venv/bin/python tests/grader/test_ch09_homework.py   (or pytest)
"""

import json
import re
import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

HOMEWORK = ROOT / "chapters" / "09-test-hypothesis" / "assignments" / "homework.ipynb"
HOMEWORK_ID = "ch09-homework"

SETUP = "import numpy as np\nimport pandas as pd\n"

WRONG_ANSWERS = {
    "q6": {
        "proportion instead of percent": SETUP + "print('Observed percent:', round(42 / 600, 2))\nprint('Test statistic:', round(abs(42 / 600 - 5), 2))",
    },
    "q7": {
        "not halved": SETUP + "a = pd.Series([0.40, 0.25, 0.30, 0.05])\nb = pd.Series([0.42, 0.31, 0.22, 0.05])\nprint('TVD:', round((b - a).abs().sum(), 2))",
    },
    "q8": {
        "count instead of proportion": SETUP + "s = pd.Series([0.0, 1.2, 0.2, 0.8, 1.1, 0.2, 0.8, 2.1, 1.3, 1.2, 0.3, 0.7, 0.3, 1.1, 0.9, 0.4, 1.1, 1.1, 0.1, 0.7, 0.4, 0.4, 1.6, 2.6, 0.2])\nprint('P-value:', (s >= 2.0).sum())",
    },
    "q9": {
        "reversed rule": SETUP + "for c in [0.05, 0.1]:\n    if 0.08 > c:\n        print('At ' + str(c) + ':', 'reject')\n    else:\n        print('At ' + str(c) + ':', 'do not reject')",
    },
    "q10": {
        "90th percentile": SETUP + "s = pd.Series([0.037, 0.028, 0.044, 0.051, 0.065, 0.050, 0.062, 0.010, 0.031, 0.025, 0.054, 0.061, 0.013, 0.046, 0.068, 0.073, 0.022, 0.064, 0.058, 0.039])\nc = round(np.percentile(s, 90), 3)\nprint('95th percentile:', c)\nprint('Observed is above it:', 0.071 > c)",
    },
}


def true_false_names():
    notebook = json.loads(HOMEWORK.read_text())
    text = "".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "markdown")
    return sorted(set(re.findall(r'name="ch09-hw-(q\d+)"', text)), key=lambda q: int(q[1:]))


def true_false_solutions():
    """Map q1..q5 to the True/False stated in each question's solution cell."""
    notebook = json.loads(HOMEWORK.read_text())
    cells = notebook["cells"]
    answers = {}
    for index, cell in enumerate(cells[:-1]):
        match = re.search(r'name="ch09-hw-(q\d+)"', "".join(cell["source"]))
        if cell["cell_type"] == "markdown" and match:
            solution = "".join(cells[index + 1]["source"])
            stated = re.search(r"^# (True|False)$", solution, re.MULTILINE)
            answers[match.group(1)] = stated.group(1) == "True" if stated else None
    return answers


def collect_results():
    definition = assignment_definition("dsm_homework_definition", HOMEWORK_ID)
    checks = {}
    outputs = definition["code_outputs"]
    questions, solutions = notebook_code_cells(HOMEWORK, "homework-answer")
    ids = [f"q{n}" for n in range(6, 6 + len(questions))]
    tf_ids = true_false_names()
    results = [
        ("definition", "coding ids match notebook", sorted(outputs, key=lambda q: int(q[1:])) == ids, ""),
        ("definition", "runner profile", definition.get("runner_profile") == "pandas", ""),
        ("definition", "true/false ids match notebook", sorted(definition.get("true_false", {})) == tf_ids, ""),
        ("definition", "true/false key matches solution cells", definition.get("true_false") == true_false_solutions(), ""),
    ]
    key = definition.get("true_false", {})
    true_count = sum(1 for value in key.values() if value)
    results.append(("definition", "true/false balance is 3:2 or 2:3", true_count in (2, 3), f"{true_count} true"))
    return results + check_questions(ids, questions, solutions, checks, WRONG_ANSWERS, "pandas", outputs)


def test_ch09_homework():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
