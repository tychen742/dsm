"""Grader test for the Chapter 07 lab (ch07-lab).

Runs every lab question through the server-side runner (seaborn profile) with
the plot checks and expected outputs defined in _html_extra/api/lib/quiz-app.php:

- the reference solution (lab-answer cell) must pass,
- a student submission (question cell with the solution filled in) must pass,
- the unedited question cell must fail,
- common wrong answers must fail with a hint.

Run with:  .venv/bin/python tests/grader/test_ch07_lab.py   (or pytest)
"""

import sys

from grader_helpers import ROOT, assignment_definition, check_questions, notebook_code_cells, report

LAB = ROOT / "chapters" / "07-seaborn" / "assignments" / "lab.ipynb"
LAB_ID = "ch07-lab"

SETUP = "import matplotlib.pyplot as plt\nimport pandas as pd\nimport seaborn as sns\n"
ORDERS = "orders = pd.DataFrame({'order_value': [45, 52, 38, 61, 75, 49, 58, 66, 40, 55, 70, 48]})\n"
CAMPAIGNS = (
    "campaigns = pd.DataFrame({'ad_spend': [5, 10, 15, 20, 25, 30, 35, 40], "
    "'revenue': [60, 70, 110, 105, 150, 140, 190, 170], 'region': ['North', 'South'] * 4})\n"
)
SALES = (
    "sales = pd.DataFrame({'quarter': ['Q1', 'Q2', 'Q3', 'Q4'], "
    "'North': [150, 165, 158, 180], 'South': [120, 118, 135, 142]})\n"
)
DELIVERIES = (
    "deliveries = pd.DataFrame({'method': ['Standard'] * 5 + ['Express'] * 5 + ['Overnight'] * 5, "
    "'days': [5, 6, 5, 7, 6, 2, 4, 3, 5, 2, 1, 1, 2, 1, 1]})\n"
)
PROMO = (
    "promo = pd.DataFrame({'discount': [5, 10, 15, 20] * 3, "
    "'units': [40, 52, 61, 75, 38, 41, 45, 47, 30, 45, 58, 70], "
    "'region': ['East'] * 4 + ['West'] * 4 + ['North'] * 4})\n"
)

WRONG_ANSWERS = {
    "q1": {
        "default bins": SETUP + ORDERS + "fig, ax = plt.subplots()\nsns.histplot(data=orders, x='order_value', ax=ax)\nax.set_title('Order Values')",
        "matplotlib hist": SETUP + ORDERS + "fig, ax = plt.subplots()\nax.hist(orders['order_value'], bins=5)\nax.set_title('Order Values')",
    },
    "q2": {
        "no hue": SETUP + CAMPAIGNS + "fig, ax = plt.subplots()\nsns.scatterplot(data=campaigns, x='ad_spend', y='revenue', ax=ax)\nax.set_title('Ad Spend vs Revenue')",
        "axes swapped": SETUP + CAMPAIGNS + "fig, ax = plt.subplots()\nsns.scatterplot(data=campaigns, x='revenue', y='ad_spend', hue='region', ax=ax)\nax.set_title('Ad Spend vs Revenue')",
    },
    "q3": {
        "wide data, no hue": SETUP + SALES + "tidy = sales.melt(id_vars='quarter', var_name='region', value_name='revenue')\nprint('Tidy rows:', len(tidy))\nfig, ax = plt.subplots()\nsns.barplot(data=sales, x='quarter', y='North', ax=ax)",
        "no hue": SETUP + SALES + "tidy = sales.melt(id_vars='quarter', var_name='region', value_name='revenue')\nprint('Tidy rows:', len(tidy))\nfig, ax = plt.subplots()\nsns.barplot(data=tidy, x='quarter', y='revenue', ax=ax)",
        "missing row count": SETUP + SALES + "tidy = sales.melt(id_vars='quarter', var_name='region', value_name='revenue')\nfig, ax = plt.subplots()\nsns.barplot(data=tidy, x='quarter', y='revenue', hue='region', ax=ax)",
    },
    "q4": {
        "bar plot": SETUP + DELIVERIES + "fig, ax = plt.subplots()\nsns.barplot(data=deliveries, x='method', y='days', ax=ax)\nax.set_title('Delivery Days by Method')\nprint('Fastest median:', deliveries.groupby('method')['days'].median().idxmin())",
        "slowest instead": SETUP + DELIVERIES + "fig, ax = plt.subplots()\nsns.boxplot(data=deliveries, x='method', y='days', ax=ax)\nax.set_title('Delivery Days by Method')\nprint('Fastest median:', deliveries.groupby('method')['days'].median().idxmax())",
    },
    "q5": {
        "single axes": SETUP + PROMO + "fig, ax = plt.subplots()\nsns.scatterplot(data=promo, x='discount', y='units', hue='region', ax=ax)",
        "hue instead of col": SETUP + PROMO + "sns.relplot(data=promo, x='discount', y='units', hue='region', height=3)",
        "default height": SETUP + PROMO + "sns.relplot(data=promo, x='discount', y='units', col='region')",
    },
}


def collect_results():
    definition = assignment_definition("dsm_lab_definition", LAB_ID)
    checks = definition["plot_checks"]
    outputs = definition.get("code_outputs", {})
    questions, solutions = notebook_code_cells(LAB, "lab-answer")
    ids = [f"q{n}" for n in range(1, len(questions) + 1)]
    results = [
        ("definition", "question ids match notebook", sorted(checks) == ids, ""),
        ("definition", "runner profile", definition.get("runner_profile") == "seaborn", ""),
        ("definition", "output ids are question ids", set(outputs) <= set(ids), ""),
    ]
    return results + check_questions(ids, questions, solutions, checks, WRONG_ANSWERS, "seaborn", outputs)


def test_ch07_lab():
    failures = [r for r in collect_results() if not r[2]]
    assert not failures, failures


if __name__ == "__main__":
    sys.exit(report(collect_results()))
