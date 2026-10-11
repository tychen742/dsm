"""Grader test for the Chapter 13 homework (ch13-homework).

Checks the five coding questions (q6-q10) the same way as the lab test:
reference solutions and filled-in submissions pass (sklearn profile), unedited questions fail,
and common wrong answers fail with a hint. Also checks that the true/false
answer key covers the notebook's radio-button questions, matches the
solution cells, and keeps a 3:2 or 2:3 balance.

Run with:  .venv/bin/python tests/grader/test_ch13_homework.py   (or pytest)
"""

import json
import re
import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

HOMEWORK = ROOT / "chapters" / "13-multiple-regression" / "assignments" / "homework.ipynb"
HOMEWORK_ID = "ch13-homework"

SETUP = "import numpy as np\nimport pandas as pd\n"

LR = "from sklearn.linear_model import LinearRegression\n"
SP = "from sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_squared_error, r2_score\n"
H = "homes = pd.DataFrame({'sqft': [2800, 2700, 2600, 2700, 1300, 2600, 2800, 1600, 1500, 1300, 2600, 2900, 2200, 2300, 2600, 1200], 'rooms': [9, 9, 8, 9, 5, 8, 9, 6, 6, 3, 9, 9, 7, 9, 9, 4], 'age': [44, 26, 42, 7, 45, 41, 27, 25, 17, 13, 15, 39, 20, 49, 20, 27], 'price': [400, 417, 350, 450, 151, 363, 390, 247, 259, 198, 403, 387, 326, 325, 409, 168]})\n"

WRONG_ANSWERS = {
    "q6": {
        "sqft-only model": SETUP + LR + H + "l = pd.DataFrame({'sqft': [1500, 2200, 1900]})\nm = LinearRegression().fit(homes[['sqft']], homes['price'])\nfor n, v in enumerate(m.predict(l), 1):\n    print('Listing ' + str(n) + ':', round(v, 1))",
    },
    "q7": {
        "predicted minus actual": SETUP + "print('Residuals:', [5, -10, 5, -15, 7, 5])\nprint('Test RMSE:', 8.65)",
    },
    "q8": {
        "single nearest neighbor": SETUP + "print('Predicted price:', 300.0)",
    },
    "q9": {
        "threshold not applied": SETUP + "print('Correlation:', 0.83)\nprint('Multicollinearity flag:', False)",
    },
    "q10": {
        "chose by training RMSE": SETUP + "print('Best model:', 'C')\nprint('Gap for C:', 12.5)",
    },
}


def true_false_names():
    notebook = json.loads(HOMEWORK.read_text())
    text = "".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "markdown")
    return sorted(set(re.findall(r'name="ch13-hw-(q\d+)"', text)), key=lambda q: int(q[1:]))


def true_false_solutions():
    """Map q1..q5 to the True/False stated in each question's solution cell."""
    notebook = json.loads(HOMEWORK.read_text())
    cells = notebook["cells"]
    answers = {}
    for index, cell in enumerate(cells[:-1]):
        match = re.search(r'name="ch13-hw-(q\d+)"', "".join(cell["source"]))
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
        ("definition", "runner profile", definition.get("runner_profile") == "sklearn", ""),
        ("definition", "true/false ids match notebook", sorted(definition.get("true_false", {})) == tf_ids, ""),
        ("definition", "true/false key matches solution cells", definition.get("true_false") == true_false_solutions(), ""),
    ]
    key = definition.get("true_false", {})
    true_count = sum(1 for value in key.values() if value)
    results.append(("definition", "true/false balance is 3:2 or 2:3", true_count in (2, 3), f"{true_count} true"))
    return results + check_questions(ids, questions, solutions, checks, WRONG_ANSWERS, "sklearn", outputs)


def test_ch13_homework():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
