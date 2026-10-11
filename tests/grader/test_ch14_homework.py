"""Grader test for the Chapter 14 homework (ch14-homework).

Checks the five coding questions (q6-q10) the same way as the lab test:
reference solutions and filled-in submissions pass (pandas profile), unedited questions fail,
and common wrong answers fail with a hint. Also checks that the true/false
answer key covers the notebook's radio-button questions, matches the
solution cells, and keeps a 3:2 or 2:3 balance.

Run with:  .venv/bin/python tests/grader/test_ch14_homework.py   (or pytest)
"""

import json
import re
import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

HOMEWORK = ROOT / "chapters" / "14-classification" / "assignments" / "homework.ipynb"
HOMEWORK_ID = "ch14-homework"

SETUP = "import numpy as np\nimport pandas as pd\n"

L = "loans = pd.DataFrame({'income_su': [1.2, 0.8, -0.3, -1.1, 0.4, -0.9, 1.5, -0.2, 0.1, -1.4], 'debt_su': [-0.9, -0.4, 0.6, 1.3, -0.1, 0.9, -1.2, 1.0, 0.3, 0.2], 'outcome': ['repaid', 'repaid', 'default', 'default', 'repaid', 'default', 'repaid', 'default', 'repaid', 'default']})\n"

WRONG_ANSWERS = {
    "q6": {
        "squared distance": SETUP + "print('Distance:', 2.0)",
    },
    "q7": {
        "k = 1": SETUP + "print('Nearest labels:', ['renew'])\nprint('Prediction:', 'renew')",
    },
    "q8": {
        "test set's own mean and SD": SETUP + "t = pd.Series([35, 55, 70])\nprint('Scaled test spend:', ((t - np.mean(t)) / np.std(t)).round(2).tolist())",
    },
    "q9": {
        "ignores the baseline": SETUP + "print('Accuracy:', 0.9)\nprint('Always-ok accuracy:', 0.0)\nprint('Fraud caught:', 1, 'of', 2)",
    },
    "q10": {
        "picks the largest k": SETUP + "print('k1:', 0.625)\nprint('k3:', 0.875)\nprint('k5:', 0.625)\nprint('Best:', 'k5')",
    },
}


def true_false_names():
    notebook = json.loads(HOMEWORK.read_text())
    text = "".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "markdown")
    return sorted(set(re.findall(r'name="ch14-hw-(q\d+)"', text)), key=lambda q: int(q[1:]))


def true_false_solutions():
    """Map q1..q5 to the True/False stated in each question's solution cell."""
    notebook = json.loads(HOMEWORK.read_text())
    cells = notebook["cells"]
    answers = {}
    for index, cell in enumerate(cells[:-1]):
        match = re.search(r'name="ch14-hw-(q\d+)"', "".join(cell["source"]))
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


def test_ch14_homework():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
