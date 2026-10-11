"""Grader test for the Chapter 10 homework (ch10-homework).

Checks the five coding questions (q6-q10) the same way as the lab test:
reference solutions and filled-in submissions pass (pandas profile), unedited questions fail,
and common wrong answers fail with a hint. Also checks that the true/false
answer key covers the notebook's radio-button questions, matches the
solution cells, and keeps a 3:2 or 2:3 balance.

Run with:  .venv/bin/python tests/grader/test_ch10_homework.py   (or pytest)
"""

import json
import re
import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

HOMEWORK = ROOT / "chapters" / "10-two-samples" / "assignments" / "homework.ipynb"
HOMEWORK_ID = "ch10-homework"

SETUP = "import numpy as np\nimport pandas as pd\n"

WRONG_ANSWERS = {
    "q6": {
        "signed difference": SETUP + "b = pd.DataFrame({'segment': ['new'] * 6 + ['returning'] * 6, 'basket': [31, 28, 35, 30, 27, 33, 33, 31, 36, 29, 38, 32]})\nm = b.groupby('segment')['basket'].mean().round(2)\nprint('New:', m['new'])\nprint('Returning:', m['returning'])\nprint('Distance:', round(m['new'] - m['returning'], 2))",
    },
    "q7": {
        "counts instead of rates": SETUP + "c = pd.DataFrame({'plan': ['annual'] * 10 + ['monthly'] * 8, 'churned': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]})\nr = c.groupby('plan')['churned'].sum()\nprint('Annual:', r['annual'])\nprint('Monthly:', r['monthly'])\nprint('Difference:', r['monthly'] - r['annual'])",
    },
    "q8": {
        "strictly greater": SETUP + "s = pd.Series([1.83, 0.5, 0.17, 3.17, 0.83, 0.17, 0.83, 1.17, 0.17, 0.5, 1.17, 0.17, 2.17, 0.17, 2.83, 3.17, 0.17, 1.17, 1.83, 0.83, 0.5, 2.17, 2.17, 0.17, 3.83])\nprint('P-value:', (s > 3.17).mean())\nprint('Decision:', 'do not reject the null')",
    },
    "q9": {
        "absolute lift": SETUP + "print('Rate A:', 0.08)\nprint('Rate B:', 0.1)\nprint('Relative lift:', round((0.1 - 0.08) * 100, 1))",
    },
    "q10": {
        "relief counts": SETUP + "print('Treatment relief:', 12)\nprint('Control relief:', 3)\nprint('Difference:', 9)",
    },
}


def true_false_names():
    notebook = json.loads(HOMEWORK.read_text())
    text = "".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "markdown")
    return sorted(set(re.findall(r'name="ch10-hw-(q\d+)"', text)), key=lambda q: int(q[1:]))


def true_false_solutions():
    """Map q1..q5 to the True/False stated in each question's solution cell."""
    notebook = json.loads(HOMEWORK.read_text())
    cells = notebook["cells"]
    answers = {}
    for index, cell in enumerate(cells[:-1]):
        match = re.search(r'name="ch10-hw-(q\d+)"', "".join(cell["source"]))
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


def test_ch10_homework():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
