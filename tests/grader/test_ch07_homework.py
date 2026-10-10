"""Grader test for the Chapter 07 homework (ch07-homework).

Checks the five coding questions (q6-q10) the same way as the lab test:
reference solutions and filled-in submissions pass (seaborn profile), unedited questions fail,
and common wrong answers fail with a hint. Also checks that the true/false
answer key covers the notebook's radio-button questions, matches the
solution cells, and keeps a 3:2 or 2:3 balance.

Run with:  .venv/bin/python tests/grader/test_ch07_homework.py   (or pytest)
"""

import json
import re
import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

HOMEWORK = ROOT / "chapters" / "07-seaborn" / "assignments" / "homework.ipynb"
HOMEWORK_ID = "ch07-homework"

SETUP = "import matplotlib.pyplot as plt\nimport pandas as pd\nimport seaborn as sns\n"
CHANNELS = (
    "orders = pd.DataFrame({'channel': ['Online', 'Retail', 'Online', 'Phone', 'Online', "
    "'Retail', 'Online', 'Phone', 'Retail', 'Online']})\n"
)
CUSTOMERS = (
    "customers = pd.DataFrame({'spend': [22, 35, 28, 40, 31, 26, 55, 62, 48, 70, 58, 66], "
    "'segment': ['New'] * 6 + ['Returning'] * 6})\n"
)
MONTHLY = (
    "monthly = pd.DataFrame({'month': [1, 2, 3, 4, 5, 6] * 2, "
    "'revenue': [120, 128, 135, 131, 142, 150, 98, 104, 101, 110, 118, 125], "
    "'region': ['North'] * 6 + ['South'] * 6})\n"
)
METRICS = (
    "metrics = pd.DataFrame({'ad_spend': [5, 10, 15, 20, 25, 30], "
    "'visits': [210, 300, 250, 380, 330, 450], 'returns': [12, 9, 11, 8, 10, 9]})\n"
)
ORDERS = (
    "orders = pd.DataFrame({'order_value': [45, 52, 38, 61, 75, 49, 58, 66, 40, 55, 70, 48], "
    "'channel': ['Online', 'Retail'] * 6})\n"
)

WRONG_ANSWERS = {
    "q6": {
        "horizontal (y instead of x)": SETUP + CHANNELS + "fig, ax = plt.subplots()\nsns.countplot(data=orders, y='channel', ax=ax)\nax.set_title('Orders by Channel')",
        "no title": SETUP + CHANNELS + "fig, ax = plt.subplots()\nsns.countplot(data=orders, x='channel', ax=ax)",
    },
    "q7": {
        "no hue": SETUP + CUSTOMERS + "fig, ax = plt.subplots()\nsns.kdeplot(data=customers, x='spend', ax=ax)\nax.set_title('Spend by Segment')",
        "histogram": SETUP + CUSTOMERS + "fig, ax = plt.subplots()\nsns.histplot(data=customers, x='spend', hue='segment', ax=ax)\nax.set_title('Spend by Segment')",
    },
    "q8": {
        "no markers": SETUP + MONTHLY + "fig, ax = plt.subplots()\nsns.lineplot(data=monthly, x='month', y='revenue', hue='region', ax=ax)\nax.set_title('Monthly Revenue')",
        "no hue": SETUP + MONTHLY + "fig, ax = plt.subplots()\nsns.lineplot(data=monthly, x='month', y='revenue', marker='o', ax=ax)\nax.set_title('Monthly Revenue')",
    },
    "q9": {
        "no annotations": SETUP + METRICS + "corr = metrics.corr()\nfig, ax = plt.subplots()\nsns.heatmap(corr, cmap='Blues', vmin=-1, vmax=1, ax=ax)\nax.set_title('Metric Correlations')",
        "default color range": SETUP + METRICS + "corr = metrics.corr()\nfig, ax = plt.subplots()\nsns.heatmap(corr, annot=True, cmap='Blues', ax=ax)\nax.set_title('Metric Correlations')",
        "raw data instead of corr": SETUP + METRICS + "fig, ax = plt.subplots()\nsns.heatmap(metrics, annot=True, cmap='Blues', vmin=-1, vmax=1, ax=ax)\nax.set_title('Metric Correlations')",
    },
    "q10": {
        "hue instead of col": SETUP + ORDERS + "sns.displot(data=orders, x='order_value', hue='channel', bins=4, height=3)",
        "default bins": SETUP + ORDERS + "sns.displot(data=orders, x='order_value', col='channel', height=3)",
    },
}


def true_false_names():
    notebook = json.loads(HOMEWORK.read_text())
    text = "".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "markdown")
    return sorted(set(re.findall(r'name="ch07-hw-(q\d+)"', text)), key=lambda q: int(q[1:]))


def true_false_solutions():
    """Map q1..q5 to the True/False stated in each question's solution cell."""
    notebook = json.loads(HOMEWORK.read_text())
    cells = notebook["cells"]
    answers = {}
    for index, cell in enumerate(cells[:-1]):
        match = re.search(r'name="ch07-hw-(q\d+)"', "".join(cell["source"]))
        if cell["cell_type"] == "markdown" and match:
            solution = "".join(cells[index + 1]["source"])
            stated = re.search(r"^# (True|False)$", solution, re.MULTILINE)
            answers[match.group(1)] = stated.group(1) == "True" if stated else None
    return answers


def collect_results():
    definition = assignment_definition("dsm_homework_definition", HOMEWORK_ID)
    checks = definition["plot_checks"]
    questions, solutions = notebook_code_cells(HOMEWORK, "homework-answer")
    ids = [f"q{n}" for n in range(6, 6 + len(questions))]
    tf_ids = true_false_names()
    results = [
        ("definition", "coding ids match notebook", sorted(checks, key=lambda q: int(q[1:])) == ids, ""),
        ("definition", "runner profile", definition.get("runner_profile") == "seaborn", ""),
        ("definition", "true/false ids match notebook", sorted(definition.get("true_false", {})) == tf_ids, ""),
        ("definition", "true/false key matches solution cells", definition.get("true_false") == true_false_solutions(), ""),
    ]
    key = definition.get("true_false", {})
    true_count = sum(1 for value in key.values() if value)
    results.append(("definition", "true/false balance is 3:2 or 2:3", true_count in (2, 3), f"{true_count} true"))
    return results + check_questions(ids, questions, solutions, checks, WRONG_ANSWERS, "seaborn")


def test_ch07_homework():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
