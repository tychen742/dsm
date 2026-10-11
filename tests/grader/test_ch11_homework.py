"""Grader test for the Chapter 11 homework (ch11-homework).

Checks the five coding questions (q6-q10) the same way as the lab test:
reference solutions and filled-in submissions pass (pandas profile), unedited questions fail,
and common wrong answers fail with a hint. Also checks that the true/false
answer key covers the notebook's radio-button questions, matches the
solution cells, and keeps a 3:2 or 2:3 balance.

Run with:  .venv/bin/python tests/grader/test_ch11_homework.py   (or pytest)
"""

import json
import re
import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

HOMEWORK = ROOT / "chapters" / "11-estimation" / "assignments" / "homework.ipynb"
HOMEWORK_ID = "ch11-homework"

SETUP = "import numpy as np\nimport pandas as pd\n"

WRONG_ANSWERS = {
    "q6": {
        "mean instead of median": SETUP + "o = pd.Series([38, 52, 45, 61, 47, 55, 40, 49, 58, 44, 51, 46, 63, 42, 50])\nprint('25th percentile:', np.percentile(o, 25, method='nearest'))\nprint('Median:', o.mean())\nprint('75th percentile:', np.percentile(o, 75, method='nearest'))",
    },
    "q7": {
        "original sample instead of resample": SETUP + "o = pd.Series([38, 52, 45, 61, 47, 55, 40, 49, 58, 44, 51, 46, 63, 42, 50])\nprint('Resample mean:', round(o.mean(), 2))\nprint('Distinct values:', o.nunique(), 'of', len(o))",
    },
    "q8": {
        "min to max": SETUP + "print('95% CI:', 44.4, 'to', 53.33)",
    },
    "q9": {
        "ratio reversed": SETUP + "print('Width A:', 0.18)\nprint('Width B:', 0.09)\nprint('Ratio:', round(0.09 / 0.18, 1))",
    },
    "q10": {
        "compares the estimate": SETUP + "print('95% CI:', 0.033, 'to', 0.083)\nprint('Claim inside interval:', 0.06 == 0.05)",
    },
}


def true_false_names():
    notebook = json.loads(HOMEWORK.read_text())
    text = "".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "markdown")
    return sorted(set(re.findall(r'name="ch11-hw-(q\d+)"', text)), key=lambda q: int(q[1:]))


def true_false_solutions():
    """Map q1..q5 to the True/False stated in each question's solution cell."""
    notebook = json.loads(HOMEWORK.read_text())
    cells = notebook["cells"]
    answers = {}
    for index, cell in enumerate(cells[:-1]):
        match = re.search(r'name="ch11-hw-(q\d+)"', "".join(cell["source"]))
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


def test_ch11_homework():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
