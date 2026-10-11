"""Grader test for the Chapter 15 homework (ch15-homework).

Checks the five coding questions (q6-q10) the same way as the lab test:
reference solutions and filled-in submissions pass (sklearn profile), unedited questions fail,
and common wrong answers fail with a hint. Also checks that the true/false
answer key covers the notebook's radio-button questions, matches the
solution cells, and keeps a 3:2 or 2:3 balance.

Run with:  .venv/bin/python tests/grader/test_ch15_homework.py   (or pytest)
"""

import json
import re
import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

HOMEWORK = ROOT / "chapters" / "15-clustering" / "assignments" / "homework.ipynb"
HOMEWORK_ID = "ch15-homework"

SETUP = "import numpy as np\nimport pandas as pd\n"

C = "customers = pd.DataFrame({'spend': [300, 650, 450, 800, 500, 900, 700, 1100, 2000, 2500, 2900, 2300, 2100, 2700, 3000, 2400], 'orders': [3, 2, 4, 3, 24, 22, 26, 25, 5, 4, 6, 5, 28, 26, 30, 27]})\nscaled = (customers - customers.mean()) / customers.std(ddof=0)\n"
K = "from sklearn.cluster import KMeans\nfrom sklearn.metrics import silhouette_score\n"
ST = "stores = pd.DataFrame({'traffic_su': [-1.2, -1.0, -1.3, -0.9, 0.1, 0.3, 0.0, 0.2, 1.3, 1.1, 1.4, 1.2], 'basket_su': [1.1, 0.9, 1.2, 1.0, -1.0, -1.2, -0.9, -1.1, 0.2, 0.0, 0.3, 0.1]})\n"

WRONG_ANSWERS = {
    "q6": {
        "ties to the wrong center": SETUP + "print('Assignments:', [0, 0, 1, 1, 1, 1, 1])\nprint('Sizes:', [2, 5])",
    },
    "q7": {
        "distances not squared": SETUP + "print('Centers:', [[1.5, 1.5], [9.0, 8.0]])\nprint('Inertia:', 2.83)",
    },
    "q8": {
        "k = 4": SETUP + K + ST + "l = KMeans(n_clusters=4, n_init=10, random_state=0).fit_predict(stores)\nprint('Cluster sizes:', sorted(pd.Series(l).value_counts().tolist()))",
    },
    "q9": {
        "picks the largest k": SETUP + "print('k=2:', 0.682)\nprint('k=3:', 0.864)\nprint('k=4:', 0.773)\nprint('Best k:', 4)",
    },
    "q10": {
        "highest spend instead of visits": SETUP + "print('Most frequent visitors: cluster', 0)\nprint('Their mean spend:', 120.0)\nprint('Customers:', 3)",
    },
}


def true_false_names():
    notebook = json.loads(HOMEWORK.read_text())
    text = "".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "markdown")
    return sorted(set(re.findall(r'name="ch15-hw-(q\d+)"', text)), key=lambda q: int(q[1:]))


def true_false_solutions():
    """Map q1..q5 to the True/False stated in each question's solution cell."""
    notebook = json.loads(HOMEWORK.read_text())
    cells = notebook["cells"]
    answers = {}
    for index, cell in enumerate(cells[:-1]):
        match = re.search(r'name="ch15-hw-(q\d+)"', "".join(cell["source"]))
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


def test_ch15_homework():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
