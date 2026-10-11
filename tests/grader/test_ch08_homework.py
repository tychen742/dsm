"""Grader test for the Chapter 08 homework (ch08-homework).

Checks the five coding questions (q6-q10) the same way as the lab test:
reference solutions and filled-in submissions pass (pandas profile), unedited questions fail,
and common wrong answers fail with a hint. Also checks that the true/false
answer key covers the notebook's radio-button questions, matches the
solution cells, and keeps a 3:2 or 2:3 balance.

Run with:  .venv/bin/python tests/grader/test_ch08_homework.py   (or pytest)
"""

import json
import re
import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

HOMEWORK = ROOT / "chapters" / "08-prob-stats" / "assignments" / "homework.ipynb"
HOMEWORK_ID = "ch08-homework"

SETUP = "import numpy as np\nimport pandas as pd\n"

WRONG_ANSWERS = {
    "q6": {
        "count instead of rate": SETUP + "o = pd.Series(['No'] * 17 + ['Yes'] * 3)\nprint('Return rate:', (o == 'Yes').sum())\nprint('Kept rate:', (o == 'No').sum())",
    },
    "q7": {
        "count instead of proportion": SETUP + "items = pd.Series([1, 2, 2, 3, 1, 2, 4, 2, 1, 3])\nprint('Proportion with 2 items:', items.value_counts()[2])\nprint('Average items:', items.mean())",
    },
    "q8": {
        "mean instead of median": SETUP + "w = pd.Series([2, 3, 3, 4, 4, 5, 6, 7, 12, 13])\nprint('Median wait:', w.mean())\nprint('90th percentile:', round(np.percentile(w, 90), 1))",
    },
    "q9": {
        "dropped smallest": SETUP + "r = pd.Series([500, 650, 600, 550, 700, 600, 4100])\nw = r[r != r.min()]\nprint('Mean with large order:', r.mean())\nprint('Mean without:', w.mean())\nprint('Median with large order:', r.median())\nprint('Median without:', w.median())",
    },
    "q10": {
        "doubled n": SETUP + "print('SE with n=36:', 12 / np.sqrt(36))\nprint('SE with n=72:', 12 / np.sqrt(72))",
    },
}


def true_false_names():
    notebook = json.loads(HOMEWORK.read_text())
    text = "".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "markdown")
    return sorted(set(re.findall(r'name="ch08-hw-(q\d+)"', text)), key=lambda q: int(q[1:]))


def true_false_solutions():
    """Map q1..q5 to the True/False stated in each question's solution cell."""
    notebook = json.loads(HOMEWORK.read_text())
    cells = notebook["cells"]
    answers = {}
    for index, cell in enumerate(cells[:-1]):
        match = re.search(r'name="ch08-hw-(q\d+)"', "".join(cell["source"]))
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


def test_ch08_homework():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
