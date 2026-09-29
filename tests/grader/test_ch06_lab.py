"""Grader test for the Chapter 06 lab (ch06-lab).

Runs every lab question through the server-side runner with the plot checks
defined in _html_extra/api/lib/quiz-app.php:

- the reference solution (lab-answer cell) must pass,
- a student submission (question cell with the solution filled in) must pass,
- the unedited question cell must fail,
- common wrong answers must fail with a hint.

Run with:  .venv/bin/python tests/grader/test_ch06_lab.py   (or pytest)
"""

import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

LAB = ROOT / "chapters" / "06-matplotlib" / "assignments" / "lab.ipynb"
LAB_ID = "ch06-lab"

WRONG_ANSWERS = {
    "q1": {
        "no marker": "fig, ax = plt.subplots()\nax.plot(['Q1','Q2','Q3','Q4'], [120,135,128,150])\nax.set_title('Quarterly Revenue')\nax.set_xlabel('Quarter')\nax.set_ylabel('Revenue ($K)')",
        "axes swapped": "fig, ax = plt.subplots()\nax.plot([120,135,128,150], ['Q1','Q2','Q3','Q4'], marker='o')\nax.set_title('Quarterly Revenue')\nax.set_xlabel('Quarter')\nax.set_ylabel('Revenue ($K)')",
    },
    "q2": {
        "no legend": "fig, ax = plt.subplots()\nax.plot(['Q1','Q2','Q3','Q4'], [120,135,128,150], label='Actual')\nax.plot(['Q1','Q2','Q3','Q4'], [118,130,140,145], ls='--', color='gray', label='Forecast')\nax.set_title('Actual vs Forecast')",
        "styles reversed": "fig, ax = plt.subplots()\nax.plot(['Q1','Q2','Q3','Q4'], [120,135,128,150], ls='--', color='gray', label='Actual')\nax.plot(['Q1','Q2','Q3','Q4'], [118,130,140,145], label='Forecast')\nax.set_title('Actual vs Forecast')\nax.legend()",
    },
    "q3": {
        "default bins": "fig, axes = plt.subplots(1, 2, figsize=(10, 4))\naxes[0].bar(['North','South','East','West'], [150,120,180,90])\naxes[0].set_title('Revenue by Region')\naxes[1].hist([45,52,38,61,75,49,58,66,40,55,70,48])\naxes[1].set_title('Order Values')\nfig.suptitle('Regional Dashboard')",
        "axes title instead of suptitle": "fig, axes = plt.subplots(1, 2, figsize=(10, 4))\naxes[0].bar(['North','South','East','West'], [150,120,180,90])\naxes[0].set_title('Regional Dashboard')\naxes[1].hist([45,52,38,61,75,49,58,66,40,55,70,48], bins=5)\naxes[1].set_title('Order Values')",
    },
    "q4": {
        "line plot": "fig, ax = plt.subplots()\nax.plot([5,10,15,20,25,30,35,40], [60,85,110,120,150,165,190,205], 'o')\nax.set_xlabel('Ad Spend ($K)')\nax.set_ylabel('Sales ($K)')\nax.set_xlim(0, 50)\nax.set_ylim(0, 250)",
        "default limits": "fig, ax = plt.subplots()\nax.scatter([5,10,15,20,25,30,35,40], [60,85,110,120,150,165,190,205])\nax.set_xlabel('Ad Spend ($K)')\nax.set_ylabel('Sales ($K)')",
    },
    "q5": {
        "no savefig": "fig, ax = plt.subplots(figsize=(8, 4))\nax.bar(['North','South','East','West'], [12.5,9.8,14.2,7.6])\nax.set_title('Q2 Margin by Region')\nax.set_ylabel('Margin (%)')",
        "default dpi": "fig, ax = plt.subplots(figsize=(8, 4))\nax.bar(['North','South','East','West'], [12.5,9.8,14.2,7.6])\nax.set_title('Q2 Margin by Region')\nax.set_ylabel('Margin (%)')\nfig.savefig('regional_margin_q2.png')",
    },
}


def collect_results():
    definition = assignment_definition("dsm_lab_definition", LAB_ID)
    checks = definition["plot_checks"]
    questions, solutions = notebook_code_cells(LAB, "lab-answer")
    ids = [f"q{n}" for n in range(1, len(questions) + 1)]
    results = [
        ("definition", "question ids match notebook", sorted(checks) == ids, ""),
        ("definition", "runner profile", definition.get("runner_profile") == "matplotlib", ""),
    ]
    return results + check_questions(ids, questions, solutions, checks, WRONG_ANSWERS)


def test_ch06_lab():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
