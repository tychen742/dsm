"""Grader test for the Chapter 06 homework (ch06-homework).

Checks the five coding questions (q6-q10) the same way as the lab test:
reference solutions and filled-in submissions pass, unedited questions fail,
and common wrong answers fail with a hint. Also checks that the true/false
answer key covers the notebook's radio-button questions, matches the
solution cells, and keeps a 3:2 or 2:3 balance.

Run with:  .venv/bin/python tests/grader/test_ch06_homework.py   (or pytest)
"""

import json
import re
import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

HOMEWORK = ROOT / "chapters" / "06-matplotlib" / "assignments" / "homework.ipynb"
HOMEWORK_ID = "ch06-homework"

WRONG_ANSWERS = {
    "q6": {
        "default width": "fig, ax = plt.subplots()\nax.plot(['Jan','Feb','Mar','Apr','May','Jun'], [132,128,145,151,139,160], marker='s', label='Sales')\nax.plot(['Jan','Feb','Mar','Apr','May','Jun'], [140]*6, color='red', ls=':', label='Target')\nax.set_ylabel('Units Sold')\nax.legend()",
        "dashed target": "fig, ax = plt.subplots()\nax.plot(['Jan','Feb','Mar','Apr','May','Jun'], [132,128,145,151,139,160], lw=2.5, marker='s', label='Sales')\nax.plot(['Jan','Feb','Mar','Apr','May','Jun'], [140]*6, 'r--', label='Target')\nax.set_ylabel('Units Sold')\nax.legend()",
    },
    "q7": {
        "no alpha": "fig, ax = plt.subplots()\nax.hist([42,48,51,45,39,55,47,50,44,53,46,49], bins=6, label='Store A')\nax.hist([58,62,55,66,60,71,57,64,59,68,61,63], bins=6, label='Store B')\nax.set_xlabel('Daily Orders')\nax.legend()",
        "two axes": "fig, axes = plt.subplots(1, 2)\naxes[0].hist([42,48,51,45,39,55,47,50,44,53,46,49], bins=6, alpha=0.5, label='Store A')\naxes[1].hist([58,62,55,66,60,71,57,64,59,68,61,63], bins=6, alpha=0.5, label='Store B')\naxes[0].set_xlabel('Daily Orders')\naxes[0].legend()",
    },
    "q8": {
        "inset shows full year": "fig = plt.figure(figsize=(6, 4))\nm = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']\nr = [110,104,118,121,125,119,130,128,135,150,168,190]\na = fig.add_axes([0.1, 0.1, 0.8, 0.8])\na.plot(m, r)\na.set_title('Monthly Revenue')\nb = fig.add_axes([0.2, 0.5, 0.3, 0.3])\nb.plot(m, r)\nb.set_title('Q4')",
        "first three months": "fig = plt.figure(figsize=(6, 4))\nm = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']\nr = [110,104,118,121,125,119,130,128,135,150,168,190]\na = fig.add_axes([0.1, 0.1, 0.8, 0.8])\na.plot(m, r)\na.set_title('Monthly Revenue')\nb = fig.add_axes([0.2, 0.5, 0.3, 0.3])\nb.plot(m[:3], r[:3])\nb.set_title('Q4')",
        "subplots instead": "fig, axes = plt.subplots(1, 2, figsize=(6, 4))\nm = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']\nr = [110,104,118,121,125,119,130,128,135,150,168,190]\naxes[0].plot(m, r)\naxes[0].set_title('Monthly Revenue')\naxes[1].plot(m[-3:], r[-3:])\naxes[1].set_title('Q4')",
    },
    "q9": {
        "no sharey": "fig, axes = plt.subplots(1, 3, figsize=(12, 3))\nfor ax, name, values in zip(axes, ['North','South','West'], [[150,162,158,171],[120,118,131,127],[60,64,59,70]]):\n    ax.bar(['Q1','Q2','Q3','Q4'], values)\n    ax.set_title(name)",
        "same data everywhere": "fig, axes = plt.subplots(1, 3, figsize=(12, 3), sharey=True)\nfor ax, name in zip(axes, ['North','South','West']):\n    ax.bar(['Q1','Q2','Q3','Q4'], [150,162,158,171])\n    ax.set_title(name)",
    },
    "q10": {
        "no ylim": "df = pd.DataFrame({'Online': [82,90,97,105,118,126], 'In-Store': [140,136,131,129,124,120]}, index=['Jan','Feb','Mar','Apr','May','Jun'])\nfig, ax = plt.subplots()\ndf.plot(ax=ax)\nax.set_title('Sales by Channel')\nax.set_ylabel('Revenue ($K)')",
        "one column": "df = pd.DataFrame({'Online': [82,90,97,105,118,126], 'In-Store': [140,136,131,129,124,120]}, index=['Jan','Feb','Mar','Apr','May','Jun'])\nfig, ax = plt.subplots()\ndf['Online'].plot(ax=ax, legend=True)\nax.set_title('Sales by Channel')\nax.set_ylabel('Revenue ($K)')\nax.set_ylim(0, 200)",
    },
}


def true_false_names():
    notebook = json.loads(HOMEWORK.read_text())
    text = "".join("".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "markdown")
    return sorted(set(re.findall(r'name="ch06-hw-(q\d+)"', text)), key=lambda q: int(q[1:]))


def true_false_solutions():
    """Map q1..q5 to the True/False stated in each question's solution cell."""
    notebook = json.loads(HOMEWORK.read_text())
    cells = notebook["cells"]
    answers = {}
    for index, cell in enumerate(cells[:-1]):
        match = re.search(r'name="ch06-hw-(q\d+)"', "".join(cell["source"]))
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
        ("definition", "runner profile", definition.get("runner_profile") == "matplotlib", ""),
        ("definition", "true/false ids match notebook", sorted(definition.get("true_false", {})) == tf_ids, ""),
        ("definition", "true/false key matches solution cells", definition.get("true_false") == true_false_solutions(), ""),
    ]
    key = definition.get("true_false", {})
    true_count = sum(1 for value in key.values() if value)
    results.append(("definition", "true/false balance is 3:2 or 2:3", true_count in (2, 3), f"{true_count} true"))
    return results + check_questions(ids, questions, solutions, checks, WRONG_ANSWERS)


def test_ch06_homework():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
